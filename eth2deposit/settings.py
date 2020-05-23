from typing import Dict, NamedTuple


class BaseChainSetting(NamedTuple):
    GENESIS_FORK_VERSION: bytes


MainnetSetting = BaseChainSetting(
    GENESIS_FORK_VERSION=bytes.fromhex('00000000'),
)

MAINNET = 'mainnet'
ALL_CHAINS: Dict[str, BaseChainSetting] = {
    MAINNET: MainnetSetting,
}


def get_setting(chain_name: str = MAINNET) -> BaseChainSetting:
    return ALL_CHAINS[chain_name]
