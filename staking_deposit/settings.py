from typing import Dict, NamedTuple
from eth_utils import decode_hex

DEPOSIT_CLI_VERSION = '2.8.0'


class BaseChainSetting(NamedTuple):
    NETWORK_NAME: str
    GENESIS_FORK_VERSION: bytes
    GENESIS_VALIDATORS_ROOT: bytes


MAINNET = 'mainnet'
SEPOLIA = 'sepolia'
HOLESKY = 'holesky'
MEKONG = 'mekong'

# Mainnet setting
MainnetSetting = BaseChainSetting(
    NETWORK_NAME=MAINNET, GENESIS_FORK_VERSION=bytes.fromhex('00000000'),
    GENESIS_VALIDATORS_ROOT=bytes.fromhex('4b363db94e286120d76eb905340fdd4e54bfe9f06bf33ff6cf5ad27f511bfe95'))
# Sepolia setting
SepoliaSetting = BaseChainSetting(
    NETWORK_NAME=SEPOLIA, GENESIS_FORK_VERSION=bytes.fromhex('90000069'),
    GENESIS_VALIDATORS_ROOT=bytes.fromhex('d8ea171f3c94aea21ebc42a1ed61052acf3f9209c00e4efbaaddac09ed9b8078'))
# Holesky setting
HoleskySetting = BaseChainSetting(
    NETWORK_NAME=HOLESKY, GENESIS_FORK_VERSION=bytes.fromhex('01017000'),
    GENESIS_VALIDATORS_ROOT=bytes.fromhex('9143aa7c615a7f7115e2b6aac319c03529df8242ae705fba9df39b79c59fa8b1'))
# Mekong setting
MekongSetting = BaseChainSetting(
    NETWORK_NAME=MEKONG, GENESIS_FORK_VERSION=bytes.fromhex('10637624'),
    GENESIS_VALIDATORS_ROOT=bytes.fromhex('9838240bca889c52818d7502179b393a828f61f15119d9027827c36caeb67db7'))


ALL_CHAINS: Dict[str, BaseChainSetting] = {
    MAINNET: MainnetSetting,
    SEPOLIA: SepoliaSetting,
    HOLESKY: HoleskySetting,
    MEKONG: MekongSetting,
}


def get_chain_setting(chain_name: str = MAINNET) -> BaseChainSetting:
    return ALL_CHAINS[chain_name]


def get_devnet_chain_setting(network_name: str,
                             genesis_fork_version: str,
                             genesis_validator_root: str) -> BaseChainSetting:
    return BaseChainSetting(
        NETWORK_NAME=network_name,
        GENESIS_FORK_VERSION=decode_hex(genesis_fork_version),
        GENESIS_VALIDATORS_ROOT=decode_hex(genesis_validator_root),
    )
