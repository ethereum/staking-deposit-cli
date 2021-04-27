import click
from typing import (
    Any,
)

from eth2deposit.exceptions import ValidationError
from eth2deposit.key_handling.key_derivation.mnemonic import (
    verify_mnemonic,
)
from eth2deposit.utils.constants import (
    WORD_LISTS_PATH,
)
from eth2deposit.utils.click import (
    captive_prompt_callback,
    jit_option,
)
from eth2deposit.utils.intl import load_text
from eth2deposit.utils.validation import validate_int_range
from .generate_keys import (
    generate_keys,
    generate_keys_arguments_decorator,
)


def validate_mnemonic(ctx: click.Context, param: Any, mnemonic: str) -> str:
    if verify_mnemonic(mnemonic, WORD_LISTS_PATH):
        return mnemonic
    else:
        raise ValidationError(load_text(['err_invalid_mnemonic']))


@click.command(
    help=load_text(['arg_existing_mnemonic', 'help'], func='existing_mnemonic'),
)
@jit_option(
    callback=validate_mnemonic,
    help=lambda: load_text(['arg_mnemonic', 'help'], func='existing_mnemonic'),
    param_decls='--mnemonic',
    prompt=lambda: load_text(['arg_mnemonic', 'prompt'], func='existing_mnemonic'),
    type=str,
)
@jit_option(
    callback=captive_prompt_callback(
        lambda x: x,
        load_text(['arg_mnemonic_password', 'prompt'], func='existing_mnemonic'),
        load_text(['arg_mnemonic_password', 'confirm'], func='existing_mnemonic'),
        load_text(['arg_mnemonic_password', 'mismatch'], func='existing_mnemonic'),
        True,
    ),
    default='',
    help=lambda: load_text(['arg_mnemonic_password', 'help'], func='existing_mnemonic'),
    hidden=True,
    param_decls='--mnemonic-password',
    prompt=False,
)
@jit_option(
    callback=captive_prompt_callback(
        lambda num: validate_int_range(num, 0, 2**32),
        load_text(['arg_validator_start_index', 'prompt'], func='existing_mnemonic'),
        load_text(['arg_validator_start_index', 'confirm'], func='existing_mnemonic'),
    ),
    default=0,
    help=lambda: load_text(['arg_validator_start_index', 'help'], func='existing_mnemonic'),
    param_decls="--validator_start_index",
    prompt=lambda: load_text(['arg_validator_start_index', 'prompt'], func='existing_mnemonic'),
)
@generate_keys_arguments_decorator
@click.pass_context
def existing_mnemonic(ctx: click.Context, mnemonic: str, mnemonic_password: str, **kwargs: Any) -> None:
    if mnemonic_password != '':
        click.clear()
        click.confirm(load_text(['msg_mnemonic_password_confirm']), abort=True)

    ctx.obj = {} if ctx.obj is None else ctx.obj  # Create a new ctx.obj if it doesn't exist
    ctx.obj.update({'mnemonic': mnemonic, 'mnemonic_password': mnemonic_password})
    ctx.forward(generate_keys)
