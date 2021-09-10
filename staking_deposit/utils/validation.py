import click
import json
from eth_typing import (
    BLSPubkey,
    BLSSignature,
)
from typing import Any, Dict, Sequence

from py_ecc.bls import G2ProofOfPossession as bls

from staking_deposit.exceptions import ValidationError
from staking_deposit.utils.intl import load_text
from staking_deposit.utils.ssz import (
    compute_deposit_domain,
    compute_signing_root,
    DepositData,
    DepositMessage,
)
from staking_deposit.credentials import (
    Credential,
)
from staking_deposit.utils.constants import (
    MAX_DEPOSIT_AMOUNT,
    MIN_DEPOSIT_AMOUNT,
    BLS_WITHDRAWAL_PREFIX,
    ETH1_ADDRESS_WITHDRAWAL_PREFIX,
)
from staking_deposit.utils.crypto import SHA256


def verify_deposit_data_json(filefolder: str, credentials: Sequence[Credential]) -> bool:
    """
    Validate every deposit found in the deposit-data JSON file folder.
    """
    with open(filefolder, 'r') as f:
        deposit_json = json.load(f)
        with click.progressbar(deposit_json, label=load_text(['msg_deposit_verification']),
                               show_percent=False, show_pos=True) as deposits:
            return all([validate_deposit(deposit, credential) for deposit, credential in zip(deposits, credentials)])
    return False


def validate_deposit(deposit_data_dict: Dict[str, Any], credential: Credential) -> bool:
    '''
    Checks whether a deposit is valid based on the staking deposit rules.
    https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md#deposits
    '''
    pubkey = BLSPubkey(bytes.fromhex(deposit_data_dict['pubkey']))
    withdrawal_credentials = bytes.fromhex(deposit_data_dict['withdrawal_credentials'])
    amount = deposit_data_dict['amount']
    signature = BLSSignature(bytes.fromhex(deposit_data_dict['signature']))
    deposit_message_root = bytes.fromhex(deposit_data_dict['deposit_data_root'])
    fork_version = bytes.fromhex(deposit_data_dict['fork_version'])

    # Verify pubkey
    if len(pubkey) != 48:
        return False
    if pubkey != credential.signing_pk:
        return False

    # Verify withdrawal credential
    if len(withdrawal_credentials) != 32:
        return False
    if withdrawal_credentials[:1] == BLS_WITHDRAWAL_PREFIX == credential.withdrawal_prefix:
        if withdrawal_credentials[1:] != SHA256(credential.withdrawal_pk)[1:]:
            return False
    elif withdrawal_credentials[:1] == ETH1_ADDRESS_WITHDRAWAL_PREFIX == credential.withdrawal_prefix:
        if withdrawal_credentials[1:12] != b'\x00' * 11:
            return False
        if credential.eth1_withdrawal_address is None:
            return False
        if withdrawal_credentials[12:] != credential.eth1_withdrawal_address:
            return False
    else:
        return False

    # Verify deposit amount
    if not MIN_DEPOSIT_AMOUNT < amount <= MAX_DEPOSIT_AMOUNT:
        return False

    # Verify deposit signature && pubkey
    deposit_message = DepositMessage(pubkey=pubkey, withdrawal_credentials=withdrawal_credentials, amount=amount)
    domain = compute_deposit_domain(fork_version)
    signing_root = compute_signing_root(deposit_message, domain)
    if not bls.Verify(pubkey, signing_root, signature):
        return False

    # Verify Deposit Root
    signed_deposit = DepositData(
        pubkey=pubkey,
        withdrawal_credentials=withdrawal_credentials,
        amount=amount,
        signature=signature,
    )
    return signed_deposit.hash_tree_root == deposit_message_root


def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValidationError(load_text(['msg_password_length']))
    return password


def validate_int_range(num: Any, low: int, high: int) -> int:
    '''
    Verifies that `num` is an `int` andlow <= num < high
    '''
    try:
        num_int = int(num)  # Try cast to int
        assert num_int == float(num)  # Check num is not float
        assert low <= num_int < high  # Check num in range
        return num_int
    except (ValueError, AssertionError):
        raise ValidationError(load_text(['err_not_positive_integer']))
