from key_derivation.tree import (
    _flip_bits_256,
    _IKM_to_lamport_SK,
    _parent_SK_to_lamport_PK,
    _HKDF_mod_r,
)
from json import load

with open('tests/test_key_derivation/test_vectors/tree_kdf_intermediate.json', 'r') as f:
    test_vector = load(f)


def test_flip_bits_256():
    test_vector_int = int(test_vector['seed'][:64], 16)  # 64 comes from string chars containing .5 bytes
    assert test_vector_int & _flip_bits_256(test_vector_int) == 0


def test_IKM_to_lamport_SK():
    test_vector_lamport_0 = [bytes.fromhex(x) for x in test_vector['lamport_0']]
    test_vector_lamport_1 = [bytes.fromhex(x) for x in test_vector['lamport_1']]
    salt = test_vector['child_index'].to_bytes(4, 'big')
    IKM = test_vector['master_SK'].to_bytes(32, 'big')
    lamport_0 = _IKM_to_lamport_SK(IKM=IKM, salt=salt)
    not_IKM = _flip_bits_256(test_vector['master_SK']).to_bytes(32, 'big')
    lamport_1 = _IKM_to_lamport_SK(IKM=not_IKM, salt=salt)
    assert test_vector_lamport_0 == lamport_0
    assert test_vector_lamport_1 == lamport_1


def test_parent_SK_to_lamport_PK():
    parent_SK = test_vector['master_SK']
    index = test_vector['child_index']
    lamport_PK = bytes.fromhex(test_vector['compressed_lamport_PK'])
    assert lamport_PK == _parent_SK_to_lamport_PK(parent_SK=parent_SK, index=index)


def test_HKDF_mod_r():
    test_0 = (bytes.fromhex(test_vector['seed']), test_vector['master_SK'])
    test_1 = (bytes.fromhex(test_vector['compressed_lamport_PK']), test_vector['child_SK'])
    for test in (test_0, test_1):
        assert _HKDF_mod_r(IKM=test[0]) == test[1]
