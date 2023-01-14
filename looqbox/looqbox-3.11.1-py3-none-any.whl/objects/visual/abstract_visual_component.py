from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject
from abc import abstractmethod


class AbstractVisualComponent(LooqObject):

    @abstractmethod
    def to_json_structure(self, visitor: BaseRender):
        ...
