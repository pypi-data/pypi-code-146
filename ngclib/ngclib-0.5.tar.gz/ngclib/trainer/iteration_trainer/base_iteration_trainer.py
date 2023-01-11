"""NGC Iteration trainer module"""
from pathlib import Path
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Dict, List
from nwutils.data_structures import topological_sort
from torch.utils.data import DataLoader
from lightning_module_enhanced import LightningModuleEnhanced as LME
from lightning_module_enhanced.utils import accelerator_params_from_module
from pytorch_lightning import Trainer
from pytorch_lightning.loggers import TensorBoardLogger
from nwgraph import Edge

from ...models import NGC
from ...models.edges import NGCEdge
from ..trainable_ngc import TrainableNGC
from ..utils import is_edge_trained, is_edge_partially_trained, get_edge_last_weights_file, \
    ngc_trainer_dataloader_params
from ...logger import logger
from ...readers import NGCNpzReader

class BaseIterationTrainer(ABC):
    """
    BaseIterationTrainer implementation

    Parameters:
        graph The full ngc graph
        train_reader The train reader
        validation_reader The validation reader
        iter_dir The ngcdir/iterX/models directory where this iteration's edges are stored
        dataloader_params The parameters passed to the dataloader (no collate_fn, generator or worker_init)
        trainer_params The parameters passed to the lighting trainer
        seed The seed used for the trainer
    """
    def __init__(self, graph: NGC, train_reader: NGCNpzReader, validation_reader: NGCNpzReader,
                 iter_dir: Path, dataloader_params: Dict, trainer_params: Dict, seed: int = 0):
        assert iter_dir.name == "models", f"Iter dir is not called 'models', probably a mistake ({iter_dir})"
        if validation_reader is None:
            logger.warning("No validation set provided. Using train set as validation set as well.")
            validation_reader = train_reader
        assert not "collate_fn" in dataloader_params, "'collate_fn' is provided by the NGC Reader directly."
        assert not "generator" in dataloader_params, "'generator' is controlled using the seed parameter"
        assert not "worker_init" in dataloader_params, "'worker_init' is set by the trainer directly"
        assert sorted(train_reader.nodes, key=lambda n: n.name) == \
               sorted(validation_reader.nodes, key=lambda n: n.name)

        self.graph = graph.to("cpu")
        self.train_reader = train_reader
        self.validation_reader = validation_reader
        self.iter_dir = iter_dir
        self.dataloader_params = dataloader_params
        self.trainer_params = trainer_params
        self.seed = seed
        LME(graph).reset_parameters(seed)

        logger.info(f"Building all the subgraphs for this graph ({len(graph.edges)} edges)")
        self.subgraphs: Dict[str, NGC] = self.graph.edge_subgraphs(graph.input_node_names, graph.num_iterations)
        self._topological_sorted_edge_names: List[str] = None

    @property
    def trained_edges(self) -> List[Edge]:
        """Returns a list of all trained edges"""
        return [edge for edge in self.graph.edges if is_edge_trained(edge, self.iter_dir)]

    @property
    def untrained_edges(self) -> List[Edge]:
        """Returns a list of all untrained edges"""
        topo_sorted = self.topological_sorted_edges
        topo_sorted_untrained = [edge for edge in topo_sorted if not is_edge_trained(edge, self.iter_dir)]
        return topo_sorted_untrained

    @property
    def topological_sorted_edges(self) -> List[Edge]:
        """The list of all edges, sorted topologically be requirements"""
        if self._topological_sorted_edge_names is None:
            # We know the last edge is the same as the key in the subraphs
            dep_graph = {str(k): [str(_v) for _v in v.edges[0: -1]] for k, v in self.subgraphs.items()}
            self._topological_sorted_edge_names = topological_sort(dep_graph)
        return [self.graph.name_to_edge[e] for e in self._topological_sorted_edge_names]

    def _are_all_edges_trained(self) -> bool:
        """Checks if all edges are trained"""
        return len(self.untrained_edges) == 0

    def _get_dependencies(self, edge: Edge) -> List[Edge]:
        res = []
        subgraph_edge: Edge
        for subgraph_edge in self.subgraphs[edge.name].edges:
            if edge.name != subgraph_edge.name:
                res.append(subgraph_edge)
        return res

    def _are_dependencies_trained(self, edge: Edge) -> bool:
        """Checks if all edge dependencies are trained for a particular edge via the subgraph"""
        dependency_edges = self._get_dependencies(edge)
        for dependency_edge in dependency_edges:
            if not is_edge_trained(dependency_edge, self.iter_dir):
                return False
        return True

    def _load_all_dependencies_weights(self, subgraph: NGC, edge: Edge):
        """For a subgraph, load all edges, except the given edge"""
        # Load all n-1 edges (TODO: if they have params)
        dep_edge: NGCEdge
        for dep_edge in subgraph.edges:
            if dep_edge.name == edge.name:
                continue
            if len(tuple(dep_edge.parameters())) == 0:
                continue
            dep_weight_file = self.iter_dir / str(dep_edge) / "checkpoints/model_best.ckpt"
            dep_edge.load_weights(dep_weight_file)
            dep_edge.requires_grad_(False)
        (self.iter_dir / str(edge)).mkdir(exist_ok=True, parents=True)

    def _set_subgraph_train_params(self, subgraph: NGC, edge: Edge):
        """Set the parameters to untrainable for all the other edges, as we train each edge independently in NGC"""
        subgraph_edge: Edge
        for subgraph_edge in subgraph.edges:
            if edge.name != subgraph_edge.name:
                LME(subgraph_edge).trainable_params = False

    def train_one_edge(self, edge: NGCEdge) -> bool:
        """The main function. Trains the edge if not already trained. If partially trained, loads it first"""
        last_edge_name = self.subgraphs[edge.name].edges[-1].name
        assert last_edge_name == edge.name, "Edge must be the last one in the subgraph. " \
                                            f"Last: {last_edge_name}. Expected: {edge.name}"
        # Get the index of the device and copy it back to cpu as fast as possible
        accelerator, index = accelerator_params_from_module(edge)
        edge.to("cpu")

        if is_edge_trained(edge, self.iter_dir):
            logger.debug(f"Edge '{edge}' already trained")
            return True
        if not self._are_dependencies_trained(edge):
            logger.debug(f"Not all dependencies of '{edge}' already trained")
            return False

        logger.info(f"Training edge '{edge}'")
        subgraph = deepcopy(self.subgraphs[edge.name])
        self._set_subgraph_train_params(subgraph, edge)
        self._load_all_dependencies_weights(subgraph, edge)
        ckpt_path = None
        if is_edge_partially_trained(edge, self.iter_dir):
            logger.debug(f"Edge '{edge}' is partially trained, resuming from checkpoint.")
            ckpt_path = get_edge_last_weights_file(edge, self.iter_dir)

        subgraph_train_reader = self.train_reader.subreader(subgraph.nodes)
        subgraph_validation_reader = self.validation_reader.subreader(subgraph.nodes)
        train_dl_params = ngc_trainer_dataloader_params(subgraph_train_reader, self.dataloader_params, self.seed)
        validation_dl_params = {**train_dl_params, "shuffle": False}

        train_loader = DataLoader(subgraph_train_reader, **train_dl_params)
        validation_loader = DataLoader(subgraph_validation_reader, **validation_dl_params)

        training_graph = TrainableNGC(subgraph)
        lme_training_graph = LME(training_graph)

        pl_logger = TensorBoardLogger(save_dir=self.iter_dir, name=str(edge), version="")
        pl_trainer = Trainer(default_root_dir=self.iter_dir, logger=pl_logger, devices=index,
                             accelerator=accelerator, **self.trainer_params)
        pl_trainer.fit(lme_training_graph, train_loader, validation_loader, ckpt_path=ckpt_path)
        subgraph.to("cpu")
        del subgraph
        return True

    @abstractmethod
    def run(self):
        """The method to run this iteration. Must be overriden by parallelism stragies"""

    def __call__(self):
        return self.run()
