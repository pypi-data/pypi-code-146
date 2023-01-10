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
            feohb__ovhgy, zxxhw__rvmtd = get_series_tz(lhs)
            vznh__bpp, zxxhw__rvmtd = get_series_tz(rhs)
            raise BodoError(
                f'{numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} with two Timestamps requires both Timestamps share the same timezone. '
                 +
                f'Argument 0 has timezone {feohb__ovhgy} and argument 1 has timezone {vznh__bpp}. '
                 +
                'To compare these values please convert to timezone naive with ts.tz_convert(None).'
                )
        hbldu__bmy = lhs.data if isinstance(lhs, SeriesType) else lhs
        hdgwi__dei = rhs.data if isinstance(rhs, SeriesType) else rhs
        if hbldu__bmy in (bodo.pd_timestamp_tz_naive_type, bodo.
            pd_timedelta_type) and hdgwi__dei.dtype in (bodo.datetime64ns,
            bodo.timedelta64ns):
            hbldu__bmy = hdgwi__dei.dtype
        elif hdgwi__dei in (bodo.pd_timestamp_tz_naive_type, bodo.
            pd_timedelta_type) and hbldu__bmy.dtype in (bodo.datetime64ns,
            bodo.timedelta64ns):
            hdgwi__dei = hbldu__bmy.dtype
        wxkr__qorpo = hbldu__bmy, hdgwi__dei
        sjs__bsk = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            zbxud__zhak = self.context.resolve_function_type(self.key,
                wxkr__qorpo, {}).return_type
        except Exception as ycglk__krqv:
            raise BodoError(sjs__bsk)
        if is_overload_bool(zbxud__zhak):
            raise BodoError(sjs__bsk)
        yinjl__nqqiz = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ohs__qfey = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        peuth__xbg = types.bool_
        tvsv__nuqx = SeriesType(peuth__xbg, zbxud__zhak, yinjl__nqqiz,
            ohs__qfey)
        return tvsv__nuqx(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        oplhg__najt = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if oplhg__najt is None:
            oplhg__najt = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, oplhg__najt, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        hbldu__bmy = lhs.data if isinstance(lhs, SeriesType) else lhs
        hdgwi__dei = rhs.data if isinstance(rhs, SeriesType) else rhs
        wxkr__qorpo = hbldu__bmy, hdgwi__dei
        sjs__bsk = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            zbxud__zhak = self.context.resolve_function_type(self.key,
                wxkr__qorpo, {}).return_type
        except Exception as hch__vge:
            raise BodoError(sjs__bsk)
        yinjl__nqqiz = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ohs__qfey = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        peuth__xbg = zbxud__zhak.dtype
        tvsv__nuqx = SeriesType(peuth__xbg, zbxud__zhak, yinjl__nqqiz,
            ohs__qfey)
        return tvsv__nuqx(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        oplhg__najt = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if oplhg__najt is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                oplhg__najt = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, oplhg__najt, sig, args)
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
            oplhg__najt = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return oplhg__najt(lhs, rhs)
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
            oplhg__najt = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return oplhg__najt(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    qepd__imvno = lhs == datetime_timedelta_type and rhs == datetime_date_type
    swk__zzu = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return qepd__imvno or swk__zzu


def add_timestamp(lhs, rhs):
    fmjyl__fnvb = isinstance(lhs, bodo.PandasTimestampType
        ) and is_timedelta_type(rhs)
    ifnbh__zvabo = is_timedelta_type(lhs) and isinstance(rhs, bodo.
        PandasTimestampType)
    return fmjyl__fnvb or ifnbh__zvabo


def add_datetime_and_timedeltas(lhs, rhs):
    klx__tkshd = [datetime_timedelta_type, pd_timedelta_type]
    xgy__liekn = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    iee__bgo = lhs in klx__tkshd and rhs in klx__tkshd
    oyvu__inodm = (lhs == datetime_datetime_type and rhs in klx__tkshd or 
        rhs == datetime_datetime_type and lhs in klx__tkshd)
    return iee__bgo or oyvu__inodm


def mul_string_arr_and_int(lhs, rhs):
    hdgwi__dei = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    hbldu__bmy = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return hdgwi__dei or hbldu__bmy


def mul_timedelta_and_int(lhs, rhs):
    qepd__imvno = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    swk__zzu = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return qepd__imvno or swk__zzu


def mul_date_offset_and_int(lhs, rhs):
    mzqyy__hulpd = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    krs__gxd = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return mzqyy__hulpd or krs__gxd


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    djhnd__dwo = [datetime_datetime_type, datetime_date_type,
        pd_timestamp_tz_naive_type]
    tz_aware_classes = bodo.PandasTimestampType,
    igzp__ypzca = week_type, month_begin_type, month_end_type
    tbg__flbz = date_offset_type,
    return rhs in igzp__ypzca and isinstance(lhs, tz_aware_classes) or (rhs in
        tbg__flbz or rhs in igzp__ypzca) and lhs in djhnd__dwo


def sub_dt_index_and_timestamp(lhs, rhs):
    lssoo__qpy = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_tz_naive_type
    brs__givi = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_tz_naive_type
    return lssoo__qpy or brs__givi


def sub_dt_or_td(lhs, rhs):
    ywlyb__abfu = lhs == datetime_date_type and rhs == datetime_timedelta_type
    qgtic__gboy = lhs == datetime_date_type and rhs == datetime_date_type
    wqd__isgq = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return ywlyb__abfu or qgtic__gboy or wqd__isgq


def sub_datetime_and_timedeltas(lhs, rhs):
    rhpj__yug = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    qcw__dnlk = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return rhpj__yug or qcw__dnlk


def div_timedelta_and_int(lhs, rhs):
    iee__bgo = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    eab__tmrx = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return iee__bgo or eab__tmrx


def div_datetime_timedelta(lhs, rhs):
    iee__bgo = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    eab__tmrx = lhs == datetime_timedelta_type and rhs == types.int64
    return iee__bgo or eab__tmrx


def mod_timedeltas(lhs, rhs):
    brlpf__anvh = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    amhcq__jsp = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return brlpf__anvh or amhcq__jsp


def cmp_dt_index_to_string(lhs, rhs):
    lssoo__qpy = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    brs__givi = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return lssoo__qpy or brs__givi


def cmp_timestamp_or_date(lhs, rhs):
    mopjx__nqkif = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType
        ) and rhs == bodo.hiframes.datetime_date_ext.datetime_date_type
    mvdp__vrq = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        isinstance(rhs, bodo.hiframes.pd_timestamp_ext.PandasTimestampType))
    jyfg__gkb = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType) and isinstance(rhs, bodo.hiframes.
        pd_timestamp_ext.PandasTimestampType)
    dujsf__tbb = lhs == pd_timestamp_tz_naive_type and rhs == bodo.datetime64ns
    vmkpd__dgjly = (rhs == pd_timestamp_tz_naive_type and lhs == bodo.
        datetime64ns)
    return mopjx__nqkif or mvdp__vrq or jyfg__gkb or dujsf__tbb or vmkpd__dgjly


def get_series_tz(val):
    if bodo.hiframes.pd_series_ext.is_dt64_series_typ(val):
        if isinstance(val.data, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType
            ):
            pnkji__npn = val.data.tz
        else:
            pnkji__npn = None
    elif isinstance(val, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        pnkji__npn = val.tz
    elif isinstance(val, types.Array) and val.dtype == bodo.datetime64ns:
        pnkji__npn = None
    elif isinstance(val, bodo.PandasTimestampType):
        pnkji__npn = val.tz
    elif val == bodo.datetime64ns:
        pnkji__npn = None
    else:
        return None, False
    return pnkji__npn, True


def is_cmp_tz_mismatch(lhs, rhs):
    feohb__ovhgy, cjh__hqzzh = get_series_tz(lhs)
    vznh__bpp, tds__sfd = get_series_tz(rhs)
    return cjh__hqzzh and tds__sfd and feohb__ovhgy != vznh__bpp


def cmp_timeseries(lhs, rhs):
    cjah__bhb = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type)
    kbrb__iif = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type)
    rupf__jagaa = (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and 
        rhs.dtype == bodo.datetime64ns and lhs == bodo.hiframes.
        pd_timestamp_ext.pd_timestamp_tz_naive_type or bodo.hiframes.
        pd_series_ext.is_dt64_series_typ(lhs) and lhs.dtype == bodo.
        datetime64ns and rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_tz_naive_type)
    ojtd__utf = cjah__bhb or kbrb__iif or rupf__jagaa
    zxoyw__uywg = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    pdw__mlflr = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    xbf__cyys = zxoyw__uywg or pdw__mlflr
    return ojtd__utf or xbf__cyys


def cmp_timedeltas(lhs, rhs):
    iee__bgo = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in iee__bgo and rhs in iee__bgo


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    rpddd__yyzq = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_tz_naive_type]
    return rpddd__yyzq


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    vphyf__ygio = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    lqup__yoxeh = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    spt__xkzx = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    slq__xjao = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return vphyf__ygio or lqup__yoxeh or spt__xkzx or slq__xjao


def args_td_and_int_array(lhs, rhs):
    slv__jin = (isinstance(lhs, IntegerArrayType) or isinstance(lhs, types.
        Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance(rhs,
        IntegerArrayType) or isinstance(rhs, types.Array) and isinstance(
        rhs.dtype, types.Integer))
    fxefa__xrdnw = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return slv__jin and fxefa__xrdnw


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        swk__zzu = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        qepd__imvno = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        ceh__enf = swk__zzu or qepd__imvno
        kuhp__qjjkd = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        cvva__gcqp = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        dtc__rii = kuhp__qjjkd or cvva__gcqp
        cfgh__qxzpz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        jpbb__rla = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        xlg__pwpzq = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        gvny__ign = cfgh__qxzpz or jpbb__rla or xlg__pwpzq
        lodw__zhvxr = isinstance(lhs, types.List) and isinstance(rhs, types
            .Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        ihm__rjhzl = isinstance(lhs, tys) or isinstance(rhs, tys)
        bgwe__fpvxv = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (ceh__enf or dtc__rii or gvny__ign or lodw__zhvxr or
            ihm__rjhzl or bgwe__fpvxv)
    if op == operator.pow:
        pefiv__svd = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        uvew__ksq = isinstance(lhs, types.Float) and isinstance(rhs, (types
            .IntegerLiteral, types.Float, types.Integer) or rhs in types.
            unsigned_domain or rhs in types.signed_domain)
        xlg__pwpzq = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        bgwe__fpvxv = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return pefiv__svd or uvew__ksq or xlg__pwpzq or bgwe__fpvxv
    if op == operator.floordiv:
        jpbb__rla = lhs in types.real_domain and rhs in types.real_domain
        cfgh__qxzpz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        umo__umr = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        iee__bgo = isinstance(lhs, types.NPTimedelta) and isinstance(rhs, (
            types.Integer, types.Float, types.NPTimedelta))
        bgwe__fpvxv = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return jpbb__rla or cfgh__qxzpz or umo__umr or iee__bgo or bgwe__fpvxv
    if op == operator.truediv:
        imgxw__gjmx = lhs in machine_ints and rhs in machine_ints
        jpbb__rla = lhs in types.real_domain and rhs in types.real_domain
        xlg__pwpzq = (lhs in types.complex_domain and rhs in types.
            complex_domain)
        cfgh__qxzpz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        umo__umr = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        sgca__tzlly = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        iee__bgo = isinstance(lhs, types.NPTimedelta) and isinstance(rhs, (
            types.Integer, types.Float, types.NPTimedelta))
        bgwe__fpvxv = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (imgxw__gjmx or jpbb__rla or xlg__pwpzq or cfgh__qxzpz or
            umo__umr or sgca__tzlly or iee__bgo or bgwe__fpvxv)
    if op == operator.mod:
        imgxw__gjmx = lhs in machine_ints and rhs in machine_ints
        jpbb__rla = lhs in types.real_domain and rhs in types.real_domain
        cfgh__qxzpz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        umo__umr = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        bgwe__fpvxv = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (imgxw__gjmx or jpbb__rla or cfgh__qxzpz or umo__umr or
            bgwe__fpvxv)
    if op == operator.add or op == operator.sub:
        ceh__enf = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        zlwnz__fjqy = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        szw__flvet = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        wykj__qtzd = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        cfgh__qxzpz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        jpbb__rla = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        xlg__pwpzq = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        gvny__ign = cfgh__qxzpz or jpbb__rla or xlg__pwpzq
        bgwe__fpvxv = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        yfcan__qpvv = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        lodw__zhvxr = isinstance(lhs, types.List) and isinstance(rhs, types
            .List)
        jep__hnlo = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        qjbu__zevr = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        qwn__btamu = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        ewtub__ulip = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        klq__bzokw = jep__hnlo or qjbu__zevr or qwn__btamu or ewtub__ulip
        dtc__rii = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        zox__zlbth = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        pzi__jjauv = dtc__rii or zox__zlbth
        lsmt__kdl = lhs == types.NPTimedelta and rhs == types.NPDatetime
        ngci__grusq = (yfcan__qpvv or lodw__zhvxr or klq__bzokw or
            pzi__jjauv or lsmt__kdl)
        fqwom__nkp = op == operator.add and ngci__grusq
        return (ceh__enf or zlwnz__fjqy or szw__flvet or wykj__qtzd or
            gvny__ign or bgwe__fpvxv or fqwom__nkp)


def cmp_op_supported_by_numba(lhs, rhs):
    bgwe__fpvxv = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    lodw__zhvxr = isinstance(lhs, types.ListType) and isinstance(rhs, types
        .ListType)
    ceh__enf = isinstance(lhs, types.NPTimedelta) and isinstance(rhs, types
        .NPTimedelta)
    tnjxy__gltjc = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
        types.NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    dtc__rii = isinstance(lhs, unicode_types) and isinstance(rhs, unicode_types
        )
    yfcan__qpvv = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
        types.BaseTuple)
    wykj__qtzd = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    gvny__ign = isinstance(lhs, types.Number) and isinstance(rhs, types.Number)
    zrz__azv = isinstance(lhs, types.Boolean) and isinstance(rhs, types.Boolean
        )
    xku__lzoc = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    hem__vnwqa = isinstance(lhs, types.DictType) and isinstance(rhs, types.
        DictType)
    bkwx__pvbgv = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    lki__ctzvk = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (lodw__zhvxr or ceh__enf or tnjxy__gltjc or dtc__rii or
        yfcan__qpvv or wykj__qtzd or gvny__ign or zrz__azv or xku__lzoc or
        hem__vnwqa or bgwe__fpvxv or bkwx__pvbgv or lki__ctzvk)


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
        xme__whl = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(xme__whl)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        xme__whl = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(xme__whl)


install_arith_ops()
