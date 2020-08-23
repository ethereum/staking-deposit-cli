import os
import sys
from unicodedata import normalize
from secrets import randbits
from typing import (
    Optional,
    Sequence,
    Tuple,
)

from eth2deposit.utils.crypto import (
    SHA256,
    PBKDF2,
)


def _resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def _get_word_list(language: str, path: str) -> Sequence[str]:
    path = _resource_path(path)
    dirty_list = open(os.path.join(path, '%s.txt' % language), encoding='utf-8').readlines()
    return [word.replace('\n', '') for word in dirty_list]


def _index_to_word(word_list: Sequence[str], index: int) -> str:
    """
    Given the index of a word in the word list, return the corresponding word.
    """
    assert index < 2048
    return word_list[index]


def _word_to_index(word_list: Sequence[str], word: str) -> int:
    try:
        return word_list.index(word)
    except ValueError:
        raise ValueError('Word %s not in BIP39 word-list' % word)


def _uint11_array_to_uint(unit_array: Sequence[int]) -> int:
    return sum([x << i * 11 for i, x in enumerate(reversed(unit_array))])


def get_seed(*, mnemonic: str, password: str) -> bytes:
    """
    Derive the seed for the pre-image root of the tree.

    Ref: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#from-mnemonic-to-seed
    """
    encoded_mnemonic = normalize('NFKD', mnemonic).encode('utf-8')
    salt = normalize('NFKD', 'mnemonic' + password).encode('utf-8')
    return PBKDF2(password=encoded_mnemonic, salt=salt, dklen=64, c=2048, prf='sha512')


def get_languages(path: str) -> Tuple[str, ...]:
    """
    Walk the `path` and list all the languages with word-lists available.
    """
    path = _resource_path(path)
    (_, _, filenames) = next(os.walk(path))
    languages = tuple([name[:-4] for name in filenames])
    return languages


def determine_mnemonic_language(mnemonic: str, words_path:str) -> Sequence[str]:
    """
    Given a `mnemonic` determine what language it is written in.
    """
    languages = get_languages(words_path)
    word_language_map = {word: lang  for lang in languages for word in _get_word_list(lang, words_path)}
    try:
        mnemonic_list = mnemonic.split(' ')
        word_languages = [word_language_map[word] for word in mnemonic_list]
        return set(word_languages)
    except KeyError:
        raise ValueError('Word not found in mnemonic word lists for any language.')


def _get_checksum(entropy: bytes) -> int:
    """
    Determine the index of the checksum word given the entropy
    """
    entropy_length = len(entropy) * 8
    assert entropy_length in range(128, 257, 32)
    checksum_length = (entropy_length // 32)
    return int.from_bytes(SHA256(entropy), 'big') >> 256 - checksum_length


def verify_mnemonic(mnemonic: str, words_path: str) -> bool:
    languages = determine_mnemonic_language(mnemonic, words_path)
    for language in languages:
        try:
            word_list = _get_word_list(language, words_path)
            mnemonic_list = mnemonic.split(' ')
            word_indices = [_word_to_index(word_list, word) for word in mnemonic_list]
            mnemonic_int = _uint11_array_to_uint(word_indices)
            checksum_length = len(mnemonic_list)//3
            checksum = mnemonic_int & 2**checksum_length - 1
            entropy = (mnemonic_int - checksum) >> checksum_length
            entropy_bits = entropy.to_bytes(checksum_length * 4, 'big')
            return _get_checksum(entropy_bits) == checksum
        except ValueError:
            pass
    return False



def get_mnemonic(*, language: str, words_path: str, entropy: Optional[bytes]=None) -> str:
    """
    Return a mnemonic string in a given `language` based on `entropy`.
    """
    if entropy is None:
        entropy = randbits(256).to_bytes(32, 'big')
    entropy_length = len(entropy) * 8
    assert entropy_length in range(128, 257, 32)
    checksum_length = (entropy_length // 32)
    checksum = _get_checksum(entropy)
    entropy_bits = int.from_bytes(entropy, 'big') << checksum_length
    entropy_bits += checksum
    entropy_length += checksum_length
    mnemonic = []
    word_list = _get_word_list(language, words_path)
    for i in range(entropy_length // 11 - 1, -1, -1):
        index = (entropy_bits >> i * 11) & 2**11 - 1
        word = _index_to_word(word_list, index)
        mnemonic.append(word)
    return ' '.join(mnemonic)
