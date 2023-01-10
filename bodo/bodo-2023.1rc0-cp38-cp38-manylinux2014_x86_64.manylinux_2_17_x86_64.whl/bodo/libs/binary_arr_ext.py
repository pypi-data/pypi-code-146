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
            ons__edimc = bodo.utils.conversion.ensure_contig_if_np(arr[ind])
            return cast_uint8array_bytes(ons__edimc)
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
        jbry__zyezq, = args
        ydgfs__siy = context.make_helper(builder, binary_array_type)
        ydgfs__siy.data = jbry__zyezq
        context.nrt.incref(builder, data_typ, jbry__zyezq)
        return ydgfs__siy._getvalue()
    return binary_array_type(data_typ), codegen


@intrinsic
def init_bytes_type(typingctx, data_typ, length_type):
    assert data_typ == types.Array(types.uint8, 1, 'C')
    assert length_type == types.int64

    def codegen(context, builder, sig, args):
        nih__xeqk = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        btg__fikr = args[1]
        sll__ban = cgutils.create_struct_proxy(bytes_type)(context, builder)
        sll__ban.meminfo = context.nrt.meminfo_alloc(builder, btg__fikr)
        sll__ban.nitems = btg__fikr
        sll__ban.itemsize = lir.Constant(sll__ban.itemsize.type, 1)
        sll__ban.data = context.nrt.meminfo_data(builder, sll__ban.meminfo)
        sll__ban.parent = cgutils.get_null_value(sll__ban.parent.type)
        sll__ban.shape = cgutils.pack_array(builder, [btg__fikr], context.
            get_value_type(types.intp))
        sll__ban.strides = nih__xeqk.strides
        cgutils.memcpy(builder, sll__ban.data, nih__xeqk.data, btg__fikr)
        return sll__ban._getvalue()
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
    wel__unwhd = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def impl(arr):
        btg__fikr = len(arr) * 2
        output = numba.cpython.unicode._empty_string(wel__unwhd, btg__fikr, 1)
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
        spdbm__zrqj = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        vmt__rqagw = cgutils.create_struct_proxy(sig.args[1])(context,
            builder, value=args[1])
        jwxlx__eiy = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64)])
        eaady__kugy = cgutils.get_or_insert_function(builder.module,
            jwxlx__eiy, name='bytes_to_hex')
        builder.call(eaady__kugy, (spdbm__zrqj.data, vmt__rqagw.data,
            vmt__rqagw.nitems))
    return types.void(output, arr), codegen


@overload(operator.getitem, no_unliteral=True)
def binary_arr_getitem(arr, ind):
    if arr != binary_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl(arr, ind):
            nfav__dhzax = arr._data[ind]
            return init_bytes_type(nfav__dhzax, len(nfav__dhzax))
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
        wel__unwhd = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(hex_str):
            if not hex_str._is_ascii or hex_str._kind != wel__unwhd:
                raise TypeError(
                    'bytes.fromhex is only supported on ascii strings')
            jbry__zyezq = np.empty(len(hex_str) // 2, np.uint8)
            btg__fikr = _bytes_fromhex(jbry__zyezq.ctypes, hex_str._data,
                len(hex_str))
            flbxv__unmmw = init_bytes_type(jbry__zyezq, btg__fikr)
            return flbxv__unmmw
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
            qneu__rewwm = len(binary_list)
            ojlt__qwk = pre_alloc_binary_array(qneu__rewwm, -1)
            for tkgsd__dhuu in range(qneu__rewwm):
                rgu__olri = binary_list[tkgsd__dhuu]
                ojlt__qwk[tkgsd__dhuu] = rgu__olri
            return ojlt__qwk
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
    tycu__oowq = (
        f'Binary array setitem with index {ind} and value {val} not supported.'
        )
    if isinstance(ind, types.Integer):
        if val != bytes_type:
            raise BodoError(tycu__oowq)
        yvv__lbp = numba.njit(lambda a: None)

        def impl(arr, ind, val):
            jbry__zyezq = arr._data
            shrp__qvm = cast_bytes_uint8array(val)
            ttqa__cvdp = len(shrp__qvm)
            uagvx__ckjaw = np.int64(getitem_str_offset(arr, ind))
            xsef__qgk = uagvx__ckjaw + ttqa__cvdp
            bodo.libs.array_item_arr_ext.ensure_data_capacity(jbry__zyezq,
                uagvx__ckjaw, xsef__qgk)
            setitem_binary_array(get_offset_ptr(arr), get_data_ptr(arr),
                xsef__qgk, shrp__qvm.ctypes, ttqa__cvdp, ind)
            str_arr_set_not_na(arr, ind)
            yvv__lbp(arr)
            yvv__lbp(val)
        return impl
    elif isinstance(ind, types.SliceType):
        if val == binary_array_type:

            def impl_slice(arr, ind, val):
                kla__juiyo = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                ozfa__ben = kla__juiyo.start
                jbry__zyezq = arr._data
                uagvx__ckjaw = np.int64(getitem_str_offset(arr, ozfa__ben))
                xsef__qgk = uagvx__ckjaw + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(jbry__zyezq,
                    uagvx__ckjaw, xsef__qgk)
                set_string_array_range(arr, val, ozfa__ben, uagvx__ckjaw)
                dqb__awx = 0
                for tkgsd__dhuu in range(kla__juiyo.start, kla__juiyo.stop,
                    kla__juiyo.step):
                    if str_arr_is_na(val, dqb__awx):
                        str_arr_set_na(arr, tkgsd__dhuu)
                    else:
                        str_arr_set_not_na(arr, tkgsd__dhuu)
                    dqb__awx += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == bytes_type:

            def impl_slice_list(arr, ind, val):
                smabf__drt = binary_list_to_array(val)
                arr[ind] = smabf__drt
            return impl_slice_list
        elif val == bytes_type:

            def impl_slice(arr, ind, val):
                kla__juiyo = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for tkgsd__dhuu in range(kla__juiyo.start, kla__juiyo.stop,
                    kla__juiyo.step):
                    arr[tkgsd__dhuu] = val
            return impl_slice
    raise BodoError(tycu__oowq)


def create_binary_cmp_op_overload(op):

    def overload_binary_cmp(lhs, rhs):
        xpm__duc = lhs == binary_array_type
        ypg__avw = rhs == binary_array_type
        ocz__rbqdf = 'lhs' if xpm__duc else 'rhs'
        qct__mcgtr = 'def impl(lhs, rhs):\n'
        qct__mcgtr += '  numba.parfors.parfor.init_prange()\n'
        qct__mcgtr += f'  n = len({ocz__rbqdf})\n'
        qct__mcgtr += (
            '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n)\n')
        qct__mcgtr += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        pbbfc__fjb = []
        if xpm__duc:
            pbbfc__fjb.append('bodo.libs.array_kernels.isna(lhs, i)')
        if ypg__avw:
            pbbfc__fjb.append('bodo.libs.array_kernels.isna(rhs, i)')
        qct__mcgtr += f"    if {' or '.join(pbbfc__fjb)}:\n"
        qct__mcgtr += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        qct__mcgtr += '      continue\n'
        enbi__fbzyp = 'lhs[i]' if xpm__duc else 'lhs'
        yapa__pro = 'rhs[i]' if ypg__avw else 'rhs'
        qct__mcgtr += f'    out_arr[i] = op({enbi__fbzyp}, {yapa__pro})\n'
        qct__mcgtr += '  return out_arr\n'
        kgwnp__phvj = {}
        exec(qct__mcgtr, {'bodo': bodo, 'numba': numba, 'op': op}, kgwnp__phvj)
        return kgwnp__phvj['impl']
    return overload_binary_cmp


lower_builtin('getiter', binary_array_type)(numba.np.arrayobj.getiter_array)


def pre_alloc_binary_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_binary_arr_ext_pre_alloc_binary_array
    ) = pre_alloc_binary_arr_equiv
