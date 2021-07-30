import os
import random
import sys

with open("./flag", "rb")as f:
    flag = f.read()

MENU = \
'''
let's play a game
'''

def game():
    count = 0
    random.seed(os.urandom(32))
    print("play a game with me!")
    for i in range(512):
        number = random.getrandbits(64)
        guess = int(input("your number:"))
        if guess == number:
            count += 1
            print("win")
        else:
            print(f"lose!my number is {number}\n")
    
    if count >= 200:
        print(flag)


while True:
    print(MENU)
    game()
    sys.exit(1)
