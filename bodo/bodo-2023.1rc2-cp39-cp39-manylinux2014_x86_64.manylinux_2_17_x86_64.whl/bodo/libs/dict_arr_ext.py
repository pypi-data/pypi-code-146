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
        ayk__xrlb = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_),
            ('has_deduped_local_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, ayk__xrlb)


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
        puy__iwo, ncehu__uje, wkfth__oofyy, xgi__omsz = args
        oafz__tif = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        oafz__tif.data = puy__iwo
        oafz__tif.indices = ncehu__uje
        oafz__tif.has_global_dictionary = wkfth__oofyy
        oafz__tif.has_deduped_local_dictionary = xgi__omsz
        context.nrt.incref(builder, signature.args[0], puy__iwo)
        context.nrt.incref(builder, signature.args[1], ncehu__uje)
        return oafz__tif._getvalue()
    xcv__ppbh = DictionaryArrayType(data_t)
    ekvb__tjc = xcv__ppbh(data_t, indices_t, types.bool_, types.bool_)
    return ekvb__tjc, codegen


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
    mcefn__gpiz = c.pyapi.unserialize(c.pyapi.serialize_object(to_pa_dict_arr))
    val = c.pyapi.call_function_objargs(mcefn__gpiz, [val])
    c.pyapi.decref(mcefn__gpiz)
    oafz__tif = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fbfuh__wnsd = c.pyapi.object_getattr_string(val, 'dictionary')
    dksyq__pohkh = c.pyapi.bool_from_bool(c.context.get_constant(types.
        bool_, False))
    yrmti__esl = c.pyapi.call_method(fbfuh__wnsd, 'to_numpy', (dksyq__pohkh,))
    oafz__tif.data = c.unbox(typ.data, yrmti__esl).value
    ufti__hxhvt = c.pyapi.object_getattr_string(val, 'indices')
    qua__taztk = c.context.insert_const_string(c.builder.module, 'pandas')
    uiml__bjxa = c.pyapi.import_module_noblock(qua__taztk)
    rvge__swl = c.pyapi.string_from_constant_string('Int32')
    gemkv__irpo = c.pyapi.call_method(uiml__bjxa, 'array', (ufti__hxhvt,
        rvge__swl))
    oafz__tif.indices = c.unbox(dict_indices_arr_type, gemkv__irpo).value
    oafz__tif.has_global_dictionary = c.context.get_constant(types.bool_, False
        )
    oafz__tif.has_deduped_local_dictionary = c.context.get_constant(types.
        bool_, False)
    c.pyapi.decref(fbfuh__wnsd)
    c.pyapi.decref(dksyq__pohkh)
    c.pyapi.decref(yrmti__esl)
    c.pyapi.decref(ufti__hxhvt)
    c.pyapi.decref(uiml__bjxa)
    c.pyapi.decref(rvge__swl)
    c.pyapi.decref(gemkv__irpo)
    c.pyapi.decref(val)
    poss__npzh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(oafz__tif._getvalue(), is_error=poss__npzh)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    oafz__tif = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        if bodo.libs.str_arr_ext.use_pd_pyarrow_string_array:
            from bodo.libs.array import array_info_type, array_to_info_codegen
            pqvdo__legb = array_to_info_codegen(c.context, c.builder,
                array_info_type(typ), (val,), incref=False)
            zrrm__mpxin = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
                as_pointer()])
            kba__ywew = 'pd_pyarrow_array_from_string_array'
            fnss__flry = cgutils.get_or_insert_function(c.builder.module,
                zrrm__mpxin, name=kba__ywew)
            arr = c.builder.call(fnss__flry, [pqvdo__legb])
            c.context.nrt.decref(c.builder, typ, val)
            return arr
        c.context.nrt.incref(c.builder, typ.data, oafz__tif.data)
        ptveg__dwcjp = c.box(typ.data, oafz__tif.data)
        dsn__amvuq = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, oafz__tif.indices)
        zrrm__mpxin = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        fnss__flry = cgutils.get_or_insert_function(c.builder.module,
            zrrm__mpxin, name='box_dict_str_array')
        pkrjm__rhv = cgutils.create_struct_proxy(types.Array(types.int32, 1,
            'C'))(c.context, c.builder, dsn__amvuq.data)
        thux__ocbxl = c.builder.extract_value(pkrjm__rhv.shape, 0)
        oezmi__fcrnd = pkrjm__rhv.data
        qxwfn__uhg = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, dsn__amvuq.null_bitmap).data
        yrmti__esl = c.builder.call(fnss__flry, [thux__ocbxl, ptveg__dwcjp,
            oezmi__fcrnd, qxwfn__uhg])
        c.pyapi.decref(ptveg__dwcjp)
    else:
        qua__taztk = c.context.insert_const_string(c.builder.module, 'pyarrow')
        kxjox__zldph = c.pyapi.import_module_noblock(qua__taztk)
        dclfo__ddvvw = c.pyapi.object_getattr_string(kxjox__zldph,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, oafz__tif.data)
        ptveg__dwcjp = c.box(typ.data, oafz__tif.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, oafz__tif.
            indices)
        ufti__hxhvt = c.box(dict_indices_arr_type, oafz__tif.indices)
        tjjqn__zgdvd = c.pyapi.call_method(dclfo__ddvvw, 'from_arrays', (
            ufti__hxhvt, ptveg__dwcjp))
        dksyq__pohkh = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        yrmti__esl = c.pyapi.call_method(tjjqn__zgdvd, 'to_numpy', (
            dksyq__pohkh,))
        c.pyapi.decref(kxjox__zldph)
        c.pyapi.decref(ptveg__dwcjp)
        c.pyapi.decref(ufti__hxhvt)
        c.pyapi.decref(dclfo__ddvvw)
        c.pyapi.decref(tjjqn__zgdvd)
        c.pyapi.decref(dksyq__pohkh)
    c.context.nrt.decref(c.builder, typ, val)
    return yrmti__esl


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
    rjd__gyoh = pyval.dictionary.to_numpy(False)
    rbz__tfa = pd.array(pyval.indices, 'Int32')
    rjd__gyoh = context.get_constant_generic(builder, typ.data, rjd__gyoh)
    rbz__tfa = context.get_constant_generic(builder, dict_indices_arr_type,
        rbz__tfa)
    ldub__ilfk = context.get_constant(types.bool_, False)
    fmepe__elbrm = context.get_constant(types.bool_, False)
    arv__kya = lir.Constant.literal_struct([rjd__gyoh, rbz__tfa, ldub__ilfk,
        fmepe__elbrm])
    return arv__kya


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            zscy__ygkm = A._indices[ind]
            return A._data[zscy__ygkm]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary, A._has_deduped_local_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        puy__iwo = A._data
        ncehu__uje = A._indices
        thux__ocbxl = len(ncehu__uje)
        fiwt__ctu = [get_str_arr_item_length(puy__iwo, i) for i in range(
            len(puy__iwo))]
        xocw__ram = 0
        for i in range(thux__ocbxl):
            if not bodo.libs.array_kernels.isna(ncehu__uje, i):
                xocw__ram += fiwt__ctu[ncehu__uje[i]]
        wpux__adn = pre_alloc_string_array(thux__ocbxl, xocw__ram)
        for i in range(thux__ocbxl):
            if bodo.libs.array_kernels.isna(ncehu__uje, i):
                bodo.libs.array_kernels.setna(wpux__adn, i)
                continue
            ind = ncehu__uje[i]
            if bodo.libs.array_kernels.isna(puy__iwo, ind):
                bodo.libs.array_kernels.setna(wpux__adn, i)
                continue
            wpux__adn[i] = puy__iwo[ind]
        return wpux__adn
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_unique(arr, val):
    zscy__ygkm = -1
    puy__iwo = arr._data
    for i in range(len(puy__iwo)):
        if bodo.libs.array_kernels.isna(puy__iwo, i):
            continue
        if puy__iwo[i] == val:
            zscy__ygkm = i
            break
    return zscy__ygkm


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_non_unique(arr, val):
    crthr__sooq = set()
    puy__iwo = arr._data
    for i in range(len(puy__iwo)):
        if bodo.libs.array_kernels.isna(puy__iwo, i):
            continue
        if puy__iwo[i] == val:
            crthr__sooq.add(i)
    return crthr__sooq


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    thux__ocbxl = len(arr)
    if arr._has_deduped_local_dictionary:
        zscy__ygkm = find_dict_ind_unique(arr, val)
        if zscy__ygkm == -1:
            return init_bool_array(np.full(thux__ocbxl, False, np.bool_),
                arr._indices._null_bitmap.copy())
        return arr._indices == zscy__ygkm
    else:
        qyd__gbnp = find_dict_ind_non_unique(arr, val)
        if len(qyd__gbnp) == 0:
            return init_bool_array(np.full(thux__ocbxl, False, np.bool_),
                arr._indices._null_bitmap.copy())
        sblp__sjyh = np.empty(thux__ocbxl, dtype=np.bool_)
        for i in range(len(arr._indices)):
            sblp__sjyh[i] = arr._indices[i] in qyd__gbnp
        return init_bool_array(sblp__sjyh, arr._indices._null_bitmap.copy())


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    thux__ocbxl = len(arr)
    if arr._has_deduped_local_dictionary:
        zscy__ygkm = find_dict_ind_unique(arr, val)
        if zscy__ygkm == -1:
            return init_bool_array(np.full(thux__ocbxl, True, np.bool_),
                arr._indices._null_bitmap.copy())
        return arr._indices != zscy__ygkm
    else:
        qyd__gbnp = find_dict_ind_non_unique(arr, val)
        if len(qyd__gbnp) == 0:
            return init_bool_array(np.full(thux__ocbxl, True, np.bool_),
                arr._indices._null_bitmap.copy())
        sblp__sjyh = np.empty(thux__ocbxl, dtype=np.bool_)
        for i in range(len(arr._indices)):
            sblp__sjyh[i] = arr._indices[i] not in qyd__gbnp
        return init_bool_array(sblp__sjyh, arr._indices._null_bitmap.copy())


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
        ryhh__zkta = arr._data
        gkfu__pekn = bodo.libs.int_arr_ext.alloc_int_array(len(ryhh__zkta),
            dtype)
        for ejat__czb in range(len(ryhh__zkta)):
            if bodo.libs.array_kernels.isna(ryhh__zkta, ejat__czb):
                bodo.libs.array_kernels.setna(gkfu__pekn, ejat__czb)
                continue
            gkfu__pekn[ejat__czb] = np.int64(ryhh__zkta[ejat__czb])
        thux__ocbxl = len(arr)
        ncehu__uje = arr._indices
        wpux__adn = bodo.libs.int_arr_ext.alloc_int_array(thux__ocbxl, dtype)
        for i in range(thux__ocbxl):
            if bodo.libs.array_kernels.isna(ncehu__uje, i):
                bodo.libs.array_kernels.setna(wpux__adn, i)
                continue
            wpux__adn[i] = gkfu__pekn[ncehu__uje[i]]
        return wpux__adn
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    usgil__iobb = len(arrs)
    ycytu__rorta = 'def impl(arrs, sep):\n'
    ycytu__rorta += '  ind_map = {}\n'
    ycytu__rorta += '  out_strs = []\n'
    ycytu__rorta += '  n = len(arrs[0])\n'
    for i in range(usgil__iobb):
        ycytu__rorta += f'  indices{i} = arrs[{i}]._indices\n'
    for i in range(usgil__iobb):
        ycytu__rorta += f'  data{i} = arrs[{i}]._data\n'
    ycytu__rorta += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    ycytu__rorta += '  for i in range(n):\n'
    uajs__nmzi = ' or '.join([f'bodo.libs.array_kernels.isna(arrs[{i}], i)' for
        i in range(usgil__iobb)])
    ycytu__rorta += f'    if {uajs__nmzi}:\n'
    ycytu__rorta += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    ycytu__rorta += '      continue\n'
    for i in range(usgil__iobb):
        ycytu__rorta += f'    ind{i} = indices{i}[i]\n'
    hfal__fqq = '(' + ', '.join(f'ind{i}' for i in range(usgil__iobb)) + ')'
    ycytu__rorta += f'    if {hfal__fqq} not in ind_map:\n'
    ycytu__rorta += '      out_ind = len(out_strs)\n'
    ycytu__rorta += f'      ind_map[{hfal__fqq}] = out_ind\n'
    gbag__jlzvl = "''" if is_overload_none(sep) else 'sep'
    gspj__urmwm = ', '.join([f'data{i}[ind{i}]' for i in range(usgil__iobb)])
    ycytu__rorta += f'      v = {gbag__jlzvl}.join([{gspj__urmwm}])\n'
    ycytu__rorta += '      out_strs.append(v)\n'
    ycytu__rorta += '    else:\n'
    ycytu__rorta += f'      out_ind = ind_map[{hfal__fqq}]\n'
    ycytu__rorta += '    out_indices[i] = out_ind\n'
    ycytu__rorta += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    ycytu__rorta += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False, False)
"""
    yvz__pffx = {}
    exec(ycytu__rorta, {'bodo': bodo, 'numba': numba, 'np': np}, yvz__pffx)
    impl = yvz__pffx['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    yaedl__ksy = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    ekvb__tjc = toty(fromty)
    znk__wlvs = context.compile_internal(builder, yaedl__ksy, ekvb__tjc, (val,)
        )
    return impl_ret_new_ref(context, builder, toty, znk__wlvs)


@register_jitable
def dict_arr_to_numeric(arr, errors, downcast):
    oafz__tif = arr._data
    dict_arr_out = pd.to_numeric(oafz__tif, errors, downcast)
    rbz__tfa = arr._indices
    bjlcy__yhqx = len(rbz__tfa)
    wpux__adn = bodo.utils.utils.alloc_type(bjlcy__yhqx, dict_arr_out, (-1,))
    for i in range(bjlcy__yhqx):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(wpux__adn, i)
            continue
        zscy__ygkm = rbz__tfa[i]
        if bodo.libs.array_kernels.isna(dict_arr_out, zscy__ygkm):
            bodo.libs.array_kernels.setna(wpux__adn, i)
            continue
        wpux__adn[i] = dict_arr_out[zscy__ygkm]
    return wpux__adn


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    rjd__gyoh = arr._data
    nul__babxm = len(rjd__gyoh)
    keq__qfrwj = pre_alloc_string_array(nul__babxm, -1)
    if regex:
        ubwx__niqt = re.compile(pat, flags)
        for i in range(nul__babxm):
            if bodo.libs.array_kernels.isna(rjd__gyoh, i):
                bodo.libs.array_kernels.setna(keq__qfrwj, i)
                continue
            keq__qfrwj[i] = ubwx__niqt.sub(repl=repl, string=rjd__gyoh[i])
    else:
        for i in range(nul__babxm):
            if bodo.libs.array_kernels.isna(rjd__gyoh, i):
                bodo.libs.array_kernels.setna(keq__qfrwj, i)
                continue
            keq__qfrwj[i] = rjd__gyoh[i].replace(pat, repl)
    return init_dict_arr(keq__qfrwj, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_startswith(arr, pat, na):
    oafz__tif = arr._data
    wig__kfvhh = len(oafz__tif)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(wig__kfvhh)
    for i in range(wig__kfvhh):
        dict_arr_out[i] = oafz__tif[i].startswith(pat)
    rbz__tfa = arr._indices
    bjlcy__yhqx = len(rbz__tfa)
    wpux__adn = bodo.libs.bool_arr_ext.alloc_bool_array(bjlcy__yhqx)
    for i in range(bjlcy__yhqx):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(wpux__adn, i)
        else:
            wpux__adn[i] = dict_arr_out[rbz__tfa[i]]
    return wpux__adn


@register_jitable
def str_endswith(arr, pat, na):
    oafz__tif = arr._data
    wig__kfvhh = len(oafz__tif)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(wig__kfvhh)
    for i in range(wig__kfvhh):
        dict_arr_out[i] = oafz__tif[i].endswith(pat)
    rbz__tfa = arr._indices
    bjlcy__yhqx = len(rbz__tfa)
    wpux__adn = bodo.libs.bool_arr_ext.alloc_bool_array(bjlcy__yhqx)
    for i in range(bjlcy__yhqx):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(wpux__adn, i)
        else:
            wpux__adn[i] = dict_arr_out[rbz__tfa[i]]
    return wpux__adn


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    oafz__tif = arr._data
    tcnit__bnzjd = pd.Series(oafz__tif)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = pd.array(tcnit__bnzjd.array, 'string')._str_contains(pat
            , case, flags, na, regex)
    rbz__tfa = arr._indices
    bjlcy__yhqx = len(rbz__tfa)
    wpux__adn = bodo.libs.bool_arr_ext.alloc_bool_array(bjlcy__yhqx)
    for i in range(bjlcy__yhqx):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(wpux__adn, i)
        else:
            wpux__adn[i] = dict_arr_out[rbz__tfa[i]]
    return wpux__adn


@register_jitable
def str_contains_non_regex(arr, pat, case):
    oafz__tif = arr._data
    wig__kfvhh = len(oafz__tif)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(wig__kfvhh)
    if not case:
        wkp__ceo = pat.upper()
    for i in range(wig__kfvhh):
        if case:
            dict_arr_out[i] = pat in oafz__tif[i]
        else:
            dict_arr_out[i] = wkp__ceo in oafz__tif[i].upper()
    rbz__tfa = arr._indices
    bjlcy__yhqx = len(rbz__tfa)
    wpux__adn = bodo.libs.bool_arr_ext.alloc_bool_array(bjlcy__yhqx)
    for i in range(bjlcy__yhqx):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(wpux__adn, i)
        else:
            wpux__adn[i] = dict_arr_out[rbz__tfa[i]]
    return wpux__adn


@numba.njit
def str_match(arr, pat, case, flags, na):
    oafz__tif = arr._data
    rbz__tfa = arr._indices
    bjlcy__yhqx = len(rbz__tfa)
    wpux__adn = bodo.libs.bool_arr_ext.alloc_bool_array(bjlcy__yhqx)
    tcnit__bnzjd = pd.Series(oafz__tif)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = tcnit__bnzjd.array._str_match(pat, case, flags, na)
    for i in range(bjlcy__yhqx):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(wpux__adn, i)
        else:
            wpux__adn[i] = dict_arr_out[rbz__tfa[i]]
    return wpux__adn


def create_simple_str2str_methods(func_name, func_args, can_create_non_unique):
    ycytu__rorta = f"""def str_{func_name}({', '.join(func_args)}):
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
        ycytu__rorta += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, False)
"""
    else:
        ycytu__rorta += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, arr._has_deduped_local_dictionary)
"""
    yvz__pffx = {}
    exec(ycytu__rorta, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, yvz__pffx)
    return yvz__pffx[f'str_{func_name}']


def _register_simple_str2str_methods():
    bohc__ojm = {**dict.fromkeys(['capitalize', 'lower', 'swapcase',
        'title', 'upper'], ('arr',)), **dict.fromkeys(['lstrip', 'rstrip',
        'strip'], ('arr', 'to_strip')), **dict.fromkeys(['center', 'ljust',
        'rjust'], ('arr', 'width', 'fillchar')), **dict.fromkeys(['zfill'],
        ('arr', 'width'))}
    obue__zwbm = {**dict.fromkeys(['capitalize', 'lower', 'title', 'upper',
        'lstrip', 'rstrip', 'strip', 'center', 'zfill', 'ljust', 'rjust'], 
        True), **dict.fromkeys(['swapcase'], False)}
    for func_name in bohc__ojm.keys():
        zcrg__axlub = create_simple_str2str_methods(func_name, bohc__ojm[
            func_name], obue__zwbm[func_name])
        zcrg__axlub = register_jitable(zcrg__axlub)
        globals()[f'str_{func_name}'] = zcrg__axlub


_register_simple_str2str_methods()


@register_jitable
def str_index(arr, sub, start, end):
    rjd__gyoh = arr._data
    rbz__tfa = arr._indices
    nul__babxm = len(rjd__gyoh)
    bjlcy__yhqx = len(rbz__tfa)
    ech__vhfln = bodo.libs.int_arr_ext.alloc_int_array(nul__babxm, np.int64)
    wpux__adn = bodo.libs.int_arr_ext.alloc_int_array(bjlcy__yhqx, np.int64)
    bqgzf__mrznd = False
    for i in range(nul__babxm):
        if bodo.libs.array_kernels.isna(rjd__gyoh, i):
            bodo.libs.array_kernels.setna(ech__vhfln, i)
        else:
            ech__vhfln[i] = rjd__gyoh[i].find(sub, start, end)
    for i in range(bjlcy__yhqx):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(ech__vhfln, rbz__tfa[i]):
            bodo.libs.array_kernels.setna(wpux__adn, i)
        else:
            wpux__adn[i] = ech__vhfln[rbz__tfa[i]]
            if wpux__adn[i] == -1:
                bqgzf__mrznd = True
    vvixt__crn = 'substring not found' if bqgzf__mrznd else ''
    synchronize_error_njit('ValueError', vvixt__crn)
    return wpux__adn


@register_jitable
def str_rindex(arr, sub, start, end):
    rjd__gyoh = arr._data
    rbz__tfa = arr._indices
    nul__babxm = len(rjd__gyoh)
    bjlcy__yhqx = len(rbz__tfa)
    ech__vhfln = bodo.libs.int_arr_ext.alloc_int_array(nul__babxm, np.int64)
    wpux__adn = bodo.libs.int_arr_ext.alloc_int_array(bjlcy__yhqx, np.int64)
    bqgzf__mrznd = False
    for i in range(nul__babxm):
        if bodo.libs.array_kernels.isna(rjd__gyoh, i):
            bodo.libs.array_kernels.setna(ech__vhfln, i)
        else:
            ech__vhfln[i] = rjd__gyoh[i].rindex(sub, start, end)
    for i in range(bjlcy__yhqx):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(ech__vhfln, rbz__tfa[i]):
            bodo.libs.array_kernels.setna(wpux__adn, i)
        else:
            wpux__adn[i] = ech__vhfln[rbz__tfa[i]]
            if wpux__adn[i] == -1:
                bqgzf__mrznd = True
    vvixt__crn = 'substring not found' if bqgzf__mrznd else ''
    synchronize_error_njit('ValueError', vvixt__crn)
    return wpux__adn


def create_find_methods(func_name):
    ycytu__rorta = f"""def str_{func_name}(arr, sub, start, end):
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
    yvz__pffx = {}
    exec(ycytu__rorta, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr, 'np': np}, yvz__pffx)
    return yvz__pffx[f'str_{func_name}']


def _register_find_methods():
    mnu__kiuq = ['find', 'rfind']
    for func_name in mnu__kiuq:
        zcrg__axlub = create_find_methods(func_name)
        zcrg__axlub = register_jitable(zcrg__axlub)
        globals()[f'str_{func_name}'] = zcrg__axlub


_register_find_methods()


@register_jitable
def str_count(arr, pat, flags):
    rjd__gyoh = arr._data
    rbz__tfa = arr._indices
    nul__babxm = len(rjd__gyoh)
    bjlcy__yhqx = len(rbz__tfa)
    ech__vhfln = bodo.libs.int_arr_ext.alloc_int_array(nul__babxm, np.int64)
    issd__jwec = bodo.libs.int_arr_ext.alloc_int_array(bjlcy__yhqx, np.int64)
    regex = re.compile(pat, flags)
    for i in range(nul__babxm):
        if bodo.libs.array_kernels.isna(rjd__gyoh, i):
            bodo.libs.array_kernels.setna(ech__vhfln, i)
            continue
        ech__vhfln[i] = bodo.libs.str_ext.str_findall_count(regex, rjd__gyoh[i]
            )
    for i in range(bjlcy__yhqx):
        if bodo.libs.array_kernels.isna(rbz__tfa, i
            ) or bodo.libs.array_kernels.isna(ech__vhfln, rbz__tfa[i]):
            bodo.libs.array_kernels.setna(issd__jwec, i)
        else:
            issd__jwec[i] = ech__vhfln[rbz__tfa[i]]
    return issd__jwec


@register_jitable
def str_len(arr):
    rjd__gyoh = arr._data
    rbz__tfa = arr._indices
    bjlcy__yhqx = len(rbz__tfa)
    ech__vhfln = bodo.libs.array_kernels.get_arr_lens(rjd__gyoh, False)
    issd__jwec = bodo.libs.int_arr_ext.alloc_int_array(bjlcy__yhqx, np.int64)
    for i in range(bjlcy__yhqx):
        if bodo.libs.array_kernels.isna(rbz__tfa, i
            ) or bodo.libs.array_kernels.isna(ech__vhfln, rbz__tfa[i]):
            bodo.libs.array_kernels.setna(issd__jwec, i)
        else:
            issd__jwec[i] = ech__vhfln[rbz__tfa[i]]
    return issd__jwec


@register_jitable
def str_slice(arr, start, stop, step):
    rjd__gyoh = arr._data
    nul__babxm = len(rjd__gyoh)
    keq__qfrwj = bodo.libs.str_arr_ext.pre_alloc_string_array(nul__babxm, -1)
    for i in range(nul__babxm):
        if bodo.libs.array_kernels.isna(rjd__gyoh, i):
            bodo.libs.array_kernels.setna(keq__qfrwj, i)
            continue
        keq__qfrwj[i] = rjd__gyoh[i][start:stop:step]
    return init_dict_arr(keq__qfrwj, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_get(arr, i):
    rjd__gyoh = arr._data
    rbz__tfa = arr._indices
    nul__babxm = len(rjd__gyoh)
    bjlcy__yhqx = len(rbz__tfa)
    keq__qfrwj = pre_alloc_string_array(nul__babxm, -1)
    wpux__adn = pre_alloc_string_array(bjlcy__yhqx, -1)
    for ejat__czb in range(nul__babxm):
        if bodo.libs.array_kernels.isna(rjd__gyoh, ejat__czb) or not -len(
            rjd__gyoh[ejat__czb]) <= i < len(rjd__gyoh[ejat__czb]):
            bodo.libs.array_kernels.setna(keq__qfrwj, ejat__czb)
            continue
        keq__qfrwj[ejat__czb] = rjd__gyoh[ejat__czb][i]
    for ejat__czb in range(bjlcy__yhqx):
        if bodo.libs.array_kernels.isna(rbz__tfa, ejat__czb
            ) or bodo.libs.array_kernels.isna(keq__qfrwj, rbz__tfa[ejat__czb]):
            bodo.libs.array_kernels.setna(wpux__adn, ejat__czb)
            continue
        wpux__adn[ejat__czb] = keq__qfrwj[rbz__tfa[ejat__czb]]
    return wpux__adn


@register_jitable
def str_repeat_int(arr, repeats):
    rjd__gyoh = arr._data
    nul__babxm = len(rjd__gyoh)
    keq__qfrwj = pre_alloc_string_array(nul__babxm, -1)
    for i in range(nul__babxm):
        if bodo.libs.array_kernels.isna(rjd__gyoh, i):
            bodo.libs.array_kernels.setna(keq__qfrwj, i)
            continue
        keq__qfrwj[i] = rjd__gyoh[i] * repeats
    return init_dict_arr(keq__qfrwj, arr._indices.copy(), arr.
        _has_global_dictionary, arr._has_deduped_local_dictionary and 
        repeats != 0)


def create_str2bool_methods(func_name):
    ycytu__rorta = f"""def str_{func_name}(arr):
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
    yvz__pffx = {}
    exec(ycytu__rorta, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr}, yvz__pffx)
    return yvz__pffx[f'str_{func_name}']


def _register_str2bool_methods():
    for func_name in bodo.hiframes.pd_series_ext.str2bool_methods:
        zcrg__axlub = create_str2bool_methods(func_name)
        zcrg__axlub = register_jitable(zcrg__axlub)
        globals()[f'str_{func_name}'] = zcrg__axlub


_register_str2bool_methods()


@register_jitable
def str_extract(arr, pat, flags, n_cols):
    rjd__gyoh = arr._data
    rbz__tfa = arr._indices
    nul__babxm = len(rjd__gyoh)
    bjlcy__yhqx = len(rbz__tfa)
    regex = re.compile(pat, flags=flags)
    ocyw__opyz = []
    for wpjxp__mpwsd in range(n_cols):
        ocyw__opyz.append(pre_alloc_string_array(nul__babxm, -1))
    brxkq__lmcm = bodo.libs.bool_arr_ext.alloc_bool_array(nul__babxm)
    yhyi__ovw = rbz__tfa.copy()
    for i in range(nul__babxm):
        if bodo.libs.array_kernels.isna(rjd__gyoh, i):
            brxkq__lmcm[i] = True
            for ejat__czb in range(n_cols):
                bodo.libs.array_kernels.setna(ocyw__opyz[ejat__czb], i)
            continue
        rov__gpg = regex.search(rjd__gyoh[i])
        if rov__gpg:
            brxkq__lmcm[i] = False
            mmwsc__xmzlj = rov__gpg.groups()
            for ejat__czb in range(n_cols):
                ocyw__opyz[ejat__czb][i] = mmwsc__xmzlj[ejat__czb]
        else:
            brxkq__lmcm[i] = True
            for ejat__czb in range(n_cols):
                bodo.libs.array_kernels.setna(ocyw__opyz[ejat__czb], i)
    for i in range(bjlcy__yhqx):
        if brxkq__lmcm[yhyi__ovw[i]]:
            bodo.libs.array_kernels.setna(yhyi__ovw, i)
    iljr__uyqja = [init_dict_arr(ocyw__opyz[i], yhyi__ovw.copy(), arr.
        _has_global_dictionary, False) for i in range(n_cols)]
    return iljr__uyqja


def create_extractall_methods(is_multi_group):
    ejmia__euo = '_multi' if is_multi_group else ''
    ycytu__rorta = f"""def str_extractall{ejmia__euo}(arr, regex, n_cols, index_arr):
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
    yvz__pffx = {}
    exec(ycytu__rorta, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr, 'pre_alloc_string_array':
        pre_alloc_string_array}, yvz__pffx)
    return yvz__pffx[f'str_extractall{ejmia__euo}']


def _register_extractall_methods():
    for is_multi_group in [True, False]:
        ejmia__euo = '_multi' if is_multi_group else ''
        zcrg__axlub = create_extractall_methods(is_multi_group)
        zcrg__axlub = register_jitable(zcrg__axlub)
        globals()[f'str_extractall{ejmia__euo}'] = zcrg__axlub


_register_extractall_methods()
