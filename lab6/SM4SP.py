Sbox = [[214, 144, 233, 254, 204, 225, 61, 183, 22, 182, 20, 194, 40, 251, 44, 5],
        [43, 103, 154, 118, 42, 190, 4, 195, 170, 68, 19, 38, 73, 134, 6, 153],
        [156, 66, 80, 244, 145, 239, 152, 122, 51, 84, 11, 67, 237, 207, 172, 98],
        [228, 179, 28, 169, 201, 8, 232, 149, 128, 223, 148, 250, 117, 143, 63, 166],
        [71, 7, 167, 252, 243, 115, 23, 186, 131, 89, 60, 25, 230, 133, 79, 168],
        [104, 107, 129, 178, 113, 100, 218, 139, 248, 235, 15, 75, 112, 86, 157, 53],
        [30, 36, 14, 94, 99, 88, 209, 162, 37, 34, 124, 59, 1, 33, 120, 135],
        [212, 0, 70, 87, 159, 211, 39, 82, 76, 54, 2, 231, 160, 196, 200, 158],
        [234, 191, 138, 210, 64, 199, 56, 181, 163, 247, 242, 206, 249, 97, 21, 161],
        [224, 174, 93, 164, 155, 52, 26, 85, 173, 147, 50, 48, 245, 140, 177, 227],
        [29, 246, 226, 46, 130, 102, 202, 96, 192, 41, 35, 171, 13, 83, 78, 111],
        [213, 219, 55, 69, 222, 253, 142, 47, 3, 255, 106, 114, 109, 108, 91, 81],
        [141, 27, 175, 146, 187, 221, 188, 127, 17, 217, 92, 65, 31, 16, 90, 216],
        [10, 193, 49, 136, 165, 205, 123, 189, 45, 116, 208, 18, 184, 229, 180, 176],
        [137, 105, 151, 74, 12, 150, 119, 126, 101, 185, 241, 9, 197, 110, 198, 132],
        [24, 240, 125, 236, 58, 220, 77, 32, 121, 238, 95, 62, 215, 203, 57, 72]]


def shift(num, pos):
    return ((num << pos) | (num >> (32 - pos))) & 0xffffffff

def div(n):
    return [n >> 96, (n >> 64) & 0xffffffff, (n >> 32) & 0xffffffff, n & 0xffffffff]


def rebuild(state):
    res = 0
    for i in range(4):
        res <<= 32
        res |= state[i]
    return res


def SboxReplace(a):
    return Sbox[a >> 4][a & 0xf]


def pbox(n):
    a = [n >> 24, (n >> 16) & 0xff, (n >> 8) & 0xff, n & 0xff]
    b = list(map(SboxReplace, a))
    n = (b[0] << 24) + (b[1] << 16) + (b[2] << 8) + b[3]
    return n ^ shift(n, 2) ^ shift(n, 10) ^ shift(n, 18) ^ shift(n, 24)

def ppbox(n, i):
    a = [n >> 24, (n >> 16) & 0xff, (n >> 8) & 0xff, n & 0xff]
    a[i] = SboxReplace(a[i])
    x = (a[0] << 24) + (a[1] << 16) + (a[2] << 8) + a[3]
    return x ^ shift(x, 2) ^ shift(x, 10) ^ shift(x, 18) ^ shift(x, 24)

dict1 = []
dict2 = []
dict3 = []
dict4 = []

def pp(n):
    a, b, c, d = [n >> 24, (n >> 16) & 0xff, (n >> 8) & 0xff, n & 0xff]
    return dict1[a] ^ dict2[b] ^ dict3[c] ^ dict4[d]

if __name__ == '__main__':
    for i in range(256):
        dict1.append(ppbox(i << 24, 0))
        dict2.append(ppbox(i << 16, 1))
        dict3.append(ppbox(i << 8, 2))
        dict4.append(ppbox(i, 3))
    print(list(map(hex, dict1)))
    print(list(map(hex, dict2)))
    print(list(map(hex, dict3)))
    print(list(map(hex, dict4)))
    import random
    while True:
        a = random.getrandbits(32)
        assert pp(a) == pbox(a)
