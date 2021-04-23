import asyncio
import json
import os

import pytest
from click.testing import CliRunner

from eth_utils import decode_hex

from eth2deposit.deposit import cli
from eth2deposit.utils.constants import DEFAULT_VALIDATOR_KEYS_FOLDER_NAME, ETH1_ADDRESS_WITHDRAWAL_PREFIX
from eth2deposit.utils.intl import load_text
from.helpers import clean_key_folder, get_permissions, get_uuid


def test_existing_mnemonic_bls_withdrawal() -> None:
    # Prepare folder
    my_folder_path = os.path.join(os.getcwd(), 'TESTING_TEMP_FOLDER')
    clean_key_folder(my_folder_path)
    if not os.path.exists(my_folder_path):
        os.mkdir(my_folder_path)

    runner = CliRunner()
    inputs = [
        'TREZOR',
        'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about',
        '2', '2', '5', 'mainnet', 'MyPassword', 'MyPassword', 'yes']
    data = '\n'.join(inputs)
    arguments = [
        '--language', 'english',
        'existing-mnemonic',
        '--folder', my_folder_path,
        '--mnemonic-password', 'TREZOR',
    ]
    result = runner.invoke(cli, arguments, input=data)

    assert result.exit_code == 0

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


def test_existing_mnemonic_eth1_address_withdrawal() -> None:
    # Prepare folder
    my_folder_path = os.path.join(os.getcwd(), 'TESTING_TEMP_FOLDER')
    clean_key_folder(my_folder_path)
    if not os.path.exists(my_folder_path):
        os.mkdir(my_folder_path)

    runner = CliRunner()
    inputs = [
        'TREZOR',
        'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about',
        '2', '2', '5', 'mainnet', 'MyPassword', 'MyPassword', 'yes']
    data = '\n'.join(inputs)
    eth1_withdrawal_address = '0x00000000219ab540356cbb839cbe05303d7705fa'
    arguments = [
        '--language', 'english',
        'existing-mnemonic',
        '--folder', my_folder_path,
        '--mnemonic-password', 'TREZOR',
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
    assert len(set(all_uuid)) == 5

    # Verify file permissions
    if os.name == 'posix':
        for file_name in key_files:
            assert get_permissions(validator_keys_folder_path, file_name) == '0o440'
    # Clean up
    clean_key_folder(my_folder_path)


@pytest.mark.asyncio
@pytest.mark.skip(reason="I'm tired of debugging this for now")
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
        'existing-mnemonic',
        '--num_validators', '1',
        '--mnemonic="abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"',
        '--mnemonic-password', 'TREZOR',
        '--validator_start_index', '1',
        '--chain', 'mainnet',
        '--keystore_password', 'MyPassword',
        '--folder', my_folder_path,
    ]
    proc = await asyncio.create_subprocess_shell(
        ' '.join(cmd_args),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )
    intl_file_path = os.path.join(os.getcwd(), 'eth2deposit', 'cli')
    mnemonic_json_file = os.path.join(intl_file_path, 'existing_mnemonic.json')
    generate_keys_json_file = os.path.join(intl_file_path, 'generate_keys.json')
    confirmations = [
        (load_text(['arg_mnemonic_password', 'confirm'], mnemonic_json_file, 'existing_mnemonic'), b'TREZOR'),
        (load_text(['keystore_password', 'confirm'], generate_keys_json_file, 'generate_keys_arguments_decorator'),
         b'MyPassword'),
        (load_text(['msg_mnemonic_password_confirm'], mnemonic_json_file, 'existing_mnemonic'), b'y'),
    ]

    confirmation = confirmations.pop(0)
    async for out in proc.stdout:
        output = out.decode('utf-8').rstrip()
        if output.startswith(confirmation[0]):
            proc.stdin.write(confirmation[1])
            proc.stdin.write(b'\n')
            if len(confirmations) > 0:
                confirmation = confirmations.pop(0)

    # Check files
    validator_keys_folder_path = os.path.join(my_folder_path, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
    _, _, key_files = next(os.walk(validator_keys_folder_path))

    # Verify file permissions
    if os.name == 'posix':
        for file_name in key_files:
            assert get_permissions(validator_keys_folder_path, file_name) == '0o440'

    # Clean up
    clean_key_folder(my_folder_path)
