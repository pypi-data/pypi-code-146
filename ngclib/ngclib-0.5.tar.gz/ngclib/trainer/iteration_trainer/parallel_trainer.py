"""Parallel iteration trainer module"""
from copy import deepcopy
from multiprocessing import cpu_count
from overrides import overrides
import torch as tr
from nwgraph import Edge
from pool_resources import PoolResources, TorchResource
from ...logger import logger
from ..utils import is_edge_trained
from .base_iteration_trainer import BaseIterationTrainer

class ParallelTrainer(BaseIterationTrainer):
    """Parallel iteration trainer implementation"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # It seems having >1 workers make them hang on parallel processes.
        self.dataloader_params = deepcopy(self.dataloader_params)
        self.dataloader_params["num_workers"] = 0

    @overrides
    def train_one_edge(self, edge: Edge) -> bool:
        res = super().train_one_edge(edge)
        if res is False:
            deps_trained = {k.name: is_edge_trained(k, self.iter_dir) for k in self._get_dependencies(edge)}

            # Raise exception os the pool knows this edge is not done yet and will put it back in the untrained list
            raise Exception(f"Edge '{edge}' could not be trained. Deps: {deps_trained}. "
                            "If all are True, some other error may have happened and we need to investigate further")
        return True

    @overrides
    def run(self):
        num_gpus = tr.cuda.device_count()
        num_subgraphs = len(self.subgraphs)
        if num_gpus == 0:
            logger.debug(f"No GPUs were found. Training {num_subgraphs} in parallel on CPUs.")
            # use all cpus if the number of subgraphs is less
            num_cpus = min(num_subgraphs, cpu_count())
            resources = [TorchResource(f"cpu:{i}") for i in range(num_cpus)]
        else:
            logger.debug(f"{num_gpus} GPUs found. Training {num_subgraphs} in parallel on GPUs.")
            resources = [TorchResource(f"cuda:{i}") for i in range(num_gpus)]
        pool = PoolResources(resources, timeout=5, pbar=False)
        while not self._are_all_edges_trained():
            pool.map(self.train_one_edge, self.untrained_edges)
