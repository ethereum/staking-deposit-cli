import asyncio
import os

# For not importing staking_deposit here
DEFAULT_VALIDATOR_KEYS_FOLDER_NAME = 'validator_keys'


async def main():
    my_folder_path = os.path.join(os.getcwd(), 'TESTING_TEMP_FOLDER')
    if not os.path.exists(my_folder_path):
        os.mkdir(my_folder_path)

    if os.name == 'nt':  # Windows
        run_script_cmd = 'sh deposit.sh'
    else:  # Mac or Linux
        run_script_cmd = './deposit.sh'

    install_cmd = run_script_cmd + ' install'
    print('[INFO] Creating subprocess 1: installation:' , install_cmd)
    proc = await asyncio.create_subprocess_shell(
        install_cmd,
    )
    await proc.wait()
    print('[INFO] Installed')

    cmd_args = [
        run_script_cmd,
        '--language', 'english',
        '--non_interactive',
        'new-mnemonic',
        '--num_validators', '1',
        '--mnemonic_language', 'english',
        '--chain', 'mainnet',
        '--keystore_password', 'MyPassword',
        '--folder', my_folder_path,
    ]
    proc = await asyncio.create_subprocess_shell(
        ' '.join(cmd_args),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    seed_phrase = ''
    parsing = False
    async for out in proc.stdout:
        output = out.decode('utf-8').rstrip()
        if output.startswith("This is your mnemonic"):
            parsing = True
        elif output.startswith("Please type your mnemonic"):
            parsing = False
        elif parsing:
            seed_phrase += output
            if len(seed_phrase) > 0:
                encoded_phrase = seed_phrase.encode()
                proc.stdin.write(encoded_phrase)
                proc.stdin.write(b'\n')
        print(output)

    async for out in proc.stderr:
        output = out.decode('utf-8').rstrip()
        print(f'[stderr] {output}')

    assert len(seed_phrase) > 0

    # Check files
    validator_keys_folder_path = os.path.join(my_folder_path, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
    _, _, key_files = next(os.walk(validator_keys_folder_path))

    # Clean up
    for key_file_name in key_files:
        os.remove(os.path.join(validator_keys_folder_path, key_file_name))
    os.rmdir(validator_keys_folder_path)
    os.rmdir(my_folder_path)


if os.name == 'nt':  # Windows
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
else:
    asyncio.run(main())
