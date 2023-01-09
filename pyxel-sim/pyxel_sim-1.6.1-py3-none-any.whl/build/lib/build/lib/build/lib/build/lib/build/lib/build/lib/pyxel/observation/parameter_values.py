#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""TBW."""

from collections import abc
from enum import Enum
from numbers import Number
from typing import Iterator, Optional, Sequence, Tuple, Union

from typing_extensions import Literal

from pyxel.evaluator import eval_range


class ParameterType(Enum):
    """TBW."""

    # one-dimensional, can be a dataset coordinate
    Simple = "simple"
    # multi-dimensional or loaded from a file in parallel mode, cannot be a dataset coordinate
    Multi = "multi"


# TODO: Add unit tests. See #336
class ParameterValues:
    """Contains keys and values of parameters in a parametric step."""

    def __init__(
        self,
        key: str,
        values: Union[
            Literal["_"], Sequence[Literal["_"]], Sequence[Number], Sequence[str]
        ],
        boundaries: Optional[Tuple[float, float]] = None,
        enabled: bool = True,
        logarithmic: bool = False,
    ):

        # TODO: maybe use numpy to check multi-dimensional input lists
        # Check YAML input (not real values yet) and define parameter type
        if values == "_":
            self.type = ParameterType("multi")
        elif isinstance(values, str) and "numpy" in values:
            self.type = ParameterType("simple")
        elif isinstance(values, abc.Sequence) and any(
            [(el == "_" or isinstance(el, abc.Sequence)) for el in values]
        ):
            self.type = ParameterType("multi")
        elif isinstance(values, abc.Sequence) and all(
            [isinstance(el, (Number, str)) for el in values]
        ):
            self.type = ParameterType("simple")
        else:
            raise ValueError("Parameter values cannot be initiated with those values.")

        if "sampling.start_time" in key:
            key = "detector.sampling_properties.start_time"

        # unique identifier to the step. example: 'detector.geometry.row'
        self._key: str = key
        self._values: Union[
            Literal["_"], Sequence[Literal["_"]], Sequence[Number], Sequence[str]
        ] = values

        # short  name identifier: 'row'
        self._short_name = key.split(".")[-1]

        self._enabled: bool = enabled
        self._logarithmic: bool = logarithmic
        self._boundaries: Optional[Tuple[float, float]] = boundaries

        self._current: Optional[Union[Literal["_"], Number, str]] = None

    def __repr__(self) -> str:
        cls_name: str = self.__class__.__name__

        return f"{cls_name}<key={self.key!r}, values={self.values!r}, enabled={self.enabled!r}>"

    def __len__(self) -> int:

        try:
            values: Sequence = eval_range(self.values)
        except Exception as exc:
            raise NameError(
                f"Wrong value: {self.values!r} for key: {self.key!r}. Error: {exc}"
            ) from exc

        return len(values)

    # TODO: Is method '__contains__' needed ? If yes then this class will act as a `Collections.abc.Sequence`
    def __iter__(self) -> Iterator[Number]:
        values = eval_range(self.values)
        yield from values

    @property
    def key(self) -> str:
        """TBW."""
        return self._key

    @property
    def short_name(self) -> str:
        """TBW."""
        return self._short_name

    @property
    def values(
        self,
    ) -> Union[Literal["_"], Sequence[Literal["_"]], Sequence[Number], Sequence[str]]:
        """TBW."""
        return self._values

    @property
    def enabled(self) -> bool:
        """TBW."""
        return self._enabled

    @property
    def current(self) -> Optional[Union[Literal["_"], Number, str]]:
        """TBW."""
        return self._current

    @current.setter
    def current(self, value: Union[Literal["_"], str, Number]) -> None:
        """TBW."""
        self._current = value

    @property
    def logarithmic(self) -> bool:
        """TBW."""
        return self._logarithmic

    @property
    def boundaries(self) -> Optional[Tuple[float, float]]:
        """TBW."""
        return self._boundaries
