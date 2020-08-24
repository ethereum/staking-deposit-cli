import sys
import click

from eth2deposit.credentials import (
    CredentialList,
)
from eth2deposit.key_handling.key_derivation.mnemonic import (
    get_languages,
    get_mnemonic,
)
from eth2deposit.utils.validation import verify_deposit_data_json
from eth2deposit.utils.constants import (
    WORD_LISTS_PATH,
    MAX_DEPOSIT_AMOUNT,
    DEFAULT_VALIDATOR_KEYS_FOLDER_NAME,
)
from eth2deposit.utils.ascii_art import RHINO_0
from eth2deposit.settings import (
    ALL_CHAINS,
    MAINNET,
    get_setting,
)

languages = get_languages(WORD_LISTS_PATH)

@click.command()
@click.option(
    '--mnemonic_language',
    prompt='Please choose your mnemonic language',
    type=click.Choice(languages, case_sensitive=False),
    default='english',
)
def generate_mnemonic(mnemonic_language: str) -> str:
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
    return mnemonic
