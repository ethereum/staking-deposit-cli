import click
from typing import (
    Any,
)

from staking_deposit.utils.click import (
    captive_prompt_callback,
    jit_option,
)
from staking_deposit.utils.intl import load_text
from staking_deposit.utils.validation import validate_int_range
from .generate_keys import (
    generate_keys,
    generate_keys_arguments_decorator,
)


def validate_mnemonic(ctx: click.Context, param: Any, mnemonic: str) -> str:
    return mnemonic


@click.command(
    help=''
)
@jit_option(
    callback=validate_mnemonic,
    help='',
    param_decls='--seed',
    prompt='Enter seed',
    type=str,
)
@jit_option(
    default=0,
    help='',
    param_decls="--validator_start_index",
    prompt='Validator start index'
)

@generate_keys_arguments_decorator
@click.pass_context
def existing_seed(ctx: click.Context, seed: str, **kwargs: Any) -> None:
    ctx.obj = {} if ctx.obj is None else ctx.obj  # Create a new ctx.obj if it doesn't exist
    ctx.obj.update({'seed': bytes.fromhex(seed)})
    ctx.forward(generate_keys)