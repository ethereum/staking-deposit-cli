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
from eth2deposit.utils.intl import load_text
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
        click.echo(e)
    else:
        is_valid_password = True

    while not is_valid_password:
        password = get_password(load_text('en', ['msg_password_prompt']))
        try:
            validate_password_strength(password)
        except ValidationError as e:
            click.echo(e)
        else:
            # Confirm password
            password_confirmation = get_password(load_text('en', ['msg_password_confirm']))
            if password == password_confirmation:
                is_valid_password = True
            else:
                click.echo(load_text('en', ['err_password_mismatch']))

    return password


def generate_keys_arguments_decorator(function: Callable[..., Any]) -> Callable[..., Any]:
    '''
    This is a decorator that, when applied to a parent-command, implements the
    to obtain the necessary arguments for the generate_keys() subcommand.
    '''
    decorators = [
        click.option(
            load_text('en', ['num_validators', 'argument']),
            help=load_text('en', ['num_validators', 'help']),
            prompt=load_text('en', ['num_validators', 'prompt']),
            required=True,
            type=click.IntRange(0, 2**32 - 1),
        ),
        click.option(
            load_text('en', ['folder', 'argument']),
            default=os.getcwd(),
            help=load_text('en', ['folder', 'help']),
            type=click.Path(exists=True, file_okay=False, dir_okay=True),
        ),
        click.option(
            load_text('en', ['chain', 'argument']),
            default=MAINNET,
            help=load_text('en', ['chain', 'help']),
            prompt=load_text('en', ['chain', 'prompt']),
            type=click.Choice(ALL_CHAINS.keys(), case_sensitive=False),
        ),
        click.password_option(
            load_text('en', ['keystore_password', 'argument']),
            callback=validate_password,
            help=load_text('en', ['keystore_password', 'help']),
            prompt=load_text('en', ['keystore_password', 'prompt']),
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
    click.echo(load_text('en', ['msg_key_creation']))
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
        raise ValidationError(load_text('en', ['err_verify_keystores']))
    if not verify_deposit_data_json(deposits_file):
        raise ValidationError(load_text('en', ['err_verify_deposit']))
    click.echo(load_text('en', ['msg_creation_success']) + folder)
    click.pause(load_text('en', ['msg_pause']))
