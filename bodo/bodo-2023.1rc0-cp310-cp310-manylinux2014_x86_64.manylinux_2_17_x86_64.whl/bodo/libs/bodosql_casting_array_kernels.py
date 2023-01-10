"""
Implements a number of array kernels that handling casting functions for BodoSQL
"""
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import BodoError


def cast_float64(arr):
    return


def cast_float64_util(arr):
    return


def cast_float32(arr):
    return


def cast_float32_util(arr):
    return


def cast_int64(arr):
    return


def cast_int64_util(arr):
    return


def cast_int32(arr):
    return


def cast_int32_util(arr):
    return


def cast_int16(arr):
    return


def cast_int16_util(arr):
    return


def cast_int8(arr):
    return


def cast_int8_util(arr):
    return


def cast_boolean(arr):
    return


def cast_char(arr):
    return


def cast_date(arr):
    return arr


def cast_timestamp(arr):
    return


def cast_interval(arr):
    return


def cast_interval_util(arr):
    return


cast_funcs_utils_names = (cast_float64, cast_float64_util, 'float64'), (
    cast_float32, cast_float32_util, 'float32'), (cast_int64,
    cast_int64_util, 'int64'), (cast_int32, cast_int32_util, 'int32'), (
    cast_int16, cast_int16_util, 'int16'), (cast_int8, cast_int8_util, 'int8'
    ), (cast_boolean, None, 'boolean'), (cast_char, None, 'char'), (cast_date,
    None, 'date'), (cast_timestamp, None, 'timestamp'), (cast_interval,
    cast_interval, 'interval')
fname_to_equiv = {'float64': 'np.float64', 'float32': 'np.float32', 'int64':
    'np.int64', 'int32': 'np.int32', 'int16': 'np.int16', 'int8': 'np.int8',
    'interval': 'pd.to_timedelta'}
fname_to_dtype = {'float64': types.Array(bodo.float64, 1, 'C'), 'float32':
    types.Array(bodo.float32, 1, 'C'), 'int64': bodo.libs.int_arr_ext.
    IntegerArrayType(types.int64), 'int32': bodo.libs.int_arr_ext.
    IntegerArrayType(types.int32), 'int16': bodo.libs.int_arr_ext.
    IntegerArrayType(types.int16), 'int8': bodo.libs.int_arr_ext.
    IntegerArrayType(types.int8), 'interval': np.dtype('timedelta64[ns]')}


def create_cast_func_overload(func_name):

    def overload_cast_func(arr):
        if isinstance(arr, types.optional):
            return unopt_argument(
                f'bodo.libs.bodosql_array_kernels.cast_{func_name}', ['arr'], 0
                )
        zym__xtxo = 'def impl(arr):\n'
        if func_name == 'boolean':
            zym__xtxo += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_boolean_util(arr, numba.literally(True))
"""
        elif func_name == 'char':
            zym__xtxo += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_char_util(arr)
"""
        elif func_name == 'date':
            zym__xtxo += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_date_util(arr, None, numba.literally(True), numba.literally(False))
"""
        elif func_name == 'timestamp':
            zym__xtxo += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_date_util(arr, None, numba.literally(False), numba.literally(True))
"""
        else:
            zym__xtxo += (
                f'  return bodo.libs.bodosql_array_kernels.cast_{func_name}_util(arr)'
                )
        qdaz__guvq = {}
        exec(zym__xtxo, {'bodo': bodo, 'numba': numba}, qdaz__guvq)
        return qdaz__guvq['impl']
    return overload_cast_func


def create_cast_util_overload(func_name):

    def overload_cast_util(arr):
        jftd__dhbm = ['arr']
        ktatg__ulpb = [arr]
        mqfq__sav = [True]
        hgb__eojna = ''
        if func_name[:3
            ] == 'int' and func_name != 'interval' and not is_valid_boolean_arg(
            arr):
            if is_valid_int_arg(arr):
                hgb__eojna += """if arg0 < np.iinfo(np.int64).min or arg0 > np.iinfo(np.int64).max:
"""
                hgb__eojna += '  bodo.libs.array_kernels.setna(res, i)\n'
                hgb__eojna += 'else:\n'
                hgb__eojna += f'  res[i] = {fname_to_equiv[func_name]}(arg0)\n'
            else:
                if is_valid_string_arg(arr):
                    hgb__eojna = 'i_val = 0\n'
                    hgb__eojna += 'f_val = np.float64(arg0)\n'
                    hgb__eojna += """is_valid = not (pd.isna(f_val) or np.isinf(f_val) or f_val < np.iinfo(np.int64).min or f_val > np.iinfo(np.int64).max)
"""
                    hgb__eojna += 'is_int = (f_val % 1 == 0)\n'
                    hgb__eojna += 'if not (is_valid and is_int):\n'
                    hgb__eojna += '  val = f_val\n'
                    hgb__eojna += 'else:\n'
                    hgb__eojna += '  val = np.int64(arg0)\n'
                    hgb__eojna += '  i_val = np.int64(arg0)\n'
                else:
                    if not is_valid_float_arg(arr):
                        raise BodoError(
                            'only strings, floats, booleans, and ints can be cast to ints'
                            )
                    hgb__eojna += 'val = arg0\n'
                    hgb__eojna += """is_valid = not(pd.isna(val) or np.isinf(val) or val < np.iinfo(np.int64).min or val > np.iinfo(np.int64).max)
"""
                    hgb__eojna += 'is_int = (val % 1 == 0)\n'
                hgb__eojna += 'if not is_valid:\n'
                hgb__eojna += '  bodo.libs.array_kernels.setna(res, i)\n'
                hgb__eojna += 'else:\n'
                if is_valid_float_arg(arr):
                    hgb__eojna += '  i_val = np.int64(val)\n'
                hgb__eojna += '  if not is_int:\n'
                hgb__eojna += (
                    '    ans = np.int64(np.sign(val) * np.floor(np.abs(val) + 0.5))\n'
                    )
                hgb__eojna += '  else:\n'
                hgb__eojna += '    ans = i_val\n'
                if func_name == 'int64':
                    hgb__eojna += f'  res[i] = ans\n'
                else:
                    hgb__eojna += (
                        f'  res[i] = {fname_to_equiv[func_name]}(ans)')
        elif func_name == 'interval':
            fqjm__watzu = (
                'bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
                .utils.utils.is_array_typ(arr, True) else '')
            hgb__eojna += f'res[i] = {fqjm__watzu}(pd.to_timedelta(arg0))'
        else:
            hgb__eojna += f'res[i] = {fname_to_equiv[func_name]}(arg0)'
        jzvu__fvv = fname_to_dtype[func_name]
        return gen_vectorized(jftd__dhbm, ktatg__ulpb, mqfq__sav,
            hgb__eojna, jzvu__fvv)
    return overload_cast_util


def _install_cast_func_overloads(funcs_utils_names):
    for sebi__usp, kea__dpwyj, bgqw__okmgm in funcs_utils_names:
        overload(sebi__usp)(create_cast_func_overload(bgqw__okmgm))
        if bgqw__okmgm not in ('boolean', 'char', 'date', 'timestamp'):
            overload(kea__dpwyj)(create_cast_util_overload(bgqw__okmgm))


_install_cast_func_overloads(cast_funcs_utils_names)
