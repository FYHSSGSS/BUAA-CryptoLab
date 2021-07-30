# !/usr/bin/env python3
import socketserver
import signal
import string
import random
import os

flag = b'flag{XXXXXXXXXXXX}'

def isPrime(n):
    basis = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79]
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for b in basis:
        x = pow(b, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
            else:
                return False
    return True


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


    def handle(self):
        signal.alarm(1000)

        self.send(b'[+] Welcome!')
        self.send(b'[+] Let\'s play a game!')

        self.send(b"[+] Plz give me your P: ")
        p = int(self.recv().strip().decode())
        self.send(b"[+] Plz give me your Q: ")
        q = int(self.recv().strip().decode())
        self.send(b"[+] Plz give me your R: ")
        r = int(self.recv().strip().decode())
        self.send(b"[+] Plz give me your N: ")
        n = int(self.recv().strip().decode())
        if isPrime(p) and isPrime(q) and isPrime(r) and isPrime(n) and p * q * r == n:
            if n.bit_length() < 1024:
                self.send(b"[+] It's 2021 now,young man.")
                self.send(b'[!] Go away!')
                self.request.close()
                return

            m = int.from_bytes(flag, 'big')
            self.send(b"[+] here is your flag %d" % pow(m, 0x10001, n))
            self.request.close()
            return
        else:
            self.send(b"[+] mission impossible. CIA needed.")
            self.send(b'[!] Go away!')

        self.request.close()
        return


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 22354
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
