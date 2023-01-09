from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

# from layers import FactorizedDense, QResLayer
import yasmll.layers
import yasmll.models
from yasmll.yasmll import init, shutdown
