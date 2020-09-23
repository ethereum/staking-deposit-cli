from typing import List

from .mnemonic import get_seed
from .tree import (
    derive_master_SK,
    derive_child_SK,
)


def path_to_nodes(path: str) -> List[int]:
    """
    Maps from a path string to a list of indices where each index represents the corresponding level in the path.
    """
    path = path.replace(' ', '')
    if not set(path).issubset(set('m1234567890/')):
        raise ValueError(f"Invalid path {path}")

    indices = path.split('/')

    if indices[0] != 'm':
        raise ValueError(f"The first character of path should be `m`. Got {indices[0]}.")
    indices.pop(0)

    return [int(index) for index in indices]


def mnemonic_and_path_to_key(*, mnemonic: str, path: str, password: str) -> int:
    """
    Return the SK at position `path`, derived from `mnemonic`. The password is to be
    compliant with BIP39 mnemonics that use passwords, but is not used by this CLI outside of tests.
    """
    seed = get_seed(mnemonic=mnemonic, password=password)
    sk = derive_master_SK(seed)
    for node in path_to_nodes(path):
        sk = derive_child_SK(parent_SK=sk, index=node)
    return sk
