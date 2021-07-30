# !/usr/bin/env python3
import socketserver
from sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from os import urandom
from binascii import hexlify, unhexlify
from hashlib import *
import random
import string
import signal
flag = "flag{efb55e10-c25d-4a23-9f1d-22184129748d}"

class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 1024
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

    def recv(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self._recvall()

    def encrypt1(self, key, pt):
        cipher = CryptSM4()
        cipher.set_key(key, SM4_ENCRYPT)
        ct = cipher.crypt_ecb(pt)
        return ct

    def encrypt2(self, key, pt, r, f, p):
        cipher = CryptSM4()
        cipher.set_key(key, SM4_ENCRYPT)
        ct = cipher.crypt_ecb(pt, r, f, p)
        return ct

    def decrypt(self, key, ct):
        cipher = CryptSM4()
        cipher.set_key(key, SM4_DECRYPT)
        pt = cipher.crypt_ecb(ct)
        return pt

    def handle(self):
        signal.alarm(600)
        try:
            key = urandom(16)
            self.send(b"your flag is")
            self.send(hexlify(self.encrypt1(key, flag.encode())))
            while True:
                self.send(b"1.encrypt1\n2.encrypt2\n3.decrypt\n")
                choice = self.recv()
                if choice == b'1' or choice == b'encrypt1':
                    self.send(b"your plaintext in hex", False)
                    pt = self.recv(prompt=b":")
                    ct = self.encrypt1(key, unhexlify(pt))
                    self.send(b"your ciphertext in hex:" + hexlify(ct))
                elif choice == b'2' or choice == b'encrypt2':
                    self.send(b"your plaintext in hex", False)
                    pt = self.recv(prompt=b":")
                    self.send(b"give me the value of r f p", False)
                    tmp = self.recv(prompt=b":")
                    r, f, p = tmp.split(b" ")
                    r = int(r) % 0x20
                    f = int(f) % 0xff
                    p = int(p) % 16
                    ct = self.encrypt2(key, unhexlify(pt), r, f, p)
                    self.send(b"your ciphertext in hex:" + hexlify(ct))
                elif choice == b'3' or choice == b'decrypt':
                    self.send(b"your key in hex", False)
                    key = self.recv(prompt=b":")
                    self.send(b"your ciphertext in hex", False)
                    ct = self.recv(prompt=b":")
                    pt = self.decrypt(unhexlify(key), unhexlify(ct))
                    self.send(b"your plaintext in hex:" + hexlify(pt))
                else:
                    self.send(b"choose another command.")
        except:
            pass

class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 23367
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()


