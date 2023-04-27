import click
import os

from typing import Any, Sequence
from staking_deposit.cli.existing_mnemonic import load_mnemonic_arguments_decorator
from staking_deposit.credentials import Credential
from staking_deposit.exit_transaction import exit_transaction_generation, export_exit_transactions_json
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
from staking_deposit.utils.validation import validate_int_range, validate_validator_indices


FUNC_NAME = 'exit_transaction_mnemonic'


@click.command(
    help=load_text(['arg_exit_transaction_mnemonic', 'help'], func=FUNC_NAME),
)
@jit_option(
    callback=captive_prompt_callback(
        lambda x: closest_match(x, list(ALL_CHAINS.keys())),
        choice_prompt_func(
            lambda: load_text(['arg_exit_transaction_mnemonic_chain', 'prompt'], func=FUNC_NAME),
            list(ALL_CHAINS.keys())
        ),
    ),
    default=MAINNET,
    help=lambda: load_text(['arg_exit_transaction_mnemonic_chain', 'help'], func=FUNC_NAME),
    param_decls='--chain',
    prompt=choice_prompt_func(
        lambda: load_text(['arg_exit_transaction_mnemonic_chain', 'prompt'], func=FUNC_NAME),
        # Since `prater` is alias of `goerli`, do not show `prater` in the prompt message.
        list(key for key in ALL_CHAINS.keys() if key != PRATER)
    ),
)
@load_mnemonic_arguments_decorator
@jit_option(
    callback=captive_prompt_callback(
        lambda num: validate_int_range(num, 0, 2**32),
        lambda: load_text(['arg_exit_transaction_mnemonic_start_index', 'prompt'], func=FUNC_NAME),
    ),
    default=0,
    help=lambda: load_text(['arg_exit_transaction_mnemonic_start_index', 'help'], func=FUNC_NAME),
    param_decls="--validator_start_index",
    prompt=lambda: load_text(['arg_exit_transaction_mnemonic_start_index', 'prompt'], func=FUNC_NAME),
)
@jit_option(
    callback=captive_prompt_callback(
        lambda validator_indices: validate_validator_indices(validator_indices),
        lambda: load_text(['arg_exit_transaction_mnemonic_indices', 'prompt'], func=FUNC_NAME),
    ),
    help=lambda: load_text(['arg_exit_transaction_mnemonic_indices', 'help'], func=FUNC_NAME),
    param_decls='--validator_indices',
    prompt=lambda: load_text(['arg_exit_transaction_mnemonic_indices', 'prompt'], func=FUNC_NAME),
)
@jit_option(
    default=0,
    help=lambda: load_text(['arg_exit_transaction_mnemonic_epoch', 'help'], func=FUNC_NAME),
    param_decls='--epoch',
)
@jit_option(
    default=os.getcwd(),
    help=lambda: load_text(['arg_exit_transaction_mnemonic_output_folder', 'help'], func=FUNC_NAME),
    param_decls='--output_folder',
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.pass_context
def exit_transaction_mnemonic(
        ctx: click.Context,
        chain: str,
        mnemonic: str,
        mnemonic_password: str,
        validator_start_index: int,
        validator_indices: Sequence[int],
        epoch: int,
        output_folder: str,
        **kwargs: Any) -> None:

    chain_settings = get_chain_setting(chain)
    num_keys = len(validator_indices)
    key_indices = range(validator_start_index, validator_start_index + num_keys)

    signed_exits = []
    # We assume that the list of validator indices are in order and increment the start index
    for key_index, validator_index in zip(key_indices, validator_indices):
        credential = Credential(
            mnemonic=mnemonic,
            mnemonic_password=mnemonic_password,
            index=key_index,
            amount=0,  # Unneeded for this purpose
            chain_setting=chain_settings,
            hex_eth1_withdrawal_address=None
        )

        signing_key = credential.signing_sk

        signed_voluntary_exit = exit_transaction_generation(
            chain_settings=chain_settings,
            signing_key=signing_key,
            validator_index=validator_index,
            epoch=epoch
        )

        signed_exits.append(signed_voluntary_exit)

    saved_folder = export_exit_transactions_json(folder=output_folder, signed_exits=signed_exits)

    click.echo(load_text(['msg_creation_success']) + saved_folder)
    click.pause(load_text(['msg_pause']))
