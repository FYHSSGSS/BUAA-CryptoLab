from ClassicalCrypto import AffineDecrypt, l2n, SimpleReplaceEncrypt
import wordninja

dict = {'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253,
        'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094,
        'i': 0.06996, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
        'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929,
        'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
        'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150,
        'y': 0.01974, 'z': 0.00074
        }

common_word = []
d_order = {}
def getword():
    global d_order
    d_order = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    file = open('words.txt')
    for line in file:
        common_word.append(line.strip().split()[-1])
    # print(d_order)
    return

def getFrequency(text):
    global dict_sorted
    chList = list(text)
    Set = set(chList)
    Dict = {}
    for i in Set:
        Dict[i] = chList.count(i)

    dict_sorted = sorted(Dict.items(), key=lambda x: x[1], reverse=True)
    frequency_list = []
    print("char", "times", "frequency")
    for i in dict_sorted:
        print(i[0], "\t", i[1], "\t", i[1] / len(text))
        frequency_list.append(i[0])
    return dict_sorted


def caesar(dict_sorted, text):
    most_ch = ['e', 't', 'a', 'o']
    for ch in most_ch:
        dis = l2n(dict_sorted[0][0]) - l2n(ch)
        temp_text = AffineDecrypt(1, dis, text)
        print(temp_text)


def fuzzReplace(dict_sorted, text):
    fuzz = [0] * 26
    global d_order
    print(d_order)
    for j in range(min(len(dict_sorted), len(d_order))):
        pos1 = d_order[j][0]
        pos2 = dict_sorted[j][0]
        fuzz[l2n(pos2)] = pos1
    print(fuzz)
    print(dict_sorted)
    for i in range(len(fuzz)):
        if fuzz[i] == 0:
            fuzz[i] = 'a'
    print(SimpleReplaceEncrypt(fuzz, text))


if __name__ == "__main__":
    getword()
    file = open('Caesar.txt')
    text = file.read()
    getFrequency(text)
    caesar(dict_sorted,text)
    # fuzzReplace(dict_sorted, text)
