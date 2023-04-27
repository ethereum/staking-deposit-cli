
import json
import os
import time
from typing import Any, Dict, List
from py_ecc.bls import G2ProofOfPossession as bls

from staking_deposit.settings import BaseChainSetting
from staking_deposit.utils.constants import DEFAULT_EXIT_TRANSACTION_FOLDER_NAME
from staking_deposit.utils.ssz import (
    SignedVoluntaryExit,
    VoluntaryExit,
    compute_signing_root,
    compute_voluntary_exit_domain,
)


def exit_transaction_generation(
        chain_settings: BaseChainSetting,
        signing_key: int,
        validator_index: int,
        epoch: int) -> SignedVoluntaryExit:
    message = VoluntaryExit(
        epoch=epoch,
        validator_index=validator_index
    )

    domain = compute_voluntary_exit_domain(
        fork_version=chain_settings.CURRENT_FORK_VERSION,
        genesis_validators_root=chain_settings.GENESIS_VALIDATORS_ROOT
    )

    signing_root = compute_signing_root(message, domain)
    signature = bls.Sign(signing_key, signing_root)

    signed_exit = SignedVoluntaryExit(
        message=message,
        signature=signature,
    )

    return signed_exit


def export_exit_transactions_json(folder: str, signed_exits: List[SignedVoluntaryExit]) -> str:
    signed_exits_json = []
    for exit in signed_exits:
        signed_exit_json: Dict[str, Any] = {}
        message = {
            'epoch': str(exit.message.epoch),
            'validator_index': str(exit.message.validator_index),
        }
        signed_exit_json.update({'message': message})
        signed_exit_json.update({'signature': '0x' + exit.signature.hex()})

        signed_exits_json.append(signed_exit_json)

    output_folder = os.path.join(
        folder,
        DEFAULT_EXIT_TRANSACTION_FOLDER_NAME,
    )
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    filefolder = os.path.join(output_folder, 'signed_exit_transactions-%i.json' % time.time())

    with open(filefolder, 'w') as f:
        json.dump(signed_exits_json, f)
    if os.name == 'posix':
        os.chmod(filefolder, int('440', 8))  # Read for owner & group
    return filefolder
