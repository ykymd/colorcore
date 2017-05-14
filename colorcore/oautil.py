# -*- coding: utf-8 -*-
import binascii
import hashlib

import base58


def leb128(hex):
    r = 0
    for i in range(int(len(hex) / 2)):
        r += (int(hex[i * 2:(i + 1) * 2], 16) & 0x7f) << (7 * i)
        if int(hex[i * 2], 16) < 8:
            return r, hex[(i + 1) * 2:]


def hash160(hex):
    s = hashlib.sha256(binascii.unhexlify(hex)).digest()
    h = hashlib.new('ripemd160')
    h.update(s)
    return h.hexdigest()


def checksum(hex):
    s = hashlib.sha256(binascii.unhexlify(hex)).digest()
    h = hashlib.sha256(s)
    return h.hexdigest()[0:8]


def encode_base58(hexstring):
    return base58.b58encode(bytes.fromhex(hexstring))


@staticmethod
def getAssetId(scriptPubKeyHex, isTestnet):
    script = hash160(scriptPubKeyHex)
    # mainnet: 23, testnet:115
    prefix = 115 if isTestnet else 23
    script = hex(prefix)[2:] + script
    script = script + checksum(script)
    return encode_base58(script)
