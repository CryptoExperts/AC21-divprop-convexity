'''
06:57:46.970 DEBUG __main__:HeavyPeeks: run #3089 fset frozenset({3, 4, 30, 23}) inv? True
06:57:54.573 INFO __main__:HeavyPeeks: computed divcore n=32 in 3089 bit-ANF calls, stat 1:32 2:490 3:998 4:33 1:32 2:489 3:990 4:25, size 7152
06:57:54.621 INFO __main__: computed divcore: 7152 elements

real    417m56.201s
user    402m38.419s
sys 9m6.920s
'''

import os
import gc
import subprocess
import pickle
import argparse
import gzip

from binteger import Bin

from subsets import DenseSet
from divprop.lib import Sbox, Sbox32
from divprop.WeightedSetInts import WeightedSetInts

from divprop import SboxDivision, SboxPeekANFs

import logging
import justlogs

log = logging.getLogger(f"{__name__}:RandomSboxBenchmark")


class HeavyPeeks(SboxPeekANFs):
    log = logging.getLogger(f"{__name__}:HeavyPeeks")

    def __init__(self, n, fws, bks, cache_dir=None, memorize=False):
        self.n = int(n)
        self.cache_dir = cache_dir
        if memorize:
            self.log.info("loading forward coordinates to memory")
            self.fws = [DenseSet.load_from_file(f) for f in fws]
            self.log.info("loading backward coordinates to memory")
            self.bks = [DenseSet.load_from_file(f) for f in bks]
            self.log.info("loaded to memory done")
        else:
            self.fws = fws
            self.bks = bks
        self.memorize = memorize

    def get_coord(self, i, inverse):
        lst = self.bks if inverse else self.fws
        if self.memorize:
            return lst[i]
        else:
            return DenseSet.load_from_file(lst[i])

    def get_product(self, mask, inverse):
        cur = DenseSet(self.n)
        cur.fill()
        for i in Bin(mask, self.n).support:
            cur &= self.get_coord(i, inverse)
        return cur

    def run_mask(self, mask, inverse=False):
        self.n_queries += 1
        if self.cache_dir is not None:
            str_mask = f"{mask:x}".zfill((self.n + 3) // 4)
            filename = os.path.join(
                self.cache_dir, f"{str_mask}_{['fw','bk'][inverse]}"
            )
            if os.path.isfile(filename):
                with open(filename, "rb") as f:
                    try:
                        return pickle.load(f)
                    except Exception as err:
                        log.warning(f"cache error: file {filename} err {err}")
                        pass

        self.log.debug(
            f"run #{self.n_queries} mask {Bin(mask, self.n).support} "
            f"inv? {inverse} "
            f"queue ({self.queue.qsize()})"
        )
        ret = super().run_mask(mask, inverse)

        if self.cache_dir is not None:
            with open(filename, "wb") as f:
                pickle.dump(ret, f)

        return ret


def reduntant_from_divcore(divcore, n, m):
    redundant = WeightedSetInts(n + m)
    for v in divcore:
        for j in range(m):
            if v & (1 << j) == 0:
                redundant.add(v | (1 << j))
    log.info(f"reducing redundant: {len(divcore)} x m -> {len(redundant)}")
    redundant.do_MinSet()
    # ret = []
    # for v in redundant:
    #     if any(v.is_succ(u) for u in redundant):
    #         continue
    #     ret.append(v)
    log.info(f"reduced: {len(redundant)}")
    return list(redundant)


def tool_RandomSboxBenchmark():
    global log

    parser = argparse.ArgumentParser(
        description="Generate division core of a random S-box for benchmark."
    )

    parser.add_argument(
        "n", type=int,
        help="bit size of the S-box",
    )
    parser.add_argument(
        "-l", "--large", action="store_true",
        help="Large S-box (use extensive caching and files)",
    )
    parser.add_argument(
        "-s", "--seed", type=str, default="2021",
        help="Seed for S-box generation",
    )
    parser.add_argument(
        "-o", "--output", type=str, default="divcore_random",
        help="Base directory for files (logs, cache, divcore, etc.)",
    )

    args = parser.parse_args()

    n = args.n
    seed = int(args.seed)

    path = os.path.join(args.output, f"{n:02d}")
    os.makedirs(path, exist_ok=True)

    justlogs.addFileHandler(f"{path}/log")
    justlogs.setup(level="DEBUG")

    log.info(f"{args}")

    if args.large:
        run_large(n, path, seed)
    else:
        run_small(n, path, seed)


def run_large(n, path, seed):
    filename = f"{path}/fw.sbox"
    ifilename = f"{path}/bk.sbox"
    last_filename = f"{path}/bk{n-1}.set"

    if not os.path.isfile(last_filename):
        log.info(f"generating {n}-bit S-box...")
        sbox = Sbox32.GEN_random_permutation(n, seed)  # seed
        log.info(f"{sbox}")

        log.info(f"saving to {filename} ...")
        sbox.save_to_file(filename)

        log.info("hashing...")
        h = subprocess.check_output(["sha256sum", filename]).split()[0]
        log.info(f"sha256sum: {h}")

        log.info("splitting into coordinates...")
        for i in range(n):
            coord = sbox.coordinate(i)
            coord.save_to_file(f"{path}/fw{i}.set")
            log.info(f"coord {i}/{n} saved")

        log.info("inverting...")
        # somehow ~sbox caused extra (temporary) instance
        isbox = sbox
        del sbox
        isbox.invert_in_place()
        gc.collect()

        log.info(f"saving to {ifilename} ...")
        isbox.save_to_file(ifilename)

        log.info("hashing...")
        h = subprocess.check_output(["sha256sum", ifilename]).split()[0]
        log.info(f"sha256sum: {h}")

        log.info("splitting into coordinates...")
        for i in range(n):
            coord = isbox.coordinate(i)
            coord.save_to_file(f"{path}/bk{i}.set")
            log.info(f"coord {i}/{n} saved")

        del isbox
        gc.collect()

    log.info("heavy peeks")
    fws = [f"{path}/fw{i}.set" for i in range(n)]
    bks = [f"{path}/bk{i}.set" for i in range(n)]

    cache_dir = f"{path}/cache/"
    os.makedirs(cache_dir, exist_ok=True)
    pa = HeavyPeeks(n, fws, bks, cache_dir=cache_dir, memorize=True)

    divcore, lb = pa.compute()
    divcore = sorted(divcore)
    lb = sorted(lb)
    ub = sorted(reduntant_from_divcore(divcore, n=n, m=n))

    divcore_file = f"{path}/divcore.txt.gz"
    lb_file = f"{path}/lb.txt.gz"
    ub_file = f"{path}/ub.txt.gz"
    log.info(f"divcore: {len(divcore)} elements, saving to {divcore_file} ...")
    log.info(f"lb: {len(lb)} elements, saving to {lb_file} ...")
    log.info(f"ub: {len(ub)} elements, saving to {ub_file} ...")

    with gzip.open(divcore_file, "wt") as f:
        print(len(divcore), file=f)
        for uv in divcore:
            print(int(uv), file=f, end=" ")

    with gzip.open(lb_file, "wt") as f:
        print(len(lb), file=f)
        for uv in lb:
            print(int(uv), file=f, end=" ")

    with gzip.open(ub_file, "wt") as f:
        print(len(ub), file=f)
        for uv in ub:
            print(int(uv), file=f, end=" ")

    log.info("finished")


def run_small(n, path, seed):
    assert n < 24, "are you crazy?"

    log.info(f"generating {n}-bit S-box...")
    sbox = Sbox32.GEN_random_permutation(n, seed)
    log.info(f"{sbox}")

    filename = f"{path}/fw.sbox"
    log.info(f"saving to {filename} ...")
    sbox.save_to_file(filename)

    log.info("hashing...")
    h = subprocess.check_output(["sha256sum", filename])
    log.info(f"sha256sum: {h}")

    log.info("computing division core...")
    pa = SboxPeekANFs(sbox)
    log.info("sorting...")

    divcore, lb = pa.compute()
    divcore = sorted(divcore)
    lb = sorted(lb)
    ub = sorted(reduntant_from_divcore(divcore, n=n, m=n))

    divcore_file = f"{path}/divcore.txt.gz"
    lb_file = f"{path}/lb.txt.gz"
    ub_file = f"{path}/ub.txt.gz"
    log.info(f"divcore: {len(divcore)} elements, saving to {divcore_file} ...")
    log.info(f"lb: {len(lb)} elements, saving to {lb_file} ...")
    log.info(f"ub: {len(ub)} elements, saving to {ub_file} ...")

    with gzip.open(divcore_file, "wt") as f:
        print(len(divcore), file=f)
        for uv in divcore:
            print(int(uv), file=f, end=" ")

    with gzip.open(lb_file, "wt") as f:
        print(len(lb), file=f)
        for uv in lb:
            print(int(uv), file=f, end=" ")

    with gzip.open(ub_file, "wt") as f:
        print(len(ub), file=f)
        for uv in ub:
            print(int(uv), file=f, end=" ")

    log.info("testing...")

    if n <= 16:
        ans = sorted(SboxDivision(sbox).divcore.to_Bins())
        assert divcore == ans
        ans = sorted(SboxDivision(sbox).invalid_max.to_Bins())
        assert lb == ans
        ans = sorted(SboxDivision(sbox).redundant_min.to_Bins())
        assert ub == ans
        log.info("sanity check ok! (n <= 16)")

    log.info("finished")


if __name__ == '__main__':
    tool_RandomSboxBenchmark()
