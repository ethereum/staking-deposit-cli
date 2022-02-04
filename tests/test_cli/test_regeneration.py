import json
import os
from pathlib import Path

from click.testing import CliRunner
from staking_deposit.cli import new_mnemonic
from staking_deposit.deposit import cli
from staking_deposit.utils.constants import DEFAULT_VALIDATOR_KEYS_FOLDER_NAME
from .helpers import clean_key_folder, get_permissions, get_uuid


def test_regeneration(monkeypatch) -> None:
    # Part 1: new-mnemonic

    # monkeypatch get_mnemonic
    mock_mnemonic = "legal winner thank year wave sausage worth useful legal winner thank yellow"

    def mock_get_mnemonic(language, words_path, entropy=None) -> str:
        return mock_mnemonic

    monkeypatch.setattr(new_mnemonic, "get_mnemonic", mock_get_mnemonic)

    # Prepare folder
    folder_path_1 = os.path.join(os.getcwd(), 'TESTING_TEMP_FOLDER_1')
    folder_path_2 = os.path.join(os.getcwd(), 'TESTING_TEMP_FOLDER_2')
    clean_key_folder(folder_path_1)
    clean_key_folder(folder_path_2)
    if not os.path.exists(folder_path_1):
        os.mkdir(folder_path_1)
    if not os.path.exists(folder_path_2):
        os.mkdir(folder_path_2)

    runner = CliRunner()
    # Create index 0 and 1
    my_password = "MyPassword"
    inputs = ['english', 'english', '2', 'mainnet', my_password, my_password, mock_mnemonic]
    data = '\n'.join(inputs)
    result = runner.invoke(cli, ['new-mnemonic', '--folder', folder_path_1], input=data)
    assert result.exit_code == 0

    # Check files
    validator_keys_folder_path_1 = os.path.join(folder_path_1, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
    _, _, files = next(os.walk(validator_keys_folder_path_1))
    part_1_key_files = sorted([key_file for key_file in files if key_file.startswith('keystore')])

    all_uuid = [get_uuid(validator_keys_folder_path_1 + '/' + key_file)
                for key_file in part_1_key_files]
    assert len(set(all_uuid)) == 2

    # Verify file permissions
    if os.name == 'posix':
        for file_name in part_1_key_files:
            assert get_permissions(validator_keys_folder_path_1, file_name) == '0o440'

    # Part 2: existing-mnemonic
    runner = CliRunner()
    # Create index 1 and 2
    inputs = [
        'english',
        mock_mnemonic,
        '1', '1', '2', 'mainnet', 'MyPassword', 'MyPassword']
    data = '\n'.join(inputs)
    arguments = ['existing-mnemonic', '--folder', folder_path_2]
    result = runner.invoke(cli, arguments, input=data)

    assert result.exit_code == 0

    # Check files
    validator_keys_folder_path_2 = os.path.join(folder_path_2, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
    _, _, files = next(os.walk(validator_keys_folder_path_2))
    part_2_key_files = sorted([key_file for key_file in files if key_file.startswith('keystore')])

    all_uuid = [get_uuid(validator_keys_folder_path_2 + '/' + key_file)
                for key_file in part_2_key_files]
    assert len(set(all_uuid)) == 2

    # Finally:
    # Check the index=1 files have the same pubkey
    assert '1_0_0' in part_1_key_files[1] and '1_0_0' in part_2_key_files[0]
    with open(Path(validator_keys_folder_path_1 + '/' + part_1_key_files[1])) as f:
        keystore_1_1 = json.load(f)
    with open(Path(validator_keys_folder_path_2 + '/' + part_2_key_files[0])) as f:
        keystore_2_0 = json.load(f)
    assert keystore_1_1['pubkey'] == keystore_2_0['pubkey']
    assert keystore_1_1['path'] == keystore_2_0['path']

    # Verify file permissions
    if os.name == 'posix':
        for file_name in part_2_key_files:
            assert get_permissions(validator_keys_folder_path_2, file_name) == '0o440'

    # Clean up
    clean_key_folder(folder_path_1)
    clean_key_folder(folder_path_2)
