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
    for jer__sxh in range(2):
        if isinstance(args[jer__sxh], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.booland',
                ['A', 'B'], jer__sxh)

    def impl(A, B):
        return booland_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolor(A, B):
    args = [A, B]
    for jer__sxh in range(2):
        if isinstance(args[jer__sxh], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolor',
                ['A', 'B'], jer__sxh)

    def impl(A, B):
        return boolor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolxor(A, B):
    args = [A, B]
    for jer__sxh in range(2):
        if isinstance(args[jer__sxh], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolxor',
                ['A', 'B'], jer__sxh)

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
    for jer__sxh in range(3):
        if isinstance(args[jer__sxh], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.cond', [
                'arr', 'ifbranch', 'elsebranch'], jer__sxh)

    def impl(arr, ifbranch, elsebranch):
        return cond_util(arr, ifbranch, elsebranch)
    return impl


@numba.generated_jit(nopython=True)
def equal_null(A, B):
    args = [A, B]
    for jer__sxh in range(2):
        if isinstance(args[jer__sxh], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.equal_null',
                ['A', 'B'], jer__sxh)

    def impl(A, B):
        return equal_null_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def booland_util(A, B):
    verify_int_float_arg(A, 'BOOLAND', 'A')
    verify_int_float_arg(B, 'BOOLAND', 'B')
    ypb__lsn = ['A', 'B']
    xpje__riat = [A, B]
    ytnn__tqcbi = [False] * 2
    if A == bodo.none:
        ytnn__tqcbi = [False, True]
        lcgv__ofwap = 'if arg1 != 0:\n'
        lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
        lcgv__ofwap += 'else:\n'
        lcgv__ofwap += '   res[i] = False\n'
    elif B == bodo.none:
        ytnn__tqcbi = [True, False]
        lcgv__ofwap = 'if arg0 != 0:\n'
        lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
        lcgv__ofwap += 'else:\n'
        lcgv__ofwap += '   res[i] = False\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            lcgv__ofwap = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
            lcgv__ofwap += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
            lcgv__ofwap += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
            lcgv__ofwap += 'else:\n'
            lcgv__ofwap += '   res[i] = (arg0 != 0) and (arg1 != 0)'
        else:
            lcgv__ofwap = (
                'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
            lcgv__ofwap += 'else:\n'
            lcgv__ofwap += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        lcgv__ofwap = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
        lcgv__ofwap += 'else:\n'
        lcgv__ofwap += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    else:
        lcgv__ofwap = 'res[i] = (arg0 != 0) and (arg1 != 0)'
    jnnq__trnm = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(ypb__lsn, xpje__riat, ytnn__tqcbi, lcgv__ofwap,
        jnnq__trnm)


@numba.generated_jit(nopython=True)
def boolor_util(A, B):
    verify_int_float_arg(A, 'BOOLOR', 'A')
    verify_int_float_arg(B, 'BOOLOR', 'B')
    ypb__lsn = ['A', 'B']
    xpje__riat = [A, B]
    ytnn__tqcbi = [False] * 2
    if A == bodo.none:
        ytnn__tqcbi = [False, True]
        lcgv__ofwap = 'if arg1 == 0:\n'
        lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
        lcgv__ofwap += 'else:\n'
        lcgv__ofwap += '   res[i] = True\n'
    elif B == bodo.none:
        ytnn__tqcbi = [True, False]
        lcgv__ofwap = 'if arg0 == 0:\n'
        lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
        lcgv__ofwap += 'else:\n'
        lcgv__ofwap += '   res[i] = True\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            lcgv__ofwap = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
            lcgv__ofwap += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            lcgv__ofwap += '   res[i] = True\n'
            lcgv__ofwap += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
            lcgv__ofwap += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            lcgv__ofwap += '   res[i] = True\n'
            lcgv__ofwap += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
            lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
            lcgv__ofwap += 'else:\n'
            lcgv__ofwap += '   res[i] = (arg0 != 0) or (arg1 != 0)'
        else:
            lcgv__ofwap = (
                'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            lcgv__ofwap += '   res[i] = True\n'
            lcgv__ofwap += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
            lcgv__ofwap += 'else:\n'
            lcgv__ofwap += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        lcgv__ofwap = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        lcgv__ofwap += '   res[i] = True\n'
        lcgv__ofwap += (
            'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
        lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
        lcgv__ofwap += 'else:\n'
        lcgv__ofwap += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    else:
        lcgv__ofwap = 'res[i] = (arg0 != 0) or (arg1 != 0)'
    jnnq__trnm = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(ypb__lsn, xpje__riat, ytnn__tqcbi, lcgv__ofwap,
        jnnq__trnm)


@numba.generated_jit(nopython=True)
def boolxor_util(A, B):
    verify_int_float_arg(A, 'BOOLXOR', 'A')
    verify_int_float_arg(B, 'BOOLXOR', 'B')
    ypb__lsn = ['A', 'B']
    xpje__riat = [A, B]
    ytnn__tqcbi = [True] * 2
    lcgv__ofwap = 'res[i] = (arg0 == 0) != (arg1 == 0)'
    jnnq__trnm = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(ypb__lsn, xpje__riat, ytnn__tqcbi, lcgv__ofwap,
        jnnq__trnm)


@numba.generated_jit(nopython=True)
def boolnot_util(A):
    verify_int_float_arg(A, 'BOOLNOT', 'A')
    ypb__lsn = ['A']
    xpje__riat = [A]
    ytnn__tqcbi = [True]
    lcgv__ofwap = 'res[i] = arg0 == 0'
    jnnq__trnm = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(ypb__lsn, xpje__riat, ytnn__tqcbi, lcgv__ofwap,
        jnnq__trnm)


@numba.generated_jit(nopython=True)
def nullif(arr0, arr1):
    args = [arr0, arr1]
    for jer__sxh in range(2):
        if isinstance(args[jer__sxh], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.nullif',
                ['arr0', 'arr1'], jer__sxh)

    def impl(arr0, arr1):
        return nullif_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def regr_valx(y, x):
    args = [y, x]
    for jer__sxh in range(2):
        if isinstance(args[jer__sxh], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valx',
                ['y', 'x'], jer__sxh)

    def impl(y, x):
        return regr_valx_util(y, x)
    return impl


@numba.generated_jit(nopython=True)
def regr_valy(y, x):
    args = [y, x]
    for jer__sxh in range(2):
        if isinstance(args[jer__sxh], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valy',
                ['y', 'x'], jer__sxh)

    def impl(y, x):
        return regr_valx(x, y)
    return impl


@numba.generated_jit(nopython=True)
def cond_util(arr, ifbranch, elsebranch):
    verify_boolean_arg(arr, 'cond', 'arr')
    if bodo.utils.utils.is_array_typ(arr, True
        ) and ifbranch == bodo.none and elsebranch == bodo.none:
        raise_bodo_error('Both branches of IF() cannot be scalar NULL')
    ypb__lsn = ['arr', 'ifbranch', 'elsebranch']
    xpje__riat = [arr, ifbranch, elsebranch]
    ytnn__tqcbi = [False] * 3
    if bodo.utils.utils.is_array_typ(arr, True):
        lcgv__ofwap = (
            'if (not bodo.libs.array_kernels.isna(arr, i)) and arg0:\n')
    elif arr != bodo.none:
        lcgv__ofwap = 'if arg0:\n'
    else:
        lcgv__ofwap = ''
    if arr != bodo.none:
        if bodo.utils.utils.is_array_typ(ifbranch, True):
            lcgv__ofwap += '   if bodo.libs.array_kernels.isna(ifbranch, i):\n'
            lcgv__ofwap += '      bodo.libs.array_kernels.setna(res, i)\n'
            lcgv__ofwap += '   else:\n'
            lcgv__ofwap += '      res[i] = arg1\n'
        elif ifbranch == bodo.none:
            lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
        else:
            lcgv__ofwap += '   res[i] = arg1\n'
        lcgv__ofwap += 'else:\n'
    if bodo.utils.utils.is_array_typ(elsebranch, True):
        lcgv__ofwap += '   if bodo.libs.array_kernels.isna(elsebranch, i):\n'
        lcgv__ofwap += '      bodo.libs.array_kernels.setna(res, i)\n'
        lcgv__ofwap += '   else:\n'
        lcgv__ofwap += '      res[i] = arg2\n'
    elif elsebranch == bodo.none:
        lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)\n'
    else:
        lcgv__ofwap += '   res[i] = arg2\n'
    jnnq__trnm = get_common_broadcasted_type([ifbranch, elsebranch], 'IF')
    return gen_vectorized(ypb__lsn, xpje__riat, ytnn__tqcbi, lcgv__ofwap,
        jnnq__trnm)


@numba.generated_jit(nopython=True)
def equal_null_util(A, B):
    get_common_broadcasted_type([A, B], 'EQUAL_NULL')
    ypb__lsn = ['A', 'B']
    xpje__riat = [A, B]
    ytnn__tqcbi = [False] * 2
    if A == bodo.none:
        if B == bodo.none:
            lcgv__ofwap = 'res[i] = True'
        elif bodo.utils.utils.is_array_typ(B, True):
            lcgv__ofwap = 'res[i] = bodo.libs.array_kernels.isna(B, i)'
        else:
            lcgv__ofwap = 'res[i] = False'
    elif B == bodo.none:
        if bodo.utils.utils.is_array_typ(A, True):
            lcgv__ofwap = 'res[i] = bodo.libs.array_kernels.isna(A, i)'
        else:
            lcgv__ofwap = 'res[i] = False'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            lcgv__ofwap = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            lcgv__ofwap += '   res[i] = True\n'
            lcgv__ofwap += """elif bodo.libs.array_kernels.isna(A, i) or bodo.libs.array_kernels.isna(B, i):
"""
            lcgv__ofwap += '   res[i] = False\n'
            lcgv__ofwap += 'else:\n'
            lcgv__ofwap += '   res[i] = arg0 == arg1'
        else:
            lcgv__ofwap = (
                'res[i] = (not bodo.libs.array_kernels.isna(A, i)) and arg0 == arg1'
                )
    elif bodo.utils.utils.is_array_typ(B, True):
        lcgv__ofwap = (
            'res[i] = (not bodo.libs.array_kernels.isna(B, i)) and arg0 == arg1'
            )
    else:
        lcgv__ofwap = 'res[i] = arg0 == arg1'
    jnnq__trnm = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(ypb__lsn, xpje__riat, ytnn__tqcbi, lcgv__ofwap,
        jnnq__trnm)


@numba.generated_jit(nopython=True)
def nullif_util(arr0, arr1):
    ypb__lsn = ['arr0', 'arr1']
    xpje__riat = [arr0, arr1]
    ytnn__tqcbi = [True, False]
    if arr1 == bodo.none:
        lcgv__ofwap = 'res[i] = arg0\n'
    elif bodo.utils.utils.is_array_typ(arr1, True):
        lcgv__ofwap = (
            'if bodo.libs.array_kernels.isna(arr1, i) or arg0 != arg1:\n')
        lcgv__ofwap += '   res[i] = arg0\n'
        lcgv__ofwap += 'else:\n'
        lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)'
    else:
        lcgv__ofwap = 'if arg0 != arg1:\n'
        lcgv__ofwap += '   res[i] = arg0\n'
        lcgv__ofwap += 'else:\n'
        lcgv__ofwap += '   bodo.libs.array_kernels.setna(res, i)'
    jnnq__trnm = get_common_broadcasted_type([arr0, arr1], 'NULLIF')
    return gen_vectorized(ypb__lsn, xpje__riat, ytnn__tqcbi, lcgv__ofwap,
        jnnq__trnm)


@numba.generated_jit(nopython=True)
def regr_valx_util(y, x):
    verify_int_float_arg(y, 'regr_valx', 'y')
    verify_int_float_arg(x, 'regr_valx', 'x')
    ypb__lsn = ['y', 'x']
    xpje__riat = [y, x]
    jqeu__uuq = [True] * 2
    lcgv__ofwap = 'res[i] = arg1'
    jnnq__trnm = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(ypb__lsn, xpje__riat, jqeu__uuq, lcgv__ofwap,
        jnnq__trnm)
