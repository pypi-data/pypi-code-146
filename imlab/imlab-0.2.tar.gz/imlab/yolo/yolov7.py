import json
import os

import torch
from torch import nn

from .utils import parse_model

path_dir = os.path.dirname(os.path.abspath(__file__))


class Model(torch.nn.Module):
    """Model. yolo model"""

    def __init__(
        self,
        classes: list = [],
        n_input: int = 3,
        anchors: list = [
            [12, 16, 19, 36, 40, 28],
            [36, 75, 76, 55, 72, 146],
            [142, 110, 192, 243, 459, 401],
        ],
        config: str = os.path.join(path_dir, "yoloV7.json"),
        model: object = None,
    ):
        """__init__.

        :param classes:
        :type classes: list
        :param n_input:
        :type n_input: int
        :param anchors:
        :type anchors: list
        :param config:
        :type config: str
        :param model:
        :type model: object
        """
        super(Model, self).__init__()
        self.classes = classes
        self.num_classes = len(classes)
        self.n_input = n_input
        self.anchors = anchors
        if model is None:
            self.set_yoloV7(config)
        else:
            self.model = model

    def set_yoloV7(self, config: str) -> object:
        """set_yoloV7.

        :param config:
        :type config: str
        :rtype: object
        """
        with open(config, "r") as cfg:
            model = json.load(cfg)
        self.model = nn.Sequential(
            *parse_model(
                model,
                ci=self.n_input,
                num_classes=self.num_classes,
                anchors=self.anchors,
            )
        )
        return self.model

    def forward(self, x: torch.FloatTensor) -> torch.FloatTensor:
        """forward.

        :param x:
        :type x: torch.FloatTensor
        :rtype: torch.FloatTensor
        """
        return self.forward_once(x)  # single-scale inference, train

    def forward_once(
        self,
        x: torch.FloatTensor,
    ) -> torch.FloatTensor:
        """forward_once.

        :param x:
        :type x: torch.FloatTensor
        :rtype: torch.FloatTensor
        """
        children = {}
        for i, module in enumerate(self.model):
            if i > 0:
                x = []
                for parent in module.parent:
                    x += [children[module.id][parent]]
                if len(module.parent) == 1:
                    x = x[0]

                del children[module.id]
            x = module(x)

            for layer in module.childs:
                if layer not in children:
                    children[layer] = {}
                children[layer][module.id] = x
        return x
