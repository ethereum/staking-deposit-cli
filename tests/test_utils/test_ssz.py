import pytest

from staking_deposit.utils.ssz import (
    DepositMessage,
    compute_deposit_domain,
    compute_deposit_fork_data_root,
    compute_signing_root,
)


@pytest.mark.parametrize(
    'fork_version, valid, result',
    [
        (b"\x12" * 4, True, b'\x03\x00\x00\x00\rf`\x8a\xf5W\xf4\xfa\xdb\xfc\xe2H\xac7\xf6\xe7c\x9c\xe3q\x10\x0cC\xd1Z\xad\x05\xcb'),  # noqa: E501
        (b"\x12" * 5, False, None),
        (b"\x12" * 3, False, None),
    ]
)
def test_compute_deposit_domain(fork_version, valid, result):
    if valid:
        assert compute_deposit_domain(fork_version) == result
    else:
        with pytest.raises(ValueError):
            compute_deposit_domain(fork_version)


@pytest.mark.parametrize(
    'current_version, valid, result',
    [
        (b"\x12" * 4, True, b'\rf`\x8a\xf5W\xf4\xfa\xdb\xfc\xe2H\xac7\xf6\xe7c\x9c\xe3q\x10\x0cC\xd1Z\xad\x05\xcb\x08\xac\x1d\xc2'),  # noqa: E501
        (b"\x12" * 5, False, None),
        (b"\x12" * 3, False, None),
    ]
)
def test_compute_deposit_fork_data_root(current_version, valid, result):
    if valid:
        assert compute_deposit_fork_data_root(current_version=current_version) == result
    else:
        with pytest.raises(ValueError):
            compute_deposit_fork_data_root(current_version=current_version)


@pytest.mark.parametrize(
    'domain, valid, result',
    [
        (b"\x12" * 32, True, b'g\xa33\x0f\xf8{\xdbF\xbb{\x80\xcazd\x1e9\x8dj\xc4\xe8zhVR|\xac\xc8)\xfba\x89o'),  # noqa: E501
        (b"\x12" * 31, False, None),
        (b"\x12" * 33, False, None),
    ]
)
def test_compute_signing_root(domain, valid, result):
    deposit_message = DepositMessage(
        pubkey=b'\x12' * 48,
        withdrawal_credentials=b'\x12' * 32,
        amount=100,
    )
    if valid:
        assert compute_signing_root(deposit_message, domain) == result
    else:
        with pytest.raises(ValueError):
            compute_signing_root(deposit_message, domain)
