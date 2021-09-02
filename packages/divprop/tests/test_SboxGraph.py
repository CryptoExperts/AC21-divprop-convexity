from divprop import Sbox


def test_Sbox():
    s = Sbox([1, 2, 3, 4, 0, 7, 6, 5], 3, 3)

    a = s.graph_dense()
    assert str(a) == "<DenseSet hash=b441a66a51d4a4f8 n=6 wt=8 | 1:2 2:1 3:2 4:1 5:2>"

    cs = s.coordinates()

    assert str(cs[0]) == "<DenseSet hash=3d139ee2d974e0e8 n=3 wt=4 | 2:3 3:1>"
    assert str(cs[1]) == "<DenseSet hash=53022f5ea743192d n=3 wt=4 | 1:2 2:2>"
    assert str(cs[2]) == "<DenseSet hash=5e0e6f8cfbc012e4 n=3 wt=4 | 0:1 1:1 2:1 3:1>"

    assert list(cs[0]) == [3, 5, 6, 7]
    assert list(cs[1]) == [1, 2, 5, 6]
    assert list(cs[2]) == [0, 2, 5, 7]

    qs = [s.coordinate_product(2**i) for i in range(3)][::-1]
    assert qs == list(cs)

    q3 = s.coordinate_product(3)
    assert list(q3) == [2, 5]
    q7 = s.coordinate_product(7)
    assert list(q7) == [5]


if __name__ == '__main__':
    test_Sbox()
