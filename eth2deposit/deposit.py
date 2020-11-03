import sys
import click

from eth2deposit.cli.existing_mnemonic import existing_mnemonic
from eth2deposit.cli.new_mnemonic import new_mnemonic


def check_python_version() -> None:
    '''
    Checks that the python version running is sufficient and exits if not.
    '''
    if sys.version_info < (3, 7):
        click.pause('Your python version is insufficient, please install version 3.7 or greater.')
        sys.exit()


@click.group()
def cli() -> None:
    pass


cli.add_command(existing_mnemonic)
cli.add_command(new_mnemonic)


if __name__ == '__main__':
    check_python_version()
    cli()
