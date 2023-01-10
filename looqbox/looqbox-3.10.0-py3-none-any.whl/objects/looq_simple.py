from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ObjSimple(LooqObject):
    """
    Create an object to be used inside a looq.objSimple. The goal of this object is to
    send a JSON to be used inside IoT, wearables and assistants.
    """
    def __init__(self, text):
        """
        :param text: Text to be showed in the device.
        """
        super().__init__()
        self.text = text

    def to_json_structure(self, visitor: BaseRender):
        return visitor.simple_render(self)
