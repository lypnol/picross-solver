from utils import timed
from model.BaseModel import BaseModel
from itertools import combinations_with_replacement


class ModelIKJ(BaseModel):

    @staticmethod
    def name():
        return 'ikj'

    @staticmethod
    @timed("ModelIKJ", "modelize")
    def modelize(n, line_blocks, col_blocks):
        var = 0
        clauses = set()

        reverse_index = {}
        col_index = []
        line_index = []

        for o, blocks in enumerate((line_blocks, col_blocks)):
            index = line_index
            o = (o+1)%2
            if not o:
                index = col_index

            for i in range(n):
                index.append([])
                for k, v in enumerate(blocks[i]):
                    index[i].append([])
                    for j in range(n-v+1):
                        var += 1
                        reverse_index[var] = (o, i, k, j)
                        index[i][k].append(var)

        for o, blocks in enumerate((line_blocks, col_blocks)):
            index = line_index
            other_index = col_index
            other_blocks = col_blocks
            o = (o+1)%2
            if not o:
                other_blocks = line_blocks
                other_index = line_index
                index = col_index

            for i in range(n):
                for k, v in enumerate(blocks[i]):
                    clauses.add(tuple([index[i][k][j] for j in range(n-v+1)]))

                    for j in range(n-v+1):

                        for l in range(n-v+1):
                            if l != j:
                                clauses.add((-index[i][k][j], -index[i][k][l]))

                        for k1, w in enumerate(blocks[i]):
                            if k1 != k:
                                for h in range(n-w+1):
                                    a, b = j, j+v-1
                                    x, y = max(0, h-1), min(n, h+w+1)-1
                                    if (max(a, x) <= min(b, y)):
                                        clauses.add((-index[i][k][j], -index[i][k1][h]))

                        if k > 0:
                            k1 = k-1
                            w = blocks[i][k1]
                            for h in range(j+v, n-w+1):
                                clauses.add((-index[i][k][j], -index[i][k1][h]))

                        for t in range(j, j+v):
                            c = [-index[i][k][j]]
                            for l, w in  enumerate(other_blocks[t]):
                                for h in range(n-w+1):
                                    if h <= i <= h+w-1:
                                        c.append(other_index[t][l][h])
                            clauses.add(tuple(c))

        return var, [list(c) for c in clauses], reverse_index

    @staticmethod
    @timed("ModelIKJ", "reverse")
    def sat_solution_to_grid(n, line_blocks, col_blocks, n_var, solution, index):
        grid = [[0 for _ in range(n)] for __ in range(n)]
        for var in solution:
            if var > 0:
                o, i, k, j = index[var]
                blocks = line_blocks if o else col_blocks
                v = blocks[i][k]
                for u in range(v):
                    if o:
                        grid[i][j+u] = 1
                    else:
                        grid[j+u][i] = 1
        return grid
