import os

from eth2spec.phase0 import spec


DOMAIN_DEPOSIT = spec.DOMAIN_DEPOSIT

GENESIS_FORK_VERSION = spec.GENESIS_FORK_VERSION

MIN_DEPOSIT_AMOUNT = spec.MIN_DEPOSIT_AMOUNT
MAX_EFFECTIVE_BALANCE = spec.MAX_EFFECTIVE_BALANCE

WORD_LISTS_PATH = os.path.join('eth2deposit', 'key_handling', 'key_derivation', 'word_lists')
