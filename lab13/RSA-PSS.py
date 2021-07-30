from hashlib import sha1
from math import ceil
from CryptoLab import getRandomNBitInteger, getStrongPrime, invmod


def MGF1(msg, maskLen):
    T = b''
    k = ceil(maskLen / 20)
    for counter in range(k):
        cnt = counter.to_bytes(4, 'big')
        T += sha1(msg + cnt).digest()
    return T[:maskLen]


def RSA_key_gen():
    p, q = getStrongPrime(), getStrongPrime()
    N = p * q
    e = 65537
    d = invmod(e, (p - 1) * (q - 1))
    return N, e, d


N = 3473368149650603148803248362859305810616830384713657576189830461663272229290941849749535852215753586078339602564703534544019270264758123888720790402066935128355365198517106201587833213985641081363529915405154534421955067011239544160379626647436269174669982624065257106974978034397237801426486327072733866941256103866379494352699331703600225626341270638466960870963368915890428723335452705666327012968661441098599531507370330709071561749402190081263005751377060766912253160596080441317443444238137527565995930091079370074820236433361851170139013408559792217741431999167452032312421940893219990759342422335291584922679
e = 65537
d = 1162152933236773514914592216622348563638949855440454755797345047276381791108713747673952456892855099188638949067531609708733304215414439791749233134512164937280871081573509693584051859503442904498824846804159919294515017614820036381720317578237980231963064818049391303259949621408710049432839345408714287109345398814512462890065142333990159447216394268072867586567865841287731904542012092589440889131990826657294780274422404008400777545284141318433828812877026565204852346034671074895135016040661630824182518645904726697790893178433416235613878827124199015085219721368430257092776492449477981215171599784246139064769


def RSAPSSmsg_encode(msg, emBits):
    emLen = ceil(emBits / 8)
    salt = getRandomNBitInteger(160).to_bytes(20, 'big')
    mHash = sha1(msg).digest()
    padding1 = (0).to_bytes(8, 'big')
    padding2 = b'\x00' * (emLen - 42) + b'\x01'
    H = sha1(padding1 + mHash + salt).digest()
    DB = padding2 + salt
    dbMask = MGF1(H, emLen - 21)
    maskedDB = b''
    for i in range(emLen - 21):
        maskedDB += (DB[i] ^ dbMask[i]).to_bytes(1, 'big')
    first = maskedDB[0] & (255 - (1 << (7 - 8 * emLen + emBits)))
    return (first).to_bytes(1, 'big') + maskedDB[1:] + H + b'\xbc'


def RSAPSS_sig(msg, emBits):
    m = RSAPSSmsg_encode(msg, emBits)
    s = pow(int.from_bytes(m, 'big'), d, N)
    return s.to_bytes(256, 'big')


def RSARSS_sig_verify(cipher, msg, emBits):
    cipher = int.from_bytes(cipher, 'big')
    emLen = ceil(emBits / 8)
    m = pow(cipher, e, N)
    EM = m.to_bytes(emLen, 'big')
    mHash = sha1(msg).digest()
    if emLen < 42 or EM[-1] != 188:
        return False
    maskedDB = EM[: emLen - 21]
    H = EM[emLen - 21: -1]
    if (maskedDB[0] >> (7 - 8 * emLen + emBits)) & 1:
        return False
    dbMask = MGF1(H, emLen - 21)
    DB = b''
    for i in range(emLen - 21):
        DB += (maskedDB[i] ^ dbMask[i]).to_bytes(1, 'big')
    salt = DB[-20:]
    padding1 = (0).to_bytes(8, 'big')
    M_ = padding1 + mHash + salt
    H_ = sha1(M_).digest()
    return H_ == H


def RSAPSS_demo(msg, emBits):
    sig = RSAPSS_sig(msg, emBits)
    print(sig)
    if not RSARSS_sig_verify(sig, msg, emBits):
        raise Exception('sig failed')


if __name__ == '__main__':
    RSAPSS_demo(b'flag{fyh_is_dying}', 2001)
