""" Implementation of binary operators for the different types.
    Currently implemented operators:
        arith: add, sub, mul, truediv, floordiv, mod, pow
        cmp: lt, le, eq, ne, ge, gt
"""
import operator
import numba
from numba.core import types
from numba.core.imputils import lower_builtin
from numba.core.typing.builtins import machine_ints
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type, datetime_timedelta_type
from bodo.hiframes.datetime_timedelta_ext import datetime_datetime_type, datetime_timedelta_array_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import DatetimeIndexType, HeterogeneousIndexType, is_index_type
from bodo.hiframes.pd_offsets_ext import date_offset_type, month_begin_type, month_end_type, week_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_tz_naive_type
from bodo.hiframes.series_impl import SeriesType
from bodo.hiframes.time_ext import TimeType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.typing import BodoError, is_overload_bool, is_str_arr_type, is_timedelta_type


class SeriesCmpOpTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        lhs, rhs = args
        if cmp_timeseries(lhs, rhs) or (isinstance(lhs, DataFrameType) or
            isinstance(rhs, DataFrameType)) or not (isinstance(lhs,
            SeriesType) or isinstance(rhs, SeriesType)):
            return
        if is_cmp_tz_mismatch(lhs, rhs):
            cksze__msiub, gfy__nqfr = get_series_tz(lhs)
            ibynv__mnabm, gfy__nqfr = get_series_tz(rhs)
            raise BodoError(
                f'{numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} with two Timestamps requires both Timestamps share the same timezone. '
                 +
                f'Argument 0 has timezone {cksze__msiub} and argument 1 has timezone {ibynv__mnabm}. '
                 +
                'To compare these values please convert to timezone naive with ts.tz_convert(None).'
                )
        rank__hjhy = lhs.data if isinstance(lhs, SeriesType) else lhs
        zrz__dgbzt = rhs.data if isinstance(rhs, SeriesType) else rhs
        if rank__hjhy in (bodo.pd_timestamp_tz_naive_type, bodo.
            pd_timedelta_type) and zrz__dgbzt.dtype in (bodo.datetime64ns,
            bodo.timedelta64ns):
            rank__hjhy = zrz__dgbzt.dtype
        elif zrz__dgbzt in (bodo.pd_timestamp_tz_naive_type, bodo.
            pd_timedelta_type) and rank__hjhy.dtype in (bodo.datetime64ns,
            bodo.timedelta64ns):
            zrz__dgbzt = rank__hjhy.dtype
        wgin__eccpr = rank__hjhy, zrz__dgbzt
        fpn__dja = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            yogp__wpk = self.context.resolve_function_type(self.key,
                wgin__eccpr, {}).return_type
        except Exception as ftk__ahudn:
            raise BodoError(fpn__dja)
        if is_overload_bool(yogp__wpk):
            raise BodoError(fpn__dja)
        dpnpt__kxma = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        iimz__gkuu = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        jyrb__wyt = types.bool_
        qdhrs__gapnv = SeriesType(jyrb__wyt, yogp__wpk, dpnpt__kxma, iimz__gkuu
            )
        return qdhrs__gapnv(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        luym__albo = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if luym__albo is None:
            luym__albo = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, luym__albo, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        rank__hjhy = lhs.data if isinstance(lhs, SeriesType) else lhs
        zrz__dgbzt = rhs.data if isinstance(rhs, SeriesType) else rhs
        wgin__eccpr = rank__hjhy, zrz__dgbzt
        fpn__dja = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            yogp__wpk = self.context.resolve_function_type(self.key,
                wgin__eccpr, {}).return_type
        except Exception as zwpv__dcnr:
            raise BodoError(fpn__dja)
        dpnpt__kxma = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        iimz__gkuu = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        jyrb__wyt = yogp__wpk.dtype
        qdhrs__gapnv = SeriesType(jyrb__wyt, yogp__wpk, dpnpt__kxma, iimz__gkuu
            )
        return qdhrs__gapnv(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        luym__albo = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if luym__albo is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                luym__albo = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, luym__albo, sig, args)
    return lower_and_or_impl


def overload_add_operator_scalars(lhs, rhs):
    if lhs == week_type or rhs == week_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_week_offset_type(lhs, rhs))
    if lhs == month_begin_type or rhs == month_begin_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_begin_offset_type(lhs, rhs))
    if lhs == month_end_type or rhs == month_end_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_end_offset_type(lhs, rhs))
    if lhs == date_offset_type or rhs == date_offset_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_date_offset_type(lhs, rhs))
    if add_timestamp(lhs, rhs):
        return bodo.hiframes.pd_timestamp_ext.overload_add_operator_timestamp(
            lhs, rhs)
    if add_dt_td_and_dt_date(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_add_operator_datetime_date(lhs, rhs))
    if add_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_add_operator_datetime_timedelta(lhs, rhs))
    raise_error_if_not_numba_supported(operator.add, lhs, rhs)


def overload_sub_operator_scalars(lhs, rhs):
    if sub_offset_to_datetime_or_timestamp(lhs, rhs):
        return bodo.hiframes.pd_offsets_ext.overload_sub_operator_offsets(lhs,
            rhs)
    if (isinstance(lhs, bodo.PandasTimestampType) and rhs in (
        datetime_timedelta_type, pd_timedelta_type) or lhs ==
        pd_timestamp_tz_naive_type and rhs == pd_timestamp_tz_naive_type):
        return bodo.hiframes.pd_timestamp_ext.overload_sub_operator_timestamp(
            lhs, rhs)
    if sub_dt_or_td(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_sub_operator_datetime_date(lhs, rhs))
    if sub_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_sub_operator_datetime_timedelta(lhs, rhs))
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
        return (bodo.hiframes.datetime_datetime_ext.
            overload_sub_operator_datetime_datetime(lhs, rhs))
    raise_error_if_not_numba_supported(operator.sub, lhs, rhs)


def create_overload_arith_op(op):

    def overload_arith_operator(lhs, rhs):
        if op not in [operator.add, operator.sub]:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
                f'{op} operator')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
                f'{op} operator')
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if time_series_operation(lhs, rhs) and op in [operator.add,
            operator.sub]:
            return bodo.hiframes.series_dt_impl.create_bin_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return bodo.hiframes.series_impl.create_binary_op_overload(op)(lhs,
                rhs)
        if sub_dt_index_and_timestamp(lhs, rhs) and op == operator.sub:
            return (bodo.hiframes.pd_index_ext.
                overload_sub_operator_datetime_index(lhs, rhs))
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if args_td_and_int_array(lhs, rhs):
            return bodo.libs.int_arr_ext.get_int_array_op_pd_td(op)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, FloatingArrayType) or isinstance(rhs,
            FloatingArrayType):
            return bodo.libs.float_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if op == operator.add and (is_str_arr_type(lhs) or types.unliteral(
            lhs) == string_type):
            return bodo.libs.str_arr_ext.overload_add_operator_string_array(lhs
                , rhs)
        if op == operator.add and (isinstance(lhs, bodo.DatetimeArrayType) or
            isinstance(rhs, bodo.DatetimeArrayType)):
            return (bodo.libs.pd_datetime_arr_ext.
                overload_add_operator_datetime_arr(lhs, rhs))
        if op == operator.add:
            return overload_add_operator_scalars(lhs, rhs)
        if op == operator.sub:
            return overload_sub_operator_scalars(lhs, rhs)
        if op == operator.mul:
            if mul_timedelta_and_int(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mul_operator_timedelta(lhs, rhs))
            if mul_string_arr_and_int(lhs, rhs):
                return bodo.libs.str_arr_ext.overload_mul_operator_str_arr(lhs,
                    rhs)
            if mul_date_offset_and_int(lhs, rhs):
                return (bodo.hiframes.pd_offsets_ext.
                    overload_mul_date_offset_types(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op in [operator.truediv, operator.floordiv]:
            if div_timedelta_and_int(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_pd_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_pd_timedelta(lhs, rhs))
            if div_datetime_timedelta(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_dt_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_dt_timedelta(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.mod:
            if mod_timedeltas(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mod_operator_timedeltas(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.pow:
            raise_error_if_not_numba_supported(op, lhs, rhs)
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_arith_operator


def create_overload_cmp_operator(op):

    def overload_cmp_operator(lhs, rhs):
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
                f'{op} operator')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
                f'{op} operator')
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if cmp_timeseries(lhs, rhs):
            return bodo.hiframes.series_dt_impl.create_cmp_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return
        if isinstance(lhs, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType
            ) or isinstance(rhs, bodo.libs.pd_datetime_arr_ext.
            DatetimeArrayType):
            return bodo.libs.pd_datetime_arr_ext.create_cmp_op_overload_arr(op
                )(lhs, rhs)
        if isinstance(lhs, types.Array
            ) and lhs.dtype == bodo.datetime64ns and rhs in (
            datetime_date_array_type, datetime_date_type) or lhs in (
            datetime_date_array_type, datetime_date_type) and isinstance(rhs,
            types.Array) and rhs.dtype == bodo.datetime64ns:
            return (bodo.hiframes.datetime_date_ext.
                create_datetime_array_date_cmp_op_overload(op)(lhs, rhs))
        if lhs == datetime_date_array_type or rhs == datetime_date_array_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload_arr(
                op)(lhs, rhs)
        if (lhs == datetime_timedelta_array_type or rhs ==
            datetime_timedelta_array_type):
            luym__albo = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return luym__albo(lhs, rhs)
        if is_str_arr_type(lhs) or is_str_arr_type(rhs):
            return bodo.libs.str_arr_ext.create_binary_op_overload(op)(lhs, rhs
                )
        if isinstance(lhs, Decimal128Type) and isinstance(rhs, Decimal128Type):
            return bodo.libs.decimal_arr_ext.decimal_create_cmp_op_overload(op
                )(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, FloatingArrayType) or isinstance(rhs,
            FloatingArrayType):
            return bodo.libs.float_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if binary_array_cmp(lhs, rhs):
            return bodo.libs.binary_arr_ext.create_binary_cmp_op_overload(op)(
                lhs, rhs)
        if cmp_dt_index_to_string(lhs, rhs):
            return bodo.hiframes.pd_index_ext.overload_binop_dti_str(op)(lhs,
                rhs)
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if lhs == datetime_date_type and rhs == datetime_date_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload(op)(
                lhs, rhs)
        if isinstance(lhs, TimeType) and isinstance(rhs, TimeType):
            return bodo.hiframes.time_ext.create_cmp_op_overload(op)(lhs, rhs)
        if can_cmp_date_datetime(lhs, rhs, op):
            return (bodo.hiframes.datetime_date_ext.
                create_datetime_date_cmp_op_overload(op)(lhs, rhs))
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
            return bodo.hiframes.datetime_datetime_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:
            return bodo.hiframes.datetime_timedelta_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if cmp_timedeltas(lhs, rhs):
            luym__albo = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return luym__albo(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    fezve__rfz = lhs == datetime_timedelta_type and rhs == datetime_date_type
    kpq__vksyz = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return fezve__rfz or kpq__vksyz


def add_timestamp(lhs, rhs):
    oyczz__vze = isinstance(lhs, bodo.PandasTimestampType
        ) and is_timedelta_type(rhs)
    syisw__fcfix = is_timedelta_type(lhs) and isinstance(rhs, bodo.
        PandasTimestampType)
    return oyczz__vze or syisw__fcfix


def add_datetime_and_timedeltas(lhs, rhs):
    kcmic__xyel = [datetime_timedelta_type, pd_timedelta_type]
    npy__hxdk = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    lkk__bmsl = lhs in kcmic__xyel and rhs in kcmic__xyel
    ximme__zco = (lhs == datetime_datetime_type and rhs in kcmic__xyel or 
        rhs == datetime_datetime_type and lhs in kcmic__xyel)
    return lkk__bmsl or ximme__zco


def mul_string_arr_and_int(lhs, rhs):
    zrz__dgbzt = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    rank__hjhy = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return zrz__dgbzt or rank__hjhy


def mul_timedelta_and_int(lhs, rhs):
    fezve__rfz = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    kpq__vksyz = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return fezve__rfz or kpq__vksyz


def mul_date_offset_and_int(lhs, rhs):
    cjy__ogpz = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    plcrj__zqx = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return cjy__ogpz or plcrj__zqx


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    kav__rsup = [datetime_datetime_type, datetime_date_type,
        pd_timestamp_tz_naive_type]
    tz_aware_classes = bodo.PandasTimestampType,
    gjedk__luhc = week_type, month_begin_type, month_end_type
    mys__hzcip = date_offset_type,
    return rhs in gjedk__luhc and isinstance(lhs, tz_aware_classes) or (rhs in
        mys__hzcip or rhs in gjedk__luhc) and lhs in kav__rsup


def sub_dt_index_and_timestamp(lhs, rhs):
    tnyr__kfxdp = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_tz_naive_type
    cqwy__namin = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_tz_naive_type
    return tnyr__kfxdp or cqwy__namin


def sub_dt_or_td(lhs, rhs):
    mhv__jvk = lhs == datetime_date_type and rhs == datetime_timedelta_type
    gbuy__eyu = lhs == datetime_date_type and rhs == datetime_date_type
    anlt__iim = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return mhv__jvk or gbuy__eyu or anlt__iim


def sub_datetime_and_timedeltas(lhs, rhs):
    vdwm__rzv = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    vpltu__ojvg = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return vdwm__rzv or vpltu__ojvg


def div_timedelta_and_int(lhs, rhs):
    lkk__bmsl = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    zlxca__ggp = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return lkk__bmsl or zlxca__ggp


def div_datetime_timedelta(lhs, rhs):
    lkk__bmsl = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    zlxca__ggp = lhs == datetime_timedelta_type and rhs == types.int64
    return lkk__bmsl or zlxca__ggp


def mod_timedeltas(lhs, rhs):
    ttr__mfhyt = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    nmo__rpyko = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return ttr__mfhyt or nmo__rpyko


def cmp_dt_index_to_string(lhs, rhs):
    tnyr__kfxdp = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    cqwy__namin = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return tnyr__kfxdp or cqwy__namin


def cmp_timestamp_or_date(lhs, rhs):
    kjm__uiyq = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType
        ) and rhs == bodo.hiframes.datetime_date_ext.datetime_date_type
    zhheo__hcbg = (lhs == bodo.hiframes.datetime_date_ext.
        datetime_date_type and isinstance(rhs, bodo.hiframes.
        pd_timestamp_ext.PandasTimestampType))
    lrtju__ijz = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType) and isinstance(rhs, bodo.hiframes.
        pd_timestamp_ext.PandasTimestampType)
    wihm__aaopn = (lhs == pd_timestamp_tz_naive_type and rhs == bodo.
        datetime64ns)
    raxb__hbb = rhs == pd_timestamp_tz_naive_type and lhs == bodo.datetime64ns
    return kjm__uiyq or zhheo__hcbg or lrtju__ijz or wihm__aaopn or raxb__hbb


def get_series_tz(val):
    if bodo.hiframes.pd_series_ext.is_dt64_series_typ(val):
        if isinstance(val.data, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType
            ):
            hsuck__hxu = val.data.tz
        else:
            hsuck__hxu = None
    elif isinstance(val, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        hsuck__hxu = val.tz
    elif isinstance(val, types.Array) and val.dtype == bodo.datetime64ns:
        hsuck__hxu = None
    elif isinstance(val, bodo.PandasTimestampType):
        hsuck__hxu = val.tz
    elif val == bodo.datetime64ns:
        hsuck__hxu = None
    else:
        return None, False
    return hsuck__hxu, True


def is_cmp_tz_mismatch(lhs, rhs):
    cksze__msiub, bknt__jqso = get_series_tz(lhs)
    ibynv__mnabm, xaoi__acnb = get_series_tz(rhs)
    return bknt__jqso and xaoi__acnb and cksze__msiub != ibynv__mnabm


def cmp_timeseries(lhs, rhs):
    dgsdb__ndfs = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type)
    ogt__vfcwx = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type)
    qajn__yehuq = (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and 
        rhs.dtype == bodo.datetime64ns and lhs == bodo.hiframes.
        pd_timestamp_ext.pd_timestamp_tz_naive_type or bodo.hiframes.
        pd_series_ext.is_dt64_series_typ(lhs) and lhs.dtype == bodo.
        datetime64ns and rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_tz_naive_type)
    myce__hpxgr = dgsdb__ndfs or ogt__vfcwx or qajn__yehuq
    mmvd__qyb = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    qesx__chdx = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    atoo__eqfw = mmvd__qyb or qesx__chdx
    return myce__hpxgr or atoo__eqfw


def cmp_timedeltas(lhs, rhs):
    lkk__bmsl = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in lkk__bmsl and rhs in lkk__bmsl


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    qhcp__gxlsz = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_tz_naive_type]
    return qhcp__gxlsz


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    trao__jdnh = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    huwtr__hllz = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    sdrwn__jxpl = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    ovfm__orwhd = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return trao__jdnh or huwtr__hllz or sdrwn__jxpl or ovfm__orwhd


def args_td_and_int_array(lhs, rhs):
    dzuw__rzoe = (isinstance(lhs, IntegerArrayType) or isinstance(lhs,
        types.Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance
        (rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    jpwc__hguiw = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return dzuw__rzoe and jpwc__hguiw


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        kpq__vksyz = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        fezve__rfz = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        qqpcv__mjcv = kpq__vksyz or fezve__rfz
        djzmz__myk = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        dkw__cjtee = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        mauzs__twfh = djzmz__myk or dkw__cjtee
        obxlm__lcefe = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        uoa__cyr = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        esea__nal = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        ohvh__nkc = obxlm__lcefe or uoa__cyr or esea__nal
        jokl__ebl = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        rrd__cthqy = isinstance(lhs, tys) or isinstance(rhs, tys)
        lloy__kxp = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return (qqpcv__mjcv or mauzs__twfh or ohvh__nkc or jokl__ebl or
            rrd__cthqy or lloy__kxp)
    if op == operator.pow:
        syz__hvvy = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        imu__tnwie = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        esea__nal = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        lloy__kxp = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return syz__hvvy or imu__tnwie or esea__nal or lloy__kxp
    if op == operator.floordiv:
        uoa__cyr = lhs in types.real_domain and rhs in types.real_domain
        obxlm__lcefe = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        zar__hoobi = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        lkk__bmsl = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        lloy__kxp = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return uoa__cyr or obxlm__lcefe or zar__hoobi or lkk__bmsl or lloy__kxp
    if op == operator.truediv:
        ymjs__yrxvh = lhs in machine_ints and rhs in machine_ints
        uoa__cyr = lhs in types.real_domain and rhs in types.real_domain
        esea__nal = lhs in types.complex_domain and rhs in types.complex_domain
        obxlm__lcefe = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        zar__hoobi = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        kgp__hag = isinstance(lhs, types.Complex) and isinstance(rhs, types
            .Complex)
        lkk__bmsl = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        lloy__kxp = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return (ymjs__yrxvh or uoa__cyr or esea__nal or obxlm__lcefe or
            zar__hoobi or kgp__hag or lkk__bmsl or lloy__kxp)
    if op == operator.mod:
        ymjs__yrxvh = lhs in machine_ints and rhs in machine_ints
        uoa__cyr = lhs in types.real_domain and rhs in types.real_domain
        obxlm__lcefe = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        zar__hoobi = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        lloy__kxp = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return (ymjs__yrxvh or uoa__cyr or obxlm__lcefe or zar__hoobi or
            lloy__kxp)
    if op == operator.add or op == operator.sub:
        qqpcv__mjcv = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        fak__btajc = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        ljaul__teyc = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        aycu__prxr = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        obxlm__lcefe = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        uoa__cyr = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        esea__nal = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        ohvh__nkc = obxlm__lcefe or uoa__cyr or esea__nal
        lloy__kxp = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        pxsqd__wuza = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        jokl__ebl = isinstance(lhs, types.List) and isinstance(rhs, types.List)
        eflbo__fxyt = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        ekmv__zqy = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        mufq__dzluh = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        cqzug__pqk = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        wigvz__qnen = eflbo__fxyt or ekmv__zqy or mufq__dzluh or cqzug__pqk
        mauzs__twfh = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        wwxn__tto = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        zhlek__zqr = mauzs__twfh or wwxn__tto
        ovide__mrlut = lhs == types.NPTimedelta and rhs == types.NPDatetime
        jgik__ycq = (pxsqd__wuza or jokl__ebl or wigvz__qnen or zhlek__zqr or
            ovide__mrlut)
        daw__tkp = op == operator.add and jgik__ycq
        return (qqpcv__mjcv or fak__btajc or ljaul__teyc or aycu__prxr or
            ohvh__nkc or lloy__kxp or daw__tkp)


def cmp_op_supported_by_numba(lhs, rhs):
    lloy__kxp = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    jokl__ebl = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    qqpcv__mjcv = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    hbt__iim = isinstance(lhs, types.NPDatetime) and isinstance(rhs, types.
        NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    mauzs__twfh = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    pxsqd__wuza = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
        types.BaseTuple)
    aycu__prxr = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    ohvh__nkc = isinstance(lhs, types.Number) and isinstance(rhs, types.Number)
    scw__jjs = isinstance(lhs, types.Boolean) and isinstance(rhs, types.Boolean
        )
    mye__gma = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    jutst__zuv = isinstance(lhs, types.DictType) and isinstance(rhs, types.
        DictType)
    uxuc__wxrv = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    hxakm__plun = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (jokl__ebl or qqpcv__mjcv or hbt__iim or mauzs__twfh or
        pxsqd__wuza or aycu__prxr or ohvh__nkc or scw__jjs or mye__gma or
        jutst__zuv or lloy__kxp or uxuc__wxrv or hxakm__plun)


def raise_error_if_not_numba_supported(op, lhs, rhs):
    if arith_op_supported_by_numba(op, lhs, rhs):
        return
    raise BodoError(
        f'{op} operator not supported for data types {lhs} and {rhs}.')


def _install_series_and_or():
    for op in (operator.or_, operator.and_):
        infer_global(op)(SeriesAndOrTyper)
        lower_impl = lower_series_and_or(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)


_install_series_and_or()


def _install_cmp_ops():
    for op in (operator.lt, operator.eq, operator.ne, operator.ge, operator
        .gt, operator.le):
        infer_global(op)(SeriesCmpOpTemplate)
        lower_impl = series_cmp_op_lower(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)
        cry__hia = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(cry__hia)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        cry__hia = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(cry__hia)


install_arith_ops()
