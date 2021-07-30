# !/usr/bin/env python3

from poly import *
from math import floor, log
from copy import deepcopy
import os
import socketserver
import signal
import random
import sys

flag = b'flag{or4nge&&L3ft_egd3!!}'

q = 2 ** 54
n = 1024
t = 83
T = 100
l = floor(log(q, t))
delta = floor(q / t)
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
        if c.cofficient[i] >= t / 2:
            c.cofficient[i] -= t
    return c


def keygen():
    s = Poly(n, q)
    s.randomize(type=2, sigma=sigma, mu=mu)
    e = Poly(n, q)
    e.randomize(type=1, sigma=sigma, mu=mu)
    a = Poly(n, q)
    a.randomize(B=q)
    pk = [Round(-1 * (a * s + e), q), a]
    return pk, s


def encrypt(pk, m):
    u = Poly(n, q)
    u.randomize(type=1, sigma=sigma, mu=mu)
    e1 = Poly(n, q)
    e1.randomize(type=1, sigma=sigma, mu=mu)
    e2 = Poly(n, q)
    e2.randomize(type=1, sigma=sigma, mu=mu)
    return [Round(pk[0] * u + e1 + delta * m, q), Round(pk[1] * u + e2, q)]


def decrypt(sk, ct):
    tmp = t * Round(ct[0] + ct[1] * sk, q)
    for i in range(tmp.n):
        tmp.cofficient[i] = round(tmp.cofficient[i] / q)
    return Round(tmp, t)


class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'[-] '):
        self.send(prompt, newline=False)
        return self._recvall()

    def fun(self):
        global pk, sk, m, ct
        a = Poly(n, q)
        b = Poly(n, q)
        tmp = [0] * n
        self.send(b'c0:')
        s = self.recv().strip().decode().replace(" ", "").split(",")
        # print(s)
        a.cofficient = deepcopy(list(map(int, s)))
        self.send(b'c1:')
        s = self.recv().strip().decode().replace(" ", "").split(",")
        # print(s)
        b.cofficient = deepcopy(list(map(int, s)))

        if a.cofficient == ct[0].cofficient or b.cofficient == ct[1].cofficient:
            self.send(b'opps')
            self.request.close()
        if tmp == a.cofficient or tmp == b.cofficient:
            self.send(b'opps')
            self.request.close()
        try:
            self.send(str(decrypt(sk, [a, b]).cofficient).encode())
        except:
            self.send(b'opps')
            self.request.close()

    def handle(self):
        global pk, sk, m, ct
        signal.alarm(1000)
        pk, sk = keygen()
        m = encode(flag)
        ct = encrypt(pk, m)
        self.send(str(pk[0].cofficient).encode())
        self.send(str(pk[1].cofficient).encode())
        self.send(str(ct[0].cofficient).encode())
        self.send(str(ct[1].cofficient).encode())

        while True:
            self.send(MENU.encode())
            option = int(self.recv().strip().decode())
            if option == 1:
                self.fun()
            else:
                self.send(b'exit')
                self.request.close()


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 22338
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
