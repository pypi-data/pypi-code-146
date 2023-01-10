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
        hmxw__nufy = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_),
            ('has_deduped_local_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, hmxw__nufy)


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
        btg__knobd, izbdo__hygnx, svokn__tglg, lxvxs__rvmrr = args
        xej__geyc = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        xej__geyc.data = btg__knobd
        xej__geyc.indices = izbdo__hygnx
        xej__geyc.has_global_dictionary = svokn__tglg
        xej__geyc.has_deduped_local_dictionary = lxvxs__rvmrr
        context.nrt.incref(builder, signature.args[0], btg__knobd)
        context.nrt.incref(builder, signature.args[1], izbdo__hygnx)
        return xej__geyc._getvalue()
    lpk__arkai = DictionaryArrayType(data_t)
    wrt__jhywp = lpk__arkai(data_t, indices_t, types.bool_, types.bool_)
    return wrt__jhywp, codegen


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
    iuo__evkm = c.pyapi.unserialize(c.pyapi.serialize_object(to_pa_dict_arr))
    val = c.pyapi.call_function_objargs(iuo__evkm, [val])
    c.pyapi.decref(iuo__evkm)
    xej__geyc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ixk__agbh = c.pyapi.object_getattr_string(val, 'dictionary')
    hde__mahg = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_, 
        False))
    ldv__wqiaq = c.pyapi.call_method(ixk__agbh, 'to_numpy', (hde__mahg,))
    xej__geyc.data = c.unbox(typ.data, ldv__wqiaq).value
    uliji__mfbx = c.pyapi.object_getattr_string(val, 'indices')
    nbmsp__ban = c.context.insert_const_string(c.builder.module, 'pandas')
    almry__pzuta = c.pyapi.import_module_noblock(nbmsp__ban)
    xvq__bws = c.pyapi.string_from_constant_string('Int32')
    smjut__ndcig = c.pyapi.call_method(almry__pzuta, 'array', (uliji__mfbx,
        xvq__bws))
    xej__geyc.indices = c.unbox(dict_indices_arr_type, smjut__ndcig).value
    xej__geyc.has_global_dictionary = c.context.get_constant(types.bool_, False
        )
    xej__geyc.has_deduped_local_dictionary = c.context.get_constant(types.
        bool_, False)
    c.pyapi.decref(ixk__agbh)
    c.pyapi.decref(hde__mahg)
    c.pyapi.decref(ldv__wqiaq)
    c.pyapi.decref(uliji__mfbx)
    c.pyapi.decref(almry__pzuta)
    c.pyapi.decref(xvq__bws)
    c.pyapi.decref(smjut__ndcig)
    c.pyapi.decref(val)
    ghkz__dvpqy = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(xej__geyc._getvalue(), is_error=ghkz__dvpqy)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    xej__geyc = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        if bodo.libs.str_arr_ext.use_pd_pyarrow_string_array:
            from bodo.libs.array import array_info_type, array_to_info_codegen
            qbat__vlw = array_to_info_codegen(c.context, c.builder,
                array_info_type(typ), (val,), incref=False)
            hrf__zfov = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
                as_pointer()])
            lvvwk__wrbam = 'pd_pyarrow_array_from_string_array'
            shp__aanz = cgutils.get_or_insert_function(c.builder.module,
                hrf__zfov, name=lvvwk__wrbam)
            arr = c.builder.call(shp__aanz, [qbat__vlw])
            c.context.nrt.decref(c.builder, typ, val)
            return arr
        c.context.nrt.incref(c.builder, typ.data, xej__geyc.data)
        kbage__ryed = c.box(typ.data, xej__geyc.data)
        fimnt__tpvr = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, xej__geyc.indices)
        hrf__zfov = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        shp__aanz = cgutils.get_or_insert_function(c.builder.module,
            hrf__zfov, name='box_dict_str_array')
        zoji__nvmx = cgutils.create_struct_proxy(types.Array(types.int32, 1,
            'C'))(c.context, c.builder, fimnt__tpvr.data)
        cjrmj__japlw = c.builder.extract_value(zoji__nvmx.shape, 0)
        sosr__tqke = zoji__nvmx.data
        taaux__fmjm = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, fimnt__tpvr.null_bitmap).data
        ldv__wqiaq = c.builder.call(shp__aanz, [cjrmj__japlw, kbage__ryed,
            sosr__tqke, taaux__fmjm])
        c.pyapi.decref(kbage__ryed)
    else:
        nbmsp__ban = c.context.insert_const_string(c.builder.module, 'pyarrow')
        sabg__jbuns = c.pyapi.import_module_noblock(nbmsp__ban)
        kryue__bkm = c.pyapi.object_getattr_string(sabg__jbuns,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, xej__geyc.data)
        kbage__ryed = c.box(typ.data, xej__geyc.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, xej__geyc.
            indices)
        uliji__mfbx = c.box(dict_indices_arr_type, xej__geyc.indices)
        dvoi__wdqq = c.pyapi.call_method(kryue__bkm, 'from_arrays', (
            uliji__mfbx, kbage__ryed))
        hde__mahg = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        ldv__wqiaq = c.pyapi.call_method(dvoi__wdqq, 'to_numpy', (hde__mahg,))
        c.pyapi.decref(sabg__jbuns)
        c.pyapi.decref(kbage__ryed)
        c.pyapi.decref(uliji__mfbx)
        c.pyapi.decref(kryue__bkm)
        c.pyapi.decref(dvoi__wdqq)
        c.pyapi.decref(hde__mahg)
    c.context.nrt.decref(c.builder, typ, val)
    return ldv__wqiaq


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
    bok__ynpcj = pyval.dictionary.to_numpy(False)
    mlqi__mzj = pd.array(pyval.indices, 'Int32')
    bok__ynpcj = context.get_constant_generic(builder, typ.data, bok__ynpcj)
    mlqi__mzj = context.get_constant_generic(builder, dict_indices_arr_type,
        mlqi__mzj)
    abps__bknq = context.get_constant(types.bool_, False)
    nqfxs__lupz = context.get_constant(types.bool_, False)
    uzo__xwhf = lir.Constant.literal_struct([bok__ynpcj, mlqi__mzj,
        abps__bknq, nqfxs__lupz])
    return uzo__xwhf


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            ynu__ymt = A._indices[ind]
            return A._data[ynu__ymt]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary, A._has_deduped_local_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        btg__knobd = A._data
        izbdo__hygnx = A._indices
        cjrmj__japlw = len(izbdo__hygnx)
        cjpd__cyz = [get_str_arr_item_length(btg__knobd, i) for i in range(
            len(btg__knobd))]
        dwt__dewut = 0
        for i in range(cjrmj__japlw):
            if not bodo.libs.array_kernels.isna(izbdo__hygnx, i):
                dwt__dewut += cjpd__cyz[izbdo__hygnx[i]]
        mzwod__grhbg = pre_alloc_string_array(cjrmj__japlw, dwt__dewut)
        for i in range(cjrmj__japlw):
            if bodo.libs.array_kernels.isna(izbdo__hygnx, i):
                bodo.libs.array_kernels.setna(mzwod__grhbg, i)
                continue
            ind = izbdo__hygnx[i]
            if bodo.libs.array_kernels.isna(btg__knobd, ind):
                bodo.libs.array_kernels.setna(mzwod__grhbg, i)
                continue
            mzwod__grhbg[i] = btg__knobd[ind]
        return mzwod__grhbg
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_unique(arr, val):
    ynu__ymt = -1
    btg__knobd = arr._data
    for i in range(len(btg__knobd)):
        if bodo.libs.array_kernels.isna(btg__knobd, i):
            continue
        if btg__knobd[i] == val:
            ynu__ymt = i
            break
    return ynu__ymt


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_non_unique(arr, val):
    oef__blyk = set()
    btg__knobd = arr._data
    for i in range(len(btg__knobd)):
        if bodo.libs.array_kernels.isna(btg__knobd, i):
            continue
        if btg__knobd[i] == val:
            oef__blyk.add(i)
    return oef__blyk


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    cjrmj__japlw = len(arr)
    if arr._has_deduped_local_dictionary:
        ynu__ymt = find_dict_ind_unique(arr, val)
        if ynu__ymt == -1:
            return init_bool_array(np.full(cjrmj__japlw, False, np.bool_),
                arr._indices._null_bitmap.copy())
        return arr._indices == ynu__ymt
    else:
        bgjo__svbg = find_dict_ind_non_unique(arr, val)
        if len(bgjo__svbg) == 0:
            return init_bool_array(np.full(cjrmj__japlw, False, np.bool_),
                arr._indices._null_bitmap.copy())
        ppjv__uxi = np.empty(cjrmj__japlw, dtype=np.bool_)
        for i in range(len(arr._indices)):
            ppjv__uxi[i] = arr._indices[i] in bgjo__svbg
        return init_bool_array(ppjv__uxi, arr._indices._null_bitmap.copy())


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    cjrmj__japlw = len(arr)
    if arr._has_deduped_local_dictionary:
        ynu__ymt = find_dict_ind_unique(arr, val)
        if ynu__ymt == -1:
            return init_bool_array(np.full(cjrmj__japlw, True, np.bool_),
                arr._indices._null_bitmap.copy())
        return arr._indices != ynu__ymt
    else:
        bgjo__svbg = find_dict_ind_non_unique(arr, val)
        if len(bgjo__svbg) == 0:
            return init_bool_array(np.full(cjrmj__japlw, True, np.bool_),
                arr._indices._null_bitmap.copy())
        ppjv__uxi = np.empty(cjrmj__japlw, dtype=np.bool_)
        for i in range(len(arr._indices)):
            ppjv__uxi[i] = arr._indices[i] not in bgjo__svbg
        return init_bool_array(ppjv__uxi, arr._indices._null_bitmap.copy())


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
        zagp__ruzck = arr._data
        phe__wsdx = bodo.libs.int_arr_ext.alloc_int_array(len(zagp__ruzck),
            dtype)
        for gsnbp__zaz in range(len(zagp__ruzck)):
            if bodo.libs.array_kernels.isna(zagp__ruzck, gsnbp__zaz):
                bodo.libs.array_kernels.setna(phe__wsdx, gsnbp__zaz)
                continue
            phe__wsdx[gsnbp__zaz] = np.int64(zagp__ruzck[gsnbp__zaz])
        cjrmj__japlw = len(arr)
        izbdo__hygnx = arr._indices
        mzwod__grhbg = bodo.libs.int_arr_ext.alloc_int_array(cjrmj__japlw,
            dtype)
        for i in range(cjrmj__japlw):
            if bodo.libs.array_kernels.isna(izbdo__hygnx, i):
                bodo.libs.array_kernels.setna(mzwod__grhbg, i)
                continue
            mzwod__grhbg[i] = phe__wsdx[izbdo__hygnx[i]]
        return mzwod__grhbg
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    jfw__zeth = len(arrs)
    vojps__jkkt = 'def impl(arrs, sep):\n'
    vojps__jkkt += '  ind_map = {}\n'
    vojps__jkkt += '  out_strs = []\n'
    vojps__jkkt += '  n = len(arrs[0])\n'
    for i in range(jfw__zeth):
        vojps__jkkt += f'  indices{i} = arrs[{i}]._indices\n'
    for i in range(jfw__zeth):
        vojps__jkkt += f'  data{i} = arrs[{i}]._data\n'
    vojps__jkkt += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    vojps__jkkt += '  for i in range(n):\n'
    ncygn__bfk = ' or '.join([f'bodo.libs.array_kernels.isna(arrs[{i}], i)' for
        i in range(jfw__zeth)])
    vojps__jkkt += f'    if {ncygn__bfk}:\n'
    vojps__jkkt += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    vojps__jkkt += '      continue\n'
    for i in range(jfw__zeth):
        vojps__jkkt += f'    ind{i} = indices{i}[i]\n'
    ztq__rwkad = '(' + ', '.join(f'ind{i}' for i in range(jfw__zeth)) + ')'
    vojps__jkkt += f'    if {ztq__rwkad} not in ind_map:\n'
    vojps__jkkt += '      out_ind = len(out_strs)\n'
    vojps__jkkt += f'      ind_map[{ztq__rwkad}] = out_ind\n'
    mcv__obbzo = "''" if is_overload_none(sep) else 'sep'
    zawry__mizh = ', '.join([f'data{i}[ind{i}]' for i in range(jfw__zeth)])
    vojps__jkkt += f'      v = {mcv__obbzo}.join([{zawry__mizh}])\n'
    vojps__jkkt += '      out_strs.append(v)\n'
    vojps__jkkt += '    else:\n'
    vojps__jkkt += f'      out_ind = ind_map[{ztq__rwkad}]\n'
    vojps__jkkt += '    out_indices[i] = out_ind\n'
    vojps__jkkt += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    vojps__jkkt += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False, False)
"""
    sja__yecz = {}
    exec(vojps__jkkt, {'bodo': bodo, 'numba': numba, 'np': np}, sja__yecz)
    impl = sja__yecz['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    iswck__edt = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    wrt__jhywp = toty(fromty)
    yqkmm__qgsyq = context.compile_internal(builder, iswck__edt, wrt__jhywp,
        (val,))
    return impl_ret_new_ref(context, builder, toty, yqkmm__qgsyq)


@register_jitable
def dict_arr_to_numeric(arr, errors, downcast):
    xej__geyc = arr._data
    dict_arr_out = pd.to_numeric(xej__geyc, errors, downcast)
    mlqi__mzj = arr._indices
    zjs__tiqy = len(mlqi__mzj)
    mzwod__grhbg = bodo.utils.utils.alloc_type(zjs__tiqy, dict_arr_out, (-1,))
    for i in range(zjs__tiqy):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(mzwod__grhbg, i)
            continue
        ynu__ymt = mlqi__mzj[i]
        if bodo.libs.array_kernels.isna(dict_arr_out, ynu__ymt):
            bodo.libs.array_kernels.setna(mzwod__grhbg, i)
            continue
        mzwod__grhbg[i] = dict_arr_out[ynu__ymt]
    return mzwod__grhbg


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    bok__ynpcj = arr._data
    jpny__vgxvi = len(bok__ynpcj)
    yjjw__egq = pre_alloc_string_array(jpny__vgxvi, -1)
    if regex:
        mxgp__xitdp = re.compile(pat, flags)
        for i in range(jpny__vgxvi):
            if bodo.libs.array_kernels.isna(bok__ynpcj, i):
                bodo.libs.array_kernels.setna(yjjw__egq, i)
                continue
            yjjw__egq[i] = mxgp__xitdp.sub(repl=repl, string=bok__ynpcj[i])
    else:
        for i in range(jpny__vgxvi):
            if bodo.libs.array_kernels.isna(bok__ynpcj, i):
                bodo.libs.array_kernels.setna(yjjw__egq, i)
                continue
            yjjw__egq[i] = bok__ynpcj[i].replace(pat, repl)
    return init_dict_arr(yjjw__egq, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_startswith(arr, pat, na):
    xej__geyc = arr._data
    vfznf__nmyvh = len(xej__geyc)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(vfznf__nmyvh)
    for i in range(vfznf__nmyvh):
        dict_arr_out[i] = xej__geyc[i].startswith(pat)
    mlqi__mzj = arr._indices
    zjs__tiqy = len(mlqi__mzj)
    mzwod__grhbg = bodo.libs.bool_arr_ext.alloc_bool_array(zjs__tiqy)
    for i in range(zjs__tiqy):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(mzwod__grhbg, i)
        else:
            mzwod__grhbg[i] = dict_arr_out[mlqi__mzj[i]]
    return mzwod__grhbg


@register_jitable
def str_endswith(arr, pat, na):
    xej__geyc = arr._data
    vfznf__nmyvh = len(xej__geyc)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(vfznf__nmyvh)
    for i in range(vfznf__nmyvh):
        dict_arr_out[i] = xej__geyc[i].endswith(pat)
    mlqi__mzj = arr._indices
    zjs__tiqy = len(mlqi__mzj)
    mzwod__grhbg = bodo.libs.bool_arr_ext.alloc_bool_array(zjs__tiqy)
    for i in range(zjs__tiqy):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(mzwod__grhbg, i)
        else:
            mzwod__grhbg[i] = dict_arr_out[mlqi__mzj[i]]
    return mzwod__grhbg


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    xej__geyc = arr._data
    qrtg__borf = pd.Series(xej__geyc)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = pd.array(qrtg__borf.array, 'string')._str_contains(pat,
            case, flags, na, regex)
    mlqi__mzj = arr._indices
    zjs__tiqy = len(mlqi__mzj)
    mzwod__grhbg = bodo.libs.bool_arr_ext.alloc_bool_array(zjs__tiqy)
    for i in range(zjs__tiqy):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(mzwod__grhbg, i)
        else:
            mzwod__grhbg[i] = dict_arr_out[mlqi__mzj[i]]
    return mzwod__grhbg


@register_jitable
def str_contains_non_regex(arr, pat, case):
    xej__geyc = arr._data
    vfznf__nmyvh = len(xej__geyc)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(vfznf__nmyvh)
    if not case:
        hdnr__wdau = pat.upper()
    for i in range(vfznf__nmyvh):
        if case:
            dict_arr_out[i] = pat in xej__geyc[i]
        else:
            dict_arr_out[i] = hdnr__wdau in xej__geyc[i].upper()
    mlqi__mzj = arr._indices
    zjs__tiqy = len(mlqi__mzj)
    mzwod__grhbg = bodo.libs.bool_arr_ext.alloc_bool_array(zjs__tiqy)
    for i in range(zjs__tiqy):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(mzwod__grhbg, i)
        else:
            mzwod__grhbg[i] = dict_arr_out[mlqi__mzj[i]]
    return mzwod__grhbg


@numba.njit
def str_match(arr, pat, case, flags, na):
    xej__geyc = arr._data
    mlqi__mzj = arr._indices
    zjs__tiqy = len(mlqi__mzj)
    mzwod__grhbg = bodo.libs.bool_arr_ext.alloc_bool_array(zjs__tiqy)
    qrtg__borf = pd.Series(xej__geyc)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = qrtg__borf.array._str_match(pat, case, flags, na)
    for i in range(zjs__tiqy):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(mzwod__grhbg, i)
        else:
            mzwod__grhbg[i] = dict_arr_out[mlqi__mzj[i]]
    return mzwod__grhbg


def create_simple_str2str_methods(func_name, func_args, can_create_non_unique):
    vojps__jkkt = f"""def str_{func_name}({', '.join(func_args)}):
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
        vojps__jkkt += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, False)
"""
    else:
        vojps__jkkt += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, arr._has_deduped_local_dictionary)
"""
    sja__yecz = {}
    exec(vojps__jkkt, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, sja__yecz)
    return sja__yecz[f'str_{func_name}']


def _register_simple_str2str_methods():
    xeuvn__lzo = {**dict.fromkeys(['capitalize', 'lower', 'swapcase',
        'title', 'upper'], ('arr',)), **dict.fromkeys(['lstrip', 'rstrip',
        'strip'], ('arr', 'to_strip')), **dict.fromkeys(['center', 'ljust',
        'rjust'], ('arr', 'width', 'fillchar')), **dict.fromkeys(['zfill'],
        ('arr', 'width'))}
    nfbr__awsqu = {**dict.fromkeys(['capitalize', 'lower', 'title', 'upper',
        'lstrip', 'rstrip', 'strip', 'center', 'zfill', 'ljust', 'rjust'], 
        True), **dict.fromkeys(['swapcase'], False)}
    for func_name in xeuvn__lzo.keys():
        tqnfk__iwfi = create_simple_str2str_methods(func_name, xeuvn__lzo[
            func_name], nfbr__awsqu[func_name])
        tqnfk__iwfi = register_jitable(tqnfk__iwfi)
        globals()[f'str_{func_name}'] = tqnfk__iwfi


_register_simple_str2str_methods()


@register_jitable
def str_index(arr, sub, start, end):
    bok__ynpcj = arr._data
    mlqi__mzj = arr._indices
    jpny__vgxvi = len(bok__ynpcj)
    zjs__tiqy = len(mlqi__mzj)
    wedeh__qhlae = bodo.libs.int_arr_ext.alloc_int_array(jpny__vgxvi, np.int64)
    mzwod__grhbg = bodo.libs.int_arr_ext.alloc_int_array(zjs__tiqy, np.int64)
    chc__hnfgq = False
    for i in range(jpny__vgxvi):
        if bodo.libs.array_kernels.isna(bok__ynpcj, i):
            bodo.libs.array_kernels.setna(wedeh__qhlae, i)
        else:
            wedeh__qhlae[i] = bok__ynpcj[i].find(sub, start, end)
    for i in range(zjs__tiqy):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(wedeh__qhlae, mlqi__mzj[i]):
            bodo.libs.array_kernels.setna(mzwod__grhbg, i)
        else:
            mzwod__grhbg[i] = wedeh__qhlae[mlqi__mzj[i]]
            if mzwod__grhbg[i] == -1:
                chc__hnfgq = True
    ksm__lst = 'substring not found' if chc__hnfgq else ''
    synchronize_error_njit('ValueError', ksm__lst)
    return mzwod__grhbg


@register_jitable
def str_rindex(arr, sub, start, end):
    bok__ynpcj = arr._data
    mlqi__mzj = arr._indices
    jpny__vgxvi = len(bok__ynpcj)
    zjs__tiqy = len(mlqi__mzj)
    wedeh__qhlae = bodo.libs.int_arr_ext.alloc_int_array(jpny__vgxvi, np.int64)
    mzwod__grhbg = bodo.libs.int_arr_ext.alloc_int_array(zjs__tiqy, np.int64)
    chc__hnfgq = False
    for i in range(jpny__vgxvi):
        if bodo.libs.array_kernels.isna(bok__ynpcj, i):
            bodo.libs.array_kernels.setna(wedeh__qhlae, i)
        else:
            wedeh__qhlae[i] = bok__ynpcj[i].rindex(sub, start, end)
    for i in range(zjs__tiqy):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(wedeh__qhlae, mlqi__mzj[i]):
            bodo.libs.array_kernels.setna(mzwod__grhbg, i)
        else:
            mzwod__grhbg[i] = wedeh__qhlae[mlqi__mzj[i]]
            if mzwod__grhbg[i] == -1:
                chc__hnfgq = True
    ksm__lst = 'substring not found' if chc__hnfgq else ''
    synchronize_error_njit('ValueError', ksm__lst)
    return mzwod__grhbg


def create_find_methods(func_name):
    vojps__jkkt = f"""def str_{func_name}(arr, sub, start, end):
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
    sja__yecz = {}
    exec(vojps__jkkt, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr, 'np': np}, sja__yecz)
    return sja__yecz[f'str_{func_name}']


def _register_find_methods():
    hjxu__plz = ['find', 'rfind']
    for func_name in hjxu__plz:
        tqnfk__iwfi = create_find_methods(func_name)
        tqnfk__iwfi = register_jitable(tqnfk__iwfi)
        globals()[f'str_{func_name}'] = tqnfk__iwfi


_register_find_methods()


@register_jitable
def str_count(arr, pat, flags):
    bok__ynpcj = arr._data
    mlqi__mzj = arr._indices
    jpny__vgxvi = len(bok__ynpcj)
    zjs__tiqy = len(mlqi__mzj)
    wedeh__qhlae = bodo.libs.int_arr_ext.alloc_int_array(jpny__vgxvi, np.int64)
    xnxgq__uixa = bodo.libs.int_arr_ext.alloc_int_array(zjs__tiqy, np.int64)
    regex = re.compile(pat, flags)
    for i in range(jpny__vgxvi):
        if bodo.libs.array_kernels.isna(bok__ynpcj, i):
            bodo.libs.array_kernels.setna(wedeh__qhlae, i)
            continue
        wedeh__qhlae[i] = bodo.libs.str_ext.str_findall_count(regex,
            bok__ynpcj[i])
    for i in range(zjs__tiqy):
        if bodo.libs.array_kernels.isna(mlqi__mzj, i
            ) or bodo.libs.array_kernels.isna(wedeh__qhlae, mlqi__mzj[i]):
            bodo.libs.array_kernels.setna(xnxgq__uixa, i)
        else:
            xnxgq__uixa[i] = wedeh__qhlae[mlqi__mzj[i]]
    return xnxgq__uixa


@register_jitable
def str_len(arr):
    bok__ynpcj = arr._data
    mlqi__mzj = arr._indices
    zjs__tiqy = len(mlqi__mzj)
    wedeh__qhlae = bodo.libs.array_kernels.get_arr_lens(bok__ynpcj, False)
    xnxgq__uixa = bodo.libs.int_arr_ext.alloc_int_array(zjs__tiqy, np.int64)
    for i in range(zjs__tiqy):
        if bodo.libs.array_kernels.isna(mlqi__mzj, i
            ) or bodo.libs.array_kernels.isna(wedeh__qhlae, mlqi__mzj[i]):
            bodo.libs.array_kernels.setna(xnxgq__uixa, i)
        else:
            xnxgq__uixa[i] = wedeh__qhlae[mlqi__mzj[i]]
    return xnxgq__uixa


@register_jitable
def str_slice(arr, start, stop, step):
    bok__ynpcj = arr._data
    jpny__vgxvi = len(bok__ynpcj)
    yjjw__egq = bodo.libs.str_arr_ext.pre_alloc_string_array(jpny__vgxvi, -1)
    for i in range(jpny__vgxvi):
        if bodo.libs.array_kernels.isna(bok__ynpcj, i):
            bodo.libs.array_kernels.setna(yjjw__egq, i)
            continue
        yjjw__egq[i] = bok__ynpcj[i][start:stop:step]
    return init_dict_arr(yjjw__egq, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_get(arr, i):
    bok__ynpcj = arr._data
    mlqi__mzj = arr._indices
    jpny__vgxvi = len(bok__ynpcj)
    zjs__tiqy = len(mlqi__mzj)
    yjjw__egq = pre_alloc_string_array(jpny__vgxvi, -1)
    mzwod__grhbg = pre_alloc_string_array(zjs__tiqy, -1)
    for gsnbp__zaz in range(jpny__vgxvi):
        if bodo.libs.array_kernels.isna(bok__ynpcj, gsnbp__zaz) or not -len(
            bok__ynpcj[gsnbp__zaz]) <= i < len(bok__ynpcj[gsnbp__zaz]):
            bodo.libs.array_kernels.setna(yjjw__egq, gsnbp__zaz)
            continue
        yjjw__egq[gsnbp__zaz] = bok__ynpcj[gsnbp__zaz][i]
    for gsnbp__zaz in range(zjs__tiqy):
        if bodo.libs.array_kernels.isna(mlqi__mzj, gsnbp__zaz
            ) or bodo.libs.array_kernels.isna(yjjw__egq, mlqi__mzj[gsnbp__zaz]
            ):
            bodo.libs.array_kernels.setna(mzwod__grhbg, gsnbp__zaz)
            continue
        mzwod__grhbg[gsnbp__zaz] = yjjw__egq[mlqi__mzj[gsnbp__zaz]]
    return mzwod__grhbg


@register_jitable
def str_repeat_int(arr, repeats):
    bok__ynpcj = arr._data
    jpny__vgxvi = len(bok__ynpcj)
    yjjw__egq = pre_alloc_string_array(jpny__vgxvi, -1)
    for i in range(jpny__vgxvi):
        if bodo.libs.array_kernels.isna(bok__ynpcj, i):
            bodo.libs.array_kernels.setna(yjjw__egq, i)
            continue
        yjjw__egq[i] = bok__ynpcj[i] * repeats
    return init_dict_arr(yjjw__egq, arr._indices.copy(), arr.
        _has_global_dictionary, arr._has_deduped_local_dictionary and 
        repeats != 0)


def create_str2bool_methods(func_name):
    vojps__jkkt = f"""def str_{func_name}(arr):
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
    sja__yecz = {}
    exec(vojps__jkkt, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr}, sja__yecz)
    return sja__yecz[f'str_{func_name}']


def _register_str2bool_methods():
    for func_name in bodo.hiframes.pd_series_ext.str2bool_methods:
        tqnfk__iwfi = create_str2bool_methods(func_name)
        tqnfk__iwfi = register_jitable(tqnfk__iwfi)
        globals()[f'str_{func_name}'] = tqnfk__iwfi


_register_str2bool_methods()


@register_jitable
def str_extract(arr, pat, flags, n_cols):
    bok__ynpcj = arr._data
    mlqi__mzj = arr._indices
    jpny__vgxvi = len(bok__ynpcj)
    zjs__tiqy = len(mlqi__mzj)
    regex = re.compile(pat, flags=flags)
    xis__poq = []
    for ast__zwq in range(n_cols):
        xis__poq.append(pre_alloc_string_array(jpny__vgxvi, -1))
    fwder__koim = bodo.libs.bool_arr_ext.alloc_bool_array(jpny__vgxvi)
    ody__kjlbz = mlqi__mzj.copy()
    for i in range(jpny__vgxvi):
        if bodo.libs.array_kernels.isna(bok__ynpcj, i):
            fwder__koim[i] = True
            for gsnbp__zaz in range(n_cols):
                bodo.libs.array_kernels.setna(xis__poq[gsnbp__zaz], i)
            continue
        beuks__jsc = regex.search(bok__ynpcj[i])
        if beuks__jsc:
            fwder__koim[i] = False
            kvl__ginly = beuks__jsc.groups()
            for gsnbp__zaz in range(n_cols):
                xis__poq[gsnbp__zaz][i] = kvl__ginly[gsnbp__zaz]
        else:
            fwder__koim[i] = True
            for gsnbp__zaz in range(n_cols):
                bodo.libs.array_kernels.setna(xis__poq[gsnbp__zaz], i)
    for i in range(zjs__tiqy):
        if fwder__koim[ody__kjlbz[i]]:
            bodo.libs.array_kernels.setna(ody__kjlbz, i)
    vtw__dbs = [init_dict_arr(xis__poq[i], ody__kjlbz.copy(), arr.
        _has_global_dictionary, False) for i in range(n_cols)]
    return vtw__dbs


def create_extractall_methods(is_multi_group):
    kjr__viv = '_multi' if is_multi_group else ''
    vojps__jkkt = f"""def str_extractall{kjr__viv}(arr, regex, n_cols, index_arr):
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
    sja__yecz = {}
    exec(vojps__jkkt, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr, 'pre_alloc_string_array':
        pre_alloc_string_array}, sja__yecz)
    return sja__yecz[f'str_extractall{kjr__viv}']


def _register_extractall_methods():
    for is_multi_group in [True, False]:
        kjr__viv = '_multi' if is_multi_group else ''
        tqnfk__iwfi = create_extractall_methods(is_multi_group)
        tqnfk__iwfi = register_jitable(tqnfk__iwfi)
        globals()[f'str_extractall{kjr__viv}'] = tqnfk__iwfi


_register_extractall_methods()
