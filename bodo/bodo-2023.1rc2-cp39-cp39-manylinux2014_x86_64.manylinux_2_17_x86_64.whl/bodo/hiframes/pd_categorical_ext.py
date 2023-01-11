import enum
import operator
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.utils.typing import NOT_CONSTANT, BodoError, MetaType, check_unsupported_args, dtype_to_array_type, get_literal_value, get_overload_const, get_overload_const_bool, is_common_scalar_dtype, is_iterable_type, is_list_like_index_type, is_literal_type, is_overload_constant_bool, is_overload_none, is_overload_true, is_scalar_type, raise_bodo_error


class PDCategoricalDtype(types.Opaque):

    def __init__(self, categories, elem_type, ordered, data=None, int_type=None
        ):
        self.categories = categories
        self.elem_type = elem_type
        self.ordered = ordered
        self.data = _get_cat_index_type(elem_type) if data is None else data
        self.int_type = int_type
        woqb__goo = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=woqb__goo)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    owjf__zsxbi = tuple(val.categories.values)
    elem_type = None if len(owjf__zsxbi) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(owjf__zsxbi, elem_type, val.ordered, bodo.
        typeof(val.categories), int_type)


def _get_cat_index_type(elem_type):
    elem_type = bodo.string_type if elem_type is None else elem_type
    return bodo.utils.typing.get_index_type_from_dtype(elem_type)


@lower_constant(PDCategoricalDtype)
def lower_constant_categorical_type(context, builder, typ, pyval):
    categories = context.get_constant_generic(builder, bodo.typeof(pyval.
        categories), pyval.categories)
    ordered = context.get_constant(types.bool_, pyval.ordered)
    return lir.Constant.literal_struct([categories, ordered])


@register_model(PDCategoricalDtype)
class PDCategoricalDtypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qfk__fskml = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, qfk__fskml)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    iupqj__vcfyj = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    tcril__mog = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, wzx__yzu, wzx__yzu = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    xfgf__haq = PDCategoricalDtype(tcril__mog, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, iupqj__vcfyj)
    return xfgf__haq(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    kmgj__mvw = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, kmgj__mvw).value
    c.pyapi.decref(kmgj__mvw)
    oxxf__twtka = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, oxxf__twtka).value
    c.pyapi.decref(oxxf__twtka)
    nmx__ifsk = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=nmx__ifsk)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    kmgj__mvw = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    ligk__qncp = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    ljas__gys = c.context.insert_const_string(c.builder.module, 'pandas')
    ros__xjh = c.pyapi.import_module_noblock(ljas__gys)
    bgj__dqn = c.pyapi.call_method(ros__xjh, 'CategoricalDtype', (
        ligk__qncp, kmgj__mvw))
    c.pyapi.decref(kmgj__mvw)
    c.pyapi.decref(ligk__qncp)
    c.pyapi.decref(ros__xjh)
    c.context.nrt.decref(c.builder, typ, val)
    return bgj__dqn


@overload_attribute(PDCategoricalDtype, 'nbytes')
def pd_categorical_nbytes_overload(A):
    return lambda A: A.categories.nbytes + bodo.io.np_io.get_dtype_size(types
        .bool_)


class CategoricalArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(CategoricalArrayType, self).__init__(name=
            f'CategoricalArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return CategoricalArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.Categorical)
def _typeof_pd_cat(val, c):
    return CategoricalArrayType(bodo.typeof(val.dtype))


@register_model(CategoricalArrayType)
class CategoricalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        effsb__kikns = get_categories_int_type(fe_type.dtype)
        qfk__fskml = [('dtype', fe_type.dtype), ('codes', types.Array(
            effsb__kikns, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, qfk__fskml)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    lvw__wmh = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), lvw__wmh).value
    c.pyapi.decref(lvw__wmh)
    bgj__dqn = c.pyapi.object_getattr_string(val, 'dtype')
    hmabv__qyxki = c.pyapi.to_native_value(typ.dtype, bgj__dqn).value
    c.pyapi.decref(bgj__dqn)
    amags__cjsc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    amags__cjsc.codes = codes
    amags__cjsc.dtype = hmabv__qyxki
    return NativeValue(amags__cjsc._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    dgovr__irrw = get_categories_int_type(typ.dtype)
    uyny__nbsrh = context.get_constant_generic(builder, types.Array(
        dgovr__irrw, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, uyny__nbsrh])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    awhp__qwlx = len(cat_dtype.categories)
    if awhp__qwlx < np.iinfo(np.int8).max:
        dtype = types.int8
    elif awhp__qwlx < np.iinfo(np.int16).max:
        dtype = types.int16
    elif awhp__qwlx < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    ljas__gys = c.context.insert_const_string(c.builder.module, 'pandas')
    ros__xjh = c.pyapi.import_module_noblock(ljas__gys)
    effsb__kikns = get_categories_int_type(dtype)
    jss__pjqfp = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    ewf__cwnt = types.Array(effsb__kikns, 1, 'C')
    c.context.nrt.incref(c.builder, ewf__cwnt, jss__pjqfp.codes)
    lvw__wmh = c.pyapi.from_native_value(ewf__cwnt, jss__pjqfp.codes, c.
        env_manager)
    c.context.nrt.incref(c.builder, dtype, jss__pjqfp.dtype)
    bgj__dqn = c.pyapi.from_native_value(dtype, jss__pjqfp.dtype, c.env_manager
        )
    pxaz__mjhqe = c.pyapi.borrow_none()
    fdoin__jbppy = c.pyapi.object_getattr_string(ros__xjh, 'Categorical')
    visb__hqvpj = c.pyapi.call_method(fdoin__jbppy, 'from_codes', (lvw__wmh,
        pxaz__mjhqe, pxaz__mjhqe, bgj__dqn))
    c.pyapi.decref(fdoin__jbppy)
    c.pyapi.decref(lvw__wmh)
    c.pyapi.decref(bgj__dqn)
    c.pyapi.decref(ros__xjh)
    c.context.nrt.decref(c.builder, typ, val)
    return visb__hqvpj


def _to_readonly(t):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, TimedeltaIndexType
    if isinstance(t, CategoricalArrayType):
        return CategoricalArrayType(_to_readonly(t.dtype))
    if isinstance(t, PDCategoricalDtype):
        return PDCategoricalDtype(t.categories, t.elem_type, t.ordered,
            _to_readonly(t.data), t.int_type)
    if isinstance(t, types.Array):
        return types.Array(t.dtype, t.ndim, 'C', True)
    if isinstance(t, NumericIndexType):
        return NumericIndexType(t.dtype, t.name_typ, _to_readonly(t.data))
    if isinstance(t, (DatetimeIndexType, TimedeltaIndexType)):
        return t.__class__(t.name_typ, _to_readonly(t.data))
    return t


@lower_cast(CategoricalArrayType, CategoricalArrayType)
def cast_cat_arr(context, builder, fromty, toty, val):
    if _to_readonly(toty) == fromty:
        return val
    raise BodoError(f'Cannot cast from {fromty} to {toty}')


def create_cmp_op_overload(op):

    def overload_cat_arr_cmp(A, other):
        if not isinstance(A, CategoricalArrayType):
            return
        if A.dtype.categories and is_literal_type(other) and types.unliteral(
            other) == A.dtype.elem_type:
            val = get_literal_value(other)
            jnmli__mbq = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                htb__woer = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), jnmli__mbq)
                return htb__woer
            return impl_lit

        def impl(A, other):
            jnmli__mbq = get_code_for_value(A.dtype, other)
            htb__woer = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), jnmli__mbq)
            return htb__woer
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        unqrz__awr = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(unqrz__awr)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    jss__pjqfp = cat_dtype.categories
    n = len(jss__pjqfp)
    for xcy__fgcd in range(n):
        if jss__pjqfp[xcy__fgcd] == val:
            return xcy__fgcd
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    aebqd__yawrp = bodo.utils.typing.parse_dtype(dtype,
        'CategoricalArray.astype')
    if (aebqd__yawrp != A.dtype.elem_type and aebqd__yawrp != types.
        unicode_type):
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if aebqd__yawrp == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            htb__woer = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for xcy__fgcd in numba.parfors.parfor.internal_prange(n):
                tbh__jvj = codes[xcy__fgcd]
                if tbh__jvj == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(htb__woer,
                            xcy__fgcd)
                    else:
                        bodo.libs.array_kernels.setna(htb__woer, xcy__fgcd)
                    continue
                htb__woer[xcy__fgcd] = str(bodo.utils.conversion.
                    unbox_if_tz_naive_timestamp(categories[tbh__jvj]))
            return htb__woer
        return impl
    ewf__cwnt = dtype_to_array_type(aebqd__yawrp)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        htb__woer = bodo.utils.utils.alloc_type(n, ewf__cwnt, (-1,))
        for xcy__fgcd in numba.parfors.parfor.internal_prange(n):
            tbh__jvj = codes[xcy__fgcd]
            if tbh__jvj == -1:
                bodo.libs.array_kernels.setna(htb__woer, xcy__fgcd)
                continue
            htb__woer[xcy__fgcd
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                categories[tbh__jvj])
        return htb__woer
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        ncan__kfxe, hmabv__qyxki = args
        jss__pjqfp = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        jss__pjqfp.codes = ncan__kfxe
        jss__pjqfp.dtype = hmabv__qyxki
        context.nrt.incref(builder, signature.args[0], ncan__kfxe)
        context.nrt.incref(builder, signature.args[1], hmabv__qyxki)
        return jss__pjqfp._getvalue()
    jjnn__ochaj = CategoricalArrayType(cat_dtype)
    sig = jjnn__ochaj(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    bte__etysl = args[0]
    if equiv_set.has_shape(bte__etysl):
        return ArrayAnalysis.AnalyzeResult(shape=bte__etysl, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    effsb__kikns = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, effsb__kikns)
        return init_categorical_array(codes, cat_dtype)
    return impl


def alloc_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_alloc_categorical_array
    ) = alloc_categorical_array_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_categorical_arr_codes(A):
    return lambda A: A.codes


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_categorical_array',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_categorical_arr_codes',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func


@overload_method(CategoricalArrayType, 'copy', no_unliteral=True)
def cat_arr_copy_overload(arr):
    return lambda arr: init_categorical_array(arr.codes.copy(), arr.dtype)


def build_replace_dicts(to_replace, value, categories):
    return dict(), np.empty(len(categories) + 1), 0


@overload(build_replace_dicts, no_unliteral=True)
def _build_replace_dicts(to_replace, value, categories):
    if isinstance(to_replace, types.Number) or to_replace == bodo.string_type:

        def impl(to_replace, value, categories):
            return build_replace_dicts([to_replace], value, categories)
        return impl
    else:

        def impl(to_replace, value, categories):
            n = len(categories)
            kbhnx__cas = {}
            uyny__nbsrh = np.empty(n + 1, np.int64)
            cqfvy__ylqu = {}
            pdhnl__vryop = []
            wbwz__vxmb = {}
            for xcy__fgcd in range(n):
                wbwz__vxmb[categories[xcy__fgcd]] = xcy__fgcd
            for oaxqs__zrvd in to_replace:
                if oaxqs__zrvd != value:
                    if oaxqs__zrvd in wbwz__vxmb:
                        if value in wbwz__vxmb:
                            kbhnx__cas[oaxqs__zrvd] = oaxqs__zrvd
                            qdukd__diize = wbwz__vxmb[oaxqs__zrvd]
                            cqfvy__ylqu[qdukd__diize] = wbwz__vxmb[value]
                            pdhnl__vryop.append(qdukd__diize)
                        else:
                            kbhnx__cas[oaxqs__zrvd] = value
                            wbwz__vxmb[value] = wbwz__vxmb[oaxqs__zrvd]
            pdihc__vaen = np.sort(np.array(pdhnl__vryop))
            cvl__zty = 0
            klb__vhmj = []
            for vmn__dono in range(-1, n):
                while cvl__zty < len(pdihc__vaen) and vmn__dono > pdihc__vaen[
                    cvl__zty]:
                    cvl__zty += 1
                klb__vhmj.append(cvl__zty)
            for xnph__iiw in range(-1, n):
                xvm__fpfcg = xnph__iiw
                if xnph__iiw in cqfvy__ylqu:
                    xvm__fpfcg = cqfvy__ylqu[xnph__iiw]
                uyny__nbsrh[xnph__iiw + 1] = xvm__fpfcg - klb__vhmj[
                    xvm__fpfcg + 1]
            return kbhnx__cas, uyny__nbsrh, len(pdihc__vaen)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for xcy__fgcd in range(len(new_codes_arr)):
        new_codes_arr[xcy__fgcd] = codes_map_arr[old_codes_arr[xcy__fgcd] + 1]


@overload_method(CategoricalArrayType, 'replace', inline='always',
    no_unliteral=True)
def overload_replace(arr, to_replace, value):

    def impl(arr, to_replace, value):
        return bodo.hiframes.pd_categorical_ext.cat_replace(arr, to_replace,
            value)
    return impl


def cat_replace(arr, to_replace, value):
    return


@overload(cat_replace, no_unliteral=True)
def cat_replace_overload(arr, to_replace, value):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_replace,
        'CategoricalArray.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'CategoricalArray.replace()')
    kbv__evjp = arr.dtype.ordered
    flgk__qkvuh = arr.dtype.elem_type
    lpzx__lypb = get_overload_const(to_replace)
    xaax__nykrn = get_overload_const(value)
    if (arr.dtype.categories is not None and lpzx__lypb is not NOT_CONSTANT and
        xaax__nykrn is not NOT_CONSTANT):
        lox__xtsq, codes_map_arr, wzx__yzu = python_build_replace_dicts(
            lpzx__lypb, xaax__nykrn, arr.dtype.categories)
        if len(lox__xtsq) == 0:
            return lambda arr, to_replace, value: arr.copy()
        mopkb__mplse = []
        for sra__jmalk in arr.dtype.categories:
            if sra__jmalk in lox__xtsq:
                yzu__hdab = lox__xtsq[sra__jmalk]
                if yzu__hdab != sra__jmalk:
                    mopkb__mplse.append(yzu__hdab)
            else:
                mopkb__mplse.append(sra__jmalk)
        ouln__vmc = bodo.utils.utils.create_categorical_type(mopkb__mplse,
            arr.dtype.data.data, kbv__evjp)
        zjlfm__ecjv = MetaType(tuple(ouln__vmc))

        def impl_dtype(arr, to_replace, value):
            yzx__fhru = init_cat_dtype(bodo.utils.conversion.
                index_from_array(ouln__vmc), kbv__evjp, None, zjlfm__ecjv)
            jss__pjqfp = alloc_categorical_array(len(arr.codes), yzx__fhru)
            reassign_codes(jss__pjqfp.codes, arr.codes, codes_map_arr)
            return jss__pjqfp
        return impl_dtype
    flgk__qkvuh = arr.dtype.elem_type
    if flgk__qkvuh == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            kbhnx__cas, codes_map_arr, garp__angj = build_replace_dicts(
                to_replace, value, categories.values)
            if len(kbhnx__cas) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), kbv__evjp,
                    None, None))
            n = len(categories)
            ouln__vmc = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                garp__angj, -1)
            bjz__vlom = 0
            for vmn__dono in range(n):
                wsvl__niq = categories[vmn__dono]
                if wsvl__niq in kbhnx__cas:
                    xtd__tjvj = kbhnx__cas[wsvl__niq]
                    if xtd__tjvj != wsvl__niq:
                        ouln__vmc[bjz__vlom] = xtd__tjvj
                        bjz__vlom += 1
                else:
                    ouln__vmc[bjz__vlom] = wsvl__niq
                    bjz__vlom += 1
            jss__pjqfp = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                ouln__vmc), kbv__evjp, None, None))
            reassign_codes(jss__pjqfp.codes, arr.codes, codes_map_arr)
            return jss__pjqfp
        return impl_str
    spyuk__upyc = dtype_to_array_type(flgk__qkvuh)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        kbhnx__cas, codes_map_arr, garp__angj = build_replace_dicts(to_replace,
            value, categories.values)
        if len(kbhnx__cas) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), kbv__evjp, None, None))
        n = len(categories)
        ouln__vmc = bodo.utils.utils.alloc_type(n - garp__angj, spyuk__upyc,
            None)
        bjz__vlom = 0
        for xcy__fgcd in range(n):
            wsvl__niq = categories[xcy__fgcd]
            if wsvl__niq in kbhnx__cas:
                xtd__tjvj = kbhnx__cas[wsvl__niq]
                if xtd__tjvj != wsvl__niq:
                    ouln__vmc[bjz__vlom] = xtd__tjvj
                    bjz__vlom += 1
            else:
                ouln__vmc[bjz__vlom] = wsvl__niq
                bjz__vlom += 1
        jss__pjqfp = alloc_categorical_array(len(arr.codes), init_cat_dtype
            (bodo.utils.conversion.index_from_array(ouln__vmc), kbv__evjp,
            None, None))
        reassign_codes(jss__pjqfp.codes, arr.codes, codes_map_arr)
        return jss__pjqfp
    return impl


@overload(len, no_unliteral=True)
def overload_cat_arr_len(A):
    if isinstance(A, CategoricalArrayType):
        return lambda A: len(A.codes)


@overload_attribute(CategoricalArrayType, 'shape')
def overload_cat_arr_shape(A):
    return lambda A: (len(A.codes),)


@overload_attribute(CategoricalArrayType, 'ndim')
def overload_cat_arr_ndim(A):
    return lambda A: 1


@overload_attribute(CategoricalArrayType, 'nbytes')
def cat_arr_nbytes_overload(A):
    return lambda A: A.codes.nbytes + A.dtype.nbytes


@register_jitable
def get_label_dict_from_categories(vals):
    xxa__vzxmj = dict()
    sdm__wrvb = 0
    for xcy__fgcd in range(len(vals)):
        val = vals[xcy__fgcd]
        if val in xxa__vzxmj:
            continue
        xxa__vzxmj[val] = sdm__wrvb
        sdm__wrvb += 1
    return xxa__vzxmj


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    xxa__vzxmj = dict()
    for xcy__fgcd in range(len(vals)):
        val = vals[xcy__fgcd]
        xxa__vzxmj[val] = xcy__fgcd
    return xxa__vzxmj


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    ulfn__wrnda = dict(fastpath=fastpath)
    gvkug__sffp = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', ulfn__wrnda, gvkug__sffp)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        phzw__slu = get_overload_const(categories)
        if phzw__slu is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                ctbc__fqiio = False
            else:
                ctbc__fqiio = get_overload_const_bool(ordered)
            wcsrb__ini = pd.CategoricalDtype(pd.array(phzw__slu), ctbc__fqiio
                ).categories.array
            pmj__iojb = MetaType(tuple(wcsrb__ini))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                yzx__fhru = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(wcsrb__ini), ctbc__fqiio, None, pmj__iojb)
                return bodo.utils.conversion.fix_arr_dtype(data, yzx__fhru)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            owjf__zsxbi = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                owjf__zsxbi, ordered, None, None)
            return bodo.utils.conversion.fix_arr_dtype(data, cat_dtype)
        return impl_cats
    elif is_overload_none(ordered):

        def impl_auto(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, 'category')
        return impl_auto
    raise BodoError(
        f'pd.Categorical(): argument combination not supported yet: {values}, {categories}, {ordered}, {dtype}'
        )


@overload(operator.getitem, no_unliteral=True)
def categorical_array_getitem(arr, ind):
    if not isinstance(arr, CategoricalArrayType):
        return
    if isinstance(ind, types.Integer):

        def categorical_getitem_impl(arr, ind):
            chh__bewsf = arr.codes[ind]
            return arr.dtype.categories[max(chh__bewsf, 0)]
        return categorical_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) or isinstance(ind, types.SliceType):

        def impl_bool(arr, ind):
            return init_categorical_array(arr.codes[ind], arr.dtype)
        return impl_bool
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for CategoricalArrayType with indexing type {ind} not supported.'
            )


class CategoricalMatchingValues(enum.Enum):
    DIFFERENT_TYPES = -1
    DONT_MATCH = 0
    MAY_MATCH = 1
    DO_MATCH = 2


def categorical_arrs_match(arr1, arr2):
    if not (isinstance(arr1, CategoricalArrayType) and isinstance(arr2,
        CategoricalArrayType)):
        return CategoricalMatchingValues.DIFFERENT_TYPES
    if arr1.dtype.categories is None or arr2.dtype.categories is None:
        return CategoricalMatchingValues.MAY_MATCH
    return (CategoricalMatchingValues.DO_MATCH if arr1.dtype.categories ==
        arr2.dtype.categories and arr1.dtype.ordered == arr2.dtype.ordered else
        CategoricalMatchingValues.DONT_MATCH)


@register_jitable
def cat_dtype_equal(dtype1, dtype2):
    if dtype1.ordered != dtype2.ordered or len(dtype1.categories) != len(dtype2
        .categories):
        return False
    arr1 = dtype1.categories.values
    arr2 = dtype2.categories.values
    for xcy__fgcd in range(len(arr1)):
        if arr1[xcy__fgcd] != arr2[xcy__fgcd]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    pep__mqv = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    fnon__xdvck = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    lsgg__bla = categorical_arrs_match(arr, val)
    yvvi__ciye = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    bibpx__ppy = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not pep__mqv:
            raise BodoError(yvvi__ciye)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            chh__bewsf = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = chh__bewsf
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (pep__mqv or fnon__xdvck or lsgg__bla !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(yvvi__ciye)
        if lsgg__bla == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(bibpx__ppy)
        if pep__mqv:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                ewq__tcc = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for vmn__dono in range(n):
                    arr.codes[ind[vmn__dono]] = ewq__tcc
            return impl_scalar
        if lsgg__bla == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for xcy__fgcd in range(n):
                    arr.codes[ind[xcy__fgcd]] = val.codes[xcy__fgcd]
            return impl_arr_ind_mask
        if lsgg__bla == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(bibpx__ppy)
                n = len(val.codes)
                for xcy__fgcd in range(n):
                    arr.codes[ind[xcy__fgcd]] = val.codes[xcy__fgcd]
            return impl_arr_ind_mask
        if fnon__xdvck:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for vmn__dono in range(n):
                    zard__agfgy = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[vmn__dono]))
                    if zard__agfgy not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    chh__bewsf = categories.get_loc(zard__agfgy)
                    arr.codes[ind[vmn__dono]] = chh__bewsf
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (pep__mqv or fnon__xdvck or lsgg__bla !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(yvvi__ciye)
        if lsgg__bla == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(bibpx__ppy)
        if pep__mqv:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                ewq__tcc = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for vmn__dono in range(n):
                    if ind[vmn__dono]:
                        arr.codes[vmn__dono] = ewq__tcc
            return impl_scalar
        if lsgg__bla == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                rtk__wgiwy = 0
                for xcy__fgcd in range(n):
                    if ind[xcy__fgcd]:
                        arr.codes[xcy__fgcd] = val.codes[rtk__wgiwy]
                        rtk__wgiwy += 1
            return impl_bool_ind_mask
        if lsgg__bla == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(bibpx__ppy)
                n = len(ind)
                rtk__wgiwy = 0
                for xcy__fgcd in range(n):
                    if ind[xcy__fgcd]:
                        arr.codes[xcy__fgcd] = val.codes[rtk__wgiwy]
                        rtk__wgiwy += 1
            return impl_bool_ind_mask
        if fnon__xdvck:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                rtk__wgiwy = 0
                categories = arr.dtype.categories
                for vmn__dono in range(n):
                    if ind[vmn__dono]:
                        zard__agfgy = (bodo.utils.conversion.
                            unbox_if_tz_naive_timestamp(val[rtk__wgiwy]))
                        if zard__agfgy not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        chh__bewsf = categories.get_loc(zard__agfgy)
                        arr.codes[vmn__dono] = chh__bewsf
                        rtk__wgiwy += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (pep__mqv or fnon__xdvck or lsgg__bla !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(yvvi__ciye)
        if lsgg__bla == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(bibpx__ppy)
        if pep__mqv:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                ewq__tcc = arr.dtype.categories.get_loc(val)
                zozof__qqxt = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for vmn__dono in range(zozof__qqxt.start, zozof__qqxt.stop,
                    zozof__qqxt.step):
                    arr.codes[vmn__dono] = ewq__tcc
            return impl_scalar
        if lsgg__bla == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if lsgg__bla == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(bibpx__ppy)
                arr.codes[ind] = val.codes
            return impl_arr
        if fnon__xdvck:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                zozof__qqxt = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                rtk__wgiwy = 0
                for vmn__dono in range(zozof__qqxt.start, zozof__qqxt.stop,
                    zozof__qqxt.step):
                    zard__agfgy = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[rtk__wgiwy]))
                    if zard__agfgy not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    chh__bewsf = categories.get_loc(zard__agfgy)
                    arr.codes[vmn__dono] = chh__bewsf
                    rtk__wgiwy += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
