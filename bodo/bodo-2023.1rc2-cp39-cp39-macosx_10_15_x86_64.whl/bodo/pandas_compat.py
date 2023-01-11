import hashlib
import inspect
import warnings
import numpy as np
import pandas as pd
from pandas._libs import lib
pandas_version = tuple(map(int, pd.__version__.split('.')[:2]))
_check_pandas_change = False
if pandas_version < (1, 4):

    def _set_noconvert_columns(self):
        assert self.orig_names is not None
        mjhoh__tqcsv = {dhyts__zyx: rxlp__qerwe for rxlp__qerwe, dhyts__zyx in
            enumerate(self.orig_names)}
        lon__edut = [mjhoh__tqcsv[dhyts__zyx] for dhyts__zyx in self.names]
        sfbf__xhtt = self._set_noconvert_dtype_columns(lon__edut, self.names)
        for lttbf__umn in sfbf__xhtt:
            self._reader.set_noconvert(lttbf__umn)
    if _check_pandas_change:
        lines = inspect.getsource(pd.io.parsers.c_parser_wrapper.
            CParserWrapper._set_noconvert_columns)
        if (hashlib.sha256(lines.encode()).hexdigest() !=
            'afc2d738f194e3976cf05d61cb16dc4224b0139451f08a1cf49c578af6f975d3'
            ):
            warnings.warn(
                'pd.io.parsers.c_parser_wrapper.CParserWrapper._set_noconvert_columns has changed'
                )
    (pd.io.parsers.c_parser_wrapper.CParserWrapper._set_noconvert_columns
        ) = _set_noconvert_columns


def ArrowStringArray__init__(self, values):
    import pyarrow as pa
    from pandas.core.arrays.string_ import StringDtype
    self._dtype = StringDtype(storage='pyarrow')
    if isinstance(values, pa.Array):
        self._data = pa.chunked_array([values])
    elif isinstance(values, pa.ChunkedArray):
        self._data = values
    else:
        raise ValueError(
            f"Unsupported type '{type(values)}' for ArrowStringArray")
    if not (pa.types.is_string(self._data.type) or pa.types.is_large_string
        (self._data.type) or pa.types.is_dictionary(self._data.type) and (
        pa.types.is_string(self._data.type.value_type) or pa.types.
        is_large_string(self._data.type.value_type)) and pa.types.is_int32(
        self._data.type.index_type)):
        raise ValueError(
            'ArrowStringArray requires a PyArrow (chunked) array of string type'
            )


if _check_pandas_change:
    lines = inspect.getsource(pd.core.arrays.string_arrow.ArrowStringArray.
        __init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'cbb9683b2e91867ef12470d4fda28ca6243fbb7b4f78ac2472fca805607c0942':
        warnings.warn(
            'pd.core.arrays.string_arrow.ArrowStringArray.__init__ has changed'
            )
pd.core.arrays.string_arrow.ArrowStringArray.__init__ = (
    ArrowStringArray__init__)


def factorize(self, na_sentinel: int=-1):
    import numpy as np
    import pyarrow as pa
    ucx__inj = self._data if pa.types.is_dictionary(self._data.type
        ) else self._data.dictionary_encode()
    whxx__zea = pa.chunked_array([jli__hhvfd.indices for jli__hhvfd in
        ucx__inj.chunks], type=ucx__inj.type.index_type).to_pandas()
    if whxx__zea.dtype.kind == 'f':
        whxx__zea[np.isnan(whxx__zea)] = na_sentinel
    whxx__zea = whxx__zea.astype(np.int64, copy=False)
    if ucx__inj.num_chunks:
        jghrr__tclrd = type(self)(ucx__inj.chunk(0).dictionary)
    else:
        jghrr__tclrd = type(self)(pa.array([], type=ucx__inj.type.value_type))
    return whxx__zea.values, jghrr__tclrd


if _check_pandas_change:
    lines = inspect.getsource(pd.core.arrays.string_arrow.ArrowStringArray.
        factorize)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '80669a609cfe11b362dacec6bba8e5bf41418b35d0d8b58246a548858320efd9':
        warnings.warn(
            'pd.core.arrays.string_arrow.ArrowStringArray.factorize has changed'
            )
pd.core.arrays.string_arrow.ArrowStringArray.factorize = factorize


def to_numpy(self, dtype=None, copy: bool=False, na_value=lib.no_default
    ) ->np.ndarray:
    usgi__gty = self._data.combine_chunks() if len(self) != 0 else self._data
    tmim__iyo = np.array(usgi__gty, dtype=dtype)
    if self._data.null_count > 0:
        if na_value is lib.no_default:
            if dtype and np.issubdtype(dtype, np.floating):
                return tmim__iyo
            na_value = self._dtype.na_value
        pxdh__hfza = self.isna()
        tmim__iyo[pxdh__hfza] = na_value
    return tmim__iyo


if _check_pandas_change:
    lines = inspect.getsource(pd.core.arrays.string_arrow.ArrowStringArray.
        to_numpy)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '2f49768c0cb51d06eb41882aaf214938f268497fffa07bf81964a5056d572ea3':
        warnings.warn(
            'pd.core.arrays.string_arrow.ArrowStringArray.to_numpy has changed'
            )
pd.core.arrays.string_arrow.ArrowStringArray.to_numpy = to_numpy
