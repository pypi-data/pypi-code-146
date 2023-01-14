#!/usr/bin/env python3
'''
Type definitions and functions.
'''

import pathlib
from typing import Tuple, Union

# Generic number type.
Number = Union[int, float]

# Optimization value for the Optuna sweeper returned by hydronaut.run.Runner.__call__.
OptimizationValue = Union[Number, Tuple[Number, ...]]

# Generic path type for functions that can handle both pathlib Paths or strings.
Path = Union[str, pathlib.Path]
