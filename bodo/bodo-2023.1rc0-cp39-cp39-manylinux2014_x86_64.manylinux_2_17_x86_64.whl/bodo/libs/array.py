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
        fcjcb__bdsw = context.make_helper(builder, arr_type, in_arr)
        in_arr = fcjcb__bdsw.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        ogt__qqt = context.make_helper(builder, arr_type, in_arr)
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='list_string_array_to_info')
        return builder.call(uhh__nmas, [ogt__qqt.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                ikxg__hty = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for nhabc__hxwvz in arr_typ.data:
                    ikxg__hty += get_types(nhabc__hxwvz)
                return ikxg__hty
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
                vqzx__yndqg = context.make_helper(builder, arr_typ, value=arr)
                ynngb__haf = get_lengths(_get_map_arr_data_type(arr_typ),
                    vqzx__yndqg.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                nakh__wcc = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                ynngb__haf = get_lengths(arr_typ.dtype, nakh__wcc.data)
                ynngb__haf = cgutils.pack_array(builder, [nakh__wcc.
                    n_arrays] + [builder.extract_value(ynngb__haf,
                    tlbo__qdtcs) for tlbo__qdtcs in range(ynngb__haf.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                nakh__wcc = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                ynngb__haf = []
                for tlbo__qdtcs, nhabc__hxwvz in enumerate(arr_typ.data):
                    ewg__laxp = get_lengths(nhabc__hxwvz, builder.
                        extract_value(nakh__wcc.data, tlbo__qdtcs))
                    ynngb__haf += [builder.extract_value(ewg__laxp,
                        sxff__wgq) for sxff__wgq in range(ewg__laxp.type.count)
                        ]
                ynngb__haf = cgutils.pack_array(builder, [length, context.
                    get_constant(types.int64, -1)] + ynngb__haf)
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType, types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                ynngb__haf = cgutils.pack_array(builder, [length])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return ynngb__haf

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                vqzx__yndqg = context.make_helper(builder, arr_typ, value=arr)
                seu__seb = get_buffers(_get_map_arr_data_type(arr_typ),
                    vqzx__yndqg.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                nakh__wcc = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                yjh__tzpqi = get_buffers(arr_typ.dtype, nakh__wcc.data)
                she__mnncc = context.make_array(types.Array(offset_type, 1,
                    'C'))(context, builder, nakh__wcc.offsets)
                ggrtw__vpewx = builder.bitcast(she__mnncc.data, lir.IntType
                    (8).as_pointer())
                cinvw__qmibe = context.make_array(types.Array(types.uint8, 
                    1, 'C'))(context, builder, nakh__wcc.null_bitmap)
                ndl__lgs = builder.bitcast(cinvw__qmibe.data, lir.IntType(8
                    ).as_pointer())
                seu__seb = cgutils.pack_array(builder, [ggrtw__vpewx,
                    ndl__lgs] + [builder.extract_value(yjh__tzpqi,
                    tlbo__qdtcs) for tlbo__qdtcs in range(yjh__tzpqi.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                nakh__wcc = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                yjh__tzpqi = []
                for tlbo__qdtcs, nhabc__hxwvz in enumerate(arr_typ.data):
                    gwrvi__oewy = get_buffers(nhabc__hxwvz, builder.
                        extract_value(nakh__wcc.data, tlbo__qdtcs))
                    yjh__tzpqi += [builder.extract_value(gwrvi__oewy,
                        sxff__wgq) for sxff__wgq in range(gwrvi__oewy.type.
                        count)]
                cinvw__qmibe = context.make_array(types.Array(types.uint8, 
                    1, 'C'))(context, builder, nakh__wcc.null_bitmap)
                ndl__lgs = builder.bitcast(cinvw__qmibe.data, lir.IntType(8
                    ).as_pointer())
                seu__seb = cgutils.pack_array(builder, [ndl__lgs] + yjh__tzpqi)
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType)) or arr_typ in (boolean_array,
                datetime_date_array_type):
                owjko__pvsf = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    owjko__pvsf = int128_type
                elif arr_typ == datetime_date_array_type:
                    owjko__pvsf = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                ouq__wmi = context.make_array(types.Array(owjko__pvsf, 1, 'C')
                    )(context, builder, arr.data)
                cinvw__qmibe = context.make_array(types.Array(types.uint8, 
                    1, 'C'))(context, builder, arr.null_bitmap)
                qkya__ygnu = builder.bitcast(ouq__wmi.data, lir.IntType(8).
                    as_pointer())
                ndl__lgs = builder.bitcast(cinvw__qmibe.data, lir.IntType(8
                    ).as_pointer())
                seu__seb = cgutils.pack_array(builder, [ndl__lgs, qkya__ygnu])
            elif arr_typ in (string_array_type, binary_array_type):
                nakh__wcc = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                rbz__cdrh = context.make_helper(builder, offset_arr_type,
                    nakh__wcc.offsets).data
                data = context.make_helper(builder, char_arr_type,
                    nakh__wcc.data).data
                xrv__kgtea = context.make_helper(builder,
                    null_bitmap_arr_type, nakh__wcc.null_bitmap).data
                seu__seb = cgutils.pack_array(builder, [builder.bitcast(
                    rbz__cdrh, lir.IntType(8).as_pointer()), builder.
                    bitcast(xrv__kgtea, lir.IntType(8).as_pointer()),
                    builder.bitcast(data, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                qkya__ygnu = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                ulpq__dmlk = lir.Constant(lir.IntType(8).as_pointer(), None)
                seu__seb = cgutils.pack_array(builder, [ulpq__dmlk, qkya__ygnu]
                    )
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return seu__seb

        def get_field_names(arr_typ):
            hjgl__vkpli = []
            if isinstance(arr_typ, StructArrayType):
                for qju__esxs, yvnu__jvrg in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    hjgl__vkpli.append(qju__esxs)
                    hjgl__vkpli += get_field_names(yvnu__jvrg)
            elif isinstance(arr_typ, ArrayItemArrayType):
                hjgl__vkpli += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                hjgl__vkpli += get_field_names(_get_map_arr_data_type(arr_typ))
            return hjgl__vkpli
        ikxg__hty = get_types(arr_type)
        bhstq__utgjf = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in ikxg__hty])
        loqz__gco = cgutils.alloca_once_value(builder, bhstq__utgjf)
        ynngb__haf = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, ynngb__haf)
        seu__seb = get_buffers(arr_type, in_arr)
        wwvjz__vxi = cgutils.alloca_once_value(builder, seu__seb)
        hjgl__vkpli = get_field_names(arr_type)
        if len(hjgl__vkpli) == 0:
            hjgl__vkpli = ['irrelevant']
        xrxuk__tdb = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in hjgl__vkpli])
        ndlfq__ksl = cgutils.alloca_once_value(builder, xrxuk__tdb)
        if isinstance(arr_type, MapArrayType):
            iiuot__owpti = _get_map_arr_data_type(arr_type)
            olty__mrkdg = context.make_helper(builder, arr_type, value=in_arr)
            kgpxz__vdtrc = olty__mrkdg.data
        else:
            iiuot__owpti = arr_type
            kgpxz__vdtrc = in_arr
        vnhss__zcfh = context.make_helper(builder, iiuot__owpti, kgpxz__vdtrc)
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='nested_array_to_info')
        xmk__vhy = builder.call(uhh__nmas, [builder.bitcast(loqz__gco, lir.
            IntType(32).as_pointer()), builder.bitcast(wwvjz__vxi, lir.
            IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            ndlfq__ksl, lir.IntType(8).as_pointer()), vnhss__zcfh.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xmk__vhy
    if arr_type in (string_array_type, binary_array_type):
        azj__cuzke = context.make_helper(builder, arr_type, in_arr)
        yor__xidjq = ArrayItemArrayType(char_arr_type)
        ogt__qqt = context.make_helper(builder, yor__xidjq, azj__cuzke.data)
        nakh__wcc = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        rbz__cdrh = context.make_helper(builder, offset_arr_type, nakh__wcc
            .offsets).data
        data = context.make_helper(builder, char_arr_type, nakh__wcc.data).data
        xrv__kgtea = context.make_helper(builder, null_bitmap_arr_type,
            nakh__wcc.null_bitmap).data
        kgbg__flf = builder.zext(builder.load(builder.gep(rbz__cdrh, [
            nakh__wcc.n_arrays])), lir.IntType(64))
        zox__bcm = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='string_array_to_info')
        return builder.call(uhh__nmas, [nakh__wcc.n_arrays, kgbg__flf, data,
            rbz__cdrh, xrv__kgtea, ogt__qqt.meminfo, zox__bcm])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        iwsk__xlqos = arr.data
        pvsg__wqek = arr.indices
        sig = array_info_type(arr_type.data)
        ubgw__vfr = array_to_info_codegen(context, builder, sig, (
            iwsk__xlqos,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        ltip__moevi = array_to_info_codegen(context, builder, sig, (
            pvsg__wqek,), False)
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(32), lir.IntType(32)])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='dict_str_array_to_info')
        zwl__urm = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        whoxh__inf = builder.zext(arr.has_deduped_local_dictionary, lir.
            IntType(32))
        return builder.call(uhh__nmas, [ubgw__vfr, ltip__moevi, zwl__urm,
            whoxh__inf])
    lzg__cczko = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        xkwm__rbbgn = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        ilap__smvj = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(ilap__smvj, 1, 'C')
        lzg__cczko = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if lzg__cczko:
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
        klctp__dja = arr_type.dtype
        yws__cjns = numba_to_c_type(klctp__dja)
        zybx__jnhyc = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), yws__cjns))
        if lzg__cczko:
            bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(64), lir.IntType(8).as_pointer()])
            uhh__nmas = cgutils.get_or_insert_function(builder.module,
                bley__kda, name='categorical_array_to_info')
            return builder.call(uhh__nmas, [length, builder.bitcast(arr.
                data, lir.IntType(8).as_pointer()), builder.load(
                zybx__jnhyc), xkwm__rbbgn, arr.meminfo])
        else:
            bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer()])
            uhh__nmas = cgutils.get_or_insert_function(builder.module,
                bley__kda, name='numpy_array_to_info')
            return builder.call(uhh__nmas, [length, builder.bitcast(arr.
                data, lir.IntType(8).as_pointer()), builder.load(
                zybx__jnhyc), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, TimeArrayType)) or arr_type in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        klctp__dja = arr_type.dtype
        owjko__pvsf = klctp__dja
        if isinstance(arr_type, DecimalArrayType):
            owjko__pvsf = int128_type
        if arr_type == datetime_date_array_type:
            owjko__pvsf = types.int64
        ouq__wmi = context.make_array(types.Array(owjko__pvsf, 1, 'C'))(context
            , builder, arr.data)
        length = builder.extract_value(ouq__wmi.shape, 0)
        qwqd__auxq = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        yws__cjns = numba_to_c_type(klctp__dja)
        zybx__jnhyc = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), yws__cjns))
        if isinstance(arr_type, DecimalArrayType):
            bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
            uhh__nmas = cgutils.get_or_insert_function(builder.module,
                bley__kda, name='decimal_array_to_info')
            return builder.call(uhh__nmas, [length, builder.bitcast(
                ouq__wmi.data, lir.IntType(8).as_pointer()), builder.load(
                zybx__jnhyc), builder.bitcast(qwqd__auxq.data, lir.IntType(
                8).as_pointer()), ouq__wmi.meminfo, qwqd__auxq.meminfo,
                context.get_constant(types.int32, arr_type.precision),
                context.get_constant(types.int32, arr_type.scale)])
        elif isinstance(arr_type, TimeArrayType):
            bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32)])
            uhh__nmas = cgutils.get_or_insert_function(builder.module,
                bley__kda, name='time_array_to_info')
            return builder.call(uhh__nmas, [length, builder.bitcast(
                ouq__wmi.data, lir.IntType(8).as_pointer()), builder.load(
                zybx__jnhyc), builder.bitcast(qwqd__auxq.data, lir.IntType(
                8).as_pointer()), ouq__wmi.meminfo, qwqd__auxq.meminfo, lir
                .Constant(lir.IntType(32), arr_type.precision)])
        else:
            bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer()])
            uhh__nmas = cgutils.get_or_insert_function(builder.module,
                bley__kda, name='nullable_array_to_info')
            return builder.call(uhh__nmas, [length, builder.bitcast(
                ouq__wmi.data, lir.IntType(8).as_pointer()), builder.load(
                zybx__jnhyc), builder.bitcast(qwqd__auxq.data, lir.IntType(
                8).as_pointer()), ouq__wmi.meminfo, qwqd__auxq.meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        niukt__qmku = context.make_array(arr_type.arr_type)(context,
            builder, arr.left)
        jyye__shwrv = context.make_array(arr_type.arr_type)(context,
            builder, arr.right)
        length = builder.extract_value(niukt__qmku.shape, 0)
        yws__cjns = numba_to_c_type(arr_type.arr_type.dtype)
        zybx__jnhyc = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), yws__cjns))
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='interval_array_to_info')
        return builder.call(uhh__nmas, [length, builder.bitcast(niukt__qmku
            .data, lir.IntType(8).as_pointer()), builder.bitcast(
            jyye__shwrv.data, lir.IntType(8).as_pointer()), builder.load(
            zybx__jnhyc), niukt__qmku.meminfo, jyye__shwrv.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    kttfi__gsx = cgutils.alloca_once(builder, lir.IntType(64))
    qkya__ygnu = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    qfjz__beqgb = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    bley__kda = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(64).as_pointer(), lir.IntType(8).as_pointer().
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    uhh__nmas = cgutils.get_or_insert_function(builder.module, bley__kda,
        name='info_to_numpy_array')
    builder.call(uhh__nmas, [in_info, kttfi__gsx, qkya__ygnu, qfjz__beqgb])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    ficnm__eots = context.get_value_type(types.intp)
    pueyo__hup = cgutils.pack_array(builder, [builder.load(kttfi__gsx)], ty
        =ficnm__eots)
    renl__mpo = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    mtz__frluu = cgutils.pack_array(builder, [renl__mpo], ty=ficnm__eots)
    data = builder.bitcast(builder.load(qkya__ygnu), context.get_data_type(
        arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=data, shape=pueyo__hup,
        strides=mtz__frluu, itemsize=renl__mpo, meminfo=builder.load(
        qfjz__beqgb))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    wyjn__gsb = context.make_helper(builder, arr_type)
    bley__kda = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(8).as_pointer().as_pointer()])
    uhh__nmas = cgutils.get_or_insert_function(builder.module, bley__kda,
        name='info_to_list_string_array')
    builder.call(uhh__nmas, [in_info, wyjn__gsb._get_ptr_by_name('meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return wyjn__gsb._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    vmiod__sgzws = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        ctnim__ihy = lengths_pos
        vjmhb__nczcc = infos_pos
        kyxl__timl, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        ewsq__cwcva = ArrayItemArrayPayloadType(arr_typ)
        nngn__egbfw = context.get_data_type(ewsq__cwcva)
        smez__ect = context.get_abi_sizeof(nngn__egbfw)
        oflr__xnhol = define_array_item_dtor(context, builder, arr_typ,
            ewsq__cwcva)
        icwi__ylr = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, smez__ect), oflr__xnhol)
        psq__ffzxh = context.nrt.meminfo_data(builder, icwi__ylr)
        ubcxg__xlk = builder.bitcast(psq__ffzxh, nngn__egbfw.as_pointer())
        nakh__wcc = cgutils.create_struct_proxy(ewsq__cwcva)(context, builder)
        nakh__wcc.n_arrays = builder.extract_value(builder.load(lengths_ptr
            ), ctnim__ihy)
        nakh__wcc.data = kyxl__timl
        sda__ypru = builder.load(array_infos_ptr)
        kjtjs__fzc = builder.bitcast(builder.extract_value(sda__ypru,
            vjmhb__nczcc), vmiod__sgzws)
        nakh__wcc.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, kjtjs__fzc)
        mlcec__rns = builder.bitcast(builder.extract_value(sda__ypru, 
            vjmhb__nczcc + 1), vmiod__sgzws)
        nakh__wcc.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, mlcec__rns)
        builder.store(nakh__wcc._getvalue(), ubcxg__xlk)
        ogt__qqt = context.make_helper(builder, arr_typ)
        ogt__qqt.meminfo = icwi__ylr
        return ogt__qqt._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        raz__dqh = []
        vjmhb__nczcc = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for qjr__srdxh in arr_typ.data:
            kyxl__timl, lengths_pos, infos_pos = nested_to_array(context,
                builder, qjr__srdxh, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            raz__dqh.append(kyxl__timl)
        ewsq__cwcva = StructArrayPayloadType(arr_typ.data)
        nngn__egbfw = context.get_value_type(ewsq__cwcva)
        smez__ect = context.get_abi_sizeof(nngn__egbfw)
        oflr__xnhol = define_struct_arr_dtor(context, builder, arr_typ,
            ewsq__cwcva)
        icwi__ylr = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, smez__ect), oflr__xnhol)
        psq__ffzxh = context.nrt.meminfo_data(builder, icwi__ylr)
        ubcxg__xlk = builder.bitcast(psq__ffzxh, nngn__egbfw.as_pointer())
        nakh__wcc = cgutils.create_struct_proxy(ewsq__cwcva)(context, builder)
        nakh__wcc.data = cgutils.pack_array(builder, raz__dqh
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, raz__dqh)
        sda__ypru = builder.load(array_infos_ptr)
        mlcec__rns = builder.bitcast(builder.extract_value(sda__ypru,
            vjmhb__nczcc), vmiod__sgzws)
        nakh__wcc.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, mlcec__rns)
        builder.store(nakh__wcc._getvalue(), ubcxg__xlk)
        mzlnr__bgpnw = context.make_helper(builder, arr_typ)
        mzlnr__bgpnw.meminfo = icwi__ylr
        return mzlnr__bgpnw._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        sda__ypru = builder.load(array_infos_ptr)
        glvw__yqq = builder.bitcast(builder.extract_value(sda__ypru,
            infos_pos), vmiod__sgzws)
        azj__cuzke = context.make_helper(builder, arr_typ)
        yor__xidjq = ArrayItemArrayType(char_arr_type)
        ogt__qqt = context.make_helper(builder, yor__xidjq)
        bley__kda = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='info_to_string_array')
        builder.call(uhh__nmas, [glvw__yqq, ogt__qqt._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        azj__cuzke.data = ogt__qqt._getvalue()
        return azj__cuzke._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        sda__ypru = builder.load(array_infos_ptr)
        kxxba__rlo = builder.bitcast(builder.extract_value(sda__ypru, 
            infos_pos + 1), vmiod__sgzws)
        return _lower_info_to_array_numpy(arr_typ, context, builder, kxxba__rlo
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType)) or arr_typ in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        owjko__pvsf = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            owjko__pvsf = int128_type
        elif arr_typ == datetime_date_array_type:
            owjko__pvsf = types.int64
        sda__ypru = builder.load(array_infos_ptr)
        mlcec__rns = builder.bitcast(builder.extract_value(sda__ypru,
            infos_pos), vmiod__sgzws)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, mlcec__rns)
        kxxba__rlo = builder.bitcast(builder.extract_value(sda__ypru, 
            infos_pos + 1), vmiod__sgzws)
        arr.data = _lower_info_to_array_numpy(types.Array(owjko__pvsf, 1,
            'C'), context, builder, kxxba__rlo)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, lbb__ftxy = args
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
                return 1 + sum([get_num_arrays(qjr__srdxh) for qjr__srdxh in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(qjr__srdxh) for qjr__srdxh in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            tlc__anjp = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            tlc__anjp = _get_map_arr_data_type(arr_type)
        else:
            tlc__anjp = arr_type
        ogsh__qrq = get_num_arrays(tlc__anjp)
        ynngb__haf = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), 0) for lbb__ftxy in range(ogsh__qrq)])
        lengths_ptr = cgutils.alloca_once_value(builder, ynngb__haf)
        ulpq__dmlk = lir.Constant(lir.IntType(8).as_pointer(), None)
        bqeu__tmj = cgutils.pack_array(builder, [ulpq__dmlk for lbb__ftxy in
            range(get_num_infos(tlc__anjp))])
        array_infos_ptr = cgutils.alloca_once_value(builder, bqeu__tmj)
        bley__kda = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='info_to_nested_array')
        builder.call(uhh__nmas, [in_info, builder.bitcast(lengths_ptr, lir.
            IntType(64).as_pointer()), builder.bitcast(array_infos_ptr, lir
            .IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, lbb__ftxy, lbb__ftxy = nested_to_array(context, builder,
            tlc__anjp, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            fcjcb__bdsw = context.make_helper(builder, arr_type)
            fcjcb__bdsw.data = arr
            context.nrt.incref(builder, tlc__anjp, arr)
            arr = fcjcb__bdsw._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, tlc__anjp)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        azj__cuzke = context.make_helper(builder, arr_type)
        yor__xidjq = ArrayItemArrayType(char_arr_type)
        ogt__qqt = context.make_helper(builder, yor__xidjq)
        bley__kda = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='info_to_string_array')
        builder.call(uhh__nmas, [in_info, ogt__qqt._get_ptr_by_name('meminfo')]
            )
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        azj__cuzke.data = ogt__qqt._getvalue()
        return azj__cuzke._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='get_nested_info')
        ubgw__vfr = builder.call(uhh__nmas, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        ltip__moevi = builder.call(uhh__nmas, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        dxlm__wkjn = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        dxlm__wkjn.data = info_to_array_codegen(context, builder, sig, (
            ubgw__vfr, context.get_constant_null(arr_type.data)))
        hhh__rhzy = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = hhh__rhzy(array_info_type, hhh__rhzy)
        dxlm__wkjn.indices = info_to_array_codegen(context, builder, sig, (
            ltip__moevi, context.get_constant_null(hhh__rhzy)))
        bley__kda = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='get_has_global_dictionary')
        zwl__urm = builder.call(uhh__nmas, [in_info])
        dxlm__wkjn.has_global_dictionary = builder.trunc(zwl__urm, cgutils.
            bool_t)
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='get_has_deduped_local_dictionary')
        whoxh__inf = builder.call(uhh__nmas, [in_info])
        dxlm__wkjn.has_deduped_local_dictionary = builder.trunc(whoxh__inf,
            cgutils.bool_t)
        return dxlm__wkjn._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        ilap__smvj = get_categories_int_type(arr_type.dtype)
        gotm__klcv = types.Array(ilap__smvj, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(gotm__klcv, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            mgdkt__ldc = bodo.utils.utils.create_categorical_type(arr_type.
                dtype.categories, arr_type.dtype.data.data, is_ordered)
            new_cats_tup = MetaType(tuple(mgdkt__ldc))
            int_type = arr_type.dtype.int_type
            yuu__hdm = arr_type.dtype.data.data
            qpok__qvenw = context.get_constant_generic(builder, yuu__hdm,
                mgdkt__ldc)
            klctp__dja = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(yuu__hdm), [qpok__qvenw])
        else:
            klctp__dja = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, klctp__dja)
        out_arr.dtype = klctp__dja
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
        owjko__pvsf = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            owjko__pvsf = int128_type
        elif arr_type == datetime_date_array_type:
            owjko__pvsf = types.int64
        frxi__anyn = types.Array(owjko__pvsf, 1, 'C')
        ouq__wmi = context.make_array(frxi__anyn)(context, builder)
        whnjz__ecqgi = types.Array(types.uint8, 1, 'C')
        rnea__ajc = context.make_array(whnjz__ecqgi)(context, builder)
        kttfi__gsx = cgutils.alloca_once(builder, lir.IntType(64))
        rik__sxr = cgutils.alloca_once(builder, lir.IntType(64))
        qkya__ygnu = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        vjr__cyzcd = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        qfjz__beqgb = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        epgd__sxo = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        bley__kda = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='info_to_nullable_array')
        builder.call(uhh__nmas, [in_info, kttfi__gsx, rik__sxr, qkya__ygnu,
            vjr__cyzcd, qfjz__beqgb, epgd__sxo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        ficnm__eots = context.get_value_type(types.intp)
        pueyo__hup = cgutils.pack_array(builder, [builder.load(kttfi__gsx)],
            ty=ficnm__eots)
        renl__mpo = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(owjko__pvsf)))
        mtz__frluu = cgutils.pack_array(builder, [renl__mpo], ty=ficnm__eots)
        data = builder.bitcast(builder.load(qkya__ygnu), context.
            get_data_type(owjko__pvsf).as_pointer())
        numba.np.arrayobj.populate_array(ouq__wmi, data=data, shape=
            pueyo__hup, strides=mtz__frluu, itemsize=renl__mpo, meminfo=
            builder.load(qfjz__beqgb))
        arr.data = ouq__wmi._getvalue()
        pueyo__hup = cgutils.pack_array(builder, [builder.load(rik__sxr)],
            ty=ficnm__eots)
        renl__mpo = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(types.uint8)))
        mtz__frluu = cgutils.pack_array(builder, [renl__mpo], ty=ficnm__eots)
        data = builder.bitcast(builder.load(vjr__cyzcd), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(rnea__ajc, data=data, shape=
            pueyo__hup, strides=mtz__frluu, itemsize=renl__mpo, meminfo=
            builder.load(epgd__sxo))
        arr.null_bitmap = rnea__ajc._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        niukt__qmku = context.make_array(arr_type.arr_type)(context, builder)
        jyye__shwrv = context.make_array(arr_type.arr_type)(context, builder)
        kttfi__gsx = cgutils.alloca_once(builder, lir.IntType(64))
        kjjsr__bjuye = cgutils.alloca_once(builder, lir.IntType(8).as_pointer()
            )
        skkn__nutq = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        oblty__ajhzl = cgutils.alloca_once(builder, lir.IntType(8).as_pointer()
            )
        xin__ant = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        bley__kda = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='info_to_interval_array')
        builder.call(uhh__nmas, [in_info, kttfi__gsx, kjjsr__bjuye,
            skkn__nutq, oblty__ajhzl, xin__ant])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        ficnm__eots = context.get_value_type(types.intp)
        pueyo__hup = cgutils.pack_array(builder, [builder.load(kttfi__gsx)],
            ty=ficnm__eots)
        renl__mpo = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(arr_type.arr_type.dtype)))
        mtz__frluu = cgutils.pack_array(builder, [renl__mpo], ty=ficnm__eots)
        bar__nvs = builder.bitcast(builder.load(kjjsr__bjuye), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(niukt__qmku, data=bar__nvs, shape=
            pueyo__hup, strides=mtz__frluu, itemsize=renl__mpo, meminfo=
            builder.load(oblty__ajhzl))
        arr.left = niukt__qmku._getvalue()
        ipzl__akxee = builder.bitcast(builder.load(skkn__nutq), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(jyye__shwrv, data=ipzl__akxee,
            shape=pueyo__hup, strides=mtz__frluu, itemsize=renl__mpo,
            meminfo=builder.load(xin__ant))
        arr.right = jyye__shwrv._getvalue()
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
        length, lbb__ftxy = args
        yws__cjns = numba_to_c_type(array_type.dtype)
        zybx__jnhyc = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), yws__cjns))
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='alloc_numpy')
        return builder.call(uhh__nmas, [length, builder.load(zybx__jnhyc)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        length, nnw__tcapu = args
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='alloc_string_array')
        return builder.call(uhh__nmas, [length, nnw__tcapu])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    xdhe__lyke, = args
    uww__povp = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], xdhe__lyke)
    bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer().as_pointer(), lir.IntType(64)])
    uhh__nmas = cgutils.get_or_insert_function(builder.module, bley__kda,
        name='arr_info_list_to_table')
    return builder.call(uhh__nmas, [uww__povp.data, uww__povp.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='info_from_table')
        return builder.call(uhh__nmas, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    vjhz__rff = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        cpp_table, wxgf__agzs, lbb__ftxy = args
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='info_from_table')
        blddk__zqc = cgutils.create_struct_proxy(vjhz__rff)(context, builder)
        blddk__zqc.parent = cgutils.get_null_value(blddk__zqc.parent.type)
        hfhdb__muwzo = context.make_array(table_idx_arr_t)(context, builder,
            wxgf__agzs)
        deqim__jvfl = context.get_constant(types.int64, -1)
        siho__mqrz = context.get_constant(types.int64, 0)
        lvz__ybjg = cgutils.alloca_once_value(builder, siho__mqrz)
        for t, nzryt__ouzwy in vjhz__rff.type_to_blk.items():
            mcsx__pwp = context.get_constant(types.int64, len(vjhz__rff.
                block_to_arr_ind[nzryt__ouzwy]))
            lbb__ftxy, srjol__uua = ListInstance.allocate_ex(context,
                builder, types.List(t), mcsx__pwp)
            srjol__uua.size = mcsx__pwp
            ainf__cdxkv = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(vjhz__rff.block_to_arr_ind[
                nzryt__ouzwy], dtype=np.int64))
            makq__lagsc = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, ainf__cdxkv)
            with cgutils.for_range(builder, mcsx__pwp) as pvjwa__pungy:
                tlbo__qdtcs = pvjwa__pungy.index
                ixhic__jffuz = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    makq__lagsc, tlbo__qdtcs)
                jpx__tqd = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, hfhdb__muwzo, ixhic__jffuz)
                vsr__pelq = builder.icmp_unsigned('!=', jpx__tqd, deqim__jvfl)
                with builder.if_else(vsr__pelq) as (yxz__kgq, stk__uml):
                    with yxz__kgq:
                        usm__hydxk = builder.call(uhh__nmas, [cpp_table,
                            jpx__tqd])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            usm__hydxk])
                        srjol__uua.inititem(tlbo__qdtcs, arr, incref=False)
                        length = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(length, lvz__ybjg)
                    with stk__uml:
                        qxl__iis = context.get_constant_null(t)
                        srjol__uua.inititem(tlbo__qdtcs, qxl__iis, incref=False
                            )
            setattr(blddk__zqc, f'block_{nzryt__ouzwy}', srjol__uua.value)
        blddk__zqc.len = builder.load(lvz__ybjg)
        return blddk__zqc._getvalue()
    return vjhz__rff(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def cpp_table_to_py_data(cpp_table, out_col_inds_t, out_types_t, n_rows_t,
    n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
    plng__doy = out_col_inds_t.instance_type.meta
    vjhz__rff = unwrap_typeref(out_types_t.types[0])
    nezej__vhhak = [unwrap_typeref(out_types_t.types[tlbo__qdtcs]) for
        tlbo__qdtcs in range(1, len(out_types_t.types))]
    xsdd__erdz = {}
    yfcf__mnqk = get_overload_const_int(n_table_cols_t)
    xfi__wgv = {tyrpu__bfgo: tlbo__qdtcs for tlbo__qdtcs, tyrpu__bfgo in
        enumerate(plng__doy)}
    if not is_overload_none(unknown_cat_arrs_t):
        afj__whegz = {esoo__oyxos: tlbo__qdtcs for tlbo__qdtcs, esoo__oyxos in
            enumerate(cat_inds_t.instance_type.meta)}
    owx__jxex = []
    txobm__tibi = """def impl(cpp_table, out_col_inds_t, out_types_t, n_rows_t, n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
"""
    if isinstance(vjhz__rff, bodo.TableType):
        txobm__tibi += f'  py_table = init_table(py_table_type, False)\n'
        txobm__tibi += f'  py_table = set_table_len(py_table, n_rows_t)\n'
        for jciq__suy, nzryt__ouzwy in vjhz__rff.type_to_blk.items():
            eed__xsj = [xfi__wgv.get(tlbo__qdtcs, -1) for tlbo__qdtcs in
                vjhz__rff.block_to_arr_ind[nzryt__ouzwy]]
            xsdd__erdz[f'out_inds_{nzryt__ouzwy}'] = np.array(eed__xsj, np.
                int64)
            xsdd__erdz[f'out_type_{nzryt__ouzwy}'] = jciq__suy
            xsdd__erdz[f'typ_list_{nzryt__ouzwy}'] = types.List(jciq__suy)
            swg__uikyl = f'out_type_{nzryt__ouzwy}'
            if type_has_unknown_cats(jciq__suy):
                if is_overload_none(unknown_cat_arrs_t):
                    txobm__tibi += f"""  in_arr_list_{nzryt__ouzwy} = get_table_block(out_types_t[0], {nzryt__ouzwy})
"""
                    swg__uikyl = f'in_arr_list_{nzryt__ouzwy}[i]'
                else:
                    xsdd__erdz[f'cat_arr_inds_{nzryt__ouzwy}'] = np.array([
                        afj__whegz.get(tlbo__qdtcs, -1) for tlbo__qdtcs in
                        vjhz__rff.block_to_arr_ind[nzryt__ouzwy]], np.int64)
                    swg__uikyl = (
                        f'unknown_cat_arrs_t[cat_arr_inds_{nzryt__ouzwy}[i]]')
            mcsx__pwp = len(vjhz__rff.block_to_arr_ind[nzryt__ouzwy])
            txobm__tibi += f"""  arr_list_{nzryt__ouzwy} = alloc_list_like(typ_list_{nzryt__ouzwy}, {mcsx__pwp}, False)
"""
            txobm__tibi += f'  for i in range(len(arr_list_{nzryt__ouzwy})):\n'
            txobm__tibi += (
                f'    cpp_ind_{nzryt__ouzwy} = out_inds_{nzryt__ouzwy}[i]\n')
            txobm__tibi += f'    if cpp_ind_{nzryt__ouzwy} == -1:\n'
            txobm__tibi += f'      continue\n'
            txobm__tibi += f"""    arr_{nzryt__ouzwy} = info_to_array(info_from_table(cpp_table, cpp_ind_{nzryt__ouzwy}), {swg__uikyl})
"""
            txobm__tibi += (
                f'    arr_list_{nzryt__ouzwy}[i] = arr_{nzryt__ouzwy}\n')
            txobm__tibi += f"""  py_table = set_table_block(py_table, arr_list_{nzryt__ouzwy}, {nzryt__ouzwy})
"""
        owx__jxex.append('py_table')
    elif vjhz__rff != types.none:
        pbrdb__gykwu = xfi__wgv.get(0, -1)
        if pbrdb__gykwu != -1:
            xsdd__erdz[f'arr_typ_arg0'] = vjhz__rff
            swg__uikyl = f'arr_typ_arg0'
            if type_has_unknown_cats(vjhz__rff):
                if is_overload_none(unknown_cat_arrs_t):
                    swg__uikyl = f'out_types_t[0]'
                else:
                    swg__uikyl = f'unknown_cat_arrs_t[{afj__whegz[0]}]'
            txobm__tibi += f"""  out_arg0 = info_to_array(info_from_table(cpp_table, {pbrdb__gykwu}), {swg__uikyl})
"""
            owx__jxex.append('out_arg0')
    for tlbo__qdtcs, t in enumerate(nezej__vhhak):
        pbrdb__gykwu = xfi__wgv.get(yfcf__mnqk + tlbo__qdtcs, -1)
        if pbrdb__gykwu != -1:
            xsdd__erdz[f'extra_arr_type_{tlbo__qdtcs}'] = t
            swg__uikyl = f'extra_arr_type_{tlbo__qdtcs}'
            if type_has_unknown_cats(t):
                if is_overload_none(unknown_cat_arrs_t):
                    swg__uikyl = f'out_types_t[{tlbo__qdtcs + 1}]'
                else:
                    swg__uikyl = (
                        f'unknown_cat_arrs_t[{afj__whegz[yfcf__mnqk + tlbo__qdtcs]}]'
                        )
            txobm__tibi += f"""  out_{tlbo__qdtcs} = info_to_array(info_from_table(cpp_table, {pbrdb__gykwu}), {swg__uikyl})
"""
            owx__jxex.append(f'out_{tlbo__qdtcs}')
    fndxo__pqka = ',' if len(owx__jxex) == 1 else ''
    txobm__tibi += f"  return ({', '.join(owx__jxex)}{fndxo__pqka})\n"
    xsdd__erdz.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'out_col_inds': list(plng__doy), 'py_table_type': vjhz__rff})
    ebhyc__fghp = {}
    exec(txobm__tibi, xsdd__erdz, ebhyc__fghp)
    return ebhyc__fghp['impl']


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    vjhz__rff = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        py_table, lbb__ftxy = args
        vmsnb__lavp = cgutils.create_struct_proxy(vjhz__rff)(context,
            builder, py_table)
        if vjhz__rff.has_runtime_cols:
            qtuw__zjxc = lir.Constant(lir.IntType(64), 0)
            for nzryt__ouzwy, t in enumerate(vjhz__rff.arr_types):
                cgj__tgeow = getattr(vmsnb__lavp, f'block_{nzryt__ouzwy}')
                htjkj__rrpqs = ListInstance(context, builder, types.List(t),
                    cgj__tgeow)
                qtuw__zjxc = builder.add(qtuw__zjxc, htjkj__rrpqs.size)
        else:
            qtuw__zjxc = lir.Constant(lir.IntType(64), len(vjhz__rff.arr_types)
                )
        lbb__ftxy, jaxz__iln = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), qtuw__zjxc)
        jaxz__iln.size = qtuw__zjxc
        if vjhz__rff.has_runtime_cols:
            atlfc__wjh = lir.Constant(lir.IntType(64), 0)
            for nzryt__ouzwy, t in enumerate(vjhz__rff.arr_types):
                cgj__tgeow = getattr(vmsnb__lavp, f'block_{nzryt__ouzwy}')
                htjkj__rrpqs = ListInstance(context, builder, types.List(t),
                    cgj__tgeow)
                mcsx__pwp = htjkj__rrpqs.size
                with cgutils.for_range(builder, mcsx__pwp) as pvjwa__pungy:
                    tlbo__qdtcs = pvjwa__pungy.index
                    arr = htjkj__rrpqs.getitem(tlbo__qdtcs)
                    viixq__nyqjk = signature(array_info_type, t)
                    yblk__bmn = arr,
                    jim__bdkkb = array_to_info_codegen(context, builder,
                        viixq__nyqjk, yblk__bmn)
                    jaxz__iln.inititem(builder.add(atlfc__wjh, tlbo__qdtcs),
                        jim__bdkkb, incref=False)
                atlfc__wjh = builder.add(atlfc__wjh, mcsx__pwp)
        else:
            for t, nzryt__ouzwy in vjhz__rff.type_to_blk.items():
                mcsx__pwp = context.get_constant(types.int64, len(vjhz__rff
                    .block_to_arr_ind[nzryt__ouzwy]))
                cgj__tgeow = getattr(vmsnb__lavp, f'block_{nzryt__ouzwy}')
                htjkj__rrpqs = ListInstance(context, builder, types.List(t),
                    cgj__tgeow)
                ainf__cdxkv = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(vjhz__rff.
                    block_to_arr_ind[nzryt__ouzwy], dtype=np.int64))
                makq__lagsc = context.make_array(types.Array(types.int64, 1,
                    'C'))(context, builder, ainf__cdxkv)
                with cgutils.for_range(builder, mcsx__pwp) as pvjwa__pungy:
                    tlbo__qdtcs = pvjwa__pungy.index
                    ixhic__jffuz = _getitem_array_single_int(context,
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), makq__lagsc, tlbo__qdtcs)
                    vroy__ofj = signature(types.none, vjhz__rff, types.List
                        (t), types.int64, types.int64)
                    lvkz__ewm = py_table, cgj__tgeow, tlbo__qdtcs, ixhic__jffuz
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, vroy__ofj, lvkz__ewm)
                    arr = htjkj__rrpqs.getitem(tlbo__qdtcs)
                    viixq__nyqjk = signature(array_info_type, t)
                    yblk__bmn = arr,
                    jim__bdkkb = array_to_info_codegen(context, builder,
                        viixq__nyqjk, yblk__bmn)
                    jaxz__iln.inititem(ixhic__jffuz, jim__bdkkb, incref=False)
        lfp__jva = jaxz__iln.value
        djkr__ytafl = signature(table_type, types.List(array_info_type))
        hogyo__ughfo = lfp__jva,
        cpp_table = arr_info_list_to_table_codegen(context, builder,
            djkr__ytafl, hogyo__ughfo)
        context.nrt.decref(builder, types.List(array_info_type), lfp__jva)
        return cpp_table
    return table_type(vjhz__rff, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def py_data_to_cpp_table(py_table, extra_arrs_tup, in_col_inds_t,
    n_table_cols_t):
    wnvh__xjmdj = in_col_inds_t.instance_type.meta
    xsdd__erdz = {}
    yfcf__mnqk = get_overload_const_int(n_table_cols_t)
    afer__cqd = defaultdict(list)
    xfi__wgv = {}
    for tlbo__qdtcs, tyrpu__bfgo in enumerate(wnvh__xjmdj):
        if tyrpu__bfgo in xfi__wgv:
            afer__cqd[tyrpu__bfgo].append(tlbo__qdtcs)
        else:
            xfi__wgv[tyrpu__bfgo] = tlbo__qdtcs
    txobm__tibi = (
        'def impl(py_table, extra_arrs_tup, in_col_inds_t, n_table_cols_t):\n')
    txobm__tibi += (
        f'  cpp_arr_list = alloc_empty_list_type({len(wnvh__xjmdj)}, array_info_type)\n'
        )
    if py_table != types.none:
        for nzryt__ouzwy in py_table.type_to_blk.values():
            eed__xsj = [xfi__wgv.get(tlbo__qdtcs, -1) for tlbo__qdtcs in
                py_table.block_to_arr_ind[nzryt__ouzwy]]
            xsdd__erdz[f'out_inds_{nzryt__ouzwy}'] = np.array(eed__xsj, np.
                int64)
            xsdd__erdz[f'arr_inds_{nzryt__ouzwy}'] = np.array(py_table.
                block_to_arr_ind[nzryt__ouzwy], np.int64)
            txobm__tibi += f"""  arr_list_{nzryt__ouzwy} = get_table_block(py_table, {nzryt__ouzwy})
"""
            txobm__tibi += f'  for i in range(len(arr_list_{nzryt__ouzwy})):\n'
            txobm__tibi += (
                f'    out_arr_ind_{nzryt__ouzwy} = out_inds_{nzryt__ouzwy}[i]\n'
                )
            txobm__tibi += f'    if out_arr_ind_{nzryt__ouzwy} == -1:\n'
            txobm__tibi += f'      continue\n'
            txobm__tibi += (
                f'    arr_ind_{nzryt__ouzwy} = arr_inds_{nzryt__ouzwy}[i]\n')
            txobm__tibi += f"""    ensure_column_unboxed(py_table, arr_list_{nzryt__ouzwy}, i, arr_ind_{nzryt__ouzwy})
"""
            txobm__tibi += f"""    cpp_arr_list[out_arr_ind_{nzryt__ouzwy}] = array_to_info(arr_list_{nzryt__ouzwy}[i])
"""
        for gnuh__lkia, nijr__vcx in afer__cqd.items():
            if gnuh__lkia < yfcf__mnqk:
                nzryt__ouzwy = py_table.block_nums[gnuh__lkia]
                gbetu__xtc = py_table.block_offsets[gnuh__lkia]
                for pbrdb__gykwu in nijr__vcx:
                    txobm__tibi += f"""  cpp_arr_list[{pbrdb__gykwu}] = array_to_info(arr_list_{nzryt__ouzwy}[{gbetu__xtc}])
"""
    for tlbo__qdtcs in range(len(extra_arrs_tup)):
        yjzql__xzmq = xfi__wgv.get(yfcf__mnqk + tlbo__qdtcs, -1)
        if yjzql__xzmq != -1:
            quhw__olv = [yjzql__xzmq] + afer__cqd.get(yfcf__mnqk +
                tlbo__qdtcs, [])
            for pbrdb__gykwu in quhw__olv:
                txobm__tibi += f"""  cpp_arr_list[{pbrdb__gykwu}] = array_to_info(extra_arrs_tup[{tlbo__qdtcs}])
"""
    txobm__tibi += f'  return arr_info_list_to_table(cpp_arr_list)\n'
    xsdd__erdz.update({'array_info_type': array_info_type,
        'alloc_empty_list_type': bodo.hiframes.table.alloc_empty_list_type,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'ensure_column_unboxed': bodo.hiframes.table.ensure_column_unboxed,
        'array_to_info': array_to_info, 'arr_info_list_to_table':
        arr_info_list_to_table})
    ebhyc__fghp = {}
    exec(txobm__tibi, xsdd__erdz, ebhyc__fghp)
    return ebhyc__fghp['impl']


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
        bley__kda = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='delete_table')
        builder.call(uhh__nmas, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='shuffle_table')
        xmk__vhy = builder.call(uhh__nmas, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xmk__vhy
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
        bley__kda = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='delete_shuffle_info')
        return builder.call(uhh__nmas, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='reverse_shuffle_table')
        return builder.call(uhh__nmas, args)
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
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(64), lir.IntType(8).as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='hash_join_table')
        xmk__vhy = builder.call(uhh__nmas, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xmk__vhy
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
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64), lir.
            IntType(8).as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='cross_join_table')
        xmk__vhy = builder.call(uhh__nmas, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return xmk__vhy
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.boolean, types.boolean, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.int64, types.voidptr, types.
        int64, types.voidptr), codegen


@intrinsic
def sort_values_table(typingctx, table_t, n_keys_t, vect_ascending_t,
    na_position_b_t, dead_keys_t, n_rows_t, bounds_t, parallel_t):
    assert table_t == table_type, 'C++ table type expected'

    def codegen(context, builder, sig, args):
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1)])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='sort_values_table')
        xmk__vhy = builder.call(uhh__nmas, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xmk__vhy
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='sample_table')
        xmk__vhy = builder.call(uhh__nmas, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xmk__vhy
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='shuffle_renormalization')
        xmk__vhy = builder.call(uhh__nmas, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xmk__vhy
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='shuffle_renormalization_group')
        xmk__vhy = builder.call(uhh__nmas, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xmk__vhy
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='drop_duplicates_table')
        xmk__vhy = builder.call(uhh__nmas, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xmk__vhy
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
        bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        uhh__nmas = cgutils.get_or_insert_function(builder.module,
            bley__kda, name='groupby_and_aggregate')
        xmk__vhy = builder.call(uhh__nmas, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return xmk__vhy
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
    pxytl__mzdqn = array_to_info(dict_arr)
    _drop_duplicates_local_dictionary(pxytl__mzdqn, sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(pxytl__mzdqn, bodo.dict_str_arr_type)
    return out_arr


_convert_local_dictionary_to_global = types.ExternalFunction(
    'convert_local_dictionary_to_global', types.void(array_info_type, types
    .bool_, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def convert_local_dictionary_to_global(dict_arr, sort_dictionary,
    is_parallel=False):
    pxytl__mzdqn = array_to_info(dict_arr)
    _convert_local_dictionary_to_global(pxytl__mzdqn, is_parallel,
        sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(pxytl__mzdqn, bodo.dict_str_arr_type)
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
    uowhw__sqeg = array_to_info(in_arr)
    amot__hqzul = array_to_info(in_values)
    czaxn__tdjc = array_to_info(out_arr)
    chi__hfciv = arr_info_list_to_table([uowhw__sqeg, amot__hqzul, czaxn__tdjc]
        )
    _array_isin(czaxn__tdjc, uowhw__sqeg, amot__hqzul, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(chi__hfciv)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, match, pat, out_arr):
    uowhw__sqeg = array_to_info(in_arr)
    czaxn__tdjc = array_to_info(out_arr)
    _get_search_regex(uowhw__sqeg, case, match, pat, czaxn__tdjc)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    bvn__mjn = col_array_typ.dtype
    if isinstance(bvn__mjn, (types.Number, TimeType, bodo.libs.
        pd_datetime_arr_ext.PandasDatetimeTZDtype)) or bvn__mjn in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:
        if isinstance(bvn__mjn, bodo.libs.pd_datetime_arr_ext.
            PandasDatetimeTZDtype):
            bvn__mjn = bodo.datetime64ns

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                blddk__zqc, viskb__cow = args
                blddk__zqc = builder.bitcast(blddk__zqc, lir.IntType(8).
                    as_pointer().as_pointer())
                athe__mwf = lir.Constant(lir.IntType(64), c_ind)
                vldu__gbio = builder.load(builder.gep(blddk__zqc, [athe__mwf]))
                vldu__gbio = builder.bitcast(vldu__gbio, context.
                    get_data_type(bvn__mjn).as_pointer())
                return context.unpack_value(builder, bvn__mjn, builder.gep(
                    vldu__gbio, [viskb__cow]))
            return bvn__mjn(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ in (bodo.string_array_type, bodo.binary_array_type):

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                blddk__zqc, viskb__cow = args
                blddk__zqc = builder.bitcast(blddk__zqc, lir.IntType(8).
                    as_pointer().as_pointer())
                athe__mwf = lir.Constant(lir.IntType(64), c_ind)
                vldu__gbio = builder.load(builder.gep(blddk__zqc, [athe__mwf]))
                bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                uyzha__mvw = cgutils.get_or_insert_function(builder.module,
                    bley__kda, name='array_info_getitem')
                wzuw__xqr = cgutils.alloca_once(builder, lir.IntType(64))
                args = vldu__gbio, viskb__cow, wzuw__xqr
                qkya__ygnu = builder.call(uyzha__mvw, args)
                totmf__tcef = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    totmf__tcef, [qkya__ygnu, builder.load(wzuw__xqr)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                scu__ghgjd = lir.Constant(lir.IntType(64), 1)
                hnk__rlq = lir.Constant(lir.IntType(64), 2)
                blddk__zqc, viskb__cow = args
                blddk__zqc = builder.bitcast(blddk__zqc, lir.IntType(8).
                    as_pointer().as_pointer())
                athe__mwf = lir.Constant(lir.IntType(64), c_ind)
                vldu__gbio = builder.load(builder.gep(blddk__zqc, [athe__mwf]))
                bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64)])
                clea__ssahv = cgutils.get_or_insert_function(builder.module,
                    bley__kda, name='get_nested_info')
                args = vldu__gbio, hnk__rlq
                ptiiz__ealnd = builder.call(clea__ssahv, args)
                bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer()])
                qzao__jju = cgutils.get_or_insert_function(builder.module,
                    bley__kda, name='array_info_getdata1')
                args = ptiiz__ealnd,
                hnpdw__xcvc = builder.call(qzao__jju, args)
                hnpdw__xcvc = builder.bitcast(hnpdw__xcvc, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                zkowb__ydlfh = builder.sext(builder.load(builder.gep(
                    hnpdw__xcvc, [viskb__cow])), lir.IntType(64))
                args = vldu__gbio, scu__ghgjd
                syaj__qhe = builder.call(clea__ssahv, args)
                bley__kda = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                uyzha__mvw = cgutils.get_or_insert_function(builder.module,
                    bley__kda, name='array_info_getitem')
                wzuw__xqr = cgutils.alloca_once(builder, lir.IntType(64))
                args = syaj__qhe, zkowb__ydlfh, wzuw__xqr
                qkya__ygnu = builder.call(uyzha__mvw, args)
                totmf__tcef = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    totmf__tcef, [qkya__ygnu, builder.load(wzuw__xqr)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{bvn__mjn}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if isinstance(col_array_dtype, (IntegerArrayType, FloatingArrayType,
        bodo.TimeArrayType)) or col_array_dtype in (bodo.libs.bool_arr_ext.
        boolean_array, bodo.binary_array_type, bodo.datetime_date_array_type
        ) or is_str_arr_type(col_array_dtype):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                rfa__bphq, viskb__cow = args
                rfa__bphq = builder.bitcast(rfa__bphq, lir.IntType(8).
                    as_pointer().as_pointer())
                athe__mwf = lir.Constant(lir.IntType(64), c_ind)
                vldu__gbio = builder.load(builder.gep(rfa__bphq, [athe__mwf]))
                xrv__kgtea = builder.bitcast(vldu__gbio, context.
                    get_data_type(types.bool_).as_pointer())
                bev__xthtq = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    xrv__kgtea, viskb__cow)
                pdj__auf = builder.icmp_unsigned('!=', bev__xthtq, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(pdj__auf, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, (types.Array, bodo.DatetimeArrayType)):
        bvn__mjn = col_array_dtype.dtype
        if bvn__mjn in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            bvn__mjn, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype):
            if isinstance(bvn__mjn, bodo.libs.pd_datetime_arr_ext.
                PandasDatetimeTZDtype):
                bvn__mjn = bodo.datetime64ns

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    blddk__zqc, viskb__cow = args
                    blddk__zqc = builder.bitcast(blddk__zqc, lir.IntType(8)
                        .as_pointer().as_pointer())
                    athe__mwf = lir.Constant(lir.IntType(64), c_ind)
                    vldu__gbio = builder.load(builder.gep(blddk__zqc, [
                        athe__mwf]))
                    vldu__gbio = builder.bitcast(vldu__gbio, context.
                        get_data_type(bvn__mjn).as_pointer())
                    yuwq__skv = builder.load(builder.gep(vldu__gbio, [
                        viskb__cow]))
                    pdj__auf = builder.icmp_unsigned('!=', yuwq__skv, lir.
                        Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(pdj__auf, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(bvn__mjn, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    blddk__zqc, viskb__cow = args
                    blddk__zqc = builder.bitcast(blddk__zqc, lir.IntType(8)
                        .as_pointer().as_pointer())
                    athe__mwf = lir.Constant(lir.IntType(64), c_ind)
                    vldu__gbio = builder.load(builder.gep(blddk__zqc, [
                        athe__mwf]))
                    vldu__gbio = builder.bitcast(vldu__gbio, context.
                        get_data_type(bvn__mjn).as_pointer())
                    yuwq__skv = builder.load(builder.gep(vldu__gbio, [
                        viskb__cow]))
                    eiik__bvj = signature(types.bool_, bvn__mjn)
                    bev__xthtq = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, eiik__bvj, (yuwq__skv,))
                    return builder.not_(builder.sext(bev__xthtq, lir.
                        IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
