import os

from click.testing import CliRunner

from staking_deposit.deposit import cli
from staking_deposit.utils.constants import DEFAULT_BLS_TO_EXECUTION_CHANGES_FOLDER_NAME
from .helpers import (
    clean_btec_folder,
    get_permissions,
)


def test_existing_mnemonic_bls_withdrawal() -> None:
    # Prepare folder
    my_folder_path = os.path.join(os.getcwd(), 'TESTING_TEMP_FOLDER')
    clean_btec_folder(my_folder_path)
    if not os.path.exists(my_folder_path):
        os.mkdir(my_folder_path)

    runner = CliRunner()
    inputs = ['0']  # confirm `validator_start_index`
    data = '\n'.join(inputs)
    arguments = [
        '--language', 'english',
        'generate-bls-to-execution-change',
        '--bls_to_execution_changes_folder', my_folder_path,
        '--chain', 'mainnet',
        '--fork', 'capella',
        '--mnemonic', 'sister protect peanut hill ready work profit fit wish want small inflict flip member tail between sick setup bright duck morning sell paper worry',  # noqa: E501
        '--bls_withdrawal_credentials', '00bd0b5a34de5fb17df08410b5e615dda87caf4fb72d0aac91ce5e52fc6aa8de',
        '--validator_start_index', '0',
        '--validator_index', '1',
        '--execution_address', '3434343434343434343434343434343434343434',
    ]
    result = runner.invoke(cli, arguments, input=data)
    assert result.exit_code == 0

    # Check files
    bls_to_execution_changes_folder_path = os.path.join(my_folder_path, DEFAULT_BLS_TO_EXECUTION_CHANGES_FOLDER_NAME)
    _, _, btec_files = next(os.walk(bls_to_execution_changes_folder_path))

    # TODO verify file content
    assert len(set(btec_files)) == 1

    # Verify file permissions
    if os.name == 'posix':
        for file_name in btec_files:
            assert get_permissions(bls_to_execution_changes_folder_path, file_name) == '0o440'

    # Clean up
    clean_btec_folder(my_folder_path)
