import os

from click.testing import CliRunner

from cli.deposit import main
from cli import deposit
from eth2deposit.utils.constants import DEFAULT_VALIDATOR_KEYS_FOLDER_NAME


def test_deposit(monkeypatch):
    # monkeypatch get_mnemonic
    def get_mnemonic(language, words_path, entropy=None):
        return "fakephrase"

    monkeypatch.setattr(deposit, "get_mnemonic", get_mnemonic)

    # Prepare folder
    my_folder_path = os.path.join(os.getcwd(), 'my_folder_name')
    if not os.path.exists(my_folder_path):
        os.mkdir(my_folder_path)

    runner = CliRunner()
    inputs = ['1', 'english', 'MyPassword', 'MyPassword', 'fakephrase']
    data = '\n'.join(inputs)
    result = runner.invoke(main, ['--folder', my_folder_path], input=data)

    assert result.exit_code == 0

    # Check files
    validator_keys_folder_path = os.path.join(my_folder_path, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
    _, _, key_files = next(os.walk(validator_keys_folder_path))
    assert len(key_files) == 2

    # Clean up
    for key_file_name in key_files:
        os.remove(os.path.join(validator_keys_folder_path, key_file_name))
    os.rmdir(validator_keys_folder_path)
    os.rmdir(my_folder_path)
