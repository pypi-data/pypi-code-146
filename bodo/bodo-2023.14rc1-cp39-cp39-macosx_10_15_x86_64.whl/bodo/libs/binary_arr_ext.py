"""Array implementation for binary (bytes) objects, which are usually immutable.
It is equivalent to string array, except that it stores a 'bytes' object for each
element instead of 'str'.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, overload, overload_attribute, overload_method
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, offset_type
from bodo.utils.typing import BodoError, is_list_like_index_type
_bytes_fromhex = types.ExternalFunction('bytes_fromhex', types.int64(types.
    voidptr, types.voidptr, types.uint64))
ll.add_symbol('bytes_to_hex', hstr_ext.bytes_to_hex)
ll.add_symbol('bytes_fromhex', hstr_ext.bytes_fromhex)
bytes_type = types.Bytes(types.uint8, 1, 'C', readonly=True)
ll.add_symbol('setitem_binary_array', hstr_ext.setitem_binary_array)
char_type = types.uint8
setitem_binary_array = types.ExternalFunction('setitem_binary_array', types
    .void(types.CPointer(offset_type), types.CPointer(char_type), types.
    uint64, types.voidptr, types.intp, types.intp))


@overload(len)
def bytes_len_overload(bytes_obj):
    if isinstance(bytes_obj, types.Bytes):
        return lambda bytes_obj: bytes_obj._nitems


@overload(operator.getitem, no_unliteral=True)
def bytes_getitem(byte_obj, ind):
    if not isinstance(byte_obj, types.Bytes):
        return
    if isinstance(ind, types.SliceType):

        def impl(byte_obj, ind):
            arr = cast_bytes_uint8array(byte_obj)
            gtn__nhvop = bodo.utils.conversion.ensure_contig_if_np(arr[ind])
            return cast_uint8array_bytes(gtn__nhvop)
        return impl


class BinaryArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(BinaryArrayType, self).__init__(name='BinaryArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return bytes_type

    def copy(self):
        return BinaryArrayType()

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)


binary_array_type = BinaryArrayType()


@overload(len, no_unliteral=True)
def bin_arr_len_overload(bin_arr):
    if bin_arr == binary_array_type:
        return lambda bin_arr: len(bin_arr._data)


make_attribute_wrapper(types.Bytes, 'nitems', '_nitems')


@overload_attribute(BinaryArrayType, 'size')
def bin_arr_size_overload(bin_arr):
    return lambda bin_arr: len(bin_arr._data)


@overload_attribute(BinaryArrayType, 'shape')
def bin_arr_shape_overload(bin_arr):
    return lambda bin_arr: (len(bin_arr._data),)


@overload_attribute(BinaryArrayType, 'nbytes')
def bin_arr_nbytes_overload(bin_arr):
    return lambda bin_arr: bin_arr._data.nbytes


@overload_attribute(BinaryArrayType, 'ndim')
def overload_bin_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BinaryArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: np.dtype('O')


@numba.njit
def pre_alloc_binary_array(n_bytestrs, n_chars):
    if n_chars is None:
        n_chars = -1
    bin_arr = init_binary_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_bytestrs), (np.int64(n_chars)
        ,), bodo.libs.str_arr_ext.char_arr_type))
    if n_chars == 0:
        bodo.libs.str_arr_ext.set_all_offsets_to_0(bin_arr)
    return bin_arr


@intrinsic
def init_binary_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, sig, args):
        igft__bucb, = args
        bbx__pepx = context.make_helper(builder, binary_array_type)
        bbx__pepx.data = igft__bucb
        context.nrt.incref(builder, data_typ, igft__bucb)
        return bbx__pepx._getvalue()
    return binary_array_type(data_typ), codegen


@intrinsic
def init_bytes_type(typingctx, data_typ, length_type):
    assert data_typ == types.Array(types.uint8, 1, 'C')
    assert length_type == types.int64

    def codegen(context, builder, sig, args):
        mqww__hsa = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        hdgw__tqke = args[1]
        jnnu__sqa = cgutils.create_struct_proxy(bytes_type)(context, builder)
        jnnu__sqa.meminfo = context.nrt.meminfo_alloc(builder, hdgw__tqke)
        jnnu__sqa.nitems = hdgw__tqke
        jnnu__sqa.itemsize = lir.Constant(jnnu__sqa.itemsize.type, 1)
        jnnu__sqa.data = context.nrt.meminfo_data(builder, jnnu__sqa.meminfo)
        jnnu__sqa.parent = cgutils.get_null_value(jnnu__sqa.parent.type)
        jnnu__sqa.shape = cgutils.pack_array(builder, [hdgw__tqke], context
            .get_value_type(types.intp))
        jnnu__sqa.strides = mqww__hsa.strides
        cgutils.memcpy(builder, jnnu__sqa.data, mqww__hsa.data, hdgw__tqke)
        return jnnu__sqa._getvalue()
    return bytes_type(data_typ, length_type), codegen


@intrinsic
def cast_bytes_uint8array(typingctx, data_typ):
    assert data_typ == bytes_type

    def codegen(context, builder, sig, args):
        return impl_ret_borrowed(context, builder, sig.return_type, args[0])
    return types.Array(types.uint8, 1, 'C')(data_typ), codegen


@intrinsic
def cast_uint8array_bytes(typingctx, data_typ):
    assert data_typ == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, sig, args):
        return impl_ret_borrowed(context, builder, sig.return_type, args[0])
    return bytes_type(data_typ), codegen


@overload_method(BinaryArrayType, 'copy', no_unliteral=True)
def binary_arr_copy_overload(arr):

    def copy_impl(arr):
        return init_binary_arr(arr._data.copy())
    return copy_impl


@overload_method(types.Bytes, 'hex')
def binary_arr_hex(arr):
    yles__mafg = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def impl(arr):
        hdgw__tqke = len(arr) * 2
        output = numba.cpython.unicode._empty_string(yles__mafg, hdgw__tqke, 1)
        bytes_to_hex(output, arr)
        return output
    return impl


@lower_cast(types.CPointer(types.uint8), types.voidptr)
def cast_uint8_array_to_voidptr(context, builder, fromty, toty, val):
    return val


make_attribute_wrapper(types.Bytes, 'data', '_data')


@overload_method(types.Bytes, '__hash__')
def bytes_hash(arr):

    def impl(arr):
        return numba.cpython.hashing._Py_HashBytes(arr._data, len(arr))
    return impl


@intrinsic
def bytes_to_hex(typingctx, output, arr):

    def codegen(context, builder, sig, args):
        jfv__udsi = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        howx__jfzo = cgutils.create_struct_proxy(sig.args[1])(context,
            builder, value=args[1])
        irwzg__rawhs = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64)])
        lqjch__fhs = cgutils.get_or_insert_function(builder.module,
            irwzg__rawhs, name='bytes_to_hex')
        builder.call(lqjch__fhs, (jfv__udsi.data, howx__jfzo.data,
            howx__jfzo.nitems))
    return types.void(output, arr), codegen


@overload(operator.getitem, no_unliteral=True)
def binary_arr_getitem(arr, ind):
    if arr != binary_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl(arr, ind):
            nlyp__snf = arr._data[ind]
            return init_bytes_type(nlyp__snf, len(nlyp__snf))
        return impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind) and (ind.
        dtype == types.bool_ or isinstance(ind.dtype, types.Integer)
        ) or isinstance(ind, types.SliceType):
        return lambda arr, ind: init_binary_arr(arr._data[ind])
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for Binary Array with indexing type {ind} not supported.'
            )


def bytes_fromhex(hex_str):
    pass


@overload(bytes_fromhex)
def overload_bytes_fromhex(hex_str):
    hex_str = types.unliteral(hex_str)
    if hex_str == bodo.string_type:
        yles__mafg = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(hex_str):
            if not hex_str._is_ascii or hex_str._kind != yles__mafg:
                raise TypeError(
                    'bytes.fromhex is only supported on ascii strings')
            igft__bucb = np.empty(len(hex_str) // 2, np.uint8)
            hdgw__tqke = _bytes_fromhex(igft__bucb.ctypes, hex_str._data,
                len(hex_str))
            mvb__sxkgd = init_bytes_type(igft__bucb, hdgw__tqke)
            return mvb__sxkgd
        return impl
    raise BodoError(f'bytes.fromhex not supported with argument type {hex_str}'
        )


def binary_list_to_array(binary_list):
    return binary_list


@overload(binary_list_to_array, no_unliteral=True)
def binary_list_to_array_overload(binary_list):
    if isinstance(binary_list, types.List
        ) and binary_list.dtype == bodo.bytes_type:

        def binary_list_impl(binary_list):
            gjxse__lcba = len(binary_list)
            zqxy__kcfc = pre_alloc_binary_array(gjxse__lcba, -1)
            for wsmlc__giop in range(gjxse__lcba):
                zzm__wfvvk = binary_list[wsmlc__giop]
                zqxy__kcfc[wsmlc__giop] = zzm__wfvvk
            return zqxy__kcfc
        return binary_list_impl
    raise BodoError(
        f'Error, binary_list_to_array not supported for type {binary_list}')


@overload(operator.setitem)
def binary_arr_setitem(arr, ind, val):
    from bodo.libs.str_arr_ext import get_data_ptr, get_offset_ptr, getitem_str_offset, num_total_chars, set_string_array_range, str_arr_is_na, str_arr_set_na, str_arr_set_not_na
    if arr != binary_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    gguqo__txsi = (
        f'Binary array setitem with index {ind} and value {val} not supported.'
        )
    if isinstance(ind, types.Integer):
        if val != bytes_type:
            raise BodoError(gguqo__txsi)
        gzgqv__jpl = numba.njit(lambda a: None)

        def impl(arr, ind, val):
            igft__bucb = arr._data
            wpriy__jkewb = cast_bytes_uint8array(val)
            fhf__bzzm = len(wpriy__jkewb)
            bak__ifgjb = np.int64(getitem_str_offset(arr, ind))
            neey__byqhf = bak__ifgjb + fhf__bzzm
            bodo.libs.array_item_arr_ext.ensure_data_capacity(igft__bucb,
                bak__ifgjb, neey__byqhf)
            setitem_binary_array(get_offset_ptr(arr), get_data_ptr(arr),
                neey__byqhf, wpriy__jkewb.ctypes, fhf__bzzm, ind)
            str_arr_set_not_na(arr, ind)
            gzgqv__jpl(arr)
            gzgqv__jpl(val)
        return impl
    elif isinstance(ind, types.SliceType):
        if val == binary_array_type:

            def impl_slice(arr, ind, val):
                wanew__xjiz = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                nls__ansot = wanew__xjiz.start
                igft__bucb = arr._data
                bak__ifgjb = np.int64(getitem_str_offset(arr, nls__ansot))
                neey__byqhf = bak__ifgjb + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(igft__bucb,
                    bak__ifgjb, neey__byqhf)
                set_string_array_range(arr, val, nls__ansot, bak__ifgjb)
                pxfk__apg = 0
                for wsmlc__giop in range(wanew__xjiz.start, wanew__xjiz.
                    stop, wanew__xjiz.step):
                    if str_arr_is_na(val, pxfk__apg):
                        str_arr_set_na(arr, wsmlc__giop)
                    else:
                        str_arr_set_not_na(arr, wsmlc__giop)
                    pxfk__apg += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == bytes_type:

            def impl_slice_list(arr, ind, val):
                scsc__dilo = binary_list_to_array(val)
                arr[ind] = scsc__dilo
            return impl_slice_list
        elif val == bytes_type:

            def impl_slice(arr, ind, val):
                wanew__xjiz = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for wsmlc__giop in range(wanew__xjiz.start, wanew__xjiz.
                    stop, wanew__xjiz.step):
                    arr[wsmlc__giop] = val
            return impl_slice
    raise BodoError(gguqo__txsi)


def create_binary_cmp_op_overload(op):

    def overload_binary_cmp(lhs, rhs):
        viy__xtbo = lhs == binary_array_type
        gbo__jkz = rhs == binary_array_type
        xsv__miei = 'lhs' if viy__xtbo else 'rhs'
        rqm__rrusv = 'def impl(lhs, rhs):\n'
        rqm__rrusv += '  numba.parfors.parfor.init_prange()\n'
        rqm__rrusv += f'  n = len({xsv__miei})\n'
        rqm__rrusv += (
            '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n)\n')
        rqm__rrusv += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        vyz__cmgue = []
        if viy__xtbo:
            vyz__cmgue.append('bodo.libs.array_kernels.isna(lhs, i)')
        if gbo__jkz:
            vyz__cmgue.append('bodo.libs.array_kernels.isna(rhs, i)')
        rqm__rrusv += f"    if {' or '.join(vyz__cmgue)}:\n"
        rqm__rrusv += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        rqm__rrusv += '      continue\n'
        ytbq__sryic = 'lhs[i]' if viy__xtbo else 'lhs'
        wdae__ljrp = 'rhs[i]' if gbo__jkz else 'rhs'
        rqm__rrusv += f'    out_arr[i] = op({ytbq__sryic}, {wdae__ljrp})\n'
        rqm__rrusv += '  return out_arr\n'
        aweu__wqka = {}
        exec(rqm__rrusv, {'bodo': bodo, 'numba': numba, 'op': op}, aweu__wqka)
        return aweu__wqka['impl']
    return overload_binary_cmp


lower_builtin('getiter', binary_array_type)(numba.np.arrayobj.getiter_array)


def pre_alloc_binary_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_binary_arr_ext_pre_alloc_binary_array
    ) = pre_alloc_binary_arr_equiv
