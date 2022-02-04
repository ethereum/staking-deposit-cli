import os
import json
import pytest

from staking_deposit.key_handling.keystore import (
    Keystore,
    ScryptKeystore,
    Pbkdf2Keystore,
)

test_vector_password = '𝔱𝔢𝔰𝔱𝔭𝔞𝔰𝔰𝔴𝔬𝔯𝔡🔑'
test_vector_secret = bytes.fromhex('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f')
test_vector_folder = os.path.join(os.getcwd(), 'tests', 'test_key_handling', 'keystore_test_vectors')
_, _, test_vector_files = next(os.walk(test_vector_folder))  # type: ignore

test_vector_keystores = [Keystore.from_file(os.path.join(test_vector_folder, f)) for f in test_vector_files]


def test_json_serialization() -> None:
    for keystore, keystore_json_file in zip(test_vector_keystores, test_vector_files):
        keystore_json_path = os.path.join(test_vector_folder, keystore_json_file)
        with open(keystore_json_path) as f:
            assert json.loads(keystore.as_json()) == json.load(f)


def test_encrypt_decrypt_test_vectors() -> None:
    for tv in test_vector_keystores:
        aes_iv = tv.crypto.cipher.params['iv']
        kdf_salt = tv.crypto.kdf.params['salt']
        keystore = Pbkdf2Keystore if 'pbkdf' in tv.crypto.kdf.function else ScryptKeystore
        generated_keystore = keystore.encrypt(
            secret=test_vector_secret,
            password=test_vector_password,
            aes_iv=aes_iv,
            kdf_salt=kdf_salt)
        assert generated_keystore.decrypt(test_vector_password) == test_vector_secret


def test_generated_keystores() -> None:
    for tv in test_vector_keystores:
        aes_iv = tv.crypto.cipher.params['iv']
        kdf_salt = tv.crypto.kdf.params['salt']
        keystore = Pbkdf2Keystore if 'pbkdf' in tv.crypto.kdf.function else ScryptKeystore
        generated_keystore = keystore.encrypt(
            secret=test_vector_secret,
            password=test_vector_password,
            aes_iv=aes_iv,
            kdf_salt=kdf_salt)
        assert generated_keystore.crypto == tv.crypto


def test_encrypt_decrypt_pbkdf2_random_iv() -> None:
    generated_keystore = Pbkdf2Keystore.encrypt(secret=test_vector_secret, password=test_vector_password)
    assert generated_keystore.decrypt(test_vector_password) == test_vector_secret


def test_encrypt_decrypt_scrypt_random_iv() -> None:
    generated_keystore = ScryptKeystore.encrypt(secret=test_vector_secret, password=test_vector_password)
    assert generated_keystore.decrypt(test_vector_password) == test_vector_secret


def test_encrypt_decrypt_incorrect_password() -> None:
    generated_keystore = ScryptKeystore.encrypt(secret=test_vector_secret, password=test_vector_password)
    incorrect_password = test_vector_password + 'incorrect'
    with pytest.raises(ValueError):
        generated_keystore.decrypt(incorrect_password)


@pytest.mark.parametrize(
    'password,processed_password',
    [
        ['\a', b''], ['\b', b''], ['\t', b''],
        ['a', b'a'], ['abc', b'abc'], ['a\bc', b'ac'],
    ]
)
def test_process_password(password: str, processed_password: bytes) -> None:
    assert Keystore._process_password(password) == processed_password
