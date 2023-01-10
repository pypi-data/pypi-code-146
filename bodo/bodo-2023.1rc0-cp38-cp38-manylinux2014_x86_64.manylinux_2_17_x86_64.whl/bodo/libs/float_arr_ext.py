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
        wstiz__ddarf = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, wstiz__ddarf)


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
        ppvp__kcr = f'Float{dtype.bitwidth}Dtype()'
        super(FloatDtype, self).__init__(ppvp__kcr)


register_model(FloatDtype)(models.OpaqueModel)


@box(FloatDtype)
def box_floatdtype(typ, val, c):
    tmnp__xfdc = c.context.insert_const_string(c.builder.module, 'pandas')
    uglzu__cvbf = c.pyapi.import_module_noblock(tmnp__xfdc)
    tgafb__svt = c.pyapi.call_method(uglzu__cvbf, str(typ)[:-2], ())
    c.pyapi.decref(uglzu__cvbf)
    return tgafb__svt


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
    whir__oshh = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(whir__oshh)
    c.pyapi.decref(whir__oshh)
    couir__ksofb = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    yehqx__dvzkb = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    llap__rgohu = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [yehqx__dvzkb])
    bjjv__qhl = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    ddonq__kygpw = cgutils.get_or_insert_function(c.builder.module,
        bjjv__qhl, name='is_pd_float_array')
    bdh__fkqn = c.builder.call(ddonq__kygpw, [obj])
    esq__sny = c.builder.icmp_unsigned('!=', bdh__fkqn, bdh__fkqn.type(0))
    with c.builder.if_else(esq__sny) as (jux__eai, icbqy__ufgv):
        with jux__eai:
            rpar__xlerk = c.pyapi.object_getattr_string(obj, '_data')
            couir__ksofb.data = c.pyapi.to_native_value(types.Array(typ.
                dtype, 1, 'C'), rpar__xlerk).value
            xtbpx__iowp = c.pyapi.object_getattr_string(obj, '_mask')
            ddj__rzhre = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), xtbpx__iowp).value
            c.pyapi.decref(rpar__xlerk)
            c.pyapi.decref(xtbpx__iowp)
            yhpgy__wku = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, ddj__rzhre)
            bjjv__qhl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            ddonq__kygpw = cgutils.get_or_insert_function(c.builder.module,
                bjjv__qhl, name='mask_arr_to_bitmap')
            c.builder.call(ddonq__kygpw, [llap__rgohu.data, yhpgy__wku.data, n]
                )
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), ddj__rzhre)
        with icbqy__ufgv:
            wmf__eiiz = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            bjjv__qhl = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            ehih__vbda = cgutils.get_or_insert_function(c.builder.module,
                bjjv__qhl, name='float_array_from_sequence')
            c.builder.call(ehih__vbda, [obj, c.builder.bitcast(wmf__eiiz.
                data, lir.IntType(8).as_pointer()), llap__rgohu.data])
            couir__ksofb.data = wmf__eiiz._getvalue()
    couir__ksofb.null_bitmap = llap__rgohu._getvalue()
    mnzr__ltn = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(couir__ksofb._getvalue(), is_error=mnzr__ltn)


@box(FloatingArrayType)
def box_float_array(typ, val, c):
    couir__ksofb = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        couir__ksofb.data, c.env_manager)
    ndu__aawz = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, couir__ksofb.null_bitmap).data
    whir__oshh = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(whir__oshh)
    tmnp__xfdc = c.context.insert_const_string(c.builder.module, 'numpy')
    qfal__gvrru = c.pyapi.import_module_noblock(tmnp__xfdc)
    diqva__ligir = c.pyapi.object_getattr_string(qfal__gvrru, 'bool_')
    ddj__rzhre = c.pyapi.call_method(qfal__gvrru, 'empty', (whir__oshh,
        diqva__ligir))
    zaher__qxzdq = c.pyapi.object_getattr_string(ddj__rzhre, 'ctypes')
    jaqn__plmj = c.pyapi.object_getattr_string(zaher__qxzdq, 'data')
    edu__iiz = c.builder.inttoptr(c.pyapi.long_as_longlong(jaqn__plmj), lir
        .IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as frh__nqjk:
        chjk__qyuk = frh__nqjk.index
        wbc__jljh = c.builder.lshr(chjk__qyuk, lir.Constant(lir.IntType(64), 3)
            )
        yhq__bqgv = c.builder.load(cgutils.gep(c.builder, ndu__aawz, wbc__jljh)
            )
        pwwzs__owvq = c.builder.trunc(c.builder.and_(chjk__qyuk, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(yhq__bqgv, pwwzs__owvq), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        bpho__qyvy = cgutils.gep(c.builder, edu__iiz, chjk__qyuk)
        c.builder.store(val, bpho__qyvy)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        couir__ksofb.null_bitmap)
    tmnp__xfdc = c.context.insert_const_string(c.builder.module, 'pandas')
    uglzu__cvbf = c.pyapi.import_module_noblock(tmnp__xfdc)
    xrn__ucsn = c.pyapi.object_getattr_string(uglzu__cvbf, 'arrays')
    tgafb__svt = c.pyapi.call_method(xrn__ucsn, 'FloatingArray', (data,
        ddj__rzhre))
    c.pyapi.decref(uglzu__cvbf)
    c.pyapi.decref(whir__oshh)
    c.pyapi.decref(qfal__gvrru)
    c.pyapi.decref(diqva__ligir)
    c.pyapi.decref(zaher__qxzdq)
    c.pyapi.decref(jaqn__plmj)
    c.pyapi.decref(xrn__ucsn)
    c.pyapi.decref(data)
    c.pyapi.decref(ddj__rzhre)
    return tgafb__svt


@intrinsic
def init_float_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        hou__kle, sndnq__bsm = args
        couir__ksofb = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        couir__ksofb.data = hou__kle
        couir__ksofb.null_bitmap = sndnq__bsm
        context.nrt.incref(builder, signature.args[0], hou__kle)
        context.nrt.incref(builder, signature.args[1], sndnq__bsm)
        return couir__ksofb._getvalue()
    jghv__buwqi = FloatingArrayType(data.dtype)
    cmqa__ifa = jghv__buwqi(data, null_bitmap)
    return cmqa__ifa, codegen


@lower_constant(FloatingArrayType)
def lower_constant_float_arr(context, builder, typ, pyval):
    n = len(pyval)
    xvk__xrr = np.empty(n, pyval.dtype.type)
    bls__xvdd = np.empty(n + 7 >> 3, np.uint8)
    for chjk__qyuk, s in enumerate(pyval):
        gih__jbg = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(bls__xvdd, chjk__qyuk, int(not
            gih__jbg))
        if not gih__jbg:
            xvk__xrr[chjk__qyuk] = s
    zlr__zqsdy = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), xvk__xrr)
    nds__hmm = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), bls__xvdd)
    return lir.Constant.literal_struct([zlr__zqsdy, nds__hmm])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_float_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    cwwct__rvbz = args[0]
    if equiv_set.has_shape(cwwct__rvbz):
        return ArrayAnalysis.AnalyzeResult(shape=cwwct__rvbz, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_float_arr_ext_get_float_arr_data
    ) = get_float_arr_data_equiv


def init_float_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    cwwct__rvbz = args[0]
    if equiv_set.has_shape(cwwct__rvbz):
        return ArrayAnalysis.AnalyzeResult(shape=cwwct__rvbz, pre=[])
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
    xvk__xrr = np.empty(n, dtype)
    vxg__cec = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_float_array(xvk__xrr, vxg__cec)


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
            bbjyr__sxvf, xyau__plh = array_getitem_bool_index(A, ind)
            return init_float_array(bbjyr__sxvf, xyau__plh)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            bbjyr__sxvf, xyau__plh = array_getitem_int_index(A, ind)
            return init_float_array(bbjyr__sxvf, xyau__plh)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            bbjyr__sxvf, xyau__plh = array_getitem_slice_index(A, ind)
            return init_float_array(bbjyr__sxvf, xyau__plh)
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
    yhc__tznjt = (
        f"setitem for FloatingArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    rihio__othy = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if rihio__othy:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(yhc__tznjt)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean, types.Float)) or rihio__othy):
        raise BodoError(yhc__tznjt)
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
            wuhn__udhbu = np.empty(n, nb_dtype)
            for chjk__qyuk in numba.parfors.parfor.internal_prange(n):
                wuhn__udhbu[chjk__qyuk] = data[chjk__qyuk]
                if bodo.libs.array_kernels.isna(A, chjk__qyuk):
                    wuhn__udhbu[chjk__qyuk] = np.nan
            return wuhn__udhbu
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
    for bhth__qal in numba.np.ufunc_db.get_ufuncs():
        quma__mwva = create_op_overload(bhth__qal, bhth__qal.nin)
        overload(bhth__qal, no_unliteral=True)(quma__mwva)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        quma__mwva = create_op_overload(op, 2)
        overload(op)(quma__mwva)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        quma__mwva = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(quma__mwva)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        quma__mwva = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(quma__mwva)


_install_unary_ops()


@overload_method(FloatingArrayType, 'sum', no_unliteral=True)
def overload_float_arr_sum(A, skipna=True, min_count=0):
    nyp__znrrp = dict(skipna=skipna, min_count=min_count)
    aioq__jiup = dict(skipna=True, min_count=0)
    check_unsupported_args('FloatingArray.sum', nyp__znrrp, aioq__jiup)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0.0
        for chjk__qyuk in numba.parfors.parfor.internal_prange(len(A)):
            val = 0.0
            if not bodo.libs.array_kernels.isna(A, chjk__qyuk):
                val = A[chjk__qyuk]
            s += val
        return s
    return impl


@overload_method(FloatingArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_float_arr(A):
        data = []
        pwwzs__owvq = []
        ttv__ugw = False
        s = set()
        for chjk__qyuk in range(len(A)):
            val = A[chjk__qyuk]
            if bodo.libs.array_kernels.isna(A, chjk__qyuk):
                if not ttv__ugw:
                    data.append(dtype(1))
                    pwwzs__owvq.append(False)
                    ttv__ugw = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                pwwzs__owvq.append(True)
        bbjyr__sxvf = np.array(data)
        n = len(bbjyr__sxvf)
        yehqx__dvzkb = n + 7 >> 3
        xyau__plh = np.empty(yehqx__dvzkb, np.uint8)
        for jwi__yfv in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(xyau__plh, jwi__yfv,
                pwwzs__owvq[jwi__yfv])
        return init_float_array(bbjyr__sxvf, xyau__plh)
    return impl_float_arr
