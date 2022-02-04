#!/bin/bash

if [[ "$OSTYPE" == "linux"* ]] || [[ "$OSTYPE" == "linux-android"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo $OSTYPE
    if [[ $1 == "install" ]]; then
        echo "Installing dependencies..."
        pip3 install -r requirements.txt
        python3 setup.py install
        exit 1
    fi
    echo "Running deposit-cli..."
    python3 ./staking_deposit/deposit.py "$@"

elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo $OSTYPE
    if [[ $1 == "install" ]]; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
        python setup.py install
        exit 1
    fi
    echo "Running deposit-cli..."
    python ./staking_deposit/deposit.py "$@"

else
    echo "Sorry, to run deposit-cli on" $(uname -s)", please see the trouble-shooting on https://github.com/ethereum/staking-deposit-cli"
    exit 1

fi
