from __future__ import annotations
from abc import ABC
from pathlib import Path

import xarray as xr
import pandas as pd
from typing import Any, List, Union

from mfire.settings import get_logger

LOGGER = get_logger(name="sit_gen.preprocessing")


class ABCPreprocessing(ABC):
    """Abstract Preprocessing class.

    Preprocessing classes have two main methods:
        - fit : for fitting the self object to given DataArray or Dataset
        - transform : for transforming a given DataArray or Dataset

    Preprocessing parameters are stored in the self.params_df DataFrame object,
    that contains the self.params_names columns.

    This ABC class relies on the two main not implement (yet) private methods:
        - _fit_dataarray
        - _transform_dataarray
    which describes the preprocessing to apply on DataArray (here DataArrays are
    the most atomic piece of data).

    Thus, any class inheriting from ABCPreprocessing must implement these two
    methods to work.
    """

    params_names: List[str] = None

    def __init__(self, params_df: pd.DataFrame = None):
        self.params_df = pd.DataFrame(columns=self.params_names)
        if params_df is not None:
            self.params_df = pd.concat([self.params_df, params_df])

    @classmethod
    def read_csv(cls, filename: Path, index_col: int = 0, **kwargs) -> ABCPreprocessing:
        """Retrieve a DataFrame out of a given CSV file and returns the corresponding
        ABCPreprocessing object.

        Args:
            filename (Path): CSV file's name
            index_col (int, optional): Index column. Defaults to 0.

        Returns:
            ABCPreprocessing: Corresponding ABCPreprocessing object.
        """
        return cls(
            pd.read_csv(filename, index_col=index_col, **kwargs)[cls.params_names]
        )

    def to_csv(self, filename: Path, **kwargs):
        """Dumps the self.params_df to a CSV file.

        Args:
            filename (Path): CSV file's name to dump the DataFrame.
        """
        self.params_df.to_csv(filename, **kwargs)

    def __getitem__(self, index: Any):
        return self.params_df.loc[index, self.params_names]

    def __setitem__(self, index: Any, value: Any):
        self.params_df.loc[index, self.params_names] = value

    def _transform_dataarray(self, data: xr.DataArray) -> xr.DataArray:
        """Method to apply the preprocessing parameters to a given dataarray.
        In this ABC class, the method is still not implemented.
        Any class inheriting from this class must implement this method to work.

        Args:
            data (xr.DataArray): DataArray to preprocess.

        Raises:
            NotImplementedError: Currently raised due to belonging to an ABC class.

        Returns:
            xr.DataArray: Preprocessed dataarray.
        """
        raise NotImplementedError

    def _transform_dataset(self, data: xr.Dataset) -> xr.Dataset:
        """Method to apply the preprocessing parameters to a given dataset.
        This method relies on the self._transform_datarray method.

        Args:
            data (xr.Dataset): Dataset to preprocess.

        Returns:
            xr.Dataset: Preprocessed dataset.
        """
        LOGGER.debug(f"{self.__class__.__name__}.transform_dataset")
        return xr.merge([self._transform_dataarray(data[var]) for var in data])

    def transform(
        self, data: Union[xr.DataArray, xr.Dataset]
    ) -> Union[xr.DataArray, xr.Dataset]:
        """Main method for applying the preprocessing parameters to the given data.

        Args:
            data (Union[xr.DataArray, xr.Dataset]): Data to apply the pre-processing
                onto.

        Returns:
            Union[xr.DataArray, xr.Dataset]: The preprocessed data.
        """
        if isinstance(data, xr.DataArray):
            return self._transform_dataarray(data)
        return self._transform_dataset(data)

    def _fit_dataarray(self, data: xr.DataArray) -> None:
        """Method to fit the preprocessing parameters out of a given dataarray.
        The fitted parameters are stored in self.params_df.

        In this ABC class, the method is still not implemented.
        Any class inheriting from this class must implement this method to work.

        Args:
            data (xr.DataArray): Dataarray to fit.

        Raises:
            NotImplementedError: Currently raised due to belonging to an ABC class.

        """
        raise NotImplementedError

    def _fit_dataset(self, data: xr.Dataset) -> None:
        """Method to fit the preprocessing parameters out of a given dataset.
        The fitted parameters are stored in the self.params_df.
        This method relies on the self._fit_dataarray method.

        Args:
            data (xr.Dataset): Dataset to fit.
        """
        LOGGER.debug(f"{self.__class__.__name__}.fit_dataset")
        for var in data:
            self._fit_dataarray(data[var])

    def fit(self, data: Union[xr.DataArray, xr.Dataset]) -> None:
        """Main method to fit preprocessing parameters out of a given piece of data.

        Args:
            data (Union[xr.DataArray, xr.Dataset]): Data to fit.
        """
        if isinstance(data, xr.DataArray):
            self._fit_dataarray(data)
        else:
            self._fit_dataset(data)

    def __repr__(self) -> str:
        return f"{self.__class__}\n{self.params_df}"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, self.__class__):
            try:
                return all(self.params_df == __o.params_df)
            except ValueError:
                return False
        return False


class Normalizer(ABCPreprocessing):
    """Usual Mean and Standard Deviation normalizer.

    norm_data = (data - mean) / std

    >>> norm = Normalizer()
    >>> ds = xr.Dataset(
        {
            "toto": ("t", [1, 2, 3]),
            "tata": ("t", [10, 20, 40]),
        },
        coords={"t":[0, 1, 2]}
    )
    >>> ds
    <xarray.Dataset>
    Dimensions:  (t: 3)
    Coordinates:
    * t        (t) int64 0 1 2
    Data variables:
        toto     (t) int64 1 2 3
        tata     (t) int64 10 20 40
    >>> norm.fit(ds)
    >>> norm
    <class 'mfire.sit_gen.preprocessing.Normalizer'>
            mean        std
    toto        2.0   0.816497
    tata  23.333333  12.472191
    >>> norm.transform(ds)
    <xarray.Dataset>
    Dimensions:  (t: 3)
    Coordinates:
    * t        (t) int64 0 1 2
    Data variables:
        toto     (t) float64 -1.225 0.0 1.225
        tata     (t) float64 -1.069 -0.2673 1.336
    """

    params_names: List[str] = ["mean", "std"]

    def _transform_dataarray(self, data: xr.DataArray) -> xr.DataArray:
        """Method to normalize a given dataarray.

        Args:
            data (xr.DataArray): DataArray to normalize.

        Returns:
            xr.DataArray: Normalized DataArray.
        """
        LOGGER.debug(f"{self.__class__.__name__}.transform({data.name})")
        mean, std = self[data.name]
        return (data - mean) / std

    def _fit_dataarray(self, data: xr.DataArray):
        """Method to fit normalization parameters (mean and standard deviation) from
        a given dataarray

        Args:
            data (xr.DataArray): Dataarray to fit.
        """
        LOGGER.debug(f"{self.__class__.__name__}.fit({data.name})")
        self[data.name] = (float(data.mean().values), float(data.std().values))


class MinMaxScaler(ABCPreprocessing):
    """Usual Min Max Scaler.

    norm_data = (data - min) / (max - min)

    >>> scaler = MinMaxScaler()
    >>> ds = xr.Dataset(
        {
            "toto": ("t", [1, 2, 3]),
            "tata": ("t", [10, 20, 40]),
        },
        coords={"t":[0, 1, 2]}
    )
    >>> ds
    <xarray.Dataset>
    Dimensions:  (t: 3)
    Coordinates:
    * t        (t) int64 0 1 2
    Data variables:
        toto     (t) int64 1 2 3
        tata     (t) int64 10 20 40
    >>> scaler.fit(ds)
    >>> scaler
    <class 'mfire.sit_gen.preprocessing.MinMaxScaler'>
        min   max
    toto   1.0   3.0
    tata  10.0  40.0
    >>> scaler.transform(ds)
    <xarray.Dataset>
    Dimensions:  (t: 3)
    Coordinates:
    * t        (t) int64 0 1 2
    Data variables:
        toto     (t) float64 0.0 0.5 1.0
        tata     (t) float64 0.0 0.3333 1.0
    """

    params_names: List[str] = ["min", "max"]

    def _transform_dataarray(self, data: xr.DataArray) -> xr.DataArray:
        """Method for MinMax-scaling a given dataarray.

        Args:
            data (xr.DataArray): DataArray to scale.

        Returns:
            xr.DataArray: Scaled Dataarray
        """
        LOGGER.debug(f"{self.__class__.__name__}.transform({data.name})")
        mini, maxi = self[data.name]
        return (data - mini) / (maxi - mini)

    def _fit_dataarray(self, data: xr.DataArray):
        """Method for fitting the MinMaxScaler parameters (min and max) out of a given
        dataarray

        Args:
            data (xr.DataArray): DataArray to fit
        """
        LOGGER.debug(f"{self.__class__.__name__}.fit({data.name})")
        self[data.name] = (float(data.min().values), float(data.max().values))


def open_preprocessing(
    filename: Path, index_col: int = 0, **kwargs
) -> Normalizer | MinMaxScaler:
    """Read a CSV file containing preprocessing parameters and returns
    the corresponding Preprocessing Object

    Args:
        filename (Path): CSV filename
        index_col (int, optional): Index colum. Defaults to 0.

    Returns:
        Preprocessing: Preprocessing object.
    """
    df = pd.read_csv(filename, index_col=index_col, **kwargs)
    return next(
        cls(df)
        for cls in (Normalizer, MinMaxScaler)
        if set(cls.params_names).issubset(df)
    )


__all__ = ["open_preprocessing", "Normalizer", "MinMaxScaler"]
