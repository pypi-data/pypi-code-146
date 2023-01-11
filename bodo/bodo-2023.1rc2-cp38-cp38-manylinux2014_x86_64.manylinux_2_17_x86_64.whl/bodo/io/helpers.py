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
    bhmpj__jzyq = context.get_python_api(builder)
    return bhmpj__jzyq.unserialize(bhmpj__jzyq.serialize_object(pyval))


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
    bnwbs__kwt = ['ns', 'us', 'ms', 's']
    if pa_ts_typ.unit not in bnwbs__kwt:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        sadv__cote = pa_ts_typ.to_pandas_dtype().tz
        rsn__pypv = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(sadv__cote
            )
        return bodo.DatetimeArrayType(rsn__pypv), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ: pa.Field, is_index,
    nullable_from_metadata, category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        idqny__izv, mza__ejws = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(idqny__izv), mza__ejws
    if isinstance(pa_typ.type, pa.StructType):
        lzx__zngda = []
        pmh__osjgw = []
        mza__ejws = True
        for usv__pxg in pa_typ.flatten():
            pmh__osjgw.append(usv__pxg.name.split('.')[-1])
            uimy__wvxgz, kwkll__zre = _get_numba_typ_from_pa_typ(usv__pxg,
                is_index, nullable_from_metadata, category_info)
            lzx__zngda.append(uimy__wvxgz)
            mza__ejws = mza__ejws and kwkll__zre
        return StructArrayType(tuple(lzx__zngda), tuple(pmh__osjgw)), mza__ejws
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
        pnxjt__dmvi = _pyarrow_numba_type_map[pa_typ.type.index_type]
        vxlr__dvv = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=pnxjt__dmvi)
        return CategoricalArrayType(vxlr__dvv), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pyarrow_numba_type_map:
        biqt__cfyqk = _pyarrow_numba_type_map[pa_typ.type]
        mza__ejws = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if biqt__cfyqk == datetime_date_type:
        return datetime_date_array_type, mza__ejws
    if isinstance(biqt__cfyqk, TimeType):
        return TimeArrayType(biqt__cfyqk.precision), mza__ejws
    if biqt__cfyqk == bytes_type:
        return binary_array_type, mza__ejws
    idqny__izv = (string_array_type if biqt__cfyqk == string_type else
        types.Array(biqt__cfyqk, 1, 'C'))
    if biqt__cfyqk == types.bool_:
        idqny__izv = boolean_array
    vry__hkmak = (use_nullable_pd_arr if nullable_from_metadata is None else
        nullable_from_metadata)
    if vry__hkmak and not is_index and isinstance(biqt__cfyqk, types.Integer
        ) and pa_typ.nullable:
        idqny__izv = IntegerArrayType(biqt__cfyqk)
    if (vry__hkmak and bodo.libs.float_arr_ext._use_nullable_float and not
        is_index and isinstance(biqt__cfyqk, types.Float) and pa_typ.nullable):
        idqny__izv = FloatingArrayType(biqt__cfyqk)
    return idqny__izv, mza__ejws


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
        whmxf__oomb = pa.field('element', _numba_to_pyarrow_type(numba_type
            .dtype, is_iceberg)[0])
        biqt__cfyqk = pa.list_(whmxf__oomb)
    elif isinstance(numba_type, StructArrayType):
        ocfds__hfao = []
        for kde__ohtqd, jrjq__xlqsl in zip(numba_type.names, numba_type.data):
            xol__imbgh, fzqsg__zrws = _numba_to_pyarrow_type(jrjq__xlqsl,
                is_iceberg)
            ocfds__hfao.append(pa.field(kde__ohtqd, xol__imbgh, True))
        biqt__cfyqk = pa.struct(ocfds__hfao)
    elif isinstance(numba_type, DecimalArrayType):
        biqt__cfyqk = pa.decimal128(numba_type.precision, numba_type.scale)
    elif isinstance(numba_type, CategoricalArrayType):
        vxlr__dvv: PDCategoricalDtype = numba_type.dtype
        biqt__cfyqk = pa.dictionary(_numba_to_pyarrow_type(vxlr__dvv.
            int_type, is_iceberg)[0], _numba_to_pyarrow_type(vxlr__dvv.
            elem_type, is_iceberg)[0], ordered=False if vxlr__dvv.ordered is
            None else vxlr__dvv.ordered)
    elif numba_type == boolean_array:
        biqt__cfyqk = pa.bool_()
    elif numba_type in (string_array_type, bodo.dict_str_arr_type):
        biqt__cfyqk = pa.string()
    elif numba_type == binary_array_type:
        biqt__cfyqk = pa.binary()
    elif numba_type == datetime_date_array_type:
        biqt__cfyqk = pa.date32()
    elif isinstance(numba_type, bodo.DatetimeArrayType) or isinstance(
        numba_type, types.Array) and numba_type.dtype == bodo.datetime64ns:
        biqt__cfyqk = pa.timestamp('us', 'UTC'
            ) if is_iceberg else pa.timestamp('ns', 'UTC')
    elif isinstance(numba_type, types.Array
        ) and numba_type.dtype == bodo.timedelta64ns:
        biqt__cfyqk = pa.duration('ns')
    elif isinstance(numba_type, (types.Array, IntegerArrayType,
        FloatingArrayType)) and numba_type.dtype in _numba_pyarrow_type_map:
        biqt__cfyqk = _numba_pyarrow_type_map[numba_type.dtype]
    elif isinstance(numba_type, bodo.TimeArrayType):
        if numba_type.precision == 0:
            biqt__cfyqk = pa.time32('s')
        elif numba_type.precision == 3:
            biqt__cfyqk = pa.time32('ms')
        elif numba_type.precision == 6:
            biqt__cfyqk = pa.time64('us')
        elif numba_type.precision == 9:
            biqt__cfyqk = pa.time64('ns')
    else:
        raise BodoError(
            f'Conversion from Bodo array type {numba_type} to PyArrow type not supported yet'
            )
    return biqt__cfyqk, is_nullable_arrow_out(numba_type)


def numba_to_pyarrow_schema(df: DataFrameType, is_iceberg: bool=False
    ) ->pa.Schema:
    ocfds__hfao = []
    for kde__ohtqd, bnnye__iiheh in zip(df.columns, df.data):
        try:
            cqxe__ybku, llqyt__ytav = _numba_to_pyarrow_type(bnnye__iiheh,
                is_iceberg)
        except BodoError as osn__ovkrl:
            raise_bodo_error(osn__ovkrl.msg, osn__ovkrl.loc)
        ocfds__hfao.append(pa.field(kde__ohtqd, cqxe__ybku, llqyt__ytav))
    return pa.schema(ocfds__hfao)


def update_env_vars(env_vars):
    nlgau__qjle = {}
    for ekiy__cqagl, arngh__ayzu in env_vars.items():
        if ekiy__cqagl in os.environ:
            nlgau__qjle[ekiy__cqagl] = os.environ[ekiy__cqagl]
        else:
            nlgau__qjle[ekiy__cqagl] = '__none__'
        if arngh__ayzu == '__none__':
            del os.environ[ekiy__cqagl]
        else:
            os.environ[ekiy__cqagl] = arngh__ayzu
    return nlgau__qjle


def update_file_contents(fname: str, contents: str, is_parallel=True) ->str:
    xrlw__smyon = MPI.COMM_WORLD
    hyyrn__jaabm = None
    if not is_parallel or xrlw__smyon.Get_rank() == 0:
        if os.path.exists(fname):
            with open(fname, 'r') as yetcj__sad:
                hyyrn__jaabm = yetcj__sad.read()
    if is_parallel:
        hyyrn__jaabm = xrlw__smyon.bcast(hyyrn__jaabm)
    if hyyrn__jaabm is None:
        hyyrn__jaabm = '__none__'
    xeod__pqqka = bodo.get_rank() in bodo.get_nodes_first_ranks(
        ) if is_parallel else True
    if contents == '__none__':
        if xeod__pqqka and os.path.exists(fname):
            os.remove(fname)
    elif xeod__pqqka:
        with open(fname, 'w') as yetcj__sad:
            yetcj__sad.write(contents)
    if is_parallel:
        xrlw__smyon.Barrier()
    return hyyrn__jaabm


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
        except BaseException as osn__ovkrl:
            self.exc = osn__ovkrl

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
    vhsun__juop = tracing.Event('join_all_threads', is_parallel=True)
    xrlw__smyon = MPI.COMM_WORLD
    iig__pnhom = None
    try:
        for xjf__cymkm in thread_list:
            if isinstance(xjf__cymkm, threading.Thread):
                xjf__cymkm.join()
    except Exception as osn__ovkrl:
        iig__pnhom = osn__ovkrl
    cumqa__kyosg = int(iig__pnhom is not None)
    eqx__igwmd, bei__ilu = xrlw__smyon.allreduce((cumqa__kyosg, xrlw__smyon
        .Get_rank()), op=MPI.MAXLOC)
    if eqx__igwmd:
        if xrlw__smyon.Get_rank() == bei__ilu:
            ggpdz__vffe = iig__pnhom
        else:
            ggpdz__vffe = None
        ggpdz__vffe = xrlw__smyon.bcast(ggpdz__vffe, root=bei__ilu)
        if cumqa__kyosg:
            raise iig__pnhom
        else:
            raise ggpdz__vffe
    vhsun__juop.finalize()
