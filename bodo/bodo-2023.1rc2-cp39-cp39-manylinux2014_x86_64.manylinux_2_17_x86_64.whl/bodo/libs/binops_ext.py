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
            bez__ijr, nfiyt__lzqk = get_series_tz(lhs)
            yta__qxlq, nfiyt__lzqk = get_series_tz(rhs)
            raise BodoError(
                f'{numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} with two Timestamps requires both Timestamps share the same timezone. '
                 +
                f'Argument 0 has timezone {bez__ijr} and argument 1 has timezone {yta__qxlq}. '
                 +
                'To compare these values please convert to timezone naive with ts.tz_convert(None).'
                )
        tmnn__wfhkl = lhs.data if isinstance(lhs, SeriesType) else lhs
        eergt__oebyv = rhs.data if isinstance(rhs, SeriesType) else rhs
        if tmnn__wfhkl in (bodo.pd_timestamp_tz_naive_type, bodo.
            pd_timedelta_type) and eergt__oebyv.dtype in (bodo.datetime64ns,
            bodo.timedelta64ns):
            tmnn__wfhkl = eergt__oebyv.dtype
        elif eergt__oebyv in (bodo.pd_timestamp_tz_naive_type, bodo.
            pd_timedelta_type) and tmnn__wfhkl.dtype in (bodo.datetime64ns,
            bodo.timedelta64ns):
            eergt__oebyv = tmnn__wfhkl.dtype
        jigx__tnwsl = tmnn__wfhkl, eergt__oebyv
        vynf__lkbw = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            ibba__uimmc = self.context.resolve_function_type(self.key,
                jigx__tnwsl, {}).return_type
        except Exception as jtx__ytk:
            raise BodoError(vynf__lkbw)
        if is_overload_bool(ibba__uimmc):
            raise BodoError(vynf__lkbw)
        tacd__avmb = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ehs__utvbb = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        smwnm__xajr = types.bool_
        ery__lbfe = SeriesType(smwnm__xajr, ibba__uimmc, tacd__avmb, ehs__utvbb
            )
        return ery__lbfe(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        nnsy__iljnf = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if nnsy__iljnf is None:
            nnsy__iljnf = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, nnsy__iljnf, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        tmnn__wfhkl = lhs.data if isinstance(lhs, SeriesType) else lhs
        eergt__oebyv = rhs.data if isinstance(rhs, SeriesType) else rhs
        jigx__tnwsl = tmnn__wfhkl, eergt__oebyv
        vynf__lkbw = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            ibba__uimmc = self.context.resolve_function_type(self.key,
                jigx__tnwsl, {}).return_type
        except Exception as nrwzn__mks:
            raise BodoError(vynf__lkbw)
        tacd__avmb = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ehs__utvbb = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        smwnm__xajr = ibba__uimmc.dtype
        ery__lbfe = SeriesType(smwnm__xajr, ibba__uimmc, tacd__avmb, ehs__utvbb
            )
        return ery__lbfe(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        nnsy__iljnf = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if nnsy__iljnf is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                nnsy__iljnf = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, nnsy__iljnf, sig, args)
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
            nnsy__iljnf = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return nnsy__iljnf(lhs, rhs)
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
            nnsy__iljnf = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return nnsy__iljnf(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    wks__ontbv = lhs == datetime_timedelta_type and rhs == datetime_date_type
    ejys__aem = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return wks__ontbv or ejys__aem


def add_timestamp(lhs, rhs):
    xqw__kvb = isinstance(lhs, bodo.PandasTimestampType) and is_timedelta_type(
        rhs)
    hmgzx__ejdj = is_timedelta_type(lhs) and isinstance(rhs, bodo.
        PandasTimestampType)
    return xqw__kvb or hmgzx__ejdj


def add_datetime_and_timedeltas(lhs, rhs):
    mnpog__lgow = [datetime_timedelta_type, pd_timedelta_type]
    felju__hsvfn = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    foz__ckv = lhs in mnpog__lgow and rhs in mnpog__lgow
    nvs__fzmz = (lhs == datetime_datetime_type and rhs in mnpog__lgow or 
        rhs == datetime_datetime_type and lhs in mnpog__lgow)
    return foz__ckv or nvs__fzmz


def mul_string_arr_and_int(lhs, rhs):
    eergt__oebyv = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    tmnn__wfhkl = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return eergt__oebyv or tmnn__wfhkl


def mul_timedelta_and_int(lhs, rhs):
    wks__ontbv = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    ejys__aem = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return wks__ontbv or ejys__aem


def mul_date_offset_and_int(lhs, rhs):
    okup__ityhc = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    zdk__pfv = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return okup__ityhc or zdk__pfv


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    cpbjz__hojs = [datetime_datetime_type, datetime_date_type,
        pd_timestamp_tz_naive_type]
    tz_aware_classes = bodo.PandasTimestampType,
    hlu__aii = week_type, month_begin_type, month_end_type
    fzu__jyvdh = date_offset_type,
    return rhs in hlu__aii and isinstance(lhs, tz_aware_classes) or (rhs in
        fzu__jyvdh or rhs in hlu__aii) and lhs in cpbjz__hojs


def sub_dt_index_and_timestamp(lhs, rhs):
    umdz__uku = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_tz_naive_type
    flhtz__ahpmi = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_tz_naive_type
    return umdz__uku or flhtz__ahpmi


def sub_dt_or_td(lhs, rhs):
    egz__rbgkb = lhs == datetime_date_type and rhs == datetime_timedelta_type
    ckx__ivw = lhs == datetime_date_type and rhs == datetime_date_type
    ngrh__tait = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return egz__rbgkb or ckx__ivw or ngrh__tait


def sub_datetime_and_timedeltas(lhs, rhs):
    jcqo__fcr = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    cuxm__wgiug = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return jcqo__fcr or cuxm__wgiug


def div_timedelta_and_int(lhs, rhs):
    foz__ckv = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    pxegw__gvl = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return foz__ckv or pxegw__gvl


def div_datetime_timedelta(lhs, rhs):
    foz__ckv = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    pxegw__gvl = lhs == datetime_timedelta_type and rhs == types.int64
    return foz__ckv or pxegw__gvl


def mod_timedeltas(lhs, rhs):
    btw__gzv = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    irh__ubiww = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return btw__gzv or irh__ubiww


def cmp_dt_index_to_string(lhs, rhs):
    umdz__uku = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    flhtz__ahpmi = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return umdz__uku or flhtz__ahpmi


def cmp_timestamp_or_date(lhs, rhs):
    oird__daxt = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType
        ) and rhs == bodo.hiframes.datetime_date_ext.datetime_date_type
    vxuy__ppln = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        isinstance(rhs, bodo.hiframes.pd_timestamp_ext.PandasTimestampType))
    fxylc__cjzu = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType) and isinstance(rhs, bodo.hiframes.
        pd_timestamp_ext.PandasTimestampType)
    hcxtd__eghy = (lhs == pd_timestamp_tz_naive_type and rhs == bodo.
        datetime64ns)
    kulzk__afsa = (rhs == pd_timestamp_tz_naive_type and lhs == bodo.
        datetime64ns)
    return (oird__daxt or vxuy__ppln or fxylc__cjzu or hcxtd__eghy or
        kulzk__afsa)


def get_series_tz(val):
    if bodo.hiframes.pd_series_ext.is_dt64_series_typ(val):
        if isinstance(val.data, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType
            ):
            amf__eyor = val.data.tz
        else:
            amf__eyor = None
    elif isinstance(val, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        amf__eyor = val.tz
    elif isinstance(val, types.Array) and val.dtype == bodo.datetime64ns:
        amf__eyor = None
    elif isinstance(val, bodo.PandasTimestampType):
        amf__eyor = val.tz
    elif val == bodo.datetime64ns:
        amf__eyor = None
    else:
        return None, False
    return amf__eyor, True


def is_cmp_tz_mismatch(lhs, rhs):
    bez__ijr, owypd__blq = get_series_tz(lhs)
    yta__qxlq, iri__ktob = get_series_tz(rhs)
    return owypd__blq and iri__ktob and bez__ijr != yta__qxlq


def cmp_timeseries(lhs, rhs):
    nghpm__qnat = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type)
    bckdv__dwfo = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type)
    pvnr__vcwnv = (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and 
        rhs.dtype == bodo.datetime64ns and lhs == bodo.hiframes.
        pd_timestamp_ext.pd_timestamp_tz_naive_type or bodo.hiframes.
        pd_series_ext.is_dt64_series_typ(lhs) and lhs.dtype == bodo.
        datetime64ns and rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_tz_naive_type)
    wulss__eke = nghpm__qnat or bckdv__dwfo or pvnr__vcwnv
    xxkg__oyn = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    yqh__zdzr = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    cjy__dwp = xxkg__oyn or yqh__zdzr
    return wulss__eke or cjy__dwp


def cmp_timedeltas(lhs, rhs):
    foz__ckv = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in foz__ckv and rhs in foz__ckv


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    majo__fitfv = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_tz_naive_type]
    return majo__fitfv


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    bypgt__rxqmr = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    xwci__kvs = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    dtje__mhulm = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    sxb__fmj = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return bypgt__rxqmr or xwci__kvs or dtje__mhulm or sxb__fmj


def args_td_and_int_array(lhs, rhs):
    ouxls__bkbeq = (isinstance(lhs, IntegerArrayType) or isinstance(lhs,
        types.Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance
        (rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    hvswa__wph = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return ouxls__bkbeq and hvswa__wph


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        ejys__aem = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        wks__ontbv = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        vsotb__sxsj = ejys__aem or wks__ontbv
        dgto__ghavx = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        deeav__vjc = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        zfd__bhmmu = dgto__ghavx or deeav__vjc
        fidbn__nnsed = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        mjy__atzt = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        gcc__awxn = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        kzkgt__wydee = fidbn__nnsed or mjy__atzt or gcc__awxn
        hgq__uinta = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        mkmv__xvx = isinstance(lhs, tys) or isinstance(rhs, tys)
        qpi__xcrse = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (vsotb__sxsj or zfd__bhmmu or kzkgt__wydee or hgq__uinta or
            mkmv__xvx or qpi__xcrse)
    if op == operator.pow:
        fbt__mzv = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        eqjm__leup = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        gcc__awxn = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        qpi__xcrse = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return fbt__mzv or eqjm__leup or gcc__awxn or qpi__xcrse
    if op == operator.floordiv:
        mjy__atzt = lhs in types.real_domain and rhs in types.real_domain
        fidbn__nnsed = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        jnk__rxvr = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        foz__ckv = isinstance(lhs, types.NPTimedelta) and isinstance(rhs, (
            types.Integer, types.Float, types.NPTimedelta))
        qpi__xcrse = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return mjy__atzt or fidbn__nnsed or jnk__rxvr or foz__ckv or qpi__xcrse
    if op == operator.truediv:
        bsxw__xgina = lhs in machine_ints and rhs in machine_ints
        mjy__atzt = lhs in types.real_domain and rhs in types.real_domain
        gcc__awxn = lhs in types.complex_domain and rhs in types.complex_domain
        fidbn__nnsed = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        jnk__rxvr = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        bxe__wvbj = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        foz__ckv = isinstance(lhs, types.NPTimedelta) and isinstance(rhs, (
            types.Integer, types.Float, types.NPTimedelta))
        qpi__xcrse = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (bsxw__xgina or mjy__atzt or gcc__awxn or fidbn__nnsed or
            jnk__rxvr or bxe__wvbj or foz__ckv or qpi__xcrse)
    if op == operator.mod:
        bsxw__xgina = lhs in machine_ints and rhs in machine_ints
        mjy__atzt = lhs in types.real_domain and rhs in types.real_domain
        fidbn__nnsed = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        jnk__rxvr = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        qpi__xcrse = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (bsxw__xgina or mjy__atzt or fidbn__nnsed or jnk__rxvr or
            qpi__xcrse)
    if op == operator.add or op == operator.sub:
        vsotb__sxsj = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        mnoly__hav = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        yodo__gac = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        urfi__jwvcg = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        fidbn__nnsed = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        mjy__atzt = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        gcc__awxn = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        kzkgt__wydee = fidbn__nnsed or mjy__atzt or gcc__awxn
        qpi__xcrse = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        qoewx__uovc = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        hgq__uinta = isinstance(lhs, types.List) and isinstance(rhs, types.List
            )
        gjd__lip = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        cmwqh__pwkl = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        lrvk__kjz = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        guc__pmrda = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        stlts__imw = gjd__lip or cmwqh__pwkl or lrvk__kjz or guc__pmrda
        zfd__bhmmu = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        gpjz__wtdyy = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        dya__gaxt = zfd__bhmmu or gpjz__wtdyy
        yicv__erov = lhs == types.NPTimedelta and rhs == types.NPDatetime
        heb__qgg = (qoewx__uovc or hgq__uinta or stlts__imw or dya__gaxt or
            yicv__erov)
        vhrjp__qcjxi = op == operator.add and heb__qgg
        return (vsotb__sxsj or mnoly__hav or yodo__gac or urfi__jwvcg or
            kzkgt__wydee or qpi__xcrse or vhrjp__qcjxi)


def cmp_op_supported_by_numba(lhs, rhs):
    qpi__xcrse = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    hgq__uinta = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    vsotb__sxsj = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    pzly__xynde = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
        types.NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    zfd__bhmmu = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    qoewx__uovc = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
        types.BaseTuple)
    urfi__jwvcg = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    kzkgt__wydee = isinstance(lhs, types.Number) and isinstance(rhs, types.
        Number)
    kmoj__dhugw = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    mzkcn__tit = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    mpdk__vka = isinstance(lhs, types.DictType) and isinstance(rhs, types.
        DictType)
    aafgl__ild = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    wbsds__jgrd = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (hgq__uinta or vsotb__sxsj or pzly__xynde or zfd__bhmmu or
        qoewx__uovc or urfi__jwvcg or kzkgt__wydee or kmoj__dhugw or
        mzkcn__tit or mpdk__vka or qpi__xcrse or aafgl__ild or wbsds__jgrd)


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
        nzxt__ikqy = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(nzxt__ikqy)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        nzxt__ikqy = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(nzxt__ikqy)


install_arith_ops()
