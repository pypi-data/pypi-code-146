"""
Implements miscellaneous array kernels that are specific to BodoSQL
"""
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import raise_bodo_error


@numba.generated_jit(nopython=True)
def booland(A, B):
    args = [A, B]
    for rjh__mcgie in range(2):
        if isinstance(args[rjh__mcgie], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.booland',
                ['A', 'B'], rjh__mcgie)

    def impl(A, B):
        return booland_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolor(A, B):
    args = [A, B]
    for rjh__mcgie in range(2):
        if isinstance(args[rjh__mcgie], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolor',
                ['A', 'B'], rjh__mcgie)

    def impl(A, B):
        return boolor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolxor(A, B):
    args = [A, B]
    for rjh__mcgie in range(2):
        if isinstance(args[rjh__mcgie], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolxor',
                ['A', 'B'], rjh__mcgie)

    def impl(A, B):
        return boolxor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolnot(A):
    if isinstance(A, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.boolnot_util',
            ['A'], 0)

    def impl(A):
        return boolnot_util(A)
    return impl


@numba.generated_jit(nopython=True)
def cond(arr, ifbranch, elsebranch):
    args = [arr, ifbranch, elsebranch]
    for rjh__mcgie in range(3):
        if isinstance(args[rjh__mcgie], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.cond', [
                'arr', 'ifbranch', 'elsebranch'], rjh__mcgie)

    def impl(arr, ifbranch, elsebranch):
        return cond_util(arr, ifbranch, elsebranch)
    return impl


@numba.generated_jit(nopython=True)
def equal_null(A, B):
    args = [A, B]
    for rjh__mcgie in range(2):
        if isinstance(args[rjh__mcgie], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.equal_null',
                ['A', 'B'], rjh__mcgie)

    def impl(A, B):
        return equal_null_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def booland_util(A, B):
    verify_int_float_arg(A, 'BOOLAND', 'A')
    verify_int_float_arg(B, 'BOOLAND', 'B')
    akbuo__miuyw = ['A', 'B']
    hja__jvs = [A, B]
    tciy__car = [False] * 2
    if A == bodo.none:
        tciy__car = [False, True]
        ekhul__ykww = 'if arg1 != 0:\n'
        ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
        ekhul__ykww += 'else:\n'
        ekhul__ykww += '   res[i] = False\n'
    elif B == bodo.none:
        tciy__car = [True, False]
        ekhul__ykww = 'if arg0 != 0:\n'
        ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
        ekhul__ykww += 'else:\n'
        ekhul__ykww += '   res[i] = False\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            ekhul__ykww = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
            ekhul__ykww += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
            ekhul__ykww += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
            ekhul__ykww += 'else:\n'
            ekhul__ykww += '   res[i] = (arg0 != 0) and (arg1 != 0)'
        else:
            ekhul__ykww = (
                'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
            ekhul__ykww += 'else:\n'
            ekhul__ykww += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        ekhul__ykww = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
        ekhul__ykww += 'else:\n'
        ekhul__ykww += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    else:
        ekhul__ykww = 'res[i] = (arg0 != 0) and (arg1 != 0)'
    koee__mavi = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(akbuo__miuyw, hja__jvs, tciy__car, ekhul__ykww,
        koee__mavi)


@numba.generated_jit(nopython=True)
def boolor_util(A, B):
    verify_int_float_arg(A, 'BOOLOR', 'A')
    verify_int_float_arg(B, 'BOOLOR', 'B')
    akbuo__miuyw = ['A', 'B']
    hja__jvs = [A, B]
    tciy__car = [False] * 2
    if A == bodo.none:
        tciy__car = [False, True]
        ekhul__ykww = 'if arg1 == 0:\n'
        ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
        ekhul__ykww += 'else:\n'
        ekhul__ykww += '   res[i] = True\n'
    elif B == bodo.none:
        tciy__car = [True, False]
        ekhul__ykww = 'if arg0 == 0:\n'
        ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
        ekhul__ykww += 'else:\n'
        ekhul__ykww += '   res[i] = True\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            ekhul__ykww = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
            ekhul__ykww += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            ekhul__ykww += '   res[i] = True\n'
            ekhul__ykww += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
            ekhul__ykww += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            ekhul__ykww += '   res[i] = True\n'
            ekhul__ykww += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
            ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
            ekhul__ykww += 'else:\n'
            ekhul__ykww += '   res[i] = (arg0 != 0) or (arg1 != 0)'
        else:
            ekhul__ykww = (
                'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            ekhul__ykww += '   res[i] = True\n'
            ekhul__ykww += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
            ekhul__ykww += 'else:\n'
            ekhul__ykww += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        ekhul__ykww = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        ekhul__ykww += '   res[i] = True\n'
        ekhul__ykww += (
            'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
        ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
        ekhul__ykww += 'else:\n'
        ekhul__ykww += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    else:
        ekhul__ykww = 'res[i] = (arg0 != 0) or (arg1 != 0)'
    koee__mavi = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(akbuo__miuyw, hja__jvs, tciy__car, ekhul__ykww,
        koee__mavi)


@numba.generated_jit(nopython=True)
def boolxor_util(A, B):
    verify_int_float_arg(A, 'BOOLXOR', 'A')
    verify_int_float_arg(B, 'BOOLXOR', 'B')
    akbuo__miuyw = ['A', 'B']
    hja__jvs = [A, B]
    tciy__car = [True] * 2
    ekhul__ykww = 'res[i] = (arg0 == 0) != (arg1 == 0)'
    koee__mavi = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(akbuo__miuyw, hja__jvs, tciy__car, ekhul__ykww,
        koee__mavi)


@numba.generated_jit(nopython=True)
def boolnot_util(A):
    verify_int_float_arg(A, 'BOOLNOT', 'A')
    akbuo__miuyw = ['A']
    hja__jvs = [A]
    tciy__car = [True]
    ekhul__ykww = 'res[i] = arg0 == 0'
    koee__mavi = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(akbuo__miuyw, hja__jvs, tciy__car, ekhul__ykww,
        koee__mavi)


@numba.generated_jit(nopython=True)
def nullif(arr0, arr1):
    args = [arr0, arr1]
    for rjh__mcgie in range(2):
        if isinstance(args[rjh__mcgie], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.nullif',
                ['arr0', 'arr1'], rjh__mcgie)

    def impl(arr0, arr1):
        return nullif_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def regr_valx(y, x):
    args = [y, x]
    for rjh__mcgie in range(2):
        if isinstance(args[rjh__mcgie], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valx',
                ['y', 'x'], rjh__mcgie)

    def impl(y, x):
        return regr_valx_util(y, x)
    return impl


@numba.generated_jit(nopython=True)
def regr_valy(y, x):
    args = [y, x]
    for rjh__mcgie in range(2):
        if isinstance(args[rjh__mcgie], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valy',
                ['y', 'x'], rjh__mcgie)

    def impl(y, x):
        return regr_valx(x, y)
    return impl


@numba.generated_jit(nopython=True)
def cond_util(arr, ifbranch, elsebranch):
    verify_boolean_arg(arr, 'cond', 'arr')
    if bodo.utils.utils.is_array_typ(arr, True
        ) and ifbranch == bodo.none and elsebranch == bodo.none:
        raise_bodo_error('Both branches of IF() cannot be scalar NULL')
    akbuo__miuyw = ['arr', 'ifbranch', 'elsebranch']
    hja__jvs = [arr, ifbranch, elsebranch]
    tciy__car = [False] * 3
    if bodo.utils.utils.is_array_typ(arr, True):
        ekhul__ykww = (
            'if (not bodo.libs.array_kernels.isna(arr, i)) and arg0:\n')
    elif arr != bodo.none:
        ekhul__ykww = 'if arg0:\n'
    else:
        ekhul__ykww = ''
    if arr != bodo.none:
        if bodo.utils.utils.is_array_typ(ifbranch, True):
            ekhul__ykww += '   if bodo.libs.array_kernels.isna(ifbranch, i):\n'
            ekhul__ykww += '      bodo.libs.array_kernels.setna(res, i)\n'
            ekhul__ykww += '   else:\n'
            ekhul__ykww += '      res[i] = arg1\n'
        elif ifbranch == bodo.none:
            ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
        else:
            ekhul__ykww += '   res[i] = arg1\n'
        ekhul__ykww += 'else:\n'
    if bodo.utils.utils.is_array_typ(elsebranch, True):
        ekhul__ykww += '   if bodo.libs.array_kernels.isna(elsebranch, i):\n'
        ekhul__ykww += '      bodo.libs.array_kernels.setna(res, i)\n'
        ekhul__ykww += '   else:\n'
        ekhul__ykww += '      res[i] = arg2\n'
    elif elsebranch == bodo.none:
        ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)\n'
    else:
        ekhul__ykww += '   res[i] = arg2\n'
    koee__mavi = get_common_broadcasted_type([ifbranch, elsebranch], 'IF')
    return gen_vectorized(akbuo__miuyw, hja__jvs, tciy__car, ekhul__ykww,
        koee__mavi)


@numba.generated_jit(nopython=True)
def equal_null_util(A, B):
    get_common_broadcasted_type([A, B], 'EQUAL_NULL')
    akbuo__miuyw = ['A', 'B']
    hja__jvs = [A, B]
    tciy__car = [False] * 2
    if A == bodo.none:
        if B == bodo.none:
            ekhul__ykww = 'res[i] = True'
        elif bodo.utils.utils.is_array_typ(B, True):
            ekhul__ykww = 'res[i] = bodo.libs.array_kernels.isna(B, i)'
        else:
            ekhul__ykww = 'res[i] = False'
    elif B == bodo.none:
        if bodo.utils.utils.is_array_typ(A, True):
            ekhul__ykww = 'res[i] = bodo.libs.array_kernels.isna(A, i)'
        else:
            ekhul__ykww = 'res[i] = False'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            ekhul__ykww = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            ekhul__ykww += '   res[i] = True\n'
            ekhul__ykww += """elif bodo.libs.array_kernels.isna(A, i) or bodo.libs.array_kernels.isna(B, i):
"""
            ekhul__ykww += '   res[i] = False\n'
            ekhul__ykww += 'else:\n'
            ekhul__ykww += '   res[i] = arg0 == arg1'
        else:
            ekhul__ykww = (
                'res[i] = (not bodo.libs.array_kernels.isna(A, i)) and arg0 == arg1'
                )
    elif bodo.utils.utils.is_array_typ(B, True):
        ekhul__ykww = (
            'res[i] = (not bodo.libs.array_kernels.isna(B, i)) and arg0 == arg1'
            )
    else:
        ekhul__ykww = 'res[i] = arg0 == arg1'
    koee__mavi = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(akbuo__miuyw, hja__jvs, tciy__car, ekhul__ykww,
        koee__mavi)


@numba.generated_jit(nopython=True)
def nullif_util(arr0, arr1):
    akbuo__miuyw = ['arr0', 'arr1']
    hja__jvs = [arr0, arr1]
    tciy__car = [True, False]
    if arr1 == bodo.none:
        ekhul__ykww = 'res[i] = arg0\n'
    elif bodo.utils.utils.is_array_typ(arr1, True):
        ekhul__ykww = (
            'if bodo.libs.array_kernels.isna(arr1, i) or arg0 != arg1:\n')
        ekhul__ykww += '   res[i] = arg0\n'
        ekhul__ykww += 'else:\n'
        ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)'
    else:
        ekhul__ykww = 'if arg0 != arg1:\n'
        ekhul__ykww += '   res[i] = arg0\n'
        ekhul__ykww += 'else:\n'
        ekhul__ykww += '   bodo.libs.array_kernels.setna(res, i)'
    koee__mavi = get_common_broadcasted_type([arr0, arr1], 'NULLIF')
    return gen_vectorized(akbuo__miuyw, hja__jvs, tciy__car, ekhul__ykww,
        koee__mavi)


@numba.generated_jit(nopython=True)
def regr_valx_util(y, x):
    verify_int_float_arg(y, 'regr_valx', 'y')
    verify_int_float_arg(x, 'regr_valx', 'x')
    akbuo__miuyw = ['y', 'x']
    hja__jvs = [y, x]
    ckkr__oqqge = [True] * 2
    ekhul__ykww = 'res[i] = arg1'
    koee__mavi = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(akbuo__miuyw, hja__jvs, ckkr__oqqge, ekhul__ykww,
        koee__mavi)
