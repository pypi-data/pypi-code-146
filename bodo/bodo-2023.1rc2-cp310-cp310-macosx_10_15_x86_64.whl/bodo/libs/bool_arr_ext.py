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
        mzd__mks = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, mzd__mks)


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
    vfm__gmsw = c.context.insert_const_string(c.builder.module, 'pandas')
    vsub__bjfgy = c.pyapi.import_module_noblock(vfm__gmsw)
    kfv__qcp = c.pyapi.call_method(vsub__bjfgy, 'BooleanDtype', ())
    c.pyapi.decref(vsub__bjfgy)
    return kfv__qcp


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    dwns__vde = n + 7 >> 3
    return np.full(dwns__vde, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    axpi__npvk = c.context.typing_context.resolve_value_type(func)
    rcf__thzb = axpi__npvk.get_call_type(c.context.typing_context, arg_typs, {}
        )
    gzmn__deho = c.context.get_function(axpi__npvk, rcf__thzb)
    ipkpd__vtbjv = c.context.call_conv.get_function_type(rcf__thzb.
        return_type, rcf__thzb.args)
    cqnr__vys = c.builder.module
    gbtd__xcrnq = lir.Function(cqnr__vys, ipkpd__vtbjv, name=cqnr__vys.
        get_unique_name('.func_conv'))
    gbtd__xcrnq.linkage = 'internal'
    yyj__pbsk = lir.IRBuilder(gbtd__xcrnq.append_basic_block())
    nejs__mgkec = c.context.call_conv.decode_arguments(yyj__pbsk, rcf__thzb
        .args, gbtd__xcrnq)
    emdd__zjk = gzmn__deho(yyj__pbsk, nejs__mgkec)
    c.context.call_conv.return_value(yyj__pbsk, emdd__zjk)
    raosv__zxd, txu__gkrm = c.context.call_conv.call_function(c.builder,
        gbtd__xcrnq, rcf__thzb.return_type, rcf__thzb.args, args)
    return txu__gkrm


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    biix__ukg = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(biix__ukg)
    c.pyapi.decref(biix__ukg)
    ipkpd__vtbjv = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    bjvjj__dyufx = cgutils.get_or_insert_function(c.builder.module,
        ipkpd__vtbjv, name='is_bool_array')
    ipkpd__vtbjv = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    gbtd__xcrnq = cgutils.get_or_insert_function(c.builder.module,
        ipkpd__vtbjv, name='is_pd_boolean_array')
    drkc__nmy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    oafpf__dwjoq = c.builder.call(gbtd__xcrnq, [obj])
    xtviy__knu = c.builder.icmp_unsigned('!=', oafpf__dwjoq, oafpf__dwjoq.
        type(0))
    with c.builder.if_else(xtviy__knu) as (kbeo__onlh, hcme__cgyzn):
        with kbeo__onlh:
            hvf__qmp = c.pyapi.object_getattr_string(obj, '_data')
            drkc__nmy.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), hvf__qmp).value
            cyef__jlc = c.pyapi.object_getattr_string(obj, '_mask')
            crlc__rojr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), cyef__jlc).value
            dwns__vde = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            egtjj__dvk = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, crlc__rojr)
            gfib__oczw = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [dwns__vde])
            ipkpd__vtbjv = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            gbtd__xcrnq = cgutils.get_or_insert_function(c.builder.module,
                ipkpd__vtbjv, name='mask_arr_to_bitmap')
            c.builder.call(gbtd__xcrnq, [gfib__oczw.data, egtjj__dvk.data, n])
            drkc__nmy.null_bitmap = gfib__oczw._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), crlc__rojr)
            c.pyapi.decref(hvf__qmp)
            c.pyapi.decref(cyef__jlc)
        with hcme__cgyzn:
            wyu__jjeef = c.builder.call(bjvjj__dyufx, [obj])
            pdgt__lklr = c.builder.icmp_unsigned('!=', wyu__jjeef,
                wyu__jjeef.type(0))
            with c.builder.if_else(pdgt__lklr) as (mtde__dwfao, zxirp__kur):
                with mtde__dwfao:
                    drkc__nmy.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    drkc__nmy.null_bitmap = call_func_in_unbox(gen_full_bitmap,
                        (n,), (types.int64,), c)
                with zxirp__kur:
                    drkc__nmy.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    dwns__vde = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    drkc__nmy.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [dwns__vde])._getvalue()
                    qbwe__amhzr = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, drkc__nmy.data
                        ).data
                    mjqw__rbce = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, drkc__nmy.
                        null_bitmap).data
                    ipkpd__vtbjv = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    gbtd__xcrnq = cgutils.get_or_insert_function(c.builder.
                        module, ipkpd__vtbjv, name='unbox_bool_array_obj')
                    c.builder.call(gbtd__xcrnq, [obj, qbwe__amhzr,
                        mjqw__rbce, n])
    return NativeValue(drkc__nmy._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    drkc__nmy = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        drkc__nmy.data, c.env_manager)
    sxxw__ovgh = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, drkc__nmy.null_bitmap).data
    biix__ukg = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(biix__ukg)
    vfm__gmsw = c.context.insert_const_string(c.builder.module, 'numpy')
    bqj__biaf = c.pyapi.import_module_noblock(vfm__gmsw)
    ptllb__ymxyy = c.pyapi.object_getattr_string(bqj__biaf, 'bool_')
    crlc__rojr = c.pyapi.call_method(bqj__biaf, 'empty', (biix__ukg,
        ptllb__ymxyy))
    zgzo__cnc = c.pyapi.object_getattr_string(crlc__rojr, 'ctypes')
    kwhxi__dcg = c.pyapi.object_getattr_string(zgzo__cnc, 'data')
    gvyxe__loaqa = c.builder.inttoptr(c.pyapi.long_as_longlong(kwhxi__dcg),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as yhb__dng:
        spcnh__duie = yhb__dng.index
        kiwmd__oaz = c.builder.lshr(spcnh__duie, lir.Constant(lir.IntType(
            64), 3))
        rdv__yvkh = c.builder.load(cgutils.gep(c.builder, sxxw__ovgh,
            kiwmd__oaz))
        ojchc__odkom = c.builder.trunc(c.builder.and_(spcnh__duie, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(rdv__yvkh, ojchc__odkom), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        kbwy__uik = cgutils.gep(c.builder, gvyxe__loaqa, spcnh__duie)
        c.builder.store(val, kbwy__uik)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        drkc__nmy.null_bitmap)
    vfm__gmsw = c.context.insert_const_string(c.builder.module, 'pandas')
    vsub__bjfgy = c.pyapi.import_module_noblock(vfm__gmsw)
    yzlb__dvc = c.pyapi.object_getattr_string(vsub__bjfgy, 'arrays')
    kfv__qcp = c.pyapi.call_method(yzlb__dvc, 'BooleanArray', (data,
        crlc__rojr))
    c.pyapi.decref(vsub__bjfgy)
    c.pyapi.decref(biix__ukg)
    c.pyapi.decref(bqj__biaf)
    c.pyapi.decref(ptllb__ymxyy)
    c.pyapi.decref(zgzo__cnc)
    c.pyapi.decref(kwhxi__dcg)
    c.pyapi.decref(yzlb__dvc)
    c.pyapi.decref(data)
    c.pyapi.decref(crlc__rojr)
    return kfv__qcp


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    kxf__epb = np.empty(n, np.bool_)
    wrb__rns = np.empty(n + 7 >> 3, np.uint8)
    for spcnh__duie, s in enumerate(pyval):
        tmkk__vwvk = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(wrb__rns, spcnh__duie, int(not
            tmkk__vwvk))
        if not tmkk__vwvk:
            kxf__epb[spcnh__duie] = s
    okk__grdnc = context.get_constant_generic(builder, data_type, kxf__epb)
    kleg__lvki = context.get_constant_generic(builder, nulls_type, wrb__rns)
    return lir.Constant.literal_struct([okk__grdnc, kleg__lvki])


def lower_init_bool_array(context, builder, signature, args):
    imc__pobtv, gpps__ptlfa = args
    drkc__nmy = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    drkc__nmy.data = imc__pobtv
    drkc__nmy.null_bitmap = gpps__ptlfa
    context.nrt.incref(builder, signature.args[0], imc__pobtv)
    context.nrt.incref(builder, signature.args[1], gpps__ptlfa)
    return drkc__nmy._getvalue()


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
    vshix__frj = args[0]
    if equiv_set.has_shape(vshix__frj):
        return ArrayAnalysis.AnalyzeResult(shape=vshix__frj, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    vshix__frj = args[0]
    if equiv_set.has_shape(vshix__frj):
        return ArrayAnalysis.AnalyzeResult(shape=vshix__frj, pre=[])
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
    kxf__epb = np.empty(n, dtype=np.bool_)
    ekfy__qrld = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(kxf__epb, ekfy__qrld)


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
            xodv__xkpph, frir__wdbk = array_getitem_bool_index(A, ind)
            return init_bool_array(xodv__xkpph, frir__wdbk)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            xodv__xkpph, frir__wdbk = array_getitem_int_index(A, ind)
            return init_bool_array(xodv__xkpph, frir__wdbk)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            xodv__xkpph, frir__wdbk = array_getitem_slice_index(A, ind)
            return init_bool_array(xodv__xkpph, frir__wdbk)
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
    aljf__hzddr = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(aljf__hzddr)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(aljf__hzddr)
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
        for spcnh__duie in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, spcnh__duie):
                val = A[spcnh__duie]
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
            xsi__duzv = np.empty(n, nb_dtype)
            for spcnh__duie in numba.parfors.parfor.internal_prange(n):
                xsi__duzv[spcnh__duie] = data[spcnh__duie]
                if bodo.libs.array_kernels.isna(A, spcnh__duie):
                    xsi__duzv[spcnh__duie] = np.nan
            return xsi__duzv
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload_method(BooleanArrayType, 'fillna', no_unliteral=True)
def overload_bool_fillna(A, value=None, method=None, limit=None):

    def impl(A, value=None, method=None, limit=None):
        data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
        n = len(data)
        xsi__duzv = np.empty(n, dtype=np.bool_)
        for spcnh__duie in numba.parfors.parfor.internal_prange(n):
            xsi__duzv[spcnh__duie] = data[spcnh__duie]
            if bodo.libs.array_kernels.isna(A, spcnh__duie):
                xsi__duzv[spcnh__duie] = value
        return xsi__duzv
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
    ppb__bykh = op.__name__
    ppb__bykh = ufunc_aliases.get(ppb__bykh, ppb__bykh)
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
    for zjdva__hkf in numba.np.ufunc_db.get_ufuncs():
        afj__wmaia = create_op_overload(zjdva__hkf, zjdva__hkf.nin)
        overload(zjdva__hkf, no_unliteral=True)(afj__wmaia)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        afj__wmaia = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(afj__wmaia)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        afj__wmaia = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(afj__wmaia)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        afj__wmaia = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(afj__wmaia)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        ojchc__odkom = []
        swhhy__yiqu = False
        jxnyi__rjd = False
        oufkn__kdmdv = False
        for spcnh__duie in range(len(A)):
            if bodo.libs.array_kernels.isna(A, spcnh__duie):
                if not swhhy__yiqu:
                    data.append(False)
                    ojchc__odkom.append(False)
                    swhhy__yiqu = True
                continue
            val = A[spcnh__duie]
            if val and not jxnyi__rjd:
                data.append(True)
                ojchc__odkom.append(True)
                jxnyi__rjd = True
            if not val and not oufkn__kdmdv:
                data.append(False)
                ojchc__odkom.append(True)
                oufkn__kdmdv = True
            if swhhy__yiqu and jxnyi__rjd and oufkn__kdmdv:
                break
        xodv__xkpph = np.array(data)
        n = len(xodv__xkpph)
        dwns__vde = 1
        frir__wdbk = np.empty(dwns__vde, np.uint8)
        for zig__gyqb in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(frir__wdbk, zig__gyqb,
                ojchc__odkom[zig__gyqb])
        return init_bool_array(xodv__xkpph, frir__wdbk)
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
            ifuyx__xrpp = bodo.utils.conversion.nullable_bool_to_bool_na_false(
                ind)
            return A[ifuyx__xrpp]
        return impl


@lower_cast(types.Array(types.bool_, 1, 'C'), boolean_array)
def cast_np_bool_arr_to_bool_arr(context, builder, fromty, toty, val):
    func = lambda A: bodo.libs.bool_arr_ext.init_bool_array(A, np.full(len(
        A) + 7 >> 3, 255, np.uint8))
    kfv__qcp = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, kfv__qcp)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    tvn__gwv = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        ljx__rnvph = bodo.utils.utils.is_array_typ(val1, False)
        azull__xthzu = bodo.utils.utils.is_array_typ(val2, False)
        xbovd__hpmd = 'val1' if ljx__rnvph else 'val2'
        nwnw__erbu = 'def impl(val1, val2):\n'
        nwnw__erbu += f'  n = len({xbovd__hpmd})\n'
        nwnw__erbu += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        nwnw__erbu += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if ljx__rnvph:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            xww__msy = 'val1[i]'
        else:
            null1 = 'False\n'
            xww__msy = 'val1'
        if azull__xthzu:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            ponkn__ppmo = 'val2[i]'
        else:
            null2 = 'False\n'
            ponkn__ppmo = 'val2'
        if tvn__gwv:
            nwnw__erbu += f"""    result, isna_val = compute_or_body({null1}, {null2}, {xww__msy}, {ponkn__ppmo})
"""
        else:
            nwnw__erbu += f"""    result, isna_val = compute_and_body({null1}, {null2}, {xww__msy}, {ponkn__ppmo})
"""
        nwnw__erbu += '    out_arr[i] = result\n'
        nwnw__erbu += '    if isna_val:\n'
        nwnw__erbu += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        nwnw__erbu += '      continue\n'
        nwnw__erbu += '  return out_arr\n'
        gvoj__ecko = {}
        exec(nwnw__erbu, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, gvoj__ecko)
        impl = gvoj__ecko['impl']
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
        zfsoj__sqaj = boolean_array
        return zfsoj__sqaj(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    tutny__bnlcd = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return tutny__bnlcd


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        svvud__hcy = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(svvud__hcy)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(svvud__hcy)


_install_nullable_logical_lowering()
