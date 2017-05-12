from solver.Solver import Solver


class InvalidArgument(Exception): pass

class Dimacs(object):

    @staticmethod
    def read_file(path):
        f = open(path)
        start = False
        n = 0
        n_clauses = 0
        clauses = []
        for l in f:
            if l.startswith('c'):
                comments.append(l.strip())
            elif l.startswith('p cnf'):
                _, _, n_s, n_c = l.split()
                n = int(n_s)
                n_clauses = int(n_c)
                start = True
            elif len(clauses) < n_clauses:
                clauses.append(list(map(int, l.split()))[:-1])
            else:
                break
        f.close()

        return n, clauses, comments

    def __init__(self, *args):
        if len(args) == 1:
            self.file_path = args[0]
            self.n, self.clauses, self.comments = Dimacs.read_file(self.file_path)
        elif len(args) == 2:
            self.n, self.clauses = args
            self.comments = []
        elif len(args) == 3:
            self.n, self.clauses, self.comments = args
        else:
            raise InvalidArgument
        self.solved = {}

    def solve(self, solver=Solver.PYCOSAT_SOLVER):
        self.solved[solver] = Solver.get(solver).solve(self.n, self.clauses)
        return self.solved[solver]

    @staticmethod
    def write(n, clauses, f):
        f.write('p cnf {} {}\n'.format(n, len(clauses)))
        for c in clauses:
            f.write('{} 0\n'.format(' '.join(map(str, c))))

