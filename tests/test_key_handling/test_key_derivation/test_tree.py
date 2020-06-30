import os
import json
from py_ecc.bls import G2ProofOfPossession as bls
import pytest


from eth2deposit.key_handling.key_derivation.tree import (
    _HKDF_mod_r,
    derive_child_SK,
    derive_master_SK,
)


test_vector_filefolder = os.path.join(os.getcwd(), 'tests', 'test_key_handling',
                                      'test_key_derivation', 'test_vectors', 'tree_kdf.json')
with open(test_vector_filefolder, 'r') as f:
    test_vectors = json.load(f)['kdf_tests']


@pytest.mark.parametrize(
    'test',
    test_vectors
)
def test_hkdf_mod_r(test) -> None:
    seed = bytes.fromhex(test['seed'])
    assert bls.KeyGen(seed) == _HKDF_mod_r(IKM=seed)


@pytest.mark.parametrize(
    'seed',
    [b'\x00' * 32]
)
@pytest.mark.parametrize(
    'key_info',
    [b'\x00' * 32, b'\x01\x23\x45\x67\x89\xAB\xBC\xDE\xFF', b'\xFF' * 16]
)
def test_hkdf_mod_r_key_info(seed: bytes, key_info: bytes) -> None:
    assert bls.KeyGen(seed, key_info) == _HKDF_mod_r(IKM=seed, key_info=key_info)


@pytest.mark.parametrize(
    'test',
    test_vectors
)
def test_derive_master_SK(test) -> None:
    seed = bytes.fromhex(test['seed'])
    master_SK = test['master_SK']
    assert derive_master_SK(seed=seed) == master_SK


@pytest.mark.parametrize(
    'test',
    test_vectors
)
def test_derive_child_SK(test) -> None:
    parent_SK = test['master_SK']
    index = test['child_index']
    child_SK = test['child_SK']
    assert derive_child_SK(parent_SK=parent_SK, index=index) == child_SK
