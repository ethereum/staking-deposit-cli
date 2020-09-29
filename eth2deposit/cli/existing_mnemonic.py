import click
from typing import (
    Any,
)

from eth2deposit.key_handling.key_derivation.mnemonic import (
    verify_mnemonic,
)
from eth2deposit.utils.constants import (
    WORD_LISTS_PATH,
)
from .generate_keys import (
    generate_keys,
    generate_keys_arguments_decorator,
)


def validate_mnemonic(cts: click.Context, param: Any, mnemonic: str) -> str:
    if verify_mnemonic(mnemonic, WORD_LISTS_PATH):
        return mnemonic
    else:
        raise click.BadParameter('That is not a valid mnemonic, please check for typos')


@click.command()
@click.pass_context
@click.option(
    '--mnemonic',
    callback=validate_mnemonic,
    prompt='Please enter your mnemonic separated by spaces (" ")',
    required=True,
    type=str,
)
@click.password_option(
    '--mnemonic-password',
    default='',
)
@click.option(
    '--validator_start_index',
    confirmation_prompt=True,
    default=0,
    prompt='Enter the index (key number) you wish to start generating more keys from. \
            For example, if you\'ve generated 4 keys in the past, you\'d enter 4 here,',
    type=click.IntRange(0, 2**32),
)
@generate_keys_arguments_decorator
def existing_mnemonic(ctx: click.Context, mnemonic: str, mnemonic_password: str, **kwargs: Any) -> None:
    ctx.obj = {'mnemonic': mnemonic, 'mnemonic_password': mnemonic_password}
    ctx.forward(generate_keys)
