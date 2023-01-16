from typing import Dict, NamedTuple
from eth_utils import decode_hex

DEPOSIT_CLI_VERSION = '2.3.0'


class BaseChainSetting(NamedTuple):
    NETWORK_NAME: str
    GENESIS_FORK_VERSION: bytes
    GENESIS_VALIDATORS_ROOT: bytes


MAINNET = 'mainnet'
ROPSTEN = 'ropsten'
GOERLI = 'goerli'
PRATER = 'prater'
KILN = 'kiln'
SEPOLIA = 'sepolia'

# FIXME: use the real testnet genesis_validators_root
GENESIS_VALIDATORS_ROOT_STUB = bytes.fromhex('4b363db94e286120d76eb905340fdd4e54bfe9f06bf33ff6cf5ad27f511bfe95')

# Mainnet setting
MainnetSetting = BaseChainSetting(
    NETWORK_NAME=MAINNET, GENESIS_FORK_VERSION=bytes.fromhex('00000000'),
    GENESIS_VALIDATORS_ROOT=bytes.fromhex('4b363db94e286120d76eb905340fdd4e54bfe9f06bf33ff6cf5ad27f511bfe95'))
# Ropsten setting
RopstenSetting = BaseChainSetting(
    NETWORK_NAME=ROPSTEN, GENESIS_FORK_VERSION=bytes.fromhex('80000069'),
    GENESIS_VALIDATORS_ROOT=GENESIS_VALIDATORS_ROOT_STUB)
# Goerli setting
GoerliSetting = BaseChainSetting(
    NETWORK_NAME=GOERLI, GENESIS_FORK_VERSION=bytes.fromhex('00001020'),
    GENESIS_VALIDATORS_ROOT=GENESIS_VALIDATORS_ROOT_STUB)
# Merge Testnet (spec v1.1.9)
KilnSetting = BaseChainSetting(
    NETWORK_NAME=KILN, GENESIS_FORK_VERSION=bytes.fromhex('70000069'),
    GENESIS_VALIDATORS_ROOT=GENESIS_VALIDATORS_ROOT_STUB)
# Sepolia setting
SepoliaSetting = BaseChainSetting(
    NETWORK_NAME=SEPOLIA, GENESIS_FORK_VERSION=bytes.fromhex('90000069'),
    GENESIS_VALIDATORS_ROOT=GENESIS_VALIDATORS_ROOT_STUB)


ALL_CHAINS: Dict[str, BaseChainSetting] = {
    MAINNET: MainnetSetting,
    ROPSTEN: RopstenSetting,
    GOERLI: GoerliSetting,
    PRATER: GoerliSetting,  # Prater is the old name of the Prater/Goerli testnet
    KILN: KilnSetting,
    SEPOLIA: SepoliaSetting,
}


def get_chain_setting(chain_name: str = MAINNET) -> BaseChainSetting:
    return ALL_CHAINS[chain_name]


def get_devnet_chain_setting(network_name: str, genesis_fork_version: str, genesis_validator_root: str):
    return BaseChainSetting(
        NETWORK_NAME=network_name,
        GENESIS_FORK_VERSION=decode_hex(genesis_fork_version),
        GENESIS_VALIDATORS_ROOT=decode_hex(genesis_validator_root),
    )
