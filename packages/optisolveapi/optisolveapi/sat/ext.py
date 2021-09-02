import logging
import subprocess

from .base import CNF


class ExtSolver(CNF):
    BY_SOLVER = {}

    log = logging.getLogger(f"{__name__}:ExtSolver")

    CMD = NotImplemented

    def __init__(self, flags=(), solver=None):
        self.flags = flags

    def solve_file(self, filename, log=True):
        cmd = [filename if v == "<DIMACS_FILE>" else v for v in self.CMD]
        pos = cmd.index("<FLAGS>")
        cmd[pos:pos+1] = list(self.flags)

        # self.log.info(f"command {cmd}")
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE,
        )
        ret = None
        sol = []
        while True:
            line = p.stdout.readline()
            if not line:
                break
            if not line.strip():
                continue

            if log:
                self.log.debug(line)
                # print(line)

            if line[:1] == b"s":
                res = line.split()[1]
                if res == b"SATISFIABLE":
                    # self.log.info("SAT")
                    ret = True
                elif res == b"UNSATISFIABLE":
                    # self.log.info("UNSAT")
                    ret = False
                else:
                    raise RuntimeError(f"unknown status {res}")
            elif line[:1] == b"v":
                sol.extend(map(int, line[1:].split()))
            elif line[:1] == b"c":
                pass
            else:
                self.log.warning(f"unknown line type {line[:1]}: {line} ")
        if ret is None:
            raise RuntimeError("Solver did not solve")
        # self.log.debug(f"ret {ret} sol {sol}")
        if ret is True:
            assert len(set(map(abs, sol))) == len(sol)
            assert ret is True
            return {abs(v): int(v > 0) for v in sol}
        return False


@ExtSolver.register("kissat")
class Kissat(ExtSolver):
    CMD = [
        "kissat",
        "<FLAGS>",
        "<DIMACS_FILE>",
    ]
