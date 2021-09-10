import os
import json
import pytest

from staking_deposit.key_handling.key_derivation.tree import (
    _flip_bits_256,
    _IKM_to_lamport_SK,
    _parent_SK_to_lamport_PK,
    _HKDF_mod_r,
)

from staking_deposit.key_handling.key_derivation.path import (
    mnemonic_and_path_to_key,
    path_to_nodes,
)

test_vector_filefolder = os.path.join(os.getcwd(), 'tests', 'test_key_handling', 'test_key_derivation',
                                      'test_vectors', 'tree_kdf_intermediate.json')
with open(test_vector_filefolder, 'r') as f:
    test_vector_dict = json.load(f)


@pytest.mark.parametrize(
    'test_vector',
    [test_vector_dict]
)
def test_flip_bits_256(test_vector) -> None:
    test_vector_int = int(test_vector['seed'][:64], 16)  # 64 comes from string chars containing .5 bytes
    assert test_vector_int & _flip_bits_256(test_vector_int) == 0


@pytest.mark.parametrize(
    'test_vector',
    [test_vector_dict]
)
def test_IKM_to_lamport_SK(test_vector) -> None:
    test_vector_lamport_0 = [bytes.fromhex(x) for x in test_vector['lamport_0']]
    test_vector_lamport_1 = [bytes.fromhex(x) for x in test_vector['lamport_1']]
    salt = test_vector['child_index'].to_bytes(4, 'big')
    IKM = test_vector['master_SK'].to_bytes(32, 'big')
    lamport_0 = _IKM_to_lamport_SK(IKM=IKM, salt=salt)
    not_IKM = _flip_bits_256(test_vector['master_SK']).to_bytes(32, 'big')
    lamport_1 = _IKM_to_lamport_SK(IKM=not_IKM, salt=salt)
    assert test_vector_lamport_0 == lamport_0
    assert test_vector_lamport_1 == lamport_1


@pytest.mark.parametrize(
    'test_vector',
    [test_vector_dict]
)
def test_parent_SK_to_lamport_PK(test_vector) -> None:
    parent_SK = test_vector['master_SK']
    index = test_vector['child_index']
    lamport_PK = bytes.fromhex(test_vector['compressed_lamport_PK'])
    assert lamport_PK == _parent_SK_to_lamport_PK(parent_SK=parent_SK, index=index)


@pytest.mark.parametrize(
    'test_vector',
    [test_vector_dict]
)
def test_HKDF_mod_r(test_vector) -> None:
    test_0 = (bytes.fromhex(test_vector['seed']), test_vector['master_SK'])
    test_1 = (bytes.fromhex(test_vector['compressed_lamport_PK']), test_vector['child_SK'])
    for test in (test_0, test_1):
        assert _HKDF_mod_r(IKM=test[0]) == test[1]


@pytest.mark.parametrize(
    'test_vector',
    [test_vector_dict]
)
def test_mnemonic_and_path_to_key(test_vector) -> None:
    mnemonic = test_vector['mnemonic']
    password = test_vector['password']
    path = test_vector['path']
    key = test_vector['child_SK']
    assert mnemonic_and_path_to_key(mnemonic=mnemonic, path=path, password=password) == key


@pytest.mark.parametrize(
    'path, valid',
    [
        ("m/12381/3600/0/0/0", True),
        ("x/12381/3600/0/0/0", False),
        ("m/qwert/3600/0/0/0", False),
    ]
)
def test_path_to_nodes(path, valid):
    if valid:
        path_to_nodes(path)
    else:
        with pytest.raises(ValueError):
            path_to_nodes(path)
