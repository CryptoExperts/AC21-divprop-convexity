from io import BytesIO
from copy import deepcopy
from tempfile import NamedTemporaryFile

from .base import CNF


@CNF.register("formula")
class Formula(CNF):
    def init_solver(self, solver=None):
        self.clauses = []

    def add_clause(self, c):
        self.n_clauses += 1
        self.clauses.append(c)

    def add_clauses(self, cs):
        self.n_clauses += len(cs)
        self.clauses.extend(cs)

    def write_dimacs(self, filename, assumptions=(), extra_clauses=()):
        clauses = self.clauses
        if assumptions or extra_clauses:
            clauses = self.clauses.copy()
            if assumptions:
                for v in assumptions:
                    clauses.append([v])
            if extra_clauses:
                clauses.extend(extra_clauses)
        # clauses.to_file(filename)
        raise NotImplementedError()


@CNF.register("writer")
class Writer(CNF):
    def init_solver(self, solver):
        self._file = BytesIO()
        self._solver = None

    def add_clause(self, c):
        self.n_clauses += 1
        self._file.write(b" ".join(b"%d" % v for v in c))
        self._file.write(b" 0\n")

    def add_clauses(self, cs):
        for c in cs:
            self.add_clause(c)

    def write_dimacs(self, filename, assumptions=(), extra_clauses=()):
        with open(filename, "wb") as f:
            n_clauses = self.n_clauses + len(assumptions) + len(extra_clauses)
            n_vars = self.n_vars
            f.write(b"p cnf %d %d\n" % (n_vars, n_clauses))

            f.write(self._file.getbuffer())

            if assumptions:
                for v in assumptions:
                    f.write(b"%d 0\n" % v)
            if extra_clauses:
                for c in extra_clauses:
                    f.write(b" ".join(b"%d" % v for v in c))
                    f.write(b" 0\n")

    def set_solver(self, solver):
        self._solver = solver

    def solve(self, assumptions=(), extra_clauses=(), log=True):
        assert self._solver, "solver not set"
        with NamedTemporaryFile() as f:
            self.write_dimacs(
                f.name,
                assumptions=assumptions,
                extra_clauses=extra_clauses,
            )
            return self._solver.solve_file(filename=f.name, log=log)

    def copy(self):
        return deepcopy(self)
