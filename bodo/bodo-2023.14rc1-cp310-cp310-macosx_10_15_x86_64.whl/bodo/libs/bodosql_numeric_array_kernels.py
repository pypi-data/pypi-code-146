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
    mnffj__eot = arr0.dtype if is_array_typ(arr0) else arr0
    ysu__pycd = arr1.dtype if is_array_typ(arr1) else arr1
    chzh__bahye = bodo.float64
    if (arr0 is None or mnffj__eot == bodo.none
        ) or func_name in double_arg_funcs and (arr1 is None or ysu__pycd ==
        bodo.none):
        return types.Array(chzh__bahye, 1, 'C')
    if isinstance(mnffj__eot, types.Float):
        if isinstance(ysu__pycd, types.Float):
            chzh__bahye = _float[max(mnffj__eot.bitwidth, ysu__pycd.bitwidth)]
        else:
            chzh__bahye = mnffj__eot
    if func_name == 'SIGN':
        if isinstance(mnffj__eot, types.Integer):
            chzh__bahye = mnffj__eot
    elif func_name == 'MOD':
        if isinstance(mnffj__eot, types.Integer) and isinstance(ysu__pycd,
            types.Integer):
            if mnffj__eot.signed:
                if ysu__pycd.signed:
                    chzh__bahye = ysu__pycd
                else:
                    chzh__bahye = _int[min(64, ysu__pycd.bitwidth * 2)]
            else:
                chzh__bahye = ysu__pycd
    elif func_name == 'ABS':
        if isinstance(mnffj__eot, types.Integer):
            if mnffj__eot.signed:
                chzh__bahye = _uint[min(64, mnffj__eot.bitwidth * 2)]
            else:
                chzh__bahye = mnffj__eot
    elif func_name == 'ROUND':
        if isinstance(mnffj__eot, (types.Float, types.Integer)):
            chzh__bahye = mnffj__eot
    elif func_name == 'FACTORIAL':
        chzh__bahye = bodo.int64
    if isinstance(chzh__bahye, types.Integer):
        return bodo.libs.int_arr_ext.IntegerArrayType(chzh__bahye)
    else:
        return types.Array(chzh__bahye, 1, 'C')


def create_numeric_func_overload(func_name):
    if func_name not in double_arg_funcs:
        func_name = func_name.lower()

        def overload_func(arr):
            if isinstance(arr, types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.{func_name}', ['arr'], 0)
            dwzyq__mszu = 'def impl(arr):\n'
            dwzyq__mszu += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr)'
                )
            ckzdt__qkhjq = {}
            exec(dwzyq__mszu, {'bodo': bodo}, ckzdt__qkhjq)
            return ckzdt__qkhjq['impl']
    else:
        func_name = func_name.lower()

        def overload_func(arr0, arr1):
            args = [arr0, arr1]
            for ybcf__hoide in range(2):
                if isinstance(args[ybcf__hoide], types.optional):
                    return unopt_argument(
                        f'bodo.libs.bodosql_array_kernels.{func_name}', [
                        'arr0', 'arr1'], ybcf__hoide)
            dwzyq__mszu = 'def impl(arr0, arr1):\n'
            dwzyq__mszu += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr0, arr1)'
                )
            ckzdt__qkhjq = {}
            exec(dwzyq__mszu, {'bodo': bodo}, ckzdt__qkhjq)
            return ckzdt__qkhjq['impl']
    return overload_func


def create_numeric_util_overload(func_name):
    if func_name not in double_arg_funcs:

        def overload_numeric_util(arr):
            verify_int_float_arg(arr, func_name, 'arr')
            bmmq__dnl = ['arr']
            hpr__vlchi = [arr]
            mujm__vftd = [True]
            xgiec__fnol = ''
            if func_name in single_arg_funcs:
                if func_name == 'FACTORIAL':
                    xgiec__fnol += (
                        'if arg0 > 20 or np.abs(np.int64(arg0)) != arg0:\n')
                    xgiec__fnol += '  bodo.libs.array_kernels.setna(res, i)\n'
                    xgiec__fnol += 'else:\n'
                    xgiec__fnol += (
                        f'  res[i] = np.math.factorial(np.int64(arg0))')
                elif func_name == 'LN':
                    xgiec__fnol += f'res[i] = np.log(arg0)'
                else:
                    xgiec__fnol += f'res[i] = np.{func_name.lower()}(arg0)'
            else:
                ValueError(f'Unknown function name: {func_name}')
            chzh__bahye = _get_numeric_output_dtype(func_name, arr)
            return gen_vectorized(bmmq__dnl, hpr__vlchi, mujm__vftd,
                xgiec__fnol, chzh__bahye)
    else:

        def overload_numeric_util(arr0, arr1):
            verify_int_float_arg(arr0, func_name, 'arr0')
            verify_int_float_arg(arr0, func_name, 'arr1')
            bmmq__dnl = ['arr0', 'arr1']
            hpr__vlchi = [arr0, arr1]
            mujm__vftd = [True, True]
            chzh__bahye = _get_numeric_output_dtype(func_name, arr0, arr1)
            xgiec__fnol = ''
            if func_name == 'MOD':
                xgiec__fnol += 'if arg1 == 0:\n'
                xgiec__fnol += '  bodo.libs.array_kernels.setna(res, i)\n'
                xgiec__fnol += 'else:\n'
                xgiec__fnol += (
                    '  res[i] = np.sign(arg0) * np.mod(np.abs(arg0), np.abs(arg1))'
                    )
            elif func_name == 'POWER':
                xgiec__fnol += 'res[i] = np.power(np.float64(arg0), arg1)'
            elif func_name == 'ROUND':
                xgiec__fnol += 'res[i] = np.round(arg0, arg1)'
            elif func_name == 'TRUNC':
                xgiec__fnol += 'if int(arg1) == arg1:\n'
                xgiec__fnol += (
                    '  res[i] = np.trunc(arg0 * (10.0 ** arg1)) * (10.0 ** -arg1)\n'
                    )
                xgiec__fnol += 'else:\n'
                xgiec__fnol += '  bodo.libs.array_kernels.setna(res, i)'
            else:
                raise ValueError(f'Unknown function name: {func_name}')
            return gen_vectorized(bmmq__dnl, hpr__vlchi, mujm__vftd,
                xgiec__fnol, chzh__bahye)
    return overload_numeric_util


def _install_numeric_overload(funcs_utils_names):
    for rlht__xwgl, wrjm__qaszm, func_name in funcs_utils_names:
        nqbc__pqi = create_numeric_func_overload(func_name)
        overload(rlht__xwgl)(nqbc__pqi)
        ckwk__rizuh = create_numeric_util_overload(func_name)
        overload(wrjm__qaszm)(ckwk__rizuh)


_install_numeric_overload(funcs_utils_names)


@numba.generated_jit(nopython=True)
def bitand(A, B):
    args = [A, B]
    for ybcf__hoide in range(2):
        if isinstance(args[ybcf__hoide], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitand',
                ['A', 'B'], ybcf__hoide)

    def impl(A, B):
        return bitand_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftleft(A, B):
    args = [A, B]
    for ybcf__hoide in range(2):
        if isinstance(args[ybcf__hoide], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftleft', ['A', 'B'],
                ybcf__hoide)

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
    for ybcf__hoide in range(2):
        if isinstance(args[ybcf__hoide], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitor',
                ['A', 'B'], ybcf__hoide)

    def impl(A, B):
        return bitor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftright(A, B):
    args = [A, B]
    for ybcf__hoide in range(2):
        if isinstance(args[ybcf__hoide], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftright', ['A', 'B'],
                ybcf__hoide)

    def impl(A, B):
        return bitshiftright_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitxor(A, B):
    args = [A, B]
    for ybcf__hoide in range(2):
        if isinstance(args[ybcf__hoide], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitxor',
                ['A', 'B'], ybcf__hoide)

    def impl(A, B):
        return bitxor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def conv(arr, old_base, new_base):
    args = [arr, old_base, new_base]
    for ybcf__hoide in range(3):
        if isinstance(args[ybcf__hoide], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.conv', [
                'arr', 'old_base', 'new_base'], ybcf__hoide)

    def impl(arr, old_base, new_base):
        return conv_util(arr, old_base, new_base)
    return impl


@numba.generated_jit(nopython=True)
def getbit(A, B):
    args = [A, B]
    for ybcf__hoide in range(2):
        if isinstance(args[ybcf__hoide], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.getbit',
                ['A', 'B'], ybcf__hoide)

    def impl(A, B):
        return getbit_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def haversine(lat1, lon1, lat2, lon2):
    args = [lat1, lon1, lat2, lon2]
    for ybcf__hoide in range(4):
        if isinstance(args[ybcf__hoide], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.haversine',
                ['lat1', 'lon1', 'lat2', 'lon2'], ybcf__hoide)

    def impl(lat1, lon1, lat2, lon2):
        return haversine_util(lat1, lon1, lat2, lon2)
    return impl


@numba.generated_jit(nopython=True)
def div0(arr, divisor):
    args = [arr, divisor]
    for ybcf__hoide in range(2):
        if isinstance(args[ybcf__hoide], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.div0', [
                'arr', 'divisor'], ybcf__hoide)

    def impl(arr, divisor):
        return div0_util(arr, divisor)
    return impl


@numba.generated_jit(nopython=True)
def log(arr, base):
    args = [arr, base]
    for ybcf__hoide in range(2):
        if isinstance(args[ybcf__hoide], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.log', [
                'arr', 'base'], ybcf__hoide)

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
    for ybcf__hoide in range(4):
        if isinstance(args[ybcf__hoide], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.width_bucket', ['arr',
                'min_val', 'max_val', 'num_buckets'], ybcf__hoide)

    def impl(arr, min_val, max_val, num_buckets):
        return width_bucket_util(arr, min_val, max_val, num_buckets)
    return impl


@numba.generated_jit(nopython=True)
def bitand_util(A, B):
    verify_int_arg(A, 'bitand', 'A')
    verify_int_arg(B, 'bitand', 'B')
    bmmq__dnl = ['A', 'B']
    hpr__vlchi = [A, B]
    mujm__vftd = [True] * 2
    xgiec__fnol = 'res[i] = arg0 & arg1'
    chzh__bahye = get_common_broadcasted_type([A, B], 'bitand')
    return gen_vectorized(bmmq__dnl, hpr__vlchi, mujm__vftd, xgiec__fnol,
        chzh__bahye)


@numba.generated_jit(nopython=True)
def bitshiftleft_util(A, B):
    verify_int_arg(A, 'bitshiftleft', 'A')
    verify_int_arg(B, 'bitshiftleft', 'B')
    bmmq__dnl = ['A', 'B']
    hpr__vlchi = [A, B]
    mujm__vftd = [True] * 2
    xgiec__fnol = 'res[i] = arg0 << arg1'
    chzh__bahye = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(bmmq__dnl, hpr__vlchi, mujm__vftd, xgiec__fnol,
        chzh__bahye)


@numba.generated_jit(nopython=True)
def bitnot_util(A):
    verify_int_arg(A, 'bitnot', 'A')
    bmmq__dnl = ['A']
    hpr__vlchi = [A]
    mujm__vftd = [True]
    xgiec__fnol = 'res[i] = ~arg0'
    if A == bodo.none:
        chzh__bahye = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            iomx__roqz = A.dtype
        else:
            iomx__roqz = A
        chzh__bahye = bodo.libs.int_arr_ext.IntegerArrayType(iomx__roqz)
    return gen_vectorized(bmmq__dnl, hpr__vlchi, mujm__vftd, xgiec__fnol,
        chzh__bahye)


@numba.generated_jit(nopython=True)
def bitor_util(A, B):
    verify_int_arg(A, 'bitor', 'A')
    verify_int_arg(B, 'bitor', 'B')
    bmmq__dnl = ['A', 'B']
    hpr__vlchi = [A, B]
    mujm__vftd = [True] * 2
    xgiec__fnol = 'res[i] = arg0 | arg1'
    chzh__bahye = get_common_broadcasted_type([A, B], 'bitor')
    return gen_vectorized(bmmq__dnl, hpr__vlchi, mujm__vftd, xgiec__fnol,
        chzh__bahye)


@numba.generated_jit(nopython=True)
def bitshiftright_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    bmmq__dnl = ['A', 'B']
    hpr__vlchi = [A, B]
    mujm__vftd = [True] * 2
    if A == bodo.none:
        iomx__roqz = chzh__bahye = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            iomx__roqz = A.dtype
        else:
            iomx__roqz = A
        chzh__bahye = bodo.libs.int_arr_ext.IntegerArrayType(iomx__roqz)
    xgiec__fnol = f'res[i] = arg0 >> arg1\n'
    return gen_vectorized(bmmq__dnl, hpr__vlchi, mujm__vftd, xgiec__fnol,
        chzh__bahye)


@numba.generated_jit(nopython=True)
def bitxor_util(A, B):
    verify_int_arg(A, 'bitxor', 'A')
    verify_int_arg(B, 'bitxor', 'B')
    bmmq__dnl = ['A', 'B']
    hpr__vlchi = [A, B]
    mujm__vftd = [True] * 2
    xgiec__fnol = 'res[i] = arg0 ^ arg1'
    chzh__bahye = get_common_broadcasted_type([A, B], 'bitxor')
    return gen_vectorized(bmmq__dnl, hpr__vlchi, mujm__vftd, xgiec__fnol,
        chzh__bahye)


@numba.generated_jit(nopython=True)
def conv_util(arr, old_base, new_base):
    verify_string_arg(arr, 'CONV', 'arr')
    verify_int_arg(old_base, 'CONV', 'old_base')
    verify_int_arg(new_base, 'CONV', 'new_base')
    bmmq__dnl = ['arr', 'old_base', 'new_base']
    hpr__vlchi = [arr, old_base, new_base]
    mujm__vftd = [True] * 3
    xgiec__fnol = 'old_val = int(arg0, arg1)\n'
    xgiec__fnol += 'if arg2 == 2:\n'
    xgiec__fnol += "   res[i] = format(old_val, 'b')\n"
    xgiec__fnol += 'elif arg2 == 8:\n'
    xgiec__fnol += "   res[i] = format(old_val, 'o')\n"
    xgiec__fnol += 'elif arg2 == 10:\n'
    xgiec__fnol += "   res[i] = format(old_val, 'd')\n"
    xgiec__fnol += 'elif arg2 == 16:\n'
    xgiec__fnol += "   res[i] = format(old_val, 'x')\n"
    xgiec__fnol += 'else:\n'
    xgiec__fnol += '   bodo.libs.array_kernels.setna(res, i)\n'
    chzh__bahye = bodo.string_array_type
    return gen_vectorized(bmmq__dnl, hpr__vlchi, mujm__vftd, xgiec__fnol,
        chzh__bahye)


@numba.generated_jit(nopython=True)
def getbit_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    bmmq__dnl = ['A', 'B']
    hpr__vlchi = [A, B]
    mujm__vftd = [True] * 2
    xgiec__fnol = 'res[i] = (arg0 >> arg1) & 1'
    chzh__bahye = bodo.libs.int_arr_ext.IntegerArrayType(types.uint8)
    return gen_vectorized(bmmq__dnl, hpr__vlchi, mujm__vftd, xgiec__fnol,
        chzh__bahye)


@numba.generated_jit(nopython=True)
def haversine_util(lat1, lon1, lat2, lon2):
    verify_int_float_arg(lat1, 'HAVERSINE', 'lat1')
    verify_int_float_arg(lon1, 'HAVERSINE', 'lon1')
    verify_int_float_arg(lat2, 'HAVERSINE', 'lat2')
    verify_int_float_arg(lon2, 'HAVERSINE', 'lon2')
    bmmq__dnl = ['lat1', 'lon1', 'lat2', 'lon2']
    hpr__vlchi = [lat1, lon1, lat2, lon2]
    emvb__maekd = [True] * 4
    xgiec__fnol = (
        'arg0, arg1, arg2, arg3 = map(np.radians, (arg0, arg1, arg2, arg3))\n')
    pcdbj__nfnt = '(arg2 - arg0) * 0.5'
    cjs__opo = '(arg3 - arg1) * 0.5'
    nvb__llcd = (
        f'np.square(np.sin({pcdbj__nfnt})) + (np.cos(arg0) * np.cos(arg2) * np.square(np.sin({cjs__opo})))'
        )
    xgiec__fnol += f'res[i] = 12742.0 * np.arcsin(np.sqrt({nvb__llcd}))\n'
    chzh__bahye = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(bmmq__dnl, hpr__vlchi, emvb__maekd, xgiec__fnol,
        chzh__bahye)


@numba.generated_jit(nopython=True)
def div0_util(arr, divisor):
    verify_int_float_arg(arr, 'DIV0', 'arr')
    verify_int_float_arg(divisor, 'DIV0', 'divisor')
    bmmq__dnl = ['arr', 'divisor']
    hpr__vlchi = [arr, divisor]
    emvb__maekd = [True] * 2
    xgiec__fnol = 'res[i] = arg0 / arg1 if arg1 else 0\n'
    chzh__bahye = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(bmmq__dnl, hpr__vlchi, emvb__maekd, xgiec__fnol,
        chzh__bahye)


@numba.generated_jit(nopython=True)
def log_util(arr, base):
    verify_int_float_arg(arr, 'log', 'arr')
    verify_int_float_arg(base, 'log', 'base')
    bmmq__dnl = ['arr', 'base']
    hpr__vlchi = [arr, base]
    mujm__vftd = [True] * 2
    xgiec__fnol = 'res[i] = np.log(arg0) / np.log(arg1)'
    chzh__bahye = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(bmmq__dnl, hpr__vlchi, mujm__vftd, xgiec__fnol,
        chzh__bahye)


@numba.generated_jit(nopython=True)
def negate_util(arr):
    bmmq__dnl = ['arr']
    hpr__vlchi = [arr]
    mujm__vftd = [True]
    if bodo.utils.utils.is_array_typ(arr, False):
        iomx__roqz = arr.dtype
    elif bodo.utils.utils.is_array_typ(arr, True):
        iomx__roqz = arr.data.dtype
    else:
        iomx__roqz = arr
    xgiec__fnol = {types.uint8: 'res[i] = -np.int16(arg0)', types.uint16:
        'res[i] = -np.int32(arg0)', types.uint32: 'res[i] = -np.int64(arg0)'
        }.get(iomx__roqz, 'res[i] = -arg0')
    iomx__roqz = {types.uint8: types.int16, types.uint16: types.int32,
        types.uint32: types.int64, types.uint64: types.int64}.get(iomx__roqz,
        iomx__roqz)
    if isinstance(iomx__roqz, types.Integer):
        chzh__bahye = bodo.utils.typing.dtype_to_array_type(iomx__roqz)
    else:
        chzh__bahye = arr
    chzh__bahye = bodo.utils.typing.to_nullable_type(chzh__bahye)
    return gen_vectorized(bmmq__dnl, hpr__vlchi, mujm__vftd, xgiec__fnol,
        chzh__bahye)


@numba.generated_jit(nopython=True)
def width_bucket_util(arr, min_val, max_val, num_buckets):
    verify_int_float_arg(arr, 'WIDTH_BUCKET', 'arr')
    verify_int_float_arg(min_val, 'WIDTH_BUCKET', 'min_val')
    verify_int_float_arg(max_val, 'WIDTH_BUCKET', 'max_val')
    verify_int_arg(num_buckets, 'WIDTH_BUCKET', 'num_buckets')
    bmmq__dnl = ['arr', 'min_val', 'max_val', 'num_buckets']
    hpr__vlchi = [arr, min_val, max_val, num_buckets]
    mujm__vftd = [True] * 4
    xgiec__fnol = (
        "if arg1 >= arg2: raise ValueError('min_val must be less than max_val')\n"
        )
    xgiec__fnol += (
        "if arg3 <= 0: raise ValueError('num_buckets must be a positive integer')\n"
        )
    xgiec__fnol += (
        'res[i] = min(max(-1.0, math.floor((arg0 - arg1) / ((arg2 - arg1) / arg3))), arg3) + 1.0'
        )
    chzh__bahye = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(bmmq__dnl, hpr__vlchi, mujm__vftd, xgiec__fnol,
        chzh__bahye)
