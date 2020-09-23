import os
import pytest
import json
from typing import (
    Sequence,
)

from eth2deposit.key_handling.key_derivation.mnemonic import (
    _get_word,
    _get_word_list,
    get_languages,
    get_seed,
    get_mnemonic,
)


WORD_LISTS_PATH = os.path.join(os.getcwd(), 'eth2deposit', 'key_handling', 'key_derivation', 'word_lists')
all_languages = get_languages(WORD_LISTS_PATH)

test_vector_filefolder = os.path.join('tests', 'test_key_handling',
                                      'test_key_derivation', 'test_vectors', 'mnemonic.json')
with open(test_vector_filefolder, 'r', encoding='utf-8') as f:
    test_vectors = json.load(f)


@pytest.mark.parametrize(
    'language,test',
    [(language, test) for language, language_test_vectors in test_vectors.items() for test in language_test_vectors]
)
def test_bip39(language: str, test: Sequence[str]) -> None:
    test_entropy = bytes.fromhex(test[0])
    test_mnemonic = test[1]
    test_seed = bytes.fromhex(test[2])

    assert get_mnemonic(language=language, words_path=WORD_LISTS_PATH, entropy=test_entropy) == test_mnemonic
    assert get_seed(mnemonic=test_mnemonic, password='TREZOR') == test_seed


@pytest.mark.parametrize(
    'language',
    [language for language in all_languages]
)
@pytest.mark.parametrize(
    'index, valid',
    [
        (0, True),
        (2047, True),
        (2048, False),
    ]
)
def test_get_word(language, index, valid):
    word_list = _get_word_list(language, WORD_LISTS_PATH)
    if valid:
        _get_word(word_list=word_list, index=index)
    else:
        with pytest.raises(IndexError):
            _get_word(word_list=word_list, index=index)
