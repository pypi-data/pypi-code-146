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
    for uptg__abu in range(2):
        if isinstance(args[uptg__abu], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.booland',
                ['A', 'B'], uptg__abu)

    def impl(A, B):
        return booland_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolor(A, B):
    args = [A, B]
    for uptg__abu in range(2):
        if isinstance(args[uptg__abu], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolor',
                ['A', 'B'], uptg__abu)

    def impl(A, B):
        return boolor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolxor(A, B):
    args = [A, B]
    for uptg__abu in range(2):
        if isinstance(args[uptg__abu], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolxor',
                ['A', 'B'], uptg__abu)

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
    for uptg__abu in range(3):
        if isinstance(args[uptg__abu], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.cond', [
                'arr', 'ifbranch', 'elsebranch'], uptg__abu)

    def impl(arr, ifbranch, elsebranch):
        return cond_util(arr, ifbranch, elsebranch)
    return impl


@numba.generated_jit(nopython=True)
def equal_null(A, B):
    args = [A, B]
    for uptg__abu in range(2):
        if isinstance(args[uptg__abu], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.equal_null',
                ['A', 'B'], uptg__abu)

    def impl(A, B):
        return equal_null_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def booland_util(A, B):
    verify_int_float_arg(A, 'BOOLAND', 'A')
    verify_int_float_arg(B, 'BOOLAND', 'B')
    jzc__evu = ['A', 'B']
    hjmi__yaol = [A, B]
    udq__xca = [False] * 2
    if A == bodo.none:
        udq__xca = [False, True]
        jbei__hvafp = 'if arg1 != 0:\n'
        jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
        jbei__hvafp += 'else:\n'
        jbei__hvafp += '   res[i] = False\n'
    elif B == bodo.none:
        udq__xca = [True, False]
        jbei__hvafp = 'if arg0 != 0:\n'
        jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
        jbei__hvafp += 'else:\n'
        jbei__hvafp += '   res[i] = False\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            jbei__hvafp = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
            jbei__hvafp += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
            jbei__hvafp += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
            jbei__hvafp += 'else:\n'
            jbei__hvafp += '   res[i] = (arg0 != 0) and (arg1 != 0)'
        else:
            jbei__hvafp = (
                'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
            jbei__hvafp += 'else:\n'
            jbei__hvafp += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        jbei__hvafp = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
        jbei__hvafp += 'else:\n'
        jbei__hvafp += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    else:
        jbei__hvafp = 'res[i] = (arg0 != 0) and (arg1 != 0)'
    nsbgb__fawd = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(jzc__evu, hjmi__yaol, udq__xca, jbei__hvafp,
        nsbgb__fawd)


@numba.generated_jit(nopython=True)
def boolor_util(A, B):
    verify_int_float_arg(A, 'BOOLOR', 'A')
    verify_int_float_arg(B, 'BOOLOR', 'B')
    jzc__evu = ['A', 'B']
    hjmi__yaol = [A, B]
    udq__xca = [False] * 2
    if A == bodo.none:
        udq__xca = [False, True]
        jbei__hvafp = 'if arg1 == 0:\n'
        jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
        jbei__hvafp += 'else:\n'
        jbei__hvafp += '   res[i] = True\n'
    elif B == bodo.none:
        udq__xca = [True, False]
        jbei__hvafp = 'if arg0 == 0:\n'
        jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
        jbei__hvafp += 'else:\n'
        jbei__hvafp += '   res[i] = True\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            jbei__hvafp = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
            jbei__hvafp += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            jbei__hvafp += '   res[i] = True\n'
            jbei__hvafp += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
            jbei__hvafp += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            jbei__hvafp += '   res[i] = True\n'
            jbei__hvafp += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
            jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
            jbei__hvafp += 'else:\n'
            jbei__hvafp += '   res[i] = (arg0 != 0) or (arg1 != 0)'
        else:
            jbei__hvafp = (
                'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            jbei__hvafp += '   res[i] = True\n'
            jbei__hvafp += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
            jbei__hvafp += 'else:\n'
            jbei__hvafp += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        jbei__hvafp = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        jbei__hvafp += '   res[i] = True\n'
        jbei__hvafp += (
            'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
        jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
        jbei__hvafp += 'else:\n'
        jbei__hvafp += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    else:
        jbei__hvafp = 'res[i] = (arg0 != 0) or (arg1 != 0)'
    nsbgb__fawd = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(jzc__evu, hjmi__yaol, udq__xca, jbei__hvafp,
        nsbgb__fawd)


@numba.generated_jit(nopython=True)
def boolxor_util(A, B):
    verify_int_float_arg(A, 'BOOLXOR', 'A')
    verify_int_float_arg(B, 'BOOLXOR', 'B')
    jzc__evu = ['A', 'B']
    hjmi__yaol = [A, B]
    udq__xca = [True] * 2
    jbei__hvafp = 'res[i] = (arg0 == 0) != (arg1 == 0)'
    nsbgb__fawd = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(jzc__evu, hjmi__yaol, udq__xca, jbei__hvafp,
        nsbgb__fawd)


@numba.generated_jit(nopython=True)
def boolnot_util(A):
    verify_int_float_arg(A, 'BOOLNOT', 'A')
    jzc__evu = ['A']
    hjmi__yaol = [A]
    udq__xca = [True]
    jbei__hvafp = 'res[i] = arg0 == 0'
    nsbgb__fawd = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(jzc__evu, hjmi__yaol, udq__xca, jbei__hvafp,
        nsbgb__fawd)


@numba.generated_jit(nopython=True)
def nullif(arr0, arr1):
    args = [arr0, arr1]
    for uptg__abu in range(2):
        if isinstance(args[uptg__abu], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.nullif',
                ['arr0', 'arr1'], uptg__abu)

    def impl(arr0, arr1):
        return nullif_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def regr_valx(y, x):
    args = [y, x]
    for uptg__abu in range(2):
        if isinstance(args[uptg__abu], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valx',
                ['y', 'x'], uptg__abu)

    def impl(y, x):
        return regr_valx_util(y, x)
    return impl


@numba.generated_jit(nopython=True)
def regr_valy(y, x):
    args = [y, x]
    for uptg__abu in range(2):
        if isinstance(args[uptg__abu], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valy',
                ['y', 'x'], uptg__abu)

    def impl(y, x):
        return regr_valx(x, y)
    return impl


@numba.generated_jit(nopython=True)
def cond_util(arr, ifbranch, elsebranch):
    verify_boolean_arg(arr, 'cond', 'arr')
    if bodo.utils.utils.is_array_typ(arr, True
        ) and ifbranch == bodo.none and elsebranch == bodo.none:
        raise_bodo_error('Both branches of IF() cannot be scalar NULL')
    jzc__evu = ['arr', 'ifbranch', 'elsebranch']
    hjmi__yaol = [arr, ifbranch, elsebranch]
    udq__xca = [False] * 3
    if bodo.utils.utils.is_array_typ(arr, True):
        jbei__hvafp = (
            'if (not bodo.libs.array_kernels.isna(arr, i)) and arg0:\n')
    elif arr != bodo.none:
        jbei__hvafp = 'if arg0:\n'
    else:
        jbei__hvafp = ''
    if arr != bodo.none:
        if bodo.utils.utils.is_array_typ(ifbranch, True):
            jbei__hvafp += '   if bodo.libs.array_kernels.isna(ifbranch, i):\n'
            jbei__hvafp += '      bodo.libs.array_kernels.setna(res, i)\n'
            jbei__hvafp += '   else:\n'
            jbei__hvafp += '      res[i] = arg1\n'
        elif ifbranch == bodo.none:
            jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
        else:
            jbei__hvafp += '   res[i] = arg1\n'
        jbei__hvafp += 'else:\n'
    if bodo.utils.utils.is_array_typ(elsebranch, True):
        jbei__hvafp += '   if bodo.libs.array_kernels.isna(elsebranch, i):\n'
        jbei__hvafp += '      bodo.libs.array_kernels.setna(res, i)\n'
        jbei__hvafp += '   else:\n'
        jbei__hvafp += '      res[i] = arg2\n'
    elif elsebranch == bodo.none:
        jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)\n'
    else:
        jbei__hvafp += '   res[i] = arg2\n'
    nsbgb__fawd = get_common_broadcasted_type([ifbranch, elsebranch], 'IF')
    return gen_vectorized(jzc__evu, hjmi__yaol, udq__xca, jbei__hvafp,
        nsbgb__fawd)


@numba.generated_jit(nopython=True)
def equal_null_util(A, B):
    get_common_broadcasted_type([A, B], 'EQUAL_NULL')
    jzc__evu = ['A', 'B']
    hjmi__yaol = [A, B]
    udq__xca = [False] * 2
    if A == bodo.none:
        if B == bodo.none:
            jbei__hvafp = 'res[i] = True'
        elif bodo.utils.utils.is_array_typ(B, True):
            jbei__hvafp = 'res[i] = bodo.libs.array_kernels.isna(B, i)'
        else:
            jbei__hvafp = 'res[i] = False'
    elif B == bodo.none:
        if bodo.utils.utils.is_array_typ(A, True):
            jbei__hvafp = 'res[i] = bodo.libs.array_kernels.isna(A, i)'
        else:
            jbei__hvafp = 'res[i] = False'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            jbei__hvafp = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            jbei__hvafp += '   res[i] = True\n'
            jbei__hvafp += """elif bodo.libs.array_kernels.isna(A, i) or bodo.libs.array_kernels.isna(B, i):
"""
            jbei__hvafp += '   res[i] = False\n'
            jbei__hvafp += 'else:\n'
            jbei__hvafp += '   res[i] = arg0 == arg1'
        else:
            jbei__hvafp = (
                'res[i] = (not bodo.libs.array_kernels.isna(A, i)) and arg0 == arg1'
                )
    elif bodo.utils.utils.is_array_typ(B, True):
        jbei__hvafp = (
            'res[i] = (not bodo.libs.array_kernels.isna(B, i)) and arg0 == arg1'
            )
    else:
        jbei__hvafp = 'res[i] = arg0 == arg1'
    nsbgb__fawd = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(jzc__evu, hjmi__yaol, udq__xca, jbei__hvafp,
        nsbgb__fawd)


@numba.generated_jit(nopython=True)
def nullif_util(arr0, arr1):
    jzc__evu = ['arr0', 'arr1']
    hjmi__yaol = [arr0, arr1]
    udq__xca = [True, False]
    if arr1 == bodo.none:
        jbei__hvafp = 'res[i] = arg0\n'
    elif bodo.utils.utils.is_array_typ(arr1, True):
        jbei__hvafp = (
            'if bodo.libs.array_kernels.isna(arr1, i) or arg0 != arg1:\n')
        jbei__hvafp += '   res[i] = arg0\n'
        jbei__hvafp += 'else:\n'
        jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)'
    else:
        jbei__hvafp = 'if arg0 != arg1:\n'
        jbei__hvafp += '   res[i] = arg0\n'
        jbei__hvafp += 'else:\n'
        jbei__hvafp += '   bodo.libs.array_kernels.setna(res, i)'
    nsbgb__fawd = get_common_broadcasted_type([arr0, arr1], 'NULLIF')
    return gen_vectorized(jzc__evu, hjmi__yaol, udq__xca, jbei__hvafp,
        nsbgb__fawd)


@numba.generated_jit(nopython=True)
def regr_valx_util(y, x):
    verify_int_float_arg(y, 'regr_valx', 'y')
    verify_int_float_arg(x, 'regr_valx', 'x')
    jzc__evu = ['y', 'x']
    hjmi__yaol = [y, x]
    zruey__vqsc = [True] * 2
    jbei__hvafp = 'res[i] = arg1'
    nsbgb__fawd = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(jzc__evu, hjmi__yaol, zruey__vqsc, jbei__hvafp,
        nsbgb__fawd)
