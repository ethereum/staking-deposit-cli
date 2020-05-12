#!/bin/bash

case "$(uname -s)" in

    Darwin)
        echo 'Mac OS X'
        python3 -m pip install -r requirements.txt
        python3 setup.py install
        python3 ./eth2deposit/deposit.py "$@"
        ;;

    Linux)
        echo 'Linux'
        python3 -m pip install -r requirements.txt
        python3 setup.py install
        python3 ./eth2deposit/deposit.py "$@"
        ;;

    CYGWIN*|MINGW32*|MSYS*|MINGW*)
        echo 'MS Windows'
        python -m pip install -r requirements.txt
        python setup.py install
        python ./eth2deposit/deposit.py "$@"
        ;;

    *)
        echo 'Other OS'
        ;;

esac
