"""Gordo client dataframes methods."""
import io

import dateutil
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def dataframe_into_parquet_bytes(df: pd.DataFrame, compression: str = "snappy") -> bytes:
    """
    Convert a dataframe into bytes representing a parquet table.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame to be compressed
    compression: str
        Compression to use, passed to  :func:`pyarrow.parquet.write_table`

    Returns
    -------
    bytes
    """
    table = pa.Table.from_pandas(df)
    buf = pa.BufferOutputStream()
    pq.write_table(table, buf, compression=compression)
    return buf.getvalue().to_pybytes()


def dataframe_from_parquet_bytes(buf: bytes) -> pd.DataFrame:
    """
    Convert bytes representing a parquet table into a pandas dataframe.

    Parameters
    ----------
    buf: bytes
        Bytes representing a parquet table. Can be the direct result from
        `func`::gordo.server.utils.dataframe_into_parquet_bytes

    Returns
    -------
    pandas.DataFrame
    """
    table = pq.read_table(io.BytesIO(buf))
    return table.to_pandas()


def dataframe_to_dict(df: pd.DataFrame) -> dict:
    """
    Convert a dataframe can have a :class:`pandas.MultiIndex` as columns into a dict.

    Each key is the top level column name, and the value is the array
    of columns under the top level name. If it's a simple dataframe, :meth:`pandas.core.DataFrame.to_dict`
    will be used.

    This allows :func:`json.dumps` to be performed, where :meth:`pandas.DataFrame.to_dict()`
    would convert such a multi-level column dataframe into keys of ``tuple`` objects, which are
    not json serializable. However this ends up working with :meth:`pandas.DataFrame.from_dict`

    Parameters
    ----------
    df: pandas.DataFrame
        Dataframe expected to have columns of type :class:`pandas.MultiIndex` 2 levels deep.

    Returns
    -------
    List[dict]
        List of records representing the dataframe in a 'flattened' form.


    Examples
    --------
    >>> import pprint
    >>> import pandas as pd
    >>> import numpy as np
    >>> columns = pd.MultiIndex.from_tuples((f"feature{i}", f"sub-feature-{ii}") for i in range(2) for ii in range(2))
    >>> index = pd.date_range('2019-01-01', '2019-02-01', periods=2)
    >>> df = pd.DataFrame(np.arange(8).reshape((2, 4)), columns=columns, index=index)
    >>> df  # doctest: +NORMALIZE_WHITESPACE
                    feature0                    feature1
               sub-feature-0 sub-feature-1 sub-feature-0 sub-feature-1
    2019-01-01             0             1             2             3
    2019-02-01             4             5             6             7
    >>> serialized = dataframe_to_dict(df)
    >>> pprint.pprint(serialized)
    {'feature0': {'sub-feature-0': {'2019-01-01': 0, '2019-02-01': 4},
                  'sub-feature-1': {'2019-01-01': 1, '2019-02-01': 5}},
     'feature1': {'sub-feature-0': {'2019-01-01': 2, '2019-02-01': 6},
                  'sub-feature-1': {'2019-01-01': 3, '2019-02-01': 7}}}

    """
    # Need to copy, because Python's mutability allowed .index assignment to mutate the passed df
    data = df.copy()
    if isinstance(data.index, pd.DatetimeIndex):
        data.index = data.index.astype(str)
    if isinstance(df.columns, pd.MultiIndex):
        return {
            col: data[col].to_dict() if isinstance(data[col], pd.DataFrame) else pd.DataFrame(data[col]).to_dict()
            for col in data.columns.get_level_values(0)
        }
    else:
        return data.to_dict()


def dataframe_from_dict(data: dict) -> pd.DataFrame:
    """
    The inverse procedure done by :func:`.multi_lvl_column_dataframe_from_dict`
    Reconstructed a MultiIndex column dataframe from a previously serialized one.

    Expects ``data`` to be a nested dictionary where each top level key has a value
    capable of being loaded from :func:`pandas.core.DataFrame.from_dict`

    Parameters
    ----------
    data: dict
        Data to be loaded into a MultiIndex column dataframe

    Returns
    -------
    pandas.core.DataFrame
        MultiIndex column dataframe.

    Examples
    --------
    >>> serialized = {
    ... 'feature0': {'sub-feature-0': {'2019-01-01': 0, '2019-02-01': 4},
    ...              'sub-feature-1': {'2019-01-01': 1, '2019-02-01': 5}},
    ... 'feature1': {'sub-feature-0': {'2019-01-01': 2, '2019-02-01': 6},
    ...              'sub-feature-1': {'2019-01-01': 3, '2019-02-01': 7}}
    ... }
    >>> dataframe_from_dict(serialized)  # doctest: +NORMALIZE_WHITESPACE
                    feature0                    feature1
           sub-feature-0 sub-feature-1 sub-feature-0 sub-feature-1
    2019-01-01             0             1             2             3
    2019-02-01             4             5             6             7
    """

    if isinstance(data, dict) and any(isinstance(val, dict) for val in data.values()):
        keys = data.keys()
        try:
            df: pd.DataFrame = pd.concat((pd.DataFrame.from_dict(data[key]) for key in keys), axis=1, keys=keys)
        except (ValueError, AttributeError):
            df = pd.DataFrame.from_dict(data)
    else:
        df = pd.DataFrame.from_dict(data)

    try:
        df.index = df.index.map(dateutil.parser.isoparse)  # type: ignore
    except (TypeError, ValueError):
        df.index = df.index.map(int)

    df.sort_index(inplace=True)

    return df
