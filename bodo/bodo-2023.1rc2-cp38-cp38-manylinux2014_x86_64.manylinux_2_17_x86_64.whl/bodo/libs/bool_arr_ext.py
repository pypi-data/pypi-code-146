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
        ajayv__zopr = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, ajayv__zopr)


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
    mnwfo__avrxo = c.context.insert_const_string(c.builder.module, 'pandas')
    ivnsc__tfgtt = c.pyapi.import_module_noblock(mnwfo__avrxo)
    ajka__xut = c.pyapi.call_method(ivnsc__tfgtt, 'BooleanDtype', ())
    c.pyapi.decref(ivnsc__tfgtt)
    return ajka__xut


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    jeir__mrbh = n + 7 >> 3
    return np.full(jeir__mrbh, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    axfq__isp = c.context.typing_context.resolve_value_type(func)
    kjyot__cii = axfq__isp.get_call_type(c.context.typing_context, arg_typs, {}
        )
    eddnx__jcrbr = c.context.get_function(axfq__isp, kjyot__cii)
    dltha__cggs = c.context.call_conv.get_function_type(kjyot__cii.
        return_type, kjyot__cii.args)
    psnks__xgjsp = c.builder.module
    kmmm__zensk = lir.Function(psnks__xgjsp, dltha__cggs, name=psnks__xgjsp
        .get_unique_name('.func_conv'))
    kmmm__zensk.linkage = 'internal'
    xnypp__goo = lir.IRBuilder(kmmm__zensk.append_basic_block())
    smxc__ytfw = c.context.call_conv.decode_arguments(xnypp__goo,
        kjyot__cii.args, kmmm__zensk)
    yksbz__fpx = eddnx__jcrbr(xnypp__goo, smxc__ytfw)
    c.context.call_conv.return_value(xnypp__goo, yksbz__fpx)
    mmle__fhma, hne__oweff = c.context.call_conv.call_function(c.builder,
        kmmm__zensk, kjyot__cii.return_type, kjyot__cii.args, args)
    return hne__oweff


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    qry__lld = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(qry__lld)
    c.pyapi.decref(qry__lld)
    dltha__cggs = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    uizut__upyuf = cgutils.get_or_insert_function(c.builder.module,
        dltha__cggs, name='is_bool_array')
    dltha__cggs = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    kmmm__zensk = cgutils.get_or_insert_function(c.builder.module,
        dltha__cggs, name='is_pd_boolean_array')
    nqm__nhf = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ohl__sbsce = c.builder.call(kmmm__zensk, [obj])
    htgvu__cughc = c.builder.icmp_unsigned('!=', ohl__sbsce, ohl__sbsce.type(0)
        )
    with c.builder.if_else(htgvu__cughc) as (eeup__inj, fvcxg__naroq):
        with eeup__inj:
            rkvm__beq = c.pyapi.object_getattr_string(obj, '_data')
            nqm__nhf.data = c.pyapi.to_native_value(types.Array(types.bool_,
                1, 'C'), rkvm__beq).value
            pvpnp__rvd = c.pyapi.object_getattr_string(obj, '_mask')
            fsa__yeqyj = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), pvpnp__rvd).value
            jeir__mrbh = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            mrv__aqofj = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, fsa__yeqyj)
            sxj__vkkby = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [jeir__mrbh])
            dltha__cggs = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            kmmm__zensk = cgutils.get_or_insert_function(c.builder.module,
                dltha__cggs, name='mask_arr_to_bitmap')
            c.builder.call(kmmm__zensk, [sxj__vkkby.data, mrv__aqofj.data, n])
            nqm__nhf.null_bitmap = sxj__vkkby._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), fsa__yeqyj)
            c.pyapi.decref(rkvm__beq)
            c.pyapi.decref(pvpnp__rvd)
        with fvcxg__naroq:
            uby__thfh = c.builder.call(uizut__upyuf, [obj])
            ugl__dqny = c.builder.icmp_unsigned('!=', uby__thfh, uby__thfh.
                type(0))
            with c.builder.if_else(ugl__dqny) as (vsl__cdl, jjqb__lrzc):
                with vsl__cdl:
                    nqm__nhf.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    nqm__nhf.null_bitmap = call_func_in_unbox(gen_full_bitmap,
                        (n,), (types.int64,), c)
                with jjqb__lrzc:
                    nqm__nhf.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    jeir__mrbh = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    nqm__nhf.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [jeir__mrbh])._getvalue()
                    mno__grxx = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, nqm__nhf.data
                        ).data
                    pciey__vruf = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, nqm__nhf.
                        null_bitmap).data
                    dltha__cggs = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    kmmm__zensk = cgutils.get_or_insert_function(c.builder.
                        module, dltha__cggs, name='unbox_bool_array_obj')
                    c.builder.call(kmmm__zensk, [obj, mno__grxx,
                        pciey__vruf, n])
    return NativeValue(nqm__nhf._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    nqm__nhf = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        nqm__nhf.data, c.env_manager)
    syf__kdkrc = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, nqm__nhf.null_bitmap).data
    qry__lld = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(qry__lld)
    mnwfo__avrxo = c.context.insert_const_string(c.builder.module, 'numpy')
    pwvmm__zap = c.pyapi.import_module_noblock(mnwfo__avrxo)
    nelh__hayx = c.pyapi.object_getattr_string(pwvmm__zap, 'bool_')
    fsa__yeqyj = c.pyapi.call_method(pwvmm__zap, 'empty', (qry__lld,
        nelh__hayx))
    hlmrj__sra = c.pyapi.object_getattr_string(fsa__yeqyj, 'ctypes')
    gun__jicu = c.pyapi.object_getattr_string(hlmrj__sra, 'data')
    aqs__rwie = c.builder.inttoptr(c.pyapi.long_as_longlong(gun__jicu), lir
        .IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as uppub__gxdvc:
        kgnc__ixxwy = uppub__gxdvc.index
        nnvf__ytb = c.builder.lshr(kgnc__ixxwy, lir.Constant(lir.IntType(64
            ), 3))
        ijgtn__appl = c.builder.load(cgutils.gep(c.builder, syf__kdkrc,
            nnvf__ytb))
        kjzfe__xke = c.builder.trunc(c.builder.and_(kgnc__ixxwy, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(ijgtn__appl, kjzfe__xke), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        oon__bty = cgutils.gep(c.builder, aqs__rwie, kgnc__ixxwy)
        c.builder.store(val, oon__bty)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        nqm__nhf.null_bitmap)
    mnwfo__avrxo = c.context.insert_const_string(c.builder.module, 'pandas')
    ivnsc__tfgtt = c.pyapi.import_module_noblock(mnwfo__avrxo)
    xvh__tup = c.pyapi.object_getattr_string(ivnsc__tfgtt, 'arrays')
    ajka__xut = c.pyapi.call_method(xvh__tup, 'BooleanArray', (data,
        fsa__yeqyj))
    c.pyapi.decref(ivnsc__tfgtt)
    c.pyapi.decref(qry__lld)
    c.pyapi.decref(pwvmm__zap)
    c.pyapi.decref(nelh__hayx)
    c.pyapi.decref(hlmrj__sra)
    c.pyapi.decref(gun__jicu)
    c.pyapi.decref(xvh__tup)
    c.pyapi.decref(data)
    c.pyapi.decref(fsa__yeqyj)
    return ajka__xut


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    zsbfu__ribe = np.empty(n, np.bool_)
    hdegy__iid = np.empty(n + 7 >> 3, np.uint8)
    for kgnc__ixxwy, s in enumerate(pyval):
        wqejq__lxbsk = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(hdegy__iid, kgnc__ixxwy, int(
            not wqejq__lxbsk))
        if not wqejq__lxbsk:
            zsbfu__ribe[kgnc__ixxwy] = s
    pjtyp__ion = context.get_constant_generic(builder, data_type, zsbfu__ribe)
    ivwm__qempv = context.get_constant_generic(builder, nulls_type, hdegy__iid)
    return lir.Constant.literal_struct([pjtyp__ion, ivwm__qempv])


def lower_init_bool_array(context, builder, signature, args):
    jggnp__hsux, eai__pzwhc = args
    nqm__nhf = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    nqm__nhf.data = jggnp__hsux
    nqm__nhf.null_bitmap = eai__pzwhc
    context.nrt.incref(builder, signature.args[0], jggnp__hsux)
    context.nrt.incref(builder, signature.args[1], eai__pzwhc)
    return nqm__nhf._getvalue()


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
    shq__hglxw = args[0]
    if equiv_set.has_shape(shq__hglxw):
        return ArrayAnalysis.AnalyzeResult(shape=shq__hglxw, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    shq__hglxw = args[0]
    if equiv_set.has_shape(shq__hglxw):
        return ArrayAnalysis.AnalyzeResult(shape=shq__hglxw, pre=[])
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
    zsbfu__ribe = np.empty(n, dtype=np.bool_)
    lxu__obw = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(zsbfu__ribe, lxu__obw)


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
            nyrwb__wejb, mgdp__vdvy = array_getitem_bool_index(A, ind)
            return init_bool_array(nyrwb__wejb, mgdp__vdvy)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            nyrwb__wejb, mgdp__vdvy = array_getitem_int_index(A, ind)
            return init_bool_array(nyrwb__wejb, mgdp__vdvy)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            nyrwb__wejb, mgdp__vdvy = array_getitem_slice_index(A, ind)
            return init_bool_array(nyrwb__wejb, mgdp__vdvy)
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
    pbmcz__jca = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(pbmcz__jca)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(pbmcz__jca)
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
        for kgnc__ixxwy in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, kgnc__ixxwy):
                val = A[kgnc__ixxwy]
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
            dvbdj__ehz = np.empty(n, nb_dtype)
            for kgnc__ixxwy in numba.parfors.parfor.internal_prange(n):
                dvbdj__ehz[kgnc__ixxwy] = data[kgnc__ixxwy]
                if bodo.libs.array_kernels.isna(A, kgnc__ixxwy):
                    dvbdj__ehz[kgnc__ixxwy] = np.nan
            return dvbdj__ehz
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload_method(BooleanArrayType, 'fillna', no_unliteral=True)
def overload_bool_fillna(A, value=None, method=None, limit=None):

    def impl(A, value=None, method=None, limit=None):
        data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
        n = len(data)
        dvbdj__ehz = np.empty(n, dtype=np.bool_)
        for kgnc__ixxwy in numba.parfors.parfor.internal_prange(n):
            dvbdj__ehz[kgnc__ixxwy] = data[kgnc__ixxwy]
            if bodo.libs.array_kernels.isna(A, kgnc__ixxwy):
                dvbdj__ehz[kgnc__ixxwy] = value
        return dvbdj__ehz
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
    myqy__pnt = op.__name__
    myqy__pnt = ufunc_aliases.get(myqy__pnt, myqy__pnt)
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
    for cfufk__aqk in numba.np.ufunc_db.get_ufuncs():
        pxdxz__lkpc = create_op_overload(cfufk__aqk, cfufk__aqk.nin)
        overload(cfufk__aqk, no_unliteral=True)(pxdxz__lkpc)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        pxdxz__lkpc = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(pxdxz__lkpc)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        pxdxz__lkpc = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(pxdxz__lkpc)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        pxdxz__lkpc = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(pxdxz__lkpc)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        kjzfe__xke = []
        jzff__ohr = False
        svhl__uwpk = False
        vea__jlbgu = False
        for kgnc__ixxwy in range(len(A)):
            if bodo.libs.array_kernels.isna(A, kgnc__ixxwy):
                if not jzff__ohr:
                    data.append(False)
                    kjzfe__xke.append(False)
                    jzff__ohr = True
                continue
            val = A[kgnc__ixxwy]
            if val and not svhl__uwpk:
                data.append(True)
                kjzfe__xke.append(True)
                svhl__uwpk = True
            if not val and not vea__jlbgu:
                data.append(False)
                kjzfe__xke.append(True)
                vea__jlbgu = True
            if jzff__ohr and svhl__uwpk and vea__jlbgu:
                break
        nyrwb__wejb = np.array(data)
        n = len(nyrwb__wejb)
        jeir__mrbh = 1
        mgdp__vdvy = np.empty(jeir__mrbh, np.uint8)
        for vknax__kmga in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(mgdp__vdvy, vknax__kmga,
                kjzfe__xke[vknax__kmga])
        return init_bool_array(nyrwb__wejb, mgdp__vdvy)
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
            vkdff__gzpk = bodo.utils.conversion.nullable_bool_to_bool_na_false(
                ind)
            return A[vkdff__gzpk]
        return impl


@lower_cast(types.Array(types.bool_, 1, 'C'), boolean_array)
def cast_np_bool_arr_to_bool_arr(context, builder, fromty, toty, val):
    func = lambda A: bodo.libs.bool_arr_ext.init_bool_array(A, np.full(len(
        A) + 7 >> 3, 255, np.uint8))
    ajka__xut = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, ajka__xut)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    jzc__chnx = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        gsm__krxdh = bodo.utils.utils.is_array_typ(val1, False)
        bjw__kod = bodo.utils.utils.is_array_typ(val2, False)
        pwc__uayc = 'val1' if gsm__krxdh else 'val2'
        koqnp__qepa = 'def impl(val1, val2):\n'
        koqnp__qepa += f'  n = len({pwc__uayc})\n'
        koqnp__qepa += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        koqnp__qepa += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if gsm__krxdh:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            xlx__big = 'val1[i]'
        else:
            null1 = 'False\n'
            xlx__big = 'val1'
        if bjw__kod:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            xkrbs__agc = 'val2[i]'
        else:
            null2 = 'False\n'
            xkrbs__agc = 'val2'
        if jzc__chnx:
            koqnp__qepa += f"""    result, isna_val = compute_or_body({null1}, {null2}, {xlx__big}, {xkrbs__agc})
"""
        else:
            koqnp__qepa += f"""    result, isna_val = compute_and_body({null1}, {null2}, {xlx__big}, {xkrbs__agc})
"""
        koqnp__qepa += '    out_arr[i] = result\n'
        koqnp__qepa += '    if isna_val:\n'
        koqnp__qepa += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        koqnp__qepa += '      continue\n'
        koqnp__qepa += '  return out_arr\n'
        ehy__dnjfu = {}
        exec(koqnp__qepa, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, ehy__dnjfu)
        impl = ehy__dnjfu['impl']
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
        vsexj__pzp = boolean_array
        return vsexj__pzp(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    xutdv__tkh = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return xutdv__tkh


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        nkca__ewky = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(nkca__ewky)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(nkca__ewky)


_install_nullable_logical_lowering()
