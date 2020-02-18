from json import load
from key_derivation.mnemonic import (
    get_seed,
    get_mnemonic,
)

with open('tests/test_key_derivation/test_vectors/mnemonic.json', 'r') as f:
    test_vectors = load(f)


def test_bip39():
    for language, language_test_vectors in test_vectors.items():
        for test in language_test_vectors:
            test_entropy = bytes.fromhex(test[0])
            test_mnemonic = test[1]
            test_seed = bytes.fromhex(test[2])

            assert get_mnemonic(language=language, entropy=test_entropy) == test_mnemonic
            assert get_seed(mnemonic=test_mnemonic, password='TREZOR') == test_seed
