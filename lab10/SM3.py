IV = 0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e
T = [0x79cc4519] * 16 + [0x7a879d8a] * 48


def shift(num, pos):
    return ((num << pos) | (num >> (32 - pos))) & 0xffffffff


def FF(X, Y, Z, j):
    if j <= 15:
        return X ^ Y ^ Z
    else:
        return (X & Y) | (X & Z) | (Y & Z)


def GG(X, Y, Z, j):
    if j <= 15:
        return X ^ Y ^ Z
    else:
        return (X & Y) | ((X ^ 0xffffffff) & Z)


def P0(n):
    return n ^ shift(n, 9) ^ shift(n, 17)


def P1(n):
    return n ^ shift(n, 15) ^ shift(n, 23)


def padding(msg):
    l = len(msg) * 8
    intmsg = int.from_bytes(msg, 'big')
    k, length = 448 - l - 1, 1
    while k < 0:
        k += 512
        length += 1
    intmsg = ((intmsg << 1) | 1) << (k + 64) | l
    return intmsg, length


def CF(V, B):
    V0 = V
    A, W, W_ = [], [], []
    for i in range(16):
        W.append(B & 0xffffffff)
        B >>= 32
    W = W[::-1]
    for i in range(16, 68):
        W.append(P1(W[i - 16] ^ W[i - 9] ^ shift(W[i - 3], 15)) ^ shift(W[i - 13], 7) ^ W[i - 6])
    for i in range(64):
        W_.append(W[i] ^ W[i + 4])
    for i in range(8):
        A.append(V & 0xffffffff)
        V >>= 32
    A = A[::-1]
    for i in range(64):
        SS1 = shift((shift(A[0], 12) + A[4] + shift(T[i], i % 32)) % (1 << 32), 7)
        SS2 = SS1 ^ shift(A[0], 12)
        TT1 = (FF(A[0], A[1], A[2], i) + A[3] + SS2 + W_[i]) % (1 << 32)
        TT2 = (GG(A[4], A[5], A[6], i) + A[7] + SS1 + W[i]) % (1 << 32)
        A[3] = A[2]
        A[2] = shift(A[1], 9)
        A[1] = A[0]
        A[0] = TT1
        A[7] = A[6]
        A[6] = shift(A[5], 19)
        A[5] = A[4]
        A[4] = P0(TT2)
    res = A[0]
    for i in range(1, 8):
        res <<= 32
        res |= A[i]
    return res ^ V0


def SM3(msg):
    msg, l = padding(msg)
    B = []
    for i in range(l):
        B.append(msg & ((1 << 512) - 1))
        msg >>= 512
    B = B[::-1]
    V = IV
    for i in range(l):
        V = CF(V, B[i])
    return V.to_bytes(32, 'big')


if __name__ == "__main__":
    print(SM3(b'flag{just_for_fun}'))