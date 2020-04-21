from ssz import (
    ByteVector,
    Serializable,
    uint64,
    bytes32,
    bytes48,
    bytes96
)

from eth2deposit.utils.constants import (
    DOMAIN_DEPOSIT,
    GENESIS_FORK_VERSION,
)

bytes8 = ByteVector(8)


# Crypto Domain SSZ

class SigningRoot(Serializable):
    fields = [
        ('object_root', bytes32),
        ('domain', bytes8)
    ]


def compute_domain(domain_type: bytes=DOMAIN_DEPOSIT, fork_version: bytes=GENESIS_FORK_VERSION) -> bytes:
    """
    Return the domain for the ``domain_type`` and ``fork_version``.
    """
    return domain_type + fork_version


def compute_signing_root(ssz_object: Serializable, domain: bytes) -> bytes:
    """
    Return the signing root of an object by calculating the root of the object-domain tree.
    """
    domain_wrapped_object = SigningRoot(
        object_root=ssz_object.hash_tree_root,
        domain=domain,
    )
    return domain_wrapped_object.hash_tree_root


# DepositMessage SSZ

class DepositMessage(Serializable):
    fields = [
        ('pubkey', bytes48),
        ('withdrawal_credentials', bytes32),
        ('amount', uint64),
    ]


class Deposit(Serializable):
    fields = [
        ('pubkey', bytes48),
        ('withdrawal_credentials', bytes32),
        ('amount', uint64),
        ('signature', bytes96)
    ]
