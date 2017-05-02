from utils import timed

class BaseModel:

    @staticmethod
    def name():
        pass

    @staticmethod
    def modelize(n, line_blocks, col_blocks):
        pass

    @staticmethod
    def sat_solution_to_grid(n, n_var, solution, index):
        pass

class ModelAyoub(BaseModel):


    @staticmethod
    def name():
        return 'ayoub'

    @staticmethod
    @timed("ModelAyoub", "modelize")
    def modelize(n, line_blocks, col_blocks):
        n_var = 0
        clauses = []

        index = []
        for i in range(n):
            index.append([])
            for j in range(n):
                n_var += 1
                index[i].append(n_var)

        for i, block in enumerate(line_blocks):
            if n in block:
                for j in range(n):
                    clauses.append([index[i][j]])
            else:
                for k in block:
                    clauses.append([-index[i][j] for j in range(k)] + [-index[i][k]])
                    clauses.append([-index[i][n-1-k]] + [-index[i][n-k+j] for j in range(k)])
                    for j in range(1, n-k-1):
                        clauses.append([-index[i][j+u] for u in range(k)] + [-index[i][j+k]])
                        clauses.append([-index[i][j+u] for u in range(k)] + [-index[i][j-1]])
                clauses.append([index[i][j] for j in range(n)])

        for j, block in enumerate(col_blocks):
            if n in block:
                for i in range(n):
                    clauses.append([index[i][j]])
            else:
                for k in block:
                    clauses.append([-index[i][j] for i in range(k)] + [-index[k][j]])
                    clauses.append([-index[n-1-k][j]] + [-index[n-k+i][j] for i in range(k)])
                    for i in range(1, n-k-1):
                        clauses.append([-index[i+u][j] for u in range(k)] + [-index[i+k][j]])
                        clauses.append([-index[i+u][j] for u in range(k)] + [-index[i-1][j]])
                clauses.append([index[i][j] for i in range(n)])

        return n_var, clauses, index

    @staticmethod
    def sat_solution_to_grid(n, n_var, solution, index):
        index = {}
        var = 0
        for i in range(n):
            for j in range(n):
                var += 1
                index[var] = (i, j)

        grid = [[0]*n]*n
        for var in solution:
            i, j = index[abs(var)]
            grid[i][j] = 0 if var < 0 else 1

        return grid
