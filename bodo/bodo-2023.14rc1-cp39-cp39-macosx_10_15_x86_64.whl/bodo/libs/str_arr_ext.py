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
        xqg__tief = ArrayItemArrayType(char_arr_type)
        zelc__jxbo = [('data', xqg__tief)]
        models.StructModel.__init__(self, dmm, fe_type, zelc__jxbo)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        awp__gte, = args
        jrq__tjxae = context.make_helper(builder, string_array_type)
        jrq__tjxae.data = awp__gte
        context.nrt.incref(builder, data_typ, awp__gte)
        return jrq__tjxae._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    gsh__dlb = c.context.insert_const_string(c.builder.module, 'pandas')
    qkn__mfqc = c.pyapi.import_module_noblock(gsh__dlb)
    jse__hbssh = c.pyapi.call_method(qkn__mfqc, 'StringDtype', ())
    c.pyapi.decref(qkn__mfqc)
    return jse__hbssh


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        twjd__ezhbe = bodo.libs.dict_arr_ext.get_binary_op_overload(op, lhs,
            rhs)
        if twjd__ezhbe is not None:
            return twjd__ezhbe
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qrys__nxa = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(qrys__nxa)
                for i in numba.parfors.parfor.internal_prange(qrys__nxa):
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
                qrys__nxa = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(qrys__nxa)
                for i in numba.parfors.parfor.internal_prange(qrys__nxa):
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
                qrys__nxa = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(qrys__nxa)
                for i in numba.parfors.parfor.internal_prange(qrys__nxa):
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
    jqt__dpue = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    wsrpw__xez = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and wsrpw__xez or jqt__dpue and is_str_arr_type(rhs
        ):

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
    cnlp__agg = context.make_helper(builder, arr_typ, arr_value)
    xqg__tief = ArrayItemArrayType(char_arr_type)
    sdcxs__cdx = _get_array_item_arr_payload(context, builder, xqg__tief,
        cnlp__agg.data)
    return sdcxs__cdx


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        return sdcxs__cdx.n_arrays
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
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        bkuc__vtk = context.make_helper(builder, offset_arr_type,
            sdcxs__cdx.offsets).data
        return _get_num_total_chars(builder, bkuc__vtk, sdcxs__cdx.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        web__zzxs = context.make_helper(builder, offset_arr_type,
            sdcxs__cdx.offsets)
        duhj__jge = context.make_helper(builder, offset_ctypes_type)
        duhj__jge.data = builder.bitcast(web__zzxs.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        duhj__jge.meminfo = web__zzxs.meminfo
        jse__hbssh = duhj__jge._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            jse__hbssh)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        awp__gte = context.make_helper(builder, char_arr_type, sdcxs__cdx.data)
        duhj__jge = context.make_helper(builder, data_ctypes_type)
        duhj__jge.data = awp__gte.data
        duhj__jge.meminfo = awp__gte.meminfo
        jse__hbssh = duhj__jge._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, jse__hbssh
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        ehmpb__ade, ind = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            ehmpb__ade, sig.args[0])
        awp__gte = context.make_helper(builder, char_arr_type, sdcxs__cdx.data)
        duhj__jge = context.make_helper(builder, data_ctypes_type)
        duhj__jge.data = builder.gep(awp__gte.data, [ind])
        duhj__jge.meminfo = awp__gte.meminfo
        jse__hbssh = duhj__jge._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, jse__hbssh
            )
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        bioix__phj, fjznd__miubw, zest__zlgfp, qshhd__xdcs = args
        fvzlm__ozgb = builder.bitcast(builder.gep(bioix__phj, [fjznd__miubw
            ]), lir.IntType(8).as_pointer())
        bjt__odb = builder.bitcast(builder.gep(zest__zlgfp, [qshhd__xdcs]),
            lir.IntType(8).as_pointer())
        ydsxl__denfi = builder.load(bjt__odb)
        builder.store(ydsxl__denfi, fvzlm__ozgb)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        vvqb__sxveh = context.make_helper(builder, null_bitmap_arr_type,
            sdcxs__cdx.null_bitmap)
        duhj__jge = context.make_helper(builder, data_ctypes_type)
        duhj__jge.data = vvqb__sxveh.data
        duhj__jge.meminfo = vvqb__sxveh.meminfo
        jse__hbssh = duhj__jge._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, jse__hbssh
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        bkuc__vtk = context.make_helper(builder, offset_arr_type,
            sdcxs__cdx.offsets).data
        return builder.load(builder.gep(bkuc__vtk, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, sdcxs__cdx.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        dhtge__wwvbc, ind = args
        if in_bitmap_typ == data_ctypes_type:
            duhj__jge = context.make_helper(builder, data_ctypes_type,
                dhtge__wwvbc)
            dhtge__wwvbc = duhj__jge.data
        return builder.load(builder.gep(dhtge__wwvbc, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        dhtge__wwvbc, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            duhj__jge = context.make_helper(builder, data_ctypes_type,
                dhtge__wwvbc)
            dhtge__wwvbc = duhj__jge.data
        builder.store(val, builder.gep(dhtge__wwvbc, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        tzhz__kntyo = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        hkm__buj = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        powqv__eowe = context.make_helper(builder, offset_arr_type,
            tzhz__kntyo.offsets).data
        gcpye__dtjqz = context.make_helper(builder, offset_arr_type,
            hkm__buj.offsets).data
        kft__zsla = context.make_helper(builder, char_arr_type, tzhz__kntyo
            .data).data
        afhc__uai = context.make_helper(builder, char_arr_type, hkm__buj.data
            ).data
        dbu__vsno = context.make_helper(builder, null_bitmap_arr_type,
            tzhz__kntyo.null_bitmap).data
        umm__znow = context.make_helper(builder, null_bitmap_arr_type,
            hkm__buj.null_bitmap).data
        njvu__ogtl = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, gcpye__dtjqz, powqv__eowe, njvu__ogtl)
        cgutils.memcpy(builder, afhc__uai, kft__zsla, builder.load(builder.
            gep(powqv__eowe, [ind])))
        zfg__uvfwd = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        hle__hgy = builder.lshr(zfg__uvfwd, lir.Constant(lir.IntType(64), 3))
        cgutils.memcpy(builder, umm__znow, dbu__vsno, hle__hgy)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        tzhz__kntyo = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        hkm__buj = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        powqv__eowe = context.make_helper(builder, offset_arr_type,
            tzhz__kntyo.offsets).data
        kft__zsla = context.make_helper(builder, char_arr_type, tzhz__kntyo
            .data).data
        afhc__uai = context.make_helper(builder, char_arr_type, hkm__buj.data
            ).data
        num_total_chars = _get_num_total_chars(builder, powqv__eowe,
            tzhz__kntyo.n_arrays)
        cgutils.memcpy(builder, afhc__uai, kft__zsla, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        tzhz__kntyo = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        hkm__buj = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        powqv__eowe = context.make_helper(builder, offset_arr_type,
            tzhz__kntyo.offsets).data
        gcpye__dtjqz = context.make_helper(builder, offset_arr_type,
            hkm__buj.offsets).data
        dbu__vsno = context.make_helper(builder, null_bitmap_arr_type,
            tzhz__kntyo.null_bitmap).data
        qrys__nxa = tzhz__kntyo.n_arrays
        gmq__ficpb = context.get_constant(offset_type, 0)
        cfryh__rdo = cgutils.alloca_once_value(builder, gmq__ficpb)
        with cgutils.for_range(builder, qrys__nxa) as axeg__pbcef:
            xtfhb__fzymw = lower_is_na(context, builder, dbu__vsno,
                axeg__pbcef.index)
            with cgutils.if_likely(builder, builder.not_(xtfhb__fzymw)):
                ntxcd__jmf = builder.load(builder.gep(powqv__eowe, [
                    axeg__pbcef.index]))
                lpsvv__nune = builder.load(cfryh__rdo)
                builder.store(ntxcd__jmf, builder.gep(gcpye__dtjqz, [
                    lpsvv__nune]))
                builder.store(builder.add(lpsvv__nune, lir.Constant(context
                    .get_value_type(offset_type), 1)), cfryh__rdo)
        lpsvv__nune = builder.load(cfryh__rdo)
        ntxcd__jmf = builder.load(builder.gep(powqv__eowe, [qrys__nxa]))
        builder.store(ntxcd__jmf, builder.gep(gcpye__dtjqz, [lpsvv__nune]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        inz__elc, ind, str, qnt__oyzcx = args
        inz__elc = context.make_array(sig.args[0])(context, builder, inz__elc)
        xofzj__ruqn = builder.gep(inz__elc.data, [ind])
        cgutils.raw_memcpy(builder, xofzj__ruqn, str, qnt__oyzcx, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        xofzj__ruqn, ind, cdiuk__rjhzz, qnt__oyzcx = args
        xofzj__ruqn = builder.gep(xofzj__ruqn, [ind])
        cgutils.raw_memcpy(builder, xofzj__ruqn, cdiuk__rjhzz, qnt__oyzcx, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.generated_jit(nopython=True)
def get_str_arr_item_length(A, i):
    if A == bodo.dict_str_arr_type:

        def impl(A, i):
            idx = A._indices[i]
            jsp__mfvpa = A._data
            return np.int64(getitem_str_offset(jsp__mfvpa, idx + 1) -
                getitem_str_offset(jsp__mfvpa, idx))
        return impl
    else:
        return lambda A, i: np.int64(getitem_str_offset(A, i + 1) -
            getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    snses__pskj = np.int64(getitem_str_offset(A, i))
    exr__nsb = np.int64(getitem_str_offset(A, i + 1))
    l = exr__nsb - snses__pskj
    xhh__bxh = get_data_ptr_ind(A, snses__pskj)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(xhh__bxh, j) >= 128:
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
        cwmfh__dus = 'in_str_arr = A._data'
        fbbdf__modec = 'input_index = A._indices[i]'
    else:
        cwmfh__dus = 'in_str_arr = A'
        fbbdf__modec = 'input_index = i'
    yxgaj__bpzz = f"""def impl(B, j, A, i):
        if j == 0:
            setitem_str_offset(B, 0, 0)

        {cwmfh__dus}
        {fbbdf__modec}

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
    qcr__ivyji = {}
    exec(yxgaj__bpzz, {'setitem_str_offset': setitem_str_offset,
        'memcpy_region': memcpy_region, 'getitem_str_offset':
        getitem_str_offset, 'str_arr_set_na': str_arr_set_na,
        'str_arr_set_not_na': str_arr_set_not_na, 'get_data_ptr':
        get_data_ptr, 'bodo': bodo, 'np': np}, qcr__ivyji)
    impl = qcr__ivyji['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    qrys__nxa = len(str_arr)
    zbtrt__swxej = np.empty(qrys__nxa, np.bool_)
    for i in range(qrys__nxa):
        zbtrt__swxej[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return zbtrt__swxej


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            qrys__nxa = len(data)
            l = []
            for i in range(qrys__nxa):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        tpv__etamr = data.count
        kvub__covw = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(tpv__etamr)]
        if is_overload_true(str_null_bools):
            kvub__covw += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(tpv__etamr) if is_str_arr_type(data.types[i]) or data
                .types[i] == binary_array_type]
        yxgaj__bpzz = 'def f(data, str_null_bools=None):\n'
        yxgaj__bpzz += '  return ({}{})\n'.format(', '.join(kvub__covw), 
            ',' if tpv__etamr == 1 else '')
        qcr__ivyji = {}
        exec(yxgaj__bpzz, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, qcr__ivyji)
        njsz__gcl = qcr__ivyji['f']
        return njsz__gcl
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                qrys__nxa = len(list_data)
                for i in range(qrys__nxa):
                    cdiuk__rjhzz = list_data[i]
                    str_arr[i] = cdiuk__rjhzz
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                qrys__nxa = len(list_data)
                for i in range(qrys__nxa):
                    cdiuk__rjhzz = list_data[i]
                    str_arr[i] = cdiuk__rjhzz
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        tpv__etamr = str_arr.count
        kggt__lvx = 0
        yxgaj__bpzz = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(tpv__etamr):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                yxgaj__bpzz += (
                    """  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])
"""
                    .format(i, i, tpv__etamr + kggt__lvx))
                kggt__lvx += 1
            else:
                yxgaj__bpzz += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        yxgaj__bpzz += '  return\n'
        qcr__ivyji = {}
        exec(yxgaj__bpzz, {'cp_str_list_to_array': cp_str_list_to_array},
            qcr__ivyji)
        unz__gwy = qcr__ivyji['f']
        return unz__gwy
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            qrys__nxa = len(str_list)
            str_arr = pre_alloc_string_array(qrys__nxa, -1)
            for i in range(qrys__nxa):
                cdiuk__rjhzz = str_list[i]
                str_arr[i] = cdiuk__rjhzz
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            qrys__nxa = len(A)
            himxv__bxdn = 0
            for i in range(qrys__nxa):
                cdiuk__rjhzz = A[i]
                himxv__bxdn += get_utf8_size(cdiuk__rjhzz)
            return himxv__bxdn
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        qrys__nxa = len(arr)
        n_chars = num_total_chars(arr)
        wymj__vmz = pre_alloc_string_array(qrys__nxa, np.int64(n_chars))
        copy_str_arr_slice(wymj__vmz, arr, qrys__nxa)
        return wymj__vmz
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
    yxgaj__bpzz = 'def f(in_seq):\n'
    yxgaj__bpzz += '    n_strs = len(in_seq)\n'
    yxgaj__bpzz += '    A = pre_alloc_string_array(n_strs, -1)\n'
    yxgaj__bpzz += '    return A\n'
    qcr__ivyji = {}
    exec(yxgaj__bpzz, {'pre_alloc_string_array': pre_alloc_string_array},
        qcr__ivyji)
    gfyu__wqzm = qcr__ivyji['f']
    return gfyu__wqzm


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        fep__ygc = 'pre_alloc_binary_array'
    else:
        fep__ygc = 'pre_alloc_string_array'
    yxgaj__bpzz = 'def f(in_seq):\n'
    yxgaj__bpzz += '    n_strs = len(in_seq)\n'
    yxgaj__bpzz += f'    A = {fep__ygc}(n_strs, -1)\n'
    yxgaj__bpzz += '    for i in range(n_strs):\n'
    yxgaj__bpzz += '        A[i] = in_seq[i]\n'
    yxgaj__bpzz += '    return A\n'
    qcr__ivyji = {}
    exec(yxgaj__bpzz, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, qcr__ivyji)
    gfyu__wqzm = qcr__ivyji['f']
    return gfyu__wqzm


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        qogwt__ydxm = builder.add(sdcxs__cdx.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        wikl__rzylw = builder.lshr(lir.Constant(lir.IntType(64),
            offset_type.bitwidth), lir.Constant(lir.IntType(64), 3))
        hle__hgy = builder.mul(qogwt__ydxm, wikl__rzylw)
        smag__xlruy = context.make_array(offset_arr_type)(context, builder,
            sdcxs__cdx.offsets).data
        cgutils.memset(builder, smag__xlruy, hle__hgy, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        eei__xcspx = sdcxs__cdx.n_arrays
        hle__hgy = builder.lshr(builder.add(eei__xcspx, lir.Constant(lir.
            IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        kcsc__cevp = context.make_array(null_bitmap_arr_type)(context,
            builder, sdcxs__cdx.null_bitmap).data
        cgutils.memset(builder, kcsc__cevp, hle__hgy, 0)
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
    jvy__snqzg = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        ack__sabe = len(len_arr)
        for i in range(ack__sabe):
            offsets[i] = jvy__snqzg
            jvy__snqzg += len_arr[i]
        offsets[ack__sabe] = jvy__snqzg
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    giwh__jcdhe = i // 8
    aopq__utlqd = getitem_str_bitmap(bits, giwh__jcdhe)
    aopq__utlqd ^= np.uint8(-np.uint8(bit_is_set) ^ aopq__utlqd) & kBitmask[
        i % 8]
    setitem_str_bitmap(bits, giwh__jcdhe, aopq__utlqd)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    jvvr__xuh = get_null_bitmap_ptr(out_str_arr)
    ast__ezyr = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        kqxo__vrrt = get_bit_bitmap(ast__ezyr, j)
        set_bit_to(jvvr__xuh, out_start + j, kqxo__vrrt)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, ehmpb__ade, ycrhu__xxnr, fjf__blqfo = args
        tzhz__kntyo = _get_str_binary_arr_payload(context, builder,
            ehmpb__ade, string_array_type)
        hkm__buj = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        powqv__eowe = context.make_helper(builder, offset_arr_type,
            tzhz__kntyo.offsets).data
        gcpye__dtjqz = context.make_helper(builder, offset_arr_type,
            hkm__buj.offsets).data
        kft__zsla = context.make_helper(builder, char_arr_type, tzhz__kntyo
            .data).data
        afhc__uai = context.make_helper(builder, char_arr_type, hkm__buj.data
            ).data
        num_total_chars = _get_num_total_chars(builder, powqv__eowe,
            tzhz__kntyo.n_arrays)
        docxz__qtel = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        brhw__rmo = cgutils.get_or_insert_function(builder.module,
            docxz__qtel, name='set_string_array_range')
        builder.call(brhw__rmo, [gcpye__dtjqz, afhc__uai, powqv__eowe,
            kft__zsla, ycrhu__xxnr, fjf__blqfo, tzhz__kntyo.n_arrays,
            num_total_chars])
        pft__zikzl = context.typing_context.resolve_value_type(copy_nulls_range
            )
        ddh__pqso = pft__zikzl.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        qxw__ikx = context.get_function(pft__zikzl, ddh__pqso)
        qxw__ikx(builder, (out_arr, ehmpb__ade, ycrhu__xxnr))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    vkyru__hhsgm = c.context.make_helper(c.builder, typ, val)
    xqg__tief = ArrayItemArrayType(char_arr_type)
    sdcxs__cdx = _get_array_item_arr_payload(c.context, c.builder,
        xqg__tief, vkyru__hhsgm.data)
    nxo__rdfcd = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    ekuuq__utzky = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        ekuuq__utzky = 'pd_array_from_string_array'
    if use_pd_pyarrow_string_array and typ != binary_array_type:
        from bodo.libs.array import array_info_type, array_to_info_codegen
        oox__pnuk = array_to_info_codegen(c.context, c.builder,
            array_info_type(typ), (val,), incref=False)
        docxz__qtel = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
            as_pointer()])
        ekuuq__utzky = 'pd_pyarrow_array_from_string_array'
        rhcd__oeumv = cgutils.get_or_insert_function(c.builder.module,
            docxz__qtel, name=ekuuq__utzky)
        arr = c.builder.call(rhcd__oeumv, [oox__pnuk])
        c.context.nrt.decref(c.builder, typ, val)
        return arr
    docxz__qtel = lir.FunctionType(c.context.get_argument_type(types.
        pyobject), [lir.IntType(64), lir.IntType(offset_type.bitwidth).
        as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
        as_pointer(), lir.IntType(32)])
    rhcd__oeumv = cgutils.get_or_insert_function(c.builder.module,
        docxz__qtel, name=ekuuq__utzky)
    bkuc__vtk = c.context.make_array(offset_arr_type)(c.context, c.builder,
        sdcxs__cdx.offsets).data
    xhh__bxh = c.context.make_array(char_arr_type)(c.context, c.builder,
        sdcxs__cdx.data).data
    kcsc__cevp = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, sdcxs__cdx.null_bitmap).data
    arr = c.builder.call(rhcd__oeumv, [sdcxs__cdx.n_arrays, bkuc__vtk,
        xhh__bxh, kcsc__cevp, nxo__rdfcd])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in (string_array_type, binary_array_type
        ), 'str_arr_is_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        kcsc__cevp = context.make_array(null_bitmap_arr_type)(context,
            builder, sdcxs__cdx.null_bitmap).data
        fuudw__ifl = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        febao__rcmaw = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        aopq__utlqd = builder.load(builder.gep(kcsc__cevp, [fuudw__ifl],
            inbounds=True))
        ngpo__hfwq = lir.ArrayType(lir.IntType(8), 8)
        eocsa__bnjis = cgutils.alloca_once_value(builder, lir.Constant(
            ngpo__hfwq, (1, 2, 4, 8, 16, 32, 64, 128)))
        fkxvh__rvk = builder.load(builder.gep(eocsa__bnjis, [lir.Constant(
            lir.IntType(64), 0), febao__rcmaw], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(aopq__utlqd,
            fkxvh__rvk), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [string_array_type, binary_array_type
        ], 'str_arr_set_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        fuudw__ifl = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        febao__rcmaw = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        kcsc__cevp = context.make_array(null_bitmap_arr_type)(context,
            builder, sdcxs__cdx.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, sdcxs__cdx.
            offsets).data
        uxxkr__hini = builder.gep(kcsc__cevp, [fuudw__ifl], inbounds=True)
        aopq__utlqd = builder.load(uxxkr__hini)
        ngpo__hfwq = lir.ArrayType(lir.IntType(8), 8)
        eocsa__bnjis = cgutils.alloca_once_value(builder, lir.Constant(
            ngpo__hfwq, (1, 2, 4, 8, 16, 32, 64, 128)))
        fkxvh__rvk = builder.load(builder.gep(eocsa__bnjis, [lir.Constant(
            lir.IntType(64), 0), febao__rcmaw], inbounds=True))
        fkxvh__rvk = builder.xor(fkxvh__rvk, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(aopq__utlqd, fkxvh__rvk), uxxkr__hini)
        qsxo__wapu = builder.add(ind, lir.Constant(lir.IntType(64), 1))
        ybtxq__uobea = builder.icmp_unsigned('!=', qsxo__wapu, sdcxs__cdx.
            n_arrays)
        with builder.if_then(ybtxq__uobea):
            builder.store(builder.load(builder.gep(offsets, [ind])),
                builder.gep(offsets, [qsxo__wapu]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [binary_array_type, string_array_type
        ], 'str_arr_set_not_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        fuudw__ifl = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        febao__rcmaw = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        kcsc__cevp = context.make_array(null_bitmap_arr_type)(context,
            builder, sdcxs__cdx.null_bitmap).data
        uxxkr__hini = builder.gep(kcsc__cevp, [fuudw__ifl], inbounds=True)
        aopq__utlqd = builder.load(uxxkr__hini)
        ngpo__hfwq = lir.ArrayType(lir.IntType(8), 8)
        eocsa__bnjis = cgutils.alloca_once_value(builder, lir.Constant(
            ngpo__hfwq, (1, 2, 4, 8, 16, 32, 64, 128)))
        fkxvh__rvk = builder.load(builder.gep(eocsa__bnjis, [lir.Constant(
            lir.IntType(64), 0), febao__rcmaw], inbounds=True))
        builder.store(builder.or_(aopq__utlqd, fkxvh__rvk), uxxkr__hini)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        hle__hgy = builder.udiv(builder.add(sdcxs__cdx.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        kcsc__cevp = context.make_array(null_bitmap_arr_type)(context,
            builder, sdcxs__cdx.null_bitmap).data
        cgutils.memset(builder, kcsc__cevp, hle__hgy, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    kvk__sgx = context.make_helper(builder, string_array_type, str_arr)
    xqg__tief = ArrayItemArrayType(char_arr_type)
    wrd__cekz = context.make_helper(builder, xqg__tief, kvk__sgx.data)
    huye__fsv = ArrayItemArrayPayloadType(xqg__tief)
    qnxv__wdexg = context.nrt.meminfo_data(builder, wrd__cekz.meminfo)
    bfh__pwt = builder.bitcast(qnxv__wdexg, context.get_value_type(
        huye__fsv).as_pointer())
    return bfh__pwt


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        waqk__nxmgu, gsqxu__mqw = args
        qfa__mjqa = _get_str_binary_arr_data_payload_ptr(context, builder,
            gsqxu__mqw)
        rlofj__dnp = _get_str_binary_arr_data_payload_ptr(context, builder,
            waqk__nxmgu)
        gmpog__kpq = _get_str_binary_arr_payload(context, builder,
            gsqxu__mqw, sig.args[1])
        cuc__rzd = _get_str_binary_arr_payload(context, builder,
            waqk__nxmgu, sig.args[0])
        context.nrt.incref(builder, char_arr_type, gmpog__kpq.data)
        context.nrt.incref(builder, offset_arr_type, gmpog__kpq.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, gmpog__kpq.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, cuc__rzd.data)
        context.nrt.decref(builder, offset_arr_type, cuc__rzd.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, cuc__rzd.null_bitmap)
        builder.store(builder.load(qfa__mjqa), rlofj__dnp)
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
        qrys__nxa = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return qrys__nxa
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, xofzj__ruqn, whufh__nmwgg = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder, arr, sig
            .args[0])
        offsets = context.make_helper(builder, offset_arr_type, sdcxs__cdx.
            offsets).data
        data = context.make_helper(builder, char_arr_type, sdcxs__cdx.data
            ).data
        docxz__qtel = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        ajubx__uubrg = cgutils.get_or_insert_function(builder.module,
            docxz__qtel, name='setitem_string_array')
        yfi__gfc = context.get_constant(types.int32, -1)
        whyei__qoi = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, sdcxs__cdx
            .n_arrays)
        builder.call(ajubx__uubrg, [offsets, data, num_total_chars, builder
            .extract_value(xofzj__ruqn, 0), whufh__nmwgg, yfi__gfc,
            whyei__qoi, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    docxz__qtel = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64)])
    syjhg__dxmck = cgutils.get_or_insert_function(builder.module,
        docxz__qtel, name='is_na')
    return builder.call(syjhg__dxmck, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        fvzlm__ozgb, bjt__odb, tpv__etamr, omf__qhihh = args
        cgutils.raw_memcpy(builder, fvzlm__ozgb, bjt__odb, tpv__etamr,
            omf__qhihh)
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
        bekjn__vrfh, unxjt__zpl = unicode_to_utf8_and_len(val)
        ejcwb__ocof = getitem_str_offset(A, ind)
        rwnfs__kye = getitem_str_offset(A, ind + 1)
        sbepd__elx = rwnfs__kye - ejcwb__ocof
        if sbepd__elx != unxjt__zpl:
            return False
        xofzj__ruqn = get_data_ptr_ind(A, ejcwb__ocof)
        return memcmp(xofzj__ruqn, bekjn__vrfh, unxjt__zpl) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        ejcwb__ocof = getitem_str_offset(A, ind)
        sbepd__elx = bodo.libs.str_ext.int_to_str_len(val)
        cwtbb__cbo = ejcwb__ocof + sbepd__elx
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            ejcwb__ocof, cwtbb__cbo)
        xofzj__ruqn = get_data_ptr_ind(A, ejcwb__ocof)
        inplace_int64_to_str(xofzj__ruqn, sbepd__elx, val)
        setitem_str_offset(A, ind + 1, ejcwb__ocof + sbepd__elx)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        xofzj__ruqn, = args
        kfenc__ndy = context.insert_const_string(builder.module, '<NA>')
        dkptz__bybo = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, xofzj__ruqn, kfenc__ndy, dkptz__bybo, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    wyfsy__gajfo = len('<NA>')

    def impl(A, ind):
        ejcwb__ocof = getitem_str_offset(A, ind)
        cwtbb__cbo = ejcwb__ocof + wyfsy__gajfo
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            ejcwb__ocof, cwtbb__cbo)
        xofzj__ruqn = get_data_ptr_ind(A, ejcwb__ocof)
        inplace_set_NA_str(xofzj__ruqn)
        setitem_str_offset(A, ind + 1, ejcwb__ocof + wyfsy__gajfo)
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
            ejcwb__ocof = getitem_str_offset(A, ind)
            rwnfs__kye = getitem_str_offset(A, ind + 1)
            whufh__nmwgg = rwnfs__kye - ejcwb__ocof
            xofzj__ruqn = get_data_ptr_ind(A, ejcwb__ocof)
            hhrh__cao = decode_utf8(xofzj__ruqn, whufh__nmwgg)
            return hhrh__cao
        return str_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            qrys__nxa = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(qrys__nxa):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            qqbsr__cwv = get_data_ptr(out_arr).data
            ozmuz__zofz = get_data_ptr(A).data
            kggt__lvx = 0
            lpsvv__nune = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(qrys__nxa):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    vpnns__jzgb = get_str_arr_item_length(A, i)
                    if vpnns__jzgb == 0:
                        pass
                    elif vpnns__jzgb == 1:
                        copy_single_char(qqbsr__cwv, lpsvv__nune,
                            ozmuz__zofz, getitem_str_offset(A, i))
                    else:
                        memcpy_region(qqbsr__cwv, lpsvv__nune, ozmuz__zofz,
                            getitem_str_offset(A, i), vpnns__jzgb, 1)
                    lpsvv__nune += vpnns__jzgb
                    setitem_str_offset(out_arr, kggt__lvx + 1, lpsvv__nune)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, kggt__lvx)
                    else:
                        str_arr_set_not_na(out_arr, kggt__lvx)
                    kggt__lvx += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            qrys__nxa = len(ind)
            n_chars = 0
            for i in range(qrys__nxa):
                n_chars += get_str_arr_item_length(A, ind[i])
            out_arr = pre_alloc_string_array(qrys__nxa, n_chars)
            qqbsr__cwv = get_data_ptr(out_arr).data
            ozmuz__zofz = get_data_ptr(A).data
            lpsvv__nune = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(qrys__nxa):
                if bodo.libs.array_kernels.isna(ind, i):
                    raise ValueError(
                        'Cannot index with an integer indexer containing NA values'
                        )
                fxemo__dtrp = ind[i]
                vpnns__jzgb = get_str_arr_item_length(A, fxemo__dtrp)
                if vpnns__jzgb == 0:
                    pass
                elif vpnns__jzgb == 1:
                    copy_single_char(qqbsr__cwv, lpsvv__nune, ozmuz__zofz,
                        getitem_str_offset(A, fxemo__dtrp))
                else:
                    memcpy_region(qqbsr__cwv, lpsvv__nune, ozmuz__zofz,
                        getitem_str_offset(A, fxemo__dtrp), vpnns__jzgb, 1)
                lpsvv__nune += vpnns__jzgb
                setitem_str_offset(out_arr, i + 1, lpsvv__nune)
                if str_arr_is_na(A, fxemo__dtrp):
                    str_arr_set_na(out_arr, i)
                else:
                    str_arr_set_not_na(out_arr, i)
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            qrys__nxa = len(A)
            wmiiv__fgn = numba.cpython.unicode._normalize_slice(ind, qrys__nxa)
            vblnv__qwvx = numba.cpython.unicode._slice_span(wmiiv__fgn)
            if wmiiv__fgn.step == 1:
                ejcwb__ocof = getitem_str_offset(A, wmiiv__fgn.start)
                rwnfs__kye = getitem_str_offset(A, wmiiv__fgn.stop)
                n_chars = rwnfs__kye - ejcwb__ocof
                wymj__vmz = pre_alloc_string_array(vblnv__qwvx, np.int64(
                    n_chars))
                for i in range(vblnv__qwvx):
                    wymj__vmz[i] = A[wmiiv__fgn.start + i]
                    if str_arr_is_na(A, wmiiv__fgn.start + i):
                        str_arr_set_na(wymj__vmz, i)
                return wymj__vmz
            else:
                wymj__vmz = pre_alloc_string_array(vblnv__qwvx, -1)
                for i in range(vblnv__qwvx):
                    wymj__vmz[i] = A[wmiiv__fgn.start + i * wmiiv__fgn.step]
                    if str_arr_is_na(A, wmiiv__fgn.start + i * wmiiv__fgn.step
                        ):
                        str_arr_set_na(wymj__vmz, i)
                return wymj__vmz
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
    uxa__ahm = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(uxa__ahm)
        rqzch__sjj = 4

        def impl_scalar(A, idx, val):
            lyrn__ggh = (val._length if val._is_ascii else rqzch__sjj * val
                ._length)
            awp__gte = A._data
            ejcwb__ocof = np.int64(getitem_str_offset(A, idx))
            cwtbb__cbo = ejcwb__ocof + lyrn__ggh
            bodo.libs.array_item_arr_ext.ensure_data_capacity(awp__gte,
                ejcwb__ocof, cwtbb__cbo)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                cwtbb__cbo, val._data, val._length, val._kind, val.
                _is_ascii, idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                wmiiv__fgn = numba.cpython.unicode._normalize_slice(idx, len(A)
                    )
                snses__pskj = wmiiv__fgn.start
                awp__gte = A._data
                ejcwb__ocof = np.int64(getitem_str_offset(A, snses__pskj))
                cwtbb__cbo = ejcwb__ocof + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(awp__gte,
                    ejcwb__ocof, cwtbb__cbo)
                set_string_array_range(A, val, snses__pskj, ejcwb__ocof)
                peb__dbdzk = 0
                for i in range(wmiiv__fgn.start, wmiiv__fgn.stop,
                    wmiiv__fgn.step):
                    if str_arr_is_na(val, peb__dbdzk):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    peb__dbdzk += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                hal__wwpgn = str_list_to_array(val)
                A[idx] = hal__wwpgn
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                wmiiv__fgn = numba.cpython.unicode._normalize_slice(idx, len(A)
                    )
                for i in range(wmiiv__fgn.start, wmiiv__fgn.stop,
                    wmiiv__fgn.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(uxa__ahm)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                qrys__nxa = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx)
                out_arr = pre_alloc_string_array(qrys__nxa, -1)
                for i in numba.parfors.parfor.internal_prange(qrys__nxa):
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
                qrys__nxa = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(qrys__nxa, -1)
                hqlri__odt = 0
                for i in numba.parfors.parfor.internal_prange(qrys__nxa):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, hqlri__odt):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, hqlri__odt)
                        else:
                            out_arr[i] = str(val[hqlri__odt])
                        hqlri__odt += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(uxa__ahm)
    raise BodoError(uxa__ahm)


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
    yfjv__ckue = parse_dtype(dtype, 'StringArray.astype')
    if A == yfjv__ckue:
        return lambda A, dtype, copy=True: A
    if not isinstance(yfjv__ckue, (types.Float, types.Integer)
        ) and yfjv__ckue not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype, bodo.dict_str_arr_type):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(yfjv__ckue, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            qrys__nxa = len(A)
            B = np.empty(qrys__nxa, yfjv__ckue)
            for i in numba.parfors.parfor.internal_prange(qrys__nxa):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif yfjv__ckue == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            qrys__nxa = len(A)
            B = np.empty(qrys__nxa, yfjv__ckue)
            for i in numba.parfors.parfor.internal_prange(qrys__nxa):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif yfjv__ckue == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            qrys__nxa = len(A)
            B = np.empty(qrys__nxa, yfjv__ckue)
            for i in numba.parfors.parfor.internal_prange(qrys__nxa):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif yfjv__ckue == bodo.dict_str_arr_type:

        def impl_dict_str(A, dtype, copy=True):
            return str_arr_to_dict_str_arr(A)
        return impl_dict_str
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            qrys__nxa = len(A)
            B = np.empty(qrys__nxa, yfjv__ckue)
            for i in numba.parfors.parfor.internal_prange(qrys__nxa):
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
        wlwc__tsvs = bodo.libs.array.array_to_info_codegen(context, builder,
            bodo.libs.array.array_info_type(sig.args[0]), (str_arr,), False)
        docxz__qtel = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        net__mnos = cgutils.get_or_insert_function(builder.module,
            docxz__qtel, name='str_to_dict_str_array')
        eskqd__ohhpk = builder.call(net__mnos, [wlwc__tsvs])
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        jsp__mfvpa = bodo.libs.array.info_to_array_codegen(context, builder,
            sig.return_type(bodo.libs.array.array_info_type, sig.
            return_type), (eskqd__ohhpk, context.get_constant_null(sig.
            return_type)))
        return jsp__mfvpa
    assert str_arr_t == bodo.string_array_type, 'str_arr_to_dict_str_arr: Input Array is not a Bodo String Array'
    sig = bodo.dict_str_arr_type(bodo.string_array_type)
    return sig, codegen


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        xofzj__ruqn, whufh__nmwgg = args
        vuw__tfqww = context.get_python_api(builder)
        zscx__fel = vuw__tfqww.string_from_string_and_size(xofzj__ruqn,
            whufh__nmwgg)
        ruq__mwbzq = vuw__tfqww.to_native_value(string_type, zscx__fel).value
        tlny__kqts = cgutils.create_struct_proxy(string_type)(context,
            builder, ruq__mwbzq)
        tlny__kqts.hash = tlny__kqts.hash.type(-1)
        vuw__tfqww.decref(zscx__fel)
        return tlny__kqts._getvalue()
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
        gyzv__pjggz, arr, ind, isae__kgesx = args
        sdcxs__cdx = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, sdcxs__cdx.
            offsets).data
        data = context.make_helper(builder, char_arr_type, sdcxs__cdx.data
            ).data
        docxz__qtel = lir.FunctionType(lir.IntType(32), [gyzv__pjggz.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        qfczx__wxbc = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            qfczx__wxbc = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        qwpg__hqvqo = cgutils.get_or_insert_function(builder.module,
            docxz__qtel, qfczx__wxbc)
        return builder.call(qwpg__hqvqo, [gyzv__pjggz, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    nxo__rdfcd = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    docxz__qtel = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer(), lir.IntType(32)])
    rjne__msbu = cgutils.get_or_insert_function(c.builder.module,
        docxz__qtel, name='string_array_from_sequence')
    osdch__fwso = c.builder.call(rjne__msbu, [val, nxo__rdfcd])
    xqg__tief = ArrayItemArrayType(char_arr_type)
    wrd__cekz = c.context.make_helper(c.builder, xqg__tief)
    wrd__cekz.meminfo = osdch__fwso
    kvk__sgx = c.context.make_helper(c.builder, typ)
    awp__gte = wrd__cekz._getvalue()
    kvk__sgx.data = awp__gte
    giqas__aemc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(kvk__sgx._getvalue(), is_error=giqas__aemc)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    qrys__nxa = len(pyval)
    lpsvv__nune = 0
    ysjd__bbhfn = np.empty(qrys__nxa + 1, np_offset_type)
    nwnt__hjgo = []
    ydw__jax = np.empty(qrys__nxa + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        ysjd__bbhfn[i] = lpsvv__nune
        lkr__aqvb = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ydw__jax, i, int(not lkr__aqvb))
        if lkr__aqvb:
            continue
        bvcbi__kam = list(s.encode()) if isinstance(s, str) else list(s)
        nwnt__hjgo.extend(bvcbi__kam)
        lpsvv__nune += len(bvcbi__kam)
    ysjd__bbhfn[qrys__nxa] = lpsvv__nune
    kmxs__rptvf = np.array(nwnt__hjgo, np.uint8)
    xgsgj__fko = context.get_constant(types.int64, qrys__nxa)
    wgcg__kgsc = context.get_constant_generic(builder, char_arr_type,
        kmxs__rptvf)
    rofv__xqjb = context.get_constant_generic(builder, offset_arr_type,
        ysjd__bbhfn)
    ufafs__cnowb = context.get_constant_generic(builder,
        null_bitmap_arr_type, ydw__jax)
    sdcxs__cdx = lir.Constant.literal_struct([xgsgj__fko, wgcg__kgsc,
        rofv__xqjb, ufafs__cnowb])
    sdcxs__cdx = cgutils.global_constant(builder, '.const.payload', sdcxs__cdx
        ).bitcast(cgutils.voidptr_t)
    zro__aadq = context.get_constant(types.int64, -1)
    bshxq__weudd = context.get_constant_null(types.voidptr)
    hfht__fxd = lir.Constant.literal_struct([zro__aadq, bshxq__weudd,
        bshxq__weudd, sdcxs__cdx, zro__aadq])
    hfht__fxd = cgutils.global_constant(builder, '.const.meminfo', hfht__fxd
        ).bitcast(cgutils.voidptr_t)
    awp__gte = lir.Constant.literal_struct([hfht__fxd])
    kvk__sgx = lir.Constant.literal_struct([awp__gte])
    return kvk__sgx


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
