from importlib.util import find_spec

from .base_provider import BaseProvider
from .implementation.numpy_provider import BernoulliDistProvider, UniformDistProvider, GaussianDistProvider
from .implementation.pandas_provider import PandasProvider
from .manager import ProviderManager
from .metadata import ColumnMeta, ParamMeta, TableParam

if find_spec('sklearn') is not None:
    from .implementation.sklearn_provider import PcaProjectionProvider

if find_spec('cvxopt') is not None:
    from .implementation.index_builder import QuadraticProgram

if find_spec('yfinance') is not None:
    from .implementation.yfinance_provider import YFinanceProvider

if find_spec('imaginairy') is not None:
    from .implementation.stable_diffusion import StableDiffusion

if find_spec('wbgapi') is not None:
    from .implementation.world_bank import (
        WorldBankDataSources,
        WorldBankEconomies,
        WorldBankSeriesMetadata,
        WorldBankSeriesData,
    )

from .setup import copy_certs, setup
