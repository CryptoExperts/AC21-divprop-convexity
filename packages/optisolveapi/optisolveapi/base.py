import logging

log = logging.getLogger(__name__)


class SolverBase:
    BY_SOLVER = NotImplemented  # to be defined in the collection class

    @classmethod
    def register(cls, name):
        def deco(subcls):
            if name in cls.BY_SOLVER:
                log.warning(
                    f"re-registering solver {name} in class {cls.__name__}"
                )
            cls.BY_SOLVER[name.lower()] = subcls
            return subcls
        return deco

    @classmethod
    def new(cls, *args, solver, **opts):
        return cls.BY_SOLVER[solver.lower()](
            *args,
            solver=solver,
            **opts
        )
