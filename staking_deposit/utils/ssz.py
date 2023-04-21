from ssz import (
    ByteVector,
    Serializable,
    uint64,
    bytes4,
    bytes32,
    bytes48,
    bytes96
)
from staking_deposit.utils.constants import (
    DOMAIN_BLS_TO_EXECUTION_CHANGE,
    DOMAIN_DEPOSIT,
    DOMAIN_VOLUNTARY_EXIT,
    ZERO_BYTES32,
)

bytes8 = ByteVector(8)
bytes20 = ByteVector(20)


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


def compute_fork_data_root(current_version: bytes, genesis_validators_root: bytes) -> bytes:
    """
    Return the appropriate ForkData root for a given deposit version.
    """
    if len(current_version) != 4:
        raise ValueError(f"Fork version should be in 4 bytes. Got {len(current_version)}.")
    return ForkData(
        current_version=current_version,
        genesis_validators_root=genesis_validators_root,
    ).hash_tree_root


def compute_deposit_domain(fork_version: bytes) -> bytes:
    """
    Deposit-only `compute_domain`
    """
    if len(fork_version) != 4:
        raise ValueError(f"Fork version should be in 4 bytes. Got {len(fork_version)}.")
    domain_type = DOMAIN_DEPOSIT
    fork_data_root = compute_deposit_fork_data_root(fork_version)
    return domain_type + fork_data_root[:28]


def compute_voluntary_exit_domain(fork_version: bytes, genesis_validators_root: bytes) -> bytes:
    """
    VOLUNTARY_EXIT-only `compute_domain`
    """
    if len(fork_version) != 4:
        raise ValueError(f"Fork version should be in 4 bytes. Got {len(fork_version)}.")
    domain_type = DOMAIN_VOLUNTARY_EXIT
    fork_data_root = compute_fork_data_root(fork_version, genesis_validators_root)
    return domain_type + fork_data_root[:28]


def compute_bls_to_execution_change_domain(fork_version: bytes, genesis_validators_root: bytes) -> bytes:
    """
    BLS_TO_EXECUTION_CHANGE-only `compute_domain`
    """
    if len(fork_version) != 4:
        raise ValueError(f"Fork version should be in 4 bytes. Got {len(fork_version)}.")
    domain_type = DOMAIN_BLS_TO_EXECUTION_CHANGE
    fork_data_root = compute_fork_data_root(fork_version, genesis_validators_root)
    return domain_type + fork_data_root[:28]


def compute_deposit_fork_data_root(current_version: bytes) -> bytes:
    """
    Return the appropriate ForkData root for a given deposit version.
    """
    genesis_validators_root = ZERO_BYTES32  # For deposit, it's fixed value
    return compute_fork_data_root(current_version, genesis_validators_root)


def compute_signing_root(ssz_object: Serializable, domain: bytes) -> bytes:
    """
    Return the signing root of an object by calculating the root of the object-domain tree.
    The root is the hash tree root of:
    https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md#signingdata
    """
    if len(domain) != 32:
        raise ValueError(f"Domain should be in 32 bytes. Got {len(domain)}.")
    domain_wrapped_object = SigningData(
        object_root=ssz_object.hash_tree_root,
        domain=domain,
    )
    return domain_wrapped_object.hash_tree_root


class DepositMessage(Serializable):
    """
    Ref: https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md#depositmessage
    """
    fields = [
        ('pubkey', bytes48),
        ('withdrawal_credentials', bytes32),
        ('amount', uint64),
    ]


class DepositData(Serializable):
    """
    Ref: https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md#depositdata
    """
    fields = [
        ('pubkey', bytes48),
        ('withdrawal_credentials', bytes32),
        ('amount', uint64),
        ('signature', bytes96)
    ]


class BLSToExecutionChange(Serializable):
    """
    Ref: https://github.com/ethereum/consensus-specs/blob/dev/specs/capella/beacon-chain.md#blstoexecutionchange
    """
    fields = [
        ('validator_index', uint64),
        ('from_bls_pubkey', bytes48),
        ('to_execution_address', bytes20),
    ]


class SignedBLSToExecutionChange(Serializable):
    """
    Ref: https://github.com/ethereum/consensus-specs/blob/dev/specs/capella/beacon-chain.md#signedblstoexecutionchange
    """
    fields = [
        ('message', BLSToExecutionChange),
        ('signature', bytes96),
    ]


class VoluntaryExit(Serializable):
    """
    Ref: https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md#voluntaryexit
    """
    fields = [
        # TODO: Figure out correct type for epoch
        ('epoch', uint64),
        ('validator_index', uint64)
    ]


class SignedVoluntaryExit(Serializable):
    """
    Ref: https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md#signedvoluntaryexit
    """
    fields = [
        ('message', VoluntaryExit),
        ('signature', bytes96),
    ]
