#!/usr/bin/env python3

from Crypto import Random
from SM4 import *
from SM4_working_pattern import pad

KEY_LENGTH = 16
BLOCK_SIZE = 16

_random_gen = Random.new()
_key = int.from_bytes(_random_gen.read(KEY_LENGTH), 'big')

def enCBC(IV, message):
    message = pad(message)
    case = len(message) // 16
    ret = bytes([])
    for i in range(case):
        plaintext = [a ^ b for a, b in zip(message[16 * i: 16 * i + 16], IV)]
        plaintext = int.from_bytes(plaintext, 'big')
        cipher = SM4crypt(_key, plaintext, 1).to_bytes(16, 'big')
        IV = cipher
        ret += cipher
    return ret

def deCBC(IV, message):
    case = len(message) // 16
    ret = bytes([])
    for i in range(case):
        plaintext = int.from_bytes(message[16 * i: 16 * i + 16], 'big')
        temp = SM4crypt(_key, plaintext, 0).to_bytes(16, 'big')
        cipher = bytes([])
        for a, b in zip(temp, IV):
            cipher += bytes([a ^ b])
        ret += cipher
        IV = message[16 * i: 16 * i + 16]
    return ret

def _remove_padding(data):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        return None
    for i in range(1, pad_len):
        if data[-i - 1] != pad_len:
            return None
    return data[:-pad_len]


def encrypt(msg):
    init_iv = iv = _random_gen.read(16)
    cipher = enCBC(iv, msg)
    return init_iv + cipher


def _decrypt(data):
    iv = data[:BLOCK_SIZE]
    cipher = deCBC(iv, data[BLOCK_SIZE:])
    return _remove_padding(cipher)


def is_padding_ok(data):
    return _decrypt(data) is not None


if __name__ == '__main__':
    cleartext = b'Attack at dawn'
    ciphertext = encrypt(cleartext)

    print("cleartext:", cleartext)
    print("decrypted message:", _decrypt(ciphertext))
    print("padding is ok:", is_padding_ok(ciphertext))
