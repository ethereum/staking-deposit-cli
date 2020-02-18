from key_derivation.tree import (
    derive_child_SK,
    derive_master_SK,
)

from json import load

with open('tests/test_key_derivation/test_vectors/tree_kdf.json', 'r') as f:
    test_vectors = load(f)['kdf_tests']


def test_derive_master_SK():
    for test in test_vectors:
        seed = bytes.fromhex(test['seed'])
        master_SK = test['master_SK']
        assert derive_master_SK(seed=seed) == master_SK


def test_derive_child_SK():
    for test in test_vectors:
        parent_SK = test['master_SK']
        index = test['child_index']
        child_SK = test['child_SK']
        assert derive_child_SK(parent_SK=parent_SK, index=index) == child_SK
