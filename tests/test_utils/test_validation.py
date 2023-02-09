import pytest
from typing import (
    Any,
)

from staking_deposit.exceptions import ValidationError
from staking_deposit.utils.validation import (
    validate_int_range,
    validate_password_strength,
    validate_ether_amount_range
)


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


@pytest.mark.parametrize(
    'num, low, high, valid',
    [
        (2, 0, 4, True),
        (0, 0, 4, True),
        (-1, 0, 4, False),
        (4, 0, 4, False),
        (0.2, 0, 4, False),
        ('0', 0, 4, True),
        ('a', 0, 4, False),
    ]
)
def test_validate_int_range(num: Any, low: int, high: int, valid: bool) -> None:
    if valid:
        validate_int_range(num, low, high)
    else:
        with pytest.raises(ValidationError):
            validate_int_range(num, low, high)

@pytest.mark.parametrize(
    'num, valid',
    [
        (2, True),
        (0, False),
        (-1, False),
        (32, True),
        (1, True),
        (32.1, False),
        ('0',  True),
        ('a', False),
    ]
)
def test_validate_ether_amount_range(num: Any, valid: bool) -> None:
    if valid:
        validate_ether_amount_range(num)
    else:
        with pytest.raises(ValidationError):
            validate_ether_amount_range(num)


