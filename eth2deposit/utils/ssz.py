from ssz import (
    ByteVector,
    Serializable,
    uint64,
    bytes4,
    bytes32,
    bytes48,
    bytes96
)
from eth2deposit.utils.constants import (
    DOMAIN_DEPOSIT,
    ZERO_BYTES32,
)

bytes8 = ByteVector(8)


# Crypto Domain SSZ

class SigningData(Serializable):
    fields = [
        ('object_root', bytes32),
        ('domain', bytes32)
    ]


class ForkData(Serializable):
    fields = [
        ('current_version', bytes4),
        ('genesis_validators_root', bytes32),
    ]


def compute_deposit_domain(fork_version: bytes) -> bytes:
    """
    Deposit-only `compute_domain`
    """
    assert len(fork_version) == 4
    domain_type = DOMAIN_DEPOSIT
    fork_data_root = compute_deposit_fork_data_root(fork_version)
    return domain_type + fork_data_root[:28]


def compute_deposit_fork_data_root(current_version: bytes) -> bytes:
    genesis_validators_root = ZERO_BYTES32  # For deposit, it's fixed value
    assert len(current_version) == 4
    return ForkData(
        current_version=current_version,
        genesis_validators_root=genesis_validators_root,
    ).hash_tree_root


def compute_signing_root(ssz_object: Serializable, domain: bytes) -> bytes:
    """
    Return the signing root of an object by calculating the root of the object-domain tree.
    """
    assert len(domain) == 32
    domain_wrapped_object = SigningData(
        object_root=ssz_object.hash_tree_root,
        domain=domain,
    )
    return domain_wrapped_object.hash_tree_root


class DepositMessage(Serializable):
    fields = [
        ('pubkey', bytes48),
        ('withdrawal_credentials', bytes32),
        ('amount', uint64),
    ]


class DepositData(Serializable):
    fields = [
        ('pubkey', bytes48),
        ('withdrawal_credentials', bytes32),
        ('amount', uint64),
        ('signature', bytes96)
    ]
