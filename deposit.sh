#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo $OSTYPE

    if [[ $1 == install ]]; then
        python3 -m pip3 install -r requirements.txt
        python3 setup.py install
        exit 1
    fi

    python3 ./eth2deposit/deposit.py "$@"

elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo $OSTYPE
    if [[ $1 == install ]]; then
        python -m pip install -r requirements.txt
        python setup.py install
        exit 1
    fi

    python ./eth2deposit/deposit.py "$@"

else
    echo "Sorry, to run deposit-cli on" $(uname -s)", please see the trouble-shooting on https://github.com/ethereum/eth2.0-deposit-cli"
    exit 1

fi
