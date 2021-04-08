import click
from typing import (
    Any,
)
import sys

from eth2deposit.cli.existing_mnemonic import existing_mnemonic
from eth2deposit.cli.new_mnemonic import new_mnemonic
from eth2deposit.utils import config
from eth2deposit.utils.constants import INTL_LANG_OPTIONS
from eth2deposit.utils.intl import (
    get_first_options,
    fuzzy_reverse_dict_lookup,
    load_text,
)
from eth2deposit.exceptions import ValidationError


def check_python_version() -> None:
    '''
    Checks that the python version running is sufficient and exits if not.
    '''
    if sys.version_info < (3, 7):
        click.pause(load_text(['err_python_version']))
        sys.exit()


def process_language_callback(ctx: click.Context, param: Any, language: str) -> str:
    '''
    Validates the selected language and returns its ISO 639-1 name.
    '''
    while True:
        try:
            return fuzzy_reverse_dict_lookup(language, INTL_LANG_OPTIONS)
        except ValidationError:
            language = click.prompt('Please select a valid language (%s): ' % get_first_options(INTL_LANG_OPTIONS))


@click.group()
@click.pass_context
@click.option(
    '--language',
    callback=process_language_callback,
    default='English',
    prompt='Please choose your language (%s)' % get_first_options(INTL_LANG_OPTIONS),
    required=True,
    type=str,
)
def cli(ctx: click.Context, language: str) -> None:
    config.language = language


cli.add_command(existing_mnemonic)
cli.add_command(new_mnemonic)


if __name__ == '__main__':
    check_python_version()
    cli()
