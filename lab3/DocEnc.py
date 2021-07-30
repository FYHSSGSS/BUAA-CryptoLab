from random import shuffle, randint
from ClassicalCrypto import n2l, l2n, SimpleReplaceEncrypt


def Caesar(msg):
    b = randint(1, 26)
    cipher = "".join([n2l((l2n(c) + b) % 26) for c in msg])
    with open("Caesar.txt", 'w') as fout:
        fout.write(cipher)


def SimpleReplace(msg):
    array = [n2l(c) for c in range(26)]
    shuffle(array)
    cipher = SimpleReplaceEncrypt(array, msg)
    with open("SimpleReplace.txt", 'w') as fout:
        fout.write(cipher)


punc = ' ~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}'
if __name__ == "__main__":
    with open("article.txt", 'r') as fin:
        msg = fin.readline()
    msg = msg.lower()
    for c in punc:
        msg = msg.replace(c, "")
    Caesar(msg)
    SimpleReplace(msg)
