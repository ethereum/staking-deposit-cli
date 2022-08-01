# staking-deposit-cli

[![GitPOAP Badge](https://public-api.gitpoap.io/v1/repo/ethereum/staking-deposit-cli/badge)](https://www.gitpoap.io/gh/ethereum/staking-deposit-cli)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Introduction](#introduction)
- [Tutorial for users](#tutorial-for-users)
  - [Build requirements](#build-requirements)
  - [For Linux or MacOS users](#for-linux-or-macos-users)
    - [File Permissions](#file-permissions)
    - [Option 1. Download binary executable file](#option-1-download-binary-executable-file)
      - [Step 1. Installation](#step-1-installation)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json)
        - [language Argument](#language-argument)
        - [Commands](#commands)
        - [`new-mnemonic` Arguments](#new-mnemonic-arguments)
        - [`existing-mnemonic` Arguments](#existing-mnemonic-arguments)
        - [Successful message](#successful-message)
    - [Option 2. Build `deposit-cli` with native Python](#option-2-build-deposit-cli-with-native-python)
      - [Step 0. Python version checking](#step-0-python-version-checking)
      - [Step 1. Installation](#step-1-installation-1)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-1)
        - [Language Argument](#language-argument)
        - [Commands](#commands-1)
        - [Arguments](#arguments)
        - [Successful message](#successful-message-1)
    - [Option 3. Build `deposit-cli` with `virtualenv`](#option-3-build-deposit-cli-with-virtualenv)
      - [Step 0. Python version checking](#step-0-python-version-checking-1)
      - [Step 1. Installation](#step-1-installation-2)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-2)
        - [Language Argument](#language-argument-1)
        - [Commands](#commands-2)
        - [Arguments](#arguments-1)
    - [Option 4. Use Docker image](#option-4-use-docker-image)
      - [Step 1. Build the docker image](#step-1-build-the-docker-image)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-3)
        - [Arguments](#arguments-2)
        - [Successful message](#successful-message-2)
  - [For Windows users](#for-windows-users)
    - [Option 1. Download binary executable file](#option-1-download-binary-executable-file-1)
      - [Step 1. Installation](#step-1-installation-3)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-4)
        - [Language Argument](#language-argument-2)
        - [Commands](#commands-3)
        - [Arguments](#arguments-3)
    - [Option 2. Build `deposit-cli` with native Python](#option-2-build-deposit-cli-with-native-python-1)
      - [Step 0. Python version checking](#step-0-python-version-checking-2)
      - [Step 1. Installation](#step-1-installation-4)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-5)
        - [Language Argument](#language-argument-3)
        - [Commands](#commands-4)
        - [Arguments](#arguments-4)
    - [Option 3. Build `deposit-cli` with `virtualenv`](#option-3-build-deposit-cli-with-virtualenv-1)
      - [Step 0. Python version checking](#step-0-python-version-checking-3)
      - [Step 1. Installation](#step-1-installation-5)
      - [Step 2. Create keys and `deposit_data-*.json`](#step-2-create-keys-and-deposit_data-json-6)
        - [Language Argument](#language-argument-4)
        - [Commands](#commands-5)
        - [Arguments](#arguments-5)
- [Development](#development)
  - [Install basic requirements](#install-basic-requirements)
  - [Install testing requirements](#install-testing-requirements)
  - [Run tests](#run-tests)
  - [Building Binaries](#building-binaries)
      - [Mac M1 Binaries](#mac-m1-binaries)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introduction

`deposit-cli` is a tool for creating [EIP-2335 format](https://eips.ethereum.org/EIPS/eip-2335) BLS12-381 keystores and a corresponding `deposit_data*.json` file for [Ethereum Staking Launchpad](https://github.com/ethereum/staking-launchpad).

- **Warning: Please generate your keystores on your own safe, completely offline device.**
- **Warning: Please backup your mnemonic, keystores, and password securely.**

Please read [Launchpad Validator FAQs](https://launchpad.ethereum.org/faq#keys) before generating the keys.

You can find the audit report by Trail of Bits [here](https://github.com/trailofbits/publications/blob/master/reviews/ETH2DepositCLI.pdf).

## Tutorial for users

### Build requirements

- [Python **3.8+**](https://www.python.org/about/gettingstarted/)
- [pip3](https://pip.pypa.io/en/stable/installing/)

### For Linux or MacOS users

#### File Permissions

On Unix-based systems, keystores and the `deposit_data*.json` have `440`/`-r--r-----` file permissions (user & group read only). This improves security by limiting which users and processes that have access to these files. If you are getting `permission denied` errors when handling your keystores, consider changing which user/group owns the file (with `chown`) or, if need be, change the file permissions with `chmod`.

#### Option 1. Download binary executable file

##### Step 1. Installation

See [releases page](https://github.com/ethereum/staking-deposit-cli/releases) to download and decompress the corresponding binary files.

##### Step 2. Create keys and `deposit_data-*.json`

Run the following command to enter the interactive CLI and generate keys from a new mnemonic:

```sh
./deposit new-mnemonic
```

or run the following command to enter the interactive CLI and generate keys from an existing:

```sh
./deposit existing-mnemonic
```

###### language Argument

The Launchpad offers many language/internationalization options. If you wish to select one as a CLI argument, it must be passed in before one of the commands is chosen.

| Argument | Type | Description |
| -------- | -------- | -------- |
| `--language` | String. Options: `العربية`, `ελληνικά`, `English`, `Français`, `Bahasa melayu`, `Italiano`, `日本語`, `한국어`, `Português do Brasil`, `român`, `简体中文`. Default to `English` | The language you wish to use the CLI in. |

###### Commands

The CLI offers different commands depending on what you want to do with the tool.

| Command | Description |
| ------- | ----------- |
| `new-mnemonic` | (Recommended) This command is used to generate keystores with a new mnemonic. |
| `existing-mnemonic` | This command is used to re-generate or derive new keys from your existing mnemonic. Use this command, if (i) you have already generated keys with this CLI before, (ii) you want to reuse your mnemonic that you know is secure that you generated elsewhere (reusing your eth1 mnemonic .etc), or (iii) you lost your keystores and need to recover your keys. |

###### `new-mnemonic` Arguments

You can use `new-mnemonic --help` to see all arguments. Note that if there are missing arguments that the CLI needs, it will ask you for them.

| Argument | Type | Description |
| -------- | -------- | -------- |
| `--num_validators`  | Non-negative integer | The number of signing keys you want to generate. Note that the child key(s) are generated via the same master key. |
| `--mnemonic_language` | String. Options: `简体中文`, `繁體中文`, `český jazyk`, `English`, `Italiano`, `한국어`, `Português`, `Español`. Default to `English` | The mnemonic language |
| `--folder` | String. Pointing to `./validator_keys` by default | The folder path for the keystore(s) and deposit(s) |
| `--chain` | String. `mainnet` by default | The chain setting for the signing domain. |
| `--eth1_withdrawal_address` | String. Eth1 address in hexadecimal encoded form | If this field is set and valid, the given Eth1 address will be used to create the withdrawal credentials. Otherwise, it will generate withdrawal credentials with the mnemonic-derived withdrawal public key in [EIP-2334 format](https://eips.ethereum.org/EIPS/eip-2334#eth2-specific-parameters). |

###### `existing-mnemonic` Arguments

You can use `existing-mnemonic --help` to see all arguments. Note that if there are missing arguments that the CLI needs, it will ask you for them.

| Argument | Type | Description |
| -------- | -------- | -------- |
| `--validator_start_index` | Non-negative integer | The index of the first validator's keys you wish to generate. If this is your first time generating keys with this mnemonic, use 0. If you have generated keys using this mnemonic before, use the next index from which you want to start generating keys from (eg, if you've generated 4 keys before (keys #0, #1, #2, #3), then enter 4 here.|
| `--num_validators`  | Non-negative integer | The number of new signing keys you want to generate. Note that the child key(s) are generated via the same master key. |
| `--folder` | String. Pointing to `./validator_keys` by default | The folder path for the keystore(s) and deposit(s) |
| `--chain` | String. `mainnet` by default | The chain setting for the signing domain. |
| `--eth1_withdrawal_address` | String. Eth1 address in hexadecimal encoded form | If this field is set and valid, the given Eth1 address will be used to create the withdrawal credentials. Otherwise, it will generate withdrawal credentials with the mnemonic-derived withdrawal public key in [EIP-2334 format](https://eips.ethereum.org/EIPS/eip-2334#eth2-specific-parameters). |

###### Successful message

You will see the following messages after successfully generated the keystore(s) and the deposit(s):

```text
Creating your keys:               [####################################]  <N>/<N>
Creating your keystores:          [####################################]  <N>/<N>
Creating your depositdata:        [####################################]  <N>/<N>
Verifying your keystores:         [####################################]  <N>/<N>
Verifying your deposits:          [####################################]  <N>/<N>

Success!
Your keys can be found at: <YOUR_FOLDER_PATH>
```

#### Option 2. Build `deposit-cli` with native Python

##### Step 0. Python version checking

Ensure you are using Python version >= Python3.8:

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

###### Language Argument

See [here](#language_argument) for `--language` arguments.
###### Commands

See [here](#commands)

###### Arguments

See [here](#new-mnemonic-arguments) for `new-mnemonic` arguments
See [here](#existing-mnemonic-arguments) for `existing-mnemonic` arguments

###### Successful message
See [here](#successful-message)

#### Option 3. Build `deposit-cli` with `virtualenv`

##### Step 0. Python version checking

Ensure you are using Python version >= Python3.8:

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
python3 ./staking_deposit/deposit.py new-mnemonic
```

or

```sh
python3 ./staking_deposit/deposit.py existing-mnemonic
```

You can also run the tool with optional arguments:

```sh
python3 ./staking_deposit/deposit.py new-mnemonic --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

```sh
python3 ./staking_deposit/deposit.py existing-mnemonic --num_validators=<NUM_VALIDATORS> --validator_start_index=<START_INDEX> --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

###### Language Argument

See [here](#language_argument) for `--language` arguments.

###### Commands

See [here](#commands)

###### Arguments

See [here](#new-mnemonic-arguments) for `new-mnemonic` arguments
See [here](#existing-mnemonic-arguments) for `existing-mnemonic` arguments

#### Option 4. Use Docker image

##### Step 1. Build the docker image

Run the following command to locally build the docker image:

```sh
make build_docker
```

##### Step 2. Create keys and `deposit_data-*.json`

Run the following command to enter the interactive CLI:

```sh
docker run -it --rm -v $(pwd)/validator_keys:/app/validator_keys ethereum/staking-deposit-cli
```

You can also run the tool with optional arguments:

```sh
docker run -it --rm -v $(pwd)/validator_keys:/app/validator_keys ethereum/staking-deposit-cli new-mnemonic --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --folder=<YOUR_FOLDER_PATH>
```

Example for 1 validator on the [Prater testnet](https://prater.launchpad.ethereum.org/) using english:

```sh
docker run -it --rm -v $(pwd)/validator_keys:/app/validator_keys ethereum/staking-deposit-cli new-mnemonic --num_validators=1 --mnemonic_language=english --chain=prater
```

###### Arguments
See [here](#arguments)

###### Successful message
See [here](#successful-message)

----

### For Windows users

#### Option 1. Download binary executable file

##### Step 1. Installation

See [releases page](https://github.com/ethereum/staking-deposit-cli/releases) to download and decompress the corresponding binary files.

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

###### Language Argument

See [here](#language_argument) for `--language` arguments.

###### Commands

See [here](#commands)

###### Arguments

See [here](#new-mnemonic-arguments) for `new-mnemonic` arguments
See [here](#existing-mnemonic-arguments) for `existing-mnemonic` arguments

#### Option 2. Build `deposit-cli` with native Python

##### Step 0. Python version checking

Ensure you are using Python version >= Python3.8 (Assume that you've installed Python 3 as the main Python):

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

###### Language Argument

See [here](#language_argument) for `--language` arguments.

###### Commands

See [here](#commands)

###### Arguments

See [here](#new-mnemonic-arguments) for `new-mnemonic` arguments
See [here](#existing-mnemonic-arguments) for `existing-mnemonic` arguments

#### Option 3. Build `deposit-cli` with `virtualenv`

##### Step 0. Python version checking

Ensure you are using Python version >= Python3.8 (Assume that you've installed Python 3 as the main Python):

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

```cmd
python .\staking_deposit\deposit.py new-mnemonic
```

or

```cmd
python .\staking_deposit\deposit.py existing-mnemonic
```

You can also run the tool with optional arguments:

```cmd
python .\staking_deposit\deposit.py new-mnemonic --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

```cmd
python .\staking_deposit\deposit.pyexisting-mnemonic --num_validators=<NUM_VALIDATORS> --validator_start_index=<START_INDEX> --chain=<CHAIN_NAME> --folder=<YOUR_FOLDER_PATH>
```

###### Language Argument

See [here](#language_argument) for `--language` arguments.

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

### Building Binaries
**Developers Only**
##### Mac M1 Binaries

👋This is not the section you are looking for.👋
If you are trying to **build the binary** on macos with an M1 Mac and you are using pyenv to manage your python version. You'll probably need to reinstall a given python version using:
```
env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.10.3
```
