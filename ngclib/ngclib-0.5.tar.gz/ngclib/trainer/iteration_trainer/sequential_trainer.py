"""Sequential iteration trainer module"""
from overrides import overrides
import torch as tr
from .base_iteration_trainer import BaseIterationTrainer

class SequentialTrainer(BaseIterationTrainer):
    """Sequential iteration trainer implementation"""
    @overrides
    def run(self):
        device = tr.device("cuda") if tr.cuda.is_available() else tr.device("cpu")
        while not self._are_all_edges_trained():
            for edge in self.untrained_edges:
                edge.to(device)
                self.train_one_edge(edge)
