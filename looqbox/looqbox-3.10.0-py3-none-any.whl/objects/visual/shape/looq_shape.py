from abc import abstractmethod
from looqbox.objects.visual.abstract_visual_component import AbstractVisualComponent
from looqbox.render.abstract_render import BaseRender


class ObjShape(AbstractVisualComponent):
    def __init__(self, **properties):
        super().__init__(**properties)

    @abstractmethod
    def to_json_structure(self, visitor: BaseRender):
        ...
