#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""Pyxel 'Processed Data' class to generate and track processing data."""
from typing import Union

import xarray as xr


class ProcessedData:
    """Create a `ProcessedData` container.

    Examples
    --------
    >>> obj = ProcessedData()
    >>> obj.data
    <xarray.Dataset>
    Dimensions:  ()
    Data variables:
        *empty*
    >>> obj.append(xr.DataArray(...))
    """

    def __init__(self, data: Union[xr.Dataset, xr.DataArray, None] = None):
        if data is None:
            ds: xr.Dataset = xr.Dataset()
        elif isinstance(data, xr.DataArray):
            if data.name is None:
                raise ValueError("Missing parameter 'name' in the 'DataArray'")

            ds = data.to_dataset()
        else:
            ds = data

        self._data: xr.Dataset = ds

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self.data.equals(other.data)

    @property
    def data(self) -> xr.Dataset:
        return self._data

    def append(
        self,
        other: Union[xr.Dataset, xr.DataArray],
        default_name: str = "default",
    ) -> None:
        if isinstance(other, xr.DataArray):
            if other.name is None:
                ds: xr.Dataset = other.to_dataset(name=default_name)
            else:
                ds = other.to_dataset()
        else:
            ds = other

        if self._data.equals(xr.Dataset()):
            result = ds  # ToDo : Is it needed to copy?
        else:
            combined_result = xr.combine_by_coords([self._data, ds])

            # TODO: This is only for mypy. Improve this.
            assert isinstance(combined_result, xr.Dataset)
            result = combined_result

        self._data = result
