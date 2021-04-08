import inspect
import difflib
from functools import reduce
import json
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Tuple,
)
import os

from eth2deposit.utils import config
from eth2deposit.utils.constants import (
    INTL_CONTENT_PATH,
)
from eth2deposit.exceptions import ValidationError


def _get_from_dict(dataDict: Dict[str, Any], mapList: List[str]) -> str:
    '''
    Iterate nested dictionaries
    '''
    try:
        return reduce(dict.get, mapList, dataDict)  # type: ignore
    except TypeError:
        raise KeyError('%s not in internationalisation json file.' % mapList)


def load_text(params: List[str], file_path: str='', func: str='', lang: str='') -> str:
    '''
    Determine and return the appropriate internationalisation text for a given set of `params`.
    '''
    if file_path == '':
        # Auto-detect file-path based on call stack
        file_path = inspect.stack()[1].filename
        file_path = file_path[:-3] + '.json'     # replace .py with .json

    if func == '':
        # Auto-detect function based on call stack
        func = inspect.stack()[1].function

    if lang == '':
        lang = config.language

    # Determine path to json text
    file_path_list = os.path.normpath(file_path).split(os.path.sep)
    rel_path_list = file_path_list[file_path_list.index('eth2deposit') + 1:]
    json_path = os.path.join(INTL_CONTENT_PATH, lang, *rel_path_list)

    # browse json until text is found
    with open(json_path) as f:
        text_dict = json.load(f)
        return _get_from_dict(text_dict, [func] + params)


def get_first_options(options: Dict[str, Tuple[str, ...]]) -> List[str]:
    '''
    Returns the first `option` in the values of the `options` dict.
    '''
    return list(map(lambda x: x[0], options.values()))


def _closest_match(text: str, options: Iterable[str]) -> str:
    '''
    Finds the closest match to `text` in the `options_list`
    '''
    match = difflib.get_close_matches(text, options, n=1, cutoff=0.6)
    if len(match) == 0:
        raise ValidationError('%s is not a valid language option' % text)
    return match[0]


def fuzzy_reverse_dict_lookup(text: str, options: Dict[str, Tuple[str, ...]]) -> str:
    '''
    Returns the closest match to `text` out of the `options`
    :param text: The test string that needs to be found
    :param options: A dict with keys (the value that will be returned)
                    and values a list of the options to be matched against
    '''
    reverse_lookup_dict = {value: key for key, values in options.items() for value in values}
    match = _closest_match(text, reverse_lookup_dict.keys())
    return reverse_lookup_dict[match]
