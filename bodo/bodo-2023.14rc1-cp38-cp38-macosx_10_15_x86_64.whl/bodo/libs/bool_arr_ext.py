"""Nullable boolean array that stores data in Numpy format (1 byte per value)
but nulls are stored in bit arrays (1 bit per value) similar to Arrow's nulls.
Pandas converts boolean array to object when NAs are introduced.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import is_list_like_index_type
ll.add_symbol('is_bool_array', hstr_ext.is_bool_array)
ll.add_symbol('is_pd_boolean_array', hstr_ext.is_pd_boolean_array)
ll.add_symbol('unbox_bool_array_obj', hstr_ext.unbox_bool_array_obj)
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_overload_false, is_overload_true, parse_dtype, raise_bodo_error


class BooleanArrayType(types.ArrayCompatible):

    def __init__(self):
        super(BooleanArrayType, self).__init__(name='BooleanArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.bool_

    def copy(self):
        return BooleanArrayType()


boolean_array = BooleanArrayType()


@typeof_impl.register(pd.arrays.BooleanArray)
def typeof_boolean_array(val, c):
    return boolean_array


data_type = types.Array(types.bool_, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(BooleanArrayType)
class BooleanArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bvl__lnck = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, bvl__lnck)


make_attribute_wrapper(BooleanArrayType, 'data', '_data')
make_attribute_wrapper(BooleanArrayType, 'null_bitmap', '_null_bitmap')


class BooleanDtype(types.Number):

    def __init__(self):
        self.dtype = types.bool_
        super(BooleanDtype, self).__init__('BooleanDtype')


boolean_dtype = BooleanDtype()
register_model(BooleanDtype)(models.OpaqueModel)


@box(BooleanDtype)
def box_boolean_dtype(typ, val, c):
    mrzxu__nqwn = c.context.insert_const_string(c.builder.module, 'pandas')
    datzh__dkv = c.pyapi.import_module_noblock(mrzxu__nqwn)
    mecq__zqzgj = c.pyapi.call_method(datzh__dkv, 'BooleanDtype', ())
    c.pyapi.decref(datzh__dkv)
    return mecq__zqzgj


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    geyik__btu = n + 7 >> 3
    return np.full(geyik__btu, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    gqaje__lumzs = c.context.typing_context.resolve_value_type(func)
    ymr__yuhx = gqaje__lumzs.get_call_type(c.context.typing_context,
        arg_typs, {})
    asdot__gwfqq = c.context.get_function(gqaje__lumzs, ymr__yuhx)
    jkebc__shjb = c.context.call_conv.get_function_type(ymr__yuhx.
        return_type, ymr__yuhx.args)
    nfpj__rkkei = c.builder.module
    cbnyo__czzmq = lir.Function(nfpj__rkkei, jkebc__shjb, name=nfpj__rkkei.
        get_unique_name('.func_conv'))
    cbnyo__czzmq.linkage = 'internal'
    oan__pyo = lir.IRBuilder(cbnyo__czzmq.append_basic_block())
    wtvno__adey = c.context.call_conv.decode_arguments(oan__pyo, ymr__yuhx.
        args, cbnyo__czzmq)
    jds__asp = asdot__gwfqq(oan__pyo, wtvno__adey)
    c.context.call_conv.return_value(oan__pyo, jds__asp)
    eofam__uck, dagfd__ujme = c.context.call_conv.call_function(c.builder,
        cbnyo__czzmq, ymr__yuhx.return_type, ymr__yuhx.args, args)
    return dagfd__ujme


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    gdjgq__pnzw = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(gdjgq__pnzw)
    c.pyapi.decref(gdjgq__pnzw)
    jkebc__shjb = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    tsvme__inj = cgutils.get_or_insert_function(c.builder.module,
        jkebc__shjb, name='is_bool_array')
    jkebc__shjb = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    cbnyo__czzmq = cgutils.get_or_insert_function(c.builder.module,
        jkebc__shjb, name='is_pd_boolean_array')
    tjr__bhqsc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mymun__vyep = c.builder.call(cbnyo__czzmq, [obj])
    xbdt__ifx = c.builder.icmp_unsigned('!=', mymun__vyep, mymun__vyep.type(0))
    with c.builder.if_else(xbdt__ifx) as (xlarl__vkzz, szujc__tpchu):
        with xlarl__vkzz:
            ypgww__gag = c.pyapi.object_getattr_string(obj, '_data')
            tjr__bhqsc.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), ypgww__gag).value
            cgv__mml = c.pyapi.object_getattr_string(obj, '_mask')
            msnfp__eeyrb = c.pyapi.to_native_value(types.Array(types.bool_,
                1, 'C'), cgv__mml).value
            geyik__btu = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            nja__agiyi = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, msnfp__eeyrb)
            bdn__sef = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
                types.Array(types.uint8, 1, 'C'), [geyik__btu])
            jkebc__shjb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            cbnyo__czzmq = cgutils.get_or_insert_function(c.builder.module,
                jkebc__shjb, name='mask_arr_to_bitmap')
            c.builder.call(cbnyo__czzmq, [bdn__sef.data, nja__agiyi.data, n])
            tjr__bhqsc.null_bitmap = bdn__sef._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), msnfp__eeyrb)
            c.pyapi.decref(ypgww__gag)
            c.pyapi.decref(cgv__mml)
        with szujc__tpchu:
            rqswg__yosx = c.builder.call(tsvme__inj, [obj])
            sujs__tepa = c.builder.icmp_unsigned('!=', rqswg__yosx,
                rqswg__yosx.type(0))
            with c.builder.if_else(sujs__tepa) as (nlikr__lzzc, iqgjl__nqoy):
                with nlikr__lzzc:
                    tjr__bhqsc.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    tjr__bhqsc.null_bitmap = call_func_in_unbox(gen_full_bitmap
                        , (n,), (types.int64,), c)
                with iqgjl__nqoy:
                    tjr__bhqsc.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    geyik__btu = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    tjr__bhqsc.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [geyik__btu])._getvalue()
                    sdaxb__ymfpp = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, tjr__bhqsc.data
                        ).data
                    sewty__gta = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, tjr__bhqsc.
                        null_bitmap).data
                    jkebc__shjb = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    cbnyo__czzmq = cgutils.get_or_insert_function(c.builder
                        .module, jkebc__shjb, name='unbox_bool_array_obj')
                    c.builder.call(cbnyo__czzmq, [obj, sdaxb__ymfpp,
                        sewty__gta, n])
    return NativeValue(tjr__bhqsc._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    tjr__bhqsc = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        tjr__bhqsc.data, c.env_manager)
    vqd__bgsf = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, tjr__bhqsc.null_bitmap).data
    gdjgq__pnzw = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(gdjgq__pnzw)
    mrzxu__nqwn = c.context.insert_const_string(c.builder.module, 'numpy')
    qkch__vkqb = c.pyapi.import_module_noblock(mrzxu__nqwn)
    kge__wwgd = c.pyapi.object_getattr_string(qkch__vkqb, 'bool_')
    msnfp__eeyrb = c.pyapi.call_method(qkch__vkqb, 'empty', (gdjgq__pnzw,
        kge__wwgd))
    mjbho__xbgh = c.pyapi.object_getattr_string(msnfp__eeyrb, 'ctypes')
    tfz__oml = c.pyapi.object_getattr_string(mjbho__xbgh, 'data')
    juvsk__igee = c.builder.inttoptr(c.pyapi.long_as_longlong(tfz__oml),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as byyeq__rtcj:
        pfnv__anv = byyeq__rtcj.index
        jtz__qcgo = c.builder.lshr(pfnv__anv, lir.Constant(lir.IntType(64), 3))
        gse__kwuy = c.builder.load(cgutils.gep(c.builder, vqd__bgsf, jtz__qcgo)
            )
        hbkp__jjk = c.builder.trunc(c.builder.and_(pfnv__anv, lir.Constant(
            lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(gse__kwuy, hbkp__jjk), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        pfb__oxi = cgutils.gep(c.builder, juvsk__igee, pfnv__anv)
        c.builder.store(val, pfb__oxi)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        tjr__bhqsc.null_bitmap)
    mrzxu__nqwn = c.context.insert_const_string(c.builder.module, 'pandas')
    datzh__dkv = c.pyapi.import_module_noblock(mrzxu__nqwn)
    nos__zdyr = c.pyapi.object_getattr_string(datzh__dkv, 'arrays')
    mecq__zqzgj = c.pyapi.call_method(nos__zdyr, 'BooleanArray', (data,
        msnfp__eeyrb))
    c.pyapi.decref(datzh__dkv)
    c.pyapi.decref(gdjgq__pnzw)
    c.pyapi.decref(qkch__vkqb)
    c.pyapi.decref(kge__wwgd)
    c.pyapi.decref(mjbho__xbgh)
    c.pyapi.decref(tfz__oml)
    c.pyapi.decref(nos__zdyr)
    c.pyapi.decref(data)
    c.pyapi.decref(msnfp__eeyrb)
    return mecq__zqzgj


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    uibx__mowa = np.empty(n, np.bool_)
    yqir__yyks = np.empty(n + 7 >> 3, np.uint8)
    for pfnv__anv, s in enumerate(pyval):
        quac__meh = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(yqir__yyks, pfnv__anv, int(not
            quac__meh))
        if not quac__meh:
            uibx__mowa[pfnv__anv] = s
    vcqp__iws = context.get_constant_generic(builder, data_type, uibx__mowa)
    tdm__nbtx = context.get_constant_generic(builder, nulls_type, yqir__yyks)
    return lir.Constant.literal_struct([vcqp__iws, tdm__nbtx])


def lower_init_bool_array(context, builder, signature, args):
    dii__wca, odn__qigsx = args
    tjr__bhqsc = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    tjr__bhqsc.data = dii__wca
    tjr__bhqsc.null_bitmap = odn__qigsx
    context.nrt.incref(builder, signature.args[0], dii__wca)
    context.nrt.incref(builder, signature.args[1], odn__qigsx)
    return tjr__bhqsc._getvalue()


@intrinsic
def init_bool_array(typingctx, data, null_bitmap=None):
    assert data == types.Array(types.bool_, 1, 'C')
    assert null_bitmap == types.Array(types.uint8, 1, 'C')
    sig = boolean_array(data, null_bitmap)
    return sig, lower_init_bool_array


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_bool_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    odqys__ndiv = args[0]
    if equiv_set.has_shape(odqys__ndiv):
        return ArrayAnalysis.AnalyzeResult(shape=odqys__ndiv, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    odqys__ndiv = args[0]
    if equiv_set.has_shape(odqys__ndiv):
        return ArrayAnalysis.AnalyzeResult(shape=odqys__ndiv, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_init_bool_array = (
    init_bool_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_bool_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_bool_array',
    'bodo.libs.bool_arr_ext'] = alias_ext_init_bool_array
numba.core.ir_utils.alias_func_extensions['get_bool_arr_data',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_bool_arr_bitmap',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_bool_array(n):
    uibx__mowa = np.empty(n, dtype=np.bool_)
    mbmyi__ynlw = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(uibx__mowa, mbmyi__ynlw)


def alloc_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_alloc_bool_array = (
    alloc_bool_array_equiv)


@overload(operator.getitem, no_unliteral=True)
def bool_arr_getitem(A, ind):
    if A != boolean_array:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: A._data[ind]
    if ind != boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            ovwnv__jlk, vapg__ezse = array_getitem_bool_index(A, ind)
            return init_bool_array(ovwnv__jlk, vapg__ezse)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ovwnv__jlk, vapg__ezse = array_getitem_int_index(A, ind)
            return init_bool_array(ovwnv__jlk, vapg__ezse)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            ovwnv__jlk, vapg__ezse = array_getitem_slice_index(A, ind)
            return init_bool_array(ovwnv__jlk, vapg__ezse)
        return impl_slice
    if ind != boolean_array:
        raise BodoError(
            f'getitem for BooleanArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    gqn__jwnh = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(gqn__jwnh)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(gqn__jwnh)
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
        f'setitem for BooleanArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_bool_arr_len(A):
    if A == boolean_array:
        return lambda A: len(A._data)


@overload_attribute(BooleanArrayType, 'size')
def overload_bool_arr_size(A):
    return lambda A: len(A._data)


@overload_attribute(BooleanArrayType, 'shape')
def overload_bool_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(BooleanArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: pd.BooleanDtype()


@overload_attribute(BooleanArrayType, 'ndim')
def overload_bool_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BooleanArrayType, 'nbytes')
def bool_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(BooleanArrayType, 'copy', no_unliteral=True)
def overload_bool_arr_copy(A):
    return lambda A: bodo.libs.bool_arr_ext.init_bool_array(bodo.libs.
        bool_arr_ext.get_bool_arr_data(A).copy(), bodo.libs.bool_arr_ext.
        get_bool_arr_bitmap(A).copy())


@overload_method(BooleanArrayType, 'sum', no_unliteral=True, inline='always')
def overload_bool_sum(A):

    def impl(A):
        numba.parfors.parfor.init_prange()
        s = 0
        for pfnv__anv in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, pfnv__anv):
                val = A[pfnv__anv]
            s += val
        return s
    return impl


@overload_method(BooleanArrayType, 'astype', no_unliteral=True)
def overload_bool_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "BooleanArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if dtype == types.bool_:
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
    nb_dtype = parse_dtype(dtype, 'BooleanArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
            n = len(data)
            qca__uly = np.empty(n, nb_dtype)
            for pfnv__anv in numba.parfors.parfor.internal_prange(n):
                qca__uly[pfnv__anv] = data[pfnv__anv]
                if bodo.libs.array_kernels.isna(A, pfnv__anv):
                    qca__uly[pfnv__anv] = np.nan
            return qca__uly
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload_method(BooleanArrayType, 'fillna', no_unliteral=True)
def overload_bool_fillna(A, value=None, method=None, limit=None):

    def impl(A, value=None, method=None, limit=None):
        data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
        n = len(data)
        qca__uly = np.empty(n, dtype=np.bool_)
        for pfnv__anv in numba.parfors.parfor.internal_prange(n):
            qca__uly[pfnv__anv] = data[pfnv__anv]
            if bodo.libs.array_kernels.isna(A, pfnv__anv):
                qca__uly[pfnv__anv] = value
        return qca__uly
    return impl


@overload(str, no_unliteral=True)
def overload_str_bool(val):
    if val == types.bool_:

        def impl(val):
            if val:
                return 'True'
            return 'False'
        return impl


ufunc_aliases = {'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    hikrv__dmsb = op.__name__
    hikrv__dmsb = ufunc_aliases.get(hikrv__dmsb, hikrv__dmsb)
    if n_inputs == 1:

        def overload_bool_arr_op_nin_1(A):
            if isinstance(A, BooleanArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_unary_impl(op,
                    A)
        return overload_bool_arr_op_nin_1
    elif n_inputs == 2:

        def overload_bool_arr_op_nin_2(lhs, rhs):
            if lhs == boolean_array or rhs == boolean_array:
                return bodo.libs.int_arr_ext.get_nullable_array_binary_impl(op,
                    lhs, rhs)
        return overload_bool_arr_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for smtx__fouyj in numba.np.ufunc_db.get_ufuncs():
        okn__uwmih = create_op_overload(smtx__fouyj, smtx__fouyj.nin)
        overload(smtx__fouyj, no_unliteral=True)(okn__uwmih)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        okn__uwmih = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(okn__uwmih)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        okn__uwmih = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(okn__uwmih)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        okn__uwmih = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(okn__uwmih)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        hbkp__jjk = []
        dcdil__bpb = False
        zrmw__tgmj = False
        nxy__nzj = False
        for pfnv__anv in range(len(A)):
            if bodo.libs.array_kernels.isna(A, pfnv__anv):
                if not dcdil__bpb:
                    data.append(False)
                    hbkp__jjk.append(False)
                    dcdil__bpb = True
                continue
            val = A[pfnv__anv]
            if val and not zrmw__tgmj:
                data.append(True)
                hbkp__jjk.append(True)
                zrmw__tgmj = True
            if not val and not nxy__nzj:
                data.append(False)
                hbkp__jjk.append(True)
                nxy__nzj = True
            if dcdil__bpb and zrmw__tgmj and nxy__nzj:
                break
        ovwnv__jlk = np.array(data)
        n = len(ovwnv__jlk)
        geyik__btu = 1
        vapg__ezse = np.empty(geyik__btu, np.uint8)
        for lmjg__idmv in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(vapg__ezse, lmjg__idmv,
                hbkp__jjk[lmjg__idmv])
        return init_bool_array(ovwnv__jlk, vapg__ezse)
    return impl_bool_arr


@overload(operator.getitem, no_unliteral=True)
def bool_arr_ind_getitem(A, ind):
    if ind == boolean_array and (isinstance(A, (types.Array, bodo.libs.
        int_arr_ext.IntegerArrayType, bodo.libs.float_arr_ext.
        FloatingArrayType, bodo.libs.struct_arr_ext.StructArrayType, bodo.
        libs.array_item_arr_ext.ArrayItemArrayType, bodo.libs.map_arr_ext.
        MapArrayType, bodo.libs.tuple_arr_ext.TupleArrayType, bodo.
        CategoricalArrayType, bodo.TimeArrayType, bodo.DecimalArrayType,
        bodo.DatetimeArrayType)) or A in (string_array_type, bodo.hiframes.
        split_impl.string_array_split_view_type, boolean_array, bodo.
        datetime_date_array_type, bodo.datetime_timedelta_array_type, bodo.
        binary_array_type)):

        def impl(A, ind):
            clacj__iotnm = (bodo.utils.conversion.
                nullable_bool_to_bool_na_false(ind))
            return A[clacj__iotnm]
        return impl


@lower_cast(types.Array(types.bool_, 1, 'C'), boolean_array)
def cast_np_bool_arr_to_bool_arr(context, builder, fromty, toty, val):
    func = lambda A: bodo.libs.bool_arr_ext.init_bool_array(A, np.full(len(
        A) + 7 >> 3, 255, np.uint8))
    mecq__zqzgj = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, mecq__zqzgj)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    wxpwu__ktce = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        vrjre__bctui = bodo.utils.utils.is_array_typ(val1, False)
        rcjw__jvquq = bodo.utils.utils.is_array_typ(val2, False)
        rfxpk__syn = 'val1' if vrjre__bctui else 'val2'
        zyez__mcj = 'def impl(val1, val2):\n'
        zyez__mcj += f'  n = len({rfxpk__syn})\n'
        zyez__mcj += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        zyez__mcj += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if vrjre__bctui:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            vzjvu__gksrh = 'val1[i]'
        else:
            null1 = 'False\n'
            vzjvu__gksrh = 'val1'
        if rcjw__jvquq:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            vmodi__kavff = 'val2[i]'
        else:
            null2 = 'False\n'
            vmodi__kavff = 'val2'
        if wxpwu__ktce:
            zyez__mcj += f"""    result, isna_val = compute_or_body({null1}, {null2}, {vzjvu__gksrh}, {vmodi__kavff})
"""
        else:
            zyez__mcj += f"""    result, isna_val = compute_and_body({null1}, {null2}, {vzjvu__gksrh}, {vmodi__kavff})
"""
        zyez__mcj += '    out_arr[i] = result\n'
        zyez__mcj += '    if isna_val:\n'
        zyez__mcj += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        zyez__mcj += '      continue\n'
        zyez__mcj += '  return out_arr\n'
        mmz__hgh = {}
        exec(zyez__mcj, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, mmz__hgh)
        impl = mmz__hgh['impl']
        return impl
    return bool_array_impl


def compute_or_body(null1, null2, val1, val2):
    pass


@overload(compute_or_body)
def overload_compute_or_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == False
        elif null2:
            return val1, val1 == False
        else:
            return val1 | val2, False
    return impl


def compute_and_body(null1, null2, val1, val2):
    pass


@overload(compute_and_body)
def overload_compute_and_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == True
        elif null2:
            return val1, val1 == True
        else:
            return val1 & val2, False
    return impl


def create_boolean_array_logical_lower_impl(op):

    def logical_lower_impl(context, builder, sig, args):
        impl = create_nullable_logical_op_overload(op)(*sig.args)
        return context.compile_internal(builder, impl, sig, args)
    return logical_lower_impl


class BooleanArrayLogicalOperatorTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        if not is_valid_boolean_array_logical_op(args[0], args[1]):
            return
        gibo__knqe = boolean_array
        return gibo__knqe(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    yqh__ftscv = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return yqh__ftscv


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        huc__ols = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(huc__ols)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(huc__ols)


_install_nullable_logical_lowering()
