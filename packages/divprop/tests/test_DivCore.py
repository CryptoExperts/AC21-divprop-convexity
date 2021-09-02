from collections import defaultdict
from functools import reduce
from random import shuffle, randrange

from binteger import Bin
from subsets import DenseSet

from divprop import Sbox, SboxDivision, SboxPeekANFs

from test_sboxes import get_sboxes

SboxDivision.CACHE = None


def test_DivCore():
    s = Sbox([1, 2, 3, 4, 0, 7, 6, 5], 3, 3)
    dc = SboxDivision(sbox=s)
    dc2_bins, ub2 = SboxPeekANFs(s).compute()
    assert set(dc.divcore.to_Bins()) == dc2_bins

    assert dc.divcore.info() == \
        "<DenseSet hash=dfa780cfc382387a n=6 wt=12 | 2:3 3:9>"
    assert dc.divcore.get_support() == \
        (7, 11, 12, 19, 20, 25, 35, 36, 42, 49, 50, 56)

    assert dc.invalid_max.info() == \
        "<DenseSet hash=9fe09c93bbcdbb87 n=6 wt=8 | 2:6 3:2>"
    assert dc.redundant_min.info() == \
        "<DenseSet hash=60f7fb1d9a638a50 n=6 wt=12 | 3:6 4:6>"
    assert dc.redundant_alternative_min.info() == \
        "<DenseSet hash=449b201e8a75f016 n=6 wt=10 | 3:8 4:2>"
    assert dc.full_dppt.info() == \
        "<DenseSet hash=b712d2af3b433a45 n=6 wt=43 | 0:1 1:3 2:10 3:13 4:12 5:3 6:1>"
    assert dc.min_dppt.info() == \
        "<DenseSet hash=ff7ce5b30da61490 n=6 wt=15 | 0:1 2:7 3:3 4:3 6:1>"

    assert dc.invalid_max.get_support() == \
        (3, 5, 6, 17, 26, 34, 41, 48)
    assert dc.redundant_min.get_support() == \
        (13, 14, 21, 22, 27, 37, 38, 43, 51, 57, 58, 60)
    assert dc.redundant_alternative_min.get_support() == \
        (13, 14, 21, 22, 26, 37, 38, 41, 51, 60)
    assert dc.full_dppt.get_support() == \
        (0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 18, 19, 20, 21, 22, 23, 27, 28, 29, 30, 31, 33, 35, 36, 37, 38, 39, 43, 44, 45, 46, 47, 51, 52, 53, 54, 55, 63)
    assert dc.min_dppt.get_support() == \
        (0, 9, 10, 12, 18, 20, 27, 28, 33, 36, 43, 44, 51, 52, 63)


def test_Not():
    a = DenseSet(10)
    a.set(0)
    assert a.get_support() == (0,)
    a.do_Not(1)
    assert a.get_support() == (1,)
    a.do_Not(2)
    assert a.get_support() == (3,)
    a.do_Not(512)
    assert a.get_support() == (515,)


def test_DPPT():
    for name, sbox, n, m, dppt in get_sboxes():
        sbox = Sbox(sbox, n, m)
        check_one_DPPT(sbox, n, m, dppt)
        check_one_relations(sbox, n, m)
        check_propagation_map(sbox)

    for n in range(4, 10):
        for i in range(5):
            m = n
            sbox = list(range(2**n))
            shuffle(sbox)
            sbox = Sbox(sbox, n, m)
            check_one_relations(sbox, n, m)

    for n in range(4, 8):
        for i in range(5):
            m = n + 1
            sbox = [randrange(2**m) for _ in range(2**n)]
            sbox = Sbox(sbox, n, m)
            check_one_relations(sbox, n, m)

            m = n + 4
            sbox = [randrange(2**m) for _ in range(2**n)]
            sbox = Sbox(sbox, n, m)
            check_one_relations(sbox, n, m)


def check_one_DPPT(sbox, n, m, dppt):
    assert len(sbox) == 2**n
    assert 0 <= max(sbox) < 2**m

    if dppt is not None:
        mindppt1 = set()
        for u, vs in enumerate(dppt):
            for v in vs:
                mindppt1.add((u << m) | v)
        mindppt1 = tuple(sorted(mindppt1))

    dc = SboxDivision(sbox=sbox)
    if dppt is not None:
        assert tuple(dc.min_dppt) == dc.min_dppt.get_support() == mindppt1
        assert len(dc.min_dppt) == dc.min_dppt.get_weight() == len(mindppt1)
        assert dc.full_dppt == dc.divcore.UpperSet().Not(dc.mask_u)

    reduntant = DenseSet(n+m)
    for uv in dc.divcore.to_Bins():
        u = uv[:n]
        v = uv[n:]
        for i in range(m):
            if v[i] == 0:
                ii = m - 1 - i
                reduntant.add((u.int << m) | int(v | (1 << ii)))
    assert dc.redundant_min == reduntant.MinSet()


def check_one_relations(sbox, n, m):
    dc = SboxDivision(sbox=sbox)

    mid = dc.min_dppt.Not(dc.mask_u)

    lb = dc.invalid_max
    ubr = dc.redundant_min
    ubc = dc.redundant_alternative_min

    assert ubr.UpperSet() <= ubc.UpperSet()
    assert not (ubr & mid)
    assert not (ubc & mid)

    assert form_partition(mid, lb.LowerSet() | ubc.UpperSet())
    assert form_partition(lb.LowerSet(), mid, ubr.UpperSet())

    assert ubr.UpperSet() == (mid.LowerSet() | lb.LowerSet()).Complement()
    assert ubc.UpperSet() == (mid.LowerSet()).Complement()

    assert len(ubr) <= m * len(dc.divcore)

    # print(
    #     "LB", len(lb),
    #     "UB", len(ubr),
    #     "UB'", len(ubc),
    #     "MinDPPT", len(dc.min_dppt),
    #     "FullDPPT", len(dc.full_dppt),
    # )
    # print("---")


def test_SboxDivision_from_divcore():
    for name, sbox, n, m, dppt in get_sboxes():
        sd1 = SboxDivision(Sbox(sbox, n, m))
        sd2 = SboxDivision.from_divcore(sd1.divcore, n, m)

        for attr in (
            "divcore", "lb", "ub", "minimal", "invalid_max", "redundant_min",
            "propagation_map", "min_dppt", "full_dppt"
        ):
            assert getattr(sd1, attr) == getattr(sd2, attr)


def form_partition(*sets):
    for s in sets:
        break
    return (
        reduce(lambda a, b: a | b, sets).is_full()
        and sum(map(len, sets)) == 2**s.n
    )


def test_peekanfs():
    for n in range(2, 13):
        n_iter = max(1, 2**11 // 2**n)
        for i in range(n_iter):
            m = n
            sbox = list(range(2**n))
            shuffle(sbox)
            sbox = Sbox(sbox, n, m)

            test1 = (
                set(SboxDivision(sbox).divcore.to_Bins()),
                set(SboxDivision(sbox).invalid_max.to_Bins()),
            )

            test2 = SboxPeekANFs(sbox).compute()
            assert test1 == test2
    print("OK")


def test_component_anf():
    for name, sbox, n, m, dppt in get_sboxes():
        if n >= 7:
            continue
        sbox = Sbox(sbox, n, m)
        if sbox.is_invertible():
            # test remark
            anfs_full = SboxDivision(~sbox).components_anf_closures(
                remove_dups_by_maxset=False,
                only_minimal=False,
            )

            assert len(anfs_full) == 2**m-1
            for mask in range(1, 2**m):
                f = DenseSet(m)
                for x, y in enumerate(sbox):
                    if Bin(x).scalar_bin(mask):
                        f.flip(y)
                f.do_Mobius()
                f.do_LowerSet()
                assert anfs_full[mask] == f

        anfs_full = SboxDivision(sbox).components_anf_closures(
            remove_dups_by_maxset=False,
            only_minimal=False,
        )
        for mask in range(1, 2**m):
            f = DenseSet(n)
            for x, y in enumerate(sbox):
                if Bin(y).scalar_bin(mask):
                    f.flip(x)
            f.do_Mobius()
            f.do_LowerSet()
            assert anfs_full[mask] == f

        maxterms1 = {tuple(anf.MaxSet()) for mask, anf in anfs_full.items()}

        anfs_full2 = SboxDivision(sbox).components_anf_closures(
            remove_dups_by_maxset=True,
            only_minimal=False,
        )

        maxterms2 = {tuple(anf.MaxSet()) for mask, anf in anfs_full2.items()}
        assert maxterms1 == maxterms2


# ===========================================
# old code for division for comparison
# ===========================================


def check_propagation_map(sbox):
    mp1 = sbox_division(sbox, sbox.n, sbox.m)
    divcore = SboxDivision(sbox)
    mp2 = divcore.propagation_map
    print(mp1[0])
    print(mp2[0])
    assert tuple(mp1) == tuple(mp2)


def sbox_division(sbox, n, m):
    """
    Compute the reduced DPPT of n x m bit S-box
    Optimized a bit
    """
    assert 1 << n == len(sbox)
    assert max(sbox) < 1 << m

    by_k = defaultdict(set)
    # iterate over all products of coordinates
    for u in range(2**m):
        bf = [int(sbox[x] & u == u) for x in range(2**n)]
        vanf = anf(bf)
        # save the product mask per each monomial it generates
        for k, val in enumerate(vanf):
            if val:
                by_k[k].add(u)

    for k in by_k:
        by_k[k] = size_reduce_set_naive(by_k[k])

    by_hw = defaultdict(list)
    for x in range(2**n):
        by_hw[Bin(x).hw].append(x)

    # propagate info to "lower" monomials (at the input)
    # do in levels by HW
    for mask_hw in reversed(range(n + 1)):
        for mask in by_hw[mask_hw]:
            for bit in range(n):
                if mask & (1 << bit) == 0:
                    continue
                by_k[mask ^ (1 << bit)] |= by_k[mask]

    for k in by_k:
        by_k[k] = size_reduce_set_naive(by_k[k])

    return tuple(sorted(by_k[k]) for k in range(2**n))


def hw(x):
    return sum(map(int, bin(x)[2:]))


def covers(a, b):
    return a & b == b


def size_reduce_set_naive(kset):
    kset = sorted(kset, key=hw)
    i = 0
    while i < len(kset):
        top = []
        x = kset[i]
        for y in kset[i+1:]:
            if not covers(y, x):
                top.append(y)
        kset[i+1:] = top
        i += 1
    return set(kset)


def log2ceil(n):
    return int(n-1).bit_length()


def anf(arr):
    arr = list(arr)
    n = log2ceil(len(arr))
    assert len(arr) == 2**n, len(arr)
    for k in range(n):
        halfstep = 1 << k
        step = 2 << k
        for i in range(0, len(arr), step):
            for j in range(0, halfstep):
                arr[i + j + halfstep] ^= arr[i + j]
    return arr


if __name__ == '__main__':
    test_DivCore()
    test_DPPT()
    test_peekanfs()
    print("Ok!")
