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
    def solve(n, clauses):
        pass

class PycosatSolver(Solver):

    @staticmethod
    @timed("PycosatSolver", "solve")
    def solve(n, clauses):
        return pycosat.solve(clauses)
