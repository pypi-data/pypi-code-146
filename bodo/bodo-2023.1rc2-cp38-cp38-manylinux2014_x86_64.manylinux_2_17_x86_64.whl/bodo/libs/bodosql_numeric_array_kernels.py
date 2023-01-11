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
    fxpay__qiuj = arr0.dtype if is_array_typ(arr0) else arr0
    gxhq__enn = arr1.dtype if is_array_typ(arr1) else arr1
    qjge__jtgwq = bodo.float64
    if (arr0 is None or fxpay__qiuj == bodo.none
        ) or func_name in double_arg_funcs and (arr1 is None or gxhq__enn ==
        bodo.none):
        return types.Array(qjge__jtgwq, 1, 'C')
    if isinstance(fxpay__qiuj, types.Float):
        if isinstance(gxhq__enn, types.Float):
            qjge__jtgwq = _float[max(fxpay__qiuj.bitwidth, gxhq__enn.bitwidth)]
        else:
            qjge__jtgwq = fxpay__qiuj
    if func_name == 'SIGN':
        if isinstance(fxpay__qiuj, types.Integer):
            qjge__jtgwq = fxpay__qiuj
    elif func_name == 'MOD':
        if isinstance(fxpay__qiuj, types.Integer) and isinstance(gxhq__enn,
            types.Integer):
            if fxpay__qiuj.signed:
                if gxhq__enn.signed:
                    qjge__jtgwq = gxhq__enn
                else:
                    qjge__jtgwq = _int[min(64, gxhq__enn.bitwidth * 2)]
            else:
                qjge__jtgwq = gxhq__enn
    elif func_name == 'ABS':
        if isinstance(fxpay__qiuj, types.Integer):
            if fxpay__qiuj.signed:
                qjge__jtgwq = _uint[min(64, fxpay__qiuj.bitwidth * 2)]
            else:
                qjge__jtgwq = fxpay__qiuj
    elif func_name == 'ROUND':
        if isinstance(fxpay__qiuj, (types.Float, types.Integer)):
            qjge__jtgwq = fxpay__qiuj
    elif func_name == 'FACTORIAL':
        qjge__jtgwq = bodo.int64
    if isinstance(qjge__jtgwq, types.Integer):
        return bodo.libs.int_arr_ext.IntegerArrayType(qjge__jtgwq)
    else:
        return types.Array(qjge__jtgwq, 1, 'C')


def create_numeric_func_overload(func_name):
    if func_name not in double_arg_funcs:
        func_name = func_name.lower()

        def overload_func(arr):
            if isinstance(arr, types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.{func_name}', ['arr'], 0)
            urxu__bpg = 'def impl(arr):\n'
            urxu__bpg += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr)'
                )
            alrk__yhce = {}
            exec(urxu__bpg, {'bodo': bodo}, alrk__yhce)
            return alrk__yhce['impl']
    else:
        func_name = func_name.lower()

        def overload_func(arr0, arr1):
            args = [arr0, arr1]
            for usk__jojap in range(2):
                if isinstance(args[usk__jojap], types.optional):
                    return unopt_argument(
                        f'bodo.libs.bodosql_array_kernels.{func_name}', [
                        'arr0', 'arr1'], usk__jojap)
            urxu__bpg = 'def impl(arr0, arr1):\n'
            urxu__bpg += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr0, arr1)'
                )
            alrk__yhce = {}
            exec(urxu__bpg, {'bodo': bodo}, alrk__yhce)
            return alrk__yhce['impl']
    return overload_func


def create_numeric_util_overload(func_name):
    if func_name not in double_arg_funcs:

        def overload_numeric_util(arr):
            verify_int_float_arg(arr, func_name, 'arr')
            zqd__ebx = ['arr']
            firt__gzp = [arr]
            feul__mqgvt = [True]
            irh__jgkod = ''
            if func_name in single_arg_funcs:
                if func_name == 'FACTORIAL':
                    irh__jgkod += (
                        'if arg0 > 20 or np.abs(np.int64(arg0)) != arg0:\n')
                    irh__jgkod += '  bodo.libs.array_kernels.setna(res, i)\n'
                    irh__jgkod += 'else:\n'
                    irh__jgkod += (
                        f'  res[i] = np.math.factorial(np.int64(arg0))')
                elif func_name == 'LN':
                    irh__jgkod += f'res[i] = np.log(arg0)'
                else:
                    irh__jgkod += f'res[i] = np.{func_name.lower()}(arg0)'
            else:
                ValueError(f'Unknown function name: {func_name}')
            qjge__jtgwq = _get_numeric_output_dtype(func_name, arr)
            return gen_vectorized(zqd__ebx, firt__gzp, feul__mqgvt,
                irh__jgkod, qjge__jtgwq)
    else:

        def overload_numeric_util(arr0, arr1):
            verify_int_float_arg(arr0, func_name, 'arr0')
            verify_int_float_arg(arr0, func_name, 'arr1')
            zqd__ebx = ['arr0', 'arr1']
            firt__gzp = [arr0, arr1]
            feul__mqgvt = [True, True]
            qjge__jtgwq = _get_numeric_output_dtype(func_name, arr0, arr1)
            irh__jgkod = ''
            if func_name == 'MOD':
                irh__jgkod += 'if arg1 == 0:\n'
                irh__jgkod += '  bodo.libs.array_kernels.setna(res, i)\n'
                irh__jgkod += 'else:\n'
                irh__jgkod += (
                    '  res[i] = np.sign(arg0) * np.mod(np.abs(arg0), np.abs(arg1))'
                    )
            elif func_name == 'POWER':
                irh__jgkod += 'res[i] = np.power(np.float64(arg0), arg1)'
            elif func_name == 'ROUND':
                irh__jgkod += 'res[i] = np.round(arg0, arg1)'
            elif func_name == 'TRUNC':
                irh__jgkod += 'if int(arg1) == arg1:\n'
                irh__jgkod += (
                    '  res[i] = np.trunc(arg0 * (10.0 ** arg1)) * (10.0 ** -arg1)\n'
                    )
                irh__jgkod += 'else:\n'
                irh__jgkod += '  bodo.libs.array_kernels.setna(res, i)'
            else:
                raise ValueError(f'Unknown function name: {func_name}')
            return gen_vectorized(zqd__ebx, firt__gzp, feul__mqgvt,
                irh__jgkod, qjge__jtgwq)
    return overload_numeric_util


def _install_numeric_overload(funcs_utils_names):
    for hjqpu__qayz, vauf__ewdg, func_name in funcs_utils_names:
        zysvr__okunj = create_numeric_func_overload(func_name)
        overload(hjqpu__qayz)(zysvr__okunj)
        ojww__odv = create_numeric_util_overload(func_name)
        overload(vauf__ewdg)(ojww__odv)


_install_numeric_overload(funcs_utils_names)


@numba.generated_jit(nopython=True)
def bitand(A, B):
    args = [A, B]
    for usk__jojap in range(2):
        if isinstance(args[usk__jojap], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitand',
                ['A', 'B'], usk__jojap)

    def impl(A, B):
        return bitand_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftleft(A, B):
    args = [A, B]
    for usk__jojap in range(2):
        if isinstance(args[usk__jojap], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftleft', ['A', 'B'],
                usk__jojap)

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
    for usk__jojap in range(2):
        if isinstance(args[usk__jojap], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitor',
                ['A', 'B'], usk__jojap)

    def impl(A, B):
        return bitor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftright(A, B):
    args = [A, B]
    for usk__jojap in range(2):
        if isinstance(args[usk__jojap], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftright', ['A', 'B'],
                usk__jojap)

    def impl(A, B):
        return bitshiftright_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitxor(A, B):
    args = [A, B]
    for usk__jojap in range(2):
        if isinstance(args[usk__jojap], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitxor',
                ['A', 'B'], usk__jojap)

    def impl(A, B):
        return bitxor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def conv(arr, old_base, new_base):
    args = [arr, old_base, new_base]
    for usk__jojap in range(3):
        if isinstance(args[usk__jojap], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.conv', [
                'arr', 'old_base', 'new_base'], usk__jojap)

    def impl(arr, old_base, new_base):
        return conv_util(arr, old_base, new_base)
    return impl


@numba.generated_jit(nopython=True)
def getbit(A, B):
    args = [A, B]
    for usk__jojap in range(2):
        if isinstance(args[usk__jojap], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.getbit',
                ['A', 'B'], usk__jojap)

    def impl(A, B):
        return getbit_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def haversine(lat1, lon1, lat2, lon2):
    args = [lat1, lon1, lat2, lon2]
    for usk__jojap in range(4):
        if isinstance(args[usk__jojap], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.haversine',
                ['lat1', 'lon1', 'lat2', 'lon2'], usk__jojap)

    def impl(lat1, lon1, lat2, lon2):
        return haversine_util(lat1, lon1, lat2, lon2)
    return impl


@numba.generated_jit(nopython=True)
def div0(arr, divisor):
    args = [arr, divisor]
    for usk__jojap in range(2):
        if isinstance(args[usk__jojap], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.div0', [
                'arr', 'divisor'], usk__jojap)

    def impl(arr, divisor):
        return div0_util(arr, divisor)
    return impl


@numba.generated_jit(nopython=True)
def log(arr, base):
    args = [arr, base]
    for usk__jojap in range(2):
        if isinstance(args[usk__jojap], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.log', [
                'arr', 'base'], usk__jojap)

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
    for usk__jojap in range(4):
        if isinstance(args[usk__jojap], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.width_bucket', ['arr',
                'min_val', 'max_val', 'num_buckets'], usk__jojap)

    def impl(arr, min_val, max_val, num_buckets):
        return width_bucket_util(arr, min_val, max_val, num_buckets)
    return impl


@numba.generated_jit(nopython=True)
def bitand_util(A, B):
    verify_int_arg(A, 'bitand', 'A')
    verify_int_arg(B, 'bitand', 'B')
    zqd__ebx = ['A', 'B']
    firt__gzp = [A, B]
    feul__mqgvt = [True] * 2
    irh__jgkod = 'res[i] = arg0 & arg1'
    qjge__jtgwq = get_common_broadcasted_type([A, B], 'bitand')
    return gen_vectorized(zqd__ebx, firt__gzp, feul__mqgvt, irh__jgkod,
        qjge__jtgwq)


@numba.generated_jit(nopython=True)
def bitshiftleft_util(A, B):
    verify_int_arg(A, 'bitshiftleft', 'A')
    verify_int_arg(B, 'bitshiftleft', 'B')
    zqd__ebx = ['A', 'B']
    firt__gzp = [A, B]
    feul__mqgvt = [True] * 2
    irh__jgkod = 'res[i] = arg0 << arg1'
    qjge__jtgwq = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(zqd__ebx, firt__gzp, feul__mqgvt, irh__jgkod,
        qjge__jtgwq)


@numba.generated_jit(nopython=True)
def bitnot_util(A):
    verify_int_arg(A, 'bitnot', 'A')
    zqd__ebx = ['A']
    firt__gzp = [A]
    feul__mqgvt = [True]
    irh__jgkod = 'res[i] = ~arg0'
    if A == bodo.none:
        qjge__jtgwq = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            fmats__uukx = A.dtype
        else:
            fmats__uukx = A
        qjge__jtgwq = bodo.libs.int_arr_ext.IntegerArrayType(fmats__uukx)
    return gen_vectorized(zqd__ebx, firt__gzp, feul__mqgvt, irh__jgkod,
        qjge__jtgwq)


@numba.generated_jit(nopython=True)
def bitor_util(A, B):
    verify_int_arg(A, 'bitor', 'A')
    verify_int_arg(B, 'bitor', 'B')
    zqd__ebx = ['A', 'B']
    firt__gzp = [A, B]
    feul__mqgvt = [True] * 2
    irh__jgkod = 'res[i] = arg0 | arg1'
    qjge__jtgwq = get_common_broadcasted_type([A, B], 'bitor')
    return gen_vectorized(zqd__ebx, firt__gzp, feul__mqgvt, irh__jgkod,
        qjge__jtgwq)


@numba.generated_jit(nopython=True)
def bitshiftright_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    zqd__ebx = ['A', 'B']
    firt__gzp = [A, B]
    feul__mqgvt = [True] * 2
    if A == bodo.none:
        fmats__uukx = qjge__jtgwq = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            fmats__uukx = A.dtype
        else:
            fmats__uukx = A
        qjge__jtgwq = bodo.libs.int_arr_ext.IntegerArrayType(fmats__uukx)
    irh__jgkod = f'res[i] = arg0 >> arg1\n'
    return gen_vectorized(zqd__ebx, firt__gzp, feul__mqgvt, irh__jgkod,
        qjge__jtgwq)


@numba.generated_jit(nopython=True)
def bitxor_util(A, B):
    verify_int_arg(A, 'bitxor', 'A')
    verify_int_arg(B, 'bitxor', 'B')
    zqd__ebx = ['A', 'B']
    firt__gzp = [A, B]
    feul__mqgvt = [True] * 2
    irh__jgkod = 'res[i] = arg0 ^ arg1'
    qjge__jtgwq = get_common_broadcasted_type([A, B], 'bitxor')
    return gen_vectorized(zqd__ebx, firt__gzp, feul__mqgvt, irh__jgkod,
        qjge__jtgwq)


@numba.generated_jit(nopython=True)
def conv_util(arr, old_base, new_base):
    verify_string_arg(arr, 'CONV', 'arr')
    verify_int_arg(old_base, 'CONV', 'old_base')
    verify_int_arg(new_base, 'CONV', 'new_base')
    zqd__ebx = ['arr', 'old_base', 'new_base']
    firt__gzp = [arr, old_base, new_base]
    feul__mqgvt = [True] * 3
    irh__jgkod = 'old_val = int(arg0, arg1)\n'
    irh__jgkod += 'if arg2 == 2:\n'
    irh__jgkod += "   res[i] = format(old_val, 'b')\n"
    irh__jgkod += 'elif arg2 == 8:\n'
    irh__jgkod += "   res[i] = format(old_val, 'o')\n"
    irh__jgkod += 'elif arg2 == 10:\n'
    irh__jgkod += "   res[i] = format(old_val, 'd')\n"
    irh__jgkod += 'elif arg2 == 16:\n'
    irh__jgkod += "   res[i] = format(old_val, 'x')\n"
    irh__jgkod += 'else:\n'
    irh__jgkod += '   bodo.libs.array_kernels.setna(res, i)\n'
    qjge__jtgwq = bodo.string_array_type
    return gen_vectorized(zqd__ebx, firt__gzp, feul__mqgvt, irh__jgkod,
        qjge__jtgwq)


@numba.generated_jit(nopython=True)
def getbit_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    zqd__ebx = ['A', 'B']
    firt__gzp = [A, B]
    feul__mqgvt = [True] * 2
    irh__jgkod = 'res[i] = (arg0 >> arg1) & 1'
    qjge__jtgwq = bodo.libs.int_arr_ext.IntegerArrayType(types.uint8)
    return gen_vectorized(zqd__ebx, firt__gzp, feul__mqgvt, irh__jgkod,
        qjge__jtgwq)


@numba.generated_jit(nopython=True)
def haversine_util(lat1, lon1, lat2, lon2):
    verify_int_float_arg(lat1, 'HAVERSINE', 'lat1')
    verify_int_float_arg(lon1, 'HAVERSINE', 'lon1')
    verify_int_float_arg(lat2, 'HAVERSINE', 'lat2')
    verify_int_float_arg(lon2, 'HAVERSINE', 'lon2')
    zqd__ebx = ['lat1', 'lon1', 'lat2', 'lon2']
    firt__gzp = [lat1, lon1, lat2, lon2]
    tsu__oliya = [True] * 4
    irh__jgkod = (
        'arg0, arg1, arg2, arg3 = map(np.radians, (arg0, arg1, arg2, arg3))\n')
    trai__awbwi = '(arg2 - arg0) * 0.5'
    fhqvz__uau = '(arg3 - arg1) * 0.5'
    wbb__ngxnh = (
        f'np.square(np.sin({trai__awbwi})) + (np.cos(arg0) * np.cos(arg2) * np.square(np.sin({fhqvz__uau})))'
        )
    irh__jgkod += f'res[i] = 12742.0 * np.arcsin(np.sqrt({wbb__ngxnh}))\n'
    qjge__jtgwq = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(zqd__ebx, firt__gzp, tsu__oliya, irh__jgkod,
        qjge__jtgwq)


@numba.generated_jit(nopython=True)
def div0_util(arr, divisor):
    verify_int_float_arg(arr, 'DIV0', 'arr')
    verify_int_float_arg(divisor, 'DIV0', 'divisor')
    zqd__ebx = ['arr', 'divisor']
    firt__gzp = [arr, divisor]
    tsu__oliya = [True] * 2
    irh__jgkod = 'res[i] = arg0 / arg1 if arg1 else 0\n'
    qjge__jtgwq = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(zqd__ebx, firt__gzp, tsu__oliya, irh__jgkod,
        qjge__jtgwq)


@numba.generated_jit(nopython=True)
def log_util(arr, base):
    verify_int_float_arg(arr, 'log', 'arr')
    verify_int_float_arg(base, 'log', 'base')
    zqd__ebx = ['arr', 'base']
    firt__gzp = [arr, base]
    feul__mqgvt = [True] * 2
    irh__jgkod = 'res[i] = np.log(arg0) / np.log(arg1)'
    qjge__jtgwq = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(zqd__ebx, firt__gzp, feul__mqgvt, irh__jgkod,
        qjge__jtgwq)


@numba.generated_jit(nopython=True)
def negate_util(arr):
    zqd__ebx = ['arr']
    firt__gzp = [arr]
    feul__mqgvt = [True]
    if bodo.utils.utils.is_array_typ(arr, False):
        fmats__uukx = arr.dtype
    elif bodo.utils.utils.is_array_typ(arr, True):
        fmats__uukx = arr.data.dtype
    else:
        fmats__uukx = arr
    irh__jgkod = {types.uint8: 'res[i] = -np.int16(arg0)', types.uint16:
        'res[i] = -np.int32(arg0)', types.uint32: 'res[i] = -np.int64(arg0)'
        }.get(fmats__uukx, 'res[i] = -arg0')
    fmats__uukx = {types.uint8: types.int16, types.uint16: types.int32,
        types.uint32: types.int64, types.uint64: types.int64}.get(fmats__uukx,
        fmats__uukx)
    if isinstance(fmats__uukx, types.Integer):
        qjge__jtgwq = bodo.utils.typing.dtype_to_array_type(fmats__uukx)
    else:
        qjge__jtgwq = arr
    qjge__jtgwq = bodo.utils.typing.to_nullable_type(qjge__jtgwq)
    return gen_vectorized(zqd__ebx, firt__gzp, feul__mqgvt, irh__jgkod,
        qjge__jtgwq)


@numba.generated_jit(nopython=True)
def width_bucket_util(arr, min_val, max_val, num_buckets):
    verify_int_float_arg(arr, 'WIDTH_BUCKET', 'arr')
    verify_int_float_arg(min_val, 'WIDTH_BUCKET', 'min_val')
    verify_int_float_arg(max_val, 'WIDTH_BUCKET', 'max_val')
    verify_int_arg(num_buckets, 'WIDTH_BUCKET', 'num_buckets')
    zqd__ebx = ['arr', 'min_val', 'max_val', 'num_buckets']
    firt__gzp = [arr, min_val, max_val, num_buckets]
    feul__mqgvt = [True] * 4
    irh__jgkod = (
        "if arg1 >= arg2: raise ValueError('min_val must be less than max_val')\n"
        )
    irh__jgkod += (
        "if arg3 <= 0: raise ValueError('num_buckets must be a positive integer')\n"
        )
    irh__jgkod += (
        'res[i] = min(max(-1.0, math.floor((arg0 - arg1) / ((arg2 - arg1) / arg3))), arg3) + 1.0'
        )
    qjge__jtgwq = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(zqd__ebx, firt__gzp, feul__mqgvt, irh__jgkod,
        qjge__jtgwq)
