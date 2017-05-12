from solver.PycosatSolver import PycosatSolver
from solver.MiniSatSolver import MiniSatSolver

class UnkownSatSolver(Exception): pass

class Solver(object):

    PYCOSAT_SOLVER = 0
    MINISAT_SOLVER = 1

    @staticmethod
    def get(solver):
        if solver == Solver.PYCOSAT_SOLVER:
            return PycosatSolver
        elif solver == Solver.MINISAT_SOLVER:
            return MiniSatSolver
        else:
            raise UnkownSatSolver

    @staticmethod
    def all_solvers():
        return {
            PycosatSolver.name(): Solver.PYCOSAT_SOLVER,
            MiniSatSolver.name() : Solver.MINISAT_SOLVER
        }
