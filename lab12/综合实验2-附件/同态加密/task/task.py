from poly import *
from math import floor, log
from copy import deepcopy
import os
import random
import sys

flag = b'falg{}'

q = 2**54
n = 1024
t = 83
T = 100
l = floor(log(q, t))
delta = floor(q/t)
mu = 0
sigma = 1
MENU = \
'''
Happy game!
1. decrypt
2. exit
'''

def encode(s):
    _s = s + os.urandom(128 - len(flag))
    tmp = bin(int.from_bytes(_s, "big"))[2:].zfill(n)
    tmp = list(map(int, tmp))
    TMP = Poly(n, q)
    TMP.cofficient = deepcopy(tmp)
    return TMP

def Round(poly, t):
    c = deepcopy(poly)
    for i in range(c.n):
        c.cofficient[i] = c.cofficient[i] % t
        if c.cofficient[i] >= t/2:
            c.cofficient[i] -= t
    return c

def keygen():
    s = Poly(n, q)
    s.randomize(type=2, sigma=sigma,  mu=mu)
    e = Poly(n, q)
    e.randomize(type=1, sigma=sigma,  mu=mu)
    a = Poly(n, q)
    a.randomize(B=q)
    pk = [Round(-1*(a*s+e), q), a]
    return pk, s

def encrypt(pk, m):
    u = Poly(n, q)
    u.randomize(type=1, sigma=sigma,  mu=mu)
    e1 = Poly(n, q)
    e1.randomize(type=1, sigma=sigma, mu=mu)
    e2 = Poly(n, q)
    e2.randomize(type=1, sigma=sigma, mu=mu)
    return [Round(pk[0]*u+e1+delta*m, q), Round(pk[1]*u+e2, q)]

def decrypt(sk, ct):
    tmp = t * Round(ct[0] + ct[1] * sk, q)
    for i in range(tmp.n):
        tmp.cofficient[i] = round(tmp.cofficient[i] / q)
    return Round(tmp, t)

def fun():
    a = Poly(n, q)
    b = Poly(n, q)
    tmp = [0]*n
    print("c0:")
    s = input().replace(" ", "").split(",")
    a.cofficient = deepcopy(list(map(int, s)))
    print("c1:")
    s = input().replace(" ", "").split(",")
    b.cofficient = deepcopy(list(map(int, s)))
    assert a.cofficient != ct[0].cofficient and b.cofficient != ct[1].cofficient
    assert tmp != a.cofficient and tmp != b.cofficient
    print(decrypt(sk, [a, b]).cofficient)


pk, sk = keygen()
m = encode(flag)
ct = encrypt(pk, m)
allowed = False
print(pk[0].cofficient)
print(pk[1].cofficient)
print(ct[0].cofficient)
print(ct[1].cofficient)

while True:
    print(MENU)
    option = int(input())
    if option == 1:
        fun()
    else:
        print("exit")
        sys.exit(1)
