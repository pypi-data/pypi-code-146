"""Utility module about edges regarding training status"""
from pathlib import Path
from typing import Dict
import random
from nwgraph import Edge
import torch as tr
import numpy as np
from lightning_module_enhanced.train_setup import TrainSetup

from ..logger import logger
from ..models.edges import NGCEdge
from ..readers import NGCNpzReader
from ..models import NGC

def get_edge_weights_file(edge: NGCEdge, base_dir: Path) -> Path:
    """Given an edge and a base dir for all iteration weights, get the checkpoint path, or None."""
    weights_file = base_dir / str(edge) / "checkpoints/model_best.ckpt"
    return weights_file

def get_edge_last_weights_file(edge: NGCEdge, base_dir: Path) -> Path:
    """Given an edge, return the 'last.ckpt' weight file (i.e. the last trained epoch)"""
    weights_file = base_dir / str(edge) / "checkpoints/last.ckpt"
    return weights_file

def is_edge_trained(edge: NGCEdge, base_dir: Path) -> bool:
    """model_best.ckpt exists, meaning that on_train_end callback was called for this particular edge."""
    if len(tuple(edge.parameters())) == 0:
        return True
    return get_edge_weights_file(edge, base_dir).exists()

def is_edge_partially_trained(edge: NGCEdge, base_dir: Path) -> bool:
    """Training is not finished (model_best.ckpt) does not exist, but it was started (last.ckpt exists)"""
    return not is_edge_trained(edge, base_dir) and get_edge_last_weights_file(edge, base_dir).exists()

def ngc_trainer_dataloader_params(reader: NGCNpzReader, dataloader_params: Dict, seed: int = 0) -> Dict:
    """Datalodaer params. The given ones + generator/seed/collate_fn which are fixed"""
    # pylint: disable=unused-argument
    def seed_worker(worker_id):
        worker_seed = tr.initial_seed() % 2**32
        np.random.seed(worker_seed)
        random.seed(worker_seed)

    generator = tr.Generator()
    generator.manual_seed(seed)
    dataloader_params = {**dataloader_params, "generator": generator,
                         "worker_init_fn": seed_worker, "collate_fn": reader.collate_fn}
    return dataloader_params

def setup_graph_for_train(graph: NGC, train_cfg: Dict):
    """Sets up a ngc for training by adding optimizer, scheduler, criterion, callbacks and metrics to all edges"""
    logger.info("Setting up all edges for training")
    base_optimizer_dict = train_cfg["optimizer"]
    base_scheduler_dict = train_cfg["scheduler"]
    base_criterion = train_cfg["criterion"]

    edge: Edge
    for edge in graph.edges:
        if len(tuple(edge.model.parameters())) == 0:
            continue
        if edge.output_node.name not in train_cfg:
            logger.warning(f"Node '{edge.output_node.name}' not in train cfg. Getting only defaults for it !")
            train_cfg[edge.output_node.name] = {}
        node_cfg = train_cfg[edge.output_node.name]
        node_cfg["optimizer"] = node_cfg["optimizer"] if "optimizer" in node_cfg else base_optimizer_dict
        node_cfg["scheduler"] = node_cfg["scheduler"] if "scheduler" in node_cfg else base_scheduler_dict
        node_cfg["criterion"] = node_cfg["criterion"] if "criterion" in node_cfg else base_criterion
        edge_train_setup = TrainSetup(edge.model, node_cfg)
        edge_train_setup._setup_optimizer() # pylint: disable=protected-access
        edge_train_setup._setup_scheduler() # pylint: disable=protected-access

        assert "criterion" in node_cfg and node_cfg["criterion"] is not None
        assert node_cfg["criterion"]["type"] in ("mse", "cross_entropy")
        edge.model.criterion_fn = edge.output_node.criterion_fn
        edge.model.metrics = edge.output_node.metrics
        edge.model.callbacks = []
