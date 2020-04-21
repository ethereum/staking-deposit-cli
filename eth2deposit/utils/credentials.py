import os
import time
import json
from typing import List
from py_ecc.bls import G2ProofOfPossession as bls

from key_handling.key_derivation.path import mnemonic_and_path_to_key
from key_handling.keystore import (
    Keystore,
    ScryptKeystore,
)
from utils.crypto import SHA256
from utils.ssz import (
    compute_domain,
    compute_signing_root,
    DepositMessage,
    Deposit,
)


class ValidatorCredentials:
    def __init__(self, *, mnemonic: str, index: int, amount: int):
        self.signing_key_path = 'm/12381/3600/%s/0' % index
        self.signing_sk = mnemonic_and_path_to_key(mnemonic=mnemonic, path=self.signing_key_path)
        self.withdrawal_sk = mnemonic_and_path_to_key(mnemonic=mnemonic, path=self.signing_key_path + '/0')
        self.amount = amount

    @property
    def signing_pk(self):
        return bls.PrivToPub(self.signing_sk)

    @property
    def withdrawal_pk(self):
        return bls.PrivToPub(self.withdrawal_sk)

    def signing_keystore(self, password: str) -> ScryptKeystore:
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


def mnemonic_to_credentials(*, mnemonic: str, num_keys: int,
                            amounts: List[int], start_index: int=0,) -> List[ValidatorCredentials]:
    assert len(amounts) == num_keys
    key_indices = range(start_index, start_index + num_keys)
    credentials = [ValidatorCredentials(mnemonic=mnemonic, index=index, amount=amounts[index])
                   for index in key_indices]
    return credentials


def export_keystores(*, credentials: List[ValidatorCredentials], password: str, folder: str) -> List[str]:
    return [credential.save_signing_keystore(password=password, folder=folder) for credential in credentials]


def sign_deposit_data(deposit_data: DepositMessage, sk: int) -> Deposit:
    '''
    Given a DepositMessage, it signs its root and returns a Deposit
    '''
    assert bls.PrivToPub(sk) == deposit_data.pubkey
    domain = compute_domain()
    signing_root = compute_signing_root(deposit_data, domain)
    signed_deposit_data = Deposit(
        **deposit_data.as_dict(),
        signature=bls.Sign(sk, signing_root)
    )
    return signed_deposit_data


def export_deposit_data_json(*, credentials: List[ValidatorCredentials], folder: str):
    deposit_data: List[dict] = []
    for credential in credentials:
        deposit_datum = DepositMessage(
            pubkey=credential.signing_pk,
            withdrawal_credentials=SHA256(credential.withdrawal_pk),
            amount=credential.amount,
        )
        signed_deposit_datum = sign_deposit_data(deposit_datum, credential.signing_sk)
        datum_dict = signed_deposit_datum.as_dict()
        datum_dict.update({'deposit_data_root': deposit_datum.hash_tree_root})
        datum_dict.update({'signed_deposit_data_root': signed_deposit_datum.hash_tree_root})
        deposit_data.append(datum_dict)

    filefolder = os.path.join(folder, 'deposit_data-%i.json' % time.time())
    with open(filefolder, 'w') as f:
        json.dump(deposit_data, f, default=lambda x: x.hex())
    return filefolder


def verify_keystores(*, credentials: List[ValidatorCredentials],
                     keystore_filefolders: List[str], password: str) -> bool:
    return all(credential.verify_keystore(keystore_filefolder=filefolder, password=password)
               for credential, filefolder in zip(credentials, keystore_filefolders))
