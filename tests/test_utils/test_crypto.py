import pytest

from eth2deposit.utils.crypto import (
    scrypt,
    PBKDF2,
    AES_128_CTR,
)


@pytest.mark.parametrize(
    'n, r, valid',
    [
        (int(2**(128 * 1 / 8)) // 2, 1, True),
        (int(2**(128 * 1 / 8)), 1, False),
    ]
)
def test_scrypt_invalid_n(n, r, valid):
    if valid:
        scrypt(
            password="mypassword",
            salt="mysalt",
            n=n,
            r=r,
            p=1,
            dklen=32,
        )
    else:
        with pytest.raises(ValueError):
            scrypt(
                password="mypassword",
                salt="mysalt",
                n=n,
                r=r,
                p=1,
                dklen=32,
            )


@pytest.mark.parametrize(
    'prf, valid',
    [
        ("sha512", True),
        ("512", False),
    ]
)
def test_PBKDF2_invalid_prf(prf, valid):
    if valid:
        PBKDF2(
            password="mypassword",
            salt="mysalt",
            dklen=64,
            c=2048,
            prf=prf
        )
    else:
        with pytest.raises(ValueError):
            PBKDF2(
                password="mypassword",
                salt="mysalt",
                dklen=64,
                c=2048,
                prf=prf,
            )


@pytest.mark.parametrize(
    'key, iv, valid',
    [
        (b'\x12' * 16, bytes.fromhex("edc2606468f9660ad222690db8836a9d"), True),
        (b'\x12' * 15, bytes.fromhex("edc2606468f9660ad222690db8836a9d"), False),
    ]
)
def test_AES_128_CTR(key, iv, valid):
    if valid:
        AES_128_CTR(key=key, iv=iv)
    else:
        with pytest.raises(ValueError):
            AES_128_CTR(key=key, iv=iv)
