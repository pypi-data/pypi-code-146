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
        mvj__ozth = int(np.log2(self.dtype.bitwidth // 8))
        nxazz__nxwas = 0 if self.dtype.signed else 4
        idx = mvj__ozth + nxazz__nxwas
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        sjpbk__cxf = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, sjpbk__cxf)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    kjmo__fit = 8 * val.dtype.itemsize
    idqbt__fyig = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(idqbt__fyig, kjmo__fit))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        ukk__qwobs = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(ukk__qwobs)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    pmf__kmqrr = c.context.insert_const_string(c.builder.module, 'pandas')
    etkjk__pwvfh = c.pyapi.import_module_noblock(pmf__kmqrr)
    pjo__cdd = c.pyapi.call_method(etkjk__pwvfh, str(typ)[:-2], ())
    c.pyapi.decref(etkjk__pwvfh)
    return pjo__cdd


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    kjmo__fit = 8 * val.itemsize
    idqbt__fyig = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(idqbt__fyig, kjmo__fit))
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
    nihc__nlhiz = n + 7 >> 3
    mio__ymkm = np.empty(nihc__nlhiz, np.uint8)
    for i in range(n):
        xam__ufo = i // 8
        mio__ymkm[xam__ufo] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            mio__ymkm[xam__ufo]) & kBitmask[i % 8]
    return mio__ymkm


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    mvm__iha = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(mvm__iha)
    c.pyapi.decref(mvm__iha)
    nhiq__gaxj = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    nihc__nlhiz = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    sml__zktes = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [nihc__nlhiz])
    rquv__ozch = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    vktq__ljn = cgutils.get_or_insert_function(c.builder.module, rquv__ozch,
        name='is_pd_int_array')
    axaiw__fpf = c.builder.call(vktq__ljn, [obj])
    tbr__xmrp = c.builder.icmp_unsigned('!=', axaiw__fpf, axaiw__fpf.type(0))
    with c.builder.if_else(tbr__xmrp) as (xmdjp__wtc, tbyf__erpa):
        with xmdjp__wtc:
            zfxd__bafvn = c.pyapi.object_getattr_string(obj, '_data')
            nhiq__gaxj.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), zfxd__bafvn).value
            egng__mvn = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), egng__mvn).value
            c.pyapi.decref(zfxd__bafvn)
            c.pyapi.decref(egng__mvn)
            dnjf__spfn = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, mask_arr)
            rquv__ozch = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            vktq__ljn = cgutils.get_or_insert_function(c.builder.module,
                rquv__ozch, name='mask_arr_to_bitmap')
            c.builder.call(vktq__ljn, [sml__zktes.data, dnjf__spfn.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with tbyf__erpa:
            uhsle__qxd = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            rquv__ozch = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            iybe__rqu = cgutils.get_or_insert_function(c.builder.module,
                rquv__ozch, name='int_array_from_sequence')
            c.builder.call(iybe__rqu, [obj, c.builder.bitcast(uhsle__qxd.
                data, lir.IntType(8).as_pointer()), sml__zktes.data])
            nhiq__gaxj.data = uhsle__qxd._getvalue()
    nhiq__gaxj.null_bitmap = sml__zktes._getvalue()
    bmz__cfawt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nhiq__gaxj._getvalue(), is_error=bmz__cfawt)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    nhiq__gaxj = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        nhiq__gaxj.data, c.env_manager)
    duyr__yajd = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, nhiq__gaxj.null_bitmap).data
    mvm__iha = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(mvm__iha)
    pmf__kmqrr = c.context.insert_const_string(c.builder.module, 'numpy')
    unib__jeb = c.pyapi.import_module_noblock(pmf__kmqrr)
    rcp__axy = c.pyapi.object_getattr_string(unib__jeb, 'bool_')
    mask_arr = c.pyapi.call_method(unib__jeb, 'empty', (mvm__iha, rcp__axy))
    evvxs__veovq = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    rnbjv__tche = c.pyapi.object_getattr_string(evvxs__veovq, 'data')
    byk__kbm = c.builder.inttoptr(c.pyapi.long_as_longlong(rnbjv__tche),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as rdn__ambpt:
        i = rdn__ambpt.index
        bvh__nqfjb = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        fivdx__kzs = c.builder.load(cgutils.gep(c.builder, duyr__yajd,
            bvh__nqfjb))
        idvww__ino = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(fivdx__kzs, idvww__ino), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        pui__dzc = cgutils.gep(c.builder, byk__kbm, i)
        c.builder.store(val, pui__dzc)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        nhiq__gaxj.null_bitmap)
    pmf__kmqrr = c.context.insert_const_string(c.builder.module, 'pandas')
    etkjk__pwvfh = c.pyapi.import_module_noblock(pmf__kmqrr)
    abpaa__pnfp = c.pyapi.object_getattr_string(etkjk__pwvfh, 'arrays')
    pjo__cdd = c.pyapi.call_method(abpaa__pnfp, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(etkjk__pwvfh)
    c.pyapi.decref(mvm__iha)
    c.pyapi.decref(unib__jeb)
    c.pyapi.decref(rcp__axy)
    c.pyapi.decref(evvxs__veovq)
    c.pyapi.decref(rnbjv__tche)
    c.pyapi.decref(abpaa__pnfp)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return pjo__cdd


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        cekxs__bke, dxy__lhk = args
        nhiq__gaxj = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        nhiq__gaxj.data = cekxs__bke
        nhiq__gaxj.null_bitmap = dxy__lhk
        context.nrt.incref(builder, signature.args[0], cekxs__bke)
        context.nrt.incref(builder, signature.args[1], dxy__lhk)
        return nhiq__gaxj._getvalue()
    feab__wgc = IntegerArrayType(data.dtype)
    ajgs__qfk = feab__wgc(data, null_bitmap)
    return ajgs__qfk, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    equz__pzj = np.empty(n, pyval.dtype.type)
    qqrd__ryky = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        nhp__ecel = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(qqrd__ryky, i, int(not nhp__ecel))
        if not nhp__ecel:
            equz__pzj[i] = s
    jle__sssix = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), equz__pzj)
    arw__ouh = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), qqrd__ryky)
    return lir.Constant.literal_struct([jle__sssix, arw__ouh])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    pdof__pfkqf = args[0]
    if equiv_set.has_shape(pdof__pfkqf):
        return ArrayAnalysis.AnalyzeResult(shape=pdof__pfkqf, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    pdof__pfkqf = args[0]
    if equiv_set.has_shape(pdof__pfkqf):
        return ArrayAnalysis.AnalyzeResult(shape=pdof__pfkqf, pre=[])
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
    equz__pzj = np.empty(n, dtype)
    udvy__ghtch = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(equz__pzj, udvy__ghtch)


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
            tqwtl__weyh, zhp__kwo = array_getitem_bool_index(A, ind)
            return init_integer_array(tqwtl__weyh, zhp__kwo)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            tqwtl__weyh, zhp__kwo = array_getitem_int_index(A, ind)
            return init_integer_array(tqwtl__weyh, zhp__kwo)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            tqwtl__weyh, zhp__kwo = array_getitem_slice_index(A, ind)
            return init_integer_array(tqwtl__weyh, zhp__kwo)
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
    dltvc__jtgw = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    eyw__uuw = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if eyw__uuw:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(dltvc__jtgw)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or eyw__uuw):
        raise BodoError(dltvc__jtgw)
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
            wrut__lqhg = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                wrut__lqhg[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    wrut__lqhg[i] = np.nan
            return wrut__lqhg
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
    for aphr__lna in numba.np.ufunc_db.get_ufuncs():
        vvc__kmspn = create_op_overload(aphr__lna, aphr__lna.nin)
        overload(aphr__lna, no_unliteral=True)(vvc__kmspn)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        vvc__kmspn = create_op_overload(op, 2)
        overload(op)(vvc__kmspn)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        vvc__kmspn = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(vvc__kmspn)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        vvc__kmspn = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(vvc__kmspn)


_install_unary_ops()


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    uqypc__dhs = dict(skipna=skipna, min_count=min_count)
    nush__uzmfz = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', uqypc__dhs, nush__uzmfz)

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
        idvww__ino = []
        bxqh__nntb = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not bxqh__nntb:
                    data.append(dtype(1))
                    idvww__ino.append(False)
                    bxqh__nntb = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                idvww__ino.append(True)
        tqwtl__weyh = np.array(data)
        n = len(tqwtl__weyh)
        nihc__nlhiz = n + 7 >> 3
        zhp__kwo = np.empty(nihc__nlhiz, np.uint8)
        for rpv__haf in range(n):
            set_bit_to_arr(zhp__kwo, rpv__haf, idvww__ino[rpv__haf])
        return init_integer_array(tqwtl__weyh, zhp__kwo)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    kczja__iwc = numba.core.registry.cpu_target.typing_context
    wgb__urqv = kczja__iwc.resolve_function_type(op, (types.Array(A.dtype, 
        1, 'C'),), {}).return_type
    wgb__urqv = to_nullable_type(wgb__urqv)

    def impl(A):
        n = len(A)
        cyhs__cnxsf = bodo.utils.utils.alloc_type(n, wgb__urqv, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(cyhs__cnxsf, i)
                continue
            cyhs__cnxsf[i] = op(A[i])
        return cyhs__cnxsf
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    efdqt__nzbu = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    rmrva__zdr = isinstance(lhs, (types.Number, types.Boolean))
    ihj__aily = isinstance(rhs, (types.Number, types.Boolean))
    kuhxj__eeua = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    sfsvo__ejtd = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    kczja__iwc = numba.core.registry.cpu_target.typing_context
    wgb__urqv = kczja__iwc.resolve_function_type(op, (kuhxj__eeua,
        sfsvo__ejtd), {}).return_type
    wgb__urqv = to_nullable_type(wgb__urqv)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    ecj__hxtie = 'lhs' if rmrva__zdr else 'lhs[i]'
    rsa__xufmu = 'rhs' if ihj__aily else 'rhs[i]'
    uomie__zlvgs = ('False' if rmrva__zdr else
        'bodo.libs.array_kernels.isna(lhs, i)')
    ympx__ybk = ('False' if ihj__aily else
        'bodo.libs.array_kernels.isna(rhs, i)')
    nuo__agek = 'def impl(lhs, rhs):\n'
    nuo__agek += '  n = len({})\n'.format('lhs' if not rmrva__zdr else 'rhs')
    if efdqt__nzbu:
        nuo__agek += '  out_arr = {}\n'.format('lhs' if not rmrva__zdr else
            'rhs')
    else:
        nuo__agek += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    nuo__agek += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    nuo__agek += '    if ({}\n'.format(uomie__zlvgs)
    nuo__agek += '        or {}):\n'.format(ympx__ybk)
    nuo__agek += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    nuo__agek += '      continue\n'
    nuo__agek += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(op({}, {}))\n'
        .format(ecj__hxtie, rsa__xufmu))
    nuo__agek += '  return out_arr\n'
    kxen__bwaa = {}
    exec(nuo__agek, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        wgb__urqv, 'op': op}, kxen__bwaa)
    impl = kxen__bwaa['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        rmrva__zdr = lhs in [pd_timedelta_type]
        ihj__aily = rhs in [pd_timedelta_type]
        if rmrva__zdr:

            def impl(lhs, rhs):
                n = len(rhs)
                cyhs__cnxsf = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(cyhs__cnxsf, i)
                        continue
                    cyhs__cnxsf[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs, rhs[i]))
                return cyhs__cnxsf
            return impl
        elif ihj__aily:

            def impl(lhs, rhs):
                n = len(lhs)
                cyhs__cnxsf = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(cyhs__cnxsf, i)
                        continue
                    cyhs__cnxsf[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs[i], rhs))
                return cyhs__cnxsf
            return impl
    return impl
