import pycosat
from solver.BaseSolver import BaseSolver
from utils import timed


class PycosatSolver(BaseSolver):

    @staticmethod
    def name():
        return 'pycosat'

    @staticmethod
    @timed("PycosatSolver", "solve")
    def solve(n, clauses):
        return pycosat.solve(clauses)
