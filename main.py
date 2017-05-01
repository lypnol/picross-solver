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
                        help='modelization method, only AYOUB', default='AYOUB')
    parser.add_argument('-s', dest='solver', type=str,
                        help='sat solver, only PYCOSAT', default='PYCOSAT')
    parser.add_argument('-o', dest='output', type=str,
                        help='destination GRID file', default=None)
    parser.add_argument('--silent', dest='silent', action='store_true',
                        help='silent mode', default=False)

    args = parser.parse_args()

    models = {
        'AYOUB': Model.MODEL_AYOUB
    }

    solvers = {
        'PYCOSAT': Solver.PYCOSAT_SOLVER
    }

    utils.set_silent(args.silent)

    for path in args.picross:
        picross = Picross(path)
        picross.save_grid(model=models[args.model], solver=solvers[args.solver], output=args.output)

if __name__ == '__main__':
    main()
