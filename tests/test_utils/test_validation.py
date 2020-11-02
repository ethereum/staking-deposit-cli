import pytest

from eth2deposit.exceptions import ValidationError
from eth2deposit.utils.validation import validate_password_strength


@pytest.mark.parametrize(
    'password, valid',
    [
        ('12345678', True),
        ('1234567', False),
    ]
)
def test_validate_password_strength(password, valid):
    if valid:
        validate_password_strength(password=password)
    else:
        with pytest.raises(ValidationError):
            validate_password_strength(password=password)
