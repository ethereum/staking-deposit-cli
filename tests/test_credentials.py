import pytest

from eth2deposit.credentials import CredentialList


def test_from_mnemonic() -> None:
    with pytest.raises(ValueError):
        CredentialList.from_mnemonic(
            mnemonic="",
            mnemonic_password="",
            num_keys=1,
            amounts=[32, 32],
            fork_version=bytes.fromhex('00000000'),
            start_index=1,
        )
