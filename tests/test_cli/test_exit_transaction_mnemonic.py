import os

from click.testing import CliRunner

from staking_deposit.deposit import cli
from staking_deposit.utils.constants import DEFAULT_EXIT_TRANSACTION_FOLDER_NAME

from tests.test_cli.helpers import clean_exit_transaction_folder, read_json_file, verify_file_permission


def test_exit_transaction_menmonic() -> None:
    # Prepare folder
    my_folder_path = os.path.join(os.getcwd(), 'TESTING_TEMP_FOLDER')
    clean_exit_transaction_folder(my_folder_path)
    if not os.path.exists(my_folder_path):
        os.mkdir(my_folder_path)

    runner = CliRunner()
    inputs = []
    data = '\n'.join(inputs)
    arguments = [
        '--language', 'english',
        '--non_interactive',
        'exit-transaction-mnemonic',
        '--output_folder', my_folder_path,
        '--chain', 'mainnet',
        '--mnemonic', 'aban aban aban aban aban aban aban aban aban aban aban abou',
        '--validator_start_index', '0',
        '--validator_indices', '1',
        '--epoch', '1234',
    ]
    result = runner.invoke(cli, arguments, input=data)

    assert result.exit_code == 0

    # Check files
    exit_transaction_folder_path = os.path.join(my_folder_path, DEFAULT_EXIT_TRANSACTION_FOLDER_NAME)
    _, _, exit_transaction_files = next(os.walk(exit_transaction_folder_path))

    assert len(set(exit_transaction_files)) == 1

    json_data = read_json_file(exit_transaction_folder_path, exit_transaction_files[0])

    # Verify file content
    assert json_data['message']['epoch'] == '1234'
    assert json_data['message']['validator_index'] == '1'
    assert json_data['signature']

    # Verify file permissions
    verify_file_permission(os, folder_path=exit_transaction_folder_path, files=exit_transaction_files)

    # Clean up
    clean_exit_transaction_folder(my_folder_path)


def test_exit_transaction_menmonic_multiple() -> None:
    # Prepare folder
    my_folder_path = os.path.join(os.getcwd(), 'TESTING_TEMP_FOLDER')
    clean_exit_transaction_folder(my_folder_path)
    if not os.path.exists(my_folder_path):
        os.mkdir(my_folder_path)

    runner = CliRunner()
    inputs = []
    data = '\n'.join(inputs)
    arguments = [
        '--language', 'english',
        '--non_interactive',
        'exit-transaction-mnemonic',
        '--output_folder', my_folder_path,
        '--chain', 'mainnet',
        '--mnemonic', 'aban aban aban aban aban aban aban aban aban aban aban abou',
        '--validator_start_index', '0',
        '--validator_indices', '0 1 2 3',
        '--epoch', '1234',
    ]
    result = runner.invoke(cli, arguments, input=data)

    assert result.exit_code == 0

    # Check files
    exit_transaction_folder_path = os.path.join(my_folder_path, DEFAULT_EXIT_TRANSACTION_FOLDER_NAME)
    _, _, exit_transaction_files = next(os.walk(exit_transaction_folder_path))

    assert len(set(exit_transaction_files)) == 4

    # Verify file content
    exit_transaction_files.sort()
    for index in [0, 1, 2, 3]:
        json_data = read_json_file(exit_transaction_folder_path, exit_transaction_files[index])
        assert json_data['message']['epoch'] == '1234'
        assert json_data['message']['validator_index'] == str(index)
        assert json_data['signature']

    # Verify file permissions
    verify_file_permission(os, folder_path=exit_transaction_folder_path, files=exit_transaction_files)

    # Clean up
    clean_exit_transaction_folder(my_folder_path)
