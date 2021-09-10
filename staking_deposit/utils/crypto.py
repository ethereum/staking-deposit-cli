from typing import Any

from Crypto.Hash import (
    SHA256 as _sha256,
    SHA512 as _sha512,
)
from Crypto.Protocol.KDF import (
    scrypt as _scrypt,
    HKDF as _HKDF,
    PBKDF2 as _PBKDF2,
)
from Crypto.Cipher import (
    AES as _AES
)


def SHA256(x: bytes) -> bytes:
    return _sha256.new(x).digest()


def scrypt(*, password: str, salt: str, n: int, r: int, p: int, dklen: int) -> bytes:
    if n * r * p < 2**20:  # 128 MB memory usage
        raise ValueError("The Scrypt parameters chosen are not secure.")
    if n >= 2**(128 * r / 8):
        raise ValueError("The given `n` should be less than `2**(128 * r / 8)`."
                         f"\tGot `n={n}`, r={r}, 2**(128 * r / 8)={2**(128 * r / 8)}")
    res = _scrypt(password=password, salt=salt, key_len=dklen, N=n, r=r, p=p)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def PBKDF2(*, password: bytes, salt: bytes, dklen: int, c: int, prf: str) -> bytes:
    if 'sha' not in prf:
        raise ValueError(f"String 'sha' is not in `prf`({prf})")
    if 'sha256' in prf and c < 2**18:
        '''
        Verify the number of rounds of SHA256-PBKDF2. SHA512 not checked as use in BIP39
        does not require, and therefore doesn't use, safe parameters (c=2048).

        Ref: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#from-mnemonic-to-seed
        '''
        raise ValueError("The PBKDF2 parameters chosen are not secure.")
    _hash = _sha256 if 'sha256' in prf else _sha512
    res = _PBKDF2(password=password, salt=salt, dkLen=dklen, count=c, hmac_hash_module=_hash)  # type: ignore
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def HKDF(*, salt: bytes, IKM: bytes, L: int, info: bytes=b'') -> bytes:
    res = _HKDF(master=IKM, key_len=L, salt=salt, hashmod=_sha256, context=info)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def AES_128_CTR(*, key: bytes, iv: bytes) -> Any:
    if len(key) != 16:
        raise ValueError(f"The key length should be 16. Got {len(key)}.")
    return _AES.new(key=key, mode=_AES.MODE_CTR, initial_value=iv, nonce=b'')
