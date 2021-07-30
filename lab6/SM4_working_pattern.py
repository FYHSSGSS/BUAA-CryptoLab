from math import ceil

MK = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]
Sbox = [[214, 144, 233, 254, 204, 225, 61, 183, 22, 182, 20, 194, 40, 251, 44, 5],
        [43, 103, 154, 118, 42, 190, 4, 195, 170, 68, 19, 38, 73, 134, 6, 153],
        [156, 66, 80, 244, 145, 239, 152, 122, 51, 84, 11, 67, 237, 207, 172, 98],
        [228, 179, 28, 169, 201, 8, 232, 149, 128, 223, 148, 250, 117, 143, 63, 166],
        [71, 7, 167, 252, 243, 115, 23, 186, 131, 89, 60, 25, 230, 133, 79, 168],
        [104, 107, 129, 178, 113, 100, 218, 139, 248, 235, 15, 75, 112, 86, 157, 53],
        [30, 36, 14, 94, 99, 88, 209, 162, 37, 34, 124, 59, 1, 33, 120, 135],
        [212, 0, 70, 87, 159, 211, 39, 82, 76, 54, 2, 231, 160, 196, 200, 158],
        [234, 191, 138, 210, 64, 199, 56, 181, 163, 247, 242, 206, 249, 97, 21, 161],
        [224, 174, 93, 164, 155, 52, 26, 85, 173, 147, 50, 48, 245, 140, 177, 227],
        [29, 246, 226, 46, 130, 102, 202, 96, 192, 41, 35, 171, 13, 83, 78, 111],
        [213, 219, 55, 69, 222, 253, 142, 47, 3, 255, 106, 114, 109, 108, 91, 81],
        [141, 27, 175, 146, 187, 221, 188, 127, 17, 217, 92, 65, 31, 16, 90, 216],
        [10, 193, 49, 136, 165, 205, 123, 189, 45, 116, 208, 18, 184, 229, 180, 176],
        [137, 105, 151, 74, 12, 150, 119, 126, 101, 185, 241, 9, 197, 110, 198, 132],
        [24, 240, 125, 236, 58, 220, 77, 32, 121, 238, 95, 62, 215, 203, 57, 72]]
ck = [462357, 472066609, 943670861, 1415275113, 1886879365, 2358483617, 2830087869, 3301692121, 3773296373, 4228057617,
      404694573, 876298825, 1347903077, 1819507329, 2291111581, 2762715833, 3234320085, 3705924337, 4177462797,
      337322537, 808926789, 1280531041, 1752135293, 2223739545, 2695343797, 3166948049, 3638552301, 4110090761,
      269950501, 741554753, 1213159005, 1684763257]


def div(n):
    return [n >> 96, (n >> 64) & 0xffffffff, (n >> 32) & 0xffffffff, n & 0xffffffff]


def rebuild(state):
    res = 0
    for i in range(4):
        res <<= 32
        res |= state[i]
    return res


def SboxReplace(a):
    return Sbox[a >> 4][a & 0xf]


def pbox(n):
    a = [n >> 24, (n >> 16) & 0xff, (n >> 8) & 0xff, n & 0xff]
    b = list(map(SboxReplace, a))
    return (b[0] << 24) + (b[1] << 16) + (b[2] << 8) + b[3]


def shift(num, pos):
    return ((num << pos) | (num >> (32 - pos))) & 0xffffffff


def L(n, type):
    if type == 1:
        return n ^ shift(n, 13) ^ shift(n, 23)
    else:
        return n ^ shift(n, 2) ^ shift(n, 10) ^ shift(n, 18) ^ shift(n, 24)


def F(a, b, c, d, e, i):
    return a ^ L(pbox(b ^ c ^ d ^ e), i)


def keygen(key):
    KeyWord = [(a ^ b) for a, b in zip(div(key), MK)]
    for i in range(32):
        KeyWord.append(F(KeyWord[i], KeyWord[i + 1], KeyWord[i + 2], KeyWord[i + 3], ck[i], 1))
    return KeyWord


def SM4crypt(key, message, type):
    rk = keygen(key) if type == 1 else keygen(key)[::-1]
    MesWord = div(message)
    for i in range(32):
        RK = rk[i + 4] if type == 1 else rk[i]
        MesWord.append(F(MesWord[i], MesWord[i + 1], MesWord[i + 2], MesWord[i + 3], RK, 0))
    return rebuild(MesWord[35:31:-1])


pad = lambda s: s + (16 - len(s) % 16) * bytes([16 - len(s) % 16])


def SM4encryptECB(key, message):
    global fout
    message = pad(message)
    case = len(message) // 16
    for i in range(case):
        plaintext = int.from_bytes(message[16 * i: 16 * i + 16], 'big')
        cipher = SM4crypt(key, plaintext, 1).to_bytes(16, 'big')
        fout.write(cipher)


def SM4decryptECB(key, message):
    global fout
    case = len(message) // 16
    for i in range(case):
        plaintext = int.from_bytes(message[16 * i: 16 * i + 16], 'big')
        cipher = SM4crypt(key, plaintext, 0).to_bytes(16, 'big')
        if i == case - 1:
            padding = cipher[-1]
            cipher = cipher[0: 16 - padding]
        fout.write(cipher)


def SM4encryptCBC(iv, key, message):
    global fout
    IV = iv.to_bytes(16, 'big')
    message = pad(message)
    case = len(message) // 16
    for i in range(case):
        plaintext = [a ^ b for a, b in zip(message[16 * i: 16 * i + 16], IV)]
        plaintext = int.from_bytes(plaintext, 'big')
        cipher = SM4crypt(key, plaintext, 1).to_bytes(16, 'big')
        IV = cipher
        fout.write(cipher)


def SM4decryptCBC(iv, key, message):
    global fout
    IV = iv.to_bytes(16, 'big')
    case = len(message) // 16
    for i in range(case):
        plaintext = int.from_bytes(message[16 * i: 16 * i + 16], 'big')
        temp = SM4crypt(key, plaintext, 0).to_bytes(16, 'big')
        cipher = bytes([])
        for a, b in zip(temp, IV):
            cipher += bytes([a ^ b])
        IV = message[16 * i: 16 * i + 16]
        if i == case - 1:
            padding = cipher[-1]
            cipher = cipher[0: 16 - padding]
        fout.write(cipher)


def SM4cryptCTR(iv, key, message, type):
    global fout
    case = ceil(len(message) / 16)
    for i in range(case):
        temp = SM4crypt(key, iv + i, 1).to_bytes(16, 'big')
        cipher = bytes([])
        for a, b in zip(temp, message[16 * i: 16 * i + 16]):
            cipher += bytes([a ^ b])
        fout.write(cipher)
        if i == case - 1 and len(message) % 16 != 0:
            i += 1
            temp = SM4crypt(key, iv + i, type).to_bytes(16, 'big')
            cipher = bytes([])
            for a, b in zip(temp[0: len(message) - 16 * i], message[16 * i: len(message)]):
                cipher += bytes([a ^ b])
            fout.write(cipher)

def SM4cryptOFB(iv, key, message):
    global fout
    case = ceil(len(message) / 16)
    for i in range(case):
        iv = SM4crypt(key, iv, 1)
        cipher = bytes([])
        for a, b in zip(iv.to_bytes(16, 'big'), message[16 * i: 16 * i + 16]):
            cipher += bytes([a ^ b])
        fout.write(cipher)
        if i == case - 1 and len(message) % 16 != 0:
            i += 1
            temp = SM4crypt(key, iv, type).to_bytes(16, 'big')
            cipher = bytes([])
            for a, b in zip(temp[0: len(message) - 16 * i], message[16 * i: len(message)]):
                cipher += bytes([a ^ b])
            fout.write(cipher)

def SM4cryptCFB(iv, key, message, type):
    global fout
    case = ceil(len(message) / 16)
    for i in range(case):
        iv = SM4crypt(key, iv, 1)
        cipher = bytes([])
        for a, b in zip(iv.to_bytes(16, 'big'), message[16 * i: 16 * i + 16]):
            cipher += bytes([a ^ b])
        iv = int.from_bytes(cipher, 'big') if type == 1 else int.from_bytes(message[16 * i: 16 * i + 16], 'big')
        fout.write(cipher)
        if i == case - 1 and len(message) % 16 != 0:
            i += 1
            temp = SM4crypt(key, iv, type).to_bytes(16, 'big')
            cipher = bytes([])
            for a, b in zip(temp[0: len(message) - 16 * i], message[16 * i: len(message)]):
                cipher += bytes([a ^ b])
            fout.write(cipher)

if __name__ == '__main__':
    filepath = 'data/message'
    outpath = 'data/ouput'
    fin = open(filepath, "rb")
    global fout
    fout = open(outpath, 'wb')
    message = fin.read()
    useful = 0x0123456789abcdeffedcba9876543210
    SM4cryptCFB(useful, useful, message, 1)
    # SM4cryptCTR(useful, useful, message, 0)
