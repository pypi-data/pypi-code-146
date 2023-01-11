"""Init file"""
from .build_model import build_model, build_model_type
from .base_ngc_model import BaseNGCModel
from .ngc import NGC
# Model variants
from .ngc_v1 import NGCV1
from .ngc_ensemble import NGCEnsemble
from .ngc_hyperedges import NGCHyperEdges
