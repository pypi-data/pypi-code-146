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
    mxglf__toi = is_valid_string_arg(arr)
    zdyh__yfagj = is_valid_float_arg(arr)
    _try = get_overload_const_bool(_try)
    if _try:
        nkpi__ygmi = 'bodo.libs.array_kernels.setna(res, i)\n'
    else:
        if mxglf__toi:
            kvcj__ckz = (
                "string must be one of {'true', 't', 'yes', 'y', 'on', '1'} or {'false', 'f', 'no', 'n', 'off', '0'}"
                )
        else:
            kvcj__ckz = 'value must be a valid numeric expression'
        nkpi__ygmi = (
            f'raise ValueError("invalid value for boolean conversion: {kvcj__ckz}")'
            )
    bbhw__ivck = ['arr', '_try']
    pucx__hzeyt = [arr, _try]
    kitsd__xdbzq = [True, False]
    lee__tcww = None
    if mxglf__toi:
        lee__tcww = "true_vals = {'true', 't', 'yes', 'y', 'on', '1'}\n"
        lee__tcww += "false_vals = {'false', 'f', 'no', 'n', 'off', '0'}"
    if mxglf__toi:
        zzc__lhmba = 's = arg0.lower()\n'
        zzc__lhmba += f'is_true_val = s in true_vals\n'
        zzc__lhmba += f'res[i] = is_true_val\n'
        zzc__lhmba += f'if not (is_true_val or s in false_vals):\n'
        zzc__lhmba += f'  {nkpi__ygmi}\n'
    elif zdyh__yfagj:
        zzc__lhmba = 'if np.isinf(arg0) or np.isnan(arg0):\n'
        zzc__lhmba += f'  {nkpi__ygmi}\n'
        zzc__lhmba += 'else:\n'
        zzc__lhmba += f'  res[i] = bool(arg0)\n'
    else:
        zzc__lhmba = f'res[i] = bool(arg0)'
    vqx__ebi = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(bbhw__ivck, pucx__hzeyt, kitsd__xdbzq, zzc__lhmba,
        vqx__ebi, prefix_code=lee__tcww)


@numba.generated_jit(nopython=True)
def try_to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for gzrf__ygrz in range(2):
        if isinstance(args[gzrf__ygrz], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.try_to_date'
                , ['conversionVal', 'optionalConversionFormatString'],
                gzrf__ygrz)

    def impl(conversionVal, optionalConversionFormatString):
        return to_date_util(conversionVal, optionalConversionFormatString,
            numba.literally(False))
    return impl


@numba.generated_jit(nopython=True)
def to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for gzrf__ygrz in range(2):
        if isinstance(args[gzrf__ygrz], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.to_date',
                ['conversionVal', 'optionalConversionFormatString'], gzrf__ygrz
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
    bbhw__ivck = ['arr']
    pucx__hzeyt = [arr]
    kitsd__xdbzq = [True]
    if is_valid_binary_arg(arr):
        zzc__lhmba = 'with bodo.objmode(r=bodo.string_type):\n'
        zzc__lhmba += '  r = arg0.hex()\n'
        zzc__lhmba += 'res[i] = r'
    elif isinstance(arr, bodo.TimeType) or bodo.utils.utils.is_array_typ(arr
        ) and isinstance(arr.dtype, bodo.TimeType):
        zzc__lhmba = (
            "h_str = str(arg0.hour) if arg0.hour > 10 else '0' + str(arg0.hour)\n"
            )
        zzc__lhmba += (
            "m_str = str(arg0.minute) if arg0.minute > 10 else '0' + str(arg0.minute)\n"
            )
        zzc__lhmba += (
            "s_str = str(arg0.second) if arg0.second > 10 else '0' + str(arg0.second)\n"
            )
        zzc__lhmba += """ms_str = str(arg0.millisecond) if arg0.millisecond > 100 else ('0' + str(arg0.millisecond) if arg0.millisecond > 10 else '00' + str(arg0.millisecond))
"""
        zzc__lhmba += """us_str = str(arg0.microsecond) if arg0.microsecond > 100 else ('0' + str(arg0.microsecond) if arg0.microsecond > 10 else '00' + str(arg0.microsecond))
"""
        zzc__lhmba += """ns_str = str(arg0.nanosecond) if arg0.nanosecond > 100 else ('0' + str(arg0.nanosecond) if arg0.nanosecond > 10 else '00' + str(arg0.nanosecond))
"""
        zzc__lhmba += "part_str = h_str + ':' + m_str + ':' + s_str\n"
        zzc__lhmba += 'if arg0.nanosecond > 0:\n'
        zzc__lhmba += (
            "  part_str = part_str + '.' + ms_str + us_str + ns_str\n")
        zzc__lhmba += 'elif arg0.microsecond > 0:\n'
        zzc__lhmba += "  part_str = part_str + '.' + ms_str + us_str\n"
        zzc__lhmba += 'elif arg0.millisecond > 0:\n'
        zzc__lhmba += "  part_str = part_str + '.' + ms_str\n"
        zzc__lhmba += 'res[i] = part_str'
    elif is_valid_timedelta_arg(arr):
        zzc__lhmba = (
            'v = bodo.utils.conversion.unbox_if_tz_naive_timestamp(arg0)\n')
        zzc__lhmba += 'with bodo.objmode(r=bodo.string_type):\n'
        zzc__lhmba += '    r = str(v)\n'
        zzc__lhmba += 'res[i] = r'
    elif is_valid_datetime_or_date_arg(arr):
        if is_valid_tz_aware_datetime_arg(arr):
            zzc__lhmba = "tz_raw = arg0.strftime('%z')\n"
            zzc__lhmba += 'tz = tz_raw[:3] + ":" + tz_raw[3:]\n'
            zzc__lhmba += "res[i] = arg0.isoformat(' ') + tz\n"
        else:
            zzc__lhmba = "res[i] = pd.Timestamp(arg0).isoformat(' ')\n"
    elif is_valid_float_arg(arr):
        zzc__lhmba = 'if np.isinf(arg0):\n'
        zzc__lhmba += "  res[i] = 'inf' if arg0 > 0 else '-inf'\n"
        zzc__lhmba += 'elif np.isnan(arg0):\n'
        zzc__lhmba += "  res[i] = 'NaN'\n"
        zzc__lhmba += 'else:\n'
        zzc__lhmba += '  res[i] = str(arg0)'
    elif is_valid_boolean_arg(arr):
        zzc__lhmba = "res[i] = 'true' if arg0 else 'false'"
    else:
        fhymj__vdmnf = {(8): np.int8, (16): np.int16, (32): np.int32, (64):
            np.int64}
        if is_valid_int_arg(arr):
            if hasattr(arr, 'dtype'):
                pdq__fch = arr.dtype.bitwidth
            else:
                pdq__fch = arr.bitwidth
            zzc__lhmba = (
                f'if arg0 == {np.iinfo(fhymj__vdmnf[pdq__fch]).min}:\n')
            zzc__lhmba += (
                f"  res[i] = '{np.iinfo(fhymj__vdmnf[pdq__fch]).min}'\n")
            zzc__lhmba += 'else:\n'
            zzc__lhmba += '  res[i] = str(arg0)'
        else:
            zzc__lhmba = 'res[i] = str(arg0)'
    vqx__ebi = bodo.string_array_type
    return gen_vectorized(bbhw__ivck, pucx__hzeyt, kitsd__xdbzq, zzc__lhmba,
        vqx__ebi)


@register_jitable
def convert_sql_date_format_str_to_py_format(val):
    raise RuntimeError(
        'Converting to date values with format strings not currently supported'
        )


@numba.generated_jit(nopython=True)
def int_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            cla__hbx = pd.to_datetime(val, unit='s')
        elif val < 31536000000000:
            cla__hbx = pd.to_datetime(val, unit='ms')
        elif val < 31536000000000000:
            cla__hbx = pd.to_datetime(val, unit='us')
        else:
            cla__hbx = pd.to_datetime(val, unit='ns')
        return cla__hbx
    return impl


@numba.generated_jit(nopython=True)
def float_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            cla__hbx = pd.Timestamp(val, unit='s')
        elif val < 31536000000000:
            cla__hbx = pd.Timestamp(val, unit='ms')
        elif val < 31536000000000000:
            cla__hbx = pd.Timestamp(val, unit='us')
        else:
            cla__hbx = pd.Timestamp(val, unit='ns')
        return cla__hbx
    return impl


@register_jitable
def pd_to_datetime_error_checked(val, dayfirst=False, yearfirst=False, utc=
    None, format=None, exact=True, unit=None, infer_datetime_format=False,
    origin='unix', cache=True):
    if val is not None:
        srwk__swn = val.split(' ')[0]
        if len(srwk__swn) < 10:
            return False, None
        else:
            bna__xvksk = srwk__swn.count('/') in [0, 2]
            uwtj__ykfi = srwk__swn.count('-') in [0, 2]
            if not (bna__xvksk and uwtj__ykfi):
                return False, None
    with numba.objmode(ret_val='pd_timestamp_tz_naive_type', success_flag=
        'bool_'):
        success_flag = True
        ret_val = pd.Timestamp(0)
        kuwew__ihuox = pd.to_datetime(val, errors='coerce', dayfirst=
            dayfirst, yearfirst=yearfirst, utc=utc, format=format, exact=
            exact, unit=unit, infer_datetime_format=infer_datetime_format,
            origin=origin, cache=cache)
        if pd.isna(kuwew__ihuox):
            success_flag = False
        else:
            ret_val = kuwew__ihuox
    return success_flag, ret_val


@numba.generated_jit(nopython=True)
def to_date_util(conversionVal, optionalConversionFormatString, errorOnFail,
    _keep_time=False):
    errorOnFail = get_overload_const_bool(errorOnFail)
    _keep_time = get_overload_const_bool(_keep_time)
    if errorOnFail:
        intz__sdo = (
            "raise ValueError('Invalid input while converting to date value')")
    else:
        intz__sdo = 'bodo.libs.array_kernels.setna(res, i)'
    if _keep_time:
        rra__ukln = ''
    else:
        rra__ukln = '.normalize()'
    verify_string_arg(optionalConversionFormatString,
        'TO_DATE and TRY_TO_DATE', 'optionalConversionFormatString')
    sodtr__ode = bodo.utils.utils.is_array_typ(conversionVal, True
        ) or bodo.utils.utils.is_array_typ(optionalConversionFormatString, True
        )
    xvz__rwu = 'unbox_if_tz_naive_timestamp' if sodtr__ode else ''
    if not is_overload_none(optionalConversionFormatString):
        verify_string_arg(conversionVal, 'TO_DATE and TRY_TO_DATE',
            'optionalConversionFormatString')
        zzc__lhmba = (
            'py_format_str = convert_sql_date_format_str_to_py_format(arg1)\n')
        zzc__lhmba += """was_successful, tmp_val = pd_to_datetime_error_checked(arg0, format=py_format_str)
"""
        zzc__lhmba += 'if not was_successful:\n'
        zzc__lhmba += f'  {intz__sdo}\n'
        zzc__lhmba += 'else:\n'
        zzc__lhmba += f'  res[i] = {xvz__rwu}(tmp_val{rra__ukln})\n'
    elif is_valid_string_arg(conversionVal):
        """
        If no format string is specified, snowflake will use attempt to parse the string according to these date formats:
        https://docs.snowflake.com/en/user-guide/date-time-input-output.html#date-formats. All of the examples listed are
        handled by pd.to_datetime() in Bodo jit code.

        It will also check if the string is convertable to int, IE '12345' or '-4321'"""
        zzc__lhmba = 'arg0 = str(arg0)\n'
        zzc__lhmba += """if (arg0.isnumeric() or (len(arg0) > 1 and arg0[0] == '-' and arg0[1:].isnumeric())):
"""
        zzc__lhmba += (
            f'   res[i] = {xvz__rwu}(int_to_datetime(np.int64(arg0)){rra__ukln})\n'
            )
        zzc__lhmba += 'else:\n'
        zzc__lhmba += (
            '   was_successful, tmp_val = pd_to_datetime_error_checked(arg0)\n'
            )
        zzc__lhmba += '   if not was_successful:\n'
        zzc__lhmba += f'      {intz__sdo}\n'
        zzc__lhmba += '   else:\n'
        zzc__lhmba += f'      res[i] = {xvz__rwu}(tmp_val{rra__ukln})\n'
    elif is_valid_int_arg(conversionVal):
        zzc__lhmba = f'res[i] = {xvz__rwu}(int_to_datetime(arg0){rra__ukln})\n'
    elif is_valid_float_arg(conversionVal):
        zzc__lhmba = (
            f'res[i] = {xvz__rwu}(float_to_datetime(arg0){rra__ukln})\n')
    elif is_valid_datetime_or_date_arg(conversionVal):
        zzc__lhmba = f'res[i] = {xvz__rwu}(pd.Timestamp(arg0){rra__ukln})\n'
    elif is_valid_tz_aware_datetime_arg(conversionVal):
        zzc__lhmba = f'res[i] = arg0{rra__ukln}\n'
    else:
        raise raise_bodo_error(
            f'Internal error: unsupported type passed to to_date_util for argument conversionVal: {conversionVal}'
            )
    bbhw__ivck = ['conversionVal', 'optionalConversionFormatString',
        'errorOnFail', '_keep_time']
    pucx__hzeyt = [conversionVal, optionalConversionFormatString,
        errorOnFail, _keep_time]
    kitsd__xdbzq = [True, False, False, False]
    if isinstance(conversionVal, bodo.DatetimeArrayType) or isinstance(
        conversionVal, bodo.PandasTimestampType
        ) and conversionVal.tz is not None:
        vqx__ebi = bodo.DatetimeArrayType(conversionVal.tz)
    else:
        vqx__ebi = types.Array(bodo.datetime64ns, 1, 'C')
    dfcp__hgx = {'pd_to_datetime_error_checked':
        pd_to_datetime_error_checked, 'int_to_datetime': int_to_datetime,
        'float_to_datetime': float_to_datetime,
        'convert_sql_date_format_str_to_py_format':
        convert_sql_date_format_str_to_py_format,
        'unbox_if_tz_naive_timestamp': bodo.utils.conversion.
        unbox_if_tz_naive_timestamp}
    return gen_vectorized(bbhw__ivck, pucx__hzeyt, kitsd__xdbzq, zzc__lhmba,
        vqx__ebi, extra_globals=dfcp__hgx)


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
    bbhw__ivck = ['arr', 'tz']
    pucx__hzeyt = [arr, tz]
    kitsd__xdbzq = [True, False]
    nnonr__bgs = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr) else '')
    zzc__lhmba = f'res[i] = {nnonr__bgs}(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    vqx__ebi = bodo.DatetimeArrayType(tz)
    return gen_vectorized(bbhw__ivck, pucx__hzeyt, kitsd__xdbzq, zzc__lhmba,
        vqx__ebi)


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
    bbhw__ivck = ['arr', 'normalize']
    pucx__hzeyt = [arr, normalize]
    kitsd__xdbzq = [True, False]
    xvz__rwu = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
        .utils.utils.is_array_typ(arr) else '')
    zzc__lhmba = ''
    if normalize:
        zzc__lhmba += (
            'ts = pd.Timestamp(year=arg0.year, month=arg0.month, day=arg0.day)\n'
            )
    else:
        zzc__lhmba += 'ts = arg0.tz_localize(None)\n'
    zzc__lhmba += f'res[i] = {xvz__rwu}(ts)'
    vqx__ebi = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(bbhw__ivck, pucx__hzeyt, kitsd__xdbzq, zzc__lhmba,
        vqx__ebi)


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
    bbhw__ivck = ['arr', 'tz']
    pucx__hzeyt = [arr, tz]
    kitsd__xdbzq = [True, False]
    zzc__lhmba = f'res[i] = pd.to_datetime(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    vqx__ebi = bodo.DatetimeArrayType(tz)
    return gen_vectorized(bbhw__ivck, pucx__hzeyt, kitsd__xdbzq, zzc__lhmba,
        vqx__ebi)
