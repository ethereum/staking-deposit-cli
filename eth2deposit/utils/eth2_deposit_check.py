import json
from py_ecc.bls import G2ProofOfPossession as bls

from utils.ssz import (
    compute_domain,
    compute_signing_root,
    Deposit,
    DepositMessage,
)
from utils.constants import (
    DOMAIN_DEPOSIT,
    MAX_DEPOSIT_AMOUNT,
    MIN_DEPOSIT_AMOUNT,
)


def verify_deposit_data_json(filefolder: str) -> bool:
    with open(filefolder, 'r') as f:
        deposit_json = json.load(f)
        return all([verify_deposit(deposit) for deposit in deposit_json])
    return False


def verify_deposit(deposit_data_dict: dict) -> bool:
    '''
    Checks whether a deposit is valid based on the eth2 rules.
    https://github.com/ethereum/eth2.0-specs/blob/dev/specs/phase0/beacon-chain.md#deposits
    '''
    pubkey = bytes.fromhex(deposit_data_dict['pubkey'])
    withdrawal_credentials = bytes.fromhex(deposit_data_dict['withdrawal_credentials'])
    amount = deposit_data_dict['amount']
    signature = bytes.fromhex(deposit_data_dict['signature'])
    deposit_data_root = bytes.fromhex(deposit_data_dict['signed_deposit_data_root'])

    # Verify deposit amount
    if not MIN_DEPOSIT_AMOUNT < amount <= MAX_DEPOSIT_AMOUNT:
        return False

    # Verify deposit signature && pubkey
    deposit_message = DepositMessage(pubkey=pubkey, withdrawal_credentials=withdrawal_credentials, amount=amount)
    domain = compute_domain(domain_type=DOMAIN_DEPOSIT)
    signing_root = compute_signing_root(deposit_message, domain)
    if not bls.Verify(pubkey, signing_root, signature):
        return False

    # Verify Deposit Root
    deposit = Deposit(pubkey=pubkey, withdrawal_credentials=withdrawal_credentials, amount=amount, signature=signature)
    return deposit.hash_tree_root == deposit_data_root
