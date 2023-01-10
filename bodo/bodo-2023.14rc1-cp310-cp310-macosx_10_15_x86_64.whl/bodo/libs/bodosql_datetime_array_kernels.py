"""
Implements datetime array kernels that are specific to BodoSQL
"""
import numba
import numpy as np
import pandas as pd
import pytz
from numba.core import types
from numba.extending import overload, register_jitable
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import raise_bodo_error


def standardize_snowflake_date_time_part(part_str):
    pass


@overload(standardize_snowflake_date_time_part)
def overload_standardize_snowflake_date_time_part(part_str):
    jvxf__krsvi = pd.array(['year', 'y', 'yy', 'yyy', 'yyyy', 'yr', 'years',
        'yrs'])
    zpumi__uyk = pd.array(['month', 'mm', 'mon', 'mons', 'months'])
    joma__oqvc = pd.array(['day', 'd', 'dd', 'days', 'dayofmonth'])
    yhf__olay = pd.array(['dayofweek', 'weekday', 'dow', 'dw'])
    myjy__yhw = pd.array(['week', 'w', 'wk', 'weekofyear', 'woy', 'wy'])
    kjfw__pgvd = pd.array(['weekiso', 'week_iso', 'weekofyeariso',
        'weekofyear_iso'])
    tlxf__gwn = pd.array(['quarter', 'q', 'qtr', 'qtrs', 'quarters'])
    ghf__zgrs = pd.array(['hour', 'h', 'hh', 'hr', 'hours', 'hrs'])
    kmuo__jct = pd.array(['minute', 'm', 'mi', 'min', 'minutes', 'mins'])
    horc__obbf = pd.array(['second', 's', 'sec', 'seconds', 'secs'])
    zyy__xyjtc = pd.array(['millisecond', 'ms', 'msec', 'milliseconds'])
    tov__ykaq = pd.array(['microsecond', 'us', 'usec', 'microseconds'])
    rjq__gdiur = pd.array(['nanosecond', 'ns', 'nsec', 'nanosec', 'nsecond',
        'nanoseconds', 'nanosecs', 'nseconds'])
    yqr__ibmt = pd.array(['epoch_second', 'epoch', 'epoch_seconds'])
    izmav__vbdv = pd.array(['epoch_millisecond', 'epoch_milliseconds'])
    lfh__wemw = pd.array(['epoch_microsecond', 'epoch_microseconds'])
    nqdb__lqaae = pd.array(['epoch_nanosecond', 'epoch_nanoseconds'])
    xlewb__jsv = pd.array(['timezone_hour', 'tzh'])
    hcm__japdb = pd.array(['timezone_minute', 'tzm'])
    hfauh__jnryz = pd.array(['yearofweek', 'yearofweekiso'])

    def impl(part_str):
        part_str = part_str.lower()
        if part_str in jvxf__krsvi:
            return 'year'
        elif part_str in zpumi__uyk:
            return 'month'
        elif part_str in joma__oqvc:
            return 'day'
        elif part_str in yhf__olay:
            return 'dayofweek'
        elif part_str in myjy__yhw:
            return 'week'
        elif part_str in kjfw__pgvd:
            return 'weekiso'
        elif part_str in tlxf__gwn:
            return 'quarter'
        elif part_str in ghf__zgrs:
            return 'hour'
        elif part_str in kmuo__jct:
            return 'minute'
        elif part_str in horc__obbf:
            return 'second'
        elif part_str in zyy__xyjtc:
            return 'millisecond'
        elif part_str in tov__ykaq:
            return 'microsecond'
        elif part_str in rjq__gdiur:
            return 'nanosecond'
        elif part_str in yqr__ibmt:
            return 'epoch_second'
        elif part_str in izmav__vbdv:
            return 'epoch_millisecond'
        elif part_str in lfh__wemw:
            return 'epoch_microsecond'
        elif part_str in nqdb__lqaae:
            return 'epoch_nanosecond'
        elif part_str in xlewb__jsv:
            return 'timezone_hour'
        elif part_str in hcm__japdb:
            return 'timezone_minute'
        elif part_str in hfauh__jnryz:
            return part_str
        else:
            raise ValueError(
                'Invalid date or time part passed into Snowflake array kernel')
    return impl


@numba.generated_jit(nopython=True)
def add_interval(start_dt, interval):
    args = [start_dt, interval]
    for rgr__jdfyj in range(len(args)):
        if isinstance(args[rgr__jdfyj], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.add_interval_util', ['arr'
                ], rgr__jdfyj)

    def impl(start_dt, interval):
        return add_interval_util(start_dt, interval)
    return impl


def add_interval_years(amount, start_dt):
    return


def add_interval_quarters(amount, start_dt):
    return


def add_interval_months(amount, start_dt):
    return


def add_interval_weeks(amount, start_dt):
    return


def add_interval_days(amount, start_dt):
    return


def add_interval_hours(amount, start_dt):
    return


def add_interval_minutes(amount, start_dt):
    return


def add_interval_seconds(amount, start_dt):
    return


def add_interval_milliseconds(amount, start_dt):
    return


def add_interval_microseconds(amount, start_dt):
    return


def add_interval_nanoseconds(amount, start_dt):
    return


@numba.generated_jit(nopython=True)
def dayname(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.dayname_util',
            ['arr'], 0)

    def impl(arr):
        return dayname_util(arr)
    return impl


def dayofmonth(arr):
    return


def dayofweek(arr):
    return


def dayofweekiso(arr):
    return


def dayofyear(arr):
    return


def diff_day(arr0, arr1):
    return


def diff_hour(arr0, arr1):
    return


def diff_microsecond(arr0, arr1):
    return


def diff_minute(arr0, arr1):
    return


def diff_month(arr0, arr1):
    return


def diff_nanosecond(arr0, arr1):
    return


def diff_quarter(arr0, arr1):
    return


def diff_second(arr0, arr1):
    return


def diff_week(arr0, arr1):
    return


def diff_year(arr0, arr1):
    return


def get_year(arr):
    return


def get_quarter(arr):
    return


def get_month(arr):
    return


def get_week(arr):
    return


def get_hour(arr):
    return


def get_minute(arr):
    return


def get_second(arr):
    return


def get_millisecond(arr):
    return


def get_microsecond(arr):
    return


def get_nanosecond(arr):
    return


@numba.generated_jit(nopython=True)
def int_to_days(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.int_to_days_util', ['arr'], 0)

    def impl(arr):
        return int_to_days_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def last_day(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.last_day_util',
            ['arr'], 0)

    def impl(arr):
        return last_day_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def makedate(year, day):
    args = [year, day]
    for rgr__jdfyj in range(2):
        if isinstance(args[rgr__jdfyj], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.makedate',
                ['year', 'day'], rgr__jdfyj)

    def impl(year, day):
        return makedate_util(year, day)
    return impl


@numba.generated_jit(nopython=True)
def monthname(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.monthname_util',
            ['arr'], 0)

    def impl(arr):
        return monthname_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def next_day(arr0, arr1):
    args = [arr0, arr1]
    for rgr__jdfyj in range(2):
        if isinstance(args[rgr__jdfyj], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.next_day',
                ['arr0', 'arr1'], rgr__jdfyj)

    def impl(arr0, arr1):
        return next_day_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def previous_day(arr0, arr1):
    args = [arr0, arr1]
    for rgr__jdfyj in range(2):
        if isinstance(args[rgr__jdfyj], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.previous_day', ['arr0',
                'arr1'], rgr__jdfyj)

    def impl(arr0, arr1):
        return previous_day_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def second_timestamp(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.second_timestamp_util', ['arr'], 0
            )

    def impl(arr):
        return second_timestamp_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def weekday(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.weekday_util',
            ['arr'], 0)

    def impl(arr):
        return weekday_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def yearofweekiso(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.yearofweekiso_util', ['arr'], 0)

    def impl(arr):
        return yearofweekiso_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def add_interval_util(start_dt, interval):
    verify_datetime_arg_allow_tz(start_dt, 'add_interval', 'start_dt')
    atc__hto = get_tz_if_exists(start_dt)
    jtcl__fvwoz = ['start_dt', 'interval']
    pzb__gapw = [start_dt, interval]
    qag__cnkc = [True] * 2
    vqv__imw = ''
    gqb__exc = bodo.utils.utils.is_array_typ(interval, True
        ) or bodo.utils.utils.is_array_typ(start_dt, True)
    sdhi__gken = None
    if atc__hto is not None:
        if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(atc__hto):
            kte__llpu = pytz.timezone(atc__hto)
            zhlqs__sbmc = np.array(kte__llpu._utc_transition_times, dtype=
                'M8[ns]').view('i8')
            flfko__gtb = np.array(kte__llpu._transition_info)[:, 0]
            flfko__gtb = (pd.Series(flfko__gtb).dt.total_seconds() * 1000000000
                ).astype(np.int64).values
            sdhi__gken = {'trans': zhlqs__sbmc, 'deltas': flfko__gtb}
            vqv__imw += f'start_value = arg0.value\n'
            vqv__imw += 'end_value = start_value + arg0.value\n'
            vqv__imw += (
                "start_trans = np.searchsorted(trans, start_value, side='right') - 1\n"
                )
            vqv__imw += (
                "end_trans = np.searchsorted(trans, end_value, side='right') - 1\n"
                )
            vqv__imw += 'offset = deltas[start_trans] - deltas[end_trans]\n'
            vqv__imw += 'arg1 = pd.Timedelta(arg1.value + offset)\n'
        vqv__imw += f'res[i] = arg0 + arg1\n'
        irg__ggq = bodo.DatetimeArrayType(atc__hto)
    else:
        viy__hzv = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
            gqb__exc else '')
        jyzfc__ejsv = 'bodo.utils.conversion.box_if_dt64' if gqb__exc else ''
        vqv__imw = f'res[i] = {viy__hzv}({jyzfc__ejsv}(arg0) + arg1)\n'
        irg__ggq = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw,
        irg__ggq, extra_globals=sdhi__gken)


def add_interval_years_util(amount, start_dt):
    return


def add_interval_quarters_util(amount, start_dt):
    return


def add_interval_months_util(amount, start_dt):
    return


def add_interval_weeks_util(amount, start_dt):
    return


def add_interval_days_util(amount, start_dt):
    return


def add_interval_hours_util(amount, start_dt):
    return


def add_interval_minutes_util(amount, start_dt):
    return


def add_interval_seconds_util(amount, start_dt):
    return


def add_interval_milliseconds_util(amount, start_dt):
    return


def add_interval_microseconds_util(amount, start_dt):
    return


def add_interval_nanoseconds_util(amount, start_dt):
    return


def create_add_interval_func_overload(unit):

    def overload_func(amount, start_dt):
        args = [amount, start_dt]
        for rgr__jdfyj in range(2):
            if isinstance(args[rgr__jdfyj], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.add_interval_{unit}',
                    ['amount', 'start_dt'], rgr__jdfyj)
        zvy__bwu = 'def impl(amount, start_dt):\n'
        zvy__bwu += (
            f'  return bodo.libs.bodosql_array_kernels.add_interval_{unit}_util(amount, start_dt)'
            )
        slxo__hoze = {}
        exec(zvy__bwu, {'bodo': bodo}, slxo__hoze)
        return slxo__hoze['impl']
    return overload_func


def create_add_interval_util_overload(unit):

    def overload_add_datetime_interval_util(amount, start_dt):
        verify_int_arg(amount, 'add_interval_' + unit, 'amount')
        if unit in ('hours', 'minutes', 'seconds', 'milliseconds',
            'microseconds', 'nanoseconds'):
            verify_time_or_datetime_arg_allow_tz(start_dt, 'add_interval_' +
                unit, 'start_dt')
        else:
            verify_datetime_arg_allow_tz(start_dt, 'add_interval_' + unit,
                'start_dt')
        atc__hto = get_tz_if_exists(start_dt)
        jtcl__fvwoz = ['amount', 'start_dt']
        pzb__gapw = [amount, start_dt]
        qag__cnkc = [True] * 2
        gqb__exc = bodo.utils.utils.is_array_typ(amount, True
            ) or bodo.utils.utils.is_array_typ(start_dt, True)
        sdhi__gken = None
        if is_valid_time_arg(start_dt):
            mgum__xqnn = start_dt.precision
            if unit == 'hours':
                njmxv__nyqcn = 3600000000000
            elif unit == 'minutes':
                njmxv__nyqcn = 60000000000
            elif unit == 'seconds':
                njmxv__nyqcn = 1000000000
            elif unit == 'milliseconds':
                mgum__xqnn = max(mgum__xqnn, 3)
                njmxv__nyqcn = 1000000
            elif unit == 'microseconds':
                mgum__xqnn = max(mgum__xqnn, 6)
                njmxv__nyqcn = 1000
            elif unit == 'nanoseconds':
                mgum__xqnn = max(mgum__xqnn, 9)
                njmxv__nyqcn = 1
            vqv__imw = f"""amt = bodo.hiframes.time_ext.cast_time_to_int(arg1) + {njmxv__nyqcn} * arg0
"""
            vqv__imw += (
                f'res[i] = bodo.hiframes.time_ext.cast_int_to_time(amt % 86400000000000, precision={mgum__xqnn})'
                )
            irg__ggq = types.Array(bodo.hiframes.time_ext.TimeType(
                mgum__xqnn), 1, 'C')
        elif atc__hto is not None:
            if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(atc__hto):
                kte__llpu = pytz.timezone(atc__hto)
                zhlqs__sbmc = np.array(kte__llpu._utc_transition_times,
                    dtype='M8[ns]').view('i8')
                flfko__gtb = np.array(kte__llpu._transition_info)[:, 0]
                flfko__gtb = (pd.Series(flfko__gtb).dt.total_seconds() * 
                    1000000000).astype(np.int64).values
                sdhi__gken = {'trans': zhlqs__sbmc, 'deltas': flfko__gtb}
            if unit in ('months', 'quarters', 'years'):
                if unit == 'quarters':
                    vqv__imw = f'td = pd.DateOffset(months=3*arg0)\n'
                else:
                    vqv__imw = f'td = pd.DateOffset({unit}=arg0)\n'
                vqv__imw += f'start_value = arg1.value\n'
                vqv__imw += (
                    'end_value = (pd.Timestamp(arg1.value) + td).value\n')
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    atc__hto):
                    vqv__imw += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    vqv__imw += (
                        "end_trans = np.searchsorted(trans, end_value, side='right') - 1\n"
                        )
                    vqv__imw += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    vqv__imw += (
                        'td = pd.Timedelta(end_value - start_value + offset)\n'
                        )
                else:
                    vqv__imw += 'td = pd.Timedelta(end_value - start_value)\n'
            else:
                if unit == 'nanoseconds':
                    vqv__imw = 'td = pd.Timedelta(arg0)\n'
                else:
                    vqv__imw = f'td = pd.Timedelta({unit}=arg0)\n'
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    atc__hto):
                    vqv__imw += f'start_value = arg1.value\n'
                    vqv__imw += 'end_value = start_value + td.value\n'
                    vqv__imw += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    vqv__imw += (
                        "end_trans = np.searchsorted(trans, end_value, side='right') - 1\n"
                        )
                    vqv__imw += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    vqv__imw += 'td = pd.Timedelta(td.value + offset)\n'
            vqv__imw += f'res[i] = arg1 + td\n'
            irg__ggq = bodo.DatetimeArrayType(atc__hto)
        else:
            viy__hzv = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
                gqb__exc else '')
            jyzfc__ejsv = ('bodo.utils.conversion.box_if_dt64' if gqb__exc else
                '')
            if unit in ('months', 'years'):
                vqv__imw = f"""res[i] = {viy__hzv}({jyzfc__ejsv}(arg1) + pd.DateOffset({unit}=arg0))
"""
            elif unit == 'quarters':
                vqv__imw = f"""res[i] = {viy__hzv}({jyzfc__ejsv}(arg1) + pd.DateOffset(months=3*arg0))
"""
            elif unit == 'nanoseconds':
                vqv__imw = (
                    f'res[i] = {viy__hzv}({jyzfc__ejsv}(arg1) + pd.Timedelta(arg0))\n'
                    )
            else:
                vqv__imw = (
                    f'res[i] = {viy__hzv}({jyzfc__ejsv}(arg1) + pd.Timedelta({unit}=arg0))\n'
                    )
            irg__ggq = types.Array(bodo.datetime64ns, 1, 'C')
        return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw,
            irg__ggq, extra_globals=sdhi__gken)
    return overload_add_datetime_interval_util


def _install_add_interval_overload():
    tibuh__nxaz = [('years', add_interval_years, add_interval_years_util),
        ('quarters', add_interval_quarters, add_interval_quarters_util), (
        'months', add_interval_months, add_interval_months_util), ('weeks',
        add_interval_weeks, add_interval_weeks_util), ('days',
        add_interval_days, add_interval_days_util), ('hours',
        add_interval_hours, add_interval_hours_util), ('minutes',
        add_interval_minutes, add_interval_minutes_util), ('seconds',
        add_interval_seconds, add_interval_seconds_util), ('milliseconds',
        add_interval_milliseconds, add_interval_milliseconds_util), (
        'microseconds', add_interval_microseconds,
        add_interval_microseconds_util), ('nanoseconds',
        add_interval_nanoseconds, add_interval_nanoseconds_util)]
    for unit, ywk__tckpk, huk__smku in tibuh__nxaz:
        qfjg__ljvri = create_add_interval_func_overload(unit)
        overload(ywk__tckpk)(qfjg__ljvri)
        oyspc__lhhj = create_add_interval_util_overload(unit)
        overload(huk__smku)(oyspc__lhhj)


_install_add_interval_overload()


def dayofmonth_util(arr):
    return


def dayofweek_util(arr):
    return


def dayofweekiso_util(arr):
    return


def dayofyear_util(arr):
    return


def get_year_util(arr):
    return


def get_quarter_util(arr):
    return


def get_month_util(arr):
    return


def get_week_util(arr):
    return


def get_hour_util(arr):
    return


def get_minute_util(arr):
    return


def get_second_util(arr):
    return


def get_millisecond_util(arr):
    return


def get_microsecond_util(arr):
    return


def get_nanosecond_util(arr):
    return


def create_dt_extract_fn_overload(fn_name):

    def overload_func(arr):
        if isinstance(arr, types.optional):
            return unopt_argument(f'bodo.libs.bodosql_array_kernels.{fn_name}',
                ['arr'], 0)
        zvy__bwu = 'def impl(arr):\n'
        zvy__bwu += (
            f'  return bodo.libs.bodosql_array_kernels.{fn_name}_util(arr)')
        slxo__hoze = {}
        exec(zvy__bwu, {'bodo': bodo}, slxo__hoze)
        return slxo__hoze['impl']
    return overload_func


def create_dt_extract_fn_util_overload(fn_name):

    def overload_dt_extract_fn(arr):
        if fn_name in ('get_hour', 'get_minute', 'get_second',
            'get_microsecond', 'get_millisecond', 'get_nanosecond'):
            verify_time_or_datetime_arg_allow_tz(arr, fn_name, 'arr')
        else:
            verify_datetime_arg_allow_tz(arr, fn_name, 'arr')
        qyyqc__rvia = get_tz_if_exists(arr)
        jyzfc__ejsv = ('bodo.utils.conversion.box_if_dt64' if qyyqc__rvia is
            None else '')
        tgi__cmcuc = 'microsecond // 1000' if not is_valid_time_arg(arr
            ) else 'millisecond'
        ayjw__six = {'get_year': f'{jyzfc__ejsv}(arg0).year', 'get_quarter':
            f'{jyzfc__ejsv}(arg0).quarter', 'get_month':
            f'{jyzfc__ejsv}(arg0).month', 'get_week':
            f'{jyzfc__ejsv}(arg0).week', 'get_hour':
            f'{jyzfc__ejsv}(arg0).hour', 'get_minute':
            f'{jyzfc__ejsv}(arg0).minute', 'get_second':
            f'{jyzfc__ejsv}(arg0).second', 'get_millisecond':
            f'{jyzfc__ejsv}(arg0).{tgi__cmcuc}', 'get_microsecond':
            f'{jyzfc__ejsv}(arg0).microsecond', 'get_nanosecond':
            f'{jyzfc__ejsv}(arg0).nanosecond', 'dayofmonth':
            f'{jyzfc__ejsv}(arg0).day', 'dayofweek':
            f'({jyzfc__ejsv}(arg0).dayofweek + 1) % 7', 'dayofweekiso':
            f'{jyzfc__ejsv}(arg0).dayofweek + 1', 'dayofyear':
            f'{jyzfc__ejsv}(arg0).dayofyear'}
        jtcl__fvwoz = ['arr']
        pzb__gapw = [arr]
        qag__cnkc = [True]
        vqv__imw = f'res[i] = {ayjw__six[fn_name]}'
        irg__ggq = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw,
            irg__ggq)
    return overload_dt_extract_fn


def _install_dt_extract_fn_overload():
    tibuh__nxaz = [('get_year', get_year, get_year_util), ('get_quarter',
        get_quarter, get_quarter_util), ('get_month', get_month,
        get_month_util), ('get_week', get_week, get_week_util), ('get_hour',
        get_hour, get_hour_util), ('get_minute', get_minute,
        get_minute_util), ('get_second', get_second, get_second_util), (
        'get_millisecond', get_millisecond, get_millisecond_util), (
        'get_microsecond', get_microsecond, get_microsecond_util), (
        'get_nanosecond', get_nanosecond, get_nanosecond_util), (
        'dayofmonth', dayofmonth, dayofmonth_util), ('dayofweek', dayofweek,
        dayofweek_util), ('dayofweekiso', dayofweekiso, dayofweekiso_util),
        ('dayofyear', dayofyear, dayofyear_util)]
    for fn_name, ywk__tckpk, huk__smku in tibuh__nxaz:
        qfjg__ljvri = create_dt_extract_fn_overload(fn_name)
        overload(ywk__tckpk)(qfjg__ljvri)
        oyspc__lhhj = create_dt_extract_fn_util_overload(fn_name)
        overload(huk__smku)(oyspc__lhhj)


_install_dt_extract_fn_overload()


def diff_day_util(arr0, arr1):
    return


def diff_hour_util(arr0, arr1):
    return


def diff_microsecond_util(arr0, arr1):
    return


def diff_minute_util(arr0, arr1):
    return


def diff_month_util(arr0, arr1):
    return


def diff_nanosecond_util(arr0, arr1):
    return


def diff_quarter_util(arr0, arr1):
    return


def diff_second_util(arr0, arr1):
    return


def diff_week_util(arr0, arr1):
    return


def diff_year_util(arr0, arr1):
    return


@register_jitable
def get_iso_weeks_between_years(year0, year1):
    tmm__tenf = 1
    if year1 < year0:
        year0, year1 = year1, year0
        tmm__tenf = -1
    fdh__gmsm = 0
    for qslq__poi in range(year0, year1):
        fdh__gmsm += 52
        ggxs__erbm = (qslq__poi + qslq__poi // 4 - qslq__poi // 100 + 
            qslq__poi // 400) % 7
        pgz__rczd = (qslq__poi - 1 + (qslq__poi - 1) // 4 - (qslq__poi - 1) //
            100 + (qslq__poi - 1) // 400) % 7
        if ggxs__erbm == 4 or pgz__rczd == 3:
            fdh__gmsm += 1
    return tmm__tenf * fdh__gmsm


def create_dt_diff_fn_overload(unit):

    def overload_func(arr0, arr1):
        args = [arr0, arr1]
        for rgr__jdfyj in range(len(args)):
            if isinstance(args[rgr__jdfyj], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.diff_{unit}', ['arr0',
                    'arr1'], rgr__jdfyj)
        zvy__bwu = 'def impl(arr0, arr1):\n'
        zvy__bwu += (
            f'  return bodo.libs.bodosql_array_kernels.diff_{unit}_util(arr0, arr1)'
            )
        slxo__hoze = {}
        exec(zvy__bwu, {'bodo': bodo}, slxo__hoze)
        return slxo__hoze['impl']
    return overload_func


def create_dt_diff_fn_util_overload(unit):

    def overload_dt_diff_fn(arr0, arr1):
        verify_datetime_arg_allow_tz(arr0, 'diff_' + unit, 'arr0')
        verify_datetime_arg_allow_tz(arr1, 'diff_' + unit, 'arr1')
        qyyqc__rvia = get_tz_if_exists(arr0)
        if get_tz_if_exists(arr1) != qyyqc__rvia:
            raise_bodo_error(
                f'diff_{unit}: both arguments must have the same timezone')
        jtcl__fvwoz = ['arr0', 'arr1']
        pzb__gapw = [arr0, arr1]
        qag__cnkc = [True] * 2
        sdhi__gken = None
        qdk__nqko = {'yr_diff': 'arg1.year - arg0.year', 'qu_diff':
            'arg1.quarter - arg0.quarter', 'mo_diff':
            'arg1.month - arg0.month', 'y0, w0, _': 'arg0.isocalendar()',
            'y1, w1, _': 'arg1.isocalendar()', 'iso_yr_diff':
            'bodo.libs.bodosql_array_kernels.get_iso_weeks_between_years(y0, y1)'
            , 'wk_diff': 'w1 - w0', 'da_diff':
            '(pd.Timestamp(arg1.year, arg1.month, arg1.day) - pd.Timestamp(arg0.year, arg0.month, arg0.day)).days'
            , 'ns_diff': 'arg1.value - arg0.value'}
        irz__jie = {'year': ['yr_diff'], 'quarter': ['yr_diff', 'qu_diff'],
            'month': ['yr_diff', 'mo_diff'], 'week': ['y0, w0, _',
            'y1, w1, _', 'iso_yr_diff', 'wk_diff'], 'day': ['da_diff'],
            'nanosecond': ['ns_diff']}
        vqv__imw = ''
        if qyyqc__rvia == None:
            vqv__imw += 'arg0 = bodo.utils.conversion.box_if_dt64(arg0)\n'
            vqv__imw += 'arg1 = bodo.utils.conversion.box_if_dt64(arg1)\n'
        for gzl__hyb in irz__jie.get(unit, []):
            vqv__imw += f'{gzl__hyb} = {qdk__nqko[gzl__hyb]}\n'
        if unit == 'nanosecond':
            irg__ggq = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        else:
            irg__ggq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
        if unit == 'year':
            vqv__imw += 'res[i] = yr_diff'
        elif unit == 'quarter':
            vqv__imw += 'res[i] = 4 * yr_diff + qu_diff'
        elif unit == 'month':
            vqv__imw += 'res[i] = 12 * yr_diff + mo_diff'
        elif unit == 'week':
            vqv__imw += 'res[i] = iso_yr_diff + wk_diff'
        elif unit == 'day':
            vqv__imw += 'res[i] = da_diff'
        elif unit == 'nanosecond':
            vqv__imw += 'res[i] = ns_diff'
        else:
            if unit == 'hour':
                wzb__jgmo = 3600000000000
            if unit == 'minute':
                wzb__jgmo = 60000000000
            if unit == 'second':
                wzb__jgmo = 1000000000
            if unit == 'microsecond':
                wzb__jgmo = 1000
            vqv__imw += f"""res[i] = np.floor_divide((arg1.value), ({wzb__jgmo})) - np.floor_divide((arg0.value), ({wzb__jgmo}))
"""
        return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw,
            irg__ggq, extra_globals=sdhi__gken)
    return overload_dt_diff_fn


def _install_dt_diff_fn_overload():
    tibuh__nxaz = [('day', diff_day, diff_day_util), ('hour', diff_hour,
        diff_hour_util), ('microsecond', diff_microsecond,
        diff_microsecond_util), ('minute', diff_minute, diff_minute_util),
        ('month', diff_month, diff_month_util), ('nanosecond',
        diff_nanosecond, diff_nanosecond_util), ('quarter', diff_quarter,
        diff_quarter), ('second', diff_second, diff_second_util), ('week',
        diff_week, diff_week_util), ('year', diff_year, diff_year_util)]
    for unit, ywk__tckpk, huk__smku in tibuh__nxaz:
        qfjg__ljvri = create_dt_diff_fn_overload(unit)
        overload(ywk__tckpk)(qfjg__ljvri)
        oyspc__lhhj = create_dt_diff_fn_util_overload(unit)
        overload(huk__smku)(oyspc__lhhj)


_install_dt_diff_fn_overload()


def date_trunc(date_or_time_part, ts_arg):
    pass


@overload(date_trunc)
def overload_date_trunc(date_or_time_part, ts_arg):
    if isinstance(date_or_time_part, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.date_trunc',
            ['date_or_time_part', 'ts_arg'], 0)
    if isinstance(ts_arg, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.date_trunc',
            ['date_or_time_part', 'ts_arg'], 1)

    def impl(date_or_time_part, ts_arg):
        return date_trunc_util(date_or_time_part, ts_arg)
    return impl


def date_trunc_util(date_or_time_part, ts_arg):
    pass


@overload(date_trunc_util)
def overload_date_trunc_util(date_or_time_part, ts_arg):
    verify_string_arg(date_or_time_part, 'DATE_TRUNC', 'date_or_time_part')
    verify_datetime_arg_allow_tz(ts_arg, 'DATE_TRUNC', 'ts_arg')
    pijkf__spigu = get_tz_if_exists(ts_arg)
    jtcl__fvwoz = ['date_or_time_part', 'ts_arg']
    pzb__gapw = [date_or_time_part, ts_arg]
    qag__cnkc = [True, True]
    jyzfc__ejsv = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(ts_arg, True) else '')
    viy__hzv = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(ts_arg, True) else '')
    vqv__imw = """part_str = bodo.libs.bodosql_array_kernels.standardize_snowflake_date_time_part(arg0)
"""
    if pijkf__spigu is None:
        vqv__imw += f'arg1 = {jyzfc__ejsv}(arg1)\n'
    vqv__imw += "if part_str == 'quarter':\n"
    vqv__imw += """    out_val = pd.Timestamp(year=arg1.year, month= (3*(arg1.quarter - 1)) + 1, day=1, tz=tz_literal)
"""
    vqv__imw += "elif part_str == 'year':\n"
    vqv__imw += (
        '    out_val = pd.Timestamp(year=arg1.year, month=1, day=1, tz=tz_literal)\n'
        )
    vqv__imw += "elif part_str == 'month':\n"
    vqv__imw += """    out_val = pd.Timestamp(year=arg1.year, month=arg1.month, day=1, tz=tz_literal)
"""
    vqv__imw += "elif part_str == 'day':\n"
    vqv__imw += '    out_val = arg1.normalize()\n'
    vqv__imw += "elif part_str == 'week':\n"
    vqv__imw += '    if arg1.dayofweek == 0:\n'
    vqv__imw += '        out_val = arg1.normalize()\n'
    vqv__imw += '    else:\n'
    vqv__imw += (
        '        out_val = arg1.normalize() - pd.tseries.offsets.Week(n=1, weekday=0)\n'
        )
    vqv__imw += "elif part_str == 'hour':\n"
    vqv__imw += "    out_val = arg1.floor('H')\n"
    vqv__imw += "elif part_str == 'minute':\n"
    vqv__imw += "    out_val = arg1.floor('min')\n"
    vqv__imw += "elif part_str == 'second':\n"
    vqv__imw += "    out_val = arg1.floor('S')\n"
    vqv__imw += "elif part_str == 'millisecond':\n"
    vqv__imw += "    out_val = arg1.floor('ms')\n"
    vqv__imw += "elif part_str == 'microsecond':\n"
    vqv__imw += "    out_val = arg1.floor('us')\n"
    vqv__imw += "elif part_str == 'nanosecond':\n"
    vqv__imw += '    out_val = arg1\n'
    vqv__imw += 'else:\n'
    vqv__imw += (
        "    raise ValueError('Invalid date or time part for DATE_TRUNC')\n")
    if pijkf__spigu is None:
        vqv__imw += f'res[i] = {viy__hzv}(out_val)\n'
    else:
        vqv__imw += f'res[i] = out_val\n'
    if pijkf__spigu is None:
        irg__ggq = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        irg__ggq = bodo.DatetimeArrayType(pijkf__spigu)
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw,
        irg__ggq, extra_globals={'tz_literal': pijkf__spigu})


@numba.generated_jit(nopython=True)
def dayname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'dayname', 'arr')
    qyyqc__rvia = get_tz_if_exists(arr)
    jyzfc__ejsv = ('bodo.utils.conversion.box_if_dt64' if qyyqc__rvia is
        None else '')
    jtcl__fvwoz = ['arr']
    pzb__gapw = [arr]
    qag__cnkc = [True]
    vqv__imw = f'res[i] = {jyzfc__ejsv}(arg0).day_name()'
    irg__ggq = bodo.string_array_type
    wun__wak = ['V']
    hfso__dygq = pd.array(['Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday'])
    sdhi__gken = {'day_of_week_dict_arr': hfso__dygq}
    xfszg__oolop = 'dict_res = day_of_week_dict_arr'
    hao__toww = f'res[i] = {jyzfc__ejsv}(arg0).dayofweek'
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw,
        irg__ggq, synthesize_dict_if_vector=wun__wak,
        synthesize_dict_setup_text=xfszg__oolop,
        synthesize_dict_scalar_text=hao__toww, extra_globals=sdhi__gken,
        synthesize_dict_global=True, synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def int_to_days_util(arr):
    verify_int_arg(arr, 'int_to_days', 'arr')
    viy__hzv = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(arr, True) else '')
    jtcl__fvwoz = ['arr']
    pzb__gapw = [arr]
    qag__cnkc = [True]
    vqv__imw = f'res[i] = {viy__hzv}(pd.Timedelta(days=arg0))'
    irg__ggq = np.dtype('timedelta64[ns]')
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw, irg__ggq
        )


@numba.generated_jit(nopython=True)
def last_day_util(arr):
    verify_datetime_arg_allow_tz(arr, 'LAST_DAY', 'arr')
    atc__hto = get_tz_if_exists(arr)
    jyzfc__ejsv = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    viy__hzv = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(arr, True) else '')
    jtcl__fvwoz = ['arr']
    pzb__gapw = [arr]
    qag__cnkc = [True]
    if atc__hto is None:
        vqv__imw = (
            f'res[i] = {viy__hzv}({jyzfc__ejsv}(arg0) + pd.tseries.offsets.MonthEnd(n=0, normalize=True))'
            )
        irg__ggq = np.dtype('datetime64[ns]')
    else:
        vqv__imw = 'y = arg0.year\n'
        vqv__imw += 'm = arg0.month\n'
        vqv__imw += (
            'd = bodo.hiframes.pd_offsets_ext.get_days_in_month(y, m)\n')
        vqv__imw += (
            f'res[i] = pd.Timestamp(year=y, month=m, day=d, tz={repr(atc__hto)})\n'
            )
        irg__ggq = bodo.DatetimeArrayType(atc__hto)
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw, irg__ggq
        )


@numba.generated_jit(nopython=True)
def makedate_util(year, day):
    verify_int_arg(year, 'MAKEDATE', 'year')
    verify_int_arg(day, 'MAKEDATE', 'day')
    viy__hzv = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(year, True) or bodo.utils.utils.
        is_array_typ(day, True) else '')
    jtcl__fvwoz = ['year', 'day']
    pzb__gapw = [year, day]
    qag__cnkc = [True] * 2
    vqv__imw = (
        f'res[i] = {viy__hzv}(pd.Timestamp(year=arg0, month=1, day=1) + pd.Timedelta(days=arg1-1))'
        )
    irg__ggq = np.dtype('datetime64[ns]')
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw, irg__ggq
        )


@numba.generated_jit(nopython=True)
def monthname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'monthname', 'arr')
    qyyqc__rvia = get_tz_if_exists(arr)
    jyzfc__ejsv = ('bodo.utils.conversion.box_if_dt64' if qyyqc__rvia is
        None else '')
    jtcl__fvwoz = ['arr']
    pzb__gapw = [arr]
    qag__cnkc = [True]
    vqv__imw = f'res[i] = {jyzfc__ejsv}(arg0).month_name()'
    irg__ggq = bodo.string_array_type
    wun__wak = ['V']
    dazah__rzzbz = pd.array(['January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October', 'November',
        'December'])
    sdhi__gken = {'month_names_dict_arr': dazah__rzzbz}
    xfszg__oolop = 'dict_res = month_names_dict_arr'
    hao__toww = f'res[i] = {jyzfc__ejsv}(arg0).month - 1'
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw,
        irg__ggq, synthesize_dict_if_vector=wun__wak,
        synthesize_dict_setup_text=xfszg__oolop,
        synthesize_dict_scalar_text=hao__toww, extra_globals=sdhi__gken,
        synthesize_dict_global=True, synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def next_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'NEXT_DAY', 'arr0')
    verify_string_arg(arr1, 'NEXT_DAY', 'arr1')
    zcdvk__ccmd = is_valid_tz_aware_datetime_arg(arr0)
    viy__hzv = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    jtcl__fvwoz = ['arr0', 'arr1']
    pzb__gapw = [arr0, arr1]
    qag__cnkc = [True] * 2
    yaju__xzgfz = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    vqv__imw = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if zcdvk__ccmd:
        okdp__vhfrg = 'arg0'
    else:
        okdp__vhfrg = 'bodo.utils.conversion.box_if_dt64(arg0)'
    vqv__imw += f"""new_timestamp = {okdp__vhfrg}.normalize() + pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    vqv__imw += f'res[i] = {viy__hzv}(new_timestamp.tz_localize(None))\n'
    irg__ggq = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw,
        irg__ggq, prefix_code=yaju__xzgfz)


@numba.generated_jit(nopython=True)
def previous_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'PREVIOUS_DAY', 'arr0')
    verify_string_arg(arr1, 'PREVIOUS_DAY', 'arr1')
    zcdvk__ccmd = is_valid_tz_aware_datetime_arg(arr0)
    viy__hzv = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    jtcl__fvwoz = ['arr0', 'arr1']
    pzb__gapw = [arr0, arr1]
    qag__cnkc = [True] * 2
    yaju__xzgfz = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    vqv__imw = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if zcdvk__ccmd:
        okdp__vhfrg = 'arg0'
    else:
        okdp__vhfrg = 'bodo.utils.conversion.box_if_dt64(arg0)'
    vqv__imw += f"""new_timestamp = {okdp__vhfrg}.normalize() - pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    vqv__imw += f'res[i] = {viy__hzv}(new_timestamp.tz_localize(None))\n'
    irg__ggq = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw,
        irg__ggq, prefix_code=yaju__xzgfz)


@numba.generated_jit(nopython=True)
def second_timestamp_util(arr):
    verify_int_arg(arr, 'second_timestamp', 'arr')
    viy__hzv = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(arr, True) else '')
    jtcl__fvwoz = ['arr']
    pzb__gapw = [arr]
    qag__cnkc = [True]
    vqv__imw = f"res[i] = {viy__hzv}(pd.Timestamp(arg0, unit='s'))"
    irg__ggq = np.dtype('datetime64[ns]')
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw, irg__ggq
        )


@numba.generated_jit(nopython=True)
def weekday_util(arr):
    verify_datetime_arg(arr, 'WEEKDAY', 'arr')
    jtcl__fvwoz = ['arr']
    pzb__gapw = [arr]
    qag__cnkc = [True]
    jyzfc__ejsv = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    vqv__imw = f'dt = {jyzfc__ejsv}(arg0)\n'
    vqv__imw += (
        'res[i] = bodo.hiframes.pd_timestamp_ext.get_day_of_week(dt.year, dt.month, dt.day)'
        )
    irg__ggq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw, irg__ggq
        )


@numba.generated_jit(nopython=True)
def yearofweekiso_util(arr):
    verify_datetime_arg_allow_tz(arr, 'YEAROFWEEKISO', 'arr')
    jtcl__fvwoz = ['arr']
    pzb__gapw = [arr]
    qag__cnkc = [True]
    jyzfc__ejsv = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    vqv__imw = f'dt = {jyzfc__ejsv}(arg0)\n'
    vqv__imw += 'res[i] = dt.isocalendar()[0]'
    irg__ggq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw, irg__ggq
        )


def to_days(arr):
    pass


@overload(to_days)
def overload_to_days(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_days_util',
            ['arr'], 0)

    def impl(arr):
        return to_days_util(arr)
    return impl


def to_days_util(arr):
    pass


@overload(to_days_util)
def overload_to_days_util(arr):
    verify_datetime_arg(arr, 'TO_DAYS', 'arr')
    jtcl__fvwoz = ['arr']
    pzb__gapw = [arr]
    qag__cnkc = [True]
    yaju__xzgfz = 'unix_days_to_year_zero = 719528\n'
    yaju__xzgfz += 'nanoseconds_divisor = 86400000000000\n'
    irg__ggq = bodo.IntegerArrayType(types.int64)
    xgodw__rbdo = bodo.utils.utils.is_array_typ(arr, False)
    if xgodw__rbdo:
        vqv__imw = (
            '  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        vqv__imw = '  in_value = arg0.value\n'
    vqv__imw += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_days_to_year_zero\n'
        )
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw,
        irg__ggq, prefix_code=yaju__xzgfz)


def from_days(arr):
    pass


@overload(from_days)
def overload_from_days(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.from_days_util',
            ['arr'], 0)

    def impl(arr):
        return from_days_util(arr)
    return impl


def from_days_util(arr):
    pass


@overload(from_days_util)
def overload_from_days_util(arr):
    verify_int_arg(arr, 'TO_DAYS', 'arr')
    jtcl__fvwoz = ['arr']
    pzb__gapw = [arr]
    qag__cnkc = [True]
    xgodw__rbdo = bodo.utils.utils.is_array_typ(arr, False)
    if xgodw__rbdo:
        irg__ggq = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        irg__ggq = bodo.pd_timestamp_tz_naive_type
    yaju__xzgfz = 'unix_days_to_year_zero = 719528\n'
    yaju__xzgfz += 'nanoseconds_divisor = 86400000000000\n'
    vqv__imw = (
        '  nanoseconds = (arg0 - unix_days_to_year_zero) * nanoseconds_divisor\n'
        )
    if xgodw__rbdo:
        vqv__imw += (
            '  res[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(nanoseconds)\n'
            )
    else:
        vqv__imw += '  res[i] = pd.Timestamp(nanoseconds)\n'
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw,
        irg__ggq, prefix_code=yaju__xzgfz)


def to_seconds(arr):
    pass


@overload(to_seconds)
def overload_to_seconds(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_seconds_util'
            , ['arr'], 0)

    def impl(arr):
        return to_seconds_util(arr)
    return impl


def to_seconds_util(arr):
    pass


@overload(to_seconds_util)
def overload_to_seconds_util(arr):
    verify_datetime_arg_allow_tz(arr, 'TO_SECONDS', 'arr')
    meyb__sch = get_tz_if_exists(arr)
    jtcl__fvwoz = ['arr']
    pzb__gapw = [arr]
    qag__cnkc = [True]
    yaju__xzgfz = 'unix_seconds_to_year_zero = 62167219200\n'
    yaju__xzgfz += 'nanoseconds_divisor = 1000000000\n'
    irg__ggq = bodo.IntegerArrayType(types.int64)
    xgodw__rbdo = bodo.utils.utils.is_array_typ(arr, False)
    if xgodw__rbdo and not meyb__sch:
        vqv__imw = (
            f'  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        vqv__imw = f'  in_value = arg0.value\n'
    vqv__imw += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_seconds_to_year_zero\n'
        )
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw,
        irg__ggq, prefix_code=yaju__xzgfz)


def tz_aware_interval_add(tz_arg, interval_arg):
    pass


@overload(tz_aware_interval_add)
def overload_tz_aware_interval_add(tz_arg, interval_arg):
    if isinstance(tz_arg, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.tz_aware_interval_add', [
            'tz_arg', 'interval_arg'], 0)
    if isinstance(interval_arg, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.tz_aware_interval_add', [
            'tz_arg', 'interval_arg'], 1)

    def impl(tz_arg, interval_arg):
        return tz_aware_interval_add_util(tz_arg, interval_arg)
    return impl


def tz_aware_interval_add_util(tz_arg, interval_arg):
    pass


@overload(tz_aware_interval_add_util)
def overload_tz_aware_interval_add_util(tz_arg, interval_arg):
    verify_datetime_arg_require_tz(tz_arg, 'INTERVAL_ADD', 'tz_arg')
    verify_sql_interval(interval_arg, 'INTERVAL_ADD', 'interval_arg')
    meyb__sch = get_tz_if_exists(tz_arg)
    jtcl__fvwoz = ['tz_arg', 'interval_arg']
    pzb__gapw = [tz_arg, interval_arg]
    qag__cnkc = [True, True]
    if meyb__sch is not None:
        irg__ggq = bodo.DatetimeArrayType(meyb__sch)
    else:
        irg__ggq = bodo.datetime64ns
    if interval_arg == bodo.date_offset_type:
        vqv__imw = """  timedelta = bodo.libs.pd_datetime_arr_ext.convert_months_offset_to_days(arg0.year, arg0.month, arg0.day, ((arg1._years * 12) + arg1._months) * arg1.n)
"""
    else:
        vqv__imw = '  timedelta = arg1\n'
    vqv__imw += """  timedelta = bodo.hiframes.pd_offsets_ext.update_timedelta_with_transition(arg0, timedelta)
"""
    vqv__imw += '  res[i] = arg0 + timedelta\n'
    return gen_vectorized(jtcl__fvwoz, pzb__gapw, qag__cnkc, vqv__imw, irg__ggq
        )
