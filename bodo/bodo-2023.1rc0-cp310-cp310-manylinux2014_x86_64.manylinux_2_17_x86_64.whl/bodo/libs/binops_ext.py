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
            gof__ilxgb, abbk__csdpt = get_series_tz(lhs)
            rywz__ssbu, abbk__csdpt = get_series_tz(rhs)
            raise BodoError(
                f'{numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} with two Timestamps requires both Timestamps share the same timezone. '
                 +
                f'Argument 0 has timezone {gof__ilxgb} and argument 1 has timezone {rywz__ssbu}. '
                 +
                'To compare these values please convert to timezone naive with ts.tz_convert(None).'
                )
        cmd__xevxx = lhs.data if isinstance(lhs, SeriesType) else lhs
        gzu__zmyux = rhs.data if isinstance(rhs, SeriesType) else rhs
        if cmd__xevxx in (bodo.pd_timestamp_tz_naive_type, bodo.
            pd_timedelta_type) and gzu__zmyux.dtype in (bodo.datetime64ns,
            bodo.timedelta64ns):
            cmd__xevxx = gzu__zmyux.dtype
        elif gzu__zmyux in (bodo.pd_timestamp_tz_naive_type, bodo.
            pd_timedelta_type) and cmd__xevxx.dtype in (bodo.datetime64ns,
            bodo.timedelta64ns):
            gzu__zmyux = cmd__xevxx.dtype
        uvag__bsis = cmd__xevxx, gzu__zmyux
        suqa__yrei = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            puec__uhl = self.context.resolve_function_type(self.key,
                uvag__bsis, {}).return_type
        except Exception as xia__xtoc:
            raise BodoError(suqa__yrei)
        if is_overload_bool(puec__uhl):
            raise BodoError(suqa__yrei)
        xnmcl__msw = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        exg__zpg = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        seejx__rpcbg = types.bool_
        bukhp__dmos = SeriesType(seejx__rpcbg, puec__uhl, xnmcl__msw, exg__zpg)
        return bukhp__dmos(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        roay__kcpes = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if roay__kcpes is None:
            roay__kcpes = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, roay__kcpes, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        cmd__xevxx = lhs.data if isinstance(lhs, SeriesType) else lhs
        gzu__zmyux = rhs.data if isinstance(rhs, SeriesType) else rhs
        uvag__bsis = cmd__xevxx, gzu__zmyux
        suqa__yrei = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            puec__uhl = self.context.resolve_function_type(self.key,
                uvag__bsis, {}).return_type
        except Exception as urv__asx:
            raise BodoError(suqa__yrei)
        xnmcl__msw = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        exg__zpg = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        seejx__rpcbg = puec__uhl.dtype
        bukhp__dmos = SeriesType(seejx__rpcbg, puec__uhl, xnmcl__msw, exg__zpg)
        return bukhp__dmos(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        roay__kcpes = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if roay__kcpes is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                roay__kcpes = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, roay__kcpes, sig, args)
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
            roay__kcpes = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return roay__kcpes(lhs, rhs)
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
            roay__kcpes = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return roay__kcpes(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    frxrm__yqy = lhs == datetime_timedelta_type and rhs == datetime_date_type
    xpbdy__lsv = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return frxrm__yqy or xpbdy__lsv


def add_timestamp(lhs, rhs):
    bmqwf__axaas = isinstance(lhs, bodo.PandasTimestampType
        ) and is_timedelta_type(rhs)
    ztpuh__deqpu = is_timedelta_type(lhs) and isinstance(rhs, bodo.
        PandasTimestampType)
    return bmqwf__axaas or ztpuh__deqpu


def add_datetime_and_timedeltas(lhs, rhs):
    roglg__sim = [datetime_timedelta_type, pd_timedelta_type]
    inrq__lms = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    lgsz__tetst = lhs in roglg__sim and rhs in roglg__sim
    dstfv__upu = (lhs == datetime_datetime_type and rhs in roglg__sim or 
        rhs == datetime_datetime_type and lhs in roglg__sim)
    return lgsz__tetst or dstfv__upu


def mul_string_arr_and_int(lhs, rhs):
    gzu__zmyux = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    cmd__xevxx = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return gzu__zmyux or cmd__xevxx


def mul_timedelta_and_int(lhs, rhs):
    frxrm__yqy = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    xpbdy__lsv = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return frxrm__yqy or xpbdy__lsv


def mul_date_offset_and_int(lhs, rhs):
    uffry__tpjv = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    yrb__hiwc = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return uffry__tpjv or yrb__hiwc


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    cmjre__vxrbt = [datetime_datetime_type, datetime_date_type,
        pd_timestamp_tz_naive_type]
    tz_aware_classes = bodo.PandasTimestampType,
    mqt__zet = week_type, month_begin_type, month_end_type
    omcdp__sgj = date_offset_type,
    return rhs in mqt__zet and isinstance(lhs, tz_aware_classes) or (rhs in
        omcdp__sgj or rhs in mqt__zet) and lhs in cmjre__vxrbt


def sub_dt_index_and_timestamp(lhs, rhs):
    hjtrx__fcw = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_tz_naive_type
    yoz__tvgy = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_tz_naive_type
    return hjtrx__fcw or yoz__tvgy


def sub_dt_or_td(lhs, rhs):
    ice__rzfxi = lhs == datetime_date_type and rhs == datetime_timedelta_type
    mhgrc__dqz = lhs == datetime_date_type and rhs == datetime_date_type
    ypu__mjgni = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return ice__rzfxi or mhgrc__dqz or ypu__mjgni


def sub_datetime_and_timedeltas(lhs, rhs):
    qfd__rufix = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    knb__nka = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return qfd__rufix or knb__nka


def div_timedelta_and_int(lhs, rhs):
    lgsz__tetst = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    whlx__kayo = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return lgsz__tetst or whlx__kayo


def div_datetime_timedelta(lhs, rhs):
    lgsz__tetst = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    whlx__kayo = lhs == datetime_timedelta_type and rhs == types.int64
    return lgsz__tetst or whlx__kayo


def mod_timedeltas(lhs, rhs):
    dyus__hzp = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    eus__xnl = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return dyus__hzp or eus__xnl


def cmp_dt_index_to_string(lhs, rhs):
    hjtrx__fcw = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    yoz__tvgy = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return hjtrx__fcw or yoz__tvgy


def cmp_timestamp_or_date(lhs, rhs):
    apxg__fvezk = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType
        ) and rhs == bodo.hiframes.datetime_date_ext.datetime_date_type
    rzwf__hqymh = (lhs == bodo.hiframes.datetime_date_ext.
        datetime_date_type and isinstance(rhs, bodo.hiframes.
        pd_timestamp_ext.PandasTimestampType))
    amef__trx = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType) and isinstance(rhs, bodo.hiframes.
        pd_timestamp_ext.PandasTimestampType)
    wlfwa__bilpt = (lhs == pd_timestamp_tz_naive_type and rhs == bodo.
        datetime64ns)
    hdzks__evy = rhs == pd_timestamp_tz_naive_type and lhs == bodo.datetime64ns
    return (apxg__fvezk or rzwf__hqymh or amef__trx or wlfwa__bilpt or
        hdzks__evy)


def get_series_tz(val):
    if bodo.hiframes.pd_series_ext.is_dt64_series_typ(val):
        if isinstance(val.data, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType
            ):
            sdsxl__hhx = val.data.tz
        else:
            sdsxl__hhx = None
    elif isinstance(val, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        sdsxl__hhx = val.tz
    elif isinstance(val, types.Array) and val.dtype == bodo.datetime64ns:
        sdsxl__hhx = None
    elif isinstance(val, bodo.PandasTimestampType):
        sdsxl__hhx = val.tz
    elif val == bodo.datetime64ns:
        sdsxl__hhx = None
    else:
        return None, False
    return sdsxl__hhx, True


def is_cmp_tz_mismatch(lhs, rhs):
    gof__ilxgb, wslps__qeuo = get_series_tz(lhs)
    rywz__ssbu, akmeh__uahuk = get_series_tz(rhs)
    return wslps__qeuo and akmeh__uahuk and gof__ilxgb != rywz__ssbu


def cmp_timeseries(lhs, rhs):
    dgs__qiojt = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type)
    ndpn__mftvt = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type)
    npf__cqbfy = (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and 
        rhs.dtype == bodo.datetime64ns and lhs == bodo.hiframes.
        pd_timestamp_ext.pd_timestamp_tz_naive_type or bodo.hiframes.
        pd_series_ext.is_dt64_series_typ(lhs) and lhs.dtype == bodo.
        datetime64ns and rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_tz_naive_type)
    trw__irqu = dgs__qiojt or ndpn__mftvt or npf__cqbfy
    imbl__wde = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    pqx__gka = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    alq__dzxd = imbl__wde or pqx__gka
    return trw__irqu or alq__dzxd


def cmp_timedeltas(lhs, rhs):
    lgsz__tetst = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in lgsz__tetst and rhs in lgsz__tetst


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    nni__exwv = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_tz_naive_type]
    return nni__exwv


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    jjd__fzi = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    kcc__zcn = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    adsm__geq = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    igec__xnb = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return jjd__fzi or kcc__zcn or adsm__geq or igec__xnb


def args_td_and_int_array(lhs, rhs):
    ksm__ldlb = (isinstance(lhs, IntegerArrayType) or isinstance(lhs, types
        .Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance(
        rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    nbzh__kvg = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return ksm__ldlb and nbzh__kvg


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        xpbdy__lsv = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        frxrm__yqy = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        sctv__dbv = xpbdy__lsv or frxrm__yqy
        jqoso__cwtoz = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        nte__kvn = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        drryq__jagu = jqoso__cwtoz or nte__kvn
        suezh__hzjaq = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        dptbu__aclu = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        mdeaz__ehpq = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        jaifd__cydd = suezh__hzjaq or dptbu__aclu or mdeaz__ehpq
        bjtmc__ogirs = isinstance(lhs, types.List) and isinstance(rhs,
            types.Integer) or isinstance(lhs, types.Integer) and isinstance(rhs
            , types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        upe__kdiwn = isinstance(lhs, tys) or isinstance(rhs, tys)
        zflzd__clqy = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (sctv__dbv or drryq__jagu or jaifd__cydd or bjtmc__ogirs or
            upe__kdiwn or zflzd__clqy)
    if op == operator.pow:
        gtu__rpx = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        rqbdi__qsdng = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        mdeaz__ehpq = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        zflzd__clqy = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return gtu__rpx or rqbdi__qsdng or mdeaz__ehpq or zflzd__clqy
    if op == operator.floordiv:
        dptbu__aclu = lhs in types.real_domain and rhs in types.real_domain
        suezh__hzjaq = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        zzn__gbq = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        lgsz__tetst = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        zflzd__clqy = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (dptbu__aclu or suezh__hzjaq or zzn__gbq or lgsz__tetst or
            zflzd__clqy)
    if op == operator.truediv:
        jnu__sqs = lhs in machine_ints and rhs in machine_ints
        dptbu__aclu = lhs in types.real_domain and rhs in types.real_domain
        mdeaz__ehpq = (lhs in types.complex_domain and rhs in types.
            complex_domain)
        suezh__hzjaq = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        zzn__gbq = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        mwec__yql = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        lgsz__tetst = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        zflzd__clqy = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (jnu__sqs or dptbu__aclu or mdeaz__ehpq or suezh__hzjaq or
            zzn__gbq or mwec__yql or lgsz__tetst or zflzd__clqy)
    if op == operator.mod:
        jnu__sqs = lhs in machine_ints and rhs in machine_ints
        dptbu__aclu = lhs in types.real_domain and rhs in types.real_domain
        suezh__hzjaq = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        zzn__gbq = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        zflzd__clqy = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (jnu__sqs or dptbu__aclu or suezh__hzjaq or zzn__gbq or
            zflzd__clqy)
    if op == operator.add or op == operator.sub:
        sctv__dbv = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        fhl__aalmy = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        kfj__qld = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        grg__aapcu = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        suezh__hzjaq = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        dptbu__aclu = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        mdeaz__ehpq = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        jaifd__cydd = suezh__hzjaq or dptbu__aclu or mdeaz__ehpq
        zflzd__clqy = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        aaw__kxonc = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        bjtmc__ogirs = isinstance(lhs, types.List) and isinstance(rhs,
            types.List)
        pfepg__qoncu = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs
            , types.UnicodeType)
        cjdrj__kttf = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        gcb__wtpka = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        suype__werk = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        ocpp__acf = pfepg__qoncu or cjdrj__kttf or gcb__wtpka or suype__werk
        drryq__jagu = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        poos__wam = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        upp__koadk = drryq__jagu or poos__wam
        yudwd__gmcx = lhs == types.NPTimedelta and rhs == types.NPDatetime
        kflun__kak = (aaw__kxonc or bjtmc__ogirs or ocpp__acf or upp__koadk or
            yudwd__gmcx)
        zvf__tjmwi = op == operator.add and kflun__kak
        return (sctv__dbv or fhl__aalmy or kfj__qld or grg__aapcu or
            jaifd__cydd or zflzd__clqy or zvf__tjmwi)


def cmp_op_supported_by_numba(lhs, rhs):
    zflzd__clqy = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    bjtmc__ogirs = isinstance(lhs, types.ListType) and isinstance(rhs,
        types.ListType)
    sctv__dbv = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    beu__uzzs = isinstance(lhs, types.NPDatetime) and isinstance(rhs, types
        .NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    drryq__jagu = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    aaw__kxonc = isinstance(lhs, types.BaseTuple) and isinstance(rhs, types
        .BaseTuple)
    grg__aapcu = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    jaifd__cydd = isinstance(lhs, types.Number) and isinstance(rhs, types.
        Number)
    ckthe__vdsj = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    cnxh__roue = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    njk__etlo = isinstance(lhs, types.DictType) and isinstance(rhs, types.
        DictType)
    bxdqs__fqz = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    dfw__uoco = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (bjtmc__ogirs or sctv__dbv or beu__uzzs or drryq__jagu or
        aaw__kxonc or grg__aapcu or jaifd__cydd or ckthe__vdsj or
        cnxh__roue or njk__etlo or zflzd__clqy or bxdqs__fqz or dfw__uoco)


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
        uza__jbfsm = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(uza__jbfsm)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        uza__jbfsm = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(uza__jbfsm)


install_arith_ops()
