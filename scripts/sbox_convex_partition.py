import sys

from binteger import Bin
from subsets import DenseSet

from divprop import Sbox, SboxDivision
from divprop.all_sboxes import sboxes
from divprop.ciphers import ciphers

SboxDivision.CACHE = ".cache/"

data = sboxes.copy()

LED = ciphers["ssb_led"]()
Midori64 = ciphers["ssb_midori64"]()
Skinny64 = ciphers["ssb_skinny64"]()

if 1:  # generate mix functions (bitslices of MixColumn)
    mix = []
    for x in range(16):
        y = Midori64.mix(*Bin(x, 4).tuple)
        mix.append(Bin(y).int)
    data["Midori64_mix"] = Sbox(mix, 4, 4)

    # save for optimal CNF modeling
    SboxDivision(data["Midori64_mix"]).min_dppt.save_to_file("data/Midori64_mix.set")

    mix = []
    for x in range(16):
        y = Skinny64.mix(*Bin(x, 4).tuple)
        mix.append(Bin(y).int)
    data["Skinny64_mix"] = Sbox(mix, 4, 4)

    # save for optimal CNF modeling
    SboxDivision(data["Skinny64_mix"]).min_dppt.save_to_file("data/Skinny64_mix.set")

if 1:  # use 16-bit MixColumns
    data["LED_MC"] = LED.MC
    data["Midori64_MC"] = Midori64.MC
    data["Skinny64_MC"] = Skinny64.MC

if 1:
    # check available Super-Sboxes
    for name in ciphers:
        try:
            dc = DenseSet.load_from_file(f"data/{name}/divcore.set")
        except:
            continue

        print(f"using SSB: {name}")
        data[name] = SboxDivision.from_divcore(dc, dc.n//2, dc.n//2)


def main():
    if len(sys.argv) == 1:
        for name, sbox in sorted(data.items(), key=lambda v: v[1].n):
            if not isinstance(sbox, SboxDivision):
                print(f"{name} S-box ({sbox.n} -> {sbox.m})")
                # Wrapper for DivCore, useful to generate all other sets
                dc = SboxDivision(sbox)
            else:
                print(name, dc)
                dc = sbox

            process(name, dc)
    else:
        d = DenseSet.load_from_file(sys.argv[1])
        n, m = map(int, open(sys.argv[1][:-4] + ".dim").read().split())
        print("S-box DivCore from file:", sys.argv[1], "dimensions", n, m)

        dc = SboxDivision.from_divcore(d, n, m)
        process("input", dc)


def process(name, dc):
    # divcore
    # ===================================

    divcore = dc.divcore

    print("DivCore:", divcore)
    print("weight distribution:")
    stat = divcore.get_counts_by_weight_pairs(dc.n, dc.m)
    for (wl, wr), cnt in sorted(stat.items()):
        print((wl, wr), ":", cnt)
    print()

    # convex partition of all transitions
    # ===================================

    R = dc.redundant_min
    M = dc.minimal  # full convex set
    I = dc.invalid_max
    RA = dc.redundant_alternative_min

    print("I_S (full   LowerSet):", I.LowerSet())
    print("I_S (         MaxSet):", I.MaxSet())
    print()
    print("M_S (full convex set):", M)
    print("M_S (         MaxSet):", M.MaxSet())
    print("M_S (         MinSet):", M.MinSet())
    print()
    print("R_S (full   UpperSet):", R.UpperSet())
    print("R_S (         MinSet):", R.MinSet())
    print()
    print("R'_S(full   UpperSet):", RA.UpperSet())
    print("R'_S(         MinSet):", RA.MinSet())
    print()

    # sets form a partition
    assert (R.UpperSet() | M | I.LowerSet()).is_full()
    assert (R.UpperSet() & M).is_empty()
    assert (R.UpperSet() & I.LowerSet()).is_empty()
    assert (M & I.LowerSet()).is_empty()
    print()

    data = [
        dc.n, len(dc.min_dppt), len(dc.divcore), len(dc.invalid_max),
        len(dc.redundant_min), len(dc.redundant_alternative_min)
    ]
    data.append(data[3] + min(data[4], data[5]))
    data.append("-")

    def num(n):
        if len(str(n)) > 3:
            return r"\num{%d}" % n
        return str(n)

    print(f"\\scriptsize {name} & " + " & ".join(map(num, data)) + r" \\", file=sys.stderr)


if __name__ == '__main__':
    main()
