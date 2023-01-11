"""Training graph module"""
from typing import List, Dict, Callable
from functools import partial
from nwgraph import Message
from lightning_module_enhanced import LightningModuleEnhanced as LME, TrainableModule
from lightning_module_enhanced.callbacks import PlotMetrics
from pytorch_lightning.callbacks import ModelCheckpoint
import torch as tr

from ..models import NGC
from ..models.edges import NGCEdge
from .callbacks import RemovePreviousTrainArtifacts, PlotGraph

class TrainableNGC(TrainableModule):
    """
    Wrapper on top of an NGC in order to make the graph trainable. The metrics, optimizer, scheduler, callbacks and
    criterions are the sum of all the edges.
    """
    def __init__(self, base_graph: NGC):
        super().__init__()
        self.base_graph = base_graph
        self.trainable_edges: List[NGCEdge] = [edge for edge in self.base_graph.edges \
            if LME(edge).trainable_params > 0]
        assert len(self.trainable_edges) > 0

    @property
    def optimizer(self):
        res = []
        for edge in self.trainable_edges:
            if not hasattr(edge.model, "optimizer"):
                raise ValueError(f"Model of trainable edge '{edge}' has no optimizer")
            res.append(edge.model.optimizer)
        return res

    @property
    def scheduler_dict(self):
        res = []
        for edge in self.trainable_edges:
            if not hasattr(edge.model, "scheduler_dict"):
                raise ValueError(f"Model of trainable edge '{edge}' has no scheduler dict")
            res.append(edge.model.scheduler_dict)
        return res

    def _graph_criterion(self, y: Dict[str, tr.Tensor], gt: Dict[str, tr.Tensor]):
        res = []
        for edge in self.trainable_edges:
            if not hasattr(edge.model, "criterion_fn"):
                raise ValueError(f"Model of trainable edge '{edge}' has no criterion_fn")
            res.append(edge.model.criterion_fn(y[edge.output_node], gt[edge.output_node]))
        mean = sum(res) / len(res)
        return mean

    @property
    def criterion_fn(self):
        return self._graph_criterion

    @staticmethod
    def get_messages_from_edge(edge: NGCEdge) -> List[Message]:
        """Gets the messages from an edge"""
        output_node_messages = edge.output_node.messages
        edge_messages = [message for message in output_node_messages if message.source == edge.name]
        return edge_messages

    @staticmethod
    # pylint: disable=unused-argument
    def edge_metric_from_messages(y: Dict, gt: Dict, edge: NGCEdge, edge_metric: Callable):
        """Edge metrics require us to investigate the messages, not the graph's final state. So we dig..."""
        edge_messages = TrainableNGC.get_messages_from_edge(edge)
        assert len(edge_messages) == 1 # TODO: probably need to relax this at some point
        edge_message = edge_messages[0]
        return edge_metric(edge_message.content, gt[edge.output_node])

    @staticmethod
    def graph_edge_metric(y: Dict, gt: Dict, edge: NGCEdge, edge_metric: Callable):
        """Graph metric, for the edge-defined metric"""
        return edge_metric(y[edge.output_node], gt[edge.output_node])

    @property
    def metrics(self):
        # TODO: think if this needs only for mode='test'. We train the model in such a way that each subgraph is
        #  individually trained, so maybe this is not as bad as thought.
        metrics = {}

        for edge in self.trainable_edges:
            if not hasattr(edge.model, "metrics"):
                raise ValueError(f"Model of trainable edge '{edge}' has no metrics")
            for edge_metric_name, edge_metric in edge.model.metrics.items():
                metrics[f"{edge}_{edge_metric_name}"] = \
                    partial(TrainableNGC.edge_metric_from_messages, edge=edge, edge_metric=edge_metric)
                # This may overwrite some identical edges, and that's expected (i.e. l1 defined at multiple edges).
                # We do a partial here, not a lambda, because of weird dict/lambda interactions overwriting the
                #  actualy value somehow. Better than using copy()
                metrics[f"graph_{edge.output_node}_{edge_metric_name}"] = \
                    partial(TrainableNGC.graph_edge_metric, edge=edge, edge_metric=edge_metric)
        return metrics

    @property
    def callbacks(self):
        callbacks = [
            RemovePreviousTrainArtifacts(),
            ModelCheckpoint(save_last=True, save_top_k=1, monitor="val_loss"),
            PlotMetrics(),
            PlotGraph()
        ]
        for edge in self.trainable_edges:
            if not hasattr(edge.model, "callbacks"):
                raise ValueError(f"Model of trainable edge '{edge}' has no callbacks")
            callbacks.extend(edge.model.callbacks)

        return callbacks

    def forward(self, x):
        """Forwards through the underlying ngc graph"""
        return self.base_graph.forward(x)
