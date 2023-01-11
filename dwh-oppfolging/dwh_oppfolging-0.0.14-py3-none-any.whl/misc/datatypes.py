# import dataclasses
from typing import Callable, Optional
from typing_extensions import Any


__doc__ = "Sub-module for data types"

class ColumnRemap:
    """
    Extracts a column from a dict
    if the dict is nested the input path should be a.b.c and so on
    . are replaced with _ if no column name is given
    >>> ColumnRemap("city.name", allow_missing=True)({})
    {'city_name': None}
    """
    def __init__(
        self,
        input_column_path: str,
        output_column_name: Optional[str] = None,
        transform: Optional[Callable] = None,
        allow_missing: bool = False,
    ) -> None:
        self._path_in = input_column_path.split(".")
        self._output_column_name = output_column_name if output_column_name else "_".join(self._path_in)
        self._transform = transform
        self._allow_missing = allow_missing

    def __call__(self, data: dict) -> dict:
        input_value: Any = data
        try:
            for key in self._path_in:
                input_value = input_value[key]
        except KeyError:
            if not self._allow_missing:
                raise
            input_value = None
        output_value = input_value if self._transform is None else self._transform(input_value)
        return {self._output_column_name: output_value}

class RowRemap:
    """
    extracts a row from a dict using ColumnRemaps
    >>> RowRemap(ColumnRemap("pos.x", "x"), ColumnRemap("pos.y", "y"))({"pos":{"x": 32, "y": -17}})
    {'x': 32, 'y': -17}
    """
    def __init__(self, *args: ColumnRemap) -> None:
        self._columns = args
    def __call__(self, data: dict) -> dict:
        return {k: v for col in self._columns for k, v in col(data).items()}
