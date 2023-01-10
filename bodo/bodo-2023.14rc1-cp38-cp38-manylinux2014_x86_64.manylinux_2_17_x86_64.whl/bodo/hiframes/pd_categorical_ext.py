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
        kcu__ysbg = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=kcu__ysbg)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    uuext__dhm = tuple(val.categories.values)
    elem_type = None if len(uuext__dhm) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(uuext__dhm, elem_type, val.ordered, bodo.
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
        pfap__lbgz = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, pfap__lbgz)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    hquk__xxht = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    vszbv__yzig = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, wosp__qxe, wosp__qxe = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    ojk__qzw = PDCategoricalDtype(vszbv__yzig, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, hquk__xxht)
    return ojk__qzw(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ygsla__whved = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, ygsla__whved
        ).value
    c.pyapi.decref(ygsla__whved)
    dzken__rmik = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, dzken__rmik).value
    c.pyapi.decref(dzken__rmik)
    dtsa__yben = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=dtsa__yben)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    ygsla__whved = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    xibeq__dtkp = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    xhc__gyxvd = c.context.insert_const_string(c.builder.module, 'pandas')
    lxnr__enmpr = c.pyapi.import_module_noblock(xhc__gyxvd)
    arjz__zzc = c.pyapi.call_method(lxnr__enmpr, 'CategoricalDtype', (
        xibeq__dtkp, ygsla__whved))
    c.pyapi.decref(ygsla__whved)
    c.pyapi.decref(xibeq__dtkp)
    c.pyapi.decref(lxnr__enmpr)
    c.context.nrt.decref(c.builder, typ, val)
    return arjz__zzc


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
        yqrc__kdt = get_categories_int_type(fe_type.dtype)
        pfap__lbgz = [('dtype', fe_type.dtype), ('codes', types.Array(
            yqrc__kdt, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, pfap__lbgz)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    fdnzj__wqtui = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), fdnzj__wqtui
        ).value
    c.pyapi.decref(fdnzj__wqtui)
    arjz__zzc = c.pyapi.object_getattr_string(val, 'dtype')
    lbl__yllr = c.pyapi.to_native_value(typ.dtype, arjz__zzc).value
    c.pyapi.decref(arjz__zzc)
    sasg__pjgh = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    sasg__pjgh.codes = codes
    sasg__pjgh.dtype = lbl__yllr
    return NativeValue(sasg__pjgh._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    stu__yykv = get_categories_int_type(typ.dtype)
    sagh__wbt = context.get_constant_generic(builder, types.Array(stu__yykv,
        1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, sagh__wbt])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    tda__kimdh = len(cat_dtype.categories)
    if tda__kimdh < np.iinfo(np.int8).max:
        dtype = types.int8
    elif tda__kimdh < np.iinfo(np.int16).max:
        dtype = types.int16
    elif tda__kimdh < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    xhc__gyxvd = c.context.insert_const_string(c.builder.module, 'pandas')
    lxnr__enmpr = c.pyapi.import_module_noblock(xhc__gyxvd)
    yqrc__kdt = get_categories_int_type(dtype)
    atp__tttl = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    bvjx__xmtj = types.Array(yqrc__kdt, 1, 'C')
    c.context.nrt.incref(c.builder, bvjx__xmtj, atp__tttl.codes)
    fdnzj__wqtui = c.pyapi.from_native_value(bvjx__xmtj, atp__tttl.codes, c
        .env_manager)
    c.context.nrt.incref(c.builder, dtype, atp__tttl.dtype)
    arjz__zzc = c.pyapi.from_native_value(dtype, atp__tttl.dtype, c.env_manager
        )
    uoaoo__rfqve = c.pyapi.borrow_none()
    kjl__eeu = c.pyapi.object_getattr_string(lxnr__enmpr, 'Categorical')
    uyr__uyfi = c.pyapi.call_method(kjl__eeu, 'from_codes', (fdnzj__wqtui,
        uoaoo__rfqve, uoaoo__rfqve, arjz__zzc))
    c.pyapi.decref(kjl__eeu)
    c.pyapi.decref(fdnzj__wqtui)
    c.pyapi.decref(arjz__zzc)
    c.pyapi.decref(lxnr__enmpr)
    c.context.nrt.decref(c.builder, typ, val)
    return uyr__uyfi


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
            bnt__rsx = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                zmc__hrgz = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), bnt__rsx)
                return zmc__hrgz
            return impl_lit

        def impl(A, other):
            bnt__rsx = get_code_for_value(A.dtype, other)
            zmc__hrgz = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), bnt__rsx)
            return zmc__hrgz
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        njc__mud = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(njc__mud)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    atp__tttl = cat_dtype.categories
    n = len(atp__tttl)
    for xktp__vkgv in range(n):
        if atp__tttl[xktp__vkgv] == val:
            return xktp__vkgv
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    nppdb__auyfu = bodo.utils.typing.parse_dtype(dtype,
        'CategoricalArray.astype')
    if (nppdb__auyfu != A.dtype.elem_type and nppdb__auyfu != types.
        unicode_type):
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if nppdb__auyfu == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            zmc__hrgz = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for xktp__vkgv in numba.parfors.parfor.internal_prange(n):
                doras__ckivz = codes[xktp__vkgv]
                if doras__ckivz == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(zmc__hrgz,
                            xktp__vkgv)
                    else:
                        bodo.libs.array_kernels.setna(zmc__hrgz, xktp__vkgv)
                    continue
                zmc__hrgz[xktp__vkgv] = str(bodo.utils.conversion.
                    unbox_if_tz_naive_timestamp(categories[doras__ckivz]))
            return zmc__hrgz
        return impl
    bvjx__xmtj = dtype_to_array_type(nppdb__auyfu)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        zmc__hrgz = bodo.utils.utils.alloc_type(n, bvjx__xmtj, (-1,))
        for xktp__vkgv in numba.parfors.parfor.internal_prange(n):
            doras__ckivz = codes[xktp__vkgv]
            if doras__ckivz == -1:
                bodo.libs.array_kernels.setna(zmc__hrgz, xktp__vkgv)
                continue
            zmc__hrgz[xktp__vkgv
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                categories[doras__ckivz])
        return zmc__hrgz
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        tzbms__zgooy, lbl__yllr = args
        atp__tttl = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        atp__tttl.codes = tzbms__zgooy
        atp__tttl.dtype = lbl__yllr
        context.nrt.incref(builder, signature.args[0], tzbms__zgooy)
        context.nrt.incref(builder, signature.args[1], lbl__yllr)
        return atp__tttl._getvalue()
    jwbl__unry = CategoricalArrayType(cat_dtype)
    sig = jwbl__unry(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    tpn__fbmwt = args[0]
    if equiv_set.has_shape(tpn__fbmwt):
        return ArrayAnalysis.AnalyzeResult(shape=tpn__fbmwt, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    yqrc__kdt = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, yqrc__kdt)
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
            dckch__uzn = {}
            sagh__wbt = np.empty(n + 1, np.int64)
            xem__ewuq = {}
            vexh__bjxe = []
            xag__wixm = {}
            for xktp__vkgv in range(n):
                xag__wixm[categories[xktp__vkgv]] = xktp__vkgv
            for avde__luzip in to_replace:
                if avde__luzip != value:
                    if avde__luzip in xag__wixm:
                        if value in xag__wixm:
                            dckch__uzn[avde__luzip] = avde__luzip
                            bbo__xslks = xag__wixm[avde__luzip]
                            xem__ewuq[bbo__xslks] = xag__wixm[value]
                            vexh__bjxe.append(bbo__xslks)
                        else:
                            dckch__uzn[avde__luzip] = value
                            xag__wixm[value] = xag__wixm[avde__luzip]
            ebbs__uhvxk = np.sort(np.array(vexh__bjxe))
            xulo__lnc = 0
            nahi__pkggk = []
            for aic__gfwhi in range(-1, n):
                while xulo__lnc < len(ebbs__uhvxk
                    ) and aic__gfwhi > ebbs__uhvxk[xulo__lnc]:
                    xulo__lnc += 1
                nahi__pkggk.append(xulo__lnc)
            for krh__pxrns in range(-1, n):
                gayf__tdq = krh__pxrns
                if krh__pxrns in xem__ewuq:
                    gayf__tdq = xem__ewuq[krh__pxrns]
                sagh__wbt[krh__pxrns + 1] = gayf__tdq - nahi__pkggk[
                    gayf__tdq + 1]
            return dckch__uzn, sagh__wbt, len(ebbs__uhvxk)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for xktp__vkgv in range(len(new_codes_arr)):
        new_codes_arr[xktp__vkgv] = codes_map_arr[old_codes_arr[xktp__vkgv] + 1
            ]


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
    qkwva__uqic = arr.dtype.ordered
    ndsk__pqd = arr.dtype.elem_type
    uvt__sjhil = get_overload_const(to_replace)
    bwlt__app = get_overload_const(value)
    if (arr.dtype.categories is not None and uvt__sjhil is not NOT_CONSTANT and
        bwlt__app is not NOT_CONSTANT):
        ytq__qkaw, codes_map_arr, wosp__qxe = python_build_replace_dicts(
            uvt__sjhil, bwlt__app, arr.dtype.categories)
        if len(ytq__qkaw) == 0:
            return lambda arr, to_replace, value: arr.copy()
        jslob__ackuv = []
        for nfenc__lodvj in arr.dtype.categories:
            if nfenc__lodvj in ytq__qkaw:
                cmp__xnsel = ytq__qkaw[nfenc__lodvj]
                if cmp__xnsel != nfenc__lodvj:
                    jslob__ackuv.append(cmp__xnsel)
            else:
                jslob__ackuv.append(nfenc__lodvj)
        cse__qpni = bodo.utils.utils.create_categorical_type(jslob__ackuv,
            arr.dtype.data.data, qkwva__uqic)
        ddmpk__ewc = MetaType(tuple(cse__qpni))

        def impl_dtype(arr, to_replace, value):
            nskgm__tqstu = init_cat_dtype(bodo.utils.conversion.
                index_from_array(cse__qpni), qkwva__uqic, None, ddmpk__ewc)
            atp__tttl = alloc_categorical_array(len(arr.codes), nskgm__tqstu)
            reassign_codes(atp__tttl.codes, arr.codes, codes_map_arr)
            return atp__tttl
        return impl_dtype
    ndsk__pqd = arr.dtype.elem_type
    if ndsk__pqd == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            dckch__uzn, codes_map_arr, ojodt__lwy = build_replace_dicts(
                to_replace, value, categories.values)
            if len(dckch__uzn) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), qkwva__uqic,
                    None, None))
            n = len(categories)
            cse__qpni = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                ojodt__lwy, -1)
            psm__edmg = 0
            for aic__gfwhi in range(n):
                tjis__ykol = categories[aic__gfwhi]
                if tjis__ykol in dckch__uzn:
                    ityoi__wtmlo = dckch__uzn[tjis__ykol]
                    if ityoi__wtmlo != tjis__ykol:
                        cse__qpni[psm__edmg] = ityoi__wtmlo
                        psm__edmg += 1
                else:
                    cse__qpni[psm__edmg] = tjis__ykol
                    psm__edmg += 1
            atp__tttl = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                cse__qpni), qkwva__uqic, None, None))
            reassign_codes(atp__tttl.codes, arr.codes, codes_map_arr)
            return atp__tttl
        return impl_str
    mzfy__urf = dtype_to_array_type(ndsk__pqd)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        dckch__uzn, codes_map_arr, ojodt__lwy = build_replace_dicts(to_replace,
            value, categories.values)
        if len(dckch__uzn) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), qkwva__uqic, None, None))
        n = len(categories)
        cse__qpni = bodo.utils.utils.alloc_type(n - ojodt__lwy, mzfy__urf, None
            )
        psm__edmg = 0
        for xktp__vkgv in range(n):
            tjis__ykol = categories[xktp__vkgv]
            if tjis__ykol in dckch__uzn:
                ityoi__wtmlo = dckch__uzn[tjis__ykol]
                if ityoi__wtmlo != tjis__ykol:
                    cse__qpni[psm__edmg] = ityoi__wtmlo
                    psm__edmg += 1
            else:
                cse__qpni[psm__edmg] = tjis__ykol
                psm__edmg += 1
        atp__tttl = alloc_categorical_array(len(arr.codes), init_cat_dtype(
            bodo.utils.conversion.index_from_array(cse__qpni), qkwva__uqic,
            None, None))
        reassign_codes(atp__tttl.codes, arr.codes, codes_map_arr)
        return atp__tttl
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
    vrs__isnx = dict()
    yun__tbrkd = 0
    for xktp__vkgv in range(len(vals)):
        val = vals[xktp__vkgv]
        if val in vrs__isnx:
            continue
        vrs__isnx[val] = yun__tbrkd
        yun__tbrkd += 1
    return vrs__isnx


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    vrs__isnx = dict()
    for xktp__vkgv in range(len(vals)):
        val = vals[xktp__vkgv]
        vrs__isnx[val] = xktp__vkgv
    return vrs__isnx


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    bori__zlc = dict(fastpath=fastpath)
    qctxh__oux = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', bori__zlc, qctxh__oux)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        tgb__gje = get_overload_const(categories)
        if tgb__gje is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                lpjz__doev = False
            else:
                lpjz__doev = get_overload_const_bool(ordered)
            mnl__gypz = pd.CategoricalDtype(pd.array(tgb__gje), lpjz__doev
                ).categories.array
            zfz__pwmzj = MetaType(tuple(mnl__gypz))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                nskgm__tqstu = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(mnl__gypz), lpjz__doev, None, zfz__pwmzj)
                return bodo.utils.conversion.fix_arr_dtype(data, nskgm__tqstu)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            uuext__dhm = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                uuext__dhm, ordered, None, None)
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
            ynn__rok = arr.codes[ind]
            return arr.dtype.categories[max(ynn__rok, 0)]
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
    for xktp__vkgv in range(len(arr1)):
        if arr1[xktp__vkgv] != arr2[xktp__vkgv]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    gnkmy__yyoqk = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    wqj__ytj = not isinstance(val, CategoricalArrayType) and is_iterable_type(
        val) and is_common_scalar_dtype([val.dtype, arr.dtype.elem_type]
        ) and not (isinstance(arr.dtype.elem_type, types.Integer) and
        isinstance(val.dtype, types.Float))
    qpy__kddj = categorical_arrs_match(arr, val)
    rexqs__crr = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    aqxt__xymf = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not gnkmy__yyoqk:
            raise BodoError(rexqs__crr)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            ynn__rok = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = ynn__rok
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (gnkmy__yyoqk or wqj__ytj or qpy__kddj !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(rexqs__crr)
        if qpy__kddj == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(aqxt__xymf)
        if gnkmy__yyoqk:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                emom__sed = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for aic__gfwhi in range(n):
                    arr.codes[ind[aic__gfwhi]] = emom__sed
            return impl_scalar
        if qpy__kddj == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for xktp__vkgv in range(n):
                    arr.codes[ind[xktp__vkgv]] = val.codes[xktp__vkgv]
            return impl_arr_ind_mask
        if qpy__kddj == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(aqxt__xymf)
                n = len(val.codes)
                for xktp__vkgv in range(n):
                    arr.codes[ind[xktp__vkgv]] = val.codes[xktp__vkgv]
            return impl_arr_ind_mask
        if wqj__ytj:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for aic__gfwhi in range(n):
                    dmej__rngx = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[aic__gfwhi]))
                    if dmej__rngx not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    ynn__rok = categories.get_loc(dmej__rngx)
                    arr.codes[ind[aic__gfwhi]] = ynn__rok
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (gnkmy__yyoqk or wqj__ytj or qpy__kddj !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(rexqs__crr)
        if qpy__kddj == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(aqxt__xymf)
        if gnkmy__yyoqk:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                emom__sed = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for aic__gfwhi in range(n):
                    if ind[aic__gfwhi]:
                        arr.codes[aic__gfwhi] = emom__sed
            return impl_scalar
        if qpy__kddj == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                dcby__xwhls = 0
                for xktp__vkgv in range(n):
                    if ind[xktp__vkgv]:
                        arr.codes[xktp__vkgv] = val.codes[dcby__xwhls]
                        dcby__xwhls += 1
            return impl_bool_ind_mask
        if qpy__kddj == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(aqxt__xymf)
                n = len(ind)
                dcby__xwhls = 0
                for xktp__vkgv in range(n):
                    if ind[xktp__vkgv]:
                        arr.codes[xktp__vkgv] = val.codes[dcby__xwhls]
                        dcby__xwhls += 1
            return impl_bool_ind_mask
        if wqj__ytj:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                dcby__xwhls = 0
                categories = arr.dtype.categories
                for aic__gfwhi in range(n):
                    if ind[aic__gfwhi]:
                        dmej__rngx = (bodo.utils.conversion.
                            unbox_if_tz_naive_timestamp(val[dcby__xwhls]))
                        if dmej__rngx not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        ynn__rok = categories.get_loc(dmej__rngx)
                        arr.codes[aic__gfwhi] = ynn__rok
                        dcby__xwhls += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (gnkmy__yyoqk or wqj__ytj or qpy__kddj !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(rexqs__crr)
        if qpy__kddj == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(aqxt__xymf)
        if gnkmy__yyoqk:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                emom__sed = arr.dtype.categories.get_loc(val)
                yeshm__apzaq = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for aic__gfwhi in range(yeshm__apzaq.start, yeshm__apzaq.
                    stop, yeshm__apzaq.step):
                    arr.codes[aic__gfwhi] = emom__sed
            return impl_scalar
        if qpy__kddj == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if qpy__kddj == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(aqxt__xymf)
                arr.codes[ind] = val.codes
            return impl_arr
        if wqj__ytj:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                yeshm__apzaq = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                dcby__xwhls = 0
                for aic__gfwhi in range(yeshm__apzaq.start, yeshm__apzaq.
                    stop, yeshm__apzaq.step):
                    dmej__rngx = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[dcby__xwhls]))
                    if dmej__rngx not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    ynn__rok = categories.get_loc(dmej__rngx)
                    arr.codes[aic__gfwhi] = ynn__rok
                    dcby__xwhls += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
