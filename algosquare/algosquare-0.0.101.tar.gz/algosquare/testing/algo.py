"""Test algo functionality."""
import inspect

from types import ModuleType
from typing import Any, Union

from .errors import TestError
from .tabular import test_tabular_algo
from ..base.algo import Algo, extract_algo_statics
from ..base.tabular import TabularClassificationAlgo, TabularRegressionAlgo

def test_algo(algo_class: type[Algo], output_dir: str, timeout: int = 300, nan_fraction: float = 0.1) -> None:
    """
    Function for testing algo functionality.

    Args:
        algo_class: subclass of Algo.
        output_dir: local directory for saving model.
        timeout: search time in seconds.
        nan_fraction: probability of null values in data.

    Returns:
        None.
    """
    extract_algo_statics(algo_class)

    if issubclass(algo_class, TabularClassificationAlgo) or issubclass(algo_class, TabularRegressionAlgo):
        test_tabular_algo(algo_class, output_dir, timeout, nan_fraction)
    else:
        raise TestError('invalid algo class')

def test_package(package: ModuleType, output_dir: str, **kwargs: Union[int, float]) -> None:
    """
    Function for testing algos in package.

    Args:
        package: module.
        output_dir: local directory for saving model.
        kwargs: keyword args passed to test_algo

    Returns:
        None.
    """
    for field in dir(package):
        attr = getattr(package, field)
        if inspect.isclass(attr) and issubclass(attr, Algo):
            test_algo(attr, output_dir, **kwargs)
