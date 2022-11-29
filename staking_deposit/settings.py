from typing import Dict, NamedTuple


DEPOSIT_CLI_VERSION = '2.3.0'


class BaseChainSetting(NamedTuple):
    NETWORK_NAME: str
    GENESIS_FORK_VERSION: bytes


MAINNET = 'mainnet'
ROPSTEN = 'ropsten'
GOERLI = 'goerli'
PRATER = 'prater'
KILN = 'kiln'
SEPOLIA = 'sepolia'
LOCAL_TESTNET = 'local_testnet'


# Mainnet setting
MainnetSetting = BaseChainSetting(NETWORK_NAME=MAINNET, GENESIS_FORK_VERSION=bytes.fromhex('00000000'))
# Ropsten setting
RopstenSetting = BaseChainSetting(NETWORK_NAME=ROPSTEN, GENESIS_FORK_VERSION=bytes.fromhex('80000069'))
# Goerli setting
GoerliSetting = BaseChainSetting(NETWORK_NAME=GOERLI, GENESIS_FORK_VERSION=bytes.fromhex('00001020'))
# Merge Testnet (spec v1.1.9)
KilnSetting = BaseChainSetting(NETWORK_NAME=KILN, GENESIS_FORK_VERSION=bytes.fromhex('70000069'))
# Sepolia setting
SepoliaSetting = BaseChainSetting(NETWORK_NAME=SEPOLIA, GENESIS_FORK_VERSION=bytes.fromhex('90000069'))
# Local Testnet
# LocalSetting = BaseChainSetting(NETWORK_NAME=LOCAL_TESTNET, GENESIS_FORK_VERSION=bytes.fromhex('00000ffe'))
LocalSetting = BaseChainSetting(NETWORK_NAME=LOCAL_TESTNET, GENESIS_FORK_VERSION=bytes.fromhex('20000089'))


ALL_CHAINS: Dict[str, BaseChainSetting] = {
    MAINNET: MainnetSetting,
    ROPSTEN: RopstenSetting,
    GOERLI: GoerliSetting,
    PRATER: GoerliSetting,  # Prater is the old name of the Prater/Goerli testnet
    KILN: KilnSetting,
    SEPOLIA: SepoliaSetting,
    LOCAL_TESTNET: LocalSetting
}


def get_chain_setting(chain_name: str = MAINNET) -> BaseChainSetting:
    return ALL_CHAINS[chain_name]
