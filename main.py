from Picross import Picross
from model.Model import Model
from solver.Solver import Solver
import utils
import argparse


def main():
    parser = argparse.ArgumentParser(description='Picross solver.')
    parser.add_argument('picross', type=str, nargs='+',
                        help='input file in PICROSS format')
    parser.add_argument('-m', dest='model', type=str, nargs='*',
                        help='modelization method: ' + ' '.join(Model.all_models().keys()), default=['ayoub'])
    parser.add_argument('-s', dest='solver', type=str, nargs='*',
                        help='sat solver: ' + ' '.join(Solver.all_solvers().keys()), default=['pycosat'])
    parser.add_argument('-o', dest='output', type=str,
                        help='destination GRID file', default=None)
    parser.add_argument('--dimacs', dest='dimacs', action='store_true',
                        help='generate DIMACS file', default=False)
    parser.add_argument('--silent', dest='silent', action='store_true',
                        help='silent mode', default=False)

    args = parser.parse_args()

    models = Model.all_models()
    solvers = Solver.all_solvers()

    utils.set_silent(args.silent)

    for path in args.picross:
        picross = Picross(path)
        for model in args.model:
            if args.dimacs:
                picross.save_dimacs(model=models[model])
            for solver in args.solver:
                picross.print_solution(model=models[model], solver=solvers[solver])
                picross.save_grid(model=models[model], solver=solvers[solver], output=args.output)

if __name__ == '__main__':
    main()
