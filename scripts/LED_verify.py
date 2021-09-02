import sys
import logging

import justlogs

from subsets import DenseSet
from binteger import Bin

from optisolveapi.vector import Vector

from divprop import Sbox, SboxDivision
from divprop.ciphers import SSB_LED

log = logging.getLogger()

LED = SSB_LED()
RCs = [int(v, 16) for v in "01,03,07,0F,1F,3E,3D,3B,37,2F,1E,3C,39,33,27,0E,1D,3A,35,2B,16,2C,18,30".split(",")]
KEYSIZE = 128

SboxDivision.CACHE = ".cache"

# NOTE: using full dppt, since precise redundant bounds were not used
# (redundant transitions may occur)
MC_DPPT = SboxDivision(sbox=LED.MC).full_dppt


def get_DB_SSB(rno=0, colno=0, const=None):
    if const is None:
        const = get_const(rno=rno+1, colno=colno)
    # note on SSB: SB -> MC -> AC here! -> SB
    # equivalent
    # sbox = [LED.SB[LED.SBMC[x] ^ const] for x in range(2**16)]
    sbox = [LED.SB[LED.MC[LED.SB[x]] ^ const] for x in range(2**16)]
    return SboxDivision(sbox=Sbox(sbox, 16, 16))


def get_const(rno, colno):
    if colno == 0:
        return Bin.concat(
            0 ^ (KEYSIZE >> 4),
            1 ^ (KEYSIZE >> 4),
            2 ^ (KEYSIZE & 0xf),
            3 ^ (KEYSIZE & 0xf),
            n=4,
        )
    if colno == 1:
        rc = RCs[rno]
        return Bin.concat(
            (rc >> 3) & 7,
            rc & 7,
            (rc >> 3) & 7,
            rc & 7,
            n=4,
        )
    return 0


def verify_SSB(st0, st1, rno):
    st0 = st0.split(16)
    st1 = st1.split(16)

    for colno in range(4):
        SSB_DPPT = get_DB_SSB(rno=rno, colno=colno).full_dppt

        xs = Vector(st0[colno::4]).map(list).flatten()
        ys = Vector(st1[colno::4]).map(list).flatten()
        vec = Bin.concat(xs, ys).int
        assert SSB_DPPT[vec]
        global N_SSB
        N_SSB += 1


def verify_SRMCSR(st0, st1):
    st0 = st0.split(16)
    st1 = st1.split(16)

    st0 = ShiftRows(st0)

    st1 = ShiftRows(st1)
    st1 = ShiftRows(st1)
    st1 = ShiftRows(st1)

    for colno in range(4):
        xs = Vector(st0[colno::4]).map(list).flatten()
        ys = Vector(st1[colno::4]).map(list).flatten()
        vec = Bin.concat(xs, ys).int
        assert MC_DPPT[vec]
        global N_MC
        N_MC += 1


def ShiftRows(st):
    assert len(st) == 16
    st = list(st)
    for y in range(4):
        row = st[y*4:y*4+4]
        st[y*4:y*4+4] = row[y:] + row[:y]
    assert len(st) == 16
    return Vector(st)


def verify_trail(I, J, u, v, trail):
    nu = ~u
    start = Vector(
        Vector([1, 1, 1, 1])
        for _ in range(16)
    )
    # setup column I = nu
    for i in range(4):
        start[4*i+I] = nu[4*i:4*i+4]

    target = Vector(
        Vector([0, 0, 0, 0])
        for _ in range(16)
    )
    # setup column J = v
    for i in range(4):
        target[4*i+J] = v[4*i:4*i+4]

    assert start.map(list).flatten() == trail[0]
    assert target.map(list).flatten() == trail[-1]
    assert len(trail) == 6
    # SSB0 [SMS SSB2 SMS SSB4 SMS] SSB6

    verify_SRMCSR(trail[0], trail[1])
    verify_SSB   (trail[1], trail[2], rno=2)
    verify_SRMCSR(trail[2], trail[3])
    verify_SSB   (trail[3], trail[4], rno=4)
    verify_SRMCSR(trail[4], trail[5])


I = int(sys.argv[1])
J = int(sys.argv[2])

justlogs.addFileHandler(f"logs/LED_verify_{I}_{J}")
justlogs.setup(level="DEBUG")

log.info(f"I = {I} J = {J}:")
trails = {}
for line in open(f"data/LED_trails_{I}_{J}_greedy.txt"):
    u, v, *trail = line.split()
    u = Bin(u, 16)
    v = Bin(v, 16)
    trail = tuple(Bin(state, 64) for state in trail)
    trails[u, v] = trail

    if 1:
        log.info(f"~{u} -> {v}:")
        for state in trail:
            log.info(f"   {state}")

        N_SSB = 0
        N_MC = 0
        verify_trail(I, J, u, v, trail)

        log.info(f"verify ok! {N_SSB} SuperSboxes {N_MC} MixColumns")
        assert N_SSB == 8
        assert N_MC == 12

log.info(f"verified {len(trails)} trails for I {I} J {J}")

if 0:
    # test for the paper's example (1785 and 2021)
    db = get_DB_SSB(const=0)
    anfs = db.components_anf_closures(only_minimal=False)
    log.info(f"(output/forward) unique masks {len(anfs)}")
    anfs = db.inverse().components_anf_closures(only_minimal=False)
    log.info(f"(input/inverse) unique masks {len(anfs)}")
    del anfs


log.info("generating ANFs... I")
sbox_div = get_DB_SSB(rno=0, colno=I).inverse()
# do not remove redundant to make full verification
anfsI = sbox_div.components_anf_closures(only_minimal=False)
log.info(f"unique masks {len(anfsI)}")

log.info("generating ANFs... J")
sbox_div = get_DB_SSB(rno=6, colno=J)
# do not remove redundant to make full verification
anfsO = sbox_div.components_anf_closures(only_minimal=False)
log.info(f"unique masks {len(anfsO)}")

log.info("enumerating all mask pairs")

for maskI, anfI in anfsI.items():
    for maskO, anfO in anfsO.items():
        assert any((anfI[u.int] and anfO[v.int]) for u, v in trails)

log.info(f"verified all masks for I {I} J {J}")

log.info(f"VERIFIED I {I} J {J}")
