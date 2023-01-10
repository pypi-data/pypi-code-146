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
        lhxgy__ono = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, lhxgy__ono)


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
        xbmg__iqrmu = f'Float{dtype.bitwidth}Dtype()'
        super(FloatDtype, self).__init__(xbmg__iqrmu)


register_model(FloatDtype)(models.OpaqueModel)


@box(FloatDtype)
def box_floatdtype(typ, val, c):
    zkn__hnt = c.context.insert_const_string(c.builder.module, 'pandas')
    zoega__ngwn = c.pyapi.import_module_noblock(zkn__hnt)
    xdtr__ecxl = c.pyapi.call_method(zoega__ngwn, str(typ)[:-2], ())
    c.pyapi.decref(zoega__ngwn)
    return xdtr__ecxl


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
    wvz__hxjtl = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(wvz__hxjtl)
    c.pyapi.decref(wvz__hxjtl)
    myobl__syhoo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lobrb__hwibu = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    iccy__yqd = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types
        .Array(types.uint8, 1, 'C'), [lobrb__hwibu])
    ast__zgxp = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    khm__pcaie = cgutils.get_or_insert_function(c.builder.module, ast__zgxp,
        name='is_pd_float_array')
    tegb__acei = c.builder.call(khm__pcaie, [obj])
    fcdkx__kcpk = c.builder.icmp_unsigned('!=', tegb__acei, tegb__acei.type(0))
    with c.builder.if_else(fcdkx__kcpk) as (bqqt__iuvao, pvy__eydrm):
        with bqqt__iuvao:
            uqvt__sij = c.pyapi.object_getattr_string(obj, '_data')
            myobl__syhoo.data = c.pyapi.to_native_value(types.Array(typ.
                dtype, 1, 'C'), uqvt__sij).value
            dmns__bdf = c.pyapi.object_getattr_string(obj, '_mask')
            didwa__pwc = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), dmns__bdf).value
            c.pyapi.decref(uqvt__sij)
            c.pyapi.decref(dmns__bdf)
            omq__tpm = c.context.make_array(types.Array(types.bool_, 1, 'C'))(c
                .context, c.builder, didwa__pwc)
            ast__zgxp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            khm__pcaie = cgutils.get_or_insert_function(c.builder.module,
                ast__zgxp, name='mask_arr_to_bitmap')
            c.builder.call(khm__pcaie, [iccy__yqd.data, omq__tpm.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), didwa__pwc)
        with pvy__eydrm:
            nuab__zlkx = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            ast__zgxp = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            tnf__akc = cgutils.get_or_insert_function(c.builder.module,
                ast__zgxp, name='float_array_from_sequence')
            c.builder.call(tnf__akc, [obj, c.builder.bitcast(nuab__zlkx.
                data, lir.IntType(8).as_pointer()), iccy__yqd.data])
            myobl__syhoo.data = nuab__zlkx._getvalue()
    myobl__syhoo.null_bitmap = iccy__yqd._getvalue()
    ineda__bcqo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(myobl__syhoo._getvalue(), is_error=ineda__bcqo)


@box(FloatingArrayType)
def box_float_array(typ, val, c):
    myobl__syhoo = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        myobl__syhoo.data, c.env_manager)
    naq__lwi = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, myobl__syhoo.null_bitmap).data
    wvz__hxjtl = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(wvz__hxjtl)
    zkn__hnt = c.context.insert_const_string(c.builder.module, 'numpy')
    rjtxm__aekqz = c.pyapi.import_module_noblock(zkn__hnt)
    drvh__fff = c.pyapi.object_getattr_string(rjtxm__aekqz, 'bool_')
    didwa__pwc = c.pyapi.call_method(rjtxm__aekqz, 'empty', (wvz__hxjtl,
        drvh__fff))
    qjz__hvz = c.pyapi.object_getattr_string(didwa__pwc, 'ctypes')
    vwu__vuizz = c.pyapi.object_getattr_string(qjz__hvz, 'data')
    fpaes__euw = c.builder.inttoptr(c.pyapi.long_as_longlong(vwu__vuizz),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as vdr__wnaea:
        zid__nmw = vdr__wnaea.index
        ajj__rxleo = c.builder.lshr(zid__nmw, lir.Constant(lir.IntType(64), 3))
        vsqi__qgq = c.builder.load(cgutils.gep(c.builder, naq__lwi, ajj__rxleo)
            )
        qej__immzn = c.builder.trunc(c.builder.and_(zid__nmw, lir.Constant(
            lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(vsqi__qgq, qej__immzn), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        xhsa__ujjgf = cgutils.gep(c.builder, fpaes__euw, zid__nmw)
        c.builder.store(val, xhsa__ujjgf)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        myobl__syhoo.null_bitmap)
    zkn__hnt = c.context.insert_const_string(c.builder.module, 'pandas')
    zoega__ngwn = c.pyapi.import_module_noblock(zkn__hnt)
    hlat__zhep = c.pyapi.object_getattr_string(zoega__ngwn, 'arrays')
    xdtr__ecxl = c.pyapi.call_method(hlat__zhep, 'FloatingArray', (data,
        didwa__pwc))
    c.pyapi.decref(zoega__ngwn)
    c.pyapi.decref(wvz__hxjtl)
    c.pyapi.decref(rjtxm__aekqz)
    c.pyapi.decref(drvh__fff)
    c.pyapi.decref(qjz__hvz)
    c.pyapi.decref(vwu__vuizz)
    c.pyapi.decref(hlat__zhep)
    c.pyapi.decref(data)
    c.pyapi.decref(didwa__pwc)
    return xdtr__ecxl


@intrinsic
def init_float_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        ditna__ghvui, ybl__ghuy = args
        myobl__syhoo = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        myobl__syhoo.data = ditna__ghvui
        myobl__syhoo.null_bitmap = ybl__ghuy
        context.nrt.incref(builder, signature.args[0], ditna__ghvui)
        context.nrt.incref(builder, signature.args[1], ybl__ghuy)
        return myobl__syhoo._getvalue()
    jacgh__zpenh = FloatingArrayType(data.dtype)
    wos__gdah = jacgh__zpenh(data, null_bitmap)
    return wos__gdah, codegen


@lower_constant(FloatingArrayType)
def lower_constant_float_arr(context, builder, typ, pyval):
    n = len(pyval)
    faqmv__xdevm = np.empty(n, pyval.dtype.type)
    ppntg__pweoj = np.empty(n + 7 >> 3, np.uint8)
    for zid__nmw, s in enumerate(pyval):
        zbq__bmenr = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ppntg__pweoj, zid__nmw, int(
            not zbq__bmenr))
        if not zbq__bmenr:
            faqmv__xdevm[zid__nmw] = s
    ybow__fwtpe = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), faqmv__xdevm)
    udta__hkq = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), ppntg__pweoj)
    return lir.Constant.literal_struct([ybow__fwtpe, udta__hkq])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_float_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    mmjy__hksna = args[0]
    if equiv_set.has_shape(mmjy__hksna):
        return ArrayAnalysis.AnalyzeResult(shape=mmjy__hksna, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_float_arr_ext_get_float_arr_data
    ) = get_float_arr_data_equiv


def init_float_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    mmjy__hksna = args[0]
    if equiv_set.has_shape(mmjy__hksna):
        return ArrayAnalysis.AnalyzeResult(shape=mmjy__hksna, pre=[])
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
    faqmv__xdevm = np.empty(n, dtype)
    evb__bzmk = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_float_array(faqmv__xdevm, evb__bzmk)


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
            ofw__kszkw, anhs__ovtb = array_getitem_bool_index(A, ind)
            return init_float_array(ofw__kszkw, anhs__ovtb)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ofw__kszkw, anhs__ovtb = array_getitem_int_index(A, ind)
            return init_float_array(ofw__kszkw, anhs__ovtb)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            ofw__kszkw, anhs__ovtb = array_getitem_slice_index(A, ind)
            return init_float_array(ofw__kszkw, anhs__ovtb)
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
    vxw__epwqa = (
        f"setitem for FloatingArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    mqq__spkpk = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if mqq__spkpk:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(vxw__epwqa)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean, types.Float)) or mqq__spkpk):
        raise BodoError(vxw__epwqa)
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
            sfxu__ecla = np.empty(n, nb_dtype)
            for zid__nmw in numba.parfors.parfor.internal_prange(n):
                sfxu__ecla[zid__nmw] = data[zid__nmw]
                if bodo.libs.array_kernels.isna(A, zid__nmw):
                    sfxu__ecla[zid__nmw] = np.nan
            return sfxu__ecla
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
    for ops__xne in numba.np.ufunc_db.get_ufuncs():
        nsgk__wczj = create_op_overload(ops__xne, ops__xne.nin)
        overload(ops__xne, no_unliteral=True)(nsgk__wczj)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        nsgk__wczj = create_op_overload(op, 2)
        overload(op)(nsgk__wczj)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        nsgk__wczj = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(nsgk__wczj)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        nsgk__wczj = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(nsgk__wczj)


_install_unary_ops()


@overload_method(FloatingArrayType, 'sum', no_unliteral=True)
def overload_float_arr_sum(A, skipna=True, min_count=0):
    pfz__ocqb = dict(skipna=skipna, min_count=min_count)
    yub__zbl = dict(skipna=True, min_count=0)
    check_unsupported_args('FloatingArray.sum', pfz__ocqb, yub__zbl)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0.0
        for zid__nmw in numba.parfors.parfor.internal_prange(len(A)):
            val = 0.0
            if not bodo.libs.array_kernels.isna(A, zid__nmw):
                val = A[zid__nmw]
            s += val
        return s
    return impl


@overload_method(FloatingArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_float_arr(A):
        data = []
        qej__immzn = []
        pem__jhh = False
        s = set()
        for zid__nmw in range(len(A)):
            val = A[zid__nmw]
            if bodo.libs.array_kernels.isna(A, zid__nmw):
                if not pem__jhh:
                    data.append(dtype(1))
                    qej__immzn.append(False)
                    pem__jhh = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                qej__immzn.append(True)
        ofw__kszkw = np.array(data)
        n = len(ofw__kszkw)
        lobrb__hwibu = n + 7 >> 3
        anhs__ovtb = np.empty(lobrb__hwibu, np.uint8)
        for wac__vqhcs in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(anhs__ovtb, wac__vqhcs,
                qej__immzn[wac__vqhcs])
        return init_float_array(ofw__kszkw, anhs__ovtb)
    return impl_float_arr
