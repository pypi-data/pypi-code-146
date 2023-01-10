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
        yssz__ddye = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_),
            ('has_deduped_local_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, yssz__ddye)


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
        elvp__ndgvo, cimhj__rki, gpaj__ndk, tqe__avl = args
        mjw__jhpor = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        mjw__jhpor.data = elvp__ndgvo
        mjw__jhpor.indices = cimhj__rki
        mjw__jhpor.has_global_dictionary = gpaj__ndk
        mjw__jhpor.has_deduped_local_dictionary = tqe__avl
        context.nrt.incref(builder, signature.args[0], elvp__ndgvo)
        context.nrt.incref(builder, signature.args[1], cimhj__rki)
        return mjw__jhpor._getvalue()
    hdazf__wabz = DictionaryArrayType(data_t)
    wmi__qlyg = hdazf__wabz(data_t, indices_t, types.bool_, types.bool_)
    return wmi__qlyg, codegen


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
    klhw__qoh = c.pyapi.unserialize(c.pyapi.serialize_object(to_pa_dict_arr))
    val = c.pyapi.call_function_objargs(klhw__qoh, [val])
    c.pyapi.decref(klhw__qoh)
    mjw__jhpor = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    txelr__vmyjs = c.pyapi.object_getattr_string(val, 'dictionary')
    ota__mfbgz = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    wufzq__dwl = c.pyapi.call_method(txelr__vmyjs, 'to_numpy', (ota__mfbgz,))
    mjw__jhpor.data = c.unbox(typ.data, wufzq__dwl).value
    hikr__ertmq = c.pyapi.object_getattr_string(val, 'indices')
    srykg__gzx = c.context.insert_const_string(c.builder.module, 'pandas')
    oiv__iiboy = c.pyapi.import_module_noblock(srykg__gzx)
    bbyj__luw = c.pyapi.string_from_constant_string('Int32')
    gcbct__xatk = c.pyapi.call_method(oiv__iiboy, 'array', (hikr__ertmq,
        bbyj__luw))
    mjw__jhpor.indices = c.unbox(dict_indices_arr_type, gcbct__xatk).value
    mjw__jhpor.has_global_dictionary = c.context.get_constant(types.bool_, 
        False)
    mjw__jhpor.has_deduped_local_dictionary = c.context.get_constant(types.
        bool_, False)
    c.pyapi.decref(txelr__vmyjs)
    c.pyapi.decref(ota__mfbgz)
    c.pyapi.decref(wufzq__dwl)
    c.pyapi.decref(hikr__ertmq)
    c.pyapi.decref(oiv__iiboy)
    c.pyapi.decref(bbyj__luw)
    c.pyapi.decref(gcbct__xatk)
    c.pyapi.decref(val)
    run__bxyx = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(mjw__jhpor._getvalue(), is_error=run__bxyx)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    mjw__jhpor = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        if bodo.libs.str_arr_ext.use_pd_pyarrow_string_array:
            from bodo.libs.array import array_info_type, array_to_info_codegen
            qjse__umkb = array_to_info_codegen(c.context, c.builder,
                array_info_type(typ), (val,), incref=False)
            tjhj__tyb = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
                as_pointer()])
            pnt__eudiu = 'pd_pyarrow_array_from_string_array'
            idw__vixxf = cgutils.get_or_insert_function(c.builder.module,
                tjhj__tyb, name=pnt__eudiu)
            arr = c.builder.call(idw__vixxf, [qjse__umkb])
            c.context.nrt.decref(c.builder, typ, val)
            return arr
        c.context.nrt.incref(c.builder, typ.data, mjw__jhpor.data)
        exbu__emyzg = c.box(typ.data, mjw__jhpor.data)
        dmy__xmcl = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, mjw__jhpor.indices)
        tjhj__tyb = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        idw__vixxf = cgutils.get_or_insert_function(c.builder.module,
            tjhj__tyb, name='box_dict_str_array')
        bbtc__kdds = cgutils.create_struct_proxy(types.Array(types.int32, 1,
            'C'))(c.context, c.builder, dmy__xmcl.data)
        eed__rzczp = c.builder.extract_value(bbtc__kdds.shape, 0)
        tff__yoj = bbtc__kdds.data
        liwyl__abvvd = cgutils.create_struct_proxy(types.Array(types.int8, 
            1, 'C'))(c.context, c.builder, dmy__xmcl.null_bitmap).data
        wufzq__dwl = c.builder.call(idw__vixxf, [eed__rzczp, exbu__emyzg,
            tff__yoj, liwyl__abvvd])
        c.pyapi.decref(exbu__emyzg)
    else:
        srykg__gzx = c.context.insert_const_string(c.builder.module, 'pyarrow')
        tqes__hgqg = c.pyapi.import_module_noblock(srykg__gzx)
        spxry__kqup = c.pyapi.object_getattr_string(tqes__hgqg,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, mjw__jhpor.data)
        exbu__emyzg = c.box(typ.data, mjw__jhpor.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, mjw__jhpor.
            indices)
        hikr__ertmq = c.box(dict_indices_arr_type, mjw__jhpor.indices)
        uqj__pgnss = c.pyapi.call_method(spxry__kqup, 'from_arrays', (
            hikr__ertmq, exbu__emyzg))
        ota__mfbgz = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        wufzq__dwl = c.pyapi.call_method(uqj__pgnss, 'to_numpy', (ota__mfbgz,))
        c.pyapi.decref(tqes__hgqg)
        c.pyapi.decref(exbu__emyzg)
        c.pyapi.decref(hikr__ertmq)
        c.pyapi.decref(spxry__kqup)
        c.pyapi.decref(uqj__pgnss)
        c.pyapi.decref(ota__mfbgz)
    c.context.nrt.decref(c.builder, typ, val)
    return wufzq__dwl


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
    wbs__jwyj = pyval.dictionary.to_numpy(False)
    nxn__doinn = pd.array(pyval.indices, 'Int32')
    wbs__jwyj = context.get_constant_generic(builder, typ.data, wbs__jwyj)
    nxn__doinn = context.get_constant_generic(builder,
        dict_indices_arr_type, nxn__doinn)
    wip__pfd = context.get_constant(types.bool_, False)
    luw__sqdoj = context.get_constant(types.bool_, False)
    ukii__wsto = lir.Constant.literal_struct([wbs__jwyj, nxn__doinn,
        wip__pfd, luw__sqdoj])
    return ukii__wsto


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            uwisd__vkz = A._indices[ind]
            return A._data[uwisd__vkz]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary, A._has_deduped_local_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        elvp__ndgvo = A._data
        cimhj__rki = A._indices
        eed__rzczp = len(cimhj__rki)
        owwl__rvyq = [get_str_arr_item_length(elvp__ndgvo, i) for i in
            range(len(elvp__ndgvo))]
        vnak__mzmeh = 0
        for i in range(eed__rzczp):
            if not bodo.libs.array_kernels.isna(cimhj__rki, i):
                vnak__mzmeh += owwl__rvyq[cimhj__rki[i]]
        yev__czlcr = pre_alloc_string_array(eed__rzczp, vnak__mzmeh)
        for i in range(eed__rzczp):
            if bodo.libs.array_kernels.isna(cimhj__rki, i):
                bodo.libs.array_kernels.setna(yev__czlcr, i)
                continue
            ind = cimhj__rki[i]
            if bodo.libs.array_kernels.isna(elvp__ndgvo, ind):
                bodo.libs.array_kernels.setna(yev__czlcr, i)
                continue
            yev__czlcr[i] = elvp__ndgvo[ind]
        return yev__czlcr
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_unique(arr, val):
    uwisd__vkz = -1
    elvp__ndgvo = arr._data
    for i in range(len(elvp__ndgvo)):
        if bodo.libs.array_kernels.isna(elvp__ndgvo, i):
            continue
        if elvp__ndgvo[i] == val:
            uwisd__vkz = i
            break
    return uwisd__vkz


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_non_unique(arr, val):
    mqkm__fdd = set()
    elvp__ndgvo = arr._data
    for i in range(len(elvp__ndgvo)):
        if bodo.libs.array_kernels.isna(elvp__ndgvo, i):
            continue
        if elvp__ndgvo[i] == val:
            mqkm__fdd.add(i)
    return mqkm__fdd


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    eed__rzczp = len(arr)
    if arr._has_deduped_local_dictionary:
        uwisd__vkz = find_dict_ind_unique(arr, val)
        if uwisd__vkz == -1:
            return init_bool_array(np.full(eed__rzczp, False, np.bool_),
                arr._indices._null_bitmap.copy())
        return arr._indices == uwisd__vkz
    else:
        wee__jubey = find_dict_ind_non_unique(arr, val)
        if len(wee__jubey) == 0:
            return init_bool_array(np.full(eed__rzczp, False, np.bool_),
                arr._indices._null_bitmap.copy())
        xoys__zfbv = np.empty(eed__rzczp, dtype=np.bool_)
        for i in range(len(arr._indices)):
            xoys__zfbv[i] = arr._indices[i] in wee__jubey
        return init_bool_array(xoys__zfbv, arr._indices._null_bitmap.copy())


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    eed__rzczp = len(arr)
    if arr._has_deduped_local_dictionary:
        uwisd__vkz = find_dict_ind_unique(arr, val)
        if uwisd__vkz == -1:
            return init_bool_array(np.full(eed__rzczp, True, np.bool_), arr
                ._indices._null_bitmap.copy())
        return arr._indices != uwisd__vkz
    else:
        wee__jubey = find_dict_ind_non_unique(arr, val)
        if len(wee__jubey) == 0:
            return init_bool_array(np.full(eed__rzczp, True, np.bool_), arr
                ._indices._null_bitmap.copy())
        xoys__zfbv = np.empty(eed__rzczp, dtype=np.bool_)
        for i in range(len(arr._indices)):
            xoys__zfbv[i] = arr._indices[i] not in wee__jubey
        return init_bool_array(xoys__zfbv, arr._indices._null_bitmap.copy())


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
        wtek__gjo = arr._data
        pdrsy__cdwed = bodo.libs.int_arr_ext.alloc_int_array(len(wtek__gjo),
            dtype)
        for nutv__soep in range(len(wtek__gjo)):
            if bodo.libs.array_kernels.isna(wtek__gjo, nutv__soep):
                bodo.libs.array_kernels.setna(pdrsy__cdwed, nutv__soep)
                continue
            pdrsy__cdwed[nutv__soep] = np.int64(wtek__gjo[nutv__soep])
        eed__rzczp = len(arr)
        cimhj__rki = arr._indices
        yev__czlcr = bodo.libs.int_arr_ext.alloc_int_array(eed__rzczp, dtype)
        for i in range(eed__rzczp):
            if bodo.libs.array_kernels.isna(cimhj__rki, i):
                bodo.libs.array_kernels.setna(yev__czlcr, i)
                continue
            yev__czlcr[i] = pdrsy__cdwed[cimhj__rki[i]]
        return yev__czlcr
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    rwsju__wboxr = len(arrs)
    zklwu__cqyq = 'def impl(arrs, sep):\n'
    zklwu__cqyq += '  ind_map = {}\n'
    zklwu__cqyq += '  out_strs = []\n'
    zklwu__cqyq += '  n = len(arrs[0])\n'
    for i in range(rwsju__wboxr):
        zklwu__cqyq += f'  indices{i} = arrs[{i}]._indices\n'
    for i in range(rwsju__wboxr):
        zklwu__cqyq += f'  data{i} = arrs[{i}]._data\n'
    zklwu__cqyq += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    zklwu__cqyq += '  for i in range(n):\n'
    rofdk__icisw = ' or '.join([
        f'bodo.libs.array_kernels.isna(arrs[{i}], i)' for i in range(
        rwsju__wboxr)])
    zklwu__cqyq += f'    if {rofdk__icisw}:\n'
    zklwu__cqyq += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    zklwu__cqyq += '      continue\n'
    for i in range(rwsju__wboxr):
        zklwu__cqyq += f'    ind{i} = indices{i}[i]\n'
    cjqj__dwoh = '(' + ', '.join(f'ind{i}' for i in range(rwsju__wboxr)) + ')'
    zklwu__cqyq += f'    if {cjqj__dwoh} not in ind_map:\n'
    zklwu__cqyq += '      out_ind = len(out_strs)\n'
    zklwu__cqyq += f'      ind_map[{cjqj__dwoh}] = out_ind\n'
    vup__wpij = "''" if is_overload_none(sep) else 'sep'
    lmm__oufay = ', '.join([f'data{i}[ind{i}]' for i in range(rwsju__wboxr)])
    zklwu__cqyq += f'      v = {vup__wpij}.join([{lmm__oufay}])\n'
    zklwu__cqyq += '      out_strs.append(v)\n'
    zklwu__cqyq += '    else:\n'
    zklwu__cqyq += f'      out_ind = ind_map[{cjqj__dwoh}]\n'
    zklwu__cqyq += '    out_indices[i] = out_ind\n'
    zklwu__cqyq += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    zklwu__cqyq += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False, False)
"""
    wqxr__ixjhz = {}
    exec(zklwu__cqyq, {'bodo': bodo, 'numba': numba, 'np': np}, wqxr__ixjhz)
    impl = wqxr__ixjhz['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    tppa__lnku = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    wmi__qlyg = toty(fromty)
    qrkl__jjqw = context.compile_internal(builder, tppa__lnku, wmi__qlyg, (
        val,))
    return impl_ret_new_ref(context, builder, toty, qrkl__jjqw)


@register_jitable
def dict_arr_to_numeric(arr, errors, downcast):
    mjw__jhpor = arr._data
    dict_arr_out = pd.to_numeric(mjw__jhpor, errors, downcast)
    nxn__doinn = arr._indices
    amn__uccr = len(nxn__doinn)
    yev__czlcr = bodo.utils.utils.alloc_type(amn__uccr, dict_arr_out, (-1,))
    for i in range(amn__uccr):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(yev__czlcr, i)
            continue
        uwisd__vkz = nxn__doinn[i]
        if bodo.libs.array_kernels.isna(dict_arr_out, uwisd__vkz):
            bodo.libs.array_kernels.setna(yev__czlcr, i)
            continue
        yev__czlcr[i] = dict_arr_out[uwisd__vkz]
    return yev__czlcr


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    wbs__jwyj = arr._data
    kvv__ixzlh = len(wbs__jwyj)
    ktfxk__hotwi = pre_alloc_string_array(kvv__ixzlh, -1)
    if regex:
        gmdv__ktaz = re.compile(pat, flags)
        for i in range(kvv__ixzlh):
            if bodo.libs.array_kernels.isna(wbs__jwyj, i):
                bodo.libs.array_kernels.setna(ktfxk__hotwi, i)
                continue
            ktfxk__hotwi[i] = gmdv__ktaz.sub(repl=repl, string=wbs__jwyj[i])
    else:
        for i in range(kvv__ixzlh):
            if bodo.libs.array_kernels.isna(wbs__jwyj, i):
                bodo.libs.array_kernels.setna(ktfxk__hotwi, i)
                continue
            ktfxk__hotwi[i] = wbs__jwyj[i].replace(pat, repl)
    return init_dict_arr(ktfxk__hotwi, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_startswith(arr, pat, na):
    mjw__jhpor = arr._data
    riij__wyzv = len(mjw__jhpor)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(riij__wyzv)
    for i in range(riij__wyzv):
        dict_arr_out[i] = mjw__jhpor[i].startswith(pat)
    nxn__doinn = arr._indices
    amn__uccr = len(nxn__doinn)
    yev__czlcr = bodo.libs.bool_arr_ext.alloc_bool_array(amn__uccr)
    for i in range(amn__uccr):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(yev__czlcr, i)
        else:
            yev__czlcr[i] = dict_arr_out[nxn__doinn[i]]
    return yev__czlcr


@register_jitable
def str_endswith(arr, pat, na):
    mjw__jhpor = arr._data
    riij__wyzv = len(mjw__jhpor)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(riij__wyzv)
    for i in range(riij__wyzv):
        dict_arr_out[i] = mjw__jhpor[i].endswith(pat)
    nxn__doinn = arr._indices
    amn__uccr = len(nxn__doinn)
    yev__czlcr = bodo.libs.bool_arr_ext.alloc_bool_array(amn__uccr)
    for i in range(amn__uccr):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(yev__czlcr, i)
        else:
            yev__czlcr[i] = dict_arr_out[nxn__doinn[i]]
    return yev__czlcr


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    mjw__jhpor = arr._data
    quhuh__ydvzg = pd.Series(mjw__jhpor)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = pd.array(quhuh__ydvzg.array, 'string')._str_contains(pat
            , case, flags, na, regex)
    nxn__doinn = arr._indices
    amn__uccr = len(nxn__doinn)
    yev__czlcr = bodo.libs.bool_arr_ext.alloc_bool_array(amn__uccr)
    for i in range(amn__uccr):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(yev__czlcr, i)
        else:
            yev__czlcr[i] = dict_arr_out[nxn__doinn[i]]
    return yev__czlcr


@register_jitable
def str_contains_non_regex(arr, pat, case):
    mjw__jhpor = arr._data
    riij__wyzv = len(mjw__jhpor)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(riij__wyzv)
    if not case:
        eoxop__zpztf = pat.upper()
    for i in range(riij__wyzv):
        if case:
            dict_arr_out[i] = pat in mjw__jhpor[i]
        else:
            dict_arr_out[i] = eoxop__zpztf in mjw__jhpor[i].upper()
    nxn__doinn = arr._indices
    amn__uccr = len(nxn__doinn)
    yev__czlcr = bodo.libs.bool_arr_ext.alloc_bool_array(amn__uccr)
    for i in range(amn__uccr):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(yev__czlcr, i)
        else:
            yev__czlcr[i] = dict_arr_out[nxn__doinn[i]]
    return yev__czlcr


@numba.njit
def str_match(arr, pat, case, flags, na):
    mjw__jhpor = arr._data
    nxn__doinn = arr._indices
    amn__uccr = len(nxn__doinn)
    yev__czlcr = bodo.libs.bool_arr_ext.alloc_bool_array(amn__uccr)
    quhuh__ydvzg = pd.Series(mjw__jhpor)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = quhuh__ydvzg.array._str_match(pat, case, flags, na)
    for i in range(amn__uccr):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(yev__czlcr, i)
        else:
            yev__czlcr[i] = dict_arr_out[nxn__doinn[i]]
    return yev__czlcr


def create_simple_str2str_methods(func_name, func_args, can_create_non_unique):
    zklwu__cqyq = f"""def str_{func_name}({', '.join(func_args)}):
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
        zklwu__cqyq += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, False)
"""
    else:
        zklwu__cqyq += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, arr._has_deduped_local_dictionary)
"""
    wqxr__ixjhz = {}
    exec(zklwu__cqyq, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, wqxr__ixjhz)
    return wqxr__ixjhz[f'str_{func_name}']


def _register_simple_str2str_methods():
    izqdu__wtn = {**dict.fromkeys(['capitalize', 'lower', 'swapcase',
        'title', 'upper'], ('arr',)), **dict.fromkeys(['lstrip', 'rstrip',
        'strip'], ('arr', 'to_strip')), **dict.fromkeys(['center', 'ljust',
        'rjust'], ('arr', 'width', 'fillchar')), **dict.fromkeys(['zfill'],
        ('arr', 'width'))}
    pnt__tis = {**dict.fromkeys(['capitalize', 'lower', 'title', 'upper',
        'lstrip', 'rstrip', 'strip', 'center', 'zfill', 'ljust', 'rjust'], 
        True), **dict.fromkeys(['swapcase'], False)}
    for func_name in izqdu__wtn.keys():
        abf__rdc = create_simple_str2str_methods(func_name, izqdu__wtn[
            func_name], pnt__tis[func_name])
        abf__rdc = register_jitable(abf__rdc)
        globals()[f'str_{func_name}'] = abf__rdc


_register_simple_str2str_methods()


@register_jitable
def str_index(arr, sub, start, end):
    wbs__jwyj = arr._data
    nxn__doinn = arr._indices
    kvv__ixzlh = len(wbs__jwyj)
    amn__uccr = len(nxn__doinn)
    pbra__ifre = bodo.libs.int_arr_ext.alloc_int_array(kvv__ixzlh, np.int64)
    yev__czlcr = bodo.libs.int_arr_ext.alloc_int_array(amn__uccr, np.int64)
    shx__uqqv = False
    for i in range(kvv__ixzlh):
        if bodo.libs.array_kernels.isna(wbs__jwyj, i):
            bodo.libs.array_kernels.setna(pbra__ifre, i)
        else:
            pbra__ifre[i] = wbs__jwyj[i].find(sub, start, end)
    for i in range(amn__uccr):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(pbra__ifre, nxn__doinn[i]):
            bodo.libs.array_kernels.setna(yev__czlcr, i)
        else:
            yev__czlcr[i] = pbra__ifre[nxn__doinn[i]]
            if yev__czlcr[i] == -1:
                shx__uqqv = True
    oodpe__qqs = 'substring not found' if shx__uqqv else ''
    synchronize_error_njit('ValueError', oodpe__qqs)
    return yev__czlcr


@register_jitable
def str_rindex(arr, sub, start, end):
    wbs__jwyj = arr._data
    nxn__doinn = arr._indices
    kvv__ixzlh = len(wbs__jwyj)
    amn__uccr = len(nxn__doinn)
    pbra__ifre = bodo.libs.int_arr_ext.alloc_int_array(kvv__ixzlh, np.int64)
    yev__czlcr = bodo.libs.int_arr_ext.alloc_int_array(amn__uccr, np.int64)
    shx__uqqv = False
    for i in range(kvv__ixzlh):
        if bodo.libs.array_kernels.isna(wbs__jwyj, i):
            bodo.libs.array_kernels.setna(pbra__ifre, i)
        else:
            pbra__ifre[i] = wbs__jwyj[i].rindex(sub, start, end)
    for i in range(amn__uccr):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(pbra__ifre, nxn__doinn[i]):
            bodo.libs.array_kernels.setna(yev__czlcr, i)
        else:
            yev__czlcr[i] = pbra__ifre[nxn__doinn[i]]
            if yev__czlcr[i] == -1:
                shx__uqqv = True
    oodpe__qqs = 'substring not found' if shx__uqqv else ''
    synchronize_error_njit('ValueError', oodpe__qqs)
    return yev__czlcr


def create_find_methods(func_name):
    zklwu__cqyq = f"""def str_{func_name}(arr, sub, start, end):
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
    wqxr__ixjhz = {}
    exec(zklwu__cqyq, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr, 'np': np}, wqxr__ixjhz)
    return wqxr__ixjhz[f'str_{func_name}']


def _register_find_methods():
    ochdu__lbzuf = ['find', 'rfind']
    for func_name in ochdu__lbzuf:
        abf__rdc = create_find_methods(func_name)
        abf__rdc = register_jitable(abf__rdc)
        globals()[f'str_{func_name}'] = abf__rdc


_register_find_methods()


@register_jitable
def str_count(arr, pat, flags):
    wbs__jwyj = arr._data
    nxn__doinn = arr._indices
    kvv__ixzlh = len(wbs__jwyj)
    amn__uccr = len(nxn__doinn)
    pbra__ifre = bodo.libs.int_arr_ext.alloc_int_array(kvv__ixzlh, np.int64)
    fuw__hmcsk = bodo.libs.int_arr_ext.alloc_int_array(amn__uccr, np.int64)
    regex = re.compile(pat, flags)
    for i in range(kvv__ixzlh):
        if bodo.libs.array_kernels.isna(wbs__jwyj, i):
            bodo.libs.array_kernels.setna(pbra__ifre, i)
            continue
        pbra__ifre[i] = bodo.libs.str_ext.str_findall_count(regex, wbs__jwyj[i]
            )
    for i in range(amn__uccr):
        if bodo.libs.array_kernels.isna(nxn__doinn, i
            ) or bodo.libs.array_kernels.isna(pbra__ifre, nxn__doinn[i]):
            bodo.libs.array_kernels.setna(fuw__hmcsk, i)
        else:
            fuw__hmcsk[i] = pbra__ifre[nxn__doinn[i]]
    return fuw__hmcsk


@register_jitable
def str_len(arr):
    wbs__jwyj = arr._data
    nxn__doinn = arr._indices
    amn__uccr = len(nxn__doinn)
    pbra__ifre = bodo.libs.array_kernels.get_arr_lens(wbs__jwyj, False)
    fuw__hmcsk = bodo.libs.int_arr_ext.alloc_int_array(amn__uccr, np.int64)
    for i in range(amn__uccr):
        if bodo.libs.array_kernels.isna(nxn__doinn, i
            ) or bodo.libs.array_kernels.isna(pbra__ifre, nxn__doinn[i]):
            bodo.libs.array_kernels.setna(fuw__hmcsk, i)
        else:
            fuw__hmcsk[i] = pbra__ifre[nxn__doinn[i]]
    return fuw__hmcsk


@register_jitable
def str_slice(arr, start, stop, step):
    wbs__jwyj = arr._data
    kvv__ixzlh = len(wbs__jwyj)
    ktfxk__hotwi = bodo.libs.str_arr_ext.pre_alloc_string_array(kvv__ixzlh, -1)
    for i in range(kvv__ixzlh):
        if bodo.libs.array_kernels.isna(wbs__jwyj, i):
            bodo.libs.array_kernels.setna(ktfxk__hotwi, i)
            continue
        ktfxk__hotwi[i] = wbs__jwyj[i][start:stop:step]
    return init_dict_arr(ktfxk__hotwi, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_get(arr, i):
    wbs__jwyj = arr._data
    nxn__doinn = arr._indices
    kvv__ixzlh = len(wbs__jwyj)
    amn__uccr = len(nxn__doinn)
    ktfxk__hotwi = pre_alloc_string_array(kvv__ixzlh, -1)
    yev__czlcr = pre_alloc_string_array(amn__uccr, -1)
    for nutv__soep in range(kvv__ixzlh):
        if bodo.libs.array_kernels.isna(wbs__jwyj, nutv__soep) or not -len(
            wbs__jwyj[nutv__soep]) <= i < len(wbs__jwyj[nutv__soep]):
            bodo.libs.array_kernels.setna(ktfxk__hotwi, nutv__soep)
            continue
        ktfxk__hotwi[nutv__soep] = wbs__jwyj[nutv__soep][i]
    for nutv__soep in range(amn__uccr):
        if bodo.libs.array_kernels.isna(nxn__doinn, nutv__soep
            ) or bodo.libs.array_kernels.isna(ktfxk__hotwi, nxn__doinn[
            nutv__soep]):
            bodo.libs.array_kernels.setna(yev__czlcr, nutv__soep)
            continue
        yev__czlcr[nutv__soep] = ktfxk__hotwi[nxn__doinn[nutv__soep]]
    return yev__czlcr


@register_jitable
def str_repeat_int(arr, repeats):
    wbs__jwyj = arr._data
    kvv__ixzlh = len(wbs__jwyj)
    ktfxk__hotwi = pre_alloc_string_array(kvv__ixzlh, -1)
    for i in range(kvv__ixzlh):
        if bodo.libs.array_kernels.isna(wbs__jwyj, i):
            bodo.libs.array_kernels.setna(ktfxk__hotwi, i)
            continue
        ktfxk__hotwi[i] = wbs__jwyj[i] * repeats
    return init_dict_arr(ktfxk__hotwi, arr._indices.copy(), arr.
        _has_global_dictionary, arr._has_deduped_local_dictionary and 
        repeats != 0)


def create_str2bool_methods(func_name):
    zklwu__cqyq = f"""def str_{func_name}(arr):
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
    wqxr__ixjhz = {}
    exec(zklwu__cqyq, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr}, wqxr__ixjhz)
    return wqxr__ixjhz[f'str_{func_name}']


def _register_str2bool_methods():
    for func_name in bodo.hiframes.pd_series_ext.str2bool_methods:
        abf__rdc = create_str2bool_methods(func_name)
        abf__rdc = register_jitable(abf__rdc)
        globals()[f'str_{func_name}'] = abf__rdc


_register_str2bool_methods()


@register_jitable
def str_extract(arr, pat, flags, n_cols):
    wbs__jwyj = arr._data
    nxn__doinn = arr._indices
    kvv__ixzlh = len(wbs__jwyj)
    amn__uccr = len(nxn__doinn)
    regex = re.compile(pat, flags=flags)
    rrzm__ithr = []
    for mljnl__ncdlm in range(n_cols):
        rrzm__ithr.append(pre_alloc_string_array(kvv__ixzlh, -1))
    vypm__otx = bodo.libs.bool_arr_ext.alloc_bool_array(kvv__ixzlh)
    uitns__ilkfg = nxn__doinn.copy()
    for i in range(kvv__ixzlh):
        if bodo.libs.array_kernels.isna(wbs__jwyj, i):
            vypm__otx[i] = True
            for nutv__soep in range(n_cols):
                bodo.libs.array_kernels.setna(rrzm__ithr[nutv__soep], i)
            continue
        snrp__gya = regex.search(wbs__jwyj[i])
        if snrp__gya:
            vypm__otx[i] = False
            hhndw__ibmpb = snrp__gya.groups()
            for nutv__soep in range(n_cols):
                rrzm__ithr[nutv__soep][i] = hhndw__ibmpb[nutv__soep]
        else:
            vypm__otx[i] = True
            for nutv__soep in range(n_cols):
                bodo.libs.array_kernels.setna(rrzm__ithr[nutv__soep], i)
    for i in range(amn__uccr):
        if vypm__otx[uitns__ilkfg[i]]:
            bodo.libs.array_kernels.setna(uitns__ilkfg, i)
    xqky__expt = [init_dict_arr(rrzm__ithr[i], uitns__ilkfg.copy(), arr.
        _has_global_dictionary, False) for i in range(n_cols)]
    return xqky__expt


def create_extractall_methods(is_multi_group):
    ygarf__ogxg = '_multi' if is_multi_group else ''
    zklwu__cqyq = f"""def str_extractall{ygarf__ogxg}(arr, regex, n_cols, index_arr):
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
    wqxr__ixjhz = {}
    exec(zklwu__cqyq, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr, 'pre_alloc_string_array':
        pre_alloc_string_array}, wqxr__ixjhz)
    return wqxr__ixjhz[f'str_extractall{ygarf__ogxg}']


def _register_extractall_methods():
    for is_multi_group in [True, False]:
        ygarf__ogxg = '_multi' if is_multi_group else ''
        abf__rdc = create_extractall_methods(is_multi_group)
        abf__rdc = register_jitable(abf__rdc)
        globals()[f'str_extractall{ygarf__ogxg}'] = abf__rdc


_register_extractall_methods()
