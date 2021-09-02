import logging

from binteger import Bin

from divprop.lib import Sbox, Sbox8
from divprop.sboxdiv import (
    DivCore_StrongComposition8,
    DivCore_StrongComposition16,
    DivCore_StrongComposition32,
    DivCore_StrongComposition64,
)


log = logging.getLogger(__name__)


class Sandwich:
    """Computing DivCore for two S-boxes with xor key in-between."""

    def __init__(self, part1: Sbox, part2: Sbox, keys=None, mask=None):
        """
        mask identifies a single output component to analyze.
        (full output if mask=None)
        """
        assert type(part1).__name__.startswith("Sbox")
        assert type(part2).__name__.startswith("Sbox")

        assert part1.m == part2.n
        self.n = part1.n
        self.r = part1.m
        if mask is None:
            self.m = part2.n
        else:
            self.m = 1
            assert 0 <= mask < 2**part2.n
        self.part1 = part1
        if keys is None:
            self.keys = tuple(range(2**self.r))
        else:
            self.keys = tuple(map(int, keys))
            assert 0 <= min(self.keys) <= max(self.keys) < 2**self.r

        if mask is None:
            self.part2 = part2
        else:
            mask = Bin(mask, part2.n)
            table = [mask.scalar_bin(y) for y in part2]
            self.part2 = Sbox8(table, part2.n, 1)

    def compute_divcore(self, chunk=128, filename=None):
        sz = min(self.part1.ENTRY_SIZE, self.part2.ENTRY_SIZE)
        if sz <= 1:
            cls = DivCore_StrongComposition8
        elif sz <= 2:
            cls = DivCore_StrongComposition16
        elif sz <= 4:
            cls = DivCore_StrongComposition32
        else:
            assert sz <= 8
            cls = DivCore_StrongComposition64

        DCS = cls(
            self.n, self.r, self.m,
            self.part1.data, self.part2.data,
        )
        DCS.set_keys(self.keys)
        DCS.shuffle()

        log.info(
            f"processing Sandwich({self.n},{self.r},{self.m})"
            f" with {len(self.keys)} keys, saving to {filename}"
        )
        n_done = 0
        while len(DCS.keys_left):
            DCS.process(chunk)
            n_done += chunk
            log.info(f"done {n_done}/{len(self.keys)}: {DCS.divcore}")
            if filename:
                DCS.divcore.save_to_file(filename + ".set")
                with open(filename + ".dim", "w") as f:
                    print(self.n, self.m, file=f)
        return DCS.divcore
