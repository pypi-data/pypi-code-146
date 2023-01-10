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
        xjg__laddf = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_),
            ('has_deduped_local_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, xjg__laddf)


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
        xyhhh__nfyrb, mmykj__wft, dhz__scg, ggf__ihs = args
        xkb__tkg = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        xkb__tkg.data = xyhhh__nfyrb
        xkb__tkg.indices = mmykj__wft
        xkb__tkg.has_global_dictionary = dhz__scg
        xkb__tkg.has_deduped_local_dictionary = ggf__ihs
        context.nrt.incref(builder, signature.args[0], xyhhh__nfyrb)
        context.nrt.incref(builder, signature.args[1], mmykj__wft)
        return xkb__tkg._getvalue()
    smea__cbzc = DictionaryArrayType(data_t)
    xgup__evgw = smea__cbzc(data_t, indices_t, types.bool_, types.bool_)
    return xgup__evgw, codegen


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
    ijoov__aqc = c.pyapi.unserialize(c.pyapi.serialize_object(to_pa_dict_arr))
    val = c.pyapi.call_function_objargs(ijoov__aqc, [val])
    c.pyapi.decref(ijoov__aqc)
    xkb__tkg = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    rkg__foj = c.pyapi.object_getattr_string(val, 'dictionary')
    qez__fvj = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_, 
        False))
    ohvck__plhv = c.pyapi.call_method(rkg__foj, 'to_numpy', (qez__fvj,))
    xkb__tkg.data = c.unbox(typ.data, ohvck__plhv).value
    yurfj__qheut = c.pyapi.object_getattr_string(val, 'indices')
    tqqo__ihvjp = c.context.insert_const_string(c.builder.module, 'pandas')
    qdbzo__faa = c.pyapi.import_module_noblock(tqqo__ihvjp)
    bxsk__fjx = c.pyapi.string_from_constant_string('Int32')
    nczs__gjrg = c.pyapi.call_method(qdbzo__faa, 'array', (yurfj__qheut,
        bxsk__fjx))
    xkb__tkg.indices = c.unbox(dict_indices_arr_type, nczs__gjrg).value
    xkb__tkg.has_global_dictionary = c.context.get_constant(types.bool_, False)
    xkb__tkg.has_deduped_local_dictionary = c.context.get_constant(types.
        bool_, False)
    c.pyapi.decref(rkg__foj)
    c.pyapi.decref(qez__fvj)
    c.pyapi.decref(ohvck__plhv)
    c.pyapi.decref(yurfj__qheut)
    c.pyapi.decref(qdbzo__faa)
    c.pyapi.decref(bxsk__fjx)
    c.pyapi.decref(nczs__gjrg)
    c.pyapi.decref(val)
    wnk__bnuxu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(xkb__tkg._getvalue(), is_error=wnk__bnuxu)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    xkb__tkg = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        if bodo.libs.str_arr_ext.use_pd_pyarrow_string_array:
            from bodo.libs.array import array_info_type, array_to_info_codegen
            aakzg__tliz = array_to_info_codegen(c.context, c.builder,
                array_info_type(typ), (val,), incref=False)
            gkd__jbkdd = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
                as_pointer()])
            kwxbm__dsoc = 'pd_pyarrow_array_from_string_array'
            dzw__qxz = cgutils.get_or_insert_function(c.builder.module,
                gkd__jbkdd, name=kwxbm__dsoc)
            arr = c.builder.call(dzw__qxz, [aakzg__tliz])
            c.context.nrt.decref(c.builder, typ, val)
            return arr
        c.context.nrt.incref(c.builder, typ.data, xkb__tkg.data)
        tyhge__cik = c.box(typ.data, xkb__tkg.data)
        xrnai__rrbwq = cgutils.create_struct_proxy(dict_indices_arr_type)(c
            .context, c.builder, xkb__tkg.indices)
        gkd__jbkdd = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        dzw__qxz = cgutils.get_or_insert_function(c.builder.module,
            gkd__jbkdd, name='box_dict_str_array')
        nkf__uqh = cgutils.create_struct_proxy(types.Array(types.int32, 1, 'C')
            )(c.context, c.builder, xrnai__rrbwq.data)
        dkuu__jwrg = c.builder.extract_value(nkf__uqh.shape, 0)
        icolv__nnw = nkf__uqh.data
        ehpa__hpfts = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, xrnai__rrbwq.null_bitmap).data
        ohvck__plhv = c.builder.call(dzw__qxz, [dkuu__jwrg, tyhge__cik,
            icolv__nnw, ehpa__hpfts])
        c.pyapi.decref(tyhge__cik)
    else:
        tqqo__ihvjp = c.context.insert_const_string(c.builder.module, 'pyarrow'
            )
        vsoc__qlxt = c.pyapi.import_module_noblock(tqqo__ihvjp)
        fvqg__oow = c.pyapi.object_getattr_string(vsoc__qlxt, 'DictionaryArray'
            )
        c.context.nrt.incref(c.builder, typ.data, xkb__tkg.data)
        tyhge__cik = c.box(typ.data, xkb__tkg.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, xkb__tkg.indices
            )
        yurfj__qheut = c.box(dict_indices_arr_type, xkb__tkg.indices)
        thjjt__mxgjl = c.pyapi.call_method(fvqg__oow, 'from_arrays', (
            yurfj__qheut, tyhge__cik))
        qez__fvj = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        ohvck__plhv = c.pyapi.call_method(thjjt__mxgjl, 'to_numpy', (qez__fvj,)
            )
        c.pyapi.decref(vsoc__qlxt)
        c.pyapi.decref(tyhge__cik)
        c.pyapi.decref(yurfj__qheut)
        c.pyapi.decref(fvqg__oow)
        c.pyapi.decref(thjjt__mxgjl)
        c.pyapi.decref(qez__fvj)
    c.context.nrt.decref(c.builder, typ, val)
    return ohvck__plhv


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
    bbaa__kwf = pyval.dictionary.to_numpy(False)
    ytntb__uyv = pd.array(pyval.indices, 'Int32')
    bbaa__kwf = context.get_constant_generic(builder, typ.data, bbaa__kwf)
    ytntb__uyv = context.get_constant_generic(builder,
        dict_indices_arr_type, ytntb__uyv)
    uqam__jof = context.get_constant(types.bool_, False)
    whbsv__chjrl = context.get_constant(types.bool_, False)
    rknj__yno = lir.Constant.literal_struct([bbaa__kwf, ytntb__uyv,
        uqam__jof, whbsv__chjrl])
    return rknj__yno


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            gpwhd__qbeb = A._indices[ind]
            return A._data[gpwhd__qbeb]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary, A._has_deduped_local_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        xyhhh__nfyrb = A._data
        mmykj__wft = A._indices
        dkuu__jwrg = len(mmykj__wft)
        cgvj__iyy = [get_str_arr_item_length(xyhhh__nfyrb, i) for i in
            range(len(xyhhh__nfyrb))]
        ogzgg__nygh = 0
        for i in range(dkuu__jwrg):
            if not bodo.libs.array_kernels.isna(mmykj__wft, i):
                ogzgg__nygh += cgvj__iyy[mmykj__wft[i]]
        foel__zmoy = pre_alloc_string_array(dkuu__jwrg, ogzgg__nygh)
        for i in range(dkuu__jwrg):
            if bodo.libs.array_kernels.isna(mmykj__wft, i):
                bodo.libs.array_kernels.setna(foel__zmoy, i)
                continue
            ind = mmykj__wft[i]
            if bodo.libs.array_kernels.isna(xyhhh__nfyrb, ind):
                bodo.libs.array_kernels.setna(foel__zmoy, i)
                continue
            foel__zmoy[i] = xyhhh__nfyrb[ind]
        return foel__zmoy
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_unique(arr, val):
    gpwhd__qbeb = -1
    xyhhh__nfyrb = arr._data
    for i in range(len(xyhhh__nfyrb)):
        if bodo.libs.array_kernels.isna(xyhhh__nfyrb, i):
            continue
        if xyhhh__nfyrb[i] == val:
            gpwhd__qbeb = i
            break
    return gpwhd__qbeb


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_non_unique(arr, val):
    abpf__uaoqj = set()
    xyhhh__nfyrb = arr._data
    for i in range(len(xyhhh__nfyrb)):
        if bodo.libs.array_kernels.isna(xyhhh__nfyrb, i):
            continue
        if xyhhh__nfyrb[i] == val:
            abpf__uaoqj.add(i)
    return abpf__uaoqj


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    dkuu__jwrg = len(arr)
    if arr._has_deduped_local_dictionary:
        gpwhd__qbeb = find_dict_ind_unique(arr, val)
        if gpwhd__qbeb == -1:
            return init_bool_array(np.full(dkuu__jwrg, False, np.bool_),
                arr._indices._null_bitmap.copy())
        return arr._indices == gpwhd__qbeb
    else:
        eai__pzpxm = find_dict_ind_non_unique(arr, val)
        if len(eai__pzpxm) == 0:
            return init_bool_array(np.full(dkuu__jwrg, False, np.bool_),
                arr._indices._null_bitmap.copy())
        neng__huh = np.empty(dkuu__jwrg, dtype=np.bool_)
        for i in range(len(arr._indices)):
            neng__huh[i] = arr._indices[i] in eai__pzpxm
        return init_bool_array(neng__huh, arr._indices._null_bitmap.copy())


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    dkuu__jwrg = len(arr)
    if arr._has_deduped_local_dictionary:
        gpwhd__qbeb = find_dict_ind_unique(arr, val)
        if gpwhd__qbeb == -1:
            return init_bool_array(np.full(dkuu__jwrg, True, np.bool_), arr
                ._indices._null_bitmap.copy())
        return arr._indices != gpwhd__qbeb
    else:
        eai__pzpxm = find_dict_ind_non_unique(arr, val)
        if len(eai__pzpxm) == 0:
            return init_bool_array(np.full(dkuu__jwrg, True, np.bool_), arr
                ._indices._null_bitmap.copy())
        neng__huh = np.empty(dkuu__jwrg, dtype=np.bool_)
        for i in range(len(arr._indices)):
            neng__huh[i] = arr._indices[i] not in eai__pzpxm
        return init_bool_array(neng__huh, arr._indices._null_bitmap.copy())


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
        zcbna__llgmx = arr._data
        cqd__yqrpb = bodo.libs.int_arr_ext.alloc_int_array(len(zcbna__llgmx
            ), dtype)
        for ksw__bjp in range(len(zcbna__llgmx)):
            if bodo.libs.array_kernels.isna(zcbna__llgmx, ksw__bjp):
                bodo.libs.array_kernels.setna(cqd__yqrpb, ksw__bjp)
                continue
            cqd__yqrpb[ksw__bjp] = np.int64(zcbna__llgmx[ksw__bjp])
        dkuu__jwrg = len(arr)
        mmykj__wft = arr._indices
        foel__zmoy = bodo.libs.int_arr_ext.alloc_int_array(dkuu__jwrg, dtype)
        for i in range(dkuu__jwrg):
            if bodo.libs.array_kernels.isna(mmykj__wft, i):
                bodo.libs.array_kernels.setna(foel__zmoy, i)
                continue
            foel__zmoy[i] = cqd__yqrpb[mmykj__wft[i]]
        return foel__zmoy
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    tsh__ymo = len(arrs)
    tpsy__kaxc = 'def impl(arrs, sep):\n'
    tpsy__kaxc += '  ind_map = {}\n'
    tpsy__kaxc += '  out_strs = []\n'
    tpsy__kaxc += '  n = len(arrs[0])\n'
    for i in range(tsh__ymo):
        tpsy__kaxc += f'  indices{i} = arrs[{i}]._indices\n'
    for i in range(tsh__ymo):
        tpsy__kaxc += f'  data{i} = arrs[{i}]._data\n'
    tpsy__kaxc += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    tpsy__kaxc += '  for i in range(n):\n'
    xootd__xieg = ' or '.join([
        f'bodo.libs.array_kernels.isna(arrs[{i}], i)' for i in range(tsh__ymo)]
        )
    tpsy__kaxc += f'    if {xootd__xieg}:\n'
    tpsy__kaxc += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    tpsy__kaxc += '      continue\n'
    for i in range(tsh__ymo):
        tpsy__kaxc += f'    ind{i} = indices{i}[i]\n'
    neq__avqs = '(' + ', '.join(f'ind{i}' for i in range(tsh__ymo)) + ')'
    tpsy__kaxc += f'    if {neq__avqs} not in ind_map:\n'
    tpsy__kaxc += '      out_ind = len(out_strs)\n'
    tpsy__kaxc += f'      ind_map[{neq__avqs}] = out_ind\n'
    ssjc__qfhvo = "''" if is_overload_none(sep) else 'sep'
    xtzbe__cgeiz = ', '.join([f'data{i}[ind{i}]' for i in range(tsh__ymo)])
    tpsy__kaxc += f'      v = {ssjc__qfhvo}.join([{xtzbe__cgeiz}])\n'
    tpsy__kaxc += '      out_strs.append(v)\n'
    tpsy__kaxc += '    else:\n'
    tpsy__kaxc += f'      out_ind = ind_map[{neq__avqs}]\n'
    tpsy__kaxc += '    out_indices[i] = out_ind\n'
    tpsy__kaxc += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    tpsy__kaxc += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False, False)
"""
    dwei__fqi = {}
    exec(tpsy__kaxc, {'bodo': bodo, 'numba': numba, 'np': np}, dwei__fqi)
    impl = dwei__fqi['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    tnimp__bxfdk = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    xgup__evgw = toty(fromty)
    zcz__nsdcm = context.compile_internal(builder, tnimp__bxfdk, xgup__evgw,
        (val,))
    return impl_ret_new_ref(context, builder, toty, zcz__nsdcm)


@register_jitable
def dict_arr_to_numeric(arr, errors, downcast):
    xkb__tkg = arr._data
    dict_arr_out = pd.to_numeric(xkb__tkg, errors, downcast)
    ytntb__uyv = arr._indices
    blbew__hdwe = len(ytntb__uyv)
    foel__zmoy = bodo.utils.utils.alloc_type(blbew__hdwe, dict_arr_out, (-1,))
    for i in range(blbew__hdwe):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(foel__zmoy, i)
            continue
        gpwhd__qbeb = ytntb__uyv[i]
        if bodo.libs.array_kernels.isna(dict_arr_out, gpwhd__qbeb):
            bodo.libs.array_kernels.setna(foel__zmoy, i)
            continue
        foel__zmoy[i] = dict_arr_out[gpwhd__qbeb]
    return foel__zmoy


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    bbaa__kwf = arr._data
    nucsj__poin = len(bbaa__kwf)
    gzys__atjcc = pre_alloc_string_array(nucsj__poin, -1)
    if regex:
        faj__two = re.compile(pat, flags)
        for i in range(nucsj__poin):
            if bodo.libs.array_kernels.isna(bbaa__kwf, i):
                bodo.libs.array_kernels.setna(gzys__atjcc, i)
                continue
            gzys__atjcc[i] = faj__two.sub(repl=repl, string=bbaa__kwf[i])
    else:
        for i in range(nucsj__poin):
            if bodo.libs.array_kernels.isna(bbaa__kwf, i):
                bodo.libs.array_kernels.setna(gzys__atjcc, i)
                continue
            gzys__atjcc[i] = bbaa__kwf[i].replace(pat, repl)
    return init_dict_arr(gzys__atjcc, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_startswith(arr, pat, na):
    xkb__tkg = arr._data
    ucilz__ngr = len(xkb__tkg)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(ucilz__ngr)
    for i in range(ucilz__ngr):
        dict_arr_out[i] = xkb__tkg[i].startswith(pat)
    ytntb__uyv = arr._indices
    blbew__hdwe = len(ytntb__uyv)
    foel__zmoy = bodo.libs.bool_arr_ext.alloc_bool_array(blbew__hdwe)
    for i in range(blbew__hdwe):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(foel__zmoy, i)
        else:
            foel__zmoy[i] = dict_arr_out[ytntb__uyv[i]]
    return foel__zmoy


@register_jitable
def str_endswith(arr, pat, na):
    xkb__tkg = arr._data
    ucilz__ngr = len(xkb__tkg)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(ucilz__ngr)
    for i in range(ucilz__ngr):
        dict_arr_out[i] = xkb__tkg[i].endswith(pat)
    ytntb__uyv = arr._indices
    blbew__hdwe = len(ytntb__uyv)
    foel__zmoy = bodo.libs.bool_arr_ext.alloc_bool_array(blbew__hdwe)
    for i in range(blbew__hdwe):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(foel__zmoy, i)
        else:
            foel__zmoy[i] = dict_arr_out[ytntb__uyv[i]]
    return foel__zmoy


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    xkb__tkg = arr._data
    lybpq__mzeea = pd.Series(xkb__tkg)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = pd.array(lybpq__mzeea.array, 'string')._str_contains(pat
            , case, flags, na, regex)
    ytntb__uyv = arr._indices
    blbew__hdwe = len(ytntb__uyv)
    foel__zmoy = bodo.libs.bool_arr_ext.alloc_bool_array(blbew__hdwe)
    for i in range(blbew__hdwe):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(foel__zmoy, i)
        else:
            foel__zmoy[i] = dict_arr_out[ytntb__uyv[i]]
    return foel__zmoy


@register_jitable
def str_contains_non_regex(arr, pat, case):
    xkb__tkg = arr._data
    ucilz__ngr = len(xkb__tkg)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(ucilz__ngr)
    if not case:
        ktfb__law = pat.upper()
    for i in range(ucilz__ngr):
        if case:
            dict_arr_out[i] = pat in xkb__tkg[i]
        else:
            dict_arr_out[i] = ktfb__law in xkb__tkg[i].upper()
    ytntb__uyv = arr._indices
    blbew__hdwe = len(ytntb__uyv)
    foel__zmoy = bodo.libs.bool_arr_ext.alloc_bool_array(blbew__hdwe)
    for i in range(blbew__hdwe):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(foel__zmoy, i)
        else:
            foel__zmoy[i] = dict_arr_out[ytntb__uyv[i]]
    return foel__zmoy


@numba.njit
def str_match(arr, pat, case, flags, na):
    xkb__tkg = arr._data
    ytntb__uyv = arr._indices
    blbew__hdwe = len(ytntb__uyv)
    foel__zmoy = bodo.libs.bool_arr_ext.alloc_bool_array(blbew__hdwe)
    lybpq__mzeea = pd.Series(xkb__tkg)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = lybpq__mzeea.array._str_match(pat, case, flags, na)
    for i in range(blbew__hdwe):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(foel__zmoy, i)
        else:
            foel__zmoy[i] = dict_arr_out[ytntb__uyv[i]]
    return foel__zmoy


def create_simple_str2str_methods(func_name, func_args, can_create_non_unique):
    tpsy__kaxc = f"""def str_{func_name}({', '.join(func_args)}):
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
        tpsy__kaxc += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, False)
"""
    else:
        tpsy__kaxc += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, arr._has_deduped_local_dictionary)
"""
    dwei__fqi = {}
    exec(tpsy__kaxc, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, dwei__fqi)
    return dwei__fqi[f'str_{func_name}']


def _register_simple_str2str_methods():
    aoupm__zco = {**dict.fromkeys(['capitalize', 'lower', 'swapcase',
        'title', 'upper'], ('arr',)), **dict.fromkeys(['lstrip', 'rstrip',
        'strip'], ('arr', 'to_strip')), **dict.fromkeys(['center', 'ljust',
        'rjust'], ('arr', 'width', 'fillchar')), **dict.fromkeys(['zfill'],
        ('arr', 'width'))}
    jlso__atps = {**dict.fromkeys(['capitalize', 'lower', 'title', 'upper',
        'lstrip', 'rstrip', 'strip', 'center', 'zfill', 'ljust', 'rjust'], 
        True), **dict.fromkeys(['swapcase'], False)}
    for func_name in aoupm__zco.keys():
        nple__teid = create_simple_str2str_methods(func_name, aoupm__zco[
            func_name], jlso__atps[func_name])
        nple__teid = register_jitable(nple__teid)
        globals()[f'str_{func_name}'] = nple__teid


_register_simple_str2str_methods()


@register_jitable
def str_index(arr, sub, start, end):
    bbaa__kwf = arr._data
    ytntb__uyv = arr._indices
    nucsj__poin = len(bbaa__kwf)
    blbew__hdwe = len(ytntb__uyv)
    zob__phglm = bodo.libs.int_arr_ext.alloc_int_array(nucsj__poin, np.int64)
    foel__zmoy = bodo.libs.int_arr_ext.alloc_int_array(blbew__hdwe, np.int64)
    ejft__bby = False
    for i in range(nucsj__poin):
        if bodo.libs.array_kernels.isna(bbaa__kwf, i):
            bodo.libs.array_kernels.setna(zob__phglm, i)
        else:
            zob__phglm[i] = bbaa__kwf[i].find(sub, start, end)
    for i in range(blbew__hdwe):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(zob__phglm, ytntb__uyv[i]):
            bodo.libs.array_kernels.setna(foel__zmoy, i)
        else:
            foel__zmoy[i] = zob__phglm[ytntb__uyv[i]]
            if foel__zmoy[i] == -1:
                ejft__bby = True
    qjd__zxe = 'substring not found' if ejft__bby else ''
    synchronize_error_njit('ValueError', qjd__zxe)
    return foel__zmoy


@register_jitable
def str_rindex(arr, sub, start, end):
    bbaa__kwf = arr._data
    ytntb__uyv = arr._indices
    nucsj__poin = len(bbaa__kwf)
    blbew__hdwe = len(ytntb__uyv)
    zob__phglm = bodo.libs.int_arr_ext.alloc_int_array(nucsj__poin, np.int64)
    foel__zmoy = bodo.libs.int_arr_ext.alloc_int_array(blbew__hdwe, np.int64)
    ejft__bby = False
    for i in range(nucsj__poin):
        if bodo.libs.array_kernels.isna(bbaa__kwf, i):
            bodo.libs.array_kernels.setna(zob__phglm, i)
        else:
            zob__phglm[i] = bbaa__kwf[i].rindex(sub, start, end)
    for i in range(blbew__hdwe):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(zob__phglm, ytntb__uyv[i]):
            bodo.libs.array_kernels.setna(foel__zmoy, i)
        else:
            foel__zmoy[i] = zob__phglm[ytntb__uyv[i]]
            if foel__zmoy[i] == -1:
                ejft__bby = True
    qjd__zxe = 'substring not found' if ejft__bby else ''
    synchronize_error_njit('ValueError', qjd__zxe)
    return foel__zmoy


def create_find_methods(func_name):
    tpsy__kaxc = f"""def str_{func_name}(arr, sub, start, end):
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
    dwei__fqi = {}
    exec(tpsy__kaxc, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr, 'np': np}, dwei__fqi)
    return dwei__fqi[f'str_{func_name}']


def _register_find_methods():
    gkuiu__ckrf = ['find', 'rfind']
    for func_name in gkuiu__ckrf:
        nple__teid = create_find_methods(func_name)
        nple__teid = register_jitable(nple__teid)
        globals()[f'str_{func_name}'] = nple__teid


_register_find_methods()


@register_jitable
def str_count(arr, pat, flags):
    bbaa__kwf = arr._data
    ytntb__uyv = arr._indices
    nucsj__poin = len(bbaa__kwf)
    blbew__hdwe = len(ytntb__uyv)
    zob__phglm = bodo.libs.int_arr_ext.alloc_int_array(nucsj__poin, np.int64)
    gpvdg__jcnf = bodo.libs.int_arr_ext.alloc_int_array(blbew__hdwe, np.int64)
    regex = re.compile(pat, flags)
    for i in range(nucsj__poin):
        if bodo.libs.array_kernels.isna(bbaa__kwf, i):
            bodo.libs.array_kernels.setna(zob__phglm, i)
            continue
        zob__phglm[i] = bodo.libs.str_ext.str_findall_count(regex, bbaa__kwf[i]
            )
    for i in range(blbew__hdwe):
        if bodo.libs.array_kernels.isna(ytntb__uyv, i
            ) or bodo.libs.array_kernels.isna(zob__phglm, ytntb__uyv[i]):
            bodo.libs.array_kernels.setna(gpvdg__jcnf, i)
        else:
            gpvdg__jcnf[i] = zob__phglm[ytntb__uyv[i]]
    return gpvdg__jcnf


@register_jitable
def str_len(arr):
    bbaa__kwf = arr._data
    ytntb__uyv = arr._indices
    blbew__hdwe = len(ytntb__uyv)
    zob__phglm = bodo.libs.array_kernels.get_arr_lens(bbaa__kwf, False)
    gpvdg__jcnf = bodo.libs.int_arr_ext.alloc_int_array(blbew__hdwe, np.int64)
    for i in range(blbew__hdwe):
        if bodo.libs.array_kernels.isna(ytntb__uyv, i
            ) or bodo.libs.array_kernels.isna(zob__phglm, ytntb__uyv[i]):
            bodo.libs.array_kernels.setna(gpvdg__jcnf, i)
        else:
            gpvdg__jcnf[i] = zob__phglm[ytntb__uyv[i]]
    return gpvdg__jcnf


@register_jitable
def str_slice(arr, start, stop, step):
    bbaa__kwf = arr._data
    nucsj__poin = len(bbaa__kwf)
    gzys__atjcc = bodo.libs.str_arr_ext.pre_alloc_string_array(nucsj__poin, -1)
    for i in range(nucsj__poin):
        if bodo.libs.array_kernels.isna(bbaa__kwf, i):
            bodo.libs.array_kernels.setna(gzys__atjcc, i)
            continue
        gzys__atjcc[i] = bbaa__kwf[i][start:stop:step]
    return init_dict_arr(gzys__atjcc, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_get(arr, i):
    bbaa__kwf = arr._data
    ytntb__uyv = arr._indices
    nucsj__poin = len(bbaa__kwf)
    blbew__hdwe = len(ytntb__uyv)
    gzys__atjcc = pre_alloc_string_array(nucsj__poin, -1)
    foel__zmoy = pre_alloc_string_array(blbew__hdwe, -1)
    for ksw__bjp in range(nucsj__poin):
        if bodo.libs.array_kernels.isna(bbaa__kwf, ksw__bjp) or not -len(
            bbaa__kwf[ksw__bjp]) <= i < len(bbaa__kwf[ksw__bjp]):
            bodo.libs.array_kernels.setna(gzys__atjcc, ksw__bjp)
            continue
        gzys__atjcc[ksw__bjp] = bbaa__kwf[ksw__bjp][i]
    for ksw__bjp in range(blbew__hdwe):
        if bodo.libs.array_kernels.isna(ytntb__uyv, ksw__bjp
            ) or bodo.libs.array_kernels.isna(gzys__atjcc, ytntb__uyv[ksw__bjp]
            ):
            bodo.libs.array_kernels.setna(foel__zmoy, ksw__bjp)
            continue
        foel__zmoy[ksw__bjp] = gzys__atjcc[ytntb__uyv[ksw__bjp]]
    return foel__zmoy


@register_jitable
def str_repeat_int(arr, repeats):
    bbaa__kwf = arr._data
    nucsj__poin = len(bbaa__kwf)
    gzys__atjcc = pre_alloc_string_array(nucsj__poin, -1)
    for i in range(nucsj__poin):
        if bodo.libs.array_kernels.isna(bbaa__kwf, i):
            bodo.libs.array_kernels.setna(gzys__atjcc, i)
            continue
        gzys__atjcc[i] = bbaa__kwf[i] * repeats
    return init_dict_arr(gzys__atjcc, arr._indices.copy(), arr.
        _has_global_dictionary, arr._has_deduped_local_dictionary and 
        repeats != 0)


def create_str2bool_methods(func_name):
    tpsy__kaxc = f"""def str_{func_name}(arr):
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
    dwei__fqi = {}
    exec(tpsy__kaxc, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr}, dwei__fqi)
    return dwei__fqi[f'str_{func_name}']


def _register_str2bool_methods():
    for func_name in bodo.hiframes.pd_series_ext.str2bool_methods:
        nple__teid = create_str2bool_methods(func_name)
        nple__teid = register_jitable(nple__teid)
        globals()[f'str_{func_name}'] = nple__teid


_register_str2bool_methods()


@register_jitable
def str_extract(arr, pat, flags, n_cols):
    bbaa__kwf = arr._data
    ytntb__uyv = arr._indices
    nucsj__poin = len(bbaa__kwf)
    blbew__hdwe = len(ytntb__uyv)
    regex = re.compile(pat, flags=flags)
    mtx__vah = []
    for jgyb__hoyby in range(n_cols):
        mtx__vah.append(pre_alloc_string_array(nucsj__poin, -1))
    hxkiq__ykm = bodo.libs.bool_arr_ext.alloc_bool_array(nucsj__poin)
    ehvij__ksl = ytntb__uyv.copy()
    for i in range(nucsj__poin):
        if bodo.libs.array_kernels.isna(bbaa__kwf, i):
            hxkiq__ykm[i] = True
            for ksw__bjp in range(n_cols):
                bodo.libs.array_kernels.setna(mtx__vah[ksw__bjp], i)
            continue
        hald__xypa = regex.search(bbaa__kwf[i])
        if hald__xypa:
            hxkiq__ykm[i] = False
            qum__quax = hald__xypa.groups()
            for ksw__bjp in range(n_cols):
                mtx__vah[ksw__bjp][i] = qum__quax[ksw__bjp]
        else:
            hxkiq__ykm[i] = True
            for ksw__bjp in range(n_cols):
                bodo.libs.array_kernels.setna(mtx__vah[ksw__bjp], i)
    for i in range(blbew__hdwe):
        if hxkiq__ykm[ehvij__ksl[i]]:
            bodo.libs.array_kernels.setna(ehvij__ksl, i)
    zpl__ahy = [init_dict_arr(mtx__vah[i], ehvij__ksl.copy(), arr.
        _has_global_dictionary, False) for i in range(n_cols)]
    return zpl__ahy


def create_extractall_methods(is_multi_group):
    pwr__tfyfk = '_multi' if is_multi_group else ''
    tpsy__kaxc = f"""def str_extractall{pwr__tfyfk}(arr, regex, n_cols, index_arr):
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
    dwei__fqi = {}
    exec(tpsy__kaxc, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr, 'pre_alloc_string_array':
        pre_alloc_string_array}, dwei__fqi)
    return dwei__fqi[f'str_extractall{pwr__tfyfk}']


def _register_extractall_methods():
    for is_multi_group in [True, False]:
        pwr__tfyfk = '_multi' if is_multi_group else ''
        nple__teid = create_extractall_methods(is_multi_group)
        nple__teid = register_jitable(nple__teid)
        globals()[f'str_extractall{pwr__tfyfk}'] = nple__teid


_register_extractall_methods()
