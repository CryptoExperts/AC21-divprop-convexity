from tempfile import NamedTemporaryFile

from subsets import DenseSet, DenseBox


def test_DenseBox():
    d = DenseBox([2, 3, 4])
    assert d.data.n == 3*4*5

    d.set(d.pack([1, 0, 3]))
    d.set(d.pack([0, 2, 2]))
    assert d.get(d.pack([1, 0, 3])) == d.get([1, 0, 3]) == d.get((1, 0, 3)) == 1
    assert d.get(d.pack([0, 2, 2])) == d.get([0, 2, 2]) == d.get((0, 2, 2)) == 1
    assert d.get(d.pack([0, 0, 2])) == d.get([0, 0, 2]) == d.get((0, 0, 2)) == 0
    assert d.get(d.pack([0, 0, 0])) == d.get([0, 0, 0]) == d.get((0, 0, 0)) == 0

    assert d.pack([1, 0, 3]) in d
    assert d.pack([0, 0, 0]) not in d
    assert [1, 0, 3] in d
    assert [0, 0, 0] not in d

    assert d.info() == \
        "<DenseBox(2,3,4) hash=881718e8de88c276 wt=2 | 4:2>", d.info()

    d.do_LowerSet()

    assert d.info() == \
        "<DenseBox(2,3,4) hash=73e8ad231ea8609f wt=14 | 0:1 1:3 2:4 3:4 4:2>", d.info()

    d.do_MaxSet()

    assert d.info() == \
        "<DenseBox(2,3,4) hash=881718e8de88c276 wt=2 | 4:2>", d.info()

    with NamedTemporaryFile() as f:
        d.save_to_file(f.name)
        d2 = DenseBox.load_from_file(f.name)
        assert d2 == d

    assert d.to_DenseSet().get_support() == (
        0b00_011_0011,
        0b00_011_0101,
        0b00_011_0110,
        0b00_011_1001,
        0b00_011_1010,
        0b00_011_1100,
        0b00_101_0011,
        0b00_101_0101,
        0b00_101_0110,
        0b00_101_1001,
        0b00_101_1010,
        0b00_101_1100,
        0b00_110_0011,
        0b00_110_0101,
        0b00_110_0110,
        0b00_110_1001,
        0b00_110_1010,
        0b00_110_1100,
        0b01_000_0111,
        0b01_000_1011,
        0b01_000_1101,
        0b01_000_1110,
        0b10_000_0111,
        0b10_000_1011,
        0b10_000_1101,
        0b10_000_1110,
    )

    d.empty()

    d.add((1, 3, 2))

    assert d.to_DenseSet().get_support() == (
        0b01_111_0011,
        0b01_111_0101,
        0b01_111_0110,
        0b01_111_1001,
        0b01_111_1010,
        0b01_111_1100,

        0b10_111_0011,
        0b10_111_0101,
        0b10_111_0110,
        0b10_111_1001,
        0b10_111_1010,
        0b10_111_1100,
    )

    d.add((1, 0, 2))

    assert d.to_DenseSet().get_support() == (
        0b01_000_0011,
        0b01_000_0101,
        0b01_000_0110,
        0b01_000_1001,
        0b01_000_1010,
        0b01_000_1100,

        0b01_111_0011,
        0b01_111_0101,
        0b01_111_0110,
        0b01_111_1001,
        0b01_111_1010,
        0b01_111_1100,

        0b10_000_0011,
        0b10_000_0101,
        0b10_000_0110,
        0b10_000_1001,
        0b10_000_1010,
        0b10_000_1100,

        0b10_111_0011,
        0b10_111_0101,
        0b10_111_0110,
        0b10_111_1001,
        0b10_111_1010,
        0b10_111_1100,
    )

    d = DenseSet(5)
    d.add(0b01011)

    db = DenseBox([2, 3])
    assert d.to_DenseBox([2, 3]).get_support() == (
        db.pack([1, 2]),
    )


if __name__ == '__main__':
    test_DenseBox()
