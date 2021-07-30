# !/usr/bin/env python3
import socketserver
import signal
import string
import random
import os

flag = 'flag{2words_to_describe_y0u:DUGUAI}'
MENU = br'''I often say that in those days, Chen Dao zai can win 37 million yuan with 20 yuan, I  win 5 million yuan with 200,000 yuan is not a problem.
so, let's play a game.
'''

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
        count = 0
        random.seed(os.urandom(32))
        self.send(MENU, newline=False)
        for i in range(512):
            number = random.getrandbits(64)
            self.send(b"[+] plz input your number: ")
            guess = int(self.recv().strip().decode())
            if guess == number:
                count += 1
                self.send(b'[!] NB!')
            else:
                self.send(b'[!] lose!my number is %d' % number)
        if count >= 200:
            self.send(flag.encode())
        else:
            self.send(b'[!] Go away!')
        self.request.close()
        return


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 22355
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
