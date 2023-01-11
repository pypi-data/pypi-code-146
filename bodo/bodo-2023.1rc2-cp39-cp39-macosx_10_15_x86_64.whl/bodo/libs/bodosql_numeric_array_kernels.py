"""
Implements numerical array kernels that are specific to BodoSQL
"""
import numba
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.utils import is_array_typ


def cbrt(arr):
    return


def ceil(arr):
    return


def factorial(arr):
    return


def floor(arr):
    return


def mod(arr0, arr1):
    return


def sign(arr):
    return


def sqrt(arr):
    return


def round(arr0, arr1):
    return


def trunc(arr0, arr1):
    return


def abs(arr):
    return


def ln(arr):
    return


def log2(arr):
    return


def log10(arr):
    return


def exp(arr):
    return


def power(arr0, arr1):
    return


def sqrt_util(arr):
    return


def square(arr):
    return


def cbrt_util(arr):
    return


def ceil_util(arr):
    return


def factorial_util(arr):
    return


def floor_util(arr):
    return


def mod_util(arr0, arr1):
    return


def sign_util(arr):
    return


def round_util(arr0, arr1):
    return


def trunc_util(arr0, arr1):
    return


def abs_util(arr):
    return


def ln_util(arr):
    return


def log2_util(arr):
    return


def log10_util(arr):
    return


def exp_util(arr):
    return


def power_util(arr0, arr1):
    return


def square_util(arr):
    return


funcs_utils_names = (abs, abs_util, 'ABS'), (cbrt, cbrt_util, 'CBRT'), (ceil,
    ceil_util, 'CEIL'), (factorial, factorial_util, 'FACTORIAL'), (floor,
    floor_util, 'FLOOR'), (ln, ln_util, 'LN'), (log2, log2_util, 'LOG2'), (
    log10, log10_util, 'LOG10'), (mod, mod_util, 'MOD'), (sign, sign_util,
    'SIGN'), (round, round_util, 'ROUND'), (trunc, trunc_util, 'TRUNC'), (exp,
    exp_util, 'EXP'), (power, power_util, 'POWER'), (sqrt, sqrt_util, 'SQRT'
    ), (square, square_util, 'SQUARE')
double_arg_funcs = 'MOD', 'TRUNC', 'POWER', 'ROUND'
single_arg_funcs = set(a[2] for a in funcs_utils_names if a[2] not in
    double_arg_funcs)
_float = {(16): types.float16, (32): types.float32, (64): types.float64}
_int = {(8): types.int8, (16): types.int16, (32): types.int32, (64): types.
    int64}
_uint = {(8): types.uint8, (16): types.uint16, (32): types.uint32, (64):
    types.uint64}


def _get_numeric_output_dtype(func_name, arr0, arr1=None):
    gvz__odx = arr0.dtype if is_array_typ(arr0) else arr0
    zxg__uista = arr1.dtype if is_array_typ(arr1) else arr1
    lah__bjir = bodo.float64
    if (arr0 is None or gvz__odx == bodo.none
        ) or func_name in double_arg_funcs and (arr1 is None or zxg__uista ==
        bodo.none):
        return types.Array(lah__bjir, 1, 'C')
    if isinstance(gvz__odx, types.Float):
        if isinstance(zxg__uista, types.Float):
            lah__bjir = _float[max(gvz__odx.bitwidth, zxg__uista.bitwidth)]
        else:
            lah__bjir = gvz__odx
    if func_name == 'SIGN':
        if isinstance(gvz__odx, types.Integer):
            lah__bjir = gvz__odx
    elif func_name == 'MOD':
        if isinstance(gvz__odx, types.Integer) and isinstance(zxg__uista,
            types.Integer):
            if gvz__odx.signed:
                if zxg__uista.signed:
                    lah__bjir = zxg__uista
                else:
                    lah__bjir = _int[min(64, zxg__uista.bitwidth * 2)]
            else:
                lah__bjir = zxg__uista
    elif func_name == 'ABS':
        if isinstance(gvz__odx, types.Integer):
            if gvz__odx.signed:
                lah__bjir = _uint[min(64, gvz__odx.bitwidth * 2)]
            else:
                lah__bjir = gvz__odx
    elif func_name == 'ROUND':
        if isinstance(gvz__odx, (types.Float, types.Integer)):
            lah__bjir = gvz__odx
    elif func_name == 'FACTORIAL':
        lah__bjir = bodo.int64
    if isinstance(lah__bjir, types.Integer):
        return bodo.libs.int_arr_ext.IntegerArrayType(lah__bjir)
    else:
        return types.Array(lah__bjir, 1, 'C')


def create_numeric_func_overload(func_name):
    if func_name not in double_arg_funcs:
        func_name = func_name.lower()

        def overload_func(arr):
            if isinstance(arr, types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.{func_name}', ['arr'], 0)
            bpxb__boweu = 'def impl(arr):\n'
            bpxb__boweu += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr)'
                )
            tuod__udp = {}
            exec(bpxb__boweu, {'bodo': bodo}, tuod__udp)
            return tuod__udp['impl']
    else:
        func_name = func_name.lower()

        def overload_func(arr0, arr1):
            args = [arr0, arr1]
            for pht__niug in range(2):
                if isinstance(args[pht__niug], types.optional):
                    return unopt_argument(
                        f'bodo.libs.bodosql_array_kernels.{func_name}', [
                        'arr0', 'arr1'], pht__niug)
            bpxb__boweu = 'def impl(arr0, arr1):\n'
            bpxb__boweu += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr0, arr1)'
                )
            tuod__udp = {}
            exec(bpxb__boweu, {'bodo': bodo}, tuod__udp)
            return tuod__udp['impl']
    return overload_func


def create_numeric_util_overload(func_name):
    if func_name not in double_arg_funcs:

        def overload_numeric_util(arr):
            verify_int_float_arg(arr, func_name, 'arr')
            vofe__qcjc = ['arr']
            fni__lig = [arr]
            vtv__nrza = [True]
            ati__jjcbz = ''
            if func_name in single_arg_funcs:
                if func_name == 'FACTORIAL':
                    ati__jjcbz += (
                        'if arg0 > 20 or np.abs(np.int64(arg0)) != arg0:\n')
                    ati__jjcbz += '  bodo.libs.array_kernels.setna(res, i)\n'
                    ati__jjcbz += 'else:\n'
                    ati__jjcbz += (
                        f'  res[i] = np.math.factorial(np.int64(arg0))')
                elif func_name == 'LN':
                    ati__jjcbz += f'res[i] = np.log(arg0)'
                else:
                    ati__jjcbz += f'res[i] = np.{func_name.lower()}(arg0)'
            else:
                ValueError(f'Unknown function name: {func_name}')
            lah__bjir = _get_numeric_output_dtype(func_name, arr)
            return gen_vectorized(vofe__qcjc, fni__lig, vtv__nrza,
                ati__jjcbz, lah__bjir)
    else:

        def overload_numeric_util(arr0, arr1):
            verify_int_float_arg(arr0, func_name, 'arr0')
            verify_int_float_arg(arr0, func_name, 'arr1')
            vofe__qcjc = ['arr0', 'arr1']
            fni__lig = [arr0, arr1]
            vtv__nrza = [True, True]
            lah__bjir = _get_numeric_output_dtype(func_name, arr0, arr1)
            ati__jjcbz = ''
            if func_name == 'MOD':
                ati__jjcbz += 'if arg1 == 0:\n'
                ati__jjcbz += '  bodo.libs.array_kernels.setna(res, i)\n'
                ati__jjcbz += 'else:\n'
                ati__jjcbz += (
                    '  res[i] = np.sign(arg0) * np.mod(np.abs(arg0), np.abs(arg1))'
                    )
            elif func_name == 'POWER':
                ati__jjcbz += 'res[i] = np.power(np.float64(arg0), arg1)'
            elif func_name == 'ROUND':
                ati__jjcbz += 'res[i] = np.round(arg0, arg1)'
            elif func_name == 'TRUNC':
                ati__jjcbz += 'if int(arg1) == arg1:\n'
                ati__jjcbz += (
                    '  res[i] = np.trunc(arg0 * (10.0 ** arg1)) * (10.0 ** -arg1)\n'
                    )
                ati__jjcbz += 'else:\n'
                ati__jjcbz += '  bodo.libs.array_kernels.setna(res, i)'
            else:
                raise ValueError(f'Unknown function name: {func_name}')
            return gen_vectorized(vofe__qcjc, fni__lig, vtv__nrza,
                ati__jjcbz, lah__bjir)
    return overload_numeric_util


def _install_numeric_overload(funcs_utils_names):
    for wyfq__xmrfg, xwub__jxjvz, func_name in funcs_utils_names:
        jqlg__ydtrj = create_numeric_func_overload(func_name)
        overload(wyfq__xmrfg)(jqlg__ydtrj)
        uitur__ttjbk = create_numeric_util_overload(func_name)
        overload(xwub__jxjvz)(uitur__ttjbk)


_install_numeric_overload(funcs_utils_names)


@numba.generated_jit(nopython=True)
def bitand(A, B):
    args = [A, B]
    for pht__niug in range(2):
        if isinstance(args[pht__niug], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitand',
                ['A', 'B'], pht__niug)

    def impl(A, B):
        return bitand_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftleft(A, B):
    args = [A, B]
    for pht__niug in range(2):
        if isinstance(args[pht__niug], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftleft', ['A', 'B'],
                pht__niug)

    def impl(A, B):
        return bitshiftleft_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitnot(A):
    if isinstance(A, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.bitnot_util',
            ['A'], 0)

    def impl(A):
        return bitnot_util(A)
    return impl


@numba.generated_jit(nopython=True)
def bitor(A, B):
    args = [A, B]
    for pht__niug in range(2):
        if isinstance(args[pht__niug], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitor',
                ['A', 'B'], pht__niug)

    def impl(A, B):
        return bitor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftright(A, B):
    args = [A, B]
    for pht__niug in range(2):
        if isinstance(args[pht__niug], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftright', ['A', 'B'],
                pht__niug)

    def impl(A, B):
        return bitshiftright_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitxor(A, B):
    args = [A, B]
    for pht__niug in range(2):
        if isinstance(args[pht__niug], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitxor',
                ['A', 'B'], pht__niug)

    def impl(A, B):
        return bitxor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def conv(arr, old_base, new_base):
    args = [arr, old_base, new_base]
    for pht__niug in range(3):
        if isinstance(args[pht__niug], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.conv', [
                'arr', 'old_base', 'new_base'], pht__niug)

    def impl(arr, old_base, new_base):
        return conv_util(arr, old_base, new_base)
    return impl


@numba.generated_jit(nopython=True)
def getbit(A, B):
    args = [A, B]
    for pht__niug in range(2):
        if isinstance(args[pht__niug], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.getbit',
                ['A', 'B'], pht__niug)

    def impl(A, B):
        return getbit_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def haversine(lat1, lon1, lat2, lon2):
    args = [lat1, lon1, lat2, lon2]
    for pht__niug in range(4):
        if isinstance(args[pht__niug], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.haversine',
                ['lat1', 'lon1', 'lat2', 'lon2'], pht__niug)

    def impl(lat1, lon1, lat2, lon2):
        return haversine_util(lat1, lon1, lat2, lon2)
    return impl


@numba.generated_jit(nopython=True)
def div0(arr, divisor):
    args = [arr, divisor]
    for pht__niug in range(2):
        if isinstance(args[pht__niug], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.div0', [
                'arr', 'divisor'], pht__niug)

    def impl(arr, divisor):
        return div0_util(arr, divisor)
    return impl


@numba.generated_jit(nopython=True)
def log(arr, base):
    args = [arr, base]
    for pht__niug in range(2):
        if isinstance(args[pht__niug], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.log', [
                'arr', 'base'], pht__niug)

    def impl(arr, base):
        return log_util(arr, base)
    return impl


@numba.generated_jit(nopython=True)
def negate(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.negate_util',
            ['arr'], 0)

    def impl(arr):
        return negate_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def width_bucket(arr, min_val, max_val, num_buckets):
    args = [arr, min_val, max_val, num_buckets]
    for pht__niug in range(4):
        if isinstance(args[pht__niug], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.width_bucket', ['arr',
                'min_val', 'max_val', 'num_buckets'], pht__niug)

    def impl(arr, min_val, max_val, num_buckets):
        return width_bucket_util(arr, min_val, max_val, num_buckets)
    return impl


@numba.generated_jit(nopython=True)
def bitand_util(A, B):
    verify_int_arg(A, 'bitand', 'A')
    verify_int_arg(B, 'bitand', 'B')
    vofe__qcjc = ['A', 'B']
    fni__lig = [A, B]
    vtv__nrza = [True] * 2
    ati__jjcbz = 'res[i] = arg0 & arg1'
    lah__bjir = get_common_broadcasted_type([A, B], 'bitand')
    return gen_vectorized(vofe__qcjc, fni__lig, vtv__nrza, ati__jjcbz,
        lah__bjir)


@numba.generated_jit(nopython=True)
def bitshiftleft_util(A, B):
    verify_int_arg(A, 'bitshiftleft', 'A')
    verify_int_arg(B, 'bitshiftleft', 'B')
    vofe__qcjc = ['A', 'B']
    fni__lig = [A, B]
    vtv__nrza = [True] * 2
    ati__jjcbz = 'res[i] = arg0 << arg1'
    lah__bjir = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(vofe__qcjc, fni__lig, vtv__nrza, ati__jjcbz,
        lah__bjir)


@numba.generated_jit(nopython=True)
def bitnot_util(A):
    verify_int_arg(A, 'bitnot', 'A')
    vofe__qcjc = ['A']
    fni__lig = [A]
    vtv__nrza = [True]
    ati__jjcbz = 'res[i] = ~arg0'
    if A == bodo.none:
        lah__bjir = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            gwul__bnmo = A.dtype
        else:
            gwul__bnmo = A
        lah__bjir = bodo.libs.int_arr_ext.IntegerArrayType(gwul__bnmo)
    return gen_vectorized(vofe__qcjc, fni__lig, vtv__nrza, ati__jjcbz,
        lah__bjir)


@numba.generated_jit(nopython=True)
def bitor_util(A, B):
    verify_int_arg(A, 'bitor', 'A')
    verify_int_arg(B, 'bitor', 'B')
    vofe__qcjc = ['A', 'B']
    fni__lig = [A, B]
    vtv__nrza = [True] * 2
    ati__jjcbz = 'res[i] = arg0 | arg1'
    lah__bjir = get_common_broadcasted_type([A, B], 'bitor')
    return gen_vectorized(vofe__qcjc, fni__lig, vtv__nrza, ati__jjcbz,
        lah__bjir)


@numba.generated_jit(nopython=True)
def bitshiftright_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    vofe__qcjc = ['A', 'B']
    fni__lig = [A, B]
    vtv__nrza = [True] * 2
    if A == bodo.none:
        gwul__bnmo = lah__bjir = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            gwul__bnmo = A.dtype
        else:
            gwul__bnmo = A
        lah__bjir = bodo.libs.int_arr_ext.IntegerArrayType(gwul__bnmo)
    ati__jjcbz = f'res[i] = arg0 >> arg1\n'
    return gen_vectorized(vofe__qcjc, fni__lig, vtv__nrza, ati__jjcbz,
        lah__bjir)


@numba.generated_jit(nopython=True)
def bitxor_util(A, B):
    verify_int_arg(A, 'bitxor', 'A')
    verify_int_arg(B, 'bitxor', 'B')
    vofe__qcjc = ['A', 'B']
    fni__lig = [A, B]
    vtv__nrza = [True] * 2
    ati__jjcbz = 'res[i] = arg0 ^ arg1'
    lah__bjir = get_common_broadcasted_type([A, B], 'bitxor')
    return gen_vectorized(vofe__qcjc, fni__lig, vtv__nrza, ati__jjcbz,
        lah__bjir)


@numba.generated_jit(nopython=True)
def conv_util(arr, old_base, new_base):
    verify_string_arg(arr, 'CONV', 'arr')
    verify_int_arg(old_base, 'CONV', 'old_base')
    verify_int_arg(new_base, 'CONV', 'new_base')
    vofe__qcjc = ['arr', 'old_base', 'new_base']
    fni__lig = [arr, old_base, new_base]
    vtv__nrza = [True] * 3
    ati__jjcbz = 'old_val = int(arg0, arg1)\n'
    ati__jjcbz += 'if arg2 == 2:\n'
    ati__jjcbz += "   res[i] = format(old_val, 'b')\n"
    ati__jjcbz += 'elif arg2 == 8:\n'
    ati__jjcbz += "   res[i] = format(old_val, 'o')\n"
    ati__jjcbz += 'elif arg2 == 10:\n'
    ati__jjcbz += "   res[i] = format(old_val, 'd')\n"
    ati__jjcbz += 'elif arg2 == 16:\n'
    ati__jjcbz += "   res[i] = format(old_val, 'x')\n"
    ati__jjcbz += 'else:\n'
    ati__jjcbz += '   bodo.libs.array_kernels.setna(res, i)\n'
    lah__bjir = bodo.string_array_type
    return gen_vectorized(vofe__qcjc, fni__lig, vtv__nrza, ati__jjcbz,
        lah__bjir)


@numba.generated_jit(nopython=True)
def getbit_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    vofe__qcjc = ['A', 'B']
    fni__lig = [A, B]
    vtv__nrza = [True] * 2
    ati__jjcbz = 'res[i] = (arg0 >> arg1) & 1'
    lah__bjir = bodo.libs.int_arr_ext.IntegerArrayType(types.uint8)
    return gen_vectorized(vofe__qcjc, fni__lig, vtv__nrza, ati__jjcbz,
        lah__bjir)


@numba.generated_jit(nopython=True)
def haversine_util(lat1, lon1, lat2, lon2):
    verify_int_float_arg(lat1, 'HAVERSINE', 'lat1')
    verify_int_float_arg(lon1, 'HAVERSINE', 'lon1')
    verify_int_float_arg(lat2, 'HAVERSINE', 'lat2')
    verify_int_float_arg(lon2, 'HAVERSINE', 'lon2')
    vofe__qcjc = ['lat1', 'lon1', 'lat2', 'lon2']
    fni__lig = [lat1, lon1, lat2, lon2]
    jmg__vjcfv = [True] * 4
    ati__jjcbz = (
        'arg0, arg1, arg2, arg3 = map(np.radians, (arg0, arg1, arg2, arg3))\n')
    ligd__rfm = '(arg2 - arg0) * 0.5'
    wcwen__seg = '(arg3 - arg1) * 0.5'
    mbj__rjnkm = (
        f'np.square(np.sin({ligd__rfm})) + (np.cos(arg0) * np.cos(arg2) * np.square(np.sin({wcwen__seg})))'
        )
    ati__jjcbz += f'res[i] = 12742.0 * np.arcsin(np.sqrt({mbj__rjnkm}))\n'
    lah__bjir = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(vofe__qcjc, fni__lig, jmg__vjcfv, ati__jjcbz,
        lah__bjir)


@numba.generated_jit(nopython=True)
def div0_util(arr, divisor):
    verify_int_float_arg(arr, 'DIV0', 'arr')
    verify_int_float_arg(divisor, 'DIV0', 'divisor')
    vofe__qcjc = ['arr', 'divisor']
    fni__lig = [arr, divisor]
    jmg__vjcfv = [True] * 2
    ati__jjcbz = 'res[i] = arg0 / arg1 if arg1 else 0\n'
    lah__bjir = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(vofe__qcjc, fni__lig, jmg__vjcfv, ati__jjcbz,
        lah__bjir)


@numba.generated_jit(nopython=True)
def log_util(arr, base):
    verify_int_float_arg(arr, 'log', 'arr')
    verify_int_float_arg(base, 'log', 'base')
    vofe__qcjc = ['arr', 'base']
    fni__lig = [arr, base]
    vtv__nrza = [True] * 2
    ati__jjcbz = 'res[i] = np.log(arg0) / np.log(arg1)'
    lah__bjir = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(vofe__qcjc, fni__lig, vtv__nrza, ati__jjcbz,
        lah__bjir)


@numba.generated_jit(nopython=True)
def negate_util(arr):
    vofe__qcjc = ['arr']
    fni__lig = [arr]
    vtv__nrza = [True]
    if bodo.utils.utils.is_array_typ(arr, False):
        gwul__bnmo = arr.dtype
    elif bodo.utils.utils.is_array_typ(arr, True):
        gwul__bnmo = arr.data.dtype
    else:
        gwul__bnmo = arr
    ati__jjcbz = {types.uint8: 'res[i] = -np.int16(arg0)', types.uint16:
        'res[i] = -np.int32(arg0)', types.uint32: 'res[i] = -np.int64(arg0)'
        }.get(gwul__bnmo, 'res[i] = -arg0')
    gwul__bnmo = {types.uint8: types.int16, types.uint16: types.int32,
        types.uint32: types.int64, types.uint64: types.int64}.get(gwul__bnmo,
        gwul__bnmo)
    if isinstance(gwul__bnmo, types.Integer):
        lah__bjir = bodo.utils.typing.dtype_to_array_type(gwul__bnmo)
    else:
        lah__bjir = arr
    lah__bjir = bodo.utils.typing.to_nullable_type(lah__bjir)
    return gen_vectorized(vofe__qcjc, fni__lig, vtv__nrza, ati__jjcbz,
        lah__bjir)


@numba.generated_jit(nopython=True)
def width_bucket_util(arr, min_val, max_val, num_buckets):
    verify_int_float_arg(arr, 'WIDTH_BUCKET', 'arr')
    verify_int_float_arg(min_val, 'WIDTH_BUCKET', 'min_val')
    verify_int_float_arg(max_val, 'WIDTH_BUCKET', 'max_val')
    verify_int_arg(num_buckets, 'WIDTH_BUCKET', 'num_buckets')
    vofe__qcjc = ['arr', 'min_val', 'max_val', 'num_buckets']
    fni__lig = [arr, min_val, max_val, num_buckets]
    vtv__nrza = [True] * 4
    ati__jjcbz = (
        "if arg1 >= arg2: raise ValueError('min_val must be less than max_val')\n"
        )
    ati__jjcbz += (
        "if arg3 <= 0: raise ValueError('num_buckets must be a positive integer')\n"
        )
    ati__jjcbz += (
        'res[i] = min(max(-1.0, math.floor((arg0 - arg1) / ((arg2 - arg1) / arg3))), arg3) + 1.0'
        )
    lah__bjir = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(vofe__qcjc, fni__lig, vtv__nrza, ati__jjcbz,
        lah__bjir)
