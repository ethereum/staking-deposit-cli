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
        - [Arguments](#arguments)
        - [Successful message](#successful-message)
    - [Option 2. Build `deposit-cli` with native Python](#option-2-build-deposit-cli-with-native-python)
      - [Step 0. Python version checking](#step-0-python-version-checking)
      - [Step 1. Installation](#step-1-installation-1)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-1)
        - [Arguments](#arguments-1)
        - [Successful message](#successful-message-1)
    - [Option 3. Build `deposit-cli` with `virtualenv`](#option-3-build-deposit-cli-with-virtualenv)
      - [Step 0. Python version checking](#step-0-python-version-checking-1)
      - [Step 1. Installation](#step-1-installation-2)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-2)
        - [Arguments](#arguments-2)
        - [Successful message](#successful-message-2)
  - [For Windows users](#for-windows-users)
    - [Option 1. Download binary executable file](#option-1-download-binary-executable-file-1)
      - [Step 1. Installation](#step-1-installation-3)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-3)
        - [Arguments](#arguments-3)
        - [Successful message](#successful-message-3)
    - [Option 2. Build `deposit-cli` with native Python](#option-2-build-deposit-cli-with-native-python-1)
      - [Step 0. Python version checking](#step-0-python-version-checking-2)
      - [Step 1. Installation](#step-1-installation-4)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-4)
        - [Arguments](#arguments-4)
        - [Successful message](#successful-message-4)
    - [Option 3. Build `deposit-cli` with `virtualenv`](#option-3-build-deposit-cli-with-virtualenv-1)
      - [Step 0. Python version checking](#step-0-python-version-checking-3)
      - [Step 1. Installation](#step-1-installation-5)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-5)
        - [Arguments](#arguments-5)
        - [Successful message](#successful-message-5)
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

Run the following command to enter the interactive CLI:

```sh
./deposit
```

You can also run the tool with optional arguments:

```sh
./deposit --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

###### Arguments

You can use `--help` flag to see all arguments.

| Argument | Type | Description |
| -------- | -------- | -------- |
| `--num_validators`  | Non-negative integer | The number of signing keys you want to generate. Note that the child key(s) are generated via the same master key. |
| `--mnemonic_language` | String. Options: `czech`, `chinese_traditional`, `chinese_simplified`, `english`, `spanish`, `italian`, `korean`. Default to `english` | The mnemonic language |
| `--folder` | String. Pointing to `./validator_keys` by default | The folder path for the keystore(s) and deposit(s) |
| `--chain` | String. `mainnet` by default | The chain setting for the signing domain. |

###### Successful message

You will see the following messages after successfully generated the keystore(s) and the deposit(s):

```
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

Run the following command to enter the interactive CLI:

```sh
./deposit.sh
```

You can also run the tool with optional arguments:

```sh
./deposit.sh --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

###### Arguments
See [here](#arguments)

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
./venv/bin/activate
```

and install the dependencies:

```sh
python setup.py install
pip install -r requirements.txt
```

##### Step 2. Create keys and `deposit_data-*.json`

Run the following command to enter the interactive CLI:

```sh
python ./eth2deposit/deposit.py
```

You can also run the tool with optional arguments:

```sh
python ./eth2deposit/deposit.py --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

###### Arguments
See [here](#arguments)

###### Successful message
See [here](#successful-message)

----

### For Windows users

#### Option 1. Download binary executable file

##### Step 1. Installation

See [releases page](https://github.com/ethereum/eth2.0-deposit-cli/releases) to download and decompress the corresponding binary files.

##### Step 2. Create keys and `deposit_data-*.json`

Run the following command to enter the interactive CLI:

```sh
deposit.exe
```

You can also run the tool with optional arguments:

```sh
deposit.exe --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

###### Arguments
See [here](#arguments)

###### Successful message
See [here](#successful-message)

#### Option 2. Build `deposit-cli` with native Python

##### Step 0. Python version checking

Ensure you are using Python version >= Python3.7:

```sh
python -V
```

##### Step 1. Installation

Install the dependencies:

```sh
pip install -r requirements.txt
python setup.py install
```

Or use the helper script:

```sh
sh deposit.sh install
```

##### Step 2. Create keys and `deposit_data-*.json`

Run the following command to enter the interactive CLI:

```sh
sh deposit.sh
```

You can also run the tool with optional arguments:

```sh
sh deposit.sh --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

###### Arguments
See [here](#arguments)

###### Successful message
See [here](#successful-message)

#### Option 3. Build `deposit-cli` with `virtualenv`

##### Step 0. Python version checking

Ensure you are using Python version >= Python3.7:

```sh
python -V
```

##### Step 1. Installation

For the [virtualenv](https://virtualenv.pypa.io/en/latest/) users, you can create a new venv:

```sh
pip install virtualenv
virtualenv venv
./venv/bin/activate
```

and install the dependencies:

```sh
python setup.py install
pip install -r requirements.txt
```

##### Step 2. Create keys and `deposit_data-*.json`

Run the following command to enter the interactive CLI:

```sh
python ./eth2deposit/deposit.py
```

You can also run the tool with optional arguments:

```sh
python ./eth2deposit/deposit.py --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

###### Arguments
See [here](#arguments)

###### Successful message
See [here](#successful-message)

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
