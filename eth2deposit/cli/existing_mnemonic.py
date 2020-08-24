import click
from typing import (
    Tuple,
)

from key_handling.key_derivation.mnemonic import (
    verify_mnemonic,
)
from utils.constants import (
    WORD_LISTS_PATH,
)


def validate_mnemonic(mnemonic: str) -> str:
    if verify_mnemonic(mnemonic, WORD_LISTS_PATH):
        return mnemonic
    else:
        raise click.BadParameter('That is not a valid mnemonic in any language.')


@click.command()
@click.option(
    '--mnemonic',
    prompt='Please enter your mnemonic separated by spaces (" ").',
    required=True,
    type=str,
)
@click.option(
    '--mnemonic-password',
    type=str,
    defualt='',
)
def existing_mnemonic(mnemonic: str, mnemonic_password: str) -> Tuple[str, str]:
    return (mnemonic, mnemonic_password)
