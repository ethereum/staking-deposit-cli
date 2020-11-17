from typing import Dict, NamedTuple


DEPOSIT_CLI_VERSION = '1.1.0'


class BaseChainSetting(NamedTuple):
    ETH2_NETWORK_NAME: str
    GENESIS_FORK_VERSION: bytes


MAINNET = 'mainnet'
WITTI = 'witti'
ALTONA = 'altona'
MEDALLA = 'medalla'
SPADINA = 'spadina'
ZINKEN = 'zinken'
PYRMONT = 'pyrmont'


# Eth2 Mainnet setting
MainnetSetting = BaseChainSetting(ETH2_NETWORK_NAME=MAINNET, GENESIS_FORK_VERSION=bytes.fromhex('00000000'))
# Eth2 spec v0.11.3 testnet
WittiSetting = BaseChainSetting(ETH2_NETWORK_NAME=WITTI, GENESIS_FORK_VERSION=bytes.fromhex('00000113'))
# Eth2 spec v0.12.1 testnet
AltonaSetting = BaseChainSetting(ETH2_NETWORK_NAME=ALTONA, GENESIS_FORK_VERSION=bytes.fromhex('00000121'))
# Eth2 "official" public testnet (spec v0.12.2)
MedallaSetting = BaseChainSetting(ETH2_NETWORK_NAME=MEDALLA, GENESIS_FORK_VERSION=bytes.fromhex('00000001'))
# Eth2 "dress rehearsal" testnet (spec v0.12.3)
SpadinaSetting = BaseChainSetting(ETH2_NETWORK_NAME=SPADINA, GENESIS_FORK_VERSION=bytes.fromhex('00000002'))
# Eth2 "dress rehearsal" testnet (spec v0.12.3)
ZinkenSetting = BaseChainSetting(ETH2_NETWORK_NAME=ZINKEN, GENESIS_FORK_VERSION=bytes.fromhex('00000003'))
# Eth2 pre-launch testnet (spec v1.0.0)
PyrmontSetting = BaseChainSetting(ETH2_NETWORK_NAME=PYRMONT, GENESIS_FORK_VERSION=bytes.fromhex('00002009'))


ALL_CHAINS: Dict[str, BaseChainSetting] = {
    MAINNET: MainnetSetting,
    WITTI: WittiSetting,
    ALTONA: AltonaSetting,
    MEDALLA: MedallaSetting,
    SPADINA: SpadinaSetting,
    ZINKEN: ZinkenSetting,
    PYRMONT: PyrmontSetting,
}


def get_chain_setting(chain_name: str = MAINNET) -> BaseChainSetting:
    return ALL_CHAINS[chain_name]
