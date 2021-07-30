import random
from mt19937predictor import MT19937Predictor
from pwn import *
# context(log_level = 'debug')

p = remote('10.212.25.14', 22355)
predictor = MT19937Predictor()

p.recvuntil('s play a game.')

res = []
for i in range(312):
    p.recvuntil('er:')
    p.sendline('0')
    p.recvuntil('is ')
    res.append(int(p.recvuntil('\n')[:-1]))

for i in range(312):
    x = res[i]
    predictor.setrandbits(x, 64)
for i in range(200):
    i = predictor.getrandbits(64)
    p.recvuntil('your number:')
    p.sendline(str(i))

p.interactive()