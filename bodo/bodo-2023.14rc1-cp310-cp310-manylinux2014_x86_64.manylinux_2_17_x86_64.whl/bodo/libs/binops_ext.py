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
            xryb__mdh, hfchk__eim = get_series_tz(lhs)
            kfheg__vdedo, hfchk__eim = get_series_tz(rhs)
            raise BodoError(
                f'{numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} with two Timestamps requires both Timestamps share the same timezone. '
                 +
                f'Argument 0 has timezone {xryb__mdh} and argument 1 has timezone {kfheg__vdedo}. '
                 +
                'To compare these values please convert to timezone naive with ts.tz_convert(None).'
                )
        nvc__mld = lhs.data if isinstance(lhs, SeriesType) else lhs
        jkbg__vgipq = rhs.data if isinstance(rhs, SeriesType) else rhs
        if nvc__mld in (bodo.pd_timestamp_tz_naive_type, bodo.pd_timedelta_type
            ) and jkbg__vgipq.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            nvc__mld = jkbg__vgipq.dtype
        elif jkbg__vgipq in (bodo.pd_timestamp_tz_naive_type, bodo.
            pd_timedelta_type) and nvc__mld.dtype in (bodo.datetime64ns,
            bodo.timedelta64ns):
            jkbg__vgipq = nvc__mld.dtype
        erdxk__yuq = nvc__mld, jkbg__vgipq
        exh__nytip = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            uorni__anw = self.context.resolve_function_type(self.key,
                erdxk__yuq, {}).return_type
        except Exception as eakes__avvqz:
            raise BodoError(exh__nytip)
        if is_overload_bool(uorni__anw):
            raise BodoError(exh__nytip)
        bft__rsw = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ltvc__tbpho = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        lzrmz__exki = types.bool_
        nskz__znye = SeriesType(lzrmz__exki, uorni__anw, bft__rsw, ltvc__tbpho)
        return nskz__znye(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        eqbv__sqaad = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if eqbv__sqaad is None:
            eqbv__sqaad = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, eqbv__sqaad, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        nvc__mld = lhs.data if isinstance(lhs, SeriesType) else lhs
        jkbg__vgipq = rhs.data if isinstance(rhs, SeriesType) else rhs
        erdxk__yuq = nvc__mld, jkbg__vgipq
        exh__nytip = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            uorni__anw = self.context.resolve_function_type(self.key,
                erdxk__yuq, {}).return_type
        except Exception as bfxiu__riz:
            raise BodoError(exh__nytip)
        bft__rsw = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ltvc__tbpho = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        lzrmz__exki = uorni__anw.dtype
        nskz__znye = SeriesType(lzrmz__exki, uorni__anw, bft__rsw, ltvc__tbpho)
        return nskz__znye(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        eqbv__sqaad = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if eqbv__sqaad is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                eqbv__sqaad = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, eqbv__sqaad, sig, args)
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
            eqbv__sqaad = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return eqbv__sqaad(lhs, rhs)
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
            eqbv__sqaad = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return eqbv__sqaad(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    uglv__gpces = lhs == datetime_timedelta_type and rhs == datetime_date_type
    pcgs__jet = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return uglv__gpces or pcgs__jet


def add_timestamp(lhs, rhs):
    vcp__evy = isinstance(lhs, bodo.PandasTimestampType) and is_timedelta_type(
        rhs)
    njcu__mvru = is_timedelta_type(lhs) and isinstance(rhs, bodo.
        PandasTimestampType)
    return vcp__evy or njcu__mvru


def add_datetime_and_timedeltas(lhs, rhs):
    wxvon__fhr = [datetime_timedelta_type, pd_timedelta_type]
    nphk__nsv = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    qwb__azxqb = lhs in wxvon__fhr and rhs in wxvon__fhr
    ifb__apc = (lhs == datetime_datetime_type and rhs in wxvon__fhr or rhs ==
        datetime_datetime_type and lhs in wxvon__fhr)
    return qwb__azxqb or ifb__apc


def mul_string_arr_and_int(lhs, rhs):
    jkbg__vgipq = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    nvc__mld = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return jkbg__vgipq or nvc__mld


def mul_timedelta_and_int(lhs, rhs):
    uglv__gpces = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    pcgs__jet = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return uglv__gpces or pcgs__jet


def mul_date_offset_and_int(lhs, rhs):
    eksaf__eluxl = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    pjh__bqoyo = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return eksaf__eluxl or pjh__bqoyo


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    zqf__qyyu = [datetime_datetime_type, datetime_date_type,
        pd_timestamp_tz_naive_type]
    tz_aware_classes = bodo.PandasTimestampType,
    djkv__geqx = week_type, month_begin_type, month_end_type
    fikvc__bahc = date_offset_type,
    return rhs in djkv__geqx and isinstance(lhs, tz_aware_classes) or (rhs in
        fikvc__bahc or rhs in djkv__geqx) and lhs in zqf__qyyu


def sub_dt_index_and_timestamp(lhs, rhs):
    yzd__xszf = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_tz_naive_type
    mgfd__tejr = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_tz_naive_type
    return yzd__xszf or mgfd__tejr


def sub_dt_or_td(lhs, rhs):
    xmyf__ghtw = lhs == datetime_date_type and rhs == datetime_timedelta_type
    dmf__iyju = lhs == datetime_date_type and rhs == datetime_date_type
    zicbj__kgjns = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return xmyf__ghtw or dmf__iyju or zicbj__kgjns


def sub_datetime_and_timedeltas(lhs, rhs):
    sei__dtv = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    viwl__fhvoq = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return sei__dtv or viwl__fhvoq


def div_timedelta_and_int(lhs, rhs):
    qwb__azxqb = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    mpp__ofom = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return qwb__azxqb or mpp__ofom


def div_datetime_timedelta(lhs, rhs):
    qwb__azxqb = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    mpp__ofom = lhs == datetime_timedelta_type and rhs == types.int64
    return qwb__azxqb or mpp__ofom


def mod_timedeltas(lhs, rhs):
    pmc__ulvhk = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    mwdo__wgl = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return pmc__ulvhk or mwdo__wgl


def cmp_dt_index_to_string(lhs, rhs):
    yzd__xszf = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    mgfd__tejr = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return yzd__xszf or mgfd__tejr


def cmp_timestamp_or_date(lhs, rhs):
    lhb__ljf = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType
        ) and rhs == bodo.hiframes.datetime_date_ext.datetime_date_type
    kkh__zoz = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        isinstance(rhs, bodo.hiframes.pd_timestamp_ext.PandasTimestampType))
    yzyuk__qvbtk = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType) and isinstance(rhs, bodo.hiframes.
        pd_timestamp_ext.PandasTimestampType)
    yyosz__kpo = lhs == pd_timestamp_tz_naive_type and rhs == bodo.datetime64ns
    cias__jtp = rhs == pd_timestamp_tz_naive_type and lhs == bodo.datetime64ns
    return lhb__ljf or kkh__zoz or yzyuk__qvbtk or yyosz__kpo or cias__jtp


def get_series_tz(val):
    if bodo.hiframes.pd_series_ext.is_dt64_series_typ(val):
        if isinstance(val.data, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType
            ):
            hfgpy__zdx = val.data.tz
        else:
            hfgpy__zdx = None
    elif isinstance(val, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        hfgpy__zdx = val.tz
    elif isinstance(val, types.Array) and val.dtype == bodo.datetime64ns:
        hfgpy__zdx = None
    elif isinstance(val, bodo.PandasTimestampType):
        hfgpy__zdx = val.tz
    elif val == bodo.datetime64ns:
        hfgpy__zdx = None
    else:
        return None, False
    return hfgpy__zdx, True


def is_cmp_tz_mismatch(lhs, rhs):
    xryb__mdh, auc__qcyw = get_series_tz(lhs)
    kfheg__vdedo, ede__vwc = get_series_tz(rhs)
    return auc__qcyw and ede__vwc and xryb__mdh != kfheg__vdedo


def cmp_timeseries(lhs, rhs):
    zsya__uzgqx = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type)
    qghzm__oprnl = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (
        bodo.utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs
        .str_ext.string_type)
    ubb__ycko = (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and 
        rhs.dtype == bodo.datetime64ns and lhs == bodo.hiframes.
        pd_timestamp_ext.pd_timestamp_tz_naive_type or bodo.hiframes.
        pd_series_ext.is_dt64_series_typ(lhs) and lhs.dtype == bodo.
        datetime64ns and rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_tz_naive_type)
    kxw__jrx = zsya__uzgqx or qghzm__oprnl or ubb__ycko
    qpq__vfw = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    tqfbm__tbcf = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    lhqx__xtwrp = qpq__vfw or tqfbm__tbcf
    return kxw__jrx or lhqx__xtwrp


def cmp_timedeltas(lhs, rhs):
    qwb__azxqb = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in qwb__azxqb and rhs in qwb__azxqb


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    ekfgz__dlni = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_tz_naive_type]
    return ekfgz__dlni


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    azaa__rhu = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    bpiy__uvca = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    agdk__pui = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    ogh__oyk = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return azaa__rhu or bpiy__uvca or agdk__pui or ogh__oyk


def args_td_and_int_array(lhs, rhs):
    gahhv__bjbc = (isinstance(lhs, IntegerArrayType) or isinstance(lhs,
        types.Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance
        (rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    hedhp__jbnto = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return gahhv__bjbc and hedhp__jbnto


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        pcgs__jet = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        uglv__gpces = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        tgc__mlp = pcgs__jet or uglv__gpces
        wbltc__souga = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        cnkv__etp = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        bcc__scyk = wbltc__souga or cnkv__etp
        nre__rpu = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        dgm__nwzlf = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        jdk__dkm = isinstance(lhs, types.Complex) and isinstance(rhs, types
            .Complex)
        cfzyz__ytie = nre__rpu or dgm__nwzlf or jdk__dkm
        rlctz__iicw = isinstance(lhs, types.List) and isinstance(rhs, types
            .Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        lhiqv__bntz = isinstance(lhs, tys) or isinstance(rhs, tys)
        qow__kkz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return (tgc__mlp or bcc__scyk or cfzyz__ytie or rlctz__iicw or
            lhiqv__bntz or qow__kkz)
    if op == operator.pow:
        aokod__dirxt = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        nvn__myzfd = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        jdk__dkm = isinstance(lhs, types.Complex) and isinstance(rhs, types
            .Complex)
        qow__kkz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return aokod__dirxt or nvn__myzfd or jdk__dkm or qow__kkz
    if op == operator.floordiv:
        dgm__nwzlf = lhs in types.real_domain and rhs in types.real_domain
        nre__rpu = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        meqk__piqww = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        qwb__azxqb = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        qow__kkz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return dgm__nwzlf or nre__rpu or meqk__piqww or qwb__azxqb or qow__kkz
    if op == operator.truediv:
        fmyty__xtq = lhs in machine_ints and rhs in machine_ints
        dgm__nwzlf = lhs in types.real_domain and rhs in types.real_domain
        jdk__dkm = lhs in types.complex_domain and rhs in types.complex_domain
        nre__rpu = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        meqk__piqww = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        uzois__omnt = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        qwb__azxqb = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        qow__kkz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return (fmyty__xtq or dgm__nwzlf or jdk__dkm or nre__rpu or
            meqk__piqww or uzois__omnt or qwb__azxqb or qow__kkz)
    if op == operator.mod:
        fmyty__xtq = lhs in machine_ints and rhs in machine_ints
        dgm__nwzlf = lhs in types.real_domain and rhs in types.real_domain
        nre__rpu = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        meqk__piqww = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        qow__kkz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return fmyty__xtq or dgm__nwzlf or nre__rpu or meqk__piqww or qow__kkz
    if op == operator.add or op == operator.sub:
        tgc__mlp = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        hsf__wbgc = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        dlbw__tbgbm = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        vnva__bqiwr = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        nre__rpu = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        dgm__nwzlf = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        jdk__dkm = isinstance(lhs, types.Complex) and isinstance(rhs, types
            .Complex)
        cfzyz__ytie = nre__rpu or dgm__nwzlf or jdk__dkm
        qow__kkz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        liawv__rnqbh = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        rlctz__iicw = isinstance(lhs, types.List) and isinstance(rhs, types
            .List)
        jbv__skr = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        wfqes__onii = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        attdi__sop = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        dar__zgdjb = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        jfmdb__nth = jbv__skr or wfqes__onii or attdi__sop or dar__zgdjb
        bcc__scyk = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        yomzm__brc = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        tpygk__aseck = bcc__scyk or yomzm__brc
        viai__psdzs = lhs == types.NPTimedelta and rhs == types.NPDatetime
        jpgy__ceqtb = (liawv__rnqbh or rlctz__iicw or jfmdb__nth or
            tpygk__aseck or viai__psdzs)
        hxmq__zsrd = op == operator.add and jpgy__ceqtb
        return (tgc__mlp or hsf__wbgc or dlbw__tbgbm or vnva__bqiwr or
            cfzyz__ytie or qow__kkz or hxmq__zsrd)


def cmp_op_supported_by_numba(lhs, rhs):
    qow__kkz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    rlctz__iicw = isinstance(lhs, types.ListType) and isinstance(rhs, types
        .ListType)
    tgc__mlp = isinstance(lhs, types.NPTimedelta) and isinstance(rhs, types
        .NPTimedelta)
    rjq__jsgro = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
        types.NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    bcc__scyk = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    liawv__rnqbh = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
        types.BaseTuple)
    vnva__bqiwr = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    cfzyz__ytie = isinstance(lhs, types.Number) and isinstance(rhs, types.
        Number)
    cvd__zzhp = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    qpfze__pjqh = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    yhz__yug = isinstance(lhs, types.DictType) and isinstance(rhs, types.
        DictType)
    drqe__vqx = isinstance(lhs, types.EnumMember) and isinstance(rhs, types
        .EnumMember)
    bpsk__cennr = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (rlctz__iicw or tgc__mlp or rjq__jsgro or bcc__scyk or
        liawv__rnqbh or vnva__bqiwr or cfzyz__ytie or cvd__zzhp or
        qpfze__pjqh or yhz__yug or qow__kkz or drqe__vqx or bpsk__cennr)


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
        ewweg__uzr = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(ewweg__uzr)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        ewweg__uzr = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(ewweg__uzr)


install_arith_ops()
