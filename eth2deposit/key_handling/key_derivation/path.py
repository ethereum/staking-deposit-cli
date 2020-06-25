from typing import List

from .mnemonic import get_seed
from .tree import (
    derive_master_SK,
    derive_child_SK,
)


def path_to_nodes(path: str) -> List[int]:
    """
    Returns a list of the child index at every level in `path`.
    """
    path = path.replace(' ', '')
    assert set(path).issubset(set('m1234567890/'))
    indices = path.split('/')
    assert indices.pop(0) == 'm'
    return [int(index) for index in indices]


def mnemonic_and_path_to_key(*, mnemonic: str, path: str, password: str) -> int:
    """
    Returns the SK at position `path` secures with `password` derived from `mnemonic`.
    """
    seed = get_seed(mnemonic=mnemonic, password=password)
    sk = derive_master_SK(seed)
    for node in path_to_nodes(path):
        sk = derive_child_SK(parent_SK=sk, index=node)
    return sk
