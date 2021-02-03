import os
import click
from typing import (
    Any,
    Callable,
)

from eth2deposit.credentials import (
    CredentialList,
)
from eth2deposit.exceptions import ValidationError
from eth2deposit.utils.validation import (
    verify_deposit_data_json,
    validate_password_strength,
)
from eth2deposit.utils.constants import (
    MAX_DEPOSIT_AMOUNT,
    DEFAULT_VALIDATOR_KEYS_FOLDER_NAME,
)
from eth2deposit.utils.ascii_art import RHINO_0
from eth2deposit.settings import (
    ALL_CHAINS,
    MAINNET,
    get_chain_setting,
)


def get_password(text: str) -> str:
    return click.prompt(text, hide_input=True, show_default=False, type=str)


def validate_password(cts: click.Context, param: Any, password: str) -> str:
    is_valid_password = False

    # The given password has passed confirmation
    try:
        validate_password_strength(password)
    except ValidationError as e:
        click.echo(f'Error: {e} Please retype.') # Translate
    else:
        is_valid_password = True

    while not is_valid_password:
        password = get_password(text='Type the password that secures your validator keystore(s)') # Translate
        try:
            validate_password_strength(password)
        except ValidationError as e:
            click.echo(f'Error: {e} Please retype.') # Translate
        else:
            # Confirm password
            password_confirmation = get_password(text='Repeat for confirmation') # Translate
            if password == password_confirmation:
                is_valid_password = True
            else:
                click.echo('Error: the two entered values do not match. Please retype again.') # Translate

    return password


def generate_keys_arguments_decorator(function: Callable[..., Any]) -> Callable[..., Any]:
    '''
    This is a decorator that, when applied to a parent-command, implements the
    to obtain the necessary arguments for the generate_keys() subcommand.
    ''' # Do not translate
    decorators = [
        click.option(
            '--num_validators', # Do not translate
            prompt='Please choose how many validators you wish to run', # Translate
            help='The number of validators keys you want to generate (you can always generate more later)', # Translate
            required=True,
            type=click.IntRange(0, 2**32 - 1),
        ),
        click.option(
            '--folder', # Do not translate
            default=os.getcwd(),
            help='The folder to place the generated keystores and deposit_data.json in', # Translate
            type=click.Path(exists=True, file_okay=False, dir_okay=True),
        ),
        click.option(
            '--chain', # Do not translate
            default=MAINNET,
            help='The version of eth2 you are targeting. use "mainnet" if you are depositing ETH', # Translate
            prompt='Please choose the (mainnet or testnet) network/chain name', # Translate all except "mainnet" and "testnet"
            type=click.Choice(ALL_CHAINS.keys(), case_sensitive=False),
        ),
        click.password_option(
            '--keystore_password', # Do not translate
            callback=validate_password,
            help=('The password that will secure your keystores. You will need to re-enter this to decrypt them when '
                  'you setup your eth2 validators. (It is recommended not to use this argument, and wait for the CLI '
                  'to ask you for your mnemonic as otherwise it will appear in your shell history.)'), # Translate
            prompt='Type the password that secures your validator keystore(s)', # Translate
        ),
    ]
    for decorator in reversed(decorators):
        function = decorator(function)
    return function


@click.command()
@click.pass_context
def generate_keys(ctx: click.Context, validator_start_index: int,
                  num_validators: int, folder: str, chain: str, keystore_password: str, **kwargs: Any) -> None:
    mnemonic = ctx.obj['mnemonic']
    mnemonic_password = ctx.obj['mnemonic_password']
    amounts = [MAX_DEPOSIT_AMOUNT] * num_validators
    folder = os.path.join(folder, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
    chain_setting = get_chain_setting(chain)
    if not os.path.exists(folder):
        os.mkdir(folder)
    click.clear()
    click.echo(RHINO_0)
    click.echo('Creating your keys.') # Translate
    credentials = CredentialList.from_mnemonic(
        mnemonic=mnemonic,
        mnemonic_password=mnemonic_password,
        num_keys=num_validators,
        amounts=amounts,
        chain_setting=chain_setting,
        start_index=validator_start_index,
    )
    keystore_filefolders = credentials.export_keystores(password=keystore_password, folder=folder)
    deposits_file = credentials.export_deposit_data_json(folder=folder)
    if not credentials.verify_keystores(keystore_filefolders=keystore_filefolders, password=keystore_password):
        raise ValidationError("Failed to verify the keystores.") # Translate
    if not verify_deposit_data_json(deposits_file):
        raise ValidationError("Failed to verify the deposit data JSON files.") # Translate
    click.echo('\nSuccess!\nYour keys can be found at: %s' % folder) # Translate
    click.pause('\n\nPress any key.') # Translate
