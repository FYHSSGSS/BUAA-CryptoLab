#!/usr/bin/env python3

from SM4oracle import encrypt, is_padding_ok, BLOCK_SIZE


def attack_message(msg):
    cipherfake = [0] * 16
    plaintext = [0] * 16
    current = 0
    message = ""

    number_of_blocks = int(len(msg) / BLOCK_SIZE)
    blocks = [[]] * number_of_blocks
    for i in (range(number_of_blocks)):
        blocks[i] = msg[i * BLOCK_SIZE: (i + 1) * BLOCK_SIZE]

    for z in range(len(blocks) - 1):
        for itera in range(1, 17):
            for v in range(256):
                cipherfake[-itera] = v
                if is_padding_ok(bytes(cipherfake) + blocks[z + 1]):
                    current = itera
                    plaintext[-itera] = v ^ itera ^ blocks[z][-itera]

            for w in range(1, current + 1):
                cipherfake[-w] = plaintext[-w] ^ itera + 1 ^ blocks[z][-w]
        for i in range(16):
            if plaintext[i] >= 32:
                char = chr(int(plaintext[i]))
                message += char

    return str.encode(message)


def test_the_attack():
    messages = [b'doyoulikewhatyousee',b'heybuddyithinkyougottothewrongdoor',
                b'theleatherclubistwoblocksdown',b'****you']
    for msg in messages:
        print('Testing:', msg)
        cracked_ct = attack_message(encrypt(msg))
        assert cracked_ct == msg


if __name__ == '__main__':
    test_the_attack()
