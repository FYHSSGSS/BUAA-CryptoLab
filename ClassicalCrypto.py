from CryptoLab import invmod, RevMat
from itertools import cycle
from math import ceil


def l2n(c):
    return ord(c) - ord('a')


def n2l(a):
    return chr(a + ord('a'))


def AffineEncrypt(k, b, msg):
    return "".join([n2l((l2n(c) * k + b) % 26) for c in msg])


def AffineDecrypt(k, b, msg):
    return "".join([n2l(invmod(k, 26) * (l2n(c) - b) % 26) for c in msg])


def SimpleReplaceEncrypt(Replace, msg):
    assert len(Replace) == 26
    return "".join([Replace[ord(c) - ord('a')] for c in msg])


def SimpleReplaceDecrypt(Replace, msg):
    assert len(Replace) == 26
    tmp = [0] * 26
    for i in range(26):
        assert tmp[l2n(Replace[i])] == 0
        tmp[l2n(Replace[i])] = n2l(i)
    return "".join([tmp[ord(c) - ord('a')] for c in msg])


def VigenereEncrypt(key, msg):
    return "".join(n2l((l2n(c) + l2n(d)) % 26) for c, d in zip(msg, cycle(key)))


def VigenereDecrypt(key, msg):
    return "".join(n2l((l2n(c) - l2n(d) + 26) % 26) for c, d in zip(msg, cycle(key)))


def VernamEncrypt(key, input, output):
    with open(input, 'r') as fin:
        msg = fin.readline()
    cipher = bytes([ord(c) ^ ord(d) for c, d in zip(msg, cycle(key))])
    with open(output, 'wb') as fout:
        fout.write(cipher)


def VernamDecrypt(key, input, output):
    VernamEncrypt(key, input, output)


def FenceEncrypt(n, msg):
    l = ceil(len(msg) / n)
    cipher = [0] * (n * l)
    for i in range(len(msg)):
        cipher[i % n * l + i // n] = msg[i]
    while 0 in cipher:
        cipher.remove(0)
    return "".join(cipher)


def FenceDecrypt(n, msg):
    l = ceil(len(msg) / n)
    process = ''
    tmp = 0
    for i in range(l * n):
        if i % l == l - 1 and i / l > len(msg) % n:
            process += '$'
        else:
            process += msg[tmp]
            tmp += 1
    cipher = ''
    for i in range(len(msg)):
        cipher += process[i % n * l + i // n]
    return cipher.replace('$', '')


def HillEncrypt(mat, msg):
    cipher = ''
    buf = ''
    n = len(mat)
    add_chr = n2l(n) if len(msg) % n == 0 else n2l(len(msg) % n)
    msg += add_chr
    while len(msg) % n != 0:
        msg += add_chr
    for c in msg:
        if c >= 'a' and c <= 'z':
            buf += c
        else:
            cipher += c
        if len(buf) == n:
            X = []
            for ch in buf:
                X.append(l2n(ch))
            # print(buf,X)
            Y = [0] * n
            for i in range(n):
                for j in range(n):
                    Y[i] = (Y[i] + mat[j][i] * X[j]) % 26
            print(Y)
            for i in range(n):
                cipher += n2l(Y[i])
            buf = ''
    return cipher


def HillDecrypt(mat, msg):
    cipher = ''
    buf = ''
    mat = RevMat(mat, 26)
    print(mat)
    n = len(mat)
    for c in msg:
        if c >= 'a' and c <= 'z':
            buf += c
        else:
            cipher += c
        if len(buf) == n:
            X = []
            for ch in buf:
                X.append(l2n(ch))
            Y = [0] * n
            for i in range(n):
                for j in range(n):
                    Y[i] = (Y[i] + mat[j][i] * X[j]) % 26
            for i in range(n):
                cipher += n2l(Y[i])
            buf = ''
    print(cipher)
    return cipher[0:len(msg) - l2n(cipher[-1]) + 1]


def MatrixEncrypt(permutation, msg):
    permutation = [item - 1 for item in permutation]
    n = len(permutation)
    pos = [0] * n
    for i in range(n):
        pos[permutation[i]] = i
    cipher = ''
    for i in range(n):
        now = pos[i]
        while now < len(msg):
            cipher += msg[now]
            now += n
    return cipher


def MatrixDecrypt(permutation, msg):
    permutation = [item - 1 for item in permutation]
    n = len(permutation)
    cipher = [0] * len(msg)
    pos = [0] * n
    for i in range(n):
        pos[permutation[i]] = i
    row = [len(msg) // n] * n
    for i in range(n):
        if i in permutation[0:len(msg) % n]:
            row[i] += 1
    now = 0
    cnt = 0
    for c in msg:
        cipher[cnt * n + pos[now]] = c
        cnt += 1
        if cnt >= row[now]:
            now += 1
            cnt = 0
    return "".join(cipher)


def vigenereEncrypt(key, msg):
    return "".join(n2l((l2n(c) + d) % 26) for c, d in zip(msg, cycle(key)))


if __name__ == "__main__":
    cnt = 0
    for a in range(26):
        for b in range(26):
            for c in range(26):
                for d in range(26):
                    # if (a * d - c * b) % 2 == 0 and ((a % 2 == 0 and b % 2 == 0) or (c % 2 == 0 and d % 2 ==0)):
                    # if (a * d - c * b) % 2 == 0 and ((a % 2 == 0 and c % 2 == 0) or (b % 2 == 0 and d % 2 == 0)):
                    # if (a * d - c * b) % 2 == 0 and a % 2 == 1 and c % 2 == 1 and b % 2 == 1 and d % 2 == 1:
                    # if (a * d - c * b) % 2 == 0:
                    # if (a * d - c * b) % 13 == 0 and a % 13 == 0 and b % 13 == 0:
                    # if (a * d - c * b) % 13 == 0:
                    # if (a * d - c * b) % 13 != 0 and (a * d - c * b) % 2 != 0:
                        cnt += 1
    print(cnt)
'''
sendmoremoney
beokjdmsxzpmh
cashnotneeded
[x10 = 11, x00 = 24, x01 = -77, x11 = -30]
paymoremoney
'''
