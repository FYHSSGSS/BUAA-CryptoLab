#!/usr/bin/env python3

flag = open("./flag", "rb").read()


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


def get_flag():
    try:
        p = int(input("give me your P:"))
        q = int(input("give me your Q:"))
        r = int(input("give me your R:"))
        n = int(input("give me your N:"))
        if isPrime(p) and isPrime(q) and isPrime(r) and isPrime(n) and p * q * r == n:
            if n.bit_length() < 1024:
                print("It's 2021 now,young man.")
                return
            m = int.from_bytes(flag, 'big')
            print("here is your flag %d" % pow(m, 0x10001, n))
        else:
            print("mission impossible. CIA needed")
        return
    except:
        print("wrong")
    return


if __name__ == "__main__":
    get_flag()
    exit(1)
