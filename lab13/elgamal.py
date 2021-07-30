from CryptoLab import getStrongPrime, invmod, gcd
from hashlib import sha256
from random import randint


def elgamal_genindex():
    p = getStrongPrime()
    for g in range(2, p):
        if pow(g, (p - 1) // 2, p) == p - 1:
            break
    return p, g


p = 42544412271198299114817427400500351976173072640553999494011956673396285630155346690686196913357960543297089445320396106887013515159033345638012687373729821734655959414814717646818115516845862506573985525037093439610718885428738869573600133679242551078685881484786977371784948416563538976347837409044801711771
g = 2


def elgamal_sig_keygen(p, g):
    x = randint(1, p - 1)
    y = pow(g, x, p)
    return y, x


def elgamal_sig(msg, prikey, p, g):
    m = int(sha256(msg).hexdigest(), 16)
    while True:
        k = randint(1, p - 1)
        if gcd(k, p - 1) == 1:
            break
    r = pow(g, k, p)
    s = invmod(k, p - 1) * (m - prikey * r) % (p - 1)
    return r, s


def elgamal_sig_verify(msg, sig, pubkey, p, g):
    m = int(sha256(msg).hexdigest(), 16)
    r, s = sig
    V1 = pow(g, m, p)
    V2 = (pow(pubkey, r, p) * pow(r, s, p)) % p
    return V1 == V2


def elgamal_sig_demo(msg):
    pubkey, prikey = elgamal_sig_keygen(p, g)
    r, s = elgamal_sig(msg, prikey, p, g)
    print(r, s)
    if not elgamal_sig_verify(msg, (r, s), pubkey, p, g):
        raise Exception('sig failed')


if __name__ == '__main__':
    elgamal_sig_demo(b'flag{fyh_is_dying}')
