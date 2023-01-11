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
    wxgbx__oing = is_valid_string_arg(arr)
    lkc__eqks = is_valid_float_arg(arr)
    _try = get_overload_const_bool(_try)
    if _try:
        gwlyp__msup = 'bodo.libs.array_kernels.setna(res, i)\n'
    else:
        if wxgbx__oing:
            jdnde__purb = (
                "string must be one of {'true', 't', 'yes', 'y', 'on', '1'} or {'false', 'f', 'no', 'n', 'off', '0'}"
                )
        else:
            jdnde__purb = 'value must be a valid numeric expression'
        gwlyp__msup = (
            f'raise ValueError("invalid value for boolean conversion: {jdnde__purb}")'
            )
    qzpz__pyhaf = ['arr', '_try']
    itjo__gmflo = [arr, _try]
    vvm__pmola = [True, False]
    faglj__yiuz = None
    if wxgbx__oing:
        faglj__yiuz = "true_vals = {'true', 't', 'yes', 'y', 'on', '1'}\n"
        faglj__yiuz += "false_vals = {'false', 'f', 'no', 'n', 'off', '0'}"
    if wxgbx__oing:
        vmaxq__dud = 's = arg0.lower()\n'
        vmaxq__dud += f'is_true_val = s in true_vals\n'
        vmaxq__dud += f'res[i] = is_true_val\n'
        vmaxq__dud += f'if not (is_true_val or s in false_vals):\n'
        vmaxq__dud += f'  {gwlyp__msup}\n'
    elif lkc__eqks:
        vmaxq__dud = 'if np.isinf(arg0) or np.isnan(arg0):\n'
        vmaxq__dud += f'  {gwlyp__msup}\n'
        vmaxq__dud += 'else:\n'
        vmaxq__dud += f'  res[i] = bool(arg0)\n'
    else:
        vmaxq__dud = f'res[i] = bool(arg0)'
    vby__cqyec = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(qzpz__pyhaf, itjo__gmflo, vvm__pmola, vmaxq__dud,
        vby__cqyec, prefix_code=faglj__yiuz)


@numba.generated_jit(nopython=True)
def try_to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for jbd__rxv in range(2):
        if isinstance(args[jbd__rxv], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.try_to_date'
                , ['conversionVal', 'optionalConversionFormatString'], jbd__rxv
                )

    def impl(conversionVal, optionalConversionFormatString):
        return to_date_util(conversionVal, optionalConversionFormatString,
            numba.literally(False))
    return impl


@numba.generated_jit(nopython=True)
def to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for jbd__rxv in range(2):
        if isinstance(args[jbd__rxv], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.to_date',
                ['conversionVal', 'optionalConversionFormatString'], jbd__rxv)

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
    qzpz__pyhaf = ['arr']
    itjo__gmflo = [arr]
    vvm__pmola = [True]
    if is_valid_binary_arg(arr):
        vmaxq__dud = 'with bodo.objmode(r=bodo.string_type):\n'
        vmaxq__dud += '  r = arg0.hex()\n'
        vmaxq__dud += 'res[i] = r'
    elif isinstance(arr, bodo.TimeType) or bodo.utils.utils.is_array_typ(arr
        ) and isinstance(arr.dtype, bodo.TimeType):
        vmaxq__dud = (
            "h_str = str(arg0.hour) if arg0.hour > 10 else '0' + str(arg0.hour)\n"
            )
        vmaxq__dud += (
            "m_str = str(arg0.minute) if arg0.minute > 10 else '0' + str(arg0.minute)\n"
            )
        vmaxq__dud += (
            "s_str = str(arg0.second) if arg0.second > 10 else '0' + str(arg0.second)\n"
            )
        vmaxq__dud += """ms_str = str(arg0.millisecond) if arg0.millisecond > 100 else ('0' + str(arg0.millisecond) if arg0.millisecond > 10 else '00' + str(arg0.millisecond))
"""
        vmaxq__dud += """us_str = str(arg0.microsecond) if arg0.microsecond > 100 else ('0' + str(arg0.microsecond) if arg0.microsecond > 10 else '00' + str(arg0.microsecond))
"""
        vmaxq__dud += """ns_str = str(arg0.nanosecond) if arg0.nanosecond > 100 else ('0' + str(arg0.nanosecond) if arg0.nanosecond > 10 else '00' + str(arg0.nanosecond))
"""
        vmaxq__dud += "part_str = h_str + ':' + m_str + ':' + s_str\n"
        vmaxq__dud += 'if arg0.nanosecond > 0:\n'
        vmaxq__dud += (
            "  part_str = part_str + '.' + ms_str + us_str + ns_str\n")
        vmaxq__dud += 'elif arg0.microsecond > 0:\n'
        vmaxq__dud += "  part_str = part_str + '.' + ms_str + us_str\n"
        vmaxq__dud += 'elif arg0.millisecond > 0:\n'
        vmaxq__dud += "  part_str = part_str + '.' + ms_str\n"
        vmaxq__dud += 'res[i] = part_str'
    elif is_valid_timedelta_arg(arr):
        vmaxq__dud = (
            'v = bodo.utils.conversion.unbox_if_tz_naive_timestamp(arg0)\n')
        vmaxq__dud += 'with bodo.objmode(r=bodo.string_type):\n'
        vmaxq__dud += '    r = str(v)\n'
        vmaxq__dud += 'res[i] = r'
    elif is_valid_datetime_or_date_arg(arr):
        if is_valid_tz_aware_datetime_arg(arr):
            vmaxq__dud = "tz_raw = arg0.strftime('%z')\n"
            vmaxq__dud += 'tz = tz_raw[:3] + ":" + tz_raw[3:]\n'
            vmaxq__dud += "res[i] = arg0.isoformat(' ') + tz\n"
        else:
            vmaxq__dud = "res[i] = pd.Timestamp(arg0).isoformat(' ')\n"
    elif is_valid_float_arg(arr):
        vmaxq__dud = 'if np.isinf(arg0):\n'
        vmaxq__dud += "  res[i] = 'inf' if arg0 > 0 else '-inf'\n"
        vmaxq__dud += 'elif np.isnan(arg0):\n'
        vmaxq__dud += "  res[i] = 'NaN'\n"
        vmaxq__dud += 'else:\n'
        vmaxq__dud += '  res[i] = str(arg0)'
    elif is_valid_boolean_arg(arr):
        vmaxq__dud = "res[i] = 'true' if arg0 else 'false'"
    else:
        lmq__olqo = {(8): np.int8, (16): np.int16, (32): np.int32, (64): np
            .int64}
        if is_valid_int_arg(arr):
            if hasattr(arr, 'dtype'):
                hgd__dmko = arr.dtype.bitwidth
            else:
                hgd__dmko = arr.bitwidth
            vmaxq__dud = f'if arg0 == {np.iinfo(lmq__olqo[hgd__dmko]).min}:\n'
            vmaxq__dud += (
                f"  res[i] = '{np.iinfo(lmq__olqo[hgd__dmko]).min}'\n")
            vmaxq__dud += 'else:\n'
            vmaxq__dud += '  res[i] = str(arg0)'
        else:
            vmaxq__dud = 'res[i] = str(arg0)'
    vby__cqyec = bodo.string_array_type
    return gen_vectorized(qzpz__pyhaf, itjo__gmflo, vvm__pmola, vmaxq__dud,
        vby__cqyec)


@register_jitable
def convert_sql_date_format_str_to_py_format(val):
    raise RuntimeError(
        'Converting to date values with format strings not currently supported'
        )


@numba.generated_jit(nopython=True)
def int_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            unhr__ilis = pd.to_datetime(val, unit='s')
        elif val < 31536000000000:
            unhr__ilis = pd.to_datetime(val, unit='ms')
        elif val < 31536000000000000:
            unhr__ilis = pd.to_datetime(val, unit='us')
        else:
            unhr__ilis = pd.to_datetime(val, unit='ns')
        return unhr__ilis
    return impl


@numba.generated_jit(nopython=True)
def float_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            unhr__ilis = pd.Timestamp(val, unit='s')
        elif val < 31536000000000:
            unhr__ilis = pd.Timestamp(val, unit='ms')
        elif val < 31536000000000000:
            unhr__ilis = pd.Timestamp(val, unit='us')
        else:
            unhr__ilis = pd.Timestamp(val, unit='ns')
        return unhr__ilis
    return impl


@register_jitable
def pd_to_datetime_error_checked(val, dayfirst=False, yearfirst=False, utc=
    None, format=None, exact=True, unit=None, infer_datetime_format=False,
    origin='unix', cache=True):
    if val is not None:
        krbf__lbz = val.split(' ')[0]
        if len(krbf__lbz) < 10:
            return False, None
        else:
            gymvn__xehi = krbf__lbz.count('/') in [0, 2]
            mjva__stqy = krbf__lbz.count('-') in [0, 2]
            if not (gymvn__xehi and mjva__stqy):
                return False, None
    with numba.objmode(ret_val='pd_timestamp_tz_naive_type', success_flag=
        'bool_'):
        success_flag = True
        ret_val = pd.Timestamp(0)
        eeu__anvfn = pd.to_datetime(val, errors='coerce', dayfirst=dayfirst,
            yearfirst=yearfirst, utc=utc, format=format, exact=exact, unit=
            unit, infer_datetime_format=infer_datetime_format, origin=
            origin, cache=cache)
        if pd.isna(eeu__anvfn):
            success_flag = False
        else:
            ret_val = eeu__anvfn
    return success_flag, ret_val


@numba.generated_jit(nopython=True)
def to_date_util(conversionVal, optionalConversionFormatString, errorOnFail,
    _keep_time=False):
    errorOnFail = get_overload_const_bool(errorOnFail)
    _keep_time = get_overload_const_bool(_keep_time)
    if errorOnFail:
        hvn__bjco = (
            "raise ValueError('Invalid input while converting to date value')")
    else:
        hvn__bjco = 'bodo.libs.array_kernels.setna(res, i)'
    if _keep_time:
        rfk__maa = ''
    else:
        rfk__maa = '.normalize()'
    verify_string_arg(optionalConversionFormatString,
        'TO_DATE and TRY_TO_DATE', 'optionalConversionFormatString')
    abwz__clwg = bodo.utils.utils.is_array_typ(conversionVal, True
        ) or bodo.utils.utils.is_array_typ(optionalConversionFormatString, True
        )
    jakij__tlz = 'unbox_if_tz_naive_timestamp' if abwz__clwg else ''
    if not is_overload_none(optionalConversionFormatString):
        verify_string_arg(conversionVal, 'TO_DATE and TRY_TO_DATE',
            'optionalConversionFormatString')
        vmaxq__dud = (
            'py_format_str = convert_sql_date_format_str_to_py_format(arg1)\n')
        vmaxq__dud += """was_successful, tmp_val = pd_to_datetime_error_checked(arg0, format=py_format_str)
"""
        vmaxq__dud += 'if not was_successful:\n'
        vmaxq__dud += f'  {hvn__bjco}\n'
        vmaxq__dud += 'else:\n'
        vmaxq__dud += f'  res[i] = {jakij__tlz}(tmp_val{rfk__maa})\n'
    elif is_valid_string_arg(conversionVal):
        """
        If no format string is specified, snowflake will use attempt to parse the string according to these date formats:
        https://docs.snowflake.com/en/user-guide/date-time-input-output.html#date-formats. All of the examples listed are
        handled by pd.to_datetime() in Bodo jit code.

        It will also check if the string is convertable to int, IE '12345' or '-4321'"""
        vmaxq__dud = 'arg0 = str(arg0)\n'
        vmaxq__dud += """if (arg0.isnumeric() or (len(arg0) > 1 and arg0[0] == '-' and arg0[1:].isnumeric())):
"""
        vmaxq__dud += (
            f'   res[i] = {jakij__tlz}(int_to_datetime(np.int64(arg0)){rfk__maa})\n'
            )
        vmaxq__dud += 'else:\n'
        vmaxq__dud += (
            '   was_successful, tmp_val = pd_to_datetime_error_checked(arg0)\n'
            )
        vmaxq__dud += '   if not was_successful:\n'
        vmaxq__dud += f'      {hvn__bjco}\n'
        vmaxq__dud += '   else:\n'
        vmaxq__dud += f'      res[i] = {jakij__tlz}(tmp_val{rfk__maa})\n'
    elif is_valid_int_arg(conversionVal):
        vmaxq__dud = (
            f'res[i] = {jakij__tlz}(int_to_datetime(arg0){rfk__maa})\n')
    elif is_valid_float_arg(conversionVal):
        vmaxq__dud = (
            f'res[i] = {jakij__tlz}(float_to_datetime(arg0){rfk__maa})\n')
    elif is_valid_datetime_or_date_arg(conversionVal):
        vmaxq__dud = f'res[i] = {jakij__tlz}(pd.Timestamp(arg0){rfk__maa})\n'
    elif is_valid_tz_aware_datetime_arg(conversionVal):
        vmaxq__dud = f'res[i] = arg0{rfk__maa}\n'
    else:
        raise raise_bodo_error(
            f'Internal error: unsupported type passed to to_date_util for argument conversionVal: {conversionVal}'
            )
    qzpz__pyhaf = ['conversionVal', 'optionalConversionFormatString',
        'errorOnFail', '_keep_time']
    itjo__gmflo = [conversionVal, optionalConversionFormatString,
        errorOnFail, _keep_time]
    vvm__pmola = [True, False, False, False]
    if isinstance(conversionVal, bodo.DatetimeArrayType) or isinstance(
        conversionVal, bodo.PandasTimestampType
        ) and conversionVal.tz is not None:
        vby__cqyec = bodo.DatetimeArrayType(conversionVal.tz)
    else:
        vby__cqyec = types.Array(bodo.datetime64ns, 1, 'C')
    nnl__cxciw = {'pd_to_datetime_error_checked':
        pd_to_datetime_error_checked, 'int_to_datetime': int_to_datetime,
        'float_to_datetime': float_to_datetime,
        'convert_sql_date_format_str_to_py_format':
        convert_sql_date_format_str_to_py_format,
        'unbox_if_tz_naive_timestamp': bodo.utils.conversion.
        unbox_if_tz_naive_timestamp}
    return gen_vectorized(qzpz__pyhaf, itjo__gmflo, vvm__pmola, vmaxq__dud,
        vby__cqyec, extra_globals=nnl__cxciw)


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
    qzpz__pyhaf = ['arr', 'tz']
    itjo__gmflo = [arr, tz]
    vvm__pmola = [True, False]
    xpe__syqtd = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr) else '')
    vmaxq__dud = f'res[i] = {xpe__syqtd}(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    vby__cqyec = bodo.DatetimeArrayType(tz)
    return gen_vectorized(qzpz__pyhaf, itjo__gmflo, vvm__pmola, vmaxq__dud,
        vby__cqyec)


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
    qzpz__pyhaf = ['arr', 'normalize']
    itjo__gmflo = [arr, normalize]
    vvm__pmola = [True, False]
    jakij__tlz = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr) else '')
    vmaxq__dud = ''
    if normalize:
        vmaxq__dud += (
            'ts = pd.Timestamp(year=arg0.year, month=arg0.month, day=arg0.day)\n'
            )
    else:
        vmaxq__dud += 'ts = arg0.tz_localize(None)\n'
    vmaxq__dud += f'res[i] = {jakij__tlz}(ts)'
    vby__cqyec = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(qzpz__pyhaf, itjo__gmflo, vvm__pmola, vmaxq__dud,
        vby__cqyec)


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
    qzpz__pyhaf = ['arr', 'tz']
    itjo__gmflo = [arr, tz]
    vvm__pmola = [True, False]
    vmaxq__dud = f'res[i] = pd.to_datetime(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    vby__cqyec = bodo.DatetimeArrayType(tz)
    return gen_vectorized(qzpz__pyhaf, itjo__gmflo, vvm__pmola, vmaxq__dud,
        vby__cqyec)
