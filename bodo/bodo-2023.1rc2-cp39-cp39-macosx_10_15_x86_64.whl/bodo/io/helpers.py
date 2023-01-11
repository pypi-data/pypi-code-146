"""
File that contains some IO related helpers.
"""
import os
import threading
import uuid
import numba
import pyarrow as pa
from mpi4py import MPI
from numba.core import types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, models, register_model, typeof_impl, unbox
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.time_ext import TimeArrayType, TimeType
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.typing import BodoError, raise_bodo_error


class PyArrowTableSchemaType(types.Opaque):

    def __init__(self):
        super(PyArrowTableSchemaType, self).__init__(name=
            'PyArrowTableSchemaType')


pyarrow_table_schema_type = PyArrowTableSchemaType()
types.pyarrow_table_schema_type = pyarrow_table_schema_type
register_model(PyArrowTableSchemaType)(models.OpaqueModel)


@unbox(PyArrowTableSchemaType)
def unbox_pyarrow_table_schema_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(PyArrowTableSchemaType)
def box_pyarrow_table_schema_type(typ, val, c):
    c.pyapi.incref(val)
    return val


@typeof_impl.register(pa.lib.Schema)
def typeof_pyarrow_table_schema(val, c):
    return pyarrow_table_schema_type


@lower_constant(PyArrowTableSchemaType)
def lower_pyarrow_table_schema(context, builder, ty, pyval):
    iyrw__boiks = context.get_python_api(builder)
    return iyrw__boiks.unserialize(iyrw__boiks.serialize_object(pyval))


def is_nullable(typ):
    return bodo.utils.utils.is_array_typ(typ, False) and (not isinstance(
        typ, types.Array) and not isinstance(typ, bodo.DatetimeArrayType))


def pa_schema_unify_reduction(schema_a, schema_b, unused):
    return pa.unify_schemas([schema_a, schema_b])


pa_schema_unify_mpi_op = MPI.Op.Create(pa_schema_unify_reduction, commute=True)
use_nullable_pd_arr = True
_pyarrow_numba_type_map = {pa.bool_(): types.bool_, pa.int8(): types.int8,
    pa.int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.
    int64, pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32():
    types.uint32, pa.uint64(): types.uint64, pa.float32(): types.float32,
    pa.float64(): types.float64, pa.string(): string_type, pa.large_string(
    ): string_type, pa.binary(): bytes_type, pa.date32():
    datetime_date_type, pa.date64(): types.NPDatetime('ns'), pa.time32('s'):
    TimeType(0), pa.time32('ms'): TimeType(3), pa.time64('us'): TimeType(6),
    pa.time64('ns'): TimeType(9), pa.null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    hirf__fyc = ['ns', 'us', 'ms', 's']
    if pa_ts_typ.unit not in hirf__fyc:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        atoo__oyg = pa_ts_typ.to_pandas_dtype().tz
        bmmpr__hmaq = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            atoo__oyg)
        return bodo.DatetimeArrayType(bmmpr__hmaq), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ: pa.Field, is_index,
    nullable_from_metadata, category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        zlfs__rpmwu, prbpm__xvwok = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(zlfs__rpmwu), prbpm__xvwok
    if isinstance(pa_typ.type, pa.StructType):
        csbhq__xcqvu = []
        upaid__vbe = []
        prbpm__xvwok = True
        for oayl__ztlz in pa_typ.flatten():
            upaid__vbe.append(oayl__ztlz.name.split('.')[-1])
            fejn__jcuqx, atmg__sbiwx = _get_numba_typ_from_pa_typ(oayl__ztlz,
                is_index, nullable_from_metadata, category_info)
            csbhq__xcqvu.append(fejn__jcuqx)
            prbpm__xvwok = prbpm__xvwok and atmg__sbiwx
        return StructArrayType(tuple(csbhq__xcqvu), tuple(upaid__vbe)
            ), prbpm__xvwok
    if isinstance(pa_typ.type, pa.Decimal128Type):
        return DecimalArrayType(pa_typ.type.precision, pa_typ.type.scale), True
    if str_as_dict:
        if pa_typ.type != pa.string():
            raise BodoError(
                f'Read as dictionary used for non-string column {pa_typ}')
        return dict_str_arr_type, True
    if isinstance(pa_typ.type, pa.DictionaryType):
        if pa_typ.type.value_type != pa.string():
            raise BodoError(
                f'Parquet Categorical data type should be string, not {pa_typ.type.value_type}'
                )
        qnx__whjeo = _pyarrow_numba_type_map[pa_typ.type.index_type]
        fzk__idr = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=qnx__whjeo)
        return CategoricalArrayType(fzk__idr), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pyarrow_numba_type_map:
        usyw__vbv = _pyarrow_numba_type_map[pa_typ.type]
        prbpm__xvwok = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if usyw__vbv == datetime_date_type:
        return datetime_date_array_type, prbpm__xvwok
    if isinstance(usyw__vbv, TimeType):
        return TimeArrayType(usyw__vbv.precision), prbpm__xvwok
    if usyw__vbv == bytes_type:
        return binary_array_type, prbpm__xvwok
    zlfs__rpmwu = (string_array_type if usyw__vbv == string_type else types
        .Array(usyw__vbv, 1, 'C'))
    if usyw__vbv == types.bool_:
        zlfs__rpmwu = boolean_array
    kztz__knk = (use_nullable_pd_arr if nullable_from_metadata is None else
        nullable_from_metadata)
    if kztz__knk and not is_index and isinstance(usyw__vbv, types.Integer
        ) and pa_typ.nullable:
        zlfs__rpmwu = IntegerArrayType(usyw__vbv)
    if (kztz__knk and bodo.libs.float_arr_ext._use_nullable_float and not
        is_index and isinstance(usyw__vbv, types.Float) and pa_typ.nullable):
        zlfs__rpmwu = FloatingArrayType(usyw__vbv)
    return zlfs__rpmwu, prbpm__xvwok


_numba_pyarrow_type_map = {types.bool_: pa.bool_(), types.int8: pa.int8(),
    types.int16: pa.int16(), types.int32: pa.int32(), types.int64: pa.int64
    (), types.uint8: pa.uint8(), types.uint16: pa.uint16(), types.uint32:
    pa.uint32(), types.uint64: pa.uint64(), types.float32: pa.float32(),
    types.float64: pa.float64(), types.NPDatetime('ns'): pa.date64()}


def is_nullable_arrow_out(numba_type: types.ArrayCompatible) ->bool:
    return is_nullable(numba_type) or isinstance(numba_type, bodo.
        DatetimeArrayType) or isinstance(numba_type, types.Array
        ) and numba_type.dtype == bodo.datetime64ns


def _numba_to_pyarrow_type(numba_type: types.ArrayCompatible, is_iceberg:
    bool=False):
    if isinstance(numba_type, ArrayItemArrayType):
        hdp__xgo = pa.field('element', _numba_to_pyarrow_type(numba_type.
            dtype, is_iceberg)[0])
        usyw__vbv = pa.list_(hdp__xgo)
    elif isinstance(numba_type, StructArrayType):
        cxot__nmr = []
        for fbqo__jtbqq, nfx__hscu in zip(numba_type.names, numba_type.data):
            nsz__bcait, vdfko__uma = _numba_to_pyarrow_type(nfx__hscu,
                is_iceberg)
            cxot__nmr.append(pa.field(fbqo__jtbqq, nsz__bcait, True))
        usyw__vbv = pa.struct(cxot__nmr)
    elif isinstance(numba_type, DecimalArrayType):
        usyw__vbv = pa.decimal128(numba_type.precision, numba_type.scale)
    elif isinstance(numba_type, CategoricalArrayType):
        fzk__idr: PDCategoricalDtype = numba_type.dtype
        usyw__vbv = pa.dictionary(_numba_to_pyarrow_type(fzk__idr.int_type,
            is_iceberg)[0], _numba_to_pyarrow_type(fzk__idr.elem_type,
            is_iceberg)[0], ordered=False if fzk__idr.ordered is None else
            fzk__idr.ordered)
    elif numba_type == boolean_array:
        usyw__vbv = pa.bool_()
    elif numba_type in (string_array_type, bodo.dict_str_arr_type):
        usyw__vbv = pa.string()
    elif numba_type == binary_array_type:
        usyw__vbv = pa.binary()
    elif numba_type == datetime_date_array_type:
        usyw__vbv = pa.date32()
    elif isinstance(numba_type, bodo.DatetimeArrayType) or isinstance(
        numba_type, types.Array) and numba_type.dtype == bodo.datetime64ns:
        usyw__vbv = pa.timestamp('us', 'UTC') if is_iceberg else pa.timestamp(
            'ns', 'UTC')
    elif isinstance(numba_type, types.Array
        ) and numba_type.dtype == bodo.timedelta64ns:
        usyw__vbv = pa.duration('ns')
    elif isinstance(numba_type, (types.Array, IntegerArrayType,
        FloatingArrayType)) and numba_type.dtype in _numba_pyarrow_type_map:
        usyw__vbv = _numba_pyarrow_type_map[numba_type.dtype]
    elif isinstance(numba_type, bodo.TimeArrayType):
        if numba_type.precision == 0:
            usyw__vbv = pa.time32('s')
        elif numba_type.precision == 3:
            usyw__vbv = pa.time32('ms')
        elif numba_type.precision == 6:
            usyw__vbv = pa.time64('us')
        elif numba_type.precision == 9:
            usyw__vbv = pa.time64('ns')
    else:
        raise BodoError(
            f'Conversion from Bodo array type {numba_type} to PyArrow type not supported yet'
            )
    return usyw__vbv, is_nullable_arrow_out(numba_type)


def numba_to_pyarrow_schema(df: DataFrameType, is_iceberg: bool=False
    ) ->pa.Schema:
    cxot__nmr = []
    for fbqo__jtbqq, jlx__hlsxe in zip(df.columns, df.data):
        try:
            hbu__tyjyg, glwu__zdda = _numba_to_pyarrow_type(jlx__hlsxe,
                is_iceberg)
        except BodoError as fjnfe__kquzg:
            raise_bodo_error(fjnfe__kquzg.msg, fjnfe__kquzg.loc)
        cxot__nmr.append(pa.field(fbqo__jtbqq, hbu__tyjyg, glwu__zdda))
    return pa.schema(cxot__nmr)


def update_env_vars(env_vars):
    oxyd__kik = {}
    for rqew__rawss, sgtc__mchtg in env_vars.items():
        if rqew__rawss in os.environ:
            oxyd__kik[rqew__rawss] = os.environ[rqew__rawss]
        else:
            oxyd__kik[rqew__rawss] = '__none__'
        if sgtc__mchtg == '__none__':
            del os.environ[rqew__rawss]
        else:
            os.environ[rqew__rawss] = sgtc__mchtg
    return oxyd__kik


def update_file_contents(fname: str, contents: str, is_parallel=True) ->str:
    ozji__zxr = MPI.COMM_WORLD
    owvc__uxtq = None
    if not is_parallel or ozji__zxr.Get_rank() == 0:
        if os.path.exists(fname):
            with open(fname, 'r') as rkl__cxq:
                owvc__uxtq = rkl__cxq.read()
    if is_parallel:
        owvc__uxtq = ozji__zxr.bcast(owvc__uxtq)
    if owvc__uxtq is None:
        owvc__uxtq = '__none__'
    rbn__pxvi = bodo.get_rank() in bodo.get_nodes_first_ranks(
        ) if is_parallel else True
    if contents == '__none__':
        if rbn__pxvi and os.path.exists(fname):
            os.remove(fname)
    elif rbn__pxvi:
        with open(fname, 'w') as rkl__cxq:
            rkl__cxq.write(contents)
    if is_parallel:
        ozji__zxr.Barrier()
    return owvc__uxtq


@numba.njit
def uuid4_helper():
    with numba.objmode(out='unicode_type'):
        out = str(uuid.uuid4())
    return out


class ExceptionPropagatingThread(threading.Thread):

    def run(self):
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as fjnfe__kquzg:
            self.exc = fjnfe__kquzg

    def join(self, timeout=None):
        super().join(timeout)
        if self.exc:
            raise self.exc
        return self.ret


class ExceptionPropagatingThreadType(types.Opaque):

    def __init__(self):
        super(ExceptionPropagatingThreadType, self).__init__(name=
            'ExceptionPropagatingThreadType')


exception_propagating_thread_type = ExceptionPropagatingThreadType()
types.exception_propagating_thread_type = exception_propagating_thread_type
register_model(ExceptionPropagatingThreadType)(models.OpaqueModel)


@unbox(ExceptionPropagatingThreadType)
def unbox_exception_propagating_thread_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(ExceptionPropagatingThreadType)
def box_exception_propagating_thread_type(typ, val, c):
    c.pyapi.incref(val)
    return val


@typeof_impl.register(ExceptionPropagatingThread)
def typeof_exception_propagating_thread(val, c):
    return exception_propagating_thread_type


def join_all_threads(thread_list):
    cmg__gdpq = tracing.Event('join_all_threads', is_parallel=True)
    ozji__zxr = MPI.COMM_WORLD
    eqgbm__rqae = None
    try:
        for dmawf__naqki in thread_list:
            if isinstance(dmawf__naqki, threading.Thread):
                dmawf__naqki.join()
    except Exception as fjnfe__kquzg:
        eqgbm__rqae = fjnfe__kquzg
    ccz__tcndq = int(eqgbm__rqae is not None)
    gptlk__klw, jri__gcjid = ozji__zxr.allreduce((ccz__tcndq, ozji__zxr.
        Get_rank()), op=MPI.MAXLOC)
    if gptlk__klw:
        if ozji__zxr.Get_rank() == jri__gcjid:
            rvin__nxfj = eqgbm__rqae
        else:
            rvin__nxfj = None
        rvin__nxfj = ozji__zxr.bcast(rvin__nxfj, root=jri__gcjid)
        if ccz__tcndq:
            raise eqgbm__rqae
        else:
            raise rvin__nxfj
    cmg__gdpq.finalize()
