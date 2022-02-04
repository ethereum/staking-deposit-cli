import click
from typing import (
    Any,
)

from staking_deposit.key_handling.key_derivation.mnemonic import (
    get_mnemonic,
)
from staking_deposit.utils.click import (
    captive_prompt_callback,
    choice_prompt_func,
    jit_option,
)
from staking_deposit.utils.constants import (
    MNEMONIC_LANG_OPTIONS,
    WORD_LISTS_PATH,
)
from staking_deposit.utils.intl import (
    fuzzy_reverse_dict_lookup,
    load_text,
    get_first_options,
)

from .generate_keys import (
    generate_keys,
    generate_keys_arguments_decorator,
)

languages = get_first_options(MNEMONIC_LANG_OPTIONS)


@click.command(
    help=load_text(['arg_new_mnemonic', 'help'], func='new_mnemonic'),
)
@click.pass_context
@jit_option(
    callback=captive_prompt_callback(
        lambda mnemonic_language: fuzzy_reverse_dict_lookup(mnemonic_language, MNEMONIC_LANG_OPTIONS),
        choice_prompt_func(lambda: load_text(['arg_mnemonic_language', 'prompt'], func='new_mnemonic'), languages),
    ),
    default=lambda: load_text(['arg_mnemonic_language', 'default'], func='new_mnemonic'),
    help=lambda: load_text(['arg_mnemonic_language', 'help'], func='new_mnemonic'),
    param_decls='--mnemonic_language',
    prompt=choice_prompt_func(lambda: load_text(['arg_mnemonic_language', 'prompt'], func='new_mnemonic'), languages),
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
