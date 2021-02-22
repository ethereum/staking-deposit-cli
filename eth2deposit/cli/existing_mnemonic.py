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
from eth2deposit.utils.intl import load_text
from .generate_keys import (
    generate_keys,
    generate_keys_arguments_decorator,
)


def validate_mnemonic(cts: click.Context, param: Any, mnemonic: str) -> str:
    if verify_mnemonic(mnemonic, WORD_LISTS_PATH):
        return mnemonic
    else:
        raise ValidationError(load_text('en', ['err_invalid_mnemonic']))


@click.command(
    help=load_text('en', ['arg_existing_mnemonic', 'help']),
)
@click.pass_context
@click.option(
    load_text('en', ['arg_mnemonic', 'argument']),
    callback=validate_mnemonic,
    help=load_text('en', ['arg_mnemonic', 'help']),
    prompt=load_text('en', ['arg_mnemonic', 'prompt']),
    required=True,
    type=str,
)
@click.password_option(
    load_text('en', ['arg_mnemonic_password', 'argument']),
    default='',
    help=load_text('en', ['arg_mnemonic_password', 'help']),
    prompt=False,
)
@click.option(
    load_text('en', ['arg_validator_start_index', 'argument']),
    confirmation_prompt=True,
    default=0,
    help=load_text('en', ['arg_validator_start_index', 'help']),
    prompt=load_text('en', ['arg_validator_start_index', 'prompt']),
    type=click.IntRange(0, 2**32 - 1),
)
@generate_keys_arguments_decorator
def existing_mnemonic(ctx: click.Context, mnemonic: str, mnemonic_password: str, **kwargs: Any) -> None:
    if mnemonic_password != '':
        click.clear()
        click.confirm(load_text('en', ['msg_mnemonic_password_confirm']), abort=True)

    ctx.obj = {'mnemonic': mnemonic, 'mnemonic_password': mnemonic_password}
    ctx.forward(generate_keys)
