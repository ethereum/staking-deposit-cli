from dataclasses import (
    asdict,
    dataclass,
    fields,
    field as dataclass_field
)
import json
import os
from py_ecc.bls import G2ProofOfPossession as bls
from secrets import randbits
from typing import Any, Dict, Union
from unicodedata import normalize
from uuid import uuid4

from staking_deposit.utils.crypto import (
    AES_128_CTR,
    PBKDF2,
    scrypt,
    SHA256,
)
from staking_deposit.utils.constants import (
    UNICODE_CONTROL_CHARS,
)

hexdigits = set('0123456789abcdef')


def encode_bytes(obj: Union[str, Dict[str, Any]]) -> Union[bytes, str, Dict[str, Any]]:
    """
    Recursively encodes objects that contain hexstrings into objects that contain bytes.
    """
    if isinstance(obj, str) and all(c in hexdigits for c in obj):
        return bytes.fromhex(obj)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = encode_bytes(value)
    return obj


class BytesDataclass:
    """
    BytesDataClasses are DataClass objects that automatically encode hexstrings into bytes,
    and have an `as_json` function that encodes bytes back into hexstrings.
    """
    def __post_init__(self) -> None:
        for field in fields(self):
            if field.type in (bytes, Dict[str, Any]):
                # Convert hexstring to bytes
                self.__setattr__(field.name, encode_bytes(self.__getattribute__(field.name)))

    def as_json(self) -> str:
        return json.dumps(asdict(self), default=lambda x: x.hex())


@dataclass
class KeystoreModule(BytesDataclass):
    function: str = ''
    params: Dict[str, Any] = dataclass_field(default_factory=dict)
    message: bytes = bytes()


@dataclass
class KeystoreCrypto(BytesDataclass):
    kdf: KeystoreModule = KeystoreModule()
    checksum: KeystoreModule = KeystoreModule()
    cipher: KeystoreModule = KeystoreModule()

    @classmethod
    def from_json(cls, json_dict: Dict[Any, Any]) -> 'KeystoreCrypto':
        kdf = KeystoreModule(**json_dict['kdf'])
        checksum = KeystoreModule(**json_dict['checksum'])
        cipher = KeystoreModule(**json_dict['cipher'])
        return cls(kdf=kdf, checksum=checksum, cipher=cipher)


@dataclass
class Keystore(BytesDataclass):
    """
    Implement an EIP 2335-compliant keystore. A keystore is a JSON file that
    stores an encrypted version of a private key under a user-supplied password.

    Ref: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2335.md
    """
    crypto: KeystoreCrypto = KeystoreCrypto()
    description: str = ''
    pubkey: str = ''
    path: str = ''
    uuid: str = ''
    version: int = 4

    def kdf(self, **kwargs: Any) -> bytes:
        return scrypt(**kwargs) if 'scrypt' in self.crypto.kdf.function else PBKDF2(**kwargs)

    def save(self, filefolder: str) -> None:
        """
        Save self as a JSON keystore.
        """
        with open(filefolder, 'w') as f:
            f.write(self.as_json())
        if os.name == 'posix':
            os.chmod(filefolder, int('440', 8))  # Read for owner & group

    @classmethod
    def from_json(cls, json_dict: Dict[Any, Any]) -> 'Keystore':
        crypto = KeystoreCrypto.from_json(json_dict['crypto'])
        path = json_dict['path']
        uuid = json_dict['uuid']
        version = json_dict['version']
        description = json_dict.get('description', '')
        pubkey = json_dict.get('pubkey', '')
        return cls(crypto=crypto, description=description, pubkey=pubkey, path=path, uuid=uuid, version=version)

    @classmethod
    def from_file(cls, path: str) -> 'Keystore':
        with open(path, 'r') as f:
            return cls.from_json(json.load(f))

    @staticmethod
    def _process_password(password: str) -> bytes:
        """
        Encode password as NFKD UTF-8 as per:
        https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2335.md#password-requirements
        """
        password = normalize('NFKD', password)
        password = ''.join(c for c in password if ord(c) not in UNICODE_CONTROL_CHARS)
        return password.encode('UTF-8')

    @classmethod
    def encrypt(cls, *, secret: bytes, password: str, path: str='',
                kdf_salt: bytes=randbits(256).to_bytes(32, 'big'),
                aes_iv: bytes=randbits(128).to_bytes(16, 'big')) -> 'Keystore':
        """
        Encrypt a secret (BLS SK) as an EIP 2335 Keystore.
        """
        keystore = cls()
        keystore.uuid = str(uuid4())
        keystore.crypto.kdf.params['salt'] = kdf_salt
        decryption_key = keystore.kdf(
            password=cls._process_password(password),
            **keystore.crypto.kdf.params
        )
        keystore.crypto.cipher.params['iv'] = aes_iv
        cipher = AES_128_CTR(key=decryption_key[:16], **keystore.crypto.cipher.params)
        keystore.crypto.cipher.message = cipher.encrypt(secret)
        keystore.crypto.checksum.message = SHA256(decryption_key[16:32] + keystore.crypto.cipher.message)
        keystore.pubkey = bls.SkToPk(int.from_bytes(secret, 'big')).hex()
        keystore.path = path
        return keystore

    def decrypt(self, password: str) -> bytes:
        """
        Retrieve the secret (BLS SK) from the self keystore by decrypting it with `password`
        """
        decryption_key = self.kdf(
            password=self._process_password(password),
            **self.crypto.kdf.params
        )
        if SHA256(decryption_key[16:32] + self.crypto.cipher.message) != self.crypto.checksum.message:
            raise ValueError("Checksum message error")

        cipher = AES_128_CTR(key=decryption_key[:16], **self.crypto.cipher.params)
        return cipher.decrypt(self.crypto.cipher.message)


@dataclass
class Pbkdf2Keystore(Keystore):
    crypto: KeystoreCrypto = KeystoreCrypto(
        kdf=KeystoreModule(
            function='pbkdf2',
            params={
                'c': 2**18,
                'dklen': 32,
                "prf": 'hmac-sha256'
            },
        ),
        checksum=KeystoreModule(
            function='sha256',
        ),
        cipher=KeystoreModule(
            function='aes-128-ctr',
        )
    )


@dataclass
class ScryptKeystore(Keystore):
    crypto: KeystoreCrypto = KeystoreCrypto(
        kdf=KeystoreModule(
            function='scrypt',
            params={
                'dklen': 32,
                'n': 2**18,
                'r': 8,
                'p': 1,
            },
        ),
        checksum=KeystoreModule(
            function='sha256',
        ),
        cipher=KeystoreModule(
            function='aes-128-ctr',
        )
    )
