import pytest
from typing import (
    Any,
)

from staking_deposit.exceptions import ValidationError
from staking_deposit.utils.validation import (
    normalize_input_list,
    validate_int_range,
    validate_password_strength,
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
    'input, result',
    [
        ('1', ['1']),
        ('1,2,3', ['1', '2', '3']),
        ('[1,2,3]', ['1', '2', '3']),
        ('(1,2,3)', ['1', '2', '3']),
        ('{1,2,3}', ['1', '2', '3']),
        ('1 2 3', ['1', '2', '3']),
        ('1  2  3', ['1', '2', '3']),
    ]
)
def test_normalize_input_list(input, result):
    assert normalize_input_list(input) == result
