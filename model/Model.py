from utils import timed
from model.ModelSpots import ModelSpots
from model.ModelIKJ import ModelIKJ


class UknownPicrossModel(Exception): pass

class Model:

    MODEL_IKJ = 0
    MODEL_SPOTS = 1

    @staticmethod
    def get(model):
        if model == Model.MODEL_IKJ:
            return ModelIKJ
        elif model == Model.MODEL_SPOTS:
            return ModelSpots
        else:
            raise UknownPicrossModel

    @staticmethod
    def all_models():
        return {
            ModelIKJ.name(): Model.MODEL_IKJ,
            ModelSpots.name(): Model.MODEL_SPOTS
        }
