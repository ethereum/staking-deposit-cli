import click
from typing import (
    Any,
)
import sys

from eth2deposit.cli.existing_mnemonic import existing_mnemonic
from eth2deposit.cli.new_mnemonic import new_mnemonic
from eth2deposit.utils import config
from eth2deposit.utils.intl import (
    get_language_iso_name,
    get_translation_languages,
    load_text,
)


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
            return get_language_iso_name(language)
        except KeyError:
            click.echo('Please select a valid language: (%s)' % get_translation_languages())


@click.group()
@click.pass_context
@click.option(
    '--language',
    callback=process_language_callback,
    default='English',
    prompt='Please choose your language (%s)' % get_translation_languages(),
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
