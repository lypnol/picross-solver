import pycosat
from utils import timed


class UnkownSatSolver(Exception): pass

class Solver(object):

    PYCOSAT_SOLVER = 0

    @staticmethod
    def get(solver):
        if solver == Solver.PYCOSAT_SOLVER:
            return PycosatSolver
        else:
            raise UnkownSatSolver

    @staticmethod
    def all_solvers():
        return {
            PycosatSolver.name(): Solver.PYCOSAT_SOLVER
        }

    @staticmethod
    def name():
        pass

    @staticmethod
    def solve(n, clauses):
        pass

class PycosatSolver(Solver):

    @staticmethod
    def name():
        return 'pycosat'

    @staticmethod
    @timed("PycosatSolver", "solve")
    def solve(n, clauses):
        return pycosat.solve(clauses)
