import os
import click
from typing import (
    Any,
    Callable,
)
from eth_utils import decode_hex

from eth2deposit.credentials import (
    CredentialList,
)
from eth2deposit.exceptions import ValidationError
from eth2deposit.utils.validation import (
    verify_deposit_data_json,
    validate_password_strength,
)
from eth2deposit.utils.constants import (
    BLS_WITHDRAWAL_PREFIX,
    MAX_DEPOSIT_AMOUNT,
    DEFAULT_VALIDATOR_KEYS_FOLDER_NAME,
)
from eth2deposit.utils.ascii_art import RHINO_0
from eth2deposit.settings import (
    ALL_CHAINS,
    MAINNET,
    get_setting,
)


def get_password(text: str) -> str:
    return click.prompt(text, hide_input=True, show_default=False, type=str)


def validate_password(cts: click.Context, param: Any, password: str) -> str:
    is_valid_password = False

    # The given password has passed confirmation
    try:
        validate_password_strength(password)
    except ValidationError as e:
        click.echo(f'Error: {e} Please retype.')
    else:
        is_valid_password = True

    while not is_valid_password:
        password = get_password(text='Type the password that secures your validator keystore(s)')
        try:
            validate_password_strength(password)
        except ValidationError as e:
            click.echo(f'Error: {e} Please retype.')
        else:
            # Confirm password
            password_confirmation = get_password(text='Repeat for confirmation')
            if password == password_confirmation:
                is_valid_password = True
            else:
                click.echo('Error: the two entered values do not match. Please retype again.')

    return password


def validate_withdrawal_credentials(withdrawal_credentials: str) -> None:
    try:
        decoded_withdrawal_credentials = decode_hex(withdrawal_credentials)
    except Exception:
        raise ValueError("Wrong withdrawal_credentials value.")
    if len(decoded_withdrawal_credentials) != 32 or decoded_withdrawal_credentials[:1] != BLS_WITHDRAWAL_PREFIX:
        raise ValidationError("Wrong withdrawal_credentials format.")


def generate_keys_arguments_decorator(function: Callable[..., Any]) -> Callable[..., Any]:
    '''
    This is a decorator that, when applied to a parent-command, implements the
    to obtain the necessary arguments for the generate_keys() subcommand.
    '''
    decorators = [
        click.option(
            '--num_validators',
            prompt='Please choose how many validators you wish to run',
            help='The number of validators keys you want to generate (you can always generate more later)',
            required=True,
            type=click.IntRange(0, 2**32 - 1),
        ),
        click.option(
            '--folder',
            default=os.getcwd(),
            help='The folder to place the generated keystores and deposit_data.json in',
            type=click.Path(exists=True, file_okay=False, dir_okay=True),
        ),
        click.option(
            '--chain',
            default=MAINNET,
            help='The version of eth2 you are targeting. use "mainnet" if you are depositing ETH',
            prompt='Please choose the (mainnet or testnet) network/chain name',
            type=click.Choice(ALL_CHAINS.keys(), case_sensitive=False),
        ),
        click.password_option(
            '--keystore_password',
            callback=validate_password,
            help=('The password that will secure your keystores. You will need to re-enter this to decrypt them when '
                  'you setup your eth2 validators. (It is reccomened not to use this argument, and wait for the CLI '
                  'to ask you for your mnemonic as otherwise it will appear in your shell history.)'),
            prompt='Type the password that secures your validator keystore(s)',
        ),
        click.option(
            '--withdrawal_credentials',
            default='',
            help=("The pre-defined withdrawal_credentials in hex string. If it's unset, the CLI will use the "
                  "withdrawal key created by the mnemonic to generate the withdrawal_credentials"),
            type=str,
        ),
    ]
    for decorator in reversed(decorators):
        function = decorator(function)
    return function


@click.command()
@click.pass_context
def generate_keys(ctx: click.Context, validator_start_index: int,
                  num_validators: int, folder: str, chain: str,
                  keystore_password: str, withdrawal_credentials: str, **kwargs: Any) -> None:
    if withdrawal_credentials == "":
        assigned_withdrawal_credentials = None
    else:
        validate_withdrawal_credentials(withdrawal_credentials)
        assigned_withdrawal_credentials = decode_hex(withdrawal_credentials)

    mnemonic = ctx.obj['mnemonic']
    mnemonic_password = ctx.obj['mnemonic_password']
    amounts = [MAX_DEPOSIT_AMOUNT] * num_validators
    folder = os.path.join(folder, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
    setting = get_setting(chain)
    if not os.path.exists(folder):
        os.mkdir(folder)
    click.clear()
    click.echo(RHINO_0)
    click.echo('Creating your keys.')
    credential_list = CredentialList.from_mnemonic(
        mnemonic=mnemonic,
        mnemonic_password=mnemonic_password,
        num_keys=num_validators,
        amounts=amounts,
        fork_version=setting.GENESIS_FORK_VERSION,
        start_index=validator_start_index,
    )
    keystore_filefolders = credential_list.export_keystores(password=keystore_password, folder=folder)
    deposits_file = credential_list.export_deposit_data_json(
        folder=folder,
        assigned_withdrawal_credentials=assigned_withdrawal_credentials,
    )
    if assigned_withdrawal_credentials is None:
        withdrawal_credentials_list = tuple([c.withdrawal_credentials for c in credential_list.credentials])
    else:
        withdrawal_credentials_list = (assigned_withdrawal_credentials,) * len(credential_list.credentials)
    if not credential_list.verify_keystores(keystore_filefolders=keystore_filefolders, password=keystore_password):
        raise ValidationError("Failed to verify the keystores.")
    if not verify_deposit_data_json(deposits_file, withdrawal_credentials_list):
        raise ValidationError("Failed to verify the deposit data JSON files.")
    click.echo('\nSuccess!\nYour keys can be found at: %s' % folder)
    click.pause('\n\nPress any key.')
