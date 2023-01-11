"""Nullable float array corresponding to Pandas FloatingArray.
However, nulls are stored in bit arrays similar to Arrow's arrays.
"""
import operator
import os
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
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('is_pd_float_array', array_ext.is_pd_float_array)
ll.add_symbol('float_array_from_sequence', array_ext.float_array_from_sequence)
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, check_unsupported_args, is_iterable_type, is_list_like_index_type, is_overload_false, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error
_use_nullable_float = int(os.environ.get('BODO_USE_NULLABLE_FLOAT', '0'))


class FloatingArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(FloatingArrayType, self).__init__(name=
            f'FloatingArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return FloatingArrayType(self.dtype)

    @property
    def get_pandas_scalar_type_instance(self):
        return pd.Float64Dtype(
            ) if self.dtype == types.float64 else pd.Float32Dtype()


@register_model(FloatingArrayType)
class FloatingArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lmc__tdliy = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, lmc__tdliy)


make_attribute_wrapper(FloatingArrayType, 'data', '_data')
make_attribute_wrapper(FloatingArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.FloatingArray)
def _typeof_pd_float_array(val, c):
    dtype = types.float32 if val.dtype == pd.Float32Dtype() else types.float64
    return FloatingArrayType(dtype)


class FloatDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Float)
        self.dtype = dtype
        uwoyp__olqs = f'Float{dtype.bitwidth}Dtype()'
        super(FloatDtype, self).__init__(uwoyp__olqs)


register_model(FloatDtype)(models.OpaqueModel)


@box(FloatDtype)
def box_floatdtype(typ, val, c):
    seuw__yiig = c.context.insert_const_string(c.builder.module, 'pandas')
    uixvw__gjj = c.pyapi.import_module_noblock(seuw__yiig)
    ruyi__ezw = c.pyapi.call_method(uixvw__gjj, str(typ)[:-2], ())
    c.pyapi.decref(uixvw__gjj)
    return ruyi__ezw


@unbox(FloatDtype)
def unbox_floatdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_float_dtype(val, c):
    dtype = types.float32 if val == pd.Float32Dtype() else types.float64
    return FloatDtype(dtype)


def _register_float_dtype(t):
    typeof_impl.register(t)(typeof_pd_float_dtype)
    float_dtype = typeof_pd_float_dtype(t(), None)
    type_callable(t)(lambda c: lambda : float_dtype)
    lower_builtin(t)(lambda c, b, s, a: c.get_dummy_value())


_register_float_dtype(pd.Float32Dtype)
_register_float_dtype(pd.Float64Dtype)


@unbox(FloatingArrayType)
def unbox_float_array(typ, obj, c):
    maaa__udvi = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(maaa__udvi)
    c.pyapi.decref(maaa__udvi)
    pacst__wtsqd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    sio__ilyrv = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    dsfct__kznq = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [sio__ilyrv])
    nnw__wcx = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()])
    rsuh__zjlt = cgutils.get_or_insert_function(c.builder.module, nnw__wcx,
        name='is_pd_float_array')
    wwiy__scra = c.builder.call(rsuh__zjlt, [obj])
    anhdw__dju = c.builder.icmp_unsigned('!=', wwiy__scra, wwiy__scra.type(0))
    with c.builder.if_else(anhdw__dju) as (xoco__cxnq, arz__uym):
        with xoco__cxnq:
            uspn__hoc = c.pyapi.object_getattr_string(obj, '_data')
            pacst__wtsqd.data = c.pyapi.to_native_value(types.Array(typ.
                dtype, 1, 'C'), uspn__hoc).value
            pqsg__okqfx = c.pyapi.object_getattr_string(obj, '_mask')
            atb__bim = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), pqsg__okqfx).value
            c.pyapi.decref(uspn__hoc)
            c.pyapi.decref(pqsg__okqfx)
            rvdxw__szvf = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, atb__bim)
            nnw__wcx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            rsuh__zjlt = cgutils.get_or_insert_function(c.builder.module,
                nnw__wcx, name='mask_arr_to_bitmap')
            c.builder.call(rsuh__zjlt, [dsfct__kznq.data, rvdxw__szvf.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), atb__bim)
        with arz__uym:
            lqq__paoic = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            nnw__wcx = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            mrap__qss = cgutils.get_or_insert_function(c.builder.module,
                nnw__wcx, name='float_array_from_sequence')
            c.builder.call(mrap__qss, [obj, c.builder.bitcast(lqq__paoic.
                data, lir.IntType(8).as_pointer()), dsfct__kznq.data])
            pacst__wtsqd.data = lqq__paoic._getvalue()
    pacst__wtsqd.null_bitmap = dsfct__kznq._getvalue()
    ztvkm__jenvo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(pacst__wtsqd._getvalue(), is_error=ztvkm__jenvo)


@box(FloatingArrayType)
def box_float_array(typ, val, c):
    pacst__wtsqd = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        pacst__wtsqd.data, c.env_manager)
    whld__xufj = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, pacst__wtsqd.null_bitmap).data
    maaa__udvi = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(maaa__udvi)
    seuw__yiig = c.context.insert_const_string(c.builder.module, 'numpy')
    mss__huv = c.pyapi.import_module_noblock(seuw__yiig)
    vrbup__izid = c.pyapi.object_getattr_string(mss__huv, 'bool_')
    atb__bim = c.pyapi.call_method(mss__huv, 'empty', (maaa__udvi, vrbup__izid)
        )
    xxzb__uox = c.pyapi.object_getattr_string(atb__bim, 'ctypes')
    bjpn__zzvx = c.pyapi.object_getattr_string(xxzb__uox, 'data')
    udue__bfc = c.builder.inttoptr(c.pyapi.long_as_longlong(bjpn__zzvx),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as wvu__aexoa:
        vtupn__qgqzd = wvu__aexoa.index
        gsp__ulfxn = c.builder.lshr(vtupn__qgqzd, lir.Constant(lir.IntType(
            64), 3))
        sljzf__jvt = c.builder.load(cgutils.gep(c.builder, whld__xufj,
            gsp__ulfxn))
        way__rdikj = c.builder.trunc(c.builder.and_(vtupn__qgqzd, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(sljzf__jvt, way__rdikj), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        eyh__ytm = cgutils.gep(c.builder, udue__bfc, vtupn__qgqzd)
        c.builder.store(val, eyh__ytm)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        pacst__wtsqd.null_bitmap)
    seuw__yiig = c.context.insert_const_string(c.builder.module, 'pandas')
    uixvw__gjj = c.pyapi.import_module_noblock(seuw__yiig)
    kdv__wlquf = c.pyapi.object_getattr_string(uixvw__gjj, 'arrays')
    ruyi__ezw = c.pyapi.call_method(kdv__wlquf, 'FloatingArray', (data,
        atb__bim))
    c.pyapi.decref(uixvw__gjj)
    c.pyapi.decref(maaa__udvi)
    c.pyapi.decref(mss__huv)
    c.pyapi.decref(vrbup__izid)
    c.pyapi.decref(xxzb__uox)
    c.pyapi.decref(bjpn__zzvx)
    c.pyapi.decref(kdv__wlquf)
    c.pyapi.decref(data)
    c.pyapi.decref(atb__bim)
    return ruyi__ezw


@intrinsic
def init_float_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        bucn__sfna, qkkc__ldat = args
        pacst__wtsqd = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        pacst__wtsqd.data = bucn__sfna
        pacst__wtsqd.null_bitmap = qkkc__ldat
        context.nrt.incref(builder, signature.args[0], bucn__sfna)
        context.nrt.incref(builder, signature.args[1], qkkc__ldat)
        return pacst__wtsqd._getvalue()
    flwkr__tnk = FloatingArrayType(data.dtype)
    btaxr__bdmbt = flwkr__tnk(data, null_bitmap)
    return btaxr__bdmbt, codegen


@lower_constant(FloatingArrayType)
def lower_constant_float_arr(context, builder, typ, pyval):
    n = len(pyval)
    oskto__glitd = np.empty(n, pyval.dtype.type)
    ucs__sbo = np.empty(n + 7 >> 3, np.uint8)
    for vtupn__qgqzd, s in enumerate(pyval):
        xol__tmuy = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ucs__sbo, vtupn__qgqzd, int(
            not xol__tmuy))
        if not xol__tmuy:
            oskto__glitd[vtupn__qgqzd] = s
    lvtn__bnrww = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), oskto__glitd)
    bvkv__zljcu = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), ucs__sbo)
    return lir.Constant.literal_struct([lvtn__bnrww, bvkv__zljcu])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_float_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    tguo__ujwwt = args[0]
    if equiv_set.has_shape(tguo__ujwwt):
        return ArrayAnalysis.AnalyzeResult(shape=tguo__ujwwt, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_float_arr_ext_get_float_arr_data
    ) = get_float_arr_data_equiv


def init_float_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    tguo__ujwwt = args[0]
    if equiv_set.has_shape(tguo__ujwwt):
        return ArrayAnalysis.AnalyzeResult(shape=tguo__ujwwt, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_float_arr_ext_init_float_array = (
    init_float_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_float_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_float_array',
    'bodo.libs.float_arr_ext'] = alias_ext_init_float_array
numba.core.ir_utils.alias_func_extensions['get_float_arr_data',
    'bodo.libs.float_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_float_arr_bitmap',
    'bodo.libs.float_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_float_array(n, dtype):
    oskto__glitd = np.empty(n, dtype)
    htz__ktl = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_float_array(oskto__glitd, htz__ktl)


def alloc_float_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_float_arr_ext_alloc_float_array
    ) = alloc_float_array_equiv


@overload(operator.getitem, no_unliteral=True)
def float_arr_getitem(A, ind):
    if not isinstance(A, FloatingArrayType):
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            uyzsl__jcrio, bzbub__oaxjr = array_getitem_bool_index(A, ind)
            return init_float_array(uyzsl__jcrio, bzbub__oaxjr)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            uyzsl__jcrio, bzbub__oaxjr = array_getitem_int_index(A, ind)
            return init_float_array(uyzsl__jcrio, bzbub__oaxjr)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            uyzsl__jcrio, bzbub__oaxjr = array_getitem_slice_index(A, ind)
            return init_float_array(uyzsl__jcrio, bzbub__oaxjr)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for IntegerArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def float_arr_setitem(A, idx, val):
    if not isinstance(A, FloatingArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    cevlz__rtyfw = (
        f"setitem for FloatingArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    dfh__mlp = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if dfh__mlp:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(cevlz__rtyfw)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean, types.Float)) or dfh__mlp):
        raise BodoError(cevlz__rtyfw)
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
        f'setitem for FloatingArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_float_arr_len(A):
    if isinstance(A, FloatingArrayType):
        return lambda A: len(A._data)


@overload_attribute(FloatingArrayType, 'shape')
def overload_float_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(FloatingArrayType, 'dtype')
def overload_float_arr_dtype(A):
    dtype_class = (pd.Float32Dtype if A.dtype == types.float32 else pd.
        Float64Dtype)
    return lambda A: dtype_class()


@overload_attribute(FloatingArrayType, 'ndim')
def overload_float_arr_ndim(A):
    return lambda A: 1


@overload_attribute(FloatingArrayType, 'size')
def overload_float_size(A):
    return lambda A: len(A._data)


@overload_attribute(FloatingArrayType, 'nbytes')
def float_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(FloatingArrayType, 'copy', no_unliteral=True)
def overload_float_arr_copy(A, dtype=None):
    if not is_overload_none(dtype):
        return lambda A, dtype=None: A.astype(dtype, copy=True)
    else:
        return lambda A, dtype=None: bodo.libs.float_arr_ext.init_float_array(
            bodo.libs.float_arr_ext.get_float_arr_data(A).copy(), bodo.libs
            .float_arr_ext.get_float_arr_bitmap(A).copy())


@overload_method(FloatingArrayType, 'astype', no_unliteral=True)
def overload_float_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "FloatingArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.NumberClass):
        dtype = dtype.dtype
    if isinstance(dtype, FloatDtype) and A.dtype == dtype.dtype:
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
    if isinstance(dtype, FloatDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.float_arr_ext.
            init_float_array(bodo.libs.float_arr_ext.get_float_arr_data(A).
            astype(np_dtype), bodo.libs.float_arr_ext.get_float_arr_bitmap(
            A).copy()))
    if isinstance(dtype, bodo.libs.int_arr_ext.IntDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.int_arr_ext.
            init_integer_array(bodo.libs.float_arr_ext.get_float_arr_data(A
            ).astype(np_dtype), bodo.libs.float_arr_ext.
            get_float_arr_bitmap(A).copy()))
    nb_dtype = parse_dtype(dtype, 'FloatingArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.float_arr_ext.get_float_arr_data(A)
            n = len(data)
            qnaxf__bkyh = np.empty(n, nb_dtype)
            for vtupn__qgqzd in numba.parfors.parfor.internal_prange(n):
                qnaxf__bkyh[vtupn__qgqzd] = data[vtupn__qgqzd]
                if bodo.libs.array_kernels.isna(A, vtupn__qgqzd):
                    qnaxf__bkyh[vtupn__qgqzd] = np.nan
            return qnaxf__bkyh
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.float_arr_ext.
        get_float_arr_data(A).astype(nb_dtype))


ufunc_aliases = {'subtract': 'sub', 'multiply': 'mul', 'floor_divide':
    'floordiv', 'true_divide': 'truediv', 'power': 'pow', 'remainder':
    'mod', 'divide': 'div', 'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    if n_inputs == 1:

        def overload_float_arr_op_nin_1(A):
            if isinstance(A, FloatingArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_unary_impl(op,
                    A)
        return overload_float_arr_op_nin_1
    elif n_inputs == 2:

        def overload_series_op_nin_2(lhs, rhs):
            if isinstance(lhs, FloatingArrayType) or isinstance(rhs,
                FloatingArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_binary_impl(op,
                    lhs, rhs)
        return overload_series_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for lox__zlp in numba.np.ufunc_db.get_ufuncs():
        qlsfo__udk = create_op_overload(lox__zlp, lox__zlp.nin)
        overload(lox__zlp, no_unliteral=True)(qlsfo__udk)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        qlsfo__udk = create_op_overload(op, 2)
        overload(op)(qlsfo__udk)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        qlsfo__udk = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(qlsfo__udk)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        qlsfo__udk = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(qlsfo__udk)


_install_unary_ops()


@overload_method(FloatingArrayType, 'sum', no_unliteral=True)
def overload_float_arr_sum(A, skipna=True, min_count=0):
    qluc__fkl = dict(skipna=skipna, min_count=min_count)
    tvvw__mawtl = dict(skipna=True, min_count=0)
    check_unsupported_args('FloatingArray.sum', qluc__fkl, tvvw__mawtl)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0.0
        for vtupn__qgqzd in numba.parfors.parfor.internal_prange(len(A)):
            val = 0.0
            if not bodo.libs.array_kernels.isna(A, vtupn__qgqzd):
                val = A[vtupn__qgqzd]
            s += val
        return s
    return impl


@overload_method(FloatingArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_float_arr(A):
        data = []
        way__rdikj = []
        mlyv__xiqq = False
        s = set()
        for vtupn__qgqzd in range(len(A)):
            val = A[vtupn__qgqzd]
            if bodo.libs.array_kernels.isna(A, vtupn__qgqzd):
                if not mlyv__xiqq:
                    data.append(dtype(1))
                    way__rdikj.append(False)
                    mlyv__xiqq = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                way__rdikj.append(True)
        uyzsl__jcrio = np.array(data)
        n = len(uyzsl__jcrio)
        sio__ilyrv = n + 7 >> 3
        bzbub__oaxjr = np.empty(sio__ilyrv, np.uint8)
        for lppj__krcms in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(bzbub__oaxjr, lppj__krcms,
                way__rdikj[lppj__krcms])
        return init_float_array(uyzsl__jcrio, bzbub__oaxjr)
    return impl_float_arr
