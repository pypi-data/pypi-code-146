import torch
from torch import nn

from .models import SPPCSPC, Cat, Conv, Detect, RepConv


def module_identity(*args, **kwargs):
    """module_identity.

    :param args:
    :param kwargs:
    """
    return identity


def identity(x):
    """identity.

    :param x:
    """
    return x


class Module(nn.Module):
    """Module."""

    m = module_identity

    def __init__(
        self, parent: list = [], childs: list = [], id: int = 0, **kwargs
    ) -> None:
        """__init__.

        :param parent:
        :type parent: list
        :param childs:
        :type childs: list
        :param id:
        :type id: int
        :param kwargs:
        :rtype: None
        """
        super().__init__()
        self.module = self.m(**kwargs)
        self.parent = parent
        self.id = id
        self.childs = childs

    def forward(self, x: torch.FloatTensor) -> torch.FloatTensor:
        """forward.

        :param x:
        :type x: torch.FloatTensor
        :rtype: torch.FloatTensor
        """
        return self.module(x)


def parse_model(
    model: dict,
    ci: int = 3,
    num_classes: int = 80,
    anchors: list = [
        [12, 16, 19, 36, 40, 28],
        [36, 75, 76, 55, 72, 146],
        [142, 110, 192, 243, 459, 401],
    ],
) -> object:
    """parse_model.

    :param model:
    :type model: dict
    :param ci:
    :type ci: int
    :param num_classes:
    :type num_classes: int
    :param anchors:
    :type anchors: list
    :rtype: object
    """
    children = {}
    for layer in model:
        if layer["id"] not in children:
            children[layer["id"]] = []
        for parent in layer["parent"]:
            if parent not in children:
                children[parent] = []
            children[parent] += [layer["id"]]
    layers = []
    for l, layer in enumerate(model):
        if l == 0:
            layer["args"]["ci"] = ci
        lname = layer["type"].lower()
        if lname in ["conv", "convolution"]:
            module = Conv
        elif lname in ["sppcspc"]:
            module = SPPCSPC
        elif lname in ["cat", "concat"]:
            module = Cat
        elif lname in ["mp", "maxpool"]:
            module = Module
            module.m = nn.MaxPool2d
        elif lname in ["repconv"]:
            module = RepConv
        elif lname in ["upsample"]:
            module = Module
            module.m = nn.Upsample
        elif lname in ["detect"]:
            module = Detect
            layer["args"]["nc"] = num_classes
            layer["args"]["stride"] = torch.tensor(layer["args"]["stride"]).float()
            layer["args"]["anchors"] = torch.tensor(anchors).float().view(
                len(layer["parent"]), -1, 2
            ) / layer["args"]["stride"].view(-1, 1, 1)

        layers += [
            module(
                **layer["args"],
                parent=layer["parent"],
                childs=children[layer["id"]],
                id=layer["id"]
            )
        ]
    return layers
