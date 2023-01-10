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
        ahi__vtbxj = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, ahi__vtbxj)


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
    pqcnw__fjch = c.context.insert_const_string(c.builder.module, 'pandas')
    gywje__gvovv = c.pyapi.import_module_noblock(pqcnw__fjch)
    nwlcl__ojggo = c.pyapi.call_method(gywje__gvovv, 'BooleanDtype', ())
    c.pyapi.decref(gywje__gvovv)
    return nwlcl__ojggo


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    zuqiy__ihgu = n + 7 >> 3
    return np.full(zuqiy__ihgu, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    nujsn__gmntm = c.context.typing_context.resolve_value_type(func)
    dtt__lpkm = nujsn__gmntm.get_call_type(c.context.typing_context,
        arg_typs, {})
    spkip__znwe = c.context.get_function(nujsn__gmntm, dtt__lpkm)
    xmw__ywkty = c.context.call_conv.get_function_type(dtt__lpkm.
        return_type, dtt__lpkm.args)
    epgth__ggxs = c.builder.module
    ejk__logp = lir.Function(epgth__ggxs, xmw__ywkty, name=epgth__ggxs.
        get_unique_name('.func_conv'))
    ejk__logp.linkage = 'internal'
    nzdtg__lgua = lir.IRBuilder(ejk__logp.append_basic_block())
    dnux__opy = c.context.call_conv.decode_arguments(nzdtg__lgua, dtt__lpkm
        .args, ejk__logp)
    byun__mny = spkip__znwe(nzdtg__lgua, dnux__opy)
    c.context.call_conv.return_value(nzdtg__lgua, byun__mny)
    ryror__pukik, mruo__hlpi = c.context.call_conv.call_function(c.builder,
        ejk__logp, dtt__lpkm.return_type, dtt__lpkm.args, args)
    return mruo__hlpi


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    udp__tet = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(udp__tet)
    c.pyapi.decref(udp__tet)
    xmw__ywkty = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    yobbw__rjlc = cgutils.get_or_insert_function(c.builder.module,
        xmw__ywkty, name='is_bool_array')
    xmw__ywkty = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    ejk__logp = cgutils.get_or_insert_function(c.builder.module, xmw__ywkty,
        name='is_pd_boolean_array')
    sdt__edpcr = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    foqtt__sqfrh = c.builder.call(ejk__logp, [obj])
    lcqal__fwy = c.builder.icmp_unsigned('!=', foqtt__sqfrh, foqtt__sqfrh.
        type(0))
    with c.builder.if_else(lcqal__fwy) as (xws__vhu, fytpy__kuacy):
        with xws__vhu:
            lha__yjyzn = c.pyapi.object_getattr_string(obj, '_data')
            sdt__edpcr.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), lha__yjyzn).value
            gliic__rfha = c.pyapi.object_getattr_string(obj, '_mask')
            kxykn__ymzsh = c.pyapi.to_native_value(types.Array(types.bool_,
                1, 'C'), gliic__rfha).value
            zuqiy__ihgu = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            faa__cpz = c.context.make_array(types.Array(types.bool_, 1, 'C'))(c
                .context, c.builder, kxykn__ymzsh)
            xtsu__mdpkx = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [zuqiy__ihgu])
            xmw__ywkty = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            ejk__logp = cgutils.get_or_insert_function(c.builder.module,
                xmw__ywkty, name='mask_arr_to_bitmap')
            c.builder.call(ejk__logp, [xtsu__mdpkx.data, faa__cpz.data, n])
            sdt__edpcr.null_bitmap = xtsu__mdpkx._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), kxykn__ymzsh)
            c.pyapi.decref(lha__yjyzn)
            c.pyapi.decref(gliic__rfha)
        with fytpy__kuacy:
            fcnd__qkbg = c.builder.call(yobbw__rjlc, [obj])
            hogx__vvgt = c.builder.icmp_unsigned('!=', fcnd__qkbg,
                fcnd__qkbg.type(0))
            with c.builder.if_else(hogx__vvgt) as (eld__bhn, kkup__ecfze):
                with eld__bhn:
                    sdt__edpcr.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    sdt__edpcr.null_bitmap = call_func_in_unbox(gen_full_bitmap
                        , (n,), (types.int64,), c)
                with kkup__ecfze:
                    sdt__edpcr.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    zuqiy__ihgu = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    sdt__edpcr.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [zuqiy__ihgu])._getvalue()
                    xfnu__smw = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, sdt__edpcr.data
                        ).data
                    rivt__vzzx = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, sdt__edpcr.
                        null_bitmap).data
                    xmw__ywkty = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    ejk__logp = cgutils.get_or_insert_function(c.builder.
                        module, xmw__ywkty, name='unbox_bool_array_obj')
                    c.builder.call(ejk__logp, [obj, xfnu__smw, rivt__vzzx, n])
    return NativeValue(sdt__edpcr._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    sdt__edpcr = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        sdt__edpcr.data, c.env_manager)
    qhxqc__pvhis = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, sdt__edpcr.null_bitmap).data
    udp__tet = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(udp__tet)
    pqcnw__fjch = c.context.insert_const_string(c.builder.module, 'numpy')
    bsnx__lfki = c.pyapi.import_module_noblock(pqcnw__fjch)
    zrff__qdl = c.pyapi.object_getattr_string(bsnx__lfki, 'bool_')
    kxykn__ymzsh = c.pyapi.call_method(bsnx__lfki, 'empty', (udp__tet,
        zrff__qdl))
    zityy__hlsz = c.pyapi.object_getattr_string(kxykn__ymzsh, 'ctypes')
    oeh__lwca = c.pyapi.object_getattr_string(zityy__hlsz, 'data')
    zgo__tfxf = c.builder.inttoptr(c.pyapi.long_as_longlong(oeh__lwca), lir
        .IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as nhaum__tzu:
        ikp__ory = nhaum__tzu.index
        jaupi__agp = c.builder.lshr(ikp__ory, lir.Constant(lir.IntType(64), 3))
        xnju__twqo = c.builder.load(cgutils.gep(c.builder, qhxqc__pvhis,
            jaupi__agp))
        bncpi__kyzbq = c.builder.trunc(c.builder.and_(ikp__ory, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(xnju__twqo, bncpi__kyzbq), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        purp__vtu = cgutils.gep(c.builder, zgo__tfxf, ikp__ory)
        c.builder.store(val, purp__vtu)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        sdt__edpcr.null_bitmap)
    pqcnw__fjch = c.context.insert_const_string(c.builder.module, 'pandas')
    gywje__gvovv = c.pyapi.import_module_noblock(pqcnw__fjch)
    cpcie__oqgq = c.pyapi.object_getattr_string(gywje__gvovv, 'arrays')
    nwlcl__ojggo = c.pyapi.call_method(cpcie__oqgq, 'BooleanArray', (data,
        kxykn__ymzsh))
    c.pyapi.decref(gywje__gvovv)
    c.pyapi.decref(udp__tet)
    c.pyapi.decref(bsnx__lfki)
    c.pyapi.decref(zrff__qdl)
    c.pyapi.decref(zityy__hlsz)
    c.pyapi.decref(oeh__lwca)
    c.pyapi.decref(cpcie__oqgq)
    c.pyapi.decref(data)
    c.pyapi.decref(kxykn__ymzsh)
    return nwlcl__ojggo


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    aqvvk__xdbn = np.empty(n, np.bool_)
    ibn__hyqdo = np.empty(n + 7 >> 3, np.uint8)
    for ikp__ory, s in enumerate(pyval):
        mead__yyrjb = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ibn__hyqdo, ikp__ory, int(not
            mead__yyrjb))
        if not mead__yyrjb:
            aqvvk__xdbn[ikp__ory] = s
    yguaa__dymi = context.get_constant_generic(builder, data_type, aqvvk__xdbn)
    vnfzj__edkro = context.get_constant_generic(builder, nulls_type, ibn__hyqdo
        )
    return lir.Constant.literal_struct([yguaa__dymi, vnfzj__edkro])


def lower_init_bool_array(context, builder, signature, args):
    ekrt__gnn, faq__uqgb = args
    sdt__edpcr = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    sdt__edpcr.data = ekrt__gnn
    sdt__edpcr.null_bitmap = faq__uqgb
    context.nrt.incref(builder, signature.args[0], ekrt__gnn)
    context.nrt.incref(builder, signature.args[1], faq__uqgb)
    return sdt__edpcr._getvalue()


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
    abado__iqj = args[0]
    if equiv_set.has_shape(abado__iqj):
        return ArrayAnalysis.AnalyzeResult(shape=abado__iqj, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    abado__iqj = args[0]
    if equiv_set.has_shape(abado__iqj):
        return ArrayAnalysis.AnalyzeResult(shape=abado__iqj, pre=[])
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
    aqvvk__xdbn = np.empty(n, dtype=np.bool_)
    rmw__wwee = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(aqvvk__xdbn, rmw__wwee)


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
            esdzm__qumjd, gwx__juvso = array_getitem_bool_index(A, ind)
            return init_bool_array(esdzm__qumjd, gwx__juvso)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            esdzm__qumjd, gwx__juvso = array_getitem_int_index(A, ind)
            return init_bool_array(esdzm__qumjd, gwx__juvso)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            esdzm__qumjd, gwx__juvso = array_getitem_slice_index(A, ind)
            return init_bool_array(esdzm__qumjd, gwx__juvso)
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
    fiy__vbw = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(fiy__vbw)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(fiy__vbw)
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
        for ikp__ory in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, ikp__ory):
                val = A[ikp__ory]
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
            veswp__ikmt = np.empty(n, nb_dtype)
            for ikp__ory in numba.parfors.parfor.internal_prange(n):
                veswp__ikmt[ikp__ory] = data[ikp__ory]
                if bodo.libs.array_kernels.isna(A, ikp__ory):
                    veswp__ikmt[ikp__ory] = np.nan
            return veswp__ikmt
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload_method(BooleanArrayType, 'fillna', no_unliteral=True)
def overload_bool_fillna(A, value=None, method=None, limit=None):

    def impl(A, value=None, method=None, limit=None):
        data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
        n = len(data)
        veswp__ikmt = np.empty(n, dtype=np.bool_)
        for ikp__ory in numba.parfors.parfor.internal_prange(n):
            veswp__ikmt[ikp__ory] = data[ikp__ory]
            if bodo.libs.array_kernels.isna(A, ikp__ory):
                veswp__ikmt[ikp__ory] = value
        return veswp__ikmt
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
    aeajy__wvxo = op.__name__
    aeajy__wvxo = ufunc_aliases.get(aeajy__wvxo, aeajy__wvxo)
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
    for ympf__keeph in numba.np.ufunc_db.get_ufuncs():
        aczo__dhw = create_op_overload(ympf__keeph, ympf__keeph.nin)
        overload(ympf__keeph, no_unliteral=True)(aczo__dhw)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        aczo__dhw = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(aczo__dhw)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        aczo__dhw = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(aczo__dhw)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        aczo__dhw = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(aczo__dhw)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        bncpi__kyzbq = []
        tnv__bvhlz = False
        wrt__rfr = False
        xdisp__xkmk = False
        for ikp__ory in range(len(A)):
            if bodo.libs.array_kernels.isna(A, ikp__ory):
                if not tnv__bvhlz:
                    data.append(False)
                    bncpi__kyzbq.append(False)
                    tnv__bvhlz = True
                continue
            val = A[ikp__ory]
            if val and not wrt__rfr:
                data.append(True)
                bncpi__kyzbq.append(True)
                wrt__rfr = True
            if not val and not xdisp__xkmk:
                data.append(False)
                bncpi__kyzbq.append(True)
                xdisp__xkmk = True
            if tnv__bvhlz and wrt__rfr and xdisp__xkmk:
                break
        esdzm__qumjd = np.array(data)
        n = len(esdzm__qumjd)
        zuqiy__ihgu = 1
        gwx__juvso = np.empty(zuqiy__ihgu, np.uint8)
        for jcyom__oor in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(gwx__juvso, jcyom__oor,
                bncpi__kyzbq[jcyom__oor])
        return init_bool_array(esdzm__qumjd, gwx__juvso)
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
            nbcb__ajwo = bodo.utils.conversion.nullable_bool_to_bool_na_false(
                ind)
            return A[nbcb__ajwo]
        return impl


@lower_cast(types.Array(types.bool_, 1, 'C'), boolean_array)
def cast_np_bool_arr_to_bool_arr(context, builder, fromty, toty, val):
    func = lambda A: bodo.libs.bool_arr_ext.init_bool_array(A, np.full(len(
        A) + 7 >> 3, 255, np.uint8))
    nwlcl__ojggo = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, nwlcl__ojggo)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    ymu__sxpj = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        fhibb__facov = bodo.utils.utils.is_array_typ(val1, False)
        odg__vrakb = bodo.utils.utils.is_array_typ(val2, False)
        cqw__adsqa = 'val1' if fhibb__facov else 'val2'
        htmks__hosqd = 'def impl(val1, val2):\n'
        htmks__hosqd += f'  n = len({cqw__adsqa})\n'
        htmks__hosqd += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        htmks__hosqd += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if fhibb__facov:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            xic__klzss = 'val1[i]'
        else:
            null1 = 'False\n'
            xic__klzss = 'val1'
        if odg__vrakb:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            qou__bxj = 'val2[i]'
        else:
            null2 = 'False\n'
            qou__bxj = 'val2'
        if ymu__sxpj:
            htmks__hosqd += f"""    result, isna_val = compute_or_body({null1}, {null2}, {xic__klzss}, {qou__bxj})
"""
        else:
            htmks__hosqd += f"""    result, isna_val = compute_and_body({null1}, {null2}, {xic__klzss}, {qou__bxj})
"""
        htmks__hosqd += '    out_arr[i] = result\n'
        htmks__hosqd += '    if isna_val:\n'
        htmks__hosqd += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        htmks__hosqd += '      continue\n'
        htmks__hosqd += '  return out_arr\n'
        ovr__vmnc = {}
        exec(htmks__hosqd, {'bodo': bodo, 'numba': numba,
            'compute_and_body': compute_and_body, 'compute_or_body':
            compute_or_body}, ovr__vmnc)
        impl = ovr__vmnc['impl']
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
        vso__ipzb = boolean_array
        return vso__ipzb(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    arxr__jgbp = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return arxr__jgbp


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        kbnxw__trjb = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(kbnxw__trjb)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(kbnxw__trjb)


_install_nullable_logical_lowering()
