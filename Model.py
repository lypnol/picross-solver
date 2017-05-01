from utils import timed


class UknownPicrossModel(Exception): pass

class Model(object):

    MODEL_AYOUB = 0

    @staticmethod
    def get(model):
        if model == Model.MODEL_AYOUB:
            return ModelAyoub
        else:
            raise UknownPicrossModel

    @staticmethod
    def all_models():
        return {
            ModelAyoub.name(): Model.MODEL_AYOUB
        }

    @staticmethod
    def name():
        pass

    @staticmethod
    def modelize(n, line_blocks, col_blocks):
        pass

    @staticmethod
    def sat_solution_to_grid(n, n_var, solution):
        pass


class ModelAyoub(Model):

    @staticmethod
    def name():
        return 'ayoub'

    @staticmethod
    @timed("ModelAyoub", "modelize")
    def modelize(n, line_blocks, col_blocks):
        n_var = 0
        clauses = []

        for blocks in [line_blocks, col_blocks]:
            index = []
            for i in range(n):
                index.append([])
                for k in range(n):
                    index[i].append([])
                    for j in range(n - k):
                        n_var += 1
                        index[i][k].append(n_var)

            for i, block in enumerate(blocks):
                if n in block:
                    clauses.append([index[i][n-1][0]])
                else:
                    for k in block:
                        clauses.append([-index[i][k-1][0], -index[i][0][n-k]])
                        clauses.append([-index[i][k-1][n-k], -index[i][0][n-k-1]])
                        for j in range(1, n-k-1):
                            clauses.append([-index[i][k-1][j], index[i][0][j-1], -index[i][0][j+k]])
                            clauses.append([-index[i][k-1][j], index[i][0][j+k], -index[i][0][j-1]])

        return n_var, clauses

    @staticmethod
    def sat_solution_to_grid(n, n_var, solution):
        index = {}
        var = 0
        for _ in range(2):
            for i in range(n):
                for k in range(n):
                    for j in range(n - k):
                        var += 1
                        index[var] = (i, k, j)

        grid = [[0]*n]*n
        for var in solution:
            if abs(var) <= n_var // 2:
                i, k, j = index[abs(var)]
                for u in range(k + 1):
                    grid[i][j + u] = 0 if var < 0 else 1
            else:
                i, k, j = index[abs(var)]
                for u in range(k + 1):
                    grid[j + u][i] = 0 if var < 0 else 1

        return grid
