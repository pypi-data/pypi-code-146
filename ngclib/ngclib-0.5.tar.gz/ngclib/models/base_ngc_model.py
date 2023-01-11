"""
BaseNGCModel module. This is used to create the edge's models based on the input and ouput nodes. Output nodes
must be enhanced with the criterion_fn, metrics, optimizer_type and scheduler_dict_type attributes.

TODO: nodes should have these properties and not check them with hasattr.
"""
from typing import Callable
from nwgraph import Node
from lightning_module_enhanced import TrainableModule
from torch import nn

class BaseNGCModel(TrainableModule):
    """Base ngc model class"""
    def __init__(self, base_model_type: Callable[[int, int], nn.Module], input_node: Node, output_node: Node):
        assert hasattr(output_node, "criterion_fn"), output_node
        assert hasattr(output_node, "metrics"), output_node
        assert hasattr(output_node, "optimizer_type"), output_node
        assert hasattr(output_node, "scheduler_type_dict"), output_node
        assert isinstance(base_model_type, Callable)
        super().__init__()
        self.input_node = input_node
        self.output_node = output_node
        self._optimizer = None
        self.base_model: nn.Module = base_model_type(input_node.num_dims, output_node.num_dims)

    def forward(self, x):
        """Forward on the base model"""
        return self.base_model(x)

    @property
    def criterion_fn(self):
        return self.output_node.criterion_fn

    @property
    def callbacks(self):
        return []

    @property
    def metrics(self):
        return self.output_node.metrics

    @property
    def optimizer(self):
        if self._optimizer is None:
            self._optimizer = self.output_node.optimizer_type(self.parameters())
        return self._optimizer

    @property
    def scheduler_dict(self):
        if len(self.output_node.scheduler_type_dict) == 0:
            return None

        scheduler_type_dict = self.output_node.scheduler_type_dict
        assert "scheduler_type" in scheduler_type_dict
        scheduler_type = scheduler_type_dict.pop("scheduler_type")
        return {
            "scheduler": scheduler_type(self.optimizer),
            **scheduler_type_dict
        }
