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
from eth2deposit.utils.validation import verify_deposit_data_json
from eth2deposit.utils.constants import (
    MAX_DEPOSIT_AMOUNT,
    DEFAULT_VALIDATOR_KEYS_FOLDER_NAME,
)
from eth2deposit.utils.ascii_art import RHINO_0
from eth2deposit.settings import (
    ALL_CHAINS,
    MAINNET,
    get_setting,
)


def generate_keys_arguments_decorator(function: Callable[..., Any]) -> Callable[..., Any]:
    '''
    This is a decorator that, when applied to a parent-command, implements the
    to obtain the necessary arguments for the generate_keys() subcommand.
    '''
    decorators = [
        click.option(
            '--num_validators',
            prompt='Please choose how many validators you wish to run',
            required=True,
            type=click.IntRange(0, 2**32),
        ),
        click.option(
            '--folder',
            type=click.Path(exists=True, file_okay=False, dir_okay=True),
            default=os.getcwd()
        ),
        click.option(
            '--chain',
            prompt='Please choose the (mainnet or testnet) network/chain name',
            type=click.Choice(ALL_CHAINS.keys(), case_sensitive=False),
            default=MAINNET,
        ),
        click.password_option('--keystore_password', prompt='Type the password that secures your validator keystore(s)')
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
    setting = get_setting(chain)
    if not os.path.exists(folder):
        os.mkdir(folder)
    click.clear()
    click.echo(RHINO_0)
    click.echo('Creating your keys.')
    credentials = CredentialList.from_mnemonic(
        mnemonic=mnemonic,
        mnemonic_password=mnemonic_password,
        num_keys=num_validators,
        amounts=amounts,
        fork_version=setting.GENESIS_FORK_VERSION,
        start_index=validator_start_index,
    )
    click.echo('Saving your keystore(s).')
    keystore_filefolders = credentials.export_keystores(password=keystore_password, folder=folder)
    click.echo('Creating your deposit(s).')
    deposits_file = credentials.export_deposit_data_json(folder=folder)
    click.echo('Verifying your keystore(s).')
    if not credentials.verify_keystores(keystore_filefolders=keystore_filefolders, password=keystore_password):
        raise ValidationError("Failed to verify the keystores.")
    click.echo('Verifying your deposit(s).')
    if not verify_deposit_data_json(deposits_file):
        raise ValidationError("Failed to verify the deposit data JSON files.")
    click.echo('\nSuccess!\nYour keys can be found at: %s' % folder)
    click.pause('\n\nPress any key.')
