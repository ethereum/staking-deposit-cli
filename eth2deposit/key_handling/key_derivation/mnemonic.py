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
    return open(os.path.join(path, '%s.txt' % language), encoding='utf-8').readlines()


def _get_word(*, word_list: Sequence[str], index: int) -> str:
    assert index < 2048
    return word_list[index][:-1]


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


def get_mnemonic(*, language: str, words_path: str, entropy: Optional[bytes]=None) -> str:
    """
    Return a mnemonic string in a given `language` based on `entropy`.
    """
    if entropy is None:
        entropy = randbits(256).to_bytes(32, 'big')
    entropy_length = len(entropy) * 8
    assert entropy_length in range(128, 257, 32)
    checksum_length = (entropy_length // 32)
    checksum = int.from_bytes(SHA256(entropy), 'big') >> 256 - checksum_length
    entropy_bits = int.from_bytes(entropy, 'big') << checksum_length
    entropy_bits += checksum
    entropy_length += checksum_length
    mnemonic = []
    word_list = _get_word_list(language, words_path)
    for i in range(entropy_length // 11 - 1, -1, -1):
        index = (entropy_bits >> i * 11) & 2**11 - 1
        word = _get_word(word_list=word_list, index=index)
        mnemonic.append(word)
    return ' '.join(mnemonic)
