from CryptoLab import invmod, sqrtmod, byteslen
from random import randint
from libnum import s2n


class ECC:
    def __init__(self, a, b, p, n, G):
        if 4 * a * a ** 3 + 27 * b ** 2 % p == 0:
            raise Exception('It\'s not an EllipticCurve.')
        self.a, self.b, self.p, self.n = a, b, p, n
        self.G = ECCpoint(G[0], G[1], self)

    def __str__(self):
        return 'GF({}), y ** 2 = x ** 2 + {} * x + {}'.format(self.p, self.a, self.b)

    def f(self, x, tp=-1):
        a, b, p = self.a, self.b, self.p
        try:
            res = sqrtmod((x ** 3 + a * x + b) % p, p)
        except:
            raise Exception('There is no point.')
        if tp == -1:
            return res
        if res % 2 != tp:
            res = p - res
        return res

    def is_on_curve(self, point):
        x, y = point
        return y ** 2 % self.p == (x ** 3 + self.a * x + self.b) % self.p

    def gen(self):
        while True:
            x = randint(0, self.p)
            try:
                y = self.f(x)
            except:
                continue
            else:
                assert self.is_on_curve((x, y))
                return ECCpoint(x, y, self)

    def ECCencode(self, msg):
        X = chr(len(msg)).encode() + msg
        while True:
            try:
                self.f(s2n(X))
            except:
                X += chr(randint(0, 256)).encode()
            else:
                break
        return X

    def ECCdecode(self, msg):
        msg = msg.to_bytes(byteslen(msg), 'big')
        return msg[1:1 + msg[0]]


class ECCpoint:
    def __init__(self, x, y, curve: ECC):
        self.x = x
        self.y = y
        self.curve = curve

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __neg__(self):
        return ECCpoint(self.x, (-self.y + self.curve.p) % self.curve.p, self.curve)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.curve == other.curve

    def __add__(self, other):
        if not self.curve == other.curve:
            raise Exception('Not the same curve.')
        p1 = (self.x, self.y)
        p2 = (other.x, other.y)
        a, b, p = self.curve.a, self.curve.b, self.curve.p
        if p1 == (0, 0):
            return ECCpoint(p2[0], p2[1], self.curve)
        if p2 == (0, 0):
            return ECCpoint(p1[0], p1[1], self.curve)
        if p1[0] == p2[0] and (p1[1] != p2[1] or p1[1] == 0):
            return ECCpoint(0, 0, self.curve)
        if p1[0] == p2[0]:
            k = (3 * p1[0] * p1[0] + a) * invmod(2 * p1[1], p) % p
        else:
            k = (p2[1] - p1[1]) * invmod(p2[0] - p1[0], p) % p
        x = (k * k - p1[0] - p2[0]) % p
        y = (k * (p1[0] - x) - p1[1]) % p
        return ECCpoint(int(x), int(y), self.curve)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, r: int):
        res = ECCpoint(0, 0, self.curve)
        tmp = ECCpoint(self.x, self.y, self.curve)
        while r:
            if r & 1:
                res += tmp
            r, tmp = r >> 1, tmp + tmp
        return res


def p2b(p: ECCpoint, tp=1):
    x, y = p.x, p.y
    len = byteslen(p.curve.p)
    x1 = x.to_bytes(len, 'big')
    if tp == 1:
        PC = b'\x03' if y % 2 else b'\x02'
        return PC + x1
    elif tp == 2:
        return b'\x04' + x1 + y.to_bytes(len, 'big')
    else:
        PC = b'\x07' if y % 2 else b'\x06'
        return PC + x1 + y.to_bytes(len, 'big')


def b2p(bts, curve, tp=1):
    l = (len(bts) - 1) // 2
    if tp == 1:
        if not bts[0] == 2 and not bts[0] == 3:
            raise Exception('Transmission Error')
        y_ = bts[0] - 2
        X = int.from_bytes(bts[1:], 'big')
        return ECCpoint(X, curve.f(X, y_), curve)
    elif tp == 2:
        if not bts[0] == 4:
            raise Exception('Transmission Error')
        X = int.from_bytes(bts[1:1 + l], 'big')
        Y = int.from_bytes(bts[1 + l:], 'big')
        return ECCpoint(X, Y, curve)
    else:
        if not bts[0] == 6 and not bts[0] == 7:
            raise Exception('Transmission Error')
        X = int.from_bytes(bts[1:1 + l], 'big')
        Y = int.from_bytes(bts[1 + l:], 'big')
        return ECCpoint(X, Y, curve)


def keygen(curve: ECC):
    k = randint(0, curve.n)
    K = curve.G * k
    return (k, K)


def ECCencrypt(X, curve: ECC, pubkey, tp=1):
    r = randint(0, curve.n)
    M = ECCpoint(X, curve.f(X), curve)
    return p2b(M + pubkey * r, tp), p2b(curve.G * r, tp)


def ECCdecrypt(rec1, rec2, curve: ECC, prikey, tp=1):
    rec1, rec2 = b2p(rec1, curve, tp), b2p(rec2, curve, tp)
    return rec1 - rec2 * prikey


def ECC_demo(msg, curve: ECC):
    prikey, pubkey = keygen(curve)
    send = curve.ECCencode(msg)
    send1, send2 = ECCencrypt(s2n(send), curve, pubkey)
    M = ECCdecrypt(send1, send2, curve, prikey)
    rev = curve.ECCdecode(M.x)
    assert rev == msg


def prikeySwap(pri, pub):
    return pub * pri


def DiffieHellman_demo(curve: ECC):
    nA, nB = randint(0, curve.n), randint(0, curve.n)
    QA, QB = curve.G * nA, curve.G * nB
    UserA = prikeySwap(nA, QB)
    UserB = prikeySwap(nB, QA)
    assert UserA == UserB


F192 = ECC(
    p=0xBDB6F4FE3E8B1D9E0DA8C0D46F4C318CEFE4AFE3B6B8551F,
    a=0xBB8E5E8FBC115E139FE6A814FE48AAA6F0ADA1AA5DF91985,
    b=0x1854BEBDC31B21B7AEFC80AB0ECD10D5B1B3308E6DBF11C1,
    G=(0x4AD5F7048DE709AD51236DE65E4D4B482C836DC6E4106640,
       0x02BB3A02D4AAADACAE24817A4CA3A1B014B5270432DB27D2),
    n=0xBDB6F4FE3E8B1D9E0DA8C0D40FC962195DFAE76F56564677
)
F256 = ECC(
    p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3,
    a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498,
    b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A,
    G=(0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D,
       0x0680512BCBB42C07D47349D215B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2),
    n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
)
secp256k1 = ECC(
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    a=0,
    b=7,
    G=(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
       0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    n=0xFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
)

CISCN = ECC(
    p=104466759016764083234793487593720243861078529984099167682215758982276722207663,
    a=307741287276458391503506338633462355433,
    b=178916432495924348407526661075077695253,
    G=(4000845518290273963066606431579740778245542598780355501281623551531115036532,
       19098911116117250245375515920214811578609102353700578594965693993196176198033),
    n=0
)
if __name__ == "__main__":
    DiffieHellman_demo(F192)
    # tmp_point = CISCN.G
    # fp = open('data.txt', 'r')
    # flag = ''
    # for line in fp.readlines():
    #     line = int(line.replace('\n', ''))
    #     for i in range(128):
    #         if (tmp_point * i).x == line:
    #             tmp_point = tmp_point * i
    #             flag += chr(i)
    # print(flag)
    # p = 104466759016764083234793487593720243861078529984099167682215758982276722207663
    # x1 = 4000845518290273963066606431579740778245542598780355501281623551531115036532
    # y1 = 19098911116117250245375515920214811578609102353700578594965693993196176198033
    # x2 = 30933137690693274770581385330077244937989273717049042727367799086363664474872
    # y2 = 68198610651278270431725899396511412842027441125758508637455759084125162270171
    # a = (((y2 ** 2 - x2 ** 3) - (y1 ** 2 - x1 ** 3)) % p + p) % p * invmod((x2 - x1), p) % p
    # print(a)
    # b = (((y1 ** 2 - x1 ** 3) - a * x1) % p + p) % p
    # print(b)
    # assert (y1 ** 2) % p == (x1 ** 3 + a * x1 + b) % p
    # assert (y2 ** 2) % p == (x2 ** 3 + a * x2 + b) % p
