from BaseModel import BaseModel
from utils import timed
import re

class ModelCoco(BaseModel):

    @staticmethod
    def name():
        return 'coco'

    @staticmethod
    @timed("ModelCoco", "modelize")
    def modelize(n, line_blocks, col_blocks):
        return picross_to_dimacs((n, line_blocks, col_blocks))

    @staticmethod
    def get_coords_from_string(str):
        reg = 'x_([0-9]+)_([0-9]+)'
        m = re.match(reg, str)
        if m:
            i, j = [int(x) for x in m.groups()]
            return i, j

    @staticmethod
    @timed("ModelCoco", "sat_solution_to_grid")
    def sat_solution_to_grid(n, n_var, solution, index):

        grille_sol = [[0 for _ in range(n)] for _2 in range(n)]

        for v in solution:
            var_name = index[abs(v)]
            if 'x' in var_name:
                i, j = ModelCoco.get_coords_from_string(var_name)
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

class PicrossLiteral(Literal):

    def __init__(self, i, j, truth):
        self.i = i
        self.j = j
        self.truth = truth

    @property
    def name(self):
        return "x_{i}_{j}".format(
            i=self.i,
            j=self.j
        )

    def inverted(self):
        return PicrossLiteral(self.i, self.j, not self.truth)

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

    return formulas

def dnf_to_cnf(dnf, id):
    """
    prend une dnf sous la forme d'une liste de liste de literaux
    ie 
    :return: meme format, en CNF
    """
    n = len(dnf)
    l = Literal(id, True)

    # variables pour chaque ligne / colonne
    new_variables = [Literal("{id}_{i}".format(id=id, i=i)) for i in range(n)]

    result = And([])
    # first global literal
    result.append(Or([l]))

    # l => l1 v l1 v ...
    result.append(Or([l.inverted()] + new_variables))
    # l <= l1 v l2 ... == (l v -l1) ^ (l v -l2) ...
    for v in new_variables:
        result.append(Or([l, v.inverted()]))

    # specific clauses
    for i in range(n):
        l_i = new_variables[i]
        # l_i <=> dnf[i]
        # revient à
        # l_i => dnf[i] == -l_i v (x1 ^ x2 ^ ..)
        result.append(Or([l_i] + [x.inverted() for x in dnf[i]]))
        for v in dnf[i]:
            result.append(Or([l_i.inverted(), v]))
    return result

def get_all_cnfs(dnfs):
    cnfs = {}
    for line in dnfs:
        cnfs[line] = dnf_to_cnf(dnfs[line], line)
    return cnfs

def flatten_cnfs(cnfs):
    result = And([])
    for key in cnfs:
        result.extend(cnfs[key])
    return result

def cnf_to_dimacs(cnf):
    # list variables
    variables = []
    for clause in cnf:
        for lit in clause:
            if lit.name not in variables:
                variables.append(lit.name)
    # put ids in dict
    variables_dict = {}
    for i, v in enumerate(variables):
        variables_dict[v] = i + 1

    n_var = len(variables)
    clauses_dimacs = []

    # to dimacs
    dimacs = "p cnf {n_var} {n_clause}\n".format(n_var=len(variables), n_clause=len(cnf))
    for clause in cnf:
        line_dimacs = []
        for lit in clause:
            var = (1 if lit.truth else -1) * variables_dict[lit.name]
            line_dimacs.append(var)
        clauses_dimacs.append(line_dimacs)
    return n_var, clauses_dimacs, [None] + variables


def picross_to_dimacs(picross):
    return cnf_to_dimacs(flatten_cnfs(get_all_cnfs(get_all_dnfs(picross))))

def output_to_result(output, variable):
    vars = output.split()

    for v in vars:
        if v == "0":
            break
        if v.startswith("-"):
            print(variable[int(v[1:])] + " : false")
        else:
            print(variable[int(v)] + " : true")

