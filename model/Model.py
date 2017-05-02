from utils import timed
from model.ModelCoco import ModelCoco
from model.ModelAyoub import ModelAyoub


class UknownPicrossModel(Exception): pass

class Model:

    MODEL_AYOUB = 0
    MODEL_COCO = 1

    @staticmethod
    def get(model):
        if model == Model.MODEL_AYOUB:
            return ModelAyoub
        elif model == Model.MODEL_COCO:
            return ModelCoco
        else:
            raise UknownPicrossModel

    @staticmethod
    def all_models():
        return {
            ModelAyoub.name(): Model.MODEL_AYOUB,
            ModelCoco.name(): Model.MODEL_COCO
        }
