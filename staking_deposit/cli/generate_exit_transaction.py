import json
import click
import os
import time
from py_ecc.bls import G2ProofOfPossession as bls

from typing import Any, Dict
from staking_deposit.exceptions import ValidationError
from staking_deposit.key_handling.keystore import Keystore
from staking_deposit.settings import ALL_CHAINS, MAINNET, PRATER, get_chain_setting
from staking_deposit.utils.click import (
    captive_prompt_callback,
    choice_prompt_func, 
    jit_option,
)
from staking_deposit.utils.intl import (
    closest_match,
    load_text,
)
from staking_deposit.utils.ssz import SignedVoluntaryExit, VoluntaryExit, compute_signing_root, compute_voluntary_exit_domain
from staking_deposit.utils.validation import validate_int_range

FUNC_NAME = 'generate_exit_transaction'

@click.command(
    help=load_text(['arg_generate_exit_transaction', 'help'], func=FUNC_NAME),
)
@jit_option(
    callback=captive_prompt_callback(
        lambda x: closest_match(x, list(ALL_CHAINS.keys())),
        choice_prompt_func(
            lambda: load_text(['arg_generate_exit_transaction_chain', 'prompt'], func=FUNC_NAME),
            list(ALL_CHAINS.keys())
        ),
    ),
    default=MAINNET,
    help=lambda: load_text(['arg_generate_exit_transaction_chain', 'help'], func=FUNC_NAME),
    param_decls='--chain',
    prompt=choice_prompt_func(
        lambda: load_text(['arg_generate_exit_transaction_chain', 'prompt'], func=FUNC_NAME),
        # Since `prater` is alias of `goerli`, do not show `prater` in the prompt message.
        list(key for key in ALL_CHAINS.keys() if key != PRATER)
    ),
)
@jit_option(
    default=os.getcwd(),
    help=lambda: load_text(['arg_generate_exit_transaction_keystore', 'help'], func=FUNC_NAME),
    param_decls='--keystore',
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@jit_option(
    callback=captive_prompt_callback(
        lambda x: x,
        lambda:load_text(['arg_generate_exit_transaction_keystore_password', 'prompt'], func=FUNC_NAME),
        None,
        lambda: load_text(['arg_generate_exit_transaction_keystore_password', 'invalid'], func=FUNC_NAME),
        True,
    ),
    help=lambda: load_text(['arg_generate_exit_transaction_keystore_password', 'help'], func=FUNC_NAME),
    hide_input=True,
    param_decls='--keystore_password',
    prompt=lambda: load_text(['arg_generate_exit_transaction_keystore_password', 'prompt'], func=FUNC_NAME),
)
@jit_option(
    callback=captive_prompt_callback(
        lambda num: validate_int_range(num, 0, 2**32),
        lambda: load_text(['arg_validator_index', 'prompt'], func=FUNC_NAME),
    ),
    help=lambda: load_text(['arg_validator_index', 'help'], func=FUNC_NAME),
    param_decls='--validator_index',
    prompt=lambda: load_text(['arg_validator_index', 'prompt'], func=FUNC_NAME),
)
@jit_option(
    default=0,
    help=lambda: load_text(['arg_generate_exit_transaction_epoch', 'help'], func=FUNC_NAME),
    param_decls='--epoch',
)
@click.pass_context
def generate_exit_transaction(
        ctx: click.Context, 
        chain: str,
        keystore: str, 
        keystore_password: str, 
        validator_index: int,
        epoch: int,
        **kwargs: Any) -> None:
    saved_keystore = Keystore.from_file(keystore)

    try:
        secret_bytes = saved_keystore.decrypt(keystore_password)
    except Exception:
        raise ValidationError(load_text(['arg_generate_exit_transaction_keystore_password', 'mismatch']))
    
    signing_key = int.from_bytes(secret_bytes, 'big')

    message = VoluntaryExit(
        epoch=epoch,
        validator_index=validator_index
    )

    chain_settings = get_chain_setting(chain)
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

    folder = "./"
    export_exit_transaction_json(folder=folder, signed_exit=signed_exit)

    click.echo(load_text(['msg_creation_success']) + folder)
    click.pause(load_text(['msg_pause']))

def export_exit_transaction_json(folder: str, signed_exit: SignedVoluntaryExit) -> str:
    filefolder = os.path.join(folder, 'signed_exit_transaction-%i.json' % time.time())

    signed_exit_json: Dict[str, Any] = {}
    message = {
        'epoch': str(signed_exit.message.epoch),
        'validator_index': str(signed_exit.message.validator_index),
    }
    signed_exit_json.update({'message': message})
    signed_exit_json.update({'signature': '0x' + signed_exit.signature.hex()})

    with open(filefolder, 'w') as f:
        json.dump(signed_exit_json, f)
    if os.name == 'posix':
        os.chmod(filefolder, int('440', 8))  # Read for owner & group
    return filefolder
