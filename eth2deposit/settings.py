from typing import Dict, NamedTuple


class BaseChainSetting(NamedTuple):
    GENESIS_FORK_VERSION: bytes


# Eth2 Mainnet setting
MainnetSetting = BaseChainSetting(GENESIS_FORK_VERSION=bytes.fromhex('00000000'))
# Eth2 spec v0.11.3 testnet
WittiSetting = BaseChainSetting(GENESIS_FORK_VERSION=bytes.fromhex('00000113'))
# Eth2 spec v0.12.1 testnet
AltonaSetting = BaseChainSetting(GENESIS_FORK_VERSION=bytes.fromhex('00000121'))
# Eth2 "official" public testnet (spec v0.12.2)
MedallaSetting = BaseChainSetting(GENESIS_FORK_VERSION=bytes.fromhex('00000001'))

MAINNET = 'mainnet'
WITTI = 'witti'
ALTONA = 'altona'
MEDALLA = 'medalla'
ALL_CHAINS: Dict[str, BaseChainSetting] = {
    MAINNET: MainnetSetting,
    WITTI: WittiSetting,
    ALTONA: AltonaSetting,
    MEDALLA: MedallaSetting,
}


def get_setting(chain_name: str = MAINNET) -> BaseChainSetting:
    return ALL_CHAINS[chain_name]
