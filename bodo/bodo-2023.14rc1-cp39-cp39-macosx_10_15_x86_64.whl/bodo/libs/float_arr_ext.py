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
        xldd__bqwzl = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, xldd__bqwzl)


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
        jpuni__ayy = f'Float{dtype.bitwidth}Dtype()'
        super(FloatDtype, self).__init__(jpuni__ayy)


register_model(FloatDtype)(models.OpaqueModel)


@box(FloatDtype)
def box_floatdtype(typ, val, c):
    kjna__fyjmw = c.context.insert_const_string(c.builder.module, 'pandas')
    eep__cnojd = c.pyapi.import_module_noblock(kjna__fyjmw)
    amr__sqwy = c.pyapi.call_method(eep__cnojd, str(typ)[:-2], ())
    c.pyapi.decref(eep__cnojd)
    return amr__sqwy


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
    rjpw__jyfo = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(rjpw__jyfo)
    c.pyapi.decref(rjpw__jyfo)
    uncot__qxd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    gmf__cbj = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64),
        7)), lir.Constant(lir.IntType(64), 8))
    zorw__yajt = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [gmf__cbj])
    aogrb__febua = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    dcsq__azc = cgutils.get_or_insert_function(c.builder.module,
        aogrb__febua, name='is_pd_float_array')
    ddsx__ugll = c.builder.call(dcsq__azc, [obj])
    lklsd__fwyt = c.builder.icmp_unsigned('!=', ddsx__ugll, ddsx__ugll.type(0))
    with c.builder.if_else(lklsd__fwyt) as (bbbab__esww, wtna__jsva):
        with bbbab__esww:
            zwqa__sejg = c.pyapi.object_getattr_string(obj, '_data')
            uncot__qxd.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), zwqa__sejg).value
            ant__xjp = c.pyapi.object_getattr_string(obj, '_mask')
            behqh__ubtrl = c.pyapi.to_native_value(types.Array(types.bool_,
                1, 'C'), ant__xjp).value
            c.pyapi.decref(zwqa__sejg)
            c.pyapi.decref(ant__xjp)
            tue__spf = c.context.make_array(types.Array(types.bool_, 1, 'C'))(c
                .context, c.builder, behqh__ubtrl)
            aogrb__febua = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            dcsq__azc = cgutils.get_or_insert_function(c.builder.module,
                aogrb__febua, name='mask_arr_to_bitmap')
            c.builder.call(dcsq__azc, [zorw__yajt.data, tue__spf.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), behqh__ubtrl)
        with wtna__jsva:
            com__yxqn = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            aogrb__febua = lir.FunctionType(lir.IntType(32), [lir.IntType(8
                ).as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8)
                .as_pointer()])
            thbv__sme = cgutils.get_or_insert_function(c.builder.module,
                aogrb__febua, name='float_array_from_sequence')
            c.builder.call(thbv__sme, [obj, c.builder.bitcast(com__yxqn.
                data, lir.IntType(8).as_pointer()), zorw__yajt.data])
            uncot__qxd.data = com__yxqn._getvalue()
    uncot__qxd.null_bitmap = zorw__yajt._getvalue()
    bliz__jzt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(uncot__qxd._getvalue(), is_error=bliz__jzt)


@box(FloatingArrayType)
def box_float_array(typ, val, c):
    uncot__qxd = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        uncot__qxd.data, c.env_manager)
    wrgi__ogpaa = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, uncot__qxd.null_bitmap).data
    rjpw__jyfo = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(rjpw__jyfo)
    kjna__fyjmw = c.context.insert_const_string(c.builder.module, 'numpy')
    omyh__vqxj = c.pyapi.import_module_noblock(kjna__fyjmw)
    yfqwr__urds = c.pyapi.object_getattr_string(omyh__vqxj, 'bool_')
    behqh__ubtrl = c.pyapi.call_method(omyh__vqxj, 'empty', (rjpw__jyfo,
        yfqwr__urds))
    czacx__wjb = c.pyapi.object_getattr_string(behqh__ubtrl, 'ctypes')
    szx__zvynk = c.pyapi.object_getattr_string(czacx__wjb, 'data')
    yxeb__vbn = c.builder.inttoptr(c.pyapi.long_as_longlong(szx__zvynk),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as gykk__eaj:
        gxdcg__stp = gykk__eaj.index
        knoey__vhnrb = c.builder.lshr(gxdcg__stp, lir.Constant(lir.IntType(
            64), 3))
        fec__tmr = c.builder.load(cgutils.gep(c.builder, wrgi__ogpaa,
            knoey__vhnrb))
        lvc__xhc = c.builder.trunc(c.builder.and_(gxdcg__stp, lir.Constant(
            lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(fec__tmr, lvc__xhc), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        jckx__yzg = cgutils.gep(c.builder, yxeb__vbn, gxdcg__stp)
        c.builder.store(val, jckx__yzg)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        uncot__qxd.null_bitmap)
    kjna__fyjmw = c.context.insert_const_string(c.builder.module, 'pandas')
    eep__cnojd = c.pyapi.import_module_noblock(kjna__fyjmw)
    itp__cvw = c.pyapi.object_getattr_string(eep__cnojd, 'arrays')
    amr__sqwy = c.pyapi.call_method(itp__cvw, 'FloatingArray', (data,
        behqh__ubtrl))
    c.pyapi.decref(eep__cnojd)
    c.pyapi.decref(rjpw__jyfo)
    c.pyapi.decref(omyh__vqxj)
    c.pyapi.decref(yfqwr__urds)
    c.pyapi.decref(czacx__wjb)
    c.pyapi.decref(szx__zvynk)
    c.pyapi.decref(itp__cvw)
    c.pyapi.decref(data)
    c.pyapi.decref(behqh__ubtrl)
    return amr__sqwy


@intrinsic
def init_float_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        rme__dtg, pws__vhv = args
        uncot__qxd = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        uncot__qxd.data = rme__dtg
        uncot__qxd.null_bitmap = pws__vhv
        context.nrt.incref(builder, signature.args[0], rme__dtg)
        context.nrt.incref(builder, signature.args[1], pws__vhv)
        return uncot__qxd._getvalue()
    rcj__hzc = FloatingArrayType(data.dtype)
    hrw__ciwd = rcj__hzc(data, null_bitmap)
    return hrw__ciwd, codegen


@lower_constant(FloatingArrayType)
def lower_constant_float_arr(context, builder, typ, pyval):
    n = len(pyval)
    zvqmo__nzqm = np.empty(n, pyval.dtype.type)
    ugjr__rsdyp = np.empty(n + 7 >> 3, np.uint8)
    for gxdcg__stp, s in enumerate(pyval):
        awtqm__ygt = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ugjr__rsdyp, gxdcg__stp, int(
            not awtqm__ygt))
        if not awtqm__ygt:
            zvqmo__nzqm[gxdcg__stp] = s
    sdt__qnee = context.get_constant_generic(builder, types.Array(typ.dtype,
        1, 'C'), zvqmo__nzqm)
    kfgxq__hrz = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), ugjr__rsdyp)
    return lir.Constant.literal_struct([sdt__qnee, kfgxq__hrz])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_float_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    gnp__ghnp = args[0]
    if equiv_set.has_shape(gnp__ghnp):
        return ArrayAnalysis.AnalyzeResult(shape=gnp__ghnp, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_float_arr_ext_get_float_arr_data
    ) = get_float_arr_data_equiv


def init_float_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    gnp__ghnp = args[0]
    if equiv_set.has_shape(gnp__ghnp):
        return ArrayAnalysis.AnalyzeResult(shape=gnp__ghnp, pre=[])
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
    zvqmo__nzqm = np.empty(n, dtype)
    mgg__houow = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_float_array(zvqmo__nzqm, mgg__houow)


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
            ftt__zgqw, nlv__ppei = array_getitem_bool_index(A, ind)
            return init_float_array(ftt__zgqw, nlv__ppei)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ftt__zgqw, nlv__ppei = array_getitem_int_index(A, ind)
            return init_float_array(ftt__zgqw, nlv__ppei)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            ftt__zgqw, nlv__ppei = array_getitem_slice_index(A, ind)
            return init_float_array(ftt__zgqw, nlv__ppei)
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
    wgojw__setzz = (
        f"setitem for FloatingArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    rzhl__vmek = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if rzhl__vmek:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(wgojw__setzz)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean, types.Float)) or rzhl__vmek):
        raise BodoError(wgojw__setzz)
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
            cbq__mzhf = np.empty(n, nb_dtype)
            for gxdcg__stp in numba.parfors.parfor.internal_prange(n):
                cbq__mzhf[gxdcg__stp] = data[gxdcg__stp]
                if bodo.libs.array_kernels.isna(A, gxdcg__stp):
                    cbq__mzhf[gxdcg__stp] = np.nan
            return cbq__mzhf
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
    for iwve__eqltw in numba.np.ufunc_db.get_ufuncs():
        artc__vwcf = create_op_overload(iwve__eqltw, iwve__eqltw.nin)
        overload(iwve__eqltw, no_unliteral=True)(artc__vwcf)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        artc__vwcf = create_op_overload(op, 2)
        overload(op)(artc__vwcf)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        artc__vwcf = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(artc__vwcf)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        artc__vwcf = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(artc__vwcf)


_install_unary_ops()


@overload_method(FloatingArrayType, 'sum', no_unliteral=True)
def overload_float_arr_sum(A, skipna=True, min_count=0):
    wejx__kaz = dict(skipna=skipna, min_count=min_count)
    yzdn__enwx = dict(skipna=True, min_count=0)
    check_unsupported_args('FloatingArray.sum', wejx__kaz, yzdn__enwx)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0.0
        for gxdcg__stp in numba.parfors.parfor.internal_prange(len(A)):
            val = 0.0
            if not bodo.libs.array_kernels.isna(A, gxdcg__stp):
                val = A[gxdcg__stp]
            s += val
        return s
    return impl


@overload_method(FloatingArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_float_arr(A):
        data = []
        lvc__xhc = []
        kmgdt__xwob = False
        s = set()
        for gxdcg__stp in range(len(A)):
            val = A[gxdcg__stp]
            if bodo.libs.array_kernels.isna(A, gxdcg__stp):
                if not kmgdt__xwob:
                    data.append(dtype(1))
                    lvc__xhc.append(False)
                    kmgdt__xwob = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                lvc__xhc.append(True)
        ftt__zgqw = np.array(data)
        n = len(ftt__zgqw)
        gmf__cbj = n + 7 >> 3
        nlv__ppei = np.empty(gmf__cbj, np.uint8)
        for kvqk__favt in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(nlv__ppei, kvqk__favt,
                lvc__xhc[kvqk__favt])
        return init_float_array(ftt__zgqw, nlv__ppei)
    return impl_float_arr
