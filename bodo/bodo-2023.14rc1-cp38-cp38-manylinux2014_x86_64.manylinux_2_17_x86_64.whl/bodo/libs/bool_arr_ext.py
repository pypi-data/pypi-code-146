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
        bnvf__eping = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, bnvf__eping)


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
    bsmq__hgdve = c.context.insert_const_string(c.builder.module, 'pandas')
    nykq__jmz = c.pyapi.import_module_noblock(bsmq__hgdve)
    pbp__qswcr = c.pyapi.call_method(nykq__jmz, 'BooleanDtype', ())
    c.pyapi.decref(nykq__jmz)
    return pbp__qswcr


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    lym__giioj = n + 7 >> 3
    return np.full(lym__giioj, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    obetd__rdwra = c.context.typing_context.resolve_value_type(func)
    ufy__kpfbs = obetd__rdwra.get_call_type(c.context.typing_context,
        arg_typs, {})
    xmabu__fie = c.context.get_function(obetd__rdwra, ufy__kpfbs)
    psgy__unv = c.context.call_conv.get_function_type(ufy__kpfbs.
        return_type, ufy__kpfbs.args)
    nqc__eaof = c.builder.module
    qqvw__wned = lir.Function(nqc__eaof, psgy__unv, name=nqc__eaof.
        get_unique_name('.func_conv'))
    qqvw__wned.linkage = 'internal'
    ptghi__caj = lir.IRBuilder(qqvw__wned.append_basic_block())
    uxjwk__vzn = c.context.call_conv.decode_arguments(ptghi__caj,
        ufy__kpfbs.args, qqvw__wned)
    yfnuk__nldl = xmabu__fie(ptghi__caj, uxjwk__vzn)
    c.context.call_conv.return_value(ptghi__caj, yfnuk__nldl)
    fld__uvw, ytkx__oyiph = c.context.call_conv.call_function(c.builder,
        qqvw__wned, ufy__kpfbs.return_type, ufy__kpfbs.args, args)
    return ytkx__oyiph


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    uih__yakt = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(uih__yakt)
    c.pyapi.decref(uih__yakt)
    psgy__unv = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    toyn__dkazr = cgutils.get_or_insert_function(c.builder.module,
        psgy__unv, name='is_bool_array')
    psgy__unv = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    qqvw__wned = cgutils.get_or_insert_function(c.builder.module, psgy__unv,
        name='is_pd_boolean_array')
    pvit__rcfz = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mrbtu__qej = c.builder.call(qqvw__wned, [obj])
    bgla__bog = c.builder.icmp_unsigned('!=', mrbtu__qej, mrbtu__qej.type(0))
    with c.builder.if_else(bgla__bog) as (pocig__jbs, zkpxx__vgj):
        with pocig__jbs:
            hqck__gkeat = c.pyapi.object_getattr_string(obj, '_data')
            pvit__rcfz.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), hqck__gkeat).value
            uhtl__xtbx = c.pyapi.object_getattr_string(obj, '_mask')
            plbwt__ghepu = c.pyapi.to_native_value(types.Array(types.bool_,
                1, 'C'), uhtl__xtbx).value
            lym__giioj = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            fse__ztwfo = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, plbwt__ghepu)
            fwvpw__wrhws = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [lym__giioj])
            psgy__unv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            qqvw__wned = cgutils.get_or_insert_function(c.builder.module,
                psgy__unv, name='mask_arr_to_bitmap')
            c.builder.call(qqvw__wned, [fwvpw__wrhws.data, fse__ztwfo.data, n])
            pvit__rcfz.null_bitmap = fwvpw__wrhws._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), plbwt__ghepu)
            c.pyapi.decref(hqck__gkeat)
            c.pyapi.decref(uhtl__xtbx)
        with zkpxx__vgj:
            shi__djys = c.builder.call(toyn__dkazr, [obj])
            qmz__mdy = c.builder.icmp_unsigned('!=', shi__djys, shi__djys.
                type(0))
            with c.builder.if_else(qmz__mdy) as (ypua__uyytn, cqk__rpdi):
                with ypua__uyytn:
                    pvit__rcfz.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    pvit__rcfz.null_bitmap = call_func_in_unbox(gen_full_bitmap
                        , (n,), (types.int64,), c)
                with cqk__rpdi:
                    pvit__rcfz.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    lym__giioj = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    pvit__rcfz.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [lym__giioj])._getvalue()
                    lhwdt__aeo = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, pvit__rcfz.data
                        ).data
                    kbpgb__nbtkg = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, pvit__rcfz.
                        null_bitmap).data
                    psgy__unv = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    qqvw__wned = cgutils.get_or_insert_function(c.builder.
                        module, psgy__unv, name='unbox_bool_array_obj')
                    c.builder.call(qqvw__wned, [obj, lhwdt__aeo,
                        kbpgb__nbtkg, n])
    return NativeValue(pvit__rcfz._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    pvit__rcfz = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        pvit__rcfz.data, c.env_manager)
    hizp__abc = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, pvit__rcfz.null_bitmap).data
    uih__yakt = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(uih__yakt)
    bsmq__hgdve = c.context.insert_const_string(c.builder.module, 'numpy')
    wlt__zux = c.pyapi.import_module_noblock(bsmq__hgdve)
    qwry__ovksr = c.pyapi.object_getattr_string(wlt__zux, 'bool_')
    plbwt__ghepu = c.pyapi.call_method(wlt__zux, 'empty', (uih__yakt,
        qwry__ovksr))
    ftew__mgw = c.pyapi.object_getattr_string(plbwt__ghepu, 'ctypes')
    vyw__vppu = c.pyapi.object_getattr_string(ftew__mgw, 'data')
    lrl__jnjl = c.builder.inttoptr(c.pyapi.long_as_longlong(vyw__vppu), lir
        .IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as qyx__oqyz:
        srad__kxzd = qyx__oqyz.index
        tseu__tkee = c.builder.lshr(srad__kxzd, lir.Constant(lir.IntType(64
            ), 3))
        bjpu__drs = c.builder.load(cgutils.gep(c.builder, hizp__abc,
            tseu__tkee))
        djmv__omewl = c.builder.trunc(c.builder.and_(srad__kxzd, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(bjpu__drs, djmv__omewl), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        aut__evy = cgutils.gep(c.builder, lrl__jnjl, srad__kxzd)
        c.builder.store(val, aut__evy)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        pvit__rcfz.null_bitmap)
    bsmq__hgdve = c.context.insert_const_string(c.builder.module, 'pandas')
    nykq__jmz = c.pyapi.import_module_noblock(bsmq__hgdve)
    ijvxn__wwj = c.pyapi.object_getattr_string(nykq__jmz, 'arrays')
    pbp__qswcr = c.pyapi.call_method(ijvxn__wwj, 'BooleanArray', (data,
        plbwt__ghepu))
    c.pyapi.decref(nykq__jmz)
    c.pyapi.decref(uih__yakt)
    c.pyapi.decref(wlt__zux)
    c.pyapi.decref(qwry__ovksr)
    c.pyapi.decref(ftew__mgw)
    c.pyapi.decref(vyw__vppu)
    c.pyapi.decref(ijvxn__wwj)
    c.pyapi.decref(data)
    c.pyapi.decref(plbwt__ghepu)
    return pbp__qswcr


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    rzvu__qhwvn = np.empty(n, np.bool_)
    ghtyg__dhnnz = np.empty(n + 7 >> 3, np.uint8)
    for srad__kxzd, s in enumerate(pyval):
        jccwa__ireg = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ghtyg__dhnnz, srad__kxzd, int(
            not jccwa__ireg))
        if not jccwa__ireg:
            rzvu__qhwvn[srad__kxzd] = s
    kzy__xhet = context.get_constant_generic(builder, data_type, rzvu__qhwvn)
    dfaiz__ktgo = context.get_constant_generic(builder, nulls_type,
        ghtyg__dhnnz)
    return lir.Constant.literal_struct([kzy__xhet, dfaiz__ktgo])


def lower_init_bool_array(context, builder, signature, args):
    zbmy__ggrrq, qoo__clvw = args
    pvit__rcfz = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    pvit__rcfz.data = zbmy__ggrrq
    pvit__rcfz.null_bitmap = qoo__clvw
    context.nrt.incref(builder, signature.args[0], zbmy__ggrrq)
    context.nrt.incref(builder, signature.args[1], qoo__clvw)
    return pvit__rcfz._getvalue()


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
    etn__tmf = args[0]
    if equiv_set.has_shape(etn__tmf):
        return ArrayAnalysis.AnalyzeResult(shape=etn__tmf, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    etn__tmf = args[0]
    if equiv_set.has_shape(etn__tmf):
        return ArrayAnalysis.AnalyzeResult(shape=etn__tmf, pre=[])
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
    rzvu__qhwvn = np.empty(n, dtype=np.bool_)
    ftuv__hdy = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(rzvu__qhwvn, ftuv__hdy)


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
            oykj__bqlu, myyh__jgy = array_getitem_bool_index(A, ind)
            return init_bool_array(oykj__bqlu, myyh__jgy)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            oykj__bqlu, myyh__jgy = array_getitem_int_index(A, ind)
            return init_bool_array(oykj__bqlu, myyh__jgy)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            oykj__bqlu, myyh__jgy = array_getitem_slice_index(A, ind)
            return init_bool_array(oykj__bqlu, myyh__jgy)
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
    mfdhj__xju = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(mfdhj__xju)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(mfdhj__xju)
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
        for srad__kxzd in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, srad__kxzd):
                val = A[srad__kxzd]
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
            uej__kktnw = np.empty(n, nb_dtype)
            for srad__kxzd in numba.parfors.parfor.internal_prange(n):
                uej__kktnw[srad__kxzd] = data[srad__kxzd]
                if bodo.libs.array_kernels.isna(A, srad__kxzd):
                    uej__kktnw[srad__kxzd] = np.nan
            return uej__kktnw
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload_method(BooleanArrayType, 'fillna', no_unliteral=True)
def overload_bool_fillna(A, value=None, method=None, limit=None):

    def impl(A, value=None, method=None, limit=None):
        data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
        n = len(data)
        uej__kktnw = np.empty(n, dtype=np.bool_)
        for srad__kxzd in numba.parfors.parfor.internal_prange(n):
            uej__kktnw[srad__kxzd] = data[srad__kxzd]
            if bodo.libs.array_kernels.isna(A, srad__kxzd):
                uej__kktnw[srad__kxzd] = value
        return uej__kktnw
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
    hoyb__ymnvt = op.__name__
    hoyb__ymnvt = ufunc_aliases.get(hoyb__ymnvt, hoyb__ymnvt)
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
    for oqieq__odbf in numba.np.ufunc_db.get_ufuncs():
        fypvw__fob = create_op_overload(oqieq__odbf, oqieq__odbf.nin)
        overload(oqieq__odbf, no_unliteral=True)(fypvw__fob)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        fypvw__fob = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(fypvw__fob)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        fypvw__fob = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(fypvw__fob)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        fypvw__fob = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(fypvw__fob)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        djmv__omewl = []
        wzi__semxz = False
        ppfi__obo = False
        evu__zbua = False
        for srad__kxzd in range(len(A)):
            if bodo.libs.array_kernels.isna(A, srad__kxzd):
                if not wzi__semxz:
                    data.append(False)
                    djmv__omewl.append(False)
                    wzi__semxz = True
                continue
            val = A[srad__kxzd]
            if val and not ppfi__obo:
                data.append(True)
                djmv__omewl.append(True)
                ppfi__obo = True
            if not val and not evu__zbua:
                data.append(False)
                djmv__omewl.append(True)
                evu__zbua = True
            if wzi__semxz and ppfi__obo and evu__zbua:
                break
        oykj__bqlu = np.array(data)
        n = len(oykj__bqlu)
        lym__giioj = 1
        myyh__jgy = np.empty(lym__giioj, np.uint8)
        for xgtve__jtkc in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(myyh__jgy, xgtve__jtkc,
                djmv__omewl[xgtve__jtkc])
        return init_bool_array(oykj__bqlu, myyh__jgy)
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
            lyg__zuhv = bodo.utils.conversion.nullable_bool_to_bool_na_false(
                ind)
            return A[lyg__zuhv]
        return impl


@lower_cast(types.Array(types.bool_, 1, 'C'), boolean_array)
def cast_np_bool_arr_to_bool_arr(context, builder, fromty, toty, val):
    func = lambda A: bodo.libs.bool_arr_ext.init_bool_array(A, np.full(len(
        A) + 7 >> 3, 255, np.uint8))
    pbp__qswcr = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, pbp__qswcr)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    utgf__qldog = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        mgdpr__beo = bodo.utils.utils.is_array_typ(val1, False)
        tsll__nna = bodo.utils.utils.is_array_typ(val2, False)
        nofws__bsl = 'val1' if mgdpr__beo else 'val2'
        viymh__kvi = 'def impl(val1, val2):\n'
        viymh__kvi += f'  n = len({nofws__bsl})\n'
        viymh__kvi += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        viymh__kvi += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if mgdpr__beo:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            nds__nms = 'val1[i]'
        else:
            null1 = 'False\n'
            nds__nms = 'val1'
        if tsll__nna:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            pem__drsxw = 'val2[i]'
        else:
            null2 = 'False\n'
            pem__drsxw = 'val2'
        if utgf__qldog:
            viymh__kvi += f"""    result, isna_val = compute_or_body({null1}, {null2}, {nds__nms}, {pem__drsxw})
"""
        else:
            viymh__kvi += f"""    result, isna_val = compute_and_body({null1}, {null2}, {nds__nms}, {pem__drsxw})
"""
        viymh__kvi += '    out_arr[i] = result\n'
        viymh__kvi += '    if isna_val:\n'
        viymh__kvi += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        viymh__kvi += '      continue\n'
        viymh__kvi += '  return out_arr\n'
        cwgxi__nbvty = {}
        exec(viymh__kvi, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, cwgxi__nbvty
            )
        impl = cwgxi__nbvty['impl']
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
        wyal__pqgyo = boolean_array
        return wyal__pqgyo(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    mnbnv__ffxl = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return mnbnv__ffxl


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        dsci__dqroq = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(dsci__dqroq)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(dsci__dqroq)


_install_nullable_logical_lowering()
