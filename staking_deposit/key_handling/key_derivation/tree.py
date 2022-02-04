from staking_deposit.utils.crypto import (
    HKDF,
    SHA256,
)
from py_ecc.optimized_bls12_381 import curve_order as bls_curve_order
from typing import List


def _flip_bits_256(input: int) -> int:
    """
    Flips 256 bits worth of `input`.
    """
    return input ^ (2**256 - 1)


def _IKM_to_lamport_SK(*, IKM: bytes, salt: bytes) -> List[bytes]:
    """
    Derives the lamport SK for a given `IKM` and `salt`.

    Ref: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2333.md#ikm_to_lamport_sk
    """
    OKM = HKDF(salt=salt, IKM=IKM, L=8160)
    lamport_SK = [OKM[i: i + 32] for i in range(0, 8160, 32)]
    return lamport_SK


def _parent_SK_to_lamport_PK(*, parent_SK: int, index: int) -> bytes:
    """
    Derives the `index`th child's lamport PK from the `parent_SK`.

    Ref: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2333.md#parent_sk_to_lamport_pk
    """
    salt = index.to_bytes(4, byteorder='big')
    IKM = parent_SK.to_bytes(32, byteorder='big')
    lamport_0 = _IKM_to_lamport_SK(IKM=IKM, salt=salt)
    not_IKM = _flip_bits_256(parent_SK).to_bytes(32, byteorder='big')
    lamport_1 = _IKM_to_lamport_SK(IKM=not_IKM, salt=salt)
    lamport_SKs = lamport_0 + lamport_1
    lamport_PKs = [SHA256(sk) for sk in lamport_SKs]
    compressed_PK = SHA256(b''.join(lamport_PKs))
    return compressed_PK


def _HKDF_mod_r(*, IKM: bytes, key_info: bytes=b'') -> int:
    """
    Hashes the IKM using HKDF and returns the answer as an int modulo r, the BLS field order.

    Ref: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2333.md#hkdf_mod_r
    """
    L = 48  # `ceil((3 * ceil(log2(r))) / 16)`, where `r` is the order of the BLS 12-381 curve
    salt = b'BLS-SIG-KEYGEN-SALT-'
    SK = 0
    while SK == 0:
        salt = SHA256(salt)
        okm = HKDF(
            salt=salt,
            IKM=IKM + b'\x00',  # add postfix `I2OSP(0, 1)`
            L=L,
            info=key_info + L.to_bytes(2, 'big'),
        )
        SK = int.from_bytes(okm, byteorder='big') % bls_curve_order
    return SK


def derive_child_SK(*, parent_SK: int, index: int) -> int:
    """
    Given a parent SK `parent_SK`, return the child SK at the supplied `index`.

    Ref: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2333.md#derive_child_sk
    """
    if index < 0 or index >= 2**32:
        raise IndexError(f"`index` should be greater than or equal to  0 and less than 2**32. Got index={index}.")
    lamport_PK = _parent_SK_to_lamport_PK(parent_SK=parent_SK, index=index)
    return _HKDF_mod_r(IKM=lamport_PK)


def derive_master_SK(seed: bytes) -> int:
    """
    Given a seed, derive the master SK.

    Ref: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2333.md#derive_master_sk
    """
    if len(seed) < 32:
        raise ValueError(f"`len(seed)` should be greater than or equal to 32. Got {len(seed)}.")
    return _HKDF_mod_r(IKM=seed)
