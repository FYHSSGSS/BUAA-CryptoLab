from z3 import *
from ClassicalCrypto import l2n, HillEncrypt


def HillAttack(n, msg, cipher):
    assert len(msg) == len(cipher) and len(msg) % n == 0
    solver = Solver()
    for i in range(n):
        for j in range(n):
            unknown = 'x' + str(i) + str(j)
            command = unknown + '=Int(\'' + unknown + '\')'
            print(command)
            exec(command)

    buf1 = ''
    buf2 = ''
    for (c1, c2) in zip(msg, cipher):
        buf1 += c1
        buf2 += c2
        if len(buf1) == n:
            X = []
            Y = []
            for ch1, ch2 in zip(buf1, buf2):
                X.append(l2n(ch1))
                Y.append(l2n(ch2))
            for i in range(n):
                command = 'solver.add(('
                for j in range(n):
                    unknown = 'x' + str(j) + str(i) + '*' + str(X[j])
                    command += unknown
                    if j != n - 1:
                        command += '+'
                command += ') % 26 == ' + str(Y[i]) + ')'
                eval(command)
                print(command)
            buf1 = ''
            buf2 = ''
    mat = [([0] * n) for i in range(n)]
    print("as")
    if solver.check() == sat:
        m = solver.model()
        for c in m:
            j, i = int(str(c)[-2]), int(str(c)[-1])
            mat[j][i] = ((int(str(m[c]))) + 26) % 26
    assert HillEncrypt(mat, msg)[0:len(msg)] == cipher
    return mat

if __name__ == "__main__":
    print(HillAttack(2, "youarepretty", "kqoimjvdbokn"))
    print(HillAttack(3, "youaresocute", "ywwpcwsogfuk"))
'''
solver.add(a * b == 3)
(x00*x0+x10*x1)%26=y0
(x01*x0+x11*x1)%26=y1

if solver.check() == sat:
    m = solver.model()
    print(m)
'''
