import time
import ctypes
import pickle
from random import randrange, shuffle
from tempfile import NamedTemporaryFile

from binteger import Bin

from subsets import DenseSet, BitSet


def assert_raises(f, err=RuntimeError):
    try:
        f()
    except err as e:
        print("exception good:", e)
    else:
        assert 0, f"exception {err} not raised"


def test_DenseSet():
    a = DenseSet(3)  # 3-bit vectors
    a.add(1)
    a.add(5)
    a.add(7)
    assert a.get_support() == (1, 5, 7)

    b = DenseSet(3, (2, 3, 4, 5))
    b.set(5)
    b.set(4, 0)
    assert b.get_support() == (2, 3, 5)

    a |= b

    assert a.get_support() == (1, 2, 3, 5, 7)

    for itr in range(100):
        a.resize(randrange(3, 7))
        assert a.get_support() == (1, 2, 3, 5, 7)
    a.resize(6)

    b = a.copy()
    b.set(0, 1)
    b.set(7, 0)
    b.set(8)
    a.set(3, 0)
    a.set(4, 1)
    assert a.get_support() == (1, 2, 4, 5, 7)
    assert b.get_support() == (0, 1, 2, 3, 5, 8)
    assert b.get_weight() == 6

    assert b.info() == '<DenseSet hash=f01a3338f076a640 n=6 wt=6 | 0:1 1:3 2:2>'
    assert DenseSet(6, [1, 2, 4, 5, 7]) == a

    assert_raises(
        lambda: DenseSet(2, [1, 2, 4, 5, 7])
    )
    assert_raises(
        lambda: a.save_to_file("/NON-EXISTENT STUFF")
    )

    a = DenseSet(4)
    a.set(0b1100)
    assert a.LowerSet().get_support() == (0b0000, 0b0100, 0b1000, 0b1100)
    assert a.UpperSet().get_support() == (0b1100, 0b1101, 0b1110, 0b1111)
    # assert a.Complement() == ~a
    assert a.Complement().get_support() == \
        tuple(v for v in range(16) if v != 12)
    a.set(0b0110)
    assert a.LowerSet().get_support() == (
        0b0000,
        0b0010,
        0b0100,
        0b0110,
        0b1000,
        0b1100,
    )
    assert a.UpperSet().get_support() == (
        0b0110,
        0b0111,
        0b1100,
        0b1101,
        0b1110,
        0b1111,
    )
    assert a.UpperSet().MinSet() == a
    assert a.LowerSet().MaxSet() == a

    assert a.LowerSet(2).get_support() == (
        0b0100,
        0b0110,
        0b1100,
    )
    assert a.UpperSet(2).get_support() == (
        0b0110,
        0b1100,
        0b1110,
    )

    a = DenseSet(3, [6, 7])
    assert a.Mobius().get_support() == (
        0b110,
    )

    # matches SageMath's

    d = DenseSet(3, [6, 7])
    assert d.WalshHadamard() == (4, 0, 4, 0, 4, 0, -4, 0)

    d = DenseSet(5, [1, 4, 9, 10, 13, 15, 16, 17, 18, 20, 21, 23, 24, 25])
    assert d.WalshHadamard() == (
        4, 4, -12, 4, -4, -4, -4, 12, -4, -4, -4, -4, 4, 4, 4,
        4, 4, 4, 4, 4, 4, 4, 4, 4, 12, -4, -4, -4, -4, 12, -4, -4,
    )


def test_save_load():
    for d in gen_densesets(maxn=8, maxnum=32):
        with NamedTemporaryFile() as f:
            d.save_to_file(f.name)
            assert d == DenseSet.load_from_file(f.name)


def test_properties():
    for a in gen_densesets(maxn=9):
        if a.n <= 6:
            X = a
            U = X.ParitySet()
            for u in range(2**X.n):
                test1 = int(u in U)
                test2 = 0
                for x in X:
                    if x & u == u:
                        test2 ^= 1
                assert test1 == test2

        assert a.ParitySet() == a.Not().Mobius().Not()

        assert a.LowerSet().Not() == a.Not().UpperSet()
        assert a.UpperSet().Not() == a.Not().LowerSet()
        assert a.MaxSet().Not() == a.Not().MinSet()
        assert a.MinSet().Not() == a.Not().MaxSet()

        assert a.LowerSet() == a.Not().UpperSet().Not()
        assert a.UpperSet() == a.Not().LowerSet().Not()
        assert a.MaxSet() == a.Not().MinSet().Not()
        assert a.MinSet() == a.Not().MaxSet().Not()

        assert a.UpperSet().MinSet() == a.MinSet()
        assert a.LowerSet().MaxSet() == a.MaxSet()
        assert a.MinSet().UpperSet() == a.UpperSet()
        assert a.MaxSet().LowerSet() == a.LowerSet()

        assert a.Mobius() <= a.ParitySet().MinSet().Not().LowerSet()
        assert a.Mobius() <= a.ParitySet().Not().LowerSet()
        assert a.Mobius() <= a.ParitySet().UpperSet().Not()
        assert a.Mobius().Not() <= a.ParitySet().UpperSet()
        assert a.Mobius().LowerSet() == a.ParitySet().UpperSet().Not()
        assert a.Mobius().LowerSet() >= a.ParitySet().UpperSet().Not()
        assert a.Mobius().Not().UpperSet() >= a.ParitySet()
        assert a.Mobius().LowerSet().Not() >= a.ParitySet()
        assert a.Mobius().LowerSet() >= a.ParitySet().Not()

        assert a.Mobius().LowerSet() == a.ParitySet().UpperSet().Not()

        assert a.Mobius() == a.Not().ParitySet().Not() <= a.ParitySet().Not().LowerSet()

        # "random" sets
        b = a
        for i in range(4):
            b = a ^ a.Mobius().Complement().Not().Mobius()
            assert (a == b) == (set(a) == set(b))
            assert (a != b) == (set(a) != set(b))
            assert (a < b) == (set(a) < set(b))
            assert (a > b) == (set(a) > set(b))
            assert (a <= b) == (set(a) <= set(b))
            assert (a >= b) == (set(a) >= set(b))
    print("prop ok")


def test_BouraCanteaut16_lemma3():
    """
    Lemma 3 from Boura-Canteaut CRYPTO'2016.
    1-to-1 correspondence between ANF coefficients
    of products of output bits of an S-box
    and ANF coefficients
    of products of output bits of the inverse:

    S^v contains x^u
    iff
    (~. S^{-1} .~)^(~u) contains x^{~v}

    (. denotes composition, i.e. inputs and outputs
    of the inverse of S are inverted)
    """
    for _ in range(5):
        for n in range(1, 8):

            sbox = list(range(2**n))
            shuffle(sbox)

            for _ in range(100):
                v = Bin(randrange(1, 2**n), n)
                iv = ~v
                u = Bin(randrange(1, 2**n), n)
                iu = ~u

                # F = sbox^v,
                # iF = (~.isbox.~)^~u,
                F = DenseSet(n)
                iF = DenseSet(n)
                for x, y in enumerate(sbox):
                    if y & v == v:
                        F.set(x)

                    ix = ~Bin(x, n)
                    iy = ~Bin(y, n)
                    if ix & iu == iu:
                        iF.set(iy.int)

                F.do_Mobius()
                iF.do_Mobius()
                # F contains x^u ?
                # iF contains x^~v ?
                assert F[u] == iF[iv]


def test_pickle():
    for d in gen_densesets(maxn=8):
        assert pickle.loads(pickle.dumps(d)) == d
        assert d.copy() == d


def test_bytes_byref():
    conv = BitSet._bytes_to_ctypes

    b = b"A" * (32 * 2**20)  # 32 MB

    t = time.time()
    test1 = conv(b)
    test2 = conv(b)
    assert time.time() - t < 0.5

    assert test1.value == test2.value


def mem_test():
    # mem test
    d = DenseSet(28)  # 64 MB
    d.fill()
    d.empty()

    for i in range(16 * 1000):
        print("itr", i)
        assert pickle.loads(pickle.dumps(d)) == d
        assert d.copy() == d


def gen_densesets(maxn, maxnum=512):
    for n in range(1, maxn+1):
        a = DenseSet(n)
        yield a
        for i in range(maxnum // 2):
            a.set(randrange(2**n))
            yield a
        for i in range(maxnum // 2):
            a = a ^ a.Mobius().Complement().Not().Mobius()
            yield a


if __name__ == '__main__':
    test_DenseSet()
    test_save_load()
    test_properties()
    test_pickle()
    # mem_test()
