import os
import pytest
import json

from eth2deposit.key_handling.key_derivation.mnemonic import (
    get_seed,
    get_mnemonic,
)


WORD_LISTS_PATH = os.path.join(os.getcwd(), 'eth2deposit', 'key_handling', 'key_derivation', 'word_lists')

test_vector_filefolder = os.path.join('tests', 'test_key_handling',
                                      'test_key_derivation', 'test_vectors', 'mnemonic.json')
with open(test_vector_filefolder, 'r', encoding='utf-8') as f:
    test_vectors = json.load(f)


@pytest.mark.parametrize(
    'language,language_test_vectors',
    [(a, b) for a, b in test_vectors.items()]
)
def test_bip39(language, language_test_vectors):
    for test in language_test_vectors:
        test_entropy = bytes.fromhex(test[0])
        test_mnemonic = test[1]
        test_seed = bytes.fromhex(test[2])

        assert get_mnemonic(language=language, words_path=WORD_LISTS_PATH, entropy=test_entropy) == test_mnemonic
        assert get_seed(mnemonic=test_mnemonic, password='TREZOR') == test_seed
