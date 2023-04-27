import click
import os

from typing import Any
from staking_deposit.exit_transaction import exit_transaction_generation, export_exit_transactions_json
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
from staking_deposit.utils.validation import validate_int_range


FUNC_NAME = 'exit_transaction_keystore'


@click.command(
    help=load_text(['arg_exit_transaction_keystore', 'help'], func=FUNC_NAME),
)
@jit_option(
    callback=captive_prompt_callback(
        lambda x: closest_match(x, list(ALL_CHAINS.keys())),
        choice_prompt_func(
            lambda: load_text(['arg_exit_transaction_keystore_chain', 'prompt'], func=FUNC_NAME),
            list(ALL_CHAINS.keys())
        ),
    ),
    default=MAINNET,
    help=lambda: load_text(['arg_exit_transaction_keystore_chain', 'help'], func=FUNC_NAME),
    param_decls='--chain',
    prompt=choice_prompt_func(
        lambda: load_text(['arg_exit_transaction_keystore_chain', 'prompt'], func=FUNC_NAME),
        # Since `prater` is alias of `goerli`, do not show `prater` in the prompt message.
        list(key for key in ALL_CHAINS.keys() if key != PRATER)
    ),
)
@jit_option(
    callback=captive_prompt_callback(
        lambda x: x,
        lambda: load_text(['arg_exit_transaction_keystore_keystore', 'prompt'], func=FUNC_NAME),
    ),
    help=lambda: load_text(['arg_exit_transaction_keystore_keystore', 'help'], func=FUNC_NAME),
    param_decls='--keystore',
    prompt=lambda: load_text(['arg_exit_transaction_keystore_keystore', 'prompt'], func=FUNC_NAME),
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@jit_option(
    callback=captive_prompt_callback(
        lambda x: x,
        lambda: load_text(['arg_exit_transaction_keystore_keystore_password', 'prompt'], func=FUNC_NAME),
        None,
        lambda: load_text(['arg_exit_transaction_keystore_keystore_password', 'invalid'], func=FUNC_NAME),
        True,
    ),
    help=lambda: load_text(['arg_exit_transaction_keystore_keystore_password', 'help'], func=FUNC_NAME),
    hide_input=True,
    param_decls='--keystore_password',
    prompt=lambda: load_text(['arg_exit_transaction_keystore_keystore_password', 'prompt'], func=FUNC_NAME),
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
    help=lambda: load_text(['arg_exit_transaction_keystore_epoch', 'help'], func=FUNC_NAME),
    param_decls='--epoch',
)
@jit_option(
    default=os.getcwd(),
    help=lambda: load_text(['arg_exit_transaction_keystore_output_folder', 'help'], func=FUNC_NAME),
    param_decls='--output_folder',
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.pass_context
def exit_transaction_keystore(
        ctx: click.Context,
        chain: str,
        keystore: str,
        keystore_password: str,
        validator_index: int,
        epoch: int,
        output_folder: str,
        **kwargs: Any) -> None:
    saved_keystore = Keystore.from_file(keystore)

    try:
        secret_bytes = saved_keystore.decrypt(keystore_password)
    except ValueError:
        click.echo(load_text(['arg_exit_transaction_keystore_keystore_password', 'mismatch']))
        exit(1)

    signing_key = int.from_bytes(secret_bytes, 'big')
    chain_settings = get_chain_setting(chain)

    signed_exit = exit_transaction_generation(
        chain_settings=chain_settings,
        signing_key=signing_key,
        validator_index=validator_index,
        epoch=epoch,
    )

    saved_folder = export_exit_transactions_json(folder=output_folder, signed_exits=[signed_exit])

    click.echo(load_text(['msg_creation_success']) + saved_folder)
    click.pause(load_text(['msg_pause']))
