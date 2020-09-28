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


def validate_mnemonic(mnemonic: str) -> str:
    if verify_mnemonic(mnemonic, WORD_LISTS_PATH):
        return mnemonic
    else:
        raise click.BadParameter('That is not a valid mnemonic in any language.')


@click.command()
@click.pass_context
@generate_keys_arguments_decorator
@click.option(
    '--mnemonic',
    prompt='Please enter your mnemonic separated by spaces (" ").',
    required=True,
    type=str,
)
@click.option(
    '--mnemonic-password',
    type=str,
    default='',
)
def existing_mnemonic(ctx: click.Context, mnemonic: str, mnemonic_password: str, **kwargs: Any) -> None:
    ctx.obj = {'mnemonic': mnemonic, 'mnemonic_password': mnemonic_password}
    ctx.forward(generate_keys)
