import logging

from itertools import product
from divprop import Sbox
from divprop.sandwich import Sandwich


log = logging.getLogger(__name__)


def precomp_multab(n, poly):
    tab = {}
    for a, b in product(range(2**n), repeat=2):
        key = a, b
        res = 0
        while a:
            if a & 1:
                res ^= b
            a >>= 1
            b <<= 1
            if b >> 4:
                b ^= poly
        tab[key] = res
    return tab


class SSB16:
    sbox = NotImplemented
    poly = None
    n = r = m = 16

    def __init__(self):
        if self.poly:
            self.MULTAB = precomp_multab(n=4, poly=self.poly)
        self.SB = self.compute(self.sub)
        self.MC = self.compute(self.mix)
        self.SBMC = self.compute(self.sub, self.mix)
        self.MCSB = self.compute(self.mix, self.sub)

    def get_keys(self):
        return list(range(2**self.r))

    def get_part1(self):
        return self.SBMC

    def get_part2(self):
        return self.SB

    def mix(self, a, b, c, d):
        raise NotImplementedError()

    def sub(self, a, b, c, d):
        return tuple(map(self.sbox.__getitem__, (a, b, c, d)))

    def compute(self, *funcs):
        s = []
        for a, b, c, d in product(range(16), repeat=4):
            for func in funcs:
                a, b, c, d = func(a, b, c, d)
            s.append((a << 12) | (b << 8) | (c << 4) | d)
        return Sbox(s, 16, 16)

    def make_sandwich(self, mask=None, keys=None):
        if keys is None:
            keys = self.get_keys()
        return Sandwich(
            part1=self.get_part1(),
            part2=self.get_part2(),
            keys=keys,
            mask=mask
        )


class SSB_Midori64(SSB16):
    # same as MANTIS, CRAFT
    sbox = 0xc, 0xa, 0xd, 0x3, 0xe, 0xb, 0xf, 0x7, 0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6

    def mix(self, a, b, c, d):
        t = a ^ b ^ c ^ d
        a ^= t
        b ^= t
        c ^= t
        d ^= t
        return a, b, c, d


class SSB_LED(SSB16):
    # same as PRESENT
    sbox = 0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2
    poly = 0x13

    def mix(self, a, b, c, d):
        for i in range(4):
            tmp = (
                self.MULTAB[a, 4] ^ self.MULTAB[b, 1]
                ^ self.MULTAB[c, 2] ^ self.MULTAB[d, 2]
            )
            a, b, c, d = b, c, d, tmp
        return a, b, c, d


class SSB_SKINNY64(SSB16):
    sbox = 0xc, 0x6, 0x9, 0x0, 0x1, 0xa, 0x2, 0xb, 0x3, 0x8, 0x5, 0xd, 0x4, 0xe, 0x7, 0xf

    def mix(self, a, b, c, d):
        b ^= c
        c ^= a
        d ^= c
        a, b, c, d = d, a, b, c
        return a, b, c, d

    def get_keys(self):
        return [(a << 8) | 0x20 for a in range(16 * 16)]


class SSB_ZEROKEY_SKINNY64(SSB_SKINNY64):
    def get_keys(self):
        return [0]


class SSB_ZEROKEY_LED(SSB_LED):
    def get_keys(self):
        return [0]


# from divprop.all_sboxes import misty_s9, misty_s7

# misty_s9 = misty_s9.s
# misty_s7 = misty_s7.s

# class MISTY_FI:
#     r = n = m = 16

#     def __init__(self):
#         self.part1 = []
#         for l, r in product(range(2**9), range(2**7)):
#             l = misty_s9[l]
#             l ^= r  # zero-extend 7->9

#             l, r = r, l

#             l = misty_s7[l]
#             l ^= r & 127  # truncate 9->7

#             y = (l << 9) | r
#             self.part1.append(y)
#         assert sorted(self.part1) == sorted(range(2**16))

#         self.part2 = []
#         for l, r in product(range(2**7), range(2**9)):
#             l, r = r, l

#             l = misty_s9[l]
#             l ^= r  # zero-extend 7->9

#             l, r = r, l
#             y = (l << 9) | r
#             self.part2.append(y)
#         assert sorted(self.part2) == sorted(range(2**16))

#     def get_keys(self):
#         return list(range(2**9))

#     def get_part1(self):
#         return self.part1

#     def get_part2(self):
#         return self.part2


ciphers = {
    cls.__name__.lower(): cls
    for cls in (
        SSB_Midori64,
        SSB_LED, SSB_ZEROKEY_LED,
        SSB_SKINNY64, SSB_ZEROKEY_SKINNY64,
        # MISTY_FI,
    )
}
