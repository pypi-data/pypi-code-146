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
    fck__kkc = pd.array(['year', 'y', 'yy', 'yyy', 'yyyy', 'yr', 'years',
        'yrs'])
    iqxyu__tlozf = pd.array(['month', 'mm', 'mon', 'mons', 'months'])
    skis__oazl = pd.array(['day', 'd', 'dd', 'days', 'dayofmonth'])
    dujl__ilftu = pd.array(['dayofweek', 'weekday', 'dow', 'dw'])
    mzzvg__cryz = pd.array(['week', 'w', 'wk', 'weekofyear', 'woy', 'wy'])
    pmd__rcbhy = pd.array(['weekiso', 'week_iso', 'weekofyeariso',
        'weekofyear_iso'])
    vlg__dicb = pd.array(['quarter', 'q', 'qtr', 'qtrs', 'quarters'])
    wpe__moq = pd.array(['hour', 'h', 'hh', 'hr', 'hours', 'hrs'])
    kmx__gewtw = pd.array(['minute', 'm', 'mi', 'min', 'minutes', 'mins'])
    oxd__mkawn = pd.array(['second', 's', 'sec', 'seconds', 'secs'])
    ckim__dsyqu = pd.array(['millisecond', 'ms', 'msec', 'milliseconds'])
    ssjj__lup = pd.array(['microsecond', 'us', 'usec', 'microseconds'])
    wgm__yki = pd.array(['nanosecond', 'ns', 'nsec', 'nanosec', 'nsecond',
        'nanoseconds', 'nanosecs', 'nseconds'])
    kezrs__vagu = pd.array(['epoch_second', 'epoch', 'epoch_seconds'])
    ebmdt__fyygs = pd.array(['epoch_millisecond', 'epoch_milliseconds'])
    hss__hwtsq = pd.array(['epoch_microsecond', 'epoch_microseconds'])
    nrtmt__dthi = pd.array(['epoch_nanosecond', 'epoch_nanoseconds'])
    xcjn__oyev = pd.array(['timezone_hour', 'tzh'])
    jvg__ngspn = pd.array(['timezone_minute', 'tzm'])
    mugtu__yov = pd.array(['yearofweek', 'yearofweekiso'])

    def impl(part_str):
        part_str = part_str.lower()
        if part_str in fck__kkc:
            return 'year'
        elif part_str in iqxyu__tlozf:
            return 'month'
        elif part_str in skis__oazl:
            return 'day'
        elif part_str in dujl__ilftu:
            return 'dayofweek'
        elif part_str in mzzvg__cryz:
            return 'week'
        elif part_str in pmd__rcbhy:
            return 'weekiso'
        elif part_str in vlg__dicb:
            return 'quarter'
        elif part_str in wpe__moq:
            return 'hour'
        elif part_str in kmx__gewtw:
            return 'minute'
        elif part_str in oxd__mkawn:
            return 'second'
        elif part_str in ckim__dsyqu:
            return 'millisecond'
        elif part_str in ssjj__lup:
            return 'microsecond'
        elif part_str in wgm__yki:
            return 'nanosecond'
        elif part_str in kezrs__vagu:
            return 'epoch_second'
        elif part_str in ebmdt__fyygs:
            return 'epoch_millisecond'
        elif part_str in hss__hwtsq:
            return 'epoch_microsecond'
        elif part_str in nrtmt__dthi:
            return 'epoch_nanosecond'
        elif part_str in xcjn__oyev:
            return 'timezone_hour'
        elif part_str in jvg__ngspn:
            return 'timezone_minute'
        elif part_str in mugtu__yov:
            return part_str
        else:
            raise ValueError(
                'Invalid date or time part passed into Snowflake array kernel')
    return impl


@numba.generated_jit(nopython=True)
def add_interval(start_dt, interval):
    args = [start_dt, interval]
    for gnm__ieb in range(len(args)):
        if isinstance(args[gnm__ieb], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.add_interval_util', ['arr'
                ], gnm__ieb)

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
    for gnm__ieb in range(2):
        if isinstance(args[gnm__ieb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.makedate',
                ['year', 'day'], gnm__ieb)

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
    for gnm__ieb in range(2):
        if isinstance(args[gnm__ieb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.next_day',
                ['arr0', 'arr1'], gnm__ieb)

    def impl(arr0, arr1):
        return next_day_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def previous_day(arr0, arr1):
    args = [arr0, arr1]
    for gnm__ieb in range(2):
        if isinstance(args[gnm__ieb], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.previous_day', ['arr0',
                'arr1'], gnm__ieb)

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
    axfa__kuz = get_tz_if_exists(start_dt)
    pao__gtnd = ['start_dt', 'interval']
    vsfuy__axwz = [start_dt, interval]
    aglss__uahwj = [True] * 2
    oqw__gcnbr = ''
    cue__knna = bodo.utils.utils.is_array_typ(interval, True
        ) or bodo.utils.utils.is_array_typ(start_dt, True)
    ofzho__ovlo = None
    if axfa__kuz is not None:
        if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(axfa__kuz):
            upzn__mdjr = pytz.timezone(axfa__kuz)
            ync__bvehb = np.array(upzn__mdjr._utc_transition_times, dtype=
                'M8[ns]').view('i8')
            wem__mlue = np.array(upzn__mdjr._transition_info)[:, 0]
            wem__mlue = (pd.Series(wem__mlue).dt.total_seconds() * 1000000000
                ).astype(np.int64).values
            ofzho__ovlo = {'trans': ync__bvehb, 'deltas': wem__mlue}
            oqw__gcnbr += f'start_value = arg0.value\n'
            oqw__gcnbr += 'end_value = start_value + arg0.value\n'
            oqw__gcnbr += (
                "start_trans = np.searchsorted(trans, start_value, side='right') - 1\n"
                )
            oqw__gcnbr += (
                "end_trans = np.searchsorted(trans, end_value, side='right') - 1\n"
                )
            oqw__gcnbr += 'offset = deltas[start_trans] - deltas[end_trans]\n'
            oqw__gcnbr += 'arg1 = pd.Timedelta(arg1.value + offset)\n'
        oqw__gcnbr += f'res[i] = arg0 + arg1\n'
        huz__aiu = bodo.DatetimeArrayType(axfa__kuz)
    else:
        lvqre__bpixi = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
            cue__knna else '')
        xci__igdq = 'bodo.utils.conversion.box_if_dt64' if cue__knna else ''
        oqw__gcnbr = f'res[i] = {lvqre__bpixi}({xci__igdq}(arg0) + arg1)\n'
        huz__aiu = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu, extra_globals=ofzho__ovlo)


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
        for gnm__ieb in range(2):
            if isinstance(args[gnm__ieb], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.add_interval_{unit}',
                    ['amount', 'start_dt'], gnm__ieb)
        vczy__ylihg = 'def impl(amount, start_dt):\n'
        vczy__ylihg += (
            f'  return bodo.libs.bodosql_array_kernels.add_interval_{unit}_util(amount, start_dt)'
            )
        jha__psh = {}
        exec(vczy__ylihg, {'bodo': bodo}, jha__psh)
        return jha__psh['impl']
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
        axfa__kuz = get_tz_if_exists(start_dt)
        pao__gtnd = ['amount', 'start_dt']
        vsfuy__axwz = [amount, start_dt]
        aglss__uahwj = [True] * 2
        cue__knna = bodo.utils.utils.is_array_typ(amount, True
            ) or bodo.utils.utils.is_array_typ(start_dt, True)
        ofzho__ovlo = None
        if is_valid_time_arg(start_dt):
            jzgv__pdpo = start_dt.precision
            if unit == 'hours':
                yybj__fog = 3600000000000
            elif unit == 'minutes':
                yybj__fog = 60000000000
            elif unit == 'seconds':
                yybj__fog = 1000000000
            elif unit == 'milliseconds':
                jzgv__pdpo = max(jzgv__pdpo, 3)
                yybj__fog = 1000000
            elif unit == 'microseconds':
                jzgv__pdpo = max(jzgv__pdpo, 6)
                yybj__fog = 1000
            elif unit == 'nanoseconds':
                jzgv__pdpo = max(jzgv__pdpo, 9)
                yybj__fog = 1
            oqw__gcnbr = f"""amt = bodo.hiframes.time_ext.cast_time_to_int(arg1) + {yybj__fog} * arg0
"""
            oqw__gcnbr += (
                f'res[i] = bodo.hiframes.time_ext.cast_int_to_time(amt % 86400000000000, precision={jzgv__pdpo})'
                )
            huz__aiu = types.Array(bodo.hiframes.time_ext.TimeType(
                jzgv__pdpo), 1, 'C')
        elif axfa__kuz is not None:
            if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(axfa__kuz):
                upzn__mdjr = pytz.timezone(axfa__kuz)
                ync__bvehb = np.array(upzn__mdjr._utc_transition_times,
                    dtype='M8[ns]').view('i8')
                wem__mlue = np.array(upzn__mdjr._transition_info)[:, 0]
                wem__mlue = (pd.Series(wem__mlue).dt.total_seconds() * 
                    1000000000).astype(np.int64).values
                ofzho__ovlo = {'trans': ync__bvehb, 'deltas': wem__mlue}
            if unit in ('months', 'quarters', 'years'):
                if unit == 'quarters':
                    oqw__gcnbr = f'td = pd.DateOffset(months=3*arg0)\n'
                else:
                    oqw__gcnbr = f'td = pd.DateOffset({unit}=arg0)\n'
                oqw__gcnbr += f'start_value = arg1.value\n'
                oqw__gcnbr += (
                    'end_value = (pd.Timestamp(arg1.value) + td).value\n')
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    axfa__kuz):
                    oqw__gcnbr += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    oqw__gcnbr += """end_trans = np.searchsorted(trans, end_value, side='right') - 1
"""
                    oqw__gcnbr += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    oqw__gcnbr += (
                        'td = pd.Timedelta(end_value - start_value + offset)\n'
                        )
                else:
                    oqw__gcnbr += (
                        'td = pd.Timedelta(end_value - start_value)\n')
            else:
                if unit == 'nanoseconds':
                    oqw__gcnbr = 'td = pd.Timedelta(arg0)\n'
                else:
                    oqw__gcnbr = f'td = pd.Timedelta({unit}=arg0)\n'
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    axfa__kuz):
                    oqw__gcnbr += f'start_value = arg1.value\n'
                    oqw__gcnbr += 'end_value = start_value + td.value\n'
                    oqw__gcnbr += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    oqw__gcnbr += """end_trans = np.searchsorted(trans, end_value, side='right') - 1
"""
                    oqw__gcnbr += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    oqw__gcnbr += 'td = pd.Timedelta(td.value + offset)\n'
            oqw__gcnbr += f'res[i] = arg1 + td\n'
            huz__aiu = bodo.DatetimeArrayType(axfa__kuz)
        else:
            lvqre__bpixi = (
                'bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
                cue__knna else '')
            xci__igdq = ('bodo.utils.conversion.box_if_dt64' if cue__knna else
                '')
            if unit in ('months', 'years'):
                oqw__gcnbr = f"""res[i] = {lvqre__bpixi}({xci__igdq}(arg1) + pd.DateOffset({unit}=arg0))
"""
            elif unit == 'quarters':
                oqw__gcnbr = f"""res[i] = {lvqre__bpixi}({xci__igdq}(arg1) + pd.DateOffset(months=3*arg0))
"""
            elif unit == 'nanoseconds':
                oqw__gcnbr = (
                    f'res[i] = {lvqre__bpixi}({xci__igdq}(arg1) + pd.Timedelta(arg0))\n'
                    )
            else:
                oqw__gcnbr = f"""res[i] = {lvqre__bpixi}({xci__igdq}(arg1) + pd.Timedelta({unit}=arg0))
"""
            huz__aiu = types.Array(bodo.datetime64ns, 1, 'C')
        return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj,
            oqw__gcnbr, huz__aiu, extra_globals=ofzho__ovlo)
    return overload_add_datetime_interval_util


def _install_add_interval_overload():
    fmt__dfzr = [('years', add_interval_years, add_interval_years_util), (
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
    for unit, ycrn__riql, ltffm__dshuh in fmt__dfzr:
        kkdpg__atf = create_add_interval_func_overload(unit)
        overload(ycrn__riql)(kkdpg__atf)
        tzie__ubiy = create_add_interval_util_overload(unit)
        overload(ltffm__dshuh)(tzie__ubiy)


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
        vczy__ylihg = 'def impl(arr):\n'
        vczy__ylihg += (
            f'  return bodo.libs.bodosql_array_kernels.{fn_name}_util(arr)')
        jha__psh = {}
        exec(vczy__ylihg, {'bodo': bodo}, jha__psh)
        return jha__psh['impl']
    return overload_func


def create_dt_extract_fn_util_overload(fn_name):

    def overload_dt_extract_fn(arr):
        if fn_name in ('get_hour', 'get_minute', 'get_second',
            'get_microsecond', 'get_millisecond', 'get_nanosecond'):
            verify_time_or_datetime_arg_allow_tz(arr, fn_name, 'arr')
        else:
            verify_datetime_arg_allow_tz(arr, fn_name, 'arr')
        zhp__thz = get_tz_if_exists(arr)
        xci__igdq = ('bodo.utils.conversion.box_if_dt64' if zhp__thz is
            None else '')
        gemen__djxj = 'microsecond // 1000' if not is_valid_time_arg(arr
            ) else 'millisecond'
        lplz__cllhk = {'get_year': f'{xci__igdq}(arg0).year', 'get_quarter':
            f'{xci__igdq}(arg0).quarter', 'get_month':
            f'{xci__igdq}(arg0).month', 'get_week':
            f'{xci__igdq}(arg0).week', 'get_hour':
            f'{xci__igdq}(arg0).hour', 'get_minute':
            f'{xci__igdq}(arg0).minute', 'get_second':
            f'{xci__igdq}(arg0).second', 'get_millisecond':
            f'{xci__igdq}(arg0).{gemen__djxj}', 'get_microsecond':
            f'{xci__igdq}(arg0).microsecond', 'get_nanosecond':
            f'{xci__igdq}(arg0).nanosecond', 'dayofmonth':
            f'{xci__igdq}(arg0).day', 'dayofweek':
            f'({xci__igdq}(arg0).dayofweek + 1) % 7', 'dayofweekiso':
            f'{xci__igdq}(arg0).dayofweek + 1', 'dayofyear':
            f'{xci__igdq}(arg0).dayofyear'}
        pao__gtnd = ['arr']
        vsfuy__axwz = [arr]
        aglss__uahwj = [True]
        oqw__gcnbr = f'res[i] = {lplz__cllhk[fn_name]}'
        huz__aiu = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj,
            oqw__gcnbr, huz__aiu)
    return overload_dt_extract_fn


def _install_dt_extract_fn_overload():
    fmt__dfzr = [('get_year', get_year, get_year_util), ('get_quarter',
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
    for fn_name, ycrn__riql, ltffm__dshuh in fmt__dfzr:
        kkdpg__atf = create_dt_extract_fn_overload(fn_name)
        overload(ycrn__riql)(kkdpg__atf)
        tzie__ubiy = create_dt_extract_fn_util_overload(fn_name)
        overload(ltffm__dshuh)(tzie__ubiy)


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
    ppd__ltb = 1
    if year1 < year0:
        year0, year1 = year1, year0
        ppd__ltb = -1
    bonyk__ctmw = 0
    for faoyy__rhdnr in range(year0, year1):
        bonyk__ctmw += 52
        msoek__zjre = (faoyy__rhdnr + faoyy__rhdnr // 4 - faoyy__rhdnr // 
            100 + faoyy__rhdnr // 400) % 7
        kutao__gxrx = (faoyy__rhdnr - 1 + (faoyy__rhdnr - 1) // 4 - (
            faoyy__rhdnr - 1) // 100 + (faoyy__rhdnr - 1) // 400) % 7
        if msoek__zjre == 4 or kutao__gxrx == 3:
            bonyk__ctmw += 1
    return ppd__ltb * bonyk__ctmw


def create_dt_diff_fn_overload(unit):

    def overload_func(arr0, arr1):
        args = [arr0, arr1]
        for gnm__ieb in range(len(args)):
            if isinstance(args[gnm__ieb], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.diff_{unit}', ['arr0',
                    'arr1'], gnm__ieb)
        vczy__ylihg = 'def impl(arr0, arr1):\n'
        vczy__ylihg += (
            f'  return bodo.libs.bodosql_array_kernels.diff_{unit}_util(arr0, arr1)'
            )
        jha__psh = {}
        exec(vczy__ylihg, {'bodo': bodo}, jha__psh)
        return jha__psh['impl']
    return overload_func


def create_dt_diff_fn_util_overload(unit):

    def overload_dt_diff_fn(arr0, arr1):
        verify_datetime_arg_allow_tz(arr0, 'diff_' + unit, 'arr0')
        verify_datetime_arg_allow_tz(arr1, 'diff_' + unit, 'arr1')
        zhp__thz = get_tz_if_exists(arr0)
        if get_tz_if_exists(arr1) != zhp__thz:
            raise_bodo_error(
                f'diff_{unit}: both arguments must have the same timezone')
        pao__gtnd = ['arr0', 'arr1']
        vsfuy__axwz = [arr0, arr1]
        aglss__uahwj = [True] * 2
        ofzho__ovlo = None
        duyc__utmoe = {'yr_diff': 'arg1.year - arg0.year', 'qu_diff':
            'arg1.quarter - arg0.quarter', 'mo_diff':
            'arg1.month - arg0.month', 'y0, w0, _': 'arg0.isocalendar()',
            'y1, w1, _': 'arg1.isocalendar()', 'iso_yr_diff':
            'bodo.libs.bodosql_array_kernels.get_iso_weeks_between_years(y0, y1)'
            , 'wk_diff': 'w1 - w0', 'da_diff':
            '(pd.Timestamp(arg1.year, arg1.month, arg1.day) - pd.Timestamp(arg0.year, arg0.month, arg0.day)).days'
            , 'ns_diff': 'arg1.value - arg0.value'}
        rugom__gdn = {'year': ['yr_diff'], 'quarter': ['yr_diff', 'qu_diff'
            ], 'month': ['yr_diff', 'mo_diff'], 'week': ['y0, w0, _',
            'y1, w1, _', 'iso_yr_diff', 'wk_diff'], 'day': ['da_diff'],
            'nanosecond': ['ns_diff']}
        oqw__gcnbr = ''
        if zhp__thz == None:
            oqw__gcnbr += 'arg0 = bodo.utils.conversion.box_if_dt64(arg0)\n'
            oqw__gcnbr += 'arg1 = bodo.utils.conversion.box_if_dt64(arg1)\n'
        for uagy__isr in rugom__gdn.get(unit, []):
            oqw__gcnbr += f'{uagy__isr} = {duyc__utmoe[uagy__isr]}\n'
        if unit == 'nanosecond':
            huz__aiu = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        else:
            huz__aiu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
        if unit == 'year':
            oqw__gcnbr += 'res[i] = yr_diff'
        elif unit == 'quarter':
            oqw__gcnbr += 'res[i] = 4 * yr_diff + qu_diff'
        elif unit == 'month':
            oqw__gcnbr += 'res[i] = 12 * yr_diff + mo_diff'
        elif unit == 'week':
            oqw__gcnbr += 'res[i] = iso_yr_diff + wk_diff'
        elif unit == 'day':
            oqw__gcnbr += 'res[i] = da_diff'
        elif unit == 'nanosecond':
            oqw__gcnbr += 'res[i] = ns_diff'
        else:
            if unit == 'hour':
                yxrog__tny = 3600000000000
            if unit == 'minute':
                yxrog__tny = 60000000000
            if unit == 'second':
                yxrog__tny = 1000000000
            if unit == 'microsecond':
                yxrog__tny = 1000
            oqw__gcnbr += f"""res[i] = np.floor_divide((arg1.value), ({yxrog__tny})) - np.floor_divide((arg0.value), ({yxrog__tny}))
"""
        return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj,
            oqw__gcnbr, huz__aiu, extra_globals=ofzho__ovlo)
    return overload_dt_diff_fn


def _install_dt_diff_fn_overload():
    fmt__dfzr = [('day', diff_day, diff_day_util), ('hour', diff_hour,
        diff_hour_util), ('microsecond', diff_microsecond,
        diff_microsecond_util), ('minute', diff_minute, diff_minute_util),
        ('month', diff_month, diff_month_util), ('nanosecond',
        diff_nanosecond, diff_nanosecond_util), ('quarter', diff_quarter,
        diff_quarter), ('second', diff_second, diff_second_util), ('week',
        diff_week, diff_week_util), ('year', diff_year, diff_year_util)]
    for unit, ycrn__riql, ltffm__dshuh in fmt__dfzr:
        kkdpg__atf = create_dt_diff_fn_overload(unit)
        overload(ycrn__riql)(kkdpg__atf)
        tzie__ubiy = create_dt_diff_fn_util_overload(unit)
        overload(ltffm__dshuh)(tzie__ubiy)


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
    nkhx__vdsg = get_tz_if_exists(ts_arg)
    pao__gtnd = ['date_or_time_part', 'ts_arg']
    vsfuy__axwz = [date_or_time_part, ts_arg]
    aglss__uahwj = [True, True]
    xci__igdq = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(ts_arg, True) else '')
    lvqre__bpixi = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(ts_arg, True) else '')
    oqw__gcnbr = """part_str = bodo.libs.bodosql_array_kernels.standardize_snowflake_date_time_part(arg0)
"""
    if nkhx__vdsg is None:
        oqw__gcnbr += f'arg1 = {xci__igdq}(arg1)\n'
    oqw__gcnbr += "if part_str == 'quarter':\n"
    oqw__gcnbr += """    out_val = pd.Timestamp(year=arg1.year, month= (3*(arg1.quarter - 1)) + 1, day=1, tz=tz_literal)
"""
    oqw__gcnbr += "elif part_str == 'year':\n"
    oqw__gcnbr += (
        '    out_val = pd.Timestamp(year=arg1.year, month=1, day=1, tz=tz_literal)\n'
        )
    oqw__gcnbr += "elif part_str == 'month':\n"
    oqw__gcnbr += """    out_val = pd.Timestamp(year=arg1.year, month=arg1.month, day=1, tz=tz_literal)
"""
    oqw__gcnbr += "elif part_str == 'day':\n"
    oqw__gcnbr += '    out_val = arg1.normalize()\n'
    oqw__gcnbr += "elif part_str == 'week':\n"
    oqw__gcnbr += '    if arg1.dayofweek == 0:\n'
    oqw__gcnbr += '        out_val = arg1.normalize()\n'
    oqw__gcnbr += '    else:\n'
    oqw__gcnbr += (
        '        out_val = arg1.normalize() - pd.tseries.offsets.Week(n=1, weekday=0)\n'
        )
    oqw__gcnbr += "elif part_str == 'hour':\n"
    oqw__gcnbr += "    out_val = arg1.floor('H')\n"
    oqw__gcnbr += "elif part_str == 'minute':\n"
    oqw__gcnbr += "    out_val = arg1.floor('min')\n"
    oqw__gcnbr += "elif part_str == 'second':\n"
    oqw__gcnbr += "    out_val = arg1.floor('S')\n"
    oqw__gcnbr += "elif part_str == 'millisecond':\n"
    oqw__gcnbr += "    out_val = arg1.floor('ms')\n"
    oqw__gcnbr += "elif part_str == 'microsecond':\n"
    oqw__gcnbr += "    out_val = arg1.floor('us')\n"
    oqw__gcnbr += "elif part_str == 'nanosecond':\n"
    oqw__gcnbr += '    out_val = arg1\n'
    oqw__gcnbr += 'else:\n'
    oqw__gcnbr += (
        "    raise ValueError('Invalid date or time part for DATE_TRUNC')\n")
    if nkhx__vdsg is None:
        oqw__gcnbr += f'res[i] = {lvqre__bpixi}(out_val)\n'
    else:
        oqw__gcnbr += f'res[i] = out_val\n'
    if nkhx__vdsg is None:
        huz__aiu = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        huz__aiu = bodo.DatetimeArrayType(nkhx__vdsg)
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu, extra_globals={'tz_literal': nkhx__vdsg})


@numba.generated_jit(nopython=True)
def dayname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'dayname', 'arr')
    zhp__thz = get_tz_if_exists(arr)
    xci__igdq = 'bodo.utils.conversion.box_if_dt64' if zhp__thz is None else ''
    pao__gtnd = ['arr']
    vsfuy__axwz = [arr]
    aglss__uahwj = [True]
    oqw__gcnbr = f'res[i] = {xci__igdq}(arg0).day_name()'
    huz__aiu = bodo.string_array_type
    mykj__ioo = ['V']
    hprd__eqszt = pd.array(['Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday'])
    ofzho__ovlo = {'day_of_week_dict_arr': hprd__eqszt}
    vibds__hvs = 'dict_res = day_of_week_dict_arr'
    dyhxn__oqnj = f'res[i] = {xci__igdq}(arg0).dayofweek'
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu, synthesize_dict_if_vector=mykj__ioo,
        synthesize_dict_setup_text=vibds__hvs, synthesize_dict_scalar_text=
        dyhxn__oqnj, extra_globals=ofzho__ovlo, synthesize_dict_global=True,
        synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def int_to_days_util(arr):
    verify_int_arg(arr, 'int_to_days', 'arr')
    lvqre__bpixi = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    pao__gtnd = ['arr']
    vsfuy__axwz = [arr]
    aglss__uahwj = [True]
    oqw__gcnbr = f'res[i] = {lvqre__bpixi}(pd.Timedelta(days=arg0))'
    huz__aiu = np.dtype('timedelta64[ns]')
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu)


@numba.generated_jit(nopython=True)
def last_day_util(arr):
    verify_datetime_arg_allow_tz(arr, 'LAST_DAY', 'arr')
    axfa__kuz = get_tz_if_exists(arr)
    xci__igdq = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    lvqre__bpixi = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    pao__gtnd = ['arr']
    vsfuy__axwz = [arr]
    aglss__uahwj = [True]
    if axfa__kuz is None:
        oqw__gcnbr = (
            f'res[i] = {lvqre__bpixi}({xci__igdq}(arg0) + pd.tseries.offsets.MonthEnd(n=0, normalize=True))'
            )
        huz__aiu = np.dtype('datetime64[ns]')
    else:
        oqw__gcnbr = 'y = arg0.year\n'
        oqw__gcnbr += 'm = arg0.month\n'
        oqw__gcnbr += (
            'd = bodo.hiframes.pd_offsets_ext.get_days_in_month(y, m)\n')
        oqw__gcnbr += (
            f'res[i] = pd.Timestamp(year=y, month=m, day=d, tz={repr(axfa__kuz)})\n'
            )
        huz__aiu = bodo.DatetimeArrayType(axfa__kuz)
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu)


@numba.generated_jit(nopython=True)
def makedate_util(year, day):
    verify_int_arg(year, 'MAKEDATE', 'year')
    verify_int_arg(day, 'MAKEDATE', 'day')
    lvqre__bpixi = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(year, True) or bodo.utils.utils.
        is_array_typ(day, True) else '')
    pao__gtnd = ['year', 'day']
    vsfuy__axwz = [year, day]
    aglss__uahwj = [True] * 2
    oqw__gcnbr = (
        f'res[i] = {lvqre__bpixi}(pd.Timestamp(year=arg0, month=1, day=1) + pd.Timedelta(days=arg1-1))'
        )
    huz__aiu = np.dtype('datetime64[ns]')
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu)


@numba.generated_jit(nopython=True)
def monthname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'monthname', 'arr')
    zhp__thz = get_tz_if_exists(arr)
    xci__igdq = 'bodo.utils.conversion.box_if_dt64' if zhp__thz is None else ''
    pao__gtnd = ['arr']
    vsfuy__axwz = [arr]
    aglss__uahwj = [True]
    oqw__gcnbr = f'res[i] = {xci__igdq}(arg0).month_name()'
    huz__aiu = bodo.string_array_type
    mykj__ioo = ['V']
    fndfu__oza = pd.array(['January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October', 'November',
        'December'])
    ofzho__ovlo = {'month_names_dict_arr': fndfu__oza}
    vibds__hvs = 'dict_res = month_names_dict_arr'
    dyhxn__oqnj = f'res[i] = {xci__igdq}(arg0).month - 1'
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu, synthesize_dict_if_vector=mykj__ioo,
        synthesize_dict_setup_text=vibds__hvs, synthesize_dict_scalar_text=
        dyhxn__oqnj, extra_globals=ofzho__ovlo, synthesize_dict_global=True,
        synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def next_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'NEXT_DAY', 'arr0')
    verify_string_arg(arr1, 'NEXT_DAY', 'arr1')
    ctnum__jcx = is_valid_tz_aware_datetime_arg(arr0)
    lvqre__bpixi = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    pao__gtnd = ['arr0', 'arr1']
    vsfuy__axwz = [arr0, arr1]
    aglss__uahwj = [True] * 2
    dolsr__lcxr = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    oqw__gcnbr = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if ctnum__jcx:
        gocw__pybs = 'arg0'
    else:
        gocw__pybs = 'bodo.utils.conversion.box_if_dt64(arg0)'
    oqw__gcnbr += f"""new_timestamp = {gocw__pybs}.normalize() + pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    oqw__gcnbr += f'res[i] = {lvqre__bpixi}(new_timestamp.tz_localize(None))\n'
    huz__aiu = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu, prefix_code=dolsr__lcxr)


@numba.generated_jit(nopython=True)
def previous_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'PREVIOUS_DAY', 'arr0')
    verify_string_arg(arr1, 'PREVIOUS_DAY', 'arr1')
    ctnum__jcx = is_valid_tz_aware_datetime_arg(arr0)
    lvqre__bpixi = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    pao__gtnd = ['arr0', 'arr1']
    vsfuy__axwz = [arr0, arr1]
    aglss__uahwj = [True] * 2
    dolsr__lcxr = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    oqw__gcnbr = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if ctnum__jcx:
        gocw__pybs = 'arg0'
    else:
        gocw__pybs = 'bodo.utils.conversion.box_if_dt64(arg0)'
    oqw__gcnbr += f"""new_timestamp = {gocw__pybs}.normalize() - pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    oqw__gcnbr += f'res[i] = {lvqre__bpixi}(new_timestamp.tz_localize(None))\n'
    huz__aiu = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu, prefix_code=dolsr__lcxr)


@numba.generated_jit(nopython=True)
def second_timestamp_util(arr):
    verify_int_arg(arr, 'second_timestamp', 'arr')
    lvqre__bpixi = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    pao__gtnd = ['arr']
    vsfuy__axwz = [arr]
    aglss__uahwj = [True]
    oqw__gcnbr = f"res[i] = {lvqre__bpixi}(pd.Timestamp(arg0, unit='s'))"
    huz__aiu = np.dtype('datetime64[ns]')
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu)


@numba.generated_jit(nopython=True)
def weekday_util(arr):
    verify_datetime_arg(arr, 'WEEKDAY', 'arr')
    pao__gtnd = ['arr']
    vsfuy__axwz = [arr]
    aglss__uahwj = [True]
    xci__igdq = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    oqw__gcnbr = f'dt = {xci__igdq}(arg0)\n'
    oqw__gcnbr += (
        'res[i] = bodo.hiframes.pd_timestamp_ext.get_day_of_week(dt.year, dt.month, dt.day)'
        )
    huz__aiu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu)


@numba.generated_jit(nopython=True)
def yearofweekiso_util(arr):
    verify_datetime_arg_allow_tz(arr, 'YEAROFWEEKISO', 'arr')
    pao__gtnd = ['arr']
    vsfuy__axwz = [arr]
    aglss__uahwj = [True]
    xci__igdq = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    oqw__gcnbr = f'dt = {xci__igdq}(arg0)\n'
    oqw__gcnbr += 'res[i] = dt.isocalendar()[0]'
    huz__aiu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu)


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
    pao__gtnd = ['arr']
    vsfuy__axwz = [arr]
    aglss__uahwj = [True]
    dolsr__lcxr = 'unix_days_to_year_zero = 719528\n'
    dolsr__lcxr += 'nanoseconds_divisor = 86400000000000\n'
    huz__aiu = bodo.IntegerArrayType(types.int64)
    vprs__vtco = bodo.utils.utils.is_array_typ(arr, False)
    if vprs__vtco:
        oqw__gcnbr = (
            '  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        oqw__gcnbr = '  in_value = arg0.value\n'
    oqw__gcnbr += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_days_to_year_zero\n'
        )
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu, prefix_code=dolsr__lcxr)


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
    pao__gtnd = ['arr']
    vsfuy__axwz = [arr]
    aglss__uahwj = [True]
    vprs__vtco = bodo.utils.utils.is_array_typ(arr, False)
    if vprs__vtco:
        huz__aiu = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        huz__aiu = bodo.pd_timestamp_tz_naive_type
    dolsr__lcxr = 'unix_days_to_year_zero = 719528\n'
    dolsr__lcxr += 'nanoseconds_divisor = 86400000000000\n'
    oqw__gcnbr = (
        '  nanoseconds = (arg0 - unix_days_to_year_zero) * nanoseconds_divisor\n'
        )
    if vprs__vtco:
        oqw__gcnbr += (
            '  res[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(nanoseconds)\n'
            )
    else:
        oqw__gcnbr += '  res[i] = pd.Timestamp(nanoseconds)\n'
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu, prefix_code=dolsr__lcxr)


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
    fbcmd__cqxzn = get_tz_if_exists(arr)
    pao__gtnd = ['arr']
    vsfuy__axwz = [arr]
    aglss__uahwj = [True]
    dolsr__lcxr = 'unix_seconds_to_year_zero = 62167219200\n'
    dolsr__lcxr += 'nanoseconds_divisor = 1000000000\n'
    huz__aiu = bodo.IntegerArrayType(types.int64)
    vprs__vtco = bodo.utils.utils.is_array_typ(arr, False)
    if vprs__vtco and not fbcmd__cqxzn:
        oqw__gcnbr = (
            f'  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        oqw__gcnbr = f'  in_value = arg0.value\n'
    oqw__gcnbr += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_seconds_to_year_zero\n'
        )
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu, prefix_code=dolsr__lcxr)


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
    fbcmd__cqxzn = get_tz_if_exists(tz_arg)
    pao__gtnd = ['tz_arg', 'interval_arg']
    vsfuy__axwz = [tz_arg, interval_arg]
    aglss__uahwj = [True, True]
    if fbcmd__cqxzn is not None:
        huz__aiu = bodo.DatetimeArrayType(fbcmd__cqxzn)
    else:
        huz__aiu = bodo.datetime64ns
    if interval_arg == bodo.date_offset_type:
        oqw__gcnbr = """  timedelta = bodo.libs.pd_datetime_arr_ext.convert_months_offset_to_days(arg0.year, arg0.month, arg0.day, ((arg1._years * 12) + arg1._months) * arg1.n)
"""
    else:
        oqw__gcnbr = '  timedelta = arg1\n'
    oqw__gcnbr += """  timedelta = bodo.hiframes.pd_offsets_ext.update_timedelta_with_transition(arg0, timedelta)
"""
    oqw__gcnbr += '  res[i] = arg0 + timedelta\n'
    return gen_vectorized(pao__gtnd, vsfuy__axwz, aglss__uahwj, oqw__gcnbr,
        huz__aiu)
