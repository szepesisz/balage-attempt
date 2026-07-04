"""
Az a feladat, hogy A + 2A - 3A = 6 -nak van-e megoldása speckó halmazokra
(ez azt jelenti, hogy a_1 + 2 * a_2 - 3 * a_3 , ahol a_1,a_2,a_3 \\in A) bizonyos A halmazokra.
Még annyi, hogy előzetes dolgok miatt nem lehet A-ban a,a+2 , a,a+3 , a,a+6.

És ezeket az A-kat nézi meg egészen szabadon módosíthatóan
(nincs jól beépítve, ha hasznosabb lett volna, akkor megszépíthettem volna akár).
Szóval az lett volna a cél, hogy 9-elemű ilyen A-kra, de sajni 13-ra működik csak, amit eddig is tudtunk.
Ebben a formában, amiben küldöm azt print-eli ki, hogy mi az a 2 (borzalmas, hogy van ez a 2,
ha nem lenne ez a kettő, akkor lenne egy "új" becslésünk)
"""

from collections.abc import Iterable
from functools import partial
from itertools import chain, combinations, pairwise, permutations, product

S_0 = list(range(0, 42, 3))
S_1 = list(range(1, 42, 3))
S_2 = list(range(2, 42, 3))
S = [S_0, S_1, S_2]

FORBIDDEN_WITHIN = {3, 6}
FORBIDDEN_GLOBAL = {2, 3, 6}


def good(subset: Iterable[int], frbdn: set):
    """
    Check that subset has no difference in frbdn
    """
    return all(v1 - v0 not in frbdn for v0, v1 in pairwise(sorted(subset)))


good_36 = partial(good, frbdn=FORBIDDEN_WITHIN)
good_2 = partial(good, frbdn={2})


def good_global(subset: Iterable[int]):
    """
    Check that subset has no difference satisfies A + 2A - 3A = 6
    """
    return all(a + 2 * b - 3 * c != 6 for a, b, c in product(subset, repeat=3))


# Create lists for each s_i
valid = {}

for i, s_i in enumerate(S):
    # k = 0 → empty set
    valid[i, 0] = [()]

    # k = 1 → singletons
    valid[i, 1] = [(x,) for x in s_i]

    # k = 2,3,4,5 → filtered subsets
    for k in [2, 3, 4, 5]:
        valid[i, k] = [T for T in combinations(s_i, k) if good_36(T)]

# Valid pairs for 9
pairs = [[5, 5, 2], [5, 4, 3], [4, 4, 4]]
violating = []

for e1, e2, e3 in chain(
    *(
        product(valid[0, i], valid[1, j], valid[2, k])
        for i, j, k in set(chain(*map(permutations, pairs)))
    )
):
    testset = sorted(chain(e1, e2, e3))

    if good_2(testset) and good_global(testset):
        violating.append(testset)

print(violating)

# violating = [
#     testset
#     for e1, e2, e3 in chain(
#         *(
#             product(valid[0, i], valid[1, j], valid[2, k])
#             for i, j, k in set(chain(*map(permutations, pairs)))
#         )
#     )
#     if good_2(testset := sorted(chain(e1, e2, e3))) and good_global(testset)
# ]
# print(violating)
