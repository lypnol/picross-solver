from Picross import Picross
from Model import Model
from Solver import Solver
import utils
import argparse


def main():
    parser = argparse.ArgumentParser(description='Picross solver.')
    parser.add_argument('picross', type=str, nargs='+',
                        help='input file in PICROSS format')
    parser.add_argument('-m', dest='model', type=str,
                        help='modelization method: ' + ' '.join(Model.all_models().keys()), default='ayoub')
    parser.add_argument('-s', dest='solver', type=str,
                        help='sat solver: ' + ' '.join(Solver.all_solvers().keys()), default='pycosat')
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
        if args.dimacs:
            picross.save_dimacs(model=models[args.model])
        picross.print_solution(model=models[args.model], solver=solvers[args.solver])
        picross.save_grid(model=models[args.model], solver=solvers[args.solver], output=args.output)

if __name__ == '__main__':
    main()
