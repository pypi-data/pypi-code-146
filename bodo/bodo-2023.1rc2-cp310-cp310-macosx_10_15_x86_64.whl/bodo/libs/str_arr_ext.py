"""Array implementation for string objects, which are usually immutable.
The characters are stored in a contiguous data array, and an offsets array marks the
the individual strings. For example:
value:             ['a', 'bc', '', 'abc', None, 'bb']
data:              [a, b, c, a, b, c, b, b]
offsets:           [0, 1, 3, 3, 6, 6, 8]
"""
import glob
import operator
import numba
import numba.core.typing.typeof
import numpy as np
import pandas as pd
import pyarrow as pa
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.unsafe.bytes import memcpy_region
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, type_callable, typeof_impl, unbox
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, pre_alloc_binary_array
from bodo.libs.str_ext import memcmp, string_type, unicode_to_utf8_and_len
from bodo.utils.typing import BodoArrayIterator, BodoError, is_list_like_index_type, is_overload_constant_int, is_overload_none, is_overload_true, is_str_arr_type, parse_dtype, raise_bodo_error
use_pd_string_array = False
use_pd_pyarrow_string_array = True
char_type = types.uint8
char_arr_type = types.Array(char_type, 1, 'C')
offset_arr_type = types.Array(offset_type, 1, 'C')
null_bitmap_arr_type = types.Array(types.uint8, 1, 'C')
data_ctypes_type = types.ArrayCTypes(char_arr_type)
offset_ctypes_type = types.ArrayCTypes(offset_arr_type)


class StringArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(StringArrayType, self).__init__(name='StringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    def copy(self):
        return StringArrayType()


string_array_type = StringArrayType()


@typeof_impl.register(pd.arrays.StringArray)
def typeof_string_array(val, c):
    return string_array_type


@typeof_impl.register(pd.arrays.ArrowStringArray)
def typeof_pyarrow_string_array(val, c):
    if pa.types.is_dictionary(val._data.combine_chunks().type):
        return bodo.dict_str_arr_type
    return string_array_type


@register_model(BinaryArrayType)
@register_model(StringArrayType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kjke__yqp = ArrayItemArrayType(char_arr_type)
        bjs__epl = [('data', kjke__yqp)]
        models.StructModel.__init__(self, dmm, fe_type, bjs__epl)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        fcd__zistm, = args
        meg__eshwn = context.make_helper(builder, string_array_type)
        meg__eshwn.data = fcd__zistm
        context.nrt.incref(builder, data_typ, fcd__zistm)
        return meg__eshwn._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    wxpxe__zwsn = c.context.insert_const_string(c.builder.module, 'pandas')
    aefql__idiv = c.pyapi.import_module_noblock(wxpxe__zwsn)
    deeft__put = c.pyapi.call_method(aefql__idiv, 'StringDtype', ())
    c.pyapi.decref(aefql__idiv)
    return deeft__put


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        bbenu__ysjqy = bodo.libs.dict_arr_ext.get_binary_op_overload(op,
            lhs, rhs)
        if bbenu__ysjqy is not None:
            return bbenu__ysjqy
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pqzrf__eht = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(pqzrf__eht)
                for i in numba.parfors.parfor.internal_prange(pqzrf__eht):
                    if bodo.libs.array_kernels.isna(lhs, i
                        ) or bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_both
        if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

            def impl_left(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pqzrf__eht = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(pqzrf__eht)
                for i in numba.parfors.parfor.internal_prange(pqzrf__eht):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs)
                    out_arr[i] = val
                return out_arr
            return impl_left
        if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

            def impl_right(lhs, rhs):
                numba.parfors.parfor.init_prange()
                pqzrf__eht = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(pqzrf__eht)
                for i in numba.parfors.parfor.internal_prange(pqzrf__eht):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs, rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_right
        raise_bodo_error(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_string_array_binary_op


def overload_add_operator_string_array(lhs, rhs):
    xftd__ploa = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    dmubk__mhrcw = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and dmubk__mhrcw or xftd__ploa and is_str_arr_type(
        rhs):

        def impl_both(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j
                    ) or bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs[j]
            return out_arr
        return impl_both
    if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

        def impl_left(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs
            return out_arr
        return impl_left
    if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

        def impl_right(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(rhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs + rhs[j]
            return out_arr
        return impl_right


def overload_mul_operator_str_arr(lhs, rhs):
    if is_str_arr_type(lhs) and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] * rhs
            return out_arr
        return impl
    if isinstance(lhs, types.Integer) and is_str_arr_type(rhs):

        def impl(lhs, rhs):
            return rhs * lhs
        return impl


def _get_str_binary_arr_payload(context, builder, arr_value, arr_typ):
    assert arr_typ == string_array_type or arr_typ == binary_array_type
    vzgzv__jpy = context.make_helper(builder, arr_typ, arr_value)
    kjke__yqp = ArrayItemArrayType(char_arr_type)
    mrel__vyznx = _get_array_item_arr_payload(context, builder, kjke__yqp,
        vzgzv__jpy.data)
    return mrel__vyznx


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        return mrel__vyznx.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@numba.njit
def check_offsets(str_arr):
    offsets = bodo.libs.array_item_arr_ext.get_offsets(str_arr._data)
    n_chars = bodo.libs.str_arr_ext.num_total_chars(str_arr)
    for i in range(bodo.libs.array_item_arr_ext.get_n_arrays(str_arr._data)):
        if offsets[i] > n_chars or offsets[i + 1] - offsets[i] < 0:
            print('wrong offset found', i, offsets[i])
            break


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        hfn__ilmm = context.make_helper(builder, offset_arr_type,
            mrel__vyznx.offsets).data
        return _get_num_total_chars(builder, hfn__ilmm, mrel__vyznx.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        yernh__brjp = context.make_helper(builder, offset_arr_type,
            mrel__vyznx.offsets)
        iyz__zxd = context.make_helper(builder, offset_ctypes_type)
        iyz__zxd.data = builder.bitcast(yernh__brjp.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        iyz__zxd.meminfo = yernh__brjp.meminfo
        deeft__put = iyz__zxd._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            deeft__put)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        fcd__zistm = context.make_helper(builder, char_arr_type,
            mrel__vyznx.data)
        iyz__zxd = context.make_helper(builder, data_ctypes_type)
        iyz__zxd.data = fcd__zistm.data
        iyz__zxd.meminfo = fcd__zistm.meminfo
        deeft__put = iyz__zxd._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, deeft__put
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        iabj__elpi, ind = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            iabj__elpi, sig.args[0])
        fcd__zistm = context.make_helper(builder, char_arr_type,
            mrel__vyznx.data)
        iyz__zxd = context.make_helper(builder, data_ctypes_type)
        iyz__zxd.data = builder.gep(fcd__zistm.data, [ind])
        iyz__zxd.meminfo = fcd__zistm.meminfo
        deeft__put = iyz__zxd._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, deeft__put
            )
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        lwqj__xnahp, tde__rvc, wsaf__ayxb, nfwml__rhy = args
        puwmh__bbskf = builder.bitcast(builder.gep(lwqj__xnahp, [tde__rvc]),
            lir.IntType(8).as_pointer())
        dxy__qmmn = builder.bitcast(builder.gep(wsaf__ayxb, [nfwml__rhy]),
            lir.IntType(8).as_pointer())
        bazgy__tqd = builder.load(dxy__qmmn)
        builder.store(bazgy__tqd, puwmh__bbskf)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        vmvd__vvkze = context.make_helper(builder, null_bitmap_arr_type,
            mrel__vyznx.null_bitmap)
        iyz__zxd = context.make_helper(builder, data_ctypes_type)
        iyz__zxd.data = vmvd__vvkze.data
        iyz__zxd.meminfo = vmvd__vvkze.meminfo
        deeft__put = iyz__zxd._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, deeft__put
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        hfn__ilmm = context.make_helper(builder, offset_arr_type,
            mrel__vyznx.offsets).data
        return builder.load(builder.gep(hfn__ilmm, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, mrel__vyznx
            .offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        vcz__rrnc, ind = args
        if in_bitmap_typ == data_ctypes_type:
            iyz__zxd = context.make_helper(builder, data_ctypes_type, vcz__rrnc
                )
            vcz__rrnc = iyz__zxd.data
        return builder.load(builder.gep(vcz__rrnc, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        vcz__rrnc, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            iyz__zxd = context.make_helper(builder, data_ctypes_type, vcz__rrnc
                )
            vcz__rrnc = iyz__zxd.data
        builder.store(val, builder.gep(vcz__rrnc, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        xfgxg__moo = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        vwvqs__mazul = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        egqv__ocr = context.make_helper(builder, offset_arr_type,
            xfgxg__moo.offsets).data
        arua__alaq = context.make_helper(builder, offset_arr_type,
            vwvqs__mazul.offsets).data
        amwu__btuc = context.make_helper(builder, char_arr_type, xfgxg__moo
            .data).data
        lhrbz__jkw = context.make_helper(builder, char_arr_type,
            vwvqs__mazul.data).data
        hejxw__dycxj = context.make_helper(builder, null_bitmap_arr_type,
            xfgxg__moo.null_bitmap).data
        whqks__wldqp = context.make_helper(builder, null_bitmap_arr_type,
            vwvqs__mazul.null_bitmap).data
        rglb__pqz = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, arua__alaq, egqv__ocr, rglb__pqz)
        cgutils.memcpy(builder, lhrbz__jkw, amwu__btuc, builder.load(
            builder.gep(egqv__ocr, [ind])))
        apdq__ogwu = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        yhfun__zqfo = builder.lshr(apdq__ogwu, lir.Constant(lir.IntType(64), 3)
            )
        cgutils.memcpy(builder, whqks__wldqp, hejxw__dycxj, yhfun__zqfo)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        xfgxg__moo = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        vwvqs__mazul = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        egqv__ocr = context.make_helper(builder, offset_arr_type,
            xfgxg__moo.offsets).data
        amwu__btuc = context.make_helper(builder, char_arr_type, xfgxg__moo
            .data).data
        lhrbz__jkw = context.make_helper(builder, char_arr_type,
            vwvqs__mazul.data).data
        num_total_chars = _get_num_total_chars(builder, egqv__ocr,
            xfgxg__moo.n_arrays)
        cgutils.memcpy(builder, lhrbz__jkw, amwu__btuc, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        xfgxg__moo = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        vwvqs__mazul = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        egqv__ocr = context.make_helper(builder, offset_arr_type,
            xfgxg__moo.offsets).data
        arua__alaq = context.make_helper(builder, offset_arr_type,
            vwvqs__mazul.offsets).data
        hejxw__dycxj = context.make_helper(builder, null_bitmap_arr_type,
            xfgxg__moo.null_bitmap).data
        pqzrf__eht = xfgxg__moo.n_arrays
        mjf__kdbau = context.get_constant(offset_type, 0)
        jtxs__pdy = cgutils.alloca_once_value(builder, mjf__kdbau)
        with cgutils.for_range(builder, pqzrf__eht) as kyk__are:
            puumb__iebz = lower_is_na(context, builder, hejxw__dycxj,
                kyk__are.index)
            with cgutils.if_likely(builder, builder.not_(puumb__iebz)):
                hah__brkkg = builder.load(builder.gep(egqv__ocr, [kyk__are.
                    index]))
                cbs__xngo = builder.load(jtxs__pdy)
                builder.store(hah__brkkg, builder.gep(arua__alaq, [cbs__xngo]))
                builder.store(builder.add(cbs__xngo, lir.Constant(context.
                    get_value_type(offset_type), 1)), jtxs__pdy)
        cbs__xngo = builder.load(jtxs__pdy)
        hah__brkkg = builder.load(builder.gep(egqv__ocr, [pqzrf__eht]))
        builder.store(hah__brkkg, builder.gep(arua__alaq, [cbs__xngo]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        eym__udasi, ind, str, tsyfl__vievo = args
        eym__udasi = context.make_array(sig.args[0])(context, builder,
            eym__udasi)
        tyq__qjqf = builder.gep(eym__udasi.data, [ind])
        cgutils.raw_memcpy(builder, tyq__qjqf, str, tsyfl__vievo, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        tyq__qjqf, ind, eoon__majd, tsyfl__vievo = args
        tyq__qjqf = builder.gep(tyq__qjqf, [ind])
        cgutils.raw_memcpy(builder, tyq__qjqf, eoon__majd, tsyfl__vievo, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.generated_jit(nopython=True)
def get_str_arr_item_length(A, i):
    if A == bodo.dict_str_arr_type:

        def impl(A, i):
            idx = A._indices[i]
            jxdni__jyt = A._data
            return np.int64(getitem_str_offset(jxdni__jyt, idx + 1) -
                getitem_str_offset(jxdni__jyt, idx))
        return impl
    else:
        return lambda A, i: np.int64(getitem_str_offset(A, i + 1) -
            getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    wvho__zprr = np.int64(getitem_str_offset(A, i))
    oxfqa__iouyu = np.int64(getitem_str_offset(A, i + 1))
    l = oxfqa__iouyu - wvho__zprr
    mbb__sqz = get_data_ptr_ind(A, wvho__zprr)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(mbb__sqz, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.generated_jit(no_cpython_wrapper=True, nopython=True)
def get_str_arr_item_copy(B, j, A, i):
    if B != string_array_type:
        raise BodoError(
            'get_str_arr_item_copy(): Output array must be a string array')
    if not is_str_arr_type(A):
        raise BodoError(
            'get_str_arr_item_copy(): Input array must be a string array or dictionary encoded array'
            )
    if A == bodo.dict_str_arr_type:
        snp__tpg = 'in_str_arr = A._data'
        leybk__nawo = 'input_index = A._indices[i]'
    else:
        snp__tpg = 'in_str_arr = A'
        leybk__nawo = 'input_index = i'
    tivn__bfkov = f"""def impl(B, j, A, i):
        if j == 0:
            setitem_str_offset(B, 0, 0)

        {snp__tpg}
        {leybk__nawo}

        # set NA
        if bodo.libs.array_kernels.isna(A, i):
            str_arr_set_na(B, j)
            return
        else:
            str_arr_set_not_na(B, j)

        # get input array offsets
        in_start_offset = getitem_str_offset(in_str_arr, input_index)
        in_end_offset = getitem_str_offset(in_str_arr, input_index + 1)
        val_len = in_end_offset - in_start_offset

        # set output offset
        out_start_offset = getitem_str_offset(B, j)
        out_end_offset = out_start_offset + val_len
        setitem_str_offset(B, j + 1, out_end_offset)

        # copy data
        if val_len != 0:
            # ensure required space in output array
            data_arr = B._data
            bodo.libs.array_item_arr_ext.ensure_data_capacity(
                data_arr, np.int64(out_start_offset), np.int64(out_end_offset)
            )
            out_data_ptr = get_data_ptr(B).data
            in_data_ptr = get_data_ptr(in_str_arr).data
            memcpy_region(
                out_data_ptr,
                out_start_offset,
                in_data_ptr,
                in_start_offset,
                val_len,
                1,
            )"""
    grl__ippqn = {}
    exec(tivn__bfkov, {'setitem_str_offset': setitem_str_offset,
        'memcpy_region': memcpy_region, 'getitem_str_offset':
        getitem_str_offset, 'str_arr_set_na': str_arr_set_na,
        'str_arr_set_not_na': str_arr_set_not_na, 'get_data_ptr':
        get_data_ptr, 'bodo': bodo, 'np': np}, grl__ippqn)
    impl = grl__ippqn['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    pqzrf__eht = len(str_arr)
    mfctl__dnp = np.empty(pqzrf__eht, np.bool_)
    for i in range(pqzrf__eht):
        mfctl__dnp[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return mfctl__dnp


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            pqzrf__eht = len(data)
            l = []
            for i in range(pqzrf__eht):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        vcej__eed = data.count
        oep__vcbj = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(vcej__eed)]
        if is_overload_true(str_null_bools):
            oep__vcbj += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(vcej__eed) if is_str_arr_type(data.types[i]) or data.
                types[i] == binary_array_type]
        tivn__bfkov = 'def f(data, str_null_bools=None):\n'
        tivn__bfkov += '  return ({}{})\n'.format(', '.join(oep__vcbj), ',' if
            vcej__eed == 1 else '')
        grl__ippqn = {}
        exec(tivn__bfkov, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, grl__ippqn)
        xsv__kevc = grl__ippqn['f']
        return xsv__kevc
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                pqzrf__eht = len(list_data)
                for i in range(pqzrf__eht):
                    eoon__majd = list_data[i]
                    str_arr[i] = eoon__majd
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                pqzrf__eht = len(list_data)
                for i in range(pqzrf__eht):
                    eoon__majd = list_data[i]
                    str_arr[i] = eoon__majd
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        vcej__eed = str_arr.count
        xlxd__dedhj = 0
        tivn__bfkov = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(vcej__eed):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                tivn__bfkov += (
                    """  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])
"""
                    .format(i, i, vcej__eed + xlxd__dedhj))
                xlxd__dedhj += 1
            else:
                tivn__bfkov += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        tivn__bfkov += '  return\n'
        grl__ippqn = {}
        exec(tivn__bfkov, {'cp_str_list_to_array': cp_str_list_to_array},
            grl__ippqn)
        nkdre__bwcgo = grl__ippqn['f']
        return nkdre__bwcgo
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            pqzrf__eht = len(str_list)
            str_arr = pre_alloc_string_array(pqzrf__eht, -1)
            for i in range(pqzrf__eht):
                eoon__majd = str_list[i]
                str_arr[i] = eoon__majd
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            pqzrf__eht = len(A)
            essum__llfn = 0
            for i in range(pqzrf__eht):
                eoon__majd = A[i]
                essum__llfn += get_utf8_size(eoon__majd)
            return essum__llfn
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        pqzrf__eht = len(arr)
        n_chars = num_total_chars(arr)
        vhbgx__mhn = pre_alloc_string_array(pqzrf__eht, np.int64(n_chars))
        copy_str_arr_slice(vhbgx__mhn, arr, pqzrf__eht)
        return vhbgx__mhn
    return copy_impl


@overload(len, no_unliteral=True)
def str_arr_len_overload(str_arr):
    if str_arr == string_array_type:

        def str_arr_len(str_arr):
            return str_arr.size
        return str_arr_len


@overload_attribute(StringArrayType, 'size')
def str_arr_size_overload(str_arr):
    return lambda str_arr: len(str_arr._data)


@overload_attribute(StringArrayType, 'shape')
def str_arr_shape_overload(str_arr):
    return lambda str_arr: (str_arr.size,)


@overload_attribute(StringArrayType, 'nbytes')
def str_arr_nbytes_overload(str_arr):
    return lambda str_arr: str_arr._data.nbytes


@overload_method(types.Array, 'tolist', no_unliteral=True)
@overload_method(StringArrayType, 'tolist', no_unliteral=True)
def overload_to_list(arr):
    return lambda arr: list(arr)


import llvmlite.binding as ll
from llvmlite import ir as lir
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('setitem_string_array', hstr_ext.setitem_string_array)
ll.add_symbol('is_na', hstr_ext.is_na)
ll.add_symbol('string_array_from_sequence', array_ext.
    string_array_from_sequence)
ll.add_symbol('pd_array_from_string_array', hstr_ext.pd_array_from_string_array
    )
ll.add_symbol('np_array_from_string_array', hstr_ext.np_array_from_string_array
    )
ll.add_symbol('pd_pyarrow_array_from_string_array', hstr_ext.
    pd_pyarrow_array_from_string_array)
ll.add_symbol('convert_len_arr_to_offset32', hstr_ext.
    convert_len_arr_to_offset32)
ll.add_symbol('convert_len_arr_to_offset', hstr_ext.convert_len_arr_to_offset)
ll.add_symbol('set_string_array_range', hstr_ext.set_string_array_range)
ll.add_symbol('str_arr_to_int64', hstr_ext.str_arr_to_int64)
ll.add_symbol('str_arr_to_float64', hstr_ext.str_arr_to_float64)
ll.add_symbol('get_utf8_size', hstr_ext.get_utf8_size)
ll.add_symbol('print_str_arr', hstr_ext.print_str_arr)
ll.add_symbol('inplace_int64_to_str', hstr_ext.inplace_int64_to_str)
ll.add_symbol('str_to_dict_str_array', hstr_ext.str_to_dict_str_array)
inplace_int64_to_str = types.ExternalFunction('inplace_int64_to_str', types
    .void(types.voidptr, types.int64, types.int64))
convert_len_arr_to_offset32 = types.ExternalFunction(
    'convert_len_arr_to_offset32', types.void(types.voidptr, types.intp))
convert_len_arr_to_offset = types.ExternalFunction('convert_len_arr_to_offset',
    types.void(types.voidptr, types.voidptr, types.intp))
setitem_string_array = types.ExternalFunction('setitem_string_array', types
    .void(types.CPointer(offset_type), types.CPointer(char_type), types.
    uint64, types.voidptr, types.intp, offset_type, offset_type, types.intp))
_get_utf8_size = types.ExternalFunction('get_utf8_size', types.intp(types.
    voidptr, types.intp, offset_type))
_print_str_arr = types.ExternalFunction('print_str_arr', types.void(types.
    uint64, types.uint64, types.CPointer(offset_type), types.CPointer(
    char_type)))


@numba.generated_jit(nopython=True)
def empty_str_arr(in_seq):
    tivn__bfkov = 'def f(in_seq):\n'
    tivn__bfkov += '    n_strs = len(in_seq)\n'
    tivn__bfkov += '    A = pre_alloc_string_array(n_strs, -1)\n'
    tivn__bfkov += '    return A\n'
    grl__ippqn = {}
    exec(tivn__bfkov, {'pre_alloc_string_array': pre_alloc_string_array},
        grl__ippqn)
    feu__dqh = grl__ippqn['f']
    return feu__dqh


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        ztcjt__gfelz = 'pre_alloc_binary_array'
    else:
        ztcjt__gfelz = 'pre_alloc_string_array'
    tivn__bfkov = 'def f(in_seq):\n'
    tivn__bfkov += '    n_strs = len(in_seq)\n'
    tivn__bfkov += f'    A = {ztcjt__gfelz}(n_strs, -1)\n'
    tivn__bfkov += '    for i in range(n_strs):\n'
    tivn__bfkov += '        A[i] = in_seq[i]\n'
    tivn__bfkov += '    return A\n'
    grl__ippqn = {}
    exec(tivn__bfkov, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, grl__ippqn)
    feu__dqh = grl__ippqn['f']
    return feu__dqh


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        srhix__wbei = builder.add(mrel__vyznx.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        klsxa__ymw = builder.lshr(lir.Constant(lir.IntType(64), offset_type
            .bitwidth), lir.Constant(lir.IntType(64), 3))
        yhfun__zqfo = builder.mul(srhix__wbei, klsxa__ymw)
        dkq__fpcwk = context.make_array(offset_arr_type)(context, builder,
            mrel__vyznx.offsets).data
        cgutils.memset(builder, dkq__fpcwk, yhfun__zqfo, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        uwbm__kfgfg = mrel__vyznx.n_arrays
        yhfun__zqfo = builder.lshr(builder.add(uwbm__kfgfg, lir.Constant(
            lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        wyynm__gsh = context.make_array(null_bitmap_arr_type)(context,
            builder, mrel__vyznx.null_bitmap).data
        cgutils.memset(builder, wyynm__gsh, yhfun__zqfo, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@numba.njit
def pre_alloc_string_array(n_strs, n_chars):
    if n_chars is None:
        n_chars = -1
    str_arr = init_str_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_strs), (np.int64(n_chars),),
        char_arr_type))
    if n_chars == 0:
        set_all_offsets_to_0(str_arr)
    return str_arr


@register_jitable
def gen_na_str_array_lens(n_strs, total_len, len_arr):
    str_arr = pre_alloc_string_array(n_strs, total_len)
    set_bitmap_all_NA(str_arr)
    offsets = bodo.libs.array_item_arr_ext.get_offsets(str_arr._data)
    gpzke__tyb = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        smth__lcbgk = len(len_arr)
        for i in range(smth__lcbgk):
            offsets[i] = gpzke__tyb
            gpzke__tyb += len_arr[i]
        offsets[smth__lcbgk] = gpzke__tyb
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    fxw__enzwz = i // 8
    wbja__xxup = getitem_str_bitmap(bits, fxw__enzwz)
    wbja__xxup ^= np.uint8(-np.uint8(bit_is_set) ^ wbja__xxup) & kBitmask[i % 8
        ]
    setitem_str_bitmap(bits, fxw__enzwz, wbja__xxup)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    ryjr__qedzp = get_null_bitmap_ptr(out_str_arr)
    sptqo__wtwv = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        liiv__ioxp = get_bit_bitmap(sptqo__wtwv, j)
        set_bit_to(ryjr__qedzp, out_start + j, liiv__ioxp)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, iabj__elpi, awzb__edi, nue__enihz = args
        xfgxg__moo = _get_str_binary_arr_payload(context, builder,
            iabj__elpi, string_array_type)
        vwvqs__mazul = _get_str_binary_arr_payload(context, builder,
            out_arr, string_array_type)
        egqv__ocr = context.make_helper(builder, offset_arr_type,
            xfgxg__moo.offsets).data
        arua__alaq = context.make_helper(builder, offset_arr_type,
            vwvqs__mazul.offsets).data
        amwu__btuc = context.make_helper(builder, char_arr_type, xfgxg__moo
            .data).data
        lhrbz__jkw = context.make_helper(builder, char_arr_type,
            vwvqs__mazul.data).data
        num_total_chars = _get_num_total_chars(builder, egqv__ocr,
            xfgxg__moo.n_arrays)
        mzwz__biat = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        lga__xemks = cgutils.get_or_insert_function(builder.module,
            mzwz__biat, name='set_string_array_range')
        builder.call(lga__xemks, [arua__alaq, lhrbz__jkw, egqv__ocr,
            amwu__btuc, awzb__edi, nue__enihz, xfgxg__moo.n_arrays,
            num_total_chars])
        ygy__vxsu = context.typing_context.resolve_value_type(copy_nulls_range)
        rhpsc__onx = ygy__vxsu.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        ums__ryyph = context.get_function(ygy__vxsu, rhpsc__onx)
        ums__ryyph(builder, (out_arr, iabj__elpi, awzb__edi))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    hergb__dkyyc = c.context.make_helper(c.builder, typ, val)
    kjke__yqp = ArrayItemArrayType(char_arr_type)
    mrel__vyznx = _get_array_item_arr_payload(c.context, c.builder,
        kjke__yqp, hergb__dkyyc.data)
    zixh__rxckz = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    gqn__nhd = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        gqn__nhd = 'pd_array_from_string_array'
    if use_pd_pyarrow_string_array and typ != binary_array_type:
        from bodo.libs.array import array_info_type, array_to_info_codegen
        eowlo__asyrk = array_to_info_codegen(c.context, c.builder,
            array_info_type(typ), (val,), incref=False)
        mzwz__biat = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
            as_pointer()])
        gqn__nhd = 'pd_pyarrow_array_from_string_array'
        rpz__revz = cgutils.get_or_insert_function(c.builder.module,
            mzwz__biat, name=gqn__nhd)
        arr = c.builder.call(rpz__revz, [eowlo__asyrk])
        c.context.nrt.decref(c.builder, typ, val)
        return arr
    mzwz__biat = lir.FunctionType(c.context.get_argument_type(types.
        pyobject), [lir.IntType(64), lir.IntType(offset_type.bitwidth).
        as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
        as_pointer(), lir.IntType(32)])
    rpz__revz = cgutils.get_or_insert_function(c.builder.module, mzwz__biat,
        name=gqn__nhd)
    hfn__ilmm = c.context.make_array(offset_arr_type)(c.context, c.builder,
        mrel__vyznx.offsets).data
    mbb__sqz = c.context.make_array(char_arr_type)(c.context, c.builder,
        mrel__vyznx.data).data
    wyynm__gsh = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, mrel__vyznx.null_bitmap).data
    arr = c.builder.call(rpz__revz, [mrel__vyznx.n_arrays, hfn__ilmm,
        mbb__sqz, wyynm__gsh, zixh__rxckz])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in (string_array_type, binary_array_type
        ), 'str_arr_is_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        wyynm__gsh = context.make_array(null_bitmap_arr_type)(context,
            builder, mrel__vyznx.null_bitmap).data
        cbk__ovhu = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        jua__rrjte = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        wbja__xxup = builder.load(builder.gep(wyynm__gsh, [cbk__ovhu],
            inbounds=True))
        seq__gyu = lir.ArrayType(lir.IntType(8), 8)
        uahoy__sxtf = cgutils.alloca_once_value(builder, lir.Constant(
            seq__gyu, (1, 2, 4, 8, 16, 32, 64, 128)))
        adkkh__xfao = builder.load(builder.gep(uahoy__sxtf, [lir.Constant(
            lir.IntType(64), 0), jua__rrjte], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(wbja__xxup,
            adkkh__xfao), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [string_array_type, binary_array_type
        ], 'str_arr_set_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        cbk__ovhu = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        jua__rrjte = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        wyynm__gsh = context.make_array(null_bitmap_arr_type)(context,
            builder, mrel__vyznx.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, mrel__vyznx
            .offsets).data
        trq__jas = builder.gep(wyynm__gsh, [cbk__ovhu], inbounds=True)
        wbja__xxup = builder.load(trq__jas)
        seq__gyu = lir.ArrayType(lir.IntType(8), 8)
        uahoy__sxtf = cgutils.alloca_once_value(builder, lir.Constant(
            seq__gyu, (1, 2, 4, 8, 16, 32, 64, 128)))
        adkkh__xfao = builder.load(builder.gep(uahoy__sxtf, [lir.Constant(
            lir.IntType(64), 0), jua__rrjte], inbounds=True))
        adkkh__xfao = builder.xor(adkkh__xfao, lir.Constant(lir.IntType(8), -1)
            )
        builder.store(builder.and_(wbja__xxup, adkkh__xfao), trq__jas)
        rmi__kvlp = builder.add(ind, lir.Constant(lir.IntType(64), 1))
        slt__bvls = builder.icmp_unsigned('!=', rmi__kvlp, mrel__vyznx.n_arrays
            )
        with builder.if_then(slt__bvls):
            builder.store(builder.load(builder.gep(offsets, [ind])),
                builder.gep(offsets, [rmi__kvlp]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [binary_array_type, string_array_type
        ], 'str_arr_set_not_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        cbk__ovhu = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        jua__rrjte = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        wyynm__gsh = context.make_array(null_bitmap_arr_type)(context,
            builder, mrel__vyznx.null_bitmap).data
        trq__jas = builder.gep(wyynm__gsh, [cbk__ovhu], inbounds=True)
        wbja__xxup = builder.load(trq__jas)
        seq__gyu = lir.ArrayType(lir.IntType(8), 8)
        uahoy__sxtf = cgutils.alloca_once_value(builder, lir.Constant(
            seq__gyu, (1, 2, 4, 8, 16, 32, 64, 128)))
        adkkh__xfao = builder.load(builder.gep(uahoy__sxtf, [lir.Constant(
            lir.IntType(64), 0), jua__rrjte], inbounds=True))
        builder.store(builder.or_(wbja__xxup, adkkh__xfao), trq__jas)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        yhfun__zqfo = builder.udiv(builder.add(mrel__vyznx.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        wyynm__gsh = context.make_array(null_bitmap_arr_type)(context,
            builder, mrel__vyznx.null_bitmap).data
        cgutils.memset(builder, wyynm__gsh, yhfun__zqfo, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    ymnzx__ytn = context.make_helper(builder, string_array_type, str_arr)
    kjke__yqp = ArrayItemArrayType(char_arr_type)
    kavy__xzlx = context.make_helper(builder, kjke__yqp, ymnzx__ytn.data)
    okfqn__jhkk = ArrayItemArrayPayloadType(kjke__yqp)
    tfokr__oizyg = context.nrt.meminfo_data(builder, kavy__xzlx.meminfo)
    muanc__htlh = builder.bitcast(tfokr__oizyg, context.get_value_type(
        okfqn__jhkk).as_pointer())
    return muanc__htlh


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        olxfq__gebwl, ogm__umcc = args
        bmp__tmj = _get_str_binary_arr_data_payload_ptr(context, builder,
            ogm__umcc)
        jimkh__dnozm = _get_str_binary_arr_data_payload_ptr(context,
            builder, olxfq__gebwl)
        lpd__tqnj = _get_str_binary_arr_payload(context, builder, ogm__umcc,
            sig.args[1])
        viffo__cay = _get_str_binary_arr_payload(context, builder,
            olxfq__gebwl, sig.args[0])
        context.nrt.incref(builder, char_arr_type, lpd__tqnj.data)
        context.nrt.incref(builder, offset_arr_type, lpd__tqnj.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, lpd__tqnj.null_bitmap
            )
        context.nrt.decref(builder, char_arr_type, viffo__cay.data)
        context.nrt.decref(builder, offset_arr_type, viffo__cay.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, viffo__cay.
            null_bitmap)
        builder.store(builder.load(bmp__tmj), jimkh__dnozm)
        return context.get_dummy_value()
    return types.none(to_arr_typ, from_arr_typ), codegen


dummy_use = numba.njit(lambda a: None)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_utf8_size(s):
    if isinstance(s, types.StringLiteral):
        l = len(s.literal_value.encode())
        return lambda s: l

    def impl(s):
        if s is None:
            return 0
        s = bodo.utils.indexing.unoptional(s)
        if s._is_ascii == 1:
            return len(s)
        pqzrf__eht = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return pqzrf__eht
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, tyq__qjqf, hmm__rlt = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder, arr,
            sig.args[0])
        offsets = context.make_helper(builder, offset_arr_type, mrel__vyznx
            .offsets).data
        data = context.make_helper(builder, char_arr_type, mrel__vyznx.data
            ).data
        mzwz__biat = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        rxen__npw = cgutils.get_or_insert_function(builder.module,
            mzwz__biat, name='setitem_string_array')
        mos__xyx = context.get_constant(types.int32, -1)
        zmg__xwkuz = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets,
            mrel__vyznx.n_arrays)
        builder.call(rxen__npw, [offsets, data, num_total_chars, builder.
            extract_value(tyq__qjqf, 0), hmm__rlt, mos__xyx, zmg__xwkuz, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    mzwz__biat = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64)])
    pqz__vbh = cgutils.get_or_insert_function(builder.module, mzwz__biat,
        name='is_na')
    return builder.call(pqz__vbh, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        puwmh__bbskf, dxy__qmmn, vcej__eed, scnk__xqkx = args
        cgutils.raw_memcpy(builder, puwmh__bbskf, dxy__qmmn, vcej__eed,
            scnk__xqkx)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.voidptr, types.intp, types.intp
        ), codegen


@numba.njit
def print_str_arr(arr):
    _print_str_arr(num_strings(arr), num_total_chars(arr), get_offset_ptr(
        arr), get_data_ptr(arr))


def inplace_eq(A, i, val):
    return A[i] == val


@overload(inplace_eq)
def inplace_eq_overload(A, ind, val):

    def impl(A, ind, val):
        xqcvd__kag, atz__iax = unicode_to_utf8_and_len(val)
        ccg__qczn = getitem_str_offset(A, ind)
        hpoxe__lrwu = getitem_str_offset(A, ind + 1)
        jaxna__fdvo = hpoxe__lrwu - ccg__qczn
        if jaxna__fdvo != atz__iax:
            return False
        tyq__qjqf = get_data_ptr_ind(A, ccg__qczn)
        return memcmp(tyq__qjqf, xqcvd__kag, atz__iax) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        ccg__qczn = getitem_str_offset(A, ind)
        jaxna__fdvo = bodo.libs.str_ext.int_to_str_len(val)
        bmg__ink = ccg__qczn + jaxna__fdvo
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            ccg__qczn, bmg__ink)
        tyq__qjqf = get_data_ptr_ind(A, ccg__qczn)
        inplace_int64_to_str(tyq__qjqf, jaxna__fdvo, val)
        setitem_str_offset(A, ind + 1, ccg__qczn + jaxna__fdvo)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        tyq__qjqf, = args
        zfuq__udv = context.insert_const_string(builder.module, '<NA>')
        vclhy__xmv = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, tyq__qjqf, zfuq__udv, vclhy__xmv, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    slu__oubi = len('<NA>')

    def impl(A, ind):
        ccg__qczn = getitem_str_offset(A, ind)
        bmg__ink = ccg__qczn + slu__oubi
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            ccg__qczn, bmg__ink)
        tyq__qjqf = get_data_ptr_ind(A, ccg__qczn)
        inplace_set_NA_str(tyq__qjqf)
        setitem_str_offset(A, ind + 1, ccg__qczn + slu__oubi)
        str_arr_set_not_na(A, ind)
    return impl


@overload(operator.getitem, no_unliteral=True)
def str_arr_getitem_int(A, ind):
    if A != string_array_type:
        return
    if isinstance(ind, types.Integer):

        def str_arr_getitem_impl(A, ind):
            if ind < 0:
                ind += A.size
            ccg__qczn = getitem_str_offset(A, ind)
            hpoxe__lrwu = getitem_str_offset(A, ind + 1)
            hmm__rlt = hpoxe__lrwu - ccg__qczn
            tyq__qjqf = get_data_ptr_ind(A, ccg__qczn)
            gnw__dedv = decode_utf8(tyq__qjqf, hmm__rlt)
            return gnw__dedv
        return str_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            pqzrf__eht = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(pqzrf__eht):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            yxnn__naokl = get_data_ptr(out_arr).data
            cmw__pyqom = get_data_ptr(A).data
            xlxd__dedhj = 0
            cbs__xngo = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(pqzrf__eht):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    jpcn__sbfw = get_str_arr_item_length(A, i)
                    if jpcn__sbfw == 0:
                        pass
                    elif jpcn__sbfw == 1:
                        copy_single_char(yxnn__naokl, cbs__xngo, cmw__pyqom,
                            getitem_str_offset(A, i))
                    else:
                        memcpy_region(yxnn__naokl, cbs__xngo, cmw__pyqom,
                            getitem_str_offset(A, i), jpcn__sbfw, 1)
                    cbs__xngo += jpcn__sbfw
                    setitem_str_offset(out_arr, xlxd__dedhj + 1, cbs__xngo)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, xlxd__dedhj)
                    else:
                        str_arr_set_not_na(out_arr, xlxd__dedhj)
                    xlxd__dedhj += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            pqzrf__eht = len(ind)
            n_chars = 0
            for i in range(pqzrf__eht):
                n_chars += get_str_arr_item_length(A, ind[i])
            out_arr = pre_alloc_string_array(pqzrf__eht, n_chars)
            yxnn__naokl = get_data_ptr(out_arr).data
            cmw__pyqom = get_data_ptr(A).data
            cbs__xngo = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(pqzrf__eht):
                if bodo.libs.array_kernels.isna(ind, i):
                    raise ValueError(
                        'Cannot index with an integer indexer containing NA values'
                        )
                euq__otvx = ind[i]
                jpcn__sbfw = get_str_arr_item_length(A, euq__otvx)
                if jpcn__sbfw == 0:
                    pass
                elif jpcn__sbfw == 1:
                    copy_single_char(yxnn__naokl, cbs__xngo, cmw__pyqom,
                        getitem_str_offset(A, euq__otvx))
                else:
                    memcpy_region(yxnn__naokl, cbs__xngo, cmw__pyqom,
                        getitem_str_offset(A, euq__otvx), jpcn__sbfw, 1)
                cbs__xngo += jpcn__sbfw
                setitem_str_offset(out_arr, i + 1, cbs__xngo)
                if str_arr_is_na(A, euq__otvx):
                    str_arr_set_na(out_arr, i)
                else:
                    str_arr_set_not_na(out_arr, i)
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            pqzrf__eht = len(A)
            mcbu__jhyf = numba.cpython.unicode._normalize_slice(ind, pqzrf__eht
                )
            tdgo__oszq = numba.cpython.unicode._slice_span(mcbu__jhyf)
            if mcbu__jhyf.step == 1:
                ccg__qczn = getitem_str_offset(A, mcbu__jhyf.start)
                hpoxe__lrwu = getitem_str_offset(A, mcbu__jhyf.stop)
                n_chars = hpoxe__lrwu - ccg__qczn
                vhbgx__mhn = pre_alloc_string_array(tdgo__oszq, np.int64(
                    n_chars))
                for i in range(tdgo__oszq):
                    vhbgx__mhn[i] = A[mcbu__jhyf.start + i]
                    if str_arr_is_na(A, mcbu__jhyf.start + i):
                        str_arr_set_na(vhbgx__mhn, i)
                return vhbgx__mhn
            else:
                vhbgx__mhn = pre_alloc_string_array(tdgo__oszq, -1)
                for i in range(tdgo__oszq):
                    vhbgx__mhn[i] = A[mcbu__jhyf.start + i * mcbu__jhyf.step]
                    if str_arr_is_na(A, mcbu__jhyf.start + i * mcbu__jhyf.step
                        ):
                        str_arr_set_na(vhbgx__mhn, i)
                return vhbgx__mhn
        return str_arr_slice_impl
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for StringArray with indexing type {ind} not supported.')


dummy_use = numba.njit(lambda a: None)


@overload(operator.setitem)
def str_arr_setitem(A, idx, val):
    if A != string_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    nzqw__unyf = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(nzqw__unyf)
        wdtx__wfl = 4

        def impl_scalar(A, idx, val):
            ixhdg__dxh = (val._length if val._is_ascii else wdtx__wfl * val
                ._length)
            fcd__zistm = A._data
            ccg__qczn = np.int64(getitem_str_offset(A, idx))
            bmg__ink = ccg__qczn + ixhdg__dxh
            bodo.libs.array_item_arr_ext.ensure_data_capacity(fcd__zistm,
                ccg__qczn, bmg__ink)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                bmg__ink, val._data, val._length, val._kind, val._is_ascii, idx
                )
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                mcbu__jhyf = numba.cpython.unicode._normalize_slice(idx, len(A)
                    )
                wvho__zprr = mcbu__jhyf.start
                fcd__zistm = A._data
                ccg__qczn = np.int64(getitem_str_offset(A, wvho__zprr))
                bmg__ink = ccg__qczn + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(fcd__zistm,
                    ccg__qczn, bmg__ink)
                set_string_array_range(A, val, wvho__zprr, ccg__qczn)
                utbvg__nnkol = 0
                for i in range(mcbu__jhyf.start, mcbu__jhyf.stop,
                    mcbu__jhyf.step):
                    if str_arr_is_na(val, utbvg__nnkol):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    utbvg__nnkol += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                xxi__seq = str_list_to_array(val)
                A[idx] = xxi__seq
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                mcbu__jhyf = numba.cpython.unicode._normalize_slice(idx, len(A)
                    )
                for i in range(mcbu__jhyf.start, mcbu__jhyf.stop,
                    mcbu__jhyf.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(nzqw__unyf)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                pqzrf__eht = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx)
                out_arr = pre_alloc_string_array(pqzrf__eht, -1)
                for i in numba.parfors.parfor.internal_prange(pqzrf__eht):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        out_arr[i] = val
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_scalar
        elif val == string_array_type or isinstance(val, types.Array
            ) and isinstance(val.dtype, types.UnicodeCharSeq):

            def impl_bool_arr(A, idx, val):
                pqzrf__eht = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(pqzrf__eht, -1)
                zgeqv__ffo = 0
                for i in numba.parfors.parfor.internal_prange(pqzrf__eht):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, zgeqv__ffo):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, zgeqv__ffo)
                        else:
                            out_arr[i] = str(val[zgeqv__ffo])
                        zgeqv__ffo += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(nzqw__unyf)
    raise BodoError(nzqw__unyf)


@overload_attribute(StringArrayType, 'dtype')
def overload_str_arr_dtype(A):
    return lambda A: pd.StringDtype()


@overload_attribute(StringArrayType, 'ndim')
def overload_str_arr_ndim(A):
    return lambda A: 1


@overload_method(StringArrayType, 'astype', no_unliteral=True)
def overload_str_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "StringArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.Function) and dtype.key[0] == str:
        return lambda A, dtype, copy=True: A
    cceab__wcuwp = parse_dtype(dtype, 'StringArray.astype')
    if A == cceab__wcuwp:
        return lambda A, dtype, copy=True: A
    if not isinstance(cceab__wcuwp, (types.Float, types.Integer)
        ) and cceab__wcuwp not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype, bodo.dict_str_arr_type):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(cceab__wcuwp, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            pqzrf__eht = len(A)
            B = np.empty(pqzrf__eht, cceab__wcuwp)
            for i in numba.parfors.parfor.internal_prange(pqzrf__eht):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif cceab__wcuwp == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            pqzrf__eht = len(A)
            B = np.empty(pqzrf__eht, cceab__wcuwp)
            for i in numba.parfors.parfor.internal_prange(pqzrf__eht):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif cceab__wcuwp == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            pqzrf__eht = len(A)
            B = np.empty(pqzrf__eht, cceab__wcuwp)
            for i in numba.parfors.parfor.internal_prange(pqzrf__eht):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif cceab__wcuwp == bodo.dict_str_arr_type:

        def impl_dict_str(A, dtype, copy=True):
            return str_arr_to_dict_str_arr(A)
        return impl_dict_str
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            pqzrf__eht = len(A)
            B = np.empty(pqzrf__eht, cceab__wcuwp)
            for i in numba.parfors.parfor.internal_prange(pqzrf__eht):
                B[i] = int(A[i])
            return B
        return impl_int


@numba.jit
def str_arr_to_dict_str_arr(A):
    return str_arr_to_dict_str_arr_cpp(A)


@intrinsic
def str_arr_to_dict_str_arr_cpp(typingctx, str_arr_t):

    def codegen(context, builder, sig, args):
        str_arr, = args
        xovq__segu = bodo.libs.array.array_to_info_codegen(context, builder,
            bodo.libs.array.array_info_type(sig.args[0]), (str_arr,), False)
        mzwz__biat = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        gjjz__nxidf = cgutils.get_or_insert_function(builder.module,
            mzwz__biat, name='str_to_dict_str_array')
        ith__vaa = builder.call(gjjz__nxidf, [xovq__segu])
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        jxdni__jyt = bodo.libs.array.info_to_array_codegen(context, builder,
            sig.return_type(bodo.libs.array.array_info_type, sig.
            return_type), (ith__vaa, context.get_constant_null(sig.
            return_type)))
        return jxdni__jyt
    assert str_arr_t == bodo.string_array_type, 'str_arr_to_dict_str_arr: Input Array is not a Bodo String Array'
    sig = bodo.dict_str_arr_type(bodo.string_array_type)
    return sig, codegen


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        tyq__qjqf, hmm__rlt = args
        rnqv__tem = context.get_python_api(builder)
        fern__matk = rnqv__tem.string_from_string_and_size(tyq__qjqf, hmm__rlt)
        zwp__syd = rnqv__tem.to_native_value(string_type, fern__matk).value
        jtcvx__tobq = cgutils.create_struct_proxy(string_type)(context,
            builder, zwp__syd)
        jtcvx__tobq.hash = jtcvx__tobq.hash.type(-1)
        rnqv__tem.decref(fern__matk)
        return jtcvx__tobq._getvalue()
    return string_type(types.voidptr, types.intp), codegen


def get_arr_data_ptr(arr, ind):
    return arr


@overload(get_arr_data_ptr, no_unliteral=True)
def overload_get_arr_data_ptr(arr, ind):
    assert isinstance(types.unliteral(ind), types.Integer)
    if isinstance(arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(arr, ind):
            return bodo.hiframes.split_impl.get_c_arr_ptr(arr._data.ctypes, ind
                )
        return impl_int
    assert isinstance(arr, types.Array)

    def impl_np(arr, ind):
        return bodo.hiframes.split_impl.get_c_arr_ptr(arr.ctypes, ind)
    return impl_np


def set_to_numeric_out_na_err(out_arr, out_ind, err_code):
    pass


@overload(set_to_numeric_out_na_err)
def set_to_numeric_out_na_err_overload(out_arr, out_ind, err_code):
    if isinstance(out_arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(out_arr, out_ind, err_code):
            bodo.libs.int_arr_ext.set_bit_to_arr(out_arr._null_bitmap,
                out_ind, 0 if err_code == -1 else 1)
        return impl_int
    assert isinstance(out_arr, types.Array)
    if isinstance(out_arr.dtype, types.Float):

        def impl_np(out_arr, out_ind, err_code):
            if err_code == -1:
                out_arr[out_ind] = np.nan
        return impl_np
    return lambda out_arr, out_ind, err_code: None


@numba.njit(no_cpython_wrapper=True)
def str_arr_item_to_numeric(out_arr, out_ind, str_arr, ind):
    err_code = _str_arr_item_to_numeric(get_arr_data_ptr(out_arr, out_ind),
        str_arr, ind, out_arr.dtype)
    set_to_numeric_out_na_err(out_arr, out_ind, err_code)


@intrinsic
def _str_arr_item_to_numeric(typingctx, out_ptr_t, str_arr_t, ind_t,
    out_dtype_t=None):
    assert str_arr_t == string_array_type, '_str_arr_item_to_numeric: str arr expected'
    assert ind_t == types.int64, '_str_arr_item_to_numeric: integer index expected'

    def codegen(context, builder, sig, args):
        xzmrk__prx, arr, ind, lwlos__znwur = args
        mrel__vyznx = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, mrel__vyznx
            .offsets).data
        data = context.make_helper(builder, char_arr_type, mrel__vyznx.data
            ).data
        mzwz__biat = lir.FunctionType(lir.IntType(32), [xzmrk__prx.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        fjncn__gbm = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            fjncn__gbm = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        mxcug__mqc = cgutils.get_or_insert_function(builder.module,
            mzwz__biat, fjncn__gbm)
        return builder.call(mxcug__mqc, [xzmrk__prx, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    zixh__rxckz = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    mzwz__biat = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType
        (8).as_pointer(), lir.IntType(32)])
    jzm__jls = cgutils.get_or_insert_function(c.builder.module, mzwz__biat,
        name='string_array_from_sequence')
    bfrn__omxy = c.builder.call(jzm__jls, [val, zixh__rxckz])
    kjke__yqp = ArrayItemArrayType(char_arr_type)
    kavy__xzlx = c.context.make_helper(c.builder, kjke__yqp)
    kavy__xzlx.meminfo = bfrn__omxy
    ymnzx__ytn = c.context.make_helper(c.builder, typ)
    fcd__zistm = kavy__xzlx._getvalue()
    ymnzx__ytn.data = fcd__zistm
    odace__cbt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ymnzx__ytn._getvalue(), is_error=odace__cbt)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    pqzrf__eht = len(pyval)
    cbs__xngo = 0
    bxhh__dxeg = np.empty(pqzrf__eht + 1, np_offset_type)
    gdj__iodso = []
    xecwo__ttju = np.empty(pqzrf__eht + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        bxhh__dxeg[i] = cbs__xngo
        kyc__hllp = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(xecwo__ttju, i, int(not kyc__hllp)
            )
        if kyc__hllp:
            continue
        itdt__rxqqf = list(s.encode()) if isinstance(s, str) else list(s)
        gdj__iodso.extend(itdt__rxqqf)
        cbs__xngo += len(itdt__rxqqf)
    bxhh__dxeg[pqzrf__eht] = cbs__xngo
    npsmd__mbwb = np.array(gdj__iodso, np.uint8)
    mqso__mal = context.get_constant(types.int64, pqzrf__eht)
    jwrz__tnim = context.get_constant_generic(builder, char_arr_type,
        npsmd__mbwb)
    gumqv__rbgmy = context.get_constant_generic(builder, offset_arr_type,
        bxhh__dxeg)
    ywsb__zgug = context.get_constant_generic(builder, null_bitmap_arr_type,
        xecwo__ttju)
    mrel__vyznx = lir.Constant.literal_struct([mqso__mal, jwrz__tnim,
        gumqv__rbgmy, ywsb__zgug])
    mrel__vyznx = cgutils.global_constant(builder, '.const.payload',
        mrel__vyznx).bitcast(cgutils.voidptr_t)
    itwu__zdncd = context.get_constant(types.int64, -1)
    izq__pfn = context.get_constant_null(types.voidptr)
    ghimt__tcxr = lir.Constant.literal_struct([itwu__zdncd, izq__pfn,
        izq__pfn, mrel__vyznx, itwu__zdncd])
    ghimt__tcxr = cgutils.global_constant(builder, '.const.meminfo',
        ghimt__tcxr).bitcast(cgutils.voidptr_t)
    fcd__zistm = lir.Constant.literal_struct([ghimt__tcxr])
    ymnzx__ytn = lir.Constant.literal_struct([fcd__zistm])
    return ymnzx__ytn


def pre_alloc_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_str_arr_ext_pre_alloc_string_array
    ) = pre_alloc_str_arr_equiv


@overload(glob.glob, no_unliteral=True)
def overload_glob_glob(pathname, recursive=False):

    def _glob_glob_impl(pathname, recursive=False):
        with numba.objmode(l='list_str_type'):
            l = glob.glob(pathname, recursive=recursive)
        return l
    return _glob_glob_impl
