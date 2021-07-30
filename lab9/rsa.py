from CryptoLab import getPrime, invmod, CRT,getStrongPrime
from libnum import *
from random import randint
# from gmpy2 import *

# p = getStrongPrime
p = 179576248552484923459628840857751797431548554686666619106711264699949252218122479246291018525624002389192622702303417031679905549654823396084463237591495583942933491121437747884506770683391897806997141502111836734425848558609972891838129894267819793344855466260376720959454244794283168112985588476927546936451
# q = getStrongPrime
q = 98841128586929019142599180892569441012327744233269284437305189300598621989227304871532779846414668684060913839296402017024610877416894733903531123681222547779636919348647384011082240754859946762793634888381263621522898878374706397456346355816020052967812919356305694183465422435207225951922678096075744217629
N = p * q
# e = 284100478693161642327695712452505468891794410301906465434604643365855064101922252698327584524956955373553355814138784402605517536436009073372339264422522610010012877243630454889127160056358637599704871937659443985644871453345576728414422489075791739731547285138648307770775155312545928721094602949588237119345
# N = 468459887279781789188886188573017406548524570309663876064881031936564733341508945283407498306248145591559137207097347130203582813352382018491852922849186827279111555223982032271701972642438224730082216672110316142528108239708171781850491578433309964093293907697072741538649347894863899103340030347858867705231
# c = 225959163039382792063969156595642930940854956840991461420767658113591137387768433807406322866630268475859008972090971902714782079518283320987088621381668841235751177056166331645627735330598686808613971994535149999753995364795142186948367218065301138932337812401877312020570951171717817363438636481898904201215

def encrypt(m, e, N):
    return pow(m, e, N)


def decrypt(c, e, p, q):
    phi = (p - 1) * (q - 1)
    d = invmod(e, phi)
    item = [(pow(c % p, d % (p - 1), p), p), (pow(c % q, d % (q - 1), q), q)]
    ans = CRT(item)
    assert ans == pow(c, d, p * q)
    return ans


def hackN(e, d, N):
    t = d * e - 1
    r = 0
    while (t & 1) == 0:
        r += 1
        t >>= 1
    for i in range(10):
        a = randint(1, 65536) % (N - 2) + 2
        x = (pow(a, t, N) - 1 + N) % N
        if gcd(N, x) != 1 and gcd(N, x) != N:
            return (gcd(N, x), N // gcd(N, x))
        for i in range(r):
            x = x * x % N
            tmp = (x + 1) % N
            if gcd(N, tmp) != 1 and gcd(N, tmp) != N:
                return (gcd(N, tmp), N // gcd(N, tmp))
    return "Failed"


def ContinuedFraction(x, y):
    res = []
    while y:
        res.append(x // y)
        x, y = y, x % y
    return res


def calc(seq):
    num, den = 1, 0
    for i in seq[::-1]:
        den, num = num, i * num + den
    return (den, num)

def solve(a, b, c):
    delta = gmpy2.iroot(b ** 2 - 4 * a * c, 2)[0]
    x1, x2 = (-b - delta) // (2 * a), (-b + delta) // (2 * a)
    return x1, x2

def wienerAttack(N, e):
    res = ContinuedFraction(e, N)
    res = list(map(calc, (res[0:i] for i in range(1, len(res)))))
    for (d, k) in res:
        if k == 0:
            continue
        elif (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k
        x1, x2 = solve(1, N - phi + 1, N)
        if x1 * x2 == N:
            return abs(int(x1)), abs(int(x2))
    return "Failed"


if __name__ == "__main__":
    msg = s2n("flag{sadsd}")
    c = encrypt(msg, 65537, N)
    print(n2s(decrypt(c, 65537, p, q)))
    N = 3473368149650603148803248362859305810616830384713657576189830461663272229290941849749535852215753586078339602564703534544019270264758123888720790402066935128355365198517106201587833213985641081363529915405154534421955067011239544160379626647436269174669982624065257106974978034397237801426486327072733866941256103866379494352699331703600225626341270638466960870963368915890428723335452705666327012968661441098599531507370330709071561749402190081263005751377060766912253160596080441317443444238137527565995930091079370074820236433361851170139013408559792217741431999167452032312421940893219990759342422335291584922679
    d = 1162152933236773514914592216622348563638949855440454755797345047276381791108713747673952456892855099188638949067531609708733304215414439791749233134512164937280871081573509693584051859503442904498824846804159919294515017614820036381720317578237980231963064818049391303259949621408710049432839345408714287109345398814512462890065142333990159447216394268072867586567865841287731904542012092589440889131990826657294780274422404008400777545284141318433828812877026565204852346034671074895135016040661630824182518645904726697790893178433416235613878827124199015085219721368430257092776492449477981215171599784246139064769
    p, q = hackN(65537, d, N)
    print(65537 * d % ((p - 1) * (q - 1)))
    m = 9374184159784028425756101620350784600486804400715517237475677725076455357396053693993984723139778862028803709896515312149918108551969467212768801532800183907107127769129242010964472729279257740792330468855162194822086765920270332759022649879700975455382260017445363866272891076388079436620719325537954072537533089276337973858671673730524684121864746690126015316199064265789566060767470309804765533109121672187527846765179467965243234591112201963007085351954016137212468860511159467096530163770349280735657260150846577147204198628696740820245501500830404117139929734729510006170408481842786820083482462160083179979452 % N
    print(m)
    s = pow(m, d, N)
    m_ = pow(s, 65537, N)
    print(m_)
    # p, q = wienerAttack(N, e)
    # print(n2s(decrypt(c, e, p, q)))