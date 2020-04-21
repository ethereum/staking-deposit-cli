import os
import sys
import click

from key_handling.key_derivation.mnemonic import (
    get_languages,
    get_mnemonic,
)
from utils.eth2_deposit_check import verify_deposit_data_json
from utils.credentials import (
    mnemonic_to_credentials,
    export_keystores,
    export_deposit_data_json,
    verify_keystores,
)
from utils.constants import (
    WORD_LISTS_PATH,
    MAX_DEPOSIT_AMOUNT,
)
from utils.ascii_art import RHINO_0

words_path = os.path.join(os.getcwd(), WORD_LISTS_PATH)
languages = get_languages(words_path)


def generate_mnemonic(language: str, words_path: str) -> str:
    mnemonic = get_mnemonic(language=language, words_path=words_path)
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
    return mnemonic


def check_python_version():
    '''
    Checks that the python version running is sufficient and exits if not.
    '''
    if sys.version_info < (3, 7):
        click.pause('Your python version is insufficient, please install version 3.7 or greater.')
        sys.exit()


@click.command()
@click.option(
    '--num_validators',
    prompt='Please choose how many validators you wish to run',
    required=True,
    type=int,
)
@click.password_option(prompt='Type the password that secures your validator keystore(s)')
@click.option(
    '--mnemonic_language',
    prompt='Please choose your mnemonic language',
    type=click.Choice(languages, case_sensitive=False),  # type: ignore
    default='english',
)
@click.option(
    '--folder',
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=os.getcwd()
)
def main(num_validators: int, mnemonic_language: str, password: str, folder: str):
    check_python_version()
    mnemonic = generate_mnemonic(mnemonic_language, words_path)
    amounts = [MAX_DEPOSIT_AMOUNT] * num_validators
    folder = os.path.join(folder, 'validator_keys')
    if not os.path.exists(folder):
        os.mkdir(folder)
    click.clear()
    click.echo(RHINO_0)
    click.echo('Creating your keys.')
    credentials = mnemonic_to_credentials(mnemonic=mnemonic, num_keys=num_validators, amounts=amounts)
    click.echo('Saving your keystore(s).')
    keystore_filefolders = export_keystores(credentials=credentials, password=password, folder=folder)
    click.echo('Creating your deposit(s).')
    deposits_file = export_deposit_data_json(credentials=credentials, folder=folder)
    click.echo('Verifying your keystore(s).')
    assert verify_keystores(credentials=credentials, keystore_filefolders=keystore_filefolders, password=password)
    click.echo('Verifying your deposit(s).')
    assert verify_deposit_data_json(deposits_file)
    click.echo('\nSuccess!\nYour keys can be found at: %s' % folder)
    click.pause('\n\nPress any key.')


if __name__ == '__main__':
    main()
