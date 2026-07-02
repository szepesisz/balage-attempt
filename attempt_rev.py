"""
Semmi extra, de most programoztam icipicit a kutatáshoz (sajnos nem lett belőle pozitív eredmény), s gondoltam elküldöm.
Az a feladat, hogy A + 2A - 3A = 6 -nak van-e megoldása speckó halmazokra
(ez azt jelenti, hogy a_1 + 2 * a_2 - 3 * a_3 , ahol a_1,a_2,a_3 \in A) bizonyos A halmazokra.
Még annyi, hogy előzetes dolgok miatt nem lehet A-ban a,a+2 , a,a+3 , a,a+6. 

És ezeket az A-kat nézi meg egészen szabadon módosíthatóan
(nincs jól beépítve, ha hasznosabb lett volna, akkor megszépíthettem volna akár).
Szóval az lett volna a cél, hogy 9-elemű ilyen A-kra, de sajni 13-ra működik csak, amit eddig is tudtunk.
Ebben a formában, amiben küldöm azt print-eli ki, hogy mi az a 2 (borzalmas, hogy van ez a 2,
ha nem lenne ez a kettő, akkor lenne egy "új" becslésünk)
Nem izgi, meg nem a legjobban dokumentált, meg nincs benne a háttér, de gondoltam elküldöm 😁
"""


from itertools import combinations, product, permutations

S_0 = list(range(0, 42, 3))
S_1 = list(range(1, 42, 3))
S_2 = list(range(2, 42, 3))
S = [S_0,S_1,S_2]

FORBIDDEN_WITHIN = {3, 6}
FORBIDDEN_GLOBAL = {2, 3, 6}

def good_36(subset):
    # Check that subset has no difference 3 or 6
    subset = sorted(subset)
    m = len(subset)-1
    for i in range(m):
        if subset[i+1] - subset[i] in FORBIDDEN_WITHIN:
                return False
    return True

def good_2(subset):
    # Check that subset has no difference 2
    m = len(subset)-1
    for i in range(m):
        if subset[i+1] - subset[i] == 2:
                return False
    return True

def good_global(subset):
    # Check that subset has no difference satisfies A + 2A - 3A = 6
    for a, b, c in product(subset, repeat=3):
        if a + 2*b - 3*c == 6:
             return False
    return True

# Create lists for each Si
valid = {}

for i, Si in enumerate(S):
    # k = 0 → empty set
    valid[f"S{i}_0_valid"] = [()]

    # k = 1 → singletons
    valid[f"S{i}_1_valid"] = [(x,) for x in Si]

    # k = 2,3,4,5 → filtered subsets
    for k in [2, 3, 4, 5]:
        valid[f"S{i}_{k}_valid"] = [
            T for T in combinations(Si, k)
            if good_36(T)
        ]

# Valid pairs for 9
pairs = [[5,5,2], [5,4,3], [4,4,4]]
violating = []

for triple in pairs:
    for i, j, k in set(permutations(triple)):

        for e1 in valid[f"S0_{i}_valid"]:
            for e2 in valid[f"S1_{j}_valid"]:
                for e3 in valid[f"S2_{k}_valid"]:

                    testset = list(e1) + list(e2) + list(e3)
                    testset = sorted(testset)

                    if good_2(testset) and good_global(testset):
                        violating.append(testset)

print(violating)
