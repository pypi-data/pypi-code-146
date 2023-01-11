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
    kqeh__cqoj = pd.array(['year', 'y', 'yy', 'yyy', 'yyyy', 'yr', 'years',
        'yrs'])
    iuwh__lnur = pd.array(['month', 'mm', 'mon', 'mons', 'months'])
    vnhjo__qolj = pd.array(['day', 'd', 'dd', 'days', 'dayofmonth'])
    hqs__pbfi = pd.array(['dayofweek', 'weekday', 'dow', 'dw'])
    kzoj__flai = pd.array(['week', 'w', 'wk', 'weekofyear', 'woy', 'wy'])
    vxfg__vhasx = pd.array(['weekiso', 'week_iso', 'weekofyeariso',
        'weekofyear_iso'])
    epkos__kjg = pd.array(['quarter', 'q', 'qtr', 'qtrs', 'quarters'])
    xlbuk__brnp = pd.array(['hour', 'h', 'hh', 'hr', 'hours', 'hrs'])
    buqf__ojv = pd.array(['minute', 'm', 'mi', 'min', 'minutes', 'mins'])
    ahnuo__fvq = pd.array(['second', 's', 'sec', 'seconds', 'secs'])
    uhqu__nnlys = pd.array(['millisecond', 'ms', 'msec', 'milliseconds'])
    icoj__aoyr = pd.array(['microsecond', 'us', 'usec', 'microseconds'])
    nltcj__qglj = pd.array(['nanosecond', 'ns', 'nsec', 'nanosec',
        'nsecond', 'nanoseconds', 'nanosecs', 'nseconds'])
    zdpwr__ujk = pd.array(['epoch_second', 'epoch', 'epoch_seconds'])
    hqmao__ddz = pd.array(['epoch_millisecond', 'epoch_milliseconds'])
    xqys__xaoul = pd.array(['epoch_microsecond', 'epoch_microseconds'])
    oun__dnz = pd.array(['epoch_nanosecond', 'epoch_nanoseconds'])
    apx__qlp = pd.array(['timezone_hour', 'tzh'])
    jfsj__ndpi = pd.array(['timezone_minute', 'tzm'])
    mdqe__tfbpl = pd.array(['yearofweek', 'yearofweekiso'])

    def impl(part_str):
        part_str = part_str.lower()
        if part_str in kqeh__cqoj:
            return 'year'
        elif part_str in iuwh__lnur:
            return 'month'
        elif part_str in vnhjo__qolj:
            return 'day'
        elif part_str in hqs__pbfi:
            return 'dayofweek'
        elif part_str in kzoj__flai:
            return 'week'
        elif part_str in vxfg__vhasx:
            return 'weekiso'
        elif part_str in epkos__kjg:
            return 'quarter'
        elif part_str in xlbuk__brnp:
            return 'hour'
        elif part_str in buqf__ojv:
            return 'minute'
        elif part_str in ahnuo__fvq:
            return 'second'
        elif part_str in uhqu__nnlys:
            return 'millisecond'
        elif part_str in icoj__aoyr:
            return 'microsecond'
        elif part_str in nltcj__qglj:
            return 'nanosecond'
        elif part_str in zdpwr__ujk:
            return 'epoch_second'
        elif part_str in hqmao__ddz:
            return 'epoch_millisecond'
        elif part_str in xqys__xaoul:
            return 'epoch_microsecond'
        elif part_str in oun__dnz:
            return 'epoch_nanosecond'
        elif part_str in apx__qlp:
            return 'timezone_hour'
        elif part_str in jfsj__ndpi:
            return 'timezone_minute'
        elif part_str in mdqe__tfbpl:
            return part_str
        else:
            raise ValueError(
                'Invalid date or time part passed into Snowflake array kernel')
    return impl


@numba.generated_jit(nopython=True)
def add_interval(start_dt, interval):
    args = [start_dt, interval]
    for togr__knldw in range(len(args)):
        if isinstance(args[togr__knldw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.add_interval_util', ['arr'
                ], togr__knldw)

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
    for togr__knldw in range(2):
        if isinstance(args[togr__knldw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.makedate',
                ['year', 'day'], togr__knldw)

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
    for togr__knldw in range(2):
        if isinstance(args[togr__knldw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.next_day',
                ['arr0', 'arr1'], togr__knldw)

    def impl(arr0, arr1):
        return next_day_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def previous_day(arr0, arr1):
    args = [arr0, arr1]
    for togr__knldw in range(2):
        if isinstance(args[togr__knldw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.previous_day', ['arr0',
                'arr1'], togr__knldw)

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
    rdyts__qou = get_tz_if_exists(start_dt)
    wpr__mypu = ['start_dt', 'interval']
    itxuu__fwuf = [start_dt, interval]
    qqz__yzp = [True] * 2
    pvjn__jpmo = ''
    csdbw__cwp = bodo.utils.utils.is_array_typ(interval, True
        ) or bodo.utils.utils.is_array_typ(start_dt, True)
    gdsnh__dejq = None
    if rdyts__qou is not None:
        if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(rdyts__qou):
            opp__pvt = pytz.timezone(rdyts__qou)
            nif__cjnb = np.array(opp__pvt._utc_transition_times, dtype='M8[ns]'
                ).view('i8')
            eoe__idrv = np.array(opp__pvt._transition_info)[:, 0]
            eoe__idrv = (pd.Series(eoe__idrv).dt.total_seconds() * 1000000000
                ).astype(np.int64).values
            gdsnh__dejq = {'trans': nif__cjnb, 'deltas': eoe__idrv}
            pvjn__jpmo += f'start_value = arg0.value\n'
            pvjn__jpmo += 'end_value = start_value + arg0.value\n'
            pvjn__jpmo += (
                "start_trans = np.searchsorted(trans, start_value, side='right') - 1\n"
                )
            pvjn__jpmo += (
                "end_trans = np.searchsorted(trans, end_value, side='right') - 1\n"
                )
            pvjn__jpmo += 'offset = deltas[start_trans] - deltas[end_trans]\n'
            pvjn__jpmo += 'arg1 = pd.Timedelta(arg1.value + offset)\n'
        pvjn__jpmo += f'res[i] = arg0 + arg1\n'
        ios__qoen = bodo.DatetimeArrayType(rdyts__qou)
    else:
        nbn__vrn = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
            csdbw__cwp else '')
        omyy__jmip = 'bodo.utils.conversion.box_if_dt64' if csdbw__cwp else ''
        pvjn__jpmo = f'res[i] = {nbn__vrn}({omyy__jmip}(arg0) + arg1)\n'
        ios__qoen = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen, extra_globals=gdsnh__dejq)


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
        for togr__knldw in range(2):
            if isinstance(args[togr__knldw], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.add_interval_{unit}',
                    ['amount', 'start_dt'], togr__knldw)
        uxuji__hliab = 'def impl(amount, start_dt):\n'
        uxuji__hliab += (
            f'  return bodo.libs.bodosql_array_kernels.add_interval_{unit}_util(amount, start_dt)'
            )
        kwzx__ltp = {}
        exec(uxuji__hliab, {'bodo': bodo}, kwzx__ltp)
        return kwzx__ltp['impl']
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
        rdyts__qou = get_tz_if_exists(start_dt)
        wpr__mypu = ['amount', 'start_dt']
        itxuu__fwuf = [amount, start_dt]
        qqz__yzp = [True] * 2
        csdbw__cwp = bodo.utils.utils.is_array_typ(amount, True
            ) or bodo.utils.utils.is_array_typ(start_dt, True)
        gdsnh__dejq = None
        if is_valid_time_arg(start_dt):
            sxkz__rzs = start_dt.precision
            if unit == 'hours':
                unya__tebm = 3600000000000
            elif unit == 'minutes':
                unya__tebm = 60000000000
            elif unit == 'seconds':
                unya__tebm = 1000000000
            elif unit == 'milliseconds':
                sxkz__rzs = max(sxkz__rzs, 3)
                unya__tebm = 1000000
            elif unit == 'microseconds':
                sxkz__rzs = max(sxkz__rzs, 6)
                unya__tebm = 1000
            elif unit == 'nanoseconds':
                sxkz__rzs = max(sxkz__rzs, 9)
                unya__tebm = 1
            pvjn__jpmo = f"""amt = bodo.hiframes.time_ext.cast_time_to_int(arg1) + {unya__tebm} * arg0
"""
            pvjn__jpmo += (
                f'res[i] = bodo.hiframes.time_ext.cast_int_to_time(amt % 86400000000000, precision={sxkz__rzs})'
                )
            ios__qoen = types.Array(bodo.hiframes.time_ext.TimeType(
                sxkz__rzs), 1, 'C')
        elif rdyts__qou is not None:
            if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(rdyts__qou
                ):
                opp__pvt = pytz.timezone(rdyts__qou)
                nif__cjnb = np.array(opp__pvt._utc_transition_times, dtype=
                    'M8[ns]').view('i8')
                eoe__idrv = np.array(opp__pvt._transition_info)[:, 0]
                eoe__idrv = (pd.Series(eoe__idrv).dt.total_seconds() * 
                    1000000000).astype(np.int64).values
                gdsnh__dejq = {'trans': nif__cjnb, 'deltas': eoe__idrv}
            if unit in ('months', 'quarters', 'years'):
                if unit == 'quarters':
                    pvjn__jpmo = f'td = pd.DateOffset(months=3*arg0)\n'
                else:
                    pvjn__jpmo = f'td = pd.DateOffset({unit}=arg0)\n'
                pvjn__jpmo += f'start_value = arg1.value\n'
                pvjn__jpmo += (
                    'end_value = (pd.Timestamp(arg1.value) + td).value\n')
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    rdyts__qou):
                    pvjn__jpmo += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    pvjn__jpmo += """end_trans = np.searchsorted(trans, end_value, side='right') - 1
"""
                    pvjn__jpmo += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    pvjn__jpmo += (
                        'td = pd.Timedelta(end_value - start_value + offset)\n'
                        )
                else:
                    pvjn__jpmo += (
                        'td = pd.Timedelta(end_value - start_value)\n')
            else:
                if unit == 'nanoseconds':
                    pvjn__jpmo = 'td = pd.Timedelta(arg0)\n'
                else:
                    pvjn__jpmo = f'td = pd.Timedelta({unit}=arg0)\n'
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    rdyts__qou):
                    pvjn__jpmo += f'start_value = arg1.value\n'
                    pvjn__jpmo += 'end_value = start_value + td.value\n'
                    pvjn__jpmo += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    pvjn__jpmo += """end_trans = np.searchsorted(trans, end_value, side='right') - 1
"""
                    pvjn__jpmo += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    pvjn__jpmo += 'td = pd.Timedelta(td.value + offset)\n'
            pvjn__jpmo += f'res[i] = arg1 + td\n'
            ios__qoen = bodo.DatetimeArrayType(rdyts__qou)
        else:
            nbn__vrn = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
                csdbw__cwp else '')
            omyy__jmip = ('bodo.utils.conversion.box_if_dt64' if csdbw__cwp
                 else '')
            if unit in ('months', 'years'):
                pvjn__jpmo = f"""res[i] = {nbn__vrn}({omyy__jmip}(arg1) + pd.DateOffset({unit}=arg0))
"""
            elif unit == 'quarters':
                pvjn__jpmo = f"""res[i] = {nbn__vrn}({omyy__jmip}(arg1) + pd.DateOffset(months=3*arg0))
"""
            elif unit == 'nanoseconds':
                pvjn__jpmo = (
                    f'res[i] = {nbn__vrn}({omyy__jmip}(arg1) + pd.Timedelta(arg0))\n'
                    )
            else:
                pvjn__jpmo = f"""res[i] = {nbn__vrn}({omyy__jmip}(arg1) + pd.Timedelta({unit}=arg0))
"""
            ios__qoen = types.Array(bodo.datetime64ns, 1, 'C')
        return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
            ios__qoen, extra_globals=gdsnh__dejq)
    return overload_add_datetime_interval_util


def _install_add_interval_overload():
    iot__min = [('years', add_interval_years, add_interval_years_util), (
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
    for unit, stl__qtkn, pwoqh__pin in iot__min:
        nsy__yotig = create_add_interval_func_overload(unit)
        overload(stl__qtkn)(nsy__yotig)
        fqs__rotx = create_add_interval_util_overload(unit)
        overload(pwoqh__pin)(fqs__rotx)


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
        uxuji__hliab = 'def impl(arr):\n'
        uxuji__hliab += (
            f'  return bodo.libs.bodosql_array_kernels.{fn_name}_util(arr)')
        kwzx__ltp = {}
        exec(uxuji__hliab, {'bodo': bodo}, kwzx__ltp)
        return kwzx__ltp['impl']
    return overload_func


def create_dt_extract_fn_util_overload(fn_name):

    def overload_dt_extract_fn(arr):
        if fn_name in ('get_hour', 'get_minute', 'get_second',
            'get_microsecond', 'get_millisecond', 'get_nanosecond'):
            verify_time_or_datetime_arg_allow_tz(arr, fn_name, 'arr')
        else:
            verify_datetime_arg_allow_tz(arr, fn_name, 'arr')
        did__pidn = get_tz_if_exists(arr)
        omyy__jmip = ('bodo.utils.conversion.box_if_dt64' if did__pidn is
            None else '')
        uqz__zku = 'microsecond // 1000' if not is_valid_time_arg(arr
            ) else 'millisecond'
        bivt__othk = {'get_year': f'{omyy__jmip}(arg0).year', 'get_quarter':
            f'{omyy__jmip}(arg0).quarter', 'get_month':
            f'{omyy__jmip}(arg0).month', 'get_week':
            f'{omyy__jmip}(arg0).week', 'get_hour':
            f'{omyy__jmip}(arg0).hour', 'get_minute':
            f'{omyy__jmip}(arg0).minute', 'get_second':
            f'{omyy__jmip}(arg0).second', 'get_millisecond':
            f'{omyy__jmip}(arg0).{uqz__zku}', 'get_microsecond':
            f'{omyy__jmip}(arg0).microsecond', 'get_nanosecond':
            f'{omyy__jmip}(arg0).nanosecond', 'dayofmonth':
            f'{omyy__jmip}(arg0).day', 'dayofweek':
            f'({omyy__jmip}(arg0).dayofweek + 1) % 7', 'dayofweekiso':
            f'{omyy__jmip}(arg0).dayofweek + 1', 'dayofyear':
            f'{omyy__jmip}(arg0).dayofyear'}
        wpr__mypu = ['arr']
        itxuu__fwuf = [arr]
        qqz__yzp = [True]
        pvjn__jpmo = f'res[i] = {bivt__othk[fn_name]}'
        ios__qoen = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
            ios__qoen)
    return overload_dt_extract_fn


def _install_dt_extract_fn_overload():
    iot__min = [('get_year', get_year, get_year_util), ('get_quarter',
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
    for fn_name, stl__qtkn, pwoqh__pin in iot__min:
        nsy__yotig = create_dt_extract_fn_overload(fn_name)
        overload(stl__qtkn)(nsy__yotig)
        fqs__rotx = create_dt_extract_fn_util_overload(fn_name)
        overload(pwoqh__pin)(fqs__rotx)


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
    ozl__jblex = 1
    if year1 < year0:
        year0, year1 = year1, year0
        ozl__jblex = -1
    qfux__cozt = 0
    for gbzw__shk in range(year0, year1):
        qfux__cozt += 52
        fgg__wlqe = (gbzw__shk + gbzw__shk // 4 - gbzw__shk // 100 + 
            gbzw__shk // 400) % 7
        lehpi__pbd = (gbzw__shk - 1 + (gbzw__shk - 1) // 4 - (gbzw__shk - 1
            ) // 100 + (gbzw__shk - 1) // 400) % 7
        if fgg__wlqe == 4 or lehpi__pbd == 3:
            qfux__cozt += 1
    return ozl__jblex * qfux__cozt


def create_dt_diff_fn_overload(unit):

    def overload_func(arr0, arr1):
        args = [arr0, arr1]
        for togr__knldw in range(len(args)):
            if isinstance(args[togr__knldw], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.diff_{unit}', ['arr0',
                    'arr1'], togr__knldw)
        uxuji__hliab = 'def impl(arr0, arr1):\n'
        uxuji__hliab += (
            f'  return bodo.libs.bodosql_array_kernels.diff_{unit}_util(arr0, arr1)'
            )
        kwzx__ltp = {}
        exec(uxuji__hliab, {'bodo': bodo}, kwzx__ltp)
        return kwzx__ltp['impl']
    return overload_func


def create_dt_diff_fn_util_overload(unit):

    def overload_dt_diff_fn(arr0, arr1):
        verify_datetime_arg_allow_tz(arr0, 'diff_' + unit, 'arr0')
        verify_datetime_arg_allow_tz(arr1, 'diff_' + unit, 'arr1')
        did__pidn = get_tz_if_exists(arr0)
        if get_tz_if_exists(arr1) != did__pidn:
            raise_bodo_error(
                f'diff_{unit}: both arguments must have the same timezone')
        wpr__mypu = ['arr0', 'arr1']
        itxuu__fwuf = [arr0, arr1]
        qqz__yzp = [True] * 2
        gdsnh__dejq = None
        rzepc__nvla = {'yr_diff': 'arg1.year - arg0.year', 'qu_diff':
            'arg1.quarter - arg0.quarter', 'mo_diff':
            'arg1.month - arg0.month', 'y0, w0, _': 'arg0.isocalendar()',
            'y1, w1, _': 'arg1.isocalendar()', 'iso_yr_diff':
            'bodo.libs.bodosql_array_kernels.get_iso_weeks_between_years(y0, y1)'
            , 'wk_diff': 'w1 - w0', 'da_diff':
            '(pd.Timestamp(arg1.year, arg1.month, arg1.day) - pd.Timestamp(arg0.year, arg0.month, arg0.day)).days'
            , 'ns_diff': 'arg1.value - arg0.value'}
        oktc__ktkrd = {'year': ['yr_diff'], 'quarter': ['yr_diff',
            'qu_diff'], 'month': ['yr_diff', 'mo_diff'], 'week': [
            'y0, w0, _', 'y1, w1, _', 'iso_yr_diff', 'wk_diff'], 'day': [
            'da_diff'], 'nanosecond': ['ns_diff']}
        pvjn__jpmo = ''
        if did__pidn == None:
            pvjn__jpmo += 'arg0 = bodo.utils.conversion.box_if_dt64(arg0)\n'
            pvjn__jpmo += 'arg1 = bodo.utils.conversion.box_if_dt64(arg1)\n'
        for ugap__wrbb in oktc__ktkrd.get(unit, []):
            pvjn__jpmo += f'{ugap__wrbb} = {rzepc__nvla[ugap__wrbb]}\n'
        if unit == 'nanosecond':
            ios__qoen = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        else:
            ios__qoen = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
        if unit == 'year':
            pvjn__jpmo += 'res[i] = yr_diff'
        elif unit == 'quarter':
            pvjn__jpmo += 'res[i] = 4 * yr_diff + qu_diff'
        elif unit == 'month':
            pvjn__jpmo += 'res[i] = 12 * yr_diff + mo_diff'
        elif unit == 'week':
            pvjn__jpmo += 'res[i] = iso_yr_diff + wk_diff'
        elif unit == 'day':
            pvjn__jpmo += 'res[i] = da_diff'
        elif unit == 'nanosecond':
            pvjn__jpmo += 'res[i] = ns_diff'
        else:
            if unit == 'hour':
                rjpu__bdt = 3600000000000
            if unit == 'minute':
                rjpu__bdt = 60000000000
            if unit == 'second':
                rjpu__bdt = 1000000000
            if unit == 'microsecond':
                rjpu__bdt = 1000
            pvjn__jpmo += f"""res[i] = np.floor_divide((arg1.value), ({rjpu__bdt})) - np.floor_divide((arg0.value), ({rjpu__bdt}))
"""
        return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
            ios__qoen, extra_globals=gdsnh__dejq)
    return overload_dt_diff_fn


def _install_dt_diff_fn_overload():
    iot__min = [('day', diff_day, diff_day_util), ('hour', diff_hour,
        diff_hour_util), ('microsecond', diff_microsecond,
        diff_microsecond_util), ('minute', diff_minute, diff_minute_util),
        ('month', diff_month, diff_month_util), ('nanosecond',
        diff_nanosecond, diff_nanosecond_util), ('quarter', diff_quarter,
        diff_quarter), ('second', diff_second, diff_second_util), ('week',
        diff_week, diff_week_util), ('year', diff_year, diff_year_util)]
    for unit, stl__qtkn, pwoqh__pin in iot__min:
        nsy__yotig = create_dt_diff_fn_overload(unit)
        overload(stl__qtkn)(nsy__yotig)
        fqs__rotx = create_dt_diff_fn_util_overload(unit)
        overload(pwoqh__pin)(fqs__rotx)


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
    npk__dcvti = get_tz_if_exists(ts_arg)
    wpr__mypu = ['date_or_time_part', 'ts_arg']
    itxuu__fwuf = [date_or_time_part, ts_arg]
    qqz__yzp = [True, True]
    omyy__jmip = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(ts_arg, True) else '')
    nbn__vrn = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(ts_arg, True) else '')
    pvjn__jpmo = """part_str = bodo.libs.bodosql_array_kernels.standardize_snowflake_date_time_part(arg0)
"""
    if npk__dcvti is None:
        pvjn__jpmo += f'arg1 = {omyy__jmip}(arg1)\n'
    pvjn__jpmo += "if part_str == 'quarter':\n"
    pvjn__jpmo += """    out_val = pd.Timestamp(year=arg1.year, month= (3*(arg1.quarter - 1)) + 1, day=1, tz=tz_literal)
"""
    pvjn__jpmo += "elif part_str == 'year':\n"
    pvjn__jpmo += (
        '    out_val = pd.Timestamp(year=arg1.year, month=1, day=1, tz=tz_literal)\n'
        )
    pvjn__jpmo += "elif part_str == 'month':\n"
    pvjn__jpmo += """    out_val = pd.Timestamp(year=arg1.year, month=arg1.month, day=1, tz=tz_literal)
"""
    pvjn__jpmo += "elif part_str == 'day':\n"
    pvjn__jpmo += '    out_val = arg1.normalize()\n'
    pvjn__jpmo += "elif part_str == 'week':\n"
    pvjn__jpmo += '    if arg1.dayofweek == 0:\n'
    pvjn__jpmo += '        out_val = arg1.normalize()\n'
    pvjn__jpmo += '    else:\n'
    pvjn__jpmo += (
        '        out_val = arg1.normalize() - pd.tseries.offsets.Week(n=1, weekday=0)\n'
        )
    pvjn__jpmo += "elif part_str == 'hour':\n"
    pvjn__jpmo += "    out_val = arg1.floor('H')\n"
    pvjn__jpmo += "elif part_str == 'minute':\n"
    pvjn__jpmo += "    out_val = arg1.floor('min')\n"
    pvjn__jpmo += "elif part_str == 'second':\n"
    pvjn__jpmo += "    out_val = arg1.floor('S')\n"
    pvjn__jpmo += "elif part_str == 'millisecond':\n"
    pvjn__jpmo += "    out_val = arg1.floor('ms')\n"
    pvjn__jpmo += "elif part_str == 'microsecond':\n"
    pvjn__jpmo += "    out_val = arg1.floor('us')\n"
    pvjn__jpmo += "elif part_str == 'nanosecond':\n"
    pvjn__jpmo += '    out_val = arg1\n'
    pvjn__jpmo += 'else:\n'
    pvjn__jpmo += (
        "    raise ValueError('Invalid date or time part for DATE_TRUNC')\n")
    if npk__dcvti is None:
        pvjn__jpmo += f'res[i] = {nbn__vrn}(out_val)\n'
    else:
        pvjn__jpmo += f'res[i] = out_val\n'
    if npk__dcvti is None:
        ios__qoen = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        ios__qoen = bodo.DatetimeArrayType(npk__dcvti)
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen, extra_globals={'tz_literal': npk__dcvti})


@numba.generated_jit(nopython=True)
def dayname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'dayname', 'arr')
    did__pidn = get_tz_if_exists(arr)
    omyy__jmip = ('bodo.utils.conversion.box_if_dt64' if did__pidn is None else
        '')
    wpr__mypu = ['arr']
    itxuu__fwuf = [arr]
    qqz__yzp = [True]
    pvjn__jpmo = f'res[i] = {omyy__jmip}(arg0).day_name()'
    ios__qoen = bodo.string_array_type
    jnud__rxsua = ['V']
    atiy__pdaki = pd.array(['Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday'])
    gdsnh__dejq = {'day_of_week_dict_arr': atiy__pdaki}
    qjkg__wksh = 'dict_res = day_of_week_dict_arr'
    wxcm__eqge = f'res[i] = {omyy__jmip}(arg0).dayofweek'
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen, synthesize_dict_if_vector=jnud__rxsua,
        synthesize_dict_setup_text=qjkg__wksh, synthesize_dict_scalar_text=
        wxcm__eqge, extra_globals=gdsnh__dejq, synthesize_dict_global=True,
        synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def int_to_days_util(arr):
    verify_int_arg(arr, 'int_to_days', 'arr')
    nbn__vrn = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(arr, True) else '')
    wpr__mypu = ['arr']
    itxuu__fwuf = [arr]
    qqz__yzp = [True]
    pvjn__jpmo = f'res[i] = {nbn__vrn}(pd.Timedelta(days=arg0))'
    ios__qoen = np.dtype('timedelta64[ns]')
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen)


@numba.generated_jit(nopython=True)
def last_day_util(arr):
    verify_datetime_arg_allow_tz(arr, 'LAST_DAY', 'arr')
    rdyts__qou = get_tz_if_exists(arr)
    omyy__jmip = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    nbn__vrn = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(arr, True) else '')
    wpr__mypu = ['arr']
    itxuu__fwuf = [arr]
    qqz__yzp = [True]
    if rdyts__qou is None:
        pvjn__jpmo = (
            f'res[i] = {nbn__vrn}({omyy__jmip}(arg0) + pd.tseries.offsets.MonthEnd(n=0, normalize=True))'
            )
        ios__qoen = np.dtype('datetime64[ns]')
    else:
        pvjn__jpmo = 'y = arg0.year\n'
        pvjn__jpmo += 'm = arg0.month\n'
        pvjn__jpmo += (
            'd = bodo.hiframes.pd_offsets_ext.get_days_in_month(y, m)\n')
        pvjn__jpmo += (
            f'res[i] = pd.Timestamp(year=y, month=m, day=d, tz={repr(rdyts__qou)})\n'
            )
        ios__qoen = bodo.DatetimeArrayType(rdyts__qou)
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen)


@numba.generated_jit(nopython=True)
def makedate_util(year, day):
    verify_int_arg(year, 'MAKEDATE', 'year')
    verify_int_arg(day, 'MAKEDATE', 'day')
    nbn__vrn = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(year, True) or bodo.utils.utils.
        is_array_typ(day, True) else '')
    wpr__mypu = ['year', 'day']
    itxuu__fwuf = [year, day]
    qqz__yzp = [True] * 2
    pvjn__jpmo = (
        f'res[i] = {nbn__vrn}(pd.Timestamp(year=arg0, month=1, day=1) + pd.Timedelta(days=arg1-1))'
        )
    ios__qoen = np.dtype('datetime64[ns]')
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen)


@numba.generated_jit(nopython=True)
def monthname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'monthname', 'arr')
    did__pidn = get_tz_if_exists(arr)
    omyy__jmip = ('bodo.utils.conversion.box_if_dt64' if did__pidn is None else
        '')
    wpr__mypu = ['arr']
    itxuu__fwuf = [arr]
    qqz__yzp = [True]
    pvjn__jpmo = f'res[i] = {omyy__jmip}(arg0).month_name()'
    ios__qoen = bodo.string_array_type
    jnud__rxsua = ['V']
    fjrws__svq = pd.array(['January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October', 'November',
        'December'])
    gdsnh__dejq = {'month_names_dict_arr': fjrws__svq}
    qjkg__wksh = 'dict_res = month_names_dict_arr'
    wxcm__eqge = f'res[i] = {omyy__jmip}(arg0).month - 1'
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen, synthesize_dict_if_vector=jnud__rxsua,
        synthesize_dict_setup_text=qjkg__wksh, synthesize_dict_scalar_text=
        wxcm__eqge, extra_globals=gdsnh__dejq, synthesize_dict_global=True,
        synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def next_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'NEXT_DAY', 'arr0')
    verify_string_arg(arr1, 'NEXT_DAY', 'arr1')
    lgfyq__otpxd = is_valid_tz_aware_datetime_arg(arr0)
    nbn__vrn = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    wpr__mypu = ['arr0', 'arr1']
    itxuu__fwuf = [arr0, arr1]
    qqz__yzp = [True] * 2
    qkc__eqvr = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    pvjn__jpmo = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if lgfyq__otpxd:
        ijleh__sfad = 'arg0'
    else:
        ijleh__sfad = 'bodo.utils.conversion.box_if_dt64(arg0)'
    pvjn__jpmo += f"""new_timestamp = {ijleh__sfad}.normalize() + pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    pvjn__jpmo += f'res[i] = {nbn__vrn}(new_timestamp.tz_localize(None))\n'
    ios__qoen = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen, prefix_code=qkc__eqvr)


@numba.generated_jit(nopython=True)
def previous_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'PREVIOUS_DAY', 'arr0')
    verify_string_arg(arr1, 'PREVIOUS_DAY', 'arr1')
    lgfyq__otpxd = is_valid_tz_aware_datetime_arg(arr0)
    nbn__vrn = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    wpr__mypu = ['arr0', 'arr1']
    itxuu__fwuf = [arr0, arr1]
    qqz__yzp = [True] * 2
    qkc__eqvr = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    pvjn__jpmo = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if lgfyq__otpxd:
        ijleh__sfad = 'arg0'
    else:
        ijleh__sfad = 'bodo.utils.conversion.box_if_dt64(arg0)'
    pvjn__jpmo += f"""new_timestamp = {ijleh__sfad}.normalize() - pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    pvjn__jpmo += f'res[i] = {nbn__vrn}(new_timestamp.tz_localize(None))\n'
    ios__qoen = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen, prefix_code=qkc__eqvr)


@numba.generated_jit(nopython=True)
def second_timestamp_util(arr):
    verify_int_arg(arr, 'second_timestamp', 'arr')
    nbn__vrn = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(arr, True) else '')
    wpr__mypu = ['arr']
    itxuu__fwuf = [arr]
    qqz__yzp = [True]
    pvjn__jpmo = f"res[i] = {nbn__vrn}(pd.Timestamp(arg0, unit='s'))"
    ios__qoen = np.dtype('datetime64[ns]')
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen)


@numba.generated_jit(nopython=True)
def weekday_util(arr):
    verify_datetime_arg(arr, 'WEEKDAY', 'arr')
    wpr__mypu = ['arr']
    itxuu__fwuf = [arr]
    qqz__yzp = [True]
    omyy__jmip = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    pvjn__jpmo = f'dt = {omyy__jmip}(arg0)\n'
    pvjn__jpmo += (
        'res[i] = bodo.hiframes.pd_timestamp_ext.get_day_of_week(dt.year, dt.month, dt.day)'
        )
    ios__qoen = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen)


@numba.generated_jit(nopython=True)
def yearofweekiso_util(arr):
    verify_datetime_arg_allow_tz(arr, 'YEAROFWEEKISO', 'arr')
    wpr__mypu = ['arr']
    itxuu__fwuf = [arr]
    qqz__yzp = [True]
    omyy__jmip = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    pvjn__jpmo = f'dt = {omyy__jmip}(arg0)\n'
    pvjn__jpmo += 'res[i] = dt.isocalendar()[0]'
    ios__qoen = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen)


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
    wpr__mypu = ['arr']
    itxuu__fwuf = [arr]
    qqz__yzp = [True]
    qkc__eqvr = 'unix_days_to_year_zero = 719528\n'
    qkc__eqvr += 'nanoseconds_divisor = 86400000000000\n'
    ios__qoen = bodo.IntegerArrayType(types.int64)
    xfmwv__hgm = bodo.utils.utils.is_array_typ(arr, False)
    if xfmwv__hgm:
        pvjn__jpmo = (
            '  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        pvjn__jpmo = '  in_value = arg0.value\n'
    pvjn__jpmo += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_days_to_year_zero\n'
        )
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen, prefix_code=qkc__eqvr)


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
    wpr__mypu = ['arr']
    itxuu__fwuf = [arr]
    qqz__yzp = [True]
    xfmwv__hgm = bodo.utils.utils.is_array_typ(arr, False)
    if xfmwv__hgm:
        ios__qoen = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        ios__qoen = bodo.pd_timestamp_tz_naive_type
    qkc__eqvr = 'unix_days_to_year_zero = 719528\n'
    qkc__eqvr += 'nanoseconds_divisor = 86400000000000\n'
    pvjn__jpmo = (
        '  nanoseconds = (arg0 - unix_days_to_year_zero) * nanoseconds_divisor\n'
        )
    if xfmwv__hgm:
        pvjn__jpmo += (
            '  res[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(nanoseconds)\n'
            )
    else:
        pvjn__jpmo += '  res[i] = pd.Timestamp(nanoseconds)\n'
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen, prefix_code=qkc__eqvr)


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
    jmg__iwutk = get_tz_if_exists(arr)
    wpr__mypu = ['arr']
    itxuu__fwuf = [arr]
    qqz__yzp = [True]
    qkc__eqvr = 'unix_seconds_to_year_zero = 62167219200\n'
    qkc__eqvr += 'nanoseconds_divisor = 1000000000\n'
    ios__qoen = bodo.IntegerArrayType(types.int64)
    xfmwv__hgm = bodo.utils.utils.is_array_typ(arr, False)
    if xfmwv__hgm and not jmg__iwutk:
        pvjn__jpmo = (
            f'  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        pvjn__jpmo = f'  in_value = arg0.value\n'
    pvjn__jpmo += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_seconds_to_year_zero\n'
        )
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen, prefix_code=qkc__eqvr)


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
    jmg__iwutk = get_tz_if_exists(tz_arg)
    wpr__mypu = ['tz_arg', 'interval_arg']
    itxuu__fwuf = [tz_arg, interval_arg]
    qqz__yzp = [True, True]
    if jmg__iwutk is not None:
        ios__qoen = bodo.DatetimeArrayType(jmg__iwutk)
    else:
        ios__qoen = bodo.datetime64ns
    if interval_arg == bodo.date_offset_type:
        pvjn__jpmo = """  timedelta = bodo.libs.pd_datetime_arr_ext.convert_months_offset_to_days(arg0.year, arg0.month, arg0.day, ((arg1._years * 12) + arg1._months) * arg1.n)
"""
    else:
        pvjn__jpmo = '  timedelta = arg1\n'
    pvjn__jpmo += """  timedelta = bodo.hiframes.pd_offsets_ext.update_timedelta_with_transition(arg0, timedelta)
"""
    pvjn__jpmo += '  res[i] = arg0 + timedelta\n'
    return gen_vectorized(wpr__mypu, itxuu__fwuf, qqz__yzp, pvjn__jpmo,
        ios__qoen)
