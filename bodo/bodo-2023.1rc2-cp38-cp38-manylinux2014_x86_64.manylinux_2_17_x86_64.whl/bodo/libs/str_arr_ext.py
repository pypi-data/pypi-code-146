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
        sxji__huyw = ArrayItemArrayType(char_arr_type)
        aqkhy__dbpgh = [('data', sxji__huyw)]
        models.StructModel.__init__(self, dmm, fe_type, aqkhy__dbpgh)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        nbm__opca, = args
        pwbac__mkxob = context.make_helper(builder, string_array_type)
        pwbac__mkxob.data = nbm__opca
        context.nrt.incref(builder, data_typ, nbm__opca)
        return pwbac__mkxob._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    fvpoj__gtole = c.context.insert_const_string(c.builder.module, 'pandas')
    rqcp__rgo = c.pyapi.import_module_noblock(fvpoj__gtole)
    xkglz__awytm = c.pyapi.call_method(rqcp__rgo, 'StringDtype', ())
    c.pyapi.decref(rqcp__rgo)
    return xkglz__awytm


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        wneas__wweeh = bodo.libs.dict_arr_ext.get_binary_op_overload(op,
            lhs, rhs)
        if wneas__wweeh is not None:
            return wneas__wweeh
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                dyfur__bhz = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(dyfur__bhz)
                for i in numba.parfors.parfor.internal_prange(dyfur__bhz):
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
                dyfur__bhz = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(dyfur__bhz)
                for i in numba.parfors.parfor.internal_prange(dyfur__bhz):
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
                dyfur__bhz = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(dyfur__bhz)
                for i in numba.parfors.parfor.internal_prange(dyfur__bhz):
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
    aemr__gqmgg = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    aoi__fad = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and aoi__fad or aemr__gqmgg and is_str_arr_type(rhs
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
    olw__puewe = context.make_helper(builder, arr_typ, arr_value)
    sxji__huyw = ArrayItemArrayType(char_arr_type)
    puh__oay = _get_array_item_arr_payload(context, builder, sxji__huyw,
        olw__puewe.data)
    return puh__oay


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        puh__oay = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        return puh__oay.n_arrays
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
        puh__oay = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        rqyp__prmgu = context.make_helper(builder, offset_arr_type,
            puh__oay.offsets).data
        return _get_num_total_chars(builder, rqyp__prmgu, puh__oay.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        puh__oay = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        ktl__eqbth = context.make_helper(builder, offset_arr_type, puh__oay
            .offsets)
        arv__emolm = context.make_helper(builder, offset_ctypes_type)
        arv__emolm.data = builder.bitcast(ktl__eqbth.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        arv__emolm.meminfo = ktl__eqbth.meminfo
        xkglz__awytm = arv__emolm._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            xkglz__awytm)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        puh__oay = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        nbm__opca = context.make_helper(builder, char_arr_type, puh__oay.data)
        arv__emolm = context.make_helper(builder, data_ctypes_type)
        arv__emolm.data = nbm__opca.data
        arv__emolm.meminfo = nbm__opca.meminfo
        xkglz__awytm = arv__emolm._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            xkglz__awytm)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        tce__cmk, ind = args
        puh__oay = _get_str_binary_arr_payload(context, builder, tce__cmk,
            sig.args[0])
        nbm__opca = context.make_helper(builder, char_arr_type, puh__oay.data)
        arv__emolm = context.make_helper(builder, data_ctypes_type)
        arv__emolm.data = builder.gep(nbm__opca.data, [ind])
        arv__emolm.meminfo = nbm__opca.meminfo
        xkglz__awytm = arv__emolm._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            xkglz__awytm)
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        ssiad__dlsq, unh__fekt, qrk__vond, gnr__fezwp = args
        dtwx__fpmm = builder.bitcast(builder.gep(ssiad__dlsq, [unh__fekt]),
            lir.IntType(8).as_pointer())
        lmx__mvok = builder.bitcast(builder.gep(qrk__vond, [gnr__fezwp]),
            lir.IntType(8).as_pointer())
        zdk__xffo = builder.load(lmx__mvok)
        builder.store(zdk__xffo, dtwx__fpmm)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        puh__oay = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        pqwla__dsuv = context.make_helper(builder, null_bitmap_arr_type,
            puh__oay.null_bitmap)
        arv__emolm = context.make_helper(builder, data_ctypes_type)
        arv__emolm.data = pqwla__dsuv.data
        arv__emolm.meminfo = pqwla__dsuv.meminfo
        xkglz__awytm = arv__emolm._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            xkglz__awytm)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        puh__oay = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        rqyp__prmgu = context.make_helper(builder, offset_arr_type,
            puh__oay.offsets).data
        return builder.load(builder.gep(rqyp__prmgu, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        puh__oay = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, puh__oay.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        azvbl__akl, ind = args
        if in_bitmap_typ == data_ctypes_type:
            arv__emolm = context.make_helper(builder, data_ctypes_type,
                azvbl__akl)
            azvbl__akl = arv__emolm.data
        return builder.load(builder.gep(azvbl__akl, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        azvbl__akl, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            arv__emolm = context.make_helper(builder, data_ctypes_type,
                azvbl__akl)
            azvbl__akl = arv__emolm.data
        builder.store(val, builder.gep(azvbl__akl, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        otsnn__emhot = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        fbgl__qgmc = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        moh__vjdbi = context.make_helper(builder, offset_arr_type,
            otsnn__emhot.offsets).data
        wubt__rzket = context.make_helper(builder, offset_arr_type,
            fbgl__qgmc.offsets).data
        dpt__kro = context.make_helper(builder, char_arr_type, otsnn__emhot
            .data).data
        tcau__cudc = context.make_helper(builder, char_arr_type, fbgl__qgmc
            .data).data
        zwg__qmpg = context.make_helper(builder, null_bitmap_arr_type,
            otsnn__emhot.null_bitmap).data
        khgld__zhaa = context.make_helper(builder, null_bitmap_arr_type,
            fbgl__qgmc.null_bitmap).data
        hxeof__ued = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, wubt__rzket, moh__vjdbi, hxeof__ued)
        cgutils.memcpy(builder, tcau__cudc, dpt__kro, builder.load(builder.
            gep(moh__vjdbi, [ind])))
        kifqq__dcf = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        akog__fqz = builder.lshr(kifqq__dcf, lir.Constant(lir.IntType(64), 3))
        cgutils.memcpy(builder, khgld__zhaa, zwg__qmpg, akog__fqz)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        otsnn__emhot = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        fbgl__qgmc = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        moh__vjdbi = context.make_helper(builder, offset_arr_type,
            otsnn__emhot.offsets).data
        dpt__kro = context.make_helper(builder, char_arr_type, otsnn__emhot
            .data).data
        tcau__cudc = context.make_helper(builder, char_arr_type, fbgl__qgmc
            .data).data
        num_total_chars = _get_num_total_chars(builder, moh__vjdbi,
            otsnn__emhot.n_arrays)
        cgutils.memcpy(builder, tcau__cudc, dpt__kro, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        otsnn__emhot = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        fbgl__qgmc = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        moh__vjdbi = context.make_helper(builder, offset_arr_type,
            otsnn__emhot.offsets).data
        wubt__rzket = context.make_helper(builder, offset_arr_type,
            fbgl__qgmc.offsets).data
        zwg__qmpg = context.make_helper(builder, null_bitmap_arr_type,
            otsnn__emhot.null_bitmap).data
        dyfur__bhz = otsnn__emhot.n_arrays
        fjccs__tkb = context.get_constant(offset_type, 0)
        zyv__iknm = cgutils.alloca_once_value(builder, fjccs__tkb)
        with cgutils.for_range(builder, dyfur__bhz) as rpn__jrt:
            nptx__rsakt = lower_is_na(context, builder, zwg__qmpg, rpn__jrt
                .index)
            with cgutils.if_likely(builder, builder.not_(nptx__rsakt)):
                hcit__meeci = builder.load(builder.gep(moh__vjdbi, [
                    rpn__jrt.index]))
                hbt__jux = builder.load(zyv__iknm)
                builder.store(hcit__meeci, builder.gep(wubt__rzket, [hbt__jux])
                    )
                builder.store(builder.add(hbt__jux, lir.Constant(context.
                    get_value_type(offset_type), 1)), zyv__iknm)
        hbt__jux = builder.load(zyv__iknm)
        hcit__meeci = builder.load(builder.gep(moh__vjdbi, [dyfur__bhz]))
        builder.store(hcit__meeci, builder.gep(wubt__rzket, [hbt__jux]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        ywhhj__tdyj, ind, str, vxwv__fezu = args
        ywhhj__tdyj = context.make_array(sig.args[0])(context, builder,
            ywhhj__tdyj)
        tpno__uwn = builder.gep(ywhhj__tdyj.data, [ind])
        cgutils.raw_memcpy(builder, tpno__uwn, str, vxwv__fezu, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        tpno__uwn, ind, iixvb__pcup, vxwv__fezu = args
        tpno__uwn = builder.gep(tpno__uwn, [ind])
        cgutils.raw_memcpy(builder, tpno__uwn, iixvb__pcup, vxwv__fezu, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.generated_jit(nopython=True)
def get_str_arr_item_length(A, i):
    if A == bodo.dict_str_arr_type:

        def impl(A, i):
            idx = A._indices[i]
            kxz__vysrg = A._data
            return np.int64(getitem_str_offset(kxz__vysrg, idx + 1) -
                getitem_str_offset(kxz__vysrg, idx))
        return impl
    else:
        return lambda A, i: np.int64(getitem_str_offset(A, i + 1) -
            getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    lzrb__eqwof = np.int64(getitem_str_offset(A, i))
    wfnw__oxn = np.int64(getitem_str_offset(A, i + 1))
    l = wfnw__oxn - lzrb__eqwof
    vbkzm__ziry = get_data_ptr_ind(A, lzrb__eqwof)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(vbkzm__ziry, j) >= 128:
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
        zjfyr__tju = 'in_str_arr = A._data'
        scbxi__vvvwj = 'input_index = A._indices[i]'
    else:
        zjfyr__tju = 'in_str_arr = A'
        scbxi__vvvwj = 'input_index = i'
    ozzlx__tgikn = f"""def impl(B, j, A, i):
        if j == 0:
            setitem_str_offset(B, 0, 0)

        {zjfyr__tju}
        {scbxi__vvvwj}

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
    aub__vwx = {}
    exec(ozzlx__tgikn, {'setitem_str_offset': setitem_str_offset,
        'memcpy_region': memcpy_region, 'getitem_str_offset':
        getitem_str_offset, 'str_arr_set_na': str_arr_set_na,
        'str_arr_set_not_na': str_arr_set_not_na, 'get_data_ptr':
        get_data_ptr, 'bodo': bodo, 'np': np}, aub__vwx)
    impl = aub__vwx['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    dyfur__bhz = len(str_arr)
    pdz__pbogl = np.empty(dyfur__bhz, np.bool_)
    for i in range(dyfur__bhz):
        pdz__pbogl[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return pdz__pbogl


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            dyfur__bhz = len(data)
            l = []
            for i in range(dyfur__bhz):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        xcp__jfshg = data.count
        iktij__zngs = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(xcp__jfshg)]
        if is_overload_true(str_null_bools):
            iktij__zngs += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(xcp__jfshg) if is_str_arr_type(data.types[i]) or data
                .types[i] == binary_array_type]
        ozzlx__tgikn = 'def f(data, str_null_bools=None):\n'
        ozzlx__tgikn += '  return ({}{})\n'.format(', '.join(iktij__zngs), 
            ',' if xcp__jfshg == 1 else '')
        aub__vwx = {}
        exec(ozzlx__tgikn, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, aub__vwx)
        dlpc__cymi = aub__vwx['f']
        return dlpc__cymi
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                dyfur__bhz = len(list_data)
                for i in range(dyfur__bhz):
                    iixvb__pcup = list_data[i]
                    str_arr[i] = iixvb__pcup
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                dyfur__bhz = len(list_data)
                for i in range(dyfur__bhz):
                    iixvb__pcup = list_data[i]
                    str_arr[i] = iixvb__pcup
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        xcp__jfshg = str_arr.count
        qpac__bxntz = 0
        ozzlx__tgikn = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(xcp__jfshg):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                ozzlx__tgikn += (
                    """  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])
"""
                    .format(i, i, xcp__jfshg + qpac__bxntz))
                qpac__bxntz += 1
            else:
                ozzlx__tgikn += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        ozzlx__tgikn += '  return\n'
        aub__vwx = {}
        exec(ozzlx__tgikn, {'cp_str_list_to_array': cp_str_list_to_array},
            aub__vwx)
        egor__qpym = aub__vwx['f']
        return egor__qpym
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            dyfur__bhz = len(str_list)
            str_arr = pre_alloc_string_array(dyfur__bhz, -1)
            for i in range(dyfur__bhz):
                iixvb__pcup = str_list[i]
                str_arr[i] = iixvb__pcup
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            dyfur__bhz = len(A)
            znpzl__krjbl = 0
            for i in range(dyfur__bhz):
                iixvb__pcup = A[i]
                znpzl__krjbl += get_utf8_size(iixvb__pcup)
            return znpzl__krjbl
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        dyfur__bhz = len(arr)
        n_chars = num_total_chars(arr)
        cbgy__nfni = pre_alloc_string_array(dyfur__bhz, np.int64(n_chars))
        copy_str_arr_slice(cbgy__nfni, arr, dyfur__bhz)
        return cbgy__nfni
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
    ozzlx__tgikn = 'def f(in_seq):\n'
    ozzlx__tgikn += '    n_strs = len(in_seq)\n'
    ozzlx__tgikn += '    A = pre_alloc_string_array(n_strs, -1)\n'
    ozzlx__tgikn += '    return A\n'
    aub__vwx = {}
    exec(ozzlx__tgikn, {'pre_alloc_string_array': pre_alloc_string_array},
        aub__vwx)
    maobg__kolh = aub__vwx['f']
    return maobg__kolh


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        imh__hsmrc = 'pre_alloc_binary_array'
    else:
        imh__hsmrc = 'pre_alloc_string_array'
    ozzlx__tgikn = 'def f(in_seq):\n'
    ozzlx__tgikn += '    n_strs = len(in_seq)\n'
    ozzlx__tgikn += f'    A = {imh__hsmrc}(n_strs, -1)\n'
    ozzlx__tgikn += '    for i in range(n_strs):\n'
    ozzlx__tgikn += '        A[i] = in_seq[i]\n'
    ozzlx__tgikn += '    return A\n'
    aub__vwx = {}
    exec(ozzlx__tgikn, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, aub__vwx)
    maobg__kolh = aub__vwx['f']
    return maobg__kolh


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        puh__oay = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        sac__wkr = builder.add(puh__oay.n_arrays, lir.Constant(lir.IntType(
            64), 1))
        jbdtt__rnqe = builder.lshr(lir.Constant(lir.IntType(64),
            offset_type.bitwidth), lir.Constant(lir.IntType(64), 3))
        akog__fqz = builder.mul(sac__wkr, jbdtt__rnqe)
        vnah__ucjm = context.make_array(offset_arr_type)(context, builder,
            puh__oay.offsets).data
        cgutils.memset(builder, vnah__ucjm, akog__fqz, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        puh__oay = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        pmbvi__aji = puh__oay.n_arrays
        akog__fqz = builder.lshr(builder.add(pmbvi__aji, lir.Constant(lir.
            IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        akud__lef = context.make_array(null_bitmap_arr_type)(context,
            builder, puh__oay.null_bitmap).data
        cgutils.memset(builder, akud__lef, akog__fqz, 0)
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
    bnud__sndz = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        spi__lvij = len(len_arr)
        for i in range(spi__lvij):
            offsets[i] = bnud__sndz
            bnud__sndz += len_arr[i]
        offsets[spi__lvij] = bnud__sndz
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    odj__ysayk = i // 8
    dbp__dvxi = getitem_str_bitmap(bits, odj__ysayk)
    dbp__dvxi ^= np.uint8(-np.uint8(bit_is_set) ^ dbp__dvxi) & kBitmask[i % 8]
    setitem_str_bitmap(bits, odj__ysayk, dbp__dvxi)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    nook__zsre = get_null_bitmap_ptr(out_str_arr)
    xoz__kwswt = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        wdwk__fxozd = get_bit_bitmap(xoz__kwswt, j)
        set_bit_to(nook__zsre, out_start + j, wdwk__fxozd)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, tce__cmk, vvpj__lqd, tbtv__vmgul = args
        otsnn__emhot = _get_str_binary_arr_payload(context, builder,
            tce__cmk, string_array_type)
        fbgl__qgmc = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        moh__vjdbi = context.make_helper(builder, offset_arr_type,
            otsnn__emhot.offsets).data
        wubt__rzket = context.make_helper(builder, offset_arr_type,
            fbgl__qgmc.offsets).data
        dpt__kro = context.make_helper(builder, char_arr_type, otsnn__emhot
            .data).data
        tcau__cudc = context.make_helper(builder, char_arr_type, fbgl__qgmc
            .data).data
        num_total_chars = _get_num_total_chars(builder, moh__vjdbi,
            otsnn__emhot.n_arrays)
        fqx__nqlb = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        jmytz__jqi = cgutils.get_or_insert_function(builder.module,
            fqx__nqlb, name='set_string_array_range')
        builder.call(jmytz__jqi, [wubt__rzket, tcau__cudc, moh__vjdbi,
            dpt__kro, vvpj__lqd, tbtv__vmgul, otsnn__emhot.n_arrays,
            num_total_chars])
        lfmy__qijt = context.typing_context.resolve_value_type(copy_nulls_range
            )
        evj__ctrh = lfmy__qijt.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        bcm__uop = context.get_function(lfmy__qijt, evj__ctrh)
        bcm__uop(builder, (out_arr, tce__cmk, vvpj__lqd))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    mjff__nnhgp = c.context.make_helper(c.builder, typ, val)
    sxji__huyw = ArrayItemArrayType(char_arr_type)
    puh__oay = _get_array_item_arr_payload(c.context, c.builder, sxji__huyw,
        mjff__nnhgp.data)
    foez__fvk = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    nkt__nsvr = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        nkt__nsvr = 'pd_array_from_string_array'
    if use_pd_pyarrow_string_array and typ != binary_array_type:
        from bodo.libs.array import array_info_type, array_to_info_codegen
        uqw__ljn = array_to_info_codegen(c.context, c.builder,
            array_info_type(typ), (val,), incref=False)
        fqx__nqlb = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
            as_pointer()])
        nkt__nsvr = 'pd_pyarrow_array_from_string_array'
        hofyh__mqr = cgutils.get_or_insert_function(c.builder.module,
            fqx__nqlb, name=nkt__nsvr)
        arr = c.builder.call(hofyh__mqr, [uqw__ljn])
        c.context.nrt.decref(c.builder, typ, val)
        return arr
    fqx__nqlb = lir.FunctionType(c.context.get_argument_type(types.pyobject
        ), [lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
        lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
        IntType(32)])
    hofyh__mqr = cgutils.get_or_insert_function(c.builder.module, fqx__nqlb,
        name=nkt__nsvr)
    rqyp__prmgu = c.context.make_array(offset_arr_type)(c.context, c.
        builder, puh__oay.offsets).data
    vbkzm__ziry = c.context.make_array(char_arr_type)(c.context, c.builder,
        puh__oay.data).data
    akud__lef = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, puh__oay.null_bitmap).data
    arr = c.builder.call(hofyh__mqr, [puh__oay.n_arrays, rqyp__prmgu,
        vbkzm__ziry, akud__lef, foez__fvk])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in (string_array_type, binary_array_type
        ), 'str_arr_is_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        puh__oay = _get_str_binary_arr_payload(context, builder, in_str_arr,
            str_arr_typ)
        akud__lef = context.make_array(null_bitmap_arr_type)(context,
            builder, puh__oay.null_bitmap).data
        uqll__mlapq = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        dgd__vydr = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        dbp__dvxi = builder.load(builder.gep(akud__lef, [uqll__mlapq],
            inbounds=True))
        gfkp__bjet = lir.ArrayType(lir.IntType(8), 8)
        yoqq__zuce = cgutils.alloca_once_value(builder, lir.Constant(
            gfkp__bjet, (1, 2, 4, 8, 16, 32, 64, 128)))
        bas__znbam = builder.load(builder.gep(yoqq__zuce, [lir.Constant(lir
            .IntType(64), 0), dgd__vydr], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(dbp__dvxi,
            bas__znbam), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [string_array_type, binary_array_type
        ], 'str_arr_set_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        puh__oay = _get_str_binary_arr_payload(context, builder, in_str_arr,
            str_arr_typ)
        uqll__mlapq = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        dgd__vydr = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        akud__lef = context.make_array(null_bitmap_arr_type)(context,
            builder, puh__oay.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, puh__oay.
            offsets).data
        hhto__zxw = builder.gep(akud__lef, [uqll__mlapq], inbounds=True)
        dbp__dvxi = builder.load(hhto__zxw)
        gfkp__bjet = lir.ArrayType(lir.IntType(8), 8)
        yoqq__zuce = cgutils.alloca_once_value(builder, lir.Constant(
            gfkp__bjet, (1, 2, 4, 8, 16, 32, 64, 128)))
        bas__znbam = builder.load(builder.gep(yoqq__zuce, [lir.Constant(lir
            .IntType(64), 0), dgd__vydr], inbounds=True))
        bas__znbam = builder.xor(bas__znbam, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(dbp__dvxi, bas__znbam), hhto__zxw)
        yfbmt__ttour = builder.add(ind, lir.Constant(lir.IntType(64), 1))
        elgwz__ddvqo = builder.icmp_unsigned('!=', yfbmt__ttour, puh__oay.
            n_arrays)
        with builder.if_then(elgwz__ddvqo):
            builder.store(builder.load(builder.gep(offsets, [ind])),
                builder.gep(offsets, [yfbmt__ttour]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [binary_array_type, string_array_type
        ], 'str_arr_set_not_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        puh__oay = _get_str_binary_arr_payload(context, builder, in_str_arr,
            str_arr_typ)
        uqll__mlapq = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        dgd__vydr = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        akud__lef = context.make_array(null_bitmap_arr_type)(context,
            builder, puh__oay.null_bitmap).data
        hhto__zxw = builder.gep(akud__lef, [uqll__mlapq], inbounds=True)
        dbp__dvxi = builder.load(hhto__zxw)
        gfkp__bjet = lir.ArrayType(lir.IntType(8), 8)
        yoqq__zuce = cgutils.alloca_once_value(builder, lir.Constant(
            gfkp__bjet, (1, 2, 4, 8, 16, 32, 64, 128)))
        bas__znbam = builder.load(builder.gep(yoqq__zuce, [lir.Constant(lir
            .IntType(64), 0), dgd__vydr], inbounds=True))
        builder.store(builder.or_(dbp__dvxi, bas__znbam), hhto__zxw)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        puh__oay = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        akog__fqz = builder.udiv(builder.add(puh__oay.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        akud__lef = context.make_array(null_bitmap_arr_type)(context,
            builder, puh__oay.null_bitmap).data
        cgutils.memset(builder, akud__lef, akog__fqz, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    sbxrs__ngbj = context.make_helper(builder, string_array_type, str_arr)
    sxji__huyw = ArrayItemArrayType(char_arr_type)
    tyo__bwqt = context.make_helper(builder, sxji__huyw, sbxrs__ngbj.data)
    vqz__wty = ArrayItemArrayPayloadType(sxji__huyw)
    qob__xfdp = context.nrt.meminfo_data(builder, tyo__bwqt.meminfo)
    liry__qerft = builder.bitcast(qob__xfdp, context.get_value_type(
        vqz__wty).as_pointer())
    return liry__qerft


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        moth__qqxc, szv__spfxe = args
        favr__yxek = _get_str_binary_arr_data_payload_ptr(context, builder,
            szv__spfxe)
        mcncc__kjn = _get_str_binary_arr_data_payload_ptr(context, builder,
            moth__qqxc)
        ukwne__zmob = _get_str_binary_arr_payload(context, builder,
            szv__spfxe, sig.args[1])
        yuec__lyode = _get_str_binary_arr_payload(context, builder,
            moth__qqxc, sig.args[0])
        context.nrt.incref(builder, char_arr_type, ukwne__zmob.data)
        context.nrt.incref(builder, offset_arr_type, ukwne__zmob.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, ukwne__zmob.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, yuec__lyode.data)
        context.nrt.decref(builder, offset_arr_type, yuec__lyode.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, yuec__lyode.
            null_bitmap)
        builder.store(builder.load(favr__yxek), mcncc__kjn)
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
        dyfur__bhz = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return dyfur__bhz
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, tpno__uwn, yjb__gze = args
        puh__oay = _get_str_binary_arr_payload(context, builder, arr, sig.
            args[0])
        offsets = context.make_helper(builder, offset_arr_type, puh__oay.
            offsets).data
        data = context.make_helper(builder, char_arr_type, puh__oay.data).data
        fqx__nqlb = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        cowk__zntf = cgutils.get_or_insert_function(builder.module,
            fqx__nqlb, name='setitem_string_array')
        kbrq__moejs = context.get_constant(types.int32, -1)
        ivj__cxpbp = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, puh__oay.
            n_arrays)
        builder.call(cowk__zntf, [offsets, data, num_total_chars, builder.
            extract_value(tpno__uwn, 0), yjb__gze, kbrq__moejs, ivj__cxpbp,
            ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    fqx__nqlb = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer
        (), lir.IntType(64)])
    til__wmh = cgutils.get_or_insert_function(builder.module, fqx__nqlb,
        name='is_na')
    return builder.call(til__wmh, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        dtwx__fpmm, lmx__mvok, xcp__jfshg, arka__ajv = args
        cgutils.raw_memcpy(builder, dtwx__fpmm, lmx__mvok, xcp__jfshg,
            arka__ajv)
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
        fhql__uepq, pnzvv__ieqnf = unicode_to_utf8_and_len(val)
        hxyf__vji = getitem_str_offset(A, ind)
        uqn__wcxz = getitem_str_offset(A, ind + 1)
        yapmn__bmy = uqn__wcxz - hxyf__vji
        if yapmn__bmy != pnzvv__ieqnf:
            return False
        tpno__uwn = get_data_ptr_ind(A, hxyf__vji)
        return memcmp(tpno__uwn, fhql__uepq, pnzvv__ieqnf) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        hxyf__vji = getitem_str_offset(A, ind)
        yapmn__bmy = bodo.libs.str_ext.int_to_str_len(val)
        nkp__xxtfj = hxyf__vji + yapmn__bmy
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            hxyf__vji, nkp__xxtfj)
        tpno__uwn = get_data_ptr_ind(A, hxyf__vji)
        inplace_int64_to_str(tpno__uwn, yapmn__bmy, val)
        setitem_str_offset(A, ind + 1, hxyf__vji + yapmn__bmy)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        tpno__uwn, = args
        ygdk__ieuz = context.insert_const_string(builder.module, '<NA>')
        xipjq__mvzn = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, tpno__uwn, ygdk__ieuz, xipjq__mvzn, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    jlu__whm = len('<NA>')

    def impl(A, ind):
        hxyf__vji = getitem_str_offset(A, ind)
        nkp__xxtfj = hxyf__vji + jlu__whm
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            hxyf__vji, nkp__xxtfj)
        tpno__uwn = get_data_ptr_ind(A, hxyf__vji)
        inplace_set_NA_str(tpno__uwn)
        setitem_str_offset(A, ind + 1, hxyf__vji + jlu__whm)
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
            hxyf__vji = getitem_str_offset(A, ind)
            uqn__wcxz = getitem_str_offset(A, ind + 1)
            yjb__gze = uqn__wcxz - hxyf__vji
            tpno__uwn = get_data_ptr_ind(A, hxyf__vji)
            eerws__nvp = decode_utf8(tpno__uwn, yjb__gze)
            return eerws__nvp
        return str_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            dyfur__bhz = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(dyfur__bhz):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            fqc__ctx = get_data_ptr(out_arr).data
            vimz__shs = get_data_ptr(A).data
            qpac__bxntz = 0
            hbt__jux = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(dyfur__bhz):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    tlsa__evbm = get_str_arr_item_length(A, i)
                    if tlsa__evbm == 0:
                        pass
                    elif tlsa__evbm == 1:
                        copy_single_char(fqc__ctx, hbt__jux, vimz__shs,
                            getitem_str_offset(A, i))
                    else:
                        memcpy_region(fqc__ctx, hbt__jux, vimz__shs,
                            getitem_str_offset(A, i), tlsa__evbm, 1)
                    hbt__jux += tlsa__evbm
                    setitem_str_offset(out_arr, qpac__bxntz + 1, hbt__jux)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, qpac__bxntz)
                    else:
                        str_arr_set_not_na(out_arr, qpac__bxntz)
                    qpac__bxntz += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            dyfur__bhz = len(ind)
            n_chars = 0
            for i in range(dyfur__bhz):
                n_chars += get_str_arr_item_length(A, ind[i])
            out_arr = pre_alloc_string_array(dyfur__bhz, n_chars)
            fqc__ctx = get_data_ptr(out_arr).data
            vimz__shs = get_data_ptr(A).data
            hbt__jux = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(dyfur__bhz):
                if bodo.libs.array_kernels.isna(ind, i):
                    raise ValueError(
                        'Cannot index with an integer indexer containing NA values'
                        )
                hhgah__tqx = ind[i]
                tlsa__evbm = get_str_arr_item_length(A, hhgah__tqx)
                if tlsa__evbm == 0:
                    pass
                elif tlsa__evbm == 1:
                    copy_single_char(fqc__ctx, hbt__jux, vimz__shs,
                        getitem_str_offset(A, hhgah__tqx))
                else:
                    memcpy_region(fqc__ctx, hbt__jux, vimz__shs,
                        getitem_str_offset(A, hhgah__tqx), tlsa__evbm, 1)
                hbt__jux += tlsa__evbm
                setitem_str_offset(out_arr, i + 1, hbt__jux)
                if str_arr_is_na(A, hhgah__tqx):
                    str_arr_set_na(out_arr, i)
                else:
                    str_arr_set_not_na(out_arr, i)
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            dyfur__bhz = len(A)
            qvl__xbtk = numba.cpython.unicode._normalize_slice(ind, dyfur__bhz)
            kszn__zjvnb = numba.cpython.unicode._slice_span(qvl__xbtk)
            if qvl__xbtk.step == 1:
                hxyf__vji = getitem_str_offset(A, qvl__xbtk.start)
                uqn__wcxz = getitem_str_offset(A, qvl__xbtk.stop)
                n_chars = uqn__wcxz - hxyf__vji
                cbgy__nfni = pre_alloc_string_array(kszn__zjvnb, np.int64(
                    n_chars))
                for i in range(kszn__zjvnb):
                    cbgy__nfni[i] = A[qvl__xbtk.start + i]
                    if str_arr_is_na(A, qvl__xbtk.start + i):
                        str_arr_set_na(cbgy__nfni, i)
                return cbgy__nfni
            else:
                cbgy__nfni = pre_alloc_string_array(kszn__zjvnb, -1)
                for i in range(kszn__zjvnb):
                    cbgy__nfni[i] = A[qvl__xbtk.start + i * qvl__xbtk.step]
                    if str_arr_is_na(A, qvl__xbtk.start + i * qvl__xbtk.step):
                        str_arr_set_na(cbgy__nfni, i)
                return cbgy__nfni
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
    xxjqe__zid = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(xxjqe__zid)
        vcsdm__isptn = 4

        def impl_scalar(A, idx, val):
            wcy__bsp = (val._length if val._is_ascii else vcsdm__isptn *
                val._length)
            nbm__opca = A._data
            hxyf__vji = np.int64(getitem_str_offset(A, idx))
            nkp__xxtfj = hxyf__vji + wcy__bsp
            bodo.libs.array_item_arr_ext.ensure_data_capacity(nbm__opca,
                hxyf__vji, nkp__xxtfj)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                nkp__xxtfj, val._data, val._length, val._kind, val.
                _is_ascii, idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                qvl__xbtk = numba.cpython.unicode._normalize_slice(idx, len(A))
                lzrb__eqwof = qvl__xbtk.start
                nbm__opca = A._data
                hxyf__vji = np.int64(getitem_str_offset(A, lzrb__eqwof))
                nkp__xxtfj = hxyf__vji + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(nbm__opca,
                    hxyf__vji, nkp__xxtfj)
                set_string_array_range(A, val, lzrb__eqwof, hxyf__vji)
                cjv__vouo = 0
                for i in range(qvl__xbtk.start, qvl__xbtk.stop, qvl__xbtk.step
                    ):
                    if str_arr_is_na(val, cjv__vouo):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    cjv__vouo += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                wojtm__ujvct = str_list_to_array(val)
                A[idx] = wojtm__ujvct
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                qvl__xbtk = numba.cpython.unicode._normalize_slice(idx, len(A))
                for i in range(qvl__xbtk.start, qvl__xbtk.stop, qvl__xbtk.step
                    ):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(xxjqe__zid)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                dyfur__bhz = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx)
                out_arr = pre_alloc_string_array(dyfur__bhz, -1)
                for i in numba.parfors.parfor.internal_prange(dyfur__bhz):
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
                dyfur__bhz = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(dyfur__bhz, -1)
                uzfxj__avyo = 0
                for i in numba.parfors.parfor.internal_prange(dyfur__bhz):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, uzfxj__avyo):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, uzfxj__avyo)
                        else:
                            out_arr[i] = str(val[uzfxj__avyo])
                        uzfxj__avyo += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(xxjqe__zid)
    raise BodoError(xxjqe__zid)


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
    ziy__vvst = parse_dtype(dtype, 'StringArray.astype')
    if A == ziy__vvst:
        return lambda A, dtype, copy=True: A
    if not isinstance(ziy__vvst, (types.Float, types.Integer)
        ) and ziy__vvst not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype, bodo.dict_str_arr_type):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(ziy__vvst, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            dyfur__bhz = len(A)
            B = np.empty(dyfur__bhz, ziy__vvst)
            for i in numba.parfors.parfor.internal_prange(dyfur__bhz):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif ziy__vvst == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            dyfur__bhz = len(A)
            B = np.empty(dyfur__bhz, ziy__vvst)
            for i in numba.parfors.parfor.internal_prange(dyfur__bhz):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif ziy__vvst == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            dyfur__bhz = len(A)
            B = np.empty(dyfur__bhz, ziy__vvst)
            for i in numba.parfors.parfor.internal_prange(dyfur__bhz):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif ziy__vvst == bodo.dict_str_arr_type:

        def impl_dict_str(A, dtype, copy=True):
            return str_arr_to_dict_str_arr(A)
        return impl_dict_str
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            dyfur__bhz = len(A)
            B = np.empty(dyfur__bhz, ziy__vvst)
            for i in numba.parfors.parfor.internal_prange(dyfur__bhz):
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
        fafga__hru = bodo.libs.array.array_to_info_codegen(context, builder,
            bodo.libs.array.array_info_type(sig.args[0]), (str_arr,), False)
        fqx__nqlb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        ukz__jbdt = cgutils.get_or_insert_function(builder.module,
            fqx__nqlb, name='str_to_dict_str_array')
        ahjg__cuj = builder.call(ukz__jbdt, [fafga__hru])
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        kxz__vysrg = bodo.libs.array.info_to_array_codegen(context, builder,
            sig.return_type(bodo.libs.array.array_info_type, sig.
            return_type), (ahjg__cuj, context.get_constant_null(sig.
            return_type)))
        return kxz__vysrg
    assert str_arr_t == bodo.string_array_type, 'str_arr_to_dict_str_arr: Input Array is not a Bodo String Array'
    sig = bodo.dict_str_arr_type(bodo.string_array_type)
    return sig, codegen


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        tpno__uwn, yjb__gze = args
        rsm__ctx = context.get_python_api(builder)
        lsex__zyawo = rsm__ctx.string_from_string_and_size(tpno__uwn, yjb__gze)
        pda__oom = rsm__ctx.to_native_value(string_type, lsex__zyawo).value
        zmwo__xarjb = cgutils.create_struct_proxy(string_type)(context,
            builder, pda__oom)
        zmwo__xarjb.hash = zmwo__xarjb.hash.type(-1)
        rsm__ctx.decref(lsex__zyawo)
        return zmwo__xarjb._getvalue()
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
        fxnwo__qzc, arr, ind, eqgo__itob = args
        puh__oay = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, puh__oay.
            offsets).data
        data = context.make_helper(builder, char_arr_type, puh__oay.data).data
        fqx__nqlb = lir.FunctionType(lir.IntType(32), [fxnwo__qzc.type, lir
            .IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        xqi__hmj = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            xqi__hmj = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        yqyoo__ghfm = cgutils.get_or_insert_function(builder.module,
            fqx__nqlb, xqi__hmj)
        return builder.call(yqyoo__ghfm, [fxnwo__qzc, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    foez__fvk = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    fqx__nqlb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer(), lir.IntType(32)])
    jzfzl__foso = cgutils.get_or_insert_function(c.builder.module,
        fqx__nqlb, name='string_array_from_sequence')
    rod__ymkvj = c.builder.call(jzfzl__foso, [val, foez__fvk])
    sxji__huyw = ArrayItemArrayType(char_arr_type)
    tyo__bwqt = c.context.make_helper(c.builder, sxji__huyw)
    tyo__bwqt.meminfo = rod__ymkvj
    sbxrs__ngbj = c.context.make_helper(c.builder, typ)
    nbm__opca = tyo__bwqt._getvalue()
    sbxrs__ngbj.data = nbm__opca
    pya__talf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(sbxrs__ngbj._getvalue(), is_error=pya__talf)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    dyfur__bhz = len(pyval)
    hbt__jux = 0
    rfqx__yoex = np.empty(dyfur__bhz + 1, np_offset_type)
    hvbt__gyq = []
    byrx__yrobo = np.empty(dyfur__bhz + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        rfqx__yoex[i] = hbt__jux
        cye__dutb = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(byrx__yrobo, i, int(not cye__dutb)
            )
        if cye__dutb:
            continue
        yzyqp__cdyzi = list(s.encode()) if isinstance(s, str) else list(s)
        hvbt__gyq.extend(yzyqp__cdyzi)
        hbt__jux += len(yzyqp__cdyzi)
    rfqx__yoex[dyfur__bhz] = hbt__jux
    amq__hsj = np.array(hvbt__gyq, np.uint8)
    qfn__diktj = context.get_constant(types.int64, dyfur__bhz)
    jxvgk__ofp = context.get_constant_generic(builder, char_arr_type, amq__hsj)
    dfzn__fazx = context.get_constant_generic(builder, offset_arr_type,
        rfqx__yoex)
    aaeh__gwev = context.get_constant_generic(builder, null_bitmap_arr_type,
        byrx__yrobo)
    puh__oay = lir.Constant.literal_struct([qfn__diktj, jxvgk__ofp,
        dfzn__fazx, aaeh__gwev])
    puh__oay = cgutils.global_constant(builder, '.const.payload', puh__oay
        ).bitcast(cgutils.voidptr_t)
    vgimj__tdpe = context.get_constant(types.int64, -1)
    uko__exxb = context.get_constant_null(types.voidptr)
    efvhe__tex = lir.Constant.literal_struct([vgimj__tdpe, uko__exxb,
        uko__exxb, puh__oay, vgimj__tdpe])
    efvhe__tex = cgutils.global_constant(builder, '.const.meminfo', efvhe__tex
        ).bitcast(cgutils.voidptr_t)
    nbm__opca = lir.Constant.literal_struct([efvhe__tex])
    sbxrs__ngbj = lir.Constant.literal_struct([nbm__opca])
    return sbxrs__ngbj


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
