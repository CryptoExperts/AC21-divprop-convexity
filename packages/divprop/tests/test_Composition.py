import logging

from divprop import Sbox, SboxDivision, DivCore_StrongComposition

from test_sboxes import get_sboxes

logging.basicConfig(level="DEBUG")


def test_DPPT():
    for name, sbox, n, m, dppt in get_sboxes():
        check_one_DPPT(sbox, n, m, dppt)


def check_one_DPPT(sbox, n, m, dppt):
    assert len(sbox) == 2**n
    assert 0 <= max(sbox) < 2**m
    if n != m:
        return
    DCS = DivCore_StrongComposition(n, m, m, sbox, sbox)
    DCS.process_logged(64)
    # for lst in DCS.current:
    #     print(lst, lst.to_Bins())
    # print()
    res = DCS.divcore
    print(res)
    print()

    id = list(range(2**n))
    test1 = DivCore_StrongComposition(n, n, n, id, sbox)
    test2 = DivCore_StrongComposition(n, n, n, sbox, id)
    test1.process()
    test2.process()
    ans = SboxDivision(Sbox(sbox, n, m))
    assert test1.divcore == test2.divcore == ans.divcore

    test = DivCore_StrongComposition(n, n, n, sbox, sbox)
    test.set_keys([0])
    test.process()
    sbox2 = [sbox[y] for y in sbox]
    ans = SboxDivision(Sbox(sbox2, n, m))
    assert test.divcore == ans.divcore


if __name__ == '__main__':
    test_DPPT()
