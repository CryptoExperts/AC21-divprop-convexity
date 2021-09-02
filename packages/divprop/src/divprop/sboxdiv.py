import logging

from optisolveapi.sat import ConvexFormula
from optisolveapi.vector import Vector

from subsets import DenseSet

from divprop import Sbox
from divprop.utils import cached_method

from divprop.lib import (
    DivCore_StrongComposition,
    DivCore_StrongComposition8,
    DivCore_StrongComposition16,
    DivCore_StrongComposition32,
    DivCore_StrongComposition64,
)
from divprop.divcore_peekanfs import SboxPeekANFs


def make_mask(m):
    return (1 << m) - 1


class SboxDivision:
    CACHE = None

    log = logging.getLogger()

    def __init__(self, sbox: Sbox):
        self.sbox = sbox
        self.cache_key = "sbox%016X" % sbox.get_hash()  # too small hash?

        self.n = int(sbox.n)
        self.m = int(sbox.m)
        self.mask_u = make_mask(self.n) << self.m
        self.mask_v = make_mask(self.m)

    @classmethod
    def from_divcore(cls, divcore: DenseSet, n, m=None):
        assert isinstance(divcore, DenseSet)

        if m is None:
            m = divcore.n - n

        self = super().__new__(cls)

        self.n = int(n)
        self.m = int(m)
        assert divcore.n == self.n + self.m
        self.mask_u = make_mask(self.n) << self.m
        self.mask_v = make_mask(self.m)

        self.cache_key = "divcore%016X" % divcore.get_hash()  # too small hash?
        f = cls.divcore.fget
        f._cache[f._calc_key(self)] = divcore
        assert self.divcore == divcore
        return self

    @property
    @cached_method
    def divcore(self):
        ret = self.sbox.graph_dense()
        ret.do_Mobius()
        ret.do_MaxSet()
        ret.do_Not()
        return ret

    @property
    @cached_method
    def divcore_heavy(self):
        pass

    @property
    @cached_method
    def valid(self):
        return self.divcore.UpperSet()
    valid_min = divcore

    @property
    @cached_method
    def invalid_max(self):
        return self.divcore.ComplementU2L()
    lb = invalid_max  # complementary lower bound

    @property
    @cached_method
    def redundant_min(self):
        ret = self.divcore.copy()
        ret.do_UpperSet_Up1(True, self.mask_v)  # is_minset=true
        ret.do_MinSet()
        return ret
    ub = redundant_min  # complementary upper bound

    @property
    @cached_method
    def redundant_alternative_min(self):
        return self.minimal_max.ComplementL2U()
    ub2 = redundant_alternative_min  # complementary upper bound (alternative)

    @property
    @cached_method
    def redundant_best_min(self):
        """best of ub and ub2"""
        if self.ub.get_weight() < self.ub2.get_weight():
            return self.ub
        return self.ub2
    ubest = redundant_best_min  # smallest (by extremes) upper bound

    @property
    @cached_method
    def minimal(self):
        ret = self.divcore.copy()
        ret.do_UpperSet(self.mask_u)
        ret.do_MinSet(self.mask_v)
        return ret

    @property
    @cached_method
    def minimal_max(self):
        return self.minimal.MaxSet()
    minimal_min = divcore

    @property
    @cached_method
    def full_dppt(self):
        ret = self.divcore.copy()
        ret.do_UpperSet()
        ret.do_Not(self.mask_u)
        return ret

    @property
    @cached_method
    def min_dppt(self):
        ret = self.divcore.copy()
        ret.do_UpperSet(self.mask_u)
        ret.do_MinSet(self.mask_v)
        ret.do_Not(self.mask_u)
        return ret

    @property
    @cached_method
    def propagation_map(self):
        ret = [list() for _ in range(2**self.n)]
        for uv in self.min_dppt.to_Bins():
            u, v = uv.split(ns=(self.n, self.m))
            ret[u.int].append(v.int)
        return ret

    @cached_method
    def components_anf_closures(self, remove_dups_by_maxset=True, only_minimal=True):
        """
        (unique/non-redundant) closures of ANFs of components
        """
        n = self.sbox.n
        m = self.sbox.m
        # linear-time build all components
        cs = list(self.sbox.coordinates())
        xors = [DenseSet(n)] + [None] * (2**m-1)
        for i in range(m):
            for j in range(2**i):
                xors[j + 2**i] = xors[j] ^ cs[m - 1 - i]

        # ANF closures
        anfs_full = {
            mask: xor.Mobius().LowerSet()
            for mask, xor in enumerate(xors)
        }
        del anfs_full[0]
        anfs_max = {
            mask: anf.MaxSet()
            for mask, anf in anfs_full.items()
        }
        del xors
        assert len(anfs_full) == 2**m - 1

        if remove_dups_by_maxset:
            unique = []
            seen = {}
            for mask in range(1, 2**m):
                mx = anfs_max[mask]
                h = mx.get_hash()
                if h in seen:
                    # check that it's not a hash collision
                    assert seen[h] == mx
                    continue
                seen[h] = mx
                unique.append(mask)
            del seen
            anfs_full = {mask: anfs_full[mask] for mask in unique}
            self.log.debug(f"unique masks {len(anfs_full)}")

        if only_minimal:
            minimal = []
            for mask1 in anfs_full:
                for mask2 in anfs_full:
                    if mask1 == mask2:
                        continue
                    if is_max_preceq_full(anfs_max[mask2], anfs_full[mask1]):
                        break
                else:
                    minimal.append(mask1)
            anfs_full = {mask: anfs_full[mask] for mask in minimal}
            self.log.debug(f"minimal masks {len(anfs_full)}")
        return anfs_full

    def inverse(self):
        return SboxDivision(sbox=self.sbox.inverse())

    # CONSTRAINTS
    # ======================================

    @property
    @cached_method
    def cnf_lb(self):
        return ConvexFormula(lb=self.lb)

    @property
    @cached_method
    def cnf_ub(self):
        return ConvexFormula(ub=self.ub)

    @property
    @cached_method
    def cnf_ub2(self):
        return ConvexFormula(ub=self.ub2)

    @property
    @cached_method
    def cnf_ubest(self):
        return ConvexFormula(ub=self.ubest)

    @cached_method
    def box(self, dimensions):
        assert sum(dimensions) == self.sbox.n + self.sbox.m
        return self.minimal.to_DenseBox(dimensions)

    @cached_method
    def box_lb(self, dimensions):
        return self.box(dimensions).MinSet().ComplementU2L()

    @cached_method
    def box_ub(self, dimensions):
        return self.box(dimensions).MaxSet().ComplementL2U()

    def sat_constraint_lb(self, solver, xs, ys):
        assert len(xs) == self.sbox.n
        assert len(ys) == self.sbox.m
        solver.apply(self.cnf_lb, Vector(-xs).concat(ys))

    def sat_constraint_ub(self, solver, xs, ys):
        assert len(xs) == self.sbox.n
        assert len(ys) == self.sbox.m
        solver.apply(self.cnf_ub, Vector(-xs).concat(ys))

    def sat_constraint_ub2(self, solver, xs, ys):
        assert len(xs) == self.sbox.n
        assert len(ys) == self.sbox.m
        solver.apply(self.cnf_ub2, Vector(-xs).concat(ys))

    def sat_constraint_ubest(self, solver, xs, ys):
        assert len(xs) == self.sbox.n
        assert len(ys) == self.sbox.m
        solver.apply(self.cnf_ubest, Vector(-xs).concat(ys))


def is_max_preceq_full(s1: DenseSet, s2: DenseSet):
    """Faster variant. s2 must be lower-closed"""
    for u in s1:
        if u not in s2:
            return False
    return True


if __name__ == '__main__':
    import justlogs
    justlogs.setup(level="DEBUG")

    db = SboxDivision(Sbox([1, 2, 3, 0], 2, 2))
    print(db.divcore)
    print(db.box_ub([2, 2]))
