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
        shfuu__jvuy = int(np.log2(self.dtype.bitwidth // 8))
        kwk__wivx = 0 if self.dtype.signed else 4
        idx = shfuu__jvuy + kwk__wivx
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        gwpe__tps = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, gwpe__tps)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    gxp__zaeb = 8 * val.dtype.itemsize
    ygdef__yuoj = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(ygdef__yuoj, gxp__zaeb))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        lcfu__nmtwe = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(lcfu__nmtwe)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    pqb__rkz = c.context.insert_const_string(c.builder.module, 'pandas')
    dei__mciz = c.pyapi.import_module_noblock(pqb__rkz)
    qfva__rdxb = c.pyapi.call_method(dei__mciz, str(typ)[:-2], ())
    c.pyapi.decref(dei__mciz)
    return qfva__rdxb


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    gxp__zaeb = 8 * val.itemsize
    ygdef__yuoj = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(ygdef__yuoj, gxp__zaeb))
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
    polx__lxs = n + 7 >> 3
    vfg__ooi = np.empty(polx__lxs, np.uint8)
    for i in range(n):
        fwxq__lyskj = i // 8
        vfg__ooi[fwxq__lyskj] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            vfg__ooi[fwxq__lyskj]) & kBitmask[i % 8]
    return vfg__ooi


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    dutex__yzn = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(dutex__yzn)
    c.pyapi.decref(dutex__yzn)
    uqto__pky = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    polx__lxs = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64
        ), 7)), lir.Constant(lir.IntType(64), 8))
    lcygb__msf = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [polx__lxs])
    tec__nwj = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()])
    kbbnz__hxo = cgutils.get_or_insert_function(c.builder.module, tec__nwj,
        name='is_pd_int_array')
    nwbbh__ntpv = c.builder.call(kbbnz__hxo, [obj])
    fjt__rhnz = c.builder.icmp_unsigned('!=', nwbbh__ntpv, nwbbh__ntpv.type(0))
    with c.builder.if_else(fjt__rhnz) as (bfo__acis, nonjw__apdsz):
        with bfo__acis:
            hpy__xngsm = c.pyapi.object_getattr_string(obj, '_data')
            uqto__pky.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), hpy__xngsm).value
            ivfu__cki = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), ivfu__cki).value
            c.pyapi.decref(hpy__xngsm)
            c.pyapi.decref(ivfu__cki)
            pnzzo__vfsdt = c.context.make_array(types.Array(types.bool_, 1,
                'C'))(c.context, c.builder, mask_arr)
            tec__nwj = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            kbbnz__hxo = cgutils.get_or_insert_function(c.builder.module,
                tec__nwj, name='mask_arr_to_bitmap')
            c.builder.call(kbbnz__hxo, [lcygb__msf.data, pnzzo__vfsdt.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with nonjw__apdsz:
            anfav__omoc = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            tec__nwj = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            nggbf__lgqtc = cgutils.get_or_insert_function(c.builder.module,
                tec__nwj, name='int_array_from_sequence')
            c.builder.call(nggbf__lgqtc, [obj, c.builder.bitcast(
                anfav__omoc.data, lir.IntType(8).as_pointer()), lcygb__msf.
                data])
            uqto__pky.data = anfav__omoc._getvalue()
    uqto__pky.null_bitmap = lcygb__msf._getvalue()
    bjal__lcx = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(uqto__pky._getvalue(), is_error=bjal__lcx)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    uqto__pky = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        uqto__pky.data, c.env_manager)
    buywn__nvro = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, uqto__pky.null_bitmap).data
    dutex__yzn = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(dutex__yzn)
    pqb__rkz = c.context.insert_const_string(c.builder.module, 'numpy')
    jrtp__tkgn = c.pyapi.import_module_noblock(pqb__rkz)
    ttch__wzlss = c.pyapi.object_getattr_string(jrtp__tkgn, 'bool_')
    mask_arr = c.pyapi.call_method(jrtp__tkgn, 'empty', (dutex__yzn,
        ttch__wzlss))
    yvilf__scmyr = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    frv__ito = c.pyapi.object_getattr_string(yvilf__scmyr, 'data')
    hys__ioya = c.builder.inttoptr(c.pyapi.long_as_longlong(frv__ito), lir.
        IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as zfvew__lnyyl:
        i = zfvew__lnyyl.index
        tido__djx = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        hcgw__pgl = c.builder.load(cgutils.gep(c.builder, buywn__nvro,
            tido__djx))
        ysaf__mwn = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(hcgw__pgl, ysaf__mwn), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        zwljq__anl = cgutils.gep(c.builder, hys__ioya, i)
        c.builder.store(val, zwljq__anl)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        uqto__pky.null_bitmap)
    pqb__rkz = c.context.insert_const_string(c.builder.module, 'pandas')
    dei__mciz = c.pyapi.import_module_noblock(pqb__rkz)
    szqc__pjqp = c.pyapi.object_getattr_string(dei__mciz, 'arrays')
    qfva__rdxb = c.pyapi.call_method(szqc__pjqp, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(dei__mciz)
    c.pyapi.decref(dutex__yzn)
    c.pyapi.decref(jrtp__tkgn)
    c.pyapi.decref(ttch__wzlss)
    c.pyapi.decref(yvilf__scmyr)
    c.pyapi.decref(frv__ito)
    c.pyapi.decref(szqc__pjqp)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return qfva__rdxb


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        iev__lscew, coajt__vktks = args
        uqto__pky = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        uqto__pky.data = iev__lscew
        uqto__pky.null_bitmap = coajt__vktks
        context.nrt.incref(builder, signature.args[0], iev__lscew)
        context.nrt.incref(builder, signature.args[1], coajt__vktks)
        return uqto__pky._getvalue()
    qcoai__lys = IntegerArrayType(data.dtype)
    dmv__dvb = qcoai__lys(data, null_bitmap)
    return dmv__dvb, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    kacd__opm = np.empty(n, pyval.dtype.type)
    dev__gaosj = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        lps__ael = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(dev__gaosj, i, int(not lps__ael))
        if not lps__ael:
            kacd__opm[i] = s
    bufzk__houeg = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), kacd__opm)
    ckzip__slljc = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), dev__gaosj)
    return lir.Constant.literal_struct([bufzk__houeg, ckzip__slljc])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    aqgx__poxxi = args[0]
    if equiv_set.has_shape(aqgx__poxxi):
        return ArrayAnalysis.AnalyzeResult(shape=aqgx__poxxi, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    aqgx__poxxi = args[0]
    if equiv_set.has_shape(aqgx__poxxi):
        return ArrayAnalysis.AnalyzeResult(shape=aqgx__poxxi, pre=[])
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
    kacd__opm = np.empty(n, dtype)
    brid__blzme = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(kacd__opm, brid__blzme)


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
            ymw__oag, vxo__pgix = array_getitem_bool_index(A, ind)
            return init_integer_array(ymw__oag, vxo__pgix)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ymw__oag, vxo__pgix = array_getitem_int_index(A, ind)
            return init_integer_array(ymw__oag, vxo__pgix)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            ymw__oag, vxo__pgix = array_getitem_slice_index(A, ind)
            return init_integer_array(ymw__oag, vxo__pgix)
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
    ajuc__vcjn = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    wkyp__gmefy = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if wkyp__gmefy:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(ajuc__vcjn)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or wkyp__gmefy):
        raise BodoError(ajuc__vcjn)
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
            eohzb__bbe = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                eohzb__bbe[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    eohzb__bbe[i] = np.nan
            return eohzb__bbe
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
    for hzd__hsj in numba.np.ufunc_db.get_ufuncs():
        wncy__qfqo = create_op_overload(hzd__hsj, hzd__hsj.nin)
        overload(hzd__hsj, no_unliteral=True)(wncy__qfqo)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        wncy__qfqo = create_op_overload(op, 2)
        overload(op)(wncy__qfqo)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        wncy__qfqo = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(wncy__qfqo)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        wncy__qfqo = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(wncy__qfqo)


_install_unary_ops()


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    xlfwh__dqx = dict(skipna=skipna, min_count=min_count)
    lbncv__yhi = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', xlfwh__dqx, lbncv__yhi)

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
        ysaf__mwn = []
        sbqit__wwsb = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not sbqit__wwsb:
                    data.append(dtype(1))
                    ysaf__mwn.append(False)
                    sbqit__wwsb = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                ysaf__mwn.append(True)
        ymw__oag = np.array(data)
        n = len(ymw__oag)
        polx__lxs = n + 7 >> 3
        vxo__pgix = np.empty(polx__lxs, np.uint8)
        for scyea__wrmqo in range(n):
            set_bit_to_arr(vxo__pgix, scyea__wrmqo, ysaf__mwn[scyea__wrmqo])
        return init_integer_array(ymw__oag, vxo__pgix)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    rodcb__tex = numba.core.registry.cpu_target.typing_context
    hgm__vtokj = rodcb__tex.resolve_function_type(op, (types.Array(A.dtype,
        1, 'C'),), {}).return_type
    hgm__vtokj = to_nullable_type(hgm__vtokj)

    def impl(A):
        n = len(A)
        kkmj__xvaw = bodo.utils.utils.alloc_type(n, hgm__vtokj, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(kkmj__xvaw, i)
                continue
            kkmj__xvaw[i] = op(A[i])
        return kkmj__xvaw
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    ors__kdef = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    efd__tkf = isinstance(lhs, (types.Number, types.Boolean))
    zrgrm__agwb = isinstance(rhs, (types.Number, types.Boolean))
    lncob__gya = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    ozjc__hvd = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    rodcb__tex = numba.core.registry.cpu_target.typing_context
    hgm__vtokj = rodcb__tex.resolve_function_type(op, (lncob__gya,
        ozjc__hvd), {}).return_type
    hgm__vtokj = to_nullable_type(hgm__vtokj)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    cbvzx__ukm = 'lhs' if efd__tkf else 'lhs[i]'
    syybv__akp = 'rhs' if zrgrm__agwb else 'rhs[i]'
    abk__gltnk = ('False' if efd__tkf else
        'bodo.libs.array_kernels.isna(lhs, i)')
    pvvrz__dxy = ('False' if zrgrm__agwb else
        'bodo.libs.array_kernels.isna(rhs, i)')
    fuqsg__vmwe = 'def impl(lhs, rhs):\n'
    fuqsg__vmwe += '  n = len({})\n'.format('lhs' if not efd__tkf else 'rhs')
    if ors__kdef:
        fuqsg__vmwe += '  out_arr = {}\n'.format('lhs' if not efd__tkf else
            'rhs')
    else:
        fuqsg__vmwe += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    fuqsg__vmwe += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    fuqsg__vmwe += '    if ({}\n'.format(abk__gltnk)
    fuqsg__vmwe += '        or {}):\n'.format(pvvrz__dxy)
    fuqsg__vmwe += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    fuqsg__vmwe += '      continue\n'
    fuqsg__vmwe += (
        """    out_arr[i] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(op({}, {}))
"""
        .format(cbvzx__ukm, syybv__akp))
    fuqsg__vmwe += '  return out_arr\n'
    ldz__kjzv = {}
    exec(fuqsg__vmwe, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        hgm__vtokj, 'op': op}, ldz__kjzv)
    impl = ldz__kjzv['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        efd__tkf = lhs in [pd_timedelta_type]
        zrgrm__agwb = rhs in [pd_timedelta_type]
        if efd__tkf:

            def impl(lhs, rhs):
                n = len(rhs)
                kkmj__xvaw = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(kkmj__xvaw, i)
                        continue
                    kkmj__xvaw[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs, rhs[i]))
                return kkmj__xvaw
            return impl
        elif zrgrm__agwb:

            def impl(lhs, rhs):
                n = len(lhs)
                kkmj__xvaw = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(kkmj__xvaw, i)
                        continue
                    kkmj__xvaw[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs[i], rhs))
                return kkmj__xvaw
            return impl
    return impl
