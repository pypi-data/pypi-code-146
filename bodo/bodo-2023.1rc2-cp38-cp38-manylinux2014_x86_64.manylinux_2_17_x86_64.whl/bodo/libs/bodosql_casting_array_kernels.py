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
        mbzq__lcuak = 'def impl(arr):\n'
        if func_name == 'boolean':
            mbzq__lcuak += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_boolean_util(arr, numba.literally(True))
"""
        elif func_name == 'char':
            mbzq__lcuak += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_char_util(arr)
"""
        elif func_name == 'date':
            mbzq__lcuak += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_date_util(arr, None, numba.literally(True), numba.literally(False))
"""
        elif func_name == 'timestamp':
            mbzq__lcuak += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_date_util(arr, None, numba.literally(False), numba.literally(True))
"""
        else:
            mbzq__lcuak += (
                f'  return bodo.libs.bodosql_array_kernels.cast_{func_name}_util(arr)'
                )
        wrsp__hyir = {}
        exec(mbzq__lcuak, {'bodo': bodo, 'numba': numba}, wrsp__hyir)
        return wrsp__hyir['impl']
    return overload_cast_func


def create_cast_util_overload(func_name):

    def overload_cast_util(arr):
        mvdf__oyk = ['arr']
        fsxk__dzejb = [arr]
        ypvii__dyck = [True]
        noahq__btk = ''
        if func_name[:3
            ] == 'int' and func_name != 'interval' and not is_valid_boolean_arg(
            arr):
            if is_valid_int_arg(arr):
                noahq__btk += """if arg0 < np.iinfo(np.int64).min or arg0 > np.iinfo(np.int64).max:
"""
                noahq__btk += '  bodo.libs.array_kernels.setna(res, i)\n'
                noahq__btk += 'else:\n'
                noahq__btk += f'  res[i] = {fname_to_equiv[func_name]}(arg0)\n'
            else:
                if is_valid_string_arg(arr):
                    noahq__btk = 'i_val = 0\n'
                    noahq__btk += 'f_val = np.float64(arg0)\n'
                    noahq__btk += """is_valid = not (pd.isna(f_val) or np.isinf(f_val) or f_val < np.iinfo(np.int64).min or f_val > np.iinfo(np.int64).max)
"""
                    noahq__btk += 'is_int = (f_val % 1 == 0)\n'
                    noahq__btk += 'if not (is_valid and is_int):\n'
                    noahq__btk += '  val = f_val\n'
                    noahq__btk += 'else:\n'
                    noahq__btk += '  val = np.int64(arg0)\n'
                    noahq__btk += '  i_val = np.int64(arg0)\n'
                else:
                    if not is_valid_float_arg(arr):
                        raise BodoError(
                            'only strings, floats, booleans, and ints can be cast to ints'
                            )
                    noahq__btk += 'val = arg0\n'
                    noahq__btk += """is_valid = not(pd.isna(val) or np.isinf(val) or val < np.iinfo(np.int64).min or val > np.iinfo(np.int64).max)
"""
                    noahq__btk += 'is_int = (val % 1 == 0)\n'
                noahq__btk += 'if not is_valid:\n'
                noahq__btk += '  bodo.libs.array_kernels.setna(res, i)\n'
                noahq__btk += 'else:\n'
                if is_valid_float_arg(arr):
                    noahq__btk += '  i_val = np.int64(val)\n'
                noahq__btk += '  if not is_int:\n'
                noahq__btk += (
                    '    ans = np.int64(np.sign(val) * np.floor(np.abs(val) + 0.5))\n'
                    )
                noahq__btk += '  else:\n'
                noahq__btk += '    ans = i_val\n'
                if func_name == 'int64':
                    noahq__btk += f'  res[i] = ans\n'
                else:
                    noahq__btk += (
                        f'  res[i] = {fname_to_equiv[func_name]}(ans)')
        elif func_name == 'interval':
            psdhs__arkyc = (
                'bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
                .utils.utils.is_array_typ(arr, True) else '')
            noahq__btk += f'res[i] = {psdhs__arkyc}(pd.to_timedelta(arg0))'
        else:
            noahq__btk += f'res[i] = {fname_to_equiv[func_name]}(arg0)'
        kdm__antuj = fname_to_dtype[func_name]
        return gen_vectorized(mvdf__oyk, fsxk__dzejb, ypvii__dyck,
            noahq__btk, kdm__antuj)
    return overload_cast_util


def _install_cast_func_overloads(funcs_utils_names):
    for ltp__bux, pbf__mrks, kpmvo__jsq in funcs_utils_names:
        overload(ltp__bux)(create_cast_func_overload(kpmvo__jsq))
        if kpmvo__jsq not in ('boolean', 'char', 'date', 'timestamp'):
            overload(pbf__mrks)(create_cast_util_overload(kpmvo__jsq))


_install_cast_func_overloads(cast_funcs_utils_names)
