import os
import sys
import logging
import pickle

import justlogs

from random import shuffle
from functools import cache

from binteger import Bin

from optisolveapi.sat import CNF, ExtSolver, ConvexFormula
from optisolveapi.vector import Vector

from divprop import Sbox, SboxDivision
from divprop.ciphers import SSB_LED


log = logging.getLogger()

SAT_SOLVER = ExtSolver.new(solver="kissat")

SboxDivision.CACHE = ".cache"

"""
AC0 SB0 SR0 MC0
AC1 SB1 SR1 MC1
AC2 SB2 SR2 MC2
AC3 SB3 SR3 MC3
AC4 SB4 SR4 MC4
AC5 SB5 SR5 MC5
AC6 SB6 SR6 MC6
AC7 SB7 SR7 MC7
swap even SB and SR
=>

AC0 SR0
<ANF input mask>
[SB0 MC0 AC1 SB1] SSB
<start model>
[SR1 MC1 AC2 SR2] SMS
[SB2 MC2 AC3 SB3] SSB
[SR3 MC3 AC4 SR4] SMS
[SB4 MC4 AC5 SB5] SSB
[SR5 MC5 AC6 SR6] SMS
<end model>
[SB6 MC6 AC7 SB7] SSB
<ANF output mask>
SR7 MC7
"""


class LED_Model(SSB_LED):
    RCs = [int(v, 16) for v in "01,03,07,0F,1F,3E,3D,3B,37,2F,1E,3C,39,33,27,0E,1D,3A,35,2B,16,2C,18,30".split(",")]

    cons_SSB_card = 1
    cons_SSB_box_lb = 0
    cons_SSB_box_ub = 0
    cons_SSB_lb = 1
    cons_SSB_ub = 0

    cons_MC_card = 1
    cons_MC_matching = 0
    cons_MC_lb = 1
    cons_MC_ub2 = 0

    def __init__(self, keysize=128):
        super().__init__()

        self.keysize = keysize
        self.solver = None

        self.cache_key = "keysize%d" % self.keysize

        log.info(
            "Constraints: " + "".join(map(str, map(int, [
                self.cons_SSB_card,
                self.cons_SSB_box_lb,
                self.cons_SSB_box_ub,
                self.cons_SSB_lb,
                self.cons_SSB_ub,
                self.cons_MC_card,
                self.cons_MC_matching,
                self.cons_MC_lb,
                self.cons_MC_ub2,
            ])))
        )
        log.info(f"cons_SSB_card = {self.cons_SSB_card}")
        log.info(f"cons_SSB_box_lb = {self.cons_SSB_box_lb}")
        log.info(f"cons_SSB_box_ub = {self.cons_SSB_box_ub}")
        log.info(f"cons_SSB_lb = {self.cons_SSB_lb}")
        log.info(f"cons_SSB_ub = {self.cons_SSB_ub}")
        log.info(f"cons_MC_card = {self.cons_MC_card}")
        log.info(f"cons_MC_matching = {self.cons_MC_matching}")
        log.info(f"cons_MC_lb = {self.cons_MC_lb}")
        log.info(f"cons_MC_ub2 = {self.cons_MC_ub2}")

    def set_solver(self, solver):
        self.solver = solver

    def get_keys(self):
        return self.keys

    def get_MC_divinfo(self):
        return SboxDivision(sbox=self.MC)

    def get_MC_matrix(self):
        return self.MC.to_matrix()

    def get_SSB_divinfo(self, rno=0, colno=0, reduced=False):
        const = self.get_const(rno=rno+1, colno=colno)
        return self.get_SSB_divinfo_by_const(const, reduced=reduced)

    def get_SSB_divinfo_by_const(self, const, reduced=False):
        if reduced:
            sbox = self.SB
        else:
            sbox = [self.SB[self.SBMC[x] ^ const] for x in range(2**16)]
            sbox = Sbox(sbox, 16, 16)
        return SboxDivision(sbox=sbox)

    def get_SBOX_divinfo(self):
        sbox = Sbox(self.sbox, 4, 4)
        return SboxDivision(sbox=sbox)

    def get_const(self, rno, colno):
        if colno == 0:
            return Bin.concat(
                0 ^ (self.keysize >> 4),
                1 ^ (self.keysize >> 4),
                2 ^ (self.keysize & 0xf),
                3 ^ (self.keysize & 0xf),
                n=4,
            )
        if colno == 1:
            rc = self.RCs[rno]
            return Bin.concat(
                (rc >> 3) & 7,
                rc & 7,
                (rc >> 3) & 7,
                rc & 7,
                n=4,
            )
        return 0

    def SubBytes(self, st):
        st2 = self.solver.vars(64).split(16)
        sbox_di = self.get_SBOX_divinfo()
        for xs, ys in zip(st, st2):
            sbox_di.sat_constraint_lb(self.solver, xs, ys)
            sbox_di.sat_constraint_ub(self.solver, xs, ys)
        return st2

    def MixColumns(self, st):
        st = list(st)
        for x in range(4):
            st[x::4] = self.MixColumn(st[x::4])
        return Vector(st)

    def SuperSboxes(self, st, rno, light=False):
        st = list(st)
        for x in range(4):
            st[x::4] = self.SuperSbox(st[x::4], rno=rno, colno=x, light=light)
        return Vector(st)

    def ShiftRows(self, st):
        st = list(st)
        for y in range(0, 16, 4):
            row = st[y:y+4]
            st[y:y+4] = row[y//4:] + row[:y//4]
        return Vector(st)

    def MixColumn(self, col):
        xs = col[0].concat(*col[1:])
        ys = self.solver.vars(16)

        # partial LB and full UB by cardinality
        if self.cons_MC_card:
            card = self.solver.Card((-xs).concat(ys), limit=17)
            assert len(card) == 1 + 17
            self.solver.CardLEk(card, 16)  # UB
            self.solver.CardGEk(card, 16)

        # partial LB by matching
        if self.cons_MC_matching:
            self.solver.constraint_matching(xs, ys, self.get_MC_matrix())

        # complete LB
        if self.cons_MC_lb:
            mc_di = self.get_MC_divinfo()
            mc_di.sat_constraint_lb(self.solver, xs, ys)

        # complete UB
        if self.cons_MC_ub2:
            mc_di = self.get_MC_divinfo()
            mc_di.sat_constraint_ub2(self.solver, xs, ys)
        return ys.split(4)

    def SuperSbox(self, col, rno, colno, light=False):
        """ SB MC SB """
        if light:
            sbox_di = self.get_SBOX_divinfo()
            coly = self.solver.vars(16).split(4)
            for xs, ys in zip(col, coly):
                sbox_di.sat_constraint_lb(self.solver, xs, ys)
                sbox_di.sat_constraint_ub(self.solver, xs, ys)
            col = coly

            col = self.MixColumn(col)

            coly = self.solver.vars(16).split(4)
            for xs, ys in zip(col, coly):
                sbox_di.sat_constraint_lb(self.solver, xs, ys)
                sbox_di.sat_constraint_ub(self.solver, xs, ys)
            col = coly
            return col

        assert len(col) == 4
        xs = Vector(col).flatten()
        ys = self.solver.vars(16)
        assert len(xs) == 16
        assert len(ys) == 16
        ret = Vector(ys).split(4)

        log.info(f"SSB round {rno} column {colno}")
        uv = (-xs).concat(ys)

        curssb = self.get_SSB_divinfo(rno=rno, colno=colno)

        if self.cons_SSB_card:
            # 1-dimensional cardinality nound
            ub = max(word.weight for word in curssb.minimal_max.to_Bins())
            lb = min(word.weight for word in curssb.minimal_min.to_Bins())

            card = self.solver.Card(uv, limit=ub+1)
            self.solver.CardLEk(card, ub)
            self.solver.CardGEk(card, lb)

            # 2-dimensional cardinality bound (degree-based)
            # cardx = self.solver.Card(xs, limit=16)
            # cardy = self.solver.Card(ys, limit=16)
            # assert len(cardx) == 17
            # assert len(cardy) == 17
            # UB
            # self.solver.CardLE(cardy, cardx)

            # LB1
            # self.solver.CardLE(cardx, self.solver.CardScale(cardy, 9))
            # x <= 9y
            # y >= x/9
            '''
            (u,v)
            not u -S> v
            not v -Si> u

            v >= (n-u) / 9
            9v >= n-u

            9v + u >= n
            9u + v >= n

            9v >= (n-u)
            9u >= (n-v)

            a = n-u
            b = v

            9b >= a
            9(n-a) >= (n-b)
            '''

            # LB2
            # cardnx = self.solver.CardNeg(cardx)
            # cardny = self.solver.CardNeg(cardy)
            # self.solver.CardLE(cardny, self.solver.CardScale(cardnx, 9))

        if self.cons_SSB_box_lb or self.cons_SSB_box_ub:
            cards = [self.solver.Card(chunk) for chunk in uv.split(8)]
            dimensions = [4] * 8

            if self.cons_SSB_box_lb:
                box = curssb.box_lb(dimensions=dimensions)
                for vs in box:
                    clause = []
                    for card, val in zip(cards, box.unpack(vs)):
                        clause.append(card[val+1])
                    self.solver.add_clause(clause)

            if self.cons_SSB_box_ub:
                box = curssb.box_ub(dimensions=dimensions)
                for vs in box:
                    clause = []
                    for card, val in zip(cards, box.unpack(vs)):
                        clause.append(-card[val])
                    self.solver.add_clause(clause)

        # no UB because it's huge
        # approx Box UB is enough
        if self.cons_SSB_lb:
            self.solver.apply(curssb.cnf_lb, uv)
        if self.cons_SSB_ub:
            self.solver.apply(curssb.cnf_ub, uv)
        return ret

    def setup_middle_of_8(self):
        S = CNF.new(solver="writer")
        S.set_solver(SAT_SOLVER)
        self.set_solver(S)

        S.states = []

        self.start = st = S.vars(64).split(16)

        # middle SSB rounds
        S.states.append(("initial", st))

        st = self.ShiftRows(self.MixColumns(self.ShiftRows(st)))
        S.states.append(("after SR MC SR", st))

        st = self.SuperSboxes(st, rno=2, light=False)
        S.states.append(("after SSB", st))

        st = self.ShiftRows(self.MixColumns(self.ShiftRows(st)))
        S.states.append(("after SR MC SR", st))

        st = self.SuperSboxes(st, rno=4, light=False)
        S.states.append(("after SSB", st))

        st = self.ShiftRows(self.MixColumns(self.ShiftRows(st)))
        S.states.append(("after SR MC SR", st))

        self.target = st

    def clone_for_SSB_to_SSB(self, I, J, check=True):
        S = self.solver.copy()

        # first round - all but one SSBs are 1111->1111
        # last round - all but one SSBs are 0000->0000
        start_cols = []
        target_cols = []
        for x in range(4):
            if x != I:
                start_cols += list(Vector(self.start[x::4]).flatten())
            if x != J:
                target_cols += list(Vector(self.target[x::4]).flatten())

        for c in start_cols:
            S.add_clause([c])  # = 1
        for c in target_cols:
            S.add_clause([-c])  # = 0

        xs = Vector(self.start[I::4])
        ys = Vector(self.target[J::4])

        xs = xs.flatten()
        ys = ys.flatten()
        if check:
            # sanity check - no extra constraints on the I,J SuperSboxes
            assert S.solve()
        return S, xs, ys

    def __repr__(self):
        return f"<LED_Model keysize={self.keysize}>"


def main():
    justlogs.setup(level="INFO")

    I = J = 0

    if len(sys.argv) == 3:
        I = int(sys.argv[1])
        J = int(sys.argv[2])
    else:
        cons = list(map(int, sys.argv[1:]))
        assert len(cons) == 7
        log.info(f"cons {cons}")
        # note: reverse order
        LED_Model.cons_SSB_card = cons.pop()
        LED_Model.cons_SSB_box_lb = cons.pop()
        LED_Model.cons_SSB_box_ub = cons.pop()
        LED_Model.cons_SSB_lb = 1
        LED_Model.cons_SSB_ub = cons.pop()

        LED_Model.cons_MC_card = cons.pop()
        LED_Model.cons_MC_matching = cons.pop()
        LED_Model.cons_MC_lb = 1
        LED_Model.cons_MC_ub2 = cons.pop()

    justlogs.addFileHandler(f"logs/LED_{I}_{J}_{os.urandom(2).hex()}")

    log.info(f"columns {I} -> {J}")

    L = LED_Model(keysize=128)

    sbox1div = L.get_SSB_divinfo(rno=0, colno=I).inverse()
    if 0:
        # sanity test for reduced SSB (only SB instead of SB MC SB)
        # check that the approach fails (because there are distinguishers!)
        log.info("sanity test reduced ssb")
        sbox2div = L.get_SSB_divinfo(rno=6, colno=J, reduced=True)
    else:
        log.info("full ssb")
        sbox2div = L.get_SSB_divinfo(rno=6, colno=J)

    anfsI_full = sbox1div.components_anf_closures()
    log.info(f"anfsI {len(anfsI_full)}")

    anfsO_full = sbox2div.components_anf_closures()
    log.info(f"anfsO {len(anfsO_full)}")

    anfsI_max = {mask: anf.MaxSet() for mask, anf in anfsI_full.items()}
    anfsO_max = {mask: anf.MaxSet() for mask, anf in anfsO_full.items()}

    # AND of ANF closures
    # (find monomials that will provide a trail for all linear masks)

    L.setup_middle_of_8()

    trails_file = f"data/LED_trails_{I}_{J}.pickle"
    greedy_file_pickle = f"data/LED_trails_{I}_{J}_greedy.pickle"
    greedy_file_text = f"data/LED_trails_{I}_{J}_greedy.txt"

    try:
        trails = pickle.load(open(trails_file, "rb"))
        log.info(f"loaded {len(trails)} trails")
    except Exception as err:
        trails = {}

    mask_pairs = [(maski, masko) for maski in anfsI_full for masko in anfsO_full]
    shuffle(mask_pairs)

    log.info(f"mask pairs: {len(anfsI_full)} x {len(anfsO_full)} = {len(mask_pairs)}")

    SAT_times = []
    total = len(mask_pairs)
    current = 0
    for maski, masko in mask_pairs:
        current += 1
        anfI_max = anfsI_max[maski]
        anfO_max = anfsO_max[masko]

        found = False
        for u, v in trails:
            # u <= anfI_max && v <= anfO_max
            if int(u) in anfsI_full[maski] and int(v) in anfsO_full[masko]:
                found = True
                break
        if found:
            continue

        log.info(f"#trails {len(trails)} ")
        log.info(f"mask pair #{current} / {total}: "
                 f"{Bin(maski, 16)} {Bin(masko, 16)}"
                 f"anfI_max {anfI_max} anfO_max {anfO_max}")

        curi_ub = anfI_max.ComplementL2U()
        if 1:
            ci = ConvexFormula(ub=curi_ub)
        else:
            # as a MaxSet (antichain), anfI_max is Convex
            # => can be constrained by a lower and an upper bound
            curi_lb = anfI_max.ComplementU2L()
            ci = ConvexFormula(lb=curi_lb, ub=curi_ub)

        # not specifying an upper bound because need to catch prec vectors too
        curo_ub = anfO_max.ComplementL2U()
        co = ConvexFormula(ub=curo_ub)

        SS, xs, ys = L.clone_for_SSB_to_SSB(I=I, J=J, check=True)

        SS.apply(ci, -xs)
        SS.apply(co, ys)

        from time import time
        log.info("solving SAT...")
        t0 = time()
        sol = SS.solve()
        SAT_times.append(time() - t0)
        log.info(f"SAT solve time: {SAT_times[-1]}")
        SAT_times = sorted(SAT_times)
        log.info(
            f"SAT_times: {min(SAT_times):.1f} - {max(SAT_times):.1f}, "
            f"avg {sum(SAT_times)/len(SAT_times):.1f} "
            f"med {SAT_times[len(SAT_times)//2]:.1f}"
        )

        if not sol:
            log.error(f"oops, method failed {sol} distinguisher found???")
            quit()

        vxs = Bin(SS.sol_eval(sol, xs), 16)
        nvxs = ~vxs
        vys = Bin(SS.sol_eval(sol, ys), 16)
        log.info(
            f"middle division transition "
            f"~{nvxs.str} -> {vys.str} (~{nvxs.hw} -> {vys.hw})"
        )

        log.info(f"mid transition: {nvxs.str} {vys.str} {nvxs.hw} {vys.hw}")
        log.info("full trace:")

        trail = []
        for name, st in SS.states:
            row = Vector(st).flatten()
            row = Bin(SS.sol_eval(sol, row), 64)
            log.info(" ".join(v.str for v in row.split(16)) + "# " + name)
            trail.append(row)
        log.info("")

        trails[nvxs, vys] = trail

        log.info(f"new trail: {nvxs} -> {vys}")

        pickle.dump(trails, open(trails_file, "wb"))
    log.info("")

    log.info(
        f"final SAT_times: {min(SAT_times):.1f} - {max(SAT_times):.1f}, "
        f"avg {sum(SAT_times)/len(SAT_times):.1f} "
        f"med {SAT_times[len(SAT_times)//2]:.1f}"
    )
    log.info(f"SAT_times all {SAT_times}")

    log.info("Trails:")
    for (u, v), rows in trails.items():
        log.info(f"trail ~{u} -> {v}: {' '.join(row.str for row in rows)}")
    log.info("")

    log.info("Greedy:")

    @cache
    def satisfy(maski, masko, trail):
        u, v = trail
        if int(u) in anfsI_full[maski] and int(v) in anfsO_full[masko]:
            return True
        return False

    tocover = {(maski, masko) for maski in anfsI_full for masko in anfsO_full}
    chosen = []
    while tocover:
        log.info(f"greedy iter, tocover {len(tocover)}")
        counts_by_trail = {}
        for trail in trails:
            counts_by_trail[trail] = sum(satisfy(*msk, trail) for msk in tocover)

        counts_by_trail = sorted(counts_by_trail.items(), key=lambda v: v[1])
        for trail, cnt in counts_by_trail[-1:]:
            log.info(f"trail {trail} cnt {cnt}")

        trail, cnt = counts_by_trail[-1]
        tocover = {msk for msk in tocover if not satisfy(*msk, trail)}
        chosen.append(trail)
        log.info("-----")
        assert cnt

    with open(greedy_file_text, "w") as fg:
        log.info(f"chosen trails: {len(chosen)}")
        greedy = {}
        for trail in chosen:
            rows = trails[trail]
            u, v = trail
            log.info(f"trail ~{u} -> {v}: {' '.join(row.str for row in rows)}")
            greedy[u, v] = rows
            print(u, v, *[row.str for row in rows], file=fg)
        log.info("end")

    pickle.dump(greedy, open(greedy_file_pickle, "wb"))


if __name__ == '__main__':
    main()

# reduced
# anfI_max <DenseSet hash=dfccb12f4cdcb9d2 n=16 wt=4333 | 0:1 1:16 2:120 3:556 4:1405 5:1671 6:560 7:4> max <DenseSet hash=93d90531c3a4b298 n=16 wt=808 | 3:7 4:21 5:240 6:536 7:4>
# curo <DenseSet hash=c274f4587854fdaf n=16 wt=3641 | 0:1 1:16 2:120 3:551 4:1378 5:1437 6:138> max <DenseSet hash=9a9f29e58c5ea93c n=16 wt=1049 | 3:5 4:34 5:872 6:138>

# all masks
# anfI_max <DenseSet hash=363d721f617034e9 n=16 wt=235 | 0:1 1:16 2:104 3:102 4:12> max <DenseSet hash=bef1a371658184ce n=16 wt=91 | 2:13 3:66 4:12>
# curo <DenseSet hash=5c03c5782c8eedb9 n=16 wt=189 | 0:1 1:16 2:115 3:57> max <DenseSet hash=c70c8bbcf6c7e692 n=16 wt=96 | 2:39 3:57>
