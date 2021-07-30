from hashlib import sha1
from random import randint
from CryptoLab import i2b, isPrime, getRandomNBitInteger, getPrime


def schnorr_genindex():
    q = getPrime(160)
    while True:
        r = getRandomNBitInteger(864)
        p = r * q + 1
        if isPrime(p):
            print(p, q)
            break
    for g in range(2, p):
        if pow(g, (p - 1) // 2, p) == p - 1:
            break
    g = pow(g, r, p)
    assert pow(g, q, p) == 1
    return p, q, g


p = 84958388206032748170493283013155238571162531544929971275958891333123307488183264027551586768492548367308300799416208654939642708411647183530732604670677742491605096023355760781484214112772120182730978697500344363183801796347215473527933301968337675888844779248789279922374433060164724023695473875862545292037
q = 1245239071094782032741659290395084523881662289289
g = 49832215898263969959124789833055480445598107142575918485493818609007291210947426506131351726099663621516396781573607922032218558743068101208867818731075036559625991084379441458037800962536842381742351595759234696472605258233777524956671604978076410112005048858846768741493761232239265216107732025105290188961


def schnorr_sig_keygen(p, g):
    s = randint(1, p - 1)
    v = pow(g, (p - 1 - s) % (p - 1), p)
    return v, s


def schnorr_sig(msg, prikey, p, q, g):
    r = randint(1, q - 1)
    x = i2b(pow(g, r, p))
    e = int(sha1(msg + x).hexdigest(), 16)
    y = (r + prikey * e) % q
    return e, y


def schnorr_sig_verify(msg, sig, pubkey, p, g):
    e, y = sig
    x_ = (pow(g, y, p) * pow(pubkey, e, p)) % p
    return e == int(sha1(msg + i2b(x_)).hexdigest(), 16)


def schnorr_sig_demo(msg):
    pubkey, prikey = schnorr_sig_keygen(p, g)
    sig = schnorr_sig(msg, prikey, p, q, g)
    print(sig)
    if not schnorr_sig_verify(msg, sig, pubkey, p, g):
        raise Exception('sig failed')


if __name__ == '__main__':
    schnorr_sig_demo(b'flag{fyh_is_dying}')
