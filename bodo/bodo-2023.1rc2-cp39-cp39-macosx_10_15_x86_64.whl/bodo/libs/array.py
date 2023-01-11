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
        mtfyq__mkk = context.make_helper(builder, arr_type, in_arr)
        in_arr = mtfyq__mkk.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        mnsfh__wvzf = context.make_helper(builder, arr_type, in_arr)
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='list_string_array_to_info')
        return builder.call(gap__wxr, [mnsfh__wvzf.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                qonsu__zplr = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for pzcvd__ifq in arr_typ.data:
                    qonsu__zplr += get_types(pzcvd__ifq)
                return qonsu__zplr
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
                zuc__tddkg = context.make_helper(builder, arr_typ, value=arr)
                ppl__dngd = get_lengths(_get_map_arr_data_type(arr_typ),
                    zuc__tddkg.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                tno__qhxb = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                ppl__dngd = get_lengths(arr_typ.dtype, tno__qhxb.data)
                ppl__dngd = cgutils.pack_array(builder, [tno__qhxb.n_arrays
                    ] + [builder.extract_value(ppl__dngd, gybyh__qvrzi) for
                    gybyh__qvrzi in range(ppl__dngd.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                tno__qhxb = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                ppl__dngd = []
                for gybyh__qvrzi, pzcvd__ifq in enumerate(arr_typ.data):
                    atkl__jgvs = get_lengths(pzcvd__ifq, builder.
                        extract_value(tno__qhxb.data, gybyh__qvrzi))
                    ppl__dngd += [builder.extract_value(atkl__jgvs,
                        pckc__fxcjo) for pckc__fxcjo in range(atkl__jgvs.
                        type.count)]
                ppl__dngd = cgutils.pack_array(builder, [length, context.
                    get_constant(types.int64, -1)] + ppl__dngd)
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType, types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                ppl__dngd = cgutils.pack_array(builder, [length])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return ppl__dngd

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                zuc__tddkg = context.make_helper(builder, arr_typ, value=arr)
                yehc__sdvj = get_buffers(_get_map_arr_data_type(arr_typ),
                    zuc__tddkg.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                tno__qhxb = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                tdn__gmv = get_buffers(arr_typ.dtype, tno__qhxb.data)
                ptnt__rxxro = context.make_array(types.Array(offset_type, 1,
                    'C'))(context, builder, tno__qhxb.offsets)
                qtwqs__mvjyn = builder.bitcast(ptnt__rxxro.data, lir.
                    IntType(8).as_pointer())
                ojbwg__vnm = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, tno__qhxb.null_bitmap)
                eqh__oqaq = builder.bitcast(ojbwg__vnm.data, lir.IntType(8)
                    .as_pointer())
                yehc__sdvj = cgutils.pack_array(builder, [qtwqs__mvjyn,
                    eqh__oqaq] + [builder.extract_value(tdn__gmv,
                    gybyh__qvrzi) for gybyh__qvrzi in range(tdn__gmv.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                tno__qhxb = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                tdn__gmv = []
                for gybyh__qvrzi, pzcvd__ifq in enumerate(arr_typ.data):
                    omcd__qkj = get_buffers(pzcvd__ifq, builder.
                        extract_value(tno__qhxb.data, gybyh__qvrzi))
                    tdn__gmv += [builder.extract_value(omcd__qkj,
                        pckc__fxcjo) for pckc__fxcjo in range(omcd__qkj.
                        type.count)]
                ojbwg__vnm = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, tno__qhxb.null_bitmap)
                eqh__oqaq = builder.bitcast(ojbwg__vnm.data, lir.IntType(8)
                    .as_pointer())
                yehc__sdvj = cgutils.pack_array(builder, [eqh__oqaq] + tdn__gmv
                    )
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType)) or arr_typ in (boolean_array,
                datetime_date_array_type):
                bdu__nnt = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    bdu__nnt = int128_type
                elif arr_typ == datetime_date_array_type:
                    bdu__nnt = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                cpmc__oeihl = context.make_array(types.Array(bdu__nnt, 1, 'C')
                    )(context, builder, arr.data)
                ojbwg__vnm = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, arr.null_bitmap)
                qyj__zrv = builder.bitcast(cpmc__oeihl.data, lir.IntType(8)
                    .as_pointer())
                eqh__oqaq = builder.bitcast(ojbwg__vnm.data, lir.IntType(8)
                    .as_pointer())
                yehc__sdvj = cgutils.pack_array(builder, [eqh__oqaq, qyj__zrv])
            elif arr_typ in (string_array_type, binary_array_type):
                tno__qhxb = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                ocbj__tmlw = context.make_helper(builder, offset_arr_type,
                    tno__qhxb.offsets).data
                data = context.make_helper(builder, char_arr_type,
                    tno__qhxb.data).data
                qkxj__urwbp = context.make_helper(builder,
                    null_bitmap_arr_type, tno__qhxb.null_bitmap).data
                yehc__sdvj = cgutils.pack_array(builder, [builder.bitcast(
                    ocbj__tmlw, lir.IntType(8).as_pointer()), builder.
                    bitcast(qkxj__urwbp, lir.IntType(8).as_pointer()),
                    builder.bitcast(data, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                qyj__zrv = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                mvz__ell = lir.Constant(lir.IntType(8).as_pointer(), None)
                yehc__sdvj = cgutils.pack_array(builder, [mvz__ell, qyj__zrv])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return yehc__sdvj

        def get_field_names(arr_typ):
            cigeu__fiex = []
            if isinstance(arr_typ, StructArrayType):
                for jgpm__bhoyl, ikida__gnrna in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    cigeu__fiex.append(jgpm__bhoyl)
                    cigeu__fiex += get_field_names(ikida__gnrna)
            elif isinstance(arr_typ, ArrayItemArrayType):
                cigeu__fiex += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                cigeu__fiex += get_field_names(_get_map_arr_data_type(arr_typ))
            return cigeu__fiex
        qonsu__zplr = get_types(arr_type)
        umfiu__ndgu = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in qonsu__zplr])
        ncp__dlvze = cgutils.alloca_once_value(builder, umfiu__ndgu)
        ppl__dngd = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, ppl__dngd)
        yehc__sdvj = get_buffers(arr_type, in_arr)
        fnr__bjof = cgutils.alloca_once_value(builder, yehc__sdvj)
        cigeu__fiex = get_field_names(arr_type)
        if len(cigeu__fiex) == 0:
            cigeu__fiex = ['irrelevant']
        shvi__hjmf = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in cigeu__fiex])
        ryyb__wyh = cgutils.alloca_once_value(builder, shvi__hjmf)
        if isinstance(arr_type, MapArrayType):
            epq__zqnh = _get_map_arr_data_type(arr_type)
            ahjfz__jljh = context.make_helper(builder, arr_type, value=in_arr)
            beecp__ngyp = ahjfz__jljh.data
        else:
            epq__zqnh = arr_type
            beecp__ngyp = in_arr
        rlwof__suviw = context.make_helper(builder, epq__zqnh, beecp__ngyp)
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='nested_array_to_info')
        hot__jnsb = builder.call(gap__wxr, [builder.bitcast(ncp__dlvze, lir
            .IntType(32).as_pointer()), builder.bitcast(fnr__bjof, lir.
            IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            ryyb__wyh, lir.IntType(8).as_pointer()), rlwof__suviw.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return hot__jnsb
    if arr_type in (string_array_type, binary_array_type):
        whw__phcx = context.make_helper(builder, arr_type, in_arr)
        vyxyd__xbj = ArrayItemArrayType(char_arr_type)
        mnsfh__wvzf = context.make_helper(builder, vyxyd__xbj, whw__phcx.data)
        tno__qhxb = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        ocbj__tmlw = context.make_helper(builder, offset_arr_type,
            tno__qhxb.offsets).data
        data = context.make_helper(builder, char_arr_type, tno__qhxb.data).data
        qkxj__urwbp = context.make_helper(builder, null_bitmap_arr_type,
            tno__qhxb.null_bitmap).data
        eosxt__fko = builder.zext(builder.load(builder.gep(ocbj__tmlw, [
            tno__qhxb.n_arrays])), lir.IntType(64))
        hap__iqk = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='string_array_to_info')
        return builder.call(gap__wxr, [tno__qhxb.n_arrays, eosxt__fko, data,
            ocbj__tmlw, qkxj__urwbp, mnsfh__wvzf.meminfo, hap__iqk])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        rzwg__prmnv = arr.data
        bzdm__bcn = arr.indices
        sig = array_info_type(arr_type.data)
        nup__ivpt = array_to_info_codegen(context, builder, sig, (
            rzwg__prmnv,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        eaeyz__xmmnx = array_to_info_codegen(context, builder, sig, (
            bzdm__bcn,), False)
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(32), lir.IntType(32)])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='dict_str_array_to_info')
        bho__dqjg = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        iro__brsq = builder.zext(arr.has_deduped_local_dictionary, lir.
            IntType(32))
        return builder.call(gap__wxr, [nup__ivpt, eaeyz__xmmnx, bho__dqjg,
            iro__brsq])
    liaba__tilp = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        kqie__ukha = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        rpni__qme = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(rpni__qme, 1, 'C')
        liaba__tilp = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if liaba__tilp:
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
        lfu__eikp = arr_type.dtype
        gwv__ssei = numba_to_c_type(lfu__eikp)
        njym__nhnx = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), gwv__ssei))
        if liaba__tilp:
            udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(64), lir.IntType(8).as_pointer()])
            gap__wxr = cgutils.get_or_insert_function(builder.module,
                udiqd__sqd, name='categorical_array_to_info')
            return builder.call(gap__wxr, [length, builder.bitcast(arr.data,
                lir.IntType(8).as_pointer()), builder.load(njym__nhnx),
                kqie__ukha, arr.meminfo])
        else:
            udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer()])
            gap__wxr = cgutils.get_or_insert_function(builder.module,
                udiqd__sqd, name='numpy_array_to_info')
            return builder.call(gap__wxr, [length, builder.bitcast(arr.data,
                lir.IntType(8).as_pointer()), builder.load(njym__nhnx), arr
                .meminfo])
    if isinstance(arr_type, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, TimeArrayType)) or arr_type in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        lfu__eikp = arr_type.dtype
        bdu__nnt = lfu__eikp
        if isinstance(arr_type, DecimalArrayType):
            bdu__nnt = int128_type
        if arr_type == datetime_date_array_type:
            bdu__nnt = types.int64
        cpmc__oeihl = context.make_array(types.Array(bdu__nnt, 1, 'C'))(context
            , builder, arr.data)
        length = builder.extract_value(cpmc__oeihl.shape, 0)
        unmw__rbix = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        gwv__ssei = numba_to_c_type(lfu__eikp)
        njym__nhnx = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), gwv__ssei))
        if isinstance(arr_type, DecimalArrayType):
            udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
            gap__wxr = cgutils.get_or_insert_function(builder.module,
                udiqd__sqd, name='decimal_array_to_info')
            return builder.call(gap__wxr, [length, builder.bitcast(
                cpmc__oeihl.data, lir.IntType(8).as_pointer()), builder.
                load(njym__nhnx), builder.bitcast(unmw__rbix.data, lir.
                IntType(8).as_pointer()), cpmc__oeihl.meminfo, unmw__rbix.
                meminfo, context.get_constant(types.int32, arr_type.
                precision), context.get_constant(types.int32, arr_type.scale)])
        elif isinstance(arr_type, TimeArrayType):
            udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32)])
            gap__wxr = cgutils.get_or_insert_function(builder.module,
                udiqd__sqd, name='time_array_to_info')
            return builder.call(gap__wxr, [length, builder.bitcast(
                cpmc__oeihl.data, lir.IntType(8).as_pointer()), builder.
                load(njym__nhnx), builder.bitcast(unmw__rbix.data, lir.
                IntType(8).as_pointer()), cpmc__oeihl.meminfo, unmw__rbix.
                meminfo, lir.Constant(lir.IntType(32), arr_type.precision)])
        else:
            udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer()])
            gap__wxr = cgutils.get_or_insert_function(builder.module,
                udiqd__sqd, name='nullable_array_to_info')
            return builder.call(gap__wxr, [length, builder.bitcast(
                cpmc__oeihl.data, lir.IntType(8).as_pointer()), builder.
                load(njym__nhnx), builder.bitcast(unmw__rbix.data, lir.
                IntType(8).as_pointer()), cpmc__oeihl.meminfo, unmw__rbix.
                meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        lnpl__jfror = context.make_array(arr_type.arr_type)(context,
            builder, arr.left)
        lzr__ktwb = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        length = builder.extract_value(lnpl__jfror.shape, 0)
        gwv__ssei = numba_to_c_type(arr_type.arr_type.dtype)
        njym__nhnx = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), gwv__ssei))
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='interval_array_to_info')
        return builder.call(gap__wxr, [length, builder.bitcast(lnpl__jfror.
            data, lir.IntType(8).as_pointer()), builder.bitcast(lzr__ktwb.
            data, lir.IntType(8).as_pointer()), builder.load(njym__nhnx),
            lnpl__jfror.meminfo, lzr__ktwb.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    brxci__meprj = cgutils.alloca_once(builder, lir.IntType(64))
    qyj__zrv = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    ddxhr__mddy = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    udiqd__sqd = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    gap__wxr = cgutils.get_or_insert_function(builder.module, udiqd__sqd,
        name='info_to_numpy_array')
    builder.call(gap__wxr, [in_info, brxci__meprj, qyj__zrv, ddxhr__mddy])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    ridx__qepgc = context.get_value_type(types.intp)
    dqs__kncte = cgutils.pack_array(builder, [builder.load(brxci__meprj)],
        ty=ridx__qepgc)
    noivm__vvgd = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    tdm__tpmgs = cgutils.pack_array(builder, [noivm__vvgd], ty=ridx__qepgc)
    data = builder.bitcast(builder.load(qyj__zrv), context.get_data_type(
        arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=data, shape=dqs__kncte,
        strides=tdm__tpmgs, itemsize=noivm__vvgd, meminfo=builder.load(
        ddxhr__mddy))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    doq__uat = context.make_helper(builder, arr_type)
    udiqd__sqd = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    gap__wxr = cgutils.get_or_insert_function(builder.module, udiqd__sqd,
        name='info_to_list_string_array')
    builder.call(gap__wxr, [in_info, doq__uat._get_ptr_by_name('meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return doq__uat._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    quh__xelv = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        tyjr__ptb = lengths_pos
        ixncs__cvx = infos_pos
        vvhfe__htys, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        ntgzl__moa = ArrayItemArrayPayloadType(arr_typ)
        vvb__fook = context.get_data_type(ntgzl__moa)
        ewps__ikzw = context.get_abi_sizeof(vvb__fook)
        ahzu__vkvyh = define_array_item_dtor(context, builder, arr_typ,
            ntgzl__moa)
        jfbt__wqj = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, ewps__ikzw), ahzu__vkvyh)
        gaff__hkjok = context.nrt.meminfo_data(builder, jfbt__wqj)
        awn__mqnqu = builder.bitcast(gaff__hkjok, vvb__fook.as_pointer())
        tno__qhxb = cgutils.create_struct_proxy(ntgzl__moa)(context, builder)
        tno__qhxb.n_arrays = builder.extract_value(builder.load(lengths_ptr
            ), tyjr__ptb)
        tno__qhxb.data = vvhfe__htys
        zpmth__nkro = builder.load(array_infos_ptr)
        lzw__yfxhn = builder.bitcast(builder.extract_value(zpmth__nkro,
            ixncs__cvx), quh__xelv)
        tno__qhxb.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, lzw__yfxhn)
        cgjdh__uqvnd = builder.bitcast(builder.extract_value(zpmth__nkro, 
            ixncs__cvx + 1), quh__xelv)
        tno__qhxb.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, cgjdh__uqvnd)
        builder.store(tno__qhxb._getvalue(), awn__mqnqu)
        mnsfh__wvzf = context.make_helper(builder, arr_typ)
        mnsfh__wvzf.meminfo = jfbt__wqj
        return mnsfh__wvzf._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        emov__ioma = []
        ixncs__cvx = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for rxat__wyc in arr_typ.data:
            vvhfe__htys, lengths_pos, infos_pos = nested_to_array(context,
                builder, rxat__wyc, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            emov__ioma.append(vvhfe__htys)
        ntgzl__moa = StructArrayPayloadType(arr_typ.data)
        vvb__fook = context.get_value_type(ntgzl__moa)
        ewps__ikzw = context.get_abi_sizeof(vvb__fook)
        ahzu__vkvyh = define_struct_arr_dtor(context, builder, arr_typ,
            ntgzl__moa)
        jfbt__wqj = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, ewps__ikzw), ahzu__vkvyh)
        gaff__hkjok = context.nrt.meminfo_data(builder, jfbt__wqj)
        awn__mqnqu = builder.bitcast(gaff__hkjok, vvb__fook.as_pointer())
        tno__qhxb = cgutils.create_struct_proxy(ntgzl__moa)(context, builder)
        tno__qhxb.data = cgutils.pack_array(builder, emov__ioma
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, emov__ioma)
        zpmth__nkro = builder.load(array_infos_ptr)
        cgjdh__uqvnd = builder.bitcast(builder.extract_value(zpmth__nkro,
            ixncs__cvx), quh__xelv)
        tno__qhxb.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, cgjdh__uqvnd)
        builder.store(tno__qhxb._getvalue(), awn__mqnqu)
        lhb__kava = context.make_helper(builder, arr_typ)
        lhb__kava.meminfo = jfbt__wqj
        return lhb__kava._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        zpmth__nkro = builder.load(array_infos_ptr)
        hwonl__pvdn = builder.bitcast(builder.extract_value(zpmth__nkro,
            infos_pos), quh__xelv)
        whw__phcx = context.make_helper(builder, arr_typ)
        vyxyd__xbj = ArrayItemArrayType(char_arr_type)
        mnsfh__wvzf = context.make_helper(builder, vyxyd__xbj)
        udiqd__sqd = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='info_to_string_array')
        builder.call(gap__wxr, [hwonl__pvdn, mnsfh__wvzf._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        whw__phcx.data = mnsfh__wvzf._getvalue()
        return whw__phcx._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        zpmth__nkro = builder.load(array_infos_ptr)
        nko__aheen = builder.bitcast(builder.extract_value(zpmth__nkro, 
            infos_pos + 1), quh__xelv)
        return _lower_info_to_array_numpy(arr_typ, context, builder, nko__aheen
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType)) or arr_typ in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        bdu__nnt = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            bdu__nnt = int128_type
        elif arr_typ == datetime_date_array_type:
            bdu__nnt = types.int64
        zpmth__nkro = builder.load(array_infos_ptr)
        cgjdh__uqvnd = builder.bitcast(builder.extract_value(zpmth__nkro,
            infos_pos), quh__xelv)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, cgjdh__uqvnd)
        nko__aheen = builder.bitcast(builder.extract_value(zpmth__nkro, 
            infos_pos + 1), quh__xelv)
        arr.data = _lower_info_to_array_numpy(types.Array(bdu__nnt, 1, 'C'),
            context, builder, nko__aheen)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, zfkcg__tcies = args
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
                return 1 + sum([get_num_arrays(rxat__wyc) for rxat__wyc in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(rxat__wyc) for rxat__wyc in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            eqx__kfjrk = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            eqx__kfjrk = _get_map_arr_data_type(arr_type)
        else:
            eqx__kfjrk = arr_type
        tnfuh__wis = get_num_arrays(eqx__kfjrk)
        ppl__dngd = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), 0) for zfkcg__tcies in range(tnfuh__wis)])
        lengths_ptr = cgutils.alloca_once_value(builder, ppl__dngd)
        mvz__ell = lir.Constant(lir.IntType(8).as_pointer(), None)
        czilb__qwwbb = cgutils.pack_array(builder, [mvz__ell for
            zfkcg__tcies in range(get_num_infos(eqx__kfjrk))])
        array_infos_ptr = cgutils.alloca_once_value(builder, czilb__qwwbb)
        udiqd__sqd = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='info_to_nested_array')
        builder.call(gap__wxr, [in_info, builder.bitcast(lengths_ptr, lir.
            IntType(64).as_pointer()), builder.bitcast(array_infos_ptr, lir
            .IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, zfkcg__tcies, zfkcg__tcies = nested_to_array(context, builder,
            eqx__kfjrk, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            mtfyq__mkk = context.make_helper(builder, arr_type)
            mtfyq__mkk.data = arr
            context.nrt.incref(builder, eqx__kfjrk, arr)
            arr = mtfyq__mkk._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, eqx__kfjrk)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        whw__phcx = context.make_helper(builder, arr_type)
        vyxyd__xbj = ArrayItemArrayType(char_arr_type)
        mnsfh__wvzf = context.make_helper(builder, vyxyd__xbj)
        udiqd__sqd = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='info_to_string_array')
        builder.call(gap__wxr, [in_info, mnsfh__wvzf._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        whw__phcx.data = mnsfh__wvzf._getvalue()
        return whw__phcx._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='get_nested_info')
        nup__ivpt = builder.call(gap__wxr, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        eaeyz__xmmnx = builder.call(gap__wxr, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        hqg__cfi = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        hqg__cfi.data = info_to_array_codegen(context, builder, sig, (
            nup__ivpt, context.get_constant_null(arr_type.data)))
        kpf__qxwwi = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = kpf__qxwwi(array_info_type, kpf__qxwwi)
        hqg__cfi.indices = info_to_array_codegen(context, builder, sig, (
            eaeyz__xmmnx, context.get_constant_null(kpf__qxwwi)))
        udiqd__sqd = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='get_has_global_dictionary')
        bho__dqjg = builder.call(gap__wxr, [in_info])
        hqg__cfi.has_global_dictionary = builder.trunc(bho__dqjg, cgutils.
            bool_t)
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='get_has_deduped_local_dictionary')
        iro__brsq = builder.call(gap__wxr, [in_info])
        hqg__cfi.has_deduped_local_dictionary = builder.trunc(iro__brsq,
            cgutils.bool_t)
        return hqg__cfi._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        rpni__qme = get_categories_int_type(arr_type.dtype)
        una__sep = types.Array(rpni__qme, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(una__sep, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            lqlff__vjkpp = bodo.utils.utils.create_categorical_type(arr_type
                .dtype.categories, arr_type.dtype.data.data, is_ordered)
            new_cats_tup = MetaType(tuple(lqlff__vjkpp))
            int_type = arr_type.dtype.int_type
            gnih__chbh = arr_type.dtype.data.data
            npyxz__ooc = context.get_constant_generic(builder, gnih__chbh,
                lqlff__vjkpp)
            lfu__eikp = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(gnih__chbh), [npyxz__ooc])
        else:
            lfu__eikp = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, lfu__eikp)
        out_arr.dtype = lfu__eikp
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
        bdu__nnt = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            bdu__nnt = int128_type
        elif arr_type == datetime_date_array_type:
            bdu__nnt = types.int64
        ndsgm__aebl = types.Array(bdu__nnt, 1, 'C')
        cpmc__oeihl = context.make_array(ndsgm__aebl)(context, builder)
        xrioj__spr = types.Array(types.uint8, 1, 'C')
        biflh__xnth = context.make_array(xrioj__spr)(context, builder)
        brxci__meprj = cgutils.alloca_once(builder, lir.IntType(64))
        qxsl__tpyi = cgutils.alloca_once(builder, lir.IntType(64))
        qyj__zrv = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        rwk__aiskv = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ddxhr__mddy = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        zvm__rdqfg = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        udiqd__sqd = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='info_to_nullable_array')
        builder.call(gap__wxr, [in_info, brxci__meprj, qxsl__tpyi, qyj__zrv,
            rwk__aiskv, ddxhr__mddy, zvm__rdqfg])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        ridx__qepgc = context.get_value_type(types.intp)
        dqs__kncte = cgutils.pack_array(builder, [builder.load(brxci__meprj
            )], ty=ridx__qepgc)
        noivm__vvgd = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(bdu__nnt)))
        tdm__tpmgs = cgutils.pack_array(builder, [noivm__vvgd], ty=ridx__qepgc)
        data = builder.bitcast(builder.load(qyj__zrv), context.
            get_data_type(bdu__nnt).as_pointer())
        numba.np.arrayobj.populate_array(cpmc__oeihl, data=data, shape=
            dqs__kncte, strides=tdm__tpmgs, itemsize=noivm__vvgd, meminfo=
            builder.load(ddxhr__mddy))
        arr.data = cpmc__oeihl._getvalue()
        dqs__kncte = cgutils.pack_array(builder, [builder.load(qxsl__tpyi)],
            ty=ridx__qepgc)
        noivm__vvgd = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(types.uint8)))
        tdm__tpmgs = cgutils.pack_array(builder, [noivm__vvgd], ty=ridx__qepgc)
        data = builder.bitcast(builder.load(rwk__aiskv), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(biflh__xnth, data=data, shape=
            dqs__kncte, strides=tdm__tpmgs, itemsize=noivm__vvgd, meminfo=
            builder.load(zvm__rdqfg))
        arr.null_bitmap = biflh__xnth._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        lnpl__jfror = context.make_array(arr_type.arr_type)(context, builder)
        lzr__ktwb = context.make_array(arr_type.arr_type)(context, builder)
        brxci__meprj = cgutils.alloca_once(builder, lir.IntType(64))
        alt__ppgyj = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        xuukv__yopu = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        wiwv__ajepp = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        neoa__fjj = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        udiqd__sqd = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='info_to_interval_array')
        builder.call(gap__wxr, [in_info, brxci__meprj, alt__ppgyj,
            xuukv__yopu, wiwv__ajepp, neoa__fjj])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        ridx__qepgc = context.get_value_type(types.intp)
        dqs__kncte = cgutils.pack_array(builder, [builder.load(brxci__meprj
            )], ty=ridx__qepgc)
        noivm__vvgd = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
        tdm__tpmgs = cgutils.pack_array(builder, [noivm__vvgd], ty=ridx__qepgc)
        ivf__cxipo = builder.bitcast(builder.load(alt__ppgyj), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(lnpl__jfror, data=ivf__cxipo,
            shape=dqs__kncte, strides=tdm__tpmgs, itemsize=noivm__vvgd,
            meminfo=builder.load(wiwv__ajepp))
        arr.left = lnpl__jfror._getvalue()
        fciox__bxa = builder.bitcast(builder.load(xuukv__yopu), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(lzr__ktwb, data=fciox__bxa, shape=
            dqs__kncte, strides=tdm__tpmgs, itemsize=noivm__vvgd, meminfo=
            builder.load(neoa__fjj))
        arr.right = lzr__ktwb._getvalue()
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
        length, zfkcg__tcies = args
        gwv__ssei = numba_to_c_type(array_type.dtype)
        njym__nhnx = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), gwv__ssei))
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='alloc_numpy')
        return builder.call(gap__wxr, [length, builder.load(njym__nhnx)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        length, fwvj__bpcz = args
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='alloc_string_array')
        return builder.call(gap__wxr, [length, fwvj__bpcz])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    hwzc__ybv, = args
    wbyxn__gnhp = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], hwzc__ybv)
    udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType
        (8).as_pointer().as_pointer(), lir.IntType(64)])
    gap__wxr = cgutils.get_or_insert_function(builder.module, udiqd__sqd,
        name='arr_info_list_to_table')
    return builder.call(gap__wxr, [wbyxn__gnhp.data, wbyxn__gnhp.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='info_from_table')
        return builder.call(gap__wxr, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    ikriv__mled = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        cpp_table, adoc__xfoqy, zfkcg__tcies = args
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='info_from_table')
        jkx__tlk = cgutils.create_struct_proxy(ikriv__mled)(context, builder)
        jkx__tlk.parent = cgutils.get_null_value(jkx__tlk.parent.type)
        mzqnh__wcg = context.make_array(table_idx_arr_t)(context, builder,
            adoc__xfoqy)
        gfa__hyaps = context.get_constant(types.int64, -1)
        cqzwm__dbj = context.get_constant(types.int64, 0)
        uqp__zfya = cgutils.alloca_once_value(builder, cqzwm__dbj)
        for t, zcpe__mit in ikriv__mled.type_to_blk.items():
            dpzhh__axkdu = context.get_constant(types.int64, len(
                ikriv__mled.block_to_arr_ind[zcpe__mit]))
            zfkcg__tcies, jorq__sjuss = ListInstance.allocate_ex(context,
                builder, types.List(t), dpzhh__axkdu)
            jorq__sjuss.size = dpzhh__axkdu
            pxu__ynjlo = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(ikriv__mled.block_to_arr_ind
                [zcpe__mit], dtype=np.int64))
            xwnrj__rlu = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, pxu__ynjlo)
            with cgutils.for_range(builder, dpzhh__axkdu) as gky__flc:
                gybyh__qvrzi = gky__flc.index
                dna__kbbs = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    xwnrj__rlu, gybyh__qvrzi)
                ilchk__pqm = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, mzqnh__wcg, dna__kbbs)
                rmh__dwg = builder.icmp_unsigned('!=', ilchk__pqm, gfa__hyaps)
                with builder.if_else(rmh__dwg) as (eer__jcan, brblc__ookla):
                    with eer__jcan:
                        wka__zamn = builder.call(gap__wxr, [cpp_table,
                            ilchk__pqm])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            wka__zamn])
                        jorq__sjuss.inititem(gybyh__qvrzi, arr, incref=False)
                        length = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(length, uqp__zfya)
                    with brblc__ookla:
                        kcfh__zabvd = context.get_constant_null(t)
                        jorq__sjuss.inititem(gybyh__qvrzi, kcfh__zabvd,
                            incref=False)
            setattr(jkx__tlk, f'block_{zcpe__mit}', jorq__sjuss.value)
        jkx__tlk.len = builder.load(uqp__zfya)
        return jkx__tlk._getvalue()
    return ikriv__mled(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def cpp_table_to_py_data(cpp_table, out_col_inds_t, out_types_t, n_rows_t,
    n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
    uyv__epdtn = out_col_inds_t.instance_type.meta
    ikriv__mled = unwrap_typeref(out_types_t.types[0])
    aywfs__pxi = [unwrap_typeref(out_types_t.types[gybyh__qvrzi]) for
        gybyh__qvrzi in range(1, len(out_types_t.types))]
    tpr__krihx = {}
    hgc__opk = get_overload_const_int(n_table_cols_t)
    bkp__udxhn = {ogbi__bbl: gybyh__qvrzi for gybyh__qvrzi, ogbi__bbl in
        enumerate(uyv__epdtn)}
    if not is_overload_none(unknown_cat_arrs_t):
        rtm__vmnh = {rme__xxao: gybyh__qvrzi for gybyh__qvrzi, rme__xxao in
            enumerate(cat_inds_t.instance_type.meta)}
    iuues__cnsi = []
    sbrsk__ytre = """def impl(cpp_table, out_col_inds_t, out_types_t, n_rows_t, n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
"""
    if isinstance(ikriv__mled, bodo.TableType):
        sbrsk__ytre += f'  py_table = init_table(py_table_type, False)\n'
        sbrsk__ytre += f'  py_table = set_table_len(py_table, n_rows_t)\n'
        for hkqs__ghdh, zcpe__mit in ikriv__mled.type_to_blk.items():
            hbdj__bsqzv = [bkp__udxhn.get(gybyh__qvrzi, -1) for
                gybyh__qvrzi in ikriv__mled.block_to_arr_ind[zcpe__mit]]
            tpr__krihx[f'out_inds_{zcpe__mit}'] = np.array(hbdj__bsqzv, np.
                int64)
            tpr__krihx[f'out_type_{zcpe__mit}'] = hkqs__ghdh
            tpr__krihx[f'typ_list_{zcpe__mit}'] = types.List(hkqs__ghdh)
            kpnq__ttgn = f'out_type_{zcpe__mit}'
            if type_has_unknown_cats(hkqs__ghdh):
                if is_overload_none(unknown_cat_arrs_t):
                    sbrsk__ytre += f"""  in_arr_list_{zcpe__mit} = get_table_block(out_types_t[0], {zcpe__mit})
"""
                    kpnq__ttgn = f'in_arr_list_{zcpe__mit}[i]'
                else:
                    tpr__krihx[f'cat_arr_inds_{zcpe__mit}'] = np.array([
                        rtm__vmnh.get(gybyh__qvrzi, -1) for gybyh__qvrzi in
                        ikriv__mled.block_to_arr_ind[zcpe__mit]], np.int64)
                    kpnq__ttgn = (
                        f'unknown_cat_arrs_t[cat_arr_inds_{zcpe__mit}[i]]')
            dpzhh__axkdu = len(ikriv__mled.block_to_arr_ind[zcpe__mit])
            sbrsk__ytre += f"""  arr_list_{zcpe__mit} = alloc_list_like(typ_list_{zcpe__mit}, {dpzhh__axkdu}, False)
"""
            sbrsk__ytre += f'  for i in range(len(arr_list_{zcpe__mit})):\n'
            sbrsk__ytre += (
                f'    cpp_ind_{zcpe__mit} = out_inds_{zcpe__mit}[i]\n')
            sbrsk__ytre += f'    if cpp_ind_{zcpe__mit} == -1:\n'
            sbrsk__ytre += f'      continue\n'
            sbrsk__ytre += f"""    arr_{zcpe__mit} = info_to_array(info_from_table(cpp_table, cpp_ind_{zcpe__mit}), {kpnq__ttgn})
"""
            sbrsk__ytre += f'    arr_list_{zcpe__mit}[i] = arr_{zcpe__mit}\n'
            sbrsk__ytre += f"""  py_table = set_table_block(py_table, arr_list_{zcpe__mit}, {zcpe__mit})
"""
        iuues__cnsi.append('py_table')
    elif ikriv__mled != types.none:
        nrkdx__unhe = bkp__udxhn.get(0, -1)
        if nrkdx__unhe != -1:
            tpr__krihx[f'arr_typ_arg0'] = ikriv__mled
            kpnq__ttgn = f'arr_typ_arg0'
            if type_has_unknown_cats(ikriv__mled):
                if is_overload_none(unknown_cat_arrs_t):
                    kpnq__ttgn = f'out_types_t[0]'
                else:
                    kpnq__ttgn = f'unknown_cat_arrs_t[{rtm__vmnh[0]}]'
            sbrsk__ytre += f"""  out_arg0 = info_to_array(info_from_table(cpp_table, {nrkdx__unhe}), {kpnq__ttgn})
"""
            iuues__cnsi.append('out_arg0')
    for gybyh__qvrzi, t in enumerate(aywfs__pxi):
        nrkdx__unhe = bkp__udxhn.get(hgc__opk + gybyh__qvrzi, -1)
        if nrkdx__unhe != -1:
            tpr__krihx[f'extra_arr_type_{gybyh__qvrzi}'] = t
            kpnq__ttgn = f'extra_arr_type_{gybyh__qvrzi}'
            if type_has_unknown_cats(t):
                if is_overload_none(unknown_cat_arrs_t):
                    kpnq__ttgn = f'out_types_t[{gybyh__qvrzi + 1}]'
                else:
                    kpnq__ttgn = (
                        f'unknown_cat_arrs_t[{rtm__vmnh[hgc__opk + gybyh__qvrzi]}]'
                        )
            sbrsk__ytre += f"""  out_{gybyh__qvrzi} = info_to_array(info_from_table(cpp_table, {nrkdx__unhe}), {kpnq__ttgn})
"""
            iuues__cnsi.append(f'out_{gybyh__qvrzi}')
    ehq__ipzo = ',' if len(iuues__cnsi) == 1 else ''
    sbrsk__ytre += f"  return ({', '.join(iuues__cnsi)}{ehq__ipzo})\n"
    tpr__krihx.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'out_col_inds': list(uyv__epdtn), 'py_table_type': ikriv__mled})
    tejj__bgwcw = {}
    exec(sbrsk__ytre, tpr__krihx, tejj__bgwcw)
    return tejj__bgwcw['impl']


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    ikriv__mled = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        py_table, zfkcg__tcies = args
        lqi__ufe = cgutils.create_struct_proxy(ikriv__mled)(context,
            builder, py_table)
        if ikriv__mled.has_runtime_cols:
            maipl__ifu = lir.Constant(lir.IntType(64), 0)
            for zcpe__mit, t in enumerate(ikriv__mled.arr_types):
                gbsbt__dme = getattr(lqi__ufe, f'block_{zcpe__mit}')
                sob__zxa = ListInstance(context, builder, types.List(t),
                    gbsbt__dme)
                maipl__ifu = builder.add(maipl__ifu, sob__zxa.size)
        else:
            maipl__ifu = lir.Constant(lir.IntType(64), len(ikriv__mled.
                arr_types))
        zfkcg__tcies, ohzx__clmh = ListInstance.allocate_ex(context,
            builder, types.List(array_info_type), maipl__ifu)
        ohzx__clmh.size = maipl__ifu
        if ikriv__mled.has_runtime_cols:
            zpej__snmqh = lir.Constant(lir.IntType(64), 0)
            for zcpe__mit, t in enumerate(ikriv__mled.arr_types):
                gbsbt__dme = getattr(lqi__ufe, f'block_{zcpe__mit}')
                sob__zxa = ListInstance(context, builder, types.List(t),
                    gbsbt__dme)
                dpzhh__axkdu = sob__zxa.size
                with cgutils.for_range(builder, dpzhh__axkdu) as gky__flc:
                    gybyh__qvrzi = gky__flc.index
                    arr = sob__zxa.getitem(gybyh__qvrzi)
                    ycs__aahj = signature(array_info_type, t)
                    fau__ttcb = arr,
                    dblze__vttr = array_to_info_codegen(context, builder,
                        ycs__aahj, fau__ttcb)
                    ohzx__clmh.inititem(builder.add(zpej__snmqh,
                        gybyh__qvrzi), dblze__vttr, incref=False)
                zpej__snmqh = builder.add(zpej__snmqh, dpzhh__axkdu)
        else:
            for t, zcpe__mit in ikriv__mled.type_to_blk.items():
                dpzhh__axkdu = context.get_constant(types.int64, len(
                    ikriv__mled.block_to_arr_ind[zcpe__mit]))
                gbsbt__dme = getattr(lqi__ufe, f'block_{zcpe__mit}')
                sob__zxa = ListInstance(context, builder, types.List(t),
                    gbsbt__dme)
                pxu__ynjlo = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(ikriv__mled.
                    block_to_arr_ind[zcpe__mit], dtype=np.int64))
                xwnrj__rlu = context.make_array(types.Array(types.int64, 1,
                    'C'))(context, builder, pxu__ynjlo)
                with cgutils.for_range(builder, dpzhh__axkdu) as gky__flc:
                    gybyh__qvrzi = gky__flc.index
                    dna__kbbs = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        xwnrj__rlu, gybyh__qvrzi)
                    obp__gafqi = signature(types.none, ikriv__mled, types.
                        List(t), types.int64, types.int64)
                    cwbl__ylv = py_table, gbsbt__dme, gybyh__qvrzi, dna__kbbs
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, obp__gafqi, cwbl__ylv)
                    arr = sob__zxa.getitem(gybyh__qvrzi)
                    ycs__aahj = signature(array_info_type, t)
                    fau__ttcb = arr,
                    dblze__vttr = array_to_info_codegen(context, builder,
                        ycs__aahj, fau__ttcb)
                    ohzx__clmh.inititem(dna__kbbs, dblze__vttr, incref=False)
        ezpzw__cajmf = ohzx__clmh.value
        yrmz__bkcuo = signature(table_type, types.List(array_info_type))
        wfy__uuh = ezpzw__cajmf,
        cpp_table = arr_info_list_to_table_codegen(context, builder,
            yrmz__bkcuo, wfy__uuh)
        context.nrt.decref(builder, types.List(array_info_type), ezpzw__cajmf)
        return cpp_table
    return table_type(ikriv__mled, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def py_data_to_cpp_table(py_table, extra_arrs_tup, in_col_inds_t,
    n_table_cols_t):
    vcxm__ladmx = in_col_inds_t.instance_type.meta
    tpr__krihx = {}
    hgc__opk = get_overload_const_int(n_table_cols_t)
    fugo__jxq = defaultdict(list)
    bkp__udxhn = {}
    for gybyh__qvrzi, ogbi__bbl in enumerate(vcxm__ladmx):
        if ogbi__bbl in bkp__udxhn:
            fugo__jxq[ogbi__bbl].append(gybyh__qvrzi)
        else:
            bkp__udxhn[ogbi__bbl] = gybyh__qvrzi
    sbrsk__ytre = (
        'def impl(py_table, extra_arrs_tup, in_col_inds_t, n_table_cols_t):\n')
    sbrsk__ytre += (
        f'  cpp_arr_list = alloc_empty_list_type({len(vcxm__ladmx)}, array_info_type)\n'
        )
    if py_table != types.none:
        for zcpe__mit in py_table.type_to_blk.values():
            hbdj__bsqzv = [bkp__udxhn.get(gybyh__qvrzi, -1) for
                gybyh__qvrzi in py_table.block_to_arr_ind[zcpe__mit]]
            tpr__krihx[f'out_inds_{zcpe__mit}'] = np.array(hbdj__bsqzv, np.
                int64)
            tpr__krihx[f'arr_inds_{zcpe__mit}'] = np.array(py_table.
                block_to_arr_ind[zcpe__mit], np.int64)
            sbrsk__ytre += (
                f'  arr_list_{zcpe__mit} = get_table_block(py_table, {zcpe__mit})\n'
                )
            sbrsk__ytre += f'  for i in range(len(arr_list_{zcpe__mit})):\n'
            sbrsk__ytre += (
                f'    out_arr_ind_{zcpe__mit} = out_inds_{zcpe__mit}[i]\n')
            sbrsk__ytre += f'    if out_arr_ind_{zcpe__mit} == -1:\n'
            sbrsk__ytre += f'      continue\n'
            sbrsk__ytre += (
                f'    arr_ind_{zcpe__mit} = arr_inds_{zcpe__mit}[i]\n')
            sbrsk__ytre += f"""    ensure_column_unboxed(py_table, arr_list_{zcpe__mit}, i, arr_ind_{zcpe__mit})
"""
            sbrsk__ytre += f"""    cpp_arr_list[out_arr_ind_{zcpe__mit}] = array_to_info(arr_list_{zcpe__mit}[i])
"""
        for qcjm__jhz, fmf__iuu in fugo__jxq.items():
            if qcjm__jhz < hgc__opk:
                zcpe__mit = py_table.block_nums[qcjm__jhz]
                lfzbf__hvxe = py_table.block_offsets[qcjm__jhz]
                for nrkdx__unhe in fmf__iuu:
                    sbrsk__ytre += f"""  cpp_arr_list[{nrkdx__unhe}] = array_to_info(arr_list_{zcpe__mit}[{lfzbf__hvxe}])
"""
    for gybyh__qvrzi in range(len(extra_arrs_tup)):
        cki__xggo = bkp__udxhn.get(hgc__opk + gybyh__qvrzi, -1)
        if cki__xggo != -1:
            dyovq__jil = [cki__xggo] + fugo__jxq.get(hgc__opk +
                gybyh__qvrzi, [])
            for nrkdx__unhe in dyovq__jil:
                sbrsk__ytre += f"""  cpp_arr_list[{nrkdx__unhe}] = array_to_info(extra_arrs_tup[{gybyh__qvrzi}])
"""
    sbrsk__ytre += f'  return arr_info_list_to_table(cpp_arr_list)\n'
    tpr__krihx.update({'array_info_type': array_info_type,
        'alloc_empty_list_type': bodo.hiframes.table.alloc_empty_list_type,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'ensure_column_unboxed': bodo.hiframes.table.ensure_column_unboxed,
        'array_to_info': array_to_info, 'arr_info_list_to_table':
        arr_info_list_to_table})
    tejj__bgwcw = {}
    exec(sbrsk__ytre, tpr__krihx, tejj__bgwcw)
    return tejj__bgwcw['impl']


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
        udiqd__sqd = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='delete_table')
        builder.call(gap__wxr, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='shuffle_table')
        hot__jnsb = builder.call(gap__wxr, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return hot__jnsb
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
        udiqd__sqd = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='delete_shuffle_info')
        return builder.call(gap__wxr, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='reverse_shuffle_table')
        return builder.call(gap__wxr, args)
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
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(64), lir.IntType(8).as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='hash_join_table')
        hot__jnsb = builder.call(gap__wxr, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return hot__jnsb
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
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64), lir.
            IntType(8).as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='cross_join_table')
        hot__jnsb = builder.call(gap__wxr, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return hot__jnsb
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.boolean, types.boolean, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.int64, types.voidptr, types.
        int64, types.voidptr), codegen


@intrinsic
def sort_values_table(typingctx, table_t, n_keys_t, vect_ascending_t,
    na_position_b_t, dead_keys_t, n_rows_t, bounds_t, parallel_t):
    assert table_t == table_type, 'C++ table type expected'

    def codegen(context, builder, sig, args):
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1)])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='sort_values_table')
        hot__jnsb = builder.call(gap__wxr, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return hot__jnsb
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='sample_table')
        hot__jnsb = builder.call(gap__wxr, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return hot__jnsb
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='shuffle_renormalization')
        hot__jnsb = builder.call(gap__wxr, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return hot__jnsb
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='shuffle_renormalization_group')
        hot__jnsb = builder.call(gap__wxr, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return hot__jnsb
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='drop_duplicates_table')
        hot__jnsb = builder.call(gap__wxr, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return hot__jnsb
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
        udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        gap__wxr = cgutils.get_or_insert_function(builder.module,
            udiqd__sqd, name='groupby_and_aggregate')
        hot__jnsb = builder.call(gap__wxr, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return hot__jnsb
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
    cjiuk__rsk = array_to_info(dict_arr)
    _drop_duplicates_local_dictionary(cjiuk__rsk, sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(cjiuk__rsk, bodo.dict_str_arr_type)
    return out_arr


_convert_local_dictionary_to_global = types.ExternalFunction(
    'convert_local_dictionary_to_global', types.void(array_info_type, types
    .bool_, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def convert_local_dictionary_to_global(dict_arr, sort_dictionary,
    is_parallel=False):
    cjiuk__rsk = array_to_info(dict_arr)
    _convert_local_dictionary_to_global(cjiuk__rsk, is_parallel,
        sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(cjiuk__rsk, bodo.dict_str_arr_type)
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
    jxqg__mxy = array_to_info(in_arr)
    tgm__mnoh = array_to_info(in_values)
    dbb__ozwrk = array_to_info(out_arr)
    tkl__pezh = arr_info_list_to_table([jxqg__mxy, tgm__mnoh, dbb__ozwrk])
    _array_isin(dbb__ozwrk, jxqg__mxy, tgm__mnoh, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(tkl__pezh)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, match, pat, out_arr):
    jxqg__mxy = array_to_info(in_arr)
    dbb__ozwrk = array_to_info(out_arr)
    _get_search_regex(jxqg__mxy, case, match, pat, dbb__ozwrk)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    zdo__kwz = col_array_typ.dtype
    if isinstance(zdo__kwz, (types.Number, TimeType, bodo.libs.
        pd_datetime_arr_ext.PandasDatetimeTZDtype)) or zdo__kwz in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:
        if isinstance(zdo__kwz, bodo.libs.pd_datetime_arr_ext.
            PandasDatetimeTZDtype):
            zdo__kwz = bodo.datetime64ns

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                jkx__tlk, oxin__svs = args
                jkx__tlk = builder.bitcast(jkx__tlk, lir.IntType(8).
                    as_pointer().as_pointer())
                fil__pigx = lir.Constant(lir.IntType(64), c_ind)
                qqrpc__ojjey = builder.load(builder.gep(jkx__tlk, [fil__pigx]))
                qqrpc__ojjey = builder.bitcast(qqrpc__ojjey, context.
                    get_data_type(zdo__kwz).as_pointer())
                return context.unpack_value(builder, zdo__kwz, builder.gep(
                    qqrpc__ojjey, [oxin__svs]))
            return zdo__kwz(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ in (bodo.string_array_type, bodo.binary_array_type):

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                jkx__tlk, oxin__svs = args
                jkx__tlk = builder.bitcast(jkx__tlk, lir.IntType(8).
                    as_pointer().as_pointer())
                fil__pigx = lir.Constant(lir.IntType(64), c_ind)
                qqrpc__ojjey = builder.load(builder.gep(jkx__tlk, [fil__pigx]))
                udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                tdtdw__wktk = cgutils.get_or_insert_function(builder.module,
                    udiqd__sqd, name='array_info_getitem')
                tmw__pagcu = cgutils.alloca_once(builder, lir.IntType(64))
                args = qqrpc__ojjey, oxin__svs, tmw__pagcu
                qyj__zrv = builder.call(tdtdw__wktk, args)
                lcsfl__wambl = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    lcsfl__wambl, [qyj__zrv, builder.load(tmw__pagcu)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                ljktn__nfcb = lir.Constant(lir.IntType(64), 1)
                zhwna__gkxc = lir.Constant(lir.IntType(64), 2)
                jkx__tlk, oxin__svs = args
                jkx__tlk = builder.bitcast(jkx__tlk, lir.IntType(8).
                    as_pointer().as_pointer())
                fil__pigx = lir.Constant(lir.IntType(64), c_ind)
                qqrpc__ojjey = builder.load(builder.gep(jkx__tlk, [fil__pigx]))
                udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                kqm__jlyn = cgutils.get_or_insert_function(builder.module,
                    udiqd__sqd, name='get_nested_info')
                args = qqrpc__ojjey, zhwna__gkxc
                fmyxs__tkzai = builder.call(kqm__jlyn, args)
                udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                tqjke__ygcal = cgutils.get_or_insert_function(builder.
                    module, udiqd__sqd, name='array_info_getdata1')
                args = fmyxs__tkzai,
                ppcxd__qnic = builder.call(tqjke__ygcal, args)
                ppcxd__qnic = builder.bitcast(ppcxd__qnic, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                nbktb__ppz = builder.sext(builder.load(builder.gep(
                    ppcxd__qnic, [oxin__svs])), lir.IntType(64))
                args = qqrpc__ojjey, ljktn__nfcb
                mas__pekut = builder.call(kqm__jlyn, args)
                udiqd__sqd = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                tdtdw__wktk = cgutils.get_or_insert_function(builder.module,
                    udiqd__sqd, name='array_info_getitem')
                tmw__pagcu = cgutils.alloca_once(builder, lir.IntType(64))
                args = mas__pekut, nbktb__ppz, tmw__pagcu
                qyj__zrv = builder.call(tdtdw__wktk, args)
                lcsfl__wambl = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    lcsfl__wambl, [qyj__zrv, builder.load(tmw__pagcu)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{zdo__kwz}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if isinstance(col_array_dtype, (IntegerArrayType, FloatingArrayType,
        bodo.TimeArrayType)) or col_array_dtype in (bodo.libs.bool_arr_ext.
        boolean_array, bodo.binary_array_type, bodo.datetime_date_array_type
        ) or is_str_arr_type(col_array_dtype):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                mpqn__auh, oxin__svs = args
                mpqn__auh = builder.bitcast(mpqn__auh, lir.IntType(8).
                    as_pointer().as_pointer())
                fil__pigx = lir.Constant(lir.IntType(64), c_ind)
                qqrpc__ojjey = builder.load(builder.gep(mpqn__auh, [fil__pigx])
                    )
                qkxj__urwbp = builder.bitcast(qqrpc__ojjey, context.
                    get_data_type(types.bool_).as_pointer())
                dipt__oldvj = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    qkxj__urwbp, oxin__svs)
                gym__vvvz = builder.icmp_unsigned('!=', dipt__oldvj, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(gym__vvvz, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, (types.Array, bodo.DatetimeArrayType)):
        zdo__kwz = col_array_dtype.dtype
        if zdo__kwz in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            zdo__kwz, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype):
            if isinstance(zdo__kwz, bodo.libs.pd_datetime_arr_ext.
                PandasDatetimeTZDtype):
                zdo__kwz = bodo.datetime64ns

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    jkx__tlk, oxin__svs = args
                    jkx__tlk = builder.bitcast(jkx__tlk, lir.IntType(8).
                        as_pointer().as_pointer())
                    fil__pigx = lir.Constant(lir.IntType(64), c_ind)
                    qqrpc__ojjey = builder.load(builder.gep(jkx__tlk, [
                        fil__pigx]))
                    qqrpc__ojjey = builder.bitcast(qqrpc__ojjey, context.
                        get_data_type(zdo__kwz).as_pointer())
                    dmpfe__tnpxc = builder.load(builder.gep(qqrpc__ojjey, [
                        oxin__svs]))
                    gym__vvvz = builder.icmp_unsigned('!=', dmpfe__tnpxc,
                        lir.Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(gym__vvvz, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(zdo__kwz, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    jkx__tlk, oxin__svs = args
                    jkx__tlk = builder.bitcast(jkx__tlk, lir.IntType(8).
                        as_pointer().as_pointer())
                    fil__pigx = lir.Constant(lir.IntType(64), c_ind)
                    qqrpc__ojjey = builder.load(builder.gep(jkx__tlk, [
                        fil__pigx]))
                    qqrpc__ojjey = builder.bitcast(qqrpc__ojjey, context.
                        get_data_type(zdo__kwz).as_pointer())
                    dmpfe__tnpxc = builder.load(builder.gep(qqrpc__ojjey, [
                        oxin__svs]))
                    jhi__nctuc = signature(types.bool_, zdo__kwz)
                    dipt__oldvj = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, jhi__nctuc, (dmpfe__tnpxc,))
                    return builder.not_(builder.sext(dipt__oldvj, lir.
                        IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
