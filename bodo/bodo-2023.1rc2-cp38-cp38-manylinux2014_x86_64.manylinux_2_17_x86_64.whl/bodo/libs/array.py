"""Tools for handling bodo arrays, e.g. passing to C/C++ code
"""
from collections import defaultdict
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_cast
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import intrinsic, models, register_model
from numba.np.arrayobj import _getitem_array_single_int
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, get_categories_int_type
from bodo.hiframes.time_ext import TimeArrayType, TimeType
from bodo.libs import array_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, define_array_item_dtor, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType, int128_type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType, _get_map_arr_data_type, init_map_arr_codegen
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, char_arr_type, null_bitmap_arr_type, offset_arr_type, string_array_type
from bodo.libs.struct_arr_ext import StructArrayPayloadType, StructArrayType, StructType, _get_struct_arr_payload, define_struct_arr_dtor
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, get_overload_const_int, is_overload_none, is_str_arr_type, raise_bodo_error, type_has_unknown_cats, unwrap_typeref
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, numba_to_c_type
ll.add_symbol('list_string_array_to_info', array_ext.list_string_array_to_info)
ll.add_symbol('nested_array_to_info', array_ext.nested_array_to_info)
ll.add_symbol('string_array_to_info', array_ext.string_array_to_info)
ll.add_symbol('dict_str_array_to_info', array_ext.dict_str_array_to_info)
ll.add_symbol('get_nested_info', array_ext.get_nested_info)
ll.add_symbol('get_has_global_dictionary', array_ext.get_has_global_dictionary)
ll.add_symbol('get_has_deduped_local_dictionary', array_ext.
    get_has_deduped_local_dictionary)
ll.add_symbol('numpy_array_to_info', array_ext.numpy_array_to_info)
ll.add_symbol('categorical_array_to_info', array_ext.categorical_array_to_info)
ll.add_symbol('nullable_array_to_info', array_ext.nullable_array_to_info)
ll.add_symbol('interval_array_to_info', array_ext.interval_array_to_info)
ll.add_symbol('decimal_array_to_info', array_ext.decimal_array_to_info)
ll.add_symbol('time_array_to_info', array_ext.time_array_to_info)
ll.add_symbol('info_to_nested_array', array_ext.info_to_nested_array)
ll.add_symbol('info_to_list_string_array', array_ext.info_to_list_string_array)
ll.add_symbol('info_to_string_array', array_ext.info_to_string_array)
ll.add_symbol('info_to_numpy_array', array_ext.info_to_numpy_array)
ll.add_symbol('info_to_nullable_array', array_ext.info_to_nullable_array)
ll.add_symbol('info_to_interval_array', array_ext.info_to_interval_array)
ll.add_symbol('alloc_numpy', array_ext.alloc_numpy)
ll.add_symbol('alloc_string_array', array_ext.alloc_string_array)
ll.add_symbol('arr_info_list_to_table', array_ext.arr_info_list_to_table)
ll.add_symbol('info_from_table', array_ext.info_from_table)
ll.add_symbol('delete_info_decref_array', array_ext.delete_info_decref_array)
ll.add_symbol('delete_table_decref_arrays', array_ext.
    delete_table_decref_arrays)
ll.add_symbol('decref_table_array', array_ext.decref_table_array)
ll.add_symbol('delete_table', array_ext.delete_table)
ll.add_symbol('shuffle_table', array_ext.shuffle_table)
ll.add_symbol('get_shuffle_info', array_ext.get_shuffle_info)
ll.add_symbol('delete_shuffle_info', array_ext.delete_shuffle_info)
ll.add_symbol('reverse_shuffle_table', array_ext.reverse_shuffle_table)
ll.add_symbol('hash_join_table', array_ext.hash_join_table)
ll.add_symbol('cross_join_table', array_ext.cross_join_table)
ll.add_symbol('drop_duplicates_table', array_ext.drop_duplicates_table)
ll.add_symbol('sort_values_table', array_ext.sort_values_table)
ll.add_symbol('sample_table', array_ext.sample_table)
ll.add_symbol('shuffle_renormalization', array_ext.shuffle_renormalization)
ll.add_symbol('shuffle_renormalization_group', array_ext.
    shuffle_renormalization_group)
ll.add_symbol('groupby_and_aggregate', array_ext.groupby_and_aggregate)
ll.add_symbol('convert_local_dictionary_to_global', array_ext.
    convert_local_dictionary_to_global)
ll.add_symbol('drop_duplicates_local_dictionary', array_ext.
    drop_duplicates_local_dictionary)
ll.add_symbol('get_groupby_labels', array_ext.get_groupby_labels)
ll.add_symbol('array_isin', array_ext.array_isin)
ll.add_symbol('get_search_regex', array_ext.get_search_regex)
ll.add_symbol('array_info_getitem', array_ext.array_info_getitem)
ll.add_symbol('array_info_getdata1', array_ext.array_info_getdata1)


class ArrayInfoType(types.Type):

    def __init__(self):
        super(ArrayInfoType, self).__init__(name='ArrayInfoType()')


array_info_type = ArrayInfoType()
register_model(ArrayInfoType)(models.OpaqueModel)


class TableTypeCPP(types.Type):

    def __init__(self):
        super(TableTypeCPP, self).__init__(name='TableTypeCPP()')


table_type = TableTypeCPP()
register_model(TableTypeCPP)(models.OpaqueModel)


@lower_cast(table_type, types.voidptr)
def lower_table_type(context, builder, fromty, toty, val):
    return val


@intrinsic
def array_to_info(typingctx, arr_type_t=None):
    return array_info_type(arr_type_t), array_to_info_codegen


def array_to_info_codegen(context, builder, sig, args, incref=True):
    in_arr, = args
    arr_type = sig.args[0]
    if incref:
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, TupleArrayType):
        bhn__iky = context.make_helper(builder, arr_type, in_arr)
        in_arr = bhn__iky.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        lbvr__kkw = context.make_helper(builder, arr_type, in_arr)
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='list_string_array_to_info')
        return builder.call(wtev__qiutk, [lbvr__kkw.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                hjoj__rhmgk = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for znc__tkcf in arr_typ.data:
                    hjoj__rhmgk += get_types(znc__tkcf)
                return hjoj__rhmgk
            elif isinstance(arr_typ, (types.Array, IntegerArrayType,
                FloatingArrayType)) or arr_typ == boolean_array:
                return get_types(arr_typ.dtype)
            elif arr_typ == string_array_type:
                return [CTypeEnum.STRING.value]
            elif arr_typ == binary_array_type:
                return [CTypeEnum.BINARY.value]
            elif isinstance(arr_typ, DecimalArrayType):
                return [CTypeEnum.Decimal.value, arr_typ.precision, arr_typ
                    .scale]
            else:
                return [numba_to_c_type(arr_typ)]

        def get_lengths(arr_typ, arr):
            length = context.compile_internal(builder, lambda a: len(a),
                types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                kga__rlc = context.make_helper(builder, arr_typ, value=arr)
                caehd__ylej = get_lengths(_get_map_arr_data_type(arr_typ),
                    kga__rlc.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                dcr__tpxg = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                caehd__ylej = get_lengths(arr_typ.dtype, dcr__tpxg.data)
                caehd__ylej = cgutils.pack_array(builder, [dcr__tpxg.
                    n_arrays] + [builder.extract_value(caehd__ylej,
                    tdnd__ubqnn) for tdnd__ubqnn in range(caehd__ylej.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                dcr__tpxg = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                caehd__ylej = []
                for tdnd__ubqnn, znc__tkcf in enumerate(arr_typ.data):
                    fferq__kkzz = get_lengths(znc__tkcf, builder.
                        extract_value(dcr__tpxg.data, tdnd__ubqnn))
                    caehd__ylej += [builder.extract_value(fferq__kkzz,
                        rzag__qvinq) for rzag__qvinq in range(fferq__kkzz.
                        type.count)]
                caehd__ylej = cgutils.pack_array(builder, [length, context.
                    get_constant(types.int64, -1)] + caehd__ylej)
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType, types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                caehd__ylej = cgutils.pack_array(builder, [length])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return caehd__ylej

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                kga__rlc = context.make_helper(builder, arr_typ, value=arr)
                idf__aqil = get_buffers(_get_map_arr_data_type(arr_typ),
                    kga__rlc.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                dcr__tpxg = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                sulfb__qvp = get_buffers(arr_typ.dtype, dcr__tpxg.data)
                gxcvj__eqdx = context.make_array(types.Array(offset_type, 1,
                    'C'))(context, builder, dcr__tpxg.offsets)
                fwc__epl = builder.bitcast(gxcvj__eqdx.data, lir.IntType(8)
                    .as_pointer())
                cuh__syfx = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, dcr__tpxg.null_bitmap)
                iqrnd__hmi = builder.bitcast(cuh__syfx.data, lir.IntType(8)
                    .as_pointer())
                idf__aqil = cgutils.pack_array(builder, [fwc__epl,
                    iqrnd__hmi] + [builder.extract_value(sulfb__qvp,
                    tdnd__ubqnn) for tdnd__ubqnn in range(sulfb__qvp.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                dcr__tpxg = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                sulfb__qvp = []
                for tdnd__ubqnn, znc__tkcf in enumerate(arr_typ.data):
                    iuwgc__eabqj = get_buffers(znc__tkcf, builder.
                        extract_value(dcr__tpxg.data, tdnd__ubqnn))
                    sulfb__qvp += [builder.extract_value(iuwgc__eabqj,
                        rzag__qvinq) for rzag__qvinq in range(iuwgc__eabqj.
                        type.count)]
                cuh__syfx = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, dcr__tpxg.null_bitmap)
                iqrnd__hmi = builder.bitcast(cuh__syfx.data, lir.IntType(8)
                    .as_pointer())
                idf__aqil = cgutils.pack_array(builder, [iqrnd__hmi] +
                    sulfb__qvp)
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType)) or arr_typ in (boolean_array,
                datetime_date_array_type):
                xgfew__xdrw = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    xgfew__xdrw = int128_type
                elif arr_typ == datetime_date_array_type:
                    xgfew__xdrw = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                okksu__woqi = context.make_array(types.Array(xgfew__xdrw, 1,
                    'C'))(context, builder, arr.data)
                cuh__syfx = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, arr.null_bitmap)
                gjyyp__jtn = builder.bitcast(okksu__woqi.data, lir.IntType(
                    8).as_pointer())
                iqrnd__hmi = builder.bitcast(cuh__syfx.data, lir.IntType(8)
                    .as_pointer())
                idf__aqil = cgutils.pack_array(builder, [iqrnd__hmi,
                    gjyyp__jtn])
            elif arr_typ in (string_array_type, binary_array_type):
                dcr__tpxg = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                vpsw__rxvi = context.make_helper(builder, offset_arr_type,
                    dcr__tpxg.offsets).data
                data = context.make_helper(builder, char_arr_type,
                    dcr__tpxg.data).data
                txy__jvcsb = context.make_helper(builder,
                    null_bitmap_arr_type, dcr__tpxg.null_bitmap).data
                idf__aqil = cgutils.pack_array(builder, [builder.bitcast(
                    vpsw__rxvi, lir.IntType(8).as_pointer()), builder.
                    bitcast(txy__jvcsb, lir.IntType(8).as_pointer()),
                    builder.bitcast(data, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                gjyyp__jtn = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                stwq__vcb = lir.Constant(lir.IntType(8).as_pointer(), None)
                idf__aqil = cgutils.pack_array(builder, [stwq__vcb, gjyyp__jtn]
                    )
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return idf__aqil

        def get_field_names(arr_typ):
            icohm__lxdy = []
            if isinstance(arr_typ, StructArrayType):
                for cdcla__wyc, odz__prpph in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    icohm__lxdy.append(cdcla__wyc)
                    icohm__lxdy += get_field_names(odz__prpph)
            elif isinstance(arr_typ, ArrayItemArrayType):
                icohm__lxdy += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                icohm__lxdy += get_field_names(_get_map_arr_data_type(arr_typ))
            return icohm__lxdy
        hjoj__rhmgk = get_types(arr_type)
        akv__qsf = cgutils.pack_array(builder, [context.get_constant(types.
            int32, t) for t in hjoj__rhmgk])
        wyu__jxsy = cgutils.alloca_once_value(builder, akv__qsf)
        caehd__ylej = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, caehd__ylej)
        idf__aqil = get_buffers(arr_type, in_arr)
        xgfnr__tfqu = cgutils.alloca_once_value(builder, idf__aqil)
        icohm__lxdy = get_field_names(arr_type)
        if len(icohm__lxdy) == 0:
            icohm__lxdy = ['irrelevant']
        ocrd__uoqkd = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in icohm__lxdy])
        kat__qsnmr = cgutils.alloca_once_value(builder, ocrd__uoqkd)
        if isinstance(arr_type, MapArrayType):
            jgjn__mmci = _get_map_arr_data_type(arr_type)
            ilni__sxbbf = context.make_helper(builder, arr_type, value=in_arr)
            ocpvn__jwpm = ilni__sxbbf.data
        else:
            jgjn__mmci = arr_type
            ocpvn__jwpm = in_arr
        bcubw__bdd = context.make_helper(builder, jgjn__mmci, ocpvn__jwpm)
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='nested_array_to_info')
        akdo__vhf = builder.call(wtev__qiutk, [builder.bitcast(wyu__jxsy,
            lir.IntType(32).as_pointer()), builder.bitcast(xgfnr__tfqu, lir
            .IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            kat__qsnmr, lir.IntType(8).as_pointer()), bcubw__bdd.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return akdo__vhf
    if arr_type in (string_array_type, binary_array_type):
        mhwk__anwiq = context.make_helper(builder, arr_type, in_arr)
        uifny__hde = ArrayItemArrayType(char_arr_type)
        lbvr__kkw = context.make_helper(builder, uifny__hde, mhwk__anwiq.data)
        dcr__tpxg = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        vpsw__rxvi = context.make_helper(builder, offset_arr_type,
            dcr__tpxg.offsets).data
        data = context.make_helper(builder, char_arr_type, dcr__tpxg.data).data
        txy__jvcsb = context.make_helper(builder, null_bitmap_arr_type,
            dcr__tpxg.null_bitmap).data
        cuvqb__elchu = builder.zext(builder.load(builder.gep(vpsw__rxvi, [
            dcr__tpxg.n_arrays])), lir.IntType(64))
        eai__uxsl = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='string_array_to_info')
        return builder.call(wtev__qiutk, [dcr__tpxg.n_arrays, cuvqb__elchu,
            data, vpsw__rxvi, txy__jvcsb, lbvr__kkw.meminfo, eai__uxsl])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        hnie__ydzz = arr.data
        rsly__vbkcl = arr.indices
        sig = array_info_type(arr_type.data)
        ekfwr__rlei = array_to_info_codegen(context, builder, sig, (
            hnie__ydzz,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        dsh__qsv = array_to_info_codegen(context, builder, sig, (
            rsly__vbkcl,), False)
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(32), lir.IntType(32)])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='dict_str_array_to_info')
        kguvq__pwan = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        jjd__bsoq = builder.zext(arr.has_deduped_local_dictionary, lir.
            IntType(32))
        return builder.call(wtev__qiutk, [ekfwr__rlei, dsh__qsv,
            kguvq__pwan, jjd__bsoq])
    fuhj__enzas = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        wgc__wemx = context.compile_internal(builder, lambda a: len(a.dtype
            .categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        vzf__rtfji = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(vzf__rtfji, 1, 'C')
        fuhj__enzas = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if fuhj__enzas:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        length = builder.extract_value(arr.shape, 0)
        obzj__qzpnz = arr_type.dtype
        lzcew__ajjks = numba_to_c_type(obzj__qzpnz)
        uwlqi__llc = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), lzcew__ajjks))
        if fuhj__enzas:
            lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(64), lir.IntType(8).as_pointer()])
            wtev__qiutk = cgutils.get_or_insert_function(builder.module,
                lbk__rrbr, name='categorical_array_to_info')
            return builder.call(wtev__qiutk, [length, builder.bitcast(arr.
                data, lir.IntType(8).as_pointer()), builder.load(uwlqi__llc
                ), wgc__wemx, arr.meminfo])
        else:
            lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer()])
            wtev__qiutk = cgutils.get_or_insert_function(builder.module,
                lbk__rrbr, name='numpy_array_to_info')
            return builder.call(wtev__qiutk, [length, builder.bitcast(arr.
                data, lir.IntType(8).as_pointer()), builder.load(uwlqi__llc
                ), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, TimeArrayType)) or arr_type in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        obzj__qzpnz = arr_type.dtype
        xgfew__xdrw = obzj__qzpnz
        if isinstance(arr_type, DecimalArrayType):
            xgfew__xdrw = int128_type
        if arr_type == datetime_date_array_type:
            xgfew__xdrw = types.int64
        okksu__woqi = context.make_array(types.Array(xgfew__xdrw, 1, 'C'))(
            context, builder, arr.data)
        length = builder.extract_value(okksu__woqi.shape, 0)
        gthm__ywbri = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        lzcew__ajjks = numba_to_c_type(obzj__qzpnz)
        uwlqi__llc = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), lzcew__ajjks))
        if isinstance(arr_type, DecimalArrayType):
            lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
            wtev__qiutk = cgutils.get_or_insert_function(builder.module,
                lbk__rrbr, name='decimal_array_to_info')
            return builder.call(wtev__qiutk, [length, builder.bitcast(
                okksu__woqi.data, lir.IntType(8).as_pointer()), builder.
                load(uwlqi__llc), builder.bitcast(gthm__ywbri.data, lir.
                IntType(8).as_pointer()), okksu__woqi.meminfo, gthm__ywbri.
                meminfo, context.get_constant(types.int32, arr_type.
                precision), context.get_constant(types.int32, arr_type.scale)])
        elif isinstance(arr_type, TimeArrayType):
            lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32)])
            wtev__qiutk = cgutils.get_or_insert_function(builder.module,
                lbk__rrbr, name='time_array_to_info')
            return builder.call(wtev__qiutk, [length, builder.bitcast(
                okksu__woqi.data, lir.IntType(8).as_pointer()), builder.
                load(uwlqi__llc), builder.bitcast(gthm__ywbri.data, lir.
                IntType(8).as_pointer()), okksu__woqi.meminfo, gthm__ywbri.
                meminfo, lir.Constant(lir.IntType(32), arr_type.precision)])
        else:
            lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer()])
            wtev__qiutk = cgutils.get_or_insert_function(builder.module,
                lbk__rrbr, name='nullable_array_to_info')
            return builder.call(wtev__qiutk, [length, builder.bitcast(
                okksu__woqi.data, lir.IntType(8).as_pointer()), builder.
                load(uwlqi__llc), builder.bitcast(gthm__ywbri.data, lir.
                IntType(8).as_pointer()), okksu__woqi.meminfo, gthm__ywbri.
                meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        djfcq__nsr = context.make_array(arr_type.arr_type)(context, builder,
            arr.left)
        jpf__miiky = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        length = builder.extract_value(djfcq__nsr.shape, 0)
        lzcew__ajjks = numba_to_c_type(arr_type.arr_type.dtype)
        uwlqi__llc = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), lzcew__ajjks))
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='interval_array_to_info')
        return builder.call(wtev__qiutk, [length, builder.bitcast(
            djfcq__nsr.data, lir.IntType(8).as_pointer()), builder.bitcast(
            jpf__miiky.data, lir.IntType(8).as_pointer()), builder.load(
            uwlqi__llc), djfcq__nsr.meminfo, jpf__miiky.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    shz__fre = cgutils.alloca_once(builder, lir.IntType(64))
    gjyyp__jtn = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    fpbh__mphtf = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    lbk__rrbr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(64).as_pointer(), lir.IntType(8).as_pointer().
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    wtev__qiutk = cgutils.get_or_insert_function(builder.module, lbk__rrbr,
        name='info_to_numpy_array')
    builder.call(wtev__qiutk, [in_info, shz__fre, gjyyp__jtn, fpbh__mphtf])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    hfnx__ewlc = context.get_value_type(types.intp)
    ykn__vcyft = cgutils.pack_array(builder, [builder.load(shz__fre)], ty=
        hfnx__ewlc)
    xayz__pohz = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    yla__fvirx = cgutils.pack_array(builder, [xayz__pohz], ty=hfnx__ewlc)
    data = builder.bitcast(builder.load(gjyyp__jtn), context.get_data_type(
        arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=data, shape=ykn__vcyft,
        strides=yla__fvirx, itemsize=xayz__pohz, meminfo=builder.load(
        fpbh__mphtf))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    zefk__gcwdz = context.make_helper(builder, arr_type)
    lbk__rrbr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(8).as_pointer().as_pointer()])
    wtev__qiutk = cgutils.get_or_insert_function(builder.module, lbk__rrbr,
        name='info_to_list_string_array')
    builder.call(wtev__qiutk, [in_info, zefk__gcwdz._get_ptr_by_name(
        'meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return zefk__gcwdz._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    plpx__ibqg = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        sorwc__scnj = lengths_pos
        ggzgy__ixb = infos_pos
        efdvp__lypza, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        hpvp__gpjg = ArrayItemArrayPayloadType(arr_typ)
        gwqmo__ganhf = context.get_data_type(hpvp__gpjg)
        uryui__glvs = context.get_abi_sizeof(gwqmo__ganhf)
        haz__wrpty = define_array_item_dtor(context, builder, arr_typ,
            hpvp__gpjg)
        fvkk__ygogq = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, uryui__glvs), haz__wrpty)
        zuakk__xlj = context.nrt.meminfo_data(builder, fvkk__ygogq)
        xue__fmtdq = builder.bitcast(zuakk__xlj, gwqmo__ganhf.as_pointer())
        dcr__tpxg = cgutils.create_struct_proxy(hpvp__gpjg)(context, builder)
        dcr__tpxg.n_arrays = builder.extract_value(builder.load(lengths_ptr
            ), sorwc__scnj)
        dcr__tpxg.data = efdvp__lypza
        yed__ogol = builder.load(array_infos_ptr)
        xpmip__dskva = builder.bitcast(builder.extract_value(yed__ogol,
            ggzgy__ixb), plpx__ibqg)
        dcr__tpxg.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, xpmip__dskva)
        nfq__mhzpm = builder.bitcast(builder.extract_value(yed__ogol, 
            ggzgy__ixb + 1), plpx__ibqg)
        dcr__tpxg.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, nfq__mhzpm)
        builder.store(dcr__tpxg._getvalue(), xue__fmtdq)
        lbvr__kkw = context.make_helper(builder, arr_typ)
        lbvr__kkw.meminfo = fvkk__ygogq
        return lbvr__kkw._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        dsmp__potz = []
        ggzgy__ixb = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for dxsg__fbyu in arr_typ.data:
            efdvp__lypza, lengths_pos, infos_pos = nested_to_array(context,
                builder, dxsg__fbyu, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            dsmp__potz.append(efdvp__lypza)
        hpvp__gpjg = StructArrayPayloadType(arr_typ.data)
        gwqmo__ganhf = context.get_value_type(hpvp__gpjg)
        uryui__glvs = context.get_abi_sizeof(gwqmo__ganhf)
        haz__wrpty = define_struct_arr_dtor(context, builder, arr_typ,
            hpvp__gpjg)
        fvkk__ygogq = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, uryui__glvs), haz__wrpty)
        zuakk__xlj = context.nrt.meminfo_data(builder, fvkk__ygogq)
        xue__fmtdq = builder.bitcast(zuakk__xlj, gwqmo__ganhf.as_pointer())
        dcr__tpxg = cgutils.create_struct_proxy(hpvp__gpjg)(context, builder)
        dcr__tpxg.data = cgutils.pack_array(builder, dsmp__potz
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, dsmp__potz)
        yed__ogol = builder.load(array_infos_ptr)
        nfq__mhzpm = builder.bitcast(builder.extract_value(yed__ogol,
            ggzgy__ixb), plpx__ibqg)
        dcr__tpxg.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, nfq__mhzpm)
        builder.store(dcr__tpxg._getvalue(), xue__fmtdq)
        pfvdn__fjg = context.make_helper(builder, arr_typ)
        pfvdn__fjg.meminfo = fvkk__ygogq
        return pfvdn__fjg._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        yed__ogol = builder.load(array_infos_ptr)
        xohz__wlw = builder.bitcast(builder.extract_value(yed__ogol,
            infos_pos), plpx__ibqg)
        mhwk__anwiq = context.make_helper(builder, arr_typ)
        uifny__hde = ArrayItemArrayType(char_arr_type)
        lbvr__kkw = context.make_helper(builder, uifny__hde)
        lbk__rrbr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='info_to_string_array')
        builder.call(wtev__qiutk, [xohz__wlw, lbvr__kkw._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        mhwk__anwiq.data = lbvr__kkw._getvalue()
        return mhwk__anwiq._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        yed__ogol = builder.load(array_infos_ptr)
        zfjse__narz = builder.bitcast(builder.extract_value(yed__ogol, 
            infos_pos + 1), plpx__ibqg)
        return _lower_info_to_array_numpy(arr_typ, context, builder,
            zfjse__narz), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType)) or arr_typ in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        xgfew__xdrw = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            xgfew__xdrw = int128_type
        elif arr_typ == datetime_date_array_type:
            xgfew__xdrw = types.int64
        yed__ogol = builder.load(array_infos_ptr)
        nfq__mhzpm = builder.bitcast(builder.extract_value(yed__ogol,
            infos_pos), plpx__ibqg)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, nfq__mhzpm)
        zfjse__narz = builder.bitcast(builder.extract_value(yed__ogol, 
            infos_pos + 1), plpx__ibqg)
        arr.data = _lower_info_to_array_numpy(types.Array(xgfew__xdrw, 1,
            'C'), context, builder, zfjse__narz)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, nsc__het = args
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        return _lower_info_to_array_list_string_array(arr_type, context,
            builder, in_info)
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType,
        StructArrayType, TupleArrayType)):

        def get_num_arrays(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 1 + get_num_arrays(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_arrays(dxsg__fbyu) for dxsg__fbyu in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(dxsg__fbyu) for dxsg__fbyu in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            eyk__zjb = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            eyk__zjb = _get_map_arr_data_type(arr_type)
        else:
            eyk__zjb = arr_type
        cqx__nqdwq = get_num_arrays(eyk__zjb)
        caehd__ylej = cgutils.pack_array(builder, [lir.Constant(lir.IntType
            (64), 0) for nsc__het in range(cqx__nqdwq)])
        lengths_ptr = cgutils.alloca_once_value(builder, caehd__ylej)
        stwq__vcb = lir.Constant(lir.IntType(8).as_pointer(), None)
        ecbnp__uwtcc = cgutils.pack_array(builder, [stwq__vcb for nsc__het in
            range(get_num_infos(eyk__zjb))])
        array_infos_ptr = cgutils.alloca_once_value(builder, ecbnp__uwtcc)
        lbk__rrbr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='info_to_nested_array')
        builder.call(wtev__qiutk, [in_info, builder.bitcast(lengths_ptr,
            lir.IntType(64).as_pointer()), builder.bitcast(array_infos_ptr,
            lir.IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, nsc__het, nsc__het = nested_to_array(context, builder,
            eyk__zjb, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            bhn__iky = context.make_helper(builder, arr_type)
            bhn__iky.data = arr
            context.nrt.incref(builder, eyk__zjb, arr)
            arr = bhn__iky._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, eyk__zjb)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        mhwk__anwiq = context.make_helper(builder, arr_type)
        uifny__hde = ArrayItemArrayType(char_arr_type)
        lbvr__kkw = context.make_helper(builder, uifny__hde)
        lbk__rrbr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='info_to_string_array')
        builder.call(wtev__qiutk, [in_info, lbvr__kkw._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        mhwk__anwiq.data = lbvr__kkw._getvalue()
        return mhwk__anwiq._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='get_nested_info')
        ekfwr__rlei = builder.call(wtev__qiutk, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        dsh__qsv = builder.call(wtev__qiutk, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        lrd__fllh = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        lrd__fllh.data = info_to_array_codegen(context, builder, sig, (
            ekfwr__rlei, context.get_constant_null(arr_type.data)))
        fvi__qvged = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = fvi__qvged(array_info_type, fvi__qvged)
        lrd__fllh.indices = info_to_array_codegen(context, builder, sig, (
            dsh__qsv, context.get_constant_null(fvi__qvged)))
        lbk__rrbr = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='get_has_global_dictionary')
        kguvq__pwan = builder.call(wtev__qiutk, [in_info])
        lrd__fllh.has_global_dictionary = builder.trunc(kguvq__pwan,
            cgutils.bool_t)
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='get_has_deduped_local_dictionary')
        jjd__bsoq = builder.call(wtev__qiutk, [in_info])
        lrd__fllh.has_deduped_local_dictionary = builder.trunc(jjd__bsoq,
            cgutils.bool_t)
        return lrd__fllh._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        vzf__rtfji = get_categories_int_type(arr_type.dtype)
        mkf__aeyy = types.Array(vzf__rtfji, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(mkf__aeyy, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            jplsh__xnweg = bodo.utils.utils.create_categorical_type(arr_type
                .dtype.categories, arr_type.dtype.data.data, is_ordered)
            new_cats_tup = MetaType(tuple(jplsh__xnweg))
            int_type = arr_type.dtype.int_type
            lpxwl__oeurr = arr_type.dtype.data.data
            bdebf__wpg = context.get_constant_generic(builder, lpxwl__oeurr,
                jplsh__xnweg)
            obzj__qzpnz = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(lpxwl__oeurr), [bdebf__wpg])
        else:
            obzj__qzpnz = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, obzj__qzpnz)
        out_arr.dtype = obzj__qzpnz
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        data = _lower_info_to_array_numpy(arr_type.data_array_type, context,
            builder, in_info)
        arr.data = data
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, TimeArrayType)) or arr_type in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        xgfew__xdrw = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            xgfew__xdrw = int128_type
        elif arr_type == datetime_date_array_type:
            xgfew__xdrw = types.int64
        jjo__sdrww = types.Array(xgfew__xdrw, 1, 'C')
        okksu__woqi = context.make_array(jjo__sdrww)(context, builder)
        oahsw__ffdge = types.Array(types.uint8, 1, 'C')
        pvsm__nwno = context.make_array(oahsw__ffdge)(context, builder)
        shz__fre = cgutils.alloca_once(builder, lir.IntType(64))
        pzzi__txr = cgutils.alloca_once(builder, lir.IntType(64))
        gjyyp__jtn = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        uuhyn__qss = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        fpbh__mphtf = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        wyws__ggvd = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        lbk__rrbr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='info_to_nullable_array')
        builder.call(wtev__qiutk, [in_info, shz__fre, pzzi__txr, gjyyp__jtn,
            uuhyn__qss, fpbh__mphtf, wyws__ggvd])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        hfnx__ewlc = context.get_value_type(types.intp)
        ykn__vcyft = cgutils.pack_array(builder, [builder.load(shz__fre)],
            ty=hfnx__ewlc)
        xayz__pohz = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(xgfew__xdrw)))
        yla__fvirx = cgutils.pack_array(builder, [xayz__pohz], ty=hfnx__ewlc)
        data = builder.bitcast(builder.load(gjyyp__jtn), context.
            get_data_type(xgfew__xdrw).as_pointer())
        numba.np.arrayobj.populate_array(okksu__woqi, data=data, shape=
            ykn__vcyft, strides=yla__fvirx, itemsize=xayz__pohz, meminfo=
            builder.load(fpbh__mphtf))
        arr.data = okksu__woqi._getvalue()
        ykn__vcyft = cgutils.pack_array(builder, [builder.load(pzzi__txr)],
            ty=hfnx__ewlc)
        xayz__pohz = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(types.uint8)))
        yla__fvirx = cgutils.pack_array(builder, [xayz__pohz], ty=hfnx__ewlc)
        data = builder.bitcast(builder.load(uuhyn__qss), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(pvsm__nwno, data=data, shape=
            ykn__vcyft, strides=yla__fvirx, itemsize=xayz__pohz, meminfo=
            builder.load(wyws__ggvd))
        arr.null_bitmap = pvsm__nwno._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        djfcq__nsr = context.make_array(arr_type.arr_type)(context, builder)
        jpf__miiky = context.make_array(arr_type.arr_type)(context, builder)
        shz__fre = cgutils.alloca_once(builder, lir.IntType(64))
        tfk__pgcj = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        bris__qmyyz = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ocht__jsfud = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        kwqp__ivkm = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        lbk__rrbr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='info_to_interval_array')
        builder.call(wtev__qiutk, [in_info, shz__fre, tfk__pgcj,
            bris__qmyyz, ocht__jsfud, kwqp__ivkm])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        hfnx__ewlc = context.get_value_type(types.intp)
        ykn__vcyft = cgutils.pack_array(builder, [builder.load(shz__fre)],
            ty=hfnx__ewlc)
        xayz__pohz = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
        yla__fvirx = cgutils.pack_array(builder, [xayz__pohz], ty=hfnx__ewlc)
        jjele__ievjg = builder.bitcast(builder.load(tfk__pgcj), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(djfcq__nsr, data=jjele__ievjg,
            shape=ykn__vcyft, strides=yla__fvirx, itemsize=xayz__pohz,
            meminfo=builder.load(ocht__jsfud))
        arr.left = djfcq__nsr._getvalue()
        mllyg__vqwk = builder.bitcast(builder.load(bris__qmyyz), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(jpf__miiky, data=mllyg__vqwk,
            shape=ykn__vcyft, strides=yla__fvirx, itemsize=xayz__pohz,
            meminfo=builder.load(kwqp__ivkm))
        arr.right = jpf__miiky._getvalue()
        return arr._getvalue()
    raise_bodo_error(f'info_to_array(): array type {arr_type} is not supported'
        )


@intrinsic
def info_to_array(typingctx, info_type, array_type):
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    assert info_type == array_info_type, 'info_to_array: expected info type'
    return arr_type(info_type, array_type), info_to_array_codegen


@intrinsic
def test_alloc_np(typingctx, len_typ, arr_type):
    array_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type

    def codegen(context, builder, sig, args):
        length, nsc__het = args
        lzcew__ajjks = numba_to_c_type(array_type.dtype)
        uwlqi__llc = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), lzcew__ajjks))
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='alloc_numpy')
        return builder.call(wtev__qiutk, [length, builder.load(uwlqi__llc)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        length, woql__mpaia = args
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='alloc_string_array')
        return builder.call(wtev__qiutk, [length, woql__mpaia])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    sbao__noxw, = args
    owym__zonz = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], sbao__noxw)
    lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer().as_pointer(), lir.IntType(64)])
    wtev__qiutk = cgutils.get_or_insert_function(builder.module, lbk__rrbr,
        name='arr_info_list_to_table')
    return builder.call(wtev__qiutk, [owym__zonz.data, owym__zonz.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='info_from_table')
        return builder.call(wtev__qiutk, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    rpm__dkza = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        cpp_table, qla__rfc, nsc__het = args
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='info_from_table')
        ugll__ftw = cgutils.create_struct_proxy(rpm__dkza)(context, builder)
        ugll__ftw.parent = cgutils.get_null_value(ugll__ftw.parent.type)
        bqvk__sgbj = context.make_array(table_idx_arr_t)(context, builder,
            qla__rfc)
        roz__qbb = context.get_constant(types.int64, -1)
        lpyn__pvxt = context.get_constant(types.int64, 0)
        qxf__bmsml = cgutils.alloca_once_value(builder, lpyn__pvxt)
        for t, wztf__tgt in rpm__dkza.type_to_blk.items():
            wax__mdd = context.get_constant(types.int64, len(rpm__dkza.
                block_to_arr_ind[wztf__tgt]))
            nsc__het, dubd__goyp = ListInstance.allocate_ex(context,
                builder, types.List(t), wax__mdd)
            dubd__goyp.size = wax__mdd
            sok__gvmn = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(rpm__dkza.block_to_arr_ind[
                wztf__tgt], dtype=np.int64))
            bztj__pjg = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, sok__gvmn)
            with cgutils.for_range(builder, wax__mdd) as mfhbx__zfj:
                tdnd__ubqnn = mfhbx__zfj.index
                ayfr__rmy = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    bztj__pjg, tdnd__ubqnn)
                nusnl__yosnr = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, bqvk__sgbj, ayfr__rmy)
                fauz__oiuzl = builder.icmp_unsigned('!=', nusnl__yosnr,
                    roz__qbb)
                with builder.if_else(fauz__oiuzl) as (oleut__kjosp, xufd__tgtn
                    ):
                    with oleut__kjosp:
                        tlbe__mbgz = builder.call(wtev__qiutk, [cpp_table,
                            nusnl__yosnr])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            tlbe__mbgz])
                        dubd__goyp.inititem(tdnd__ubqnn, arr, incref=False)
                        length = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(length, qxf__bmsml)
                    with xufd__tgtn:
                        evdit__jclwo = context.get_constant_null(t)
                        dubd__goyp.inititem(tdnd__ubqnn, evdit__jclwo,
                            incref=False)
            setattr(ugll__ftw, f'block_{wztf__tgt}', dubd__goyp.value)
        ugll__ftw.len = builder.load(qxf__bmsml)
        return ugll__ftw._getvalue()
    return rpm__dkza(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def cpp_table_to_py_data(cpp_table, out_col_inds_t, out_types_t, n_rows_t,
    n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
    sculq__iksf = out_col_inds_t.instance_type.meta
    rpm__dkza = unwrap_typeref(out_types_t.types[0])
    udbvl__bsl = [unwrap_typeref(out_types_t.types[tdnd__ubqnn]) for
        tdnd__ubqnn in range(1, len(out_types_t.types))]
    ifwe__dygfs = {}
    uew__yvr = get_overload_const_int(n_table_cols_t)
    lur__sigjz = {ntn__cpv: tdnd__ubqnn for tdnd__ubqnn, ntn__cpv in
        enumerate(sculq__iksf)}
    if not is_overload_none(unknown_cat_arrs_t):
        wjo__zec = {oyzd__cuf: tdnd__ubqnn for tdnd__ubqnn, oyzd__cuf in
            enumerate(cat_inds_t.instance_type.meta)}
    rnuyj__gudqw = []
    pmw__vxfv = """def impl(cpp_table, out_col_inds_t, out_types_t, n_rows_t, n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
"""
    if isinstance(rpm__dkza, bodo.TableType):
        pmw__vxfv += f'  py_table = init_table(py_table_type, False)\n'
        pmw__vxfv += f'  py_table = set_table_len(py_table, n_rows_t)\n'
        for oedho__icld, wztf__tgt in rpm__dkza.type_to_blk.items():
            upwh__ilfvo = [lur__sigjz.get(tdnd__ubqnn, -1) for tdnd__ubqnn in
                rpm__dkza.block_to_arr_ind[wztf__tgt]]
            ifwe__dygfs[f'out_inds_{wztf__tgt}'] = np.array(upwh__ilfvo, np
                .int64)
            ifwe__dygfs[f'out_type_{wztf__tgt}'] = oedho__icld
            ifwe__dygfs[f'typ_list_{wztf__tgt}'] = types.List(oedho__icld)
            rbh__rfz = f'out_type_{wztf__tgt}'
            if type_has_unknown_cats(oedho__icld):
                if is_overload_none(unknown_cat_arrs_t):
                    pmw__vxfv += f"""  in_arr_list_{wztf__tgt} = get_table_block(out_types_t[0], {wztf__tgt})
"""
                    rbh__rfz = f'in_arr_list_{wztf__tgt}[i]'
                else:
                    ifwe__dygfs[f'cat_arr_inds_{wztf__tgt}'] = np.array([
                        wjo__zec.get(tdnd__ubqnn, -1) for tdnd__ubqnn in
                        rpm__dkza.block_to_arr_ind[wztf__tgt]], np.int64)
                    rbh__rfz = (
                        f'unknown_cat_arrs_t[cat_arr_inds_{wztf__tgt}[i]]')
            wax__mdd = len(rpm__dkza.block_to_arr_ind[wztf__tgt])
            pmw__vxfv += f"""  arr_list_{wztf__tgt} = alloc_list_like(typ_list_{wztf__tgt}, {wax__mdd}, False)
"""
            pmw__vxfv += f'  for i in range(len(arr_list_{wztf__tgt})):\n'
            pmw__vxfv += f'    cpp_ind_{wztf__tgt} = out_inds_{wztf__tgt}[i]\n'
            pmw__vxfv += f'    if cpp_ind_{wztf__tgt} == -1:\n'
            pmw__vxfv += f'      continue\n'
            pmw__vxfv += f"""    arr_{wztf__tgt} = info_to_array(info_from_table(cpp_table, cpp_ind_{wztf__tgt}), {rbh__rfz})
"""
            pmw__vxfv += f'    arr_list_{wztf__tgt}[i] = arr_{wztf__tgt}\n'
            pmw__vxfv += f"""  py_table = set_table_block(py_table, arr_list_{wztf__tgt}, {wztf__tgt})
"""
        rnuyj__gudqw.append('py_table')
    elif rpm__dkza != types.none:
        onx__qimn = lur__sigjz.get(0, -1)
        if onx__qimn != -1:
            ifwe__dygfs[f'arr_typ_arg0'] = rpm__dkza
            rbh__rfz = f'arr_typ_arg0'
            if type_has_unknown_cats(rpm__dkza):
                if is_overload_none(unknown_cat_arrs_t):
                    rbh__rfz = f'out_types_t[0]'
                else:
                    rbh__rfz = f'unknown_cat_arrs_t[{wjo__zec[0]}]'
            pmw__vxfv += f"""  out_arg0 = info_to_array(info_from_table(cpp_table, {onx__qimn}), {rbh__rfz})
"""
            rnuyj__gudqw.append('out_arg0')
    for tdnd__ubqnn, t in enumerate(udbvl__bsl):
        onx__qimn = lur__sigjz.get(uew__yvr + tdnd__ubqnn, -1)
        if onx__qimn != -1:
            ifwe__dygfs[f'extra_arr_type_{tdnd__ubqnn}'] = t
            rbh__rfz = f'extra_arr_type_{tdnd__ubqnn}'
            if type_has_unknown_cats(t):
                if is_overload_none(unknown_cat_arrs_t):
                    rbh__rfz = f'out_types_t[{tdnd__ubqnn + 1}]'
                else:
                    rbh__rfz = (
                        f'unknown_cat_arrs_t[{wjo__zec[uew__yvr + tdnd__ubqnn]}]'
                        )
            pmw__vxfv += f"""  out_{tdnd__ubqnn} = info_to_array(info_from_table(cpp_table, {onx__qimn}), {rbh__rfz})
"""
            rnuyj__gudqw.append(f'out_{tdnd__ubqnn}')
    bun__nhhpu = ',' if len(rnuyj__gudqw) == 1 else ''
    pmw__vxfv += f"  return ({', '.join(rnuyj__gudqw)}{bun__nhhpu})\n"
    ifwe__dygfs.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'out_col_inds': list(sculq__iksf), 'py_table_type': rpm__dkza})
    vcf__pmjp = {}
    exec(pmw__vxfv, ifwe__dygfs, vcf__pmjp)
    return vcf__pmjp['impl']


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    rpm__dkza = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        py_table, nsc__het = args
        yaaaw__lyiok = cgutils.create_struct_proxy(rpm__dkza)(context,
            builder, py_table)
        if rpm__dkza.has_runtime_cols:
            qhknc__bngwg = lir.Constant(lir.IntType(64), 0)
            for wztf__tgt, t in enumerate(rpm__dkza.arr_types):
                qws__etek = getattr(yaaaw__lyiok, f'block_{wztf__tgt}')
                qcyy__ejtw = ListInstance(context, builder, types.List(t),
                    qws__etek)
                qhknc__bngwg = builder.add(qhknc__bngwg, qcyy__ejtw.size)
        else:
            qhknc__bngwg = lir.Constant(lir.IntType(64), len(rpm__dkza.
                arr_types))
        nsc__het, rhgvi__zxdbx = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), qhknc__bngwg)
        rhgvi__zxdbx.size = qhknc__bngwg
        if rpm__dkza.has_runtime_cols:
            oxjlz__glldu = lir.Constant(lir.IntType(64), 0)
            for wztf__tgt, t in enumerate(rpm__dkza.arr_types):
                qws__etek = getattr(yaaaw__lyiok, f'block_{wztf__tgt}')
                qcyy__ejtw = ListInstance(context, builder, types.List(t),
                    qws__etek)
                wax__mdd = qcyy__ejtw.size
                with cgutils.for_range(builder, wax__mdd) as mfhbx__zfj:
                    tdnd__ubqnn = mfhbx__zfj.index
                    arr = qcyy__ejtw.getitem(tdnd__ubqnn)
                    vtya__txcsq = signature(array_info_type, t)
                    qic__upx = arr,
                    qdx__zbcw = array_to_info_codegen(context, builder,
                        vtya__txcsq, qic__upx)
                    rhgvi__zxdbx.inititem(builder.add(oxjlz__glldu,
                        tdnd__ubqnn), qdx__zbcw, incref=False)
                oxjlz__glldu = builder.add(oxjlz__glldu, wax__mdd)
        else:
            for t, wztf__tgt in rpm__dkza.type_to_blk.items():
                wax__mdd = context.get_constant(types.int64, len(rpm__dkza.
                    block_to_arr_ind[wztf__tgt]))
                qws__etek = getattr(yaaaw__lyiok, f'block_{wztf__tgt}')
                qcyy__ejtw = ListInstance(context, builder, types.List(t),
                    qws__etek)
                sok__gvmn = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(rpm__dkza.
                    block_to_arr_ind[wztf__tgt], dtype=np.int64))
                bztj__pjg = context.make_array(types.Array(types.int64, 1, 'C')
                    )(context, builder, sok__gvmn)
                with cgutils.for_range(builder, wax__mdd) as mfhbx__zfj:
                    tdnd__ubqnn = mfhbx__zfj.index
                    ayfr__rmy = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        bztj__pjg, tdnd__ubqnn)
                    jtvvs__asyk = signature(types.none, rpm__dkza, types.
                        List(t), types.int64, types.int64)
                    lqvcw__vqpwy = py_table, qws__etek, tdnd__ubqnn, ayfr__rmy
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, jtvvs__asyk, lqvcw__vqpwy)
                    arr = qcyy__ejtw.getitem(tdnd__ubqnn)
                    vtya__txcsq = signature(array_info_type, t)
                    qic__upx = arr,
                    qdx__zbcw = array_to_info_codegen(context, builder,
                        vtya__txcsq, qic__upx)
                    rhgvi__zxdbx.inititem(ayfr__rmy, qdx__zbcw, incref=False)
        myie__ixhs = rhgvi__zxdbx.value
        zdx__dzel = signature(table_type, types.List(array_info_type))
        mdcdx__ryxc = myie__ixhs,
        cpp_table = arr_info_list_to_table_codegen(context, builder,
            zdx__dzel, mdcdx__ryxc)
        context.nrt.decref(builder, types.List(array_info_type), myie__ixhs)
        return cpp_table
    return table_type(rpm__dkza, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def py_data_to_cpp_table(py_table, extra_arrs_tup, in_col_inds_t,
    n_table_cols_t):
    pinh__fjxh = in_col_inds_t.instance_type.meta
    ifwe__dygfs = {}
    uew__yvr = get_overload_const_int(n_table_cols_t)
    wcczb__bhhlo = defaultdict(list)
    lur__sigjz = {}
    for tdnd__ubqnn, ntn__cpv in enumerate(pinh__fjxh):
        if ntn__cpv in lur__sigjz:
            wcczb__bhhlo[ntn__cpv].append(tdnd__ubqnn)
        else:
            lur__sigjz[ntn__cpv] = tdnd__ubqnn
    pmw__vxfv = (
        'def impl(py_table, extra_arrs_tup, in_col_inds_t, n_table_cols_t):\n')
    pmw__vxfv += (
        f'  cpp_arr_list = alloc_empty_list_type({len(pinh__fjxh)}, array_info_type)\n'
        )
    if py_table != types.none:
        for wztf__tgt in py_table.type_to_blk.values():
            upwh__ilfvo = [lur__sigjz.get(tdnd__ubqnn, -1) for tdnd__ubqnn in
                py_table.block_to_arr_ind[wztf__tgt]]
            ifwe__dygfs[f'out_inds_{wztf__tgt}'] = np.array(upwh__ilfvo, np
                .int64)
            ifwe__dygfs[f'arr_inds_{wztf__tgt}'] = np.array(py_table.
                block_to_arr_ind[wztf__tgt], np.int64)
            pmw__vxfv += (
                f'  arr_list_{wztf__tgt} = get_table_block(py_table, {wztf__tgt})\n'
                )
            pmw__vxfv += f'  for i in range(len(arr_list_{wztf__tgt})):\n'
            pmw__vxfv += (
                f'    out_arr_ind_{wztf__tgt} = out_inds_{wztf__tgt}[i]\n')
            pmw__vxfv += f'    if out_arr_ind_{wztf__tgt} == -1:\n'
            pmw__vxfv += f'      continue\n'
            pmw__vxfv += f'    arr_ind_{wztf__tgt} = arr_inds_{wztf__tgt}[i]\n'
            pmw__vxfv += f"""    ensure_column_unboxed(py_table, arr_list_{wztf__tgt}, i, arr_ind_{wztf__tgt})
"""
            pmw__vxfv += f"""    cpp_arr_list[out_arr_ind_{wztf__tgt}] = array_to_info(arr_list_{wztf__tgt}[i])
"""
        for xixtz__kobx, mzfdr__iwl in wcczb__bhhlo.items():
            if xixtz__kobx < uew__yvr:
                wztf__tgt = py_table.block_nums[xixtz__kobx]
                cmkwe__nkpze = py_table.block_offsets[xixtz__kobx]
                for onx__qimn in mzfdr__iwl:
                    pmw__vxfv += f"""  cpp_arr_list[{onx__qimn}] = array_to_info(arr_list_{wztf__tgt}[{cmkwe__nkpze}])
"""
    for tdnd__ubqnn in range(len(extra_arrs_tup)):
        oiwpz__owjr = lur__sigjz.get(uew__yvr + tdnd__ubqnn, -1)
        if oiwpz__owjr != -1:
            oxysp__vbx = [oiwpz__owjr] + wcczb__bhhlo.get(uew__yvr +
                tdnd__ubqnn, [])
            for onx__qimn in oxysp__vbx:
                pmw__vxfv += f"""  cpp_arr_list[{onx__qimn}] = array_to_info(extra_arrs_tup[{tdnd__ubqnn}])
"""
    pmw__vxfv += f'  return arr_info_list_to_table(cpp_arr_list)\n'
    ifwe__dygfs.update({'array_info_type': array_info_type,
        'alloc_empty_list_type': bodo.hiframes.table.alloc_empty_list_type,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'ensure_column_unboxed': bodo.hiframes.table.ensure_column_unboxed,
        'array_to_info': array_to_info, 'arr_info_list_to_table':
        arr_info_list_to_table})
    vcf__pmjp = {}
    exec(pmw__vxfv, ifwe__dygfs, vcf__pmjp)
    return vcf__pmjp['impl']


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))
decref_table_array = types.ExternalFunction('decref_table_array', types.
    void(table_type, types.int32))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        lbk__rrbr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='delete_table')
        builder.call(wtev__qiutk, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='shuffle_table')
        akdo__vhf = builder.call(wtev__qiutk, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return akdo__vhf
    return table_type(table_t, types.int64, types.boolean, types.int32
        ), codegen


class ShuffleInfoType(types.Type):

    def __init__(self):
        super(ShuffleInfoType, self).__init__(name='ShuffleInfoType()')


shuffle_info_type = ShuffleInfoType()
register_model(ShuffleInfoType)(models.OpaqueModel)
get_shuffle_info = types.ExternalFunction('get_shuffle_info',
    shuffle_info_type(table_type))


@intrinsic
def delete_shuffle_info(typingctx, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[0] == types.none:
            return
        lbk__rrbr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='delete_shuffle_info')
        return builder.call(wtev__qiutk, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='reverse_shuffle_table')
        return builder.call(wtev__qiutk, args)
    return table_type(table_type, shuffle_info_t), codegen


@intrinsic
def get_null_shuffle_info(typingctx):

    def codegen(context, builder, sig, args):
        return context.get_constant_null(sig.return_type)
    return shuffle_info_type(), codegen


@intrinsic
def hash_join_table(typingctx, left_table_t, right_table_t, left_parallel_t,
    right_parallel_t, n_keys_t, n_data_left_t, n_data_right_t, same_vect_t,
    key_in_out_t, same_need_typechange_t, is_left_t, is_right_t, is_join_t,
    extra_data_col_t, indicator, _bodo_na_equal, cond_func, left_col_nums,
    left_col_nums_len, right_col_nums, right_col_nums_len, num_rows_ptr_t):
    assert left_table_t == table_type
    assert right_table_t == table_type

    def codegen(context, builder, sig, args):
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(64), lir.IntType(8).as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='hash_join_table')
        akdo__vhf = builder.call(wtev__qiutk, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return akdo__vhf
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.int64, types.int64, types.int64, types.voidptr,
        types.voidptr, types.voidptr, types.boolean, types.boolean, types.
        boolean, types.boolean, types.boolean, types.boolean, types.voidptr,
        types.voidptr, types.int64, types.voidptr, types.int64, types.voidptr
        ), codegen


@intrinsic
def cross_join_table(typingctx, left_table_t, right_table_t,
    left_parallel_t, right_parallel_t, is_left_t, is_right_t,
    key_in_output_t, need_typechange_t, cond_func, left_col_nums,
    left_col_nums_len, right_col_nums, right_col_nums_len, num_rows_ptr_t):
    assert left_table_t == table_type, 'cross_join_table: cpp table type expected'
    assert right_table_t == table_type, 'cross_join_table: cpp table type expected'

    def codegen(context, builder, sig, args):
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64), lir.
            IntType(8).as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='cross_join_table')
        akdo__vhf = builder.call(wtev__qiutk, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return akdo__vhf
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.boolean, types.boolean, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.int64, types.voidptr, types.
        int64, types.voidptr), codegen


@intrinsic
def sort_values_table(typingctx, table_t, n_keys_t, vect_ascending_t,
    na_position_b_t, dead_keys_t, n_rows_t, bounds_t, parallel_t):
    assert table_t == table_type, 'C++ table type expected'

    def codegen(context, builder, sig, args):
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1)])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='sort_values_table')
        akdo__vhf = builder.call(wtev__qiutk, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return akdo__vhf
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='sample_table')
        akdo__vhf = builder.call(wtev__qiutk, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return akdo__vhf
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='shuffle_renormalization')
        akdo__vhf = builder.call(wtev__qiutk, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return akdo__vhf
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='shuffle_renormalization_group')
        akdo__vhf = builder.call(wtev__qiutk, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return akdo__vhf
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='drop_duplicates_table')
        akdo__vhf = builder.call(wtev__qiutk, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return akdo__vhf
    return table_type(table_t, types.boolean, types.int64, types.int64,
        types.boolean, types.boolean), codegen


@intrinsic
def groupby_and_aggregate(typingctx, table_t, n_keys_t, input_has_index,
    ftypes, func_offsets, udf_n_redvars, is_parallel, skipdropna_t,
    shift_periods_t, transform_func, head_n, return_keys, return_index,
    dropna, update_cb, combine_cb, eval_cb, general_udfs_cb,
    udf_table_dummy_t, n_out_rows_t, n_shuffle_keys_t):
    assert table_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        wtev__qiutk = cgutils.get_or_insert_function(builder.module,
            lbk__rrbr, name='groupby_and_aggregate')
        akdo__vhf = builder.call(wtev__qiutk, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return akdo__vhf
    return table_type(table_t, types.int64, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, types.boolean, types.boolean, types.
        int64, types.int64, types.int64, types.boolean, types.boolean,
        types.boolean, types.voidptr, types.voidptr, types.voidptr, types.
        voidptr, table_t, types.voidptr, types.int64), codegen


_drop_duplicates_local_dictionary = types.ExternalFunction(
    'drop_duplicates_local_dictionary', types.void(array_info_type, types.
    bool_))


@numba.njit(no_cpython_wrapper=True)
def drop_duplicates_local_dictionary(dict_arr, sort_dictionary):
    letgv__kmkox = array_to_info(dict_arr)
    _drop_duplicates_local_dictionary(letgv__kmkox, sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(letgv__kmkox, bodo.dict_str_arr_type)
    return out_arr


_convert_local_dictionary_to_global = types.ExternalFunction(
    'convert_local_dictionary_to_global', types.void(array_info_type, types
    .bool_, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def convert_local_dictionary_to_global(dict_arr, sort_dictionary,
    is_parallel=False):
    letgv__kmkox = array_to_info(dict_arr)
    _convert_local_dictionary_to_global(letgv__kmkox, is_parallel,
        sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(letgv__kmkox, bodo.dict_str_arr_type)
    return out_arr


get_groupby_labels = types.ExternalFunction('get_groupby_labels', types.
    int64(table_type, types.voidptr, types.voidptr, types.boolean, types.bool_)
    )
_array_isin = types.ExternalFunction('array_isin', types.void(
    array_info_type, array_info_type, array_info_type, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def array_isin(out_arr, in_arr, in_values, is_parallel):
    in_arr = decode_if_dict_array(in_arr)
    in_values = decode_if_dict_array(in_values)
    hsdkv__xixii = array_to_info(in_arr)
    tdp__cwuf = array_to_info(in_values)
    yttm__yah = array_to_info(out_arr)
    ariq__yje = arr_info_list_to_table([hsdkv__xixii, tdp__cwuf, yttm__yah])
    _array_isin(yttm__yah, hsdkv__xixii, tdp__cwuf, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(ariq__yje)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, match, pat, out_arr):
    hsdkv__xixii = array_to_info(in_arr)
    yttm__yah = array_to_info(out_arr)
    _get_search_regex(hsdkv__xixii, case, match, pat, yttm__yah)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    cig__tyzee = col_array_typ.dtype
    if isinstance(cig__tyzee, (types.Number, TimeType, bodo.libs.
        pd_datetime_arr_ext.PandasDatetimeTZDtype)) or cig__tyzee in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:
        if isinstance(cig__tyzee, bodo.libs.pd_datetime_arr_ext.
            PandasDatetimeTZDtype):
            cig__tyzee = bodo.datetime64ns

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                ugll__ftw, wrmsd__xnoe = args
                ugll__ftw = builder.bitcast(ugll__ftw, lir.IntType(8).
                    as_pointer().as_pointer())
                zfkj__wrt = lir.Constant(lir.IntType(64), c_ind)
                kjos__eayja = builder.load(builder.gep(ugll__ftw, [zfkj__wrt]))
                kjos__eayja = builder.bitcast(kjos__eayja, context.
                    get_data_type(cig__tyzee).as_pointer())
                return context.unpack_value(builder, cig__tyzee, builder.
                    gep(kjos__eayja, [wrmsd__xnoe]))
            return cig__tyzee(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ in (bodo.string_array_type, bodo.binary_array_type):

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                ugll__ftw, wrmsd__xnoe = args
                ugll__ftw = builder.bitcast(ugll__ftw, lir.IntType(8).
                    as_pointer().as_pointer())
                zfkj__wrt = lir.Constant(lir.IntType(64), c_ind)
                kjos__eayja = builder.load(builder.gep(ugll__ftw, [zfkj__wrt]))
                lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                xsh__trv = cgutils.get_or_insert_function(builder.module,
                    lbk__rrbr, name='array_info_getitem')
                vem__njr = cgutils.alloca_once(builder, lir.IntType(64))
                args = kjos__eayja, wrmsd__xnoe, vem__njr
                gjyyp__jtn = builder.call(xsh__trv, args)
                ycl__ilss = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    ycl__ilss, [gjyyp__jtn, builder.load(vem__njr)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                yqb__uqwo = lir.Constant(lir.IntType(64), 1)
                zclwn__mnn = lir.Constant(lir.IntType(64), 2)
                ugll__ftw, wrmsd__xnoe = args
                ugll__ftw = builder.bitcast(ugll__ftw, lir.IntType(8).
                    as_pointer().as_pointer())
                zfkj__wrt = lir.Constant(lir.IntType(64), c_ind)
                kjos__eayja = builder.load(builder.gep(ugll__ftw, [zfkj__wrt]))
                lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64)])
                rso__frcfw = cgutils.get_or_insert_function(builder.module,
                    lbk__rrbr, name='get_nested_info')
                args = kjos__eayja, zclwn__mnn
                bib__iamaj = builder.call(rso__frcfw, args)
                lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer()])
                xvdg__sam = cgutils.get_or_insert_function(builder.module,
                    lbk__rrbr, name='array_info_getdata1')
                args = bib__iamaj,
                sjog__qwg = builder.call(xvdg__sam, args)
                sjog__qwg = builder.bitcast(sjog__qwg, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                yxyru__xdtp = builder.sext(builder.load(builder.gep(
                    sjog__qwg, [wrmsd__xnoe])), lir.IntType(64))
                args = kjos__eayja, yqb__uqwo
                gpnc__ddz = builder.call(rso__frcfw, args)
                lbk__rrbr = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                xsh__trv = cgutils.get_or_insert_function(builder.module,
                    lbk__rrbr, name='array_info_getitem')
                vem__njr = cgutils.alloca_once(builder, lir.IntType(64))
                args = gpnc__ddz, yxyru__xdtp, vem__njr
                gjyyp__jtn = builder.call(xsh__trv, args)
                ycl__ilss = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    ycl__ilss, [gjyyp__jtn, builder.load(vem__njr)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{cig__tyzee}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if isinstance(col_array_dtype, (IntegerArrayType, FloatingArrayType,
        bodo.TimeArrayType)) or col_array_dtype in (bodo.libs.bool_arr_ext.
        boolean_array, bodo.binary_array_type, bodo.datetime_date_array_type
        ) or is_str_arr_type(col_array_dtype):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                egts__jmg, wrmsd__xnoe = args
                egts__jmg = builder.bitcast(egts__jmg, lir.IntType(8).
                    as_pointer().as_pointer())
                zfkj__wrt = lir.Constant(lir.IntType(64), c_ind)
                kjos__eayja = builder.load(builder.gep(egts__jmg, [zfkj__wrt]))
                txy__jvcsb = builder.bitcast(kjos__eayja, context.
                    get_data_type(types.bool_).as_pointer())
                lzz__pakf = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    txy__jvcsb, wrmsd__xnoe)
                cdwan__ive = builder.icmp_unsigned('!=', lzz__pakf, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(cdwan__ive, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, (types.Array, bodo.DatetimeArrayType)):
        cig__tyzee = col_array_dtype.dtype
        if cig__tyzee in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            cig__tyzee, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype):
            if isinstance(cig__tyzee, bodo.libs.pd_datetime_arr_ext.
                PandasDatetimeTZDtype):
                cig__tyzee = bodo.datetime64ns

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    ugll__ftw, wrmsd__xnoe = args
                    ugll__ftw = builder.bitcast(ugll__ftw, lir.IntType(8).
                        as_pointer().as_pointer())
                    zfkj__wrt = lir.Constant(lir.IntType(64), c_ind)
                    kjos__eayja = builder.load(builder.gep(ugll__ftw, [
                        zfkj__wrt]))
                    kjos__eayja = builder.bitcast(kjos__eayja, context.
                        get_data_type(cig__tyzee).as_pointer())
                    hlmw__njn = builder.load(builder.gep(kjos__eayja, [
                        wrmsd__xnoe]))
                    cdwan__ive = builder.icmp_unsigned('!=', hlmw__njn, lir
                        .Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(cdwan__ive, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(cig__tyzee, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    ugll__ftw, wrmsd__xnoe = args
                    ugll__ftw = builder.bitcast(ugll__ftw, lir.IntType(8).
                        as_pointer().as_pointer())
                    zfkj__wrt = lir.Constant(lir.IntType(64), c_ind)
                    kjos__eayja = builder.load(builder.gep(ugll__ftw, [
                        zfkj__wrt]))
                    kjos__eayja = builder.bitcast(kjos__eayja, context.
                        get_data_type(cig__tyzee).as_pointer())
                    hlmw__njn = builder.load(builder.gep(kjos__eayja, [
                        wrmsd__xnoe]))
                    kkfy__axdco = signature(types.bool_, cig__tyzee)
                    lzz__pakf = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, kkfy__axdco, (hlmw__njn,))
                    return builder.not_(builder.sext(lzz__pakf, lir.IntType(8))
                        )
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
