import os


ZERO_BYTES32 = b'\x00' * 32

# Spec constants
DOMAIN_DEPOSIT = bytes.fromhex('03000000')
BLS_WITHDRAWAL_PREFIX = bytes.fromhex('00')

MIN_DEPOSIT_AMOUNT = 2 ** 0 * 10 ** 9
MAX_DEPOSIT_AMOUNT = 2 ** 5 * 10 ** 9


# File/folder constants
WORD_LISTS_PATH = os.path.join('eth2deposit', 'key_handling', 'key_derivation', 'word_lists')
DEFAULT_VALIDATOR_KEYS_FOLDER_NAME = 'validator_keys'


# Sundry constants
UNICODE_CONTROL_CHARS = list(range(0x00, 0x20)) + list(range(0x7F, 0xA0))
