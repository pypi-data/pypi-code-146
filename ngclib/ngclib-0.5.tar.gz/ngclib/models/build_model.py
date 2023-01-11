"""NGC model builder"""
from typing import Type, List
from nwgraph import Edge

from .ngc import NGC, VoteFn
from .ngc_v1 import NGCV1
from .ngc_ensemble import NGCEnsemble
from .ngc_hyperedges import NGCHyperEdges

def build_model_type(str_model_type: str) -> Type[NGC]:
    """Gets the type of the NGC, given a graph_cfg. Useful for analysis w/o instantiating the entire graph."""
    graph_type: Type[NGC] = {
        "NGC-V1": NGCV1,
        "NGC-Ensemble": NGCEnsemble,
        "NGC-HyperEdges": NGCHyperEdges,
    }[str_model_type]
    return graph_type

def build_model(graph_type: Type[NGC], edges: List[Edge], input_node_names: List[str], vote_fn: VoteFn) -> NGC:
    """Simply calls the constructor of a given ngc architecture."""
    return graph_type(edges, vote_fn, input_node_names)
