import pytest

from eth2deposit.credentials import CredentialList


def test_from_mnemonic():
    with pytest.raises(ValueError):
        CredentialList.from_mnemonic(
            mnemonic="",
            num_keys=1,
            amounts=[32, 32],
            fork_version=bytes.fromhex('00000001'),
            start_index=1,
        )
