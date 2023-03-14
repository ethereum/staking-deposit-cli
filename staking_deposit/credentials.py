import os
import click
from enum import Enum
import time
import json
from typing import Dict, List, Optional, Any, Sequence

from eth_typing import Address, HexAddress
from eth_utils import to_canonical_address
from py_ecc.bls import G2ProofOfPossession as bls

from staking_deposit.exceptions import ValidationError
from staking_deposit.key_handling.key_derivation.path import mnemonic_and_path_to_key
from staking_deposit.key_handling.keystore import (
    Keystore,
    ScryptKeystore,
)
from staking_deposit.settings import DEPOSIT_CLI_VERSION, BaseChainSetting
from staking_deposit.utils.constants import (
    BLS_WITHDRAWAL_PREFIX,
    ETH1_ADDRESS_WITHDRAWAL_PREFIX,
    ETH2GWEI,
    MAX_DEPOSIT_AMOUNT,
    MIN_DEPOSIT_AMOUNT,
)
from staking_deposit.utils.crypto import SHA256
from staking_deposit.utils.intl import load_text
from staking_deposit.utils.ssz import (
    compute_deposit_domain,
    compute_bls_to_execution_change_domain,
    compute_signing_root,
    BLSToExecutionChange,
    DepositData,
    DepositMessage,
    SignedBLSToExecutionChange,
)


class WithdrawalType(Enum):
    BLS_WITHDRAWAL = 0
    ETH1_ADDRESS_WITHDRAWAL = 1


class Credential:
    """
    A Credential object contains all of the information for a single validator and the corresponding functionality.
    Once created, it is the only object that should be required to perform any processing for a validator.
    """
    def __init__(self, *, mnemonic: str, mnemonic_password: str,
                 index: int, amount: int, chain_setting: BaseChainSetting,
                 hex_eth1_withdrawal_address: Optional[HexAddress]):
        # Set path as EIP-2334 format
        # https://eips.ethereum.org/EIPS/eip-2334
        purpose = '12381'
        coin_type = '3600'
        account = str(index)
        withdrawal_key_path = f'm/{purpose}/{coin_type}/{account}/0'
        self.signing_key_path = f'{withdrawal_key_path}/0'

        self.withdrawal_sk = mnemonic_and_path_to_key(
            mnemonic=mnemonic, path=withdrawal_key_path, password=mnemonic_password)
        self.signing_sk = mnemonic_and_path_to_key(
            mnemonic=mnemonic, path=self.signing_key_path, password=mnemonic_password)
        self.amount = amount
        self.chain_setting = chain_setting
        self.hex_eth1_withdrawal_address = hex_eth1_withdrawal_address

    @property
    def signing_pk(self) -> bytes:
        return bls.SkToPk(self.signing_sk)

    @property
    def withdrawal_pk(self) -> bytes:
        return bls.SkToPk(self.withdrawal_sk)

    @property
    def eth1_withdrawal_address(self) -> Optional[Address]:
        if self.hex_eth1_withdrawal_address is None:
            return None
        return to_canonical_address(self.hex_eth1_withdrawal_address)

    @property
    def withdrawal_prefix(self) -> bytes:
        if self.eth1_withdrawal_address is not None:
            return ETH1_ADDRESS_WITHDRAWAL_PREFIX
        else:
            return BLS_WITHDRAWAL_PREFIX

    @property
    def withdrawal_type(self) -> WithdrawalType:
        if self.withdrawal_prefix == BLS_WITHDRAWAL_PREFIX:
            return WithdrawalType.BLS_WITHDRAWAL
        elif self.withdrawal_prefix == ETH1_ADDRESS_WITHDRAWAL_PREFIX:
            return WithdrawalType.ETH1_ADDRESS_WITHDRAWAL
        else:
            raise ValueError(f"Invalid withdrawal_prefix {self.withdrawal_prefix.hex()}")

    @property
    def withdrawal_credentials(self) -> bytes:
        if self.withdrawal_type == WithdrawalType.BLS_WITHDRAWAL:
            withdrawal_credentials = BLS_WITHDRAWAL_PREFIX
            withdrawal_credentials += SHA256(self.withdrawal_pk)[1:]
        elif (
            self.withdrawal_type == WithdrawalType.ETH1_ADDRESS_WITHDRAWAL
            and self.eth1_withdrawal_address is not None
        ):
            withdrawal_credentials = ETH1_ADDRESS_WITHDRAWAL_PREFIX
            withdrawal_credentials += b'\x00' * 11
            withdrawal_credentials += self.eth1_withdrawal_address
        else:
            raise ValueError(f"Invalid withdrawal_type {self.withdrawal_type}")
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
        domain = compute_deposit_domain(fork_version=self.chain_setting.GENESIS_FORK_VERSION)
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
        datum_dict.update({'fork_version': self.chain_setting.GENESIS_FORK_VERSION})
        datum_dict.update({'network_name': self.chain_setting.NETWORK_NAME})
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
        saved_keystore = Keystore.from_file(keystore_filefolder)
        secret_bytes = saved_keystore.decrypt(password)
        return self.signing_sk == int.from_bytes(secret_bytes, 'big')

    def get_bls_to_execution_change(self, validator_index: int) -> SignedBLSToExecutionChange:
        if self.eth1_withdrawal_address is None:
            raise ValueError("The execution address should NOT be empty.")

        message = BLSToExecutionChange(
            validator_index=validator_index,
            from_bls_pubkey=self.withdrawal_pk,
            to_execution_address=self.eth1_withdrawal_address,
        )
        domain = compute_bls_to_execution_change_domain(
            fork_version=self.chain_setting.GENESIS_FORK_VERSION,
            genesis_validators_root=self.chain_setting.GENESIS_VALIDATORS_ROOT,
        )
        signing_root = compute_signing_root(message, domain)
        signature = bls.Sign(self.withdrawal_sk, signing_root)

        return SignedBLSToExecutionChange(
            message=message,
            signature=signature,
        )

    def get_bls_to_execution_change_dict(self, validator_index: int) -> Dict[str, bytes]:
        result_dict: Dict[str, Any] = {}
        signed_bls_to_execution_change = self.get_bls_to_execution_change(validator_index)
        message = {
            'validator_index': str(signed_bls_to_execution_change.message.validator_index),
            'from_bls_pubkey': '0x' + signed_bls_to_execution_change.message.from_bls_pubkey.hex(),
            'to_execution_address': '0x' + signed_bls_to_execution_change.message.to_execution_address.hex(),
        }
        result_dict.update({'message': message})
        result_dict.update({'signature': '0x' + signed_bls_to_execution_change.signature.hex()})

        # metadata
        metadata: Dict[str, Any] = {
            'network_name': self.chain_setting.NETWORK_NAME,
            'genesis_validators_root': '0x' + self.chain_setting.GENESIS_VALIDATORS_ROOT.hex(),
            'deposit_cli_version': DEPOSIT_CLI_VERSION,
        }

        result_dict.update({'metadata': metadata})
        return result_dict


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
                      mnemonic_password: str,
                      num_keys: int,
                      amounts: List[int],
                      chain_setting: BaseChainSetting,
                      start_index: int,
                      hex_eth1_withdrawal_address: Optional[HexAddress]) -> 'CredentialList':
        if len(amounts) != num_keys:
            raise ValueError(
                f"The number of keys ({num_keys}) doesn't equal to the corresponding deposit amounts ({len(amounts)})."
            )
        key_indices = range(start_index, start_index + num_keys)
        with click.progressbar(key_indices, label=load_text(['msg_key_creation']),
                               show_percent=False, show_pos=True) as indices:
            return cls([Credential(mnemonic=mnemonic, mnemonic_password=mnemonic_password,
                                   index=index, amount=amounts[index - start_index], chain_setting=chain_setting,
                                   hex_eth1_withdrawal_address=hex_eth1_withdrawal_address)
                        for index in indices])

    def export_keystores(self, password: str, folder: str) -> List[str]:
        with click.progressbar(self.credentials, label=load_text(['msg_keystore_creation']),
                               show_percent=False, show_pos=True) as credentials:
            return [credential.save_signing_keystore(password=password, folder=folder) for credential in credentials]

    def export_deposit_data_json(self, folder: str) -> str:
        with click.progressbar(self.credentials, label=load_text(['msg_depositdata_creation']),
                               show_percent=False, show_pos=True) as credentials:
            deposit_data = [cred.deposit_datum_dict for cred in credentials]
        filefolder = os.path.join(folder, 'deposit_data-%i.json' % time.time())
        with open(filefolder, 'w') as f:
            json.dump(deposit_data, f, default=lambda x: x.hex())
        if os.name == 'posix':
            os.chmod(filefolder, int('440', 8))  # Read for owner & group
        return filefolder

    def verify_keystores(self, keystore_filefolders: List[str], password: str) -> bool:
        with click.progressbar(zip(self.credentials, keystore_filefolders),
                               label=load_text(['msg_keystore_verification']),
                               length=len(self.credentials), show_percent=False, show_pos=True) as items:
            return all(credential.verify_keystore(keystore_filefolder=filefolder, password=password)
                       for credential, filefolder in items)

    def export_bls_to_execution_change_json(self, folder: str, validator_indices: Sequence[int]) -> str:
        with click.progressbar(self.credentials, label=load_text(['msg_bls_to_execution_change_creation']),
                               show_percent=False, show_pos=True) as credentials:
            bls_to_execution_changes = [cred.get_bls_to_execution_change_dict(validator_indices[i])
                                        for i, cred in enumerate(credentials)]

        filefolder = os.path.join(folder, 'bls_to_execution_change-%i.json' % time.time())
        with open(filefolder, 'w') as f:
            json.dump(bls_to_execution_changes, f)
        if os.name == 'posix':
            os.chmod(filefolder, int('440', 8))  # Read for owner & group
        return filefolder
