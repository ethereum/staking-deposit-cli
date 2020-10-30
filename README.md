# eth2.0-deposit-cli

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Pre-production warning](#pre-production-warning)
- [Tutorial for users](#tutorial-for-users)
  - [Build requirements](#build-requirements)
  - [For Linux or MacOS users](#for-linux-or-macos-users)
    - [Option 1. Download binary executable file](#option-1-download-binary-executable-file)
      - [Step 1. Installation](#step-1-installation)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json)
        - [Commands](#commands)
        - [`new-mnemonic` Arguments](#new-mnemonic-arguments)
        - [`existing-mnemonic` Arguments](#existing-mnemonic-arguments)
        - [Successful message](#successful-message)
    - [Option 2. Build `deposit-cli` with native Python](#option-2-build-deposit-cli-with-native-python)
      - [Step 0. Python version checking](#step-0-python-version-checking)
      - [Step 1. Installation](#step-1-installation-1)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-1)
        - [Commands](#commands-1)
        - [Arguments](#arguments)
        - [Successful message](#successful-message-1)
    - [Option 3. Build `deposit-cli` with `virtualenv`](#option-3-build-deposit-cli-with-virtualenv)
      - [Step 0. Python version checking](#step-0-python-version-checking-1)
      - [Step 1. Installation](#step-1-installation-2)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-2)
        - [Commands](#commands-2)
        - [Arguments](#arguments-1)
  - [For Windows users](#for-windows-users)
    - [Option 1. Download binary executable file](#option-1-download-binary-executable-file-1)
      - [Step 1. Installation](#step-1-installation-3)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-3)
        - [Commands](#commands-3)
        - [Arguments](#arguments-2)
    - [Option 2. Build `deposit-cli` with native Python](#option-2-build-deposit-cli-with-native-python-1)
      - [Step 0. Python version checking](#step-0-python-version-checking-2)
      - [Step 1. Installation](#step-1-installation-4)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-4)
        - [Commands](#commands-4)
        - [Arguments](#arguments-3)
    - [Option 3. Build `deposit-cli` with `virtualenv`](#option-3-build-deposit-cli-with-virtualenv-1)
      - [Step 0. Python version checking](#step-0-python-version-checking-3)
      - [Step 1. Installation](#step-1-installation-5)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-5)
        - [Commands](#commands-5)
        - [Arguments](#arguments-4)
- [Development](#development)
  - [Install basic requirements](#install-basic-requirements)
  - [Install testing requirements](#install-testing-requirements)
  - [Run tests](#run-tests)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Pre-production warning

This software is a pre-release version which has not yet been audited and therefore should not yet be trusted to generate keys with the intent of securing actual ETH.

## Tutorial for users

### Build requirements

- [Python **3.7+**](https://www.python.org/about/gettingstarted/)
- [pip3](https://pip.pypa.io/en/stable/installing/)

### For Linux or MacOS users

#### Option 1. Download binary executable file

##### Step 1. Installation

See [releases page](https://github.com/ethereum/eth2.0-deposit-cli/releases) to download and decompress the corresponding binary files.

##### Step 2. Create keys and `deposit_data-*.json`

Run the following command to enter the interactive CLI and generate keys from a new mnemonic:

```sh
./deposit new-mnemonic
```

or run the following command to enter the interactive CLI and generate keys from an existing:

```sh
./deposit existing-mnemonic
```

###### Commands

The CLI offers different commands depending on what you want to do with the tool.

| Command | Description |
| ------- | ----------- |
| `new-mnemonic` | (Recommended) If you don't already have a mnemonic that you have securely backed up, or you want to have a separate mnemonic for your eth2 validators, use this option. |
| `existing-mnemonic` | If you have a mnemonic that you already use, then this option allows you to derive new keys from your existing mnemonic. Use this tool, if you have already generated keys with this CLI before, if you want to reuse your mnemonic that you know is secure that you generated elsewhere (reusing your eth1 mnemonic etc), or if you lost your keystores and need to recover your validator/withdrawal keys. |

###### `new-mnemonic` Arguments

You can use `new-mnemonic --help` to see all arguments. Note that if there are missing arguments that the CLI needs, it will ask you for them.

| Argument | Type | Description |
| -------- | -------- | -------- |
| `--num_validators`  | Non-negative integer | The number of signing keys you want to generate. Note that the child key(s) are generated via the same master key. |
| `--mnemonic_language` | String. Options: `czech`, `chinese_traditional`, `chinese_simplified`, `english`, `spanish`, `italian`, `korean`. Default to `english` | The mnemonic language |
| `--folder` | String. Pointing to `./validator_keys` by default | The folder path for the keystore(s) and deposit(s) |
| `--chain` | String. `mainnet` by default | The chain setting for the signing domain. |

###### `existing-mnemonic` Arguments

You can use `existing-mnemonic --help` to see all arguments. Note that if there are missing arguments that the CLI needs, it will ask you for them.

| Argument | Type | Description |
| -------- | -------- | -------- |
| `--validator_start_index` | Non-negative integer | The index of the first validator's keys you wish to generate. If this is your first time generating keys with this mnemonic, use 0. If you have generated keys using this mnemonic before, use the next index from which you want to start generating keys from (eg, if you've generated 4 keys before (keys #0, #1, #2, #3), then enter 4 here.|
| `--num_validators`  | Non-negative integer | The number of signing keys you want to generate. Note that the child key(s) are generated via the same master key. |
| `--folder` | String. Pointing to `./validator_keys` by default | The folder path for the keystore(s) and deposit(s) |
| `--chain` | String. `mainnet` by default | The chain setting for the signing domain. |

###### Successful message

You will see the following messages after successfully generated the keystore(s) and the deposit(s):

```text
Creating your keys.
Saving your keystore(s).
Creating your deposit(s).
Verifying your keystore(s).
Verifying your deposit(s).

Success!
Your keys can be found at: <YOUR_FOLDER_PATH>
```

#### Option 2. Build `deposit-cli` with native Python

##### Step 0. Python version checking

Ensure you are using Python version >= Python3.7:

```sh
python3 -V
```

##### Step 1. Installation

Install the dependencies:

```sh
pip3 install -r requirements.txt
python3 setup.py install
```

Or use the helper script:

```sh
./deposit.sh install
```

##### Step 2. Create keys and `deposit_data-*.json`

Run one of the following command to enter the interactive CLI:

```sh
./deposit.sh new-mnemonic
```

or

```sh
./deposit.sh existing-mnemonic
```

You can also run the tool with optional arguments:

```sh
./deposit.sh new-mnemonic --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

```sh
./deposit.sh existing-mnemonic --num_validators=<NUM_VALIDATORS> --validator_start_index=<START_INDEX> --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

###### Commands

See [here](#commands)

###### Arguments

See [here](#new-mnemonic-arguments) for `new-mnemonic` arguments
See [here](#existing-mnemonic-arguments) for `existing-mnemonic` arguments

###### Successful message
See [here](#successful-message)

#### Option 3. Build `deposit-cli` with `virtualenv`

##### Step 0. Python version checking

Ensure you are using Python version >= Python3.7:

```sh
python3 -V
```

##### Step 1. Installation

For the [virtualenv](https://virtualenv.pypa.io/en/latest/) users, you can create a new venv:

```sh
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```

and install the dependencies:

```sh
python3 setup.py install
pip3 install -r requirements.txt
```

##### Step 2. Create keys and `deposit_data-*.json`

Run one of the following command to enter the interactive CLI:

```sh
python3 ./eth2deposit/deposit.py new-mnemonic
```

or

```sh
python3 ./eth2deposit/deposit.py existing-mnemonic
```

You can also run the tool with optional arguments:

```sh
python3 ./eth2deposit/deposit.py new-mnemonic --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

```sh
python3 ./eth2deposit/deposit.py existing-mnemonic --num_validators=<NUM_VALIDATORS> --validator_start_index=<START_INDEX> --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

###### Commands

See [here](#commands)

###### Arguments

See [here](#new-mnemonic-arguments) for `new-mnemonic` arguments
See [here](#existing-mnemonic-arguments) for `existing-mnemonic` arguments

----

### For Windows users

#### Option 1. Download binary executable file

##### Step 1. Installation

See [releases page](https://github.com/ethereum/eth2.0-deposit-cli/releases) to download and decompress the corresponding binary files.

##### Step 2. Create keys and `deposit_data-*.json`

Run one of the following command to enter the interactive CLI:

```sh
deposit.exe new-mnemonic
```

or

```sh
deposit.exe existing-mnemonic
```

You can also run the tool with optional arguments:

```sh
deposit.exe new-mnemonic --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

```sh
deposit.exe existing-mnemonic --num_validators=<NUM_VALIDATORS> --validator_start_index=<START_INDEX> --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

###### Commands

See [here](#commands)

###### Arguments

See [here](#new-mnemonic-arguments) for `new-mnemonic` arguments
See [here](#existing-mnemonic-arguments) for `existing-mnemonic` arguments

#### Option 2. Build `deposit-cli` with native Python

##### Step 0. Python version checking

Ensure you are using Python version >= Python3.7 (Assume that you've installed Python 3 as the main Python):

```sh
python -V
```

##### Step 1. Installation

Install the dependencies:

```sh
pip3 install -r requirements.txt
python setup.py install
```

Or use the helper script:

```sh
sh deposit.sh install
```

##### Step 2. Create keys and `deposit_data-*.json`

Run one of the following command to enter the interactive CLI:

```sh
./deposit.sh new-mnemonic
```

or

```sh
./deposit.sh existing-mnemonic
```

You can also run the tool with optional arguments:

```sh
./deposit.sh new-mnemonic --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

```sh
./deposit.sh existing-mnemonic --num_validators=<NUM_VALIDATORS> --validator_start_index=<START_INDEX> --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

###### Commands

See [here](#commands)

###### Arguments

See [here](#new-mnemonic-arguments) for `new-mnemonic` arguments
See [here](#existing-mnemonic-arguments) for `existing-mnemonic` arguments

#### Option 3. Build `deposit-cli` with `virtualenv`

##### Step 0. Python version checking

Ensure you are using Python version >= Python3.7 (Assume that you've installed Python 3 as the main Python):

```cmd
python -V
```

##### Step 1. Installation

For the [virtualenv](https://virtualenv.pypa.io/en/latest/) users, you can create a new venv:

```cmd
pip3 install virtualenv
virtualenv venv
.\venv\Scripts\activate
```

and install the dependencies:

```cmd
python setup.py install
pip3 install -r requirements.txt
```

##### Step 2. Create keys and `deposit_data-*.json`

Run one of the following command to enter the interactive CLI:

``cmd
python .\eth2deposit\deposit.py new-mnemonic
```

or

```cmd
python .\eth2deposit\deposit.py existing-mnemonic
```

You can also run the tool with optional arguments:

```cmd
python .\eth2deposit\deposit.py new-mnemonic --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

```cmd
python .\eth2deposit\deposit.pyexisting-mnemonic --num_validators=<NUM_VALIDATORS> --validator_start_index=<START_INDEX> --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

###### Commands

See [here](#commands)

###### Arguments

See [here](#new-mnemonic-arguments) for `new-mnemonic` arguments
See [here](#existing-mnemonic-arguments) for `existing-mnemonic` arguments

## Development

### Install basic requirements

```sh
python3 -m pip install -r requirements.txt
python3 setup.py install
```

### Install testing requirements

```sh
python3 -m pip install -r requirements_test.txt
```

### Run tests

```sh
python3 -m pytest .
```
