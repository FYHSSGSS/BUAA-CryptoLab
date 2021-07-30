from random import randint


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def exgcd(a, b):
    if b == 0:
        return 1, 0, a
    x, y, z = exgcd(b, a % b)
    return y, x - (a // b) * y, z


def invmod(a, b):
    x, y, z = exgcd(a, b)
    assert z == 1
    return (x + b) % b


def modpow(n, k):
    global mod
    res = 1
    tmp = n
    while k:
        if k & 1:
            res = res * tmp % mod
        tmp = tmp * tmp % mod
        k >>= 1
    return res


def CRT(items):  # (a, b) in items, a is msg, b is modulo
    P = 1
    res = 0
    for a, n in items:
        P *= n
    for a, n in items:
        M = P // n
        res = (res + invmod(M, n) * M * a) % P
    return res


def exCRT(items):  # (a, b) in items, a is msg, b is modulo
    n = len(items)
    c, m = [], []
    for a, b in items:
        c.append(a)
        m.append(b)

    for i in range(1, n):
        t = gcd(m[i], m[i - 1])
        assert (c[i] - c[i - 1]) % t == 0
        c[i] = (invmod(m[i - 1] // t, m[i] // t) * (c[i] - c[i - 1]) // t) % (m[i] // t) * m[i - 1] + c[i - 1]
        m[i] = m[i] // t * m[i - 1]
        c[i] = (c[i] % m[i] + m[i]) % m[i]

    return c[n - 1]


def isPrime(p):
    if p < 2:
        return False
    if p == 2:
        return True
    if p == 3:
        return True
    d = p - 1
    r = 0
    while (d & 1) == 0:
        r += 1
        d >>= 1
    for i in range(10):
        a = randint(1, 65536) % (p - 2) + 2
        try:
            x = pow(a, d, p)
        except:
            print(a, d, p)
        if x == 1 or x == p - 1:
            continue
        for i in range(r):
            x = x * x % p
            if x == p - 1:
                break
        if x != p - 1:
            return False
    return True


def getRandomNBitInteger(N):
    return randint(2 ** (N - 1), 2 ** N)


def getPrime(N):
    number = getRandomNBitInteger(N) | 1
    while (not isPrime(number)):
        number = number + 2
    return number


def Matmul(a, b, p):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                res[i][j] = (res[i][j] + a[i][k] * b[k][j]) % p
    return res


def Matpow(a, n, p):
    res = a
    tmp = a
    n -= 1
    while n:
        if n & 1:
            res = Matmul(res, tmp, p)
        tmp = Matmul(tmp, tmp, p)
        n >>= 1
    return res


def RevMat(mat, mod):
    n = len(mat)
    line = [0] * n
    for i in range(n):
        line[i] = 1
        mat[i] += line
        line[i] = 0
    for i in range(n):
        k = i
        for j in range(i + 1, n):
            if mat[j][i] > mat[k][i]:
                k = j
        for j in range(i, 2 * n):
            mat[i][j], mat[k][j] = mat[k][j], mat[i][j]
        for j in range(n):
            if j != i:
                if mat[j][i] == 0:
                    continue
                lcm = mat[j][i] * mat[i][i] / gcd(mat[j][i], mat[i][i])
                det = mat[j][i]
                for k in range(2 * n):
                    mat[j][k] = lcm / mat[i][i] * mat[i][k] - lcm / det * mat[j][k]
    for i in range(n):
        GCD = mat[i][j]
        for j in range(n, 2 * n):
            GCD = gcd(GCD, mat[i][j])
        GCD = abs(GCD)
        for j in range(2 * n):
            if mat[i][j] != 0:
                mat[i][j] /= GCD
        for j in range(n, 2 * n):
            mat[i][j] = int((mat[i][j] * invmod(mat[i][i], mod)) % mod)
    res = []
    for i in range(n):
        res.append(mat[i][n: 2 * n])
    return res


prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
         109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
         233, 239, 241, 251]


def getStrongPrime():
    p1 = getRandomNBitInteger(256)
    while True:
        q1 = getRandomNBitInteger(256)
        r = p1 * q1 + 1
        if isPrime(r):
            break
    while True:
        q2 = getRandomNBitInteger(512)
        p = r * q2 + 1
        if isPrime(p):
            tmp = p
            for num in prime:
                while tmp % num == 0:
                    tmp = tmp // num
            if tmp > 2 ** 128:
                break
    return p


def Lucas(p, x, y, k):
    mat = [[x, 1], [(p - y) % p, 0]]
    mat = Matpow(mat, k - 1, p)
    u = mat[0][0]
    v = (mat[0][0] * x + mat[1][0] * 2) % p
    return u, v


def sqrtmod(g, p) -> int:
    if p % 4 == 3:
        u = (p - 3) // 4
        y = pow(g, u + 1, p)
        if y * y % p != g:
            raise Exception('There is no solution.')
        return y
    elif p % 8 == 5:
        u = (p - 5) // 8
        z = pow(g, 2 * u + 1, p)
        if z % p == 1:
            return pow(g, u + 1, p)
        elif z % p == p - 1:
            return (2 * g * pow(4 * g, u, p)) % p
        else:
            raise Exception('There is no solution.')
    elif p % 8 == 1:
        u = (p - 1) // 8
        Y = g
        while True:
            X = randint(0, p)
            U, V = Lucas(p, X, Y, 4 * u + 1)
            if V * V % p == (4 * Y) % p:
                return (V * invmod(2, p)) % p
            elif U % p != 1 and U % p != p - 1:
                raise Exception('There is no solution.')


def TonelliShanks(a, p):
    b = randint(1, p)
    while (pow(b, (p - 1) // 2, p) == 1):
        b = randint(1, p)
    t = p - 1
    s = 0
    while (t % 2 == 0):
        s += 1
        t = t // 2
    x = pow(a, (t + 1) // 2, p)
    e = pow(a, t, p)
    k = 1
    while (k < s):
        if (pow(e, 1 << (s - k - 1), p) != 1):
            x = x * pow(b, (1 << (k - 1)) * t, p) % p
        e = pow(a, p - 2, p) * x % p * x % p
        k += 1
    return x


def last(num, length):
    return num & ((1 << length) - 1)


def shift(num, pos, length):
    return last((num << pos) | (num >> (length - pos)), length)


def bitlen(num):
    if num == 0:
        return 1
    res = 1
    while num:
        res, num = res + 1, num >> 1
    return res


def byteslen(num):
    return bitlen(num) // 8 if bitlen(num) % 8 == 0 else bitlen(num) // 8 + 1


def s2b(str):
    res = ''
    for c in str:
        res += hex(ord(c))[2:]
    return res

def i2b(num):
    return num.to_bytes(byteslen(num), 'big')

def printh(x):
    print(hex(x)[2:])


if __name__ == "__main__":
    print(sqrtmod(9, 41))
    print(TonelliShanks(9, 41))
    pass
'''
'''
