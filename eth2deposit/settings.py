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
# Eth2 "dress rehearsal" testnet (spec v0.12.3)
SpadinaSetting = BaseChainSetting(GENESIS_FORK_VERSION=bytes.fromhex('00000002'))
# Eth2 "dress rehearsal" testnet (spec v0.12.3)
ZinkenSetting = BaseChainSetting(GENESIS_FORK_VERSION=bytes.fromhex('00000003'))


MAINNET = 'mainnet'
WITTI = 'witti'
ALTONA = 'altona'
MEDALLA = 'medalla'
SPADINA = 'spadina'
ZINKEN = 'zinken'
ALL_CHAINS: Dict[str, BaseChainSetting] = {
    MAINNET: MainnetSetting,
    WITTI: WittiSetting,
    ALTONA: AltonaSetting,
    MEDALLA: MedallaSetting,
    SPADINA: SpadinaSetting,
    ZINKEN: ZinkenSetting,
}


def get_setting(chain_name: str = MAINNET) -> BaseChainSetting:
    return ALL_CHAINS[chain_name]
