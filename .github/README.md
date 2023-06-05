# BLS To Execution Change with a Ledger wallet

This is a fork of the [staking-deposit-cli](https://github.com/ethereum/staking-deposit-cli)
tool by the Ethereum Foundation.

The official documentation to create the BLS To Execution Change can be found
[here](https://launchpad.ethereum.org/en/btec/).

:warning: This is only supported on the Nano X *for now*, minimum firmware version 2.1.0 :warning:

## Setting-up

* Have [Python 3](https://www.python.org/downloads/) installed on your system
* Download/Clone the _master_ branch of this repository
* On your terminal, place yourself at the root of the repository
* Create a Python virtual environment :
```bash
$> python3 -m venv ./venv
```
* Jump into the newly created environment :
```bash
$> . ./venv/bin/activate
```
* Install the tool + all its dependencies :
```bash
(venv) $> ./deposit.sh install
```
* Have the [BTEC app](https://github.com/LedgerHQ/app-btec) on your wallet (installed from Ledger Live with _Developer mode_ activated in Settings > Experimental features) and opened :

![image](https://user-images.githubusercontent.com/94451027/235108339-96a14201-ec07-46f2-ae9b-8df66d754e60.png)


## Generating the message

This is where things are a bit different from the official tool. As the whole
point of a hardware wallet is to secure the mnemonic (24 words), having to give
it to a script on a potentially compromised machine completely defeats its purpose.

Instead, the script was slightly modified in order to not handle any secret data,
but instead rely on the Ledger wallet for these steps.

You can provide the tool with all the information it requires as arguments to the command
itself, but it's easier to not provide them and let the tool ask you for them like so :

```bash
(venv) $> ./deposit.sh generate-bls-to-execution-change
linux-gnu
Running deposit-cli...
Please choose your language ['1. العربية', '2. ελληνικά', '3. English', '4. Français', '5. Bahasa melayu', '6. Italiano', '7. 日本語', '8. 한국어', '9. Português do Brasil', '10. român', '11. Türkçe', '12. 简体中文']:  [English]:
Please choose the (mainnet or testnet) network/chain name ['mainnet', 'goerli', 'sepolia', 'zhejiang']:  [mainnet]: goerli
Please enter the index position for the keys to start generating withdrawal credentials in ERC-2334 format. [0]:
Please enter a list of the validator index number(s) of your validator(s) as identified on the beacon chain. Split multiple items with whitespaces or commas.: 473031
Please enter a list of the old BLS withdrawal credentials of your validator(s). Split multiple items with whitespaces or commas. The withdrawal credentials are in hexadecimal encoded form.: 0x00382f9e880710428e966fa70ebb86b4fa5ef4d8a585823170c7dba03c135cd6
Please enter the 20-byte execution address for the new withdrawal credentials. Note that you CANNOT change it once you have set it on chain. (leave empty to get it from the Ledger wallet) []:
Getting public keys from Ledger wallet:		  [####################################]  1/1
Creating your SignedBLSToExecutionChange:	  [####################################]  1/1

Success!
Your SignedBLSToExecutionChange JSON file can be found at: /home/user/Downloads/staking-deposit-cli/bls_to_execution_changes


Press any key.
```

As, can be seen in this example, five informations are required :
* the network (which will probably be mainnet for you)
* the derivation index used when creating the validator keys (will probably be 0 for you, but double-check)
* the validator index (specfic to your validator)
* old BLS withdrawal credentials (specific to your validator)
* withdrawal address (optional, if not provided, gets it from the Ledger wallet on the given derivation index)

On the page of your validator stats on [beaconcha.in](https://beaconcha.in) :

![image](https://user-images.githubusercontent.com/94451027/235096222-73d06d45-c1bb-4e92-89a6-330d9c102d94.png)

* Circled in yellow :yellow_square:, you can find your validator index
* Circled in red :red_square:, you can find your old BLS withdrawal credentials

## Broadcasting the message to the blockchain

After running the command, a new json file should have been created under the directory _bls\_to\_execution\_changes_, this is the message which we want to broadcast :

```bash
(venv) $> ls bls_to_execution_changes/
bls_to_execution_change-1682674631.json
(venv) $> cat bls_to_execution_changes/bls_to_execution_change-1682674631.json
[{"message": {"validator_index": "468190", "from_bls_pubkey": "0xaf99be032f77317efd8b8b076b075c6e71b28dc1f3ccd80cce97c03d5dd99391105d4e592fd4df9ca9c9162ca2548448", "to_execution_address": "0x612474b4e72f14873be701a6cd9333201ce80888"}, "signature": "0x81e8a2200f25626b1b6d5388cb4385bdd1a40c3942a7c59714b6eb7eb5dbc43bd8da6160a2a7e5c1a35197db4590089e10d8316c4f39278584e0296ac5b8ffb36f8c01ce5465bdd5f48f95887f099d631405ad971a194ae22c32ca056396e1a0", "metadata": {"network_name": "goerli", "genesis_validators_root": "0x043db0d9a83813551ee2f33450d23797757d430911a9320530ad8a0eabc43efb", "deposit_cli_version": "2.5.0"}}]
```

:warning: Make sure that the value of _to\_execution\_address_ in this file corresponds to
an address under your control as **once a BLS To Execution Change has been broadcasted, there
is no way to change it again**. :warning:

To broadcast the message, simply upload the file [there](https://beaconcha.in/tools/broadcast).

![image](https://user-images.githubusercontent.com/94451027/235105667-5fcc6e8f-4a9a-44cc-bed4-cd51cb8c8fa0.png)

After a while, you should see some change on the page of your validator :

![image](https://user-images.githubusercontent.com/94451027/235119089-6b153909-7b08-4f2a-b739-f96c5264af69.png)
