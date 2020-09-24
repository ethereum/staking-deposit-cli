import os
import sys
import itertools
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
    """
    Get the absolute path to a resource in a manner friendly to PyInstaller.
    PyInstaller creates a temp folder and stores path in _MEIPASS which this function swaps
    into a resource path so it is avaible both when building binaries and running natively.
    """
    try:
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def _get_word_list(language: str, path: str) -> Sequence[str]:
    """
    Given the language and path to the wordlist, return the list of BIP39 words.

    Ref: https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md
    """
    path = _resource_path(path)
    return open(os.path.join(path, '%s.txt' % language), encoding='utf-8').readlines()


def _get_word(*, word_list: Sequence[str], index: int) -> str:
    """
    Return the corresponding word for the supplied index while stripping out '\\n' chars.
    """
    if index >= 2048:
        raise IndexError(f"`index` should be less than 2048. Got {index}.")
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
    filenames = [f for f in filenames if f[-4:] == '.txt']
    languages = tuple([name[:-4] for name in filenames])
    return languages


def check_mnemonic(words: str, language: str, words_path: str) -> bytearray:
    """
    Modified function from https://github.com/trezor/python-mnemonic
    """
    sys.tracebacklimit = 0
    word_list = [x.strip() for x in _get_word_list(language, words_path)]
    [i.strip() for i in word_list]
    words = words.split(" ")
    if len(words) not in [12, 15, 18, 21, 24]:
        raise ValueError('%d is not a valid number of words in mnemonics, must be 12, 15, 18, 21 or 24.'% len(words))
        
    mnemonic_length = len(words) * 11
    checksum_length = mnemonic_length // 33
    entropy_length = mnemonic_length - checksum_length
        
    #Set and fill bitarray
    entropy_to_Bits = [False] * mnemonic_length
    wordindex = 0
    for word in words:
        index = word_list.index(word)
        for ii in range(11):
            entropy_to_Bits[(wordindex * 11) + ii] = (index & (1 << (10 - ii))) != 0
        wordindex += 1
        
    # Extract original entropy as bytes.
    entropy = bytearray(entropy_length // 8)
    for ii in range(len(entropy)):
        for jj in range(8):
            if entropy_to_Bits[(ii * 8) + jj]:
                entropy[ii] |= 1 << (7 - jj)
        
    # Take the digest of the entropy.
    hashBytes = SHA256(entropy)
    hashBits = list(
        itertools.chain.from_iterable(
            [c & (1 << (7 - i)) != 0 for i in range(8)] for c in hashBytes
        )
    )
    # Check all the checksum bits.
    for i in range(checksum_length):
        if entropy_to_Bits[entropy_length + i] != hashBits[i]:
         raise ValueError("Failed checksum of mnemonics.")
           
    return True
  
          
def get_mnemonic(*, language: str, words_path: str, entropy: Optional[bytes]=None) -> str:
    """
    Return a mnemonic string in a given `language` based on `entropy` via the calculated checksum.

    Ref: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#generating-the-mnemonic
    """
    if entropy is None:
        entropy = randbits(256).to_bytes(32, 'big')
    entropy_length = len(entropy) * 8
    if entropy_length not in range(128, 257, 32):
        raise IndexError(f"`entropy_length` should be in [128, 160, 192,224, 256]. Got {entropy_length}.")
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
