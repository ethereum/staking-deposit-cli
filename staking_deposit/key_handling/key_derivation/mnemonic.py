import os
from unicodedata import normalize
from secrets import randbits
from typing import (
    Optional,
    Sequence,
)

from staking_deposit.utils.constants import (
    MNEMONIC_LANG_OPTIONS,
)
from staking_deposit.utils.crypto import (
    SHA256,
    PBKDF2,
)
from staking_deposit.utils.file_handling import (
    resource_path,
)


def _get_word_list(language: str, path: str) -> Sequence[str]:
    """
    Given the language and path to the wordlist, return the list of BIP39 words.

    Ref: https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md
    """
    path = resource_path(path)
    dirty_list = open(os.path.join(path, '%s.txt' % language), encoding='utf-8').readlines()
    return [word.replace('\n', '') for word in dirty_list]


def _index_to_word(word_list: Sequence[str], index: int) -> str:
    """
    Return the corresponding word for the supplied index while stripping out '\\n' chars.
    """
    if index >= 2048:
        raise IndexError(f"`index` should be less than 2048. Got {index}.")
    return word_list[index]


def _word_to_index(word_list: Sequence[str], word: str) -> int:
    try:
        return word_list.index(word)
    except ValueError:
        raise ValueError('Word %s not in BIP39 word-list' % word)


def _uint11_array_to_uint(uint11_array: Sequence[int]) -> int:
    return sum(x << i * 11 for i, x in enumerate(reversed(uint11_array)))


def get_seed(*, mnemonic: str, password: str) -> bytes:
    """
    Derive the seed for the pre-image root of the tree.

    Ref: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#from-mnemonic-to-seed
    """
    encoded_mnemonic = normalize('NFKD', mnemonic).encode('utf-8')
    salt = normalize('NFKD', 'mnemonic' + password).encode('utf-8')
    return PBKDF2(password=encoded_mnemonic, salt=salt, dklen=64, c=2048, prf='sha512')


def determine_mnemonic_language(mnemonic: str, words_path: str) -> Sequence[str]:
    """
    Given a `mnemonic` determine what language[s] it is written in.
    There are collisions between word-lists, so multiple candidate languages are returned.
    """
    languages = MNEMONIC_LANG_OPTIONS.keys()
    word_language_map = {word: lang for lang in languages for word in _get_word_list(lang, words_path)}
    try:
        mnemonic_list = mnemonic.split(' ')
        word_languages = [word_language_map[word] for word in mnemonic_list]
        return list(set(word_languages))
    except KeyError:
        raise ValueError('Word not found in mnemonic word lists for any language.')


def _validate_entropy_length(entropy: bytes) -> None:
    entropy_length = len(entropy) * 8
    if entropy_length not in range(128, 257, 32):
        raise IndexError(f"`entropy_length` should be in [128, 160, 192, 224, 256]. Got {entropy_length}.")


def _get_checksum(entropy: bytes) -> int:
    """
    Determine the index of the checksum word given the entropy
    """
    _validate_entropy_length(entropy)
    checksum_length = len(entropy) // 4
    return int.from_bytes(SHA256(entropy), 'big') >> (256 - checksum_length)


def verify_mnemonic(mnemonic: str, words_path: str) -> bool:
    """
    Given a mnemonic, verify it against its own checksum."
    """
    try:
        languages = determine_mnemonic_language(mnemonic, words_path)
    except ValueError:
        return False
    for language in languages:
        try:
            word_list = _get_word_list(language, words_path)
            mnemonic_list = mnemonic.split(' ')
            if len(mnemonic_list) not in range(12, 25, 3):
                return False
            word_indices = [_word_to_index(word_list, word) for word in mnemonic_list]
            mnemonic_int = _uint11_array_to_uint(word_indices)
            checksum_length = len(mnemonic_list) // 3
            checksum = mnemonic_int & 2**checksum_length - 1
            entropy = (mnemonic_int - checksum) >> checksum_length
            entropy_bits = entropy.to_bytes(checksum_length * 4, 'big')
            return _get_checksum(entropy_bits) == checksum
        except ValueError:
            pass
    return False


def get_mnemonic(*, language: str, words_path: str, entropy: Optional[bytes]=None) -> str:
    """
    Return a mnemonic string in a given `language` based on `entropy` via the calculated checksum.

    Ref: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#generating-the-mnemonic
    """
    if entropy is None:
        entropy = randbits(256).to_bytes(32, 'big')
    entropy_length = len(entropy) * 8
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
