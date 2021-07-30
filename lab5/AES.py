from lab2.poly import poly
from CryptoLab import shift

Sbox = [[99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118],
        [202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192],
        [183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21],
        [4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117],
        [9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132],
        [83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207],
        [208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168],
        [81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210],
        [205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115],
        [96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219],
        [224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121],
        [231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8],
        [186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138],
        [112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158],
        [225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223],
        [140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]]

revSbox = [[82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251],
           [124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203],
           [84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78],
           [8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37],
           [114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146],
           [108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132],
           [144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6],
           [208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107],
           [58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115],
           [150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110],
           [71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27],
           [252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244],
           [31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95],
           [96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239],
           [160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97],
           [23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]]
Rcon = [0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 0x20000000, 0x40000000, 0x80000000, 0x1B000000,
        0x36000000]
Move = [0, 0, 0, 0, 1, 1, 1, -3, 2, 2, -2, -2, 3, -1, -1, -1]
revMove = [0, 0, 0, 0, 3, -1, -1, -1, 2, 2, -2, -2, 1, 1, 1, -3]
tr = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]


def StateMatrix(m):
    state = [0] * 16
    for i in range(16):
        state[tr[i]] = m & ((1 << 8) - 1)
        m >>= 8
    return state[::-1]


def rebuild(state):
    res = 0
    for i in range(16):
        res <<= 8
        res |= state[tr[i]]
    return res


def AddRoundKey(State, key):
    return [(State[i] ^ key[i]) for i in range(16)]


def SubBytes(State, box):
    return [boxReplace(c, box) for c in State]


def ShiftRows(State, step):
    return [State[i + step[i]] for i in range(16)]


def boxReplace(a, box):
    i, res = 0, 0
    if a == 0:
        return box[0][0]
    while (a):
        res |= (box[(a & 255) >> 4][a & 0xf] << (i * 8))
        i += 1
        a >>= 8
    return res


def mul(a, b):
    return (poly(a) * poly(b)).data


def mix(a, b, c, d):
    aa = mul(2, a) ^ mul(3, b) ^ c ^ d
    bb = a ^ mul(2, b) ^ mul(3, c) ^ d
    cc = a ^ b ^ mul(2, c) ^ mul(3, d)
    dd = mul(3, a) ^ b ^ c ^ mul(2, d)
    return aa, bb, cc, dd


def remix(a, b, c, d):
    aa = mul(0xe, a) ^ mul(0xb, b) ^ mul(0xd, c) ^ mul(0x9, d)
    bb = mul(0x9, a) ^ mul(0xe, b) ^ mul(0xb, c) ^ mul(0xd, d)
    cc = mul(0xd, a) ^ mul(0x9, b) ^ mul(0xe, c) ^ mul(0xb, d)
    dd = mul(0xb, a) ^ mul(0xd, b) ^ mul(0x9, c) ^ mul(0xe, d)
    return aa, bb, cc, dd


def MixColumns(state, type):
    res = [0] * 16
    for i in range(4):
        if type == 1:
            res[i], res[i + 4], res[i + 8], res[i + 12] = mix(state[i], state[i + 4], state[i + 8], state[i + 12])
        else:
            res[i], res[i + 4], res[i + 8], res[i + 12] = remix(state[i], state[i + 4], state[i + 8], state[i + 12])
    return res


def KeyGen(init_key):
    w, key = [], []
    for i in range(4):
        w.append(
            (init_key[i] << 24) | (init_key[i + 4] << 16) | (init_key[i + 8] << 8) | (init_key[i + 12]))
    for i in range(4, 44):
        temp = w[i - 1]
        if i % 4 == 0:
            temp = boxReplace(shift(temp, 8, 32), Sbox) ^ Rcon[(i // 4) - 1]
        w.append(w[i - 4] ^ temp)

    for i in range(11):
        key.append(
            (w[4 * i] << 96) | (w[4 * i + 1] << 64) | (w[4 * i + 2] << 32) | (w[4 * i + 3]))
    return key


def AESencrypt(key, message):
    rk = KeyGen(StateMatrix(key))
    mesState = AddRoundKey(StateMatrix(message), StateMatrix(rk[0]))
    for i in range(1, 11):
        mesState = SubBytes(mesState, Sbox)
        mesState = ShiftRows(mesState, Move)
        if i < 10:
            mesState = MixColumns(mesState, 1)
        mesState = AddRoundKey(mesState, StateMatrix(rk[i]))
    return hex(rebuild(mesState))


def AESdecrypt(key, cipher):
    rk = KeyGen(StateMatrix(key))[::-1]
    cipState = AddRoundKey(StateMatrix(cipher), StateMatrix(rk[0]))
    for i in range(1, 11):
        cipState = ShiftRows(cipState, revMove)
        cipState = SubBytes(cipState, revSbox)
        cipState = AddRoundKey(cipState, StateMatrix(rk[i]))
        if i < 10:
            cipState = MixColumns(cipState, 0)

    return hex(rebuild(cipState))


if __name__ == "__main__":
    print(AESencrypt(0x3475bd76fa040b73f521ffcd9de93f24, 0x1b5e8b0f1bc78d238064826704830cdb))
    print(AESdecrypt(0x3475bd76fa040b73f521ffcd9de93f24, 0xf3855216ddf401d4d42c8002e686c6e7))
    # print(AESencrypt(0x0f1571c947d9e8590cb7add6af7f6798, 0x0123456789abcdeffedcba9876543210))
    # print(AESdecrypt(0x0f1571c947d9e8590cb7add6af7f6798, 0xff0b844a0853bf7c6934ab4364148fb9))
    # print(AESencrypt(0x3475bd76fa040b73f521ffcd9de93f24, 0x1b5e8b0f1bc78d238064826704830cdb))
