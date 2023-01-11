"""Types module for the NGC library."""
# pylint: disable=pointless-string-statement
from typing import Callable, List, Dict
from nwgraph import Node
import torch as tr

# agg:VxD -> D
VoteFn = Callable[[tr.Tensor], tr.Tensor]

# f(int, int) => nn.Module
NGCEdgeFn = Callable[[int, int], tr.nn.Module]
# f(node) => (g(int, int) => nn.Module) (lazy init)
ModelFn = Callable[[Node], NGCEdgeFn]

"""
ConfigEdges is a mapping like this:
edges:
  SL:
    - [a, b]
    - [c, d]
  ENS:
    - [a, b, c]
"""
ConfigEdges = Dict[str, List[List[str]]]
