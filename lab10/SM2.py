from ECC import *
import uuid
from CryptoLab import bitlen, i2b, invmod
from SM3 import SM3
from math import ceil
from random import randint

def KDF(msg, maskLen):
    T = b''
    k = ceil(maskLen / 32)
    for counter in range(1, k + 1):
        cnt = counter.to_bytes(4, 'big')
        T += SM3(msg + cnt)
    return T[:maskLen]

def DigitalSignature(Za, msg, prikey, curve: ECC):
    e = int.from_bytes(SM3(Za + msg), 'big')
    while True:
        k = randint(1, curve.n - 1)
        x1 = (curve.G * k).x
        r = (e + x1) % curve.n
        if r == 0 or r + k == curve.n:
            continue
        s = (invmod(1 + prikey, curve.n) * (k - r * prikey)) % curve.n
        if s == 0:
            continue
        return i2b(r), i2b(s)


def SigatureCheck(Za, sig1, sig2, msg, pubkey, curve: ECC):
    r, s = int.from_bytes(sig1, 'big'), int.from_bytes(sig2, 'big')
    if r < 1 or r >= curve.n:
        return False
    if s < 1 or s >= curve.n:
        return False
    e_ = int.from_bytes(SM3(Za + msg), 'big')
    t = (r + s) % curve.n
    if t == 0:
        return False
    x1_ = (curve.G * s + pubkey * t).x
    R = (e_ + x1_) % curve.n
    return R == r


def SM2DigitalSignature_demo(msg, curve: ECC):
    prikey, pubkey = keygen(curve)
    IDa = int(str(uuid.uuid3(uuid.NAMESPACE_DNS, 'FYHSSGSS')).replace('-', ''), 16)
    entlenA = bitlen(IDa).to_bytes(2, 'big')
    IDa = IDa.to_bytes(byteslen(IDa), 'big')
    Za = SM3(entlenA + IDa + i2b(curve.a) + i2b(curve.b) \
             + i2b(curve.G.x) + i2b(curve.G.y) + i2b(pubkey.x) + i2b(pubkey.y))
    sig1, sig2 = DigitalSignature(Za, msg, prikey, curve)
    assert SigatureCheck(Za=Za, sig1=sig1, sig2=sig2, msg=msg, pubkey=pubkey,
                         curve=curve) == True

def SM2_encrypt(msg, pubkey, curve: ECC):
    klen = len(msg)
    while True:
        k = randint(1, curve.n)
        C1 = p2b(curve.G * k)
        temp = pubkey * k
        x2, y2 = i2b(temp.x), i2b(temp.y)
        t = KDF(x2 + y2, klen)
        if int.from_bytes(t, 'big'):
            break
    C2 = b''
    for i in range(klen):
        C2 += (msg[i] ^ t[i]).to_bytes(1, 'big')
    C3 = SM3(x2 + msg + y2)
    return C1 + C3 + C2


def SM2_decrypt(cipher, prikey, curve: ECC):
    first_len = len(p2b(curve.gen()))
    C1 = cipher[: first_len]
    C3 = cipher[first_len: first_len + 32]
    C2 = cipher[first_len + 32:]
    klen = len(C2)
    C1_point = b2p(C1, curve)
    if not curve.is_on_curve((C1_point.x, C1_point.y)):
        raise Exception('decrypt failed')
    temp = C1_point * prikey
    x2, y2 = i2b(temp.x), i2b(temp.y)
    t = KDF(x2 + y2, klen)
    msg = b''
    for i in range(klen):
        msg += (C2[i] ^ t[i]).to_bytes(1, 'big')
    u = SM3(x2 + msg + y2)
    if u != C3:
        raise Exception('decrypt failed')
    return msg

def SM2_demo(msg, curve: ECC):
    prikey, pubkey = keygen(curve)
    cipher = SM2_encrypt(msg, pubkey, curve)
    rebuild_msg = SM2_decrypt(cipher, prikey, curve)
    assert msg == rebuild_msg

if __name__ == '__main__':
    SM2_demo(b'flag{fyh_is_dying}, F192)
    SM2DigitalSignature_demo(b'flag{fyh_is_dying}', F192)
