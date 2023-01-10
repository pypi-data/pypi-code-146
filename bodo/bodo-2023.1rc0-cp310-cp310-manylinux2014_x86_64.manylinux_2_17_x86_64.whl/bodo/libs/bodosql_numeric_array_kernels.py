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
    njccx__qyss = arr0.dtype if is_array_typ(arr0) else arr0
    osxb__wbn = arr1.dtype if is_array_typ(arr1) else arr1
    dob__wtdld = bodo.float64
    if (arr0 is None or njccx__qyss == bodo.none
        ) or func_name in double_arg_funcs and (arr1 is None or osxb__wbn ==
        bodo.none):
        return types.Array(dob__wtdld, 1, 'C')
    if isinstance(njccx__qyss, types.Float):
        if isinstance(osxb__wbn, types.Float):
            dob__wtdld = _float[max(njccx__qyss.bitwidth, osxb__wbn.bitwidth)]
        else:
            dob__wtdld = njccx__qyss
    if func_name == 'SIGN':
        if isinstance(njccx__qyss, types.Integer):
            dob__wtdld = njccx__qyss
    elif func_name == 'MOD':
        if isinstance(njccx__qyss, types.Integer) and isinstance(osxb__wbn,
            types.Integer):
            if njccx__qyss.signed:
                if osxb__wbn.signed:
                    dob__wtdld = osxb__wbn
                else:
                    dob__wtdld = _int[min(64, osxb__wbn.bitwidth * 2)]
            else:
                dob__wtdld = osxb__wbn
    elif func_name == 'ABS':
        if isinstance(njccx__qyss, types.Integer):
            if njccx__qyss.signed:
                dob__wtdld = _uint[min(64, njccx__qyss.bitwidth * 2)]
            else:
                dob__wtdld = njccx__qyss
    elif func_name == 'ROUND':
        if isinstance(njccx__qyss, (types.Float, types.Integer)):
            dob__wtdld = njccx__qyss
    elif func_name == 'FACTORIAL':
        dob__wtdld = bodo.int64
    if isinstance(dob__wtdld, types.Integer):
        return bodo.libs.int_arr_ext.IntegerArrayType(dob__wtdld)
    else:
        return types.Array(dob__wtdld, 1, 'C')


def create_numeric_func_overload(func_name):
    if func_name not in double_arg_funcs:
        func_name = func_name.lower()

        def overload_func(arr):
            if isinstance(arr, types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.{func_name}', ['arr'], 0)
            hboam__utuu = 'def impl(arr):\n'
            hboam__utuu += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr)'
                )
            pozr__axyp = {}
            exec(hboam__utuu, {'bodo': bodo}, pozr__axyp)
            return pozr__axyp['impl']
    else:
        func_name = func_name.lower()

        def overload_func(arr0, arr1):
            args = [arr0, arr1]
            for sly__bfvog in range(2):
                if isinstance(args[sly__bfvog], types.optional):
                    return unopt_argument(
                        f'bodo.libs.bodosql_array_kernels.{func_name}', [
                        'arr0', 'arr1'], sly__bfvog)
            hboam__utuu = 'def impl(arr0, arr1):\n'
            hboam__utuu += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr0, arr1)'
                )
            pozr__axyp = {}
            exec(hboam__utuu, {'bodo': bodo}, pozr__axyp)
            return pozr__axyp['impl']
    return overload_func


def create_numeric_util_overload(func_name):
    if func_name not in double_arg_funcs:

        def overload_numeric_util(arr):
            verify_int_float_arg(arr, func_name, 'arr')
            xkxej__jgbq = ['arr']
            hdl__khpa = [arr]
            dmw__kcr = [True]
            gvat__gkk = ''
            if func_name in single_arg_funcs:
                if func_name == 'FACTORIAL':
                    gvat__gkk += (
                        'if arg0 > 20 or np.abs(np.int64(arg0)) != arg0:\n')
                    gvat__gkk += '  bodo.libs.array_kernels.setna(res, i)\n'
                    gvat__gkk += 'else:\n'
                    gvat__gkk += (
                        f'  res[i] = np.math.factorial(np.int64(arg0))')
                elif func_name == 'LN':
                    gvat__gkk += f'res[i] = np.log(arg0)'
                else:
                    gvat__gkk += f'res[i] = np.{func_name.lower()}(arg0)'
            else:
                ValueError(f'Unknown function name: {func_name}')
            dob__wtdld = _get_numeric_output_dtype(func_name, arr)
            return gen_vectorized(xkxej__jgbq, hdl__khpa, dmw__kcr,
                gvat__gkk, dob__wtdld)
    else:

        def overload_numeric_util(arr0, arr1):
            verify_int_float_arg(arr0, func_name, 'arr0')
            verify_int_float_arg(arr0, func_name, 'arr1')
            xkxej__jgbq = ['arr0', 'arr1']
            hdl__khpa = [arr0, arr1]
            dmw__kcr = [True, True]
            dob__wtdld = _get_numeric_output_dtype(func_name, arr0, arr1)
            gvat__gkk = ''
            if func_name == 'MOD':
                gvat__gkk += 'if arg1 == 0:\n'
                gvat__gkk += '  bodo.libs.array_kernels.setna(res, i)\n'
                gvat__gkk += 'else:\n'
                gvat__gkk += (
                    '  res[i] = np.sign(arg0) * np.mod(np.abs(arg0), np.abs(arg1))'
                    )
            elif func_name == 'POWER':
                gvat__gkk += 'res[i] = np.power(np.float64(arg0), arg1)'
            elif func_name == 'ROUND':
                gvat__gkk += 'res[i] = np.round(arg0, arg1)'
            elif func_name == 'TRUNC':
                gvat__gkk += 'if int(arg1) == arg1:\n'
                gvat__gkk += (
                    '  res[i] = np.trunc(arg0 * (10.0 ** arg1)) * (10.0 ** -arg1)\n'
                    )
                gvat__gkk += 'else:\n'
                gvat__gkk += '  bodo.libs.array_kernels.setna(res, i)'
            else:
                raise ValueError(f'Unknown function name: {func_name}')
            return gen_vectorized(xkxej__jgbq, hdl__khpa, dmw__kcr,
                gvat__gkk, dob__wtdld)
    return overload_numeric_util


def _install_numeric_overload(funcs_utils_names):
    for rmi__khri, euye__udc, func_name in funcs_utils_names:
        eilif__vabi = create_numeric_func_overload(func_name)
        overload(rmi__khri)(eilif__vabi)
        cewtj__wiyd = create_numeric_util_overload(func_name)
        overload(euye__udc)(cewtj__wiyd)


_install_numeric_overload(funcs_utils_names)


@numba.generated_jit(nopython=True)
def bitand(A, B):
    args = [A, B]
    for sly__bfvog in range(2):
        if isinstance(args[sly__bfvog], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitand',
                ['A', 'B'], sly__bfvog)

    def impl(A, B):
        return bitand_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftleft(A, B):
    args = [A, B]
    for sly__bfvog in range(2):
        if isinstance(args[sly__bfvog], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftleft', ['A', 'B'],
                sly__bfvog)

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
    for sly__bfvog in range(2):
        if isinstance(args[sly__bfvog], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitor',
                ['A', 'B'], sly__bfvog)

    def impl(A, B):
        return bitor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftright(A, B):
    args = [A, B]
    for sly__bfvog in range(2):
        if isinstance(args[sly__bfvog], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftright', ['A', 'B'],
                sly__bfvog)

    def impl(A, B):
        return bitshiftright_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitxor(A, B):
    args = [A, B]
    for sly__bfvog in range(2):
        if isinstance(args[sly__bfvog], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitxor',
                ['A', 'B'], sly__bfvog)

    def impl(A, B):
        return bitxor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def conv(arr, old_base, new_base):
    args = [arr, old_base, new_base]
    for sly__bfvog in range(3):
        if isinstance(args[sly__bfvog], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.conv', [
                'arr', 'old_base', 'new_base'], sly__bfvog)

    def impl(arr, old_base, new_base):
        return conv_util(arr, old_base, new_base)
    return impl


@numba.generated_jit(nopython=True)
def getbit(A, B):
    args = [A, B]
    for sly__bfvog in range(2):
        if isinstance(args[sly__bfvog], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.getbit',
                ['A', 'B'], sly__bfvog)

    def impl(A, B):
        return getbit_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def haversine(lat1, lon1, lat2, lon2):
    args = [lat1, lon1, lat2, lon2]
    for sly__bfvog in range(4):
        if isinstance(args[sly__bfvog], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.haversine',
                ['lat1', 'lon1', 'lat2', 'lon2'], sly__bfvog)

    def impl(lat1, lon1, lat2, lon2):
        return haversine_util(lat1, lon1, lat2, lon2)
    return impl


@numba.generated_jit(nopython=True)
def div0(arr, divisor):
    args = [arr, divisor]
    for sly__bfvog in range(2):
        if isinstance(args[sly__bfvog], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.div0', [
                'arr', 'divisor'], sly__bfvog)

    def impl(arr, divisor):
        return div0_util(arr, divisor)
    return impl


@numba.generated_jit(nopython=True)
def log(arr, base):
    args = [arr, base]
    for sly__bfvog in range(2):
        if isinstance(args[sly__bfvog], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.log', [
                'arr', 'base'], sly__bfvog)

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
    for sly__bfvog in range(4):
        if isinstance(args[sly__bfvog], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.width_bucket', ['arr',
                'min_val', 'max_val', 'num_buckets'], sly__bfvog)

    def impl(arr, min_val, max_val, num_buckets):
        return width_bucket_util(arr, min_val, max_val, num_buckets)
    return impl


@numba.generated_jit(nopython=True)
def bitand_util(A, B):
    verify_int_arg(A, 'bitand', 'A')
    verify_int_arg(B, 'bitand', 'B')
    xkxej__jgbq = ['A', 'B']
    hdl__khpa = [A, B]
    dmw__kcr = [True] * 2
    gvat__gkk = 'res[i] = arg0 & arg1'
    dob__wtdld = get_common_broadcasted_type([A, B], 'bitand')
    return gen_vectorized(xkxej__jgbq, hdl__khpa, dmw__kcr, gvat__gkk,
        dob__wtdld)


@numba.generated_jit(nopython=True)
def bitshiftleft_util(A, B):
    verify_int_arg(A, 'bitshiftleft', 'A')
    verify_int_arg(B, 'bitshiftleft', 'B')
    xkxej__jgbq = ['A', 'B']
    hdl__khpa = [A, B]
    dmw__kcr = [True] * 2
    gvat__gkk = 'res[i] = arg0 << arg1'
    dob__wtdld = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(xkxej__jgbq, hdl__khpa, dmw__kcr, gvat__gkk,
        dob__wtdld)


@numba.generated_jit(nopython=True)
def bitnot_util(A):
    verify_int_arg(A, 'bitnot', 'A')
    xkxej__jgbq = ['A']
    hdl__khpa = [A]
    dmw__kcr = [True]
    gvat__gkk = 'res[i] = ~arg0'
    if A == bodo.none:
        dob__wtdld = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            mwvn__svd = A.dtype
        else:
            mwvn__svd = A
        dob__wtdld = bodo.libs.int_arr_ext.IntegerArrayType(mwvn__svd)
    return gen_vectorized(xkxej__jgbq, hdl__khpa, dmw__kcr, gvat__gkk,
        dob__wtdld)


@numba.generated_jit(nopython=True)
def bitor_util(A, B):
    verify_int_arg(A, 'bitor', 'A')
    verify_int_arg(B, 'bitor', 'B')
    xkxej__jgbq = ['A', 'B']
    hdl__khpa = [A, B]
    dmw__kcr = [True] * 2
    gvat__gkk = 'res[i] = arg0 | arg1'
    dob__wtdld = get_common_broadcasted_type([A, B], 'bitor')
    return gen_vectorized(xkxej__jgbq, hdl__khpa, dmw__kcr, gvat__gkk,
        dob__wtdld)


@numba.generated_jit(nopython=True)
def bitshiftright_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    xkxej__jgbq = ['A', 'B']
    hdl__khpa = [A, B]
    dmw__kcr = [True] * 2
    if A == bodo.none:
        mwvn__svd = dob__wtdld = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            mwvn__svd = A.dtype
        else:
            mwvn__svd = A
        dob__wtdld = bodo.libs.int_arr_ext.IntegerArrayType(mwvn__svd)
    gvat__gkk = f'res[i] = arg0 >> arg1\n'
    return gen_vectorized(xkxej__jgbq, hdl__khpa, dmw__kcr, gvat__gkk,
        dob__wtdld)


@numba.generated_jit(nopython=True)
def bitxor_util(A, B):
    verify_int_arg(A, 'bitxor', 'A')
    verify_int_arg(B, 'bitxor', 'B')
    xkxej__jgbq = ['A', 'B']
    hdl__khpa = [A, B]
    dmw__kcr = [True] * 2
    gvat__gkk = 'res[i] = arg0 ^ arg1'
    dob__wtdld = get_common_broadcasted_type([A, B], 'bitxor')
    return gen_vectorized(xkxej__jgbq, hdl__khpa, dmw__kcr, gvat__gkk,
        dob__wtdld)


@numba.generated_jit(nopython=True)
def conv_util(arr, old_base, new_base):
    verify_string_arg(arr, 'CONV', 'arr')
    verify_int_arg(old_base, 'CONV', 'old_base')
    verify_int_arg(new_base, 'CONV', 'new_base')
    xkxej__jgbq = ['arr', 'old_base', 'new_base']
    hdl__khpa = [arr, old_base, new_base]
    dmw__kcr = [True] * 3
    gvat__gkk = 'old_val = int(arg0, arg1)\n'
    gvat__gkk += 'if arg2 == 2:\n'
    gvat__gkk += "   res[i] = format(old_val, 'b')\n"
    gvat__gkk += 'elif arg2 == 8:\n'
    gvat__gkk += "   res[i] = format(old_val, 'o')\n"
    gvat__gkk += 'elif arg2 == 10:\n'
    gvat__gkk += "   res[i] = format(old_val, 'd')\n"
    gvat__gkk += 'elif arg2 == 16:\n'
    gvat__gkk += "   res[i] = format(old_val, 'x')\n"
    gvat__gkk += 'else:\n'
    gvat__gkk += '   bodo.libs.array_kernels.setna(res, i)\n'
    dob__wtdld = bodo.string_array_type
    return gen_vectorized(xkxej__jgbq, hdl__khpa, dmw__kcr, gvat__gkk,
        dob__wtdld)


@numba.generated_jit(nopython=True)
def getbit_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    xkxej__jgbq = ['A', 'B']
    hdl__khpa = [A, B]
    dmw__kcr = [True] * 2
    gvat__gkk = 'res[i] = (arg0 >> arg1) & 1'
    dob__wtdld = bodo.libs.int_arr_ext.IntegerArrayType(types.uint8)
    return gen_vectorized(xkxej__jgbq, hdl__khpa, dmw__kcr, gvat__gkk,
        dob__wtdld)


@numba.generated_jit(nopython=True)
def haversine_util(lat1, lon1, lat2, lon2):
    verify_int_float_arg(lat1, 'HAVERSINE', 'lat1')
    verify_int_float_arg(lon1, 'HAVERSINE', 'lon1')
    verify_int_float_arg(lat2, 'HAVERSINE', 'lat2')
    verify_int_float_arg(lon2, 'HAVERSINE', 'lon2')
    xkxej__jgbq = ['lat1', 'lon1', 'lat2', 'lon2']
    hdl__khpa = [lat1, lon1, lat2, lon2]
    gbig__xyaa = [True] * 4
    gvat__gkk = (
        'arg0, arg1, arg2, arg3 = map(np.radians, (arg0, arg1, arg2, arg3))\n')
    cqqfu__zuqf = '(arg2 - arg0) * 0.5'
    mez__hnvuq = '(arg3 - arg1) * 0.5'
    kenun__jlc = (
        f'np.square(np.sin({cqqfu__zuqf})) + (np.cos(arg0) * np.cos(arg2) * np.square(np.sin({mez__hnvuq})))'
        )
    gvat__gkk += f'res[i] = 12742.0 * np.arcsin(np.sqrt({kenun__jlc}))\n'
    dob__wtdld = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(xkxej__jgbq, hdl__khpa, gbig__xyaa, gvat__gkk,
        dob__wtdld)


@numba.generated_jit(nopython=True)
def div0_util(arr, divisor):
    verify_int_float_arg(arr, 'DIV0', 'arr')
    verify_int_float_arg(divisor, 'DIV0', 'divisor')
    xkxej__jgbq = ['arr', 'divisor']
    hdl__khpa = [arr, divisor]
    gbig__xyaa = [True] * 2
    gvat__gkk = 'res[i] = arg0 / arg1 if arg1 else 0\n'
    dob__wtdld = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(xkxej__jgbq, hdl__khpa, gbig__xyaa, gvat__gkk,
        dob__wtdld)


@numba.generated_jit(nopython=True)
def log_util(arr, base):
    verify_int_float_arg(arr, 'log', 'arr')
    verify_int_float_arg(base, 'log', 'base')
    xkxej__jgbq = ['arr', 'base']
    hdl__khpa = [arr, base]
    dmw__kcr = [True] * 2
    gvat__gkk = 'res[i] = np.log(arg0) / np.log(arg1)'
    dob__wtdld = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(xkxej__jgbq, hdl__khpa, dmw__kcr, gvat__gkk,
        dob__wtdld)


@numba.generated_jit(nopython=True)
def negate_util(arr):
    xkxej__jgbq = ['arr']
    hdl__khpa = [arr]
    dmw__kcr = [True]
    if bodo.utils.utils.is_array_typ(arr, False):
        mwvn__svd = arr.dtype
    elif bodo.utils.utils.is_array_typ(arr, True):
        mwvn__svd = arr.data.dtype
    else:
        mwvn__svd = arr
    gvat__gkk = {types.uint8: 'res[i] = -np.int16(arg0)', types.uint16:
        'res[i] = -np.int32(arg0)', types.uint32: 'res[i] = -np.int64(arg0)'
        }.get(mwvn__svd, 'res[i] = -arg0')
    mwvn__svd = {types.uint8: types.int16, types.uint16: types.int32, types
        .uint32: types.int64, types.uint64: types.int64}.get(mwvn__svd,
        mwvn__svd)
    if isinstance(mwvn__svd, types.Integer):
        dob__wtdld = bodo.utils.typing.dtype_to_array_type(mwvn__svd)
    else:
        dob__wtdld = arr
    dob__wtdld = bodo.utils.typing.to_nullable_type(dob__wtdld)
    return gen_vectorized(xkxej__jgbq, hdl__khpa, dmw__kcr, gvat__gkk,
        dob__wtdld)


@numba.generated_jit(nopython=True)
def width_bucket_util(arr, min_val, max_val, num_buckets):
    verify_int_float_arg(arr, 'WIDTH_BUCKET', 'arr')
    verify_int_float_arg(min_val, 'WIDTH_BUCKET', 'min_val')
    verify_int_float_arg(max_val, 'WIDTH_BUCKET', 'max_val')
    verify_int_arg(num_buckets, 'WIDTH_BUCKET', 'num_buckets')
    xkxej__jgbq = ['arr', 'min_val', 'max_val', 'num_buckets']
    hdl__khpa = [arr, min_val, max_val, num_buckets]
    dmw__kcr = [True] * 4
    gvat__gkk = (
        "if arg1 >= arg2: raise ValueError('min_val must be less than max_val')\n"
        )
    gvat__gkk += (
        "if arg3 <= 0: raise ValueError('num_buckets must be a positive integer')\n"
        )
    gvat__gkk += (
        'res[i] = min(max(-1.0, math.floor((arg0 - arg1) / ((arg2 - arg1) / arg3))), arg3) + 1.0'
        )
    dob__wtdld = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(xkxej__jgbq, hdl__khpa, dmw__kcr, gvat__gkk,
        dob__wtdld)
