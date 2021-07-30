from lab2.poly import poly

Sbox = []
ans = []
revSbox = []
revans = []

def tf(a):
    b = [0] * 8
    d = [0] * 8
    c = [0] * 8
    cc = 0b01100011
    res = 0
    for i in range(8):
        b[i] = a & 1
        c[i] = cc & 1
        a >>= 1
        cc >>= 1
    for i in range(8):
        d[i] = b[i] ^ b[(i + 4) % 8] ^ b[(i + 5) % 8] ^ b[(i + 6) % 8] ^ b[(i + 7) % 8] ^ c[i]
    for i in range(8):
        res |= (d[i] << i)
    return res

def rev_tf(a):
    b = [0] * 8
    d = [0] * 8
    c = [0] * 8
    cc = 5
    res = 0
    for i in range(8):
        b[i] = a & 1
        c[i] = cc & 1
        a >>= 1
        cc >>= 1
    for i in range(8):
        d[i] = b[(i + 2) % 8] ^ b[(i + 5) % 8] ^ b[(i + 7) % 8] ^ c[i]
    for i in range(8):
        res |= (d[i] << i)
    return res

def mul(a, b):
    return (poly(a) * poly(b)).data


if __name__ == "__main__":
    print(mul(2, 0x87) ^ mul(3, 0x6e) ^ mul(1, 0x46) ^ mul(1, 0xa6))

    for i in range(16):
        table = []
        tt = []
        for j in range(16):
            table.append(poly((i << 4) + j))
            tt.append(0)
        Sbox.append(table)
        ans.append(tt)
        revans.append(tt)
        revSbox.append(tt)


    for i in range(16):
        for j in range(16):
            t = Sbox[i][j]
            if t.data == 0:
                Sbox[i][j] = poly(0)
            else:
                Sbox[i][j] = poly.invmod(t)

    for i in range(16):
        for j in range(16):
            ans[i][j] = poly(tf(Sbox[i][j].data)).data

    for i in range(16):
        for j in range(16):
            revSbox[i][j] = poly.invmod(poly(rev_tf((i << 4) + j)))
            revans[i][j] = revSbox[i][j].data
    print(revans)