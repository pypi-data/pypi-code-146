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
        yeahk__rby = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, yeahk__rby)


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
        qlb__qpnf = f'Float{dtype.bitwidth}Dtype()'
        super(FloatDtype, self).__init__(qlb__qpnf)


register_model(FloatDtype)(models.OpaqueModel)


@box(FloatDtype)
def box_floatdtype(typ, val, c):
    wlsfn__vchcb = c.context.insert_const_string(c.builder.module, 'pandas')
    via__vvk = c.pyapi.import_module_noblock(wlsfn__vchcb)
    cfms__lqscw = c.pyapi.call_method(via__vvk, str(typ)[:-2], ())
    c.pyapi.decref(via__vvk)
    return cfms__lqscw


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
    put__qeeu = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(put__qeeu)
    c.pyapi.decref(put__qeeu)
    asugb__adpsv = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hqsem__bnjdm = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    vcirn__eeks = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [hqsem__bnjdm])
    lky__fhbq = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    qbf__qry = cgutils.get_or_insert_function(c.builder.module, lky__fhbq,
        name='is_pd_float_array')
    udpju__ena = c.builder.call(qbf__qry, [obj])
    wpef__ubzsl = c.builder.icmp_unsigned('!=', udpju__ena, udpju__ena.type(0))
    with c.builder.if_else(wpef__ubzsl) as (clwad__udow, shj__hgq):
        with clwad__udow:
            qso__xqfe = c.pyapi.object_getattr_string(obj, '_data')
            asugb__adpsv.data = c.pyapi.to_native_value(types.Array(typ.
                dtype, 1, 'C'), qso__xqfe).value
            egmrn__nue = c.pyapi.object_getattr_string(obj, '_mask')
            zsno__doe = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), egmrn__nue).value
            c.pyapi.decref(qso__xqfe)
            c.pyapi.decref(egmrn__nue)
            qzr__fghpo = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, zsno__doe)
            lky__fhbq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            qbf__qry = cgutils.get_or_insert_function(c.builder.module,
                lky__fhbq, name='mask_arr_to_bitmap')
            c.builder.call(qbf__qry, [vcirn__eeks.data, qzr__fghpo.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), zsno__doe)
        with shj__hgq:
            pwpj__qcadm = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            lky__fhbq = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            yeab__pkz = cgutils.get_or_insert_function(c.builder.module,
                lky__fhbq, name='float_array_from_sequence')
            c.builder.call(yeab__pkz, [obj, c.builder.bitcast(pwpj__qcadm.
                data, lir.IntType(8).as_pointer()), vcirn__eeks.data])
            asugb__adpsv.data = pwpj__qcadm._getvalue()
    asugb__adpsv.null_bitmap = vcirn__eeks._getvalue()
    aeiny__vgxs = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(asugb__adpsv._getvalue(), is_error=aeiny__vgxs)


@box(FloatingArrayType)
def box_float_array(typ, val, c):
    asugb__adpsv = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        asugb__adpsv.data, c.env_manager)
    isiku__lviez = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, asugb__adpsv.null_bitmap).data
    put__qeeu = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(put__qeeu)
    wlsfn__vchcb = c.context.insert_const_string(c.builder.module, 'numpy')
    prm__npn = c.pyapi.import_module_noblock(wlsfn__vchcb)
    xggjm__vgcs = c.pyapi.object_getattr_string(prm__npn, 'bool_')
    zsno__doe = c.pyapi.call_method(prm__npn, 'empty', (put__qeeu, xggjm__vgcs)
        )
    vay__pfus = c.pyapi.object_getattr_string(zsno__doe, 'ctypes')
    nenah__mey = c.pyapi.object_getattr_string(vay__pfus, 'data')
    shic__qpuja = c.builder.inttoptr(c.pyapi.long_as_longlong(nenah__mey),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as nrzta__wko:
        jjher__she = nrzta__wko.index
        wnw__qvrp = c.builder.lshr(jjher__she, lir.Constant(lir.IntType(64), 3)
            )
        libo__ebil = c.builder.load(cgutils.gep(c.builder, isiku__lviez,
            wnw__qvrp))
        jyk__lsseh = c.builder.trunc(c.builder.and_(jjher__she, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(libo__ebil, jyk__lsseh), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        feis__jbbjl = cgutils.gep(c.builder, shic__qpuja, jjher__she)
        c.builder.store(val, feis__jbbjl)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        asugb__adpsv.null_bitmap)
    wlsfn__vchcb = c.context.insert_const_string(c.builder.module, 'pandas')
    via__vvk = c.pyapi.import_module_noblock(wlsfn__vchcb)
    cwy__quwsa = c.pyapi.object_getattr_string(via__vvk, 'arrays')
    cfms__lqscw = c.pyapi.call_method(cwy__quwsa, 'FloatingArray', (data,
        zsno__doe))
    c.pyapi.decref(via__vvk)
    c.pyapi.decref(put__qeeu)
    c.pyapi.decref(prm__npn)
    c.pyapi.decref(xggjm__vgcs)
    c.pyapi.decref(vay__pfus)
    c.pyapi.decref(nenah__mey)
    c.pyapi.decref(cwy__quwsa)
    c.pyapi.decref(data)
    c.pyapi.decref(zsno__doe)
    return cfms__lqscw


@intrinsic
def init_float_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        xkojx__fojjp, bwkj__zeqx = args
        asugb__adpsv = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        asugb__adpsv.data = xkojx__fojjp
        asugb__adpsv.null_bitmap = bwkj__zeqx
        context.nrt.incref(builder, signature.args[0], xkojx__fojjp)
        context.nrt.incref(builder, signature.args[1], bwkj__zeqx)
        return asugb__adpsv._getvalue()
    avnd__lqzrd = FloatingArrayType(data.dtype)
    mguwd__pisj = avnd__lqzrd(data, null_bitmap)
    return mguwd__pisj, codegen


@lower_constant(FloatingArrayType)
def lower_constant_float_arr(context, builder, typ, pyval):
    n = len(pyval)
    fwhr__vrp = np.empty(n, pyval.dtype.type)
    pvncq__ktsxy = np.empty(n + 7 >> 3, np.uint8)
    for jjher__she, s in enumerate(pyval):
        ijt__vxwzh = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(pvncq__ktsxy, jjher__she, int(
            not ijt__vxwzh))
        if not ijt__vxwzh:
            fwhr__vrp[jjher__she] = s
    hltdb__yoy = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), fwhr__vrp)
    mbpvp__qugy = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), pvncq__ktsxy)
    return lir.Constant.literal_struct([hltdb__yoy, mbpvp__qugy])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_float_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    uvsq__qtfga = args[0]
    if equiv_set.has_shape(uvsq__qtfga):
        return ArrayAnalysis.AnalyzeResult(shape=uvsq__qtfga, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_float_arr_ext_get_float_arr_data
    ) = get_float_arr_data_equiv


def init_float_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    uvsq__qtfga = args[0]
    if equiv_set.has_shape(uvsq__qtfga):
        return ArrayAnalysis.AnalyzeResult(shape=uvsq__qtfga, pre=[])
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
    fwhr__vrp = np.empty(n, dtype)
    cdqt__ywvj = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_float_array(fwhr__vrp, cdqt__ywvj)


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
            ofjl__tqho, iyjf__dhsou = array_getitem_bool_index(A, ind)
            return init_float_array(ofjl__tqho, iyjf__dhsou)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ofjl__tqho, iyjf__dhsou = array_getitem_int_index(A, ind)
            return init_float_array(ofjl__tqho, iyjf__dhsou)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            ofjl__tqho, iyjf__dhsou = array_getitem_slice_index(A, ind)
            return init_float_array(ofjl__tqho, iyjf__dhsou)
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
    gue__hqt = (
        f"setitem for FloatingArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    vmp__lal = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if vmp__lal:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(gue__hqt)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean, types.Float)) or vmp__lal):
        raise BodoError(gue__hqt)
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
            obvia__zxmy = np.empty(n, nb_dtype)
            for jjher__she in numba.parfors.parfor.internal_prange(n):
                obvia__zxmy[jjher__she] = data[jjher__she]
                if bodo.libs.array_kernels.isna(A, jjher__she):
                    obvia__zxmy[jjher__she] = np.nan
            return obvia__zxmy
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
    for yrlw__sehx in numba.np.ufunc_db.get_ufuncs():
        eaw__wla = create_op_overload(yrlw__sehx, yrlw__sehx.nin)
        overload(yrlw__sehx, no_unliteral=True)(eaw__wla)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        eaw__wla = create_op_overload(op, 2)
        overload(op)(eaw__wla)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        eaw__wla = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(eaw__wla)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        eaw__wla = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(eaw__wla)


_install_unary_ops()


@overload_method(FloatingArrayType, 'sum', no_unliteral=True)
def overload_float_arr_sum(A, skipna=True, min_count=0):
    cuk__jpwnk = dict(skipna=skipna, min_count=min_count)
    wdcfc__keuuv = dict(skipna=True, min_count=0)
    check_unsupported_args('FloatingArray.sum', cuk__jpwnk, wdcfc__keuuv)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0.0
        for jjher__she in numba.parfors.parfor.internal_prange(len(A)):
            val = 0.0
            if not bodo.libs.array_kernels.isna(A, jjher__she):
                val = A[jjher__she]
            s += val
        return s
    return impl


@overload_method(FloatingArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_float_arr(A):
        data = []
        jyk__lsseh = []
        bnsn__kjb = False
        s = set()
        for jjher__she in range(len(A)):
            val = A[jjher__she]
            if bodo.libs.array_kernels.isna(A, jjher__she):
                if not bnsn__kjb:
                    data.append(dtype(1))
                    jyk__lsseh.append(False)
                    bnsn__kjb = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                jyk__lsseh.append(True)
        ofjl__tqho = np.array(data)
        n = len(ofjl__tqho)
        hqsem__bnjdm = n + 7 >> 3
        iyjf__dhsou = np.empty(hqsem__bnjdm, np.uint8)
        for czzy__jvsj in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(iyjf__dhsou, czzy__jvsj,
                jyk__lsseh[czzy__jvsj])
        return init_float_array(ofjl__tqho, iyjf__dhsou)
    return impl_float_arr
