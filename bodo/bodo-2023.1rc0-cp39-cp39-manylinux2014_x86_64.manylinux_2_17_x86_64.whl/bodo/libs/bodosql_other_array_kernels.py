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
    for bqv__sac in range(2):
        if isinstance(args[bqv__sac], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.booland',
                ['A', 'B'], bqv__sac)

    def impl(A, B):
        return booland_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolor(A, B):
    args = [A, B]
    for bqv__sac in range(2):
        if isinstance(args[bqv__sac], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolor',
                ['A', 'B'], bqv__sac)

    def impl(A, B):
        return boolor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolxor(A, B):
    args = [A, B]
    for bqv__sac in range(2):
        if isinstance(args[bqv__sac], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolxor',
                ['A', 'B'], bqv__sac)

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
    for bqv__sac in range(3):
        if isinstance(args[bqv__sac], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.cond', [
                'arr', 'ifbranch', 'elsebranch'], bqv__sac)

    def impl(arr, ifbranch, elsebranch):
        return cond_util(arr, ifbranch, elsebranch)
    return impl


@numba.generated_jit(nopython=True)
def equal_null(A, B):
    args = [A, B]
    for bqv__sac in range(2):
        if isinstance(args[bqv__sac], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.equal_null',
                ['A', 'B'], bqv__sac)

    def impl(A, B):
        return equal_null_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def booland_util(A, B):
    verify_int_float_arg(A, 'BOOLAND', 'A')
    verify_int_float_arg(B, 'BOOLAND', 'B')
    tytu__ufwe = ['A', 'B']
    dyq__dond = [A, B]
    gha__uloln = [False] * 2
    if A == bodo.none:
        gha__uloln = [False, True]
        dww__msqvo = 'if arg1 != 0:\n'
        dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
        dww__msqvo += 'else:\n'
        dww__msqvo += '   res[i] = False\n'
    elif B == bodo.none:
        gha__uloln = [True, False]
        dww__msqvo = 'if arg0 != 0:\n'
        dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
        dww__msqvo += 'else:\n'
        dww__msqvo += '   res[i] = False\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            dww__msqvo = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
            dww__msqvo += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
            dww__msqvo += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
            dww__msqvo += 'else:\n'
            dww__msqvo += '   res[i] = (arg0 != 0) and (arg1 != 0)'
        else:
            dww__msqvo = (
                'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
            dww__msqvo += 'else:\n'
            dww__msqvo += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        dww__msqvo = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
        dww__msqvo += 'else:\n'
        dww__msqvo += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    else:
        dww__msqvo = 'res[i] = (arg0 != 0) and (arg1 != 0)'
    tbhnn__qnaso = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(tytu__ufwe, dyq__dond, gha__uloln, dww__msqvo,
        tbhnn__qnaso)


@numba.generated_jit(nopython=True)
def boolor_util(A, B):
    verify_int_float_arg(A, 'BOOLOR', 'A')
    verify_int_float_arg(B, 'BOOLOR', 'B')
    tytu__ufwe = ['A', 'B']
    dyq__dond = [A, B]
    gha__uloln = [False] * 2
    if A == bodo.none:
        gha__uloln = [False, True]
        dww__msqvo = 'if arg1 == 0:\n'
        dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
        dww__msqvo += 'else:\n'
        dww__msqvo += '   res[i] = True\n'
    elif B == bodo.none:
        gha__uloln = [True, False]
        dww__msqvo = 'if arg0 == 0:\n'
        dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
        dww__msqvo += 'else:\n'
        dww__msqvo += '   res[i] = True\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            dww__msqvo = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
            dww__msqvo += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            dww__msqvo += '   res[i] = True\n'
            dww__msqvo += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
            dww__msqvo += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            dww__msqvo += '   res[i] = True\n'
            dww__msqvo += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
            dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
            dww__msqvo += 'else:\n'
            dww__msqvo += '   res[i] = (arg0 != 0) or (arg1 != 0)'
        else:
            dww__msqvo = (
                'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            dww__msqvo += '   res[i] = True\n'
            dww__msqvo += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
            dww__msqvo += 'else:\n'
            dww__msqvo += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        dww__msqvo = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        dww__msqvo += '   res[i] = True\n'
        dww__msqvo += (
            'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
        dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
        dww__msqvo += 'else:\n'
        dww__msqvo += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    else:
        dww__msqvo = 'res[i] = (arg0 != 0) or (arg1 != 0)'
    tbhnn__qnaso = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(tytu__ufwe, dyq__dond, gha__uloln, dww__msqvo,
        tbhnn__qnaso)


@numba.generated_jit(nopython=True)
def boolxor_util(A, B):
    verify_int_float_arg(A, 'BOOLXOR', 'A')
    verify_int_float_arg(B, 'BOOLXOR', 'B')
    tytu__ufwe = ['A', 'B']
    dyq__dond = [A, B]
    gha__uloln = [True] * 2
    dww__msqvo = 'res[i] = (arg0 == 0) != (arg1 == 0)'
    tbhnn__qnaso = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(tytu__ufwe, dyq__dond, gha__uloln, dww__msqvo,
        tbhnn__qnaso)


@numba.generated_jit(nopython=True)
def boolnot_util(A):
    verify_int_float_arg(A, 'BOOLNOT', 'A')
    tytu__ufwe = ['A']
    dyq__dond = [A]
    gha__uloln = [True]
    dww__msqvo = 'res[i] = arg0 == 0'
    tbhnn__qnaso = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(tytu__ufwe, dyq__dond, gha__uloln, dww__msqvo,
        tbhnn__qnaso)


@numba.generated_jit(nopython=True)
def nullif(arr0, arr1):
    args = [arr0, arr1]
    for bqv__sac in range(2):
        if isinstance(args[bqv__sac], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.nullif',
                ['arr0', 'arr1'], bqv__sac)

    def impl(arr0, arr1):
        return nullif_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def regr_valx(y, x):
    args = [y, x]
    for bqv__sac in range(2):
        if isinstance(args[bqv__sac], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valx',
                ['y', 'x'], bqv__sac)

    def impl(y, x):
        return regr_valx_util(y, x)
    return impl


@numba.generated_jit(nopython=True)
def regr_valy(y, x):
    args = [y, x]
    for bqv__sac in range(2):
        if isinstance(args[bqv__sac], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valy',
                ['y', 'x'], bqv__sac)

    def impl(y, x):
        return regr_valx(x, y)
    return impl


@numba.generated_jit(nopython=True)
def cond_util(arr, ifbranch, elsebranch):
    verify_boolean_arg(arr, 'cond', 'arr')
    if bodo.utils.utils.is_array_typ(arr, True
        ) and ifbranch == bodo.none and elsebranch == bodo.none:
        raise_bodo_error('Both branches of IF() cannot be scalar NULL')
    tytu__ufwe = ['arr', 'ifbranch', 'elsebranch']
    dyq__dond = [arr, ifbranch, elsebranch]
    gha__uloln = [False] * 3
    if bodo.utils.utils.is_array_typ(arr, True):
        dww__msqvo = (
            'if (not bodo.libs.array_kernels.isna(arr, i)) and arg0:\n')
    elif arr != bodo.none:
        dww__msqvo = 'if arg0:\n'
    else:
        dww__msqvo = ''
    if arr != bodo.none:
        if bodo.utils.utils.is_array_typ(ifbranch, True):
            dww__msqvo += '   if bodo.libs.array_kernels.isna(ifbranch, i):\n'
            dww__msqvo += '      bodo.libs.array_kernels.setna(res, i)\n'
            dww__msqvo += '   else:\n'
            dww__msqvo += '      res[i] = arg1\n'
        elif ifbranch == bodo.none:
            dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
        else:
            dww__msqvo += '   res[i] = arg1\n'
        dww__msqvo += 'else:\n'
    if bodo.utils.utils.is_array_typ(elsebranch, True):
        dww__msqvo += '   if bodo.libs.array_kernels.isna(elsebranch, i):\n'
        dww__msqvo += '      bodo.libs.array_kernels.setna(res, i)\n'
        dww__msqvo += '   else:\n'
        dww__msqvo += '      res[i] = arg2\n'
    elif elsebranch == bodo.none:
        dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)\n'
    else:
        dww__msqvo += '   res[i] = arg2\n'
    tbhnn__qnaso = get_common_broadcasted_type([ifbranch, elsebranch], 'IF')
    return gen_vectorized(tytu__ufwe, dyq__dond, gha__uloln, dww__msqvo,
        tbhnn__qnaso)


@numba.generated_jit(nopython=True)
def equal_null_util(A, B):
    get_common_broadcasted_type([A, B], 'EQUAL_NULL')
    tytu__ufwe = ['A', 'B']
    dyq__dond = [A, B]
    gha__uloln = [False] * 2
    if A == bodo.none:
        if B == bodo.none:
            dww__msqvo = 'res[i] = True'
        elif bodo.utils.utils.is_array_typ(B, True):
            dww__msqvo = 'res[i] = bodo.libs.array_kernels.isna(B, i)'
        else:
            dww__msqvo = 'res[i] = False'
    elif B == bodo.none:
        if bodo.utils.utils.is_array_typ(A, True):
            dww__msqvo = 'res[i] = bodo.libs.array_kernels.isna(A, i)'
        else:
            dww__msqvo = 'res[i] = False'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            dww__msqvo = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            dww__msqvo += '   res[i] = True\n'
            dww__msqvo += """elif bodo.libs.array_kernels.isna(A, i) or bodo.libs.array_kernels.isna(B, i):
"""
            dww__msqvo += '   res[i] = False\n'
            dww__msqvo += 'else:\n'
            dww__msqvo += '   res[i] = arg0 == arg1'
        else:
            dww__msqvo = (
                'res[i] = (not bodo.libs.array_kernels.isna(A, i)) and arg0 == arg1'
                )
    elif bodo.utils.utils.is_array_typ(B, True):
        dww__msqvo = (
            'res[i] = (not bodo.libs.array_kernels.isna(B, i)) and arg0 == arg1'
            )
    else:
        dww__msqvo = 'res[i] = arg0 == arg1'
    tbhnn__qnaso = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(tytu__ufwe, dyq__dond, gha__uloln, dww__msqvo,
        tbhnn__qnaso)


@numba.generated_jit(nopython=True)
def nullif_util(arr0, arr1):
    tytu__ufwe = ['arr0', 'arr1']
    dyq__dond = [arr0, arr1]
    gha__uloln = [True, False]
    if arr1 == bodo.none:
        dww__msqvo = 'res[i] = arg0\n'
    elif bodo.utils.utils.is_array_typ(arr1, True):
        dww__msqvo = (
            'if bodo.libs.array_kernels.isna(arr1, i) or arg0 != arg1:\n')
        dww__msqvo += '   res[i] = arg0\n'
        dww__msqvo += 'else:\n'
        dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)'
    else:
        dww__msqvo = 'if arg0 != arg1:\n'
        dww__msqvo += '   res[i] = arg0\n'
        dww__msqvo += 'else:\n'
        dww__msqvo += '   bodo.libs.array_kernels.setna(res, i)'
    tbhnn__qnaso = get_common_broadcasted_type([arr0, arr1], 'NULLIF')
    return gen_vectorized(tytu__ufwe, dyq__dond, gha__uloln, dww__msqvo,
        tbhnn__qnaso)


@numba.generated_jit(nopython=True)
def regr_valx_util(y, x):
    verify_int_float_arg(y, 'regr_valx', 'y')
    verify_int_float_arg(x, 'regr_valx', 'x')
    tytu__ufwe = ['y', 'x']
    dyq__dond = [y, x]
    gkd__ffof = [True] * 2
    dww__msqvo = 'res[i] = arg1'
    tbhnn__qnaso = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(tytu__ufwe, dyq__dond, gkd__ffof, dww__msqvo,
        tbhnn__qnaso)
