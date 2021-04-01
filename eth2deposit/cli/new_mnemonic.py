import click
from typing import (
    Any,
)

from eth2deposit.key_handling.key_derivation.mnemonic import (
    get_languages,
    get_mnemonic,
)
from eth2deposit.utils.click import jit_option
from eth2deposit.utils.constants import WORD_LISTS_PATH
from eth2deposit.utils.intl import load_text

from .generate_keys import (
    generate_keys,
    generate_keys_arguments_decorator,
)

languages = get_languages(WORD_LISTS_PATH)


@click.command(
    help=load_text(['arg_new_mnemonic', 'help'], func='new_mnemonic'),
)
@click.pass_context
@jit_option(
    default=lambda: load_text(['arg_mnemonic_language', 'default'], func='new_mnemonic'),
    help=lambda: load_text(['arg_mnemonic_language', 'help'], func='new_mnemonic'),
    param_decls=lambda: load_text(['arg_mnemonic_language', 'argument'], func='new_mnemonic'),
    prompt=lambda: load_text(['arg_mnemonic_language', 'prompt'], func='new_mnemonic'),
    type=click.Choice(languages, case_sensitive=False),
)
@generate_keys_arguments_decorator
def new_mnemonic(ctx: click.Context, mnemonic_language: str, **kwargs: Any) -> None:
    mnemonic = get_mnemonic(language=mnemonic_language, words_path=WORD_LISTS_PATH)
    test_mnemonic = ''
    while mnemonic != test_mnemonic:
        click.clear()
        click.echo(load_text(['msg_mnemonic_presentation']))
        click.echo('\n\n%s\n\n' % mnemonic)
        click.pause(load_text(['msg_press_any_key']))

        click.clear()
        test_mnemonic = click.prompt(load_text(['msg_mnemonic_retype_prompt']) + '\n\n')
        test_mnemonic = test_mnemonic.lower()
    click.clear()
    # Do NOT use mnemonic_password.
    ctx.obj = {'mnemonic': mnemonic, 'mnemonic_password': ''}
    ctx.params['validator_start_index'] = 0
    ctx.forward(generate_keys)
