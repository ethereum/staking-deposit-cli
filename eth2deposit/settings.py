from typing import Dict, NamedTuple


class BaseChainSetting(NamedTuple):
    GENESIS_FORK_VERSION: bytes


# Eth2 Mainet setting
MainnetSetting = BaseChainSetting(GENESIS_FORK_VERSION=bytes.fromhex('00000000'))
# Eth2 spec v0.11.3 testnet
WittiSetting = BaseChainSetting(GENESIS_FORK_VERSION=bytes.fromhex('00000113'))
# Eth2 spec v0.12.1 testnet
AltonaSetting = BaseChainSetting(GENESIS_FORK_VERSION=bytes.fromhex('00000121'))


MAINNET = 'mainnet'
WITTI = 'witti'
ALTONA = 'altona'
ALL_CHAINS: Dict[str, BaseChainSetting] = {
    MAINNET: MainnetSetting,
    WITTI: WittiSetting,
    ALTONA: AltonaSetting,
}


def get_setting(chain_name: str = MAINNET) -> BaseChainSetting:
    return ALL_CHAINS[chain_name]
