import click
from typing import (
    Any,
)

from eth2deposit.key_handling.key_derivation.mnemonic import (
    get_languages,
    get_mnemonic,
)
from eth2deposit.utils.constants import WORD_LISTS_PATH

from .generate_keys import (
    generate_keys,
    generate_keys_arguments_decorator,
)

languages = get_languages(WORD_LISTS_PATH)


@click.command(
    help='Generate a new mnemonic and keys',
)
@click.pass_context
@click.option(
    '--mnemonic_language',
    default='english',
    help='The language that your mnemonic is in.',
    prompt='Please choose your mnemonic language',
    type=click.Choice(languages, case_sensitive=False),
)
@generate_keys_arguments_decorator
def new_mnemonic(ctx: click.Context, mnemonic_language: str, **kwargs: Any) -> None:
    mnemonic = get_mnemonic(language=mnemonic_language, words_path=WORD_LISTS_PATH)
    test_mnemonic = ''
    while mnemonic != test_mnemonic:
        click.clear()
        click.echo('This is your seed phrase. Write it down and store it safely, it is the ONLY way to retrieve your deposit.')  # noqa: E501
        click.echo('\n\n%s\n\n' % mnemonic)
        click.pause('Press any key when you have written down your mnemonic.')

        click.clear()
        test_mnemonic = click.prompt('Please type your mnemonic (separated by spaces) to confirm you have written it down\n\n')  # noqa: E501
        test_mnemonic = test_mnemonic.lower()
    click.clear()
    # Do NOT use mnemonic_password.
    ctx.obj = {'mnemonic': mnemonic, 'mnemonic_password': ''}
    ctx.params['validator_start_index'] = 0
    ctx.forward(generate_keys)
