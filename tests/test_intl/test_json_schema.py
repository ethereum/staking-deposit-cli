import json
import jsonschema
import os
import pytest
import re
from typing import (
    List,
)

from staking_deposit.utils.constants import INTL_CONTENT_PATH


TEST_SCHEMAS_FOLDER = os.path.join(os.path.dirname(__file__), 'schemas')


def files_to_check(root_dir: str) -> List[str]:
    file_list = []
    for dir_, _, files in os.walk(root_dir):
        for file_name in files:
            rel_dir = os.path.relpath(dir_, root_dir)
            rel_file = os.path.join(rel_dir, file_name)
            file_list.append(rel_file)
    return file_list


def languages_to_check(root_dir: str) -> List[str]:
    dirs = next(os.walk(root_dir))[1]
    regex = re.compile('([A-Za-z]){2}(-([A-Za-z]){2})?')
    return [d for d in dirs if re.fullmatch(regex, d)]


@pytest.mark.parametrize(
    'lang, schema_path',
    [
        (lang, schema)
        for schema in files_to_check(TEST_SCHEMAS_FOLDER)
        for lang in languages_to_check(INTL_CONTENT_PATH)
    ]
)
def test_language_schemas(lang: str, schema_path: str) -> None:
    with open(os.path.join(TEST_SCHEMAS_FOLDER, schema_path)) as schema_file:
        schema = json.load(schema_file)
        with open(os.path.join(INTL_CONTENT_PATH, lang, schema_path)) as lang_file:
            lang_json = json.load(lang_file)
            jsonschema.validate(lang_json, schema)
