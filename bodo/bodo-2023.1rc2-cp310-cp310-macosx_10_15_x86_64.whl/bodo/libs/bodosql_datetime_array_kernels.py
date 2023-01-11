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
    bnz__kzg = pd.array(['year', 'y', 'yy', 'yyy', 'yyyy', 'yr', 'years',
        'yrs'])
    hmr__tii = pd.array(['month', 'mm', 'mon', 'mons', 'months'])
    tpjee__mgdg = pd.array(['day', 'd', 'dd', 'days', 'dayofmonth'])
    mja__rih = pd.array(['dayofweek', 'weekday', 'dow', 'dw'])
    sxt__oah = pd.array(['week', 'w', 'wk', 'weekofyear', 'woy', 'wy'])
    bxddy__lvpy = pd.array(['weekiso', 'week_iso', 'weekofyeariso',
        'weekofyear_iso'])
    cnd__qoqby = pd.array(['quarter', 'q', 'qtr', 'qtrs', 'quarters'])
    qqkcu__igd = pd.array(['hour', 'h', 'hh', 'hr', 'hours', 'hrs'])
    cedca__qpco = pd.array(['minute', 'm', 'mi', 'min', 'minutes', 'mins'])
    dwa__vtafk = pd.array(['second', 's', 'sec', 'seconds', 'secs'])
    cav__plebl = pd.array(['millisecond', 'ms', 'msec', 'milliseconds'])
    tsv__vhh = pd.array(['microsecond', 'us', 'usec', 'microseconds'])
    xoxks__pjf = pd.array(['nanosecond', 'ns', 'nsec', 'nanosec', 'nsecond',
        'nanoseconds', 'nanosecs', 'nseconds'])
    rphz__tll = pd.array(['epoch_second', 'epoch', 'epoch_seconds'])
    sdq__bxyah = pd.array(['epoch_millisecond', 'epoch_milliseconds'])
    bxcw__mykdx = pd.array(['epoch_microsecond', 'epoch_microseconds'])
    ufgtn__viuct = pd.array(['epoch_nanosecond', 'epoch_nanoseconds'])
    gjmop__smqo = pd.array(['timezone_hour', 'tzh'])
    ydsjl__wed = pd.array(['timezone_minute', 'tzm'])
    gloj__sjb = pd.array(['yearofweek', 'yearofweekiso'])

    def impl(part_str):
        part_str = part_str.lower()
        if part_str in bnz__kzg:
            return 'year'
        elif part_str in hmr__tii:
            return 'month'
        elif part_str in tpjee__mgdg:
            return 'day'
        elif part_str in mja__rih:
            return 'dayofweek'
        elif part_str in sxt__oah:
            return 'week'
        elif part_str in bxddy__lvpy:
            return 'weekiso'
        elif part_str in cnd__qoqby:
            return 'quarter'
        elif part_str in qqkcu__igd:
            return 'hour'
        elif part_str in cedca__qpco:
            return 'minute'
        elif part_str in dwa__vtafk:
            return 'second'
        elif part_str in cav__plebl:
            return 'millisecond'
        elif part_str in tsv__vhh:
            return 'microsecond'
        elif part_str in xoxks__pjf:
            return 'nanosecond'
        elif part_str in rphz__tll:
            return 'epoch_second'
        elif part_str in sdq__bxyah:
            return 'epoch_millisecond'
        elif part_str in bxcw__mykdx:
            return 'epoch_microsecond'
        elif part_str in ufgtn__viuct:
            return 'epoch_nanosecond'
        elif part_str in gjmop__smqo:
            return 'timezone_hour'
        elif part_str in ydsjl__wed:
            return 'timezone_minute'
        elif part_str in gloj__sjb:
            return part_str
        else:
            raise ValueError(
                'Invalid date or time part passed into Snowflake array kernel')
    return impl


@numba.generated_jit(nopython=True)
def add_interval(start_dt, interval):
    args = [start_dt, interval]
    for lakyw__mqyf in range(len(args)):
        if isinstance(args[lakyw__mqyf], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.add_interval_util', ['arr'
                ], lakyw__mqyf)

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
    for lakyw__mqyf in range(2):
        if isinstance(args[lakyw__mqyf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.makedate',
                ['year', 'day'], lakyw__mqyf)

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
    for lakyw__mqyf in range(2):
        if isinstance(args[lakyw__mqyf], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.next_day',
                ['arr0', 'arr1'], lakyw__mqyf)

    def impl(arr0, arr1):
        return next_day_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def previous_day(arr0, arr1):
    args = [arr0, arr1]
    for lakyw__mqyf in range(2):
        if isinstance(args[lakyw__mqyf], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.previous_day', ['arr0',
                'arr1'], lakyw__mqyf)

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
    rmw__kvvp = get_tz_if_exists(start_dt)
    nvgd__lbsd = ['start_dt', 'interval']
    sfb__wbsib = [start_dt, interval]
    zoloe__nlb = [True] * 2
    jmi__ryjz = ''
    mddg__thv = bodo.utils.utils.is_array_typ(interval, True
        ) or bodo.utils.utils.is_array_typ(start_dt, True)
    qrc__mwq = None
    if rmw__kvvp is not None:
        if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(rmw__kvvp):
            sibfp__hux = pytz.timezone(rmw__kvvp)
            lmabz__dvro = np.array(sibfp__hux._utc_transition_times, dtype=
                'M8[ns]').view('i8')
            sgx__ecq = np.array(sibfp__hux._transition_info)[:, 0]
            sgx__ecq = (pd.Series(sgx__ecq).dt.total_seconds() * 1000000000
                ).astype(np.int64).values
            qrc__mwq = {'trans': lmabz__dvro, 'deltas': sgx__ecq}
            jmi__ryjz += f'start_value = arg0.value\n'
            jmi__ryjz += 'end_value = start_value + arg0.value\n'
            jmi__ryjz += (
                "start_trans = np.searchsorted(trans, start_value, side='right') - 1\n"
                )
            jmi__ryjz += (
                "end_trans = np.searchsorted(trans, end_value, side='right') - 1\n"
                )
            jmi__ryjz += 'offset = deltas[start_trans] - deltas[end_trans]\n'
            jmi__ryjz += 'arg1 = pd.Timedelta(arg1.value + offset)\n'
        jmi__ryjz += f'res[i] = arg0 + arg1\n'
        ytqb__mcth = bodo.DatetimeArrayType(rmw__kvvp)
    else:
        xgqyv__myoy = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
            mddg__thv else '')
        xov__axe = 'bodo.utils.conversion.box_if_dt64' if mddg__thv else ''
        jmi__ryjz = f'res[i] = {xgqyv__myoy}({xov__axe}(arg0) + arg1)\n'
        ytqb__mcth = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth, extra_globals=qrc__mwq)


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
        for lakyw__mqyf in range(2):
            if isinstance(args[lakyw__mqyf], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.add_interval_{unit}',
                    ['amount', 'start_dt'], lakyw__mqyf)
        irbgx__yqfw = 'def impl(amount, start_dt):\n'
        irbgx__yqfw += (
            f'  return bodo.libs.bodosql_array_kernels.add_interval_{unit}_util(amount, start_dt)'
            )
        tvvs__mgtfg = {}
        exec(irbgx__yqfw, {'bodo': bodo}, tvvs__mgtfg)
        return tvvs__mgtfg['impl']
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
        rmw__kvvp = get_tz_if_exists(start_dt)
        nvgd__lbsd = ['amount', 'start_dt']
        sfb__wbsib = [amount, start_dt]
        zoloe__nlb = [True] * 2
        mddg__thv = bodo.utils.utils.is_array_typ(amount, True
            ) or bodo.utils.utils.is_array_typ(start_dt, True)
        qrc__mwq = None
        if is_valid_time_arg(start_dt):
            vef__jrqy = start_dt.precision
            if unit == 'hours':
                pgfh__zzql = 3600000000000
            elif unit == 'minutes':
                pgfh__zzql = 60000000000
            elif unit == 'seconds':
                pgfh__zzql = 1000000000
            elif unit == 'milliseconds':
                vef__jrqy = max(vef__jrqy, 3)
                pgfh__zzql = 1000000
            elif unit == 'microseconds':
                vef__jrqy = max(vef__jrqy, 6)
                pgfh__zzql = 1000
            elif unit == 'nanoseconds':
                vef__jrqy = max(vef__jrqy, 9)
                pgfh__zzql = 1
            jmi__ryjz = f"""amt = bodo.hiframes.time_ext.cast_time_to_int(arg1) + {pgfh__zzql} * arg0
"""
            jmi__ryjz += (
                f'res[i] = bodo.hiframes.time_ext.cast_int_to_time(amt % 86400000000000, precision={vef__jrqy})'
                )
            ytqb__mcth = types.Array(bodo.hiframes.time_ext.TimeType(
                vef__jrqy), 1, 'C')
        elif rmw__kvvp is not None:
            if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(rmw__kvvp):
                sibfp__hux = pytz.timezone(rmw__kvvp)
                lmabz__dvro = np.array(sibfp__hux._utc_transition_times,
                    dtype='M8[ns]').view('i8')
                sgx__ecq = np.array(sibfp__hux._transition_info)[:, 0]
                sgx__ecq = (pd.Series(sgx__ecq).dt.total_seconds() * 1000000000
                    ).astype(np.int64).values
                qrc__mwq = {'trans': lmabz__dvro, 'deltas': sgx__ecq}
            if unit in ('months', 'quarters', 'years'):
                if unit == 'quarters':
                    jmi__ryjz = f'td = pd.DateOffset(months=3*arg0)\n'
                else:
                    jmi__ryjz = f'td = pd.DateOffset({unit}=arg0)\n'
                jmi__ryjz += f'start_value = arg1.value\n'
                jmi__ryjz += (
                    'end_value = (pd.Timestamp(arg1.value) + td).value\n')
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    rmw__kvvp):
                    jmi__ryjz += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    jmi__ryjz += """end_trans = np.searchsorted(trans, end_value, side='right') - 1
"""
                    jmi__ryjz += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    jmi__ryjz += (
                        'td = pd.Timedelta(end_value - start_value + offset)\n'
                        )
                else:
                    jmi__ryjz += 'td = pd.Timedelta(end_value - start_value)\n'
            else:
                if unit == 'nanoseconds':
                    jmi__ryjz = 'td = pd.Timedelta(arg0)\n'
                else:
                    jmi__ryjz = f'td = pd.Timedelta({unit}=arg0)\n'
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    rmw__kvvp):
                    jmi__ryjz += f'start_value = arg1.value\n'
                    jmi__ryjz += 'end_value = start_value + td.value\n'
                    jmi__ryjz += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    jmi__ryjz += """end_trans = np.searchsorted(trans, end_value, side='right') - 1
"""
                    jmi__ryjz += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    jmi__ryjz += 'td = pd.Timedelta(td.value + offset)\n'
            jmi__ryjz += f'res[i] = arg1 + td\n'
            ytqb__mcth = bodo.DatetimeArrayType(rmw__kvvp)
        else:
            xgqyv__myoy = (
                'bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
                mddg__thv else '')
            xov__axe = 'bodo.utils.conversion.box_if_dt64' if mddg__thv else ''
            if unit in ('months', 'years'):
                jmi__ryjz = f"""res[i] = {xgqyv__myoy}({xov__axe}(arg1) + pd.DateOffset({unit}=arg0))
"""
            elif unit == 'quarters':
                jmi__ryjz = f"""res[i] = {xgqyv__myoy}({xov__axe}(arg1) + pd.DateOffset(months=3*arg0))
"""
            elif unit == 'nanoseconds':
                jmi__ryjz = (
                    f'res[i] = {xgqyv__myoy}({xov__axe}(arg1) + pd.Timedelta(arg0))\n'
                    )
            else:
                jmi__ryjz = f"""res[i] = {xgqyv__myoy}({xov__axe}(arg1) + pd.Timedelta({unit}=arg0))
"""
            ytqb__mcth = types.Array(bodo.datetime64ns, 1, 'C')
        return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
            ytqb__mcth, extra_globals=qrc__mwq)
    return overload_add_datetime_interval_util


def _install_add_interval_overload():
    evd__aygg = [('years', add_interval_years, add_interval_years_util), (
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
    for unit, qilu__qdkgr, wma__zmliu in evd__aygg:
        yfyct__shhsm = create_add_interval_func_overload(unit)
        overload(qilu__qdkgr)(yfyct__shhsm)
        ywm__tafn = create_add_interval_util_overload(unit)
        overload(wma__zmliu)(ywm__tafn)


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
        irbgx__yqfw = 'def impl(arr):\n'
        irbgx__yqfw += (
            f'  return bodo.libs.bodosql_array_kernels.{fn_name}_util(arr)')
        tvvs__mgtfg = {}
        exec(irbgx__yqfw, {'bodo': bodo}, tvvs__mgtfg)
        return tvvs__mgtfg['impl']
    return overload_func


def create_dt_extract_fn_util_overload(fn_name):

    def overload_dt_extract_fn(arr):
        if fn_name in ('get_hour', 'get_minute', 'get_second',
            'get_microsecond', 'get_millisecond', 'get_nanosecond'):
            verify_time_or_datetime_arg_allow_tz(arr, fn_name, 'arr')
        else:
            verify_datetime_arg_allow_tz(arr, fn_name, 'arr')
        rpxmj__ghqnf = get_tz_if_exists(arr)
        xov__axe = ('bodo.utils.conversion.box_if_dt64' if rpxmj__ghqnf is
            None else '')
        oaiy__otxpt = 'microsecond // 1000' if not is_valid_time_arg(arr
            ) else 'millisecond'
        zxes__shic = {'get_year': f'{xov__axe}(arg0).year', 'get_quarter':
            f'{xov__axe}(arg0).quarter', 'get_month':
            f'{xov__axe}(arg0).month', 'get_week': f'{xov__axe}(arg0).week',
            'get_hour': f'{xov__axe}(arg0).hour', 'get_minute':
            f'{xov__axe}(arg0).minute', 'get_second':
            f'{xov__axe}(arg0).second', 'get_millisecond':
            f'{xov__axe}(arg0).{oaiy__otxpt}', 'get_microsecond':
            f'{xov__axe}(arg0).microsecond', 'get_nanosecond':
            f'{xov__axe}(arg0).nanosecond', 'dayofmonth':
            f'{xov__axe}(arg0).day', 'dayofweek':
            f'({xov__axe}(arg0).dayofweek + 1) % 7', 'dayofweekiso':
            f'{xov__axe}(arg0).dayofweek + 1', 'dayofyear':
            f'{xov__axe}(arg0).dayofyear'}
        nvgd__lbsd = ['arr']
        sfb__wbsib = [arr]
        zoloe__nlb = [True]
        jmi__ryjz = f'res[i] = {zxes__shic[fn_name]}'
        ytqb__mcth = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
            ytqb__mcth)
    return overload_dt_extract_fn


def _install_dt_extract_fn_overload():
    evd__aygg = [('get_year', get_year, get_year_util), ('get_quarter',
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
    for fn_name, qilu__qdkgr, wma__zmliu in evd__aygg:
        yfyct__shhsm = create_dt_extract_fn_overload(fn_name)
        overload(qilu__qdkgr)(yfyct__shhsm)
        ywm__tafn = create_dt_extract_fn_util_overload(fn_name)
        overload(wma__zmliu)(ywm__tafn)


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
    npsh__ofhmk = 1
    if year1 < year0:
        year0, year1 = year1, year0
        npsh__ofhmk = -1
    sjj__bzuwl = 0
    for iylzo__hfi in range(year0, year1):
        sjj__bzuwl += 52
        jrwzj__lujj = (iylzo__hfi + iylzo__hfi // 4 - iylzo__hfi // 100 + 
            iylzo__hfi // 400) % 7
        djqqr__vcuqq = (iylzo__hfi - 1 + (iylzo__hfi - 1) // 4 - (
            iylzo__hfi - 1) // 100 + (iylzo__hfi - 1) // 400) % 7
        if jrwzj__lujj == 4 or djqqr__vcuqq == 3:
            sjj__bzuwl += 1
    return npsh__ofhmk * sjj__bzuwl


def create_dt_diff_fn_overload(unit):

    def overload_func(arr0, arr1):
        args = [arr0, arr1]
        for lakyw__mqyf in range(len(args)):
            if isinstance(args[lakyw__mqyf], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.diff_{unit}', ['arr0',
                    'arr1'], lakyw__mqyf)
        irbgx__yqfw = 'def impl(arr0, arr1):\n'
        irbgx__yqfw += (
            f'  return bodo.libs.bodosql_array_kernels.diff_{unit}_util(arr0, arr1)'
            )
        tvvs__mgtfg = {}
        exec(irbgx__yqfw, {'bodo': bodo}, tvvs__mgtfg)
        return tvvs__mgtfg['impl']
    return overload_func


def create_dt_diff_fn_util_overload(unit):

    def overload_dt_diff_fn(arr0, arr1):
        verify_datetime_arg_allow_tz(arr0, 'diff_' + unit, 'arr0')
        verify_datetime_arg_allow_tz(arr1, 'diff_' + unit, 'arr1')
        rpxmj__ghqnf = get_tz_if_exists(arr0)
        if get_tz_if_exists(arr1) != rpxmj__ghqnf:
            raise_bodo_error(
                f'diff_{unit}: both arguments must have the same timezone')
        nvgd__lbsd = ['arr0', 'arr1']
        sfb__wbsib = [arr0, arr1]
        zoloe__nlb = [True] * 2
        qrc__mwq = None
        urtr__hbph = {'yr_diff': 'arg1.year - arg0.year', 'qu_diff':
            'arg1.quarter - arg0.quarter', 'mo_diff':
            'arg1.month - arg0.month', 'y0, w0, _': 'arg0.isocalendar()',
            'y1, w1, _': 'arg1.isocalendar()', 'iso_yr_diff':
            'bodo.libs.bodosql_array_kernels.get_iso_weeks_between_years(y0, y1)'
            , 'wk_diff': 'w1 - w0', 'da_diff':
            '(pd.Timestamp(arg1.year, arg1.month, arg1.day) - pd.Timestamp(arg0.year, arg0.month, arg0.day)).days'
            , 'ns_diff': 'arg1.value - arg0.value'}
        rura__wut = {'year': ['yr_diff'], 'quarter': ['yr_diff', 'qu_diff'],
            'month': ['yr_diff', 'mo_diff'], 'week': ['y0, w0, _',
            'y1, w1, _', 'iso_yr_diff', 'wk_diff'], 'day': ['da_diff'],
            'nanosecond': ['ns_diff']}
        jmi__ryjz = ''
        if rpxmj__ghqnf == None:
            jmi__ryjz += 'arg0 = bodo.utils.conversion.box_if_dt64(arg0)\n'
            jmi__ryjz += 'arg1 = bodo.utils.conversion.box_if_dt64(arg1)\n'
        for fhpyd__ybmy in rura__wut.get(unit, []):
            jmi__ryjz += f'{fhpyd__ybmy} = {urtr__hbph[fhpyd__ybmy]}\n'
        if unit == 'nanosecond':
            ytqb__mcth = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        else:
            ytqb__mcth = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
        if unit == 'year':
            jmi__ryjz += 'res[i] = yr_diff'
        elif unit == 'quarter':
            jmi__ryjz += 'res[i] = 4 * yr_diff + qu_diff'
        elif unit == 'month':
            jmi__ryjz += 'res[i] = 12 * yr_diff + mo_diff'
        elif unit == 'week':
            jmi__ryjz += 'res[i] = iso_yr_diff + wk_diff'
        elif unit == 'day':
            jmi__ryjz += 'res[i] = da_diff'
        elif unit == 'nanosecond':
            jmi__ryjz += 'res[i] = ns_diff'
        else:
            if unit == 'hour':
                ewj__lovz = 3600000000000
            if unit == 'minute':
                ewj__lovz = 60000000000
            if unit == 'second':
                ewj__lovz = 1000000000
            if unit == 'microsecond':
                ewj__lovz = 1000
            jmi__ryjz += f"""res[i] = np.floor_divide((arg1.value), ({ewj__lovz})) - np.floor_divide((arg0.value), ({ewj__lovz}))
"""
        return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
            ytqb__mcth, extra_globals=qrc__mwq)
    return overload_dt_diff_fn


def _install_dt_diff_fn_overload():
    evd__aygg = [('day', diff_day, diff_day_util), ('hour', diff_hour,
        diff_hour_util), ('microsecond', diff_microsecond,
        diff_microsecond_util), ('minute', diff_minute, diff_minute_util),
        ('month', diff_month, diff_month_util), ('nanosecond',
        diff_nanosecond, diff_nanosecond_util), ('quarter', diff_quarter,
        diff_quarter), ('second', diff_second, diff_second_util), ('week',
        diff_week, diff_week_util), ('year', diff_year, diff_year_util)]
    for unit, qilu__qdkgr, wma__zmliu in evd__aygg:
        yfyct__shhsm = create_dt_diff_fn_overload(unit)
        overload(qilu__qdkgr)(yfyct__shhsm)
        ywm__tafn = create_dt_diff_fn_util_overload(unit)
        overload(wma__zmliu)(ywm__tafn)


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
    yfns__qlrz = get_tz_if_exists(ts_arg)
    nvgd__lbsd = ['date_or_time_part', 'ts_arg']
    sfb__wbsib = [date_or_time_part, ts_arg]
    zoloe__nlb = [True, True]
    xov__axe = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(ts_arg, True) else '')
    xgqyv__myoy = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(ts_arg, True) else '')
    jmi__ryjz = """part_str = bodo.libs.bodosql_array_kernels.standardize_snowflake_date_time_part(arg0)
"""
    if yfns__qlrz is None:
        jmi__ryjz += f'arg1 = {xov__axe}(arg1)\n'
    jmi__ryjz += "if part_str == 'quarter':\n"
    jmi__ryjz += """    out_val = pd.Timestamp(year=arg1.year, month= (3*(arg1.quarter - 1)) + 1, day=1, tz=tz_literal)
"""
    jmi__ryjz += "elif part_str == 'year':\n"
    jmi__ryjz += (
        '    out_val = pd.Timestamp(year=arg1.year, month=1, day=1, tz=tz_literal)\n'
        )
    jmi__ryjz += "elif part_str == 'month':\n"
    jmi__ryjz += """    out_val = pd.Timestamp(year=arg1.year, month=arg1.month, day=1, tz=tz_literal)
"""
    jmi__ryjz += "elif part_str == 'day':\n"
    jmi__ryjz += '    out_val = arg1.normalize()\n'
    jmi__ryjz += "elif part_str == 'week':\n"
    jmi__ryjz += '    if arg1.dayofweek == 0:\n'
    jmi__ryjz += '        out_val = arg1.normalize()\n'
    jmi__ryjz += '    else:\n'
    jmi__ryjz += (
        '        out_val = arg1.normalize() - pd.tseries.offsets.Week(n=1, weekday=0)\n'
        )
    jmi__ryjz += "elif part_str == 'hour':\n"
    jmi__ryjz += "    out_val = arg1.floor('H')\n"
    jmi__ryjz += "elif part_str == 'minute':\n"
    jmi__ryjz += "    out_val = arg1.floor('min')\n"
    jmi__ryjz += "elif part_str == 'second':\n"
    jmi__ryjz += "    out_val = arg1.floor('S')\n"
    jmi__ryjz += "elif part_str == 'millisecond':\n"
    jmi__ryjz += "    out_val = arg1.floor('ms')\n"
    jmi__ryjz += "elif part_str == 'microsecond':\n"
    jmi__ryjz += "    out_val = arg1.floor('us')\n"
    jmi__ryjz += "elif part_str == 'nanosecond':\n"
    jmi__ryjz += '    out_val = arg1\n'
    jmi__ryjz += 'else:\n'
    jmi__ryjz += (
        "    raise ValueError('Invalid date or time part for DATE_TRUNC')\n")
    if yfns__qlrz is None:
        jmi__ryjz += f'res[i] = {xgqyv__myoy}(out_val)\n'
    else:
        jmi__ryjz += f'res[i] = out_val\n'
    if yfns__qlrz is None:
        ytqb__mcth = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        ytqb__mcth = bodo.DatetimeArrayType(yfns__qlrz)
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth, extra_globals={'tz_literal': yfns__qlrz})


@numba.generated_jit(nopython=True)
def dayname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'dayname', 'arr')
    rpxmj__ghqnf = get_tz_if_exists(arr)
    xov__axe = ('bodo.utils.conversion.box_if_dt64' if rpxmj__ghqnf is None
         else '')
    nvgd__lbsd = ['arr']
    sfb__wbsib = [arr]
    zoloe__nlb = [True]
    jmi__ryjz = f'res[i] = {xov__axe}(arg0).day_name()'
    ytqb__mcth = bodo.string_array_type
    jyo__qvoo = ['V']
    abz__ape = pd.array(['Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday'])
    qrc__mwq = {'day_of_week_dict_arr': abz__ape}
    iuz__ebj = 'dict_res = day_of_week_dict_arr'
    fxr__qqog = f'res[i] = {xov__axe}(arg0).dayofweek'
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth, synthesize_dict_if_vector=jyo__qvoo,
        synthesize_dict_setup_text=iuz__ebj, synthesize_dict_scalar_text=
        fxr__qqog, extra_globals=qrc__mwq, synthesize_dict_global=True,
        synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def int_to_days_util(arr):
    verify_int_arg(arr, 'int_to_days', 'arr')
    xgqyv__myoy = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    nvgd__lbsd = ['arr']
    sfb__wbsib = [arr]
    zoloe__nlb = [True]
    jmi__ryjz = f'res[i] = {xgqyv__myoy}(pd.Timedelta(days=arg0))'
    ytqb__mcth = np.dtype('timedelta64[ns]')
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth)


@numba.generated_jit(nopython=True)
def last_day_util(arr):
    verify_datetime_arg_allow_tz(arr, 'LAST_DAY', 'arr')
    rmw__kvvp = get_tz_if_exists(arr)
    xov__axe = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    xgqyv__myoy = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    nvgd__lbsd = ['arr']
    sfb__wbsib = [arr]
    zoloe__nlb = [True]
    if rmw__kvvp is None:
        jmi__ryjz = (
            f'res[i] = {xgqyv__myoy}({xov__axe}(arg0) + pd.tseries.offsets.MonthEnd(n=0, normalize=True))'
            )
        ytqb__mcth = np.dtype('datetime64[ns]')
    else:
        jmi__ryjz = 'y = arg0.year\n'
        jmi__ryjz += 'm = arg0.month\n'
        jmi__ryjz += (
            'd = bodo.hiframes.pd_offsets_ext.get_days_in_month(y, m)\n')
        jmi__ryjz += (
            f'res[i] = pd.Timestamp(year=y, month=m, day=d, tz={repr(rmw__kvvp)})\n'
            )
        ytqb__mcth = bodo.DatetimeArrayType(rmw__kvvp)
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth)


@numba.generated_jit(nopython=True)
def makedate_util(year, day):
    verify_int_arg(year, 'MAKEDATE', 'year')
    verify_int_arg(day, 'MAKEDATE', 'day')
    xgqyv__myoy = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(year, True) or bodo.utils.utils.
        is_array_typ(day, True) else '')
    nvgd__lbsd = ['year', 'day']
    sfb__wbsib = [year, day]
    zoloe__nlb = [True] * 2
    jmi__ryjz = (
        f'res[i] = {xgqyv__myoy}(pd.Timestamp(year=arg0, month=1, day=1) + pd.Timedelta(days=arg1-1))'
        )
    ytqb__mcth = np.dtype('datetime64[ns]')
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth)


@numba.generated_jit(nopython=True)
def monthname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'monthname', 'arr')
    rpxmj__ghqnf = get_tz_if_exists(arr)
    xov__axe = ('bodo.utils.conversion.box_if_dt64' if rpxmj__ghqnf is None
         else '')
    nvgd__lbsd = ['arr']
    sfb__wbsib = [arr]
    zoloe__nlb = [True]
    jmi__ryjz = f'res[i] = {xov__axe}(arg0).month_name()'
    ytqb__mcth = bodo.string_array_type
    jyo__qvoo = ['V']
    kmdn__tui = pd.array(['January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October', 'November',
        'December'])
    qrc__mwq = {'month_names_dict_arr': kmdn__tui}
    iuz__ebj = 'dict_res = month_names_dict_arr'
    fxr__qqog = f'res[i] = {xov__axe}(arg0).month - 1'
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth, synthesize_dict_if_vector=jyo__qvoo,
        synthesize_dict_setup_text=iuz__ebj, synthesize_dict_scalar_text=
        fxr__qqog, extra_globals=qrc__mwq, synthesize_dict_global=True,
        synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def next_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'NEXT_DAY', 'arr0')
    verify_string_arg(arr1, 'NEXT_DAY', 'arr1')
    dnsqi__hrksb = is_valid_tz_aware_datetime_arg(arr0)
    xgqyv__myoy = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    nvgd__lbsd = ['arr0', 'arr1']
    sfb__wbsib = [arr0, arr1]
    zoloe__nlb = [True] * 2
    zwz__vdvab = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    jmi__ryjz = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if dnsqi__hrksb:
        ipr__xebd = 'arg0'
    else:
        ipr__xebd = 'bodo.utils.conversion.box_if_dt64(arg0)'
    jmi__ryjz += f"""new_timestamp = {ipr__xebd}.normalize() + pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    jmi__ryjz += f'res[i] = {xgqyv__myoy}(new_timestamp.tz_localize(None))\n'
    ytqb__mcth = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth, prefix_code=zwz__vdvab)


@numba.generated_jit(nopython=True)
def previous_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'PREVIOUS_DAY', 'arr0')
    verify_string_arg(arr1, 'PREVIOUS_DAY', 'arr1')
    dnsqi__hrksb = is_valid_tz_aware_datetime_arg(arr0)
    xgqyv__myoy = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    nvgd__lbsd = ['arr0', 'arr1']
    sfb__wbsib = [arr0, arr1]
    zoloe__nlb = [True] * 2
    zwz__vdvab = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    jmi__ryjz = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if dnsqi__hrksb:
        ipr__xebd = 'arg0'
    else:
        ipr__xebd = 'bodo.utils.conversion.box_if_dt64(arg0)'
    jmi__ryjz += f"""new_timestamp = {ipr__xebd}.normalize() - pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    jmi__ryjz += f'res[i] = {xgqyv__myoy}(new_timestamp.tz_localize(None))\n'
    ytqb__mcth = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth, prefix_code=zwz__vdvab)


@numba.generated_jit(nopython=True)
def second_timestamp_util(arr):
    verify_int_arg(arr, 'second_timestamp', 'arr')
    xgqyv__myoy = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    nvgd__lbsd = ['arr']
    sfb__wbsib = [arr]
    zoloe__nlb = [True]
    jmi__ryjz = f"res[i] = {xgqyv__myoy}(pd.Timestamp(arg0, unit='s'))"
    ytqb__mcth = np.dtype('datetime64[ns]')
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth)


@numba.generated_jit(nopython=True)
def weekday_util(arr):
    verify_datetime_arg(arr, 'WEEKDAY', 'arr')
    nvgd__lbsd = ['arr']
    sfb__wbsib = [arr]
    zoloe__nlb = [True]
    xov__axe = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    jmi__ryjz = f'dt = {xov__axe}(arg0)\n'
    jmi__ryjz += (
        'res[i] = bodo.hiframes.pd_timestamp_ext.get_day_of_week(dt.year, dt.month, dt.day)'
        )
    ytqb__mcth = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth)


@numba.generated_jit(nopython=True)
def yearofweekiso_util(arr):
    verify_datetime_arg_allow_tz(arr, 'YEAROFWEEKISO', 'arr')
    nvgd__lbsd = ['arr']
    sfb__wbsib = [arr]
    zoloe__nlb = [True]
    xov__axe = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    jmi__ryjz = f'dt = {xov__axe}(arg0)\n'
    jmi__ryjz += 'res[i] = dt.isocalendar()[0]'
    ytqb__mcth = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth)


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
    nvgd__lbsd = ['arr']
    sfb__wbsib = [arr]
    zoloe__nlb = [True]
    zwz__vdvab = 'unix_days_to_year_zero = 719528\n'
    zwz__vdvab += 'nanoseconds_divisor = 86400000000000\n'
    ytqb__mcth = bodo.IntegerArrayType(types.int64)
    iuo__mjjde = bodo.utils.utils.is_array_typ(arr, False)
    if iuo__mjjde:
        jmi__ryjz = (
            '  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        jmi__ryjz = '  in_value = arg0.value\n'
    jmi__ryjz += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_days_to_year_zero\n'
        )
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth, prefix_code=zwz__vdvab)


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
    nvgd__lbsd = ['arr']
    sfb__wbsib = [arr]
    zoloe__nlb = [True]
    iuo__mjjde = bodo.utils.utils.is_array_typ(arr, False)
    if iuo__mjjde:
        ytqb__mcth = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        ytqb__mcth = bodo.pd_timestamp_tz_naive_type
    zwz__vdvab = 'unix_days_to_year_zero = 719528\n'
    zwz__vdvab += 'nanoseconds_divisor = 86400000000000\n'
    jmi__ryjz = (
        '  nanoseconds = (arg0 - unix_days_to_year_zero) * nanoseconds_divisor\n'
        )
    if iuo__mjjde:
        jmi__ryjz += (
            '  res[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(nanoseconds)\n'
            )
    else:
        jmi__ryjz += '  res[i] = pd.Timestamp(nanoseconds)\n'
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth, prefix_code=zwz__vdvab)


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
    rroy__szin = get_tz_if_exists(arr)
    nvgd__lbsd = ['arr']
    sfb__wbsib = [arr]
    zoloe__nlb = [True]
    zwz__vdvab = 'unix_seconds_to_year_zero = 62167219200\n'
    zwz__vdvab += 'nanoseconds_divisor = 1000000000\n'
    ytqb__mcth = bodo.IntegerArrayType(types.int64)
    iuo__mjjde = bodo.utils.utils.is_array_typ(arr, False)
    if iuo__mjjde and not rroy__szin:
        jmi__ryjz = (
            f'  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        jmi__ryjz = f'  in_value = arg0.value\n'
    jmi__ryjz += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_seconds_to_year_zero\n'
        )
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth, prefix_code=zwz__vdvab)


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
    rroy__szin = get_tz_if_exists(tz_arg)
    nvgd__lbsd = ['tz_arg', 'interval_arg']
    sfb__wbsib = [tz_arg, interval_arg]
    zoloe__nlb = [True, True]
    if rroy__szin is not None:
        ytqb__mcth = bodo.DatetimeArrayType(rroy__szin)
    else:
        ytqb__mcth = bodo.datetime64ns
    if interval_arg == bodo.date_offset_type:
        jmi__ryjz = """  timedelta = bodo.libs.pd_datetime_arr_ext.convert_months_offset_to_days(arg0.year, arg0.month, arg0.day, ((arg1._years * 12) + arg1._months) * arg1.n)
"""
    else:
        jmi__ryjz = '  timedelta = arg1\n'
    jmi__ryjz += """  timedelta = bodo.hiframes.pd_offsets_ext.update_timedelta_with_transition(arg0, timedelta)
"""
    jmi__ryjz += '  res[i] = arg0 + timedelta\n'
    return gen_vectorized(nvgd__lbsd, sfb__wbsib, zoloe__nlb, jmi__ryjz,
        ytqb__mcth)
