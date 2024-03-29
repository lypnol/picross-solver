from model.BaseModel import BaseModel
from utils import timed
import re

class ModelSpots(BaseModel):

    @staticmethod
    def name():
        return 'spots'

    @staticmethod
    @timed("ModelSpots", "modelize")
    def modelize(n, line_blocks, col_blocks):
        return picross_to_dimacs((n, line_blocks, col_blocks))

    @staticmethod
    @timed("ModelSpots", "sat_solution_to_grid")
    def sat_solution_to_grid(n, line_blocks, col_blocks, n_var, solution, index):
        grille_sol = [[0 for _ in range(n)] for _2 in range(n)]
        for v in solution:
            var_name = index[abs(v)]
            if var_name is not None:
                if 'x' in var_name:
                    i, j = get_coords_from_string(var_name)
                    grille_sol[i][j] = 1 if v > 0 else 0
        return grille_sol

class And(list):
    def __repr__(self):
        return "(" + " ∧ ".join(str(x) for x in self) + ")"

class Or(list):
    def __repr__(self):
        return "(" + " ∨ ".join(str(x) for x in self) + ")"

class Literal:
    def __init__(self, name, truth=True):
        self.name = str(name)
        self.truth = truth

    def to_string(self):
        truth = "" if self.truth else "-"
        return truth + self.name

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def inverted(self):
        return Literal(self.name, not self.truth)

    def __eq__(self, other):
        return self.name == other.name and self.truth == other.truth

assert (Literal('x') == Literal('x'))
assert (Literal('x')) != Literal('x', False)
assert (Literal('x')) != Literal('y')
assert (Literal('x') == Literal('x', False).inverted())


def PicrossLiteral(i, j, truth):
    return Literal("x_{i}_{j}".format(
            i=i,
            j=j
        ), truth)


def get_all_possible_rec(current, restants, size):
    if restants == []:
        return [current + [0] * (size - len(current))]
    a = restants[0]
    i = len(current)  # position courante
    possibles = []
    j = 0  # combien de 0 avant d'ajouter l'élément
    while i + j + a <= size:
        p = current + [0] * j + [1] * a
        if len(p) < size:
            p.append(0)
        possibles.append(p)
        j += 1
    result = []
    for p in possibles:
        r = get_all_possible_rec(p, restants[1:], size)
        result.extend(r)
    return result

def get_all_possible(coefficients, size):
    return get_all_possible_rec([], coefficients, size)

def convert_to_dnf(possibles, line=None, column=None):
    if line is None and column is None:
        raise Exception("no line or column")
    return Or([
        And([
            PicrossLiteral(line if line is not None else j,
                           column if column is not None else j,
                           truth=bool(x))
            for j, x in enumerate(p)
        ])
        for p in possibles
    ])

a = get_all_possible_rec([], [1, 1], 5)

def get_all_dnfs(picross):
    formulas = {}
    size, lines, columns = picross
    for i, l in enumerate(lines):
        formulas["l" + str(i)] = convert_to_dnf(get_all_possible(l, size), line=i)

    for i, c in enumerate(columns):
        formulas["c" + str(i)] = convert_to_dnf(get_all_possible(c, size), column=i)

    print("******************dnfs done*******************")

    print(len(formulas))
    return formulas

def dnf_to_cnf(dnf, id):
    """
    prend une dnf sous la forme d'une liste de liste de literaux : Or(And(x1, x2), And(x2, x5))
    ie
    :return: meme format, en CNF
    """
    n = len(dnf)
    l = Literal(id, True)

    # cas particulier
    if len(dnf) == 1:
        and_clause = dnf[0]
        return And([Or([x]) for x in and_clause])


    # variables pour chaque ligne / colonne
    new_variables = [
        Literal("{id}_{i}".format(id=id, i=i)) if len(dnf[i]) > 1 
        else dnf[i][0]
        for i in range(n)]


    result = And([])

    # l1 v l1 v ...
    result.append(Or(new_variables))
    
    # specific clauses
    for i in range(n):
        l_i = new_variables[i]
        # l_i <=> dnf[i] <=> x1 ^ x2 ^ x3
        # revient à
        # l_i => dnf[i] == -l_i v (x1 ^ x2 ^ ..)
        if len(dnf[i]) > 1:
            result.append(Or([l_i] + [x.inverted() for x in dnf[i]]))
            for v in dnf[i]:
                result.append(Or([l_i.inverted(), v]))
        else:
            result.append(Or([x for x in dnf[i][0]]))
    return result

def get_all_cnfs(dnfs):
    cnfs = {}
    for i, line in enumerate(dnfs):
        cnfs[line] = dnf_to_cnf(dnfs[line], line)
    return cnfs

def flatten_cnfs(cnfs):
    print("**** flattening cnf*********")
    result = And([])
    for key in cnfs:
        result.extend(cnfs[key])
    print("done flattening cnfs")
    return result

def cnf_to_dimacs(cnf):
    print("converting to dimacs")
    # list variables
    variables = set()
    for i, clause in enumerate(cnf):
        for lit in clause:
            if lit.name not in variables:
                variables.add(lit.name)
    print("done enumerating variables")
    variables = list(variables)
    # put ids in dict
    variables_dict = {}
    for i, v in enumerate(variables):
        variables_dict[v] = i + 1

    n_var = len(variables)
    clauses_dimacs = []
    # to dimacs
    # dimacs = "p cnf {n_var} {n_clause}\n".format(n_var=len(variables), n_clause=len(cnf))
    for clause in cnf:
        line_dimacs = []
        for lit in clause:
            var = (1 if lit.truth else -1) * variables_dict[lit.name]
            line_dimacs.append(var)
        clauses_dimacs.append(line_dimacs)
    print("done converting")
    return n_var, clauses_dimacs, [None] + variables


def picross_to_dimacs(picross):
    return cnf_to_dimacs(flatten_cnfs(get_all_cnfs(get_all_dnfs(picross))))

def get_coords_from_string(str):
    reg = 'x_([0-9]+)_([0-9]+)'
    m = re.match(reg, str)
    if m:
        i, j = [int(x) for x in m.groups()]
        return i, j