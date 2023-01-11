"""Classification Node module"""
from typing import Union, List
from .node import Node

class ClassificationNode(Node):
    """Classification Node class"""
    def __init__(self, name: str, classes: Union[List, int]):
        if isinstance(classes, list):
            num_classes = len(classes)
        else:
            num_classes = classes
            classes = range(num_classes)
        self.classes = classes
        super().__init__(name, num_dims=num_classes)
