from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject
from abc import abstractmethod
import numpy as np


class AbstractContainer(LooqObject):

    def __init__(self, *children, **properties):
        """
        :param children: Children to be contained.
        """
        super().__init__(**properties)
        self.children = list(np.hstack(children)) if children else []

    @abstractmethod
    def to_json_structure(self, visitor: BaseRender):
        """
        Convert python objects into json to Front-End render
        """

    def __eq__(self, other):
        return self.children.__class__ == other.children.__class__ and vars(self) == vars(other)
