import datetime
import operator
import warnings
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_new_ref, lower_constant
from numba.core.typing.templates import AttributeTemplate, signature
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
import bodo.hiframes
import bodo.utils.conversion
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_tz_naive_type
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.transform import get_const_func_output_type
from bodo.utils.typing import BodoError, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_overload_const_func, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_tuple, get_udf_error_msg, get_udf_out_arr_type, get_val_type_maybe_str_literal, is_const_func_type, is_heterogeneous_tuple_type, is_iterable_type, is_overload_bool, is_overload_constant_int, is_overload_constant_list, is_overload_constant_nan, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_none, is_overload_true, is_str_arr_type, parse_dtype, raise_bodo_error
from bodo.utils.utils import is_null_value
_dt_index_data_typ = types.Array(types.NPDatetime('ns'), 1, 'C')
_timedelta_index_data_typ = types.Array(types.NPTimedelta('ns'), 1, 'C')
iNaT = pd._libs.tslibs.iNaT
NaT = types.NPDatetime('ns')('NaT')
idx_cpy_arg_defaults = dict(deep=False, dtype=None, names=None)
idx_typ_to_format_str_map = dict()


@typeof_impl.register(pd.Index)
def typeof_pd_index(val, c):
    if val.inferred_type == 'string' or pd._libs.lib.infer_dtype(val, True
        ) == 'string':
        return StringIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'bytes' or pd._libs.lib.infer_dtype(val, True
        ) == 'bytes':
        return BinaryIndexType(get_val_type_maybe_str_literal(val.name))
    if val.equals(pd.Index([])):
        return StringIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'date':
        return DatetimeIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'integer' or pd._libs.lib.infer_dtype(val, True
        ) == 'integer':
        if isinstance(val.dtype, pd.core.arrays.integer._IntegerDtype):
            idks__onu = val.dtype.numpy_dtype
            dtype = numba.np.numpy_support.from_dtype(idks__onu)
        else:
            dtype = types.int64
        return NumericIndexType(dtype, get_val_type_maybe_str_literal(val.
            name), IntegerArrayType(dtype))
    if val.inferred_type == 'floating' or pd._libs.lib.infer_dtype(val, True
        ) == 'floating':
        if isinstance(val.dtype, (pd.Float32Dtype, pd.Float64Dtype)):
            idks__onu = val.dtype.numpy_dtype
            dtype = numba.np.numpy_support.from_dtype(idks__onu)
        else:
            dtype = types.float64
        return NumericIndexType(dtype, get_val_type_maybe_str_literal(val.
            name), FloatingArrayType(dtype))
    if val.inferred_type == 'boolean' or pd._libs.lib.infer_dtype(val, True
        ) == 'boolean':
        return NumericIndexType(types.bool_, get_val_type_maybe_str_literal
            (val.name), boolean_array)
    raise NotImplementedError(f'unsupported pd.Index type {val}')


class DatetimeIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = types.Array(bodo.datetime64ns, 1, 'C'
            ) if data is None else data
        super(DatetimeIndexType, self).__init__(name=
            f'DatetimeIndex({name_typ}, {self.data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return self.data.dtype

    @property
    def tzval(self):
        return self.data.tz if isinstance(self.data, bodo.DatetimeArrayType
            ) else None

    def copy(self):
        return DatetimeIndexType(self.name_typ, self.data)

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self, bodo.hiframes.
            pd_timestamp_ext.PandasTimestampType(self.tzval))

    @property
    def pandas_type_name(self):
        return self.data.dtype.type_name

    @property
    def numpy_type_name(self):
        return str(self.data.dtype)


types.datetime_index = DatetimeIndexType()


@typeof_impl.register(pd.DatetimeIndex)
def typeof_datetime_index(val, c):
    if isinstance(val.dtype, pd.DatetimeTZDtype):
        return DatetimeIndexType(get_val_type_maybe_str_literal(val.name),
            DatetimeArrayType(val.tz))
    return DatetimeIndexType(get_val_type_maybe_str_literal(val.name))


@register_model(DatetimeIndexType)
class DatetimeIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ofgt__msmd = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(_dt_index_data_typ.dtype, types.int64))]
        super(DatetimeIndexModel, self).__init__(dmm, fe_type, ofgt__msmd)


make_attribute_wrapper(DatetimeIndexType, 'data', '_data')
make_attribute_wrapper(DatetimeIndexType, 'name', '_name')
make_attribute_wrapper(DatetimeIndexType, 'dict', '_dict')


@overload_method(DatetimeIndexType, 'copy', no_unliteral=True)
def overload_datetime_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    amisc__pgijx = dict(deep=deep, dtype=dtype, names=names)
    yng__jtz = idx_typ_to_format_str_map[DatetimeIndexType].format('copy()')
    check_unsupported_args('copy', amisc__pgijx, idx_cpy_arg_defaults,
        fn_str=yng__jtz, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_datetime_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_datetime_index(A._data.
                copy(), A._name)
    return impl


@box(DatetimeIndexType)
def box_dt_index(typ, val, c):
    nrttr__ydfyo = c.context.insert_const_string(c.builder.module, 'pandas')
    bxko__fdp = c.pyapi.import_module_noblock(nrttr__ydfyo)
    tgdcg__byj = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, tgdcg__byj.data)
    bpe__skerx = c.pyapi.from_native_value(typ.data, tgdcg__byj.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, tgdcg__byj.name)
    qwh__ohiqx = c.pyapi.from_native_value(typ.name_typ, tgdcg__byj.name, c
        .env_manager)
    args = c.pyapi.tuple_pack([bpe__skerx])
    mhkn__mxcd = c.pyapi.object_getattr_string(bxko__fdp, 'DatetimeIndex')
    kws = c.pyapi.dict_pack([('name', qwh__ohiqx)])
    ilsy__vsjmx = c.pyapi.call(mhkn__mxcd, args, kws)
    c.pyapi.decref(bpe__skerx)
    c.pyapi.decref(qwh__ohiqx)
    c.pyapi.decref(bxko__fdp)
    c.pyapi.decref(mhkn__mxcd)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ilsy__vsjmx


@unbox(DatetimeIndexType)
def unbox_datetime_index(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        bpaja__qmng = c.pyapi.object_getattr_string(val, 'array')
    else:
        bpaja__qmng = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, bpaja__qmng).value
    qwh__ohiqx = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, qwh__ohiqx).value
    qizmc__fib = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qizmc__fib.data = data
    qizmc__fib.name = name
    dtype = _dt_index_data_typ.dtype
    fzh__hfgz, fesi__rmrcv = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    qizmc__fib.dict = fesi__rmrcv
    c.pyapi.decref(bpaja__qmng)
    c.pyapi.decref(qwh__ohiqx)
    return NativeValue(qizmc__fib._getvalue())


@intrinsic
def init_datetime_index(typingctx, data, name):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        dfyr__fknq, lvbap__ndlqk = args
        tgdcg__byj = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        tgdcg__byj.data = dfyr__fknq
        tgdcg__byj.name = lvbap__ndlqk
        context.nrt.incref(builder, signature.args[0], dfyr__fknq)
        context.nrt.incref(builder, signature.args[1], lvbap__ndlqk)
        dtype = _dt_index_data_typ.dtype
        tgdcg__byj.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return tgdcg__byj._getvalue()
    ahu__fnuh = DatetimeIndexType(name, data)
    sig = signature(ahu__fnuh, data, name)
    return sig, codegen


def init_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) >= 1 and not kws
    yky__icyoj = args[0]
    if equiv_set.has_shape(yky__icyoj):
        return ArrayAnalysis.AnalyzeResult(shape=yky__icyoj, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_datetime_index
    ) = init_index_equiv


def gen_dti_field_impl(field):
    abd__wuyu = 'def impl(dti):\n'
    abd__wuyu += '    numba.parfors.parfor.init_prange()\n'
    abd__wuyu += '    A = bodo.hiframes.pd_index_ext.get_index_data(dti)\n'
    abd__wuyu += '    name = bodo.hiframes.pd_index_ext.get_index_name(dti)\n'
    abd__wuyu += '    n = len(A)\n'
    abd__wuyu += '    S = np.empty(n, np.int64)\n'
    abd__wuyu += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    abd__wuyu += '        val = A[i]\n'
    abd__wuyu += '        ts = bodo.utils.conversion.box_if_dt64(val)\n'
    if field in ['weekday']:
        abd__wuyu += '        S[i] = ts.' + field + '()\n'
    else:
        abd__wuyu += '        S[i] = ts.' + field + '\n'
    abd__wuyu += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    aha__iwa = {}
    exec(abd__wuyu, {'numba': numba, 'np': np, 'bodo': bodo}, aha__iwa)
    impl = aha__iwa['impl']
    return impl


def _install_dti_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        if field in ['is_leap_year']:
            continue
        impl = gen_dti_field_impl(field)
        overload_attribute(DatetimeIndexType, field)(lambda dti: impl)


_install_dti_date_fields()


@overload_attribute(DatetimeIndexType, 'is_leap_year')
def overload_datetime_index_is_leap_year(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        svaxh__xlacb = len(A)
        S = np.empty(svaxh__xlacb, np.bool_)
        for i in numba.parfors.parfor.internal_prange(svaxh__xlacb):
            val = A[i]
            tmvg__grxi = bodo.utils.conversion.box_if_dt64(val)
            S[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(tmvg__grxi.year)
        return S
    return impl


@overload_attribute(DatetimeIndexType, 'date')
def overload_datetime_index_date(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        svaxh__xlacb = len(A)
        S = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            svaxh__xlacb)
        for i in numba.parfors.parfor.internal_prange(svaxh__xlacb):
            val = A[i]
            tmvg__grxi = bodo.utils.conversion.box_if_dt64(val)
            S[i] = datetime.date(tmvg__grxi.year, tmvg__grxi.month,
                tmvg__grxi.day)
        return S
    return impl


@numba.njit(no_cpython_wrapper=True)
def _dti_val_finalize(s, count):
    if not count:
        s = iNaT
    return bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(s)


@numba.njit(no_cpython_wrapper=True)
def _tdi_val_finalize(s, count):
    return pd.Timedelta('nan') if not count else pd.Timedelta(s)


@overload_method(DatetimeIndexType, 'min', no_unliteral=True)
def overload_datetime_index_min(dti, axis=None, skipna=True):
    tsp__ume = dict(axis=axis, skipna=skipna)
    ugzcb__bvng = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.min', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.min()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        nepuj__nod = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_max_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(nepuj__nod)):
            if not bodo.libs.array_kernels.isna(nepuj__nod, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(nepuj__nod
                    [i])
                s = min(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@overload_method(DatetimeIndexType, 'max', no_unliteral=True)
def overload_datetime_index_max(dti, axis=None, skipna=True):
    tsp__ume = dict(axis=axis, skipna=skipna)
    ugzcb__bvng = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.max', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.max()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        nepuj__nod = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(nepuj__nod)):
            if not bodo.libs.array_kernels.isna(nepuj__nod, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(nepuj__nod
                    [i])
                s = max(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@overload_method(DatetimeIndexType, 'tz_convert', no_unliteral=True)
def overload_pd_datetime_tz_convert(A, tz):

    def impl(A, tz):
        return init_datetime_index(A._data.tz_convert(tz), A._name)
    return impl


@infer_getattr
class DatetimeIndexAttribute(AttributeTemplate):
    key = DatetimeIndexType

    def resolve_values(self, ary):
        return _dt_index_data_typ


@overload(pd.DatetimeIndex, no_unliteral=True)
def pd_datetimeindex_overload(data=None, freq=None, tz=None, normalize=
    False, closed=None, ambiguous='raise', dayfirst=False, yearfirst=False,
    dtype=None, copy=False, name=None):
    if is_overload_none(data):
        raise BodoError('data argument in pd.DatetimeIndex() expected')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'pandas.DatetimeIndex()')
    tsp__ume = dict(freq=freq, tz=tz, normalize=normalize, closed=closed,
        ambiguous=ambiguous, dayfirst=dayfirst, yearfirst=yearfirst, dtype=
        dtype, copy=copy)
    ugzcb__bvng = dict(freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False)
    check_unsupported_args('pandas.DatetimeIndex', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')

    def f(data=None, freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False, name=None):
        neaf__lkhcn = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_dt64ns(neaf__lkhcn)
        return bodo.hiframes.pd_index_ext.init_datetime_index(S, name)
    return f


def overload_sub_operator_datetime_index(lhs, rhs):
    if isinstance(lhs, DatetimeIndexType
        ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
        kyoy__exwbe = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            nepuj__nod = bodo.hiframes.pd_index_ext.get_index_data(lhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(lhs)
            svaxh__xlacb = len(nepuj__nod)
            S = np.empty(svaxh__xlacb, kyoy__exwbe)
            vld__drod = rhs.value
            for i in numba.parfors.parfor.internal_prange(svaxh__xlacb):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    nepuj__nod[i]) - vld__drod)
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl
    if isinstance(rhs, DatetimeIndexType
        ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
        kyoy__exwbe = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            nepuj__nod = bodo.hiframes.pd_index_ext.get_index_data(rhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(rhs)
            svaxh__xlacb = len(nepuj__nod)
            S = np.empty(svaxh__xlacb, kyoy__exwbe)
            vld__drod = lhs.value
            for i in numba.parfors.parfor.internal_prange(svaxh__xlacb):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    vld__drod - bodo.hiframes.pd_timestamp_ext.
                    dt64_to_integer(nepuj__nod[i]))
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl


def gen_dti_str_binop_impl(op, is_lhs_dti):
    pep__cqcav = numba.core.utils.OPERATORS_TO_BUILTINS[op]
    abd__wuyu = 'def impl(lhs, rhs):\n'
    if is_lhs_dti:
        abd__wuyu += '  dt_index, _str = lhs, rhs\n'
        ham__arp = 'arr[i] {} other'.format(pep__cqcav)
    else:
        abd__wuyu += '  dt_index, _str = rhs, lhs\n'
        ham__arp = 'other {} arr[i]'.format(pep__cqcav)
    abd__wuyu += (
        '  arr = bodo.hiframes.pd_index_ext.get_index_data(dt_index)\n')
    abd__wuyu += '  l = len(arr)\n'
    abd__wuyu += (
        '  other = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(_str)\n')
    abd__wuyu += '  S = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    abd__wuyu += '  for i in numba.parfors.parfor.internal_prange(l):\n'
    abd__wuyu += '    S[i] = {}\n'.format(ham__arp)
    abd__wuyu += '  return S\n'
    aha__iwa = {}
    exec(abd__wuyu, {'bodo': bodo, 'numba': numba, 'np': np}, aha__iwa)
    impl = aha__iwa['impl']
    return impl


def overload_binop_dti_str(op):

    def overload_impl(lhs, rhs):
        if isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
            ) == string_type:
            return gen_dti_str_binop_impl(op, True)
        if isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
            ) == string_type:
            return gen_dti_str_binop_impl(op, False)
    return overload_impl


@overload(pd.Index, inline='always', no_unliteral=True)
def pd_index_overload(data=None, dtype=None, copy=False, name=None,
    tupleize_cols=True):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'pandas.Index()')
    data = types.unliteral(data) if not isinstance(data, types.LiteralList
        ) else data
    if not is_overload_none(dtype):
        qbdpi__ksikg = parse_dtype(dtype, 'pandas.Index')
        bmto__jnro = False
    else:
        qbdpi__ksikg = getattr(data, 'dtype', None)
        bmto__jnro = True
    if isinstance(qbdpi__ksikg, types.misc.PyObject):
        raise BodoError(
            "pd.Index() object 'dtype' is not specific enough for typing. Please provide a more exact type (e.g. str)."
            )
    if isinstance(data, RangeIndexType):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.RangeIndex(data, name=name)
    elif isinstance(data, DatetimeIndexType
        ) or qbdpi__ksikg == types.NPDatetime('ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.DatetimeIndex(data, name=name)
    elif isinstance(data, TimedeltaIndexType
        ) or qbdpi__ksikg == types.NPTimedelta('ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.TimedeltaIndex(data, name=name)
    elif is_heterogeneous_tuple_type(data):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return bodo.hiframes.pd_index_ext.init_heter_index(data, name)
        return impl
    elif bodo.utils.utils.is_array_typ(data, False) or isinstance(data, (
        SeriesType, types.List, types.UniTuple)):
        if isinstance(qbdpi__ksikg, (types.Integer, types.Float, types.Boolean)
            ):
            if bmto__jnro:

                def impl(data=None, dtype=None, copy=False, name=None,
                    tupleize_cols=True):
                    neaf__lkhcn = bodo.utils.conversion.coerce_to_array(data)
                    return bodo.hiframes.pd_index_ext.init_numeric_index(
                        neaf__lkhcn, name)
            else:

                def impl(data=None, dtype=None, copy=False, name=None,
                    tupleize_cols=True):
                    neaf__lkhcn = bodo.utils.conversion.coerce_to_array(data)
                    qkwmf__vjud = bodo.utils.conversion.fix_arr_dtype(
                        neaf__lkhcn, qbdpi__ksikg)
                    return bodo.hiframes.pd_index_ext.init_numeric_index(
                        qkwmf__vjud, name)
        elif qbdpi__ksikg in [types.string, bytes_type]:

            def impl(data=None, dtype=None, copy=False, name=None,
                tupleize_cols=True):
                return bodo.hiframes.pd_index_ext.init_binary_str_index(bodo
                    .utils.conversion.coerce_to_array(data), name)
        else:
            raise BodoError(
                'pd.Index(): provided array is of unsupported type.')
    elif is_overload_none(data):
        raise BodoError(
            'data argument in pd.Index() is invalid: None or scalar is not acceptable'
            )
    else:
        raise BodoError(
            f'pd.Index(): the provided argument type {data} is not supported')
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_datetime_index_getitem(dti, ind):
    if isinstance(dti, DatetimeIndexType):
        if isinstance(ind, types.Integer):

            def impl(dti, ind):
                yxw__mgfo = bodo.hiframes.pd_index_ext.get_index_data(dti)
                val = yxw__mgfo[ind]
                return bodo.utils.conversion.box_if_dt64(val)
            return impl
        else:

            def impl(dti, ind):
                yxw__mgfo = bodo.hiframes.pd_index_ext.get_index_data(dti)
                name = bodo.hiframes.pd_index_ext.get_index_name(dti)
                xpzvq__lhjp = yxw__mgfo[ind]
                return bodo.hiframes.pd_index_ext.init_datetime_index(
                    xpzvq__lhjp, name)
            return impl


@overload(operator.getitem, no_unliteral=True)
def overload_timedelta_index_getitem(I, ind):
    if not isinstance(I, TimedeltaIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            cmxk__ewh = bodo.hiframes.pd_index_ext.get_index_data(I)
            return pd.Timedelta(cmxk__ewh[ind])
        return impl

    def impl(I, ind):
        cmxk__ewh = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        xpzvq__lhjp = cmxk__ewh[ind]
        return bodo.hiframes.pd_index_ext.init_timedelta_index(xpzvq__lhjp,
            name)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_categorical_index_getitem(I, ind):
    if not isinstance(I, CategoricalIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            tshko__alzu = bodo.hiframes.pd_index_ext.get_index_data(I)
            val = tshko__alzu[ind]
            return val
        return impl
    if isinstance(ind, types.SliceType):

        def impl(I, ind):
            tshko__alzu = bodo.hiframes.pd_index_ext.get_index_data(I)
            name = bodo.hiframes.pd_index_ext.get_index_name(I)
            xpzvq__lhjp = tshko__alzu[ind]
            return bodo.hiframes.pd_index_ext.init_categorical_index(
                xpzvq__lhjp, name)
        return impl
    raise BodoError(
        f'pd.CategoricalIndex.__getitem__: unsupported index type {ind}')


@numba.njit(no_cpython_wrapper=True)
def validate_endpoints(closed):
    hjzsw__jif = False
    jikdl__gxd = False
    if closed is None:
        hjzsw__jif = True
        jikdl__gxd = True
    elif closed == 'left':
        hjzsw__jif = True
    elif closed == 'right':
        jikdl__gxd = True
    else:
        raise ValueError("Closed has to be either 'left', 'right' or None")
    return hjzsw__jif, jikdl__gxd


@numba.njit(no_cpython_wrapper=True)
def to_offset_value(freq):
    if freq is None:
        return None
    with numba.objmode(r='int64'):
        r = pd.tseries.frequencies.to_offset(freq).nanos
    return r


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _dummy_convert_none_to_int(val):
    if is_overload_none(val):

        def impl(val):
            return 0
        return impl
    if isinstance(val, types.Optional):

        def impl(val):
            if val is None:
                return 0
            return bodo.utils.indexing.unoptional(val)
        return impl
    return lambda val: val


@overload(pd.date_range, inline='always')
def pd_date_range_overload(start=None, end=None, periods=None, freq=None,
    tz=None, normalize=False, name=None, closed=None):
    tsp__ume = dict(tz=tz, normalize=normalize, closed=closed)
    ugzcb__bvng = dict(tz=None, normalize=False, closed=None)
    check_unsupported_args('pandas.date_range', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='General')
    if not is_overload_none(tz):
        raise_bodo_error('pd.date_range(): tz argument not supported yet')
    djdh__igayo = ''
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
        djdh__igayo = "  freq = 'D'\n"
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise_bodo_error(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )
    abd__wuyu = """def f(start=None, end=None, periods=None, freq=None, tz=None, normalize=False, name=None, closed=None):
"""
    abd__wuyu += djdh__igayo
    if is_overload_none(start):
        abd__wuyu += "  start_t = pd.Timestamp('1800-01-03')\n"
    else:
        abd__wuyu += '  start_t = pd.Timestamp(start)\n'
    if is_overload_none(end):
        abd__wuyu += "  end_t = pd.Timestamp('1800-01-03')\n"
    else:
        abd__wuyu += '  end_t = pd.Timestamp(end)\n'
    if not is_overload_none(freq):
        abd__wuyu += (
            '  stride = bodo.hiframes.pd_index_ext.to_offset_value(freq)\n')
        if is_overload_none(periods):
            abd__wuyu += '  b = start_t.value\n'
            abd__wuyu += (
                '  e = b + (end_t.value - b) // stride * stride + stride // 2 + 1\n'
                )
        elif not is_overload_none(start):
            abd__wuyu += '  b = start_t.value\n'
            abd__wuyu += '  addend = np.int64(periods) * np.int64(stride)\n'
            abd__wuyu += '  e = np.int64(b) + addend\n'
        elif not is_overload_none(end):
            abd__wuyu += '  e = end_t.value + stride\n'
            abd__wuyu += '  addend = np.int64(periods) * np.int64(-stride)\n'
            abd__wuyu += '  b = np.int64(e) + addend\n'
        else:
            raise_bodo_error(
                "at least 'start' or 'end' should be specified if a 'period' is given."
                )
        abd__wuyu += '  arr = np.arange(b, e, stride, np.int64)\n'
    else:
        abd__wuyu += '  delta = end_t.value - start_t.value\n'
        abd__wuyu += '  step = delta / (periods - 1)\n'
        abd__wuyu += '  arr1 = np.arange(0, periods, 1, np.float64)\n'
        abd__wuyu += '  arr1 *= step\n'
        abd__wuyu += '  arr1 += start_t.value\n'
        abd__wuyu += '  arr = arr1.astype(np.int64)\n'
        abd__wuyu += '  arr[-1] = end_t.value\n'
    abd__wuyu += '  A = bodo.utils.conversion.convert_to_dt64ns(arr)\n'
    abd__wuyu += (
        '  return bodo.hiframes.pd_index_ext.init_datetime_index(A, name)\n')
    aha__iwa = {}
    exec(abd__wuyu, {'bodo': bodo, 'np': np, 'pd': pd}, aha__iwa)
    f = aha__iwa['f']
    return f


@overload(pd.timedelta_range, no_unliteral=True)
def pd_timedelta_range_overload(start=None, end=None, periods=None, freq=
    None, name=None, closed=None):
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise BodoError(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )

    def f(start=None, end=None, periods=None, freq=None, name=None, closed=None
        ):
        if freq is None and (start is None or end is None or periods is None):
            freq = 'D'
        freq = bodo.hiframes.pd_index_ext.to_offset_value(freq)
        crk__gtf = pd.Timedelta('1 day')
        if start is not None:
            crk__gtf = pd.Timedelta(start)
        vdrd__dra = pd.Timedelta('1 day')
        if end is not None:
            vdrd__dra = pd.Timedelta(end)
        if start is None and end is None and closed is not None:
            raise ValueError(
                'Closed has to be None if not both of start and end are defined'
                )
        hjzsw__jif, jikdl__gxd = bodo.hiframes.pd_index_ext.validate_endpoints(
            closed)
        if freq is not None:
            tzvn__ueh = _dummy_convert_none_to_int(freq)
            if periods is None:
                b = crk__gtf.value
                frgv__kcl = b + (vdrd__dra.value - b
                    ) // tzvn__ueh * tzvn__ueh + tzvn__ueh // 2 + 1
            elif start is not None:
                periods = _dummy_convert_none_to_int(periods)
                b = crk__gtf.value
                dry__crunf = np.int64(periods) * np.int64(tzvn__ueh)
                frgv__kcl = np.int64(b) + dry__crunf
            elif end is not None:
                periods = _dummy_convert_none_to_int(periods)
                frgv__kcl = vdrd__dra.value + tzvn__ueh
                dry__crunf = np.int64(periods) * np.int64(-tzvn__ueh)
                b = np.int64(frgv__kcl) + dry__crunf
            else:
                raise ValueError(
                    "at least 'start' or 'end' should be specified if a 'period' is given."
                    )
            abph__hoc = np.arange(b, frgv__kcl, tzvn__ueh, np.int64)
        else:
            periods = _dummy_convert_none_to_int(periods)
            hvso__gknmy = vdrd__dra.value - crk__gtf.value
            step = hvso__gknmy / (periods - 1)
            ebvzp__gsnnc = np.arange(0, periods, 1, np.float64)
            ebvzp__gsnnc *= step
            ebvzp__gsnnc += crk__gtf.value
            abph__hoc = ebvzp__gsnnc.astype(np.int64)
            abph__hoc[-1] = vdrd__dra.value
        if not hjzsw__jif and len(abph__hoc) and abph__hoc[0
            ] == crk__gtf.value:
            abph__hoc = abph__hoc[1:]
        if not jikdl__gxd and len(abph__hoc) and abph__hoc[-1
            ] == vdrd__dra.value:
            abph__hoc = abph__hoc[:-1]
        S = bodo.utils.conversion.convert_to_dt64ns(abph__hoc)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return f


@overload_method(DatetimeIndexType, 'isocalendar', inline='always',
    no_unliteral=True)
def overload_pd_timestamp_isocalendar(idx):
    liwrb__svcl = ColNamesMetaType(('year', 'week', 'day'))

    def impl(idx):
        A = bodo.hiframes.pd_index_ext.get_index_data(idx)
        numba.parfors.parfor.init_prange()
        svaxh__xlacb = len(A)
        ludfs__fgktj = bodo.libs.int_arr_ext.alloc_int_array(svaxh__xlacb,
            np.uint32)
        jxc__jkd = bodo.libs.int_arr_ext.alloc_int_array(svaxh__xlacb, np.
            uint32)
        qfdw__lyfl = bodo.libs.int_arr_ext.alloc_int_array(svaxh__xlacb, np
            .uint32)
        for i in numba.parfors.parfor.internal_prange(svaxh__xlacb):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(ludfs__fgktj, i)
                bodo.libs.array_kernels.setna(jxc__jkd, i)
                bodo.libs.array_kernels.setna(qfdw__lyfl, i)
                continue
            ludfs__fgktj[i], jxc__jkd[i], qfdw__lyfl[i
                ] = bodo.utils.conversion.box_if_dt64(A[i]).isocalendar()
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((ludfs__fgktj,
            jxc__jkd, qfdw__lyfl), idx, liwrb__svcl)
    return impl


class TimedeltaIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = types.Array(bodo.timedelta64ns, 1, 'C'
            ) if data is None else data
        super(TimedeltaIndexType, self).__init__(name=
            f'TimedeltaIndexType({name_typ}, {self.data})')
    ndim = 1

    def copy(self):
        return TimedeltaIndexType(self.name_typ)

    @property
    def dtype(self):
        return types.NPTimedelta('ns')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def key(self):
        return self.name_typ, self.data

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self, bodo.pd_timedelta_type
            )

    @property
    def pandas_type_name(self):
        return 'timedelta'

    @property
    def numpy_type_name(self):
        return 'timedelta64[ns]'


timedelta_index = TimedeltaIndexType()
types.timedelta_index = timedelta_index


@register_model(TimedeltaIndexType)
class TimedeltaIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ofgt__msmd = [('data', _timedelta_index_data_typ), ('name', fe_type
            .name_typ), ('dict', types.DictType(_timedelta_index_data_typ.
            dtype, types.int64))]
        super(TimedeltaIndexTypeModel, self).__init__(dmm, fe_type, ofgt__msmd)


@typeof_impl.register(pd.TimedeltaIndex)
def typeof_timedelta_index(val, c):
    return TimedeltaIndexType(get_val_type_maybe_str_literal(val.name))


@box(TimedeltaIndexType)
def box_timedelta_index(typ, val, c):
    nrttr__ydfyo = c.context.insert_const_string(c.builder.module, 'pandas')
    bxko__fdp = c.pyapi.import_module_noblock(nrttr__ydfyo)
    timedelta_index = numba.core.cgutils.create_struct_proxy(typ)(c.context,
        c.builder, val)
    c.context.nrt.incref(c.builder, _timedelta_index_data_typ,
        timedelta_index.data)
    bpe__skerx = c.pyapi.from_native_value(_timedelta_index_data_typ,
        timedelta_index.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, timedelta_index.name)
    qwh__ohiqx = c.pyapi.from_native_value(typ.name_typ, timedelta_index.
        name, c.env_manager)
    args = c.pyapi.tuple_pack([bpe__skerx])
    kws = c.pyapi.dict_pack([('name', qwh__ohiqx)])
    mhkn__mxcd = c.pyapi.object_getattr_string(bxko__fdp, 'TimedeltaIndex')
    ilsy__vsjmx = c.pyapi.call(mhkn__mxcd, args, kws)
    c.pyapi.decref(bpe__skerx)
    c.pyapi.decref(qwh__ohiqx)
    c.pyapi.decref(bxko__fdp)
    c.pyapi.decref(mhkn__mxcd)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ilsy__vsjmx


@unbox(TimedeltaIndexType)
def unbox_timedelta_index(typ, val, c):
    uwdm__ufg = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(_timedelta_index_data_typ, uwdm__ufg).value
    qwh__ohiqx = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, qwh__ohiqx).value
    c.pyapi.decref(uwdm__ufg)
    c.pyapi.decref(qwh__ohiqx)
    qizmc__fib = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qizmc__fib.data = data
    qizmc__fib.name = name
    dtype = _timedelta_index_data_typ.dtype
    fzh__hfgz, fesi__rmrcv = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    qizmc__fib.dict = fesi__rmrcv
    return NativeValue(qizmc__fib._getvalue())


@intrinsic
def init_timedelta_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        dfyr__fknq, lvbap__ndlqk = args
        timedelta_index = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        timedelta_index.data = dfyr__fknq
        timedelta_index.name = lvbap__ndlqk
        context.nrt.incref(builder, signature.args[0], dfyr__fknq)
        context.nrt.incref(builder, signature.args[1], lvbap__ndlqk)
        dtype = _timedelta_index_data_typ.dtype
        timedelta_index.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return timedelta_index._getvalue()
    ahu__fnuh = TimedeltaIndexType(name)
    sig = signature(ahu__fnuh, data, name)
    return sig, codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_timedelta_index
    ) = init_index_equiv


@infer_getattr
class TimedeltaIndexAttribute(AttributeTemplate):
    key = TimedeltaIndexType

    def resolve_values(self, ary):
        return _timedelta_index_data_typ


make_attribute_wrapper(TimedeltaIndexType, 'data', '_data')
make_attribute_wrapper(TimedeltaIndexType, 'name', '_name')
make_attribute_wrapper(TimedeltaIndexType, 'dict', '_dict')


@overload_method(TimedeltaIndexType, 'copy', no_unliteral=True)
def overload_timedelta_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    amisc__pgijx = dict(deep=deep, dtype=dtype, names=names)
    yng__jtz = idx_typ_to_format_str_map[TimedeltaIndexType].format('copy()')
    check_unsupported_args('TimedeltaIndex.copy', amisc__pgijx,
        idx_cpy_arg_defaults, fn_str=yng__jtz, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_timedelta_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_timedelta_index(A._data.
                copy(), A._name)
    return impl


@overload_method(TimedeltaIndexType, 'min', inline='always', no_unliteral=True)
def overload_timedelta_index_min(tdi, axis=None, skipna=True):
    tsp__ume = dict(axis=axis, skipna=skipna)
    ugzcb__bvng = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.min', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        svaxh__xlacb = len(data)
        ekf__uln = numba.cpython.builtins.get_type_max_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(svaxh__xlacb):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            ekf__uln = min(ekf__uln, val)
        ejzt__caaiq = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            ekf__uln)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(ejzt__caaiq, count)
    return impl


@overload_method(TimedeltaIndexType, 'max', inline='always', no_unliteral=True)
def overload_timedelta_index_max(tdi, axis=None, skipna=True):
    tsp__ume = dict(axis=axis, skipna=skipna)
    ugzcb__bvng = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.max', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')
    if not is_overload_none(axis) or not is_overload_true(skipna):
        raise BodoError(
            'Index.min(): axis and skipna arguments not supported yet')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        svaxh__xlacb = len(data)
        ubj__zdf = numba.cpython.builtins.get_type_min_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(svaxh__xlacb):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            ubj__zdf = max(ubj__zdf, val)
        ejzt__caaiq = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            ubj__zdf)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(ejzt__caaiq, count)
    return impl


def gen_tdi_field_impl(field):
    abd__wuyu = 'def impl(tdi):\n'
    abd__wuyu += '    numba.parfors.parfor.init_prange()\n'
    abd__wuyu += '    A = bodo.hiframes.pd_index_ext.get_index_data(tdi)\n'
    abd__wuyu += '    name = bodo.hiframes.pd_index_ext.get_index_name(tdi)\n'
    abd__wuyu += '    n = len(A)\n'
    abd__wuyu += '    S = np.empty(n, np.int64)\n'
    abd__wuyu += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    abd__wuyu += (
        '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
        )
    if field == 'nanoseconds':
        abd__wuyu += '        S[i] = td64 % 1000\n'
    elif field == 'microseconds':
        abd__wuyu += '        S[i] = td64 // 1000 % 100000\n'
    elif field == 'seconds':
        abd__wuyu += (
            '        S[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
    elif field == 'days':
        abd__wuyu += '        S[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n'
    else:
        assert False, 'invalid timedelta field'
    abd__wuyu += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    aha__iwa = {}
    exec(abd__wuyu, {'numba': numba, 'np': np, 'bodo': bodo}, aha__iwa)
    impl = aha__iwa['impl']
    return impl


def _install_tdi_time_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        impl = gen_tdi_field_impl(field)
        overload_attribute(TimedeltaIndexType, field)(lambda tdi: impl)


_install_tdi_time_fields()


@overload(pd.TimedeltaIndex, no_unliteral=True)
def pd_timedelta_index_overload(data=None, unit=None, freq=None, dtype=None,
    copy=False, name=None):
    if is_overload_none(data):
        raise BodoError('data argument in pd.TimedeltaIndex() expected')
    tsp__ume = dict(unit=unit, freq=freq, dtype=dtype, copy=copy)
    ugzcb__bvng = dict(unit=None, freq=None, dtype=None, copy=False)
    check_unsupported_args('pandas.TimedeltaIndex', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')

    def impl(data=None, unit=None, freq=None, dtype=None, copy=False, name=None
        ):
        neaf__lkhcn = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_td64ns(neaf__lkhcn)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return impl


class RangeIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None):
        if name_typ is None:
            name_typ = types.none
        self.name_typ = name_typ
        super(RangeIndexType, self).__init__(name=f'RangeIndexType({name_typ})'
            )
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return RangeIndexType(self.name_typ)

    @property
    def iterator_type(self):
        return types.iterators.RangeIteratorType(types.int64)

    @property
    def dtype(self):
        return types.int64

    @property
    def pandas_type_name(self):
        return str(self.dtype)

    @property
    def numpy_type_name(self):
        return str(self.dtype)

    def unify(self, typingctx, other):
        if isinstance(other, NumericIndexType):
            name_typ = self.name_typ.unify(typingctx, other.name_typ)
            if name_typ is None:
                name_typ = types.none
            return NumericIndexType(types.int64, name_typ)


@typeof_impl.register(pd.RangeIndex)
def typeof_pd_range_index(val, c):
    return RangeIndexType(get_val_type_maybe_str_literal(val.name))


@register_model(RangeIndexType)
class RangeIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ofgt__msmd = [('start', types.int64), ('stop', types.int64), (
            'step', types.int64), ('name', fe_type.name_typ)]
        super(RangeIndexModel, self).__init__(dmm, fe_type, ofgt__msmd)


make_attribute_wrapper(RangeIndexType, 'start', '_start')
make_attribute_wrapper(RangeIndexType, 'stop', '_stop')
make_attribute_wrapper(RangeIndexType, 'step', '_step')
make_attribute_wrapper(RangeIndexType, 'name', '_name')


@overload_method(RangeIndexType, 'copy', no_unliteral=True)
def overload_range_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    amisc__pgijx = dict(deep=deep, dtype=dtype, names=names)
    yng__jtz = idx_typ_to_format_str_map[RangeIndexType].format('copy()')
    check_unsupported_args('RangeIndex.copy', amisc__pgijx,
        idx_cpy_arg_defaults, fn_str=yng__jtz, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_range_index(A._start, A.
                _stop, A._step, name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_range_index(A._start, A.
                _stop, A._step, A._name)
    return impl


@box(RangeIndexType)
def box_range_index(typ, val, c):
    nrttr__ydfyo = c.context.insert_const_string(c.builder.module, 'pandas')
    fjoss__ibn = c.pyapi.import_module_noblock(nrttr__ydfyo)
    nnuxz__aeou = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    nyy__fmkb = c.pyapi.from_native_value(types.int64, nnuxz__aeou.start, c
        .env_manager)
    dpq__pdqm = c.pyapi.from_native_value(types.int64, nnuxz__aeou.stop, c.
        env_manager)
    yhixq__kngpy = c.pyapi.from_native_value(types.int64, nnuxz__aeou.step,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, nnuxz__aeou.name)
    qwh__ohiqx = c.pyapi.from_native_value(typ.name_typ, nnuxz__aeou.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([nyy__fmkb, dpq__pdqm, yhixq__kngpy])
    kws = c.pyapi.dict_pack([('name', qwh__ohiqx)])
    mhkn__mxcd = c.pyapi.object_getattr_string(fjoss__ibn, 'RangeIndex')
    zlk__psqx = c.pyapi.call(mhkn__mxcd, args, kws)
    c.pyapi.decref(nyy__fmkb)
    c.pyapi.decref(dpq__pdqm)
    c.pyapi.decref(yhixq__kngpy)
    c.pyapi.decref(qwh__ohiqx)
    c.pyapi.decref(fjoss__ibn)
    c.pyapi.decref(mhkn__mxcd)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return zlk__psqx


@intrinsic
def init_range_index(typingctx, start, stop, step, name=None):
    name = types.none if name is None else name
    wkr__ytvsk = is_overload_constant_int(step) and get_overload_const_int(step
        ) == 0

    def codegen(context, builder, signature, args):
        assert len(args) == 4
        if wkr__ytvsk:
            raise_bodo_error('Step must not be zero')
        lxpef__qex = cgutils.is_scalar_zero(builder, args[2])
        fvelg__jjmd = context.get_python_api(builder)
        with builder.if_then(lxpef__qex):
            fvelg__jjmd.err_format('PyExc_ValueError', 'Step must not be zero')
            val = context.get_constant(types.int32, -1)
            builder.ret(val)
        nnuxz__aeou = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        nnuxz__aeou.start = args[0]
        nnuxz__aeou.stop = args[1]
        nnuxz__aeou.step = args[2]
        nnuxz__aeou.name = args[3]
        context.nrt.incref(builder, signature.return_type.name_typ, args[3])
        return nnuxz__aeou._getvalue()
    return RangeIndexType(name)(start, stop, step, name), codegen


def init_range_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    start, stop, step, hhqg__sokd = args
    if self.typemap[start.name] == types.IntegerLiteral(0) and self.typemap[
        step.name] == types.IntegerLiteral(1) and equiv_set.has_shape(stop):
        return ArrayAnalysis.AnalyzeResult(shape=stop, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_range_index
    ) = init_range_index_equiv


@unbox(RangeIndexType)
def unbox_range_index(typ, val, c):
    nyy__fmkb = c.pyapi.object_getattr_string(val, 'start')
    start = c.pyapi.to_native_value(types.int64, nyy__fmkb).value
    dpq__pdqm = c.pyapi.object_getattr_string(val, 'stop')
    stop = c.pyapi.to_native_value(types.int64, dpq__pdqm).value
    yhixq__kngpy = c.pyapi.object_getattr_string(val, 'step')
    step = c.pyapi.to_native_value(types.int64, yhixq__kngpy).value
    qwh__ohiqx = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, qwh__ohiqx).value
    c.pyapi.decref(nyy__fmkb)
    c.pyapi.decref(dpq__pdqm)
    c.pyapi.decref(yhixq__kngpy)
    c.pyapi.decref(qwh__ohiqx)
    nnuxz__aeou = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    nnuxz__aeou.start = start
    nnuxz__aeou.stop = stop
    nnuxz__aeou.step = step
    nnuxz__aeou.name = name
    return NativeValue(nnuxz__aeou._getvalue())


@lower_constant(RangeIndexType)
def lower_constant_range_index(context, builder, ty, pyval):
    start = context.get_constant(types.int64, pyval.start)
    stop = context.get_constant(types.int64, pyval.stop)
    step = context.get_constant(types.int64, pyval.step)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    return lir.Constant.literal_struct([start, stop, step, name])


@overload(pd.RangeIndex, no_unliteral=True, inline='always')
def range_index_overload(start=None, stop=None, step=None, dtype=None, copy
    =False, name=None):

    def _ensure_int_or_none(value, field):
        rups__dsy = (
            'RangeIndex(...) must be called with integers, {value} was passed for {field}'
            )
        if not is_overload_none(value) and not isinstance(value, types.
            IntegerLiteral) and not isinstance(value, types.Integer):
            raise BodoError(rups__dsy.format(value=value, field=field))
    _ensure_int_or_none(start, 'start')
    _ensure_int_or_none(stop, 'stop')
    _ensure_int_or_none(step, 'step')
    if is_overload_none(start) and is_overload_none(stop) and is_overload_none(
        step):
        rups__dsy = 'RangeIndex(...) must be called with integers'
        raise BodoError(rups__dsy)
    jshjv__hqv = 'start'
    zht__mng = 'stop'
    lad__ekl = 'step'
    if is_overload_none(start):
        jshjv__hqv = '0'
    if is_overload_none(stop):
        zht__mng = 'start'
        jshjv__hqv = '0'
    if is_overload_none(step):
        lad__ekl = '1'
    abd__wuyu = """def _pd_range_index_imp(start=None, stop=None, step=None, dtype=None, copy=False, name=None):
"""
    abd__wuyu += '  return init_range_index({}, {}, {}, name)\n'.format(
        jshjv__hqv, zht__mng, lad__ekl)
    aha__iwa = {}
    exec(abd__wuyu, {'init_range_index': init_range_index}, aha__iwa)
    nbwgm__prvpm = aha__iwa['_pd_range_index_imp']
    return nbwgm__prvpm


@overload(pd.CategoricalIndex, no_unliteral=True, inline='always')
def categorical_index_overload(data=None, categories=None, ordered=None,
    dtype=None, copy=False, name=None):
    raise BodoError('pd.CategoricalIndex() initializer not yet supported.')


@overload_attribute(RangeIndexType, 'start')
def rangeIndex_get_start(ri):

    def impl(ri):
        return ri._start
    return impl


@overload_attribute(RangeIndexType, 'stop')
def rangeIndex_get_stop(ri):

    def impl(ri):
        return ri._stop
    return impl


@overload_attribute(RangeIndexType, 'step')
def rangeIndex_get_step(ri):

    def impl(ri):
        return ri._step
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_range_index_getitem(I, idx):
    if isinstance(I, RangeIndexType):
        if isinstance(types.unliteral(idx), types.Integer):
            return lambda I, idx: idx * I._step + I._start
        if isinstance(idx, types.SliceType):

            def impl(I, idx):
                cqiy__qvp = numba.cpython.unicode._normalize_slice(idx, len(I))
                name = bodo.hiframes.pd_index_ext.get_index_name(I)
                start = I._start + I._step * cqiy__qvp.start
                stop = I._start + I._step * cqiy__qvp.stop
                step = I._step * cqiy__qvp.step
                return bodo.hiframes.pd_index_ext.init_range_index(start,
                    stop, step, name)
            return impl
        return lambda I, idx: bodo.hiframes.pd_index_ext.init_numeric_index(np
            .arange(I._start, I._stop, I._step, np.int64)[idx], bodo.
            hiframes.pd_index_ext.get_index_name(I))


@overload(len, no_unliteral=True)
def overload_range_len(r):
    if isinstance(r, RangeIndexType):
        return lambda r: max(0, -(-(r._stop - r._start) // r._step))


class PeriodIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, freq, name_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.freq = freq
        self.name_typ = name_typ
        super(PeriodIndexType, self).__init__(name=
            'PeriodIndexType({}, {})'.format(freq, name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return PeriodIndexType(self.freq, self.name_typ)

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return f'period[{self.freq}]'


@typeof_impl.register(pd.PeriodIndex)
def typeof_pd_period_index(val, c):
    return PeriodIndexType(val.freqstr, get_val_type_maybe_str_literal(val.
        name))


@register_model(PeriodIndexType)
class PeriodIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ofgt__msmd = [('data', bodo.IntegerArrayType(types.int64)), ('name',
            fe_type.name_typ), ('dict', types.DictType(types.int64, types.
            int64))]
        super(PeriodIndexModel, self).__init__(dmm, fe_type, ofgt__msmd)


make_attribute_wrapper(PeriodIndexType, 'data', '_data')
make_attribute_wrapper(PeriodIndexType, 'name', '_name')
make_attribute_wrapper(PeriodIndexType, 'dict', '_dict')


@overload_method(PeriodIndexType, 'copy', no_unliteral=True)
def overload_period_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    freq = A.freq
    amisc__pgijx = dict(deep=deep, dtype=dtype, names=names)
    yng__jtz = idx_typ_to_format_str_map[PeriodIndexType].format('copy()')
    check_unsupported_args('PeriodIndex.copy', amisc__pgijx,
        idx_cpy_arg_defaults, fn_str=yng__jtz, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_period_index(A._data.
                copy(), name, freq)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_period_index(A._data.
                copy(), A._name, freq)
    return impl


@intrinsic
def init_period_index(typingctx, data, name, freq):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        dfyr__fknq, lvbap__ndlqk, hhqg__sokd = args
        cdlf__hqhf = signature.return_type
        qfy__zjt = cgutils.create_struct_proxy(cdlf__hqhf)(context, builder)
        qfy__zjt.data = dfyr__fknq
        qfy__zjt.name = lvbap__ndlqk
        context.nrt.incref(builder, signature.args[0], args[0])
        context.nrt.incref(builder, signature.args[1], args[1])
        qfy__zjt.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(types.int64, types.int64), types.DictType(
            types.int64, types.int64)(), [])
        return qfy__zjt._getvalue()
    qud__egn = get_overload_const_str(freq)
    ahu__fnuh = PeriodIndexType(qud__egn, name)
    sig = signature(ahu__fnuh, data, name, freq)
    return sig, codegen


@box(PeriodIndexType)
def box_period_index(typ, val, c):
    nrttr__ydfyo = c.context.insert_const_string(c.builder.module, 'pandas')
    fjoss__ibn = c.pyapi.import_module_noblock(nrttr__ydfyo)
    qizmc__fib = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, bodo.IntegerArrayType(types.int64),
        qizmc__fib.data)
    bpaja__qmng = c.pyapi.from_native_value(bodo.IntegerArrayType(types.
        int64), qizmc__fib.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, qizmc__fib.name)
    qwh__ohiqx = c.pyapi.from_native_value(typ.name_typ, qizmc__fib.name, c
        .env_manager)
    djri__yfo = c.pyapi.string_from_constant_string(typ.freq)
    args = c.pyapi.tuple_pack([])
    kws = c.pyapi.dict_pack([('ordinal', bpaja__qmng), ('name', qwh__ohiqx),
        ('freq', djri__yfo)])
    mhkn__mxcd = c.pyapi.object_getattr_string(fjoss__ibn, 'PeriodIndex')
    zlk__psqx = c.pyapi.call(mhkn__mxcd, args, kws)
    c.pyapi.decref(bpaja__qmng)
    c.pyapi.decref(qwh__ohiqx)
    c.pyapi.decref(djri__yfo)
    c.pyapi.decref(fjoss__ibn)
    c.pyapi.decref(mhkn__mxcd)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return zlk__psqx


@unbox(PeriodIndexType)
def unbox_period_index(typ, val, c):
    arr_typ = bodo.IntegerArrayType(types.int64)
    aifev__lwdx = c.pyapi.object_getattr_string(val, 'asi8')
    afcf__wrsub = c.pyapi.call_method(val, 'isna', ())
    qwh__ohiqx = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, qwh__ohiqx).value
    nrttr__ydfyo = c.context.insert_const_string(c.builder.module, 'pandas')
    bxko__fdp = c.pyapi.import_module_noblock(nrttr__ydfyo)
    qufx__ijvf = c.pyapi.object_getattr_string(bxko__fdp, 'arrays')
    bpaja__qmng = c.pyapi.call_method(qufx__ijvf, 'IntegerArray', (
        aifev__lwdx, afcf__wrsub))
    data = c.pyapi.to_native_value(arr_typ, bpaja__qmng).value
    c.pyapi.decref(aifev__lwdx)
    c.pyapi.decref(afcf__wrsub)
    c.pyapi.decref(qwh__ohiqx)
    c.pyapi.decref(bxko__fdp)
    c.pyapi.decref(qufx__ijvf)
    c.pyapi.decref(bpaja__qmng)
    qizmc__fib = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qizmc__fib.data = data
    qizmc__fib.name = name
    fzh__hfgz, fesi__rmrcv = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(types.int64, types.int64), types.DictType(types.int64,
        types.int64)(), [])
    qizmc__fib.dict = fesi__rmrcv
    return NativeValue(qizmc__fib._getvalue())


class CategoricalIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, data, name_typ=None):
        from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
        assert isinstance(data, CategoricalArrayType
            ), 'CategoricalIndexType expects CategoricalArrayType'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = data
        super(CategoricalIndexType, self).__init__(name=
            f'CategoricalIndexType(data={self.data}, name={name_typ})')
    ndim = 1

    def copy(self):
        return CategoricalIndexType(self.data, self.name_typ)

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return self.data.dtype

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'categorical'

    @property
    def numpy_type_name(self):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        return str(get_categories_int_type(self.dtype))

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self, self.dtype.elem_type)


@register_model(CategoricalIndexType)
class CategoricalIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        mpy__dzw = get_categories_int_type(fe_type.data.dtype)
        ofgt__msmd = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(mpy__dzw, types.int64))]
        super(CategoricalIndexTypeModel, self).__init__(dmm, fe_type,
            ofgt__msmd)


@typeof_impl.register(pd.CategoricalIndex)
def typeof_categorical_index(val, c):
    return CategoricalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(CategoricalIndexType)
def box_categorical_index(typ, val, c):
    nrttr__ydfyo = c.context.insert_const_string(c.builder.module, 'pandas')
    bxko__fdp = c.pyapi.import_module_noblock(nrttr__ydfyo)
    leglk__zlbc = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, leglk__zlbc.data)
    bpe__skerx = c.pyapi.from_native_value(typ.data, leglk__zlbc.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, leglk__zlbc.name)
    qwh__ohiqx = c.pyapi.from_native_value(typ.name_typ, leglk__zlbc.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([bpe__skerx])
    kws = c.pyapi.dict_pack([('name', qwh__ohiqx)])
    mhkn__mxcd = c.pyapi.object_getattr_string(bxko__fdp, 'CategoricalIndex')
    ilsy__vsjmx = c.pyapi.call(mhkn__mxcd, args, kws)
    c.pyapi.decref(bpe__skerx)
    c.pyapi.decref(qwh__ohiqx)
    c.pyapi.decref(bxko__fdp)
    c.pyapi.decref(mhkn__mxcd)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ilsy__vsjmx


@unbox(CategoricalIndexType)
def unbox_categorical_index(typ, val, c):
    from bodo.hiframes.pd_categorical_ext import get_categories_int_type
    uwdm__ufg = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, uwdm__ufg).value
    qwh__ohiqx = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, qwh__ohiqx).value
    c.pyapi.decref(uwdm__ufg)
    c.pyapi.decref(qwh__ohiqx)
    qizmc__fib = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qizmc__fib.data = data
    qizmc__fib.name = name
    dtype = get_categories_int_type(typ.data.dtype)
    fzh__hfgz, fesi__rmrcv = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    qizmc__fib.dict = fesi__rmrcv
    return NativeValue(qizmc__fib._getvalue())


@intrinsic
def init_categorical_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        dfyr__fknq, lvbap__ndlqk = args
        leglk__zlbc = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        leglk__zlbc.data = dfyr__fknq
        leglk__zlbc.name = lvbap__ndlqk
        context.nrt.incref(builder, signature.args[0], dfyr__fknq)
        context.nrt.incref(builder, signature.args[1], lvbap__ndlqk)
        dtype = get_categories_int_type(signature.return_type.data.dtype)
        leglk__zlbc.dict = context.compile_internal(builder, lambda : numba
            .typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return leglk__zlbc._getvalue()
    ahu__fnuh = CategoricalIndexType(data, name)
    sig = signature(ahu__fnuh, data, name)
    return sig, codegen


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_categorical_index
    ) = init_index_equiv
make_attribute_wrapper(CategoricalIndexType, 'data', '_data')
make_attribute_wrapper(CategoricalIndexType, 'name', '_name')
make_attribute_wrapper(CategoricalIndexType, 'dict', '_dict')


@overload_method(CategoricalIndexType, 'copy', no_unliteral=True)
def overload_categorical_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    yng__jtz = idx_typ_to_format_str_map[CategoricalIndexType].format('copy()')
    amisc__pgijx = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('CategoricalIndex.copy', amisc__pgijx,
        idx_cpy_arg_defaults, fn_str=yng__jtz, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_categorical_index(A.
                _data.copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_categorical_index(A.
                _data.copy(), A._name)
    return impl


class IntervalIndexType(types.ArrayCompatible):

    def __init__(self, data, name_typ=None):
        from bodo.libs.interval_arr_ext import IntervalArrayType
        assert isinstance(data, IntervalArrayType
            ), 'IntervalIndexType expects IntervalArrayType'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = data
        super(IntervalIndexType, self).__init__(name=
            f'IntervalIndexType(data={self.data}, name={name_typ})')
    ndim = 1

    def copy(self):
        return IntervalIndexType(self.data, self.name_typ)

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return f'interval[{self.data.arr_type.dtype}, right]'


@register_model(IntervalIndexType)
class IntervalIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ofgt__msmd = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(types.UniTuple(fe_type.data.arr_type.
            dtype, 2), types.int64))]
        super(IntervalIndexTypeModel, self).__init__(dmm, fe_type, ofgt__msmd)


@typeof_impl.register(pd.IntervalIndex)
def typeof_interval_index(val, c):
    return IntervalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(IntervalIndexType)
def box_interval_index(typ, val, c):
    nrttr__ydfyo = c.context.insert_const_string(c.builder.module, 'pandas')
    bxko__fdp = c.pyapi.import_module_noblock(nrttr__ydfyo)
    dye__hmckc = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, dye__hmckc.data)
    bpe__skerx = c.pyapi.from_native_value(typ.data, dye__hmckc.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, dye__hmckc.name)
    qwh__ohiqx = c.pyapi.from_native_value(typ.name_typ, dye__hmckc.name, c
        .env_manager)
    args = c.pyapi.tuple_pack([bpe__skerx])
    kws = c.pyapi.dict_pack([('name', qwh__ohiqx)])
    mhkn__mxcd = c.pyapi.object_getattr_string(bxko__fdp, 'IntervalIndex')
    ilsy__vsjmx = c.pyapi.call(mhkn__mxcd, args, kws)
    c.pyapi.decref(bpe__skerx)
    c.pyapi.decref(qwh__ohiqx)
    c.pyapi.decref(bxko__fdp)
    c.pyapi.decref(mhkn__mxcd)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return ilsy__vsjmx


@unbox(IntervalIndexType)
def unbox_interval_index(typ, val, c):
    uwdm__ufg = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, uwdm__ufg).value
    qwh__ohiqx = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, qwh__ohiqx).value
    c.pyapi.decref(uwdm__ufg)
    c.pyapi.decref(qwh__ohiqx)
    qizmc__fib = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qizmc__fib.data = data
    qizmc__fib.name = name
    dtype = types.UniTuple(typ.data.arr_type.dtype, 2)
    fzh__hfgz, fesi__rmrcv = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    qizmc__fib.dict = fesi__rmrcv
    return NativeValue(qizmc__fib._getvalue())


@intrinsic
def init_interval_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        dfyr__fknq, lvbap__ndlqk = args
        dye__hmckc = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        dye__hmckc.data = dfyr__fknq
        dye__hmckc.name = lvbap__ndlqk
        context.nrt.incref(builder, signature.args[0], dfyr__fknq)
        context.nrt.incref(builder, signature.args[1], lvbap__ndlqk)
        dtype = types.UniTuple(data.arr_type.dtype, 2)
        dye__hmckc.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return dye__hmckc._getvalue()
    ahu__fnuh = IntervalIndexType(data, name)
    sig = signature(ahu__fnuh, data, name)
    return sig, codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_interval_index
    ) = init_index_equiv
make_attribute_wrapper(IntervalIndexType, 'data', '_data')
make_attribute_wrapper(IntervalIndexType, 'name', '_name')
make_attribute_wrapper(IntervalIndexType, 'dict', '_dict')


class NumericIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, dtype, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.dtype = dtype
        self.name_typ = name_typ
        data = dtype_to_array_type(dtype) if data is None else data
        self.data = data
        super(NumericIndexType, self).__init__(name=
            f'NumericIndexType({dtype}, {name_typ}, {data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return NumericIndexType(self.dtype, self.name_typ, self.data)

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)

    @property
    def pandas_type_name(self):
        return str(self.dtype)

    @property
    def numpy_type_name(self):
        return str(self.dtype)


with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    Int64Index = pd.Int64Index
    UInt64Index = pd.UInt64Index
    Float64Index = pd.Float64Index


@typeof_impl.register(Int64Index)
def typeof_pd_int64_index(val, c):
    return NumericIndexType(types.int64, get_val_type_maybe_str_literal(val
        .name))


@typeof_impl.register(UInt64Index)
def typeof_pd_uint64_index(val, c):
    return NumericIndexType(types.uint64, get_val_type_maybe_str_literal(
        val.name))


@typeof_impl.register(Float64Index)
def typeof_pd_float64_index(val, c):
    return NumericIndexType(types.float64, get_val_type_maybe_str_literal(
        val.name))


@register_model(NumericIndexType)
class NumericIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ofgt__msmd = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(fe_type.dtype, types.int64))]
        super(NumericIndexModel, self).__init__(dmm, fe_type, ofgt__msmd)


make_attribute_wrapper(NumericIndexType, 'data', '_data')
make_attribute_wrapper(NumericIndexType, 'name', '_name')
make_attribute_wrapper(NumericIndexType, 'dict', '_dict')


@overload_method(NumericIndexType, 'copy', no_unliteral=True)
def overload_numeric_index_copy(A, name=None, deep=False, dtype=None, names
    =None):
    yng__jtz = idx_typ_to_format_str_map[NumericIndexType].format('copy()')
    amisc__pgijx = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', amisc__pgijx, idx_cpy_arg_defaults,
        fn_str=yng__jtz, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), A._name)
    return impl


@box(NumericIndexType)
def box_numeric_index(typ, val, c):
    nrttr__ydfyo = c.context.insert_const_string(c.builder.module, 'pandas')
    fjoss__ibn = c.pyapi.import_module_noblock(nrttr__ydfyo)
    qizmc__fib = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, qizmc__fib.data)
    bpaja__qmng = c.pyapi.from_native_value(typ.data, qizmc__fib.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, qizmc__fib.name)
    qwh__ohiqx = c.pyapi.from_native_value(typ.name_typ, qizmc__fib.name, c
        .env_manager)
    nrx__csi = c.pyapi.make_none()
    hhds__mfxwk = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    zlk__psqx = c.pyapi.call_method(fjoss__ibn, 'Index', (bpaja__qmng,
        nrx__csi, hhds__mfxwk, qwh__ohiqx))
    c.pyapi.decref(bpaja__qmng)
    c.pyapi.decref(nrx__csi)
    c.pyapi.decref(hhds__mfxwk)
    c.pyapi.decref(qwh__ohiqx)
    c.pyapi.decref(fjoss__ibn)
    c.context.nrt.decref(c.builder, typ, val)
    return zlk__psqx


@intrinsic
def init_numeric_index(typingctx, data, name=None):
    name = types.none if is_overload_none(name) else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        cdlf__hqhf = signature.return_type
        qizmc__fib = cgutils.create_struct_proxy(cdlf__hqhf)(context, builder)
        qizmc__fib.data = args[0]
        qizmc__fib.name = args[1]
        context.nrt.incref(builder, cdlf__hqhf.data, args[0])
        context.nrt.incref(builder, cdlf__hqhf.name_typ, args[1])
        dtype = cdlf__hqhf.dtype
        qizmc__fib.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return qizmc__fib._getvalue()
    return NumericIndexType(data.dtype, name, data)(data, name), codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_numeric_index
    ) = init_index_equiv


@unbox(NumericIndexType)
def unbox_numeric_index(typ, val, c):
    uwdm__ufg = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, uwdm__ufg).value
    qwh__ohiqx = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, qwh__ohiqx).value
    c.pyapi.decref(uwdm__ufg)
    c.pyapi.decref(qwh__ohiqx)
    qizmc__fib = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qizmc__fib.data = data
    qizmc__fib.name = name
    dtype = typ.dtype
    fzh__hfgz, fesi__rmrcv = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    qizmc__fib.dict = fesi__rmrcv
    return NativeValue(qizmc__fib._getvalue())


def create_numeric_constructor(func, func_str, default_dtype):

    def overload_impl(data=None, dtype=None, copy=False, name=None):
        cxm__ndhmv = dict(dtype=dtype)
        rhrlc__fjrr = dict(dtype=None)
        check_unsupported_args(func_str, cxm__ndhmv, rhrlc__fjrr,
            package_name='pandas', module_name='Index')
        if is_overload_false(copy):

            def impl(data=None, dtype=None, copy=False, name=None):
                neaf__lkhcn = bodo.utils.conversion.coerce_to_ndarray(data)
                qewyo__qyzc = bodo.utils.conversion.fix_arr_dtype(neaf__lkhcn,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(
                    qewyo__qyzc, name)
        else:

            def impl(data=None, dtype=None, copy=False, name=None):
                neaf__lkhcn = bodo.utils.conversion.coerce_to_ndarray(data)
                if copy:
                    neaf__lkhcn = neaf__lkhcn.copy()
                qewyo__qyzc = bodo.utils.conversion.fix_arr_dtype(neaf__lkhcn,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(
                    qewyo__qyzc, name)
        return impl
    return overload_impl


def _install_numeric_constructors():
    for func, func_str, default_dtype in ((Int64Index, 'pandas.Int64Index',
        np.int64), (UInt64Index, 'pandas.UInt64Index', np.uint64), (
        Float64Index, 'pandas.Float64Index', np.float64)):
        overload_impl = create_numeric_constructor(func, func_str,
            default_dtype)
        overload(func, no_unliteral=True)(overload_impl)


_install_numeric_constructors()


class StringIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = string_array_type if data_typ is None else data_typ
        super(StringIndexType, self).__init__(name=
            f'StringIndexType({name_typ}, {self.data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return StringIndexType(self.name_typ, self.data)

    @property
    def dtype(self):
        return string_type

    @property
    def pandas_type_name(self):
        return 'unicode'

    @property
    def numpy_type_name(self):
        return 'object'

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)


@register_model(StringIndexType)
class StringIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ofgt__msmd = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(string_type, types.int64))]
        super(StringIndexModel, self).__init__(dmm, fe_type, ofgt__msmd)


make_attribute_wrapper(StringIndexType, 'data', '_data')
make_attribute_wrapper(StringIndexType, 'name', '_name')
make_attribute_wrapper(StringIndexType, 'dict', '_dict')


class BinaryIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data_typ=None):
        assert data_typ is None or data_typ == binary_array_type, 'data_typ must be binary_array_type'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = binary_array_type
        super(BinaryIndexType, self).__init__(name='BinaryIndexType({})'.
            format(name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return BinaryIndexType(self.name_typ)

    @property
    def dtype(self):
        return bytes_type

    @property
    def pandas_type_name(self):
        return 'bytes'

    @property
    def numpy_type_name(self):
        return 'object'

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)


@register_model(BinaryIndexType)
class BinaryIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ofgt__msmd = [('data', binary_array_type), ('name', fe_type.
            name_typ), ('dict', types.DictType(bytes_type, types.int64))]
        super(BinaryIndexModel, self).__init__(dmm, fe_type, ofgt__msmd)


make_attribute_wrapper(BinaryIndexType, 'data', '_data')
make_attribute_wrapper(BinaryIndexType, 'name', '_name')
make_attribute_wrapper(BinaryIndexType, 'dict', '_dict')


@unbox(BinaryIndexType)
@unbox(StringIndexType)
def unbox_binary_str_index(typ, val, c):
    ydgd__bmcvp = typ.data
    scalar_type = typ.data.dtype
    uwdm__ufg = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(ydgd__bmcvp, uwdm__ufg).value
    qwh__ohiqx = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, qwh__ohiqx).value
    c.pyapi.decref(uwdm__ufg)
    c.pyapi.decref(qwh__ohiqx)
    qizmc__fib = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qizmc__fib.data = data
    qizmc__fib.name = name
    fzh__hfgz, fesi__rmrcv = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(scalar_type, types.int64), types.DictType(scalar_type,
        types.int64)(), [])
    qizmc__fib.dict = fesi__rmrcv
    return NativeValue(qizmc__fib._getvalue())


@box(BinaryIndexType)
@box(StringIndexType)
def box_binary_str_index(typ, val, c):
    ydgd__bmcvp = typ.data
    nrttr__ydfyo = c.context.insert_const_string(c.builder.module, 'pandas')
    fjoss__ibn = c.pyapi.import_module_noblock(nrttr__ydfyo)
    qizmc__fib = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, ydgd__bmcvp, qizmc__fib.data)
    bpaja__qmng = c.pyapi.from_native_value(ydgd__bmcvp, qizmc__fib.data, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, qizmc__fib.name)
    qwh__ohiqx = c.pyapi.from_native_value(typ.name_typ, qizmc__fib.name, c
        .env_manager)
    nrx__csi = c.pyapi.make_none()
    hhds__mfxwk = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    zlk__psqx = c.pyapi.call_method(fjoss__ibn, 'Index', (bpaja__qmng,
        nrx__csi, hhds__mfxwk, qwh__ohiqx))
    c.pyapi.decref(bpaja__qmng)
    c.pyapi.decref(nrx__csi)
    c.pyapi.decref(hhds__mfxwk)
    c.pyapi.decref(qwh__ohiqx)
    c.pyapi.decref(fjoss__ibn)
    c.context.nrt.decref(c.builder, typ, val)
    return zlk__psqx


@intrinsic
def init_binary_str_index(typingctx, data, name=None):
    name = types.none if name is None else name
    sig = type(bodo.utils.typing.get_index_type_from_dtype(data.dtype))(name,
        data)(data, name)
    pyrys__oxx = get_binary_str_codegen(is_binary=data.dtype == bytes_type)
    return sig, pyrys__oxx


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_binary_str_index
    ) = init_index_equiv


def get_binary_str_codegen(is_binary=False):
    if is_binary:
        acwk__eude = 'bytes_type'
    else:
        acwk__eude = 'string_type'
    abd__wuyu = 'def impl(context, builder, signature, args):\n'
    abd__wuyu += '    assert len(args) == 2\n'
    abd__wuyu += '    index_typ = signature.return_type\n'
    abd__wuyu += (
        '    index_val = cgutils.create_struct_proxy(index_typ)(context, builder)\n'
        )
    abd__wuyu += '    index_val.data = args[0]\n'
    abd__wuyu += '    index_val.name = args[1]\n'
    abd__wuyu += '    # increase refcount of stored values\n'
    abd__wuyu += (
        '    context.nrt.incref(builder, signature.args[0], args[0])\n')
    abd__wuyu += (
        '    context.nrt.incref(builder, index_typ.name_typ, args[1])\n')
    abd__wuyu += '    # create empty dict for get_loc hashmap\n'
    abd__wuyu += '    index_val.dict = context.compile_internal(\n'
    abd__wuyu += '       builder,\n'
    abd__wuyu += (
        f'       lambda: numba.typed.Dict.empty({acwk__eude}, types.int64),\n')
    abd__wuyu += f'        types.DictType({acwk__eude}, types.int64)(), [],)\n'
    abd__wuyu += '    return index_val._getvalue()\n'
    aha__iwa = {}
    exec(abd__wuyu, {'bodo': bodo, 'signature': signature, 'cgutils':
        cgutils, 'numba': numba, 'types': types, 'bytes_type': bytes_type,
        'string_type': string_type}, aha__iwa)
    impl = aha__iwa['impl']
    return impl


@overload_method(BinaryIndexType, 'copy', no_unliteral=True)
@overload_method(StringIndexType, 'copy', no_unliteral=True)
def overload_binary_string_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    typ = type(A)
    yng__jtz = idx_typ_to_format_str_map[typ].format('copy()')
    amisc__pgijx = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', amisc__pgijx, idx_cpy_arg_defaults,
        fn_str=yng__jtz, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_binary_str_index(A._data
                .copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_binary_str_index(A._data
                .copy(), A._name)
    return impl


@overload_attribute(BinaryIndexType, 'name')
@overload_attribute(StringIndexType, 'name')
@overload_attribute(DatetimeIndexType, 'name')
@overload_attribute(TimedeltaIndexType, 'name')
@overload_attribute(RangeIndexType, 'name')
@overload_attribute(PeriodIndexType, 'name')
@overload_attribute(NumericIndexType, 'name')
@overload_attribute(IntervalIndexType, 'name')
@overload_attribute(CategoricalIndexType, 'name')
@overload_attribute(MultiIndexType, 'name')
def Index_get_name(i):

    def impl(i):
        return i._name
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_index_getitem(I, ind):
    if isinstance(I, (NumericIndexType, StringIndexType, BinaryIndexType)
        ) and isinstance(ind, types.Integer):
        return lambda I, ind: bodo.hiframes.pd_index_ext.get_index_data(I)[ind]
    if isinstance(I, NumericIndexType):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_numeric_index(
            bodo.hiframes.pd_index_ext.get_index_data(I)[ind], bodo.
            hiframes.pd_index_ext.get_index_name(I))
    if isinstance(I, (StringIndexType, BinaryIndexType)):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_binary_str_index(
            bodo.hiframes.pd_index_ext.get_index_data(I)[ind], bodo.
            hiframes.pd_index_ext.get_index_name(I))


def array_type_to_index(arr_typ, name_typ=None):
    if is_str_arr_type(arr_typ):
        return StringIndexType(name_typ, arr_typ)
    if arr_typ == bodo.binary_array_type:
        return BinaryIndexType(name_typ)
    assert isinstance(arr_typ, (types.Array, IntegerArrayType,
        FloatingArrayType, bodo.CategoricalArrayType)) or arr_typ in (bodo.
        datetime_date_array_type, bodo.boolean_array
        ), f'Converting array type {arr_typ} to index not supported'
    if (arr_typ == bodo.datetime_date_array_type or arr_typ.dtype == types.
        NPDatetime('ns')):
        return DatetimeIndexType(name_typ)
    if isinstance(arr_typ, bodo.DatetimeArrayType):
        return DatetimeIndexType(name_typ, arr_typ)
    if isinstance(arr_typ, bodo.CategoricalArrayType):
        return CategoricalIndexType(arr_typ, name_typ)
    if arr_typ.dtype == types.NPTimedelta('ns'):
        return TimedeltaIndexType(name_typ)
    if isinstance(arr_typ.dtype, (types.Integer, types.Float, types.Boolean)):
        return NumericIndexType(arr_typ.dtype, name_typ, arr_typ)
    raise BodoError(f'invalid index type {arr_typ}')


def is_pd_index_type(t):
    return isinstance(t, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType, IntervalIndexType, CategoricalIndexType,
        PeriodIndexType, StringIndexType, BinaryIndexType, RangeIndexType,
        HeterogeneousIndexType))


def _verify_setop_compatible(func_name, I, other):
    if not is_pd_index_type(other) and not isinstance(other, (SeriesType,
        types.Array)):
        raise BodoError(
            f'pd.Index.{func_name}(): unsupported type for argument other: {other}'
            )
    fliaq__kxo = I.dtype if not isinstance(I, RangeIndexType) else types.int64
    uwev__gztsx = other.dtype if not isinstance(other, RangeIndexType
        ) else types.int64
    if fliaq__kxo != uwev__gztsx:
        raise BodoError(
            f'Index.{func_name}(): incompatible types {fliaq__kxo} and {uwev__gztsx}'
            )


@overload_method(NumericIndexType, 'union', inline='always')
@overload_method(StringIndexType, 'union', inline='always')
@overload_method(BinaryIndexType, 'union', inline='always')
@overload_method(DatetimeIndexType, 'union', inline='always')
@overload_method(TimedeltaIndexType, 'union', inline='always')
@overload_method(RangeIndexType, 'union', inline='always')
def overload_index_union(I, other, sort=None):
    tsp__ume = dict(sort=sort)
    uyxht__sva = dict(sort=None)
    check_unsupported_args('Index.union', tsp__ume, uyxht__sva,
        package_name='pandas', module_name='Index')
    _verify_setop_compatible('union', I, other)
    ilr__pck = get_index_constructor(I) if not isinstance(I, RangeIndexType
        ) else init_numeric_index

    def impl(I, other, sort=None):
        bbu__guww = bodo.utils.conversion.coerce_to_array(I)
        btptn__tgfxs = bodo.utils.conversion.coerce_to_array(other)
        wcp__aam = bodo.libs.array_kernels.concat([bbu__guww, btptn__tgfxs])
        vdnf__iobo = bodo.libs.array_kernels.unique(wcp__aam)
        return ilr__pck(vdnf__iobo, None)
    return impl


@overload_method(NumericIndexType, 'intersection', inline='always')
@overload_method(StringIndexType, 'intersection', inline='always')
@overload_method(BinaryIndexType, 'intersection', inline='always')
@overload_method(DatetimeIndexType, 'intersection', inline='always')
@overload_method(TimedeltaIndexType, 'intersection', inline='always')
@overload_method(RangeIndexType, 'intersection', inline='always')
def overload_index_intersection(I, other, sort=None):
    tsp__ume = dict(sort=sort)
    uyxht__sva = dict(sort=None)
    check_unsupported_args('Index.intersection', tsp__ume, uyxht__sva,
        package_name='pandas', module_name='Index')
    _verify_setop_compatible('intersection', I, other)
    ilr__pck = get_index_constructor(I) if not isinstance(I, RangeIndexType
        ) else init_numeric_index

    def impl(I, other, sort=None):
        bbu__guww = bodo.utils.conversion.coerce_to_array(I)
        btptn__tgfxs = bodo.utils.conversion.coerce_to_array(other)
        vbjh__oqw = bodo.libs.array_kernels.unique(bbu__guww)
        qmukf__uqpn = bodo.libs.array_kernels.unique(btptn__tgfxs)
        wcp__aam = bodo.libs.array_kernels.concat([vbjh__oqw, qmukf__uqpn])
        ntpz__cjrdo = pd.Series(wcp__aam).sort_values().values
        ekem__rthvv = bodo.libs.array_kernels.intersection_mask(ntpz__cjrdo)
        return ilr__pck(ntpz__cjrdo[ekem__rthvv], None)
    return impl


@overload_method(NumericIndexType, 'difference', inline='always')
@overload_method(StringIndexType, 'difference', inline='always')
@overload_method(BinaryIndexType, 'difference', inline='always')
@overload_method(DatetimeIndexType, 'difference', inline='always')
@overload_method(TimedeltaIndexType, 'difference', inline='always')
@overload_method(RangeIndexType, 'difference', inline='always')
def overload_index_difference(I, other, sort=None):
    tsp__ume = dict(sort=sort)
    uyxht__sva = dict(sort=None)
    check_unsupported_args('Index.difference', tsp__ume, uyxht__sva,
        package_name='pandas', module_name='Index')
    _verify_setop_compatible('difference', I, other)
    ilr__pck = get_index_constructor(I) if not isinstance(I, RangeIndexType
        ) else init_numeric_index

    def impl(I, other, sort=None):
        bbu__guww = bodo.utils.conversion.coerce_to_array(I)
        btptn__tgfxs = bodo.utils.conversion.coerce_to_array(other)
        vbjh__oqw = bodo.libs.array_kernels.unique(bbu__guww)
        qmukf__uqpn = bodo.libs.array_kernels.unique(btptn__tgfxs)
        ekem__rthvv = np.empty(len(vbjh__oqw), np.bool_)
        bodo.libs.array.array_isin(ekem__rthvv, vbjh__oqw, qmukf__uqpn, False)
        return ilr__pck(vbjh__oqw[~ekem__rthvv], None)
    return impl


@overload_method(NumericIndexType, 'symmetric_difference', inline='always')
@overload_method(StringIndexType, 'symmetric_difference', inline='always')
@overload_method(BinaryIndexType, 'symmetric_difference', inline='always')
@overload_method(DatetimeIndexType, 'symmetric_difference', inline='always')
@overload_method(TimedeltaIndexType, 'symmetric_difference', inline='always')
@overload_method(RangeIndexType, 'symmetric_difference', inline='always')
def overload_index_symmetric_difference(I, other, result_name=None, sort=None):
    tsp__ume = dict(result_name=result_name, sort=sort)
    uyxht__sva = dict(result_name=None, sort=None)
    check_unsupported_args('Index.symmetric_difference', tsp__ume,
        uyxht__sva, package_name='pandas', module_name='Index')
    _verify_setop_compatible('symmetric_difference', I, other)
    ilr__pck = get_index_constructor(I) if not isinstance(I, RangeIndexType
        ) else init_numeric_index

    def impl(I, other, result_name=None, sort=None):
        bbu__guww = bodo.utils.conversion.coerce_to_array(I)
        btptn__tgfxs = bodo.utils.conversion.coerce_to_array(other)
        vbjh__oqw = bodo.libs.array_kernels.unique(bbu__guww)
        qmukf__uqpn = bodo.libs.array_kernels.unique(btptn__tgfxs)
        irxr__qol = np.empty(len(vbjh__oqw), np.bool_)
        lwcgd__dzmlu = np.empty(len(qmukf__uqpn), np.bool_)
        bodo.libs.array.array_isin(irxr__qol, vbjh__oqw, qmukf__uqpn, False)
        bodo.libs.array.array_isin(lwcgd__dzmlu, qmukf__uqpn, vbjh__oqw, False)
        rwdu__iocr = bodo.libs.array_kernels.concat([vbjh__oqw[~irxr__qol],
            qmukf__uqpn[~lwcgd__dzmlu]])
        return ilr__pck(rwdu__iocr, None)
    return impl


@overload_method(RangeIndexType, 'take', no_unliteral=True)
@overload_method(NumericIndexType, 'take', no_unliteral=True)
@overload_method(StringIndexType, 'take', no_unliteral=True)
@overload_method(BinaryIndexType, 'take', no_unliteral=True)
@overload_method(CategoricalIndexType, 'take', no_unliteral=True)
@overload_method(PeriodIndexType, 'take', no_unliteral=True)
@overload_method(DatetimeIndexType, 'take', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'take', no_unliteral=True)
def overload_index_take(I, indices, axis=0, allow_fill=True, fill_value=None):
    tsp__ume = dict(axis=axis, allow_fill=allow_fill, fill_value=fill_value)
    uyxht__sva = dict(axis=0, allow_fill=True, fill_value=None)
    check_unsupported_args('Index.take', tsp__ume, uyxht__sva, package_name
        ='pandas', module_name='Index')
    return lambda I, indices: I[indices]


def _init_engine(I, ban_unique=True):
    pass


@overload(_init_engine)
def overload_init_engine(I, ban_unique=True):
    if isinstance(I, CategoricalIndexType):

        def impl(I, ban_unique=True):
            if len(I) > 0 and not I._dict:
                abph__hoc = bodo.utils.conversion.coerce_to_array(I)
                for i in range(len(abph__hoc)):
                    if not bodo.libs.array_kernels.isna(abph__hoc, i):
                        val = (bodo.hiframes.pd_categorical_ext.
                            get_code_for_value(abph__hoc.dtype, abph__hoc[i]))
                        if ban_unique and val in I._dict:
                            raise ValueError(
                                'Index.get_loc(): non-unique Index not supported yet'
                                )
                        I._dict[val] = i
        return impl
    else:

        def impl(I, ban_unique=True):
            if len(I) > 0 and not I._dict:
                abph__hoc = bodo.utils.conversion.coerce_to_array(I)
                for i in range(len(abph__hoc)):
                    if not bodo.libs.array_kernels.isna(abph__hoc, i):
                        val = abph__hoc[i]
                        if ban_unique and val in I._dict:
                            raise ValueError(
                                'Index.get_loc(): non-unique Index not supported yet'
                                )
                        I._dict[val] = i
        return impl


@overload(operator.contains, no_unliteral=True)
def index_contains(I, val):
    if not is_index_type(I):
        return
    if isinstance(I, RangeIndexType):
        return lambda I, val: range_contains(I.start, I.stop, I.step, val)
    if isinstance(I, CategoricalIndexType):

        def impl(I, val):
            key = bodo.utils.conversion.unbox_if_tz_naive_timestamp(val)
            if not is_null_value(I._dict):
                _init_engine(I, False)
                abph__hoc = bodo.utils.conversion.coerce_to_array(I)
                utooa__opde = (bodo.hiframes.pd_categorical_ext.
                    get_code_for_value(abph__hoc.dtype, key))
                return utooa__opde in I._dict
            else:
                rups__dsy = (
                    'Global Index objects can be slow (pass as argument to JIT function for better performance).'
                    )
                warnings.warn(rups__dsy)
                abph__hoc = bodo.utils.conversion.coerce_to_array(I)
                ind = -1
                for i in range(len(abph__hoc)):
                    if not bodo.libs.array_kernels.isna(abph__hoc, i):
                        if abph__hoc[i] == key:
                            ind = i
            return ind != -1
        return impl

    def impl(I, val):
        key = bodo.utils.conversion.unbox_if_tz_naive_timestamp(val)
        if not is_null_value(I._dict):
            _init_engine(I, False)
            return key in I._dict
        else:
            rups__dsy = (
                'Global Index objects can be slow (pass as argument to JIT function for better performance).'
                )
            warnings.warn(rups__dsy)
            abph__hoc = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(abph__hoc)):
                if not bodo.libs.array_kernels.isna(abph__hoc, i):
                    if abph__hoc[i] == key:
                        ind = i
        return ind != -1
    return impl


@register_jitable
def range_contains(start, stop, step, val):
    if step > 0 and not start <= val < stop:
        return False
    if step < 0 and not stop <= val < start:
        return False
    return (val - start) % step == 0


@overload_method(RangeIndexType, 'get_loc', no_unliteral=True)
@overload_method(NumericIndexType, 'get_loc', no_unliteral=True)
@overload_method(StringIndexType, 'get_loc', no_unliteral=True)
@overload_method(BinaryIndexType, 'get_loc', no_unliteral=True)
@overload_method(PeriodIndexType, 'get_loc', no_unliteral=True)
@overload_method(DatetimeIndexType, 'get_loc', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'get_loc', no_unliteral=True)
def overload_index_get_loc(I, key, method=None, tolerance=None):
    tsp__ume = dict(method=method, tolerance=tolerance)
    ugzcb__bvng = dict(method=None, tolerance=None)
    check_unsupported_args('Index.get_loc', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')
    key = types.unliteral(key)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'DatetimeIndex.get_loc')
    if key == pd_timestamp_tz_naive_type:
        key = bodo.datetime64ns
    if key == pd_timedelta_type:
        key = bodo.timedelta64ns
    if key != I.dtype:
        raise_bodo_error(
            'Index.get_loc(): invalid label type in Index.get_loc()')
    if isinstance(I, RangeIndexType):

        def impl_range(I, key, method=None, tolerance=None):
            if not range_contains(I.start, I.stop, I.step, key):
                raise KeyError('Index.get_loc(): key not found')
            return key - I.start if I.step == 1 else (key - I.start) // I.step
        return impl_range

    def impl(I, key, method=None, tolerance=None):
        key = bodo.utils.conversion.unbox_if_tz_naive_timestamp(key)
        if not is_null_value(I._dict):
            _init_engine(I)
            ind = I._dict.get(key, -1)
        else:
            rups__dsy = (
                'Index.get_loc() can be slow for global Index objects (pass as argument to JIT function for better performance).'
                )
            warnings.warn(rups__dsy)
            abph__hoc = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(abph__hoc)):
                if abph__hoc[i] == key:
                    if ind != -1:
                        raise ValueError(
                            'Index.get_loc(): non-unique Index not supported yet'
                            )
                    ind = i
        if ind == -1:
            raise KeyError('Index.get_loc(): key not found')
        return ind
    return impl


def create_isna_specific_method(overload_name):

    def overload_index_isna_specific_method(I):
        xcq__wbv = overload_name in {'isna', 'isnull'}
        if isinstance(I, RangeIndexType):

            def impl(I):
                numba.parfors.parfor.init_prange()
                svaxh__xlacb = len(I)
                fjhb__zrn = np.empty(svaxh__xlacb, np.bool_)
                for i in numba.parfors.parfor.internal_prange(svaxh__xlacb):
                    fjhb__zrn[i] = not xcq__wbv
                return fjhb__zrn
            return impl
        abd__wuyu = f"""def impl(I):
    numba.parfors.parfor.init_prange()
    arr = bodo.hiframes.pd_index_ext.get_index_data(I)
    n = len(arr)
    out_arr = np.empty(n, np.bool_)
    for i in numba.parfors.parfor.internal_prange(n):
       out_arr[i] = {'' if xcq__wbv else 'not '}bodo.libs.array_kernels.isna(arr, i)
    return out_arr
"""
        aha__iwa = {}
        exec(abd__wuyu, {'bodo': bodo, 'np': np, 'numba': numba}, aha__iwa)
        impl = aha__iwa['impl']
        return impl
    return overload_index_isna_specific_method


isna_overload_types = (RangeIndexType, NumericIndexType, StringIndexType,
    BinaryIndexType, CategoricalIndexType, PeriodIndexType,
    DatetimeIndexType, TimedeltaIndexType)
isna_specific_methods = 'isna', 'notna', 'isnull', 'notnull'


def _install_isna_specific_methods():
    for osj__hkpi in isna_overload_types:
        for overload_name in isna_specific_methods:
            overload_impl = create_isna_specific_method(overload_name)
            overload_method(osj__hkpi, overload_name, no_unliteral=True,
                inline='always')(overload_impl)


_install_isna_specific_methods()


@overload_attribute(RangeIndexType, 'values')
@overload_attribute(NumericIndexType, 'values')
@overload_attribute(StringIndexType, 'values')
@overload_attribute(BinaryIndexType, 'values')
@overload_attribute(CategoricalIndexType, 'values')
@overload_attribute(PeriodIndexType, 'values')
@overload_attribute(DatetimeIndexType, 'values')
@overload_attribute(TimedeltaIndexType, 'values')
def overload_values(I):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I, 'Index.values'
        )
    return lambda I: bodo.utils.conversion.coerce_to_array(I)


@overload(len, no_unliteral=True)
def overload_index_len(I):
    if isinstance(I, (NumericIndexType, StringIndexType, BinaryIndexType,
        PeriodIndexType, IntervalIndexType, CategoricalIndexType,
        DatetimeIndexType, TimedeltaIndexType, HeterogeneousIndexType)):
        return lambda I: len(bodo.hiframes.pd_index_ext.get_index_data(I))


@overload(len, no_unliteral=True)
def overload_multi_index_len(I):
    if isinstance(I, MultiIndexType):
        return lambda I: len(bodo.hiframes.pd_index_ext.get_index_data(I)[0])


@overload_attribute(DatetimeIndexType, 'shape')
@overload_attribute(NumericIndexType, 'shape')
@overload_attribute(StringIndexType, 'shape')
@overload_attribute(BinaryIndexType, 'shape')
@overload_attribute(PeriodIndexType, 'shape')
@overload_attribute(TimedeltaIndexType, 'shape')
@overload_attribute(IntervalIndexType, 'shape')
@overload_attribute(CategoricalIndexType, 'shape')
def overload_index_shape(s):
    return lambda s: (len(bodo.hiframes.pd_index_ext.get_index_data(s)),)


@overload_attribute(RangeIndexType, 'shape')
def overload_range_index_shape(s):
    return lambda s: (len(s),)


@overload_attribute(MultiIndexType, 'shape')
def overload_index_shape(s):
    return lambda s: (len(bodo.hiframes.pd_index_ext.get_index_data(s)[0]),)


@overload_attribute(NumericIndexType, 'is_monotonic', inline='always')
@overload_attribute(RangeIndexType, 'is_monotonic', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic', inline='always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic', inline='always')
@overload_attribute(NumericIndexType, 'is_monotonic_increasing', inline=
    'always')
@overload_attribute(RangeIndexType, 'is_monotonic_increasing', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic_increasing', inline=
    'always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic_increasing', inline=
    'always')
def overload_index_is_montonic(I):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.is_monotonic_increasing')
    if isinstance(I, (NumericIndexType, DatetimeIndexType, TimedeltaIndexType)
        ):

        def impl(I):
            abph__hoc = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(abph__hoc, 1)
        return impl
    elif isinstance(I, RangeIndexType):

        def impl(I):
            return I._step > 0 or len(I) <= 1
        return impl


@overload_attribute(NumericIndexType, 'is_monotonic_decreasing', inline=
    'always')
@overload_attribute(RangeIndexType, 'is_monotonic_decreasing', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic_decreasing', inline=
    'always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic_decreasing', inline=
    'always')
def overload_index_is_montonic_decreasing(I):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.is_monotonic_decreasing')
    if isinstance(I, (NumericIndexType, DatetimeIndexType, TimedeltaIndexType)
        ):

        def impl(I):
            abph__hoc = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(abph__hoc, 2)
        return impl
    elif isinstance(I, RangeIndexType):

        def impl(I):
            return I._step < 0 or len(I) <= 1
        return impl


@overload_method(NumericIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(DatetimeIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(TimedeltaIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(StringIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(PeriodIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(CategoricalIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(BinaryIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(RangeIndexType, 'duplicated', inline='always',
    no_unliteral=True)
def overload_index_duplicated(I, keep='first'):
    if isinstance(I, RangeIndexType):

        def impl(I, keep='first'):
            return np.zeros(len(I), np.bool_)
        return impl

    def impl(I, keep='first'):
        abph__hoc = bodo.hiframes.pd_index_ext.get_index_data(I)
        fjhb__zrn = bodo.libs.array_kernels.duplicated((abph__hoc,))
        return fjhb__zrn
    return impl


@overload_method(NumericIndexType, 'any', no_unliteral=True, inline='always')
@overload_method(StringIndexType, 'any', no_unliteral=True, inline='always')
@overload_method(BinaryIndexType, 'any', no_unliteral=True, inline='always')
@overload_method(RangeIndexType, 'any', no_unliteral=True, inline='always')
def overload_index_any(I):
    if isinstance(I, RangeIndexType):

        def impl(I):
            return len(I) > 0 and (I._start != 0 or len(I) > 1)
        return impl

    def impl(I):
        A = bodo.hiframes.pd_index_ext.get_index_data(I)
        return bodo.libs.array_ops.array_op_any(A)
    return impl


@overload_method(NumericIndexType, 'all', no_unliteral=True, inline='always')
@overload_method(StringIndexType, 'all', no_unliteral=True, inline='always')
@overload_method(RangeIndexType, 'all', no_unliteral=True, inline='always')
@overload_method(BinaryIndexType, 'all', no_unliteral=True, inline='always')
def overload_index_all(I):
    if isinstance(I, RangeIndexType):

        def impl(I):
            return len(I) == 0 or I._step > 0 and (I._start > 0 or I._stop <= 0
                ) or I._step < 0 and (I._start < 0 or I._stop >= 0
                ) or I._start % I._step != 0
        return impl

    def impl(I):
        A = bodo.hiframes.pd_index_ext.get_index_data(I)
        return bodo.libs.array_ops.array_op_all(A)
    return impl


@overload_method(RangeIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(NumericIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(StringIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(BinaryIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(CategoricalIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(PeriodIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(DatetimeIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(TimedeltaIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
def overload_index_drop_duplicates(I, keep='first'):
    tsp__ume = dict(keep=keep)
    ugzcb__bvng = dict(keep='first')
    check_unsupported_args('Index.drop_duplicates', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):
        return lambda I, keep='first': I.copy()
    abd__wuyu = """def impl(I, keep='first'):
    data = bodo.hiframes.pd_index_ext.get_index_data(I)
    arr = bodo.libs.array_kernels.drop_duplicates_array(data)
    name = bodo.hiframes.pd_index_ext.get_index_name(I)
"""
    if isinstance(I, PeriodIndexType):
        abd__wuyu += f"""    return bodo.hiframes.pd_index_ext.init_period_index(arr, name, '{I.freq}')
"""
    else:
        abd__wuyu += (
            '    return bodo.utils.conversion.index_from_array(arr, name)')
    aha__iwa = {}
    exec(abd__wuyu, {'bodo': bodo}, aha__iwa)
    impl = aha__iwa['impl']
    return impl


@numba.generated_jit(nopython=True)
def get_index_data(S):
    return lambda S: S._data


@numba.generated_jit(nopython=True)
def get_index_name(S):
    return lambda S: S._name


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_index_data',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_datetime_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_timedelta_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_numeric_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_binary_str_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_categorical_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func


def get_index_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    yky__icyoj = args[0]
    if isinstance(self.typemap[yky__icyoj.name], (HeterogeneousIndexType,
        MultiIndexType)):
        return None
    if equiv_set.has_shape(yky__icyoj):
        return ArrayAnalysis.AnalyzeResult(shape=yky__icyoj, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_get_index_data
    ) = get_index_data_equiv


@overload_method(RangeIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(NumericIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(StringIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(BinaryIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(CategoricalIndexType, 'map', inline='always', no_unliteral
    =True)
@overload_method(PeriodIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(DatetimeIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'map', inline='always', no_unliteral=True)
def overload_index_map(I, mapper, na_action=None):
    if not is_const_func_type(mapper):
        raise BodoError("Index.map(): 'mapper' should be a function")
    tsp__ume = dict(na_action=na_action)
    htgbu__qrj = dict(na_action=None)
    check_unsupported_args('Index.map', tsp__ume, htgbu__qrj, package_name=
        'pandas', module_name='Index')
    dtype = I.dtype
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'DatetimeIndex.map')
    if dtype == types.NPDatetime('ns'):
        dtype = pd_timestamp_tz_naive_type
    if dtype == types.NPTimedelta('ns'):
        dtype = pd_timedelta_type
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = dtype.elem_type
    taqs__eefij = numba.core.registry.cpu_target.typing_context
    cdiaa__oarhn = numba.core.registry.cpu_target.target_context
    try:
        wptr__ivq = get_const_func_output_type(mapper, (dtype,), {},
            taqs__eefij, cdiaa__oarhn)
    except Exception as frgv__kcl:
        raise_bodo_error(get_udf_error_msg('Index.map()', frgv__kcl))
    vlj__kva = get_udf_out_arr_type(wptr__ivq)
    func = get_overload_const_func(mapper, None)
    abd__wuyu = 'def f(I, mapper, na_action=None):\n'
    abd__wuyu += '  name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    abd__wuyu += '  A = bodo.utils.conversion.coerce_to_array(I)\n'
    abd__wuyu += '  numba.parfors.parfor.init_prange()\n'
    abd__wuyu += '  n = len(A)\n'
    abd__wuyu += '  S = bodo.utils.utils.alloc_type(n, _arr_typ, (-1,))\n'
    abd__wuyu += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    abd__wuyu += '    t2 = bodo.utils.conversion.box_if_dt64(A[i])\n'
    abd__wuyu += '    v = map_func(t2)\n'
    abd__wuyu += (
        '    S[i] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(v)\n')
    abd__wuyu += '  return bodo.utils.conversion.index_from_array(S, name)\n'
    jigq__ipa = bodo.compiler.udf_jit(func)
    aha__iwa = {}
    exec(abd__wuyu, {'numba': numba, 'np': np, 'pd': pd, 'bodo': bodo,
        'map_func': jigq__ipa, '_arr_typ': vlj__kva, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'data_arr_type': vlj__kva.dtype},
        aha__iwa)
    f = aha__iwa['f']
    return f


@lower_builtin(operator.is_, NumericIndexType, NumericIndexType)
@lower_builtin(operator.is_, StringIndexType, StringIndexType)
@lower_builtin(operator.is_, BinaryIndexType, BinaryIndexType)
@lower_builtin(operator.is_, PeriodIndexType, PeriodIndexType)
@lower_builtin(operator.is_, DatetimeIndexType, DatetimeIndexType)
@lower_builtin(operator.is_, TimedeltaIndexType, TimedeltaIndexType)
@lower_builtin(operator.is_, IntervalIndexType, IntervalIndexType)
@lower_builtin(operator.is_, CategoricalIndexType, CategoricalIndexType)
def index_is(context, builder, sig, args):
    ena__ifm, wpk__gjf = sig.args
    if ena__ifm != wpk__gjf:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return a._data is b._data and a._name is b._name
    return context.compile_internal(builder, index_is_impl, sig, args)


@lower_builtin(operator.is_, RangeIndexType, RangeIndexType)
def range_index_is(context, builder, sig, args):
    ena__ifm, wpk__gjf = sig.args
    if ena__ifm != wpk__gjf:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._start == b._start and a._stop == b._stop and a._step ==
            b._step and a._name is b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)


def create_binary_op_overload(op):

    def overload_index_binary_op(lhs, rhs):
        if is_index_type(lhs):
            abd__wuyu = (
                'def impl(lhs, rhs):\n  arr = bodo.utils.conversion.coerce_to_array(lhs)\n'
                )
            if rhs in [bodo.hiframes.pd_timestamp_ext.
                pd_timestamp_tz_naive_type, bodo.hiframes.pd_timestamp_ext.
                pd_timedelta_type]:
                abd__wuyu += """  dt = bodo.utils.conversion.unbox_if_tz_naive_timestamp(rhs)
  return op(arr, dt)
"""
            else:
                abd__wuyu += """  rhs_arr = bodo.utils.conversion.get_array_if_series_or_index(rhs)
  return op(arr, rhs_arr)
"""
            aha__iwa = {}
            exec(abd__wuyu, {'bodo': bodo, 'op': op}, aha__iwa)
            impl = aha__iwa['impl']
            return impl
        if is_index_type(rhs):
            abd__wuyu = (
                'def impl(lhs, rhs):\n  arr = bodo.utils.conversion.coerce_to_array(rhs)\n'
                )
            if lhs in [bodo.hiframes.pd_timestamp_ext.
                pd_timestamp_tz_naive_type, bodo.hiframes.pd_timestamp_ext.
                pd_timedelta_type]:
                abd__wuyu += """  dt = bodo.utils.conversion.unbox_if_tz_naive_timestamp(lhs)
  return op(dt, arr)
"""
            else:
                abd__wuyu += """  lhs_arr = bodo.utils.conversion.get_array_if_series_or_index(lhs)
  return op(lhs_arr, arr)
"""
            aha__iwa = {}
            exec(abd__wuyu, {'bodo': bodo, 'op': op}, aha__iwa)
            impl = aha__iwa['impl']
            return impl
        if isinstance(lhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(lhs.data):

                def impl3(lhs, rhs):
                    data = bodo.utils.conversion.coerce_to_array(lhs)
                    abph__hoc = bodo.utils.conversion.coerce_to_array(data)
                    codc__npc = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    fjhb__zrn = op(abph__hoc, codc__npc)
                    return fjhb__zrn
                return impl3
            count = len(lhs.data.types)
            abd__wuyu = 'def f(lhs, rhs):\n'
            abd__wuyu += '  return [{}]\n'.format(','.join(
                'op(lhs[{}], rhs{})'.format(i, f'[{i}]' if is_iterable_type
                (rhs) else '') for i in range(count)))
            aha__iwa = {}
            exec(abd__wuyu, {'op': op, 'np': np}, aha__iwa)
            impl = aha__iwa['f']
            return impl
        if isinstance(rhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(rhs.data):

                def impl4(lhs, rhs):
                    data = bodo.hiframes.pd_index_ext.get_index_data(rhs)
                    abph__hoc = bodo.utils.conversion.coerce_to_array(data)
                    codc__npc = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    fjhb__zrn = op(codc__npc, abph__hoc)
                    return fjhb__zrn
                return impl4
            count = len(rhs.data.types)
            abd__wuyu = 'def f(lhs, rhs):\n'
            abd__wuyu += '  return [{}]\n'.format(','.join(
                'op(lhs{}, rhs[{}])'.format(f'[{i}]' if is_iterable_type(
                lhs) else '', i) for i in range(count)))
            aha__iwa = {}
            exec(abd__wuyu, {'op': op, 'np': np}, aha__iwa)
            impl = aha__iwa['f']
            return impl
    return overload_index_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        overload_impl = create_binary_op_overload(op)
        overload(op, inline='always')(overload_impl)


_install_binary_ops()


def is_index_type(t):
    return isinstance(t, (RangeIndexType, NumericIndexType, StringIndexType,
        BinaryIndexType, PeriodIndexType, DatetimeIndexType,
        TimedeltaIndexType, IntervalIndexType, CategoricalIndexType))


@lower_cast(RangeIndexType, NumericIndexType)
def cast_range_index_to_int_index(context, builder, fromty, toty, val):
    f = lambda I: init_numeric_index(np.arange(I._start, I._stop, I._step),
        bodo.hiframes.pd_index_ext.get_index_name(I))
    return context.compile_internal(builder, f, toty(fromty), [val])


@numba.njit(no_cpython_wrapper=True)
def range_index_to_numeric(I):
    return init_numeric_index(np.arange(I._start, I._stop, I._step), bodo.
        hiframes.pd_index_ext.get_index_name(I))


class HeterogeneousIndexType(types.Type):
    ndim = 1

    def __init__(self, data=None, name_typ=None):
        self.data = data
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        super(HeterogeneousIndexType, self).__init__(name=
            f'heter_index({data}, {name_typ})')

    def copy(self):
        return HeterogeneousIndexType(self.data, self.name_typ)

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return 'object'


@register_model(HeterogeneousIndexType)
class HeterogeneousIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ofgt__msmd = [('data', fe_type.data), ('name', fe_type.name_typ)]
        super(HeterogeneousIndexModel, self).__init__(dmm, fe_type, ofgt__msmd)


make_attribute_wrapper(HeterogeneousIndexType, 'data', '_data')
make_attribute_wrapper(HeterogeneousIndexType, 'name', '_name')


@overload_method(HeterogeneousIndexType, 'copy', no_unliteral=True)
def overload_heter_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    yng__jtz = idx_typ_to_format_str_map[HeterogeneousIndexType].format(
        'copy()')
    amisc__pgijx = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', amisc__pgijx, idx_cpy_arg_defaults,
        fn_str=yng__jtz, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), A._name)
    return impl


@box(HeterogeneousIndexType)
def box_heter_index(typ, val, c):
    nrttr__ydfyo = c.context.insert_const_string(c.builder.module, 'pandas')
    fjoss__ibn = c.pyapi.import_module_noblock(nrttr__ydfyo)
    qizmc__fib = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, qizmc__fib.data)
    bpaja__qmng = c.pyapi.from_native_value(typ.data, qizmc__fib.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, qizmc__fib.name)
    qwh__ohiqx = c.pyapi.from_native_value(typ.name_typ, qizmc__fib.name, c
        .env_manager)
    nrx__csi = c.pyapi.make_none()
    hhds__mfxwk = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    zlk__psqx = c.pyapi.call_method(fjoss__ibn, 'Index', (bpaja__qmng,
        nrx__csi, hhds__mfxwk, qwh__ohiqx))
    c.pyapi.decref(bpaja__qmng)
    c.pyapi.decref(nrx__csi)
    c.pyapi.decref(hhds__mfxwk)
    c.pyapi.decref(qwh__ohiqx)
    c.pyapi.decref(fjoss__ibn)
    c.context.nrt.decref(c.builder, typ, val)
    return zlk__psqx


@intrinsic
def init_heter_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        cdlf__hqhf = signature.return_type
        qizmc__fib = cgutils.create_struct_proxy(cdlf__hqhf)(context, builder)
        qizmc__fib.data = args[0]
        qizmc__fib.name = args[1]
        context.nrt.incref(builder, cdlf__hqhf.data, args[0])
        context.nrt.incref(builder, cdlf__hqhf.name_typ, args[1])
        return qizmc__fib._getvalue()
    return HeterogeneousIndexType(data, name)(data, name), codegen


@overload_attribute(HeterogeneousIndexType, 'name')
def heter_index_get_name(i):

    def impl(i):
        return i._name
    return impl


@overload_attribute(NumericIndexType, 'nbytes')
@overload_attribute(DatetimeIndexType, 'nbytes')
@overload_attribute(TimedeltaIndexType, 'nbytes')
@overload_attribute(RangeIndexType, 'nbytes')
@overload_attribute(StringIndexType, 'nbytes')
@overload_attribute(BinaryIndexType, 'nbytes')
@overload_attribute(CategoricalIndexType, 'nbytes')
@overload_attribute(PeriodIndexType, 'nbytes')
@overload_attribute(MultiIndexType, 'nbytes')
def overload_nbytes(I):
    if isinstance(I, RangeIndexType):

        def _impl_nbytes(I):
            return bodo.io.np_io.get_dtype_size(type(I._start)
                ) + bodo.io.np_io.get_dtype_size(type(I._step)
                ) + bodo.io.np_io.get_dtype_size(type(I._stop))
        return _impl_nbytes
    elif isinstance(I, MultiIndexType):
        abd__wuyu = 'def _impl_nbytes(I):\n'
        abd__wuyu += '    total = 0\n'
        abd__wuyu += '    data = I._data\n'
        for i in range(I.nlevels):
            abd__wuyu += f'    total += data[{i}].nbytes\n'
        abd__wuyu += '    return total\n'
        uezwe__cyvz = {}
        exec(abd__wuyu, {}, uezwe__cyvz)
        return uezwe__cyvz['_impl_nbytes']
    else:

        def _impl_nbytes(I):
            return I._data.nbytes
        return _impl_nbytes


@overload_method(NumericIndexType, 'to_series', inline='always')
@overload_method(DatetimeIndexType, 'to_series', inline='always')
@overload_method(TimedeltaIndexType, 'to_series', inline='always')
@overload_method(RangeIndexType, 'to_series', inline='always')
@overload_method(StringIndexType, 'to_series', inline='always')
@overload_method(BinaryIndexType, 'to_series', inline='always')
@overload_method(CategoricalIndexType, 'to_series', inline='always')
def overload_index_to_series(I, index=None, name=None):
    if not (is_overload_constant_str(name) or is_overload_constant_int(name
        ) or is_overload_none(name)):
        raise_bodo_error(
            f'Index.to_series(): only constant string/int are supported for argument name'
            )
    if is_overload_none(name):
        pxcx__wzus = 'bodo.hiframes.pd_index_ext.get_index_name(I)'
    else:
        pxcx__wzus = 'name'
    abd__wuyu = 'def impl(I, index=None, name=None):\n'
    abd__wuyu += '    data = bodo.utils.conversion.index_to_array(I)\n'
    if is_overload_none(index):
        abd__wuyu += '    new_index = I\n'
    elif is_pd_index_type(index):
        abd__wuyu += '    new_index = index\n'
    elif isinstance(index, SeriesType):
        abd__wuyu += '    arr = bodo.utils.conversion.coerce_to_array(index)\n'
        abd__wuyu += (
            '    index_name = bodo.hiframes.pd_series_ext.get_series_name(index)\n'
            )
        abd__wuyu += (
            '    new_index = bodo.utils.conversion.index_from_array(arr, index_name)\n'
            )
    elif bodo.utils.utils.is_array_typ(index, False):
        abd__wuyu += (
            '    new_index = bodo.utils.conversion.index_from_array(index)\n')
    elif isinstance(index, (types.List, types.BaseTuple)):
        abd__wuyu += '    arr = bodo.utils.conversion.coerce_to_array(index)\n'
        abd__wuyu += (
            '    new_index = bodo.utils.conversion.index_from_array(arr)\n')
    else:
        raise_bodo_error(
            f'Index.to_series(): unsupported type for argument index: {type(index).__name__}'
            )
    abd__wuyu += f'    new_name = {pxcx__wzus}\n'
    abd__wuyu += (
        '    return bodo.hiframes.pd_series_ext.init_series(data, new_index, new_name)'
        )
    aha__iwa = {}
    exec(abd__wuyu, {'bodo': bodo, 'np': np}, aha__iwa)
    impl = aha__iwa['impl']
    return impl


@overload_method(NumericIndexType, 'to_frame', inline='always',
    no_unliteral=True)
@overload_method(DatetimeIndexType, 'to_frame', inline='always',
    no_unliteral=True)
@overload_method(TimedeltaIndexType, 'to_frame', inline='always',
    no_unliteral=True)
@overload_method(RangeIndexType, 'to_frame', inline='always', no_unliteral=True
    )
@overload_method(StringIndexType, 'to_frame', inline='always', no_unliteral
    =True)
@overload_method(BinaryIndexType, 'to_frame', inline='always', no_unliteral
    =True)
@overload_method(CategoricalIndexType, 'to_frame', inline='always',
    no_unliteral=True)
def overload_index_to_frame(I, index=True, name=None):
    if is_overload_true(index):
        nruo__opyw = 'I'
    elif is_overload_false(index):
        nruo__opyw = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(I), 1, None)')
    elif not isinstance(index, types.Boolean):
        raise_bodo_error(
            'Index.to_frame(): index argument must be a constant boolean')
    else:
        raise_bodo_error(
            'Index.to_frame(): index argument must be a compile time constant')
    abd__wuyu = 'def impl(I, index=True, name=None):\n'
    abd__wuyu += '    data = bodo.utils.conversion.index_to_array(I)\n'
    abd__wuyu += f'    new_index = {nruo__opyw}\n'
    if is_overload_none(name) and I.name_typ == types.none:
        cmn__vynbr = ColNamesMetaType((0,))
    elif is_overload_none(name):
        cmn__vynbr = ColNamesMetaType((I.name_typ,))
    elif is_overload_constant_str(name):
        cmn__vynbr = ColNamesMetaType((get_overload_const_str(name),))
    elif is_overload_constant_int(name):
        cmn__vynbr = ColNamesMetaType((get_overload_const_int(name),))
    else:
        raise_bodo_error(
            f'Index.to_frame(): only constant string/int are supported for argument name'
            )
    abd__wuyu += """    return bodo.hiframes.pd_dataframe_ext.init_dataframe((data,), new_index, __col_name_meta_value)
"""
    aha__iwa = {}
    exec(abd__wuyu, {'bodo': bodo, 'np': np, '__col_name_meta_value':
        cmn__vynbr}, aha__iwa)
    impl = aha__iwa['impl']
    return impl


@overload_method(MultiIndexType, 'to_frame', inline='always', no_unliteral=True
    )
def overload_multi_index_to_frame(I, index=True, name=None):
    if is_overload_true(index):
        nruo__opyw = 'I'
    elif is_overload_false(index):
        nruo__opyw = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(I), 1, None)')
    elif not isinstance(index, types.Boolean):
        raise_bodo_error(
            'MultiIndex.to_frame(): index argument must be a constant boolean')
    else:
        raise_bodo_error(
            'MultiIndex.to_frame(): index argument must be a compile time constant'
            )
    abd__wuyu = 'def impl(I, index=True, name=None):\n'
    abd__wuyu += '    data = bodo.hiframes.pd_index_ext.get_index_data(I)\n'
    abd__wuyu += f'    new_index = {nruo__opyw}\n'
    ubvjl__cujgi = len(I.array_types)
    if is_overload_none(name) and I.names_typ == (types.none,) * ubvjl__cujgi:
        cmn__vynbr = ColNamesMetaType(tuple(range(ubvjl__cujgi)))
    elif is_overload_none(name):
        cmn__vynbr = ColNamesMetaType(I.names_typ)
    elif is_overload_constant_tuple(name) or is_overload_constant_list(name):
        if is_overload_constant_list(name):
            names = tuple(get_overload_const_list(name))
        else:
            names = get_overload_const_tuple(name)
        if ubvjl__cujgi != len(names):
            raise_bodo_error(
                f'MultiIndex.to_frame(): expected {ubvjl__cujgi} names, not {len(names)}'
                )
        if all(is_overload_constant_str(uijs__anjt) or
            is_overload_constant_int(uijs__anjt) for uijs__anjt in names):
            cmn__vynbr = ColNamesMetaType(names)
        else:
            raise_bodo_error(
                'MultiIndex.to_frame(): only constant string/int list/tuple are supported for argument name'
                )
    else:
        raise_bodo_error(
            'MultiIndex.to_frame(): only constant string/int list/tuple are supported for argument name'
            )
    abd__wuyu += """    return bodo.hiframes.pd_dataframe_ext.init_dataframe(data, new_index, __col_name_meta_value,)
"""
    aha__iwa = {}
    exec(abd__wuyu, {'bodo': bodo, 'np': np, '__col_name_meta_value':
        cmn__vynbr}, aha__iwa)
    impl = aha__iwa['impl']
    return impl


@overload_method(NumericIndexType, 'to_numpy', inline='always')
@overload_method(DatetimeIndexType, 'to_numpy', inline='always')
@overload_method(TimedeltaIndexType, 'to_numpy', inline='always')
@overload_method(RangeIndexType, 'to_numpy', inline='always')
@overload_method(StringIndexType, 'to_numpy', inline='always')
@overload_method(BinaryIndexType, 'to_numpy', inline='always')
@overload_method(CategoricalIndexType, 'to_numpy', inline='always')
@overload_method(IntervalIndexType, 'to_numpy', inline='always')
def overload_index_to_numpy(I, dtype=None, copy=False, na_value=None):
    tsp__ume = dict(dtype=dtype, na_value=na_value)
    ugzcb__bvng = dict(dtype=None, na_value=None)
    check_unsupported_args('Index.to_numpy', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')
    if not is_overload_bool(copy):
        raise_bodo_error('Index.to_numpy(): copy argument must be a boolean')
    if isinstance(I, RangeIndexType):

        def impl(I, dtype=None, copy=False, na_value=None):
            return np.arange(I._start, I._stop, I._step)
        return impl
    if is_overload_true(copy):

        def impl(I, dtype=None, copy=False, na_value=None):
            return bodo.hiframes.pd_index_ext.get_index_data(I).copy()
        return impl
    if is_overload_false(copy):

        def impl(I, dtype=None, copy=False, na_value=None):
            return bodo.hiframes.pd_index_ext.get_index_data(I)
        return impl

    def impl(I, dtype=None, copy=False, na_value=None):
        data = bodo.hiframes.pd_index_ext.get_index_data(I)
        return data.copy() if copy else data
    return impl


@overload_method(NumericIndexType, 'to_list', inline='always')
@overload_method(RangeIndexType, 'to_list', inline='always')
@overload_method(StringIndexType, 'to_list', inline='always')
@overload_method(BinaryIndexType, 'to_list', inline='always')
@overload_method(CategoricalIndexType, 'to_list', inline='always')
@overload_method(DatetimeIndexType, 'to_list', inline='always')
@overload_method(TimedeltaIndexType, 'to_list', inline='always')
@overload_method(NumericIndexType, 'tolist', inline='always')
@overload_method(RangeIndexType, 'tolist', inline='always')
@overload_method(StringIndexType, 'tolist', inline='always')
@overload_method(BinaryIndexType, 'tolist', inline='always')
@overload_method(CategoricalIndexType, 'tolist', inline='always')
@overload_method(DatetimeIndexType, 'tolist', inline='always')
@overload_method(TimedeltaIndexType, 'tolist', inline='always')
def overload_index_to_list(I):
    if isinstance(I, RangeIndexType):

        def impl(I):
            zlgq__aaut = list()
            for i in range(I._start, I._stop, I.step):
                zlgq__aaut.append(i)
            return zlgq__aaut
        return impl

    def impl(I):
        zlgq__aaut = list()
        for i in range(len(I)):
            zlgq__aaut.append(I[i])
        return zlgq__aaut
    return impl


@overload_attribute(NumericIndexType, 'T')
@overload_attribute(DatetimeIndexType, 'T')
@overload_attribute(TimedeltaIndexType, 'T')
@overload_attribute(RangeIndexType, 'T')
@overload_attribute(StringIndexType, 'T')
@overload_attribute(BinaryIndexType, 'T')
@overload_attribute(CategoricalIndexType, 'T')
@overload_attribute(PeriodIndexType, 'T')
@overload_attribute(MultiIndexType, 'T')
@overload_attribute(IntervalIndexType, 'T')
def overload_T(I):
    return lambda I: I


@overload_attribute(NumericIndexType, 'size')
@overload_attribute(DatetimeIndexType, 'size')
@overload_attribute(TimedeltaIndexType, 'size')
@overload_attribute(RangeIndexType, 'size')
@overload_attribute(StringIndexType, 'size')
@overload_attribute(BinaryIndexType, 'size')
@overload_attribute(CategoricalIndexType, 'size')
@overload_attribute(PeriodIndexType, 'size')
@overload_attribute(MultiIndexType, 'size')
@overload_attribute(IntervalIndexType, 'size')
def overload_size(I):
    return lambda I: len(I)


@overload_attribute(NumericIndexType, 'ndim')
@overload_attribute(DatetimeIndexType, 'ndim')
@overload_attribute(TimedeltaIndexType, 'ndim')
@overload_attribute(RangeIndexType, 'ndim')
@overload_attribute(StringIndexType, 'ndim')
@overload_attribute(BinaryIndexType, 'ndim')
@overload_attribute(CategoricalIndexType, 'ndim')
@overload_attribute(PeriodIndexType, 'ndim')
@overload_attribute(MultiIndexType, 'ndim')
@overload_attribute(IntervalIndexType, 'ndim')
def overload_ndim(I):
    return lambda I: 1


@overload_attribute(NumericIndexType, 'nlevels')
@overload_attribute(DatetimeIndexType, 'nlevels')
@overload_attribute(TimedeltaIndexType, 'nlevels')
@overload_attribute(RangeIndexType, 'nlevels')
@overload_attribute(StringIndexType, 'nlevels')
@overload_attribute(BinaryIndexType, 'nlevels')
@overload_attribute(CategoricalIndexType, 'nlevels')
@overload_attribute(PeriodIndexType, 'nlevels')
@overload_attribute(MultiIndexType, 'nlevels')
@overload_attribute(IntervalIndexType, 'nlevels')
def overload_nlevels(I):
    if isinstance(I, MultiIndexType):
        return lambda I: len(I._data)
    return lambda I: 1


@overload_attribute(NumericIndexType, 'empty')
@overload_attribute(DatetimeIndexType, 'empty')
@overload_attribute(TimedeltaIndexType, 'empty')
@overload_attribute(RangeIndexType, 'empty')
@overload_attribute(StringIndexType, 'empty')
@overload_attribute(BinaryIndexType, 'empty')
@overload_attribute(CategoricalIndexType, 'empty')
@overload_attribute(PeriodIndexType, 'empty')
@overload_attribute(MultiIndexType, 'empty')
@overload_attribute(IntervalIndexType, 'empty')
def overload_empty(I):
    return lambda I: len(I) == 0


@overload_attribute(NumericIndexType, 'is_all_dates')
@overload_attribute(DatetimeIndexType, 'is_all_dates')
@overload_attribute(TimedeltaIndexType, 'is_all_dates')
@overload_attribute(RangeIndexType, 'is_all_dates')
@overload_attribute(StringIndexType, 'is_all_dates')
@overload_attribute(BinaryIndexType, 'is_all_dates')
@overload_attribute(CategoricalIndexType, 'is_all_dates')
@overload_attribute(PeriodIndexType, 'is_all_dates')
@overload_attribute(MultiIndexType, 'is_all_dates')
@overload_attribute(IntervalIndexType, 'is_all_dates')
def overload_is_all_dates(I):
    if isinstance(I, (DatetimeIndexType, TimedeltaIndexType, PeriodIndexType)):
        return lambda I: True
    else:
        return lambda I: False


@overload_attribute(NumericIndexType, 'inferred_type')
@overload_attribute(DatetimeIndexType, 'inferred_type')
@overload_attribute(TimedeltaIndexType, 'inferred_type')
@overload_attribute(RangeIndexType, 'inferred_type')
@overload_attribute(StringIndexType, 'inferred_type')
@overload_attribute(BinaryIndexType, 'inferred_type')
@overload_attribute(CategoricalIndexType, 'inferred_type')
@overload_attribute(PeriodIndexType, 'inferred_type')
@overload_attribute(MultiIndexType, 'inferred_type')
@overload_attribute(IntervalIndexType, 'inferred_type')
def overload_inferred_type(I):
    if isinstance(I, NumericIndexType):
        if isinstance(I.dtype, types.Integer):
            return lambda I: 'integer'
        elif isinstance(I.dtype, types.Float):
            return lambda I: 'floating'
        elif isinstance(I.dtype, types.Boolean):
            return lambda I: 'boolean'
        return
    if isinstance(I, StringIndexType):

        def impl(I):
            if len(I._data) == 0:
                return 'empty'
            return 'string'
        return impl
    rxb__zwti = {DatetimeIndexType: 'datetime64', TimedeltaIndexType:
        'timedelta64', RangeIndexType: 'integer', BinaryIndexType: 'bytes',
        CategoricalIndexType: 'categorical', PeriodIndexType: 'period',
        IntervalIndexType: 'interval', MultiIndexType: 'mixed'}
    inferred_type = rxb__zwti[type(I)]
    return lambda I: inferred_type


@overload_attribute(NumericIndexType, 'dtype')
@overload_attribute(DatetimeIndexType, 'dtype')
@overload_attribute(TimedeltaIndexType, 'dtype')
@overload_attribute(RangeIndexType, 'dtype')
@overload_attribute(StringIndexType, 'dtype')
@overload_attribute(BinaryIndexType, 'dtype')
@overload_attribute(CategoricalIndexType, 'dtype')
@overload_attribute(MultiIndexType, 'dtype')
def overload_inferred_type(I):
    if isinstance(I, NumericIndexType):
        if isinstance(I.dtype, types.Boolean):
            return lambda I: np.dtype('O')
        dtype = I.dtype
        return lambda I: dtype
    if isinstance(I, CategoricalIndexType):
        dtype = bodo.utils.utils.create_categorical_type(I.dtype.categories,
            I.data, I.dtype.ordered)
        return lambda I: dtype
    ogn__gsty = {DatetimeIndexType: np.dtype('datetime64[ns]'),
        TimedeltaIndexType: np.dtype('timedelta64[ns]'), RangeIndexType: np
        .dtype('int64'), StringIndexType: np.dtype('O'), BinaryIndexType:
        np.dtype('O'), MultiIndexType: np.dtype('O')}
    dtype = ogn__gsty[type(I)]
    return lambda I: dtype


@overload_attribute(NumericIndexType, 'names')
@overload_attribute(DatetimeIndexType, 'names')
@overload_attribute(TimedeltaIndexType, 'names')
@overload_attribute(RangeIndexType, 'names')
@overload_attribute(StringIndexType, 'names')
@overload_attribute(BinaryIndexType, 'names')
@overload_attribute(CategoricalIndexType, 'names')
@overload_attribute(IntervalIndexType, 'names')
@overload_attribute(PeriodIndexType, 'names')
@overload_attribute(MultiIndexType, 'names')
def overload_names(I):
    if isinstance(I, MultiIndexType):
        return lambda I: I._names
    return lambda I: (I._name,)


@overload_method(NumericIndexType, 'rename', inline='always')
@overload_method(DatetimeIndexType, 'rename', inline='always')
@overload_method(TimedeltaIndexType, 'rename', inline='always')
@overload_method(RangeIndexType, 'rename', inline='always')
@overload_method(StringIndexType, 'rename', inline='always')
@overload_method(BinaryIndexType, 'rename', inline='always')
@overload_method(CategoricalIndexType, 'rename', inline='always')
@overload_method(PeriodIndexType, 'rename', inline='always')
@overload_method(IntervalIndexType, 'rename', inline='always')
@overload_method(HeterogeneousIndexType, 'rename', inline='always')
def overload_rename(I, name, inplace=False):
    if is_overload_true(inplace):
        raise BodoError('Index.rename(): inplace index renaming unsupported')
    return init_index_from_index(I, name)


def init_index_from_index(I, name):
    qgw__etxey = {NumericIndexType: bodo.hiframes.pd_index_ext.
        init_numeric_index, DatetimeIndexType: bodo.hiframes.pd_index_ext.
        init_datetime_index, TimedeltaIndexType: bodo.hiframes.pd_index_ext
        .init_timedelta_index, StringIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, BinaryIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, CategoricalIndexType: bodo.hiframes.
        pd_index_ext.init_categorical_index, IntervalIndexType: bodo.
        hiframes.pd_index_ext.init_interval_index}
    if type(I) in qgw__etxey:
        init_func = qgw__etxey[type(I)]
        return lambda I, name, inplace=False: init_func(bodo.hiframes.
            pd_index_ext.get_index_data(I).copy(), name)
    if isinstance(I, RangeIndexType):
        return lambda I, name, inplace=False: I.copy(name=name)
    if isinstance(I, PeriodIndexType):
        freq = I.freq
        return (lambda I, name, inplace=False: bodo.hiframes.pd_index_ext.
            init_period_index(bodo.hiframes.pd_index_ext.get_index_data(I).
            copy(), name, freq))
    if isinstance(I, HeterogeneousIndexType):
        return (lambda I, name, inplace=False: bodo.hiframes.pd_index_ext.
            init_heter_index(bodo.hiframes.pd_index_ext.get_index_data(I),
            name))
    raise_bodo_error(f'init_index(): Unknown type {type(I)}')


def get_index_constructor(I):
    zfwi__qhxm = {NumericIndexType: bodo.hiframes.pd_index_ext.
        init_numeric_index, DatetimeIndexType: bodo.hiframes.pd_index_ext.
        init_datetime_index, TimedeltaIndexType: bodo.hiframes.pd_index_ext
        .init_timedelta_index, StringIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, BinaryIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, CategoricalIndexType: bodo.hiframes.
        pd_index_ext.init_categorical_index, IntervalIndexType: bodo.
        hiframes.pd_index_ext.init_interval_index, RangeIndexType: bodo.
        hiframes.pd_index_ext.init_range_index}
    if type(I) in zfwi__qhxm:
        return zfwi__qhxm[type(I)]
    raise BodoError(
        f'Unsupported type for standard Index constructor: {type(I)}')


@overload_method(NumericIndexType, 'min', no_unliteral=True, inline='always')
@overload_method(RangeIndexType, 'min', no_unliteral=True, inline='always')
@overload_method(CategoricalIndexType, 'min', no_unliteral=True, inline=
    'always')
def overload_index_min(I, axis=None, skipna=True):
    tsp__ume = dict(axis=axis, skipna=skipna)
    ugzcb__bvng = dict(axis=None, skipna=True)
    check_unsupported_args('Index.min', tsp__ume, ugzcb__bvng, package_name
        ='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):

        def impl(I, axis=None, skipna=True):
            ugj__kln = len(I)
            if ugj__kln == 0:
                return np.nan
            if I._step < 0:
                return I._start + I._step * (ugj__kln - 1)
            else:
                return I._start
        return impl
    if isinstance(I, CategoricalIndexType):
        if not I.dtype.ordered:
            raise BodoError(
                'Index.min(): only ordered categoricals are possible')

    def impl(I, axis=None, skipna=True):
        abph__hoc = bodo.hiframes.pd_index_ext.get_index_data(I)
        return bodo.libs.array_ops.array_op_min(abph__hoc)
    return impl


@overload_method(NumericIndexType, 'max', no_unliteral=True, inline='always')
@overload_method(RangeIndexType, 'max', no_unliteral=True, inline='always')
@overload_method(CategoricalIndexType, 'max', no_unliteral=True, inline=
    'always')
def overload_index_max(I, axis=None, skipna=True):
    tsp__ume = dict(axis=axis, skipna=skipna)
    ugzcb__bvng = dict(axis=None, skipna=True)
    check_unsupported_args('Index.max', tsp__ume, ugzcb__bvng, package_name
        ='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):

        def impl(I, axis=None, skipna=True):
            ugj__kln = len(I)
            if ugj__kln == 0:
                return np.nan
            if I._step > 0:
                return I._start + I._step * (ugj__kln - 1)
            else:
                return I._start
        return impl
    if isinstance(I, CategoricalIndexType):
        if not I.dtype.ordered:
            raise BodoError(
                'Index.max(): only ordered categoricals are possible')

    def impl(I, axis=None, skipna=True):
        abph__hoc = bodo.hiframes.pd_index_ext.get_index_data(I)
        return bodo.libs.array_ops.array_op_max(abph__hoc)
    return impl


@overload_method(NumericIndexType, 'argmin', no_unliteral=True, inline='always'
    )
@overload_method(StringIndexType, 'argmin', no_unliteral=True, inline='always')
@overload_method(BinaryIndexType, 'argmin', no_unliteral=True, inline='always')
@overload_method(DatetimeIndexType, 'argmin', no_unliteral=True, inline=
    'always')
@overload_method(TimedeltaIndexType, 'argmin', no_unliteral=True, inline=
    'always')
@overload_method(CategoricalIndexType, 'argmin', no_unliteral=True, inline=
    'always')
@overload_method(RangeIndexType, 'argmin', no_unliteral=True, inline='always')
@overload_method(PeriodIndexType, 'argmin', no_unliteral=True, inline='always')
def overload_index_argmin(I, axis=0, skipna=True):
    tsp__ume = dict(axis=axis, skipna=skipna)
    ugzcb__bvng = dict(axis=0, skipna=True)
    check_unsupported_args('Index.argmin', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.argmin()')
    if isinstance(I, RangeIndexType):

        def impl(I, axis=0, skipna=True):
            return (I._step < 0) * (len(I) - 1)
        return impl
    if isinstance(I, CategoricalIndexType) and not I.dtype.ordered:
        raise BodoError(
            'Index.argmin(): only ordered categoricals are possible')

    def impl(I, axis=0, skipna=True):
        abph__hoc = bodo.hiframes.pd_index_ext.get_index_data(I)
        index = init_numeric_index(np.arange(len(abph__hoc)))
        return bodo.libs.array_ops.array_op_idxmin(abph__hoc, index)
    return impl


@overload_method(NumericIndexType, 'argmax', no_unliteral=True, inline='always'
    )
@overload_method(StringIndexType, 'argmax', no_unliteral=True, inline='always')
@overload_method(BinaryIndexType, 'argmax', no_unliteral=True, inline='always')
@overload_method(DatetimeIndexType, 'argmax', no_unliteral=True, inline=
    'always')
@overload_method(TimedeltaIndexType, 'argmax', no_unliteral=True, inline=
    'always')
@overload_method(RangeIndexType, 'argmax', no_unliteral=True, inline='always')
@overload_method(CategoricalIndexType, 'argmax', no_unliteral=True, inline=
    'always')
@overload_method(PeriodIndexType, 'argmax', no_unliteral=True, inline='always')
def overload_index_argmax(I, axis=0, skipna=True):
    tsp__ume = dict(axis=axis, skipna=skipna)
    ugzcb__bvng = dict(axis=0, skipna=True)
    check_unsupported_args('Index.argmax', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.argmax()')
    if isinstance(I, RangeIndexType):

        def impl(I, axis=0, skipna=True):
            return (I._step > 0) * (len(I) - 1)
        return impl
    if isinstance(I, CategoricalIndexType) and not I.dtype.ordered:
        raise BodoError(
            'Index.argmax(): only ordered categoricals are possible')

    def impl(I, axis=0, skipna=True):
        abph__hoc = bodo.hiframes.pd_index_ext.get_index_data(I)
        index = np.arange(len(abph__hoc))
        return bodo.libs.array_ops.array_op_idxmax(abph__hoc, index)
    return impl


@overload_method(NumericIndexType, 'unique', no_unliteral=True, inline='always'
    )
@overload_method(BinaryIndexType, 'unique', no_unliteral=True, inline='always')
@overload_method(StringIndexType, 'unique', no_unliteral=True, inline='always')
@overload_method(CategoricalIndexType, 'unique', no_unliteral=True, inline=
    'always')
@overload_method(IntervalIndexType, 'unique', no_unliteral=True, inline=
    'always')
@overload_method(DatetimeIndexType, 'unique', no_unliteral=True, inline=
    'always')
@overload_method(TimedeltaIndexType, 'unique', no_unliteral=True, inline=
    'always')
def overload_index_unique(I):
    ilr__pck = get_index_constructor(I)

    def impl(I):
        abph__hoc = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        xfgkh__qsaf = bodo.libs.array_kernels.unique(abph__hoc)
        return ilr__pck(xfgkh__qsaf, name)
    return impl


@overload_method(RangeIndexType, 'unique', no_unliteral=True, inline='always')
def overload_range_index_unique(I):

    def impl(I):
        return I.copy()
    return impl


@overload_method(NumericIndexType, 'nunique', inline='always')
@overload_method(BinaryIndexType, 'nunique', inline='always')
@overload_method(StringIndexType, 'nunique', inline='always')
@overload_method(CategoricalIndexType, 'nunique', inline='always')
@overload_method(DatetimeIndexType, 'nunique', inline='always')
@overload_method(TimedeltaIndexType, 'nunique', inline='always')
@overload_method(PeriodIndexType, 'nunique', inline='always')
def overload_index_nunique(I, dropna=True):

    def impl(I, dropna=True):
        abph__hoc = bodo.hiframes.pd_index_ext.get_index_data(I)
        svaxh__xlacb = bodo.libs.array_kernels.nunique(abph__hoc, dropna)
        return svaxh__xlacb
    return impl


@overload_method(RangeIndexType, 'nunique', inline='always')
def overload_range_index_nunique(I, dropna=True):

    def impl(I, dropna=True):
        start = I._start
        stop = I._stop
        step = I._step
        return max(0, -(-(stop - start) // step))
    return impl


@overload_method(NumericIndexType, 'isin', no_unliteral=True, inline='always')
@overload_method(BinaryIndexType, 'isin', no_unliteral=True, inline='always')
@overload_method(StringIndexType, 'isin', no_unliteral=True, inline='always')
@overload_method(DatetimeIndexType, 'isin', no_unliteral=True, inline='always')
@overload_method(TimedeltaIndexType, 'isin', no_unliteral=True, inline='always'
    )
def overload_index_isin(I, values):
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(I, values):
            npj__njt = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_index_ext.get_index_data(I)
            svaxh__xlacb = len(A)
            fjhb__zrn = np.empty(svaxh__xlacb, np.bool_)
            bodo.libs.array.array_isin(fjhb__zrn, A, npj__njt, False)
            return fjhb__zrn
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(I, values):
        A = bodo.hiframes.pd_index_ext.get_index_data(I)
        fjhb__zrn = bodo.libs.array_ops.array_op_isin(A, values)
        return fjhb__zrn
    return impl


@overload_method(RangeIndexType, 'isin', no_unliteral=True, inline='always')
def overload_range_index_isin(I, values):
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(I, values):
            npj__njt = bodo.utils.conversion.coerce_to_array(values)
            A = np.arange(I.start, I.stop, I.step)
            svaxh__xlacb = len(A)
            fjhb__zrn = np.empty(svaxh__xlacb, np.bool_)
            bodo.libs.array.array_isin(fjhb__zrn, A, npj__njt, False)
            return fjhb__zrn
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Index.isin(): 'values' parameter should be a set or a list")

    def impl(I, values):
        A = np.arange(I.start, I.stop, I.step)
        fjhb__zrn = bodo.libs.array_ops.array_op_isin(A, values)
        return fjhb__zrn
    return impl


@register_jitable
def order_range(I, ascending):
    step = I._step
    if ascending == (step > 0):
        return I.copy()
    else:
        start = I._start
        stop = I._stop
        name = get_index_name(I)
        ugj__kln = len(I)
        kfsf__xvbn = start + step * (ugj__kln - 1)
        kxo__hnn = kfsf__xvbn - step * ugj__kln
        return init_range_index(kfsf__xvbn, kxo__hnn, -step, name)


@overload_method(NumericIndexType, 'sort_values', no_unliteral=True, inline
    ='always')
@overload_method(BinaryIndexType, 'sort_values', no_unliteral=True, inline=
    'always')
@overload_method(StringIndexType, 'sort_values', no_unliteral=True, inline=
    'always')
@overload_method(CategoricalIndexType, 'sort_values', no_unliteral=True,
    inline='always')
@overload_method(DatetimeIndexType, 'sort_values', no_unliteral=True,
    inline='always')
@overload_method(TimedeltaIndexType, 'sort_values', no_unliteral=True,
    inline='always')
@overload_method(RangeIndexType, 'sort_values', no_unliteral=True, inline=
    'always')
def overload_index_sort_values(I, return_indexer=False, ascending=True,
    na_position='last', key=None):
    tsp__ume = dict(return_indexer=return_indexer, key=key)
    ugzcb__bvng = dict(return_indexer=False, key=None)
    check_unsupported_args('Index.sort_values', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Index.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Index.sort_values(): 'na_position' should either be 'first' or 'last'"
            )
    if isinstance(I, RangeIndexType):

        def impl(I, return_indexer=False, ascending=True, na_position=
            'last', key=None):
            return order_range(I, ascending)
        return impl
    ilr__pck = get_index_constructor(I)
    uym__ysrp = ColNamesMetaType(('$_bodo_col_',))

    def impl(I, return_indexer=False, ascending=True, na_position='last',
        key=None):
        abph__hoc = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = get_index_name(I)
        index = init_range_index(0, len(abph__hoc), 1, None)
        wjrp__hwxn = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            abph__hoc,), index, uym__ysrp)
        kgsz__yiv = wjrp__hwxn.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=False, na_position=na_position)
        fjhb__zrn = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(kgsz__yiv
            , 0)
        return ilr__pck(fjhb__zrn, name)
    return impl


@overload_method(NumericIndexType, 'argsort', no_unliteral=True, inline=
    'always')
@overload_method(BinaryIndexType, 'argsort', no_unliteral=True, inline='always'
    )
@overload_method(StringIndexType, 'argsort', no_unliteral=True, inline='always'
    )
@overload_method(CategoricalIndexType, 'argsort', no_unliteral=True, inline
    ='always')
@overload_method(DatetimeIndexType, 'argsort', no_unliteral=True, inline=
    'always')
@overload_method(TimedeltaIndexType, 'argsort', no_unliteral=True, inline=
    'always')
@overload_method(PeriodIndexType, 'argsort', no_unliteral=True, inline='always'
    )
@overload_method(RangeIndexType, 'argsort', no_unliteral=True, inline='always')
def overload_index_argsort(I, axis=0, kind='quicksort', order=None):
    tsp__ume = dict(axis=axis, kind=kind, order=order)
    ugzcb__bvng = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Index.argsort', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):

        def impl(I, axis=0, kind='quicksort', order=None):
            if I._step > 0:
                return np.arange(0, len(I), 1)
            else:
                return np.arange(len(I) - 1, -1, -1)
        return impl

    def impl(I, axis=0, kind='quicksort', order=None):
        abph__hoc = bodo.hiframes.pd_index_ext.get_index_data(I)
        fjhb__zrn = bodo.hiframes.series_impl.argsort(abph__hoc)
        return fjhb__zrn
    return impl


@overload_method(NumericIndexType, 'where', no_unliteral=True, inline='always')
@overload_method(StringIndexType, 'where', no_unliteral=True, inline='always')
@overload_method(BinaryIndexType, 'where', no_unliteral=True, inline='always')
@overload_method(DatetimeIndexType, 'where', no_unliteral=True, inline='always'
    )
@overload_method(TimedeltaIndexType, 'where', no_unliteral=True, inline=
    'always')
@overload_method(CategoricalIndexType, 'where', no_unliteral=True, inline=
    'always')
@overload_method(RangeIndexType, 'where', no_unliteral=True, inline='always')
def overload_index_where(I, cond, other=np.nan):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.where()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Index.where()')
    bodo.hiframes.series_impl._validate_arguments_mask_where('where',
        'Index', I, cond, other, inplace=False, axis=None, level=None,
        errors='raise', try_cast=False)
    if is_overload_constant_nan(other):
        xozx__vrkeh = 'None'
    else:
        xozx__vrkeh = 'other'
    abd__wuyu = 'def impl(I, cond, other=np.nan):\n'
    if isinstance(I, RangeIndexType):
        abd__wuyu += '  arr = np.arange(I._start, I._stop, I._step)\n'
        ilr__pck = 'init_numeric_index'
    else:
        abd__wuyu += '  arr = bodo.hiframes.pd_index_ext.get_index_data(I)\n'
    abd__wuyu += '  name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    abd__wuyu += (
        f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {xozx__vrkeh})\n'
        )
    abd__wuyu += f'  return constructor(out_arr, name)\n'
    aha__iwa = {}
    ilr__pck = init_numeric_index if isinstance(I, RangeIndexType
        ) else get_index_constructor(I)
    exec(abd__wuyu, {'bodo': bodo, 'np': np, 'constructor': ilr__pck}, aha__iwa
        )
    impl = aha__iwa['impl']
    return impl


@overload_method(NumericIndexType, 'putmask', no_unliteral=True, inline=
    'always')
@overload_method(StringIndexType, 'putmask', no_unliteral=True, inline='always'
    )
@overload_method(BinaryIndexType, 'putmask', no_unliteral=True, inline='always'
    )
@overload_method(DatetimeIndexType, 'putmask', no_unliteral=True, inline=
    'always')
@overload_method(TimedeltaIndexType, 'putmask', no_unliteral=True, inline=
    'always')
@overload_method(CategoricalIndexType, 'putmask', no_unliteral=True, inline
    ='always')
@overload_method(RangeIndexType, 'putmask', no_unliteral=True, inline='always')
def overload_index_putmask(I, cond, other):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.putmask()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Index.putmask()')
    bodo.hiframes.series_impl._validate_arguments_mask_where('putmask',
        'Index', I, cond, other, inplace=False, axis=None, level=None,
        errors='raise', try_cast=False)
    if is_overload_constant_nan(other):
        xozx__vrkeh = 'None'
    else:
        xozx__vrkeh = 'other'
    abd__wuyu = 'def impl(I, cond, other):\n'
    abd__wuyu += '  cond = ~cond\n'
    if isinstance(I, RangeIndexType):
        abd__wuyu += '  arr = np.arange(I._start, I._stop, I._step)\n'
    else:
        abd__wuyu += '  arr = bodo.hiframes.pd_index_ext.get_index_data(I)\n'
    abd__wuyu += '  name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    abd__wuyu += (
        f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {xozx__vrkeh})\n'
        )
    abd__wuyu += f'  return constructor(out_arr, name)\n'
    aha__iwa = {}
    ilr__pck = init_numeric_index if isinstance(I, RangeIndexType
        ) else get_index_constructor(I)
    exec(abd__wuyu, {'bodo': bodo, 'np': np, 'constructor': ilr__pck}, aha__iwa
        )
    impl = aha__iwa['impl']
    return impl


@overload_method(NumericIndexType, 'repeat', no_unliteral=True, inline='always'
    )
@overload_method(StringIndexType, 'repeat', no_unliteral=True, inline='always')
@overload_method(CategoricalIndexType, 'repeat', no_unliteral=True, inline=
    'always')
@overload_method(DatetimeIndexType, 'repeat', no_unliteral=True, inline=
    'always')
@overload_method(TimedeltaIndexType, 'repeat', no_unliteral=True, inline=
    'always')
@overload_method(RangeIndexType, 'repeat', no_unliteral=True, inline='always')
def overload_index_repeat(I, repeats, axis=None):
    tsp__ume = dict(axis=axis)
    ugzcb__bvng = dict(axis=None)
    check_unsupported_args('Index.repeat', tsp__ume, ugzcb__bvng,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.repeat()')
    if not (isinstance(repeats, types.Integer) or is_iterable_type(repeats) and
        isinstance(repeats.dtype, types.Integer)):
        raise BodoError(
            "Index.repeat(): 'repeats' should be an integer or array of integers"
            )
    abd__wuyu = 'def impl(I, repeats, axis=None):\n'
    if not isinstance(repeats, types.Integer):
        abd__wuyu += (
            '    repeats = bodo.utils.conversion.coerce_to_array(repeats)\n')
    if isinstance(I, RangeIndexType):
        abd__wuyu += '    arr = np.arange(I._start, I._stop, I._step)\n'
    else:
        abd__wuyu += '    arr = bodo.hiframes.pd_index_ext.get_index_data(I)\n'
    abd__wuyu += '    name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    abd__wuyu += (
        '    out_arr = bodo.libs.array_kernels.repeat_kernel(arr, repeats)\n')
    abd__wuyu += '    return constructor(out_arr, name)'
    aha__iwa = {}
    ilr__pck = init_numeric_index if isinstance(I, RangeIndexType
        ) else get_index_constructor(I)
    exec(abd__wuyu, {'bodo': bodo, 'np': np, 'constructor': ilr__pck}, aha__iwa
        )
    impl = aha__iwa['impl']
    return impl


@overload_method(NumericIndexType, 'is_integer', inline='always')
def overload_is_integer_numeric(I):
    truth = isinstance(I.dtype, types.Integer)
    return lambda I: truth


@overload_method(NumericIndexType, 'is_floating', inline='always')
def overload_is_floating_numeric(I):
    truth = isinstance(I.dtype, types.Float)
    return lambda I: truth


@overload_method(NumericIndexType, 'is_boolean', inline='always')
def overload_is_boolean_numeric(I):
    truth = isinstance(I.dtype, types.Boolean)
    return lambda I: truth


@overload_method(NumericIndexType, 'is_numeric', inline='always')
def overload_is_numeric_numeric(I):
    truth = not isinstance(I.dtype, types.Boolean)
    return lambda I: truth


@overload_method(NumericIndexType, 'is_object', inline='always')
def overload_is_object_numeric(I):
    truth = isinstance(I.dtype, types.Boolean)
    return lambda I: truth


@overload_method(StringIndexType, 'is_object', inline='always')
@overload_method(BinaryIndexType, 'is_object', inline='always')
@overload_method(RangeIndexType, 'is_numeric', inline='always')
@overload_method(RangeIndexType, 'is_integer', inline='always')
@overload_method(CategoricalIndexType, 'is_categorical', inline='always')
@overload_method(IntervalIndexType, 'is_interval', inline='always')
@overload_method(MultiIndexType, 'is_object', inline='always')
def overload_is_methods_true(I):
    return lambda I: True


@overload_method(NumericIndexType, 'is_categorical', inline='always')
@overload_method(NumericIndexType, 'is_interval', inline='always')
@overload_method(StringIndexType, 'is_boolean', inline='always')
@overload_method(StringIndexType, 'is_floating', inline='always')
@overload_method(StringIndexType, 'is_categorical', inline='always')
@overload_method(StringIndexType, 'is_integer', inline='always')
@overload_method(StringIndexType, 'is_interval', inline='always')
@overload_method(StringIndexType, 'is_numeric', inline='always')
@overload_method(BinaryIndexType, 'is_boolean', inline='always')
@overload_method(BinaryIndexType, 'is_floating', inline='always')
@overload_method(BinaryIndexType, 'is_categorical', inline='always')
@overload_method(BinaryIndexType, 'is_integer', inline='always')
@overload_method(BinaryIndexType, 'is_interval', inline='always')
@overload_method(BinaryIndexType, 'is_numeric', inline='always')
@overload_method(DatetimeIndexType, 'is_boolean', inline='always')
@overload_method(DatetimeIndexType, 'is_floating', inline='always')
@overload_method(DatetimeIndexType, 'is_categorical', inline='always')
@overload_method(DatetimeIndexType, 'is_integer', inline='always')
@overload_method(DatetimeIndexType, 'is_interval', inline='always')
@overload_method(DatetimeIndexType, 'is_numeric', inline='always')
@overload_method(DatetimeIndexType, 'is_object', inline='always')
@overload_method(TimedeltaIndexType, 'is_boolean', inline='always')
@overload_method(TimedeltaIndexType, 'is_floating', inline='always')
@overload_method(TimedeltaIndexType, 'is_categorical', inline='always')
@overload_method(TimedeltaIndexType, 'is_integer', inline='always')
@overload_method(TimedeltaIndexType, 'is_interval', inline='always')
@overload_method(TimedeltaIndexType, 'is_numeric', inline='always')
@overload_method(TimedeltaIndexType, 'is_object', inline='always')
@overload_method(RangeIndexType, 'is_boolean', inline='always')
@overload_method(RangeIndexType, 'is_floating', inline='always')
@overload_method(RangeIndexType, 'is_categorical', inline='always')
@overload_method(RangeIndexType, 'is_interval', inline='always')
@overload_method(RangeIndexType, 'is_object', inline='always')
@overload_method(IntervalIndexType, 'is_boolean', inline='always')
@overload_method(IntervalIndexType, 'is_floating', inline='always')
@overload_method(IntervalIndexType, 'is_categorical', inline='always')
@overload_method(IntervalIndexType, 'is_integer', inline='always')
@overload_method(IntervalIndexType, 'is_numeric', inline='always')
@overload_method(IntervalIndexType, 'is_object', inline='always')
@overload_method(CategoricalIndexType, 'is_boolean', inline='always')
@overload_method(CategoricalIndexType, 'is_floating', inline='always')
@overload_method(CategoricalIndexType, 'is_integer', inline='always')
@overload_method(CategoricalIndexType, 'is_interval', inline='always')
@overload_method(CategoricalIndexType, 'is_numeric', inline='always')
@overload_method(CategoricalIndexType, 'is_object', inline='always')
@overload_method(PeriodIndexType, 'is_boolean', inline='always')
@overload_method(PeriodIndexType, 'is_floating', inline='always')
@overload_method(PeriodIndexType, 'is_categorical', inline='always')
@overload_method(PeriodIndexType, 'is_integer', inline='always')
@overload_method(PeriodIndexType, 'is_interval', inline='always')
@overload_method(PeriodIndexType, 'is_numeric', inline='always')
@overload_method(PeriodIndexType, 'is_object', inline='always')
@overload_method(MultiIndexType, 'is_boolean', inline='always')
@overload_method(MultiIndexType, 'is_floating', inline='always')
@overload_method(MultiIndexType, 'is_categorical', inline='always')
@overload_method(MultiIndexType, 'is_integer', inline='always')
@overload_method(MultiIndexType, 'is_interval', inline='always')
@overload_method(MultiIndexType, 'is_numeric', inline='always')
def overload_is_methods_false(I):
    return lambda I: False


@overload(operator.getitem, no_unliteral=True)
def overload_heter_index_getitem(I, ind):
    if not isinstance(I, HeterogeneousIndexType):
        return
    if isinstance(ind, types.Integer):
        return lambda I, ind: bodo.hiframes.pd_index_ext.get_index_data(I)[ind]
    if isinstance(I, HeterogeneousIndexType):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_heter_index(bodo
            .hiframes.pd_index_ext.get_index_data(I)[ind], bodo.hiframes.
            pd_index_ext.get_index_name(I))


@lower_constant(DatetimeIndexType)
@lower_constant(TimedeltaIndexType)
def lower_constant_time_index(context, builder, ty, pyval):
    if isinstance(ty.data, bodo.DatetimeArrayType):
        data = context.get_constant_generic(builder, ty.data, pyval.array)
    else:
        data = context.get_constant_generic(builder, types.Array(types.
            int64, 1, 'C'), pyval.values.view(np.int64))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    dtype = ty.dtype
    tih__gpz = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, tih__gpz])


@lower_constant(PeriodIndexType)
def lower_constant_period_index(context, builder, ty, pyval):
    data = context.get_constant_generic(builder, bodo.IntegerArrayType(
        types.int64), pd.arrays.IntegerArray(pyval.asi8, pyval.isna()))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    tih__gpz = context.get_constant_null(types.DictType(types.int64, types.
        int64))
    return lir.Constant.literal_struct([data, name, tih__gpz])


@lower_constant(NumericIndexType)
def lower_constant_numeric_index(context, builder, ty, pyval):
    assert isinstance(ty.dtype, (types.Integer, types.Float, types.Boolean))
    data = context.get_constant_generic(builder, types.Array(ty.dtype, 1,
        'C'), pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    dtype = ty.dtype
    tih__gpz = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, tih__gpz])


@lower_constant(StringIndexType)
@lower_constant(BinaryIndexType)
def lower_constant_binary_string_index(context, builder, ty, pyval):
    ydgd__bmcvp = ty.data
    scalar_type = ty.data.dtype
    data = context.get_constant_generic(builder, ydgd__bmcvp, pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    tih__gpz = context.get_constant_null(types.DictType(scalar_type, types.
        int64))
    return lir.Constant.literal_struct([data, name, tih__gpz])


@lower_builtin('getiter', RangeIndexType)
def getiter_range_index(context, builder, sig, args):
    [rmnv__ypwqa] = sig.args
    [index] = args
    eqa__tdv = context.make_helper(builder, rmnv__ypwqa, value=index)
    ttg__hdwk = context.make_helper(builder, sig.return_type)
    wke__kyyf = cgutils.alloca_once_value(builder, eqa__tdv.start)
    ein__sojhd = context.get_constant(types.intp, 0)
    daf__kmob = cgutils.alloca_once_value(builder, ein__sojhd)
    ttg__hdwk.iter = wke__kyyf
    ttg__hdwk.stop = eqa__tdv.stop
    ttg__hdwk.step = eqa__tdv.step
    ttg__hdwk.count = daf__kmob
    neu__umwv = builder.sub(eqa__tdv.stop, eqa__tdv.start)
    hiita__kenze = context.get_constant(types.intp, 1)
    hyjq__aqdyb = builder.icmp_signed('>', neu__umwv, ein__sojhd)
    oldix__nfey = builder.icmp_signed('>', eqa__tdv.step, ein__sojhd)
    wznjk__mif = builder.not_(builder.xor(hyjq__aqdyb, oldix__nfey))
    with builder.if_then(wznjk__mif):
        pkf__adf = builder.srem(neu__umwv, eqa__tdv.step)
        pkf__adf = builder.select(hyjq__aqdyb, pkf__adf, builder.neg(pkf__adf))
        smh__sjpa = builder.icmp_signed('>', pkf__adf, ein__sojhd)
        vpjl__qnn = builder.add(builder.sdiv(neu__umwv, eqa__tdv.step),
            builder.select(smh__sjpa, hiita__kenze, ein__sojhd))
        builder.store(vpjl__qnn, daf__kmob)
    ilsy__vsjmx = ttg__hdwk._getvalue()
    xbz__pgcc = impl_ret_new_ref(context, builder, sig.return_type, ilsy__vsjmx
        )
    return xbz__pgcc


def _install_index_getiter():
    index_types = [NumericIndexType, StringIndexType, BinaryIndexType,
        CategoricalIndexType, TimedeltaIndexType, DatetimeIndexType]
    for typ in index_types:
        lower_builtin('getiter', typ)(numba.np.arrayobj.getiter_array)


_install_index_getiter()
index_unsupported_methods = ['append', 'asof', 'asof_locs', 'astype',
    'delete', 'drop', 'droplevel', 'dropna', 'equals', 'factorize',
    'fillna', 'format', 'get_indexer', 'get_indexer_for',
    'get_indexer_non_unique', 'get_level_values', 'get_slice_bound',
    'get_value', 'groupby', 'holds_integer', 'identical', 'insert', 'is_',
    'is_mixed', 'is_type_compatible', 'item', 'join', 'memory_usage',
    'ravel', 'reindex', 'searchsorted', 'set_names', 'set_value', 'shift',
    'slice_indexer', 'slice_locs', 'sort', 'sortlevel', 'str',
    'to_flat_index', 'to_native_types', 'transpose', 'value_counts', 'view']
index_unsupported_atrs = ['array', 'asi8', 'has_duplicates', 'hasnans',
    'is_unique']
cat_idx_unsupported_atrs = ['codes', 'categories', 'ordered',
    'is_monotonic', 'is_monotonic_increasing', 'is_monotonic_decreasing']
cat_idx_unsupported_methods = ['rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered', 'get_loc', 'isin',
    'all', 'any', 'union', 'intersection', 'difference', 'symmetric_difference'
    ]
interval_idx_unsupported_atrs = ['closed', 'is_empty',
    'is_non_overlapping_monotonic', 'is_overlapping', 'left', 'right',
    'mid', 'length', 'values', 'nbytes', 'is_monotonic',
    'is_monotonic_increasing', 'is_monotonic_decreasing', 'dtype']
interval_idx_unsupported_methods = ['contains', 'copy', 'overlaps',
    'set_closed', 'to_tuples', 'take', 'get_loc', 'isna', 'isnull', 'map',
    'isin', 'all', 'any', 'argsort', 'sort_values', 'argmax', 'argmin',
    'where', 'putmask', 'nunique', 'union', 'intersection', 'difference',
    'symmetric_difference', 'to_series', 'to_frame', 'to_list', 'tolist',
    'repeat', 'min', 'max']
multi_index_unsupported_atrs = ['levshape', 'levels', 'codes', 'dtypes',
    'values', 'is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
multi_index_unsupported_methods = ['copy', 'set_levels', 'set_codes',
    'swaplevel', 'reorder_levels', 'remove_unused_levels', 'get_loc',
    'get_locs', 'get_loc_level', 'take', 'isna', 'isnull', 'map', 'isin',
    'unique', 'all', 'any', 'argsort', 'sort_values', 'argmax', 'argmin',
    'where', 'putmask', 'nunique', 'union', 'intersection', 'difference',
    'symmetric_difference', 'to_series', 'to_list', 'tolist', 'to_numpy',
    'repeat', 'min', 'max']
dt_index_unsupported_atrs = ['time', 'timez', 'tz', 'freq', 'freqstr',
    'inferred_freq']
dt_index_unsupported_methods = ['normalize', 'strftime', 'snap',
    'tz_localize', 'round', 'floor', 'ceil', 'to_period', 'to_perioddelta',
    'to_pydatetime', 'month_name', 'day_name', 'mean', 'indexer_at_time',
    'indexer_between', 'indexer_between_time', 'all', 'any']
td_index_unsupported_atrs = ['components', 'inferred_freq']
td_index_unsupported_methods = ['to_pydatetime', 'round', 'floor', 'ceil',
    'mean', 'all', 'any']
period_index_unsupported_atrs = ['day', 'dayofweek', 'day_of_week',
    'dayofyear', 'day_of_year', 'days_in_month', 'daysinmonth', 'freq',
    'freqstr', 'hour', 'is_leap_year', 'minute', 'month', 'quarter',
    'second', 'week', 'weekday', 'weekofyear', 'year', 'end_time', 'qyear',
    'start_time', 'is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing', 'dtype']
period_index_unsupported_methods = ['asfreq', 'strftime', 'to_timestamp',
    'isin', 'unique', 'all', 'any', 'where', 'putmask', 'sort_values',
    'union', 'intersection', 'difference', 'symmetric_difference',
    'to_series', 'to_frame', 'to_numpy', 'to_list', 'tolist', 'repeat',
    'min', 'max']
string_index_unsupported_atrs = ['is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
string_index_unsupported_methods = ['min', 'max']
binary_index_unsupported_atrs = ['is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
binary_index_unsupported_methods = ['repeat', 'min', 'max']
index_types = [('pandas.RangeIndex.{}', RangeIndexType), (
    'pandas.Index.{} with numeric data', NumericIndexType), (
    'pandas.Index.{} with string data', StringIndexType), (
    'pandas.Index.{} with binary data', BinaryIndexType), (
    'pandas.TimedeltaIndex.{}', TimedeltaIndexType), (
    'pandas.IntervalIndex.{}', IntervalIndexType), (
    'pandas.CategoricalIndex.{}', CategoricalIndexType), (
    'pandas.PeriodIndex.{}', PeriodIndexType), ('pandas.DatetimeIndex.{}',
    DatetimeIndexType), ('pandas.MultiIndex.{}', MultiIndexType)]
for name, typ in index_types:
    idx_typ_to_format_str_map[typ] = name


def _install_index_unsupported():
    for klt__elw in index_unsupported_methods:
        for aluqs__bzdf, typ in index_types:
            overload_method(typ, klt__elw, no_unliteral=True)(
                create_unsupported_overload(aluqs__bzdf.format(klt__elw +
                '()')))
    for qeahc__calk in index_unsupported_atrs:
        for aluqs__bzdf, typ in index_types:
            overload_attribute(typ, qeahc__calk, no_unliteral=True)(
                create_unsupported_overload(aluqs__bzdf.format(qeahc__calk)))
    acy__fwnzw = [(StringIndexType, string_index_unsupported_atrs), (
        BinaryIndexType, binary_index_unsupported_atrs), (
        CategoricalIndexType, cat_idx_unsupported_atrs), (IntervalIndexType,
        interval_idx_unsupported_atrs), (MultiIndexType,
        multi_index_unsupported_atrs), (DatetimeIndexType,
        dt_index_unsupported_atrs), (TimedeltaIndexType,
        td_index_unsupported_atrs), (PeriodIndexType,
        period_index_unsupported_atrs)]
    roe__rprx = [(CategoricalIndexType, cat_idx_unsupported_methods), (
        IntervalIndexType, interval_idx_unsupported_methods), (
        MultiIndexType, multi_index_unsupported_methods), (
        DatetimeIndexType, dt_index_unsupported_methods), (
        TimedeltaIndexType, td_index_unsupported_methods), (PeriodIndexType,
        period_index_unsupported_methods), (BinaryIndexType,
        binary_index_unsupported_methods), (StringIndexType,
        string_index_unsupported_methods)]
    for typ, jjqxd__axv in roe__rprx:
        aluqs__bzdf = idx_typ_to_format_str_map[typ]
        for vozh__sdi in jjqxd__axv:
            overload_method(typ, vozh__sdi, no_unliteral=True)(
                create_unsupported_overload(aluqs__bzdf.format(vozh__sdi +
                '()')))
    for typ, wroq__tdj in acy__fwnzw:
        aluqs__bzdf = idx_typ_to_format_str_map[typ]
        for qeahc__calk in wroq__tdj:
            overload_attribute(typ, qeahc__calk, no_unliteral=True)(
                create_unsupported_overload(aluqs__bzdf.format(qeahc__calk)))


_install_index_unsupported()
