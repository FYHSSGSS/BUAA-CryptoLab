from __future__ import division

class poly:  # 100011011

    def __init__(self, v):
        self.data = v
        self.bin = bin(v)[2:]
        self.deg = len(self.bin) - 1

    def __repr__(self):
        return 'poly(%s)' % hex(self.data)[2:]

    def __str__(self):
        str = ''
        if self.data == 0:
            return '0'
        flag = False
        for i in range(self.deg + 1):
            if self.bin[i] == '1':
                if flag == True:
                    str += '+'
                flag = True
                if i == self.deg:
                    str += '1'
                elif i == self.deg - 1:
                    str += 'x'
                else:
                    str += 'x^' + chr(ord('0') + self.deg - i)
        return str

    def __add__(self, other):
        return poly(self.data ^ other.data)

    def __sub__(self, other):
        return self + other

    def __mul__(self, other):
        res = 0
        for i in range(self.deg + 1):
            u = ord(self.bin[i]) - ord('0')
            if u == 1:
                res ^= other.data << (self.deg - i)
        return poly(res) % poly(283)

    def __truediv__(self, other):
        u = self.data
        res = 0
        if other.data == 1:
            return self
        while (len(bin(u)[2:]) - 1) >= other.deg:
            temp = (len(bin(u)[2:]) - 1 - other.deg)
            res |= 1 << temp
            u = u ^ (other.data << temp)
        return poly(res)

    def __mod__(self, other):
        u = self.data
        res = 0
        if other.data == 1:
            return poly(0)
        while (len(bin(u)[2:]) - 1) >= other.deg:
            temp = (len(bin(u)[2:]) - 1 - other.deg)
            res |= 1 << temp
            u = u ^ (other.data << temp)
        return poly(u)

    def __pow__(self, power, modulo=None):
        res = poly(1)
        tmp = self
        while power:
            if power & 1:
                res = res * tmp
            tmp = tmp * tmp
            power >>= 1
        return res

    def gcd(a, b):
        return a if b.data == 0 else poly.gcd(b, a % b)

    def exgcd(a, b):
        if b.data == 0:
            return poly(1), poly(0), a
        x, y, z = poly.exgcd(b, a % b)
        return y, x - (a / b) * y, z

    def invmod(a):
        if a.data == 0:
            return poly(0)
        x, y, z = poly.exgcd(a, poly(283))
        assert z.data == 1
        return (x + poly(283)) % poly(283)


factor = [3, 5, 15, 17, 51, 85]


def mul(a, b):
    res = 0
    for i in range(a.deg + 1):
        u = ord(a.bin[i]) - ord('0')
        if u == 1:
            res ^= b.data << (a.deg - i)
    return res


def findIrreduciblePoly():
    IrreduciblePoly = []
    have = [0] * (1 << 9)
    for i in range(4):
        for j in range(1 << i + 1, 1 << i + 2):
            for k in range(1 << 8 - i - 1, 1 << 8 - i):
                have[mul(poly(j), poly(k))] = 1
    for i in range(1 << 8, 1 << 9):
        if have[i] == 0:
            IrreduciblePoly.append(poly(i))
    return IrreduciblePoly


def findPrimitiveElement():
    PrimitiveElement = []
    for i in range(2, 1 << 8):
        ori = now = poly(i)
        for fac in factor:
            if (now ** fac).data == 1:
                break
        else:
            PrimitiveElement.append(ori)
    return PrimitiveElement


def findPrimitivePoly():
    IrreduciblePoly = findIrreduciblePoly()
    PrimitivePoly = []
    for item in IrreduciblePoly:
        if (poly((1 << 255) | 1) % item).data != 0:
            continue
        for i in range(255):
            if (poly((1 << i) | 1) % item).data == 0:
                break
        else:
            PrimitivePoly.append(item)
    return PrimitivePoly


if __name__ == "__main__":
    # ans = [poly(0x89) + poly(0x4d), poly(0xaf) + poly(0x3b),
    #        poly(0x35) + poly(0xc6)]
    # ans = [poly(0xce) * poly(0xf1), poly(0x70) * poly(0x99),
    #        poly(0x00) * poly(0xa4)]
    # ans1 = [poly(0xde) / poly(0xc6), poly(0x8c) / poly(0x0a),
    #        poly(0x3e) / poly(0xa4)]
    # ans2 = [poly(0xde) % poly(0xc6), poly(0x8c) % poly(0x0a),
    #         poly(0x3e) % poly(0xa4)]
    # ans = [poly(0x89) ** 18829, poly(0x3e) ** 28928,
    #        poly(0x19) ** 26460, poly(0xba) ** 13563]
    # ans = [poly.exgcd(poly(0x75), poly(0x35)), poly.exgcd(poly(0xac), poly(0x59)),
    #        poly.exgcd(poly(0xf8), poly(0x2e)), poly.exgcd(poly(0x48), poly(0x99))]
    # ans = [poly.invmod(poly(0x8c)), poly.invmod(poly(0xbe)),
    #        poly.invmod(poly(0x01)), poly.invmod(poly(0x2d))]
    ls = findPrimitivePoly()
    for item in ls:
        print(str(item))
    print(len(ls))