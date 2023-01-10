"""Timestamp extension for Pandas Timestamp with timezone support."""
import calendar
import datetime
import operator
from typing import Union
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pytz
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import ConcreteTemplate, infer_global, signature
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
import bodo.libs.str_ext
import bodo.utils.utils
from bodo.hiframes.datetime_date_ext import DatetimeDateType, _ord2ymd, _ymd2ord, get_isocalendar
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, _no_input, datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdatetime_ext
from bodo.libs.pd_datetime_arr_ext import get_pytz_type_info
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import BodoError, check_unsupported_args, get_literal_value, get_overload_const_bool, get_overload_const_int, get_overload_const_str, is_iterable_type, is_literal_type, is_overload_constant_int, is_overload_constant_str, is_overload_none, raise_bodo_error
ll.add_symbol('extract_year_days', hdatetime_ext.extract_year_days)
ll.add_symbol('get_month_day', hdatetime_ext.get_month_day)
ll.add_symbol('npy_datetimestruct_to_datetime', hdatetime_ext.
    npy_datetimestruct_to_datetime)
npy_datetimestruct_to_datetime = types.ExternalFunction(
    'npy_datetimestruct_to_datetime', types.int64(types.int64, types.int32,
    types.int32, types.int32, types.int32, types.int32, types.int32))
date_fields = ['year', 'month', 'day', 'hour', 'minute', 'second',
    'microsecond', 'nanosecond', 'quarter', 'dayofyear', 'day_of_year',
    'dayofweek', 'day_of_week', 'daysinmonth', 'days_in_month',
    'is_leap_year', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end', 'week', 'weekofyear',
    'weekday']
date_methods = ['normalize', 'day_name', 'month_name']
timedelta_fields = ['days', 'seconds', 'microseconds', 'nanoseconds']
timedelta_methods = ['total_seconds', 'to_pytimedelta']
iNaT = pd._libs.tslibs.iNaT


class PandasTimestampType(types.Type):

    def __init__(self, tz_val=None):
        self.tz = tz_val
        if tz_val is None:
            inyj__kppe = 'PandasTimestampType()'
        else:
            inyj__kppe = f'PandasTimestampType({tz_val})'
        super(PandasTimestampType, self).__init__(name=inyj__kppe)


pd_timestamp_tz_naive_type = PandasTimestampType()


def check_tz_aware_unsupported(val, func_name):
    if isinstance(val, bodo.hiframes.series_dt_impl.
        SeriesDatetimePropertiesType):
        val = val.stype
    if isinstance(val, PandasTimestampType) and val.tz is not None:
        raise BodoError(
            f'{func_name} on Timezone-aware timestamp not yet supported. Please convert to timezone naive with ts.tz_convert(None)'
            )
    elif isinstance(val, bodo.DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware array not yet supported. Please convert to timezone naive with arr.tz_convert(None)'
            )
    elif isinstance(val, bodo.DatetimeIndexType) and isinstance(val.data,
        bodo.DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware index not yet supported. Please convert to timezone naive with index.tz_convert(None)'
            )
    elif isinstance(val, bodo.SeriesType) and isinstance(val.data, bodo.
        DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware series not yet supported. Please convert to timezone naive with series.dt.tz_convert(None)'
            )
    elif isinstance(val, bodo.DataFrameType):
        for jvf__jbspk in val.data:
            if isinstance(jvf__jbspk, bodo.DatetimeArrayType):
                raise BodoError(
                    f'{func_name} on Timezone-aware columns not yet supported. Please convert each column to timezone naive with series.dt.tz_convert(None)'
                    )


@typeof_impl.register(pd.Timestamp)
def typeof_pd_timestamp(val, c):
    return PandasTimestampType(get_pytz_type_info(val.tz) if val.tz else None)


ts_field_typ = types.int64


@register_model(PandasTimestampType)
class PandasTimestampModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bpkr__gbgb = [('year', ts_field_typ), ('month', ts_field_typ), (
            'day', ts_field_typ), ('hour', ts_field_typ), ('minute',
            ts_field_typ), ('second', ts_field_typ), ('microsecond',
            ts_field_typ), ('nanosecond', ts_field_typ), ('value',
            ts_field_typ)]
        models.StructModel.__init__(self, dmm, fe_type, bpkr__gbgb)


make_attribute_wrapper(PandasTimestampType, 'year', 'year')
make_attribute_wrapper(PandasTimestampType, 'month', 'month')
make_attribute_wrapper(PandasTimestampType, 'day', 'day')
make_attribute_wrapper(PandasTimestampType, 'hour', 'hour')
make_attribute_wrapper(PandasTimestampType, 'minute', 'minute')
make_attribute_wrapper(PandasTimestampType, 'second', 'second')
make_attribute_wrapper(PandasTimestampType, 'microsecond', 'microsecond')
make_attribute_wrapper(PandasTimestampType, 'nanosecond', 'nanosecond')
make_attribute_wrapper(PandasTimestampType, 'value', 'value')


@unbox(PandasTimestampType)
def unbox_pandas_timestamp(typ, val, c):
    jut__lrps = c.pyapi.object_getattr_string(val, 'year')
    sws__pjqqf = c.pyapi.object_getattr_string(val, 'month')
    bijws__uwmp = c.pyapi.object_getattr_string(val, 'day')
    bixue__fosi = c.pyapi.object_getattr_string(val, 'hour')
    ctt__lvl = c.pyapi.object_getattr_string(val, 'minute')
    djqdc__gizqx = c.pyapi.object_getattr_string(val, 'second')
    yjs__youvj = c.pyapi.object_getattr_string(val, 'microsecond')
    ekr__orpv = c.pyapi.object_getattr_string(val, 'nanosecond')
    fgxsf__xoedf = c.pyapi.object_getattr_string(val, 'value')
    amwbd__xkwgs = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    amwbd__xkwgs.year = c.pyapi.long_as_longlong(jut__lrps)
    amwbd__xkwgs.month = c.pyapi.long_as_longlong(sws__pjqqf)
    amwbd__xkwgs.day = c.pyapi.long_as_longlong(bijws__uwmp)
    amwbd__xkwgs.hour = c.pyapi.long_as_longlong(bixue__fosi)
    amwbd__xkwgs.minute = c.pyapi.long_as_longlong(ctt__lvl)
    amwbd__xkwgs.second = c.pyapi.long_as_longlong(djqdc__gizqx)
    amwbd__xkwgs.microsecond = c.pyapi.long_as_longlong(yjs__youvj)
    amwbd__xkwgs.nanosecond = c.pyapi.long_as_longlong(ekr__orpv)
    amwbd__xkwgs.value = c.pyapi.long_as_longlong(fgxsf__xoedf)
    c.pyapi.decref(jut__lrps)
    c.pyapi.decref(sws__pjqqf)
    c.pyapi.decref(bijws__uwmp)
    c.pyapi.decref(bixue__fosi)
    c.pyapi.decref(ctt__lvl)
    c.pyapi.decref(djqdc__gizqx)
    c.pyapi.decref(yjs__youvj)
    c.pyapi.decref(ekr__orpv)
    c.pyapi.decref(fgxsf__xoedf)
    oni__ixj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(amwbd__xkwgs._getvalue(), is_error=oni__ixj)


@box(PandasTimestampType)
def box_pandas_timestamp(typ, val, c):
    lxgwn__dvx = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    jut__lrps = c.pyapi.long_from_longlong(lxgwn__dvx.year)
    sws__pjqqf = c.pyapi.long_from_longlong(lxgwn__dvx.month)
    bijws__uwmp = c.pyapi.long_from_longlong(lxgwn__dvx.day)
    bixue__fosi = c.pyapi.long_from_longlong(lxgwn__dvx.hour)
    ctt__lvl = c.pyapi.long_from_longlong(lxgwn__dvx.minute)
    djqdc__gizqx = c.pyapi.long_from_longlong(lxgwn__dvx.second)
    rdiag__zal = c.pyapi.long_from_longlong(lxgwn__dvx.microsecond)
    qty__fqfhe = c.pyapi.long_from_longlong(lxgwn__dvx.nanosecond)
    uvpk__mqejd = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timestamp))
    if typ.tz is None:
        res = c.pyapi.call_function_objargs(uvpk__mqejd, (jut__lrps,
            sws__pjqqf, bijws__uwmp, bixue__fosi, ctt__lvl, djqdc__gizqx,
            rdiag__zal, qty__fqfhe))
    else:
        if isinstance(typ.tz, int):
            mvtze__zoym = c.pyapi.long_from_longlong(lir.Constant(lir.
                IntType(64), typ.tz))
        else:
            nts__oxj = c.context.insert_const_string(c.builder.module, str(
                typ.tz))
            mvtze__zoym = c.pyapi.string_from_string(nts__oxj)
        args = c.pyapi.tuple_pack(())
        kwargs = c.pyapi.dict_pack([('year', jut__lrps), ('month',
            sws__pjqqf), ('day', bijws__uwmp), ('hour', bixue__fosi), (
            'minute', ctt__lvl), ('second', djqdc__gizqx), ('microsecond',
            rdiag__zal), ('nanosecond', qty__fqfhe), ('tz', mvtze__zoym)])
        res = c.pyapi.call(uvpk__mqejd, args, kwargs)
        c.pyapi.decref(args)
        c.pyapi.decref(kwargs)
        c.pyapi.decref(mvtze__zoym)
    c.pyapi.decref(jut__lrps)
    c.pyapi.decref(sws__pjqqf)
    c.pyapi.decref(bijws__uwmp)
    c.pyapi.decref(bixue__fosi)
    c.pyapi.decref(ctt__lvl)
    c.pyapi.decref(djqdc__gizqx)
    c.pyapi.decref(rdiag__zal)
    c.pyapi.decref(qty__fqfhe)
    return res


@intrinsic
def init_timestamp(typingctx, year, month, day, hour, minute, second,
    microsecond, nanosecond, value, tz):

    def codegen(context, builder, sig, args):
        (year, month, day, hour, minute, second, ffgm__kyjk, xgq__xdgf,
            value, fpn__ivuqz) = args
        ts = cgutils.create_struct_proxy(sig.return_type)(context, builder)
        ts.year = year
        ts.month = month
        ts.day = day
        ts.hour = hour
        ts.minute = minute
        ts.second = second
        ts.microsecond = ffgm__kyjk
        ts.nanosecond = xgq__xdgf
        ts.value = value
        return ts._getvalue()
    if is_overload_none(tz):
        typ = pd_timestamp_tz_naive_type
    elif is_overload_constant_str(tz):
        typ = PandasTimestampType(get_overload_const_str(tz))
    elif is_overload_constant_int(tz):
        typ = PandasTimestampType(get_overload_const_int(tz))
    else:
        raise_bodo_error('tz must be a constant string, int, or None')
    return typ(types.int64, types.int64, types.int64, types.int64, types.
        int64, types.int64, types.int64, types.int64, types.int64, tz), codegen


@numba.generated_jit
def zero_if_none(value):
    if value == types.none:
        return lambda value: 0
    return lambda value: value


@lower_constant(PandasTimestampType)
def constant_timestamp(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    nanosecond = context.get_constant(types.int64, pyval.nanosecond)
    value = context.get_constant(types.int64, pyval.value)
    return lir.Constant.literal_struct((year, month, day, hour, minute,
        second, microsecond, nanosecond, value))


def tz_has_transition_times(tz: Union[str, int, None]):
    if isinstance(tz, str):
        qosn__anubu = pytz.timezone(tz)
        return isinstance(qosn__anubu, pytz.tzinfo.DstTzInfo)
    return False


@overload(pd.Timestamp, no_unliteral=True)
def overload_pd_timestamp(ts_input=_no_input, freq=None, tz=None, unit=None,
    year=None, month=None, day=None, hour=None, minute=None, second=None,
    microsecond=None, nanosecond=None, tzinfo=None):
    if not is_overload_none(tz) and is_overload_constant_str(tz
        ) and get_overload_const_str(tz) not in pytz.all_timezones_set:
        raise BodoError(
            "pandas.Timestamp(): 'tz', if provided, must be constant string found in pytz.all_timezones"
            )
    if ts_input == _no_input or getattr(ts_input, 'value', None) == _no_input:

        def impl_kw(ts_input=_no_input, freq=None, tz=None, unit=None, year
            =None, month=None, day=None, hour=None, minute=None, second=
            None, microsecond=None, nanosecond=None, tzinfo=None):
            return compute_val_for_timestamp(year, month, day, zero_if_none
                (hour), zero_if_none(minute), zero_if_none(second),
                zero_if_none(microsecond), zero_if_none(nanosecond), tz)
        return impl_kw
    if isinstance(types.unliteral(freq), types.Integer):

        def impl_pos(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            return compute_val_for_timestamp(ts_input, freq, tz,
                zero_if_none(unit), zero_if_none(year), zero_if_none(month),
                zero_if_none(day), zero_if_none(hour), None)
        return impl_pos
    if isinstance(ts_input, types.Number):
        if is_overload_none(unit):
            unit = 'ns'
        if not is_overload_constant_str(unit):
            raise BodoError(
                'pandas.Timedelta(): unit argument must be a constant str')
        unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
            get_overload_const_str(unit))
        hknkb__cky, precision = pd._libs.tslibs.conversion.precision_from_unit(
            unit)
        if isinstance(ts_input, types.Integer):

            def impl_int(ts_input=_no_input, freq=None, tz=None, unit=None,
                year=None, month=None, day=None, hour=None, minute=None,
                second=None, microsecond=None, nanosecond=None, tzinfo=None):
                value = ts_input * hknkb__cky
                return convert_val_to_timestamp(value, tz)
            return impl_int

        def impl_float(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            knj__kfkg = np.int64(ts_input)
            dgmy__abvx = ts_input - knj__kfkg
            if precision:
                dgmy__abvx = np.round(dgmy__abvx, precision)
            value = knj__kfkg * hknkb__cky + np.int64(dgmy__abvx * hknkb__cky)
            return convert_val_to_timestamp(value, tz)
        return impl_float
    if ts_input == bodo.string_type or is_overload_constant_str(ts_input):
        types.pd_timestamp_tz_naive_type = pd_timestamp_tz_naive_type
        if is_overload_none(tz):
            tz_val = None
        elif is_overload_constant_str(tz):
            tz_val = get_overload_const_str(tz)
        else:
            raise_bodo_error(
                'pandas.Timestamp(): tz argument must be a constant string or None'
                )
        typ = PandasTimestampType(tz_val)

        def impl_str(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            with numba.objmode(res=typ):
                res = pd.Timestamp(ts_input, tz=tz)
            return res
        return impl_str
    if isinstance(ts_input, PandasTimestampType):
        return (lambda ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None: ts_input)
    if ts_input == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:

        def impl_datetime(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            year = ts_input.year
            month = ts_input.month
            day = ts_input.day
            hour = ts_input.hour
            minute = ts_input.minute
            second = ts_input.second
            microsecond = ts_input.microsecond
            return compute_val_for_timestamp(year, month, day, zero_if_none
                (hour), zero_if_none(minute), zero_if_none(second),
                zero_if_none(microsecond), zero_if_none(nanosecond), tz)
        return impl_datetime
    if ts_input == bodo.hiframes.datetime_date_ext.datetime_date_type:

        def impl_date(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            year = ts_input.year
            month = ts_input.month
            day = ts_input.day
            return compute_val_for_timestamp(year, month, day, zero_if_none
                (hour), zero_if_none(minute), zero_if_none(second),
                zero_if_none(microsecond), zero_if_none(nanosecond), tz)
        return impl_date
    if isinstance(ts_input, numba.core.types.scalars.NPDatetime):
        hknkb__cky, precision = pd._libs.tslibs.conversion.precision_from_unit(
            ts_input.unit)

        def impl_date(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            value = np.int64(ts_input) * hknkb__cky
            return convert_val_to_timestamp(value, tz)
        return impl_date


@overload_attribute(PandasTimestampType, 'dayofyear')
@overload_attribute(PandasTimestampType, 'day_of_year')
def overload_pd_dayofyear(ptt):

    def pd_dayofyear(ptt):
        return get_day_of_year(ptt.year, ptt.month, ptt.day)
    return pd_dayofyear


@overload_method(PandasTimestampType, 'weekday')
@overload_attribute(PandasTimestampType, 'dayofweek')
@overload_attribute(PandasTimestampType, 'day_of_week')
def overload_pd_dayofweek(ptt):

    def pd_dayofweek(ptt):
        return get_day_of_week(ptt.year, ptt.month, ptt.day)
    return pd_dayofweek


@overload_attribute(PandasTimestampType, 'week')
@overload_attribute(PandasTimestampType, 'weekofyear')
def overload_week_number(ptt):

    def pd_week_number(ptt):
        fpn__ivuqz, mdtyt__dak, fpn__ivuqz = get_isocalendar(ptt.year, ptt.
            month, ptt.day)
        return mdtyt__dak
    return pd_week_number


@overload_method(PandasTimestampType, '__hash__', no_unliteral=True)
def dt64_hash(val):
    return lambda val: hash(val.value)


@overload_attribute(PandasTimestampType, 'days_in_month')
@overload_attribute(PandasTimestampType, 'daysinmonth')
def overload_pd_daysinmonth(ptt):

    def pd_daysinmonth(ptt):
        return get_days_in_month(ptt.year, ptt.month)
    return pd_daysinmonth


@overload_attribute(PandasTimestampType, 'is_leap_year')
def overload_pd_is_leap_year(ptt):

    def pd_is_leap_year(ptt):
        return is_leap_year(ptt.year)
    return pd_is_leap_year


@overload_attribute(PandasTimestampType, 'is_month_start')
def overload_pd_is_month_start(ptt):

    def pd_is_month_start(ptt):
        return ptt.day == 1
    return pd_is_month_start


@overload_attribute(PandasTimestampType, 'is_month_end')
def overload_pd_is_month_end(ptt):

    def pd_is_month_end(ptt):
        return ptt.day == get_days_in_month(ptt.year, ptt.month)
    return pd_is_month_end


@overload_attribute(PandasTimestampType, 'is_quarter_start')
def overload_pd_is_quarter_start(ptt):

    def pd_is_quarter_start(ptt):
        return ptt.day == 1 and ptt.month % 3 == 1
    return pd_is_quarter_start


@overload_attribute(PandasTimestampType, 'is_quarter_end')
def overload_pd_is_quarter_end(ptt):

    def pd_is_quarter_end(ptt):
        return ptt.month % 3 == 0 and ptt.day == get_days_in_month(ptt.year,
            ptt.month)
    return pd_is_quarter_end


@overload_attribute(PandasTimestampType, 'is_year_start')
def overload_pd_is_year_start(ptt):

    def pd_is_year_start(ptt):
        return ptt.day == 1 and ptt.month == 1
    return pd_is_year_start


@overload_attribute(PandasTimestampType, 'is_year_end')
def overload_pd_is_year_end(ptt):

    def pd_is_year_end(ptt):
        return ptt.day == 31 and ptt.month == 12
    return pd_is_year_end


@overload_attribute(PandasTimestampType, 'quarter')
def overload_quarter(ptt):

    def quarter(ptt):
        return (ptt.month - 1) // 3 + 1
    return quarter


@overload_method(PandasTimestampType, 'date', no_unliteral=True)
def overload_pd_timestamp_date(ptt):

    def pd_timestamp_date_impl(ptt):
        return datetime.date(ptt.year, ptt.month, ptt.day)
    return pd_timestamp_date_impl


@overload_method(PandasTimestampType, 'isocalendar', no_unliteral=True)
def overload_pd_timestamp_isocalendar(ptt):

    def impl(ptt):
        year, mdtyt__dak, hoy__nsqp = get_isocalendar(ptt.year, ptt.month,
            ptt.day)
        return year, mdtyt__dak, hoy__nsqp
    return impl


@overload_method(PandasTimestampType, 'isoformat', no_unliteral=True)
def overload_pd_timestamp_isoformat(ts, sep=None):
    if is_overload_none(sep):

        def timestamp_isoformat_impl(ts, sep=None):
            aqh__pqnfr = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            if ts.microsecond != 0:
                aqh__pqnfr += '.' + str_2d(ts.microsecond)
                if ts.nanosecond != 0:
                    aqh__pqnfr += str_2d(ts.nanosecond)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + 'T' + aqh__pqnfr
            return res
        return timestamp_isoformat_impl
    else:

        def timestamp_isoformat_impl(ts, sep=None):
            aqh__pqnfr = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            if ts.microsecond != 0:
                aqh__pqnfr += '.' + str_2d(ts.microsecond)
                if ts.nanosecond != 0:
                    aqh__pqnfr += str_2d(ts.nanosecond)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + sep + aqh__pqnfr
            return res
    return timestamp_isoformat_impl


@overload_method(PandasTimestampType, 'normalize', no_unliteral=True)
def overload_pd_timestamp_normalize(ptt):
    tz_literal = ptt.tz

    def impl(ptt):
        return pd.Timestamp(year=ptt.year, month=ptt.month, day=ptt.day, tz
            =tz_literal)
    return impl


@overload_method(PandasTimestampType, 'day_name', no_unliteral=True)
def overload_pd_timestamp_day_name(ptt, locale=None):
    zfpn__omk = dict(locale=locale)
    lvyqq__tbddy = dict(locale=None)
    check_unsupported_args('Timestamp.day_name', zfpn__omk, lvyqq__tbddy,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        hkyz__zhp = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday')
        fpn__ivuqz, fpn__ivuqz, xxzr__beavv = ptt.isocalendar()
        return hkyz__zhp[xxzr__beavv - 1]
    return impl


@overload_method(PandasTimestampType, 'month_name', no_unliteral=True)
def overload_pd_timestamp_month_name(ptt, locale=None):
    zfpn__omk = dict(locale=locale)
    lvyqq__tbddy = dict(locale=None)
    check_unsupported_args('Timestamp.month_name', zfpn__omk, lvyqq__tbddy,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        plqmi__xelxh = ('January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September', 'October', 'November',
            'December')
        return plqmi__xelxh[ptt.month - 1]
    return impl


@overload_method(PandasTimestampType, 'tz_convert', no_unliteral=True)
def overload_pd_timestamp_tz_convert(ptt, tz):
    if ptt.tz is None:
        raise BodoError(
            'Cannot convert tz-naive Timestamp, use tz_localize to localize')
    if is_overload_none(tz):
        return lambda ptt, tz: convert_val_to_timestamp(ptt.value)
    elif is_overload_constant_str(tz):
        return lambda ptt, tz: convert_val_to_timestamp(ptt.value, tz=tz)


@overload_method(PandasTimestampType, 'tz_localize', no_unliteral=True)
def overload_pd_timestamp_tz_localize(ptt, tz, ambiguous='raise',
    nonexistent='raise'):
    if ptt.tz is not None and not is_overload_none(tz):
        raise BodoError(
            'Cannot localize tz-aware Timestamp, use tz_convert for conversions'
            )
    zfpn__omk = dict(ambiguous=ambiguous, nonexistent=nonexistent)
    alrtp__nznfp = dict(ambiguous='raise', nonexistent='raise')
    check_unsupported_args('Timestamp.tz_localize', zfpn__omk, alrtp__nznfp,
        package_name='pandas', module_name='Timestamp')
    if is_overload_none(tz) and ptt.tz is None:
        return lambda ptt, tz, ambiguous='raise', nonexistent='raise': ptt
    if is_overload_none(tz):
        rdpa__bwx = ptt.tz
        ygcc__hybec = False
    else:
        if not is_literal_type(tz):
            raise_bodo_error(
                'Timestamp.tz_localize(): tz value must be a literal string, integer, or None'
                )
        rdpa__bwx = get_literal_value(tz)
        ygcc__hybec = True
    ipk__xoo = None
    ruz__kdpys = None
    kako__kso = False
    if tz_has_transition_times(rdpa__bwx):
        kako__kso = ygcc__hybec
        mvtze__zoym = pytz.timezone(rdpa__bwx)
        ruz__kdpys = np.array(mvtze__zoym._utc_transition_times, dtype='M8[ns]'
            ).view('i8')
        ipk__xoo = np.array(mvtze__zoym._transition_info)[:, 0]
        ipk__xoo = (pd.Series(ipk__xoo).dt.total_seconds() * 1000000000
            ).astype(np.int64).values
        kepn__nfuwk = "deltas[np.searchsorted(trans, value, side='right') - 1]"
    elif isinstance(rdpa__bwx, str):
        mvtze__zoym = pytz.timezone(rdpa__bwx)
        kepn__nfuwk = str(np.int64(mvtze__zoym._utcoffset.total_seconds() *
            1000000000))
    elif isinstance(rdpa__bwx, int):
        kepn__nfuwk = str(rdpa__bwx)
    else:
        raise_bodo_error(
            'Timestamp.tz_localize(): tz value must be a literal string, integer, or None'
            )
    if ygcc__hybec:
        hqihi__hzg = '-'
    else:
        hqihi__hzg = '+'
    kvd__eae = "def impl(ptt, tz, ambiguous='raise', nonexistent='raise'):\n"
    kvd__eae += f'    value =  ptt.value\n'
    kvd__eae += f'    delta =  {kepn__nfuwk}\n'
    kvd__eae += f'    new_value = value {hqihi__hzg} delta\n'
    if kako__kso:
        kvd__eae += (
            "    end_delta = deltas[np.searchsorted(trans, new_value, side='right') - 1]\n"
            )
        kvd__eae += '    offset = delta - end_delta\n'
        kvd__eae += '    new_value = new_value + offset\n'
    kvd__eae += f'    return convert_val_to_timestamp(new_value, tz=tz)\n'
    nun__bif = {}
    exec(kvd__eae, {'np': np, 'convert_val_to_timestamp':
        convert_val_to_timestamp, 'trans': ruz__kdpys, 'deltas': ipk__xoo},
        nun__bif)
    impl = nun__bif['impl']
    return impl


@numba.njit
def str_2d(a):
    res = str(a)
    if len(res) == 1:
        return '0' + res
    return res


@overload(str, no_unliteral=True)
def ts_str_overload(a):
    if a == pd_timestamp_tz_naive_type:
        return lambda a: a.isoformat(' ')


@intrinsic
def extract_year_days(typingctx, dt64_t=None):
    assert dt64_t in (types.int64, types.NPDatetime('ns'))

    def codegen(context, builder, sig, args):
        lshp__zsw = cgutils.alloca_once(builder, lir.IntType(64))
        builder.store(args[0], lshp__zsw)
        year = cgutils.alloca_once(builder, lir.IntType(64))
        riww__vwqk = cgutils.alloca_once(builder, lir.IntType(64))
        yudtb__fgu = lir.FunctionType(lir.VoidType(), [lir.IntType(64).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        lln__deiy = cgutils.get_or_insert_function(builder.module,
            yudtb__fgu, name='extract_year_days')
        builder.call(lln__deiy, [lshp__zsw, year, riww__vwqk])
        return cgutils.pack_array(builder, [builder.load(lshp__zsw),
            builder.load(year), builder.load(riww__vwqk)])
    return types.Tuple([types.int64, types.int64, types.int64])(dt64_t
        ), codegen


@intrinsic
def get_month_day(typingctx, year_t, days_t=None):
    assert year_t == types.int64
    assert days_t == types.int64

    def codegen(context, builder, sig, args):
        month = cgutils.alloca_once(builder, lir.IntType(64))
        day = cgutils.alloca_once(builder, lir.IntType(64))
        yudtb__fgu = lir.FunctionType(lir.VoidType(), [lir.IntType(64), lir
            .IntType(64), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        lln__deiy = cgutils.get_or_insert_function(builder.module,
            yudtb__fgu, name='get_month_day')
        builder.call(lln__deiy, [args[0], args[1], month, day])
        return cgutils.pack_array(builder, [builder.load(month), builder.
            load(day)])
    return types.Tuple([types.int64, types.int64])(types.int64, types.int64
        ), codegen


@register_jitable
def get_day_of_year(year, month, day):
    jyu__flo = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365,
        0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    zpqyp__zpaim = is_leap_year(year)
    dwdbm__hozaz = jyu__flo[zpqyp__zpaim * 13 + month - 1]
    iqku__yuuxw = dwdbm__hozaz + day
    return iqku__yuuxw


@register_jitable
def get_day_of_week(y, m, d):
    aznj__mearr = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    y -= m < 3
    day = (y + y // 4 - y // 100 + y // 400 + aznj__mearr[m - 1] + d) % 7
    return (day + 6) % 7


@register_jitable
def get_days_in_month(year, month):
    is_leap_year = year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)
    mdm__oncsa = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 29, 
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return mdm__oncsa[12 * is_leap_year + month - 1]


@register_jitable
def is_leap_year(year):
    return year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)


@numba.generated_jit(nopython=True)
def compute_val_for_timestamp(year, month, day, hour, minute, second,
    microsecond, nanosecond, tz):
    kepn__nfuwk = '0'
    rdpa__bwx = get_literal_value(tz)
    ipk__xoo = None
    ruz__kdpys = None
    kako__kso = False
    if tz_has_transition_times(rdpa__bwx):
        kako__kso = True
        mvtze__zoym = pytz.timezone(rdpa__bwx)
        ruz__kdpys = np.array(mvtze__zoym._utc_transition_times, dtype='M8[ns]'
            ).view('i8')
        ipk__xoo = np.array(mvtze__zoym._transition_info)[:, 0]
        ipk__xoo = (pd.Series(ipk__xoo).dt.total_seconds() * 1000000000
            ).astype(np.int64).values
        kepn__nfuwk = (
            "deltas[np.searchsorted(trans, original_value, side='right') - 1]")
    elif isinstance(rdpa__bwx, str):
        mvtze__zoym = pytz.timezone(rdpa__bwx)
        kepn__nfuwk = str(np.int64(mvtze__zoym._utcoffset.total_seconds() *
            1000000000))
    elif isinstance(rdpa__bwx, int):
        kepn__nfuwk = str(rdpa__bwx)
    elif rdpa__bwx is not None:
        raise_bodo_error(
            'compute_val_for_timestamp(): tz value must be a constant string, integer or None'
            )
    kvd__eae = (
        'def impl(year, month, day, hour, minute, second, microsecond, nanosecond, tz):\n'
        )
    kvd__eae += f"""  original_value = npy_datetimestruct_to_datetime(year, month, day, hour, minute, second, microsecond) + nanosecond
"""
    kvd__eae += f'  value = original_value - {kepn__nfuwk}\n'
    if kako__kso:
        kvd__eae += (
            "  start_trans = np.searchsorted(trans, original_value, side='right') - 1\n"
            )
        kvd__eae += (
            "  end_trans = np.searchsorted(trans, value, side='right') - 1\n")
        kvd__eae += '  offset = deltas[start_trans] - deltas[end_trans]\n'
        kvd__eae += '  value = value + offset\n'
    kvd__eae += '  return init_timestamp(\n'
    kvd__eae += '    year=year,\n'
    kvd__eae += '    month=month,\n'
    kvd__eae += '    day=day,\n'
    kvd__eae += '    hour=hour,\n'
    kvd__eae += '    minute=minute,'
    kvd__eae += '    second=second,\n'
    kvd__eae += '    microsecond=microsecond,\n'
    kvd__eae += '    nanosecond=nanosecond,\n'
    kvd__eae += f'    value=value,\n'
    kvd__eae += '    tz=tz,\n'
    kvd__eae += '  )\n'
    nun__bif = {}
    exec(kvd__eae, {'np': np, 'pd': pd, 'init_timestamp': init_timestamp,
        'npy_datetimestruct_to_datetime': npy_datetimestruct_to_datetime,
        'trans': ruz__kdpys, 'deltas': ipk__xoo}, nun__bif)
    impl = nun__bif['impl']
    return impl


@numba.generated_jit(nopython=True)
def convert_val_to_timestamp(ts_input, tz=None, is_convert=True):
    ruz__kdpys = ipk__xoo = np.array([])
    kepn__nfuwk = '0'
    if is_overload_constant_str(tz):
        nts__oxj = get_overload_const_str(tz)
        mvtze__zoym = pytz.timezone(nts__oxj)
        if isinstance(mvtze__zoym, pytz.tzinfo.DstTzInfo):
            ruz__kdpys = np.array(mvtze__zoym._utc_transition_times, dtype=
                'M8[ns]').view('i8')
            ipk__xoo = np.array(mvtze__zoym._transition_info)[:, 0]
            ipk__xoo = (pd.Series(ipk__xoo).dt.total_seconds() * 1000000000
                ).astype(np.int64).values
            kepn__nfuwk = (
                "deltas[np.searchsorted(trans, ts_input, side='right') - 1]")
        else:
            ipk__xoo = np.int64(mvtze__zoym._utcoffset.total_seconds() * 
                1000000000)
            kepn__nfuwk = 'deltas'
    elif is_overload_constant_int(tz):
        lsrum__uujdx = get_overload_const_int(tz)
        kepn__nfuwk = str(lsrum__uujdx)
    elif not is_overload_none(tz):
        raise_bodo_error(
            'convert_val_to_timestamp(): tz value must be a constant string or None'
            )
    is_convert = get_overload_const_bool(is_convert)
    if is_convert:
        mud__uwxx = 'tz_ts_input'
        jvm__dra = 'ts_input'
    else:
        mud__uwxx = 'ts_input'
        jvm__dra = 'tz_ts_input'
    kvd__eae = 'def impl(ts_input, tz=None, is_convert=True):\n'
    kvd__eae += f'  tz_ts_input = ts_input + {kepn__nfuwk}\n'
    kvd__eae += (
        f'  dt, year, days = extract_year_days(integer_to_dt64({mud__uwxx}))\n'
        )
    kvd__eae += '  month, day = get_month_day(year, days)\n'
    kvd__eae += '  return init_timestamp(\n'
    kvd__eae += '    year=year,\n'
    kvd__eae += '    month=month,\n'
    kvd__eae += '    day=day,\n'
    kvd__eae += '    hour=dt // (60 * 60 * 1_000_000_000),\n'
    kvd__eae += '    minute=(dt // (60 * 1_000_000_000)) % 60,\n'
    kvd__eae += '    second=(dt // 1_000_000_000) % 60,\n'
    kvd__eae += '    microsecond=(dt // 1000) % 1_000_000,\n'
    kvd__eae += '    nanosecond=dt % 1000,\n'
    kvd__eae += f'    value={jvm__dra},\n'
    kvd__eae += '    tz=tz,\n'
    kvd__eae += '  )\n'
    nun__bif = {}
    exec(kvd__eae, {'np': np, 'pd': pd, 'trans': ruz__kdpys, 'deltas':
        ipk__xoo, 'integer_to_dt64': integer_to_dt64, 'extract_year_days':
        extract_year_days, 'get_month_day': get_month_day, 'init_timestamp':
        init_timestamp, 'zero_if_none': zero_if_none}, nun__bif)
    impl = nun__bif['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def convert_datetime64_to_timestamp(dt64):
    lshp__zsw, year, riww__vwqk = extract_year_days(dt64)
    month, day = get_month_day(year, riww__vwqk)
    return init_timestamp(year=year, month=month, day=day, hour=lshp__zsw //
        (60 * 60 * 1000000000), minute=lshp__zsw // (60 * 1000000000) % 60,
        second=lshp__zsw // 1000000000 % 60, microsecond=lshp__zsw // 1000 %
        1000000, nanosecond=lshp__zsw % 1000, value=dt64, tz=None)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_datetime_timedelta(dt64):
    wmqb__zzrj = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    dvb__rdirq = wmqb__zzrj // (86400 * 1000000000)
    fzi__wkguz = wmqb__zzrj - dvb__rdirq * 86400 * 1000000000
    xmije__ppn = fzi__wkguz // 1000000000
    xwkxc__xtb = fzi__wkguz - xmije__ppn * 1000000000
    dguwt__pwh = xwkxc__xtb // 1000
    return datetime.timedelta(dvb__rdirq, xmije__ppn, dguwt__pwh)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_pd_timedelta(dt64):
    wmqb__zzrj = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    return pd.Timedelta(wmqb__zzrj)


@intrinsic
def integer_to_timedelta64(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.NPTimedelta('ns')(val), codegen


@intrinsic
def integer_to_dt64(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.NPDatetime('ns')(val), codegen


@intrinsic
def dt64_to_integer(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.int64(val), codegen


@lower_cast(types.NPDatetime('ns'), types.int64)
def cast_dt64_to_integer(context, builder, fromty, toty, val):
    return val


@overload_method(types.NPDatetime, '__hash__', no_unliteral=True)
def dt64_hash(val):
    return lambda val: hash(dt64_to_integer(val))


@overload_method(types.NPTimedelta, '__hash__', no_unliteral=True)
def td64_hash(val):
    return lambda val: hash(dt64_to_integer(val))


@intrinsic
def timedelta64_to_integer(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.int64(val), codegen


@lower_cast(bodo.timedelta64ns, types.int64)
def cast_td64_to_integer(context, builder, fromty, toty, val):
    return val


@numba.njit
def parse_datetime_str(val):
    with numba.objmode(res='int64'):
        res = pd.Timestamp(val).value
    return integer_to_dt64(res)


@numba.njit
def datetime_timedelta_to_timedelta64(val):
    with numba.objmode(res='NPTimedelta("ns")'):
        res = pd.to_timedelta(val)
        res = res.to_timedelta64()
    return res


@numba.njit
def series_str_dt64_astype(data):
    with numba.objmode(res="NPDatetime('ns')[::1]"):
        res = pd.Series(data.to_numpy()).astype('datetime64[ns]').values
    return res


@numba.njit
def series_str_td64_astype(data):
    with numba.objmode(res="NPTimedelta('ns')[::1]"):
        res = data.astype('timedelta64[ns]')
    return res


@numba.njit
def datetime_datetime_to_dt64(val):
    with numba.objmode(res='NPDatetime("ns")'):
        res = np.datetime64(val).astype('datetime64[ns]')
    return res


@register_jitable
def datetime_date_arr_to_dt64_arr(arr):
    with numba.objmode(res='NPDatetime("ns")[::1]'):
        res = np.array(arr, dtype='datetime64[ns]')
    return res


types.pd_timestamp_tz_naive_type = pd_timestamp_tz_naive_type


@register_jitable
def to_datetime_scalar(a, errors='raise', dayfirst=False, yearfirst=False,
    utc=None, format=None, exact=True, unit=None, infer_datetime_format=
    False, origin='unix', cache=True):
    with numba.objmode(t='pd_timestamp_tz_naive_type'):
        t = pd.to_datetime(a, errors=errors, dayfirst=dayfirst, yearfirst=
            yearfirst, utc=utc, format=format, exact=exact, unit=unit,
            infer_datetime_format=infer_datetime_format, origin=origin,
            cache=cache)
    return t


@numba.njit
def pandas_string_array_to_datetime(arr, errors, dayfirst, yearfirst, utc,
    format, exact, unit, infer_datetime_format, origin, cache):
    with numba.objmode(result='datetime_index'):
        result = pd.to_datetime(arr, errors=errors, dayfirst=dayfirst,
            yearfirst=yearfirst, utc=utc, format=format, exact=exact, unit=
            unit, infer_datetime_format=infer_datetime_format, origin=
            origin, cache=cache)
    return result


@numba.njit
def pandas_dict_string_array_to_datetime(arr, errors, dayfirst, yearfirst,
    utc, format, exact, unit, infer_datetime_format, origin, cache):
    qxd__epfyi = len(arr)
    duy__waad = np.empty(qxd__epfyi, 'datetime64[ns]')
    aflj__lrr = arr._indices
    puvwe__wzk = pandas_string_array_to_datetime(arr._data, errors,
        dayfirst, yearfirst, utc, format, exact, unit,
        infer_datetime_format, origin, cache).values
    for yjs__hvrb in range(qxd__epfyi):
        if bodo.libs.array_kernels.isna(aflj__lrr, yjs__hvrb):
            bodo.libs.array_kernels.setna(duy__waad, yjs__hvrb)
            continue
        duy__waad[yjs__hvrb] = puvwe__wzk[aflj__lrr[yjs__hvrb]]
    return duy__waad


@overload(pd.to_datetime, inline='always', no_unliteral=True)
def overload_to_datetime(arg_a, errors='raise', dayfirst=False, yearfirst=
    False, utc=None, format=None, exact=True, unit=None,
    infer_datetime_format=False, origin='unix', cache=True):
    dxon__zye = {'errors': errors}
    wbncx__ioo = {'errors': 'raise'}
    check_unsupported_args('pd.to_datetime', dxon__zye, wbncx__ioo,
        package_name='pandas')
    if arg_a == bodo.string_type or is_overload_constant_str(arg_a
        ) or is_overload_constant_int(arg_a) or isinstance(arg_a, types.Integer
        ):

        def pd_to_datetime_impl(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return to_datetime_scalar(arg_a, errors=errors, dayfirst=
                dayfirst, yearfirst=yearfirst, utc=utc, format=format,
                exact=exact, unit=unit, infer_datetime_format=
                infer_datetime_format, origin=origin, cache=cache)
        return pd_to_datetime_impl
    if isinstance(arg_a, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            ybz__hqe = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            inyj__kppe = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            amlx__xuwbj = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_datetime(arr, errors=errors, dayfirst=dayfirst,
                yearfirst=yearfirst, utc=utc, format=format, exact=exact,
                unit=unit, infer_datetime_format=infer_datetime_format,
                origin=origin, cache=cache))
            return bodo.hiframes.pd_series_ext.init_series(amlx__xuwbj,
                ybz__hqe, inyj__kppe)
        return impl_series
    if arg_a == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        thrf__qsun = np.dtype('datetime64[ns]')
        iNaT = pd._libs.tslibs.iNaT

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            qxd__epfyi = len(arg_a)
            duy__waad = np.empty(qxd__epfyi, thrf__qsun)
            for yjs__hvrb in numba.parfors.parfor.internal_prange(qxd__epfyi):
                val = iNaT
                if not bodo.libs.array_kernels.isna(arg_a, yjs__hvrb):
                    data = arg_a[yjs__hvrb]
                    val = (bodo.hiframes.pd_timestamp_ext.
                        npy_datetimestruct_to_datetime(data.year, data.
                        month, data.day, 0, 0, 0, 0))
                duy__waad[yjs__hvrb
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(duy__waad,
                None)
        return impl_date_arr
    if arg_a == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return (lambda arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True: bodo.
            hiframes.pd_index_ext.init_datetime_index(arg_a, None))
    if arg_a == string_array_type:

        def impl_string_array(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return pandas_string_array_to_datetime(arg_a, errors, dayfirst,
                yearfirst, utc, format, exact, unit, infer_datetime_format,
                origin, cache)
        return impl_string_array
    if isinstance(arg_a, types.Array) and isinstance(arg_a.dtype, types.Integer
        ):
        thrf__qsun = np.dtype('datetime64[ns]')

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            qxd__epfyi = len(arg_a)
            duy__waad = np.empty(qxd__epfyi, thrf__qsun)
            for yjs__hvrb in numba.parfors.parfor.internal_prange(qxd__epfyi):
                data = arg_a[yjs__hvrb]
                val = to_datetime_scalar(data, errors=errors, dayfirst=
                    dayfirst, yearfirst=yearfirst, utc=utc, format=format,
                    exact=exact, unit=unit, infer_datetime_format=
                    infer_datetime_format, origin=origin, cache=cache)
                duy__waad[yjs__hvrb
                    ] = bodo.hiframes.pd_timestamp_ext.datetime_datetime_to_dt64(
                    val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(duy__waad,
                None)
        return impl_date_arr
    if isinstance(arg_a, CategoricalArrayType
        ) and arg_a.dtype.elem_type == bodo.string_type:
        thrf__qsun = np.dtype('datetime64[ns]')

        def impl_cat_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            qxd__epfyi = len(arg_a)
            duy__waad = np.empty(qxd__epfyi, thrf__qsun)
            fvptf__yvyo = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arg_a))
            puvwe__wzk = pandas_string_array_to_datetime(arg_a.dtype.
                categories.values, errors, dayfirst, yearfirst, utc, format,
                exact, unit, infer_datetime_format, origin, cache).values
            for yjs__hvrb in numba.parfors.parfor.internal_prange(qxd__epfyi):
                c = fvptf__yvyo[yjs__hvrb]
                if c == -1:
                    bodo.libs.array_kernels.setna(duy__waad, yjs__hvrb)
                    continue
                duy__waad[yjs__hvrb] = puvwe__wzk[c]
            return bodo.hiframes.pd_index_ext.init_datetime_index(duy__waad,
                None)
        return impl_cat_arr
    if arg_a == bodo.dict_str_arr_type:

        def impl_dict_str_arr(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            duy__waad = pandas_dict_string_array_to_datetime(arg_a, errors,
                dayfirst, yearfirst, utc, format, exact, unit,
                infer_datetime_format, origin, cache)
            return bodo.hiframes.pd_index_ext.init_datetime_index(duy__waad,
                None)
        return impl_dict_str_arr
    if isinstance(arg_a, PandasTimestampType):

        def impl_timestamp(arg_a, errors='raise', dayfirst=False, yearfirst
            =False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return arg_a
        return impl_timestamp
    if arg_a == bodo.datetime64ns:

        def impl_np_datetime(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return pd.Timestamp(arg_a)
        return impl_np_datetime
    if is_overload_none(arg_a):

        def impl_np_datetime(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return None
        return impl_np_datetime
    raise_bodo_error(f'pd.to_datetime(): cannot convert date type {arg_a}')


@overload(pd.to_timedelta, inline='always', no_unliteral=True)
def overload_to_timedelta(arg_a, unit='ns', errors='raise'):
    if not is_overload_constant_str(unit):
        raise BodoError(
            'pandas.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    if isinstance(arg_a, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(arg_a, unit='ns', errors='raise'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            ybz__hqe = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            inyj__kppe = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            amlx__xuwbj = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_timedelta(arr, unit, errors))
            return bodo.hiframes.pd_series_ext.init_series(amlx__xuwbj,
                ybz__hqe, inyj__kppe)
        return impl_series
    if is_overload_constant_str(arg_a) or arg_a in (pd_timedelta_type,
        datetime_timedelta_type, bodo.string_type):

        def impl_string(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a)
        return impl_string
    if isinstance(arg_a, types.Float):
        m, sei__smykc = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_float_scalar(arg_a, unit='ns', errors='raise'):
            val = float_to_timedelta_val(arg_a, sei__smykc, m)
            return pd.Timedelta(val)
        return impl_float_scalar
    if isinstance(arg_a, types.Integer):
        m, fpn__ivuqz = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_integer_scalar(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a * m)
        return impl_integer_scalar
    if is_iterable_type(arg_a) and not isinstance(arg_a, types.BaseTuple):
        m, sei__smykc = pd._libs.tslibs.conversion.precision_from_unit(unit)
        qzpd__uuwy = np.dtype('timedelta64[ns]')
        if isinstance(arg_a.dtype, types.Float):

            def impl_float(arg_a, unit='ns', errors='raise'):
                qxd__epfyi = len(arg_a)
                duy__waad = np.empty(qxd__epfyi, qzpd__uuwy)
                for yjs__hvrb in numba.parfors.parfor.internal_prange(
                    qxd__epfyi):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, yjs__hvrb):
                        val = float_to_timedelta_val(arg_a[yjs__hvrb],
                            sei__smykc, m)
                    duy__waad[yjs__hvrb
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    duy__waad, None)
            return impl_float
        if isinstance(arg_a.dtype, types.Integer):

            def impl_int(arg_a, unit='ns', errors='raise'):
                qxd__epfyi = len(arg_a)
                duy__waad = np.empty(qxd__epfyi, qzpd__uuwy)
                for yjs__hvrb in numba.parfors.parfor.internal_prange(
                    qxd__epfyi):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, yjs__hvrb):
                        val = arg_a[yjs__hvrb] * m
                    duy__waad[yjs__hvrb
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    duy__waad, None)
            return impl_int
        if arg_a.dtype == bodo.timedelta64ns:

            def impl_td64(arg_a, unit='ns', errors='raise'):
                arr = bodo.utils.conversion.coerce_to_ndarray(arg_a)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(arr,
                    None)
            return impl_td64
        if arg_a.dtype == bodo.string_type or isinstance(arg_a.dtype, types
            .UnicodeCharSeq):

            def impl_str(arg_a, unit='ns', errors='raise'):
                return pandas_string_array_to_timedelta(arg_a, unit, errors)
            return impl_str
        if arg_a.dtype == datetime_timedelta_type:

            def impl_datetime_timedelta(arg_a, unit='ns', errors='raise'):
                qxd__epfyi = len(arg_a)
                duy__waad = np.empty(qxd__epfyi, qzpd__uuwy)
                for yjs__hvrb in numba.parfors.parfor.internal_prange(
                    qxd__epfyi):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, yjs__hvrb):
                        aei__gwifk = arg_a[yjs__hvrb]
                        val = (aei__gwifk.microseconds + 1000 * 1000 * (
                            aei__gwifk.seconds + 24 * 60 * 60 * aei__gwifk.
                            days)) * 1000
                    duy__waad[yjs__hvrb
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    duy__waad, None)
            return impl_datetime_timedelta
    if is_overload_none(arg_a):
        return lambda arg_a, unit='ns', errors='raise': None
    raise_bodo_error(
        f'pd.to_timedelta(): cannot convert date type {arg_a.dtype}')


@register_jitable
def float_to_timedelta_val(data, precision, multiplier):
    knj__kfkg = np.int64(data)
    dgmy__abvx = data - knj__kfkg
    if precision:
        dgmy__abvx = np.round(dgmy__abvx, precision)
    return knj__kfkg * multiplier + np.int64(dgmy__abvx * multiplier)


@numba.njit
def pandas_string_array_to_timedelta(arg_a, unit='ns', errors='raise'):
    with numba.objmode(result='timedelta_index'):
        result = pd.to_timedelta(arg_a, errors=errors)
    return result


def create_timestamp_cmp_op_overload(op):

    def overload_date_timestamp_cmp(lhs, rhs):
        if isinstance(lhs, PandasTimestampType
            ) and rhs == bodo.hiframes.datetime_date_ext.datetime_date_type:
            tz_literal = lhs.tz
            return lambda lhs, rhs: op(lhs, pd.Timestamp(rhs, tz=tz_literal))
        if (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
            isinstance(rhs, PandasTimestampType)):
            tz_literal = rhs.tz
            return lambda lhs, rhs: op(pd.Timestamp(lhs, tz=tz_literal), rhs)
        if isinstance(lhs, PandasTimestampType) and isinstance(rhs,
            PandasTimestampType):
            if lhs.tz != rhs.tz:
                raise BodoError(
                    f'{numba.core.utils.OPERATORS_TO_BUILTINS[op]} with two Timestamps requires both Timestamps share the same timezone. '
                     +
                    f'Argument 0 has timezone {lhs.tz} and argument 1 has timezone {rhs.tz}. '
                     +
                    'To compare these values please convert to timezone naive with ts.tz_convert(None).'
                    )
            return lambda lhs, rhs: op(lhs.value, rhs.value)
        if lhs == pd_timestamp_tz_naive_type and rhs == bodo.datetime64ns:
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                integer_to_dt64(lhs.value), rhs)
        if lhs == bodo.datetime64ns and rhs == pd_timestamp_tz_naive_type:
            return lambda lhs, rhs: op(lhs, bodo.hiframes.pd_timestamp_ext.
                integer_to_dt64(rhs.value))
    return overload_date_timestamp_cmp


@overload_method(PandasTimestampType, 'toordinal', no_unliteral=True)
def toordinal(date):

    def impl(date):
        return _ymd2ord(date.year, date.month, date.day)
    return impl


def overload_freq_methods(method):

    def freq_overload(td, freq, ambiguous='raise', nonexistent='raise'):
        zfpn__omk = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        bvhxi__ktdj = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Timestamp.{method}', zfpn__omk,
            bvhxi__ktdj, package_name='pandas', module_name='Timestamp')
        traea__iapv = ["freq == 'D'", "freq == 'H'",
            "freq == 'min' or freq == 'T'", "freq == 'S'",
            "freq == 'ms' or freq == 'L'", "freq == 'U' or freq == 'us'",
            "freq == 'N'"]
        xmk__dxe = [24 * 60 * 60 * 1000000 * 1000, 60 * 60 * 1000000 * 1000,
            60 * 1000000 * 1000, 1000000 * 1000, 1000 * 1000, 1000, 1]
        ipk__xoo = None
        ruz__kdpys = None
        tz_literal = None
        kvd__eae = (
            "def impl(td, freq, ambiguous='raise', nonexistent='raise'):\n")
        for yjs__hvrb, mjd__ibw in enumerate(traea__iapv):
            bvae__rhohy = 'if' if yjs__hvrb == 0 else 'elif'
            kvd__eae += '    {} {}:\n'.format(bvae__rhohy, mjd__ibw)
            kvd__eae += '        unit_value = {}\n'.format(xmk__dxe[yjs__hvrb])
        kvd__eae += '    else:\n'
        kvd__eae += (
            "        raise ValueError('Incorrect Frequency specification')\n")
        if td == pd_timedelta_type:
            kvd__eae += (
                """    return pd.Timedelta(unit_value * np.int64(np.{}(td.value / unit_value)))
"""
                .format(method))
        else:
            assert isinstance(td, PandasTimestampType
                ), 'Value must be a timestamp'
            kvd__eae += f'    value = td.value\n'
            tz_literal = td.tz
            if tz_literal is not None:
                kepn__nfuwk = '0'
                vgwh__ubq = False
                if tz_has_transition_times(tz_literal):
                    vgwh__ubq = True
                    mvtze__zoym = pytz.timezone(tz_literal)
                    ruz__kdpys = np.array(mvtze__zoym._utc_transition_times,
                        dtype='M8[ns]').view('i8')
                    ipk__xoo = np.array(mvtze__zoym._transition_info)[:, 0]
                    ipk__xoo = (pd.Series(ipk__xoo).dt.total_seconds() * 
                        1000000000).astype(np.int64).values
                    kepn__nfuwk = (
                        "deltas[np.searchsorted(trans, value, side='right') - 1]"
                        )
                elif isinstance(tz_literal, str):
                    mvtze__zoym = pytz.timezone(tz_literal)
                    kepn__nfuwk = str(np.int64(mvtze__zoym._utcoffset.
                        total_seconds() * 1000000000))
                elif isinstance(tz_literal, int):
                    kepn__nfuwk = str(tz_literal)
                kvd__eae += f'    delta = {kepn__nfuwk}\n'
                kvd__eae += f'    value = value + delta\n'
            if method == 'ceil':
                kvd__eae += (
                    '    value = value + np.remainder(-value, unit_value)\n')
            if method == 'floor':
                kvd__eae += (
                    '    value = value - np.remainder(value, unit_value)\n')
            if method == 'round':
                kvd__eae += '    if unit_value == 1:\n'
                kvd__eae += '        value = value\n'
                kvd__eae += '    else:\n'
                kvd__eae += (
                    '        quotient, remainder = np.divmod(value, unit_value)\n'
                    )
                kvd__eae += """        mask = np.logical_or(remainder > (unit_value // 2), np.logical_and(remainder == (unit_value // 2), quotient % 2))
"""
                kvd__eae += '        if mask:\n'
                kvd__eae += '            quotient = quotient + 1\n'
                kvd__eae += '        value = quotient * unit_value\n'
            if tz_literal is not None:
                if vgwh__ubq:
                    kvd__eae += f'    original_value = value\n'
                    kvd__eae += """    start_trans = deltas[np.searchsorted(trans, original_value, side='right') - 1]
"""
                    kvd__eae += '    value = value - start_trans\n'
                    kvd__eae += """    end_trans = deltas[np.searchsorted(trans, value, side='right') - 1]
"""
                    kvd__eae += '    offset = start_trans - end_trans\n'
                    kvd__eae += '    value = value + offset\n'
                else:
                    kvd__eae += f'    value = value - delta\n'
            kvd__eae += '    return pd.Timestamp(value, tz=tz_literal)\n'
        nun__bif = {}
        exec(kvd__eae, {'np': np, 'pd': pd, 'deltas': ipk__xoo, 'trans':
            ruz__kdpys, 'tz_literal': tz_literal}, nun__bif)
        impl = nun__bif['impl']
        return impl
    return freq_overload


def _install_freq_methods():
    nrb__vcsf = ['ceil', 'floor', 'round']
    for method in nrb__vcsf:
        bwje__cky = overload_freq_methods(method)
        overload_method(PDTimeDeltaType, method, no_unliteral=True)(bwje__cky)
        overload_method(PandasTimestampType, method, no_unliteral=True)(
            bwje__cky)


_install_freq_methods()


@register_jitable
def compute_pd_timestamp(totmicrosec, nanosecond):
    microsecond = totmicrosec % 1000000
    gaxcu__hvy = totmicrosec // 1000000
    second = gaxcu__hvy % 60
    yfv__omkl = gaxcu__hvy // 60
    minute = yfv__omkl % 60
    zim__xybw = yfv__omkl // 60
    hour = zim__xybw % 24
    bbmjs__picm = zim__xybw // 24
    year, month, day = _ord2ymd(bbmjs__picm)
    value = npy_datetimestruct_to_datetime(year, month, day, hour, minute,
        second, microsecond)
    value += zero_if_none(nanosecond)
    return init_timestamp(year, month, day, hour, minute, second,
        microsecond, nanosecond, value, None)


def overload_sub_operator_timestamp(lhs, rhs):
    if isinstance(lhs, PandasTimestampType) and rhs == datetime_timedelta_type:
        tz_literal = lhs.tz

        def impl(lhs, rhs):
            sajtl__tyos = bodo.hiframes.datetime_timedelta_ext._to_nanoseconds(
                rhs)
            return pd.Timestamp(lhs.value - sajtl__tyos, tz=tz_literal)
        return impl
    if lhs == pd_timestamp_tz_naive_type and rhs == pd_timestamp_tz_naive_type:

        def impl_timestamp(lhs, rhs):
            return convert_numpy_timedelta64_to_pd_timedelta(lhs.value -
                rhs.value)
        return impl_timestamp
    if isinstance(lhs, PandasTimestampType) and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


def overload_add_operator_timestamp(lhs, rhs):
    if isinstance(lhs, PandasTimestampType) and rhs == datetime_timedelta_type:
        tz_literal = lhs.tz

        def impl(lhs, rhs):
            sajtl__tyos = bodo.hiframes.datetime_timedelta_ext._to_nanoseconds(
                rhs)
            return pd.Timestamp(lhs.value + sajtl__tyos, tz=tz_literal)
        return impl
    if isinstance(lhs, PandasTimestampType) and rhs == pd_timedelta_type:
        tz_literal = lhs.tz

        def impl(lhs, rhs):
            return pd.Timestamp(lhs.value + rhs.value, tz=tz_literal)
        return impl
    if lhs == pd_timedelta_type and isinstance(rhs, PandasTimestampType
        ) or lhs == datetime_timedelta_type and isinstance(rhs,
        PandasTimestampType):

        def impl(lhs, rhs):
            return rhs + lhs
        return impl


@overload(min, no_unliteral=True)
def timestamp_min(lhs, rhs):
    check_tz_aware_unsupported(lhs, f'Timestamp.min()')
    check_tz_aware_unsupported(rhs, f'Timestamp.min()')
    if lhs == pd_timestamp_tz_naive_type and rhs == pd_timestamp_tz_naive_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@overload(max, no_unliteral=True)
def timestamp_max(lhs, rhs):
    check_tz_aware_unsupported(lhs, f'Timestamp.max()')
    check_tz_aware_unsupported(rhs, f'Timestamp.max()')
    if lhs == pd_timestamp_tz_naive_type and rhs == pd_timestamp_tz_naive_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload_method(DatetimeDateType, 'strftime')
@overload_method(PandasTimestampType, 'strftime')
def strftime(ts, format):
    if isinstance(ts, DatetimeDateType):
        nwjrs__swhx = 'datetime.date'
    else:
        nwjrs__swhx = 'pandas.Timestamp'
    if types.unliteral(format) != types.unicode_type:
        raise BodoError(
            f"{nwjrs__swhx}.strftime(): 'strftime' argument must be a string")

    def impl(ts, format):
        with numba.objmode(res='unicode_type'):
            res = ts.strftime(format)
        return res
    return impl


@overload_method(PandasTimestampType, 'to_datetime64')
def to_datetime64(ts):

    def impl(ts):
        return integer_to_dt64(ts.value)
    return impl


def now_impl(tz=None):
    pass


@overload(now_impl, no_unilteral=True)
def now_impl_overload(tz=None):
    if is_overload_none(tz):
        acd__wopgo = PandasTimestampType(None)
    elif is_overload_constant_str(tz):
        acd__wopgo = PandasTimestampType(get_overload_const_str(tz))
    elif is_overload_constant_int(tz):
        acd__wopgo = PandasTimestampType(get_overload_const_int(tz))
    else:
        raise_bodo_error(
            'pandas.Timestamp.now(): tz argument must be a constant string or integer literal if provided'
            )

    def impl(tz=None):
        with numba.objmode(d=acd__wopgo):
            d = pd.Timestamp.now(tz)
        return d
    return impl


class CompDT64(ConcreteTemplate):
    cases = [signature(types.boolean, types.NPDatetime('ns'), types.
        NPDatetime('ns'))]


@infer_global(operator.lt)
class CmpOpLt(CompDT64):
    key = operator.lt


@infer_global(operator.le)
class CmpOpLe(CompDT64):
    key = operator.le


@infer_global(operator.gt)
class CmpOpGt(CompDT64):
    key = operator.gt


@infer_global(operator.ge)
class CmpOpGe(CompDT64):
    key = operator.ge


@infer_global(operator.eq)
class CmpOpEq(CompDT64):
    key = operator.eq


@infer_global(operator.ne)
class CmpOpNe(CompDT64):
    key = operator.ne


@typeof_impl.register(calendar._localized_month)
def typeof_python_calendar(val, c):
    return types.Tuple([types.StringLiteral(rraws__axuu) for rraws__axuu in
        val])


@overload(str)
def overload_datetime64_str(val):
    if val == bodo.datetime64ns:

        def impl(val):
            return (bodo.hiframes.pd_timestamp_ext.
                convert_datetime64_to_timestamp(val).isoformat('T'))
        return impl


timestamp_unsupported_attrs = ['asm8', 'components', 'freqstr', 'tz',
    'fold', 'tzinfo', 'freq']
timestamp_unsupported_methods = ['astimezone', 'ctime', 'dst', 'isoweekday',
    'replace', 'strptime', 'time', 'timestamp', 'timetuple', 'timetz',
    'to_julian_date', 'to_numpy', 'to_period', 'to_pydatetime', 'tzname',
    'utcoffset', 'utctimetuple']


def _install_pd_timestamp_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for kjw__wnl in timestamp_unsupported_attrs:
        fpq__fmic = 'pandas.Timestamp.' + kjw__wnl
        overload_attribute(PandasTimestampType, kjw__wnl)(
            create_unsupported_overload(fpq__fmic))
    for xhwo__kms in timestamp_unsupported_methods:
        fpq__fmic = 'pandas.Timestamp.' + xhwo__kms
        overload_method(PandasTimestampType, xhwo__kms)(
            create_unsupported_overload(fpq__fmic + '()'))


_install_pd_timestamp_unsupported()


@lower_builtin(numba.core.types.functions.NumberClass,
    pd_timestamp_tz_naive_type, types.StringLiteral)
def datetime64_constructor(context, builder, sig, args):

    def datetime64_constructor_impl(a, b):
        return integer_to_dt64(a.value)
    return context.compile_internal(builder, datetime64_constructor_impl,
        sig, args)
