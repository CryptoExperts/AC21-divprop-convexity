import argparse

from subsets import DenseSet

import logging


def tool_setinfo():
    log = logging.getLogger("subsets.setinfo")

    logging.basicConfig(level="INFO")

    parser = argparse.ArgumentParser(
        description="Print information about a set (from file)."
    )

    parser.add_argument(
        "filename", type=str, nargs="+",
        help="File with set",
    )
    parser.add_argument(
        "-p", "--print", action="store_true",
        help="Print full set",
    )
    parser.add_argument(
        "-s", "--short", action="store_true",
        help="Print one-line description per set",
    )
    args = parser.parse_args()

    # log.info(args)
    if args.short:
        DenseSet.set_quiet()

    mxlen = max(map(len, args.filename))
    for filename in args.filename:
        if not args.short:
            log.info(f"set file {filename}")
        s = DenseSet.load_from_file(filename)

        log.info(f"{filename.rjust(mxlen)}: {s}")
        if args.short:
            continue

        stat = s.get_counts_by_weights()

        log.info("stat by weights:")
        for u, cnt in enumerate(stat):
            log.info(f"{u} : {cnt}")

        if s.n % 2 == 0:
            n = s.n // 2
            pair_stat = s.get_counts_by_weight_pairs(n, n)
            log.info("stat by pairs:")
            for (u, v), cnt in sorted(pair_stat.items()):
                log.info(f"{u} {v} : {cnt}")

        if args.print:
            print(*s)

        log.info("")
