import pytest
from typing import (
    Dict,
    List,
)

from staking_deposit.utils.constants import _add_index_to_options


@pytest.mark.parametrize(
    'arg, test', [
        ({'en': ['English', 'en']}, {'en': ['1. English', '1', 'English', 'en']}),
        ({'a': ['a'], 'b': ['b'], 'c': ['c']},
         {'a': ['1. a', '1', 'a'], 'b': ['2. b', '2', 'b'], 'c': ['3. c', '3', 'c']})
    ]
)
def test_add_index_to_options(arg: Dict[str, List[str]], test: Dict[str, List[str]]) -> None:
    assert _add_index_to_options(arg) == test
