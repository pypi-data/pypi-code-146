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
        echy__ztwq = ArrayItemArrayType(char_arr_type)
        htine__dzhbh = [('data', echy__ztwq)]
        models.StructModel.__init__(self, dmm, fe_type, htine__dzhbh)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        rqtx__zuwtg, = args
        pgsd__kzmd = context.make_helper(builder, string_array_type)
        pgsd__kzmd.data = rqtx__zuwtg
        context.nrt.incref(builder, data_typ, rqtx__zuwtg)
        return pgsd__kzmd._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    apgox__pfeuj = c.context.insert_const_string(c.builder.module, 'pandas')
    ogbt__szxxr = c.pyapi.import_module_noblock(apgox__pfeuj)
    kggu__tzuv = c.pyapi.call_method(ogbt__szxxr, 'StringDtype', ())
    c.pyapi.decref(ogbt__szxxr)
    return kggu__tzuv


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        cmasv__qajpx = bodo.libs.dict_arr_ext.get_binary_op_overload(op,
            lhs, rhs)
        if cmasv__qajpx is not None:
            return cmasv__qajpx
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                eazo__cboo = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(eazo__cboo)
                for i in numba.parfors.parfor.internal_prange(eazo__cboo):
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
                eazo__cboo = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(eazo__cboo)
                for i in numba.parfors.parfor.internal_prange(eazo__cboo):
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
                eazo__cboo = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(eazo__cboo)
                for i in numba.parfors.parfor.internal_prange(eazo__cboo):
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
    bsjva__citni = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    xfr__xtoz = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and xfr__xtoz or bsjva__citni and is_str_arr_type(
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
    kgwum__eko = context.make_helper(builder, arr_typ, arr_value)
    echy__ztwq = ArrayItemArrayType(char_arr_type)
    ntahi__arcwm = _get_array_item_arr_payload(context, builder, echy__ztwq,
        kgwum__eko.data)
    return ntahi__arcwm


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        return ntahi__arcwm.n_arrays
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
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        klyrs__hgtvf = context.make_helper(builder, offset_arr_type,
            ntahi__arcwm.offsets).data
        return _get_num_total_chars(builder, klyrs__hgtvf, ntahi__arcwm.
            n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        dlz__hgehc = context.make_helper(builder, offset_arr_type,
            ntahi__arcwm.offsets)
        xuzci__qmgct = context.make_helper(builder, offset_ctypes_type)
        xuzci__qmgct.data = builder.bitcast(dlz__hgehc.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        xuzci__qmgct.meminfo = dlz__hgehc.meminfo
        kggu__tzuv = xuzci__qmgct._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            kggu__tzuv)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        rqtx__zuwtg = context.make_helper(builder, char_arr_type,
            ntahi__arcwm.data)
        xuzci__qmgct = context.make_helper(builder, data_ctypes_type)
        xuzci__qmgct.data = rqtx__zuwtg.data
        xuzci__qmgct.meminfo = rqtx__zuwtg.meminfo
        kggu__tzuv = xuzci__qmgct._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, kggu__tzuv
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        nrkv__hxhwc, ind = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            nrkv__hxhwc, sig.args[0])
        rqtx__zuwtg = context.make_helper(builder, char_arr_type,
            ntahi__arcwm.data)
        xuzci__qmgct = context.make_helper(builder, data_ctypes_type)
        xuzci__qmgct.data = builder.gep(rqtx__zuwtg.data, [ind])
        xuzci__qmgct.meminfo = rqtx__zuwtg.meminfo
        kggu__tzuv = xuzci__qmgct._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, kggu__tzuv
            )
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        qfwgh__pzcrr, hvyct__uyv, ccxd__dzlj, iaakn__wjo = args
        wctuf__stdhu = builder.bitcast(builder.gep(qfwgh__pzcrr, [
            hvyct__uyv]), lir.IntType(8).as_pointer())
        uuvd__jttau = builder.bitcast(builder.gep(ccxd__dzlj, [iaakn__wjo]),
            lir.IntType(8).as_pointer())
        smx__mbcep = builder.load(uuvd__jttau)
        builder.store(smx__mbcep, wctuf__stdhu)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        fkv__tnbo = context.make_helper(builder, null_bitmap_arr_type,
            ntahi__arcwm.null_bitmap)
        xuzci__qmgct = context.make_helper(builder, data_ctypes_type)
        xuzci__qmgct.data = fkv__tnbo.data
        xuzci__qmgct.meminfo = fkv__tnbo.meminfo
        kggu__tzuv = xuzci__qmgct._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, kggu__tzuv
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        klyrs__hgtvf = context.make_helper(builder, offset_arr_type,
            ntahi__arcwm.offsets).data
        return builder.load(builder.gep(klyrs__hgtvf, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        offsets = context.make_helper(builder, offset_arr_type,
            ntahi__arcwm.offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        jbl__clpkn, ind = args
        if in_bitmap_typ == data_ctypes_type:
            xuzci__qmgct = context.make_helper(builder, data_ctypes_type,
                jbl__clpkn)
            jbl__clpkn = xuzci__qmgct.data
        return builder.load(builder.gep(jbl__clpkn, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        jbl__clpkn, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            xuzci__qmgct = context.make_helper(builder, data_ctypes_type,
                jbl__clpkn)
            jbl__clpkn = xuzci__qmgct.data
        builder.store(val, builder.gep(jbl__clpkn, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        nktqg__pjnk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        wycct__jjcnv = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        oowc__ofb = context.make_helper(builder, offset_arr_type,
            nktqg__pjnk.offsets).data
        szd__uzok = context.make_helper(builder, offset_arr_type,
            wycct__jjcnv.offsets).data
        tqm__ggew = context.make_helper(builder, char_arr_type, nktqg__pjnk
            .data).data
        apfm__zpiy = context.make_helper(builder, char_arr_type,
            wycct__jjcnv.data).data
        kaeas__ksol = context.make_helper(builder, null_bitmap_arr_type,
            nktqg__pjnk.null_bitmap).data
        kjugr__tgju = context.make_helper(builder, null_bitmap_arr_type,
            wycct__jjcnv.null_bitmap).data
        uvdmz__lua = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, szd__uzok, oowc__ofb, uvdmz__lua)
        cgutils.memcpy(builder, apfm__zpiy, tqm__ggew, builder.load(builder
            .gep(oowc__ofb, [ind])))
        kccp__dtd = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        fiair__vlbo = builder.lshr(kccp__dtd, lir.Constant(lir.IntType(64), 3))
        cgutils.memcpy(builder, kjugr__tgju, kaeas__ksol, fiair__vlbo)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        nktqg__pjnk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        wycct__jjcnv = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        oowc__ofb = context.make_helper(builder, offset_arr_type,
            nktqg__pjnk.offsets).data
        tqm__ggew = context.make_helper(builder, char_arr_type, nktqg__pjnk
            .data).data
        apfm__zpiy = context.make_helper(builder, char_arr_type,
            wycct__jjcnv.data).data
        num_total_chars = _get_num_total_chars(builder, oowc__ofb,
            nktqg__pjnk.n_arrays)
        cgutils.memcpy(builder, apfm__zpiy, tqm__ggew, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        nktqg__pjnk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        wycct__jjcnv = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        oowc__ofb = context.make_helper(builder, offset_arr_type,
            nktqg__pjnk.offsets).data
        szd__uzok = context.make_helper(builder, offset_arr_type,
            wycct__jjcnv.offsets).data
        kaeas__ksol = context.make_helper(builder, null_bitmap_arr_type,
            nktqg__pjnk.null_bitmap).data
        eazo__cboo = nktqg__pjnk.n_arrays
        rblwe__cqdix = context.get_constant(offset_type, 0)
        aid__jux = cgutils.alloca_once_value(builder, rblwe__cqdix)
        with cgutils.for_range(builder, eazo__cboo) as fqsc__kotr:
            fuvp__juva = lower_is_na(context, builder, kaeas__ksol,
                fqsc__kotr.index)
            with cgutils.if_likely(builder, builder.not_(fuvp__juva)):
                skar__lzgt = builder.load(builder.gep(oowc__ofb, [
                    fqsc__kotr.index]))
                vpkjt__nuog = builder.load(aid__jux)
                builder.store(skar__lzgt, builder.gep(szd__uzok, [vpkjt__nuog])
                    )
                builder.store(builder.add(vpkjt__nuog, lir.Constant(context
                    .get_value_type(offset_type), 1)), aid__jux)
        vpkjt__nuog = builder.load(aid__jux)
        skar__lzgt = builder.load(builder.gep(oowc__ofb, [eazo__cboo]))
        builder.store(skar__lzgt, builder.gep(szd__uzok, [vpkjt__nuog]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        cphg__nfyx, ind, str, bhl__xjb = args
        cphg__nfyx = context.make_array(sig.args[0])(context, builder,
            cphg__nfyx)
        zxwk__clsni = builder.gep(cphg__nfyx.data, [ind])
        cgutils.raw_memcpy(builder, zxwk__clsni, str, bhl__xjb, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        zxwk__clsni, ind, nteod__ftmdd, bhl__xjb = args
        zxwk__clsni = builder.gep(zxwk__clsni, [ind])
        cgutils.raw_memcpy(builder, zxwk__clsni, nteod__ftmdd, bhl__xjb, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.generated_jit(nopython=True)
def get_str_arr_item_length(A, i):
    if A == bodo.dict_str_arr_type:

        def impl(A, i):
            idx = A._indices[i]
            aldgn__bdfg = A._data
            return np.int64(getitem_str_offset(aldgn__bdfg, idx + 1) -
                getitem_str_offset(aldgn__bdfg, idx))
        return impl
    else:
        return lambda A, i: np.int64(getitem_str_offset(A, i + 1) -
            getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    nkidv__sjlbz = np.int64(getitem_str_offset(A, i))
    vtg__hne = np.int64(getitem_str_offset(A, i + 1))
    l = vtg__hne - nkidv__sjlbz
    lbdv__zri = get_data_ptr_ind(A, nkidv__sjlbz)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(lbdv__zri, j) >= 128:
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
        msfh__yte = 'in_str_arr = A._data'
        lzsje__xrilo = 'input_index = A._indices[i]'
    else:
        msfh__yte = 'in_str_arr = A'
        lzsje__xrilo = 'input_index = i'
    euz__vpzo = f"""def impl(B, j, A, i):
        if j == 0:
            setitem_str_offset(B, 0, 0)

        {msfh__yte}
        {lzsje__xrilo}

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
    ahl__dgv = {}
    exec(euz__vpzo, {'setitem_str_offset': setitem_str_offset,
        'memcpy_region': memcpy_region, 'getitem_str_offset':
        getitem_str_offset, 'str_arr_set_na': str_arr_set_na,
        'str_arr_set_not_na': str_arr_set_not_na, 'get_data_ptr':
        get_data_ptr, 'bodo': bodo, 'np': np}, ahl__dgv)
    impl = ahl__dgv['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    eazo__cboo = len(str_arr)
    zmwu__xci = np.empty(eazo__cboo, np.bool_)
    for i in range(eazo__cboo):
        zmwu__xci[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return zmwu__xci


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            eazo__cboo = len(data)
            l = []
            for i in range(eazo__cboo):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        noq__sowv = data.count
        iulog__hjo = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(noq__sowv)]
        if is_overload_true(str_null_bools):
            iulog__hjo += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(noq__sowv) if is_str_arr_type(data.types[i]) or data.
                types[i] == binary_array_type]
        euz__vpzo = 'def f(data, str_null_bools=None):\n'
        euz__vpzo += '  return ({}{})\n'.format(', '.join(iulog__hjo), ',' if
            noq__sowv == 1 else '')
        ahl__dgv = {}
        exec(euz__vpzo, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, ahl__dgv)
        coxsq__qaavu = ahl__dgv['f']
        return coxsq__qaavu
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                eazo__cboo = len(list_data)
                for i in range(eazo__cboo):
                    nteod__ftmdd = list_data[i]
                    str_arr[i] = nteod__ftmdd
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                eazo__cboo = len(list_data)
                for i in range(eazo__cboo):
                    nteod__ftmdd = list_data[i]
                    str_arr[i] = nteod__ftmdd
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        noq__sowv = str_arr.count
        mguy__oxqa = 0
        euz__vpzo = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(noq__sowv):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                euz__vpzo += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])\n'
                    .format(i, i, noq__sowv + mguy__oxqa))
                mguy__oxqa += 1
            else:
                euz__vpzo += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        euz__vpzo += '  return\n'
        ahl__dgv = {}
        exec(euz__vpzo, {'cp_str_list_to_array': cp_str_list_to_array},
            ahl__dgv)
        impf__uyde = ahl__dgv['f']
        return impf__uyde
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            eazo__cboo = len(str_list)
            str_arr = pre_alloc_string_array(eazo__cboo, -1)
            for i in range(eazo__cboo):
                nteod__ftmdd = str_list[i]
                str_arr[i] = nteod__ftmdd
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            eazo__cboo = len(A)
            wtl__rtj = 0
            for i in range(eazo__cboo):
                nteod__ftmdd = A[i]
                wtl__rtj += get_utf8_size(nteod__ftmdd)
            return wtl__rtj
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        eazo__cboo = len(arr)
        n_chars = num_total_chars(arr)
        zfx__hng = pre_alloc_string_array(eazo__cboo, np.int64(n_chars))
        copy_str_arr_slice(zfx__hng, arr, eazo__cboo)
        return zfx__hng
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
    euz__vpzo = 'def f(in_seq):\n'
    euz__vpzo += '    n_strs = len(in_seq)\n'
    euz__vpzo += '    A = pre_alloc_string_array(n_strs, -1)\n'
    euz__vpzo += '    return A\n'
    ahl__dgv = {}
    exec(euz__vpzo, {'pre_alloc_string_array': pre_alloc_string_array},
        ahl__dgv)
    cycf__rfd = ahl__dgv['f']
    return cycf__rfd


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        hql__rcqzn = 'pre_alloc_binary_array'
    else:
        hql__rcqzn = 'pre_alloc_string_array'
    euz__vpzo = 'def f(in_seq):\n'
    euz__vpzo += '    n_strs = len(in_seq)\n'
    euz__vpzo += f'    A = {hql__rcqzn}(n_strs, -1)\n'
    euz__vpzo += '    for i in range(n_strs):\n'
    euz__vpzo += '        A[i] = in_seq[i]\n'
    euz__vpzo += '    return A\n'
    ahl__dgv = {}
    exec(euz__vpzo, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, ahl__dgv)
    cycf__rfd = ahl__dgv['f']
    return cycf__rfd


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        pwox__ergl = builder.add(ntahi__arcwm.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        rxvqt__idcjk = builder.lshr(lir.Constant(lir.IntType(64),
            offset_type.bitwidth), lir.Constant(lir.IntType(64), 3))
        fiair__vlbo = builder.mul(pwox__ergl, rxvqt__idcjk)
        hepbp__uwu = context.make_array(offset_arr_type)(context, builder,
            ntahi__arcwm.offsets).data
        cgutils.memset(builder, hepbp__uwu, fiair__vlbo, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        mamk__zcttd = ntahi__arcwm.n_arrays
        fiair__vlbo = builder.lshr(builder.add(mamk__zcttd, lir.Constant(
            lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        jhnbo__zbivy = context.make_array(null_bitmap_arr_type)(context,
            builder, ntahi__arcwm.null_bitmap).data
        cgutils.memset(builder, jhnbo__zbivy, fiair__vlbo, 0)
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
    bbhtc__nxqrf = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        ktee__cks = len(len_arr)
        for i in range(ktee__cks):
            offsets[i] = bbhtc__nxqrf
            bbhtc__nxqrf += len_arr[i]
        offsets[ktee__cks] = bbhtc__nxqrf
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    ikba__vzxwb = i // 8
    weyk__gyc = getitem_str_bitmap(bits, ikba__vzxwb)
    weyk__gyc ^= np.uint8(-np.uint8(bit_is_set) ^ weyk__gyc) & kBitmask[i % 8]
    setitem_str_bitmap(bits, ikba__vzxwb, weyk__gyc)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    uard__ggd = get_null_bitmap_ptr(out_str_arr)
    wmm__gfiii = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        qyh__zmp = get_bit_bitmap(wmm__gfiii, j)
        set_bit_to(uard__ggd, out_start + j, qyh__zmp)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, nrkv__hxhwc, muq__dhtay, innd__ptpe = args
        nktqg__pjnk = _get_str_binary_arr_payload(context, builder,
            nrkv__hxhwc, string_array_type)
        wycct__jjcnv = _get_str_binary_arr_payload(context, builder,
            out_arr, string_array_type)
        oowc__ofb = context.make_helper(builder, offset_arr_type,
            nktqg__pjnk.offsets).data
        szd__uzok = context.make_helper(builder, offset_arr_type,
            wycct__jjcnv.offsets).data
        tqm__ggew = context.make_helper(builder, char_arr_type, nktqg__pjnk
            .data).data
        apfm__zpiy = context.make_helper(builder, char_arr_type,
            wycct__jjcnv.data).data
        num_total_chars = _get_num_total_chars(builder, oowc__ofb,
            nktqg__pjnk.n_arrays)
        pgt__sengu = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        xgl__ibc = cgutils.get_or_insert_function(builder.module,
            pgt__sengu, name='set_string_array_range')
        builder.call(xgl__ibc, [szd__uzok, apfm__zpiy, oowc__ofb, tqm__ggew,
            muq__dhtay, innd__ptpe, nktqg__pjnk.n_arrays, num_total_chars])
        yel__rry = context.typing_context.resolve_value_type(copy_nulls_range)
        pdw__gmw = yel__rry.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        hoa__jhm = context.get_function(yel__rry, pdw__gmw)
        hoa__jhm(builder, (out_arr, nrkv__hxhwc, muq__dhtay))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    huke__mmcib = c.context.make_helper(c.builder, typ, val)
    echy__ztwq = ArrayItemArrayType(char_arr_type)
    ntahi__arcwm = _get_array_item_arr_payload(c.context, c.builder,
        echy__ztwq, huke__mmcib.data)
    ijwa__vuhts = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    xfwzy__twnlv = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        xfwzy__twnlv = 'pd_array_from_string_array'
    if use_pd_pyarrow_string_array and typ != binary_array_type:
        from bodo.libs.array import array_info_type, array_to_info_codegen
        yzmh__reg = array_to_info_codegen(c.context, c.builder,
            array_info_type(typ), (val,), incref=False)
        pgt__sengu = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
            as_pointer()])
        xfwzy__twnlv = 'pd_pyarrow_array_from_string_array'
        pts__xfo = cgutils.get_or_insert_function(c.builder.module,
            pgt__sengu, name=xfwzy__twnlv)
        arr = c.builder.call(pts__xfo, [yzmh__reg])
        c.context.nrt.decref(c.builder, typ, val)
        return arr
    pgt__sengu = lir.FunctionType(c.context.get_argument_type(types.
        pyobject), [lir.IntType(64), lir.IntType(offset_type.bitwidth).
        as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
        as_pointer(), lir.IntType(32)])
    pts__xfo = cgutils.get_or_insert_function(c.builder.module, pgt__sengu,
        name=xfwzy__twnlv)
    klyrs__hgtvf = c.context.make_array(offset_arr_type)(c.context, c.
        builder, ntahi__arcwm.offsets).data
    lbdv__zri = c.context.make_array(char_arr_type)(c.context, c.builder,
        ntahi__arcwm.data).data
    jhnbo__zbivy = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, ntahi__arcwm.null_bitmap).data
    arr = c.builder.call(pts__xfo, [ntahi__arcwm.n_arrays, klyrs__hgtvf,
        lbdv__zri, jhnbo__zbivy, ijwa__vuhts])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in (string_array_type, binary_array_type
        ), 'str_arr_is_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        jhnbo__zbivy = context.make_array(null_bitmap_arr_type)(context,
            builder, ntahi__arcwm.null_bitmap).data
        webo__iykx = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        ijka__geun = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        weyk__gyc = builder.load(builder.gep(jhnbo__zbivy, [webo__iykx],
            inbounds=True))
        qapu__wne = lir.ArrayType(lir.IntType(8), 8)
        lkhhb__whfhd = cgutils.alloca_once_value(builder, lir.Constant(
            qapu__wne, (1, 2, 4, 8, 16, 32, 64, 128)))
        jqapk__owgcv = builder.load(builder.gep(lkhhb__whfhd, [lir.Constant
            (lir.IntType(64), 0), ijka__geun], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(weyk__gyc,
            jqapk__owgcv), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [string_array_type, binary_array_type
        ], 'str_arr_set_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        webo__iykx = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        ijka__geun = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        jhnbo__zbivy = context.make_array(null_bitmap_arr_type)(context,
            builder, ntahi__arcwm.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type,
            ntahi__arcwm.offsets).data
        kota__ifvn = builder.gep(jhnbo__zbivy, [webo__iykx], inbounds=True)
        weyk__gyc = builder.load(kota__ifvn)
        qapu__wne = lir.ArrayType(lir.IntType(8), 8)
        lkhhb__whfhd = cgutils.alloca_once_value(builder, lir.Constant(
            qapu__wne, (1, 2, 4, 8, 16, 32, 64, 128)))
        jqapk__owgcv = builder.load(builder.gep(lkhhb__whfhd, [lir.Constant
            (lir.IntType(64), 0), ijka__geun], inbounds=True))
        jqapk__owgcv = builder.xor(jqapk__owgcv, lir.Constant(lir.IntType(8
            ), -1))
        builder.store(builder.and_(weyk__gyc, jqapk__owgcv), kota__ifvn)
        xbwja__ahf = builder.add(ind, lir.Constant(lir.IntType(64), 1))
        blczv__ttepm = builder.icmp_unsigned('!=', xbwja__ahf, ntahi__arcwm
            .n_arrays)
        with builder.if_then(blczv__ttepm):
            builder.store(builder.load(builder.gep(offsets, [ind])),
                builder.gep(offsets, [xbwja__ahf]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [binary_array_type, string_array_type
        ], 'str_arr_set_not_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        webo__iykx = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        ijka__geun = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        jhnbo__zbivy = context.make_array(null_bitmap_arr_type)(context,
            builder, ntahi__arcwm.null_bitmap).data
        kota__ifvn = builder.gep(jhnbo__zbivy, [webo__iykx], inbounds=True)
        weyk__gyc = builder.load(kota__ifvn)
        qapu__wne = lir.ArrayType(lir.IntType(8), 8)
        lkhhb__whfhd = cgutils.alloca_once_value(builder, lir.Constant(
            qapu__wne, (1, 2, 4, 8, 16, 32, 64, 128)))
        jqapk__owgcv = builder.load(builder.gep(lkhhb__whfhd, [lir.Constant
            (lir.IntType(64), 0), ijka__geun], inbounds=True))
        builder.store(builder.or_(weyk__gyc, jqapk__owgcv), kota__ifvn)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        fiair__vlbo = builder.udiv(builder.add(ntahi__arcwm.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        jhnbo__zbivy = context.make_array(null_bitmap_arr_type)(context,
            builder, ntahi__arcwm.null_bitmap).data
        cgutils.memset(builder, jhnbo__zbivy, fiair__vlbo, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    ynqp__wrnf = context.make_helper(builder, string_array_type, str_arr)
    echy__ztwq = ArrayItemArrayType(char_arr_type)
    gth__dgomk = context.make_helper(builder, echy__ztwq, ynqp__wrnf.data)
    fzp__lwdsf = ArrayItemArrayPayloadType(echy__ztwq)
    cvnr__njtto = context.nrt.meminfo_data(builder, gth__dgomk.meminfo)
    btq__csnp = builder.bitcast(cvnr__njtto, context.get_value_type(
        fzp__lwdsf).as_pointer())
    return btq__csnp


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        lsomd__mbt, sfaoq__yvz = args
        uvbnt__yywys = _get_str_binary_arr_data_payload_ptr(context,
            builder, sfaoq__yvz)
        ogh__ylv = _get_str_binary_arr_data_payload_ptr(context, builder,
            lsomd__mbt)
        eckl__ttum = _get_str_binary_arr_payload(context, builder,
            sfaoq__yvz, sig.args[1])
        utnfz__okjoc = _get_str_binary_arr_payload(context, builder,
            lsomd__mbt, sig.args[0])
        context.nrt.incref(builder, char_arr_type, eckl__ttum.data)
        context.nrt.incref(builder, offset_arr_type, eckl__ttum.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, eckl__ttum.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, utnfz__okjoc.data)
        context.nrt.decref(builder, offset_arr_type, utnfz__okjoc.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, utnfz__okjoc.
            null_bitmap)
        builder.store(builder.load(uvbnt__yywys), ogh__ylv)
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
        eazo__cboo = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return eazo__cboo
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, zxwk__clsni, vefwj__nvas = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder, arr,
            sig.args[0])
        offsets = context.make_helper(builder, offset_arr_type,
            ntahi__arcwm.offsets).data
        data = context.make_helper(builder, char_arr_type, ntahi__arcwm.data
            ).data
        pgt__sengu = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        prd__fhyk = cgutils.get_or_insert_function(builder.module,
            pgt__sengu, name='setitem_string_array')
        srkpb__ihsbk = context.get_constant(types.int32, -1)
        jzz__ovnda = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets,
            ntahi__arcwm.n_arrays)
        builder.call(prd__fhyk, [offsets, data, num_total_chars, builder.
            extract_value(zxwk__clsni, 0), vefwj__nvas, srkpb__ihsbk,
            jzz__ovnda, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    pgt__sengu = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64)])
    juqg__zcch = cgutils.get_or_insert_function(builder.module, pgt__sengu,
        name='is_na')
    return builder.call(juqg__zcch, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        wctuf__stdhu, uuvd__jttau, noq__sowv, uwb__bcvii = args
        cgutils.raw_memcpy(builder, wctuf__stdhu, uuvd__jttau, noq__sowv,
            uwb__bcvii)
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
        phw__zrte, hshm__qqum = unicode_to_utf8_and_len(val)
        elpk__zrpgt = getitem_str_offset(A, ind)
        bhrwc__qybc = getitem_str_offset(A, ind + 1)
        ehihg__vcda = bhrwc__qybc - elpk__zrpgt
        if ehihg__vcda != hshm__qqum:
            return False
        zxwk__clsni = get_data_ptr_ind(A, elpk__zrpgt)
        return memcmp(zxwk__clsni, phw__zrte, hshm__qqum) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        elpk__zrpgt = getitem_str_offset(A, ind)
        ehihg__vcda = bodo.libs.str_ext.int_to_str_len(val)
        nulf__dlzyo = elpk__zrpgt + ehihg__vcda
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            elpk__zrpgt, nulf__dlzyo)
        zxwk__clsni = get_data_ptr_ind(A, elpk__zrpgt)
        inplace_int64_to_str(zxwk__clsni, ehihg__vcda, val)
        setitem_str_offset(A, ind + 1, elpk__zrpgt + ehihg__vcda)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        zxwk__clsni, = args
        wabnf__wyz = context.insert_const_string(builder.module, '<NA>')
        uae__bvz = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, zxwk__clsni, wabnf__wyz, uae__bvz, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    nhylt__gnsvz = len('<NA>')

    def impl(A, ind):
        elpk__zrpgt = getitem_str_offset(A, ind)
        nulf__dlzyo = elpk__zrpgt + nhylt__gnsvz
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            elpk__zrpgt, nulf__dlzyo)
        zxwk__clsni = get_data_ptr_ind(A, elpk__zrpgt)
        inplace_set_NA_str(zxwk__clsni)
        setitem_str_offset(A, ind + 1, elpk__zrpgt + nhylt__gnsvz)
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
            elpk__zrpgt = getitem_str_offset(A, ind)
            bhrwc__qybc = getitem_str_offset(A, ind + 1)
            vefwj__nvas = bhrwc__qybc - elpk__zrpgt
            zxwk__clsni = get_data_ptr_ind(A, elpk__zrpgt)
            pus__lhfzq = decode_utf8(zxwk__clsni, vefwj__nvas)
            return pus__lhfzq
        return str_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            eazo__cboo = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(eazo__cboo):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            caxdu__sgk = get_data_ptr(out_arr).data
            neym__eic = get_data_ptr(A).data
            mguy__oxqa = 0
            vpkjt__nuog = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(eazo__cboo):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    tmg__pqkt = get_str_arr_item_length(A, i)
                    if tmg__pqkt == 0:
                        pass
                    elif tmg__pqkt == 1:
                        copy_single_char(caxdu__sgk, vpkjt__nuog, neym__eic,
                            getitem_str_offset(A, i))
                    else:
                        memcpy_region(caxdu__sgk, vpkjt__nuog, neym__eic,
                            getitem_str_offset(A, i), tmg__pqkt, 1)
                    vpkjt__nuog += tmg__pqkt
                    setitem_str_offset(out_arr, mguy__oxqa + 1, vpkjt__nuog)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, mguy__oxqa)
                    else:
                        str_arr_set_not_na(out_arr, mguy__oxqa)
                    mguy__oxqa += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            eazo__cboo = len(ind)
            n_chars = 0
            for i in range(eazo__cboo):
                n_chars += get_str_arr_item_length(A, ind[i])
            out_arr = pre_alloc_string_array(eazo__cboo, n_chars)
            caxdu__sgk = get_data_ptr(out_arr).data
            neym__eic = get_data_ptr(A).data
            vpkjt__nuog = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(eazo__cboo):
                if bodo.libs.array_kernels.isna(ind, i):
                    raise ValueError(
                        'Cannot index with an integer indexer containing NA values'
                        )
                qwjfe__mpjwt = ind[i]
                tmg__pqkt = get_str_arr_item_length(A, qwjfe__mpjwt)
                if tmg__pqkt == 0:
                    pass
                elif tmg__pqkt == 1:
                    copy_single_char(caxdu__sgk, vpkjt__nuog, neym__eic,
                        getitem_str_offset(A, qwjfe__mpjwt))
                else:
                    memcpy_region(caxdu__sgk, vpkjt__nuog, neym__eic,
                        getitem_str_offset(A, qwjfe__mpjwt), tmg__pqkt, 1)
                vpkjt__nuog += tmg__pqkt
                setitem_str_offset(out_arr, i + 1, vpkjt__nuog)
                if str_arr_is_na(A, qwjfe__mpjwt):
                    str_arr_set_na(out_arr, i)
                else:
                    str_arr_set_not_na(out_arr, i)
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            eazo__cboo = len(A)
            wye__doae = numba.cpython.unicode._normalize_slice(ind, eazo__cboo)
            togi__ozkpc = numba.cpython.unicode._slice_span(wye__doae)
            if wye__doae.step == 1:
                elpk__zrpgt = getitem_str_offset(A, wye__doae.start)
                bhrwc__qybc = getitem_str_offset(A, wye__doae.stop)
                n_chars = bhrwc__qybc - elpk__zrpgt
                zfx__hng = pre_alloc_string_array(togi__ozkpc, np.int64(
                    n_chars))
                for i in range(togi__ozkpc):
                    zfx__hng[i] = A[wye__doae.start + i]
                    if str_arr_is_na(A, wye__doae.start + i):
                        str_arr_set_na(zfx__hng, i)
                return zfx__hng
            else:
                zfx__hng = pre_alloc_string_array(togi__ozkpc, -1)
                for i in range(togi__ozkpc):
                    zfx__hng[i] = A[wye__doae.start + i * wye__doae.step]
                    if str_arr_is_na(A, wye__doae.start + i * wye__doae.step):
                        str_arr_set_na(zfx__hng, i)
                return zfx__hng
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
    uxf__aanoz = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(uxf__aanoz)
        aagum__fwko = 4

        def impl_scalar(A, idx, val):
            uofab__pdud = (val._length if val._is_ascii else aagum__fwko *
                val._length)
            rqtx__zuwtg = A._data
            elpk__zrpgt = np.int64(getitem_str_offset(A, idx))
            nulf__dlzyo = elpk__zrpgt + uofab__pdud
            bodo.libs.array_item_arr_ext.ensure_data_capacity(rqtx__zuwtg,
                elpk__zrpgt, nulf__dlzyo)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                nulf__dlzyo, val._data, val._length, val._kind, val.
                _is_ascii, idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                wye__doae = numba.cpython.unicode._normalize_slice(idx, len(A))
                nkidv__sjlbz = wye__doae.start
                rqtx__zuwtg = A._data
                elpk__zrpgt = np.int64(getitem_str_offset(A, nkidv__sjlbz))
                nulf__dlzyo = elpk__zrpgt + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(rqtx__zuwtg,
                    elpk__zrpgt, nulf__dlzyo)
                set_string_array_range(A, val, nkidv__sjlbz, elpk__zrpgt)
                kena__myrfu = 0
                for i in range(wye__doae.start, wye__doae.stop, wye__doae.step
                    ):
                    if str_arr_is_na(val, kena__myrfu):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    kena__myrfu += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                uxe__rxyv = str_list_to_array(val)
                A[idx] = uxe__rxyv
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                wye__doae = numba.cpython.unicode._normalize_slice(idx, len(A))
                for i in range(wye__doae.start, wye__doae.stop, wye__doae.step
                    ):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(uxf__aanoz)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                eazo__cboo = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx)
                out_arr = pre_alloc_string_array(eazo__cboo, -1)
                for i in numba.parfors.parfor.internal_prange(eazo__cboo):
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
                eazo__cboo = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(eazo__cboo, -1)
                tlvv__fnyg = 0
                for i in numba.parfors.parfor.internal_prange(eazo__cboo):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, tlvv__fnyg):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, tlvv__fnyg)
                        else:
                            out_arr[i] = str(val[tlvv__fnyg])
                        tlvv__fnyg += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(uxf__aanoz)
    raise BodoError(uxf__aanoz)


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
    atg__yhgb = parse_dtype(dtype, 'StringArray.astype')
    if A == atg__yhgb:
        return lambda A, dtype, copy=True: A
    if not isinstance(atg__yhgb, (types.Float, types.Integer)
        ) and atg__yhgb not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype, bodo.dict_str_arr_type):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(atg__yhgb, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            eazo__cboo = len(A)
            B = np.empty(eazo__cboo, atg__yhgb)
            for i in numba.parfors.parfor.internal_prange(eazo__cboo):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif atg__yhgb == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            eazo__cboo = len(A)
            B = np.empty(eazo__cboo, atg__yhgb)
            for i in numba.parfors.parfor.internal_prange(eazo__cboo):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif atg__yhgb == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            eazo__cboo = len(A)
            B = np.empty(eazo__cboo, atg__yhgb)
            for i in numba.parfors.parfor.internal_prange(eazo__cboo):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif atg__yhgb == bodo.dict_str_arr_type:

        def impl_dict_str(A, dtype, copy=True):
            return str_arr_to_dict_str_arr(A)
        return impl_dict_str
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            eazo__cboo = len(A)
            B = np.empty(eazo__cboo, atg__yhgb)
            for i in numba.parfors.parfor.internal_prange(eazo__cboo):
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
        ohytu__jme = bodo.libs.array.array_to_info_codegen(context, builder,
            bodo.libs.array.array_info_type(sig.args[0]), (str_arr,), False)
        pgt__sengu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        yitw__atvn = cgutils.get_or_insert_function(builder.module,
            pgt__sengu, name='str_to_dict_str_array')
        bnc__yaw = builder.call(yitw__atvn, [ohytu__jme])
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        aldgn__bdfg = bodo.libs.array.info_to_array_codegen(context,
            builder, sig.return_type(bodo.libs.array.array_info_type, sig.
            return_type), (bnc__yaw, context.get_constant_null(sig.
            return_type)))
        return aldgn__bdfg
    assert str_arr_t == bodo.string_array_type, 'str_arr_to_dict_str_arr: Input Array is not a Bodo String Array'
    sig = bodo.dict_str_arr_type(bodo.string_array_type)
    return sig, codegen


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        zxwk__clsni, vefwj__nvas = args
        faqa__oou = context.get_python_api(builder)
        zkxf__uvd = faqa__oou.string_from_string_and_size(zxwk__clsni,
            vefwj__nvas)
        vxwb__obc = faqa__oou.to_native_value(string_type, zkxf__uvd).value
        oast__xkah = cgutils.create_struct_proxy(string_type)(context,
            builder, vxwb__obc)
        oast__xkah.hash = oast__xkah.hash.type(-1)
        faqa__oou.decref(zkxf__uvd)
        return oast__xkah._getvalue()
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
        oklsp__hesk, arr, ind, bjyox__mwrpg = args
        ntahi__arcwm = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type,
            ntahi__arcwm.offsets).data
        data = context.make_helper(builder, char_arr_type, ntahi__arcwm.data
            ).data
        pgt__sengu = lir.FunctionType(lir.IntType(32), [oklsp__hesk.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        exich__qaei = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            exich__qaei = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        webt__egald = cgutils.get_or_insert_function(builder.module,
            pgt__sengu, exich__qaei)
        return builder.call(webt__egald, [oklsp__hesk, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    ijwa__vuhts = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    pgt__sengu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType
        (8).as_pointer(), lir.IntType(32)])
    pevbo__rew = cgutils.get_or_insert_function(c.builder.module,
        pgt__sengu, name='string_array_from_sequence')
    pouwz__wlii = c.builder.call(pevbo__rew, [val, ijwa__vuhts])
    echy__ztwq = ArrayItemArrayType(char_arr_type)
    gth__dgomk = c.context.make_helper(c.builder, echy__ztwq)
    gth__dgomk.meminfo = pouwz__wlii
    ynqp__wrnf = c.context.make_helper(c.builder, typ)
    rqtx__zuwtg = gth__dgomk._getvalue()
    ynqp__wrnf.data = rqtx__zuwtg
    gim__ptjv = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ynqp__wrnf._getvalue(), is_error=gim__ptjv)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    eazo__cboo = len(pyval)
    vpkjt__nuog = 0
    akc__kzds = np.empty(eazo__cboo + 1, np_offset_type)
    xiz__sexg = []
    snsf__vft = np.empty(eazo__cboo + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        akc__kzds[i] = vpkjt__nuog
        rxayp__iyeh = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(snsf__vft, i, int(not rxayp__iyeh)
            )
        if rxayp__iyeh:
            continue
        ayq__iozm = list(s.encode()) if isinstance(s, str) else list(s)
        xiz__sexg.extend(ayq__iozm)
        vpkjt__nuog += len(ayq__iozm)
    akc__kzds[eazo__cboo] = vpkjt__nuog
    esw__vdn = np.array(xiz__sexg, np.uint8)
    wkxsh__bjl = context.get_constant(types.int64, eazo__cboo)
    wcnre__vsj = context.get_constant_generic(builder, char_arr_type, esw__vdn)
    euuft__jowtz = context.get_constant_generic(builder, offset_arr_type,
        akc__kzds)
    uyz__knwyi = context.get_constant_generic(builder, null_bitmap_arr_type,
        snsf__vft)
    ntahi__arcwm = lir.Constant.literal_struct([wkxsh__bjl, wcnre__vsj,
        euuft__jowtz, uyz__knwyi])
    ntahi__arcwm = cgutils.global_constant(builder, '.const.payload',
        ntahi__arcwm).bitcast(cgutils.voidptr_t)
    ezvk__ridyi = context.get_constant(types.int64, -1)
    xfs__ktw = context.get_constant_null(types.voidptr)
    dznmj__lsx = lir.Constant.literal_struct([ezvk__ridyi, xfs__ktw,
        xfs__ktw, ntahi__arcwm, ezvk__ridyi])
    dznmj__lsx = cgutils.global_constant(builder, '.const.meminfo', dznmj__lsx
        ).bitcast(cgutils.voidptr_t)
    rqtx__zuwtg = lir.Constant.literal_struct([dznmj__lsx])
    ynqp__wrnf = lir.Constant.literal_struct([rqtx__zuwtg])
    return ynqp__wrnf


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
