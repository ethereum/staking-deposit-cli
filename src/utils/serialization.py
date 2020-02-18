from ssz import (
    ByteVector,
    Serializable,
)

from utils.constants import (
    DOMAIN_DEPOSIT,
    GENESIS_FORK_VERSION,
)


class SigningRoot(Serializable):
    fields = [
        ('object_root', ByteVector(32)),
        ('domain', ByteVector(8))
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
    domain_wrapped_object = SigningRoot.create(
        object_root=ssz_object.get_hash_tree_root(),
        domain=domain,
    )
    return domain_wrapped_object.get_hash_tree_root()
