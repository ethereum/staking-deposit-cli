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
from .generate_keys import (
    generate_keys,
    generate_keys_arguments_decorator,
)


def validate_mnemonic(cts: click.Context, param: Any, mnemonic: str) -> str:
    if verify_mnemonic(mnemonic, WORD_LISTS_PATH):
        return mnemonic
    else:
        raise ValidationError('That is not a valid mnemonic, please check for typos.')


@click.command(
    help='Generate (or recover) keys from an existing mnemonic',
)
@click.pass_context
@click.option(
    '--mnemonic',
    callback=validate_mnemonic,
    help=('The mnemonic that you used to generate your keys. (It is recommended not to use this argument, and wait for '
          'the CLI to ask you for your mnemonic as otherwise it will appear in your shell history.)'),
    prompt='Please enter your mnemonic separated by spaces (" ")',
    required=True,
    type=str,
)
@click.password_option(
    '--mnemonic-password',
    default='',
    help=('This is almost certainly not the argument you are looking for: it is for mnemonic passwords, not keystore '
          'passwords. Providing a password here when you didn\'t use one initially, can result in lost keys (and '
          'therefore funds)! Also note that if you used this tool to generate your mnemonic intially, then you did not '
          'use a mnemonic password. However, if you are certain you used a password to "increase" the security of your '
          'mnemonic, this is where you enter it.'),
    prompt=False,
)
@click.option(
    '--validator_start_index',
    confirmation_prompt=True,
    default=0,
    help=('Enter the index (key number) you wish to start generating more keys from. '
          'For example, if you\'ve generated 4 keys in the past, you\'d enter 4 here,'),
    prompt=('Enter the index (key number) you wish to start generating more keys from. '
            'For example, if you\'ve generated 4 keys in the past, you\'d enter 4 here,'),
    type=click.IntRange(0, 2**32 - 1),
)
@generate_keys_arguments_decorator
def existing_mnemonic(ctx: click.Context, mnemonic: str, mnemonic_password: str, **kwargs: Any) -> None:
    if mnemonic_password != '':
        click.clear()
        click.confirm(
            ('Are you absolutely certain that you used a mnemonic password? '
             '(This is different from a keystore password!) '
             'Using one when you are not supposed to can result in loss of funds!'),
            abort=True)

    ctx.obj = {'mnemonic': mnemonic, 'mnemonic_password': mnemonic_password}
    ctx.forward(generate_keys)
