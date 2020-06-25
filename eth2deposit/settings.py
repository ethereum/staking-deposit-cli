from typing import Dict, NamedTuple


class BaseChainSetting(NamedTuple):
    GENESIS_FORK_VERSION: bytes


MainnetSetting = BaseChainSetting(
    GENESIS_FORK_VERSION=bytes.fromhex('00000000'),
)


# Eth2 spec v0.11.3 testnet
WittiSetting = BaseChainSetting(
    GENESIS_FORK_VERSION=bytes.fromhex('00000113'),
)


MAINNET = 'mainnet'
WITTI = 'witti'
ALL_CHAINS: Dict[str, BaseChainSetting] = {
    MAINNET: MainnetSetting,
    WITTI: WittiSetting,
}


def get_setting(chain_name: str = MAINNET) -> BaseChainSetting:
    return ALL_CHAINS[chain_name]
