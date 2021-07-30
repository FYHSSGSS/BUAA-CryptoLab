from CryptoLab import s2b

def init(S, K):
    j = 0
    k = []
    K = list(K)
    for i in range(len(K)):
        K[i] = ord(K[i])
    for i in range(256):
        S.append(i)
        k.append(K[i % len(K)])
    for i in range(256):
        j = (j + S[i] + k[i]) % 256
        S[i], S[j] = S[j], S[i]

def RC4crypt(key, D):
    S=[]
    init(S, key)
    i = j = 0
    result = ''

    for a in D:
        a = ord(a)
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = chr(a ^ S[(S[i] + S[j]) % 256])
        result += k
    return result

if __name__ == '__main__':
    key = 'Wiki'
    plaintext = 'pedia'
    res = RC4crypt(key, plaintext)
    print(s2b(res))
