"""Nullable integer array corresponding to Pandas IntegerArray.
However, nulls are stored in bit arrays similar to Arrow's arrays.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs.str_arr_ext import kBitmask
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('mask_arr_to_bitmap', hstr_ext.mask_arr_to_bitmap)
ll.add_symbol('is_pd_int_array', array_ext.is_pd_int_array)
ll.add_symbol('int_array_from_sequence', array_ext.int_array_from_sequence)
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, check_unsupported_args, is_iterable_type, is_list_like_index_type, is_overload_false, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error, to_nullable_type


class IntegerArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(IntegerArrayType, self).__init__(name=
            f'IntegerArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntegerArrayType(self.dtype)

    @property
    def get_pandas_scalar_type_instance(self):
        zhway__ujgig = int(np.log2(self.dtype.bitwidth // 8))
        gsaw__zcvc = 0 if self.dtype.signed else 4
        idx = zhway__ujgig + gsaw__zcvc
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        odn__qccdd = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, odn__qccdd)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    dpp__gfp = 8 * val.dtype.itemsize
    wxe__use = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(wxe__use, dpp__gfp))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        nta__awg = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(nta__awg)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    pwn__fot = c.context.insert_const_string(c.builder.module, 'pandas')
    tzab__oil = c.pyapi.import_module_noblock(pwn__fot)
    rizeb__htnzh = c.pyapi.call_method(tzab__oil, str(typ)[:-2], ())
    c.pyapi.decref(tzab__oil)
    return rizeb__htnzh


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    dpp__gfp = 8 * val.itemsize
    wxe__use = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(wxe__use, dpp__gfp))
    return IntDtype(dtype)


def _register_int_dtype(t):
    typeof_impl.register(t)(typeof_pd_int_dtype)
    int_dtype = typeof_pd_int_dtype(t(), None)
    type_callable(t)(lambda c: lambda : int_dtype)
    lower_builtin(t)(lambda c, b, s, a: c.get_dummy_value())


pd_int_dtype_classes = (pd.Int8Dtype, pd.Int16Dtype, pd.Int32Dtype, pd.
    Int64Dtype, pd.UInt8Dtype, pd.UInt16Dtype, pd.UInt32Dtype, pd.UInt64Dtype)
for t in pd_int_dtype_classes:
    _register_int_dtype(t)


@numba.extending.register_jitable
def mask_arr_to_bitmap(mask_arr):
    n = len(mask_arr)
    tdxzh__oni = n + 7 >> 3
    hnj__vpp = np.empty(tdxzh__oni, np.uint8)
    for i in range(n):
        ptlnb__apk = i // 8
        hnj__vpp[ptlnb__apk] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            hnj__vpp[ptlnb__apk]) & kBitmask[i % 8]
    return hnj__vpp


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    ofuc__xvg = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(ofuc__xvg)
    c.pyapi.decref(ofuc__xvg)
    yrzg__uqat = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    tdxzh__oni = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    ylqct__behb = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [tdxzh__oni])
    ulufk__lik = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    pwflm__smkdu = cgutils.get_or_insert_function(c.builder.module,
        ulufk__lik, name='is_pd_int_array')
    bue__daxye = c.builder.call(pwflm__smkdu, [obj])
    qgxeb__wme = c.builder.icmp_unsigned('!=', bue__daxye, bue__daxye.type(0))
    with c.builder.if_else(qgxeb__wme) as (qkzj__yov, yzl__jeo):
        with qkzj__yov:
            jfxw__tui = c.pyapi.object_getattr_string(obj, '_data')
            yrzg__uqat.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), jfxw__tui).value
            unb__odlkk = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), unb__odlkk).value
            c.pyapi.decref(jfxw__tui)
            c.pyapi.decref(unb__odlkk)
            ykpia__ryywr = c.context.make_array(types.Array(types.bool_, 1,
                'C'))(c.context, c.builder, mask_arr)
            ulufk__lik = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            pwflm__smkdu = cgutils.get_or_insert_function(c.builder.module,
                ulufk__lik, name='mask_arr_to_bitmap')
            c.builder.call(pwflm__smkdu, [ylqct__behb.data, ykpia__ryywr.
                data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with yzl__jeo:
            gdzip__wxspq = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            ulufk__lik = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            bmwbz__nss = cgutils.get_or_insert_function(c.builder.module,
                ulufk__lik, name='int_array_from_sequence')
            c.builder.call(bmwbz__nss, [obj, c.builder.bitcast(gdzip__wxspq
                .data, lir.IntType(8).as_pointer()), ylqct__behb.data])
            yrzg__uqat.data = gdzip__wxspq._getvalue()
    yrzg__uqat.null_bitmap = ylqct__behb._getvalue()
    pix__pbx = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(yrzg__uqat._getvalue(), is_error=pix__pbx)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    yrzg__uqat = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        yrzg__uqat.data, c.env_manager)
    yofnp__rybe = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, yrzg__uqat.null_bitmap).data
    ofuc__xvg = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(ofuc__xvg)
    pwn__fot = c.context.insert_const_string(c.builder.module, 'numpy')
    sgt__mhcc = c.pyapi.import_module_noblock(pwn__fot)
    itya__xin = c.pyapi.object_getattr_string(sgt__mhcc, 'bool_')
    mask_arr = c.pyapi.call_method(sgt__mhcc, 'empty', (ofuc__xvg, itya__xin))
    scmgq__iumw = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    ifzzk__eqwgs = c.pyapi.object_getattr_string(scmgq__iumw, 'data')
    qotkd__wvn = c.builder.inttoptr(c.pyapi.long_as_longlong(ifzzk__eqwgs),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as fdf__wcj:
        i = fdf__wcj.index
        rgx__mwo = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        erlrn__lzk = c.builder.load(cgutils.gep(c.builder, yofnp__rybe,
            rgx__mwo))
        razla__vdbr = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(erlrn__lzk, razla__vdbr), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        jods__ggfbv = cgutils.gep(c.builder, qotkd__wvn, i)
        c.builder.store(val, jods__ggfbv)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        yrzg__uqat.null_bitmap)
    pwn__fot = c.context.insert_const_string(c.builder.module, 'pandas')
    tzab__oil = c.pyapi.import_module_noblock(pwn__fot)
    nbo__tmmz = c.pyapi.object_getattr_string(tzab__oil, 'arrays')
    rizeb__htnzh = c.pyapi.call_method(nbo__tmmz, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(tzab__oil)
    c.pyapi.decref(ofuc__xvg)
    c.pyapi.decref(sgt__mhcc)
    c.pyapi.decref(itya__xin)
    c.pyapi.decref(scmgq__iumw)
    c.pyapi.decref(ifzzk__eqwgs)
    c.pyapi.decref(nbo__tmmz)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return rizeb__htnzh


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        iin__xdynx, ajjo__vub = args
        yrzg__uqat = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        yrzg__uqat.data = iin__xdynx
        yrzg__uqat.null_bitmap = ajjo__vub
        context.nrt.incref(builder, signature.args[0], iin__xdynx)
        context.nrt.incref(builder, signature.args[1], ajjo__vub)
        return yrzg__uqat._getvalue()
    xfs__rdku = IntegerArrayType(data.dtype)
    fvb__uiwgn = xfs__rdku(data, null_bitmap)
    return fvb__uiwgn, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    mtot__lzva = np.empty(n, pyval.dtype.type)
    frnqj__hxfo = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        vfpmv__uhh = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(frnqj__hxfo, i, int(not
            vfpmv__uhh))
        if not vfpmv__uhh:
            mtot__lzva[i] = s
    afq__sruka = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), mtot__lzva)
    iwza__yuo = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), frnqj__hxfo)
    return lir.Constant.literal_struct([afq__sruka, iwza__yuo])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    abje__hfxp = args[0]
    if equiv_set.has_shape(abje__hfxp):
        return ArrayAnalysis.AnalyzeResult(shape=abje__hfxp, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    abje__hfxp = args[0]
    if equiv_set.has_shape(abje__hfxp):
        return ArrayAnalysis.AnalyzeResult(shape=abje__hfxp, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_init_integer_array = (
    init_integer_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_integer_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_integer_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_integer_array
numba.core.ir_utils.alias_func_extensions['get_int_arr_data',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_int_arr_bitmap',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_int_array(n, dtype):
    mtot__lzva = np.empty(n, dtype)
    ccpf__huth = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(mtot__lzva, ccpf__huth)


def alloc_int_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_alloc_int_array = (
    alloc_int_array_equiv)


@numba.extending.register_jitable
def set_bit_to_arr(bits, i, bit_is_set):
    bits[i // 8] ^= np.uint8(-np.uint8(bit_is_set) ^ bits[i // 8]) & kBitmask[
        i % 8]


@numba.extending.register_jitable
def get_bit_bitmap_arr(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@overload(operator.getitem, no_unliteral=True)
def int_arr_getitem(A, ind):
    if not isinstance(A, IntegerArrayType):
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            ypcg__qsu, qgx__wwmkh = array_getitem_bool_index(A, ind)
            return init_integer_array(ypcg__qsu, qgx__wwmkh)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ypcg__qsu, qgx__wwmkh = array_getitem_int_index(A, ind)
            return init_integer_array(ypcg__qsu, qgx__wwmkh)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            ypcg__qsu, qgx__wwmkh = array_getitem_slice_index(A, ind)
            return init_integer_array(ypcg__qsu, qgx__wwmkh)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for IntegerArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    soum__idrd = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    ibtkl__aqef = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if ibtkl__aqef:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(soum__idrd)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or ibtkl__aqef):
        raise BodoError(soum__idrd)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):

        def impl_arr_ind_mask(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind_mask
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for IntegerArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_int_arr_len(A):
    if isinstance(A, IntegerArrayType):
        return lambda A: len(A._data)


@overload_attribute(IntegerArrayType, 'shape')
def overload_int_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(IntegerArrayType, 'dtype')
def overload_int_arr_dtype(A):
    dtype_class = getattr(pd, '{}Int{}Dtype'.format('' if A.dtype.signed else
        'U', A.dtype.bitwidth))
    return lambda A: dtype_class()


@overload_attribute(IntegerArrayType, 'ndim')
def overload_int_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntegerArrayType, 'nbytes')
def int_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(IntegerArrayType, 'copy', no_unliteral=True)
def overload_int_arr_copy(A, dtype=None):
    if not is_overload_none(dtype):
        return lambda A, dtype=None: A.astype(dtype, copy=True)
    else:
        return lambda A, dtype=None: bodo.libs.int_arr_ext.init_integer_array(
            bodo.libs.int_arr_ext.get_int_arr_data(A).copy(), bodo.libs.
            int_arr_ext.get_int_arr_bitmap(A).copy())


@overload_method(IntegerArrayType, 'astype', no_unliteral=True)
def overload_int_arr_astype(A, dtype, copy=True):
    if isinstance(dtype, types.TypeRef):
        dtype = dtype.instance_type
    if dtype == types.unicode_type:
        raise_bodo_error(
            "IntegerArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.NumberClass):
        dtype = dtype.dtype
    if isinstance(dtype, IntDtype) and A.dtype == dtype.dtype:
        if is_overload_false(copy):
            return lambda A, dtype, copy=True: A
        elif is_overload_true(copy):
            return lambda A, dtype, copy=True: A.copy()
        else:

            def impl(A, dtype, copy=True):
                if copy:
                    return A.copy()
                else:
                    return A
            return impl
    if isinstance(dtype, IntDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.int_arr_ext.
            init_integer_array(bodo.libs.int_arr_ext.get_int_arr_data(A).
            astype(np_dtype), bodo.libs.int_arr_ext.get_int_arr_bitmap(A).
            copy()))
    nb_dtype = parse_dtype(dtype, 'IntegerArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.int_arr_ext.get_int_arr_data(A)
            n = len(data)
            eqcg__gimxg = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                eqcg__gimxg[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    eqcg__gimxg[i] = np.nan
            return eqcg__gimxg
        return impl_float
    return lambda A, dtype, copy=True: bodo.libs.int_arr_ext.get_int_arr_data(A
        ).astype(nb_dtype)


ufunc_aliases = {'subtract': 'sub', 'multiply': 'mul', 'floor_divide':
    'floordiv', 'true_divide': 'truediv', 'power': 'pow', 'remainder':
    'mod', 'divide': 'div', 'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    if n_inputs == 1:

        def overload_int_arr_op_nin_1(A):
            if isinstance(A, IntegerArrayType):
                return get_nullable_array_unary_impl(op, A)
        return overload_int_arr_op_nin_1
    elif n_inputs == 2:

        def overload_series_op_nin_2(lhs, rhs):
            if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
                IntegerArrayType):
                return get_nullable_array_binary_impl(op, lhs, rhs)
        return overload_series_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for mxvp__uii in numba.np.ufunc_db.get_ufuncs():
        rcjdu__tyevw = create_op_overload(mxvp__uii, mxvp__uii.nin)
        overload(mxvp__uii, no_unliteral=True)(rcjdu__tyevw)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        rcjdu__tyevw = create_op_overload(op, 2)
        overload(op)(rcjdu__tyevw)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        rcjdu__tyevw = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(rcjdu__tyevw)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        rcjdu__tyevw = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(rcjdu__tyevw)


_install_unary_ops()


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    yuz__yivn = dict(skipna=skipna, min_count=min_count)
    huin__vgje = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', yuz__yivn, huin__vgje)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0
        for i in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, i):
                val = A[i]
            s += val
        return s
    return impl


@overload_method(IntegerArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_int_arr(A):
        data = []
        razla__vdbr = []
        ksmer__vgnx = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not ksmer__vgnx:
                    data.append(dtype(1))
                    razla__vdbr.append(False)
                    ksmer__vgnx = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                razla__vdbr.append(True)
        ypcg__qsu = np.array(data)
        n = len(ypcg__qsu)
        tdxzh__oni = n + 7 >> 3
        qgx__wwmkh = np.empty(tdxzh__oni, np.uint8)
        for rwwmk__mjb in range(n):
            set_bit_to_arr(qgx__wwmkh, rwwmk__mjb, razla__vdbr[rwwmk__mjb])
        return init_integer_array(ypcg__qsu, qgx__wwmkh)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    lhgz__gkqqs = numba.core.registry.cpu_target.typing_context
    vnfq__gsbc = lhgz__gkqqs.resolve_function_type(op, (types.Array(A.dtype,
        1, 'C'),), {}).return_type
    vnfq__gsbc = to_nullable_type(vnfq__gsbc)

    def impl(A):
        n = len(A)
        bqm__jon = bodo.utils.utils.alloc_type(n, vnfq__gsbc, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(bqm__jon, i)
                continue
            bqm__jon[i] = op(A[i])
        return bqm__jon
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    cykh__blp = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    ebj__fvbek = isinstance(lhs, (types.Number, types.Boolean))
    azfam__gnbm = isinstance(rhs, (types.Number, types.Boolean))
    vtb__sdnw = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    kgzl__orq = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    lhgz__gkqqs = numba.core.registry.cpu_target.typing_context
    vnfq__gsbc = lhgz__gkqqs.resolve_function_type(op, (vtb__sdnw,
        kgzl__orq), {}).return_type
    vnfq__gsbc = to_nullable_type(vnfq__gsbc)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    zbd__kags = 'lhs' if ebj__fvbek else 'lhs[i]'
    vow__crzhu = 'rhs' if azfam__gnbm else 'rhs[i]'
    upfgu__ngyvz = ('False' if ebj__fvbek else
        'bodo.libs.array_kernels.isna(lhs, i)')
    eruxr__nujmq = ('False' if azfam__gnbm else
        'bodo.libs.array_kernels.isna(rhs, i)')
    eds__hwrfq = 'def impl(lhs, rhs):\n'
    eds__hwrfq += '  n = len({})\n'.format('lhs' if not ebj__fvbek else 'rhs')
    if cykh__blp:
        eds__hwrfq += '  out_arr = {}\n'.format('lhs' if not ebj__fvbek else
            'rhs')
    else:
        eds__hwrfq += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    eds__hwrfq += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    eds__hwrfq += '    if ({}\n'.format(upfgu__ngyvz)
    eds__hwrfq += '        or {}):\n'.format(eruxr__nujmq)
    eds__hwrfq += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    eds__hwrfq += '      continue\n'
    eds__hwrfq += (
        """    out_arr[i] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(op({}, {}))
"""
        .format(zbd__kags, vow__crzhu))
    eds__hwrfq += '  return out_arr\n'
    cdanm__zfczv = {}
    exec(eds__hwrfq, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        vnfq__gsbc, 'op': op}, cdanm__zfczv)
    impl = cdanm__zfczv['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        ebj__fvbek = lhs in [pd_timedelta_type]
        azfam__gnbm = rhs in [pd_timedelta_type]
        if ebj__fvbek:

            def impl(lhs, rhs):
                n = len(rhs)
                bqm__jon = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(bqm__jon, i)
                        continue
                    bqm__jon[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs, rhs[i]))
                return bqm__jon
            return impl
        elif azfam__gnbm:

            def impl(lhs, rhs):
                n = len(lhs)
                bqm__jon = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(bqm__jon, i)
                        continue
                    bqm__jon[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs[i], rhs))
                return bqm__jon
            return impl
    return impl
