from binteger import Bin

from subsets.subsets import DenseSet


def Quine_McCluskey_Step1(P: DenseSet, n=None):
    """
    See https://doi.org/10.13154/tosc.v2020.i3.327-361 .
    Reformulation of Quine-McCluskey algorithm in two parts:
    1. finding all subsets of (P) of the form (a xor LowerSet(u))
       with maximal (u).
    2. finding a good / optimal covering of P with such subsets

    This method does part 1 in the framework of dense sets.

    Complexity: n 2^n |P|
    """
    if n is None:
        assert isinstance(P, DenseSet), "n must be given or P must be a DenseSet"
        n = P.n

    S = []
    for a in P:
        a = Bin(a, n).int

        # TBD: do in place and return orig P
        X = P.copy()
        X.do_Not(a)
        X.do_Complement()
        X.do_UpperSet()
        X.do_Complement()
        X.do_MaxSet()
        X.do_UnsetUp(a)
        for u in X:
            S.append((a, u))
    return S
