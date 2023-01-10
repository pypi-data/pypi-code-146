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
        ugvy__gzh = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=ugvy__gzh)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    ynka__powmp = tuple(val.categories.values)
    elem_type = None if len(ynka__powmp) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(ynka__powmp, elem_type, val.ordered, bodo.
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
        vjks__fpej = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, vjks__fpej)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    abz__nmqr = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    xtace__urkdb = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, vbpg__klp, vbpg__klp = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    unvvn__amihu = PDCategoricalDtype(xtace__urkdb, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, abz__nmqr)
    return unvvn__amihu(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    rpfp__vuipr = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, rpfp__vuipr).value
    c.pyapi.decref(rpfp__vuipr)
    lsyvx__dvsj = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, lsyvx__dvsj).value
    c.pyapi.decref(lsyvx__dvsj)
    urgd__srw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=urgd__srw)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    rpfp__vuipr = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    cassr__ctgvj = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    jdftq__regf = c.context.insert_const_string(c.builder.module, 'pandas')
    pbbn__mrtfp = c.pyapi.import_module_noblock(jdftq__regf)
    ysv__xhs = c.pyapi.call_method(pbbn__mrtfp, 'CategoricalDtype', (
        cassr__ctgvj, rpfp__vuipr))
    c.pyapi.decref(rpfp__vuipr)
    c.pyapi.decref(cassr__ctgvj)
    c.pyapi.decref(pbbn__mrtfp)
    c.context.nrt.decref(c.builder, typ, val)
    return ysv__xhs


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
        khmvk__twusn = get_categories_int_type(fe_type.dtype)
        vjks__fpej = [('dtype', fe_type.dtype), ('codes', types.Array(
            khmvk__twusn, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, vjks__fpej)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    herr__kqmqn = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), herr__kqmqn
        ).value
    c.pyapi.decref(herr__kqmqn)
    ysv__xhs = c.pyapi.object_getattr_string(val, 'dtype')
    akgv__crim = c.pyapi.to_native_value(typ.dtype, ysv__xhs).value
    c.pyapi.decref(ysv__xhs)
    lfq__geex = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lfq__geex.codes = codes
    lfq__geex.dtype = akgv__crim
    return NativeValue(lfq__geex._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    fzrq__srymh = get_categories_int_type(typ.dtype)
    figt__uyrvw = context.get_constant_generic(builder, types.Array(
        fzrq__srymh, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, figt__uyrvw])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    wien__lwh = len(cat_dtype.categories)
    if wien__lwh < np.iinfo(np.int8).max:
        dtype = types.int8
    elif wien__lwh < np.iinfo(np.int16).max:
        dtype = types.int16
    elif wien__lwh < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    jdftq__regf = c.context.insert_const_string(c.builder.module, 'pandas')
    pbbn__mrtfp = c.pyapi.import_module_noblock(jdftq__regf)
    khmvk__twusn = get_categories_int_type(dtype)
    yjdq__bwo = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    nkzj__hprm = types.Array(khmvk__twusn, 1, 'C')
    c.context.nrt.incref(c.builder, nkzj__hprm, yjdq__bwo.codes)
    herr__kqmqn = c.pyapi.from_native_value(nkzj__hprm, yjdq__bwo.codes, c.
        env_manager)
    c.context.nrt.incref(c.builder, dtype, yjdq__bwo.dtype)
    ysv__xhs = c.pyapi.from_native_value(dtype, yjdq__bwo.dtype, c.env_manager)
    htayz__jlq = c.pyapi.borrow_none()
    xta__ozs = c.pyapi.object_getattr_string(pbbn__mrtfp, 'Categorical')
    wlivh__ben = c.pyapi.call_method(xta__ozs, 'from_codes', (herr__kqmqn,
        htayz__jlq, htayz__jlq, ysv__xhs))
    c.pyapi.decref(xta__ozs)
    c.pyapi.decref(herr__kqmqn)
    c.pyapi.decref(ysv__xhs)
    c.pyapi.decref(pbbn__mrtfp)
    c.context.nrt.decref(c.builder, typ, val)
    return wlivh__ben


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
            zpeu__ymifh = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                lijip__nylu = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), zpeu__ymifh)
                return lijip__nylu
            return impl_lit

        def impl(A, other):
            zpeu__ymifh = get_code_for_value(A.dtype, other)
            lijip__nylu = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), zpeu__ymifh)
            return lijip__nylu
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        dluw__jfpz = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(dluw__jfpz)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    yjdq__bwo = cat_dtype.categories
    n = len(yjdq__bwo)
    for min__dcf in range(n):
        if yjdq__bwo[min__dcf] == val:
            return min__dcf
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    rvzvx__gaxrn = bodo.utils.typing.parse_dtype(dtype,
        'CategoricalArray.astype')
    if (rvzvx__gaxrn != A.dtype.elem_type and rvzvx__gaxrn != types.
        unicode_type):
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if rvzvx__gaxrn == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            lijip__nylu = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for min__dcf in numba.parfors.parfor.internal_prange(n):
                hce__dby = codes[min__dcf]
                if hce__dby == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(
                            lijip__nylu, min__dcf)
                    else:
                        bodo.libs.array_kernels.setna(lijip__nylu, min__dcf)
                    continue
                lijip__nylu[min__dcf] = str(bodo.utils.conversion.
                    unbox_if_tz_naive_timestamp(categories[hce__dby]))
            return lijip__nylu
        return impl
    nkzj__hprm = dtype_to_array_type(rvzvx__gaxrn)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        lijip__nylu = bodo.utils.utils.alloc_type(n, nkzj__hprm, (-1,))
        for min__dcf in numba.parfors.parfor.internal_prange(n):
            hce__dby = codes[min__dcf]
            if hce__dby == -1:
                bodo.libs.array_kernels.setna(lijip__nylu, min__dcf)
                continue
            lijip__nylu[min__dcf
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                categories[hce__dby])
        return lijip__nylu
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        nqv__pyqub, akgv__crim = args
        yjdq__bwo = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        yjdq__bwo.codes = nqv__pyqub
        yjdq__bwo.dtype = akgv__crim
        context.nrt.incref(builder, signature.args[0], nqv__pyqub)
        context.nrt.incref(builder, signature.args[1], akgv__crim)
        return yjdq__bwo._getvalue()
    dybiq__wefhi = CategoricalArrayType(cat_dtype)
    sig = dybiq__wefhi(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    rwaj__hngme = args[0]
    if equiv_set.has_shape(rwaj__hngme):
        return ArrayAnalysis.AnalyzeResult(shape=rwaj__hngme, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    khmvk__twusn = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, khmvk__twusn)
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
            xjfs__pydv = {}
            figt__uyrvw = np.empty(n + 1, np.int64)
            urnbz__bfjr = {}
            pzk__nmq = []
            qotf__mzm = {}
            for min__dcf in range(n):
                qotf__mzm[categories[min__dcf]] = min__dcf
            for tcxar__iouy in to_replace:
                if tcxar__iouy != value:
                    if tcxar__iouy in qotf__mzm:
                        if value in qotf__mzm:
                            xjfs__pydv[tcxar__iouy] = tcxar__iouy
                            gva__zjwk = qotf__mzm[tcxar__iouy]
                            urnbz__bfjr[gva__zjwk] = qotf__mzm[value]
                            pzk__nmq.append(gva__zjwk)
                        else:
                            xjfs__pydv[tcxar__iouy] = value
                            qotf__mzm[value] = qotf__mzm[tcxar__iouy]
            cgtc__llc = np.sort(np.array(pzk__nmq))
            xhhkk__kbo = 0
            qbhc__tcjk = []
            for dsk__onhb in range(-1, n):
                while xhhkk__kbo < len(cgtc__llc) and dsk__onhb > cgtc__llc[
                    xhhkk__kbo]:
                    xhhkk__kbo += 1
                qbhc__tcjk.append(xhhkk__kbo)
            for xysd__oaznl in range(-1, n):
                pct__iig = xysd__oaznl
                if xysd__oaznl in urnbz__bfjr:
                    pct__iig = urnbz__bfjr[xysd__oaznl]
                figt__uyrvw[xysd__oaznl + 1] = pct__iig - qbhc__tcjk[
                    pct__iig + 1]
            return xjfs__pydv, figt__uyrvw, len(cgtc__llc)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for min__dcf in range(len(new_codes_arr)):
        new_codes_arr[min__dcf] = codes_map_arr[old_codes_arr[min__dcf] + 1]


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
    zxhh__mvjv = arr.dtype.ordered
    xjg__bcj = arr.dtype.elem_type
    nivv__mubb = get_overload_const(to_replace)
    fsljv__mbi = get_overload_const(value)
    if (arr.dtype.categories is not None and nivv__mubb is not NOT_CONSTANT and
        fsljv__mbi is not NOT_CONSTANT):
        nseq__pzeey, codes_map_arr, vbpg__klp = python_build_replace_dicts(
            nivv__mubb, fsljv__mbi, arr.dtype.categories)
        if len(nseq__pzeey) == 0:
            return lambda arr, to_replace, value: arr.copy()
        sopq__mex = []
        for ycg__omxeb in arr.dtype.categories:
            if ycg__omxeb in nseq__pzeey:
                xhe__ztgw = nseq__pzeey[ycg__omxeb]
                if xhe__ztgw != ycg__omxeb:
                    sopq__mex.append(xhe__ztgw)
            else:
                sopq__mex.append(ycg__omxeb)
        ujtiw__iaqk = bodo.utils.utils.create_categorical_type(sopq__mex,
            arr.dtype.data.data, zxhh__mvjv)
        codv__svvp = MetaType(tuple(ujtiw__iaqk))

        def impl_dtype(arr, to_replace, value):
            fklje__syp = init_cat_dtype(bodo.utils.conversion.
                index_from_array(ujtiw__iaqk), zxhh__mvjv, None, codv__svvp)
            yjdq__bwo = alloc_categorical_array(len(arr.codes), fklje__syp)
            reassign_codes(yjdq__bwo.codes, arr.codes, codes_map_arr)
            return yjdq__bwo
        return impl_dtype
    xjg__bcj = arr.dtype.elem_type
    if xjg__bcj == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            xjfs__pydv, codes_map_arr, gkzgn__fpapr = build_replace_dicts(
                to_replace, value, categories.values)
            if len(xjfs__pydv) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), zxhh__mvjv,
                    None, None))
            n = len(categories)
            ujtiw__iaqk = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                gkzgn__fpapr, -1)
            vnosm__xnzul = 0
            for dsk__onhb in range(n):
                nssj__atyiw = categories[dsk__onhb]
                if nssj__atyiw in xjfs__pydv:
                    jeskz__rcw = xjfs__pydv[nssj__atyiw]
                    if jeskz__rcw != nssj__atyiw:
                        ujtiw__iaqk[vnosm__xnzul] = jeskz__rcw
                        vnosm__xnzul += 1
                else:
                    ujtiw__iaqk[vnosm__xnzul] = nssj__atyiw
                    vnosm__xnzul += 1
            yjdq__bwo = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                ujtiw__iaqk), zxhh__mvjv, None, None))
            reassign_codes(yjdq__bwo.codes, arr.codes, codes_map_arr)
            return yjdq__bwo
        return impl_str
    udq__smtan = dtype_to_array_type(xjg__bcj)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        xjfs__pydv, codes_map_arr, gkzgn__fpapr = build_replace_dicts(
            to_replace, value, categories.values)
        if len(xjfs__pydv) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), zxhh__mvjv, None, None))
        n = len(categories)
        ujtiw__iaqk = bodo.utils.utils.alloc_type(n - gkzgn__fpapr,
            udq__smtan, None)
        vnosm__xnzul = 0
        for min__dcf in range(n):
            nssj__atyiw = categories[min__dcf]
            if nssj__atyiw in xjfs__pydv:
                jeskz__rcw = xjfs__pydv[nssj__atyiw]
                if jeskz__rcw != nssj__atyiw:
                    ujtiw__iaqk[vnosm__xnzul] = jeskz__rcw
                    vnosm__xnzul += 1
            else:
                ujtiw__iaqk[vnosm__xnzul] = nssj__atyiw
                vnosm__xnzul += 1
        yjdq__bwo = alloc_categorical_array(len(arr.codes), init_cat_dtype(
            bodo.utils.conversion.index_from_array(ujtiw__iaqk), zxhh__mvjv,
            None, None))
        reassign_codes(yjdq__bwo.codes, arr.codes, codes_map_arr)
        return yjdq__bwo
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
    gjpq__yeb = dict()
    lqrdj__eua = 0
    for min__dcf in range(len(vals)):
        val = vals[min__dcf]
        if val in gjpq__yeb:
            continue
        gjpq__yeb[val] = lqrdj__eua
        lqrdj__eua += 1
    return gjpq__yeb


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    gjpq__yeb = dict()
    for min__dcf in range(len(vals)):
        val = vals[min__dcf]
        gjpq__yeb[val] = min__dcf
    return gjpq__yeb


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    rpvmi__aoimv = dict(fastpath=fastpath)
    pywc__pwps = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', rpvmi__aoimv, pywc__pwps)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        olws__yja = get_overload_const(categories)
        if olws__yja is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                cevn__uhptj = False
            else:
                cevn__uhptj = get_overload_const_bool(ordered)
            mvpx__dvqx = pd.CategoricalDtype(pd.array(olws__yja), cevn__uhptj
                ).categories.array
            usfda__uyjkm = MetaType(tuple(mvpx__dvqx))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                fklje__syp = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(mvpx__dvqx), cevn__uhptj, None,
                    usfda__uyjkm)
                return bodo.utils.conversion.fix_arr_dtype(data, fklje__syp)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            ynka__powmp = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                ynka__powmp, ordered, None, None)
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
            sgmmn__rdj = arr.codes[ind]
            return arr.dtype.categories[max(sgmmn__rdj, 0)]
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
    for min__dcf in range(len(arr1)):
        if arr1[min__dcf] != arr2[min__dcf]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    rjacp__nuz = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    zrm__kxjur = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    qpys__dsz = categorical_arrs_match(arr, val)
    ytfub__fbrq = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    ssy__ntbc = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not rjacp__nuz:
            raise BodoError(ytfub__fbrq)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            sgmmn__rdj = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = sgmmn__rdj
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (rjacp__nuz or zrm__kxjur or qpys__dsz !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ytfub__fbrq)
        if qpys__dsz == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(ssy__ntbc)
        if rjacp__nuz:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                lxl__xapqn = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for dsk__onhb in range(n):
                    arr.codes[ind[dsk__onhb]] = lxl__xapqn
            return impl_scalar
        if qpys__dsz == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for min__dcf in range(n):
                    arr.codes[ind[min__dcf]] = val.codes[min__dcf]
            return impl_arr_ind_mask
        if qpys__dsz == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(ssy__ntbc)
                n = len(val.codes)
                for min__dcf in range(n):
                    arr.codes[ind[min__dcf]] = val.codes[min__dcf]
            return impl_arr_ind_mask
        if zrm__kxjur:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for dsk__onhb in range(n):
                    abxf__xwbk = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[dsk__onhb]))
                    if abxf__xwbk not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    sgmmn__rdj = categories.get_loc(abxf__xwbk)
                    arr.codes[ind[dsk__onhb]] = sgmmn__rdj
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (rjacp__nuz or zrm__kxjur or qpys__dsz !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ytfub__fbrq)
        if qpys__dsz == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(ssy__ntbc)
        if rjacp__nuz:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                lxl__xapqn = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for dsk__onhb in range(n):
                    if ind[dsk__onhb]:
                        arr.codes[dsk__onhb] = lxl__xapqn
            return impl_scalar
        if qpys__dsz == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                yjupv__fsu = 0
                for min__dcf in range(n):
                    if ind[min__dcf]:
                        arr.codes[min__dcf] = val.codes[yjupv__fsu]
                        yjupv__fsu += 1
            return impl_bool_ind_mask
        if qpys__dsz == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(ssy__ntbc)
                n = len(ind)
                yjupv__fsu = 0
                for min__dcf in range(n):
                    if ind[min__dcf]:
                        arr.codes[min__dcf] = val.codes[yjupv__fsu]
                        yjupv__fsu += 1
            return impl_bool_ind_mask
        if zrm__kxjur:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                yjupv__fsu = 0
                categories = arr.dtype.categories
                for dsk__onhb in range(n):
                    if ind[dsk__onhb]:
                        abxf__xwbk = (bodo.utils.conversion.
                            unbox_if_tz_naive_timestamp(val[yjupv__fsu]))
                        if abxf__xwbk not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        sgmmn__rdj = categories.get_loc(abxf__xwbk)
                        arr.codes[dsk__onhb] = sgmmn__rdj
                        yjupv__fsu += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (rjacp__nuz or zrm__kxjur or qpys__dsz !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ytfub__fbrq)
        if qpys__dsz == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(ssy__ntbc)
        if rjacp__nuz:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                lxl__xapqn = arr.dtype.categories.get_loc(val)
                vel__osq = numba.cpython.unicode._normalize_slice(ind, len(arr)
                    )
                for dsk__onhb in range(vel__osq.start, vel__osq.stop,
                    vel__osq.step):
                    arr.codes[dsk__onhb] = lxl__xapqn
            return impl_scalar
        if qpys__dsz == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if qpys__dsz == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(ssy__ntbc)
                arr.codes[ind] = val.codes
            return impl_arr
        if zrm__kxjur:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                vel__osq = numba.cpython.unicode._normalize_slice(ind, len(arr)
                    )
                yjupv__fsu = 0
                for dsk__onhb in range(vel__osq.start, vel__osq.stop,
                    vel__osq.step):
                    abxf__xwbk = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[yjupv__fsu]))
                    if abxf__xwbk not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    sgmmn__rdj = categories.get_loc(abxf__xwbk)
                    arr.codes[dsk__onhb] = sgmmn__rdj
                    yjupv__fsu += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
