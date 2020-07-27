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
    assert(n < 2**(128 * r / 8))
    res = _scrypt(password=password, salt=salt, key_len=dklen, N=n, r=r, p=p)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def PBKDF2(*, password: bytes, salt: bytes, dklen: int, c: int, prf: str) -> bytes:
    assert('sha' in prf)
    _hash = _sha256 if 'sha256' in prf else _sha512
    res = _PBKDF2(password=password, salt=salt, dkLen=dklen, count=c, hmac_hash_module=_hash)  # type: ignore
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def HKDF(*, salt: bytes, IKM: bytes, L: int, info: bytes=b'') -> bytes:
    res = _HKDF(master=IKM, key_len=L, salt=salt, hashmod=_sha256, context=info)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def AES_128_CTR(*, key: bytes, iv: bytes) -> Any:
    assert len(key) == 16
    return _AES.new(key=key, mode=_AES.MODE_CTR, initial_value=iv, nonce=b'')
