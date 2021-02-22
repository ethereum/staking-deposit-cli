import inspect
from functools import reduce
import json
from typing import (
    Any,
    Dict,
    List,
)
import os

from eth2deposit.utils.constants import INTL_CONETENT_PATH


def _get_from_dict(dataDict: Dict[str, Any], mapList: List[str]) -> str:
    '''
    Iterate nested dictionaries
    '''
    return reduce(dict.get, mapList, dataDict)  # type: ignore


def load_text(lang: str, params: List[str], file_path: str='', func: str='') -> str:
    '''
    Determine and return the appropriate internationalisation text for a given `lang` and `params`
    '''
    if file_path == '':
        # Auto-detect file-path based on call stack
        file_path = inspect.stack()[1].filename
        file_path = file_path[:-3] + '.json'     # replace .py with .json

    if func == '':
        # Auto-detect function based on call stack
        func = inspect.stack()[1].function

    # Determine path to json text
    file_path_list = os.path.normpath(file_path).split(os.path.sep)
    rel_path_list = file_path_list[file_path_list.index('eth2deposit') + 1:]
    json_path = os.path.join(INTL_CONETENT_PATH, lang, *rel_path_list)

    # browse json until text is found
    with open(json_path) as f:
        text_dict = json.load(f)
        return _get_from_dict(text_dict, [func] + params)
