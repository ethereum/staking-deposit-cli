from keystore import (
    Keystore,
    ScryptKeystore,
    Pbkdf2Keystore,
)

from json import loads

test_vector_password = 'testpassword'
test_vector_secret = bytes.fromhex('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f')
test_vector_keystores_json = [
    '''
    {
        "crypto": {
            "kdf": {
                "function": "pbkdf2",
                "params": {
                    "dklen": 32,
                    "c": 262144,
                    "prf": "hmac-sha256",
                    "salt": "d4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3"
                },
                "message": ""
            },
            "checksum": {
                "function": "sha256",
                "params": {},
                "message": "18b148af8e52920318084560fd766f9d09587b4915258dec0676cba5b0da09d8"
            },
            "cipher": {
                "function": "aes-128-ctr",
                "params": {
                    "iv": "264daa3f303d7259501c93d997d84fe6"
                },
                "message": "a9249e0ca7315836356e4c7440361ff22b9fe71e2e2ed34fc1eb03976924ed48"
            }
        },
        "pubkey": "9612d7a727c9d0a22e185a1c768478dfe919cada9266988cb32359c11f2b7b27f4ae4040902382ae2910c15e2b420d07",
        "path": "m/12381/60/3141592653589793238/4626433832795028841",
        "uuid": "64625def-3331-4eea-ab6f-782f3ed16a83",
        "version": 4
    }''',
    '''
    {
        "crypto": {
            "kdf": {
                "function": "scrypt",
                "params": {
                    "dklen": 32,
                    "n": 262144,
                    "p": 1,
                    "r": 8,
                    "salt": "d4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3"
                },
                "message": ""
            },
            "checksum": {
                "function": "sha256",
                "params": {},
                "message": "149aafa27b041f3523c53d7acba1905fa6b1c90f9fef137568101f44b531a3cb"
            },
            "cipher": {
                "function": "aes-128-ctr",
                "params": {
                    "iv": "264daa3f303d7259501c93d997d84fe6"
                },
                "message": "54ecc8863c0550351eee5720f3be6a5d4a016025aa91cd6436cfec938d6a8d30"
            }
        },
        "pubkey": "9612d7a727c9d0a22e185a1c768478dfe919cada9266988cb32359c11f2b7b27f4ae4040902382ae2910c15e2b420d07",
        "path": "m/12381/60/0/0",
        "uuid": "1d85ae20-35c5-4611-98e8-aa14a633906f",
        "version": 4
    }''']
test_vector_keystores = [Keystore.from_json(x) for x in test_vector_keystores_json]


def test_json_serialization():
    for keystore, keystore_json in zip(test_vector_keystores, test_vector_keystores_json):
        assert loads(keystore.as_json()) == loads(keystore_json)


def test_encrypt_decrypt_test_vectors():
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


def test_generated_keystores():
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


def test_encrypt_decrypt_pbkdf2_random_iv():
    generated_keystore = Pbkdf2Keystore.encrypt(secret=test_vector_secret, password=test_vector_password)
    assert generated_keystore.decrypt(test_vector_password) == test_vector_secret


def test_encrypt_decrypt_scrypt_random_iv():
    generated_keystore = ScryptKeystore.encrypt(secret=test_vector_secret, password=test_vector_password)
    assert generated_keystore.decrypt(test_vector_password) == test_vector_secret
