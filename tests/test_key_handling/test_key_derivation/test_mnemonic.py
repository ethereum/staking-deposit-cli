import os
import pytest
import json
from typing import (
    Sequence,
)

from staking_deposit.utils.constants import (
    MNEMONIC_LANG_OPTIONS,
)
from staking_deposit.key_handling.key_derivation.mnemonic import (
    _index_to_word,
    _get_word_list,
    get_seed,
    get_mnemonic,
    verify_mnemonic,
)


WORD_LISTS_PATH = os.path.join(os.getcwd(), 'staking_deposit', 'key_handling', 'key_derivation', 'word_lists')
all_languages = MNEMONIC_LANG_OPTIONS.keys()

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
    'test_mnemonic,is_valid',
    [(test_mnemonic[1], True)
     for _, language_test_vectors in test_vectors.items()
     for test_mnemonic in language_test_vectors]
)
def test_verify_mnemonic(test_mnemonic: str, is_valid: bool) -> None:
    assert verify_mnemonic(test_mnemonic, WORD_LISTS_PATH) == is_valid


@pytest.mark.parametrize(
    'language', ['english']
)
@pytest.mark.parametrize(
    'index, valid',
    [
        (0, True),
        (2047, True),
        (2048, False),
    ]
)
def test_get_word(language: str, index: int, valid: bool) -> None:
    word_list = _get_word_list(language, WORD_LISTS_PATH)
    if valid:
        _index_to_word(word_list=word_list, index=index)
    else:
        with pytest.raises(IndexError):
            _index_to_word(word_list=word_list, index=index)
