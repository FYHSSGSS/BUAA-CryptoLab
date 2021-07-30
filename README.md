# BUAA-CryptoLab
BUAA-Cryptolab,consists of some basic crypto algorithm and some baby exploit scripts.

## description

- lab1

  Lab1 includes some basic arithmetic functions which we learned in AITMC.For instance,exCRT,miller-Rabin prime test,print all primes within $5\times 10^{10}$​ by sieve of Euler and bitset.Some of them were written in `CryptoLab.py`.

- lab2

  $GF(2^8)$​ Galois field's operations.

- lab3

  classical cryptography

- lab4

  DES & some optimization of DES from speed and safety.

- lab5

  AES & the generation of SBOX.

- lab6

  Block cipher's working pattern by SM4,contained ECB,CBC,CTR,CFB,and also padding oracle attack to CBC mode.

- lab7

  Lab7 is about stream cipher: BBS,RC4 and ZUC.

- lab8

  Lab8 is the big project1:Try to accelerate your encryption function.I choose to accelerate SM4,eventually,its speed is 1.06Gb/s.

- lab9

  Lab9 is about rsa and rsa's very classic attacking methods,like the wiener attack.

- lab10

  Lab10 is about elliptic curve,its arithmetic and encoding of messages in transit,Diffie Hellman demo and SM2 digital signature demo.

- lab11

  Lab11 is about hash,such as `SHA1.py`,`SM3.py`.It's very pity that I have no time to play with the second birthday attack. That sounds very intriguing.

- lab12

  Lab12 is the big project2.I choose the hacking part and helped the assistant to build 5 services on our school's CTFd. Here are those 5 services' code and dockerfile.

- lab13

  Lab13 is about digital signature.It contains 3 signature demos with 3 different algorithms.

the `flowchartgen.py` is used to generate a flowchart of the program.

## directory

```shell
.
├── ClassicalCrypto.py
├── CryptoLab.py
├── LICENSE
├── README.md
├── flowchartgen.py
├── lab1
│   ├── Miller_Rabin.py
│   ├── SieveOfEratosthenes.cpp
│   ├── SieveOfEuler.cpp
│   └── exCRT.py
├── lab2
│   └── poly.py
├── lab3
│   ├── DocDec.py
│   ├── DocEnc.py
│   └── HillAttack.py
├── lab4
│   ├── DES.py
│   ├── SPbox.py
│   ├── optDES.py
│   └── safeDES.py
├── lab5
│   ├── AES.py
│   └── SboxMaker.py
├── lab6
│   ├── SM4.py
│   ├── SM4SP.py
│   ├── SM4_working_pattern.py
│   ├── SM4oracle.py
│   ├── attack.py
│   └── data
│       ├── README.txt
│       ├── cipher-cbc
│       ├── cipher-cfb
│       ├── cipher-ctr
│       ├── cipher-ecb
│       ├── cipher-ofb
│       ├── message
│       └── ouput
├── lab7
│   ├── BBS.py
│   ├── RC4.py
│   └── ZUC.py
├── lab8
│   ├── main.c
│   ├── sm4
│   ├── sm4.c
│   └── sm4.h
└── lab9
│   └── rsa.py
├── lab10
│   ├── ECC.py
│   ├── SM2.py
│   └── SM3.py
├── lab11
│   └── SHA1.py
├── lab12
│   ├── des
│   │   ├── Dockerfile
│   │   └── desserver.py
│   ├── des.zip
│   ├── homo
│   │   ├── Dockerfile
│   │   ├── __pycache__
│   │   │   └── poly.cpython-38.pyc
│   │   ├── homoserver.py
│   │   └── poly.py
│   ├── prime
│   │   ├── Dockerfile
│   │   ├── prime.py
│   │   └── primeserver.py
│   ├── rand
│   │   ├── Dockerfile
│   │   ├── exp.py
│   │   └── randserver.py
│   ├── sm4
│   │   ├── Dockerfile
│   │   ├── func.py
│   │   ├── server.py
│   │   └── sm4.py
│   ├── sm4.zip
│   ├── 综合实验2-附件
│   │   ├── 6轮des差分攻击
│   │   │   └── server.py
│   │   ├── Miller-rabin
│   │   │   └── server.py
│   │   ├── sm4报错注入
│   │   │   ├── func.py
│   │   │   ├── sm4.py
│   │   │   └── task.py
│   │   ├── 同态加密
│   │   │   └── task
│   │   │       ├── __pycache__
│   │   │       │   └── poly.cpython-38.pyc
│   │   │       ├── poly.py
│   │   │       └── task.py
│   │   └── 随机数
│   │       └── task.py
│   └── 综合实验2-附件.7z
├── lab13
│   ├── RSA-PSS.py
│   ├── elgamal.py
    └── schnorr.py
```

## Maintainers

@FYHSSGSS
