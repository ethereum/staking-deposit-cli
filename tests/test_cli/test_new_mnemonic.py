import asyncio
import json
import os

import pytest
from click.testing import CliRunner

from eth_utils import decode_hex

from staking_deposit.cli import new_mnemonic
from staking_deposit.deposit import cli
from staking_deposit.utils.constants import DEFAULT_VALIDATOR_KEYS_FOLDER_NAME, ETH1_ADDRESS_WITHDRAWAL_PREFIX
from staking_deposit.utils.intl import load_text
from .helpers import clean_key_folder, get_permissions, get_uuid


def test_new_mnemonic_bls_withdrawal(monkeypatch) -> None:
    # monkeypatch get_mnemonic
    def mock_get_mnemonic(language, words_path, entropy=None) -> str:
        return "fakephrase"

    monkeypatch.setattr(new_mnemonic, "get_mnemonic", mock_get_mnemonic)

    # Prepare folder
    my_folder_path = os.path.join(os.getcwd(), 'TESTING_TEMP_FOLDER')
    clean_key_folder(my_folder_path)
    if not os.path.exists(my_folder_path):
        os.mkdir(my_folder_path)

    runner = CliRunner()
    inputs = ['english', 'english', '1', 'mainnet', 'MyPassword', 'MyPassword', 'fakephrase']
    data = '\n'.join(inputs)
    result = runner.invoke(cli, ['new-mnemonic', '--folder', my_folder_path], input=data)
    assert result.exit_code == 0

    # Check files
    validator_keys_folder_path = os.path.join(my_folder_path, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
    _, _, key_files = next(os.walk(validator_keys_folder_path))

    all_uuid = [
        get_uuid(validator_keys_folder_path + '/' + key_file)
        for key_file in key_files
        if key_file.startswith('keystore')
    ]
    assert len(set(all_uuid)) == 1

    # Verify file permissions
    if os.name == 'posix':
        for file_name in key_files:
            assert get_permissions(validator_keys_folder_path, file_name) == '0o440'

    # Clean up
    clean_key_folder(my_folder_path)


def test_new_mnemonic_eth1_address_withdrawal(monkeypatch) -> None:
    # monkeypatch get_mnemonic
    def mock_get_mnemonic(language, words_path, entropy=None) -> str:
        return "fakephrase"

    monkeypatch.setattr(new_mnemonic, "get_mnemonic", mock_get_mnemonic)

    # Prepare folder
    my_folder_path = os.path.join(os.getcwd(), 'TESTING_TEMP_FOLDER')
    clean_key_folder(my_folder_path)
    if not os.path.exists(my_folder_path):
        os.mkdir(my_folder_path)

    runner = CliRunner()
    inputs = ['english', '1', 'mainnet', 'MyPassword', 'MyPassword', 'fakephrase']
    data = '\n'.join(inputs)
    eth1_withdrawal_address = '0x00000000219ab540356cbb839cbe05303d7705fa'
    arguments = [
        '--language', 'english',
        'new-mnemonic',
        '--folder', my_folder_path,
        '--eth1_withdrawal_address', eth1_withdrawal_address,
    ]
    result = runner.invoke(cli, arguments, input=data)
    assert result.exit_code == 0

    # Check files
    validator_keys_folder_path = os.path.join(my_folder_path, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
    _, _, key_files = next(os.walk(validator_keys_folder_path))

    deposit_file = [key_file for key_file in key_files if key_file.startswith('deposit_data')][0]
    with open(validator_keys_folder_path + '/' + deposit_file, 'r') as f:
        deposits_dict = json.load(f)
    for deposit in deposits_dict:
        withdrawal_credentials = bytes.fromhex(deposit['withdrawal_credentials'])
        assert withdrawal_credentials == (
            ETH1_ADDRESS_WITHDRAWAL_PREFIX + b'\x00' * 11 + decode_hex(eth1_withdrawal_address)
        )

    all_uuid = [
        get_uuid(validator_keys_folder_path + '/' + key_file)
        for key_file in key_files
        if key_file.startswith('keystore')
    ]
    assert len(set(all_uuid)) == 1

    # Verify file permissions
    if os.name == 'posix':
        for file_name in key_files:
            assert get_permissions(validator_keys_folder_path, file_name) == '0o440'

    # Clean up
    clean_key_folder(my_folder_path)


@pytest.mark.asyncio
async def test_script() -> None:
    my_folder_path = os.path.join(os.getcwd(), 'TESTING_TEMP_FOLDER')
    if not os.path.exists(my_folder_path):
        os.mkdir(my_folder_path)

    if os.name == 'nt':  # Windows
        run_script_cmd = 'sh deposit.sh'
    else:  # Mac or Linux
        run_script_cmd = './deposit.sh'

    install_cmd = run_script_cmd + ' install'
    proc = await asyncio.create_subprocess_shell(
        install_cmd,
    )
    await proc.wait()

    cmd_args = [
        run_script_cmd,
        '--language', 'english',
        '--non_interactive',
        'new-mnemonic',
        '--num_validators', '5',
        '--mnemonic_language', 'english',
        '--chain', 'mainnet',
        '--keystore_password', 'MyPassword',
        '--folder', my_folder_path,
    ]
    proc = await asyncio.create_subprocess_shell(
        ' '.join(cmd_args),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )

    seed_phrase = ''
    parsing = False
    mnemonic_json_file = os.path.join(os.getcwd(), 'staking_deposit/../staking_deposit/cli/', 'new_mnemonic.json')
    async for out in proc.stdout:
        output = out.decode('utf-8').rstrip()
        if output.startswith(load_text(['msg_mnemonic_presentation'], mnemonic_json_file, 'new_mnemonic')):
            parsing = True
        elif output.startswith(load_text(['msg_mnemonic_retype_prompt'], mnemonic_json_file, 'new_mnemonic')):
            parsing = False
        elif parsing:
            seed_phrase += output
            if len(seed_phrase) > 0:
                encoded_phrase = seed_phrase.encode()
                proc.stdin.write(encoded_phrase)
                proc.stdin.write(b'\n')

    assert len(seed_phrase) > 0

    # Check files
    validator_keys_folder_path = os.path.join(my_folder_path, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
    _, _, key_files = next(os.walk(validator_keys_folder_path))

    all_uuid = [
        get_uuid(validator_keys_folder_path + '/' + key_file)
        for key_file in key_files
        if key_file.startswith('keystore')
    ]
    assert len(set(all_uuid)) == 5

    # Verify file permissions
    if os.name == 'posix':
        for file_name in key_files:
            assert get_permissions(validator_keys_folder_path, file_name) == '0o440'

    # Clean up
    clean_key_folder(my_folder_path)
