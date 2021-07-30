from CryptoLab import bitlen

KT = [0x5A827999] * 20 + [0x6ED9EBA1] * 20 + [0x8F1BBCDC] * 20 + [0xCA62C1D6] * 20

def shift(num, pos):
    return ((num << pos) | (num >> (32 - pos))) & 0xffffffff


def ft(B, C, D, t):
    if t <= 19:
        return (B & C) | ((B ^ 0xffffffff) & D)
    elif t <= 39 or t > 59:
        return B ^ C ^ D
    elif t <= 59:
        return (B & C) | (B & D) | (C & D)


def padding(msg):
    l = len(msg) * 8
    intmsg = int.from_bytes(msg, 'big')
    k, length = 448 - l - 1, 1
    while k < 0:
        k += 512
        length += 1
    intmsg = ((intmsg << 1) | 1) << (k + 64) | l
    return intmsg, length


def process(B):
    global H0, H1, H2, H3, H4
    Wt = []
    for i in range(16):
        Wt.append(B & 0xffffffff)
        B >>= 32
    Wt = Wt[::-1]
    for i in range(16, 80):
        Wt.append(shift(Wt[i - 3] ^ Wt[i - 8] ^ Wt[i - 14] ^ Wt[i - 16], 1))
    A, B, C, D, E = H0, H1, H2, H3, H4
    for i in range(80):
        temp = (shift(A, 5) + ft(B, C, D, i) + E + Wt[i] + KT[i]) & 0xffffffff
        E = D
        D = C
        C = shift(B, 30)
        B = A
        A = temp
    H0 = (H0 + A) & 0xffffffff
    H1 = (H1 + B) & 0xffffffff
    H2 = (H2 + C) & 0xffffffff
    H3 = (H3 + D) & 0xffffffff
    H4 = (H4 + E) & 0xffffffff


def SHA1(msg):
    global H0, H1, H2, H3, H4
    H0, H1, H2, H3, H4 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0
    msg, l = padding(msg)
    B = []
    for i in range(l):
        B.append(msg & ((1 << 512) - 1))
        msg >>= 512
    B = B[::-1]
    for i in range(l):
        process(B[i])
    return hex((((H0 << 32 | H1) << 32 | H2) << 32 | H3) << 32 | H4)[2:].rjust(40, '0')


def HMAC(key, msg):
    b = len(key) // 512 if len(key) % 512 == 0 else len(key) // 512 + 1
    b *= 512
    key = int.from_bytes(key, 'big')
    key <<= (b - bitlen(key))
    ipad = int("00110110" * (b // 8), 2)
    opad = int("01011100" * (b // 8), 2)
    step1 = SHA1((key ^ ipad).to_bytes(b // 8, 'big') + msg)
    return SHA1((key ^ opad).to_bytes(b // 8, 'big') + int('0x' + step1, 16).to_bytes(20, 'big'))

if __name__ == '__main__':
    print(HMAC(b'aa', b'flag{fun}'))
    print(HMAC(b'flag{fun}', b'aa'))

    # # example = b'shabi'
# 66666666666666666666666666666666666666666666666666666666666666WW
# 405c7047d5898ae90863e433bfebcc7eb2998091