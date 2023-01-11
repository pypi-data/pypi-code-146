"""Modules used to build a model from a graph cfg. Mostly wrappers on top of build_model using stuff from cfg"""
from typing import List
from nwgraph import Edge, Node
from ..models import NGC, build_model
from .graph_cfg import GraphCfg
from ..utils import VoteFn, ModelFn

def build_model_from_cfg(graph_cfg: GraphCfg, nodes: List[Node], model_fn: ModelFn, vote_fn: VoteFn) -> NGC:
    """Builds the model from the graph cfg"""
    edges: List[Edge] = graph_cfg.ngc_type.build_edges(nodes, graph_cfg.edges_raw, graph_cfg.input_nodes, model_fn)
    model = build_model(graph_cfg.ngc_type, edges, graph_cfg.input_nodes, vote_fn)
    return model
