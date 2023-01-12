from coinlib.helper import Serializable, serializeDTO
import simplejson as json

class DrawableComponent(Serializable):

    _type: str = ""

    def __init__(self, type: str):
        self._type = type
        pass
