import os


DOMAIN_DEPOSIT = bytes.fromhex('03000000')
GENESIS_FORK_VERSION = bytes.fromhex('00000000')

MIN_DEPOSIT_AMOUNT = 2 ** 0 * 10 ** 9
MAX_DEPOSIT_AMOUNT = 2 ** 5 * 10 ** 9

WORD_LISTS_PATH = os.path.join('eth2deposit', 'key_handling', 'key_derivation', 'word_lists')

DEFAULT_VALIDATOR_KEYS_FOLDER_NAME = 'validator_keys'
