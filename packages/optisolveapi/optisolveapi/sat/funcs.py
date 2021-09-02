from .simple import Formula


def ConvexFormula(lb: "DenseSet" = None, ub: "DenseSet" = None):
    C = Formula()
    assert lb is not None or ub is not None
    if lb is not None:
        n = lb.n
    elif ub is not None:
        n = ub.n
    x = C.vars(n)
    C.constraint_convex(x, lb=lb, ub=ub)
    return C
