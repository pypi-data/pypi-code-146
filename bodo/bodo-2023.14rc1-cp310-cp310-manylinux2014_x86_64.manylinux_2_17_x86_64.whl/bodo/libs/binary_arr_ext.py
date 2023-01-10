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
            xjl__pijy = bodo.utils.conversion.ensure_contig_if_np(arr[ind])
            return cast_uint8array_bytes(xjl__pijy)
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
        edeiu__brpx, = args
        dau__dyt = context.make_helper(builder, binary_array_type)
        dau__dyt.data = edeiu__brpx
        context.nrt.incref(builder, data_typ, edeiu__brpx)
        return dau__dyt._getvalue()
    return binary_array_type(data_typ), codegen


@intrinsic
def init_bytes_type(typingctx, data_typ, length_type):
    assert data_typ == types.Array(types.uint8, 1, 'C')
    assert length_type == types.int64

    def codegen(context, builder, sig, args):
        iub__pwg = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        yvtbp__aqlg = args[1]
        dyxpw__normb = cgutils.create_struct_proxy(bytes_type)(context, builder
            )
        dyxpw__normb.meminfo = context.nrt.meminfo_alloc(builder, yvtbp__aqlg)
        dyxpw__normb.nitems = yvtbp__aqlg
        dyxpw__normb.itemsize = lir.Constant(dyxpw__normb.itemsize.type, 1)
        dyxpw__normb.data = context.nrt.meminfo_data(builder, dyxpw__normb.
            meminfo)
        dyxpw__normb.parent = cgutils.get_null_value(dyxpw__normb.parent.type)
        dyxpw__normb.shape = cgutils.pack_array(builder, [yvtbp__aqlg],
            context.get_value_type(types.intp))
        dyxpw__normb.strides = iub__pwg.strides
        cgutils.memcpy(builder, dyxpw__normb.data, iub__pwg.data, yvtbp__aqlg)
        return dyxpw__normb._getvalue()
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
    xqmjt__izn = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def impl(arr):
        yvtbp__aqlg = len(arr) * 2
        output = numba.cpython.unicode._empty_string(xqmjt__izn, yvtbp__aqlg, 1
            )
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
        ohwow__wuw = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        oawn__oavr = cgutils.create_struct_proxy(sig.args[1])(context,
            builder, value=args[1])
        dnhdy__hvgul = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64)])
        hiv__qdtu = cgutils.get_or_insert_function(builder.module,
            dnhdy__hvgul, name='bytes_to_hex')
        builder.call(hiv__qdtu, (ohwow__wuw.data, oawn__oavr.data,
            oawn__oavr.nitems))
    return types.void(output, arr), codegen


@overload(operator.getitem, no_unliteral=True)
def binary_arr_getitem(arr, ind):
    if arr != binary_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl(arr, ind):
            gmusd__fkagl = arr._data[ind]
            return init_bytes_type(gmusd__fkagl, len(gmusd__fkagl))
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
        xqmjt__izn = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(hex_str):
            if not hex_str._is_ascii or hex_str._kind != xqmjt__izn:
                raise TypeError(
                    'bytes.fromhex is only supported on ascii strings')
            edeiu__brpx = np.empty(len(hex_str) // 2, np.uint8)
            yvtbp__aqlg = _bytes_fromhex(edeiu__brpx.ctypes, hex_str._data,
                len(hex_str))
            gbcl__ifjme = init_bytes_type(edeiu__brpx, yvtbp__aqlg)
            return gbcl__ifjme
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
            oky__bow = len(binary_list)
            ozogy__rnaiz = pre_alloc_binary_array(oky__bow, -1)
            for iacl__wst in range(oky__bow):
                ozzrw__ixwr = binary_list[iacl__wst]
                ozogy__rnaiz[iacl__wst] = ozzrw__ixwr
            return ozogy__rnaiz
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
    nunl__ugd = (
        f'Binary array setitem with index {ind} and value {val} not supported.'
        )
    if isinstance(ind, types.Integer):
        if val != bytes_type:
            raise BodoError(nunl__ugd)
        fbh__psmkg = numba.njit(lambda a: None)

        def impl(arr, ind, val):
            edeiu__brpx = arr._data
            fbtxr__adh = cast_bytes_uint8array(val)
            lzqxr__vjff = len(fbtxr__adh)
            bqu__uym = np.int64(getitem_str_offset(arr, ind))
            zqkig__wwp = bqu__uym + lzqxr__vjff
            bodo.libs.array_item_arr_ext.ensure_data_capacity(edeiu__brpx,
                bqu__uym, zqkig__wwp)
            setitem_binary_array(get_offset_ptr(arr), get_data_ptr(arr),
                zqkig__wwp, fbtxr__adh.ctypes, lzqxr__vjff, ind)
            str_arr_set_not_na(arr, ind)
            fbh__psmkg(arr)
            fbh__psmkg(val)
        return impl
    elif isinstance(ind, types.SliceType):
        if val == binary_array_type:

            def impl_slice(arr, ind, val):
                aidf__nir = numba.cpython.unicode._normalize_slice(ind, len
                    (arr))
                pyifr__ryvcl = aidf__nir.start
                edeiu__brpx = arr._data
                bqu__uym = np.int64(getitem_str_offset(arr, pyifr__ryvcl))
                zqkig__wwp = bqu__uym + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(edeiu__brpx,
                    bqu__uym, zqkig__wwp)
                set_string_array_range(arr, val, pyifr__ryvcl, bqu__uym)
                hwvr__kgda = 0
                for iacl__wst in range(aidf__nir.start, aidf__nir.stop,
                    aidf__nir.step):
                    if str_arr_is_na(val, hwvr__kgda):
                        str_arr_set_na(arr, iacl__wst)
                    else:
                        str_arr_set_not_na(arr, iacl__wst)
                    hwvr__kgda += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == bytes_type:

            def impl_slice_list(arr, ind, val):
                eaxuq__zgncj = binary_list_to_array(val)
                arr[ind] = eaxuq__zgncj
            return impl_slice_list
        elif val == bytes_type:

            def impl_slice(arr, ind, val):
                aidf__nir = numba.cpython.unicode._normalize_slice(ind, len
                    (arr))
                for iacl__wst in range(aidf__nir.start, aidf__nir.stop,
                    aidf__nir.step):
                    arr[iacl__wst] = val
            return impl_slice
    raise BodoError(nunl__ugd)


def create_binary_cmp_op_overload(op):

    def overload_binary_cmp(lhs, rhs):
        rpb__lsnrz = lhs == binary_array_type
        gusi__ugbsd = rhs == binary_array_type
        fsj__sorsv = 'lhs' if rpb__lsnrz else 'rhs'
        vdv__wskkb = 'def impl(lhs, rhs):\n'
        vdv__wskkb += '  numba.parfors.parfor.init_prange()\n'
        vdv__wskkb += f'  n = len({fsj__sorsv})\n'
        vdv__wskkb += (
            '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n)\n')
        vdv__wskkb += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        yvxnf__ruhf = []
        if rpb__lsnrz:
            yvxnf__ruhf.append('bodo.libs.array_kernels.isna(lhs, i)')
        if gusi__ugbsd:
            yvxnf__ruhf.append('bodo.libs.array_kernels.isna(rhs, i)')
        vdv__wskkb += f"    if {' or '.join(yvxnf__ruhf)}:\n"
        vdv__wskkb += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        vdv__wskkb += '      continue\n'
        uxxy__ocxg = 'lhs[i]' if rpb__lsnrz else 'lhs'
        hpzk__mlx = 'rhs[i]' if gusi__ugbsd else 'rhs'
        vdv__wskkb += f'    out_arr[i] = op({uxxy__ocxg}, {hpzk__mlx})\n'
        vdv__wskkb += '  return out_arr\n'
        ysii__gzioi = {}
        exec(vdv__wskkb, {'bodo': bodo, 'numba': numba, 'op': op}, ysii__gzioi)
        return ysii__gzioi['impl']
    return overload_binary_cmp


lower_builtin('getiter', binary_array_type)(numba.np.arrayobj.getiter_array)


def pre_alloc_binary_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_binary_arr_ext_pre_alloc_binary_array
    ) = pre_alloc_binary_arr_equiv
