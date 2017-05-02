from Dimacs import Dimacs
from solver.Solver import Solver
from model.Model import Model


class InvalidArgument(Exception): pass

class Picross(object):

    @staticmethod
    def read_file(path):
        f = open(path)
        start = False
        comments = []
        line_blocks = []
        col_blocks = []
        n = 0
        for l in f:
            if l.startswith('c'):
                comments.append(l.strip())
            elif l.startswith('picross'):
                _, n_s = l.split()
                n = int(n_s)
                start = True
            elif len(line_blocks) < n:
                line_blocks.append(list(map(int, l.split()))[:-1])
            else:
                col_blocks.append(list(map(int, l.split()))[:-1])
        f.close()

        return n, line_blocks, col_blocks, comments

    def __init__(self, *args):
        if len(args) == 1:
            self.file_path = args[0]
            self.n, self.line_blocks, self.col_blocks, self.comments = Picross.read_file(self.file_path)
        elif len(args) == 3:
            self.n, self.line_blocks, self.col_blocks = args
            self.comments = []
        elif len(args) == 4:
            self.n, self.line_blocks, self.col_blocks, self.comments = args
        else:
            raise InvalidArgument
        self._modelized = {}
        self._dimacs = {}
        self._solved = {}

    def modelize(self, model=Model.MODEL_AYOUB):
        if model not in self._modelized:
            self._modelized[model] = Model.get(model).modelize(self.n, self.line_blocks, self.col_blocks)

        return self._modelized[model]

    def dimacs(self, model=Model.MODEL_AYOUB):
        if model not in self._dimacs:
            n, clauses, _ = self.modelize(model)
            self._dimacs[model] = Dimacs(n, clauses, self.comments)
        return self._dimacs[model]

    def solve(self, model=Model.MODEL_AYOUB, solver=Solver.PYCOSAT_SOLVER):
        n_var, _, index = self.modelize(model)
        if (model, solver) not in self._solved:
            sat_solution = self.dimacs(model).solve(solver)
            if sat_solution is None:
                self._solved[(model, solver)] = None
            else:
                self._solved[(model, solver)] = Model.get(model).sat_solution_to_grid(self.n, n_var, sat_solution, index)
        return self._solved[(model, solver)]

    def print_solution(self, model=Model.MODEL_AYOUB, solver=Solver.PYCOSAT_SOLVER):
        grid = self.solve(model, solver)
        n = len(grid)
        max_line_block = len(max(self.line_blocks, key=lambda x: len(x)))
        max_col_block = len(max(self.col_blocks, key=lambda x: len(x)))

        for i in range(max_col_block):
            line = []
            line.append(''.join([' ' for _ in range(max_line_block)]))
            line.append('|')
            for j in range(n):
                if max_col_block - i <= len(self.col_blocks[j]):
                    line.append(str(self.col_blocks[j][max_col_block - i - 1]))
                else:
                    line.append(' ')
            print(''.join(line))

        line = []
        line.append(''.join(['-' for _ in range(max_line_block)]))
        line.append('+')
        line.append(''.join(['-' for _ in range(n)]))
        print(''.join(line))

        for i in range(n):
            line = []
            for j in range(max_line_block):
                if max_line_block - j <= len(self.line_blocks[i]):
                    line.append(str(self.line_blocks[i][max_line_block - j - 1]))
                else:
                    line.append(' ')
            line.append('|')
            line.append(''.join('#' if grid[i][j] else ' ' for j in range(n)))
            print(''.join(line))

    def save_grid(self, model=Model.MODEL_AYOUB, solver=Solver.PYCOSAT_SOLVER, output=None):
        grid = self.solve(model, solver)
        output = output or (self.file_path.split('.')[0] + '-' +
                            Model.get(model).name() + '-' +
                            Solver.get(solver).name() + '.GRID')
        f = open(output, 'w')
        for c in self.comments:
            f.write('{}\n'.format(c))
        f.write('sol {} \n'.format(self.n))
        for row in grid:
            f.write('{} 0\n'.format(' '.join(['#' if c else ' ' for c in row])))
        f.close()

    def save_dimacs(self, model=Model.MODEL_AYOUB, output=None):
        n_var, clauses, _ = self.modelize(model)
        output = output or (self.file_path.split('.')[0] + '-' +
                            Model.get(model).name() + '.DIMACS')
        f = open(output, 'w')
        for c in self.comments:
            f.write('{}\n'.format(c))
        f.write('p cnf {} {}\n'.format(n_var, len(clauses)))
        for c in clauses:
            f.write('{} 0\n'.format(' '.join(map(str, c))))
        f.close()
