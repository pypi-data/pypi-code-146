from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


def acos(arr):
    return


def acosh(arr):
    return


def asin(arr):
    return


def asinh(arr):
    return


def atan(arr):
    return


def atanh(arr):
    return


def atan2(arr0, arr1):
    return


def cos(arr):
    return


def cosh(arr):
    return


def sin(arr):
    return


def sinh(arr):
    return


def tan(arr):
    return


def tanh(arr):
    return


def radians(arr):
    return


def degrees(arr):
    return


def acos_util(arr):
    return


def acosh_util(arr):
    return


def asin_util(arr):
    return


def asinh_util(arr):
    return


def atan_util(arr):
    return


def atanh_util(arr):
    return


def atan2_util(arr0, arr1):
    return


def cos_util(arr):
    return


def cosh_util(arr):
    return


def sin_util(arr):
    return


def sinh_util(arr):
    return


def tan_util(arr):
    return


def tanh_util(arr):
    return


def radians_util(arr):
    return


def degrees_util(arr):
    return


funcs_utils_names = (acos, acos_util, 'ACOS'), (acosh, acosh_util, 'ACOSH'), (
    asin, asin_util, 'ASIN'), (asinh, asinh_util, 'ASINH'), (atan,
    atan_util, 'ATAN'), (atanh, atanh_util, 'ATANH'), (atan2, atan2_util,
    'ATAN2'), (cos, cos_util, 'COS'), (cosh, cosh_util, 'COSH'), (sin,
    sin_util, 'SIN'), (sinh, sinh_util, 'SINH'), (tan, tan_util, 'TAN'), (tanh,
    tanh_util, 'TANH'), (radians, radians_util, 'RADIANS'), (degrees,
    degrees_util, 'DEGREES')
double_arg_funcs = 'ATAN2',


def create_trig_func_overload(func_name):
    if func_name not in double_arg_funcs:
        func_name = func_name.lower()

        def overload_func(arr):
            if isinstance(arr, types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.{func_name}', ['arr'], 0)
            gfnnq__rhgc = 'def impl(arr):\n'
            gfnnq__rhgc += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr)'
                )
            fwhk__hxjjj = {}
            exec(gfnnq__rhgc, {'bodo': bodo}, fwhk__hxjjj)
            return fwhk__hxjjj['impl']
    else:
        func_name = func_name.lower()

        def overload_func(arr0, arr1):
            args = [arr0, arr1]
            for oujej__dhkfd in range(2):
                if isinstance(args[oujej__dhkfd], types.optional):
                    return unopt_argument(
                        f'bodo.libs.bodosql_array_kernels.{func_name}', [
                        'arr0', 'arr1'], oujej__dhkfd)
            gfnnq__rhgc = 'def impl(arr0, arr1):\n'
            gfnnq__rhgc += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr0, arr1)'
                )
            fwhk__hxjjj = {}
            exec(gfnnq__rhgc, {'bodo': bodo}, fwhk__hxjjj)
            return fwhk__hxjjj['impl']
    return overload_func


def create_trig_util_overload(func_name):
    if func_name not in double_arg_funcs:

        def overload_trig_util(arr):
            verify_int_float_arg(arr, func_name, 'arr')
            faau__wjjlw = ['arr']
            swlf__opn = [arr]
            hjsl__vzh = [True]
            wcsc__maj = ''
            if func_name == 'ACOS':
                wcsc__maj += 'res[i] = np.arccos(arg0)'
            elif func_name == 'ACOSH':
                wcsc__maj += 'res[i] = np.arccosh(arg0)'
            elif func_name == 'ASIN':
                wcsc__maj += 'res[i] = np.arcsin(arg0)'
            elif func_name == 'ASINH':
                wcsc__maj += 'res[i] = np.arcsinh(arg0)'
            elif func_name == 'ATAN':
                wcsc__maj += 'res[i] = np.arctan(arg0)'
            elif func_name == 'ATANH':
                wcsc__maj += 'res[i] = np.arctanh(arg0)'
            elif func_name == 'COS':
                wcsc__maj += 'res[i] = np.cos(arg0)'
            elif func_name == 'COSH':
                wcsc__maj += 'res[i] = np.cosh(arg0)'
            elif func_name == 'SIN':
                wcsc__maj += 'res[i] = np.sin(arg0)'
            elif func_name == 'SINH':
                wcsc__maj += 'res[i] = np.sinh(arg0)'
            elif func_name == 'TAN':
                wcsc__maj += 'res[i] = np.tan(arg0)'
            elif func_name == 'TANH':
                wcsc__maj += 'res[i] = np.tanh(arg0)'
            elif func_name == 'RADIANS':
                wcsc__maj += 'res[i] = np.radians(arg0)'
            elif func_name == 'DEGREES':
                wcsc__maj += 'res[i] = np.degrees(arg0)'
            else:
                raise ValueError(f'Unknown function name: {func_name}')
            ntzif__urx = types.Array(bodo.float64, 1, 'C')
            return gen_vectorized(faau__wjjlw, swlf__opn, hjsl__vzh,
                wcsc__maj, ntzif__urx)
    else:

        def overload_trig_util(arr0, arr1):
            verify_int_float_arg(arr0, func_name, 'arr0')
            verify_int_float_arg(arr1, func_name, 'arr1')
            faau__wjjlw = ['arr0', 'arr1']
            swlf__opn = [arr0, arr1]
            hjsl__vzh = [True, True]
            wcsc__maj = ''
            if func_name == 'ATAN2':
                wcsc__maj += 'res[i] = np.arctan2(arg0, arg1)\n'
            else:
                raise ValueError(f'Unknown function name: {func_name}')
            ntzif__urx = types.Array(bodo.float64, 1, 'C')
            return gen_vectorized(faau__wjjlw, swlf__opn, hjsl__vzh,
                wcsc__maj, ntzif__urx)
    return overload_trig_util


def _install_trig_overload(funcs_utils_names):
    for mch__abb, ewtx__xunqj, func_name in funcs_utils_names:
        xqbpc__whkfg = create_trig_func_overload(func_name)
        overload(mch__abb)(xqbpc__whkfg)
        eai__zlmp = create_trig_util_overload(func_name)
        overload(ewtx__xunqj)(eai__zlmp)


_install_trig_overload(funcs_utils_names)
