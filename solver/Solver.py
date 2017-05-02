from solver.PycosatSolver import PycosatSolver


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
