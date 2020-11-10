import pytest

from eth2deposit.cli.generate_keys import validate_withdrawal_credentials
from eth2deposit.exceptions import ValidationError


@pytest.mark.parametrize(
    'withdrawal_credentials, is_valid',
    [
        ('0x2222', False),
        ('0x0011111111111111111111111111111111111111111111111111111111111111', True),
        ('0011111111111111111111111111111111111111111111111111111111111111', True),
        ('001111111111111111111111111111111111111111111111111111111111111122', False),
    ]
)
def test_validate_withdrawal_credentials(withdrawal_credentials, is_valid) -> None:
    if is_valid:
        validate_withdrawal_credentials(withdrawal_credentials)
    else:
        with pytest.raises((ValidationError, ValueError)):
            validate_withdrawal_credentials(withdrawal_credentials)
