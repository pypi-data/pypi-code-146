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
        rvic__fttq = int(np.log2(self.dtype.bitwidth // 8))
        zatdf__zhwur = 0 if self.dtype.signed else 4
        idx = rvic__fttq + zatdf__zhwur
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wylq__smv = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, wylq__smv)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    wcgd__brr = 8 * val.dtype.itemsize
    mpn__lsc = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(mpn__lsc, wcgd__brr))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        atnq__xgv = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(atnq__xgv)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    eujos__kwaie = c.context.insert_const_string(c.builder.module, 'pandas')
    wfaqo__xxd = c.pyapi.import_module_noblock(eujos__kwaie)
    pep__hnj = c.pyapi.call_method(wfaqo__xxd, str(typ)[:-2], ())
    c.pyapi.decref(wfaqo__xxd)
    return pep__hnj


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    wcgd__brr = 8 * val.itemsize
    mpn__lsc = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(mpn__lsc, wcgd__brr))
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
    wbwo__fodo = n + 7 >> 3
    ikh__hkhm = np.empty(wbwo__fodo, np.uint8)
    for i in range(n):
        jmt__ufq = i // 8
        ikh__hkhm[jmt__ufq] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            ikh__hkhm[jmt__ufq]) & kBitmask[i % 8]
    return ikh__hkhm


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    eazn__ijsd = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(eazn__ijsd)
    c.pyapi.decref(eazn__ijsd)
    lwpm__ayzz = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    wbwo__fodo = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    vezbq__brfvq = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [wbwo__fodo])
    zwnu__kqw = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    pjvbg__idhb = cgutils.get_or_insert_function(c.builder.module,
        zwnu__kqw, name='is_pd_int_array')
    dsu__fmh = c.builder.call(pjvbg__idhb, [obj])
    rfqw__tfmh = c.builder.icmp_unsigned('!=', dsu__fmh, dsu__fmh.type(0))
    with c.builder.if_else(rfqw__tfmh) as (vxu__epim, pyrhx__fxe):
        with vxu__epim:
            siyyy__hya = c.pyapi.object_getattr_string(obj, '_data')
            lwpm__ayzz.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), siyyy__hya).value
            xihz__nxcq = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), xihz__nxcq).value
            c.pyapi.decref(siyyy__hya)
            c.pyapi.decref(xihz__nxcq)
            ruh__toic = c.context.make_array(types.Array(types.bool_, 1, 'C'))(
                c.context, c.builder, mask_arr)
            zwnu__kqw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            pjvbg__idhb = cgutils.get_or_insert_function(c.builder.module,
                zwnu__kqw, name='mask_arr_to_bitmap')
            c.builder.call(pjvbg__idhb, [vezbq__brfvq.data, ruh__toic.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with pyrhx__fxe:
            tpgmd__brck = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            zwnu__kqw = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            bzjqc__zdwy = cgutils.get_or_insert_function(c.builder.module,
                zwnu__kqw, name='int_array_from_sequence')
            c.builder.call(bzjqc__zdwy, [obj, c.builder.bitcast(tpgmd__brck
                .data, lir.IntType(8).as_pointer()), vezbq__brfvq.data])
            lwpm__ayzz.data = tpgmd__brck._getvalue()
    lwpm__ayzz.null_bitmap = vezbq__brfvq._getvalue()
    shx__mec = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lwpm__ayzz._getvalue(), is_error=shx__mec)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    lwpm__ayzz = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        lwpm__ayzz.data, c.env_manager)
    tnj__uuxv = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, lwpm__ayzz.null_bitmap).data
    eazn__ijsd = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(eazn__ijsd)
    eujos__kwaie = c.context.insert_const_string(c.builder.module, 'numpy')
    auhjh__imy = c.pyapi.import_module_noblock(eujos__kwaie)
    lcmtk__ciyb = c.pyapi.object_getattr_string(auhjh__imy, 'bool_')
    mask_arr = c.pyapi.call_method(auhjh__imy, 'empty', (eazn__ijsd,
        lcmtk__ciyb))
    vcw__uaezj = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    lyu__qhd = c.pyapi.object_getattr_string(vcw__uaezj, 'data')
    bfyso__bnq = c.builder.inttoptr(c.pyapi.long_as_longlong(lyu__qhd), lir
        .IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as lsmva__dysc:
        i = lsmva__dysc.index
        ccxk__tyco = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        mcmxv__ykz = c.builder.load(cgutils.gep(c.builder, tnj__uuxv,
            ccxk__tyco))
        uwl__zakdw = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(mcmxv__ykz, uwl__zakdw), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        qgc__bgx = cgutils.gep(c.builder, bfyso__bnq, i)
        c.builder.store(val, qgc__bgx)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        lwpm__ayzz.null_bitmap)
    eujos__kwaie = c.context.insert_const_string(c.builder.module, 'pandas')
    wfaqo__xxd = c.pyapi.import_module_noblock(eujos__kwaie)
    zqe__icvg = c.pyapi.object_getattr_string(wfaqo__xxd, 'arrays')
    pep__hnj = c.pyapi.call_method(zqe__icvg, 'IntegerArray', (data, mask_arr))
    c.pyapi.decref(wfaqo__xxd)
    c.pyapi.decref(eazn__ijsd)
    c.pyapi.decref(auhjh__imy)
    c.pyapi.decref(lcmtk__ciyb)
    c.pyapi.decref(vcw__uaezj)
    c.pyapi.decref(lyu__qhd)
    c.pyapi.decref(zqe__icvg)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return pep__hnj


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        vly__tgrcu, zceb__vge = args
        lwpm__ayzz = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        lwpm__ayzz.data = vly__tgrcu
        lwpm__ayzz.null_bitmap = zceb__vge
        context.nrt.incref(builder, signature.args[0], vly__tgrcu)
        context.nrt.incref(builder, signature.args[1], zceb__vge)
        return lwpm__ayzz._getvalue()
    gva__xmp = IntegerArrayType(data.dtype)
    pdnk__esmb = gva__xmp(data, null_bitmap)
    return pdnk__esmb, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    lxnl__xqs = np.empty(n, pyval.dtype.type)
    chpnd__czt = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        fypgp__jrifo = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(chpnd__czt, i, int(not
            fypgp__jrifo))
        if not fypgp__jrifo:
            lxnl__xqs[i] = s
    cdty__mqi = context.get_constant_generic(builder, types.Array(typ.dtype,
        1, 'C'), lxnl__xqs)
    nixih__unysd = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), chpnd__czt)
    return lir.Constant.literal_struct([cdty__mqi, nixih__unysd])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    zkkhf__art = args[0]
    if equiv_set.has_shape(zkkhf__art):
        return ArrayAnalysis.AnalyzeResult(shape=zkkhf__art, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    zkkhf__art = args[0]
    if equiv_set.has_shape(zkkhf__art):
        return ArrayAnalysis.AnalyzeResult(shape=zkkhf__art, pre=[])
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
    lxnl__xqs = np.empty(n, dtype)
    idjb__ipga = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(lxnl__xqs, idjb__ipga)


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
            ppwm__bsbfe, oawx__xam = array_getitem_bool_index(A, ind)
            return init_integer_array(ppwm__bsbfe, oawx__xam)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ppwm__bsbfe, oawx__xam = array_getitem_int_index(A, ind)
            return init_integer_array(ppwm__bsbfe, oawx__xam)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            ppwm__bsbfe, oawx__xam = array_getitem_slice_index(A, ind)
            return init_integer_array(ppwm__bsbfe, oawx__xam)
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
    ryxg__kvf = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    bip__pbcb = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if bip__pbcb:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(ryxg__kvf)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or bip__pbcb):
        raise BodoError(ryxg__kvf)
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
            cfkg__ffei = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                cfkg__ffei[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    cfkg__ffei[i] = np.nan
            return cfkg__ffei
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
    for ogykj__caubj in numba.np.ufunc_db.get_ufuncs():
        ddk__tdx = create_op_overload(ogykj__caubj, ogykj__caubj.nin)
        overload(ogykj__caubj, no_unliteral=True)(ddk__tdx)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        ddk__tdx = create_op_overload(op, 2)
        overload(op)(ddk__tdx)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        ddk__tdx = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(ddk__tdx)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        ddk__tdx = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(ddk__tdx)


_install_unary_ops()


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    mlf__eyh = dict(skipna=skipna, min_count=min_count)
    wdqug__xafcb = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', mlf__eyh, wdqug__xafcb)

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
        uwl__zakdw = []
        vxo__giig = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not vxo__giig:
                    data.append(dtype(1))
                    uwl__zakdw.append(False)
                    vxo__giig = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                uwl__zakdw.append(True)
        ppwm__bsbfe = np.array(data)
        n = len(ppwm__bsbfe)
        wbwo__fodo = n + 7 >> 3
        oawx__xam = np.empty(wbwo__fodo, np.uint8)
        for omi__yjfbf in range(n):
            set_bit_to_arr(oawx__xam, omi__yjfbf, uwl__zakdw[omi__yjfbf])
        return init_integer_array(ppwm__bsbfe, oawx__xam)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    aql__ics = numba.core.registry.cpu_target.typing_context
    szhwk__xtivi = aql__ics.resolve_function_type(op, (types.Array(A.dtype,
        1, 'C'),), {}).return_type
    szhwk__xtivi = to_nullable_type(szhwk__xtivi)

    def impl(A):
        n = len(A)
        jwh__mdzl = bodo.utils.utils.alloc_type(n, szhwk__xtivi, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(jwh__mdzl, i)
                continue
            jwh__mdzl[i] = op(A[i])
        return jwh__mdzl
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    vzry__ktu = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    dtxx__dne = isinstance(lhs, (types.Number, types.Boolean))
    jjgoc__nivf = isinstance(rhs, (types.Number, types.Boolean))
    dwni__wzr = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    mwzs__njbh = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    aql__ics = numba.core.registry.cpu_target.typing_context
    szhwk__xtivi = aql__ics.resolve_function_type(op, (dwni__wzr,
        mwzs__njbh), {}).return_type
    szhwk__xtivi = to_nullable_type(szhwk__xtivi)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    kin__mylz = 'lhs' if dtxx__dne else 'lhs[i]'
    exicj__vhjx = 'rhs' if jjgoc__nivf else 'rhs[i]'
    grk__ncn = 'False' if dtxx__dne else 'bodo.libs.array_kernels.isna(lhs, i)'
    jyw__ekei = ('False' if jjgoc__nivf else
        'bodo.libs.array_kernels.isna(rhs, i)')
    tsll__cfxb = 'def impl(lhs, rhs):\n'
    tsll__cfxb += '  n = len({})\n'.format('lhs' if not dtxx__dne else 'rhs')
    if vzry__ktu:
        tsll__cfxb += '  out_arr = {}\n'.format('lhs' if not dtxx__dne else
            'rhs')
    else:
        tsll__cfxb += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    tsll__cfxb += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    tsll__cfxb += '    if ({}\n'.format(grk__ncn)
    tsll__cfxb += '        or {}):\n'.format(jyw__ekei)
    tsll__cfxb += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    tsll__cfxb += '      continue\n'
    tsll__cfxb += (
        """    out_arr[i] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(op({}, {}))
"""
        .format(kin__mylz, exicj__vhjx))
    tsll__cfxb += '  return out_arr\n'
    hcqh__aguik = {}
    exec(tsll__cfxb, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        szhwk__xtivi, 'op': op}, hcqh__aguik)
    impl = hcqh__aguik['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        dtxx__dne = lhs in [pd_timedelta_type]
        jjgoc__nivf = rhs in [pd_timedelta_type]
        if dtxx__dne:

            def impl(lhs, rhs):
                n = len(rhs)
                jwh__mdzl = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(jwh__mdzl, i)
                        continue
                    jwh__mdzl[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs, rhs[i]))
                return jwh__mdzl
            return impl
        elif jjgoc__nivf:

            def impl(lhs, rhs):
                n = len(lhs)
                jwh__mdzl = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(jwh__mdzl, i)
                        continue
                    jwh__mdzl[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs[i], rhs))
                return jwh__mdzl
            return impl
    return impl
