# eth2.0-deposit-cli

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Tutorial for users](#tutorial-for-users)
  - [Requirements](#requirements)
  - [For Linux or MacOS users](#for-linux-or-macos-users)
    - [Step 1. Install deposit-cli dependencies](#step-1-install-deposit-cli-dependencies)
    - [Step 2. Create your keys and deposit data](#step-2-create-your-keys-and-deposit-data)
  - [For Windows users](#for-windows-users)
    - [Step 1. Install deposit-cli dependencies](#step-1-install-deposit-cli-dependencies-1)
    - [Step 2. Create your keys and deposit data](#step-2-create-your-keys-and-deposit-data-1)
  - [For `venv` users](#for-venv-users)
- [Development](#development)
  - [Install basic requirements](#install-basic-requirements)
  - [Install testing requirements](#install-testing-requirements)
  - [Run tests](#run-tests)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

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

Run the following command:

```sh
./deposit.sh
```

You can also run the tool with optional arguments:

```sh
./deposit.sh --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --password=<YOUR_PASSWORD> --folder=<YOUR_FOLDER_PATH>
```

### For Windows users

#### Step 1. Install deposit-cli dependencies

If it's your first time to use this tool, you need to install the Python library dependencies:

```sh
sh deposit.sh install
```

#### Step 2. Create your keys and deposit data

Run the following command:

```sh
sh deposit.sh
```

You can also run the tool with optional arguments:

```sh
sh deposit.sh --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --password=<YOUR_PASSWORD> --folder=<YOUR_FOLDER_PATH>
```

You should see the following messages after successfully generated the keystore(s) and the deposit(s):

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
