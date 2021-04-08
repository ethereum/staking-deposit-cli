import inspect
from functools import reduce
import json
from typing import (
    Any,
    Dict,
    List,
    Sequence,
)
import os
import unicodedata

from eth2deposit.utils import config
from eth2deposit.utils.constants import (
    INTL_CONTENT_PATH,
    INTL_LANG_OPTIONS,
)


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


def get_translation_languages() -> Sequence[str]:
    '''
    Returns the primary name for the languages available
    '''
    return list(map(lambda x: x[0], INTL_LANG_OPTIONS.values()))


def _normalize_caseless(text: str) -> str:
    '''
    Normalize and remove case of input string
    '''
    return unicodedata.normalize("NFKD", text.casefold())


def get_language_iso_name(long_name: str) -> str:
    '''
    Given the long version of a name, return the ISO 639-1 name
    '''
    reversed_language_dict = {_normalize_caseless(lang): iso_name
                              for iso_name, langs in INTL_LANG_OPTIONS.items() for lang in langs}
    return reversed_language_dict[_normalize_caseless(long_name)]
