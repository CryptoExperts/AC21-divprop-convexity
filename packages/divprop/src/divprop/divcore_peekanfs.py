from collections import defaultdict
from queue import PriorityQueue

from binteger import Bin

from divprop import Sbox

import logging


def half_lens(fset, n):
    l = sum(1 for i in fset if i < n)
    r = len(fset) - l
    return l, r


class SboxPeekANFs:
    """
    Advanced algorithm for DivCore computation,
    by computing backward and forward ANFs of products
    """
    log = logging.getLogger(f"{__name__}:SboxPeekANFs")
    n_queries = 0

    def __init__(self, sbox: Sbox, isbox: Sbox = None):
        assert isinstance(sbox, Sbox.classes)
        self.n = int(sbox.n)
        self.sbox = sbox
        self.isbox = ~sbox if isbox is None else isbox

    def compute(self, debug=False):
        """
        Returns:
            divcore (set(Bin))
            invalid_max (set(Bin))
        """

        n = self.n

        # initialize set of parity1 vectors (possibly redundant)
        parity1 = set()
        # - add (1...1, 0...0) to parity1
        parity1.add(frozenset(range(n)))
        # - add (0...0, 1...1) to parity1
        parity1.add(frozenset(range(n, 2*n)))

        # initialize divcore by the two known vectors (1,0), (0,1)
        divcore = parity1.copy()

        # initialize neighbor counter
        cnt = defaultdict(int)

        # cache of masks already run
        masks_run = set()

        # this dict tracks maximal vectors below divcore
        # = maximal vectors of I_S
        invalid_max = set()
        # add predecessors of (1...1, 0...0) and (0...0, 1...1) explicitly
        for i in range(n):
            fset = frozenset(range(n)) - {i}
            invalid_max.add(fset)
            fset = frozenset(range(n, 2*n)) - {n+i}
            invalid_max.add(fset)

        # initialize the exploration queue with (e_i, e_j) pairs
        self.queue = q = PriorityQueue()
        for i in range(n):
            for j in range(n):
                fset = frozenset((i, n+j))

                prio = (1, 1)
                q.put((prio, fset))

                cnt[fset] = 0
                invalid_max.add(fset)

        while q.qsize():
            _, fset = q.get()
            if fset in parity1:
                divcore.add(fset)
                invalid_max.discard(fset)
                continue

            # choose side to evaluate
            w1, w2 = half_lens(fset, n)
            inverse = w1 < w2
            mask = Bin(fset, 2*n).int
            if inverse:
                mask >>= n
            else:
                mask &= 2**n-1

            # check if already evaluated
            if (mask, inverse) not in masks_run:
                masks_run.add((mask, inverse))

                res = self.run_mask(mask, inverse=inverse)
                parity1.update({
                    frozenset(Bin(uv, 2*n).support)
                    for uv in res
                })

                if fset in parity1:
                    # case of parity 1
                    divcore.add(fset)
                    invalid_max.discard(fset)
                    continue

            # case of parity zero
            for i in range(2*n):
                if i in fset:
                    # mark downwards as not maximal
                    fset2 = fset - {i}
                    invalid_max.discard(fset2)
                    continue

                fset2 = fset | {i}
                assert len(fset2) == len(fset) + 1
                cnt[fset2] += 1

                w1, w2 = half_lens(fset2, n)
                need = w1 if w1 > 1 else 0
                need += w2 if w2 > 1 else 0
                if cnt[fset2] == need:
                    prio = min(w1, w2), max(w1, w2)
                    q.put((prio, fset2))
                    invalid_max.add(fset2)

        divcore = {Bin(v, 2*n) for v in divcore}
        invalid_max = {Bin(v, 2*n) for v in invalid_max}
        return divcore, invalid_max

    def get_product(self, mask, inverse):
        sbox = self.isbox if inverse else self.sbox
        return sbox.coordinate_product(mask)

    def run_mask(self, mask, inverse=False):
        self.n_queries += 1
        assert 0 <= mask < 1 << self.n
        func = self.get_product(mask, inverse)
        func.do_ParitySet()
        func.do_MinSet()
        if inverse:
            retdc = {(mask << self.n) | u for u in func}
        else:
            retdc = {(u << self.n) | mask for u in func}
        return retdc


if __name__ == '__main__':
    from random import shuffle, seed, randint
    from divprop import SboxDivision
    from time import time
    t2 = 0
    t3 = 0
    itr = 0
    while 1:
        itr += 1
        s = randint(0, 2**32)
        # s = 1911301760
        print("seed", s)
        seed(s)
        n = randint(3, 12)
        # n = 4
        sbox = list(range(2**n))
        shuffle(sbox)

        sbox = Sbox(sbox, n, n)
        test1 = (
            set(SboxDivision(sbox).divcore.to_Bins()),
            set(SboxDivision(sbox).invalid_max.to_Bins()),
        )

        S2 = SboxPeekANFs(sbox)
        t0 = time()
        test2 = S2.compute(exper=False)
        t2 += time() - t0

        print("seed", s)
        assert test1[0] == test2[0]

        assert test1[1] == test2[1]
        print("OK", itr)
        print(S2.n_queries, t2)
