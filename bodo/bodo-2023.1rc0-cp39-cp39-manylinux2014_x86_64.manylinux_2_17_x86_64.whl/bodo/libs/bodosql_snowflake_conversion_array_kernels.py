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
    ztz__sncld = is_valid_string_arg(arr)
    axl__sisc = is_valid_float_arg(arr)
    _try = get_overload_const_bool(_try)
    if _try:
        immu__zmm = 'bodo.libs.array_kernels.setna(res, i)\n'
    else:
        if ztz__sncld:
            nuiae__vab = (
                "string must be one of {'true', 't', 'yes', 'y', 'on', '1'} or {'false', 'f', 'no', 'n', 'off', '0'}"
                )
        else:
            nuiae__vab = 'value must be a valid numeric expression'
        immu__zmm = (
            f'raise ValueError("invalid value for boolean conversion: {nuiae__vab}")'
            )
    fmx__hfqip = ['arr', '_try']
    kwff__ogbf = [arr, _try]
    fome__jclo = [True, False]
    cwzwz__zzuh = None
    if ztz__sncld:
        cwzwz__zzuh = "true_vals = {'true', 't', 'yes', 'y', 'on', '1'}\n"
        cwzwz__zzuh += "false_vals = {'false', 'f', 'no', 'n', 'off', '0'}"
    if ztz__sncld:
        ltu__lwej = 's = arg0.lower()\n'
        ltu__lwej += f'is_true_val = s in true_vals\n'
        ltu__lwej += f'res[i] = is_true_val\n'
        ltu__lwej += f'if not (is_true_val or s in false_vals):\n'
        ltu__lwej += f'  {immu__zmm}\n'
    elif axl__sisc:
        ltu__lwej = 'if np.isinf(arg0) or np.isnan(arg0):\n'
        ltu__lwej += f'  {immu__zmm}\n'
        ltu__lwej += 'else:\n'
        ltu__lwej += f'  res[i] = bool(arg0)\n'
    else:
        ltu__lwej = f'res[i] = bool(arg0)'
    gaxq__iuqip = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(fmx__hfqip, kwff__ogbf, fome__jclo, ltu__lwej,
        gaxq__iuqip, prefix_code=cwzwz__zzuh)


@numba.generated_jit(nopython=True)
def try_to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for hwtc__uuv in range(2):
        if isinstance(args[hwtc__uuv], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.try_to_date'
                , ['conversionVal', 'optionalConversionFormatString'],
                hwtc__uuv)

    def impl(conversionVal, optionalConversionFormatString):
        return to_date_util(conversionVal, optionalConversionFormatString,
            numba.literally(False))
    return impl


@numba.generated_jit(nopython=True)
def to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for hwtc__uuv in range(2):
        if isinstance(args[hwtc__uuv], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.to_date',
                ['conversionVal', 'optionalConversionFormatString'], hwtc__uuv)

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
    fmx__hfqip = ['arr']
    kwff__ogbf = [arr]
    fome__jclo = [True]
    if is_valid_binary_arg(arr):
        ltu__lwej = 'with bodo.objmode(r=bodo.string_type):\n'
        ltu__lwej += '  r = arg0.hex()\n'
        ltu__lwej += 'res[i] = r'
    elif isinstance(arr, bodo.TimeType) or bodo.utils.utils.is_array_typ(arr
        ) and isinstance(arr.dtype, bodo.TimeType):
        ltu__lwej = (
            "h_str = str(arg0.hour) if arg0.hour > 10 else '0' + str(arg0.hour)\n"
            )
        ltu__lwej += (
            "m_str = str(arg0.minute) if arg0.minute > 10 else '0' + str(arg0.minute)\n"
            )
        ltu__lwej += (
            "s_str = str(arg0.second) if arg0.second > 10 else '0' + str(arg0.second)\n"
            )
        ltu__lwej += """ms_str = str(arg0.millisecond) if arg0.millisecond > 100 else ('0' + str(arg0.millisecond) if arg0.millisecond > 10 else '00' + str(arg0.millisecond))
"""
        ltu__lwej += """us_str = str(arg0.microsecond) if arg0.microsecond > 100 else ('0' + str(arg0.microsecond) if arg0.microsecond > 10 else '00' + str(arg0.microsecond))
"""
        ltu__lwej += """ns_str = str(arg0.nanosecond) if arg0.nanosecond > 100 else ('0' + str(arg0.nanosecond) if arg0.nanosecond > 10 else '00' + str(arg0.nanosecond))
"""
        ltu__lwej += "part_str = h_str + ':' + m_str + ':' + s_str\n"
        ltu__lwej += 'if arg0.nanosecond > 0:\n'
        ltu__lwej += "  part_str = part_str + '.' + ms_str + us_str + ns_str\n"
        ltu__lwej += 'elif arg0.microsecond > 0:\n'
        ltu__lwej += "  part_str = part_str + '.' + ms_str + us_str\n"
        ltu__lwej += 'elif arg0.millisecond > 0:\n'
        ltu__lwej += "  part_str = part_str + '.' + ms_str\n"
        ltu__lwej += 'res[i] = part_str'
    elif is_valid_timedelta_arg(arr):
        ltu__lwej = (
            'v = bodo.utils.conversion.unbox_if_tz_naive_timestamp(arg0)\n')
        ltu__lwej += 'with bodo.objmode(r=bodo.string_type):\n'
        ltu__lwej += '    r = str(v)\n'
        ltu__lwej += 'res[i] = r'
    elif is_valid_datetime_or_date_arg(arr):
        if is_valid_tz_aware_datetime_arg(arr):
            ltu__lwej = "tz_raw = arg0.strftime('%z')\n"
            ltu__lwej += 'tz = tz_raw[:3] + ":" + tz_raw[3:]\n'
            ltu__lwej += "res[i] = arg0.isoformat(' ') + tz\n"
        else:
            ltu__lwej = "res[i] = pd.Timestamp(arg0).isoformat(' ')\n"
    elif is_valid_float_arg(arr):
        ltu__lwej = 'if np.isinf(arg0):\n'
        ltu__lwej += "  res[i] = 'inf' if arg0 > 0 else '-inf'\n"
        ltu__lwej += 'elif np.isnan(arg0):\n'
        ltu__lwej += "  res[i] = 'NaN'\n"
        ltu__lwej += 'else:\n'
        ltu__lwej += '  res[i] = str(arg0)'
    elif is_valid_boolean_arg(arr):
        ltu__lwej = "res[i] = 'true' if arg0 else 'false'"
    else:
        eks__lvjev = {(8): np.int8, (16): np.int16, (32): np.int32, (64):
            np.int64}
        if is_valid_int_arg(arr):
            if hasattr(arr, 'dtype'):
                mci__sooo = arr.dtype.bitwidth
            else:
                mci__sooo = arr.bitwidth
            ltu__lwej = f'if arg0 == {np.iinfo(eks__lvjev[mci__sooo]).min}:\n'
            ltu__lwej += (
                f"  res[i] = '{np.iinfo(eks__lvjev[mci__sooo]).min}'\n")
            ltu__lwej += 'else:\n'
            ltu__lwej += '  res[i] = str(arg0)'
        else:
            ltu__lwej = 'res[i] = str(arg0)'
    gaxq__iuqip = bodo.string_array_type
    return gen_vectorized(fmx__hfqip, kwff__ogbf, fome__jclo, ltu__lwej,
        gaxq__iuqip)


@register_jitable
def convert_sql_date_format_str_to_py_format(val):
    raise RuntimeError(
        'Converting to date values with format strings not currently supported'
        )


@numba.generated_jit(nopython=True)
def int_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            wty__pwjzu = pd.to_datetime(val, unit='s')
        elif val < 31536000000000:
            wty__pwjzu = pd.to_datetime(val, unit='ms')
        elif val < 31536000000000000:
            wty__pwjzu = pd.to_datetime(val, unit='us')
        else:
            wty__pwjzu = pd.to_datetime(val, unit='ns')
        return wty__pwjzu
    return impl


@numba.generated_jit(nopython=True)
def float_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            wty__pwjzu = pd.Timestamp(val, unit='s')
        elif val < 31536000000000:
            wty__pwjzu = pd.Timestamp(val, unit='ms')
        elif val < 31536000000000000:
            wty__pwjzu = pd.Timestamp(val, unit='us')
        else:
            wty__pwjzu = pd.Timestamp(val, unit='ns')
        return wty__pwjzu
    return impl


@register_jitable
def pd_to_datetime_error_checked(val, dayfirst=False, yearfirst=False, utc=
    None, format=None, exact=True, unit=None, infer_datetime_format=False,
    origin='unix', cache=True):
    if val is not None:
        yhsc__wdh = val.split(' ')[0]
        if len(yhsc__wdh) < 10:
            return False, None
        else:
            rblj__nso = yhsc__wdh.count('/') in [0, 2]
            eqat__qkub = yhsc__wdh.count('-') in [0, 2]
            if not (rblj__nso and eqat__qkub):
                return False, None
    with numba.objmode(ret_val='pd_timestamp_tz_naive_type', success_flag=
        'bool_'):
        success_flag = True
        ret_val = pd.Timestamp(0)
        tvr__eft = pd.to_datetime(val, errors='coerce', dayfirst=dayfirst,
            yearfirst=yearfirst, utc=utc, format=format, exact=exact, unit=
            unit, infer_datetime_format=infer_datetime_format, origin=
            origin, cache=cache)
        if pd.isna(tvr__eft):
            success_flag = False
        else:
            ret_val = tvr__eft
    return success_flag, ret_val


@numba.generated_jit(nopython=True)
def to_date_util(conversionVal, optionalConversionFormatString, errorOnFail,
    _keep_time=False):
    errorOnFail = get_overload_const_bool(errorOnFail)
    _keep_time = get_overload_const_bool(_keep_time)
    if errorOnFail:
        med__mrq = (
            "raise ValueError('Invalid input while converting to date value')")
    else:
        med__mrq = 'bodo.libs.array_kernels.setna(res, i)'
    if _keep_time:
        udgun__oftnr = ''
    else:
        udgun__oftnr = '.normalize()'
    verify_string_arg(optionalConversionFormatString,
        'TO_DATE and TRY_TO_DATE', 'optionalConversionFormatString')
    gzafg__rlkfk = bodo.utils.utils.is_array_typ(conversionVal, True
        ) or bodo.utils.utils.is_array_typ(optionalConversionFormatString, True
        )
    vsc__lpadx = 'unbox_if_tz_naive_timestamp' if gzafg__rlkfk else ''
    if not is_overload_none(optionalConversionFormatString):
        verify_string_arg(conversionVal, 'TO_DATE and TRY_TO_DATE',
            'optionalConversionFormatString')
        ltu__lwej = (
            'py_format_str = convert_sql_date_format_str_to_py_format(arg1)\n')
        ltu__lwej += """was_successful, tmp_val = pd_to_datetime_error_checked(arg0, format=py_format_str)
"""
        ltu__lwej += 'if not was_successful:\n'
        ltu__lwej += f'  {med__mrq}\n'
        ltu__lwej += 'else:\n'
        ltu__lwej += f'  res[i] = {vsc__lpadx}(tmp_val{udgun__oftnr})\n'
    elif is_valid_string_arg(conversionVal):
        """
        If no format string is specified, snowflake will use attempt to parse the string according to these date formats:
        https://docs.snowflake.com/en/user-guide/date-time-input-output.html#date-formats. All of the examples listed are
        handled by pd.to_datetime() in Bodo jit code.

        It will also check if the string is convertable to int, IE '12345' or '-4321'"""
        ltu__lwej = 'arg0 = str(arg0)\n'
        ltu__lwej += """if (arg0.isnumeric() or (len(arg0) > 1 and arg0[0] == '-' and arg0[1:].isnumeric())):
"""
        ltu__lwej += (
            f'   res[i] = {vsc__lpadx}(int_to_datetime(np.int64(arg0)){udgun__oftnr})\n'
            )
        ltu__lwej += 'else:\n'
        ltu__lwej += (
            '   was_successful, tmp_val = pd_to_datetime_error_checked(arg0)\n'
            )
        ltu__lwej += '   if not was_successful:\n'
        ltu__lwej += f'      {med__mrq}\n'
        ltu__lwej += '   else:\n'
        ltu__lwej += f'      res[i] = {vsc__lpadx}(tmp_val{udgun__oftnr})\n'
    elif is_valid_int_arg(conversionVal):
        ltu__lwej = (
            f'res[i] = {vsc__lpadx}(int_to_datetime(arg0){udgun__oftnr})\n')
    elif is_valid_float_arg(conversionVal):
        ltu__lwej = (
            f'res[i] = {vsc__lpadx}(float_to_datetime(arg0){udgun__oftnr})\n')
    elif is_valid_datetime_or_date_arg(conversionVal):
        ltu__lwej = (
            f'res[i] = {vsc__lpadx}(pd.Timestamp(arg0){udgun__oftnr})\n')
    elif is_valid_tz_aware_datetime_arg(conversionVal):
        ltu__lwej = f'res[i] = arg0{udgun__oftnr}\n'
    else:
        raise raise_bodo_error(
            f'Internal error: unsupported type passed to to_date_util for argument conversionVal: {conversionVal}'
            )
    fmx__hfqip = ['conversionVal', 'optionalConversionFormatString',
        'errorOnFail', '_keep_time']
    kwff__ogbf = [conversionVal, optionalConversionFormatString,
        errorOnFail, _keep_time]
    fome__jclo = [True, False, False, False]
    if isinstance(conversionVal, bodo.DatetimeArrayType) or isinstance(
        conversionVal, bodo.PandasTimestampType
        ) and conversionVal.tz is not None:
        gaxq__iuqip = bodo.DatetimeArrayType(conversionVal.tz)
    else:
        gaxq__iuqip = types.Array(bodo.datetime64ns, 1, 'C')
    tth__viq = {'pd_to_datetime_error_checked':
        pd_to_datetime_error_checked, 'int_to_datetime': int_to_datetime,
        'float_to_datetime': float_to_datetime,
        'convert_sql_date_format_str_to_py_format':
        convert_sql_date_format_str_to_py_format,
        'unbox_if_tz_naive_timestamp': bodo.utils.conversion.
        unbox_if_tz_naive_timestamp}
    return gen_vectorized(fmx__hfqip, kwff__ogbf, fome__jclo, ltu__lwej,
        gaxq__iuqip, extra_globals=tth__viq)


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
    fmx__hfqip = ['arr', 'tz']
    kwff__ogbf = [arr, tz]
    fome__jclo = [True, False]
    vxy__gfv = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr) else '')
    ltu__lwej = f'res[i] = {vxy__gfv}(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    gaxq__iuqip = bodo.DatetimeArrayType(tz)
    return gen_vectorized(fmx__hfqip, kwff__ogbf, fome__jclo, ltu__lwej,
        gaxq__iuqip)


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
    fmx__hfqip = ['arr', 'normalize']
    kwff__ogbf = [arr, normalize]
    fome__jclo = [True, False]
    vsc__lpadx = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr) else '')
    ltu__lwej = ''
    if normalize:
        ltu__lwej += (
            'ts = pd.Timestamp(year=arg0.year, month=arg0.month, day=arg0.day)\n'
            )
    else:
        ltu__lwej += 'ts = arg0.tz_localize(None)\n'
    ltu__lwej += f'res[i] = {vsc__lpadx}(ts)'
    gaxq__iuqip = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(fmx__hfqip, kwff__ogbf, fome__jclo, ltu__lwej,
        gaxq__iuqip)


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
    fmx__hfqip = ['arr', 'tz']
    kwff__ogbf = [arr, tz]
    fome__jclo = [True, False]
    ltu__lwej = f'res[i] = pd.to_datetime(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    gaxq__iuqip = bodo.DatetimeArrayType(tz)
    return gen_vectorized(fmx__hfqip, kwff__ogbf, fome__jclo, ltu__lwej,
        gaxq__iuqip)
