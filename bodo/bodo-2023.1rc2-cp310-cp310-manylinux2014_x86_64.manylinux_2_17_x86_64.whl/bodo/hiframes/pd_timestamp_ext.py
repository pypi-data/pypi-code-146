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
            edeo__wafmy = 'PandasTimestampType()'
        else:
            edeo__wafmy = f'PandasTimestampType({tz_val})'
        super(PandasTimestampType, self).__init__(name=edeo__wafmy)


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
        for irbyl__ipnrr in val.data:
            if isinstance(irbyl__ipnrr, bodo.DatetimeArrayType):
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
        rekim__jjl = [('year', ts_field_typ), ('month', ts_field_typ), (
            'day', ts_field_typ), ('hour', ts_field_typ), ('minute',
            ts_field_typ), ('second', ts_field_typ), ('microsecond',
            ts_field_typ), ('nanosecond', ts_field_typ), ('value',
            ts_field_typ)]
        models.StructModel.__init__(self, dmm, fe_type, rekim__jjl)


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
    xnw__vxki = c.pyapi.object_getattr_string(val, 'year')
    bpcmq__wgnz = c.pyapi.object_getattr_string(val, 'month')
    pdl__yhei = c.pyapi.object_getattr_string(val, 'day')
    flks__ctr = c.pyapi.object_getattr_string(val, 'hour')
    hogg__invse = c.pyapi.object_getattr_string(val, 'minute')
    qvkf__xjgsb = c.pyapi.object_getattr_string(val, 'second')
    dqex__ytw = c.pyapi.object_getattr_string(val, 'microsecond')
    ujn__vbxf = c.pyapi.object_getattr_string(val, 'nanosecond')
    fnlp__olvfm = c.pyapi.object_getattr_string(val, 'value')
    udf__kzktk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    udf__kzktk.year = c.pyapi.long_as_longlong(xnw__vxki)
    udf__kzktk.month = c.pyapi.long_as_longlong(bpcmq__wgnz)
    udf__kzktk.day = c.pyapi.long_as_longlong(pdl__yhei)
    udf__kzktk.hour = c.pyapi.long_as_longlong(flks__ctr)
    udf__kzktk.minute = c.pyapi.long_as_longlong(hogg__invse)
    udf__kzktk.second = c.pyapi.long_as_longlong(qvkf__xjgsb)
    udf__kzktk.microsecond = c.pyapi.long_as_longlong(dqex__ytw)
    udf__kzktk.nanosecond = c.pyapi.long_as_longlong(ujn__vbxf)
    udf__kzktk.value = c.pyapi.long_as_longlong(fnlp__olvfm)
    c.pyapi.decref(xnw__vxki)
    c.pyapi.decref(bpcmq__wgnz)
    c.pyapi.decref(pdl__yhei)
    c.pyapi.decref(flks__ctr)
    c.pyapi.decref(hogg__invse)
    c.pyapi.decref(qvkf__xjgsb)
    c.pyapi.decref(dqex__ytw)
    c.pyapi.decref(ujn__vbxf)
    c.pyapi.decref(fnlp__olvfm)
    dkkt__uckk = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(udf__kzktk._getvalue(), is_error=dkkt__uckk)


@box(PandasTimestampType)
def box_pandas_timestamp(typ, val, c):
    vaddy__usdgd = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    xnw__vxki = c.pyapi.long_from_longlong(vaddy__usdgd.year)
    bpcmq__wgnz = c.pyapi.long_from_longlong(vaddy__usdgd.month)
    pdl__yhei = c.pyapi.long_from_longlong(vaddy__usdgd.day)
    flks__ctr = c.pyapi.long_from_longlong(vaddy__usdgd.hour)
    hogg__invse = c.pyapi.long_from_longlong(vaddy__usdgd.minute)
    qvkf__xjgsb = c.pyapi.long_from_longlong(vaddy__usdgd.second)
    qaes__crab = c.pyapi.long_from_longlong(vaddy__usdgd.microsecond)
    voaas__bvrd = c.pyapi.long_from_longlong(vaddy__usdgd.nanosecond)
    ojy__nncve = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timestamp))
    if typ.tz is None:
        res = c.pyapi.call_function_objargs(ojy__nncve, (xnw__vxki,
            bpcmq__wgnz, pdl__yhei, flks__ctr, hogg__invse, qvkf__xjgsb,
            qaes__crab, voaas__bvrd))
    else:
        if isinstance(typ.tz, int):
            rwwga__dhpub = c.pyapi.long_from_longlong(lir.Constant(lir.
                IntType(64), typ.tz))
        else:
            mnd__zeihc = c.context.insert_const_string(c.builder.module,
                str(typ.tz))
            rwwga__dhpub = c.pyapi.string_from_string(mnd__zeihc)
        args = c.pyapi.tuple_pack(())
        kwargs = c.pyapi.dict_pack([('year', xnw__vxki), ('month',
            bpcmq__wgnz), ('day', pdl__yhei), ('hour', flks__ctr), (
            'minute', hogg__invse), ('second', qvkf__xjgsb), ('microsecond',
            qaes__crab), ('nanosecond', voaas__bvrd), ('tz', rwwga__dhpub)])
        res = c.pyapi.call(ojy__nncve, args, kwargs)
        c.pyapi.decref(args)
        c.pyapi.decref(kwargs)
        c.pyapi.decref(rwwga__dhpub)
    c.pyapi.decref(xnw__vxki)
    c.pyapi.decref(bpcmq__wgnz)
    c.pyapi.decref(pdl__yhei)
    c.pyapi.decref(flks__ctr)
    c.pyapi.decref(hogg__invse)
    c.pyapi.decref(qvkf__xjgsb)
    c.pyapi.decref(qaes__crab)
    c.pyapi.decref(voaas__bvrd)
    return res


@intrinsic
def init_timestamp(typingctx, year, month, day, hour, minute, second,
    microsecond, nanosecond, value, tz):

    def codegen(context, builder, sig, args):
        (year, month, day, hour, minute, second, uotb__nim, pbu__kkuyd,
            value, xcg__wocz) = args
        ts = cgutils.create_struct_proxy(sig.return_type)(context, builder)
        ts.year = year
        ts.month = month
        ts.day = day
        ts.hour = hour
        ts.minute = minute
        ts.second = second
        ts.microsecond = uotb__nim
        ts.nanosecond = pbu__kkuyd
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
        bgvug__lhe = pytz.timezone(tz)
        return isinstance(bgvug__lhe, pytz.tzinfo.DstTzInfo)
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
        twof__irf, precision = pd._libs.tslibs.conversion.precision_from_unit(
            unit)
        if isinstance(ts_input, types.Integer):

            def impl_int(ts_input=_no_input, freq=None, tz=None, unit=None,
                year=None, month=None, day=None, hour=None, minute=None,
                second=None, microsecond=None, nanosecond=None, tzinfo=None):
                value = ts_input * twof__irf
                return convert_val_to_timestamp(value, tz)
            return impl_int

        def impl_float(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            duvfk__pxpz = np.int64(ts_input)
            nlti__lpud = ts_input - duvfk__pxpz
            if precision:
                nlti__lpud = np.round(nlti__lpud, precision)
            value = duvfk__pxpz * twof__irf + np.int64(nlti__lpud * twof__irf)
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
        twof__irf, precision = pd._libs.tslibs.conversion.precision_from_unit(
            ts_input.unit)

        def impl_date(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            value = np.int64(ts_input) * twof__irf
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
        xcg__wocz, qino__xcr, xcg__wocz = get_isocalendar(ptt.year, ptt.
            month, ptt.day)
        return qino__xcr
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
        year, qino__xcr, vrg__chykd = get_isocalendar(ptt.year, ptt.month,
            ptt.day)
        return year, qino__xcr, vrg__chykd
    return impl


@overload_method(PandasTimestampType, 'isoformat', no_unliteral=True)
def overload_pd_timestamp_isoformat(ts, sep=None):
    if is_overload_none(sep):

        def timestamp_isoformat_impl(ts, sep=None):
            swylw__glig = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            if ts.microsecond != 0:
                swylw__glig += '.' + str_2d(ts.microsecond)
                if ts.nanosecond != 0:
                    swylw__glig += str_2d(ts.nanosecond)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + 'T' + swylw__glig
            return res
        return timestamp_isoformat_impl
    else:

        def timestamp_isoformat_impl(ts, sep=None):
            swylw__glig = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            if ts.microsecond != 0:
                swylw__glig += '.' + str_2d(ts.microsecond)
                if ts.nanosecond != 0:
                    swylw__glig += str_2d(ts.nanosecond)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + sep + swylw__glig
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
    acm__qiewf = dict(locale=locale)
    sroh__ntkkc = dict(locale=None)
    check_unsupported_args('Timestamp.day_name', acm__qiewf, sroh__ntkkc,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        wmjc__zfakc = ('Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday')
        xcg__wocz, xcg__wocz, tcqf__kfu = ptt.isocalendar()
        return wmjc__zfakc[tcqf__kfu - 1]
    return impl


@overload_method(PandasTimestampType, 'month_name', no_unliteral=True)
def overload_pd_timestamp_month_name(ptt, locale=None):
    acm__qiewf = dict(locale=locale)
    sroh__ntkkc = dict(locale=None)
    check_unsupported_args('Timestamp.month_name', acm__qiewf, sroh__ntkkc,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        ywxi__sqbd = ('January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September', 'October', 'November',
            'December')
        return ywxi__sqbd[ptt.month - 1]
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
    acm__qiewf = dict(ambiguous=ambiguous, nonexistent=nonexistent)
    piuob__dugt = dict(ambiguous='raise', nonexistent='raise')
    check_unsupported_args('Timestamp.tz_localize', acm__qiewf, piuob__dugt,
        package_name='pandas', module_name='Timestamp')
    if is_overload_none(tz) and ptt.tz is None:
        return lambda ptt, tz, ambiguous='raise', nonexistent='raise': ptt
    if is_overload_none(tz):
        imyv__uvftr = ptt.tz
        hsn__llt = False
    else:
        if not is_literal_type(tz):
            raise_bodo_error(
                'Timestamp.tz_localize(): tz value must be a literal string, integer, or None'
                )
        imyv__uvftr = get_literal_value(tz)
        hsn__llt = True
    kjp__qlg = None
    etct__pyvr = None
    ayfb__abc = False
    if tz_has_transition_times(imyv__uvftr):
        ayfb__abc = hsn__llt
        rwwga__dhpub = pytz.timezone(imyv__uvftr)
        etct__pyvr = np.array(rwwga__dhpub._utc_transition_times, dtype=
            'M8[ns]').view('i8')
        kjp__qlg = np.array(rwwga__dhpub._transition_info)[:, 0]
        kjp__qlg = (pd.Series(kjp__qlg).dt.total_seconds() * 1000000000
            ).astype(np.int64).values
        abcwm__rvwsx = (
            "deltas[np.searchsorted(trans, value, side='right') - 1]")
    elif isinstance(imyv__uvftr, str):
        rwwga__dhpub = pytz.timezone(imyv__uvftr)
        abcwm__rvwsx = str(np.int64(rwwga__dhpub._utcoffset.total_seconds() *
            1000000000))
    elif isinstance(imyv__uvftr, int):
        abcwm__rvwsx = str(imyv__uvftr)
    else:
        raise_bodo_error(
            'Timestamp.tz_localize(): tz value must be a literal string, integer, or None'
            )
    if hsn__llt:
        kugxv__lem = '-'
    else:
        kugxv__lem = '+'
    ynq__ypim = "def impl(ptt, tz, ambiguous='raise', nonexistent='raise'):\n"
    ynq__ypim += f'    value =  ptt.value\n'
    ynq__ypim += f'    delta =  {abcwm__rvwsx}\n'
    ynq__ypim += f'    new_value = value {kugxv__lem} delta\n'
    if ayfb__abc:
        ynq__ypim += """    end_delta = deltas[np.searchsorted(trans, new_value, side='right') - 1]
"""
        ynq__ypim += '    offset = delta - end_delta\n'
        ynq__ypim += '    new_value = new_value + offset\n'
    ynq__ypim += f'    return convert_val_to_timestamp(new_value, tz=tz)\n'
    fteob__jiez = {}
    exec(ynq__ypim, {'np': np, 'convert_val_to_timestamp':
        convert_val_to_timestamp, 'trans': etct__pyvr, 'deltas': kjp__qlg},
        fteob__jiez)
    impl = fteob__jiez['impl']
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
        wgj__qrai = cgutils.alloca_once(builder, lir.IntType(64))
        builder.store(args[0], wgj__qrai)
        year = cgutils.alloca_once(builder, lir.IntType(64))
        rauw__dtgha = cgutils.alloca_once(builder, lir.IntType(64))
        xrab__eevj = lir.FunctionType(lir.VoidType(), [lir.IntType(64).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        hvf__bchog = cgutils.get_or_insert_function(builder.module,
            xrab__eevj, name='extract_year_days')
        builder.call(hvf__bchog, [wgj__qrai, year, rauw__dtgha])
        return cgutils.pack_array(builder, [builder.load(wgj__qrai),
            builder.load(year), builder.load(rauw__dtgha)])
    return types.Tuple([types.int64, types.int64, types.int64])(dt64_t
        ), codegen


@intrinsic
def get_month_day(typingctx, year_t, days_t=None):
    assert year_t == types.int64
    assert days_t == types.int64

    def codegen(context, builder, sig, args):
        month = cgutils.alloca_once(builder, lir.IntType(64))
        day = cgutils.alloca_once(builder, lir.IntType(64))
        xrab__eevj = lir.FunctionType(lir.VoidType(), [lir.IntType(64), lir
            .IntType(64), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        hvf__bchog = cgutils.get_or_insert_function(builder.module,
            xrab__eevj, name='get_month_day')
        builder.call(hvf__bchog, [args[0], args[1], month, day])
        return cgutils.pack_array(builder, [builder.load(month), builder.
            load(day)])
    return types.Tuple([types.int64, types.int64])(types.int64, types.int64
        ), codegen


@register_jitable
def get_day_of_year(year, month, day):
    dhsm__qkni = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 
        365, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    nzvxa__qpu = is_leap_year(year)
    rfeqj__rgg = dhsm__qkni[nzvxa__qpu * 13 + month - 1]
    bnz__dfeyb = rfeqj__rgg + day
    return bnz__dfeyb


@register_jitable
def get_day_of_week(y, m, d):
    kucji__gxy = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    y -= m < 3
    day = (y + y // 4 - y // 100 + y // 400 + kucji__gxy[m - 1] + d) % 7
    return (day + 6) % 7


@register_jitable
def get_days_in_month(year, month):
    is_leap_year = year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)
    xakk__bvmsc = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 29, 
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return xakk__bvmsc[12 * is_leap_year + month - 1]


@register_jitable
def is_leap_year(year):
    return year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)


@numba.generated_jit(nopython=True)
def compute_val_for_timestamp(year, month, day, hour, minute, second,
    microsecond, nanosecond, tz):
    abcwm__rvwsx = '0'
    imyv__uvftr = get_literal_value(tz)
    kjp__qlg = None
    etct__pyvr = None
    ayfb__abc = False
    if tz_has_transition_times(imyv__uvftr):
        ayfb__abc = True
        rwwga__dhpub = pytz.timezone(imyv__uvftr)
        etct__pyvr = np.array(rwwga__dhpub._utc_transition_times, dtype=
            'M8[ns]').view('i8')
        kjp__qlg = np.array(rwwga__dhpub._transition_info)[:, 0]
        kjp__qlg = (pd.Series(kjp__qlg).dt.total_seconds() * 1000000000
            ).astype(np.int64).values
        abcwm__rvwsx = (
            "deltas[np.searchsorted(trans, original_value, side='right') - 1]")
    elif isinstance(imyv__uvftr, str):
        rwwga__dhpub = pytz.timezone(imyv__uvftr)
        abcwm__rvwsx = str(np.int64(rwwga__dhpub._utcoffset.total_seconds() *
            1000000000))
    elif isinstance(imyv__uvftr, int):
        abcwm__rvwsx = str(imyv__uvftr)
    elif imyv__uvftr is not None:
        raise_bodo_error(
            'compute_val_for_timestamp(): tz value must be a constant string, integer or None'
            )
    ynq__ypim = (
        'def impl(year, month, day, hour, minute, second, microsecond, nanosecond, tz):\n'
        )
    ynq__ypim += f"""  original_value = npy_datetimestruct_to_datetime(year, month, day, hour, minute, second, microsecond) + nanosecond
"""
    ynq__ypim += f'  value = original_value - {abcwm__rvwsx}\n'
    if ayfb__abc:
        ynq__ypim += (
            "  start_trans = np.searchsorted(trans, original_value, side='right') - 1\n"
            )
        ynq__ypim += (
            "  end_trans = np.searchsorted(trans, value, side='right') - 1\n")
        ynq__ypim += '  offset = deltas[start_trans] - deltas[end_trans]\n'
        ynq__ypim += '  value = value + offset\n'
    ynq__ypim += '  return init_timestamp(\n'
    ynq__ypim += '    year=year,\n'
    ynq__ypim += '    month=month,\n'
    ynq__ypim += '    day=day,\n'
    ynq__ypim += '    hour=hour,\n'
    ynq__ypim += '    minute=minute,'
    ynq__ypim += '    second=second,\n'
    ynq__ypim += '    microsecond=microsecond,\n'
    ynq__ypim += '    nanosecond=nanosecond,\n'
    ynq__ypim += f'    value=value,\n'
    ynq__ypim += '    tz=tz,\n'
    ynq__ypim += '  )\n'
    fteob__jiez = {}
    exec(ynq__ypim, {'np': np, 'pd': pd, 'init_timestamp': init_timestamp,
        'npy_datetimestruct_to_datetime': npy_datetimestruct_to_datetime,
        'trans': etct__pyvr, 'deltas': kjp__qlg}, fteob__jiez)
    impl = fteob__jiez['impl']
    return impl


@numba.generated_jit(nopython=True)
def convert_val_to_timestamp(ts_input, tz=None, is_convert=True):
    etct__pyvr = kjp__qlg = np.array([])
    abcwm__rvwsx = '0'
    if is_overload_constant_str(tz):
        mnd__zeihc = get_overload_const_str(tz)
        rwwga__dhpub = pytz.timezone(mnd__zeihc)
        if isinstance(rwwga__dhpub, pytz.tzinfo.DstTzInfo):
            etct__pyvr = np.array(rwwga__dhpub._utc_transition_times, dtype
                ='M8[ns]').view('i8')
            kjp__qlg = np.array(rwwga__dhpub._transition_info)[:, 0]
            kjp__qlg = (pd.Series(kjp__qlg).dt.total_seconds() * 1000000000
                ).astype(np.int64).values
            abcwm__rvwsx = (
                "deltas[np.searchsorted(trans, ts_input, side='right') - 1]")
        else:
            kjp__qlg = np.int64(rwwga__dhpub._utcoffset.total_seconds() * 
                1000000000)
            abcwm__rvwsx = 'deltas'
    elif is_overload_constant_int(tz):
        yguc__jvza = get_overload_const_int(tz)
        abcwm__rvwsx = str(yguc__jvza)
    elif not is_overload_none(tz):
        raise_bodo_error(
            'convert_val_to_timestamp(): tz value must be a constant string or None'
            )
    is_convert = get_overload_const_bool(is_convert)
    if is_convert:
        ffna__piqfi = 'tz_ts_input'
        aksxb__kelg = 'ts_input'
    else:
        ffna__piqfi = 'ts_input'
        aksxb__kelg = 'tz_ts_input'
    ynq__ypim = 'def impl(ts_input, tz=None, is_convert=True):\n'
    ynq__ypim += f'  tz_ts_input = ts_input + {abcwm__rvwsx}\n'
    ynq__ypim += (
        f'  dt, year, days = extract_year_days(integer_to_dt64({ffna__piqfi}))\n'
        )
    ynq__ypim += '  month, day = get_month_day(year, days)\n'
    ynq__ypim += '  return init_timestamp(\n'
    ynq__ypim += '    year=year,\n'
    ynq__ypim += '    month=month,\n'
    ynq__ypim += '    day=day,\n'
    ynq__ypim += '    hour=dt // (60 * 60 * 1_000_000_000),\n'
    ynq__ypim += '    minute=(dt // (60 * 1_000_000_000)) % 60,\n'
    ynq__ypim += '    second=(dt // 1_000_000_000) % 60,\n'
    ynq__ypim += '    microsecond=(dt // 1000) % 1_000_000,\n'
    ynq__ypim += '    nanosecond=dt % 1000,\n'
    ynq__ypim += f'    value={aksxb__kelg},\n'
    ynq__ypim += '    tz=tz,\n'
    ynq__ypim += '  )\n'
    fteob__jiez = {}
    exec(ynq__ypim, {'np': np, 'pd': pd, 'trans': etct__pyvr, 'deltas':
        kjp__qlg, 'integer_to_dt64': integer_to_dt64, 'extract_year_days':
        extract_year_days, 'get_month_day': get_month_day, 'init_timestamp':
        init_timestamp, 'zero_if_none': zero_if_none}, fteob__jiez)
    impl = fteob__jiez['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def convert_datetime64_to_timestamp(dt64):
    wgj__qrai, year, rauw__dtgha = extract_year_days(dt64)
    month, day = get_month_day(year, rauw__dtgha)
    return init_timestamp(year=year, month=month, day=day, hour=wgj__qrai //
        (60 * 60 * 1000000000), minute=wgj__qrai // (60 * 1000000000) % 60,
        second=wgj__qrai // 1000000000 % 60, microsecond=wgj__qrai // 1000 %
        1000000, nanosecond=wgj__qrai % 1000, value=dt64, tz=None)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_datetime_timedelta(dt64):
    owd__jkih = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    hll__rfk = owd__jkih // (86400 * 1000000000)
    oszxb__zzlao = owd__jkih - hll__rfk * 86400 * 1000000000
    miu__ixqw = oszxb__zzlao // 1000000000
    hkoj__dxgt = oszxb__zzlao - miu__ixqw * 1000000000
    ljc__nbggt = hkoj__dxgt // 1000
    return datetime.timedelta(hll__rfk, miu__ixqw, ljc__nbggt)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_pd_timedelta(dt64):
    owd__jkih = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    return pd.Timedelta(owd__jkih)


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
    tadjb__yeht = len(arr)
    lqj__nrjv = np.empty(tadjb__yeht, 'datetime64[ns]')
    thj__pui = arr._indices
    rdq__zqh = pandas_string_array_to_datetime(arr._data, errors, dayfirst,
        yearfirst, utc, format, exact, unit, infer_datetime_format, origin,
        cache).values
    for gqvta__jslj in range(tadjb__yeht):
        if bodo.libs.array_kernels.isna(thj__pui, gqvta__jslj):
            bodo.libs.array_kernels.setna(lqj__nrjv, gqvta__jslj)
            continue
        lqj__nrjv[gqvta__jslj] = rdq__zqh[thj__pui[gqvta__jslj]]
    return lqj__nrjv


@overload(pd.to_datetime, inline='always', no_unliteral=True)
def overload_to_datetime(arg_a, errors='raise', dayfirst=False, yearfirst=
    False, utc=None, format=None, exact=True, unit=None,
    infer_datetime_format=False, origin='unix', cache=True):
    robbl__fdeiq = {'errors': errors}
    vfju__fgr = {'errors': 'raise'}
    check_unsupported_args('pd.to_datetime', robbl__fdeiq, vfju__fgr,
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
            srx__opxgz = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            edeo__wafmy = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            ice__nqae = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_datetime(arr, errors=errors, dayfirst=dayfirst,
                yearfirst=yearfirst, utc=utc, format=format, exact=exact,
                unit=unit, infer_datetime_format=infer_datetime_format,
                origin=origin, cache=cache))
            return bodo.hiframes.pd_series_ext.init_series(ice__nqae,
                srx__opxgz, edeo__wafmy)
        return impl_series
    if arg_a == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        txbo__xffqr = np.dtype('datetime64[ns]')
        iNaT = pd._libs.tslibs.iNaT

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            tadjb__yeht = len(arg_a)
            lqj__nrjv = np.empty(tadjb__yeht, txbo__xffqr)
            for gqvta__jslj in numba.parfors.parfor.internal_prange(tadjb__yeht
                ):
                val = iNaT
                if not bodo.libs.array_kernels.isna(arg_a, gqvta__jslj):
                    data = arg_a[gqvta__jslj]
                    val = (bodo.hiframes.pd_timestamp_ext.
                        npy_datetimestruct_to_datetime(data.year, data.
                        month, data.day, 0, 0, 0, 0))
                lqj__nrjv[gqvta__jslj
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(lqj__nrjv,
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
        txbo__xffqr = np.dtype('datetime64[ns]')

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            tadjb__yeht = len(arg_a)
            lqj__nrjv = np.empty(tadjb__yeht, txbo__xffqr)
            for gqvta__jslj in numba.parfors.parfor.internal_prange(tadjb__yeht
                ):
                data = arg_a[gqvta__jslj]
                val = to_datetime_scalar(data, errors=errors, dayfirst=
                    dayfirst, yearfirst=yearfirst, utc=utc, format=format,
                    exact=exact, unit=unit, infer_datetime_format=
                    infer_datetime_format, origin=origin, cache=cache)
                lqj__nrjv[gqvta__jslj
                    ] = bodo.hiframes.pd_timestamp_ext.datetime_datetime_to_dt64(
                    val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(lqj__nrjv,
                None)
        return impl_date_arr
    if isinstance(arg_a, CategoricalArrayType
        ) and arg_a.dtype.elem_type == bodo.string_type:
        txbo__xffqr = np.dtype('datetime64[ns]')

        def impl_cat_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            tadjb__yeht = len(arg_a)
            lqj__nrjv = np.empty(tadjb__yeht, txbo__xffqr)
            nof__gig = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arg_a))
            rdq__zqh = pandas_string_array_to_datetime(arg_a.dtype.
                categories.values, errors, dayfirst, yearfirst, utc, format,
                exact, unit, infer_datetime_format, origin, cache).values
            for gqvta__jslj in numba.parfors.parfor.internal_prange(tadjb__yeht
                ):
                c = nof__gig[gqvta__jslj]
                if c == -1:
                    bodo.libs.array_kernels.setna(lqj__nrjv, gqvta__jslj)
                    continue
                lqj__nrjv[gqvta__jslj] = rdq__zqh[c]
            return bodo.hiframes.pd_index_ext.init_datetime_index(lqj__nrjv,
                None)
        return impl_cat_arr
    if arg_a == bodo.dict_str_arr_type:

        def impl_dict_str_arr(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            lqj__nrjv = pandas_dict_string_array_to_datetime(arg_a, errors,
                dayfirst, yearfirst, utc, format, exact, unit,
                infer_datetime_format, origin, cache)
            return bodo.hiframes.pd_index_ext.init_datetime_index(lqj__nrjv,
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
            srx__opxgz = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            edeo__wafmy = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            ice__nqae = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_timedelta(arr, unit, errors))
            return bodo.hiframes.pd_series_ext.init_series(ice__nqae,
                srx__opxgz, edeo__wafmy)
        return impl_series
    if is_overload_constant_str(arg_a) or arg_a in (pd_timedelta_type,
        datetime_timedelta_type, bodo.string_type):

        def impl_string(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a)
        return impl_string
    if isinstance(arg_a, types.Float):
        m, aolkq__fpp = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_float_scalar(arg_a, unit='ns', errors='raise'):
            val = float_to_timedelta_val(arg_a, aolkq__fpp, m)
            return pd.Timedelta(val)
        return impl_float_scalar
    if isinstance(arg_a, types.Integer):
        m, xcg__wocz = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_integer_scalar(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a * m)
        return impl_integer_scalar
    if is_iterable_type(arg_a) and not isinstance(arg_a, types.BaseTuple):
        m, aolkq__fpp = pd._libs.tslibs.conversion.precision_from_unit(unit)
        iwbr__ljk = np.dtype('timedelta64[ns]')
        if isinstance(arg_a.dtype, types.Float):

            def impl_float(arg_a, unit='ns', errors='raise'):
                tadjb__yeht = len(arg_a)
                lqj__nrjv = np.empty(tadjb__yeht, iwbr__ljk)
                for gqvta__jslj in numba.parfors.parfor.internal_prange(
                    tadjb__yeht):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, gqvta__jslj):
                        val = float_to_timedelta_val(arg_a[gqvta__jslj],
                            aolkq__fpp, m)
                    lqj__nrjv[gqvta__jslj
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    lqj__nrjv, None)
            return impl_float
        if isinstance(arg_a.dtype, types.Integer):

            def impl_int(arg_a, unit='ns', errors='raise'):
                tadjb__yeht = len(arg_a)
                lqj__nrjv = np.empty(tadjb__yeht, iwbr__ljk)
                for gqvta__jslj in numba.parfors.parfor.internal_prange(
                    tadjb__yeht):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, gqvta__jslj):
                        val = arg_a[gqvta__jslj] * m
                    lqj__nrjv[gqvta__jslj
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    lqj__nrjv, None)
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
                tadjb__yeht = len(arg_a)
                lqj__nrjv = np.empty(tadjb__yeht, iwbr__ljk)
                for gqvta__jslj in numba.parfors.parfor.internal_prange(
                    tadjb__yeht):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, gqvta__jslj):
                        qwfdv__edcjh = arg_a[gqvta__jslj]
                        val = (qwfdv__edcjh.microseconds + 1000 * 1000 * (
                            qwfdv__edcjh.seconds + 24 * 60 * 60 *
                            qwfdv__edcjh.days)) * 1000
                    lqj__nrjv[gqvta__jslj
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    lqj__nrjv, None)
            return impl_datetime_timedelta
    if is_overload_none(arg_a):
        return lambda arg_a, unit='ns', errors='raise': None
    raise_bodo_error(
        f'pd.to_timedelta(): cannot convert date type {arg_a.dtype}')


@register_jitable
def float_to_timedelta_val(data, precision, multiplier):
    duvfk__pxpz = np.int64(data)
    nlti__lpud = data - duvfk__pxpz
    if precision:
        nlti__lpud = np.round(nlti__lpud, precision)
    return duvfk__pxpz * multiplier + np.int64(nlti__lpud * multiplier)


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
        acm__qiewf = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        epu__wct = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Timestamp.{method}', acm__qiewf, epu__wct,
            package_name='pandas', module_name='Timestamp')
        sani__xga = ["freq == 'D'", "freq == 'H'",
            "freq == 'min' or freq == 'T'", "freq == 'S'",
            "freq == 'ms' or freq == 'L'", "freq == 'U' or freq == 'us'",
            "freq == 'N'"]
        pkj__xdy = [24 * 60 * 60 * 1000000 * 1000, 60 * 60 * 1000000 * 1000,
            60 * 1000000 * 1000, 1000000 * 1000, 1000 * 1000, 1000, 1]
        kjp__qlg = None
        etct__pyvr = None
        tz_literal = None
        ynq__ypim = (
            "def impl(td, freq, ambiguous='raise', nonexistent='raise'):\n")
        for gqvta__jslj, qffh__qtd in enumerate(sani__xga):
            zkd__wwae = 'if' if gqvta__jslj == 0 else 'elif'
            ynq__ypim += '    {} {}:\n'.format(zkd__wwae, qffh__qtd)
            ynq__ypim += '        unit_value = {}\n'.format(pkj__xdy[
                gqvta__jslj])
        ynq__ypim += '    else:\n'
        ynq__ypim += (
            "        raise ValueError('Incorrect Frequency specification')\n")
        if td == pd_timedelta_type:
            ynq__ypim += (
                """    return pd.Timedelta(unit_value * np.int64(np.{}(td.value / unit_value)))
"""
                .format(method))
        else:
            assert isinstance(td, PandasTimestampType
                ), 'Value must be a timestamp'
            ynq__ypim += f'    value = td.value\n'
            tz_literal = td.tz
            if tz_literal is not None:
                abcwm__rvwsx = '0'
                ghagn__flq = False
                if tz_has_transition_times(tz_literal):
                    ghagn__flq = True
                    rwwga__dhpub = pytz.timezone(tz_literal)
                    etct__pyvr = np.array(rwwga__dhpub.
                        _utc_transition_times, dtype='M8[ns]').view('i8')
                    kjp__qlg = np.array(rwwga__dhpub._transition_info)[:, 0]
                    kjp__qlg = (pd.Series(kjp__qlg).dt.total_seconds() * 
                        1000000000).astype(np.int64).values
                    abcwm__rvwsx = (
                        "deltas[np.searchsorted(trans, value, side='right') - 1]"
                        )
                elif isinstance(tz_literal, str):
                    rwwga__dhpub = pytz.timezone(tz_literal)
                    abcwm__rvwsx = str(np.int64(rwwga__dhpub._utcoffset.
                        total_seconds() * 1000000000))
                elif isinstance(tz_literal, int):
                    abcwm__rvwsx = str(tz_literal)
                ynq__ypim += f'    delta = {abcwm__rvwsx}\n'
                ynq__ypim += f'    value = value + delta\n'
            if method == 'ceil':
                ynq__ypim += (
                    '    value = value + np.remainder(-value, unit_value)\n')
            if method == 'floor':
                ynq__ypim += (
                    '    value = value - np.remainder(value, unit_value)\n')
            if method == 'round':
                ynq__ypim += '    if unit_value == 1:\n'
                ynq__ypim += '        value = value\n'
                ynq__ypim += '    else:\n'
                ynq__ypim += (
                    '        quotient, remainder = np.divmod(value, unit_value)\n'
                    )
                ynq__ypim += """        mask = np.logical_or(remainder > (unit_value // 2), np.logical_and(remainder == (unit_value // 2), quotient % 2))
"""
                ynq__ypim += '        if mask:\n'
                ynq__ypim += '            quotient = quotient + 1\n'
                ynq__ypim += '        value = quotient * unit_value\n'
            if tz_literal is not None:
                if ghagn__flq:
                    ynq__ypim += f'    original_value = value\n'
                    ynq__ypim += """    start_trans = deltas[np.searchsorted(trans, original_value, side='right') - 1]
"""
                    ynq__ypim += '    value = value - start_trans\n'
                    ynq__ypim += """    end_trans = deltas[np.searchsorted(trans, value, side='right') - 1]
"""
                    ynq__ypim += '    offset = start_trans - end_trans\n'
                    ynq__ypim += '    value = value + offset\n'
                else:
                    ynq__ypim += f'    value = value - delta\n'
            ynq__ypim += '    return pd.Timestamp(value, tz=tz_literal)\n'
        fteob__jiez = {}
        exec(ynq__ypim, {'np': np, 'pd': pd, 'deltas': kjp__qlg, 'trans':
            etct__pyvr, 'tz_literal': tz_literal}, fteob__jiez)
        impl = fteob__jiez['impl']
        return impl
    return freq_overload


def _install_freq_methods():
    vox__lph = ['ceil', 'floor', 'round']
    for method in vox__lph:
        fyirc__pwn = overload_freq_methods(method)
        overload_method(PDTimeDeltaType, method, no_unliteral=True)(fyirc__pwn)
        overload_method(PandasTimestampType, method, no_unliteral=True)(
            fyirc__pwn)


_install_freq_methods()


@register_jitable
def compute_pd_timestamp(totmicrosec, nanosecond):
    microsecond = totmicrosec % 1000000
    iuse__deveu = totmicrosec // 1000000
    second = iuse__deveu % 60
    afh__cywvu = iuse__deveu // 60
    minute = afh__cywvu % 60
    qjex__yfkgr = afh__cywvu // 60
    hour = qjex__yfkgr % 24
    dkgly__wbg = qjex__yfkgr // 24
    year, month, day = _ord2ymd(dkgly__wbg)
    value = npy_datetimestruct_to_datetime(year, month, day, hour, minute,
        second, microsecond)
    value += zero_if_none(nanosecond)
    return init_timestamp(year, month, day, hour, minute, second,
        microsecond, nanosecond, value, None)


def overload_sub_operator_timestamp(lhs, rhs):
    if isinstance(lhs, PandasTimestampType) and rhs == datetime_timedelta_type:
        tz_literal = lhs.tz

        def impl(lhs, rhs):
            jjs__ieg = bodo.hiframes.datetime_timedelta_ext._to_nanoseconds(rhs
                )
            return pd.Timestamp(lhs.value - jjs__ieg, tz=tz_literal)
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
            jjs__ieg = bodo.hiframes.datetime_timedelta_ext._to_nanoseconds(rhs
                )
            return pd.Timestamp(lhs.value + jjs__ieg, tz=tz_literal)
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
        fihda__wqohl = 'datetime.date'
    else:
        fihda__wqohl = 'pandas.Timestamp'
    if types.unliteral(format) != types.unicode_type:
        raise BodoError(
            f"{fihda__wqohl}.strftime(): 'strftime' argument must be a string")

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
        kbtvm__aaviq = PandasTimestampType(None)
    elif is_overload_constant_str(tz):
        kbtvm__aaviq = PandasTimestampType(get_overload_const_str(tz))
    elif is_overload_constant_int(tz):
        kbtvm__aaviq = PandasTimestampType(get_overload_const_int(tz))
    else:
        raise_bodo_error(
            'pandas.Timestamp.now(): tz argument must be a constant string or integer literal if provided'
            )

    def impl(tz=None):
        with numba.objmode(d=kbtvm__aaviq):
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
    return types.Tuple([types.StringLiteral(rcug__nsnuu) for rcug__nsnuu in
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
    for vejwl__grmc in timestamp_unsupported_attrs:
        srskw__isy = 'pandas.Timestamp.' + vejwl__grmc
        overload_attribute(PandasTimestampType, vejwl__grmc)(
            create_unsupported_overload(srskw__isy))
    for awg__oon in timestamp_unsupported_methods:
        srskw__isy = 'pandas.Timestamp.' + awg__oon
        overload_method(PandasTimestampType, awg__oon)(
            create_unsupported_overload(srskw__isy + '()'))


_install_pd_timestamp_unsupported()


@lower_builtin(numba.core.types.functions.NumberClass,
    pd_timestamp_tz_naive_type, types.StringLiteral)
def datetime64_constructor(context, builder, sig, args):

    def datetime64_constructor_impl(a, b):
        return integer_to_dt64(a.value)
    return context.compile_internal(builder, datetime64_constructor_impl,
        sig, args)
