# eth2.0-deposit-cli

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Tutorial for users](#tutorial-for-users)
  - [Requirements](#requirements)
  - [For Linux or MacOS users](#for-linux-or-macos-users)
    - [Step 1. Install deposit-cli dependencies](#step-1-install-deposit-cli-dependencies)
    - [Step 2. Create your keys and deposit data](#step-2-create-your-keys-and-deposit-data)
    - [Arguments](#arguments)
  - [For Windows users](#for-windows-users)
    - [Step 1. Install deposit-cli dependencies](#step-1-install-deposit-cli-dependencies-1)
    - [Step 2. Create your keys and deposit data](#step-2-create-your-keys-and-deposit-data-1)
    - [Arguments](#arguments-1)
  - [For `venv` users](#for-venv-users)
- [Development](#development)
  - [Install basic requirements](#install-basic-requirements)
  - [Install testing requirements](#install-testing-requirements)
  - [Run tests](#run-tests)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Pre-production warning

This software is a pre-release version which has not yet been audited and therefore should not yet be trusted to keys with the intent of securing actual ETH.

### BLS versioning

The eth2specs changed their BLS version from [BLS v0](https://tools.ietf.org/html/draft-irtf-cfrg-bls-signature-00), and [hash to curve v4](https://tools.ietf.org/html/draft-irtf-cfrg-hash-to-curve-04) to [BLS v2](https://tools.ietf.org/html/draft-irtf-cfrg-bls-signature-02), and [hash to curve v7](https://tools.ietf.org/html/draft-irtf-cfrg-hash-to-curve-07). Because of this this version of the deposit CLI, is not compatible with eth2 versions >= `0.12.x` which includes main net.

**Using this version for Mainnet deposits will result in loss of funds**

## Tutorial for users

### Requirements

- [Python **3.7+**](https://www.python.org/about/gettingstarted/)
- [pip3](https://pip.pypa.io/en/stable/installing/)

### For Linux or MacOS users

#### Step 1. Install deposit-cli dependencies

If it's your first time to use this tool, you need to install the Python library dependencies:

```sh
./deposit.sh install
```

#### Step 2. Create your keys and deposit data

Run the following command to enter the interactive CLI:

```sh
./deposit.sh
```

You can also run the tool with optional arguments:

```sh
./deposit.sh --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --folder=<YOUR_FOLDER_PATH>
```

#### Arguments

| Argument | Type | Description |
| -------- | -------- | -------- |
| `--num_validators`  | Non-negative integer | The number of signing keys you want to generate. Note that the child key(s) are generated via the same master key. |
| `--mnemonic_language` | String. Options: `czech`, `chinese_traditional`, `chinese_simplified`, `english`, `spanish`, `italian`, `korean`. Default to `english` | The mnemonic language |
| `--folder` | String. Pointing to `./validator_keys` by default | The folder path for the keystore(s) and deposit(s) |
| `--chain` | String. `mainnet` by defualt | The chain setting for the signing domain. |

### For Windows users

#### Step 1. Install deposit-cli dependencies

If it's your first time to use this tool, you need to install the Python library dependencies:

```sh
sh deposit.sh install
```

#### Step 2. Create your keys and deposit data

Run the following command to enter the interactive CLI:

```sh
sh deposit.sh
```

You can also run the tool with optional arguments:

```sh
sh deposit.sh --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --folder=<YOUR_FOLDER_PATH>
```

You will see the following messages after successfully generated the keystore(s) and the deposit(s):

#### Arguments

See [here](#arguments)

```
Creating your keys.
Saving your keystore(s).
Creating your deposit(s).
Verifying your keystore(s).
Verifying your deposit(s).

Success!
Your keys can be found at: <YOUR_FOLDER_PATH>
```

### For `venv` users

If you want to use Python [`venv`](https://docs.python.org/3.7/library/venv.html), just run:

```sh
make venv_deposit
```

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
