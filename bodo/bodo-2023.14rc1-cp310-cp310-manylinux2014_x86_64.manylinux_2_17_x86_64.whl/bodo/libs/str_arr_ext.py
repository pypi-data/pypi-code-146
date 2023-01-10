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
        hhuk__ejoi = ArrayItemArrayType(char_arr_type)
        zvvkn__tusl = [('data', hhuk__ejoi)]
        models.StructModel.__init__(self, dmm, fe_type, zvvkn__tusl)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        fcwt__zkdlk, = args
        neswy__ouhvz = context.make_helper(builder, string_array_type)
        neswy__ouhvz.data = fcwt__zkdlk
        context.nrt.incref(builder, data_typ, fcwt__zkdlk)
        return neswy__ouhvz._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    fwqc__ajio = c.context.insert_const_string(c.builder.module, 'pandas')
    qnm__fytme = c.pyapi.import_module_noblock(fwqc__ajio)
    prax__btb = c.pyapi.call_method(qnm__fytme, 'StringDtype', ())
    c.pyapi.decref(qnm__fytme)
    return prax__btb


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        yxw__nyc = bodo.libs.dict_arr_ext.get_binary_op_overload(op, lhs, rhs)
        if yxw__nyc is not None:
            return yxw__nyc
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                gai__goss = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(gai__goss)
                for i in numba.parfors.parfor.internal_prange(gai__goss):
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
                gai__goss = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(gai__goss)
                for i in numba.parfors.parfor.internal_prange(gai__goss):
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
                gai__goss = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(gai__goss)
                for i in numba.parfors.parfor.internal_prange(gai__goss):
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
    vsydy__rag = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    bgu__dxb = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and bgu__dxb or vsydy__rag and is_str_arr_type(rhs
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
    npt__ewrc = context.make_helper(builder, arr_typ, arr_value)
    hhuk__ejoi = ArrayItemArrayType(char_arr_type)
    digo__conbi = _get_array_item_arr_payload(context, builder, hhuk__ejoi,
        npt__ewrc.data)
    return digo__conbi


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        return digo__conbi.n_arrays
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
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        gmewp__kwi = context.make_helper(builder, offset_arr_type,
            digo__conbi.offsets).data
        return _get_num_total_chars(builder, gmewp__kwi, digo__conbi.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        aax__yuuv = context.make_helper(builder, offset_arr_type,
            digo__conbi.offsets)
        fjbqm__nct = context.make_helper(builder, offset_ctypes_type)
        fjbqm__nct.data = builder.bitcast(aax__yuuv.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        fjbqm__nct.meminfo = aax__yuuv.meminfo
        prax__btb = fjbqm__nct._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            prax__btb)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        fcwt__zkdlk = context.make_helper(builder, char_arr_type,
            digo__conbi.data)
        fjbqm__nct = context.make_helper(builder, data_ctypes_type)
        fjbqm__nct.data = fcwt__zkdlk.data
        fjbqm__nct.meminfo = fcwt__zkdlk.meminfo
        prax__btb = fjbqm__nct._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, prax__btb)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        yisvd__glom, ind = args
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            yisvd__glom, sig.args[0])
        fcwt__zkdlk = context.make_helper(builder, char_arr_type,
            digo__conbi.data)
        fjbqm__nct = context.make_helper(builder, data_ctypes_type)
        fjbqm__nct.data = builder.gep(fcwt__zkdlk.data, [ind])
        fjbqm__nct.meminfo = fcwt__zkdlk.meminfo
        prax__btb = fjbqm__nct._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, prax__btb)
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        hdhei__uuuf, ikko__nop, jbtd__fwzmk, kthgc__skfqm = args
        lmj__hjjgi = builder.bitcast(builder.gep(hdhei__uuuf, [ikko__nop]),
            lir.IntType(8).as_pointer())
        bcovn__kfrf = builder.bitcast(builder.gep(jbtd__fwzmk, [
            kthgc__skfqm]), lir.IntType(8).as_pointer())
        wbea__nopst = builder.load(bcovn__kfrf)
        builder.store(wbea__nopst, lmj__hjjgi)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        fsxzo__euuie = context.make_helper(builder, null_bitmap_arr_type,
            digo__conbi.null_bitmap)
        fjbqm__nct = context.make_helper(builder, data_ctypes_type)
        fjbqm__nct.data = fsxzo__euuie.data
        fjbqm__nct.meminfo = fsxzo__euuie.meminfo
        prax__btb = fjbqm__nct._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, prax__btb)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        gmewp__kwi = context.make_helper(builder, offset_arr_type,
            digo__conbi.offsets).data
        return builder.load(builder.gep(gmewp__kwi, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, digo__conbi
            .offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        jcbn__ecpjg, ind = args
        if in_bitmap_typ == data_ctypes_type:
            fjbqm__nct = context.make_helper(builder, data_ctypes_type,
                jcbn__ecpjg)
            jcbn__ecpjg = fjbqm__nct.data
        return builder.load(builder.gep(jcbn__ecpjg, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        jcbn__ecpjg, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            fjbqm__nct = context.make_helper(builder, data_ctypes_type,
                jcbn__ecpjg)
            jcbn__ecpjg = fjbqm__nct.data
        builder.store(val, builder.gep(jcbn__ecpjg, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        axl__fojh = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        zsya__xdel = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        hpy__takk = context.make_helper(builder, offset_arr_type, axl__fojh
            .offsets).data
        qqzrj__obj = context.make_helper(builder, offset_arr_type,
            zsya__xdel.offsets).data
        egyv__kmf = context.make_helper(builder, char_arr_type, axl__fojh.data
            ).data
        zuhk__bptx = context.make_helper(builder, char_arr_type, zsya__xdel
            .data).data
        rebwb__odka = context.make_helper(builder, null_bitmap_arr_type,
            axl__fojh.null_bitmap).data
        rsbx__hey = context.make_helper(builder, null_bitmap_arr_type,
            zsya__xdel.null_bitmap).data
        ptk__kvce = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, qqzrj__obj, hpy__takk, ptk__kvce)
        cgutils.memcpy(builder, zuhk__bptx, egyv__kmf, builder.load(builder
            .gep(hpy__takk, [ind])))
        fuze__cjru = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        qdnck__hefj = builder.lshr(fuze__cjru, lir.Constant(lir.IntType(64), 3)
            )
        cgutils.memcpy(builder, rsbx__hey, rebwb__odka, qdnck__hefj)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        axl__fojh = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        zsya__xdel = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        hpy__takk = context.make_helper(builder, offset_arr_type, axl__fojh
            .offsets).data
        egyv__kmf = context.make_helper(builder, char_arr_type, axl__fojh.data
            ).data
        zuhk__bptx = context.make_helper(builder, char_arr_type, zsya__xdel
            .data).data
        num_total_chars = _get_num_total_chars(builder, hpy__takk,
            axl__fojh.n_arrays)
        cgutils.memcpy(builder, zuhk__bptx, egyv__kmf, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        axl__fojh = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        zsya__xdel = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        hpy__takk = context.make_helper(builder, offset_arr_type, axl__fojh
            .offsets).data
        qqzrj__obj = context.make_helper(builder, offset_arr_type,
            zsya__xdel.offsets).data
        rebwb__odka = context.make_helper(builder, null_bitmap_arr_type,
            axl__fojh.null_bitmap).data
        gai__goss = axl__fojh.n_arrays
        uzh__qyqyr = context.get_constant(offset_type, 0)
        tgwp__fjvk = cgutils.alloca_once_value(builder, uzh__qyqyr)
        with cgutils.for_range(builder, gai__goss) as sdbr__rbkzi:
            zmjut__bakxe = lower_is_na(context, builder, rebwb__odka,
                sdbr__rbkzi.index)
            with cgutils.if_likely(builder, builder.not_(zmjut__bakxe)):
                kyvwt__abux = builder.load(builder.gep(hpy__takk, [
                    sdbr__rbkzi.index]))
                ypi__pwvn = builder.load(tgwp__fjvk)
                builder.store(kyvwt__abux, builder.gep(qqzrj__obj, [ypi__pwvn])
                    )
                builder.store(builder.add(ypi__pwvn, lir.Constant(context.
                    get_value_type(offset_type), 1)), tgwp__fjvk)
        ypi__pwvn = builder.load(tgwp__fjvk)
        kyvwt__abux = builder.load(builder.gep(hpy__takk, [gai__goss]))
        builder.store(kyvwt__abux, builder.gep(qqzrj__obj, [ypi__pwvn]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        ent__jbbqm, ind, str, qqp__tck = args
        ent__jbbqm = context.make_array(sig.args[0])(context, builder,
            ent__jbbqm)
        domih__zqki = builder.gep(ent__jbbqm.data, [ind])
        cgutils.raw_memcpy(builder, domih__zqki, str, qqp__tck, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        domih__zqki, ind, twza__rnqod, qqp__tck = args
        domih__zqki = builder.gep(domih__zqki, [ind])
        cgutils.raw_memcpy(builder, domih__zqki, twza__rnqod, qqp__tck, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.generated_jit(nopython=True)
def get_str_arr_item_length(A, i):
    if A == bodo.dict_str_arr_type:

        def impl(A, i):
            idx = A._indices[i]
            lcl__wcxv = A._data
            return np.int64(getitem_str_offset(lcl__wcxv, idx + 1) -
                getitem_str_offset(lcl__wcxv, idx))
        return impl
    else:
        return lambda A, i: np.int64(getitem_str_offset(A, i + 1) -
            getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    yvpp__iypv = np.int64(getitem_str_offset(A, i))
    efhrg__kopov = np.int64(getitem_str_offset(A, i + 1))
    l = efhrg__kopov - yvpp__iypv
    jxxq__lgjkb = get_data_ptr_ind(A, yvpp__iypv)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(jxxq__lgjkb, j) >= 128:
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
        azv__xhrap = 'in_str_arr = A._data'
        pnavk__yquqw = 'input_index = A._indices[i]'
    else:
        azv__xhrap = 'in_str_arr = A'
        pnavk__yquqw = 'input_index = i'
    umxfa__odn = f"""def impl(B, j, A, i):
        if j == 0:
            setitem_str_offset(B, 0, 0)

        {azv__xhrap}
        {pnavk__yquqw}

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
    rcq__faso = {}
    exec(umxfa__odn, {'setitem_str_offset': setitem_str_offset,
        'memcpy_region': memcpy_region, 'getitem_str_offset':
        getitem_str_offset, 'str_arr_set_na': str_arr_set_na,
        'str_arr_set_not_na': str_arr_set_not_na, 'get_data_ptr':
        get_data_ptr, 'bodo': bodo, 'np': np}, rcq__faso)
    impl = rcq__faso['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    gai__goss = len(str_arr)
    jhti__hbb = np.empty(gai__goss, np.bool_)
    for i in range(gai__goss):
        jhti__hbb[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return jhti__hbb


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            gai__goss = len(data)
            l = []
            for i in range(gai__goss):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        zxh__imri = data.count
        qof__izpsp = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(zxh__imri)]
        if is_overload_true(str_null_bools):
            qof__izpsp += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(zxh__imri) if is_str_arr_type(data.types[i]) or data.
                types[i] == binary_array_type]
        umxfa__odn = 'def f(data, str_null_bools=None):\n'
        umxfa__odn += '  return ({}{})\n'.format(', '.join(qof__izpsp), ',' if
            zxh__imri == 1 else '')
        rcq__faso = {}
        exec(umxfa__odn, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, rcq__faso)
        mgd__ngtvj = rcq__faso['f']
        return mgd__ngtvj
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                gai__goss = len(list_data)
                for i in range(gai__goss):
                    twza__rnqod = list_data[i]
                    str_arr[i] = twza__rnqod
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                gai__goss = len(list_data)
                for i in range(gai__goss):
                    twza__rnqod = list_data[i]
                    str_arr[i] = twza__rnqod
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        zxh__imri = str_arr.count
        wioeo__yngq = 0
        umxfa__odn = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(zxh__imri):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                umxfa__odn += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])\n'
                    .format(i, i, zxh__imri + wioeo__yngq))
                wioeo__yngq += 1
            else:
                umxfa__odn += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        umxfa__odn += '  return\n'
        rcq__faso = {}
        exec(umxfa__odn, {'cp_str_list_to_array': cp_str_list_to_array},
            rcq__faso)
        xbkx__gyc = rcq__faso['f']
        return xbkx__gyc
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            gai__goss = len(str_list)
            str_arr = pre_alloc_string_array(gai__goss, -1)
            for i in range(gai__goss):
                twza__rnqod = str_list[i]
                str_arr[i] = twza__rnqod
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            gai__goss = len(A)
            rszzo__iuco = 0
            for i in range(gai__goss):
                twza__rnqod = A[i]
                rszzo__iuco += get_utf8_size(twza__rnqod)
            return rszzo__iuco
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        gai__goss = len(arr)
        n_chars = num_total_chars(arr)
        dzj__hir = pre_alloc_string_array(gai__goss, np.int64(n_chars))
        copy_str_arr_slice(dzj__hir, arr, gai__goss)
        return dzj__hir
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
    umxfa__odn = 'def f(in_seq):\n'
    umxfa__odn += '    n_strs = len(in_seq)\n'
    umxfa__odn += '    A = pre_alloc_string_array(n_strs, -1)\n'
    umxfa__odn += '    return A\n'
    rcq__faso = {}
    exec(umxfa__odn, {'pre_alloc_string_array': pre_alloc_string_array},
        rcq__faso)
    xma__bcvdi = rcq__faso['f']
    return xma__bcvdi


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        ntwah__dwmmn = 'pre_alloc_binary_array'
    else:
        ntwah__dwmmn = 'pre_alloc_string_array'
    umxfa__odn = 'def f(in_seq):\n'
    umxfa__odn += '    n_strs = len(in_seq)\n'
    umxfa__odn += f'    A = {ntwah__dwmmn}(n_strs, -1)\n'
    umxfa__odn += '    for i in range(n_strs):\n'
    umxfa__odn += '        A[i] = in_seq[i]\n'
    umxfa__odn += '    return A\n'
    rcq__faso = {}
    exec(umxfa__odn, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, rcq__faso)
    xma__bcvdi = rcq__faso['f']
    return xma__bcvdi


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        gtav__tqzk = builder.add(digo__conbi.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        zby__zwwjz = builder.lshr(lir.Constant(lir.IntType(64), offset_type
            .bitwidth), lir.Constant(lir.IntType(64), 3))
        qdnck__hefj = builder.mul(gtav__tqzk, zby__zwwjz)
        yzuit__jjdl = context.make_array(offset_arr_type)(context, builder,
            digo__conbi.offsets).data
        cgutils.memset(builder, yzuit__jjdl, qdnck__hefj, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        mls__gqnf = digo__conbi.n_arrays
        qdnck__hefj = builder.lshr(builder.add(mls__gqnf, lir.Constant(lir.
            IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        cbl__ghsx = context.make_array(null_bitmap_arr_type)(context,
            builder, digo__conbi.null_bitmap).data
        cgutils.memset(builder, cbl__ghsx, qdnck__hefj, 0)
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
    isgy__ffuu = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        gnljh__qjgi = len(len_arr)
        for i in range(gnljh__qjgi):
            offsets[i] = isgy__ffuu
            isgy__ffuu += len_arr[i]
        offsets[gnljh__qjgi] = isgy__ffuu
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    jmmbt__rddbd = i // 8
    iiree__rge = getitem_str_bitmap(bits, jmmbt__rddbd)
    iiree__rge ^= np.uint8(-np.uint8(bit_is_set) ^ iiree__rge) & kBitmask[i % 8
        ]
    setitem_str_bitmap(bits, jmmbt__rddbd, iiree__rge)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    jvlff__qqqd = get_null_bitmap_ptr(out_str_arr)
    uxa__dsqmy = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        xatp__qbha = get_bit_bitmap(uxa__dsqmy, j)
        set_bit_to(jvlff__qqqd, out_start + j, xatp__qbha)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, yisvd__glom, emgoo__kkzl, qyi__wqjbn = args
        axl__fojh = _get_str_binary_arr_payload(context, builder,
            yisvd__glom, string_array_type)
        zsya__xdel = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        hpy__takk = context.make_helper(builder, offset_arr_type, axl__fojh
            .offsets).data
        qqzrj__obj = context.make_helper(builder, offset_arr_type,
            zsya__xdel.offsets).data
        egyv__kmf = context.make_helper(builder, char_arr_type, axl__fojh.data
            ).data
        zuhk__bptx = context.make_helper(builder, char_arr_type, zsya__xdel
            .data).data
        num_total_chars = _get_num_total_chars(builder, hpy__takk,
            axl__fojh.n_arrays)
        ocjj__ezh = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        tom__rbl = cgutils.get_or_insert_function(builder.module, ocjj__ezh,
            name='set_string_array_range')
        builder.call(tom__rbl, [qqzrj__obj, zuhk__bptx, hpy__takk,
            egyv__kmf, emgoo__kkzl, qyi__wqjbn, axl__fojh.n_arrays,
            num_total_chars])
        yzrk__gter = context.typing_context.resolve_value_type(copy_nulls_range
            )
        wzq__zquh = yzrk__gter.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        jmemg__omj = context.get_function(yzrk__gter, wzq__zquh)
        jmemg__omj(builder, (out_arr, yisvd__glom, emgoo__kkzl))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    njly__gdrr = c.context.make_helper(c.builder, typ, val)
    hhuk__ejoi = ArrayItemArrayType(char_arr_type)
    digo__conbi = _get_array_item_arr_payload(c.context, c.builder,
        hhuk__ejoi, njly__gdrr.data)
    urkgc__hqsb = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    kslqw__ufu = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        kslqw__ufu = 'pd_array_from_string_array'
    if use_pd_pyarrow_string_array and typ != binary_array_type:
        from bodo.libs.array import array_info_type, array_to_info_codegen
        fjb__dely = array_to_info_codegen(c.context, c.builder,
            array_info_type(typ), (val,), incref=False)
        ocjj__ezh = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
            as_pointer()])
        kslqw__ufu = 'pd_pyarrow_array_from_string_array'
        mqk__eoqk = cgutils.get_or_insert_function(c.builder.module,
            ocjj__ezh, name=kslqw__ufu)
        arr = c.builder.call(mqk__eoqk, [fjb__dely])
        c.context.nrt.decref(c.builder, typ, val)
        return arr
    ocjj__ezh = lir.FunctionType(c.context.get_argument_type(types.pyobject
        ), [lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
        lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
        IntType(32)])
    mqk__eoqk = cgutils.get_or_insert_function(c.builder.module, ocjj__ezh,
        name=kslqw__ufu)
    gmewp__kwi = c.context.make_array(offset_arr_type)(c.context, c.builder,
        digo__conbi.offsets).data
    jxxq__lgjkb = c.context.make_array(char_arr_type)(c.context, c.builder,
        digo__conbi.data).data
    cbl__ghsx = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, digo__conbi.null_bitmap).data
    arr = c.builder.call(mqk__eoqk, [digo__conbi.n_arrays, gmewp__kwi,
        jxxq__lgjkb, cbl__ghsx, urkgc__hqsb])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in (string_array_type, binary_array_type
        ), 'str_arr_is_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        cbl__ghsx = context.make_array(null_bitmap_arr_type)(context,
            builder, digo__conbi.null_bitmap).data
        mzn__dhuu = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        gtmy__epdj = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        iiree__rge = builder.load(builder.gep(cbl__ghsx, [mzn__dhuu],
            inbounds=True))
        ixs__fytl = lir.ArrayType(lir.IntType(8), 8)
        mjly__eelsn = cgutils.alloca_once_value(builder, lir.Constant(
            ixs__fytl, (1, 2, 4, 8, 16, 32, 64, 128)))
        kabdk__iql = builder.load(builder.gep(mjly__eelsn, [lir.Constant(
            lir.IntType(64), 0), gtmy__epdj], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(iiree__rge,
            kabdk__iql), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [string_array_type, binary_array_type
        ], 'str_arr_set_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        mzn__dhuu = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        gtmy__epdj = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        cbl__ghsx = context.make_array(null_bitmap_arr_type)(context,
            builder, digo__conbi.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, digo__conbi
            .offsets).data
        dzrpw__jyfmc = builder.gep(cbl__ghsx, [mzn__dhuu], inbounds=True)
        iiree__rge = builder.load(dzrpw__jyfmc)
        ixs__fytl = lir.ArrayType(lir.IntType(8), 8)
        mjly__eelsn = cgutils.alloca_once_value(builder, lir.Constant(
            ixs__fytl, (1, 2, 4, 8, 16, 32, 64, 128)))
        kabdk__iql = builder.load(builder.gep(mjly__eelsn, [lir.Constant(
            lir.IntType(64), 0), gtmy__epdj], inbounds=True))
        kabdk__iql = builder.xor(kabdk__iql, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(iiree__rge, kabdk__iql), dzrpw__jyfmc)
        kgca__hjob = builder.add(ind, lir.Constant(lir.IntType(64), 1))
        rav__ovio = builder.icmp_unsigned('!=', kgca__hjob, digo__conbi.
            n_arrays)
        with builder.if_then(rav__ovio):
            builder.store(builder.load(builder.gep(offsets, [ind])),
                builder.gep(offsets, [kgca__hjob]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [binary_array_type, string_array_type
        ], 'str_arr_set_not_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        mzn__dhuu = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        gtmy__epdj = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        cbl__ghsx = context.make_array(null_bitmap_arr_type)(context,
            builder, digo__conbi.null_bitmap).data
        dzrpw__jyfmc = builder.gep(cbl__ghsx, [mzn__dhuu], inbounds=True)
        iiree__rge = builder.load(dzrpw__jyfmc)
        ixs__fytl = lir.ArrayType(lir.IntType(8), 8)
        mjly__eelsn = cgutils.alloca_once_value(builder, lir.Constant(
            ixs__fytl, (1, 2, 4, 8, 16, 32, 64, 128)))
        kabdk__iql = builder.load(builder.gep(mjly__eelsn, [lir.Constant(
            lir.IntType(64), 0), gtmy__epdj], inbounds=True))
        builder.store(builder.or_(iiree__rge, kabdk__iql), dzrpw__jyfmc)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        digo__conbi = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        qdnck__hefj = builder.udiv(builder.add(digo__conbi.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        cbl__ghsx = context.make_array(null_bitmap_arr_type)(context,
            builder, digo__conbi.null_bitmap).data
        cgutils.memset(builder, cbl__ghsx, qdnck__hefj, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    qyjto__lpj = context.make_helper(builder, string_array_type, str_arr)
    hhuk__ejoi = ArrayItemArrayType(char_arr_type)
    tcx__uuec = context.make_helper(builder, hhuk__ejoi, qyjto__lpj.data)
    vft__ndu = ArrayItemArrayPayloadType(hhuk__ejoi)
    edce__yaptb = context.nrt.meminfo_data(builder, tcx__uuec.meminfo)
    tzisk__xwj = builder.bitcast(edce__yaptb, context.get_value_type(
        vft__ndu).as_pointer())
    return tzisk__xwj


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        flbtx__afp, shhh__cva = args
        wlbu__hll = _get_str_binary_arr_data_payload_ptr(context, builder,
            shhh__cva)
        aua__ziom = _get_str_binary_arr_data_payload_ptr(context, builder,
            flbtx__afp)
        pujsp__mrj = _get_str_binary_arr_payload(context, builder,
            shhh__cva, sig.args[1])
        tto__zxec = _get_str_binary_arr_payload(context, builder,
            flbtx__afp, sig.args[0])
        context.nrt.incref(builder, char_arr_type, pujsp__mrj.data)
        context.nrt.incref(builder, offset_arr_type, pujsp__mrj.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, pujsp__mrj.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, tto__zxec.data)
        context.nrt.decref(builder, offset_arr_type, tto__zxec.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, tto__zxec.null_bitmap
            )
        builder.store(builder.load(wlbu__hll), aua__ziom)
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
        gai__goss = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return gai__goss
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, domih__zqki, qphix__cblk = args
        digo__conbi = _get_str_binary_arr_payload(context, builder, arr,
            sig.args[0])
        offsets = context.make_helper(builder, offset_arr_type, digo__conbi
            .offsets).data
        data = context.make_helper(builder, char_arr_type, digo__conbi.data
            ).data
        ocjj__ezh = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        mwedo__trbs = cgutils.get_or_insert_function(builder.module,
            ocjj__ezh, name='setitem_string_array')
        bacv__jqusz = context.get_constant(types.int32, -1)
        vms__ohowl = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets,
            digo__conbi.n_arrays)
        builder.call(mwedo__trbs, [offsets, data, num_total_chars, builder.
            extract_value(domih__zqki, 0), qphix__cblk, bacv__jqusz,
            vms__ohowl, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    ocjj__ezh = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer
        (), lir.IntType(64)])
    iuyls__ovtq = cgutils.get_or_insert_function(builder.module, ocjj__ezh,
        name='is_na')
    return builder.call(iuyls__ovtq, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        lmj__hjjgi, bcovn__kfrf, zxh__imri, vuok__wffol = args
        cgutils.raw_memcpy(builder, lmj__hjjgi, bcovn__kfrf, zxh__imri,
            vuok__wffol)
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
        zkifn__hzs, fvfkh__lov = unicode_to_utf8_and_len(val)
        qqabj__mmh = getitem_str_offset(A, ind)
        hpb__appe = getitem_str_offset(A, ind + 1)
        ihnmh__fxbtc = hpb__appe - qqabj__mmh
        if ihnmh__fxbtc != fvfkh__lov:
            return False
        domih__zqki = get_data_ptr_ind(A, qqabj__mmh)
        return memcmp(domih__zqki, zkifn__hzs, fvfkh__lov) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        qqabj__mmh = getitem_str_offset(A, ind)
        ihnmh__fxbtc = bodo.libs.str_ext.int_to_str_len(val)
        mwlp__jgx = qqabj__mmh + ihnmh__fxbtc
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            qqabj__mmh, mwlp__jgx)
        domih__zqki = get_data_ptr_ind(A, qqabj__mmh)
        inplace_int64_to_str(domih__zqki, ihnmh__fxbtc, val)
        setitem_str_offset(A, ind + 1, qqabj__mmh + ihnmh__fxbtc)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        domih__zqki, = args
        sdsxr__ppc = context.insert_const_string(builder.module, '<NA>')
        fztri__rpvl = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, domih__zqki, sdsxr__ppc, fztri__rpvl, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    yxc__rlx = len('<NA>')

    def impl(A, ind):
        qqabj__mmh = getitem_str_offset(A, ind)
        mwlp__jgx = qqabj__mmh + yxc__rlx
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            qqabj__mmh, mwlp__jgx)
        domih__zqki = get_data_ptr_ind(A, qqabj__mmh)
        inplace_set_NA_str(domih__zqki)
        setitem_str_offset(A, ind + 1, qqabj__mmh + yxc__rlx)
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
            qqabj__mmh = getitem_str_offset(A, ind)
            hpb__appe = getitem_str_offset(A, ind + 1)
            qphix__cblk = hpb__appe - qqabj__mmh
            domih__zqki = get_data_ptr_ind(A, qqabj__mmh)
            jdyr__uryao = decode_utf8(domih__zqki, qphix__cblk)
            return jdyr__uryao
        return str_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            gai__goss = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(gai__goss):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            hetio__gtmlj = get_data_ptr(out_arr).data
            nnxfl__stlhf = get_data_ptr(A).data
            wioeo__yngq = 0
            ypi__pwvn = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(gai__goss):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    axm__vzm = get_str_arr_item_length(A, i)
                    if axm__vzm == 0:
                        pass
                    elif axm__vzm == 1:
                        copy_single_char(hetio__gtmlj, ypi__pwvn,
                            nnxfl__stlhf, getitem_str_offset(A, i))
                    else:
                        memcpy_region(hetio__gtmlj, ypi__pwvn, nnxfl__stlhf,
                            getitem_str_offset(A, i), axm__vzm, 1)
                    ypi__pwvn += axm__vzm
                    setitem_str_offset(out_arr, wioeo__yngq + 1, ypi__pwvn)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, wioeo__yngq)
                    else:
                        str_arr_set_not_na(out_arr, wioeo__yngq)
                    wioeo__yngq += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            gai__goss = len(ind)
            n_chars = 0
            for i in range(gai__goss):
                n_chars += get_str_arr_item_length(A, ind[i])
            out_arr = pre_alloc_string_array(gai__goss, n_chars)
            hetio__gtmlj = get_data_ptr(out_arr).data
            nnxfl__stlhf = get_data_ptr(A).data
            ypi__pwvn = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(gai__goss):
                if bodo.libs.array_kernels.isna(ind, i):
                    raise ValueError(
                        'Cannot index with an integer indexer containing NA values'
                        )
                vlrrj__wzpho = ind[i]
                axm__vzm = get_str_arr_item_length(A, vlrrj__wzpho)
                if axm__vzm == 0:
                    pass
                elif axm__vzm == 1:
                    copy_single_char(hetio__gtmlj, ypi__pwvn, nnxfl__stlhf,
                        getitem_str_offset(A, vlrrj__wzpho))
                else:
                    memcpy_region(hetio__gtmlj, ypi__pwvn, nnxfl__stlhf,
                        getitem_str_offset(A, vlrrj__wzpho), axm__vzm, 1)
                ypi__pwvn += axm__vzm
                setitem_str_offset(out_arr, i + 1, ypi__pwvn)
                if str_arr_is_na(A, vlrrj__wzpho):
                    str_arr_set_na(out_arr, i)
                else:
                    str_arr_set_not_na(out_arr, i)
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            gai__goss = len(A)
            icb__npdzj = numba.cpython.unicode._normalize_slice(ind, gai__goss)
            slv__rtbst = numba.cpython.unicode._slice_span(icb__npdzj)
            if icb__npdzj.step == 1:
                qqabj__mmh = getitem_str_offset(A, icb__npdzj.start)
                hpb__appe = getitem_str_offset(A, icb__npdzj.stop)
                n_chars = hpb__appe - qqabj__mmh
                dzj__hir = pre_alloc_string_array(slv__rtbst, np.int64(n_chars)
                    )
                for i in range(slv__rtbst):
                    dzj__hir[i] = A[icb__npdzj.start + i]
                    if str_arr_is_na(A, icb__npdzj.start + i):
                        str_arr_set_na(dzj__hir, i)
                return dzj__hir
            else:
                dzj__hir = pre_alloc_string_array(slv__rtbst, -1)
                for i in range(slv__rtbst):
                    dzj__hir[i] = A[icb__npdzj.start + i * icb__npdzj.step]
                    if str_arr_is_na(A, icb__npdzj.start + i * icb__npdzj.step
                        ):
                        str_arr_set_na(dzj__hir, i)
                return dzj__hir
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
    vfz__ehe = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(vfz__ehe)
        gjg__gvnbw = 4

        def impl_scalar(A, idx, val):
            bfq__fiy = (val._length if val._is_ascii else gjg__gvnbw * val.
                _length)
            fcwt__zkdlk = A._data
            qqabj__mmh = np.int64(getitem_str_offset(A, idx))
            mwlp__jgx = qqabj__mmh + bfq__fiy
            bodo.libs.array_item_arr_ext.ensure_data_capacity(fcwt__zkdlk,
                qqabj__mmh, mwlp__jgx)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                mwlp__jgx, val._data, val._length, val._kind, val._is_ascii,
                idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                icb__npdzj = numba.cpython.unicode._normalize_slice(idx, len(A)
                    )
                yvpp__iypv = icb__npdzj.start
                fcwt__zkdlk = A._data
                qqabj__mmh = np.int64(getitem_str_offset(A, yvpp__iypv))
                mwlp__jgx = qqabj__mmh + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(fcwt__zkdlk,
                    qqabj__mmh, mwlp__jgx)
                set_string_array_range(A, val, yvpp__iypv, qqabj__mmh)
                xnv__wcni = 0
                for i in range(icb__npdzj.start, icb__npdzj.stop,
                    icb__npdzj.step):
                    if str_arr_is_na(val, xnv__wcni):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    xnv__wcni += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                cfm__bbjob = str_list_to_array(val)
                A[idx] = cfm__bbjob
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                icb__npdzj = numba.cpython.unicode._normalize_slice(idx, len(A)
                    )
                for i in range(icb__npdzj.start, icb__npdzj.stop,
                    icb__npdzj.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(vfz__ehe)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                gai__goss = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx)
                out_arr = pre_alloc_string_array(gai__goss, -1)
                for i in numba.parfors.parfor.internal_prange(gai__goss):
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
                gai__goss = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(gai__goss, -1)
                tppjt__ajl = 0
                for i in numba.parfors.parfor.internal_prange(gai__goss):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, tppjt__ajl):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, tppjt__ajl)
                        else:
                            out_arr[i] = str(val[tppjt__ajl])
                        tppjt__ajl += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(vfz__ehe)
    raise BodoError(vfz__ehe)


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
    qazvg__turxz = parse_dtype(dtype, 'StringArray.astype')
    if A == qazvg__turxz:
        return lambda A, dtype, copy=True: A
    if not isinstance(qazvg__turxz, (types.Float, types.Integer)
        ) and qazvg__turxz not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype, bodo.dict_str_arr_type):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(qazvg__turxz, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            gai__goss = len(A)
            B = np.empty(gai__goss, qazvg__turxz)
            for i in numba.parfors.parfor.internal_prange(gai__goss):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif qazvg__turxz == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            gai__goss = len(A)
            B = np.empty(gai__goss, qazvg__turxz)
            for i in numba.parfors.parfor.internal_prange(gai__goss):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif qazvg__turxz == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            gai__goss = len(A)
            B = np.empty(gai__goss, qazvg__turxz)
            for i in numba.parfors.parfor.internal_prange(gai__goss):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif qazvg__turxz == bodo.dict_str_arr_type:

        def impl_dict_str(A, dtype, copy=True):
            return str_arr_to_dict_str_arr(A)
        return impl_dict_str
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            gai__goss = len(A)
            B = np.empty(gai__goss, qazvg__turxz)
            for i in numba.parfors.parfor.internal_prange(gai__goss):
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
        plf__lltv = bodo.libs.array.array_to_info_codegen(context, builder,
            bodo.libs.array.array_info_type(sig.args[0]), (str_arr,), False)
        ocjj__ezh = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        eff__alo = cgutils.get_or_insert_function(builder.module, ocjj__ezh,
            name='str_to_dict_str_array')
        brit__xsfqk = builder.call(eff__alo, [plf__lltv])
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        lcl__wcxv = bodo.libs.array.info_to_array_codegen(context, builder,
            sig.return_type(bodo.libs.array.array_info_type, sig.
            return_type), (brit__xsfqk, context.get_constant_null(sig.
            return_type)))
        return lcl__wcxv
    assert str_arr_t == bodo.string_array_type, 'str_arr_to_dict_str_arr: Input Array is not a Bodo String Array'
    sig = bodo.dict_str_arr_type(bodo.string_array_type)
    return sig, codegen


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        domih__zqki, qphix__cblk = args
        ugyf__xfzy = context.get_python_api(builder)
        mexv__buewu = ugyf__xfzy.string_from_string_and_size(domih__zqki,
            qphix__cblk)
        aimd__dxmwz = ugyf__xfzy.to_native_value(string_type, mexv__buewu
            ).value
        bvbmc__zuvzw = cgutils.create_struct_proxy(string_type)(context,
            builder, aimd__dxmwz)
        bvbmc__zuvzw.hash = bvbmc__zuvzw.hash.type(-1)
        ugyf__xfzy.decref(mexv__buewu)
        return bvbmc__zuvzw._getvalue()
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
        ifs__sqgq, arr, ind, pxpa__nhhh = args
        digo__conbi = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, digo__conbi
            .offsets).data
        data = context.make_helper(builder, char_arr_type, digo__conbi.data
            ).data
        ocjj__ezh = lir.FunctionType(lir.IntType(32), [ifs__sqgq.type, lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        vib__wfvv = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            vib__wfvv = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        lhi__yjaox = cgutils.get_or_insert_function(builder.module,
            ocjj__ezh, vib__wfvv)
        return builder.call(lhi__yjaox, [ifs__sqgq, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    urkgc__hqsb = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    ocjj__ezh = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer(), lir.IntType(32)])
    pdwfi__nhxhd = cgutils.get_or_insert_function(c.builder.module,
        ocjj__ezh, name='string_array_from_sequence')
    pkdjm__rqp = c.builder.call(pdwfi__nhxhd, [val, urkgc__hqsb])
    hhuk__ejoi = ArrayItemArrayType(char_arr_type)
    tcx__uuec = c.context.make_helper(c.builder, hhuk__ejoi)
    tcx__uuec.meminfo = pkdjm__rqp
    qyjto__lpj = c.context.make_helper(c.builder, typ)
    fcwt__zkdlk = tcx__uuec._getvalue()
    qyjto__lpj.data = fcwt__zkdlk
    tivk__nsb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qyjto__lpj._getvalue(), is_error=tivk__nsb)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    gai__goss = len(pyval)
    ypi__pwvn = 0
    mah__hzxx = np.empty(gai__goss + 1, np_offset_type)
    xajzm__anaz = []
    mzfq__atk = np.empty(gai__goss + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        mah__hzxx[i] = ypi__pwvn
        nitm__uifh = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(mzfq__atk, i, int(not nitm__uifh))
        if nitm__uifh:
            continue
        cft__yikp = list(s.encode()) if isinstance(s, str) else list(s)
        xajzm__anaz.extend(cft__yikp)
        ypi__pwvn += len(cft__yikp)
    mah__hzxx[gai__goss] = ypi__pwvn
    hxmv__bcne = np.array(xajzm__anaz, np.uint8)
    lci__yznej = context.get_constant(types.int64, gai__goss)
    qmdar__ihkoh = context.get_constant_generic(builder, char_arr_type,
        hxmv__bcne)
    mwh__vck = context.get_constant_generic(builder, offset_arr_type, mah__hzxx
        )
    pbqcz__ibzsp = context.get_constant_generic(builder,
        null_bitmap_arr_type, mzfq__atk)
    digo__conbi = lir.Constant.literal_struct([lci__yznej, qmdar__ihkoh,
        mwh__vck, pbqcz__ibzsp])
    digo__conbi = cgutils.global_constant(builder, '.const.payload',
        digo__conbi).bitcast(cgutils.voidptr_t)
    vpmt__kda = context.get_constant(types.int64, -1)
    zfthz__oipi = context.get_constant_null(types.voidptr)
    zvuwc__ksb = lir.Constant.literal_struct([vpmt__kda, zfthz__oipi,
        zfthz__oipi, digo__conbi, vpmt__kda])
    zvuwc__ksb = cgutils.global_constant(builder, '.const.meminfo', zvuwc__ksb
        ).bitcast(cgutils.voidptr_t)
    fcwt__zkdlk = lir.Constant.literal_struct([zvuwc__ksb])
    qyjto__lpj = lir.Constant.literal_struct([fcwt__zkdlk])
    return qyjto__lpj


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
