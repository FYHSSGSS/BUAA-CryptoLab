from random import randint
from AITMCLab.Crypto.Util.number import isPrime

def Miller_Rabin(p):
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


a = int(input())
print(Miller_Rabin(a))
assert Miller_Rabin(a) == isPrime(a)

'''
172947529
22490812876539885046336053040043361022772062226905764414319531416752624982967181455912526153033030222985778230314070837549143068021815197910334221004333099

173114538715442253801652636578504897235814058376012019984132280493073144140873423822066926533851768593567972986030786930865304524765873917291156820356593465395949615668311730524585862713216977118030162614331116320577533153712280997129347743623082819252354000224098702300466561157715990374851814717133985999661
'''
