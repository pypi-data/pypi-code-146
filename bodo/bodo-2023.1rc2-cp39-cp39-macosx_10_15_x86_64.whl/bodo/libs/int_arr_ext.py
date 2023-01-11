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
        diejf__nqdql = int(np.log2(self.dtype.bitwidth // 8))
        dvyz__qajb = 0 if self.dtype.signed else 4
        idx = diejf__nqdql + dvyz__qajb
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        rztoy__laf = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, rztoy__laf)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    gbt__iogp = 8 * val.dtype.itemsize
    jrum__mdgre = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(jrum__mdgre, gbt__iogp))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        ibw__zzlpr = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(ibw__zzlpr)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    lem__bnrp = c.context.insert_const_string(c.builder.module, 'pandas')
    euvpg__rya = c.pyapi.import_module_noblock(lem__bnrp)
    ixf__zdumw = c.pyapi.call_method(euvpg__rya, str(typ)[:-2], ())
    c.pyapi.decref(euvpg__rya)
    return ixf__zdumw


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    gbt__iogp = 8 * val.itemsize
    jrum__mdgre = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(jrum__mdgre, gbt__iogp))
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
    lpigd__wbq = n + 7 >> 3
    vrhtf__qxsr = np.empty(lpigd__wbq, np.uint8)
    for i in range(n):
        yepa__bly = i // 8
        vrhtf__qxsr[yepa__bly] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            vrhtf__qxsr[yepa__bly]) & kBitmask[i % 8]
    return vrhtf__qxsr


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    ifw__iggq = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(ifw__iggq)
    c.pyapi.decref(ifw__iggq)
    dfdry__dgvqv = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lpigd__wbq = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    cokuo__bsw = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [lpigd__wbq])
    zuou__pyzvk = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    bboeb__omkls = cgutils.get_or_insert_function(c.builder.module,
        zuou__pyzvk, name='is_pd_int_array')
    bqbk__cfrbb = c.builder.call(bboeb__omkls, [obj])
    xqbzh__xivvz = c.builder.icmp_unsigned('!=', bqbk__cfrbb, bqbk__cfrbb.
        type(0))
    with c.builder.if_else(xqbzh__xivvz) as (rrlwt__gkzi, mqf__loh):
        with rrlwt__gkzi:
            vvy__aqav = c.pyapi.object_getattr_string(obj, '_data')
            dfdry__dgvqv.data = c.pyapi.to_native_value(types.Array(typ.
                dtype, 1, 'C'), vvy__aqav).value
            lnmk__srudw = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), lnmk__srudw).value
            c.pyapi.decref(vvy__aqav)
            c.pyapi.decref(lnmk__srudw)
            szde__fpq = c.context.make_array(types.Array(types.bool_, 1, 'C'))(
                c.context, c.builder, mask_arr)
            zuou__pyzvk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            bboeb__omkls = cgutils.get_or_insert_function(c.builder.module,
                zuou__pyzvk, name='mask_arr_to_bitmap')
            c.builder.call(bboeb__omkls, [cokuo__bsw.data, szde__fpq.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with mqf__loh:
            lbcw__egs = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            zuou__pyzvk = lir.FunctionType(lir.IntType(32), [lir.IntType(8)
                .as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            sulbz__ctypk = cgutils.get_or_insert_function(c.builder.module,
                zuou__pyzvk, name='int_array_from_sequence')
            c.builder.call(sulbz__ctypk, [obj, c.builder.bitcast(lbcw__egs.
                data, lir.IntType(8).as_pointer()), cokuo__bsw.data])
            dfdry__dgvqv.data = lbcw__egs._getvalue()
    dfdry__dgvqv.null_bitmap = cokuo__bsw._getvalue()
    xdtm__pmj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(dfdry__dgvqv._getvalue(), is_error=xdtm__pmj)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    dfdry__dgvqv = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        dfdry__dgvqv.data, c.env_manager)
    tox__jti = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, dfdry__dgvqv.null_bitmap).data
    ifw__iggq = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(ifw__iggq)
    lem__bnrp = c.context.insert_const_string(c.builder.module, 'numpy')
    sbn__byv = c.pyapi.import_module_noblock(lem__bnrp)
    vmve__lxcv = c.pyapi.object_getattr_string(sbn__byv, 'bool_')
    mask_arr = c.pyapi.call_method(sbn__byv, 'empty', (ifw__iggq, vmve__lxcv))
    bqyxc__jrezg = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    jqo__mpd = c.pyapi.object_getattr_string(bqyxc__jrezg, 'data')
    yxb__xog = c.builder.inttoptr(c.pyapi.long_as_longlong(jqo__mpd), lir.
        IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as ccc__lrawf:
        i = ccc__lrawf.index
        dah__xcois = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        yvdi__wovv = c.builder.load(cgutils.gep(c.builder, tox__jti,
            dah__xcois))
        toe__gmss = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(yvdi__wovv, toe__gmss), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        shevj__mqze = cgutils.gep(c.builder, yxb__xog, i)
        c.builder.store(val, shevj__mqze)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        dfdry__dgvqv.null_bitmap)
    lem__bnrp = c.context.insert_const_string(c.builder.module, 'pandas')
    euvpg__rya = c.pyapi.import_module_noblock(lem__bnrp)
    ojhba__lfey = c.pyapi.object_getattr_string(euvpg__rya, 'arrays')
    ixf__zdumw = c.pyapi.call_method(ojhba__lfey, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(euvpg__rya)
    c.pyapi.decref(ifw__iggq)
    c.pyapi.decref(sbn__byv)
    c.pyapi.decref(vmve__lxcv)
    c.pyapi.decref(bqyxc__jrezg)
    c.pyapi.decref(jqo__mpd)
    c.pyapi.decref(ojhba__lfey)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return ixf__zdumw


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        cacgk__iqqjh, rrrdt__leup = args
        dfdry__dgvqv = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        dfdry__dgvqv.data = cacgk__iqqjh
        dfdry__dgvqv.null_bitmap = rrrdt__leup
        context.nrt.incref(builder, signature.args[0], cacgk__iqqjh)
        context.nrt.incref(builder, signature.args[1], rrrdt__leup)
        return dfdry__dgvqv._getvalue()
    aaf__nnx = IntegerArrayType(data.dtype)
    wkran__wlgjd = aaf__nnx(data, null_bitmap)
    return wkran__wlgjd, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    hgs__bbgi = np.empty(n, pyval.dtype.type)
    wcpv__jrgl = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        bdprg__xuzrh = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(wcpv__jrgl, i, int(not
            bdprg__xuzrh))
        if not bdprg__xuzrh:
            hgs__bbgi[i] = s
    klxn__jcqsh = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), hgs__bbgi)
    amt__uhs = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), wcpv__jrgl)
    return lir.Constant.literal_struct([klxn__jcqsh, amt__uhs])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    whpb__nbi = args[0]
    if equiv_set.has_shape(whpb__nbi):
        return ArrayAnalysis.AnalyzeResult(shape=whpb__nbi, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    whpb__nbi = args[0]
    if equiv_set.has_shape(whpb__nbi):
        return ArrayAnalysis.AnalyzeResult(shape=whpb__nbi, pre=[])
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
    hgs__bbgi = np.empty(n, dtype)
    djlf__zes = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(hgs__bbgi, djlf__zes)


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
            wng__yle, eih__ksmq = array_getitem_bool_index(A, ind)
            return init_integer_array(wng__yle, eih__ksmq)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            wng__yle, eih__ksmq = array_getitem_int_index(A, ind)
            return init_integer_array(wng__yle, eih__ksmq)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            wng__yle, eih__ksmq = array_getitem_slice_index(A, ind)
            return init_integer_array(wng__yle, eih__ksmq)
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
    cemk__pmmw = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    jszsk__ujtd = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if jszsk__ujtd:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(cemk__pmmw)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or jszsk__ujtd):
        raise BodoError(cemk__pmmw)
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
            krlp__atyx = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                krlp__atyx[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    krlp__atyx[i] = np.nan
            return krlp__atyx
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
    for gldo__piqf in numba.np.ufunc_db.get_ufuncs():
        jfgqf__gafln = create_op_overload(gldo__piqf, gldo__piqf.nin)
        overload(gldo__piqf, no_unliteral=True)(jfgqf__gafln)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        jfgqf__gafln = create_op_overload(op, 2)
        overload(op)(jfgqf__gafln)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        jfgqf__gafln = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(jfgqf__gafln)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        jfgqf__gafln = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(jfgqf__gafln)


_install_unary_ops()


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    flij__ztii = dict(skipna=skipna, min_count=min_count)
    njuuu__uyiji = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', flij__ztii, njuuu__uyiji)

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
        toe__gmss = []
        ozjbm__vkfr = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not ozjbm__vkfr:
                    data.append(dtype(1))
                    toe__gmss.append(False)
                    ozjbm__vkfr = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                toe__gmss.append(True)
        wng__yle = np.array(data)
        n = len(wng__yle)
        lpigd__wbq = n + 7 >> 3
        eih__ksmq = np.empty(lpigd__wbq, np.uint8)
        for ciwz__ipzi in range(n):
            set_bit_to_arr(eih__ksmq, ciwz__ipzi, toe__gmss[ciwz__ipzi])
        return init_integer_array(wng__yle, eih__ksmq)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    crh__fyc = numba.core.registry.cpu_target.typing_context
    sup__rcfh = crh__fyc.resolve_function_type(op, (types.Array(A.dtype, 1,
        'C'),), {}).return_type
    sup__rcfh = to_nullable_type(sup__rcfh)

    def impl(A):
        n = len(A)
        eyx__mby = bodo.utils.utils.alloc_type(n, sup__rcfh, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(eyx__mby, i)
                continue
            eyx__mby[i] = op(A[i])
        return eyx__mby
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    ntvse__sge = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    jasp__kojqg = isinstance(lhs, (types.Number, types.Boolean))
    bevfq__lty = isinstance(rhs, (types.Number, types.Boolean))
    utd__pwtby = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    cdnf__lew = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    crh__fyc = numba.core.registry.cpu_target.typing_context
    sup__rcfh = crh__fyc.resolve_function_type(op, (utd__pwtby, cdnf__lew), {}
        ).return_type
    sup__rcfh = to_nullable_type(sup__rcfh)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    buic__tkn = 'lhs' if jasp__kojqg else 'lhs[i]'
    cbvll__btdp = 'rhs' if bevfq__lty else 'rhs[i]'
    asxv__jej = ('False' if jasp__kojqg else
        'bodo.libs.array_kernels.isna(lhs, i)')
    ypnqj__dtp = ('False' if bevfq__lty else
        'bodo.libs.array_kernels.isna(rhs, i)')
    oct__jkt = 'def impl(lhs, rhs):\n'
    oct__jkt += '  n = len({})\n'.format('lhs' if not jasp__kojqg else 'rhs')
    if ntvse__sge:
        oct__jkt += '  out_arr = {}\n'.format('lhs' if not jasp__kojqg else
            'rhs')
    else:
        oct__jkt += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    oct__jkt += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    oct__jkt += '    if ({}\n'.format(asxv__jej)
    oct__jkt += '        or {}):\n'.format(ypnqj__dtp)
    oct__jkt += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    oct__jkt += '      continue\n'
    oct__jkt += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(op({}, {}))\n'
        .format(buic__tkn, cbvll__btdp))
    oct__jkt += '  return out_arr\n'
    pszvo__dkl = {}
    exec(oct__jkt, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        sup__rcfh, 'op': op}, pszvo__dkl)
    impl = pszvo__dkl['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        jasp__kojqg = lhs in [pd_timedelta_type]
        bevfq__lty = rhs in [pd_timedelta_type]
        if jasp__kojqg:

            def impl(lhs, rhs):
                n = len(rhs)
                eyx__mby = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(eyx__mby, i)
                        continue
                    eyx__mby[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs, rhs[i]))
                return eyx__mby
            return impl
        elif bevfq__lty:

            def impl(lhs, rhs):
                n = len(lhs)
                eyx__mby = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(eyx__mby, i)
                        continue
                    eyx__mby[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs[i], rhs))
                return eyx__mby
            return impl
    return impl
