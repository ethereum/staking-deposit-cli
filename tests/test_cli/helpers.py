import os

from eth2deposit.utils.constants import DEFAULT_VALIDATOR_KEYS_FOLDER_NAME


def clean_key_folder(my_folder_path: str) -> None:
    validator_keys_folder_path = os.path.join(my_folder_path, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
    if not os.path.exists(validator_keys_folder_path):
        return

    _, _, key_files = next(os.walk(validator_keys_folder_path))
    for key_file_name in key_files:
        os.remove(os.path.join(validator_keys_folder_path, key_file_name))
    os.rmdir(validator_keys_folder_path)
    os.rmdir(my_folder_path)
