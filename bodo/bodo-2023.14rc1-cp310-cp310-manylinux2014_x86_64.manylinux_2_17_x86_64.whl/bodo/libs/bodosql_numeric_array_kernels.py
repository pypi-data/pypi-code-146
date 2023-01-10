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
    beip__exz = arr0.dtype if is_array_typ(arr0) else arr0
    yziro__svewm = arr1.dtype if is_array_typ(arr1) else arr1
    elgue__pdif = bodo.float64
    if (arr0 is None or beip__exz == bodo.none
        ) or func_name in double_arg_funcs and (arr1 is None or 
        yziro__svewm == bodo.none):
        return types.Array(elgue__pdif, 1, 'C')
    if isinstance(beip__exz, types.Float):
        if isinstance(yziro__svewm, types.Float):
            elgue__pdif = _float[max(beip__exz.bitwidth, yziro__svewm.bitwidth)
                ]
        else:
            elgue__pdif = beip__exz
    if func_name == 'SIGN':
        if isinstance(beip__exz, types.Integer):
            elgue__pdif = beip__exz
    elif func_name == 'MOD':
        if isinstance(beip__exz, types.Integer) and isinstance(yziro__svewm,
            types.Integer):
            if beip__exz.signed:
                if yziro__svewm.signed:
                    elgue__pdif = yziro__svewm
                else:
                    elgue__pdif = _int[min(64, yziro__svewm.bitwidth * 2)]
            else:
                elgue__pdif = yziro__svewm
    elif func_name == 'ABS':
        if isinstance(beip__exz, types.Integer):
            if beip__exz.signed:
                elgue__pdif = _uint[min(64, beip__exz.bitwidth * 2)]
            else:
                elgue__pdif = beip__exz
    elif func_name == 'ROUND':
        if isinstance(beip__exz, (types.Float, types.Integer)):
            elgue__pdif = beip__exz
    elif func_name == 'FACTORIAL':
        elgue__pdif = bodo.int64
    if isinstance(elgue__pdif, types.Integer):
        return bodo.libs.int_arr_ext.IntegerArrayType(elgue__pdif)
    else:
        return types.Array(elgue__pdif, 1, 'C')


def create_numeric_func_overload(func_name):
    if func_name not in double_arg_funcs:
        func_name = func_name.lower()

        def overload_func(arr):
            if isinstance(arr, types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.{func_name}', ['arr'], 0)
            yaagx__rpxd = 'def impl(arr):\n'
            yaagx__rpxd += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr)'
                )
            fpi__sfp = {}
            exec(yaagx__rpxd, {'bodo': bodo}, fpi__sfp)
            return fpi__sfp['impl']
    else:
        func_name = func_name.lower()

        def overload_func(arr0, arr1):
            args = [arr0, arr1]
            for zcz__sqd in range(2):
                if isinstance(args[zcz__sqd], types.optional):
                    return unopt_argument(
                        f'bodo.libs.bodosql_array_kernels.{func_name}', [
                        'arr0', 'arr1'], zcz__sqd)
            yaagx__rpxd = 'def impl(arr0, arr1):\n'
            yaagx__rpxd += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr0, arr1)'
                )
            fpi__sfp = {}
            exec(yaagx__rpxd, {'bodo': bodo}, fpi__sfp)
            return fpi__sfp['impl']
    return overload_func


def create_numeric_util_overload(func_name):
    if func_name not in double_arg_funcs:

        def overload_numeric_util(arr):
            verify_int_float_arg(arr, func_name, 'arr')
            swzwb__jikms = ['arr']
            qpu__njp = [arr]
            rfn__lzzhu = [True]
            glm__lwelb = ''
            if func_name in single_arg_funcs:
                if func_name == 'FACTORIAL':
                    glm__lwelb += (
                        'if arg0 > 20 or np.abs(np.int64(arg0)) != arg0:\n')
                    glm__lwelb += '  bodo.libs.array_kernels.setna(res, i)\n'
                    glm__lwelb += 'else:\n'
                    glm__lwelb += (
                        f'  res[i] = np.math.factorial(np.int64(arg0))')
                elif func_name == 'LN':
                    glm__lwelb += f'res[i] = np.log(arg0)'
                else:
                    glm__lwelb += f'res[i] = np.{func_name.lower()}(arg0)'
            else:
                ValueError(f'Unknown function name: {func_name}')
            elgue__pdif = _get_numeric_output_dtype(func_name, arr)
            return gen_vectorized(swzwb__jikms, qpu__njp, rfn__lzzhu,
                glm__lwelb, elgue__pdif)
    else:

        def overload_numeric_util(arr0, arr1):
            verify_int_float_arg(arr0, func_name, 'arr0')
            verify_int_float_arg(arr0, func_name, 'arr1')
            swzwb__jikms = ['arr0', 'arr1']
            qpu__njp = [arr0, arr1]
            rfn__lzzhu = [True, True]
            elgue__pdif = _get_numeric_output_dtype(func_name, arr0, arr1)
            glm__lwelb = ''
            if func_name == 'MOD':
                glm__lwelb += 'if arg1 == 0:\n'
                glm__lwelb += '  bodo.libs.array_kernels.setna(res, i)\n'
                glm__lwelb += 'else:\n'
                glm__lwelb += (
                    '  res[i] = np.sign(arg0) * np.mod(np.abs(arg0), np.abs(arg1))'
                    )
            elif func_name == 'POWER':
                glm__lwelb += 'res[i] = np.power(np.float64(arg0), arg1)'
            elif func_name == 'ROUND':
                glm__lwelb += 'res[i] = np.round(arg0, arg1)'
            elif func_name == 'TRUNC':
                glm__lwelb += 'if int(arg1) == arg1:\n'
                glm__lwelb += (
                    '  res[i] = np.trunc(arg0 * (10.0 ** arg1)) * (10.0 ** -arg1)\n'
                    )
                glm__lwelb += 'else:\n'
                glm__lwelb += '  bodo.libs.array_kernels.setna(res, i)'
            else:
                raise ValueError(f'Unknown function name: {func_name}')
            return gen_vectorized(swzwb__jikms, qpu__njp, rfn__lzzhu,
                glm__lwelb, elgue__pdif)
    return overload_numeric_util


def _install_numeric_overload(funcs_utils_names):
    for vvghf__creh, bno__kpk, func_name in funcs_utils_names:
        oci__gcy = create_numeric_func_overload(func_name)
        overload(vvghf__creh)(oci__gcy)
        rfhj__gzv = create_numeric_util_overload(func_name)
        overload(bno__kpk)(rfhj__gzv)


_install_numeric_overload(funcs_utils_names)


@numba.generated_jit(nopython=True)
def bitand(A, B):
    args = [A, B]
    for zcz__sqd in range(2):
        if isinstance(args[zcz__sqd], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitand',
                ['A', 'B'], zcz__sqd)

    def impl(A, B):
        return bitand_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftleft(A, B):
    args = [A, B]
    for zcz__sqd in range(2):
        if isinstance(args[zcz__sqd], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftleft', ['A', 'B'],
                zcz__sqd)

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
    for zcz__sqd in range(2):
        if isinstance(args[zcz__sqd], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitor',
                ['A', 'B'], zcz__sqd)

    def impl(A, B):
        return bitor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftright(A, B):
    args = [A, B]
    for zcz__sqd in range(2):
        if isinstance(args[zcz__sqd], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftright', ['A', 'B'],
                zcz__sqd)

    def impl(A, B):
        return bitshiftright_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitxor(A, B):
    args = [A, B]
    for zcz__sqd in range(2):
        if isinstance(args[zcz__sqd], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitxor',
                ['A', 'B'], zcz__sqd)

    def impl(A, B):
        return bitxor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def conv(arr, old_base, new_base):
    args = [arr, old_base, new_base]
    for zcz__sqd in range(3):
        if isinstance(args[zcz__sqd], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.conv', [
                'arr', 'old_base', 'new_base'], zcz__sqd)

    def impl(arr, old_base, new_base):
        return conv_util(arr, old_base, new_base)
    return impl


@numba.generated_jit(nopython=True)
def getbit(A, B):
    args = [A, B]
    for zcz__sqd in range(2):
        if isinstance(args[zcz__sqd], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.getbit',
                ['A', 'B'], zcz__sqd)

    def impl(A, B):
        return getbit_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def haversine(lat1, lon1, lat2, lon2):
    args = [lat1, lon1, lat2, lon2]
    for zcz__sqd in range(4):
        if isinstance(args[zcz__sqd], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.haversine',
                ['lat1', 'lon1', 'lat2', 'lon2'], zcz__sqd)

    def impl(lat1, lon1, lat2, lon2):
        return haversine_util(lat1, lon1, lat2, lon2)
    return impl


@numba.generated_jit(nopython=True)
def div0(arr, divisor):
    args = [arr, divisor]
    for zcz__sqd in range(2):
        if isinstance(args[zcz__sqd], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.div0', [
                'arr', 'divisor'], zcz__sqd)

    def impl(arr, divisor):
        return div0_util(arr, divisor)
    return impl


@numba.generated_jit(nopython=True)
def log(arr, base):
    args = [arr, base]
    for zcz__sqd in range(2):
        if isinstance(args[zcz__sqd], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.log', [
                'arr', 'base'], zcz__sqd)

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
    for zcz__sqd in range(4):
        if isinstance(args[zcz__sqd], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.width_bucket', ['arr',
                'min_val', 'max_val', 'num_buckets'], zcz__sqd)

    def impl(arr, min_val, max_val, num_buckets):
        return width_bucket_util(arr, min_val, max_val, num_buckets)
    return impl


@numba.generated_jit(nopython=True)
def bitand_util(A, B):
    verify_int_arg(A, 'bitand', 'A')
    verify_int_arg(B, 'bitand', 'B')
    swzwb__jikms = ['A', 'B']
    qpu__njp = [A, B]
    rfn__lzzhu = [True] * 2
    glm__lwelb = 'res[i] = arg0 & arg1'
    elgue__pdif = get_common_broadcasted_type([A, B], 'bitand')
    return gen_vectorized(swzwb__jikms, qpu__njp, rfn__lzzhu, glm__lwelb,
        elgue__pdif)


@numba.generated_jit(nopython=True)
def bitshiftleft_util(A, B):
    verify_int_arg(A, 'bitshiftleft', 'A')
    verify_int_arg(B, 'bitshiftleft', 'B')
    swzwb__jikms = ['A', 'B']
    qpu__njp = [A, B]
    rfn__lzzhu = [True] * 2
    glm__lwelb = 'res[i] = arg0 << arg1'
    elgue__pdif = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(swzwb__jikms, qpu__njp, rfn__lzzhu, glm__lwelb,
        elgue__pdif)


@numba.generated_jit(nopython=True)
def bitnot_util(A):
    verify_int_arg(A, 'bitnot', 'A')
    swzwb__jikms = ['A']
    qpu__njp = [A]
    rfn__lzzhu = [True]
    glm__lwelb = 'res[i] = ~arg0'
    if A == bodo.none:
        elgue__pdif = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            pvp__yibl = A.dtype
        else:
            pvp__yibl = A
        elgue__pdif = bodo.libs.int_arr_ext.IntegerArrayType(pvp__yibl)
    return gen_vectorized(swzwb__jikms, qpu__njp, rfn__lzzhu, glm__lwelb,
        elgue__pdif)


@numba.generated_jit(nopython=True)
def bitor_util(A, B):
    verify_int_arg(A, 'bitor', 'A')
    verify_int_arg(B, 'bitor', 'B')
    swzwb__jikms = ['A', 'B']
    qpu__njp = [A, B]
    rfn__lzzhu = [True] * 2
    glm__lwelb = 'res[i] = arg0 | arg1'
    elgue__pdif = get_common_broadcasted_type([A, B], 'bitor')
    return gen_vectorized(swzwb__jikms, qpu__njp, rfn__lzzhu, glm__lwelb,
        elgue__pdif)


@numba.generated_jit(nopython=True)
def bitshiftright_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    swzwb__jikms = ['A', 'B']
    qpu__njp = [A, B]
    rfn__lzzhu = [True] * 2
    if A == bodo.none:
        pvp__yibl = elgue__pdif = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            pvp__yibl = A.dtype
        else:
            pvp__yibl = A
        elgue__pdif = bodo.libs.int_arr_ext.IntegerArrayType(pvp__yibl)
    glm__lwelb = f'res[i] = arg0 >> arg1\n'
    return gen_vectorized(swzwb__jikms, qpu__njp, rfn__lzzhu, glm__lwelb,
        elgue__pdif)


@numba.generated_jit(nopython=True)
def bitxor_util(A, B):
    verify_int_arg(A, 'bitxor', 'A')
    verify_int_arg(B, 'bitxor', 'B')
    swzwb__jikms = ['A', 'B']
    qpu__njp = [A, B]
    rfn__lzzhu = [True] * 2
    glm__lwelb = 'res[i] = arg0 ^ arg1'
    elgue__pdif = get_common_broadcasted_type([A, B], 'bitxor')
    return gen_vectorized(swzwb__jikms, qpu__njp, rfn__lzzhu, glm__lwelb,
        elgue__pdif)


@numba.generated_jit(nopython=True)
def conv_util(arr, old_base, new_base):
    verify_string_arg(arr, 'CONV', 'arr')
    verify_int_arg(old_base, 'CONV', 'old_base')
    verify_int_arg(new_base, 'CONV', 'new_base')
    swzwb__jikms = ['arr', 'old_base', 'new_base']
    qpu__njp = [arr, old_base, new_base]
    rfn__lzzhu = [True] * 3
    glm__lwelb = 'old_val = int(arg0, arg1)\n'
    glm__lwelb += 'if arg2 == 2:\n'
    glm__lwelb += "   res[i] = format(old_val, 'b')\n"
    glm__lwelb += 'elif arg2 == 8:\n'
    glm__lwelb += "   res[i] = format(old_val, 'o')\n"
    glm__lwelb += 'elif arg2 == 10:\n'
    glm__lwelb += "   res[i] = format(old_val, 'd')\n"
    glm__lwelb += 'elif arg2 == 16:\n'
    glm__lwelb += "   res[i] = format(old_val, 'x')\n"
    glm__lwelb += 'else:\n'
    glm__lwelb += '   bodo.libs.array_kernels.setna(res, i)\n'
    elgue__pdif = bodo.string_array_type
    return gen_vectorized(swzwb__jikms, qpu__njp, rfn__lzzhu, glm__lwelb,
        elgue__pdif)


@numba.generated_jit(nopython=True)
def getbit_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    swzwb__jikms = ['A', 'B']
    qpu__njp = [A, B]
    rfn__lzzhu = [True] * 2
    glm__lwelb = 'res[i] = (arg0 >> arg1) & 1'
    elgue__pdif = bodo.libs.int_arr_ext.IntegerArrayType(types.uint8)
    return gen_vectorized(swzwb__jikms, qpu__njp, rfn__lzzhu, glm__lwelb,
        elgue__pdif)


@numba.generated_jit(nopython=True)
def haversine_util(lat1, lon1, lat2, lon2):
    verify_int_float_arg(lat1, 'HAVERSINE', 'lat1')
    verify_int_float_arg(lon1, 'HAVERSINE', 'lon1')
    verify_int_float_arg(lat2, 'HAVERSINE', 'lat2')
    verify_int_float_arg(lon2, 'HAVERSINE', 'lon2')
    swzwb__jikms = ['lat1', 'lon1', 'lat2', 'lon2']
    qpu__njp = [lat1, lon1, lat2, lon2]
    mpcwe__ccxt = [True] * 4
    glm__lwelb = (
        'arg0, arg1, arg2, arg3 = map(np.radians, (arg0, arg1, arg2, arg3))\n')
    mjtwe__dqrc = '(arg2 - arg0) * 0.5'
    ltvkx__xkpsp = '(arg3 - arg1) * 0.5'
    ycg__czb = (
        f'np.square(np.sin({mjtwe__dqrc})) + (np.cos(arg0) * np.cos(arg2) * np.square(np.sin({ltvkx__xkpsp})))'
        )
    glm__lwelb += f'res[i] = 12742.0 * np.arcsin(np.sqrt({ycg__czb}))\n'
    elgue__pdif = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(swzwb__jikms, qpu__njp, mpcwe__ccxt, glm__lwelb,
        elgue__pdif)


@numba.generated_jit(nopython=True)
def div0_util(arr, divisor):
    verify_int_float_arg(arr, 'DIV0', 'arr')
    verify_int_float_arg(divisor, 'DIV0', 'divisor')
    swzwb__jikms = ['arr', 'divisor']
    qpu__njp = [arr, divisor]
    mpcwe__ccxt = [True] * 2
    glm__lwelb = 'res[i] = arg0 / arg1 if arg1 else 0\n'
    elgue__pdif = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(swzwb__jikms, qpu__njp, mpcwe__ccxt, glm__lwelb,
        elgue__pdif)


@numba.generated_jit(nopython=True)
def log_util(arr, base):
    verify_int_float_arg(arr, 'log', 'arr')
    verify_int_float_arg(base, 'log', 'base')
    swzwb__jikms = ['arr', 'base']
    qpu__njp = [arr, base]
    rfn__lzzhu = [True] * 2
    glm__lwelb = 'res[i] = np.log(arg0) / np.log(arg1)'
    elgue__pdif = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(swzwb__jikms, qpu__njp, rfn__lzzhu, glm__lwelb,
        elgue__pdif)


@numba.generated_jit(nopython=True)
def negate_util(arr):
    swzwb__jikms = ['arr']
    qpu__njp = [arr]
    rfn__lzzhu = [True]
    if bodo.utils.utils.is_array_typ(arr, False):
        pvp__yibl = arr.dtype
    elif bodo.utils.utils.is_array_typ(arr, True):
        pvp__yibl = arr.data.dtype
    else:
        pvp__yibl = arr
    glm__lwelb = {types.uint8: 'res[i] = -np.int16(arg0)', types.uint16:
        'res[i] = -np.int32(arg0)', types.uint32: 'res[i] = -np.int64(arg0)'
        }.get(pvp__yibl, 'res[i] = -arg0')
    pvp__yibl = {types.uint8: types.int16, types.uint16: types.int32, types
        .uint32: types.int64, types.uint64: types.int64}.get(pvp__yibl,
        pvp__yibl)
    if isinstance(pvp__yibl, types.Integer):
        elgue__pdif = bodo.utils.typing.dtype_to_array_type(pvp__yibl)
    else:
        elgue__pdif = arr
    elgue__pdif = bodo.utils.typing.to_nullable_type(elgue__pdif)
    return gen_vectorized(swzwb__jikms, qpu__njp, rfn__lzzhu, glm__lwelb,
        elgue__pdif)


@numba.generated_jit(nopython=True)
def width_bucket_util(arr, min_val, max_val, num_buckets):
    verify_int_float_arg(arr, 'WIDTH_BUCKET', 'arr')
    verify_int_float_arg(min_val, 'WIDTH_BUCKET', 'min_val')
    verify_int_float_arg(max_val, 'WIDTH_BUCKET', 'max_val')
    verify_int_arg(num_buckets, 'WIDTH_BUCKET', 'num_buckets')
    swzwb__jikms = ['arr', 'min_val', 'max_val', 'num_buckets']
    qpu__njp = [arr, min_val, max_val, num_buckets]
    rfn__lzzhu = [True] * 4
    glm__lwelb = (
        "if arg1 >= arg2: raise ValueError('min_val must be less than max_val')\n"
        )
    glm__lwelb += (
        "if arg3 <= 0: raise ValueError('num_buckets must be a positive integer')\n"
        )
    glm__lwelb += (
        'res[i] = min(max(-1.0, math.floor((arg0 - arg1) / ((arg2 - arg1) / arg3))), arg3) + 1.0'
        )
    elgue__pdif = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(swzwb__jikms, qpu__njp, rfn__lzzhu, glm__lwelb,
        elgue__pdif)
