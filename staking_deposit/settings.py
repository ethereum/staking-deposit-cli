from typing import Dict, NamedTuple


DEPOSIT_CLI_VERSION = '2.1.0'


class BaseChainSetting(NamedTuple):
    NETWORK_NAME: str
    GENESIS_FORK_VERSION: bytes


MAINNET = 'mainnet'
PRATER = 'prater'
KINTSUGI = 'kintsugi'
KILN = 'kiln'


# Mainnet setting
MainnetSetting = BaseChainSetting(NETWORK_NAME=MAINNET, GENESIS_FORK_VERSION=bytes.fromhex('00000000'))
# Testnet (spec v1.0.1)
PraterSetting = BaseChainSetting(NETWORK_NAME=PRATER, GENESIS_FORK_VERSION=bytes.fromhex('00001020'))
# Merge Testnet (spec v1.1.4)
KintsugiSetting = BaseChainSetting(NETWORK_NAME=KINTSUGI, GENESIS_FORK_VERSION=bytes.fromhex('60000069'))
# Merge Testnet (spec v1.1.9)
KilnSetting = BaseChainSetting(NETWORK_NAME=KILN, GENESIS_FORK_VERSION=bytes.fromhex('70000069'))


ALL_CHAINS: Dict[str, BaseChainSetting] = {
    MAINNET: MainnetSetting,
    PRATER: PraterSetting,
    KINTSUGI: KintsugiSetting,
    KILN: KilnSetting,
}


def get_chain_setting(chain_name: str = MAINNET) -> BaseChainSetting:
    return ALL_CHAINS[chain_name]
