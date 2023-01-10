"""
Implements a number of array kernels that handling casting functions for BodoSQL
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload, register_jitable
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import get_literal_value, get_overload_const_bool, is_literal_type, is_overload_none, raise_bodo_error


@numba.generated_jit(nopython=True)
def try_to_boolean(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_boolean',
            ['arr'], 0)

    def impl(arr):
        return to_boolean_util(arr, numba.literally(True))
    return impl


@numba.generated_jit(nopython=True)
def to_boolean(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_boolean',
            ['arr'], 0)

    def impl(arr):
        return to_boolean_util(arr, numba.literally(False))
    return impl


@numba.generated_jit(nopython=True)
def to_boolean_util(arr, _try=False):
    verify_string_numeric_arg(arr, 'TO_BOOLEAN', 'arr')
    vfg__vhjef = is_valid_string_arg(arr)
    sweoz__aaf = is_valid_float_arg(arr)
    _try = get_overload_const_bool(_try)
    if _try:
        ectmi__zfye = 'bodo.libs.array_kernels.setna(res, i)\n'
    else:
        if vfg__vhjef:
            htb__pon = (
                "string must be one of {'true', 't', 'yes', 'y', 'on', '1'} or {'false', 'f', 'no', 'n', 'off', '0'}"
                )
        else:
            htb__pon = 'value must be a valid numeric expression'
        ectmi__zfye = (
            f'raise ValueError("invalid value for boolean conversion: {htb__pon}")'
            )
    gsm__plh = ['arr', '_try']
    ryn__uevn = [arr, _try]
    rno__fhh = [True, False]
    umft__ymgj = None
    if vfg__vhjef:
        umft__ymgj = "true_vals = {'true', 't', 'yes', 'y', 'on', '1'}\n"
        umft__ymgj += "false_vals = {'false', 'f', 'no', 'n', 'off', '0'}"
    if vfg__vhjef:
        dotti__wjk = 's = arg0.lower()\n'
        dotti__wjk += f'is_true_val = s in true_vals\n'
        dotti__wjk += f'res[i] = is_true_val\n'
        dotti__wjk += f'if not (is_true_val or s in false_vals):\n'
        dotti__wjk += f'  {ectmi__zfye}\n'
    elif sweoz__aaf:
        dotti__wjk = 'if np.isinf(arg0) or np.isnan(arg0):\n'
        dotti__wjk += f'  {ectmi__zfye}\n'
        dotti__wjk += 'else:\n'
        dotti__wjk += f'  res[i] = bool(arg0)\n'
    else:
        dotti__wjk = f'res[i] = bool(arg0)'
    asfx__qgd = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(gsm__plh, ryn__uevn, rno__fhh, dotti__wjk,
        asfx__qgd, prefix_code=umft__ymgj)


@numba.generated_jit(nopython=True)
def try_to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for jsh__nsw in range(2):
        if isinstance(args[jsh__nsw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.try_to_date'
                , ['conversionVal', 'optionalConversionFormatString'], jsh__nsw
                )

    def impl(conversionVal, optionalConversionFormatString):
        return to_date_util(conversionVal, optionalConversionFormatString,
            numba.literally(False))
    return impl


@numba.generated_jit(nopython=True)
def to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for jsh__nsw in range(2):
        if isinstance(args[jsh__nsw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.to_date',
                ['conversionVal', 'optionalConversionFormatString'], jsh__nsw)

    def impl(conversionVal, optionalConversionFormatString):
        return to_date_util(conversionVal, optionalConversionFormatString,
            numba.literally(True))
    return impl


@numba.generated_jit(nopython=True)
def to_char(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_char', [
            'arr'], 0)

    def impl(arr):
        return to_char_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def to_char_util(arr):
    gsm__plh = ['arr']
    ryn__uevn = [arr]
    rno__fhh = [True]
    if is_valid_binary_arg(arr):
        dotti__wjk = 'with bodo.objmode(r=bodo.string_type):\n'
        dotti__wjk += '  r = arg0.hex()\n'
        dotti__wjk += 'res[i] = r'
    elif isinstance(arr, bodo.TimeType) or bodo.utils.utils.is_array_typ(arr
        ) and isinstance(arr.dtype, bodo.TimeType):
        dotti__wjk = (
            "h_str = str(arg0.hour) if arg0.hour > 10 else '0' + str(arg0.hour)\n"
            )
        dotti__wjk += (
            "m_str = str(arg0.minute) if arg0.minute > 10 else '0' + str(arg0.minute)\n"
            )
        dotti__wjk += (
            "s_str = str(arg0.second) if arg0.second > 10 else '0' + str(arg0.second)\n"
            )
        dotti__wjk += """ms_str = str(arg0.millisecond) if arg0.millisecond > 100 else ('0' + str(arg0.millisecond) if arg0.millisecond > 10 else '00' + str(arg0.millisecond))
"""
        dotti__wjk += """us_str = str(arg0.microsecond) if arg0.microsecond > 100 else ('0' + str(arg0.microsecond) if arg0.microsecond > 10 else '00' + str(arg0.microsecond))
"""
        dotti__wjk += """ns_str = str(arg0.nanosecond) if arg0.nanosecond > 100 else ('0' + str(arg0.nanosecond) if arg0.nanosecond > 10 else '00' + str(arg0.nanosecond))
"""
        dotti__wjk += "part_str = h_str + ':' + m_str + ':' + s_str\n"
        dotti__wjk += 'if arg0.nanosecond > 0:\n'
        dotti__wjk += (
            "  part_str = part_str + '.' + ms_str + us_str + ns_str\n")
        dotti__wjk += 'elif arg0.microsecond > 0:\n'
        dotti__wjk += "  part_str = part_str + '.' + ms_str + us_str\n"
        dotti__wjk += 'elif arg0.millisecond > 0:\n'
        dotti__wjk += "  part_str = part_str + '.' + ms_str\n"
        dotti__wjk += 'res[i] = part_str'
    elif is_valid_timedelta_arg(arr):
        dotti__wjk = (
            'v = bodo.utils.conversion.unbox_if_tz_naive_timestamp(arg0)\n')
        dotti__wjk += 'with bodo.objmode(r=bodo.string_type):\n'
        dotti__wjk += '    r = str(v)\n'
        dotti__wjk += 'res[i] = r'
    elif is_valid_datetime_or_date_arg(arr):
        if is_valid_tz_aware_datetime_arg(arr):
            dotti__wjk = "tz_raw = arg0.strftime('%z')\n"
            dotti__wjk += 'tz = tz_raw[:3] + ":" + tz_raw[3:]\n'
            dotti__wjk += "res[i] = arg0.isoformat(' ') + tz\n"
        else:
            dotti__wjk = "res[i] = pd.Timestamp(arg0).isoformat(' ')\n"
    elif is_valid_float_arg(arr):
        dotti__wjk = 'if np.isinf(arg0):\n'
        dotti__wjk += "  res[i] = 'inf' if arg0 > 0 else '-inf'\n"
        dotti__wjk += 'elif np.isnan(arg0):\n'
        dotti__wjk += "  res[i] = 'NaN'\n"
        dotti__wjk += 'else:\n'
        dotti__wjk += '  res[i] = str(arg0)'
    elif is_valid_boolean_arg(arr):
        dotti__wjk = "res[i] = 'true' if arg0 else 'false'"
    else:
        ixkg__ksh = {(8): np.int8, (16): np.int16, (32): np.int32, (64): np
            .int64}
        if is_valid_int_arg(arr):
            if hasattr(arr, 'dtype'):
                pul__hwjaf = arr.dtype.bitwidth
            else:
                pul__hwjaf = arr.bitwidth
            dotti__wjk = f'if arg0 == {np.iinfo(ixkg__ksh[pul__hwjaf]).min}:\n'
            dotti__wjk += (
                f"  res[i] = '{np.iinfo(ixkg__ksh[pul__hwjaf]).min}'\n")
            dotti__wjk += 'else:\n'
            dotti__wjk += '  res[i] = str(arg0)'
        else:
            dotti__wjk = 'res[i] = str(arg0)'
    asfx__qgd = bodo.string_array_type
    return gen_vectorized(gsm__plh, ryn__uevn, rno__fhh, dotti__wjk, asfx__qgd)


@register_jitable
def convert_sql_date_format_str_to_py_format(val):
    raise RuntimeError(
        'Converting to date values with format strings not currently supported'
        )


@numba.generated_jit(nopython=True)
def int_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            xjnvf__pdlsq = pd.to_datetime(val, unit='s')
        elif val < 31536000000000:
            xjnvf__pdlsq = pd.to_datetime(val, unit='ms')
        elif val < 31536000000000000:
            xjnvf__pdlsq = pd.to_datetime(val, unit='us')
        else:
            xjnvf__pdlsq = pd.to_datetime(val, unit='ns')
        return xjnvf__pdlsq
    return impl


@numba.generated_jit(nopython=True)
def float_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            xjnvf__pdlsq = pd.Timestamp(val, unit='s')
        elif val < 31536000000000:
            xjnvf__pdlsq = pd.Timestamp(val, unit='ms')
        elif val < 31536000000000000:
            xjnvf__pdlsq = pd.Timestamp(val, unit='us')
        else:
            xjnvf__pdlsq = pd.Timestamp(val, unit='ns')
        return xjnvf__pdlsq
    return impl


@register_jitable
def pd_to_datetime_error_checked(val, dayfirst=False, yearfirst=False, utc=
    None, format=None, exact=True, unit=None, infer_datetime_format=False,
    origin='unix', cache=True):
    if val is not None:
        yhb__fnx = val.split(' ')[0]
        if len(yhb__fnx) < 10:
            return False, None
        else:
            hybt__obno = yhb__fnx.count('/') in [0, 2]
            fiv__atb = yhb__fnx.count('-') in [0, 2]
            if not (hybt__obno and fiv__atb):
                return False, None
    with numba.objmode(ret_val='pd_timestamp_tz_naive_type', success_flag=
        'bool_'):
        success_flag = True
        ret_val = pd.Timestamp(0)
        mex__uyh = pd.to_datetime(val, errors='coerce', dayfirst=dayfirst,
            yearfirst=yearfirst, utc=utc, format=format, exact=exact, unit=
            unit, infer_datetime_format=infer_datetime_format, origin=
            origin, cache=cache)
        if pd.isna(mex__uyh):
            success_flag = False
        else:
            ret_val = mex__uyh
    return success_flag, ret_val


@numba.generated_jit(nopython=True)
def to_date_util(conversionVal, optionalConversionFormatString, errorOnFail,
    _keep_time=False):
    errorOnFail = get_overload_const_bool(errorOnFail)
    _keep_time = get_overload_const_bool(_keep_time)
    if errorOnFail:
        bmk__lhe = (
            "raise ValueError('Invalid input while converting to date value')")
    else:
        bmk__lhe = 'bodo.libs.array_kernels.setna(res, i)'
    if _keep_time:
        eziy__weuvx = ''
    else:
        eziy__weuvx = '.normalize()'
    verify_string_arg(optionalConversionFormatString,
        'TO_DATE and TRY_TO_DATE', 'optionalConversionFormatString')
    rtcte__lhc = bodo.utils.utils.is_array_typ(conversionVal, True
        ) or bodo.utils.utils.is_array_typ(optionalConversionFormatString, True
        )
    eytrg__nlt = 'unbox_if_tz_naive_timestamp' if rtcte__lhc else ''
    if not is_overload_none(optionalConversionFormatString):
        verify_string_arg(conversionVal, 'TO_DATE and TRY_TO_DATE',
            'optionalConversionFormatString')
        dotti__wjk = (
            'py_format_str = convert_sql_date_format_str_to_py_format(arg1)\n')
        dotti__wjk += """was_successful, tmp_val = pd_to_datetime_error_checked(arg0, format=py_format_str)
"""
        dotti__wjk += 'if not was_successful:\n'
        dotti__wjk += f'  {bmk__lhe}\n'
        dotti__wjk += 'else:\n'
        dotti__wjk += f'  res[i] = {eytrg__nlt}(tmp_val{eziy__weuvx})\n'
    elif is_valid_string_arg(conversionVal):
        """
        If no format string is specified, snowflake will use attempt to parse the string according to these date formats:
        https://docs.snowflake.com/en/user-guide/date-time-input-output.html#date-formats. All of the examples listed are
        handled by pd.to_datetime() in Bodo jit code.

        It will also check if the string is convertable to int, IE '12345' or '-4321'"""
        dotti__wjk = 'arg0 = str(arg0)\n'
        dotti__wjk += """if (arg0.isnumeric() or (len(arg0) > 1 and arg0[0] == '-' and arg0[1:].isnumeric())):
"""
        dotti__wjk += (
            f'   res[i] = {eytrg__nlt}(int_to_datetime(np.int64(arg0)){eziy__weuvx})\n'
            )
        dotti__wjk += 'else:\n'
        dotti__wjk += (
            '   was_successful, tmp_val = pd_to_datetime_error_checked(arg0)\n'
            )
        dotti__wjk += '   if not was_successful:\n'
        dotti__wjk += f'      {bmk__lhe}\n'
        dotti__wjk += '   else:\n'
        dotti__wjk += f'      res[i] = {eytrg__nlt}(tmp_val{eziy__weuvx})\n'
    elif is_valid_int_arg(conversionVal):
        dotti__wjk = (
            f'res[i] = {eytrg__nlt}(int_to_datetime(arg0){eziy__weuvx})\n')
    elif is_valid_float_arg(conversionVal):
        dotti__wjk = (
            f'res[i] = {eytrg__nlt}(float_to_datetime(arg0){eziy__weuvx})\n')
    elif is_valid_datetime_or_date_arg(conversionVal):
        dotti__wjk = (
            f'res[i] = {eytrg__nlt}(pd.Timestamp(arg0){eziy__weuvx})\n')
    elif is_valid_tz_aware_datetime_arg(conversionVal):
        dotti__wjk = f'res[i] = arg0{eziy__weuvx}\n'
    else:
        raise raise_bodo_error(
            f'Internal error: unsupported type passed to to_date_util for argument conversionVal: {conversionVal}'
            )
    gsm__plh = ['conversionVal', 'optionalConversionFormatString',
        'errorOnFail', '_keep_time']
    ryn__uevn = [conversionVal, optionalConversionFormatString, errorOnFail,
        _keep_time]
    rno__fhh = [True, False, False, False]
    if isinstance(conversionVal, bodo.DatetimeArrayType) or isinstance(
        conversionVal, bodo.PandasTimestampType
        ) and conversionVal.tz is not None:
        asfx__qgd = bodo.DatetimeArrayType(conversionVal.tz)
    else:
        asfx__qgd = types.Array(bodo.datetime64ns, 1, 'C')
    rub__rzcy = {'pd_to_datetime_error_checked':
        pd_to_datetime_error_checked, 'int_to_datetime': int_to_datetime,
        'float_to_datetime': float_to_datetime,
        'convert_sql_date_format_str_to_py_format':
        convert_sql_date_format_str_to_py_format,
        'unbox_if_tz_naive_timestamp': bodo.utils.conversion.
        unbox_if_tz_naive_timestamp}
    return gen_vectorized(gsm__plh, ryn__uevn, rno__fhh, dotti__wjk,
        asfx__qgd, extra_globals=rub__rzcy)


def cast_tz_naive_to_tz_aware(arr, tz):
    pass


@overload(cast_tz_naive_to_tz_aware, no_unliteral=True)
def overload_cast_tz_naive_to_tz_aware(arr, tz):
    if not is_literal_type(tz):
        raise_bodo_error(
            "cast_tz_naive_to_tz_aware(): 'tz' must be a literal value")
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.cast_tz_naive_to_tz_aware', [
            'arr', 'tz'], 0)

    def impl(arr, tz):
        return cast_tz_naive_to_tz_aware_util(arr, tz)
    return impl


def cast_tz_naive_to_tz_aware_util(arr, tz):
    pass


@overload(cast_tz_naive_to_tz_aware_util, no_unliteral=True)
def overload_cast_tz_naive_to_tz_aware_util(arr, tz):
    if not is_literal_type(tz):
        raise_bodo_error(
            "cast_tz_naive_to_tz_aware(): 'tz' must be a literal value")
    verify_datetime_arg(arr, 'cast_tz_naive_to_tz_aware', 'arr')
    gsm__plh = ['arr', 'tz']
    ryn__uevn = [arr, tz]
    rno__fhh = [True, False]
    rkkf__iayzn = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr) else '')
    dotti__wjk = f'res[i] = {rkkf__iayzn}(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    asfx__qgd = bodo.DatetimeArrayType(tz)
    return gen_vectorized(gsm__plh, ryn__uevn, rno__fhh, dotti__wjk, asfx__qgd)


def cast_tz_aware_to_tz_naive(arr, normalize):
    pass


@overload(cast_tz_aware_to_tz_naive, no_unliteral=True)
def overload_cast_tz_aware_to_tz_naive(arr, normalize):
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            "cast_tz_aware_to_tz_naive(): 'normalize' must be a literal value")
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.cast_tz_aware_to_tz_naive', [
            'arr', 'normalize'], 0)

    def impl(arr, normalize):
        return cast_tz_aware_to_tz_naive_util(arr, normalize)
    return impl


def cast_tz_aware_to_tz_naive_util(arr, normalize):
    pass


@overload(cast_tz_aware_to_tz_naive_util, no_unliteral=True)
def overload_cast_tz_aware_to_tz_naive_util(arr, normalize):
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            "cast_tz_aware_to_tz_naive(): 'normalize' must be a literal value")
    normalize = get_overload_const_bool(normalize)
    verify_datetime_arg_require_tz(arr, 'cast_tz_aware_to_tz_naive', 'arr')
    gsm__plh = ['arr', 'normalize']
    ryn__uevn = [arr, normalize]
    rno__fhh = [True, False]
    eytrg__nlt = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr) else '')
    dotti__wjk = ''
    if normalize:
        dotti__wjk += (
            'ts = pd.Timestamp(year=arg0.year, month=arg0.month, day=arg0.day)\n'
            )
    else:
        dotti__wjk += 'ts = arg0.tz_localize(None)\n'
    dotti__wjk += f'res[i] = {eytrg__nlt}(ts)'
    asfx__qgd = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(gsm__plh, ryn__uevn, rno__fhh, dotti__wjk, asfx__qgd)


def cast_str_to_tz_aware(arr, tz):
    pass


@overload(cast_str_to_tz_aware, no_unliteral=True)
def overload_cast_str_to_tz_aware(arr, tz):
    if not is_literal_type(tz):
        raise_bodo_error("cast_str_to_tz_aware(): 'tz' must be a literal value"
            )
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.cast_str_to_tz_aware', ['arr',
            'tz'], 0)

    def impl(arr, tz):
        return cast_str_to_tz_aware_util(arr, tz)
    return impl


def cast_str_to_tz_aware_util(arr, tz):
    pass


@overload(cast_str_to_tz_aware_util, no_unliteral=True)
def overload_cast_str_to_tz_aware_util(arr, tz):
    if not is_literal_type(tz):
        raise_bodo_error("cast_str_to_tz_aware(): 'tz' must be a literal value"
            )
    verify_string_arg(arr, 'cast_str_to_tz_aware', 'arr')
    gsm__plh = ['arr', 'tz']
    ryn__uevn = [arr, tz]
    rno__fhh = [True, False]
    dotti__wjk = f'res[i] = pd.to_datetime(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    asfx__qgd = bodo.DatetimeArrayType(tz)
    return gen_vectorized(gsm__plh, ryn__uevn, rno__fhh, dotti__wjk, asfx__qgd)
