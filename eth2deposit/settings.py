from typing import Dict, NamedTuple


DEPOSIT_CLI_VERSION = '1.2.0'


class BaseChainSetting(NamedTuple):
    ETH2_NETWORK_NAME: str
    GENESIS_FORK_VERSION: bytes


MAINNET = 'mainnet'
PYRMONT = 'pyrmont'
PRATER = 'prater'


# Eth2 Mainnet setting
MainnetSetting = BaseChainSetting(ETH2_NETWORK_NAME=MAINNET, GENESIS_FORK_VERSION=bytes.fromhex('00000000'))
# Eth2 pre-launch testnet (spec v1.0.0)
PyrmontSetting = BaseChainSetting(ETH2_NETWORK_NAME=PYRMONT, GENESIS_FORK_VERSION=bytes.fromhex('00002009'))
# Eth2 testnet (spec v1.0.1)
PraterSetting = BaseChainSetting(ETH2_NETWORK_NAME=PRATER, GENESIS_FORK_VERSION=bytes.fromhex('00001020'))


ALL_CHAINS: Dict[str, BaseChainSetting] = {
    MAINNET: MainnetSetting,
    PYRMONT: PyrmontSetting,
    PRATER: PraterSetting,
}


def get_chain_setting(chain_name: str = MAINNET) -> BaseChainSetting:
    return ALL_CHAINS[chain_name]
