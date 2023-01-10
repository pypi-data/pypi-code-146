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
        wsif__hziqd = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=wsif__hziqd)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    qfbu__nuuz = tuple(val.categories.values)
    elem_type = None if len(qfbu__nuuz) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(qfbu__nuuz, elem_type, val.ordered, bodo.
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
        yltd__lch = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, yltd__lch)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    meyz__jnkb = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    kmv__rkzj = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, zho__ajf, zho__ajf = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    llez__eqb = PDCategoricalDtype(kmv__rkzj, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, meyz__jnkb)
    return llez__eqb(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    efwt__dio = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, efwt__dio).value
    c.pyapi.decref(efwt__dio)
    hgqe__rlinu = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, hgqe__rlinu).value
    c.pyapi.decref(hgqe__rlinu)
    thcwv__hrgm = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=thcwv__hrgm)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    efwt__dio = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    wuf__hsgg = c.pyapi.from_native_value(typ.data, cat_dtype.categories, c
        .env_manager)
    zqmjs__qbqp = c.context.insert_const_string(c.builder.module, 'pandas')
    ayugf__cvk = c.pyapi.import_module_noblock(zqmjs__qbqp)
    zhe__kki = c.pyapi.call_method(ayugf__cvk, 'CategoricalDtype', (
        wuf__hsgg, efwt__dio))
    c.pyapi.decref(efwt__dio)
    c.pyapi.decref(wuf__hsgg)
    c.pyapi.decref(ayugf__cvk)
    c.context.nrt.decref(c.builder, typ, val)
    return zhe__kki


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
        owls__reruo = get_categories_int_type(fe_type.dtype)
        yltd__lch = [('dtype', fe_type.dtype), ('codes', types.Array(
            owls__reruo, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, yltd__lch)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    pjsh__oui = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), pjsh__oui
        ).value
    c.pyapi.decref(pjsh__oui)
    zhe__kki = c.pyapi.object_getattr_string(val, 'dtype')
    jga__vaumj = c.pyapi.to_native_value(typ.dtype, zhe__kki).value
    c.pyapi.decref(zhe__kki)
    pjyul__vrsbk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    pjyul__vrsbk.codes = codes
    pjyul__vrsbk.dtype = jga__vaumj
    return NativeValue(pjyul__vrsbk._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    byi__ppdwa = get_categories_int_type(typ.dtype)
    qonl__lzyg = context.get_constant_generic(builder, types.Array(
        byi__ppdwa, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, qonl__lzyg])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    ckhh__kuvk = len(cat_dtype.categories)
    if ckhh__kuvk < np.iinfo(np.int8).max:
        dtype = types.int8
    elif ckhh__kuvk < np.iinfo(np.int16).max:
        dtype = types.int16
    elif ckhh__kuvk < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    zqmjs__qbqp = c.context.insert_const_string(c.builder.module, 'pandas')
    ayugf__cvk = c.pyapi.import_module_noblock(zqmjs__qbqp)
    owls__reruo = get_categories_int_type(dtype)
    gga__lbobh = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    bacfw__yktq = types.Array(owls__reruo, 1, 'C')
    c.context.nrt.incref(c.builder, bacfw__yktq, gga__lbobh.codes)
    pjsh__oui = c.pyapi.from_native_value(bacfw__yktq, gga__lbobh.codes, c.
        env_manager)
    c.context.nrt.incref(c.builder, dtype, gga__lbobh.dtype)
    zhe__kki = c.pyapi.from_native_value(dtype, gga__lbobh.dtype, c.env_manager
        )
    karx__xfda = c.pyapi.borrow_none()
    rsgr__cakmd = c.pyapi.object_getattr_string(ayugf__cvk, 'Categorical')
    odako__whej = c.pyapi.call_method(rsgr__cakmd, 'from_codes', (pjsh__oui,
        karx__xfda, karx__xfda, zhe__kki))
    c.pyapi.decref(rsgr__cakmd)
    c.pyapi.decref(pjsh__oui)
    c.pyapi.decref(zhe__kki)
    c.pyapi.decref(ayugf__cvk)
    c.context.nrt.decref(c.builder, typ, val)
    return odako__whej


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
            tugy__aufz = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                tew__vcutm = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), tugy__aufz)
                return tew__vcutm
            return impl_lit

        def impl(A, other):
            tugy__aufz = get_code_for_value(A.dtype, other)
            tew__vcutm = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), tugy__aufz)
            return tew__vcutm
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        cgmbl__hvcgt = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(cgmbl__hvcgt)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    gga__lbobh = cat_dtype.categories
    n = len(gga__lbobh)
    for qerxp__junwn in range(n):
        if gga__lbobh[qerxp__junwn] == val:
            return qerxp__junwn
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    hroi__llfdv = bodo.utils.typing.parse_dtype(dtype,
        'CategoricalArray.astype')
    if hroi__llfdv != A.dtype.elem_type and hroi__llfdv != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if hroi__llfdv == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            tew__vcutm = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for qerxp__junwn in numba.parfors.parfor.internal_prange(n):
                utae__qmk = codes[qerxp__junwn]
                if utae__qmk == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(tew__vcutm
                            , qerxp__junwn)
                    else:
                        bodo.libs.array_kernels.setna(tew__vcutm, qerxp__junwn)
                    continue
                tew__vcutm[qerxp__junwn] = str(bodo.utils.conversion.
                    unbox_if_tz_naive_timestamp(categories[utae__qmk]))
            return tew__vcutm
        return impl
    bacfw__yktq = dtype_to_array_type(hroi__llfdv)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        tew__vcutm = bodo.utils.utils.alloc_type(n, bacfw__yktq, (-1,))
        for qerxp__junwn in numba.parfors.parfor.internal_prange(n):
            utae__qmk = codes[qerxp__junwn]
            if utae__qmk == -1:
                bodo.libs.array_kernels.setna(tew__vcutm, qerxp__junwn)
                continue
            tew__vcutm[qerxp__junwn
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                categories[utae__qmk])
        return tew__vcutm
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        fbtrc__smlco, jga__vaumj = args
        gga__lbobh = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        gga__lbobh.codes = fbtrc__smlco
        gga__lbobh.dtype = jga__vaumj
        context.nrt.incref(builder, signature.args[0], fbtrc__smlco)
        context.nrt.incref(builder, signature.args[1], jga__vaumj)
        return gga__lbobh._getvalue()
    kys__uuw = CategoricalArrayType(cat_dtype)
    sig = kys__uuw(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    pas__cxwj = args[0]
    if equiv_set.has_shape(pas__cxwj):
        return ArrayAnalysis.AnalyzeResult(shape=pas__cxwj, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    owls__reruo = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, owls__reruo)
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
            wofxm__mpus = {}
            qonl__lzyg = np.empty(n + 1, np.int64)
            rbidh__lqsn = {}
            xwf__ipoz = []
            wlnpf__bcmb = {}
            for qerxp__junwn in range(n):
                wlnpf__bcmb[categories[qerxp__junwn]] = qerxp__junwn
            for kqvu__vjlg in to_replace:
                if kqvu__vjlg != value:
                    if kqvu__vjlg in wlnpf__bcmb:
                        if value in wlnpf__bcmb:
                            wofxm__mpus[kqvu__vjlg] = kqvu__vjlg
                            hoc__hxz = wlnpf__bcmb[kqvu__vjlg]
                            rbidh__lqsn[hoc__hxz] = wlnpf__bcmb[value]
                            xwf__ipoz.append(hoc__hxz)
                        else:
                            wofxm__mpus[kqvu__vjlg] = value
                            wlnpf__bcmb[value] = wlnpf__bcmb[kqvu__vjlg]
            aon__lxmsn = np.sort(np.array(xwf__ipoz))
            vrh__kzt = 0
            dusu__lxyrm = []
            for afne__jsfuy in range(-1, n):
                while vrh__kzt < len(aon__lxmsn) and afne__jsfuy > aon__lxmsn[
                    vrh__kzt]:
                    vrh__kzt += 1
                dusu__lxyrm.append(vrh__kzt)
            for pyqoh__vzbwp in range(-1, n):
                nmz__qkhl = pyqoh__vzbwp
                if pyqoh__vzbwp in rbidh__lqsn:
                    nmz__qkhl = rbidh__lqsn[pyqoh__vzbwp]
                qonl__lzyg[pyqoh__vzbwp + 1] = nmz__qkhl - dusu__lxyrm[
                    nmz__qkhl + 1]
            return wofxm__mpus, qonl__lzyg, len(aon__lxmsn)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for qerxp__junwn in range(len(new_codes_arr)):
        new_codes_arr[qerxp__junwn] = codes_map_arr[old_codes_arr[
            qerxp__junwn] + 1]


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
    rqf__cjjd = arr.dtype.ordered
    hyml__rebgs = arr.dtype.elem_type
    cqmwq__xei = get_overload_const(to_replace)
    tehj__hzjbc = get_overload_const(value)
    if (arr.dtype.categories is not None and cqmwq__xei is not NOT_CONSTANT and
        tehj__hzjbc is not NOT_CONSTANT):
        ukag__bhm, codes_map_arr, zho__ajf = python_build_replace_dicts(
            cqmwq__xei, tehj__hzjbc, arr.dtype.categories)
        if len(ukag__bhm) == 0:
            return lambda arr, to_replace, value: arr.copy()
        cafc__titwb = []
        for ssdnx__fdgkn in arr.dtype.categories:
            if ssdnx__fdgkn in ukag__bhm:
                taef__ymt = ukag__bhm[ssdnx__fdgkn]
                if taef__ymt != ssdnx__fdgkn:
                    cafc__titwb.append(taef__ymt)
            else:
                cafc__titwb.append(ssdnx__fdgkn)
        fnzqx__xmxz = bodo.utils.utils.create_categorical_type(cafc__titwb,
            arr.dtype.data.data, rqf__cjjd)
        ieauv__gbue = MetaType(tuple(fnzqx__xmxz))

        def impl_dtype(arr, to_replace, value):
            wjg__lpv = init_cat_dtype(bodo.utils.conversion.
                index_from_array(fnzqx__xmxz), rqf__cjjd, None, ieauv__gbue)
            gga__lbobh = alloc_categorical_array(len(arr.codes), wjg__lpv)
            reassign_codes(gga__lbobh.codes, arr.codes, codes_map_arr)
            return gga__lbobh
        return impl_dtype
    hyml__rebgs = arr.dtype.elem_type
    if hyml__rebgs == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            wofxm__mpus, codes_map_arr, pogd__qex = build_replace_dicts(
                to_replace, value, categories.values)
            if len(wofxm__mpus) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), rqf__cjjd,
                    None, None))
            n = len(categories)
            fnzqx__xmxz = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                pogd__qex, -1)
            jem__enta = 0
            for afne__jsfuy in range(n):
                cbzgg__tycre = categories[afne__jsfuy]
                if cbzgg__tycre in wofxm__mpus:
                    udz__epxiu = wofxm__mpus[cbzgg__tycre]
                    if udz__epxiu != cbzgg__tycre:
                        fnzqx__xmxz[jem__enta] = udz__epxiu
                        jem__enta += 1
                else:
                    fnzqx__xmxz[jem__enta] = cbzgg__tycre
                    jem__enta += 1
            gga__lbobh = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                fnzqx__xmxz), rqf__cjjd, None, None))
            reassign_codes(gga__lbobh.codes, arr.codes, codes_map_arr)
            return gga__lbobh
        return impl_str
    qccy__xag = dtype_to_array_type(hyml__rebgs)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        wofxm__mpus, codes_map_arr, pogd__qex = build_replace_dicts(to_replace,
            value, categories.values)
        if len(wofxm__mpus) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), rqf__cjjd, None, None))
        n = len(categories)
        fnzqx__xmxz = bodo.utils.utils.alloc_type(n - pogd__qex, qccy__xag,
            None)
        jem__enta = 0
        for qerxp__junwn in range(n):
            cbzgg__tycre = categories[qerxp__junwn]
            if cbzgg__tycre in wofxm__mpus:
                udz__epxiu = wofxm__mpus[cbzgg__tycre]
                if udz__epxiu != cbzgg__tycre:
                    fnzqx__xmxz[jem__enta] = udz__epxiu
                    jem__enta += 1
            else:
                fnzqx__xmxz[jem__enta] = cbzgg__tycre
                jem__enta += 1
        gga__lbobh = alloc_categorical_array(len(arr.codes), init_cat_dtype
            (bodo.utils.conversion.index_from_array(fnzqx__xmxz), rqf__cjjd,
            None, None))
        reassign_codes(gga__lbobh.codes, arr.codes, codes_map_arr)
        return gga__lbobh
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
    zbw__wgb = dict()
    nqlhq__fbesn = 0
    for qerxp__junwn in range(len(vals)):
        val = vals[qerxp__junwn]
        if val in zbw__wgb:
            continue
        zbw__wgb[val] = nqlhq__fbesn
        nqlhq__fbesn += 1
    return zbw__wgb


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    zbw__wgb = dict()
    for qerxp__junwn in range(len(vals)):
        val = vals[qerxp__junwn]
        zbw__wgb[val] = qerxp__junwn
    return zbw__wgb


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    wuj__mrqwc = dict(fastpath=fastpath)
    xlwp__pozm = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', wuj__mrqwc, xlwp__pozm)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        juca__upfs = get_overload_const(categories)
        if juca__upfs is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                itjy__bqzs = False
            else:
                itjy__bqzs = get_overload_const_bool(ordered)
            zhvrm__ekzg = pd.CategoricalDtype(pd.array(juca__upfs), itjy__bqzs
                ).categories.array
            rou__khfu = MetaType(tuple(zhvrm__ekzg))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                wjg__lpv = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(zhvrm__ekzg), itjy__bqzs, None, rou__khfu)
                return bodo.utils.conversion.fix_arr_dtype(data, wjg__lpv)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            qfbu__nuuz = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                qfbu__nuuz, ordered, None, None)
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
            jicqa__lbin = arr.codes[ind]
            return arr.dtype.categories[max(jicqa__lbin, 0)]
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
    for qerxp__junwn in range(len(arr1)):
        if arr1[qerxp__junwn] != arr2[qerxp__junwn]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    buc__ykk = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    bzf__hjzvg = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    mdcqo__gpay = categorical_arrs_match(arr, val)
    jjv__gloj = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    leh__olsq = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not buc__ykk:
            raise BodoError(jjv__gloj)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            jicqa__lbin = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = jicqa__lbin
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (buc__ykk or bzf__hjzvg or mdcqo__gpay !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(jjv__gloj)
        if mdcqo__gpay == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(leh__olsq)
        if buc__ykk:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                dgfiz__wdvor = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for afne__jsfuy in range(n):
                    arr.codes[ind[afne__jsfuy]] = dgfiz__wdvor
            return impl_scalar
        if mdcqo__gpay == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for qerxp__junwn in range(n):
                    arr.codes[ind[qerxp__junwn]] = val.codes[qerxp__junwn]
            return impl_arr_ind_mask
        if mdcqo__gpay == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(leh__olsq)
                n = len(val.codes)
                for qerxp__junwn in range(n):
                    arr.codes[ind[qerxp__junwn]] = val.codes[qerxp__junwn]
            return impl_arr_ind_mask
        if bzf__hjzvg:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for afne__jsfuy in range(n):
                    umxuo__ans = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[afne__jsfuy]))
                    if umxuo__ans not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    jicqa__lbin = categories.get_loc(umxuo__ans)
                    arr.codes[ind[afne__jsfuy]] = jicqa__lbin
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (buc__ykk or bzf__hjzvg or mdcqo__gpay !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(jjv__gloj)
        if mdcqo__gpay == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(leh__olsq)
        if buc__ykk:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                dgfiz__wdvor = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for afne__jsfuy in range(n):
                    if ind[afne__jsfuy]:
                        arr.codes[afne__jsfuy] = dgfiz__wdvor
            return impl_scalar
        if mdcqo__gpay == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                hpmxb__gvqi = 0
                for qerxp__junwn in range(n):
                    if ind[qerxp__junwn]:
                        arr.codes[qerxp__junwn] = val.codes[hpmxb__gvqi]
                        hpmxb__gvqi += 1
            return impl_bool_ind_mask
        if mdcqo__gpay == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(leh__olsq)
                n = len(ind)
                hpmxb__gvqi = 0
                for qerxp__junwn in range(n):
                    if ind[qerxp__junwn]:
                        arr.codes[qerxp__junwn] = val.codes[hpmxb__gvqi]
                        hpmxb__gvqi += 1
            return impl_bool_ind_mask
        if bzf__hjzvg:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                hpmxb__gvqi = 0
                categories = arr.dtype.categories
                for afne__jsfuy in range(n):
                    if ind[afne__jsfuy]:
                        umxuo__ans = (bodo.utils.conversion.
                            unbox_if_tz_naive_timestamp(val[hpmxb__gvqi]))
                        if umxuo__ans not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        jicqa__lbin = categories.get_loc(umxuo__ans)
                        arr.codes[afne__jsfuy] = jicqa__lbin
                        hpmxb__gvqi += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (buc__ykk or bzf__hjzvg or mdcqo__gpay !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(jjv__gloj)
        if mdcqo__gpay == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(leh__olsq)
        if buc__ykk:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                dgfiz__wdvor = arr.dtype.categories.get_loc(val)
                xqq__gaw = numba.cpython.unicode._normalize_slice(ind, len(arr)
                    )
                for afne__jsfuy in range(xqq__gaw.start, xqq__gaw.stop,
                    xqq__gaw.step):
                    arr.codes[afne__jsfuy] = dgfiz__wdvor
            return impl_scalar
        if mdcqo__gpay == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if mdcqo__gpay == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(leh__olsq)
                arr.codes[ind] = val.codes
            return impl_arr
        if bzf__hjzvg:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                xqq__gaw = numba.cpython.unicode._normalize_slice(ind, len(arr)
                    )
                hpmxb__gvqi = 0
                for afne__jsfuy in range(xqq__gaw.start, xqq__gaw.stop,
                    xqq__gaw.step):
                    umxuo__ans = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[hpmxb__gvqi]))
                    if umxuo__ans not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    jicqa__lbin = categories.get_loc(umxuo__ans)
                    arr.codes[afne__jsfuy] = jicqa__lbin
                    hpmxb__gvqi += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
