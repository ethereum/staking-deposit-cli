import os

from click.testing import CliRunner

from staking_deposit.credentials import Credential
from staking_deposit.deposit import cli
from staking_deposit.settings import get_chain_setting
from staking_deposit.utils.constants import DEFAULT_EXIT_TRANSACTION_FOLDER_NAME

from tests.test_cli.helpers import (
    clean_exit_transaction_folder,
    read_json_file,
    verify_file_permission,
)


def test_exit_transaction_menmonic() -> None:
    # Prepare folder
    my_folder_path = os.path.join(os.getcwd(), 'TESTING_TEMP_FOLDER')
    exit_transaction_folder_path = os.path.join(my_folder_path, DEFAULT_EXIT_TRANSACTION_FOLDER_NAME)
    clean_exit_transaction_folder(my_folder_path)
    if not os.path.exists(my_folder_path):
        os.mkdir(my_folder_path)
    if not os.path.exists(exit_transaction_folder_path):
        os.mkdir(exit_transaction_folder_path)


    # Shared parameters
    chain = 'mainnet'
    keystore_password = 'solo-stakers'

    # Prepare credential
    credential = Credential(
        mnemonic='sister protect peanut hill ready work profit fit wish want small inflict flip member tail between sick setup bright duck morning sell paper worry',
        mnemonic_password='',
        index=0,
        amount=0,
        chain_setting=get_chain_setting(chain),
        hex_eth1_withdrawal_address=None
    )

    # Save keystore file
    keystore_filepath = credential.save_signing_keystore(keystore_password, exit_transaction_folder_path)

    runner = CliRunner()
    inputs = []
    data = '\n'.join(inputs)
    arguments = [
        '--language', 'english',
        '--non_interactive',
        'exit-transaction-keystore',
        '--output_folder', my_folder_path,
        '--chain', chain,
        '--keystore', keystore_filepath,
        '--keystore_password', keystore_password,
        '--validator_index', '1',
        '--epoch', '1234',
    ]
    result = runner.invoke(cli, arguments, input=data)

    assert result.exit_code == 0

    # Check files
    _, _, exit_transaction_files = next(os.walk(exit_transaction_folder_path))

    # Filter files to signed_exit as keystore file will exist as well
    exit_transaction_files = [f for f in exit_transaction_files if 'signed_exit' in f]

    assert len(set(exit_transaction_files)) == 1

    json_data = read_json_file(exit_transaction_folder_path, exit_transaction_files[0])

    # Verify file content
    assert len(json_data) == 1
    assert json_data[0]['message']['epoch'] == '1234'
    assert json_data[0]['message']['validator_index'] == '1'

    # Verify file permissions
    verify_file_permission(os, folder_path=exit_transaction_folder_path, files=exit_transaction_files)

    # Clean up
    clean_exit_transaction_folder(my_folder_path)
