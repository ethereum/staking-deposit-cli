import os
from typing import (
    Dict,
    List,
)


ZERO_BYTES32 = b'\x00' * 32

# Execution-spec constants taken from https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md
DOMAIN_DEPOSIT = bytes.fromhex('03000000')
BLS_WITHDRAWAL_PREFIX = bytes.fromhex('00')
ETH1_ADDRESS_WITHDRAWAL_PREFIX = bytes.fromhex('01')

ETH2GWEI = 10 ** 9
MIN_DEPOSIT_AMOUNT = 2 ** 0 * ETH2GWEI
MAX_DEPOSIT_AMOUNT = 2 ** 5 * ETH2GWEI


# File/folder constants
WORD_LISTS_PATH = os.path.join('staking_deposit', 'key_handling', 'key_derivation', 'word_lists')
DEFAULT_VALIDATOR_KEYS_FOLDER_NAME = 'validator_keys'

# Internationalisation constants
INTL_CONTENT_PATH = os.path.join('staking_deposit', 'intl')


def _add_index_to_options(d: Dict[str, List[str]]) -> Dict[str, List[str]]:
    '''
    Adds the (1 indexed) index (in the dict) to the first element of value list.
    eg. {'en': ['English', 'en']} -> {'en': ['1. English', '1', 'English', 'en']}
    Requires dicts to be ordered (Python > 3.6)
    '''
    keys = list(d.keys())  # Force copy dictionary keys top prevent iteration over changing dict
    for i, key in enumerate(keys):
        d.update({key: ['%s. %s' % (i + 1, d[key][0]), str(i + 1)] + d[key]})
    return d


INTL_LANG_OPTIONS = _add_index_to_options({
    'ar': ['العربية', 'ar', 'Arabic'],
    'el': ['ελληνικά', 'el', 'Greek'],
    'en': ['English', 'en'],
    'fr': ['Français', 'Francais', 'fr', 'French'],
    'id': ['Bahasa melayu', 'Melayu', 'id', 'Malay'],
    'it': ['Italiano', 'it', 'Italian'],
    'ja': ['日本語', 'ja', 'Japanese'],
    'ko': ['한국어', '조선말', '韓國語', 'ko', 'Korean'],
    'pt-BR': ['Português do Brasil', 'Brasil', 'pt-BR', 'Brazilian Portuguese'],
    'ro': ['român', 'limba română', 'ro', 'Romainian'],
    'tr': ['Türkçe', 'tr', 'Turkish'],
    'zh-CN': ['简体中文', 'zh-CN', 'zh', 'Chinease'],
})
MNEMONIC_LANG_OPTIONS = _add_index_to_options({
    'chinese_simplified': ['简体中文', 'zh', 'zh-CN', 'Chinese Simplified'],
    'chinese_traditional': ['繁體中文', 'zh-tw', 'Chinese Traditional'],
    'czech': ['čeština', 'český jazyk', 'cs', 'Czech'],
    'english': ['English', 'en'],
    'italian': ['Italiano', 'it', 'Italian'],
    'korean': ['한국어', '조선말', '韓國語', 'ko', 'Korean'],
    # Portuguese mnemonics are in both pt & pt-BR
    'portuguese': ['Português', 'Português do Brasil', 'pt', 'pt-BR', 'Portuguese'],
    'spanish': ['Español', 'es', 'Spanish'],
})

# Sundry constants
UNICODE_CONTROL_CHARS = list(range(0x00, 0x20)) + list(range(0x7F, 0xA0))
