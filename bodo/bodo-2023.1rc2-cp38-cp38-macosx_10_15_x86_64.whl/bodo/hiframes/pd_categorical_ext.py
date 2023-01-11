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
        lac__oxwi = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=lac__oxwi)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    hzwcl__fjsh = tuple(val.categories.values)
    elem_type = None if len(hzwcl__fjsh) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(hzwcl__fjsh, elem_type, val.ordered, bodo.
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
        gnjb__axalq = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, gnjb__axalq)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    hmvy__jqulp = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    vof__gmwqx = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, ppu__brzsg, ppu__brzsg = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    ilgf__qzvma = PDCategoricalDtype(vof__gmwqx, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, hmvy__jqulp)
    return ilgf__qzvma(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fkg__nmcik = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, fkg__nmcik).value
    c.pyapi.decref(fkg__nmcik)
    atftv__ncrfw = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, atftv__ncrfw
        ).value
    c.pyapi.decref(atftv__ncrfw)
    ijx__ysc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=ijx__ysc)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    fkg__nmcik = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    jwv__aautf = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    zaikw__iga = c.context.insert_const_string(c.builder.module, 'pandas')
    dhf__vqxms = c.pyapi.import_module_noblock(zaikw__iga)
    pgg__lff = c.pyapi.call_method(dhf__vqxms, 'CategoricalDtype', (
        jwv__aautf, fkg__nmcik))
    c.pyapi.decref(fkg__nmcik)
    c.pyapi.decref(jwv__aautf)
    c.pyapi.decref(dhf__vqxms)
    c.context.nrt.decref(c.builder, typ, val)
    return pgg__lff


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
        jjvwj__cse = get_categories_int_type(fe_type.dtype)
        gnjb__axalq = [('dtype', fe_type.dtype), ('codes', types.Array(
            jjvwj__cse, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, gnjb__axalq)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    ohy__xdi = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), ohy__xdi).value
    c.pyapi.decref(ohy__xdi)
    pgg__lff = c.pyapi.object_getattr_string(val, 'dtype')
    djkuo__itw = c.pyapi.to_native_value(typ.dtype, pgg__lff).value
    c.pyapi.decref(pgg__lff)
    wpw__ggqk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    wpw__ggqk.codes = codes
    wpw__ggqk.dtype = djkuo__itw
    return NativeValue(wpw__ggqk._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    zpo__hyc = get_categories_int_type(typ.dtype)
    gzh__feeb = context.get_constant_generic(builder, types.Array(zpo__hyc,
        1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, gzh__feeb])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    mik__mbr = len(cat_dtype.categories)
    if mik__mbr < np.iinfo(np.int8).max:
        dtype = types.int8
    elif mik__mbr < np.iinfo(np.int16).max:
        dtype = types.int16
    elif mik__mbr < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    zaikw__iga = c.context.insert_const_string(c.builder.module, 'pandas')
    dhf__vqxms = c.pyapi.import_module_noblock(zaikw__iga)
    jjvwj__cse = get_categories_int_type(dtype)
    aom__bau = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    bexhs__zlkzb = types.Array(jjvwj__cse, 1, 'C')
    c.context.nrt.incref(c.builder, bexhs__zlkzb, aom__bau.codes)
    ohy__xdi = c.pyapi.from_native_value(bexhs__zlkzb, aom__bau.codes, c.
        env_manager)
    c.context.nrt.incref(c.builder, dtype, aom__bau.dtype)
    pgg__lff = c.pyapi.from_native_value(dtype, aom__bau.dtype, c.env_manager)
    xwqgk__nyx = c.pyapi.borrow_none()
    kgmnj__belq = c.pyapi.object_getattr_string(dhf__vqxms, 'Categorical')
    vxydi__yjbw = c.pyapi.call_method(kgmnj__belq, 'from_codes', (ohy__xdi,
        xwqgk__nyx, xwqgk__nyx, pgg__lff))
    c.pyapi.decref(kgmnj__belq)
    c.pyapi.decref(ohy__xdi)
    c.pyapi.decref(pgg__lff)
    c.pyapi.decref(dhf__vqxms)
    c.context.nrt.decref(c.builder, typ, val)
    return vxydi__yjbw


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
            zvbyn__wxqax = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                pas__qlbup = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), zvbyn__wxqax)
                return pas__qlbup
            return impl_lit

        def impl(A, other):
            zvbyn__wxqax = get_code_for_value(A.dtype, other)
            pas__qlbup = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), zvbyn__wxqax)
            return pas__qlbup
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        uflh__khc = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(uflh__khc)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    aom__bau = cat_dtype.categories
    n = len(aom__bau)
    for vee__bsr in range(n):
        if aom__bau[vee__bsr] == val:
            return vee__bsr
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    uazs__roll = bodo.utils.typing.parse_dtype(dtype, 'CategoricalArray.astype'
        )
    if uazs__roll != A.dtype.elem_type and uazs__roll != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if uazs__roll == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            pas__qlbup = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for vee__bsr in numba.parfors.parfor.internal_prange(n):
                vazar__yisoe = codes[vee__bsr]
                if vazar__yisoe == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(pas__qlbup
                            , vee__bsr)
                    else:
                        bodo.libs.array_kernels.setna(pas__qlbup, vee__bsr)
                    continue
                pas__qlbup[vee__bsr] = str(bodo.utils.conversion.
                    unbox_if_tz_naive_timestamp(categories[vazar__yisoe]))
            return pas__qlbup
        return impl
    bexhs__zlkzb = dtype_to_array_type(uazs__roll)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        pas__qlbup = bodo.utils.utils.alloc_type(n, bexhs__zlkzb, (-1,))
        for vee__bsr in numba.parfors.parfor.internal_prange(n):
            vazar__yisoe = codes[vee__bsr]
            if vazar__yisoe == -1:
                bodo.libs.array_kernels.setna(pas__qlbup, vee__bsr)
                continue
            pas__qlbup[vee__bsr
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                categories[vazar__yisoe])
        return pas__qlbup
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        hohxd__tba, djkuo__itw = args
        aom__bau = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        aom__bau.codes = hohxd__tba
        aom__bau.dtype = djkuo__itw
        context.nrt.incref(builder, signature.args[0], hohxd__tba)
        context.nrt.incref(builder, signature.args[1], djkuo__itw)
        return aom__bau._getvalue()
    uee__crd = CategoricalArrayType(cat_dtype)
    sig = uee__crd(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    ccnxk__opog = args[0]
    if equiv_set.has_shape(ccnxk__opog):
        return ArrayAnalysis.AnalyzeResult(shape=ccnxk__opog, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    jjvwj__cse = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, jjvwj__cse)
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
            pyi__smv = {}
            gzh__feeb = np.empty(n + 1, np.int64)
            aprz__nmbz = {}
            abgbk__gqank = []
            afi__cmpoq = {}
            for vee__bsr in range(n):
                afi__cmpoq[categories[vee__bsr]] = vee__bsr
            for wbv__zegm in to_replace:
                if wbv__zegm != value:
                    if wbv__zegm in afi__cmpoq:
                        if value in afi__cmpoq:
                            pyi__smv[wbv__zegm] = wbv__zegm
                            kua__qiezl = afi__cmpoq[wbv__zegm]
                            aprz__nmbz[kua__qiezl] = afi__cmpoq[value]
                            abgbk__gqank.append(kua__qiezl)
                        else:
                            pyi__smv[wbv__zegm] = value
                            afi__cmpoq[value] = afi__cmpoq[wbv__zegm]
            nngzx__nnx = np.sort(np.array(abgbk__gqank))
            wztmv__acnz = 0
            xjhay__jpv = []
            for fclu__ifzi in range(-1, n):
                while wztmv__acnz < len(nngzx__nnx
                    ) and fclu__ifzi > nngzx__nnx[wztmv__acnz]:
                    wztmv__acnz += 1
                xjhay__jpv.append(wztmv__acnz)
            for rvaa__nuetp in range(-1, n):
                iyu__esq = rvaa__nuetp
                if rvaa__nuetp in aprz__nmbz:
                    iyu__esq = aprz__nmbz[rvaa__nuetp]
                gzh__feeb[rvaa__nuetp + 1] = iyu__esq - xjhay__jpv[iyu__esq + 1
                    ]
            return pyi__smv, gzh__feeb, len(nngzx__nnx)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for vee__bsr in range(len(new_codes_arr)):
        new_codes_arr[vee__bsr] = codes_map_arr[old_codes_arr[vee__bsr] + 1]


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
    qtza__ctv = arr.dtype.ordered
    hwoh__gju = arr.dtype.elem_type
    wiats__swix = get_overload_const(to_replace)
    zbr__ztfd = get_overload_const(value)
    if (arr.dtype.categories is not None and wiats__swix is not
        NOT_CONSTANT and zbr__ztfd is not NOT_CONSTANT):
        cwuf__dgwjx, codes_map_arr, ppu__brzsg = python_build_replace_dicts(
            wiats__swix, zbr__ztfd, arr.dtype.categories)
        if len(cwuf__dgwjx) == 0:
            return lambda arr, to_replace, value: arr.copy()
        ysk__eebn = []
        for zwdh__pkfd in arr.dtype.categories:
            if zwdh__pkfd in cwuf__dgwjx:
                hrrq__kinrj = cwuf__dgwjx[zwdh__pkfd]
                if hrrq__kinrj != zwdh__pkfd:
                    ysk__eebn.append(hrrq__kinrj)
            else:
                ysk__eebn.append(zwdh__pkfd)
        jwfm__iin = bodo.utils.utils.create_categorical_type(ysk__eebn, arr
            .dtype.data.data, qtza__ctv)
        vyqq__aeti = MetaType(tuple(jwfm__iin))

        def impl_dtype(arr, to_replace, value):
            eizyp__epsa = init_cat_dtype(bodo.utils.conversion.
                index_from_array(jwfm__iin), qtza__ctv, None, vyqq__aeti)
            aom__bau = alloc_categorical_array(len(arr.codes), eizyp__epsa)
            reassign_codes(aom__bau.codes, arr.codes, codes_map_arr)
            return aom__bau
        return impl_dtype
    hwoh__gju = arr.dtype.elem_type
    if hwoh__gju == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            pyi__smv, codes_map_arr, dopc__khwnd = build_replace_dicts(
                to_replace, value, categories.values)
            if len(pyi__smv) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), qtza__ctv,
                    None, None))
            n = len(categories)
            jwfm__iin = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                dopc__khwnd, -1)
            mbei__eiqwq = 0
            for fclu__ifzi in range(n):
                cicp__dbha = categories[fclu__ifzi]
                if cicp__dbha in pyi__smv:
                    qqqhv__jbjvy = pyi__smv[cicp__dbha]
                    if qqqhv__jbjvy != cicp__dbha:
                        jwfm__iin[mbei__eiqwq] = qqqhv__jbjvy
                        mbei__eiqwq += 1
                else:
                    jwfm__iin[mbei__eiqwq] = cicp__dbha
                    mbei__eiqwq += 1
            aom__bau = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                jwfm__iin), qtza__ctv, None, None))
            reassign_codes(aom__bau.codes, arr.codes, codes_map_arr)
            return aom__bau
        return impl_str
    cklzu__plvby = dtype_to_array_type(hwoh__gju)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        pyi__smv, codes_map_arr, dopc__khwnd = build_replace_dicts(to_replace,
            value, categories.values)
        if len(pyi__smv) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), qtza__ctv, None, None))
        n = len(categories)
        jwfm__iin = bodo.utils.utils.alloc_type(n - dopc__khwnd,
            cklzu__plvby, None)
        mbei__eiqwq = 0
        for vee__bsr in range(n):
            cicp__dbha = categories[vee__bsr]
            if cicp__dbha in pyi__smv:
                qqqhv__jbjvy = pyi__smv[cicp__dbha]
                if qqqhv__jbjvy != cicp__dbha:
                    jwfm__iin[mbei__eiqwq] = qqqhv__jbjvy
                    mbei__eiqwq += 1
            else:
                jwfm__iin[mbei__eiqwq] = cicp__dbha
                mbei__eiqwq += 1
        aom__bau = alloc_categorical_array(len(arr.codes), init_cat_dtype(
            bodo.utils.conversion.index_from_array(jwfm__iin), qtza__ctv,
            None, None))
        reassign_codes(aom__bau.codes, arr.codes, codes_map_arr)
        return aom__bau
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
    ili__guaf = dict()
    enod__jsixw = 0
    for vee__bsr in range(len(vals)):
        val = vals[vee__bsr]
        if val in ili__guaf:
            continue
        ili__guaf[val] = enod__jsixw
        enod__jsixw += 1
    return ili__guaf


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    ili__guaf = dict()
    for vee__bsr in range(len(vals)):
        val = vals[vee__bsr]
        ili__guaf[val] = vee__bsr
    return ili__guaf


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    pix__gmjy = dict(fastpath=fastpath)
    wnl__axyl = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', pix__gmjy, wnl__axyl)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        ratln__joz = get_overload_const(categories)
        if ratln__joz is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                lgft__dcafm = False
            else:
                lgft__dcafm = get_overload_const_bool(ordered)
            dbw__zwb = pd.CategoricalDtype(pd.array(ratln__joz), lgft__dcafm
                ).categories.array
            hix__hgmc = MetaType(tuple(dbw__zwb))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                eizyp__epsa = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(dbw__zwb), lgft__dcafm, None, hix__hgmc)
                return bodo.utils.conversion.fix_arr_dtype(data, eizyp__epsa)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            hzwcl__fjsh = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                hzwcl__fjsh, ordered, None, None)
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
            tldvn__yuxae = arr.codes[ind]
            return arr.dtype.categories[max(tldvn__yuxae, 0)]
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
    for vee__bsr in range(len(arr1)):
        if arr1[vee__bsr] != arr2[vee__bsr]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    bisz__cwar = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    kpnqh__uoebo = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    dlkj__qupah = categorical_arrs_match(arr, val)
    ztb__zcbl = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    oun__yxuj = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not bisz__cwar:
            raise BodoError(ztb__zcbl)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            tldvn__yuxae = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = tldvn__yuxae
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (bisz__cwar or kpnqh__uoebo or dlkj__qupah !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ztb__zcbl)
        if dlkj__qupah == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(oun__yxuj)
        if bisz__cwar:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                iqx__tqvj = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for fclu__ifzi in range(n):
                    arr.codes[ind[fclu__ifzi]] = iqx__tqvj
            return impl_scalar
        if dlkj__qupah == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for vee__bsr in range(n):
                    arr.codes[ind[vee__bsr]] = val.codes[vee__bsr]
            return impl_arr_ind_mask
        if dlkj__qupah == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(oun__yxuj)
                n = len(val.codes)
                for vee__bsr in range(n):
                    arr.codes[ind[vee__bsr]] = val.codes[vee__bsr]
            return impl_arr_ind_mask
        if kpnqh__uoebo:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for fclu__ifzi in range(n):
                    vaxf__payh = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[fclu__ifzi]))
                    if vaxf__payh not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    tldvn__yuxae = categories.get_loc(vaxf__payh)
                    arr.codes[ind[fclu__ifzi]] = tldvn__yuxae
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (bisz__cwar or kpnqh__uoebo or dlkj__qupah !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ztb__zcbl)
        if dlkj__qupah == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(oun__yxuj)
        if bisz__cwar:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                iqx__tqvj = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for fclu__ifzi in range(n):
                    if ind[fclu__ifzi]:
                        arr.codes[fclu__ifzi] = iqx__tqvj
            return impl_scalar
        if dlkj__qupah == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                zlty__qaru = 0
                for vee__bsr in range(n):
                    if ind[vee__bsr]:
                        arr.codes[vee__bsr] = val.codes[zlty__qaru]
                        zlty__qaru += 1
            return impl_bool_ind_mask
        if dlkj__qupah == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(oun__yxuj)
                n = len(ind)
                zlty__qaru = 0
                for vee__bsr in range(n):
                    if ind[vee__bsr]:
                        arr.codes[vee__bsr] = val.codes[zlty__qaru]
                        zlty__qaru += 1
            return impl_bool_ind_mask
        if kpnqh__uoebo:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                zlty__qaru = 0
                categories = arr.dtype.categories
                for fclu__ifzi in range(n):
                    if ind[fclu__ifzi]:
                        vaxf__payh = (bodo.utils.conversion.
                            unbox_if_tz_naive_timestamp(val[zlty__qaru]))
                        if vaxf__payh not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        tldvn__yuxae = categories.get_loc(vaxf__payh)
                        arr.codes[fclu__ifzi] = tldvn__yuxae
                        zlty__qaru += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (bisz__cwar or kpnqh__uoebo or dlkj__qupah !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ztb__zcbl)
        if dlkj__qupah == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(oun__yxuj)
        if bisz__cwar:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                iqx__tqvj = arr.dtype.categories.get_loc(val)
                tzzch__wcaif = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for fclu__ifzi in range(tzzch__wcaif.start, tzzch__wcaif.
                    stop, tzzch__wcaif.step):
                    arr.codes[fclu__ifzi] = iqx__tqvj
            return impl_scalar
        if dlkj__qupah == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if dlkj__qupah == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(oun__yxuj)
                arr.codes[ind] = val.codes
            return impl_arr
        if kpnqh__uoebo:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                tzzch__wcaif = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                zlty__qaru = 0
                for fclu__ifzi in range(tzzch__wcaif.start, tzzch__wcaif.
                    stop, tzzch__wcaif.step):
                    vaxf__payh = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[zlty__qaru]))
                    if vaxf__payh not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    tldvn__yuxae = categories.get_loc(vaxf__payh)
                    arr.codes[fclu__ifzi] = tldvn__yuxae
                    zlty__qaru += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
