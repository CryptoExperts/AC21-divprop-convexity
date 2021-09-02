from tempfile import NamedTemporaryFile

from optisolveapi.sat import ExtSolver


UNSAT = """
p cnf 2 4
-1 2 0
2 -1 0
-1 0
1 0
""".strip()

SAT = """
p cnf 2 2
-1 2 0
2 -1 0
""".strip()


def test_ext():
    K = ExtSolver.new(solver="kissat")
    with NamedTemporaryFile("w") as f:
        f.write(UNSAT)
        f.flush()
        assert K.solve_file(f.name) is False

    with NamedTemporaryFile("w") as f:
        f.write(SAT)
        f.flush()
        assert K.solve_file(f.name)
