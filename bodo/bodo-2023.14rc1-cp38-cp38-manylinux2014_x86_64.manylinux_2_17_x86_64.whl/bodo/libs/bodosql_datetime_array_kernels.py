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
    sccdc__fiwz = pd.array(['year', 'y', 'yy', 'yyy', 'yyyy', 'yr', 'years',
        'yrs'])
    udjkw__uxemb = pd.array(['month', 'mm', 'mon', 'mons', 'months'])
    npyw__fbiy = pd.array(['day', 'd', 'dd', 'days', 'dayofmonth'])
    agdwb__rnv = pd.array(['dayofweek', 'weekday', 'dow', 'dw'])
    hsipp__hfir = pd.array(['week', 'w', 'wk', 'weekofyear', 'woy', 'wy'])
    sfw__uss = pd.array(['weekiso', 'week_iso', 'weekofyeariso',
        'weekofyear_iso'])
    boaz__mird = pd.array(['quarter', 'q', 'qtr', 'qtrs', 'quarters'])
    pzc__ngy = pd.array(['hour', 'h', 'hh', 'hr', 'hours', 'hrs'])
    nyt__ufx = pd.array(['minute', 'm', 'mi', 'min', 'minutes', 'mins'])
    iiteb__eua = pd.array(['second', 's', 'sec', 'seconds', 'secs'])
    ezh__qyxh = pd.array(['millisecond', 'ms', 'msec', 'milliseconds'])
    oyocj__zgim = pd.array(['microsecond', 'us', 'usec', 'microseconds'])
    irqdj__kgtjr = pd.array(['nanosecond', 'ns', 'nsec', 'nanosec',
        'nsecond', 'nanoseconds', 'nanosecs', 'nseconds'])
    emae__yve = pd.array(['epoch_second', 'epoch', 'epoch_seconds'])
    mxnvh__oas = pd.array(['epoch_millisecond', 'epoch_milliseconds'])
    fcunj__zow = pd.array(['epoch_microsecond', 'epoch_microseconds'])
    qdp__osw = pd.array(['epoch_nanosecond', 'epoch_nanoseconds'])
    qfb__oug = pd.array(['timezone_hour', 'tzh'])
    fim__xxw = pd.array(['timezone_minute', 'tzm'])
    jjpad__tns = pd.array(['yearofweek', 'yearofweekiso'])

    def impl(part_str):
        part_str = part_str.lower()
        if part_str in sccdc__fiwz:
            return 'year'
        elif part_str in udjkw__uxemb:
            return 'month'
        elif part_str in npyw__fbiy:
            return 'day'
        elif part_str in agdwb__rnv:
            return 'dayofweek'
        elif part_str in hsipp__hfir:
            return 'week'
        elif part_str in sfw__uss:
            return 'weekiso'
        elif part_str in boaz__mird:
            return 'quarter'
        elif part_str in pzc__ngy:
            return 'hour'
        elif part_str in nyt__ufx:
            return 'minute'
        elif part_str in iiteb__eua:
            return 'second'
        elif part_str in ezh__qyxh:
            return 'millisecond'
        elif part_str in oyocj__zgim:
            return 'microsecond'
        elif part_str in irqdj__kgtjr:
            return 'nanosecond'
        elif part_str in emae__yve:
            return 'epoch_second'
        elif part_str in mxnvh__oas:
            return 'epoch_millisecond'
        elif part_str in fcunj__zow:
            return 'epoch_microsecond'
        elif part_str in qdp__osw:
            return 'epoch_nanosecond'
        elif part_str in qfb__oug:
            return 'timezone_hour'
        elif part_str in fim__xxw:
            return 'timezone_minute'
        elif part_str in jjpad__tns:
            return part_str
        else:
            raise ValueError(
                'Invalid date or time part passed into Snowflake array kernel')
    return impl


@numba.generated_jit(nopython=True)
def add_interval(start_dt, interval):
    args = [start_dt, interval]
    for nyunx__ify in range(len(args)):
        if isinstance(args[nyunx__ify], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.add_interval_util', ['arr'
                ], nyunx__ify)

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
    for nyunx__ify in range(2):
        if isinstance(args[nyunx__ify], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.makedate',
                ['year', 'day'], nyunx__ify)

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
    for nyunx__ify in range(2):
        if isinstance(args[nyunx__ify], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.next_day',
                ['arr0', 'arr1'], nyunx__ify)

    def impl(arr0, arr1):
        return next_day_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def previous_day(arr0, arr1):
    args = [arr0, arr1]
    for nyunx__ify in range(2):
        if isinstance(args[nyunx__ify], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.previous_day', ['arr0',
                'arr1'], nyunx__ify)

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
    bphzv__vcs = get_tz_if_exists(start_dt)
    pxg__rktm = ['start_dt', 'interval']
    ikif__hsj = [start_dt, interval]
    osunp__mbob = [True] * 2
    xpok__kech = ''
    yrk__uugxh = bodo.utils.utils.is_array_typ(interval, True
        ) or bodo.utils.utils.is_array_typ(start_dt, True)
    nxtzu__obed = None
    if bphzv__vcs is not None:
        if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(bphzv__vcs):
            jdyq__iuo = pytz.timezone(bphzv__vcs)
            udn__gso = np.array(jdyq__iuo._utc_transition_times, dtype='M8[ns]'
                ).view('i8')
            pusn__swuaz = np.array(jdyq__iuo._transition_info)[:, 0]
            pusn__swuaz = (pd.Series(pusn__swuaz).dt.total_seconds() * 
                1000000000).astype(np.int64).values
            nxtzu__obed = {'trans': udn__gso, 'deltas': pusn__swuaz}
            xpok__kech += f'start_value = arg0.value\n'
            xpok__kech += 'end_value = start_value + arg0.value\n'
            xpok__kech += (
                "start_trans = np.searchsorted(trans, start_value, side='right') - 1\n"
                )
            xpok__kech += (
                "end_trans = np.searchsorted(trans, end_value, side='right') - 1\n"
                )
            xpok__kech += 'offset = deltas[start_trans] - deltas[end_trans]\n'
            xpok__kech += 'arg1 = pd.Timedelta(arg1.value + offset)\n'
        xpok__kech += f'res[i] = arg0 + arg1\n'
        omd__fxf = bodo.DatetimeArrayType(bphzv__vcs)
    else:
        poqn__xcbap = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
            yrk__uugxh else '')
        pec__fldn = 'bodo.utils.conversion.box_if_dt64' if yrk__uugxh else ''
        xpok__kech = f'res[i] = {poqn__xcbap}({pec__fldn}(arg0) + arg1)\n'
        omd__fxf = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf, extra_globals=nxtzu__obed)


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
        for nyunx__ify in range(2):
            if isinstance(args[nyunx__ify], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.add_interval_{unit}',
                    ['amount', 'start_dt'], nyunx__ify)
        hohm__bmcy = 'def impl(amount, start_dt):\n'
        hohm__bmcy += (
            f'  return bodo.libs.bodosql_array_kernels.add_interval_{unit}_util(amount, start_dt)'
            )
        zaco__suho = {}
        exec(hohm__bmcy, {'bodo': bodo}, zaco__suho)
        return zaco__suho['impl']
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
        bphzv__vcs = get_tz_if_exists(start_dt)
        pxg__rktm = ['amount', 'start_dt']
        ikif__hsj = [amount, start_dt]
        osunp__mbob = [True] * 2
        yrk__uugxh = bodo.utils.utils.is_array_typ(amount, True
            ) or bodo.utils.utils.is_array_typ(start_dt, True)
        nxtzu__obed = None
        if is_valid_time_arg(start_dt):
            asjp__ikf = start_dt.precision
            if unit == 'hours':
                kobct__xdkab = 3600000000000
            elif unit == 'minutes':
                kobct__xdkab = 60000000000
            elif unit == 'seconds':
                kobct__xdkab = 1000000000
            elif unit == 'milliseconds':
                asjp__ikf = max(asjp__ikf, 3)
                kobct__xdkab = 1000000
            elif unit == 'microseconds':
                asjp__ikf = max(asjp__ikf, 6)
                kobct__xdkab = 1000
            elif unit == 'nanoseconds':
                asjp__ikf = max(asjp__ikf, 9)
                kobct__xdkab = 1
            xpok__kech = f"""amt = bodo.hiframes.time_ext.cast_time_to_int(arg1) + {kobct__xdkab} * arg0
"""
            xpok__kech += (
                f'res[i] = bodo.hiframes.time_ext.cast_int_to_time(amt % 86400000000000, precision={asjp__ikf})'
                )
            omd__fxf = types.Array(bodo.hiframes.time_ext.TimeType(
                asjp__ikf), 1, 'C')
        elif bphzv__vcs is not None:
            if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(bphzv__vcs
                ):
                jdyq__iuo = pytz.timezone(bphzv__vcs)
                udn__gso = np.array(jdyq__iuo._utc_transition_times, dtype=
                    'M8[ns]').view('i8')
                pusn__swuaz = np.array(jdyq__iuo._transition_info)[:, 0]
                pusn__swuaz = (pd.Series(pusn__swuaz).dt.total_seconds() * 
                    1000000000).astype(np.int64).values
                nxtzu__obed = {'trans': udn__gso, 'deltas': pusn__swuaz}
            if unit in ('months', 'quarters', 'years'):
                if unit == 'quarters':
                    xpok__kech = f'td = pd.DateOffset(months=3*arg0)\n'
                else:
                    xpok__kech = f'td = pd.DateOffset({unit}=arg0)\n'
                xpok__kech += f'start_value = arg1.value\n'
                xpok__kech += (
                    'end_value = (pd.Timestamp(arg1.value) + td).value\n')
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    bphzv__vcs):
                    xpok__kech += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    xpok__kech += """end_trans = np.searchsorted(trans, end_value, side='right') - 1
"""
                    xpok__kech += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    xpok__kech += (
                        'td = pd.Timedelta(end_value - start_value + offset)\n'
                        )
                else:
                    xpok__kech += (
                        'td = pd.Timedelta(end_value - start_value)\n')
            else:
                if unit == 'nanoseconds':
                    xpok__kech = 'td = pd.Timedelta(arg0)\n'
                else:
                    xpok__kech = f'td = pd.Timedelta({unit}=arg0)\n'
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    bphzv__vcs):
                    xpok__kech += f'start_value = arg1.value\n'
                    xpok__kech += 'end_value = start_value + td.value\n'
                    xpok__kech += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    xpok__kech += """end_trans = np.searchsorted(trans, end_value, side='right') - 1
"""
                    xpok__kech += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    xpok__kech += 'td = pd.Timedelta(td.value + offset)\n'
            xpok__kech += f'res[i] = arg1 + td\n'
            omd__fxf = bodo.DatetimeArrayType(bphzv__vcs)
        else:
            poqn__xcbap = (
                'bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
                yrk__uugxh else '')
            pec__fldn = ('bodo.utils.conversion.box_if_dt64' if yrk__uugxh else
                '')
            if unit in ('months', 'years'):
                xpok__kech = f"""res[i] = {poqn__xcbap}({pec__fldn}(arg1) + pd.DateOffset({unit}=arg0))
"""
            elif unit == 'quarters':
                xpok__kech = f"""res[i] = {poqn__xcbap}({pec__fldn}(arg1) + pd.DateOffset(months=3*arg0))
"""
            elif unit == 'nanoseconds':
                xpok__kech = (
                    f'res[i] = {poqn__xcbap}({pec__fldn}(arg1) + pd.Timedelta(arg0))\n'
                    )
            else:
                xpok__kech = f"""res[i] = {poqn__xcbap}({pec__fldn}(arg1) + pd.Timedelta({unit}=arg0))
"""
            omd__fxf = types.Array(bodo.datetime64ns, 1, 'C')
        return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
            omd__fxf, extra_globals=nxtzu__obed)
    return overload_add_datetime_interval_util


def _install_add_interval_overload():
    biodj__tfy = [('years', add_interval_years, add_interval_years_util), (
        'quarters', add_interval_quarters, add_interval_quarters_util), (
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
    for unit, nzp__wbfd, jym__svpvl in biodj__tfy:
        esgyh__oisdr = create_add_interval_func_overload(unit)
        overload(nzp__wbfd)(esgyh__oisdr)
        ozetg__uggsl = create_add_interval_util_overload(unit)
        overload(jym__svpvl)(ozetg__uggsl)


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
        hohm__bmcy = 'def impl(arr):\n'
        hohm__bmcy += (
            f'  return bodo.libs.bodosql_array_kernels.{fn_name}_util(arr)')
        zaco__suho = {}
        exec(hohm__bmcy, {'bodo': bodo}, zaco__suho)
        return zaco__suho['impl']
    return overload_func


def create_dt_extract_fn_util_overload(fn_name):

    def overload_dt_extract_fn(arr):
        if fn_name in ('get_hour', 'get_minute', 'get_second',
            'get_microsecond', 'get_millisecond', 'get_nanosecond'):
            verify_time_or_datetime_arg_allow_tz(arr, fn_name, 'arr')
        else:
            verify_datetime_arg_allow_tz(arr, fn_name, 'arr')
        tcm__lxnz = get_tz_if_exists(arr)
        pec__fldn = ('bodo.utils.conversion.box_if_dt64' if tcm__lxnz is
            None else '')
        yim__iruqb = 'microsecond // 1000' if not is_valid_time_arg(arr
            ) else 'millisecond'
        msy__ays = {'get_year': f'{pec__fldn}(arg0).year', 'get_quarter':
            f'{pec__fldn}(arg0).quarter', 'get_month':
            f'{pec__fldn}(arg0).month', 'get_week':
            f'{pec__fldn}(arg0).week', 'get_hour':
            f'{pec__fldn}(arg0).hour', 'get_minute':
            f'{pec__fldn}(arg0).minute', 'get_second':
            f'{pec__fldn}(arg0).second', 'get_millisecond':
            f'{pec__fldn}(arg0).{yim__iruqb}', 'get_microsecond':
            f'{pec__fldn}(arg0).microsecond', 'get_nanosecond':
            f'{pec__fldn}(arg0).nanosecond', 'dayofmonth':
            f'{pec__fldn}(arg0).day', 'dayofweek':
            f'({pec__fldn}(arg0).dayofweek + 1) % 7', 'dayofweekiso':
            f'{pec__fldn}(arg0).dayofweek + 1', 'dayofyear':
            f'{pec__fldn}(arg0).dayofyear'}
        pxg__rktm = ['arr']
        ikif__hsj = [arr]
        osunp__mbob = [True]
        xpok__kech = f'res[i] = {msy__ays[fn_name]}'
        omd__fxf = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
            omd__fxf)
    return overload_dt_extract_fn


def _install_dt_extract_fn_overload():
    biodj__tfy = [('get_year', get_year, get_year_util), ('get_quarter',
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
    for fn_name, nzp__wbfd, jym__svpvl in biodj__tfy:
        esgyh__oisdr = create_dt_extract_fn_overload(fn_name)
        overload(nzp__wbfd)(esgyh__oisdr)
        ozetg__uggsl = create_dt_extract_fn_util_overload(fn_name)
        overload(jym__svpvl)(ozetg__uggsl)


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
    tcziw__elomo = 1
    if year1 < year0:
        year0, year1 = year1, year0
        tcziw__elomo = -1
    vciy__vfa = 0
    for sfzvz__sisb in range(year0, year1):
        vciy__vfa += 52
        fdrm__uphj = (sfzvz__sisb + sfzvz__sisb // 4 - sfzvz__sisb // 100 +
            sfzvz__sisb // 400) % 7
        vkj__cllna = (sfzvz__sisb - 1 + (sfzvz__sisb - 1) // 4 - (
            sfzvz__sisb - 1) // 100 + (sfzvz__sisb - 1) // 400) % 7
        if fdrm__uphj == 4 or vkj__cllna == 3:
            vciy__vfa += 1
    return tcziw__elomo * vciy__vfa


def create_dt_diff_fn_overload(unit):

    def overload_func(arr0, arr1):
        args = [arr0, arr1]
        for nyunx__ify in range(len(args)):
            if isinstance(args[nyunx__ify], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.diff_{unit}', ['arr0',
                    'arr1'], nyunx__ify)
        hohm__bmcy = 'def impl(arr0, arr1):\n'
        hohm__bmcy += (
            f'  return bodo.libs.bodosql_array_kernels.diff_{unit}_util(arr0, arr1)'
            )
        zaco__suho = {}
        exec(hohm__bmcy, {'bodo': bodo}, zaco__suho)
        return zaco__suho['impl']
    return overload_func


def create_dt_diff_fn_util_overload(unit):

    def overload_dt_diff_fn(arr0, arr1):
        verify_datetime_arg_allow_tz(arr0, 'diff_' + unit, 'arr0')
        verify_datetime_arg_allow_tz(arr1, 'diff_' + unit, 'arr1')
        tcm__lxnz = get_tz_if_exists(arr0)
        if get_tz_if_exists(arr1) != tcm__lxnz:
            raise_bodo_error(
                f'diff_{unit}: both arguments must have the same timezone')
        pxg__rktm = ['arr0', 'arr1']
        ikif__hsj = [arr0, arr1]
        osunp__mbob = [True] * 2
        nxtzu__obed = None
        pnjg__hlom = {'yr_diff': 'arg1.year - arg0.year', 'qu_diff':
            'arg1.quarter - arg0.quarter', 'mo_diff':
            'arg1.month - arg0.month', 'y0, w0, _': 'arg0.isocalendar()',
            'y1, w1, _': 'arg1.isocalendar()', 'iso_yr_diff':
            'bodo.libs.bodosql_array_kernels.get_iso_weeks_between_years(y0, y1)'
            , 'wk_diff': 'w1 - w0', 'da_diff':
            '(pd.Timestamp(arg1.year, arg1.month, arg1.day) - pd.Timestamp(arg0.year, arg0.month, arg0.day)).days'
            , 'ns_diff': 'arg1.value - arg0.value'}
        zictr__iyex = {'year': ['yr_diff'], 'quarter': ['yr_diff',
            'qu_diff'], 'month': ['yr_diff', 'mo_diff'], 'week': [
            'y0, w0, _', 'y1, w1, _', 'iso_yr_diff', 'wk_diff'], 'day': [
            'da_diff'], 'nanosecond': ['ns_diff']}
        xpok__kech = ''
        if tcm__lxnz == None:
            xpok__kech += 'arg0 = bodo.utils.conversion.box_if_dt64(arg0)\n'
            xpok__kech += 'arg1 = bodo.utils.conversion.box_if_dt64(arg1)\n'
        for tbqc__zwmxq in zictr__iyex.get(unit, []):
            xpok__kech += f'{tbqc__zwmxq} = {pnjg__hlom[tbqc__zwmxq]}\n'
        if unit == 'nanosecond':
            omd__fxf = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        else:
            omd__fxf = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
        if unit == 'year':
            xpok__kech += 'res[i] = yr_diff'
        elif unit == 'quarter':
            xpok__kech += 'res[i] = 4 * yr_diff + qu_diff'
        elif unit == 'month':
            xpok__kech += 'res[i] = 12 * yr_diff + mo_diff'
        elif unit == 'week':
            xpok__kech += 'res[i] = iso_yr_diff + wk_diff'
        elif unit == 'day':
            xpok__kech += 'res[i] = da_diff'
        elif unit == 'nanosecond':
            xpok__kech += 'res[i] = ns_diff'
        else:
            if unit == 'hour':
                wvcto__sbq = 3600000000000
            if unit == 'minute':
                wvcto__sbq = 60000000000
            if unit == 'second':
                wvcto__sbq = 1000000000
            if unit == 'microsecond':
                wvcto__sbq = 1000
            xpok__kech += f"""res[i] = np.floor_divide((arg1.value), ({wvcto__sbq})) - np.floor_divide((arg0.value), ({wvcto__sbq}))
"""
        return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
            omd__fxf, extra_globals=nxtzu__obed)
    return overload_dt_diff_fn


def _install_dt_diff_fn_overload():
    biodj__tfy = [('day', diff_day, diff_day_util), ('hour', diff_hour,
        diff_hour_util), ('microsecond', diff_microsecond,
        diff_microsecond_util), ('minute', diff_minute, diff_minute_util),
        ('month', diff_month, diff_month_util), ('nanosecond',
        diff_nanosecond, diff_nanosecond_util), ('quarter', diff_quarter,
        diff_quarter), ('second', diff_second, diff_second_util), ('week',
        diff_week, diff_week_util), ('year', diff_year, diff_year_util)]
    for unit, nzp__wbfd, jym__svpvl in biodj__tfy:
        esgyh__oisdr = create_dt_diff_fn_overload(unit)
        overload(nzp__wbfd)(esgyh__oisdr)
        ozetg__uggsl = create_dt_diff_fn_util_overload(unit)
        overload(jym__svpvl)(ozetg__uggsl)


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
    ipvl__pvzlz = get_tz_if_exists(ts_arg)
    pxg__rktm = ['date_or_time_part', 'ts_arg']
    ikif__hsj = [date_or_time_part, ts_arg]
    osunp__mbob = [True, True]
    pec__fldn = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(ts_arg, True) else '')
    poqn__xcbap = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(ts_arg, True) else '')
    xpok__kech = """part_str = bodo.libs.bodosql_array_kernels.standardize_snowflake_date_time_part(arg0)
"""
    if ipvl__pvzlz is None:
        xpok__kech += f'arg1 = {pec__fldn}(arg1)\n'
    xpok__kech += "if part_str == 'quarter':\n"
    xpok__kech += """    out_val = pd.Timestamp(year=arg1.year, month= (3*(arg1.quarter - 1)) + 1, day=1, tz=tz_literal)
"""
    xpok__kech += "elif part_str == 'year':\n"
    xpok__kech += (
        '    out_val = pd.Timestamp(year=arg1.year, month=1, day=1, tz=tz_literal)\n'
        )
    xpok__kech += "elif part_str == 'month':\n"
    xpok__kech += """    out_val = pd.Timestamp(year=arg1.year, month=arg1.month, day=1, tz=tz_literal)
"""
    xpok__kech += "elif part_str == 'day':\n"
    xpok__kech += '    out_val = arg1.normalize()\n'
    xpok__kech += "elif part_str == 'week':\n"
    xpok__kech += '    if arg1.dayofweek == 0:\n'
    xpok__kech += '        out_val = arg1.normalize()\n'
    xpok__kech += '    else:\n'
    xpok__kech += (
        '        out_val = arg1.normalize() - pd.tseries.offsets.Week(n=1, weekday=0)\n'
        )
    xpok__kech += "elif part_str == 'hour':\n"
    xpok__kech += "    out_val = arg1.floor('H')\n"
    xpok__kech += "elif part_str == 'minute':\n"
    xpok__kech += "    out_val = arg1.floor('min')\n"
    xpok__kech += "elif part_str == 'second':\n"
    xpok__kech += "    out_val = arg1.floor('S')\n"
    xpok__kech += "elif part_str == 'millisecond':\n"
    xpok__kech += "    out_val = arg1.floor('ms')\n"
    xpok__kech += "elif part_str == 'microsecond':\n"
    xpok__kech += "    out_val = arg1.floor('us')\n"
    xpok__kech += "elif part_str == 'nanosecond':\n"
    xpok__kech += '    out_val = arg1\n'
    xpok__kech += 'else:\n'
    xpok__kech += (
        "    raise ValueError('Invalid date or time part for DATE_TRUNC')\n")
    if ipvl__pvzlz is None:
        xpok__kech += f'res[i] = {poqn__xcbap}(out_val)\n'
    else:
        xpok__kech += f'res[i] = out_val\n'
    if ipvl__pvzlz is None:
        omd__fxf = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        omd__fxf = bodo.DatetimeArrayType(ipvl__pvzlz)
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf, extra_globals={'tz_literal': ipvl__pvzlz})


@numba.generated_jit(nopython=True)
def dayname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'dayname', 'arr')
    tcm__lxnz = get_tz_if_exists(arr)
    pec__fldn = ('bodo.utils.conversion.box_if_dt64' if tcm__lxnz is None else
        '')
    pxg__rktm = ['arr']
    ikif__hsj = [arr]
    osunp__mbob = [True]
    xpok__kech = f'res[i] = {pec__fldn}(arg0).day_name()'
    omd__fxf = bodo.string_array_type
    weyiw__cne = ['V']
    vrov__zdish = pd.array(['Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday'])
    nxtzu__obed = {'day_of_week_dict_arr': vrov__zdish}
    gso__osh = 'dict_res = day_of_week_dict_arr'
    vjrxj__fkmc = f'res[i] = {pec__fldn}(arg0).dayofweek'
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf, synthesize_dict_if_vector=weyiw__cne,
        synthesize_dict_setup_text=gso__osh, synthesize_dict_scalar_text=
        vjrxj__fkmc, extra_globals=nxtzu__obed, synthesize_dict_global=True,
        synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def int_to_days_util(arr):
    verify_int_arg(arr, 'int_to_days', 'arr')
    poqn__xcbap = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    pxg__rktm = ['arr']
    ikif__hsj = [arr]
    osunp__mbob = [True]
    xpok__kech = f'res[i] = {poqn__xcbap}(pd.Timedelta(days=arg0))'
    omd__fxf = np.dtype('timedelta64[ns]')
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf)


@numba.generated_jit(nopython=True)
def last_day_util(arr):
    verify_datetime_arg_allow_tz(arr, 'LAST_DAY', 'arr')
    bphzv__vcs = get_tz_if_exists(arr)
    pec__fldn = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    poqn__xcbap = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    pxg__rktm = ['arr']
    ikif__hsj = [arr]
    osunp__mbob = [True]
    if bphzv__vcs is None:
        xpok__kech = (
            f'res[i] = {poqn__xcbap}({pec__fldn}(arg0) + pd.tseries.offsets.MonthEnd(n=0, normalize=True))'
            )
        omd__fxf = np.dtype('datetime64[ns]')
    else:
        xpok__kech = 'y = arg0.year\n'
        xpok__kech += 'm = arg0.month\n'
        xpok__kech += (
            'd = bodo.hiframes.pd_offsets_ext.get_days_in_month(y, m)\n')
        xpok__kech += (
            f'res[i] = pd.Timestamp(year=y, month=m, day=d, tz={repr(bphzv__vcs)})\n'
            )
        omd__fxf = bodo.DatetimeArrayType(bphzv__vcs)
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf)


@numba.generated_jit(nopython=True)
def makedate_util(year, day):
    verify_int_arg(year, 'MAKEDATE', 'year')
    verify_int_arg(day, 'MAKEDATE', 'day')
    poqn__xcbap = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(year, True) or bodo.utils.utils.
        is_array_typ(day, True) else '')
    pxg__rktm = ['year', 'day']
    ikif__hsj = [year, day]
    osunp__mbob = [True] * 2
    xpok__kech = (
        f'res[i] = {poqn__xcbap}(pd.Timestamp(year=arg0, month=1, day=1) + pd.Timedelta(days=arg1-1))'
        )
    omd__fxf = np.dtype('datetime64[ns]')
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf)


@numba.generated_jit(nopython=True)
def monthname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'monthname', 'arr')
    tcm__lxnz = get_tz_if_exists(arr)
    pec__fldn = ('bodo.utils.conversion.box_if_dt64' if tcm__lxnz is None else
        '')
    pxg__rktm = ['arr']
    ikif__hsj = [arr]
    osunp__mbob = [True]
    xpok__kech = f'res[i] = {pec__fldn}(arg0).month_name()'
    omd__fxf = bodo.string_array_type
    weyiw__cne = ['V']
    csxg__endhi = pd.array(['January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October', 'November',
        'December'])
    nxtzu__obed = {'month_names_dict_arr': csxg__endhi}
    gso__osh = 'dict_res = month_names_dict_arr'
    vjrxj__fkmc = f'res[i] = {pec__fldn}(arg0).month - 1'
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf, synthesize_dict_if_vector=weyiw__cne,
        synthesize_dict_setup_text=gso__osh, synthesize_dict_scalar_text=
        vjrxj__fkmc, extra_globals=nxtzu__obed, synthesize_dict_global=True,
        synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def next_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'NEXT_DAY', 'arr0')
    verify_string_arg(arr1, 'NEXT_DAY', 'arr1')
    yuck__csa = is_valid_tz_aware_datetime_arg(arr0)
    poqn__xcbap = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    pxg__rktm = ['arr0', 'arr1']
    ikif__hsj = [arr0, arr1]
    osunp__mbob = [True] * 2
    mie__twky = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    xpok__kech = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if yuck__csa:
        wui__qfg = 'arg0'
    else:
        wui__qfg = 'bodo.utils.conversion.box_if_dt64(arg0)'
    xpok__kech += f"""new_timestamp = {wui__qfg}.normalize() + pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    xpok__kech += f'res[i] = {poqn__xcbap}(new_timestamp.tz_localize(None))\n'
    omd__fxf = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf, prefix_code=mie__twky)


@numba.generated_jit(nopython=True)
def previous_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'PREVIOUS_DAY', 'arr0')
    verify_string_arg(arr1, 'PREVIOUS_DAY', 'arr1')
    yuck__csa = is_valid_tz_aware_datetime_arg(arr0)
    poqn__xcbap = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    pxg__rktm = ['arr0', 'arr1']
    ikif__hsj = [arr0, arr1]
    osunp__mbob = [True] * 2
    mie__twky = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    xpok__kech = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if yuck__csa:
        wui__qfg = 'arg0'
    else:
        wui__qfg = 'bodo.utils.conversion.box_if_dt64(arg0)'
    xpok__kech += f"""new_timestamp = {wui__qfg}.normalize() - pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    xpok__kech += f'res[i] = {poqn__xcbap}(new_timestamp.tz_localize(None))\n'
    omd__fxf = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf, prefix_code=mie__twky)


@numba.generated_jit(nopython=True)
def second_timestamp_util(arr):
    verify_int_arg(arr, 'second_timestamp', 'arr')
    poqn__xcbap = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    pxg__rktm = ['arr']
    ikif__hsj = [arr]
    osunp__mbob = [True]
    xpok__kech = f"res[i] = {poqn__xcbap}(pd.Timestamp(arg0, unit='s'))"
    omd__fxf = np.dtype('datetime64[ns]')
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf)


@numba.generated_jit(nopython=True)
def weekday_util(arr):
    verify_datetime_arg(arr, 'WEEKDAY', 'arr')
    pxg__rktm = ['arr']
    ikif__hsj = [arr]
    osunp__mbob = [True]
    pec__fldn = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    xpok__kech = f'dt = {pec__fldn}(arg0)\n'
    xpok__kech += (
        'res[i] = bodo.hiframes.pd_timestamp_ext.get_day_of_week(dt.year, dt.month, dt.day)'
        )
    omd__fxf = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf)


@numba.generated_jit(nopython=True)
def yearofweekiso_util(arr):
    verify_datetime_arg_allow_tz(arr, 'YEAROFWEEKISO', 'arr')
    pxg__rktm = ['arr']
    ikif__hsj = [arr]
    osunp__mbob = [True]
    pec__fldn = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    xpok__kech = f'dt = {pec__fldn}(arg0)\n'
    xpok__kech += 'res[i] = dt.isocalendar()[0]'
    omd__fxf = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf)


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
    pxg__rktm = ['arr']
    ikif__hsj = [arr]
    osunp__mbob = [True]
    mie__twky = 'unix_days_to_year_zero = 719528\n'
    mie__twky += 'nanoseconds_divisor = 86400000000000\n'
    omd__fxf = bodo.IntegerArrayType(types.int64)
    lqrqn__prjs = bodo.utils.utils.is_array_typ(arr, False)
    if lqrqn__prjs:
        xpok__kech = (
            '  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        xpok__kech = '  in_value = arg0.value\n'
    xpok__kech += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_days_to_year_zero\n'
        )
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf, prefix_code=mie__twky)


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
    pxg__rktm = ['arr']
    ikif__hsj = [arr]
    osunp__mbob = [True]
    lqrqn__prjs = bodo.utils.utils.is_array_typ(arr, False)
    if lqrqn__prjs:
        omd__fxf = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        omd__fxf = bodo.pd_timestamp_tz_naive_type
    mie__twky = 'unix_days_to_year_zero = 719528\n'
    mie__twky += 'nanoseconds_divisor = 86400000000000\n'
    xpok__kech = (
        '  nanoseconds = (arg0 - unix_days_to_year_zero) * nanoseconds_divisor\n'
        )
    if lqrqn__prjs:
        xpok__kech += (
            '  res[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(nanoseconds)\n'
            )
    else:
        xpok__kech += '  res[i] = pd.Timestamp(nanoseconds)\n'
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf, prefix_code=mie__twky)


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
    wuugj__czjff = get_tz_if_exists(arr)
    pxg__rktm = ['arr']
    ikif__hsj = [arr]
    osunp__mbob = [True]
    mie__twky = 'unix_seconds_to_year_zero = 62167219200\n'
    mie__twky += 'nanoseconds_divisor = 1000000000\n'
    omd__fxf = bodo.IntegerArrayType(types.int64)
    lqrqn__prjs = bodo.utils.utils.is_array_typ(arr, False)
    if lqrqn__prjs and not wuugj__czjff:
        xpok__kech = (
            f'  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        xpok__kech = f'  in_value = arg0.value\n'
    xpok__kech += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_seconds_to_year_zero\n'
        )
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf, prefix_code=mie__twky)


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
    wuugj__czjff = get_tz_if_exists(tz_arg)
    pxg__rktm = ['tz_arg', 'interval_arg']
    ikif__hsj = [tz_arg, interval_arg]
    osunp__mbob = [True, True]
    if wuugj__czjff is not None:
        omd__fxf = bodo.DatetimeArrayType(wuugj__czjff)
    else:
        omd__fxf = bodo.datetime64ns
    if interval_arg == bodo.date_offset_type:
        xpok__kech = """  timedelta = bodo.libs.pd_datetime_arr_ext.convert_months_offset_to_days(arg0.year, arg0.month, arg0.day, ((arg1._years * 12) + arg1._months) * arg1.n)
"""
    else:
        xpok__kech = '  timedelta = arg1\n'
    xpok__kech += """  timedelta = bodo.hiframes.pd_offsets_ext.update_timedelta_with_transition(arg0, timedelta)
"""
    xpok__kech += '  res[i] = arg0 + timedelta\n'
    return gen_vectorized(pxg__rktm, ikif__hsj, osunp__mbob, xpok__kech,
        omd__fxf)
