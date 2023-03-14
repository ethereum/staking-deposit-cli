import os

from staking_deposit.key_handling.keystore import Keystore
from staking_deposit.utils.constants import (
    DEFAULT_BLS_TO_EXECUTION_CHANGES_FOLDER_NAME,
    DEFAULT_VALIDATOR_KEYS_FOLDER_NAME,
)


def clean_key_folder(my_folder_path: str) -> None:
    sub_folder_path = os.path.join(my_folder_path, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
    clean_folder(my_folder_path, sub_folder_path)


def clean_btec_folder(my_folder_path: str) -> None:
    sub_folder_path = os.path.join(my_folder_path, DEFAULT_BLS_TO_EXECUTION_CHANGES_FOLDER_NAME)
    clean_folder(my_folder_path, sub_folder_path)


def clean_folder(primary_folder_path: str, sub_folder_path: str) -> None:
    if not os.path.exists(sub_folder_path):
        return

    _, _, key_files = next(os.walk(sub_folder_path))
    for key_file_name in key_files:
        os.remove(os.path.join(sub_folder_path, key_file_name))
    os.rmdir(sub_folder_path)
    os.rmdir(primary_folder_path)


def get_uuid(key_file: str) -> str:
    keystore = Keystore.from_file(key_file)
    return keystore.uuid


def get_permissions(path: str, file_name: str) -> str:
    return oct(os.stat(os.path.join(path, file_name)).st_mode & 0o777)


def verify_file_permission(os_ref, folder_path, files):
    if os_ref.name == 'posix':
        for file_name in files:
            assert get_permissions(folder_path, file_name) == '0o440'


def prepare_testing_folder(os_ref, testing_folder_name='TESTING_TEMP_FOLDER'):
    my_folder_path = os_ref.path.join(os_ref.getcwd(), testing_folder_name)
    clean_btec_folder(my_folder_path)
    if not os_ref.path.exists(my_folder_path):
        os_ref.mkdir(my_folder_path)
    return my_folder_path
