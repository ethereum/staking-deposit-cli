import os
from unicodedata import normalize
from secrets import randbits
from typing import (
    List,
    Optional,
    Sequence,
)

from eth2deposit.utils.crypto import (
    SHA256,
    PBKDF2,
)


def _get_word_list(language: str, path: str) -> Sequence[str]:
    return open(os.path.join(path, '%s.txt' % language)).readlines()


def _get_word(*, word_list: Sequence[str], index: int) -> str:
    assert index < 2048
    return word_list[index][:-1]


def get_seed(*, mnemonic: str, password: str='') -> bytes:
    """
    Derives the seed for the pre-image root of the tree.
    """
    mnemonic = normalize('NFKD', mnemonic)
    salt = normalize('NFKD', 'mnemonic' + password).encode('utf-8')
    return PBKDF2(password=mnemonic, salt=salt, dklen=64, c=2048, prf='sha512')


def get_languages(path: str) -> List[str]:
    """
    Walk the `path` and list all the languages with word-lists available.
    """
    (_, _, filenames) = next(os.walk(path))
    filenames = [name[:-4] for name in filenames]
    return filenames


def get_mnemonic(*, language: str, words_path: str, entropy: Optional[bytes]=None) -> str:
    """
    Returns a mnemonic string in a given `language` based on `entropy`.
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
