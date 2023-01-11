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
    dugn__nuevv = is_valid_string_arg(arr)
    msujs__hqik = is_valid_float_arg(arr)
    _try = get_overload_const_bool(_try)
    if _try:
        ssdr__gcfat = 'bodo.libs.array_kernels.setna(res, i)\n'
    else:
        if dugn__nuevv:
            utku__ars = (
                "string must be one of {'true', 't', 'yes', 'y', 'on', '1'} or {'false', 'f', 'no', 'n', 'off', '0'}"
                )
        else:
            utku__ars = 'value must be a valid numeric expression'
        ssdr__gcfat = (
            f'raise ValueError("invalid value for boolean conversion: {utku__ars}")'
            )
    mowyy__gck = ['arr', '_try']
    fzce__xwjba = [arr, _try]
    bbkde__wkwoa = [True, False]
    nidwg__wfe = None
    if dugn__nuevv:
        nidwg__wfe = "true_vals = {'true', 't', 'yes', 'y', 'on', '1'}\n"
        nidwg__wfe += "false_vals = {'false', 'f', 'no', 'n', 'off', '0'}"
    if dugn__nuevv:
        zgal__bkal = 's = arg0.lower()\n'
        zgal__bkal += f'is_true_val = s in true_vals\n'
        zgal__bkal += f'res[i] = is_true_val\n'
        zgal__bkal += f'if not (is_true_val or s in false_vals):\n'
        zgal__bkal += f'  {ssdr__gcfat}\n'
    elif msujs__hqik:
        zgal__bkal = 'if np.isinf(arg0) or np.isnan(arg0):\n'
        zgal__bkal += f'  {ssdr__gcfat}\n'
        zgal__bkal += 'else:\n'
        zgal__bkal += f'  res[i] = bool(arg0)\n'
    else:
        zgal__bkal = f'res[i] = bool(arg0)'
    gsk__zlbcb = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(mowyy__gck, fzce__xwjba, bbkde__wkwoa, zgal__bkal,
        gsk__zlbcb, prefix_code=nidwg__wfe)


@numba.generated_jit(nopython=True)
def try_to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for mmp__zyibz in range(2):
        if isinstance(args[mmp__zyibz], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.try_to_date'
                , ['conversionVal', 'optionalConversionFormatString'],
                mmp__zyibz)

    def impl(conversionVal, optionalConversionFormatString):
        return to_date_util(conversionVal, optionalConversionFormatString,
            numba.literally(False))
    return impl


@numba.generated_jit(nopython=True)
def to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for mmp__zyibz in range(2):
        if isinstance(args[mmp__zyibz], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.to_date',
                ['conversionVal', 'optionalConversionFormatString'], mmp__zyibz
                )

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
    mowyy__gck = ['arr']
    fzce__xwjba = [arr]
    bbkde__wkwoa = [True]
    if is_valid_binary_arg(arr):
        zgal__bkal = 'with bodo.objmode(r=bodo.string_type):\n'
        zgal__bkal += '  r = arg0.hex()\n'
        zgal__bkal += 'res[i] = r'
    elif isinstance(arr, bodo.TimeType) or bodo.utils.utils.is_array_typ(arr
        ) and isinstance(arr.dtype, bodo.TimeType):
        zgal__bkal = (
            "h_str = str(arg0.hour) if arg0.hour > 10 else '0' + str(arg0.hour)\n"
            )
        zgal__bkal += (
            "m_str = str(arg0.minute) if arg0.minute > 10 else '0' + str(arg0.minute)\n"
            )
        zgal__bkal += (
            "s_str = str(arg0.second) if arg0.second > 10 else '0' + str(arg0.second)\n"
            )
        zgal__bkal += """ms_str = str(arg0.millisecond) if arg0.millisecond > 100 else ('0' + str(arg0.millisecond) if arg0.millisecond > 10 else '00' + str(arg0.millisecond))
"""
        zgal__bkal += """us_str = str(arg0.microsecond) if arg0.microsecond > 100 else ('0' + str(arg0.microsecond) if arg0.microsecond > 10 else '00' + str(arg0.microsecond))
"""
        zgal__bkal += """ns_str = str(arg0.nanosecond) if arg0.nanosecond > 100 else ('0' + str(arg0.nanosecond) if arg0.nanosecond > 10 else '00' + str(arg0.nanosecond))
"""
        zgal__bkal += "part_str = h_str + ':' + m_str + ':' + s_str\n"
        zgal__bkal += 'if arg0.nanosecond > 0:\n'
        zgal__bkal += (
            "  part_str = part_str + '.' + ms_str + us_str + ns_str\n")
        zgal__bkal += 'elif arg0.microsecond > 0:\n'
        zgal__bkal += "  part_str = part_str + '.' + ms_str + us_str\n"
        zgal__bkal += 'elif arg0.millisecond > 0:\n'
        zgal__bkal += "  part_str = part_str + '.' + ms_str\n"
        zgal__bkal += 'res[i] = part_str'
    elif is_valid_timedelta_arg(arr):
        zgal__bkal = (
            'v = bodo.utils.conversion.unbox_if_tz_naive_timestamp(arg0)\n')
        zgal__bkal += 'with bodo.objmode(r=bodo.string_type):\n'
        zgal__bkal += '    r = str(v)\n'
        zgal__bkal += 'res[i] = r'
    elif is_valid_datetime_or_date_arg(arr):
        if is_valid_tz_aware_datetime_arg(arr):
            zgal__bkal = "tz_raw = arg0.strftime('%z')\n"
            zgal__bkal += 'tz = tz_raw[:3] + ":" + tz_raw[3:]\n'
            zgal__bkal += "res[i] = arg0.isoformat(' ') + tz\n"
        else:
            zgal__bkal = "res[i] = pd.Timestamp(arg0).isoformat(' ')\n"
    elif is_valid_float_arg(arr):
        zgal__bkal = 'if np.isinf(arg0):\n'
        zgal__bkal += "  res[i] = 'inf' if arg0 > 0 else '-inf'\n"
        zgal__bkal += 'elif np.isnan(arg0):\n'
        zgal__bkal += "  res[i] = 'NaN'\n"
        zgal__bkal += 'else:\n'
        zgal__bkal += '  res[i] = str(arg0)'
    elif is_valid_boolean_arg(arr):
        zgal__bkal = "res[i] = 'true' if arg0 else 'false'"
    else:
        ijad__ijha = {(8): np.int8, (16): np.int16, (32): np.int32, (64):
            np.int64}
        if is_valid_int_arg(arr):
            if hasattr(arr, 'dtype'):
                hgzhf__yao = arr.dtype.bitwidth
            else:
                hgzhf__yao = arr.bitwidth
            zgal__bkal = (
                f'if arg0 == {np.iinfo(ijad__ijha[hgzhf__yao]).min}:\n')
            zgal__bkal += (
                f"  res[i] = '{np.iinfo(ijad__ijha[hgzhf__yao]).min}'\n")
            zgal__bkal += 'else:\n'
            zgal__bkal += '  res[i] = str(arg0)'
        else:
            zgal__bkal = 'res[i] = str(arg0)'
    gsk__zlbcb = bodo.string_array_type
    return gen_vectorized(mowyy__gck, fzce__xwjba, bbkde__wkwoa, zgal__bkal,
        gsk__zlbcb)


@register_jitable
def convert_sql_date_format_str_to_py_format(val):
    raise RuntimeError(
        'Converting to date values with format strings not currently supported'
        )


@numba.generated_jit(nopython=True)
def int_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            iri__nhrh = pd.to_datetime(val, unit='s')
        elif val < 31536000000000:
            iri__nhrh = pd.to_datetime(val, unit='ms')
        elif val < 31536000000000000:
            iri__nhrh = pd.to_datetime(val, unit='us')
        else:
            iri__nhrh = pd.to_datetime(val, unit='ns')
        return iri__nhrh
    return impl


@numba.generated_jit(nopython=True)
def float_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            iri__nhrh = pd.Timestamp(val, unit='s')
        elif val < 31536000000000:
            iri__nhrh = pd.Timestamp(val, unit='ms')
        elif val < 31536000000000000:
            iri__nhrh = pd.Timestamp(val, unit='us')
        else:
            iri__nhrh = pd.Timestamp(val, unit='ns')
        return iri__nhrh
    return impl


@register_jitable
def pd_to_datetime_error_checked(val, dayfirst=False, yearfirst=False, utc=
    None, format=None, exact=True, unit=None, infer_datetime_format=False,
    origin='unix', cache=True):
    if val is not None:
        ola__mjogx = val.split(' ')[0]
        if len(ola__mjogx) < 10:
            return False, None
        else:
            xmu__prqmj = ola__mjogx.count('/') in [0, 2]
            bysxz__xmf = ola__mjogx.count('-') in [0, 2]
            if not (xmu__prqmj and bysxz__xmf):
                return False, None
    with numba.objmode(ret_val='pd_timestamp_tz_naive_type', success_flag=
        'bool_'):
        success_flag = True
        ret_val = pd.Timestamp(0)
        fye__urviz = pd.to_datetime(val, errors='coerce', dayfirst=dayfirst,
            yearfirst=yearfirst, utc=utc, format=format, exact=exact, unit=
            unit, infer_datetime_format=infer_datetime_format, origin=
            origin, cache=cache)
        if pd.isna(fye__urviz):
            success_flag = False
        else:
            ret_val = fye__urviz
    return success_flag, ret_val


@numba.generated_jit(nopython=True)
def to_date_util(conversionVal, optionalConversionFormatString, errorOnFail,
    _keep_time=False):
    errorOnFail = get_overload_const_bool(errorOnFail)
    _keep_time = get_overload_const_bool(_keep_time)
    if errorOnFail:
        ddd__jkso = (
            "raise ValueError('Invalid input while converting to date value')")
    else:
        ddd__jkso = 'bodo.libs.array_kernels.setna(res, i)'
    if _keep_time:
        htiw__ffa = ''
    else:
        htiw__ffa = '.normalize()'
    verify_string_arg(optionalConversionFormatString,
        'TO_DATE and TRY_TO_DATE', 'optionalConversionFormatString')
    tyr__gdj = bodo.utils.utils.is_array_typ(conversionVal, True
        ) or bodo.utils.utils.is_array_typ(optionalConversionFormatString, True
        )
    yzvh__dlsee = 'unbox_if_tz_naive_timestamp' if tyr__gdj else ''
    if not is_overload_none(optionalConversionFormatString):
        verify_string_arg(conversionVal, 'TO_DATE and TRY_TO_DATE',
            'optionalConversionFormatString')
        zgal__bkal = (
            'py_format_str = convert_sql_date_format_str_to_py_format(arg1)\n')
        zgal__bkal += """was_successful, tmp_val = pd_to_datetime_error_checked(arg0, format=py_format_str)
"""
        zgal__bkal += 'if not was_successful:\n'
        zgal__bkal += f'  {ddd__jkso}\n'
        zgal__bkal += 'else:\n'
        zgal__bkal += f'  res[i] = {yzvh__dlsee}(tmp_val{htiw__ffa})\n'
    elif is_valid_string_arg(conversionVal):
        """
        If no format string is specified, snowflake will use attempt to parse the string according to these date formats:
        https://docs.snowflake.com/en/user-guide/date-time-input-output.html#date-formats. All of the examples listed are
        handled by pd.to_datetime() in Bodo jit code.

        It will also check if the string is convertable to int, IE '12345' or '-4321'"""
        zgal__bkal = 'arg0 = str(arg0)\n'
        zgal__bkal += """if (arg0.isnumeric() or (len(arg0) > 1 and arg0[0] == '-' and arg0[1:].isnumeric())):
"""
        zgal__bkal += (
            f'   res[i] = {yzvh__dlsee}(int_to_datetime(np.int64(arg0)){htiw__ffa})\n'
            )
        zgal__bkal += 'else:\n'
        zgal__bkal += (
            '   was_successful, tmp_val = pd_to_datetime_error_checked(arg0)\n'
            )
        zgal__bkal += '   if not was_successful:\n'
        zgal__bkal += f'      {ddd__jkso}\n'
        zgal__bkal += '   else:\n'
        zgal__bkal += f'      res[i] = {yzvh__dlsee}(tmp_val{htiw__ffa})\n'
    elif is_valid_int_arg(conversionVal):
        zgal__bkal = (
            f'res[i] = {yzvh__dlsee}(int_to_datetime(arg0){htiw__ffa})\n')
    elif is_valid_float_arg(conversionVal):
        zgal__bkal = (
            f'res[i] = {yzvh__dlsee}(float_to_datetime(arg0){htiw__ffa})\n')
    elif is_valid_datetime_or_date_arg(conversionVal):
        zgal__bkal = f'res[i] = {yzvh__dlsee}(pd.Timestamp(arg0){htiw__ffa})\n'
    elif is_valid_tz_aware_datetime_arg(conversionVal):
        zgal__bkal = f'res[i] = arg0{htiw__ffa}\n'
    else:
        raise raise_bodo_error(
            f'Internal error: unsupported type passed to to_date_util for argument conversionVal: {conversionVal}'
            )
    mowyy__gck = ['conversionVal', 'optionalConversionFormatString',
        'errorOnFail', '_keep_time']
    fzce__xwjba = [conversionVal, optionalConversionFormatString,
        errorOnFail, _keep_time]
    bbkde__wkwoa = [True, False, False, False]
    if isinstance(conversionVal, bodo.DatetimeArrayType) or isinstance(
        conversionVal, bodo.PandasTimestampType
        ) and conversionVal.tz is not None:
        gsk__zlbcb = bodo.DatetimeArrayType(conversionVal.tz)
    else:
        gsk__zlbcb = types.Array(bodo.datetime64ns, 1, 'C')
    hoqq__eow = {'pd_to_datetime_error_checked':
        pd_to_datetime_error_checked, 'int_to_datetime': int_to_datetime,
        'float_to_datetime': float_to_datetime,
        'convert_sql_date_format_str_to_py_format':
        convert_sql_date_format_str_to_py_format,
        'unbox_if_tz_naive_timestamp': bodo.utils.conversion.
        unbox_if_tz_naive_timestamp}
    return gen_vectorized(mowyy__gck, fzce__xwjba, bbkde__wkwoa, zgal__bkal,
        gsk__zlbcb, extra_globals=hoqq__eow)


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
    mowyy__gck = ['arr', 'tz']
    fzce__xwjba = [arr, tz]
    bbkde__wkwoa = [True, False]
    joa__bhcay = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr) else '')
    zgal__bkal = f'res[i] = {joa__bhcay}(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    gsk__zlbcb = bodo.DatetimeArrayType(tz)
    return gen_vectorized(mowyy__gck, fzce__xwjba, bbkde__wkwoa, zgal__bkal,
        gsk__zlbcb)


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
    mowyy__gck = ['arr', 'normalize']
    fzce__xwjba = [arr, normalize]
    bbkde__wkwoa = [True, False]
    yzvh__dlsee = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr) else '')
    zgal__bkal = ''
    if normalize:
        zgal__bkal += (
            'ts = pd.Timestamp(year=arg0.year, month=arg0.month, day=arg0.day)\n'
            )
    else:
        zgal__bkal += 'ts = arg0.tz_localize(None)\n'
    zgal__bkal += f'res[i] = {yzvh__dlsee}(ts)'
    gsk__zlbcb = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(mowyy__gck, fzce__xwjba, bbkde__wkwoa, zgal__bkal,
        gsk__zlbcb)


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
    mowyy__gck = ['arr', 'tz']
    fzce__xwjba = [arr, tz]
    bbkde__wkwoa = [True, False]
    zgal__bkal = f'res[i] = pd.to_datetime(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    gsk__zlbcb = bodo.DatetimeArrayType(tz)
    return gen_vectorized(mowyy__gck, fzce__xwjba, bbkde__wkwoa, zgal__bkal,
        gsk__zlbcb)
