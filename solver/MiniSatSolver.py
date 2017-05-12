import pycosat
from solver.BaseSolver import BaseSolver
from utils import timed
from tempfile import NamedTemporaryFile
from subprocess import call
import Dimacs

class MiniSatSolver(BaseSolver):

    @staticmethod
    def name():
        return 'minisat'

    @staticmethod
    @timed("MiniSatSolver", "solve")
    def solve(n, clauses):

        res = call_minisat(n, clauses)
        if res and type(res) == type([]):
            return res


def call_minisat(n, clauses):
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    infile = NamedTemporaryFile(mode='w')
    outfile = NamedTemporaryFile(mode='r')
    Dimacs.Dimacs.write(n, clauses, infile)
    call("%s/minisat %s %s" % (dir_path, infile.name, outfile.name), shell=True)
    infile.close()
    lines = outfile.readlines()
    if lines[0].strip().startswith('SAT'):
        return [int(x) for x in lines[1].strip().split()]
    else:
        return "UNSAT"