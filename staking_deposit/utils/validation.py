import click
import json
import re
from typing import Any, Dict, Sequence

from eth_typing import (
    BLSPubkey,
    BLSSignature,
    HexAddress,
)
from eth_utils import is_hex_address, is_checksum_address, to_normalized_address, decode_hex
from py_ecc.bls import G2ProofOfPossession as bls

from staking_deposit.exceptions import ValidationError
from staking_deposit.utils.intl import load_text
from staking_deposit.utils.ssz import (
    BLSToExecutionChange,
    DepositData,
    DepositMessage,
    compute_bls_to_execution_change_domain,
    compute_deposit_domain,
    compute_signing_root,
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
from staking_deposit.settings import BaseChainSetting


#
# Deposit
#

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


def validate_eth1_withdrawal_address(cts: click.Context, param: Any, address: str) -> HexAddress:
    if address is None:
        return None
    if not is_hex_address(address):
        raise ValidationError(load_text(['err_invalid_ECDSA_hex_addr']))
    if not is_checksum_address(address):
        raise ValidationError(load_text(['err_invalid_ECDSA_hex_addr_checksum']))

    normalized_address = to_normalized_address(address)
    click.echo('\n%s\n' % load_text(['msg_ECDSA_hex_addr_withdrawal']))
    return normalized_address

#
# BLSToExecutionChange
#


def verify_bls_to_execution_change_json(filefolder: str,
                                        credentials: Sequence[Credential],
                                        *,
                                        input_validator_indices: Sequence[int],
                                        input_execution_address: str,
                                        chain_setting: BaseChainSetting) -> bool:
    """
    Validate every BLSToExecutionChange found in the bls_to_execution_change JSON file folder.
    """
    with open(filefolder, 'r') as f:
        btec_json = json.load(f)
        with click.progressbar(btec_json, label=load_text(['msg_bls_to_execution_change_verification']),
                               show_percent=False, show_pos=True) as btecs:
            return all([
                validate_bls_to_execution_change(
                    btec, credential,
                    input_validator_index=input_validator_index,
                    input_execution_address=input_execution_address,
                    chain_setting=chain_setting)
                for btec, credential, input_validator_index in zip(btecs, credentials, input_validator_indices)
            ])
    return False


def validate_bls_to_execution_change(btec_dict: Dict[str, Any],
                                     credential: Credential,
                                     *,
                                     input_validator_index: int,
                                     input_execution_address: str,
                                     chain_setting: BaseChainSetting) -> bool:
    validator_index = int(btec_dict['message']['validator_index'])
    from_bls_pubkey = BLSPubkey(decode_hex(btec_dict['message']['from_bls_pubkey']))
    to_execution_address = decode_hex(btec_dict['message']['to_execution_address'])
    signature = BLSSignature(decode_hex(btec_dict['signature']))
    genesis_validators_root = decode_hex(btec_dict['metadata']['genesis_validators_root'])

    if validator_index != input_validator_index:
        return False
    if from_bls_pubkey != credential.withdrawal_pk:
        return False
    if (
        to_execution_address != credential.eth1_withdrawal_address
        or to_execution_address != decode_hex(input_execution_address)
    ):
        return False
    if genesis_validators_root != chain_setting.GENESIS_VALIDATORS_ROOT:
        return False

    message = BLSToExecutionChange(
        validator_index=validator_index,
        from_bls_pubkey=from_bls_pubkey,
        to_execution_address=to_execution_address,
    )
    domain = compute_bls_to_execution_change_domain(
        fork_version=chain_setting.GENESIS_FORK_VERSION,
        genesis_validators_root=genesis_validators_root,
    )
    signing_root = compute_signing_root(message, domain)

    if not bls.Verify(BLSPubkey(credential.withdrawal_pk), signing_root, signature):
        return False

    return True


def normalize_bls_withdrawal_credentials_to_bytes(bls_withdrawal_credentials: str) -> bytes:
    if bls_withdrawal_credentials.startswith('0x'):
        bls_withdrawal_credentials = bls_withdrawal_credentials[2:]

    try:
        bls_withdrawal_credentials_bytes = bytes.fromhex(bls_withdrawal_credentials)
    except Exception:
        raise ValidationError(load_text(['err_incorrect_hex_form']) + '\n')
    return bls_withdrawal_credentials_bytes


def is_eth1_address_withdrawal_credentials(withdrawal_credentials: bytes) -> bool:
    return (
        len(withdrawal_credentials) == 32
        and withdrawal_credentials[:1] == ETH1_ADDRESS_WITHDRAWAL_PREFIX
        and withdrawal_credentials[1:12] == b'\x00' * 11
    )


def validate_bls_withdrawal_credentials(bls_withdrawal_credentials: str) -> bytes:
    bls_withdrawal_credentials_bytes = normalize_bls_withdrawal_credentials_to_bytes(bls_withdrawal_credentials)

    if is_eth1_address_withdrawal_credentials(bls_withdrawal_credentials_bytes):
        raise ValidationError(load_text(['err_is_already_eth1_form']) + '\n')

    try:
        assert len(bls_withdrawal_credentials_bytes) == 32
        assert bls_withdrawal_credentials_bytes[:1] == BLS_WITHDRAWAL_PREFIX
    except (ValueError, AssertionError):
        raise ValidationError(load_text(['err_not_bls_form']) + '\n')

    return bls_withdrawal_credentials_bytes


def normalize_input_list(input: str) -> Sequence[str]:
    try:
        input = input.strip('[({})]')
        input = re.sub(' +', ' ', input)
        result = re.split(r'; |, | |,|;', input)
    except Exception:
        raise ValidationError(load_text(['err_incorrect_list']) + '\n')
    return result


def validate_bls_withdrawal_credentials_list(input_bls_withdrawal_credentials_list: str) -> Sequence[bytes]:
    bls_withdrawal_credentials_list = normalize_input_list(input_bls_withdrawal_credentials_list)
    return [validate_bls_withdrawal_credentials(cred) for cred in bls_withdrawal_credentials_list]


def validate_validator_indices(input_validator_indices: str) -> Sequence[int]:

    normalized_list = normalize_input_list(input_validator_indices)
    return [validate_int_range(int(index), 0, 2**32) for index in normalized_list]


def validate_bls_withdrawal_credentials_matching(bls_withdrawal_credentials: bytes, credential: Credential) -> None:
    if bls_withdrawal_credentials[1:] != SHA256(credential.withdrawal_pk)[1:]:
        raise ValidationError(load_text(['err_not_matching']) + '\n')
