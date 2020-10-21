import os
import time
import json
from typing import Dict, List
from py_ecc.bls import G2ProofOfPossession as bls

from eth2deposit.exceptions import ValidationError
from eth2deposit.key_handling.key_derivation.path import mnemonic_and_path_to_key
from eth2deposit.key_handling.keystore import (
    Keystore,
    ScryptKeystore,
)
from eth2deposit.settings import DEPOSIT_CLI_VERSION
from eth2deposit.utils.constants import (
    BLS_WITHDRAWAL_PREFIX,
    ETH2GWEI,
    MAX_DEPOSIT_AMOUNT,
    MIN_DEPOSIT_AMOUNT,
)
from eth2deposit.utils.crypto import SHA256
from eth2deposit.utils.ssz import (
    compute_deposit_domain,
    compute_signing_root,
    DepositData,
    DepositMessage,
)


class Credential:
    """
    A Credential object contains all of the information for a single validator and the corresponding functionality.
    Once created, it is the only object that should be required to perform any processing for a validator.
    """
    def __init__(self, *, mnemonic: str, index: int, amount: int, fork_version: bytes):
        # Set path as EIP-2334 format
        # https://eips.ethereum.org/EIPS/eip-2334
        purpose = '12381'
        coin_type = '3600'
        account = str(index)
        withdrawal_key_path = f'm/{purpose}/{coin_type}/{account}/0'
        self.signing_key_path = f'{withdrawal_key_path}/0'

        # Do NOT use password for seed generation.
        self.withdrawal_sk = mnemonic_and_path_to_key(mnemonic=mnemonic, path=withdrawal_key_path, password='')
        self.signing_sk = mnemonic_and_path_to_key(mnemonic=mnemonic, path=self.signing_key_path, password='')
        self.amount = amount
        self.fork_version = fork_version

    @property
    def signing_pk(self) -> bytes:
        return bls.SkToPk(self.signing_sk)

    @property
    def withdrawal_pk(self) -> bytes:
        return bls.SkToPk(self.withdrawal_sk)

    @property
    def withdrawal_credentials(self) -> bytes:
        withdrawal_credentials = BLS_WITHDRAWAL_PREFIX
        withdrawal_credentials += SHA256(self.withdrawal_pk)[1:]
        return withdrawal_credentials

    @property
    def deposit_message(self) -> DepositMessage:
        if not MIN_DEPOSIT_AMOUNT <= self.amount <= MAX_DEPOSIT_AMOUNT:
            raise ValidationError(f"{self.amount / ETH2GWEI} ETH deposits are not within the bounds of this cli.")
        return DepositMessage(
            pubkey=self.signing_pk,
            withdrawal_credentials=self.withdrawal_credentials,
            amount=self.amount,
        )

    @property
    def signed_deposit(self) -> DepositData:
        domain = compute_deposit_domain(fork_version=self.fork_version)
        signing_root = compute_signing_root(self.deposit_message, domain)
        signed_deposit = DepositData(
            **self.deposit_message.as_dict(),
            signature=bls.Sign(self.signing_sk, signing_root)
        )
        return signed_deposit

    @property
    def deposit_datum_dict(self) -> Dict[str, bytes]:
        """
        Return a single deposit datum for 1 validator including all
        the information needed to verify and process the deposit.
        """
        signed_deposit_datum = self.signed_deposit
        datum_dict = signed_deposit_datum.as_dict()
        datum_dict.update({'deposit_message_root': self.deposit_message.hash_tree_root})
        datum_dict.update({'deposit_data_root': signed_deposit_datum.hash_tree_root})
        datum_dict.update({'fork_version': self.fork_version})
        datum_dict.update({'deposit_cli_version': DEPOSIT_CLI_VERSION})
        return datum_dict

    def signing_keystore(self, password: str) -> Keystore:
        secret = self.signing_sk.to_bytes(32, 'big')
        return ScryptKeystore.encrypt(secret=secret, password=password, path=self.signing_key_path)

    def save_signing_keystore(self, password: str, folder: str) -> str:
        keystore = self.signing_keystore(password)
        filefolder = os.path.join(folder, 'keystore-%s-%i.json' % (keystore.path.replace('/', '_'), time.time()))
        keystore.save(filefolder)
        return filefolder

    def verify_keystore(self, keystore_filefolder: str, password: str) -> bool:
        saved_keystore = Keystore.from_json(keystore_filefolder)
        secret_bytes = saved_keystore.decrypt(password)
        return self.signing_sk == int.from_bytes(secret_bytes, 'big')


class CredentialList:
    """
    A collection of multiple Credentials, one for each validator.
    """
    def __init__(self, credentials: List[Credential]):
        self.credentials = credentials

    @classmethod
    def from_mnemonic(cls,
                      *,
                      mnemonic: str,
                      num_keys: int,
                      amounts: List[int],
                      fork_version: bytes,
                      start_index: int=0) -> 'CredentialList':
        if len(amounts) != num_keys:
            raise ValueError(
                f"The number of keys ({num_keys}) doesn't equal to the corresponding deposit amounts ({len(amounts)})."
            )
        key_indices = range(start_index, start_index + num_keys)
        return cls([Credential(mnemonic=mnemonic, index=index, amount=amounts[index], fork_version=fork_version)
                    for index in key_indices])

    def export_keystores(self, password: str, folder: str) -> List[str]:
        return [credential.save_signing_keystore(password=password, folder=folder) for credential in self.credentials]

    def export_deposit_data_json(self, folder: str) -> str:
        deposit_data = [cred.deposit_datum_dict for cred in self.credentials]
        filefolder = os.path.join(folder, 'deposit_data-%i.json' % time.time())
        with open(filefolder, 'w') as f:
            json.dump(deposit_data, f, default=lambda x: x.hex())
        return filefolder

    def verify_keystores(self, keystore_filefolders: List[str], password: str) -> bool:
        return all(credential.verify_keystore(keystore_filefolder=filefolder, password=password)
                   for credential, filefolder in zip(self.credentials, keystore_filefolders))
