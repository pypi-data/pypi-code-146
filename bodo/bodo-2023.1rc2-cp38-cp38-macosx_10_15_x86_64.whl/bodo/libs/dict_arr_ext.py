"""Dictionary encoded array data type, similar to DictionaryArray of Arrow.
The purpose is to improve memory consumption and performance over string_array_type for
string arrays that have a lot of repetitive values (typical in practice).
Can be extended to be used with types other than strings as well.
See:
https://bodo.atlassian.net/browse/BE-2295
https://bodo.atlassian.net/wiki/spaces/B/pages/993722369/Dictionary-encoded+String+Array+Support+in+Parquet+read+compute+...
https://arrow.apache.org/docs/cpp/api/array.html#dictionary-encoded
"""
import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_new_ref, lower_builtin, lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
import bodo
from bodo.libs import hstr_ext
from bodo.libs.bool_arr_ext import init_bool_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, get_str_arr_item_length, overload_str_arr_astype, pre_alloc_string_array, string_array_type
from bodo.utils.typing import BodoArrayIterator, is_overload_none, raise_bodo_error
from bodo.utils.utils import synchronize_error_njit
ll.add_symbol('box_dict_str_array', hstr_ext.box_dict_str_array)
dict_indices_arr_type = IntegerArrayType(types.int32)


class DictionaryArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self, arr_data_type):
        self.data = arr_data_type
        super(DictionaryArrayType, self).__init__(name=
            f'DictionaryArrayType({arr_data_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    @property
    def dtype(self):
        return self.data.dtype

    def copy(self):
        return DictionaryArrayType(self.data)

    @property
    def indices_type(self):
        return dict_indices_arr_type

    @property
    def indices_dtype(self):
        return dict_indices_arr_type.dtype

    def unify(self, typingctx, other):
        if other == string_array_type:
            return string_array_type


dict_str_arr_type = DictionaryArrayType(string_array_type)


@register_model(DictionaryArrayType)
class DictionaryArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vlvh__fjgo = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_),
            ('has_deduped_local_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, vlvh__fjgo)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
make_attribute_wrapper(DictionaryArrayType, 'has_deduped_local_dictionary',
    '_has_deduped_local_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t, unique_dict_t):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        xcljc__tgdne, dtsb__hwp, taqtr__kvjxg, snluv__pgzcc = args
        ngsi__nhop = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        ngsi__nhop.data = xcljc__tgdne
        ngsi__nhop.indices = dtsb__hwp
        ngsi__nhop.has_global_dictionary = taqtr__kvjxg
        ngsi__nhop.has_deduped_local_dictionary = snluv__pgzcc
        context.nrt.incref(builder, signature.args[0], xcljc__tgdne)
        context.nrt.incref(builder, signature.args[1], dtsb__hwp)
        return ngsi__nhop._getvalue()
    jfh__hastr = DictionaryArrayType(data_t)
    bwwh__lfj = jfh__hastr(data_t, indices_t, types.bool_, types.bool_)
    return bwwh__lfj, codegen


@typeof_impl.register(pa.DictionaryArray)
def typeof_dict_value(val, c):
    if val.type.value_type == pa.string():
        return dict_str_arr_type


def to_pa_dict_arr(A):
    if isinstance(A, pa.DictionaryArray):
        return A
    if isinstance(A, pd.arrays.ArrowStringArray) and pa.types.is_dictionary(A
        ._data.type) and (pa.types.is_string(A._data.type.value_type) or pa
        .types.is_large_string(A._data.type.value_type)) and pa.types.is_int32(
        A._data.type.index_type):
        return A._data.combine_chunks()
    return pd.array(A, 'string[pyarrow]')._data.combine_chunks(
        ).dictionary_encode()


@unbox(DictionaryArrayType)
def unbox_dict_arr(typ, val, c):
    tei__ztajz = c.pyapi.unserialize(c.pyapi.serialize_object(to_pa_dict_arr))
    val = c.pyapi.call_function_objargs(tei__ztajz, [val])
    c.pyapi.decref(tei__ztajz)
    ngsi__nhop = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hgdm__jgi = c.pyapi.object_getattr_string(val, 'dictionary')
    bczwn__rvdga = c.pyapi.bool_from_bool(c.context.get_constant(types.
        bool_, False))
    pyvw__uvfe = c.pyapi.call_method(hgdm__jgi, 'to_numpy', (bczwn__rvdga,))
    ngsi__nhop.data = c.unbox(typ.data, pyvw__uvfe).value
    qfwx__knbs = c.pyapi.object_getattr_string(val, 'indices')
    ejxne__yxs = c.context.insert_const_string(c.builder.module, 'pandas')
    bucoo__dtmyl = c.pyapi.import_module_noblock(ejxne__yxs)
    usic__fru = c.pyapi.string_from_constant_string('Int32')
    wau__wazc = c.pyapi.call_method(bucoo__dtmyl, 'array', (qfwx__knbs,
        usic__fru))
    ngsi__nhop.indices = c.unbox(dict_indices_arr_type, wau__wazc).value
    ngsi__nhop.has_global_dictionary = c.context.get_constant(types.bool_, 
        False)
    ngsi__nhop.has_deduped_local_dictionary = c.context.get_constant(types.
        bool_, False)
    c.pyapi.decref(hgdm__jgi)
    c.pyapi.decref(bczwn__rvdga)
    c.pyapi.decref(pyvw__uvfe)
    c.pyapi.decref(qfwx__knbs)
    c.pyapi.decref(bucoo__dtmyl)
    c.pyapi.decref(usic__fru)
    c.pyapi.decref(wau__wazc)
    c.pyapi.decref(val)
    elr__bdcr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ngsi__nhop._getvalue(), is_error=elr__bdcr)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    ngsi__nhop = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        if bodo.libs.str_arr_ext.use_pd_pyarrow_string_array:
            from bodo.libs.array import array_info_type, array_to_info_codegen
            dop__blil = array_to_info_codegen(c.context, c.builder,
                array_info_type(typ), (val,), incref=False)
            xlyce__wevlh = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
                as_pointer()])
            gblq__gubg = 'pd_pyarrow_array_from_string_array'
            onveg__efd = cgutils.get_or_insert_function(c.builder.module,
                xlyce__wevlh, name=gblq__gubg)
            arr = c.builder.call(onveg__efd, [dop__blil])
            c.context.nrt.decref(c.builder, typ, val)
            return arr
        c.context.nrt.incref(c.builder, typ.data, ngsi__nhop.data)
        lwt__rirw = c.box(typ.data, ngsi__nhop.data)
        nwjzh__men = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, ngsi__nhop.indices)
        xlyce__wevlh = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        onveg__efd = cgutils.get_or_insert_function(c.builder.module,
            xlyce__wevlh, name='box_dict_str_array')
        gmeoz__pzo = cgutils.create_struct_proxy(types.Array(types.int32, 1,
            'C'))(c.context, c.builder, nwjzh__men.data)
        ivq__yksbn = c.builder.extract_value(gmeoz__pzo.shape, 0)
        oikz__njkh = gmeoz__pzo.data
        jpps__adwrc = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, nwjzh__men.null_bitmap).data
        pyvw__uvfe = c.builder.call(onveg__efd, [ivq__yksbn, lwt__rirw,
            oikz__njkh, jpps__adwrc])
        c.pyapi.decref(lwt__rirw)
    else:
        ejxne__yxs = c.context.insert_const_string(c.builder.module, 'pyarrow')
        szc__axm = c.pyapi.import_module_noblock(ejxne__yxs)
        rkjj__czrn = c.pyapi.object_getattr_string(szc__axm, 'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, ngsi__nhop.data)
        lwt__rirw = c.box(typ.data, ngsi__nhop.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, ngsi__nhop.
            indices)
        qfwx__knbs = c.box(dict_indices_arr_type, ngsi__nhop.indices)
        tqoj__jsmne = c.pyapi.call_method(rkjj__czrn, 'from_arrays', (
            qfwx__knbs, lwt__rirw))
        bczwn__rvdga = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        pyvw__uvfe = c.pyapi.call_method(tqoj__jsmne, 'to_numpy', (
            bczwn__rvdga,))
        c.pyapi.decref(szc__axm)
        c.pyapi.decref(lwt__rirw)
        c.pyapi.decref(qfwx__knbs)
        c.pyapi.decref(rkjj__czrn)
        c.pyapi.decref(tqoj__jsmne)
        c.pyapi.decref(bczwn__rvdga)
    c.context.nrt.decref(c.builder, typ, val)
    return pyvw__uvfe


@overload(len, no_unliteral=True)
def overload_dict_arr_len(A):
    if isinstance(A, DictionaryArrayType):
        return lambda A: len(A._indices)


@overload_attribute(DictionaryArrayType, 'shape')
def overload_dict_arr_shape(A):
    return lambda A: (len(A._indices),)


@overload_attribute(DictionaryArrayType, 'ndim')
def overload_dict_arr_ndim(A):
    return lambda A: 1


@overload_attribute(DictionaryArrayType, 'size')
def overload_dict_arr_size(A):
    return lambda A: len(A._indices)


@overload_method(DictionaryArrayType, 'tolist', no_unliteral=True)
def overload_dict_arr_tolist(A):
    return lambda A: list(A)


overload_method(DictionaryArrayType, 'astype', no_unliteral=True)(
    overload_str_arr_astype)


@overload_method(DictionaryArrayType, 'copy', no_unliteral=True)
def overload_dict_arr_copy(A):

    def copy_impl(A):
        return init_dict_arr(A._data.copy(), A._indices.copy(), A.
            _has_global_dictionary, A._has_deduped_local_dictionary)
    return copy_impl


@overload_attribute(DictionaryArrayType, 'dtype')
def overload_dict_arr_dtype(A):
    return lambda A: A._data.dtype


@overload_attribute(DictionaryArrayType, 'nbytes')
def dict_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._indices.nbytes


@lower_constant(DictionaryArrayType)
def lower_constant_dict_arr(context, builder, typ, pyval):
    if bodo.hiframes.boxing._use_dict_str_type and isinstance(pyval, np.ndarray
        ):
        pyval = pa.array(pyval).dictionary_encode()
    betq__oul = pyval.dictionary.to_numpy(False)
    uqoz__vbqi = pd.array(pyval.indices, 'Int32')
    betq__oul = context.get_constant_generic(builder, typ.data, betq__oul)
    uqoz__vbqi = context.get_constant_generic(builder,
        dict_indices_arr_type, uqoz__vbqi)
    lzj__qdvu = context.get_constant(types.bool_, False)
    ngj__lvjb = context.get_constant(types.bool_, False)
    szl__frh = lir.Constant.literal_struct([betq__oul, uqoz__vbqi,
        lzj__qdvu, ngj__lvjb])
    return szl__frh


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            nhm__dtxau = A._indices[ind]
            return A._data[nhm__dtxau]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary, A._has_deduped_local_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        xcljc__tgdne = A._data
        dtsb__hwp = A._indices
        ivq__yksbn = len(dtsb__hwp)
        arts__egjsh = [get_str_arr_item_length(xcljc__tgdne, i) for i in
            range(len(xcljc__tgdne))]
        iic__mod = 0
        for i in range(ivq__yksbn):
            if not bodo.libs.array_kernels.isna(dtsb__hwp, i):
                iic__mod += arts__egjsh[dtsb__hwp[i]]
        bgiq__bxsvc = pre_alloc_string_array(ivq__yksbn, iic__mod)
        for i in range(ivq__yksbn):
            if bodo.libs.array_kernels.isna(dtsb__hwp, i):
                bodo.libs.array_kernels.setna(bgiq__bxsvc, i)
                continue
            ind = dtsb__hwp[i]
            if bodo.libs.array_kernels.isna(xcljc__tgdne, ind):
                bodo.libs.array_kernels.setna(bgiq__bxsvc, i)
                continue
            bgiq__bxsvc[i] = xcljc__tgdne[ind]
        return bgiq__bxsvc
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_unique(arr, val):
    nhm__dtxau = -1
    xcljc__tgdne = arr._data
    for i in range(len(xcljc__tgdne)):
        if bodo.libs.array_kernels.isna(xcljc__tgdne, i):
            continue
        if xcljc__tgdne[i] == val:
            nhm__dtxau = i
            break
    return nhm__dtxau


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_non_unique(arr, val):
    weunc__snu = set()
    xcljc__tgdne = arr._data
    for i in range(len(xcljc__tgdne)):
        if bodo.libs.array_kernels.isna(xcljc__tgdne, i):
            continue
        if xcljc__tgdne[i] == val:
            weunc__snu.add(i)
    return weunc__snu


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    ivq__yksbn = len(arr)
    if arr._has_deduped_local_dictionary:
        nhm__dtxau = find_dict_ind_unique(arr, val)
        if nhm__dtxau == -1:
            return init_bool_array(np.full(ivq__yksbn, False, np.bool_),
                arr._indices._null_bitmap.copy())
        return arr._indices == nhm__dtxau
    else:
        mup__wmbyd = find_dict_ind_non_unique(arr, val)
        if len(mup__wmbyd) == 0:
            return init_bool_array(np.full(ivq__yksbn, False, np.bool_),
                arr._indices._null_bitmap.copy())
        homvb__dxy = np.empty(ivq__yksbn, dtype=np.bool_)
        for i in range(len(arr._indices)):
            homvb__dxy[i] = arr._indices[i] in mup__wmbyd
        return init_bool_array(homvb__dxy, arr._indices._null_bitmap.copy())


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    ivq__yksbn = len(arr)
    if arr._has_deduped_local_dictionary:
        nhm__dtxau = find_dict_ind_unique(arr, val)
        if nhm__dtxau == -1:
            return init_bool_array(np.full(ivq__yksbn, True, np.bool_), arr
                ._indices._null_bitmap.copy())
        return arr._indices != nhm__dtxau
    else:
        mup__wmbyd = find_dict_ind_non_unique(arr, val)
        if len(mup__wmbyd) == 0:
            return init_bool_array(np.full(ivq__yksbn, True, np.bool_), arr
                ._indices._null_bitmap.copy())
        homvb__dxy = np.empty(ivq__yksbn, dtype=np.bool_)
        for i in range(len(arr._indices)):
            homvb__dxy[i] = arr._indices[i] not in mup__wmbyd
        return init_bool_array(homvb__dxy, arr._indices._null_bitmap.copy())


def get_binary_op_overload(op, lhs, rhs):
    if op == operator.eq:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_eq(lhs, rhs
                )
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_eq(rhs, lhs
                )
    if op == operator.ne:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_ne(lhs, rhs
                )
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_ne(rhs, lhs
                )


def convert_dict_arr_to_int(arr, dtype):
    return arr


@overload(convert_dict_arr_to_int)
def convert_dict_arr_to_int_overload(arr, dtype):

    def impl(arr, dtype):
        kwp__hgts = arr._data
        bnqgz__whhmc = bodo.libs.int_arr_ext.alloc_int_array(len(kwp__hgts),
            dtype)
        for xre__ardrg in range(len(kwp__hgts)):
            if bodo.libs.array_kernels.isna(kwp__hgts, xre__ardrg):
                bodo.libs.array_kernels.setna(bnqgz__whhmc, xre__ardrg)
                continue
            bnqgz__whhmc[xre__ardrg] = np.int64(kwp__hgts[xre__ardrg])
        ivq__yksbn = len(arr)
        dtsb__hwp = arr._indices
        bgiq__bxsvc = bodo.libs.int_arr_ext.alloc_int_array(ivq__yksbn, dtype)
        for i in range(ivq__yksbn):
            if bodo.libs.array_kernels.isna(dtsb__hwp, i):
                bodo.libs.array_kernels.setna(bgiq__bxsvc, i)
                continue
            bgiq__bxsvc[i] = bnqgz__whhmc[dtsb__hwp[i]]
        return bgiq__bxsvc
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    jsd__jwb = len(arrs)
    ugw__yvwae = 'def impl(arrs, sep):\n'
    ugw__yvwae += '  ind_map = {}\n'
    ugw__yvwae += '  out_strs = []\n'
    ugw__yvwae += '  n = len(arrs[0])\n'
    for i in range(jsd__jwb):
        ugw__yvwae += f'  indices{i} = arrs[{i}]._indices\n'
    for i in range(jsd__jwb):
        ugw__yvwae += f'  data{i} = arrs[{i}]._data\n'
    ugw__yvwae += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    ugw__yvwae += '  for i in range(n):\n'
    vyw__tkwh = ' or '.join([f'bodo.libs.array_kernels.isna(arrs[{i}], i)' for
        i in range(jsd__jwb)])
    ugw__yvwae += f'    if {vyw__tkwh}:\n'
    ugw__yvwae += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    ugw__yvwae += '      continue\n'
    for i in range(jsd__jwb):
        ugw__yvwae += f'    ind{i} = indices{i}[i]\n'
    weiw__whdqv = '(' + ', '.join(f'ind{i}' for i in range(jsd__jwb)) + ')'
    ugw__yvwae += f'    if {weiw__whdqv} not in ind_map:\n'
    ugw__yvwae += '      out_ind = len(out_strs)\n'
    ugw__yvwae += f'      ind_map[{weiw__whdqv}] = out_ind\n'
    bsz__sxct = "''" if is_overload_none(sep) else 'sep'
    hrkk__txh = ', '.join([f'data{i}[ind{i}]' for i in range(jsd__jwb)])
    ugw__yvwae += f'      v = {bsz__sxct}.join([{hrkk__txh}])\n'
    ugw__yvwae += '      out_strs.append(v)\n'
    ugw__yvwae += '    else:\n'
    ugw__yvwae += f'      out_ind = ind_map[{weiw__whdqv}]\n'
    ugw__yvwae += '    out_indices[i] = out_ind\n'
    ugw__yvwae += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    ugw__yvwae += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False, False)
"""
    zob__jkh = {}
    exec(ugw__yvwae, {'bodo': bodo, 'numba': numba, 'np': np}, zob__jkh)
    impl = zob__jkh['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    ywczp__scm = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    bwwh__lfj = toty(fromty)
    uchmr__cnpz = context.compile_internal(builder, ywczp__scm, bwwh__lfj,
        (val,))
    return impl_ret_new_ref(context, builder, toty, uchmr__cnpz)


@register_jitable
def dict_arr_to_numeric(arr, errors, downcast):
    ngsi__nhop = arr._data
    dict_arr_out = pd.to_numeric(ngsi__nhop, errors, downcast)
    uqoz__vbqi = arr._indices
    tova__neh = len(uqoz__vbqi)
    bgiq__bxsvc = bodo.utils.utils.alloc_type(tova__neh, dict_arr_out, (-1,))
    for i in range(tova__neh):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(bgiq__bxsvc, i)
            continue
        nhm__dtxau = uqoz__vbqi[i]
        if bodo.libs.array_kernels.isna(dict_arr_out, nhm__dtxau):
            bodo.libs.array_kernels.setna(bgiq__bxsvc, i)
            continue
        bgiq__bxsvc[i] = dict_arr_out[nhm__dtxau]
    return bgiq__bxsvc


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    betq__oul = arr._data
    ycd__fdigz = len(betq__oul)
    hiwv__qyus = pre_alloc_string_array(ycd__fdigz, -1)
    if regex:
        jlpb__cdfq = re.compile(pat, flags)
        for i in range(ycd__fdigz):
            if bodo.libs.array_kernels.isna(betq__oul, i):
                bodo.libs.array_kernels.setna(hiwv__qyus, i)
                continue
            hiwv__qyus[i] = jlpb__cdfq.sub(repl=repl, string=betq__oul[i])
    else:
        for i in range(ycd__fdigz):
            if bodo.libs.array_kernels.isna(betq__oul, i):
                bodo.libs.array_kernels.setna(hiwv__qyus, i)
                continue
            hiwv__qyus[i] = betq__oul[i].replace(pat, repl)
    return init_dict_arr(hiwv__qyus, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_startswith(arr, pat, na):
    ngsi__nhop = arr._data
    ziqdh__dmwki = len(ngsi__nhop)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(ziqdh__dmwki)
    for i in range(ziqdh__dmwki):
        dict_arr_out[i] = ngsi__nhop[i].startswith(pat)
    uqoz__vbqi = arr._indices
    tova__neh = len(uqoz__vbqi)
    bgiq__bxsvc = bodo.libs.bool_arr_ext.alloc_bool_array(tova__neh)
    for i in range(tova__neh):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(bgiq__bxsvc, i)
        else:
            bgiq__bxsvc[i] = dict_arr_out[uqoz__vbqi[i]]
    return bgiq__bxsvc


@register_jitable
def str_endswith(arr, pat, na):
    ngsi__nhop = arr._data
    ziqdh__dmwki = len(ngsi__nhop)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(ziqdh__dmwki)
    for i in range(ziqdh__dmwki):
        dict_arr_out[i] = ngsi__nhop[i].endswith(pat)
    uqoz__vbqi = arr._indices
    tova__neh = len(uqoz__vbqi)
    bgiq__bxsvc = bodo.libs.bool_arr_ext.alloc_bool_array(tova__neh)
    for i in range(tova__neh):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(bgiq__bxsvc, i)
        else:
            bgiq__bxsvc[i] = dict_arr_out[uqoz__vbqi[i]]
    return bgiq__bxsvc


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    ngsi__nhop = arr._data
    btxwx__ixuw = pd.Series(ngsi__nhop)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = pd.array(btxwx__ixuw.array, 'string')._str_contains(pat,
            case, flags, na, regex)
    uqoz__vbqi = arr._indices
    tova__neh = len(uqoz__vbqi)
    bgiq__bxsvc = bodo.libs.bool_arr_ext.alloc_bool_array(tova__neh)
    for i in range(tova__neh):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(bgiq__bxsvc, i)
        else:
            bgiq__bxsvc[i] = dict_arr_out[uqoz__vbqi[i]]
    return bgiq__bxsvc


@register_jitable
def str_contains_non_regex(arr, pat, case):
    ngsi__nhop = arr._data
    ziqdh__dmwki = len(ngsi__nhop)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(ziqdh__dmwki)
    if not case:
        tvlh__wami = pat.upper()
    for i in range(ziqdh__dmwki):
        if case:
            dict_arr_out[i] = pat in ngsi__nhop[i]
        else:
            dict_arr_out[i] = tvlh__wami in ngsi__nhop[i].upper()
    uqoz__vbqi = arr._indices
    tova__neh = len(uqoz__vbqi)
    bgiq__bxsvc = bodo.libs.bool_arr_ext.alloc_bool_array(tova__neh)
    for i in range(tova__neh):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(bgiq__bxsvc, i)
        else:
            bgiq__bxsvc[i] = dict_arr_out[uqoz__vbqi[i]]
    return bgiq__bxsvc


@numba.njit
def str_match(arr, pat, case, flags, na):
    ngsi__nhop = arr._data
    uqoz__vbqi = arr._indices
    tova__neh = len(uqoz__vbqi)
    bgiq__bxsvc = bodo.libs.bool_arr_ext.alloc_bool_array(tova__neh)
    btxwx__ixuw = pd.Series(ngsi__nhop)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = btxwx__ixuw.array._str_match(pat, case, flags, na)
    for i in range(tova__neh):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(bgiq__bxsvc, i)
        else:
            bgiq__bxsvc[i] = dict_arr_out[uqoz__vbqi[i]]
    return bgiq__bxsvc


def create_simple_str2str_methods(func_name, func_args, can_create_non_unique):
    ugw__yvwae = f"""def str_{func_name}({', '.join(func_args)}):
    data_arr = arr._data
    n_data = len(data_arr)
    out_str_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_data, -1)
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            bodo.libs.array_kernels.setna(out_str_arr, i)
            continue
        out_str_arr[i] = data_arr[i].{func_name}({', '.join(func_args[1:])})
"""
    if can_create_non_unique:
        ugw__yvwae += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, False)
"""
    else:
        ugw__yvwae += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, arr._has_deduped_local_dictionary)
"""
    zob__jkh = {}
    exec(ugw__yvwae, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, zob__jkh)
    return zob__jkh[f'str_{func_name}']


def _register_simple_str2str_methods():
    iyku__edixf = {**dict.fromkeys(['capitalize', 'lower', 'swapcase',
        'title', 'upper'], ('arr',)), **dict.fromkeys(['lstrip', 'rstrip',
        'strip'], ('arr', 'to_strip')), **dict.fromkeys(['center', 'ljust',
        'rjust'], ('arr', 'width', 'fillchar')), **dict.fromkeys(['zfill'],
        ('arr', 'width'))}
    etzh__trfj = {**dict.fromkeys(['capitalize', 'lower', 'title', 'upper',
        'lstrip', 'rstrip', 'strip', 'center', 'zfill', 'ljust', 'rjust'], 
        True), **dict.fromkeys(['swapcase'], False)}
    for func_name in iyku__edixf.keys():
        unpk__krc = create_simple_str2str_methods(func_name, iyku__edixf[
            func_name], etzh__trfj[func_name])
        unpk__krc = register_jitable(unpk__krc)
        globals()[f'str_{func_name}'] = unpk__krc


_register_simple_str2str_methods()


@register_jitable
def str_index(arr, sub, start, end):
    betq__oul = arr._data
    uqoz__vbqi = arr._indices
    ycd__fdigz = len(betq__oul)
    tova__neh = len(uqoz__vbqi)
    oukz__cjg = bodo.libs.int_arr_ext.alloc_int_array(ycd__fdigz, np.int64)
    bgiq__bxsvc = bodo.libs.int_arr_ext.alloc_int_array(tova__neh, np.int64)
    msfm__pyred = False
    for i in range(ycd__fdigz):
        if bodo.libs.array_kernels.isna(betq__oul, i):
            bodo.libs.array_kernels.setna(oukz__cjg, i)
        else:
            oukz__cjg[i] = betq__oul[i].find(sub, start, end)
    for i in range(tova__neh):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(oukz__cjg, uqoz__vbqi[i]):
            bodo.libs.array_kernels.setna(bgiq__bxsvc, i)
        else:
            bgiq__bxsvc[i] = oukz__cjg[uqoz__vbqi[i]]
            if bgiq__bxsvc[i] == -1:
                msfm__pyred = True
    xlqli__snamj = 'substring not found' if msfm__pyred else ''
    synchronize_error_njit('ValueError', xlqli__snamj)
    return bgiq__bxsvc


@register_jitable
def str_rindex(arr, sub, start, end):
    betq__oul = arr._data
    uqoz__vbqi = arr._indices
    ycd__fdigz = len(betq__oul)
    tova__neh = len(uqoz__vbqi)
    oukz__cjg = bodo.libs.int_arr_ext.alloc_int_array(ycd__fdigz, np.int64)
    bgiq__bxsvc = bodo.libs.int_arr_ext.alloc_int_array(tova__neh, np.int64)
    msfm__pyred = False
    for i in range(ycd__fdigz):
        if bodo.libs.array_kernels.isna(betq__oul, i):
            bodo.libs.array_kernels.setna(oukz__cjg, i)
        else:
            oukz__cjg[i] = betq__oul[i].rindex(sub, start, end)
    for i in range(tova__neh):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(oukz__cjg, uqoz__vbqi[i]):
            bodo.libs.array_kernels.setna(bgiq__bxsvc, i)
        else:
            bgiq__bxsvc[i] = oukz__cjg[uqoz__vbqi[i]]
            if bgiq__bxsvc[i] == -1:
                msfm__pyred = True
    xlqli__snamj = 'substring not found' if msfm__pyred else ''
    synchronize_error_njit('ValueError', xlqli__snamj)
    return bgiq__bxsvc


def create_find_methods(func_name):
    ugw__yvwae = f"""def str_{func_name}(arr, sub, start, end):
  data_arr = arr._data
  indices_arr = arr._indices
  n_data = len(data_arr)
  n_indices = len(indices_arr)
  tmp_dict_arr = bodo.libs.int_arr_ext.alloc_int_array(n_data, np.int64)
  out_int_arr = bodo.libs.int_arr_ext.alloc_int_array(n_indices, np.int64)
  for i in range(n_data):
    if bodo.libs.array_kernels.isna(data_arr, i):
      bodo.libs.array_kernels.setna(tmp_dict_arr, i)
      continue
    tmp_dict_arr[i] = data_arr[i].{func_name}(sub, start, end)
  for i in range(n_indices):
    if bodo.libs.array_kernels.isna(indices_arr, i) or bodo.libs.array_kernels.isna(
      tmp_dict_arr, indices_arr[i]
    ):
      bodo.libs.array_kernels.setna(out_int_arr, i)
    else:
      out_int_arr[i] = tmp_dict_arr[indices_arr[i]]
  return out_int_arr"""
    zob__jkh = {}
    exec(ugw__yvwae, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr, 'np': np}, zob__jkh)
    return zob__jkh[f'str_{func_name}']


def _register_find_methods():
    uavo__xsc = ['find', 'rfind']
    for func_name in uavo__xsc:
        unpk__krc = create_find_methods(func_name)
        unpk__krc = register_jitable(unpk__krc)
        globals()[f'str_{func_name}'] = unpk__krc


_register_find_methods()


@register_jitable
def str_count(arr, pat, flags):
    betq__oul = arr._data
    uqoz__vbqi = arr._indices
    ycd__fdigz = len(betq__oul)
    tova__neh = len(uqoz__vbqi)
    oukz__cjg = bodo.libs.int_arr_ext.alloc_int_array(ycd__fdigz, np.int64)
    ywsp__uge = bodo.libs.int_arr_ext.alloc_int_array(tova__neh, np.int64)
    regex = re.compile(pat, flags)
    for i in range(ycd__fdigz):
        if bodo.libs.array_kernels.isna(betq__oul, i):
            bodo.libs.array_kernels.setna(oukz__cjg, i)
            continue
        oukz__cjg[i] = bodo.libs.str_ext.str_findall_count(regex, betq__oul[i])
    for i in range(tova__neh):
        if bodo.libs.array_kernels.isna(uqoz__vbqi, i
            ) or bodo.libs.array_kernels.isna(oukz__cjg, uqoz__vbqi[i]):
            bodo.libs.array_kernels.setna(ywsp__uge, i)
        else:
            ywsp__uge[i] = oukz__cjg[uqoz__vbqi[i]]
    return ywsp__uge


@register_jitable
def str_len(arr):
    betq__oul = arr._data
    uqoz__vbqi = arr._indices
    tova__neh = len(uqoz__vbqi)
    oukz__cjg = bodo.libs.array_kernels.get_arr_lens(betq__oul, False)
    ywsp__uge = bodo.libs.int_arr_ext.alloc_int_array(tova__neh, np.int64)
    for i in range(tova__neh):
        if bodo.libs.array_kernels.isna(uqoz__vbqi, i
            ) or bodo.libs.array_kernels.isna(oukz__cjg, uqoz__vbqi[i]):
            bodo.libs.array_kernels.setna(ywsp__uge, i)
        else:
            ywsp__uge[i] = oukz__cjg[uqoz__vbqi[i]]
    return ywsp__uge


@register_jitable
def str_slice(arr, start, stop, step):
    betq__oul = arr._data
    ycd__fdigz = len(betq__oul)
    hiwv__qyus = bodo.libs.str_arr_ext.pre_alloc_string_array(ycd__fdigz, -1)
    for i in range(ycd__fdigz):
        if bodo.libs.array_kernels.isna(betq__oul, i):
            bodo.libs.array_kernels.setna(hiwv__qyus, i)
            continue
        hiwv__qyus[i] = betq__oul[i][start:stop:step]
    return init_dict_arr(hiwv__qyus, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_get(arr, i):
    betq__oul = arr._data
    uqoz__vbqi = arr._indices
    ycd__fdigz = len(betq__oul)
    tova__neh = len(uqoz__vbqi)
    hiwv__qyus = pre_alloc_string_array(ycd__fdigz, -1)
    bgiq__bxsvc = pre_alloc_string_array(tova__neh, -1)
    for xre__ardrg in range(ycd__fdigz):
        if bodo.libs.array_kernels.isna(betq__oul, xre__ardrg) or not -len(
            betq__oul[xre__ardrg]) <= i < len(betq__oul[xre__ardrg]):
            bodo.libs.array_kernels.setna(hiwv__qyus, xre__ardrg)
            continue
        hiwv__qyus[xre__ardrg] = betq__oul[xre__ardrg][i]
    for xre__ardrg in range(tova__neh):
        if bodo.libs.array_kernels.isna(uqoz__vbqi, xre__ardrg
            ) or bodo.libs.array_kernels.isna(hiwv__qyus, uqoz__vbqi[
            xre__ardrg]):
            bodo.libs.array_kernels.setna(bgiq__bxsvc, xre__ardrg)
            continue
        bgiq__bxsvc[xre__ardrg] = hiwv__qyus[uqoz__vbqi[xre__ardrg]]
    return bgiq__bxsvc


@register_jitable
def str_repeat_int(arr, repeats):
    betq__oul = arr._data
    ycd__fdigz = len(betq__oul)
    hiwv__qyus = pre_alloc_string_array(ycd__fdigz, -1)
    for i in range(ycd__fdigz):
        if bodo.libs.array_kernels.isna(betq__oul, i):
            bodo.libs.array_kernels.setna(hiwv__qyus, i)
            continue
        hiwv__qyus[i] = betq__oul[i] * repeats
    return init_dict_arr(hiwv__qyus, arr._indices.copy(), arr.
        _has_global_dictionary, arr._has_deduped_local_dictionary and 
        repeats != 0)


def create_str2bool_methods(func_name):
    ugw__yvwae = f"""def str_{func_name}(arr):
    data_arr = arr._data
    indices_arr = arr._indices
    n_data = len(data_arr)
    n_indices = len(indices_arr)
    out_dict_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n_data)
    out_bool_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n_indices)
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            bodo.libs.array_kernels.setna(out_dict_arr, i)
            continue
        out_dict_arr[i] = np.bool_(data_arr[i].{func_name}())
    for i in range(n_indices):
        if bodo.libs.array_kernels.isna(indices_arr, i) or bodo.libs.array_kernels.isna(
            data_arr, indices_arr[i]        ):
            bodo.libs.array_kernels.setna(out_bool_arr, i)
        else:
            out_bool_arr[i] = out_dict_arr[indices_arr[i]]
    return out_bool_arr"""
    zob__jkh = {}
    exec(ugw__yvwae, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr}, zob__jkh)
    return zob__jkh[f'str_{func_name}']


def _register_str2bool_methods():
    for func_name in bodo.hiframes.pd_series_ext.str2bool_methods:
        unpk__krc = create_str2bool_methods(func_name)
        unpk__krc = register_jitable(unpk__krc)
        globals()[f'str_{func_name}'] = unpk__krc


_register_str2bool_methods()


@register_jitable
def str_extract(arr, pat, flags, n_cols):
    betq__oul = arr._data
    uqoz__vbqi = arr._indices
    ycd__fdigz = len(betq__oul)
    tova__neh = len(uqoz__vbqi)
    regex = re.compile(pat, flags=flags)
    tuyyo__lydjp = []
    for vpugm__qzqo in range(n_cols):
        tuyyo__lydjp.append(pre_alloc_string_array(ycd__fdigz, -1))
    six__yqq = bodo.libs.bool_arr_ext.alloc_bool_array(ycd__fdigz)
    ktlp__iihkt = uqoz__vbqi.copy()
    for i in range(ycd__fdigz):
        if bodo.libs.array_kernels.isna(betq__oul, i):
            six__yqq[i] = True
            for xre__ardrg in range(n_cols):
                bodo.libs.array_kernels.setna(tuyyo__lydjp[xre__ardrg], i)
            continue
        iupqv__khwob = regex.search(betq__oul[i])
        if iupqv__khwob:
            six__yqq[i] = False
            iia__unkpa = iupqv__khwob.groups()
            for xre__ardrg in range(n_cols):
                tuyyo__lydjp[xre__ardrg][i] = iia__unkpa[xre__ardrg]
        else:
            six__yqq[i] = True
            for xre__ardrg in range(n_cols):
                bodo.libs.array_kernels.setna(tuyyo__lydjp[xre__ardrg], i)
    for i in range(tova__neh):
        if six__yqq[ktlp__iihkt[i]]:
            bodo.libs.array_kernels.setna(ktlp__iihkt, i)
    kblvj__kwvlw = [init_dict_arr(tuyyo__lydjp[i], ktlp__iihkt.copy(), arr.
        _has_global_dictionary, False) for i in range(n_cols)]
    return kblvj__kwvlw


def create_extractall_methods(is_multi_group):
    bxq__ofea = '_multi' if is_multi_group else ''
    ugw__yvwae = f"""def str_extractall{bxq__ofea}(arr, regex, n_cols, index_arr):
    data_arr = arr._data
    indices_arr = arr._indices
    n_data = len(data_arr)
    n_indices = len(indices_arr)
    indices_count = [0 for _ in range(n_data)]
    for i in range(n_indices):
        if not bodo.libs.array_kernels.isna(indices_arr, i):
            indices_count[indices_arr[i]] += 1
    dict_group_count = []
    out_dict_len = out_ind_len = 0
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            continue
        m = regex.findall(data_arr[i])
        dict_group_count.append((out_dict_len, len(m)))
        out_dict_len += len(m)
        out_ind_len += indices_count[i] * len(m)
    out_dict_arr_list = []
    for _ in range(n_cols):
        out_dict_arr_list.append(pre_alloc_string_array(out_dict_len, -1))
    out_indices_arr = bodo.libs.int_arr_ext.alloc_int_array(out_ind_len, np.int32)
    out_ind_arr = bodo.utils.utils.alloc_type(out_ind_len, index_arr, (-1,))
    out_match_arr = np.empty(out_ind_len, np.int64)
    curr_ind = 0
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            continue
        m = regex.findall(data_arr[i])
        for s in m:
            for j in range(n_cols):
                out_dict_arr_list[j][curr_ind] = s{'[j]' if is_multi_group else ''}
            curr_ind += 1
    curr_ind = 0
    for i in range(n_indices):
        if bodo.libs.array_kernels.isna(indices_arr, i):
            continue
        n_rows = dict_group_count[indices_arr[i]][1]
        for k in range(n_rows):
            out_indices_arr[curr_ind] = dict_group_count[indices_arr[i]][0] + k
            out_ind_arr[curr_ind] = index_arr[i]
            out_match_arr[curr_ind] = k
            curr_ind += 1
    out_arr_list = [
        init_dict_arr(
            out_dict_arr_list[i], out_indices_arr.copy(), arr._has_global_dictionary, False
        )
        for i in range(n_cols)
    ]
    return (out_ind_arr, out_match_arr, out_arr_list) 
"""
    zob__jkh = {}
    exec(ugw__yvwae, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr, 'pre_alloc_string_array':
        pre_alloc_string_array}, zob__jkh)
    return zob__jkh[f'str_extractall{bxq__ofea}']


def _register_extractall_methods():
    for is_multi_group in [True, False]:
        bxq__ofea = '_multi' if is_multi_group else ''
        unpk__krc = create_extractall_methods(is_multi_group)
        unpk__krc = register_jitable(unpk__krc)
        globals()[f'str_extractall{bxq__ofea}'] = unpk__krc


_register_extractall_methods()
