import click
from typing import (
    Any,
)

from eth2deposit.key_handling.key_derivation.mnemonic import (
    get_languages,
    get_mnemonic,
)
from eth2deposit.utils.constants import WORD_LISTS_PATH
from eth2deposit.utils.intl import load_text

from .generate_keys import (
    generate_keys,
    generate_keys_arguments_decorator,
)

languages = get_languages(WORD_LISTS_PATH)


@click.command(
    help=load_text('en', ['arg_new_mnemonic', 'help']),
)
@click.pass_context
@click.option(
    load_text('en', ['arg_mnemonic_language', 'argument']),
    default=load_text('en', ['arg_mnemonic_language', 'default']),
    help=load_text('en', ['arg_mnemonic_language', 'help']),
    prompt=load_text('en', ['arg_mnemonic_language', 'prompt']),
    type=click.Choice(languages, case_sensitive=False),
)
@generate_keys_arguments_decorator
def new_mnemonic(ctx: click.Context, mnemonic_language: str, **kwargs: Any) -> None:
    mnemonic = get_mnemonic(language=mnemonic_language, words_path=WORD_LISTS_PATH)
    test_mnemonic = ''
    while mnemonic != test_mnemonic:
        click.clear()
        click.echo(load_text('en', ['msg_mnemonic_presentation']))
        click.echo('\n\n%s\n\n' % mnemonic)
        click.pause(load_text('en', ['msg_press_any_key']))

        click.clear()
        test_mnemonic = click.prompt(load_text('en', ['msg_mnemonic_retype_prompt']))
        test_mnemonic = test_mnemonic.lower()
    click.clear()
    # Do NOT use mnemonic_password.
    ctx.obj = {'mnemonic': mnemonic, 'mnemonic_password': ''}
    ctx.params['validator_start_index'] = 0
    ctx.forward(generate_keys)
