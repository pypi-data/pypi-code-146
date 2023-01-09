"""Module containing BaseSource class.

BaseSource is the abstract data source class from which all concrete data sources
must inherit.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
import inspect
import logging
import os
from pathlib import Path
import shutil
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    TypeVar,
    Union,
    cast,
)

from mypy_extensions import Arg, DefaultNamedArg, KwArg, VarArg
import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_datetime64_any_dtype as is_datetime

from bitfount.data.datasources.utils import _modify_column, _modify_file_paths
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.data.exceptions import DataNotLoadedError
from bitfount.data.types import (
    DataPathModifiers,
    _Column,
    _GetColumnCallable,
    _GetDtypesCallable,
)
from bitfount.data.utils import _generate_dtypes_hash, _hash_str
from bitfount.types import _Dtypes
from bitfount.utils import delegates, seed_all

logger = logging.getLogger(__name__)


T = TypeVar("T", bound="BaseSource")
BaseSourceInitSignature = Callable[
    [
        Arg(T, "self"),  # noqa: F821
        VarArg(Any),
        DefaultNamedArg(Optional[DatasetSplitter], "data_splitter"),  # noqa: F821
        DefaultNamedArg(Optional[int], "seed"),  # noqa: F821
        DefaultNamedArg(
            Optional[Dict[str, DataPathModifiers]], "modifiers"  # noqa: F821
        ),
        DefaultNamedArg(Union[str, Sequence[str], None], "ignore_cols"),  # noqa: F821
        KwArg(Any),
    ],
    None,
]


class BaseSource(ABC):
    """Abstract Base Source from which all other data sources must inherit.

    Args:
        data_splitter: Approach used for splitting the data into training, test,
            validation. Defaults to None.
        seed: Random number seed. Used for setting random seed for all libraries.
            Defaults to None.
        modifiers: Dictionary used for modifying paths/ extensions in the dataframe.
            Defaults to None.
        ignore_cols: Column/list of columns to be ignored from the data.
            Defaults to None.

    Attributes:
        data: A Dataframe-type object which contains the data.
        data_splitter: Approach used for splitting the data into training, test,
            validation.
        seed: Random number seed. Used for setting random seed for all libraries.
    """

    def __init__(
        self,
        data_splitter: Optional[DatasetSplitter] = None,
        seed: Optional[int] = None,
        modifiers: Optional[Dict[str, DataPathModifiers]] = None,
        ignore_cols: Optional[Union[str, Sequence[str]]] = None,
        **kwargs: Any,
    ) -> None:
        self._base_source_init = True
        self.data_splitter = data_splitter
        self.seed = seed
        self._modifiers = modifiers
        self._data_is_split: bool = False
        self._data_is_loaded: bool = False
        seed_all(self.seed)

        self._train_idxs: Optional[np.ndarray] = None
        self._validation_idxs: Optional[np.ndarray] = None
        self._test_idxs: Optional[np.ndarray] = None

        self._data: pd.DataFrame
        self._table_hashes: Set[str] = set()

        self._ignore_cols: List[str] = []
        if isinstance(ignore_cols, str):
            self._ignore_cols = [ignore_cols]
        elif ignore_cols is not None:
            self._ignore_cols = list(ignore_cols)

        for unexpected_kwarg in kwargs:
            logger.warning(f"Ignoring unexpected keyword argument {unexpected_kwarg}")

        super().__init__()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        if not (inspect.isabstract(cls) or ABC in cls.__bases__):
            cls.get_dtypes = cls._get_dtypes()  # type: ignore[assignment] # reason: wrap subclass get_dtypes # noqa: B950
            cls.get_column = cls._get_column()  # type: ignore[assignment] # reason: wrap subclass get_column # noqa: B950

    @classmethod
    def _get_dtypes(cls) -> _GetDtypesCallable:
        """Decorate subclass' get_dtypes implementation.

        Decorate subclass' implementation of get_dtypes to handle ignored
        columns and handle `_table_hashes`.
        """
        subclass_get_dtypes = cls.get_dtypes

        def get_dtypes(self: BaseSource, *args: Any, **kwargs: Any) -> _Dtypes:
            dtypes: _Dtypes = subclass_get_dtypes(self, *args, **kwargs)
            if self._ignore_cols:
                for col in self._ignore_cols:
                    if col in dtypes:
                        del dtypes[col]
            self._table_hashes.add(_generate_dtypes_hash(dtypes))
            return dtypes

        return get_dtypes

    @classmethod
    def _get_column(
        cls,
    ) -> _GetColumnCallable:
        """Decorate subclass' get_column implementation.

        Decorate subclass' implementation of get_column to handle ignored
        columns and modifiers.
        """
        subclass_get_column = cls.get_column

        def get_column(
            self: BaseSource, col_name: str, *args: Any, **kwargs: Any
        ) -> _Column:

            column = subclass_get_column(self, col_name, *args, **kwargs)
            if self._modifiers:
                if modifier_dict := self._modifiers.get(col_name):
                    column = _modify_column(column, modifier_dict)
            return column

        return get_column

    @property
    def is_initialised(self) -> bool:
        """Checks if `BaseSource` was initialised."""
        if hasattr(self, "_base_source_init"):
            return True
        else:
            return False

    @property
    def data(self) -> pd.DataFrame:
        """A property containing the underlying dataframe if the data has been loaded.

        Raises:
            DataNotLoadedError: If the data has not been loaded yet.
        """
        if self._data_is_loaded:
            return self._data
        else:
            raise DataNotLoadedError(
                "Data is not loaded yet. Please call `load_data` first."
            )

    @data.setter
    def data(self, _data: Optional[pd.DataFrame]) -> None:
        """Data setter."""
        if _data is not None:
            if isinstance(_data, pd.DataFrame):

                if self._ignore_cols:
                    # If columns already ignored in data, ignore errors.
                    _data = _data.drop(columns=self._ignore_cols, errors="ignore")
                self._data = _data

                if self._modifiers:
                    _modify_file_paths(self._data, self._modifiers)

                self._data_is_loaded = True
            else:
                raise TypeError(
                    "Invalid data attribute. "
                    "Expected pandas dataframe for attribute 'data' "
                    f"but received :{type(_data)}"
                )

    @property
    def hash(self) -> str:
        """The hash associated with this BaseSource.

        This is the hash of the static information regarding the underlying DataFrame,
        primarily column names and content types but NOT anything content-related
        itself. It should be consistent across invocations, even if additional data
        is added, as long as the DataFrame is still compatible in its format.

        Returns:
            The hexdigest of the DataFrame hash.
        """
        if not self._table_hashes:
            raise DataNotLoadedError(
                "Data is not loaded yet. Please call `get_dtypes` first."
            )
        else:
            return _hash_str(str(sorted(self._table_hashes)))

    @staticmethod
    def _get_data_dtypes(data: pd.DataFrame) -> _Dtypes:
        """Returns the nullable column types of the dataframe.

        This is called by the `get_dtypes` method. This method also overrides datetime
        column dtypes to be strings. This is not done for date columns which are of
        type object.
        """
        data = cast(pd.DataFrame, data.convert_dtypes())
        dtypes: _Dtypes = data.dtypes.to_dict()
        for name in list(dtypes):
            if is_datetime(data[name]):
                dtypes[name] = pd.StringDtype()

        return dtypes

    def load_data(self, **kwargs: Any) -> None:
        """Load the data for the datasource.

        Raises:
            TypeError: If data format is not supported.
        """
        if not self._data_is_loaded and (data := self.get_data(**kwargs)) is not None:
            self.data = data

    @abstractmethod
    def get_values(
        self, col_names: List[str], **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Implement this method to get distinct values from list of columns."""
        raise NotImplementedError

    @abstractmethod
    def get_column(self, col_name: str, **kwargs: Any) -> _Column:
        """Implement this method to get single column from dataset.

        Used in the `ColumnAverage` algorithm as well as to iterate over image columns
        for the purposes of schema generation.
        """
        raise NotImplementedError

    @abstractmethod
    def get_data(self, **kwargs: Any) -> Optional[pd.DataFrame]:
        """Implement this method to load and return dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Implement this method to get the columns and column types from dataset."""
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        """Implement this method to get the number of rows in the dataset."""
        raise NotImplementedError

    @property
    def multi_table(self) -> bool:
        """This returns False if the DataSource does not subclass `MultiTableSource`.

        However this property must be re-implemented in `MultiTableSource`, therefore it
        is not necessarily True if the DataSource inherits from `MultiTableSource`.
        """
        return False

    @property
    def iterable(self) -> bool:
        """This returns False if the DataSource does not subclass `IterableSource`.

        However this property must be re-implemented in `IterableSource`, therefore it
        is not necessarily True if the DataSource inherits from `IterableSource`.
        """
        return False


@delegates()
class MultiTableSource(BaseSource, ABC):
    """Abstract base source that supports multiple tables.

    This class is used to define a data source that supports multiple tables. The
    datasources do not necessarily have multiple tables though.
    """

    @property
    @abstractmethod
    def multi_table(self) -> bool:
        """Implement this method to define whether the data source is multi-table.

        The datasource must inherit from `MultiTableSource` if this is True. However,
        the inverse is not necessarily True.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def table_names(self) -> List[str]:
        """Implement this to return a list of table names.

        If there is only one table, it should return a list with one element.
        """
        raise NotImplementedError

    @abstractmethod
    def _validate_table_name(self, table_name: str) -> None:
        """Validate the table name exists in the multi-table datasource.

        This method should raise a ValueError if the table_name is not valid.
        """
        raise NotImplementedError

    @abstractmethod
    def get_values(
        self, col_names: List[str], table_name: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Implement this method to get distinct values from list of columns."""
        raise NotImplementedError

    @abstractmethod
    def get_column(
        self, col_name: str, table_name: Optional[str] = None, **kwargs: Any
    ) -> _Column:
        """Implement this method to get single column from dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_data(
        self, table_name: Optional[str] = None, **kwargs: Any
    ) -> Optional[pd.DataFrame]:
        """Implement this method to loads and return dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_dtypes(self, table_name: Optional[str] = None, **kwargs: Any) -> _Dtypes:
        """Implement this method to get the columns and column types from dataset."""
        raise NotImplementedError


@delegates()
class IterableSource(BaseSource, ABC):
    """Abstract base source that supports iterating over the data.

    This is used for streaming data in batches as opposed to loading the entire dataset
    into memory.

    Args:
        partition_size: The size of each partition when iterating over the data.
    """

    def __init__(
        self,
        partition_size: int = 100,
        **kwargs: Any,
    ) -> None:
        self.partition_size = partition_size
        super().__init__(**kwargs)

    @property
    @abstractmethod
    def iterable(self) -> bool:
        """Implement this method to define whether the data source is iterable.

        The datasource must inherit from `IterableSource` if this is True. However,
        the inverse is not necessarily True.
        """
        raise NotImplementedError

    @abstractmethod
    def get_data(self, **kwargs: Any) -> Optional[pd.DataFrame]:
        """This method must return None if the data source is iterable."""
        raise NotImplementedError

    @abstractmethod
    def yield_data(self, **kwargs: Any) -> Iterator[pd.DataFrame]:
        """Implement this method to yield dataframes."""
        raise NotImplementedError


@delegates()
class FileSystemIterableSource(IterableSource, ABC):
    """Abstract base source that supports iterating over file-based data.

    This is used for Iterable data sources that whose data is stored as files on disk.

    Args:
        path: Path to the the directory which contains the data files. Sub-directories
            will be searched recursively.
        output_path: The path where to save intermediary output files. Defaults to
            'preprocessed/'.
        iterable: Whether the data source is iterable. This is used to determine
            whether the data source can be used in a streaming context during a task.
            Defaults to False.
        fast_load: Whether the data will be loaded in fast mode. This is used to
            determine whether the data will be iterated over during set up for schema
            generation and splitting (where necessary). Only relevant if `iterable` is
            True, otherwise it is ignored. Defaults to False.
        file_extension: File extension of the data files. If None, all files will be
            searched.
    """

    def __init__(
        self,
        path: Union[os.PathLike, str],
        output_path: Union[os.PathLike, str] = "preprocessed/",
        iterable: bool = False,
        fast_load: bool = False,
        file_extension: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.path = Path(path)
        self.out_path = Path(output_path)
        self.out_path.mkdir(exist_ok=True, parents=True)  # create if not exists

        self._iterable = iterable
        self.fast_load = fast_load
        self.file_extension = (
            f".{file_extension}"
            if file_extension and not file_extension.startswith(".")
            else file_extension
        )

    @property
    def file_names(self) -> List[str]:
        """Returns a list of file names in the directory."""
        files = [x for x in self.path.glob("**/*") if x.is_file()]
        if self.file_extension:
            files = [x for x in files if x.suffix == self.file_extension]

        return [str(x.resolve()) for x in files]

    @property
    def iterable(self) -> bool:
        """Defines whether the data source is iterable.

        This is defined by the user when instantiating the class.
        """
        return self._iterable

    @abstractmethod
    def _get_data(
        self, file_names: Optional[List[str]] = None, **kwargs: Any
    ) -> pd.DataFrame:
        """Implement to return data corresponding to the provided file names.

        This method is called under the hood by `get_data` and `yield_data`.

        Args:
            file_names: List of file names to load. If None, all files should be
                loaded.

        Returns:
            A dataframe containing the data.
        """
        raise NotImplementedError

    def get_values(
        self, col_names: List[str], **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in the dataset.

        Args:
            col_names: The list of the columns whose distinct values should be
                returned.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.
        """
        dic: Dict[str, Iterable[Any]] = {}
        if self._data_is_loaded and len(self.data) == len(self.file_names):
            pass
        elif self.iterable:
            dfs = []
            for df in self.yield_data(**kwargs):
                dfs.append(df)
            self.data = pd.concat(dfs)
        else:
            self.data = self._get_data()

        for col in col_names:
            try:
                dic[col] = self.data[col].unique()
            except TypeError:
                logger.warning(f"Found unhashable value type, skipping column {col}.")
        return dic

    def get_column(self, col_name: str, **kwargs: Any) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from the dataset.

        Args:
            col_name: The name of the column which should be loaded.

        Returns:
            The column request as a series.
        """
        if self._data_is_loaded and len(self.data) == len(self.file_names):
            pass
        elif self.iterable:
            dfs = []
            for df in self.yield_data(**kwargs):
                dfs.append(df)
            self.data = pd.concat(dfs)
        else:
            self.data = self._get_data()

        return self.data[col_name]

    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Loads and returns the column names and types of the dataframe.

        If `fast_load` is set to True, only the first file will be loaded to get the
        column names and types. Otherwise all files will be loaded.

        Returns:
            A mapping from column names to column types.
        """
        if self._data_is_loaded and len(self.data) == len(self.file_names):
            pass
        elif self.fast_load:
            self.data = self._get_data(file_names=[self.file_names[0]], **kwargs)
        elif self.iterable:
            dfs = []
            for df in self.yield_data(**kwargs):
                dfs.append(df)
            self.data = pd.concat(dfs)
        else:
            self.data = self._get_data(**kwargs)

        return self._get_data_dtypes(self.data)

    def yield_data(
        self, file_names: Optional[List[str]] = None, **kwargs: Any
    ) -> Iterator[pd.DataFrame]:
        """Yields data in batches from files that match the given file names.

        Args:
            file_names: An optional list of file names to use for yielding data.
                Otherwise all files that have already been found will be used.
                `file_names` is always provided when this method is called from the
                Dataset as part of a task.

        Raises:
            ValueError: If no file names provided and no files have been found.
        """
        if not file_names and not self.file_names:
            raise ValueError("No files found to yield data from.")

        file_names = file_names or self.file_names

        for file_names_partition in self.partition(file_names, self.partition_size):
            file_names_partition = cast(List[str], file_names_partition)
            yield self._get_data(file_names_partition)
            # Delete the files after they have been processed and used
            self._cleanup(file_names_partition)

    def get_data(self, **kwargs: Any) -> Optional[pd.DataFrame]:
        """Returns data if the datasource is not iterable, otherwise None."""
        if self.iterable:
            return None

        # We don't reload the data if it has already been loaded. We are assuming that
        # files are only added, not removed, meaning we can rely on simply matching the
        # number of files detected with the length of the dataframe to ascertain whether
        # the data has already been loaded.
        if self._data_is_loaded and len(self.data) == len(self.file_names):
            return self.data

        return self._get_data(**kwargs)

    def _recreate_file_structure(self, file_path: str, exist_ok: bool) -> Path:
        """Recreates the file structure in the output directory.

        This is used to ensure that the output directory has the same structure as the
        input directory. This is useful for when the input data is partitioned into
        subdirectories.

        Args:
            file_path: The file name to recreate the structure for.
            exist_ok: Whether to raise an error if the directory already exists.

        Returns:
            The path to the recreated file structure.

        Raises:
            FileExistsError: If the subdir already exists in the output directory and
                `exist_ok` is False.
        """
        path = Path(file_path)
        file_id = path.stem
        parent_path = path.parent.absolute()
        # Relative path gets the path of the original file relative to the specified
        # input path. This relative path is then used to recreate the file structure
        # in the output directory with the original filename being used as a
        # subdirectory instead containing any relevant extracted files.
        relative_path = parent_path.relative_to(self.path.absolute())
        save_prefix = self.out_path / relative_path / file_id
        save_prefix.mkdir(parents=True, exist_ok=exist_ok)
        return save_prefix

    def _cleanup(self, file_names: List[str]) -> None:
        """Remove intermediate files creating during yielding of partitions.

        Intended to be called by `yield_data` every partition.
        """
        for file_name in file_names:
            save_dir = self._recreate_file_structure(file_name, exist_ok=True)
            shutil.rmtree(save_dir)

    @staticmethod
    def partition(iterable: Sequence, partition_size: int = 1) -> Iterable:
        """Takes an iterable and yields partitions of size `partition_size`.

        The final partition may be less than size `partition_size` due to the variable
        length of the iterable.
        """
        len_ = len(iterable)
        for partition_start_idx in range(0, len_, partition_size):
            yield iterable[
                partition_start_idx : min(partition_start_idx + partition_size, len_)
            ]

    def load_data(self, **kwargs: Any) -> None:
        """Load the data for the datasource.

        Raises:
            TypeError: If data format is not supported.
        """
        if (data := self.get_data(**kwargs)) is not None:
            self.data = data

    def __len__(self) -> int:
        return len(self.file_names)
