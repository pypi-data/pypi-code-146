#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""TBW."""
import inspect
from typing import TYPE_CHECKING, Any, Callable, Dict, MutableMapping, Optional

from pyxel.evaluator import evaluate_reference

if TYPE_CHECKING:
    import numpy as np

    from pyxel.calibration import FittingCallable
    from pyxel.detectors import Detector


class Arguments(MutableMapping):
    """Arguments class for usage in ModelFunction.

    Class Arguments is initialized from a dictionary of model function arguments.
    It resembles the behaviour of the passed dictionary with additional methods __setattr__ and __getattr__,
    which enable to get and set the model parameters through attribute interface.
    Dictionary of arguments is saved in private attribute _arguments.

    Examples
    --------
    >>> from pyxel.pipelines.model_function import Arguments
    >>> arguments = Arguments({"one": 1, "two": 2})
    >>> arguments
    Arguments({'one': 1, 'two': 2})

    Access arguments
    >>> arguments["one"]
    1
    or
    >>> arguments.one
    1

    Changing parameters
    >>> arguments["one"] = 10
    >>> arguments["two"] = 20
    >>> arguments
    Arguments({'one': 10, 'two': 20})

    Non existing arguments
    >>> arguments["three"] = 3
    KeyError: 'No argument named three !'
    >>> arguments.three = 3
    AttributeError: 'No argument named three !'
    """

    def __init__(self, input_arguments: Dict[str, Any]):
        self._arguments: Dict[str, Any] = input_arguments

    def __setitem__(self, key, value):

        if key not in self._arguments:
            raise KeyError(f"No argument named {key} !")

        self._arguments[key] = value

    def __getitem__(self, key):

        if key not in self._arguments:
            raise KeyError(f"No argument named {key} !")

        return self._arguments[key]

    def __delitem__(self, key):
        del self._arguments[key]

    def __iter__(self):
        return iter(self._arguments)

    def __len__(self):
        return len(self._arguments)

    def __getattr__(self, key):

        # Use non-modified __getattr__ in this case.
        if key == "_arguments":
            return object.__getattribute__(self, "_arguments")

        if key not in self._arguments:
            raise AttributeError(f"'{self!r}' object has no argument {key!r} !")

        return self._arguments[key]

    def __setattr__(self, key, value):

        # Use non-modified __setattr__ in this case.
        if key == "_arguments":
            super().__setattr__(key, value)
            return

        if key not in self._arguments:
            raise AttributeError(f"'{self!r}' object has no argument {key!r} !")

        self._arguments[key] = value

    def __dir__(self):
        return dir(type(self)) + list(self)

    def __repr__(self):
        return f"Arguments({self._arguments})"

    # def __deepcopy__(self, memo) -> "Arguments":
    #     """TBW."""
    #     return Arguments(deepcopy(self._arguments))


# TODO: Improve this class. See issue #132.
# TODO: Add unit tests #182
class ModelFunction:
    """Create a wrapper function around a Model function.

    Examples
    --------
    >>> model_func = ModelFunction(
    ...     func="pyxel.models.photon_generation.illumination",
    ...     name="illumination",
    ...     arguments={"level": 1, "option": "foo"},
    ... )

    Access basic parameters

    >>> model_func.name
    'illumination'
    >>> model_func.enabled
    True
    >>> model_func.arguments
    Arguments({'level': 1, 'option': 'foo'})

    Access the arguments with a ``dict`` interface

    >>> list(model_func.arguments)
    ['level', 'option']
    >>> model_func.arguments["level"]
    1
    >>> model_func.arguments["level"] = 2
    TypeError: 'Arguments' object does not support item assignment

    Access the arguments with an attribute interface

    >>> model_func.arguments.level
    1
    """

    def __init__(
        self,
        func: str,
        name: str,
        arguments: Optional[dict] = None,
        enabled: bool = True,
    ):
        if inspect.isclass(func):
            raise AttributeError("Cannot pass a class to ModelFunction.")

        self._func: Callable = evaluate_reference(func)
        self._name = name
        self.enabled: bool = enabled

        if arguments is None:
            arguments = {}

        self._arguments = Arguments(arguments)
        # self.group = None               # TODO

    def __repr__(self) -> str:
        cls_name: str = self.__class__.__name__
        func_name = self._func.__module__ + "." + self._func.__name__

        return (
            f"{cls_name}(name={self.name!r}, func={func_name}, "
            f"arguments={self.arguments!r}, enabled={self.enabled!r})"
        )

    @property
    def name(self) -> str:
        """TBW."""
        return self._name

    @property
    def arguments(self) -> Arguments:
        """TBW."""
        return self._arguments

    def __call__(self, detector: "Detector") -> None:
        """TBW."""
        self._func(detector, **self.arguments)


class FitnessFunction:
    """Fitness function for model fitting."""

    def __init__(self, func: str):
        self._func: FittingCallable = evaluate_reference(func)

    def __call__(
        self,
        simulated: "np.ndarray",
        target: "np.ndarray",
        weighting: "np.ndarray",
    ) -> float:
        """Compute fitness."""
        result: float = self._func(
            simulated=simulated, target=target, weighting=weighting
        )
        return result
