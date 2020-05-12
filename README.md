# eth2.0-deposit-cli

## Tutorial for users

### Create deposits

```sh
./deposit.sh --num_validators=<NUM_VALIDATORS> --mnemonic_language=english --password=<YOUR_PASSWORD> --folder=<YOUR_FOLDER_PATH>
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
