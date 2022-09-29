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
L16_TESTNET = 'l16'
LUKSO = 'lukso'


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
# LUKSO L16 testnet setting
LUKSOL16Setting = BaseChainSetting(NETWORK_NAME=L16_TESTNET, GENESIS_FORK_VERSION=bytes.fromhex('60000069'))
# LUKSO mainnet setting - change when mainnet parameters are set and launched - for now reverts to L16
LUKSOSetting = BaseChainSetting(NETWORK_NAME=LUKSO, GENESIS_FORK_VERSION=bytes.fromhex('60000069'))

ALL_CHAINS: Dict[str, BaseChainSetting] = {
    MAINNET: MainnetSetting,
    ROPSTEN: RopstenSetting,
    GOERLI: GoerliSetting,
    PRATER: GoerliSetting,  # Prater is the old name of the Prater/Goerli testnet
    KILN: KilnSetting,
    SEPOLIA: SepoliaSetting,
    L16_TESTNET: LUKSOL16Setting,
    LUKSO: LUKSOSetting # Due to change when mainnet is launched
}


def get_chain_setting(chain_name: str = MAINNET) -> BaseChainSetting:
    return ALL_CHAINS[chain_name]
