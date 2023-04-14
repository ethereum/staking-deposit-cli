import struct
from ledgercomm import Transport

_trans = None

def _get_trans() -> Transport:
    global _trans
    if not _trans:
        _trans = Transport(interface="hid", debug=False)
        assert _trans != None
    return _trans

def get_withdrawal_pk(index: int) -> bytes:
    trans = _get_trans()
    trans.send(0xe0, 0x05, 0x00, 0x00, None, struct.pack(">I", index))
    sw, data = trans.recv()
    assert sw == 0x9000
    assert len(data) == 48
    return data

def get_signing_pk(index: int) -> bytes:
    trans = _get_trans()
    trans.send(0xe0, 0x06, 0x00, 0x00, None, struct.pack(">I", index))
    sw, data = trans.recv()
    assert sw == 0x9000
    assert len(data) == 48
    return data

def get_eth1_withdrawal_addr(index: int) -> bytes:
    trans = _get_trans()
    trans.send(0xe0, 0x07, 0x00, 0x00, None, struct.pack(">I", index))
    sw, data = trans.recv()
    assert sw == 0x9000
    assert len(data) == 20
    return data

def sign(index: int, signing_root: bytes) -> bytes:
    trans = _get_trans()
    assert len(signing_root) == 32
    trans.send(0xe0, 0x08, 0x00, 0x00, None, struct.pack(">I", index) + signing_root)
    sw, data = trans.recv()
    assert sw == 0x9000
    assert len(data) == 96
    return data
