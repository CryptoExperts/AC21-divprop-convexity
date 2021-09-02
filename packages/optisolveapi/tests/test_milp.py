import time

from optisolveapi.milp import (
    MILP, MILPX,
    has_scip, has_sage, has_gurobi, has_swiglpk,
)


def test_milp():
    solvers = []
    if has_scip:
        solvers.append("scip")
    if has_sage:
        solvers.append("sage/glpk")
        solvers.append("sage/coin")
        if has_gurobi:
            solvers.append("sage/gurobi")
    if has_gurobi:
        solvers.append("gurobi")

    # solvers.append("external/glpk")

    for i in range(2):
        for solver in solvers:
            t0 = time.time()
            check_solver(solver)
            print("solver", solver, "elapsed", f"{time.time() - t0:.3f}")
        print()

        assert has_swiglpk
        check_milpx("swiglpk")


def check_solver(solver):
    print("SOLVER", solver)
    if 0:
        milp = MILP.maximization(solver=solver)
        x = milp.var_int("x", 3, 7)
        y = milp.var_int("y", 2, 4)

        milp.set_objective(2*x)

        assert 14 == milp.optimize()
        assert milp.solutions
        for sol in milp.solutions:
            assert sol[x] == 7

    # ==================================

    milp = MILP.maximization(solver=solver)
    x = milp.var_int("x", 3, 7)
    y = milp.var_int("y", 2, 4)
    milp.set_objective(-3*y)

    assert -6 == milp.optimize()
    assert milp.solutions
    for sol in milp.solutions:
        assert sol[y] == 2

    milp.add_constraint(x + y >= 9)

    obj = milp.optimize()
    assert -6 == obj, obj
    assert milp.solutions
    for sol in milp.solutions:
        assert sol[y] == 2

    for i in range(100):
        c1 = milp.add_constraint(x + y >= 10)

        assert -9 == milp.optimize()
        assert milp.solutions
        for sol in milp.solutions:
            assert sol[y] == 3

        milp.remove_constraint(c1)
        obj = milp.optimize()
        assert -6 == obj, obj
        assert milp.solutions
        for sol in milp.solutions:
            assert sol[y] == 2

        c2 = milp.add_constraint(x + y == 10)

        assert -9 == milp.optimize()
        assert milp.solutions
        for sol in milp.solutions:
            assert sol[y] == 3

        milp.remove_constraint(c2)
        obj = milp.optimize()
        assert -6 == obj, obj
        assert milp.solutions
        for sol in milp.solutions:
            assert sol[y] == 2


def check_milpx(solver):
    print("SOLVER", solver)
    if 0:
        milp = MILPX.maximization(solver=solver)
        x = milp.var_int("x", 3, 7)
        y = milp.var_int("y", 2, 4)

        milp.set_objective({x: 2})

        assert 14 == milp.optimize(log=True)
        assert milp.solutions
        for sol in milp.solutions:
            assert sol[x] == 7

    if 1:
        print("Bug test")
        # was bug
        S = MILPX.feasibility(solver=solver)
        x0 = S.var_real("x0", lb=None, ub=None)
        x1 = S.var_real("x1", lb=None, ub=None)
        x2 = S.var_real("x2", lb=None, ub=None)
        c = S.var_real("c", lb=None, ub=None)

        S.add_constraint({'x0': 0, 'x1': 0, 'c': -1}, lb=0, ub=None)
        S.add_constraint({'x0': 0, 'x1': 1, 'c': -1}, lb=0, ub=None)
        S.add_constraint({'x0': -1, 'x1': 0, 'c': -1}, lb=None, ub=-1)
        S.add_constraint({'x0': 2, 'x1': 2, 'c': -1}, lb=None, ub=-1)

        assert S.optimize() is False
        print("Bug test ok")

    # ==================================

    milp = MILPX.maximization(solver=solver)
    x = milp.var_int("x", 3, 7)
    y = milp.var_int("y", 2, 4)
    milp.set_objective({y: -3})

    assert -6 == milp.optimize()
    assert milp.solutions
    for sol in milp.solutions:
        assert sol[y] == 2

    milp.add_constraint({x: 1, y: 1}, lb=9)

    obj = milp.optimize(log=1)
    assert -6 == obj, obj
    assert milp.solutions
    for sol in milp.solutions:
        assert sol[y] == 2

    for i in range(100):
        c1 = milp.add_constraint({x: 1, y: 1}, lb=10)

        assert -9 == milp.optimize(log=1)
        assert milp.solutions
        for sol in milp.solutions:
            assert sol[y] == 3

        milp.remove_constraint(c1)
        obj = milp.optimize(log=1)
        assert -6 == obj, obj
        assert milp.solutions
        for sol in milp.solutions:
            assert sol[y] == 2

        c2 = milp.add_constraint({x: 1, y: 1}, lb=10)

        assert -9 == milp.optimize(log=1)
        assert milp.solutions
        for sol in milp.solutions:
            assert sol[y] == 3

        milp.remove_constraint(c2)
        obj = milp.optimize(log=1)
        assert -6 == obj, obj
        assert milp.solutions
        for sol in milp.solutions:
            assert sol[y] == 2

    milp = MILPX.feasibility(solver=solver)
    x = milp.var_int("x", 1, 5)
    y = milp.var_int("y", 5, 10)
    z = milp.var_int("z", -100, 20)

    # 2 8 17
    for i in range(100):
        up = [
            milp.add_constraint({x: 1, y: 3}, ub=26),
            milp.add_constraint({x: 3, y: 1}, ub=14),
            milp.add_constraint({x: 1, y: 2, z: -2}, ub=-16),
        ]

        lo = [
            milp.add_constraint({x: 1, y: 3}, lb=24),
            milp.add_constraint({x: 3, y: 1}, lb=10),
            milp.add_constraint({x: 1, y: 2, z: -2}, lb=-16),
        ]

        obj = milp.optimize(log=1)
        assert obj is True, obj
        assert milp.solutions

        bad = milp.add_constraint({x: 1, y: 3}, lb=30)

        top = [
            milp.add_constraint({x: 1, y: 2, z: 3}, ub=1000),
            milp.add_constraint({x: 2, y: 4, z: 5}, ub=1001),
            milp.add_constraint({x: 4, y: 2, z: 1}, ub=1002),
        ]

        obj = milp.optimize(log=1)
        assert obj is False, obj
        assert not milp.solutions

        milp.remove_constraints(lo)

        obj = milp.optimize(log=1)
        assert obj is False, obj
        assert not milp.solutions

        milp.remove_constraint(bad)

        obj = milp.optimize(log=1)
        assert obj is True, obj
        assert milp.solutions

        milp.remove_constraints(up)

        obj = milp.optimize(log=1)
        assert obj is True, obj
        assert milp.solutions

        if i < 90:
            milp.remove_constraints(top)


# reopt is buggy..
def disabled_test_scip_reopt():
    if not has_scip:
        return

    milp = MILP.maximization(solver="scip")
    milp.set_reopt()

    x = milp.var_int("x", 3, 7)
    y = milp.var_int("y", 2, 4)
    milp.set_objective(-3*y)

    assert -6 == milp.optimize()
    assert milp.solutions
    for sol in milp.solutions:
        assert sol[y] == 2

    milp.add_constraint(x + y >= 9)

    obj = milp.optimize()
    assert -6 == obj, obj
    assert milp.solutions
    for sol in milp.solutions:
        assert sol[y] == 2

    milp.add_constraint(x + y >= 10)

    assert -9 == milp.optimize()
    assert milp.solutions
    for sol in milp.solutions:
        assert sol[y] == 3

    milp.add_constraint(x + y >= 11)

    assert -12 == milp.optimize()
    assert milp.solutions
    for sol in milp.solutions:
        assert sol[y] == 4

    milp.add_constraint(x + y >= 12)

    assert None is milp.optimize()
    assert not milp.solutions


if __name__ == '__main__':
    # test_milp()
    check_milpx("swiglpk")
