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
        kccpl__fvaqr = context.make_helper(builder, arr_type, in_arr)
        in_arr = kccpl__fvaqr.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        ibmb__noluy = context.make_helper(builder, arr_type, in_arr)
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='list_string_array_to_info')
        return builder.call(uddaa__eak, [ibmb__noluy.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                ckaf__jfvm = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for dxte__rbzvb in arr_typ.data:
                    ckaf__jfvm += get_types(dxte__rbzvb)
                return ckaf__jfvm
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
                ympep__biy = context.make_helper(builder, arr_typ, value=arr)
                kvfq__bijkz = get_lengths(_get_map_arr_data_type(arr_typ),
                    ympep__biy.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                bjryp__cin = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                kvfq__bijkz = get_lengths(arr_typ.dtype, bjryp__cin.data)
                kvfq__bijkz = cgutils.pack_array(builder, [bjryp__cin.
                    n_arrays] + [builder.extract_value(kvfq__bijkz,
                    tgpp__rgkh) for tgpp__rgkh in range(kvfq__bijkz.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                bjryp__cin = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                kvfq__bijkz = []
                for tgpp__rgkh, dxte__rbzvb in enumerate(arr_typ.data):
                    utwuo__plcy = get_lengths(dxte__rbzvb, builder.
                        extract_value(bjryp__cin.data, tgpp__rgkh))
                    kvfq__bijkz += [builder.extract_value(utwuo__plcy,
                        abq__abss) for abq__abss in range(utwuo__plcy.type.
                        count)]
                kvfq__bijkz = cgutils.pack_array(builder, [length, context.
                    get_constant(types.int64, -1)] + kvfq__bijkz)
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType, types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                kvfq__bijkz = cgutils.pack_array(builder, [length])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return kvfq__bijkz

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                ympep__biy = context.make_helper(builder, arr_typ, value=arr)
                sddqn__xgps = get_buffers(_get_map_arr_data_type(arr_typ),
                    ympep__biy.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                bjryp__cin = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                ulbk__kpk = get_buffers(arr_typ.dtype, bjryp__cin.data)
                xee__zfn = context.make_array(types.Array(offset_type, 1, 'C')
                    )(context, builder, bjryp__cin.offsets)
                lpdv__xrr = builder.bitcast(xee__zfn.data, lir.IntType(8).
                    as_pointer())
                jxiuu__qacr = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, bjryp__cin.null_bitmap)
                wcbb__yocex = builder.bitcast(jxiuu__qacr.data, lir.IntType
                    (8).as_pointer())
                sddqn__xgps = cgutils.pack_array(builder, [lpdv__xrr,
                    wcbb__yocex] + [builder.extract_value(ulbk__kpk,
                    tgpp__rgkh) for tgpp__rgkh in range(ulbk__kpk.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                bjryp__cin = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                ulbk__kpk = []
                for tgpp__rgkh, dxte__rbzvb in enumerate(arr_typ.data):
                    sbnts__woe = get_buffers(dxte__rbzvb, builder.
                        extract_value(bjryp__cin.data, tgpp__rgkh))
                    ulbk__kpk += [builder.extract_value(sbnts__woe,
                        abq__abss) for abq__abss in range(sbnts__woe.type.
                        count)]
                jxiuu__qacr = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, bjryp__cin.null_bitmap)
                wcbb__yocex = builder.bitcast(jxiuu__qacr.data, lir.IntType
                    (8).as_pointer())
                sddqn__xgps = cgutils.pack_array(builder, [wcbb__yocex] +
                    ulbk__kpk)
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType)) or arr_typ in (boolean_array,
                datetime_date_array_type):
                ctuvu__dwkj = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    ctuvu__dwkj = int128_type
                elif arr_typ == datetime_date_array_type:
                    ctuvu__dwkj = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                hyfjs__okhg = context.make_array(types.Array(ctuvu__dwkj, 1,
                    'C'))(context, builder, arr.data)
                jxiuu__qacr = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, arr.null_bitmap)
                hzjx__pxapj = builder.bitcast(hyfjs__okhg.data, lir.IntType
                    (8).as_pointer())
                wcbb__yocex = builder.bitcast(jxiuu__qacr.data, lir.IntType
                    (8).as_pointer())
                sddqn__xgps = cgutils.pack_array(builder, [wcbb__yocex,
                    hzjx__pxapj])
            elif arr_typ in (string_array_type, binary_array_type):
                bjryp__cin = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                povx__cyqv = context.make_helper(builder, offset_arr_type,
                    bjryp__cin.offsets).data
                data = context.make_helper(builder, char_arr_type,
                    bjryp__cin.data).data
                ngrr__ntv = context.make_helper(builder,
                    null_bitmap_arr_type, bjryp__cin.null_bitmap).data
                sddqn__xgps = cgutils.pack_array(builder, [builder.bitcast(
                    povx__cyqv, lir.IntType(8).as_pointer()), builder.
                    bitcast(ngrr__ntv, lir.IntType(8).as_pointer()),
                    builder.bitcast(data, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                hzjx__pxapj = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                affhr__buw = lir.Constant(lir.IntType(8).as_pointer(), None)
                sddqn__xgps = cgutils.pack_array(builder, [affhr__buw,
                    hzjx__pxapj])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return sddqn__xgps

        def get_field_names(arr_typ):
            nwvs__pcuq = []
            if isinstance(arr_typ, StructArrayType):
                for nfzva__kpb, eig__zpa in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    nwvs__pcuq.append(nfzva__kpb)
                    nwvs__pcuq += get_field_names(eig__zpa)
            elif isinstance(arr_typ, ArrayItemArrayType):
                nwvs__pcuq += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                nwvs__pcuq += get_field_names(_get_map_arr_data_type(arr_typ))
            return nwvs__pcuq
        ckaf__jfvm = get_types(arr_type)
        qbnq__ugu = cgutils.pack_array(builder, [context.get_constant(types
            .int32, t) for t in ckaf__jfvm])
        ijcf__kcp = cgutils.alloca_once_value(builder, qbnq__ugu)
        kvfq__bijkz = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, kvfq__bijkz)
        sddqn__xgps = get_buffers(arr_type, in_arr)
        ijka__vrj = cgutils.alloca_once_value(builder, sddqn__xgps)
        nwvs__pcuq = get_field_names(arr_type)
        if len(nwvs__pcuq) == 0:
            nwvs__pcuq = ['irrelevant']
        dity__yfodo = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in nwvs__pcuq])
        btm__oukr = cgutils.alloca_once_value(builder, dity__yfodo)
        if isinstance(arr_type, MapArrayType):
            clt__tqs = _get_map_arr_data_type(arr_type)
            fooja__ifhc = context.make_helper(builder, arr_type, value=in_arr)
            ufqby__nugz = fooja__ifhc.data
        else:
            clt__tqs = arr_type
            ufqby__nugz = in_arr
        ecovf__zhq = context.make_helper(builder, clt__tqs, ufqby__nugz)
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='nested_array_to_info')
        ayqcb__xttas = builder.call(uddaa__eak, [builder.bitcast(ijcf__kcp,
            lir.IntType(32).as_pointer()), builder.bitcast(ijka__vrj, lir.
            IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            btm__oukr, lir.IntType(8).as_pointer()), ecovf__zhq.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return ayqcb__xttas
    if arr_type in (string_array_type, binary_array_type):
        ykyvx__faa = context.make_helper(builder, arr_type, in_arr)
        lgik__gypf = ArrayItemArrayType(char_arr_type)
        ibmb__noluy = context.make_helper(builder, lgik__gypf, ykyvx__faa.data)
        bjryp__cin = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        povx__cyqv = context.make_helper(builder, offset_arr_type,
            bjryp__cin.offsets).data
        data = context.make_helper(builder, char_arr_type, bjryp__cin.data
            ).data
        ngrr__ntv = context.make_helper(builder, null_bitmap_arr_type,
            bjryp__cin.null_bitmap).data
        dkblg__bqc = builder.zext(builder.load(builder.gep(povx__cyqv, [
            bjryp__cin.n_arrays])), lir.IntType(64))
        oys__wbob = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='string_array_to_info')
        return builder.call(uddaa__eak, [bjryp__cin.n_arrays, dkblg__bqc,
            data, povx__cyqv, ngrr__ntv, ibmb__noluy.meminfo, oys__wbob])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        pnfvo__wxs = arr.data
        nkz__dnrjj = arr.indices
        sig = array_info_type(arr_type.data)
        fmk__jtsla = array_to_info_codegen(context, builder, sig, (
            pnfvo__wxs,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        zryd__ccp = array_to_info_codegen(context, builder, sig, (
            nkz__dnrjj,), False)
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(32), lir.IntType(32)])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='dict_str_array_to_info')
        litx__cjxr = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        ydn__vonv = builder.zext(arr.has_deduped_local_dictionary, lir.
            IntType(32))
        return builder.call(uddaa__eak, [fmk__jtsla, zryd__ccp, litx__cjxr,
            ydn__vonv])
    zizgo__kczw = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        nbg__hjmw = context.compile_internal(builder, lambda a: len(a.dtype
            .categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        ace__nsm = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(ace__nsm, 1, 'C')
        zizgo__kczw = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if zizgo__kczw:
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
        qoyzg__zqwoj = arr_type.dtype
        ofajp__mtl = numba_to_c_type(qoyzg__zqwoj)
        xkja__bqcm = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), ofajp__mtl))
        if zizgo__kczw:
            ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(64), lir.IntType(8).as_pointer()])
            uddaa__eak = cgutils.get_or_insert_function(builder.module,
                ywj__aklwu, name='categorical_array_to_info')
            return builder.call(uddaa__eak, [length, builder.bitcast(arr.
                data, lir.IntType(8).as_pointer()), builder.load(xkja__bqcm
                ), nbg__hjmw, arr.meminfo])
        else:
            ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer()])
            uddaa__eak = cgutils.get_or_insert_function(builder.module,
                ywj__aklwu, name='numpy_array_to_info')
            return builder.call(uddaa__eak, [length, builder.bitcast(arr.
                data, lir.IntType(8).as_pointer()), builder.load(xkja__bqcm
                ), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, TimeArrayType)) or arr_type in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        qoyzg__zqwoj = arr_type.dtype
        ctuvu__dwkj = qoyzg__zqwoj
        if isinstance(arr_type, DecimalArrayType):
            ctuvu__dwkj = int128_type
        if arr_type == datetime_date_array_type:
            ctuvu__dwkj = types.int64
        hyfjs__okhg = context.make_array(types.Array(ctuvu__dwkj, 1, 'C'))(
            context, builder, arr.data)
        length = builder.extract_value(hyfjs__okhg.shape, 0)
        uej__jpfcs = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        ofajp__mtl = numba_to_c_type(qoyzg__zqwoj)
        xkja__bqcm = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), ofajp__mtl))
        if isinstance(arr_type, DecimalArrayType):
            ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
            uddaa__eak = cgutils.get_or_insert_function(builder.module,
                ywj__aklwu, name='decimal_array_to_info')
            return builder.call(uddaa__eak, [length, builder.bitcast(
                hyfjs__okhg.data, lir.IntType(8).as_pointer()), builder.
                load(xkja__bqcm), builder.bitcast(uej__jpfcs.data, lir.
                IntType(8).as_pointer()), hyfjs__okhg.meminfo, uej__jpfcs.
                meminfo, context.get_constant(types.int32, arr_type.
                precision), context.get_constant(types.int32, arr_type.scale)])
        elif isinstance(arr_type, TimeArrayType):
            ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32)])
            uddaa__eak = cgutils.get_or_insert_function(builder.module,
                ywj__aklwu, name='time_array_to_info')
            return builder.call(uddaa__eak, [length, builder.bitcast(
                hyfjs__okhg.data, lir.IntType(8).as_pointer()), builder.
                load(xkja__bqcm), builder.bitcast(uej__jpfcs.data, lir.
                IntType(8).as_pointer()), hyfjs__okhg.meminfo, uej__jpfcs.
                meminfo, lir.Constant(lir.IntType(32), arr_type.precision)])
        else:
            ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer()])
            uddaa__eak = cgutils.get_or_insert_function(builder.module,
                ywj__aklwu, name='nullable_array_to_info')
            return builder.call(uddaa__eak, [length, builder.bitcast(
                hyfjs__okhg.data, lir.IntType(8).as_pointer()), builder.
                load(xkja__bqcm), builder.bitcast(uej__jpfcs.data, lir.
                IntType(8).as_pointer()), hyfjs__okhg.meminfo, uej__jpfcs.
                meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        pjl__ctcei = context.make_array(arr_type.arr_type)(context, builder,
            arr.left)
        hcs__aflv = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        length = builder.extract_value(pjl__ctcei.shape, 0)
        ofajp__mtl = numba_to_c_type(arr_type.arr_type.dtype)
        xkja__bqcm = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), ofajp__mtl))
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='interval_array_to_info')
        return builder.call(uddaa__eak, [length, builder.bitcast(pjl__ctcei
            .data, lir.IntType(8).as_pointer()), builder.bitcast(hcs__aflv.
            data, lir.IntType(8).as_pointer()), builder.load(xkja__bqcm),
            pjl__ctcei.meminfo, hcs__aflv.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    lsfv__sxh = cgutils.alloca_once(builder, lir.IntType(64))
    hzjx__pxapj = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    ixg__oocq = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    ywj__aklwu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    uddaa__eak = cgutils.get_or_insert_function(builder.module, ywj__aklwu,
        name='info_to_numpy_array')
    builder.call(uddaa__eak, [in_info, lsfv__sxh, hzjx__pxapj, ixg__oocq])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    lxz__kon = context.get_value_type(types.intp)
    ttwo__wjbq = cgutils.pack_array(builder, [builder.load(lsfv__sxh)], ty=
        lxz__kon)
    pxs__khod = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    sha__yumb = cgutils.pack_array(builder, [pxs__khod], ty=lxz__kon)
    data = builder.bitcast(builder.load(hzjx__pxapj), context.get_data_type
        (arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=data, shape=ttwo__wjbq,
        strides=sha__yumb, itemsize=pxs__khod, meminfo=builder.load(ixg__oocq))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    ehiad__mtmiy = context.make_helper(builder, arr_type)
    ywj__aklwu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    uddaa__eak = cgutils.get_or_insert_function(builder.module, ywj__aklwu,
        name='info_to_list_string_array')
    builder.call(uddaa__eak, [in_info, ehiad__mtmiy._get_ptr_by_name(
        'meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return ehiad__mtmiy._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    suw__sdyq = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        ixyc__fai = lengths_pos
        ovmlr__bgckv = infos_pos
        xdop__hqxah, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        pwuix__siioq = ArrayItemArrayPayloadType(arr_typ)
        spai__ucyj = context.get_data_type(pwuix__siioq)
        uxq__huf = context.get_abi_sizeof(spai__ucyj)
        fghhu__vwf = define_array_item_dtor(context, builder, arr_typ,
            pwuix__siioq)
        hyw__brgi = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, uxq__huf), fghhu__vwf)
        ydemn__slbmv = context.nrt.meminfo_data(builder, hyw__brgi)
        qfsq__fpod = builder.bitcast(ydemn__slbmv, spai__ucyj.as_pointer())
        bjryp__cin = cgutils.create_struct_proxy(pwuix__siioq)(context, builder
            )
        bjryp__cin.n_arrays = builder.extract_value(builder.load(
            lengths_ptr), ixyc__fai)
        bjryp__cin.data = xdop__hqxah
        redj__aonjh = builder.load(array_infos_ptr)
        wpew__vrswy = builder.bitcast(builder.extract_value(redj__aonjh,
            ovmlr__bgckv), suw__sdyq)
        bjryp__cin.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, wpew__vrswy)
        roo__xegim = builder.bitcast(builder.extract_value(redj__aonjh, 
            ovmlr__bgckv + 1), suw__sdyq)
        bjryp__cin.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, roo__xegim)
        builder.store(bjryp__cin._getvalue(), qfsq__fpod)
        ibmb__noluy = context.make_helper(builder, arr_typ)
        ibmb__noluy.meminfo = hyw__brgi
        return ibmb__noluy._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        srz__suw = []
        ovmlr__bgckv = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for xpjeg__poeab in arr_typ.data:
            xdop__hqxah, lengths_pos, infos_pos = nested_to_array(context,
                builder, xpjeg__poeab, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            srz__suw.append(xdop__hqxah)
        pwuix__siioq = StructArrayPayloadType(arr_typ.data)
        spai__ucyj = context.get_value_type(pwuix__siioq)
        uxq__huf = context.get_abi_sizeof(spai__ucyj)
        fghhu__vwf = define_struct_arr_dtor(context, builder, arr_typ,
            pwuix__siioq)
        hyw__brgi = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, uxq__huf), fghhu__vwf)
        ydemn__slbmv = context.nrt.meminfo_data(builder, hyw__brgi)
        qfsq__fpod = builder.bitcast(ydemn__slbmv, spai__ucyj.as_pointer())
        bjryp__cin = cgutils.create_struct_proxy(pwuix__siioq)(context, builder
            )
        bjryp__cin.data = cgutils.pack_array(builder, srz__suw
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, srz__suw)
        redj__aonjh = builder.load(array_infos_ptr)
        roo__xegim = builder.bitcast(builder.extract_value(redj__aonjh,
            ovmlr__bgckv), suw__sdyq)
        bjryp__cin.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, roo__xegim)
        builder.store(bjryp__cin._getvalue(), qfsq__fpod)
        pit__msvxs = context.make_helper(builder, arr_typ)
        pit__msvxs.meminfo = hyw__brgi
        return pit__msvxs._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        redj__aonjh = builder.load(array_infos_ptr)
        zifo__lfy = builder.bitcast(builder.extract_value(redj__aonjh,
            infos_pos), suw__sdyq)
        ykyvx__faa = context.make_helper(builder, arr_typ)
        lgik__gypf = ArrayItemArrayType(char_arr_type)
        ibmb__noluy = context.make_helper(builder, lgik__gypf)
        ywj__aklwu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='info_to_string_array')
        builder.call(uddaa__eak, [zifo__lfy, ibmb__noluy._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        ykyvx__faa.data = ibmb__noluy._getvalue()
        return ykyvx__faa._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        redj__aonjh = builder.load(array_infos_ptr)
        jwfsz__qqc = builder.bitcast(builder.extract_value(redj__aonjh, 
            infos_pos + 1), suw__sdyq)
        return _lower_info_to_array_numpy(arr_typ, context, builder, jwfsz__qqc
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType)) or arr_typ in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        ctuvu__dwkj = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            ctuvu__dwkj = int128_type
        elif arr_typ == datetime_date_array_type:
            ctuvu__dwkj = types.int64
        redj__aonjh = builder.load(array_infos_ptr)
        roo__xegim = builder.bitcast(builder.extract_value(redj__aonjh,
            infos_pos), suw__sdyq)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, roo__xegim)
        jwfsz__qqc = builder.bitcast(builder.extract_value(redj__aonjh, 
            infos_pos + 1), suw__sdyq)
        arr.data = _lower_info_to_array_numpy(types.Array(ctuvu__dwkj, 1,
            'C'), context, builder, jwfsz__qqc)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, uddd__bapid = args
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
                return 1 + sum([get_num_arrays(xpjeg__poeab) for
                    xpjeg__poeab in arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(xpjeg__poeab) for
                    xpjeg__poeab in arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            tjal__sncrn = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            tjal__sncrn = _get_map_arr_data_type(arr_type)
        else:
            tjal__sncrn = arr_type
        yoi__dojjo = get_num_arrays(tjal__sncrn)
        kvfq__bijkz = cgutils.pack_array(builder, [lir.Constant(lir.IntType
            (64), 0) for uddd__bapid in range(yoi__dojjo)])
        lengths_ptr = cgutils.alloca_once_value(builder, kvfq__bijkz)
        affhr__buw = lir.Constant(lir.IntType(8).as_pointer(), None)
        fjw__zkign = cgutils.pack_array(builder, [affhr__buw for
            uddd__bapid in range(get_num_infos(tjal__sncrn))])
        array_infos_ptr = cgutils.alloca_once_value(builder, fjw__zkign)
        ywj__aklwu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='info_to_nested_array')
        builder.call(uddaa__eak, [in_info, builder.bitcast(lengths_ptr, lir
            .IntType(64).as_pointer()), builder.bitcast(array_infos_ptr,
            lir.IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, uddd__bapid, uddd__bapid = nested_to_array(context, builder,
            tjal__sncrn, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            kccpl__fvaqr = context.make_helper(builder, arr_type)
            kccpl__fvaqr.data = arr
            context.nrt.incref(builder, tjal__sncrn, arr)
            arr = kccpl__fvaqr._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, tjal__sncrn)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        ykyvx__faa = context.make_helper(builder, arr_type)
        lgik__gypf = ArrayItemArrayType(char_arr_type)
        ibmb__noluy = context.make_helper(builder, lgik__gypf)
        ywj__aklwu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='info_to_string_array')
        builder.call(uddaa__eak, [in_info, ibmb__noluy._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        ykyvx__faa.data = ibmb__noluy._getvalue()
        return ykyvx__faa._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='get_nested_info')
        fmk__jtsla = builder.call(uddaa__eak, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        zryd__ccp = builder.call(uddaa__eak, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        kvjnz__ljkxm = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        kvjnz__ljkxm.data = info_to_array_codegen(context, builder, sig, (
            fmk__jtsla, context.get_constant_null(arr_type.data)))
        ycp__cztt = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = ycp__cztt(array_info_type, ycp__cztt)
        kvjnz__ljkxm.indices = info_to_array_codegen(context, builder, sig,
            (zryd__ccp, context.get_constant_null(ycp__cztt)))
        ywj__aklwu = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='get_has_global_dictionary')
        litx__cjxr = builder.call(uddaa__eak, [in_info])
        kvjnz__ljkxm.has_global_dictionary = builder.trunc(litx__cjxr,
            cgutils.bool_t)
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='get_has_deduped_local_dictionary')
        ydn__vonv = builder.call(uddaa__eak, [in_info])
        kvjnz__ljkxm.has_deduped_local_dictionary = builder.trunc(ydn__vonv,
            cgutils.bool_t)
        return kvjnz__ljkxm._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        ace__nsm = get_categories_int_type(arr_type.dtype)
        nyy__kdhu = types.Array(ace__nsm, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(nyy__kdhu, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            whc__hifn = bodo.utils.utils.create_categorical_type(arr_type.
                dtype.categories, arr_type.dtype.data.data, is_ordered)
            new_cats_tup = MetaType(tuple(whc__hifn))
            int_type = arr_type.dtype.int_type
            fsnxs__ftgt = arr_type.dtype.data.data
            hmz__jaoa = context.get_constant_generic(builder, fsnxs__ftgt,
                whc__hifn)
            qoyzg__zqwoj = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(fsnxs__ftgt), [hmz__jaoa])
        else:
            qoyzg__zqwoj = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, qoyzg__zqwoj)
        out_arr.dtype = qoyzg__zqwoj
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
        ctuvu__dwkj = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            ctuvu__dwkj = int128_type
        elif arr_type == datetime_date_array_type:
            ctuvu__dwkj = types.int64
        bis__eevm = types.Array(ctuvu__dwkj, 1, 'C')
        hyfjs__okhg = context.make_array(bis__eevm)(context, builder)
        zirop__ofyv = types.Array(types.uint8, 1, 'C')
        htli__cmgy = context.make_array(zirop__ofyv)(context, builder)
        lsfv__sxh = cgutils.alloca_once(builder, lir.IntType(64))
        oxogt__mdss = cgutils.alloca_once(builder, lir.IntType(64))
        hzjx__pxapj = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        hrxhj__jwt = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ixg__oocq = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ajg__ijk = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ywj__aklwu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='info_to_nullable_array')
        builder.call(uddaa__eak, [in_info, lsfv__sxh, oxogt__mdss,
            hzjx__pxapj, hrxhj__jwt, ixg__oocq, ajg__ijk])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        lxz__kon = context.get_value_type(types.intp)
        ttwo__wjbq = cgutils.pack_array(builder, [builder.load(lsfv__sxh)],
            ty=lxz__kon)
        pxs__khod = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(ctuvu__dwkj)))
        sha__yumb = cgutils.pack_array(builder, [pxs__khod], ty=lxz__kon)
        data = builder.bitcast(builder.load(hzjx__pxapj), context.
            get_data_type(ctuvu__dwkj).as_pointer())
        numba.np.arrayobj.populate_array(hyfjs__okhg, data=data, shape=
            ttwo__wjbq, strides=sha__yumb, itemsize=pxs__khod, meminfo=
            builder.load(ixg__oocq))
        arr.data = hyfjs__okhg._getvalue()
        ttwo__wjbq = cgutils.pack_array(builder, [builder.load(oxogt__mdss)
            ], ty=lxz__kon)
        pxs__khod = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(types.uint8)))
        sha__yumb = cgutils.pack_array(builder, [pxs__khod], ty=lxz__kon)
        data = builder.bitcast(builder.load(hrxhj__jwt), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(htli__cmgy, data=data, shape=
            ttwo__wjbq, strides=sha__yumb, itemsize=pxs__khod, meminfo=
            builder.load(ajg__ijk))
        arr.null_bitmap = htli__cmgy._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        pjl__ctcei = context.make_array(arr_type.arr_type)(context, builder)
        hcs__aflv = context.make_array(arr_type.arr_type)(context, builder)
        lsfv__sxh = cgutils.alloca_once(builder, lir.IntType(64))
        jvgl__tvmx = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        cgs__uyijm = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        xnyh__ywpt = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        dgsh__xavt = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ywj__aklwu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='info_to_interval_array')
        builder.call(uddaa__eak, [in_info, lsfv__sxh, jvgl__tvmx,
            cgs__uyijm, xnyh__ywpt, dgsh__xavt])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        lxz__kon = context.get_value_type(types.intp)
        ttwo__wjbq = cgutils.pack_array(builder, [builder.load(lsfv__sxh)],
            ty=lxz__kon)
        pxs__khod = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(arr_type.arr_type.dtype)))
        sha__yumb = cgutils.pack_array(builder, [pxs__khod], ty=lxz__kon)
        meope__zqu = builder.bitcast(builder.load(jvgl__tvmx), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(pjl__ctcei, data=meope__zqu, shape
            =ttwo__wjbq, strides=sha__yumb, itemsize=pxs__khod, meminfo=
            builder.load(xnyh__ywpt))
        arr.left = pjl__ctcei._getvalue()
        qzvp__oah = builder.bitcast(builder.load(cgs__uyijm), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(hcs__aflv, data=qzvp__oah, shape=
            ttwo__wjbq, strides=sha__yumb, itemsize=pxs__khod, meminfo=
            builder.load(dgsh__xavt))
        arr.right = hcs__aflv._getvalue()
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
        length, uddd__bapid = args
        ofajp__mtl = numba_to_c_type(array_type.dtype)
        xkja__bqcm = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), ofajp__mtl))
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='alloc_numpy')
        return builder.call(uddaa__eak, [length, builder.load(xkja__bqcm)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        length, wouyp__sdasv = args
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='alloc_string_array')
        return builder.call(uddaa__eak, [length, wouyp__sdasv])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    mkpy__yzi, = args
    oazb__qvdth = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], mkpy__yzi)
    ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType
        (8).as_pointer().as_pointer(), lir.IntType(64)])
    uddaa__eak = cgutils.get_or_insert_function(builder.module, ywj__aklwu,
        name='arr_info_list_to_table')
    return builder.call(uddaa__eak, [oazb__qvdth.data, oazb__qvdth.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='info_from_table')
        return builder.call(uddaa__eak, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    vda__oakrf = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        cpp_table, bisr__jllob, uddd__bapid = args
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='info_from_table')
        qduk__qffb = cgutils.create_struct_proxy(vda__oakrf)(context, builder)
        qduk__qffb.parent = cgutils.get_null_value(qduk__qffb.parent.type)
        wsruo__okm = context.make_array(table_idx_arr_t)(context, builder,
            bisr__jllob)
        ecyd__vmy = context.get_constant(types.int64, -1)
        szr__fku = context.get_constant(types.int64, 0)
        bdr__nup = cgutils.alloca_once_value(builder, szr__fku)
        for t, vdg__chfyq in vda__oakrf.type_to_blk.items():
            ndf__ajrh = context.get_constant(types.int64, len(vda__oakrf.
                block_to_arr_ind[vdg__chfyq]))
            uddd__bapid, mkh__gvuth = ListInstance.allocate_ex(context,
                builder, types.List(t), ndf__ajrh)
            mkh__gvuth.size = ndf__ajrh
            vlb__xmzay = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(vda__oakrf.block_to_arr_ind[
                vdg__chfyq], dtype=np.int64))
            jnn__nfg = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, vlb__xmzay)
            with cgutils.for_range(builder, ndf__ajrh) as tfsa__mtavk:
                tgpp__rgkh = tfsa__mtavk.index
                pjvu__btud = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'), jnn__nfg,
                    tgpp__rgkh)
                eogjo__zxsx = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, wsruo__okm, pjvu__btud)
                xlrj__jcfc = builder.icmp_unsigned('!=', eogjo__zxsx, ecyd__vmy
                    )
                with builder.if_else(xlrj__jcfc) as (ahvi__yysck, svo__wksa):
                    with ahvi__yysck:
                        oex__vfjbx = builder.call(uddaa__eak, [cpp_table,
                            eogjo__zxsx])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            oex__vfjbx])
                        mkh__gvuth.inititem(tgpp__rgkh, arr, incref=False)
                        length = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(length, bdr__nup)
                    with svo__wksa:
                        dyge__bfuax = context.get_constant_null(t)
                        mkh__gvuth.inititem(tgpp__rgkh, dyge__bfuax, incref
                            =False)
            setattr(qduk__qffb, f'block_{vdg__chfyq}', mkh__gvuth.value)
        qduk__qffb.len = builder.load(bdr__nup)
        return qduk__qffb._getvalue()
    return vda__oakrf(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def cpp_table_to_py_data(cpp_table, out_col_inds_t, out_types_t, n_rows_t,
    n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
    kwgr__zbe = out_col_inds_t.instance_type.meta
    vda__oakrf = unwrap_typeref(out_types_t.types[0])
    pwdtc__mrf = [unwrap_typeref(out_types_t.types[tgpp__rgkh]) for
        tgpp__rgkh in range(1, len(out_types_t.types))]
    uzo__zxz = {}
    gpa__ond = get_overload_const_int(n_table_cols_t)
    xtfr__vud = {rswq__prtg: tgpp__rgkh for tgpp__rgkh, rswq__prtg in
        enumerate(kwgr__zbe)}
    if not is_overload_none(unknown_cat_arrs_t):
        aotv__ync = {rjkd__cmhxp: tgpp__rgkh for tgpp__rgkh, rjkd__cmhxp in
            enumerate(cat_inds_t.instance_type.meta)}
    ajhx__pakke = []
    qgkd__rafw = """def impl(cpp_table, out_col_inds_t, out_types_t, n_rows_t, n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
"""
    if isinstance(vda__oakrf, bodo.TableType):
        qgkd__rafw += f'  py_table = init_table(py_table_type, False)\n'
        qgkd__rafw += f'  py_table = set_table_len(py_table, n_rows_t)\n'
        for asgxh__pwr, vdg__chfyq in vda__oakrf.type_to_blk.items():
            ngkjj__zfusl = [xtfr__vud.get(tgpp__rgkh, -1) for tgpp__rgkh in
                vda__oakrf.block_to_arr_ind[vdg__chfyq]]
            uzo__zxz[f'out_inds_{vdg__chfyq}'] = np.array(ngkjj__zfusl, np.
                int64)
            uzo__zxz[f'out_type_{vdg__chfyq}'] = asgxh__pwr
            uzo__zxz[f'typ_list_{vdg__chfyq}'] = types.List(asgxh__pwr)
            hoxew__pbiln = f'out_type_{vdg__chfyq}'
            if type_has_unknown_cats(asgxh__pwr):
                if is_overload_none(unknown_cat_arrs_t):
                    qgkd__rafw += f"""  in_arr_list_{vdg__chfyq} = get_table_block(out_types_t[0], {vdg__chfyq})
"""
                    hoxew__pbiln = f'in_arr_list_{vdg__chfyq}[i]'
                else:
                    uzo__zxz[f'cat_arr_inds_{vdg__chfyq}'] = np.array([
                        aotv__ync.get(tgpp__rgkh, -1) for tgpp__rgkh in
                        vda__oakrf.block_to_arr_ind[vdg__chfyq]], np.int64)
                    hoxew__pbiln = (
                        f'unknown_cat_arrs_t[cat_arr_inds_{vdg__chfyq}[i]]')
            ndf__ajrh = len(vda__oakrf.block_to_arr_ind[vdg__chfyq])
            qgkd__rafw += f"""  arr_list_{vdg__chfyq} = alloc_list_like(typ_list_{vdg__chfyq}, {ndf__ajrh}, False)
"""
            qgkd__rafw += f'  for i in range(len(arr_list_{vdg__chfyq})):\n'
            qgkd__rafw += (
                f'    cpp_ind_{vdg__chfyq} = out_inds_{vdg__chfyq}[i]\n')
            qgkd__rafw += f'    if cpp_ind_{vdg__chfyq} == -1:\n'
            qgkd__rafw += f'      continue\n'
            qgkd__rafw += f"""    arr_{vdg__chfyq} = info_to_array(info_from_table(cpp_table, cpp_ind_{vdg__chfyq}), {hoxew__pbiln})
"""
            qgkd__rafw += f'    arr_list_{vdg__chfyq}[i] = arr_{vdg__chfyq}\n'
            qgkd__rafw += f"""  py_table = set_table_block(py_table, arr_list_{vdg__chfyq}, {vdg__chfyq})
"""
        ajhx__pakke.append('py_table')
    elif vda__oakrf != types.none:
        umjyw__rgcx = xtfr__vud.get(0, -1)
        if umjyw__rgcx != -1:
            uzo__zxz[f'arr_typ_arg0'] = vda__oakrf
            hoxew__pbiln = f'arr_typ_arg0'
            if type_has_unknown_cats(vda__oakrf):
                if is_overload_none(unknown_cat_arrs_t):
                    hoxew__pbiln = f'out_types_t[0]'
                else:
                    hoxew__pbiln = f'unknown_cat_arrs_t[{aotv__ync[0]}]'
            qgkd__rafw += f"""  out_arg0 = info_to_array(info_from_table(cpp_table, {umjyw__rgcx}), {hoxew__pbiln})
"""
            ajhx__pakke.append('out_arg0')
    for tgpp__rgkh, t in enumerate(pwdtc__mrf):
        umjyw__rgcx = xtfr__vud.get(gpa__ond + tgpp__rgkh, -1)
        if umjyw__rgcx != -1:
            uzo__zxz[f'extra_arr_type_{tgpp__rgkh}'] = t
            hoxew__pbiln = f'extra_arr_type_{tgpp__rgkh}'
            if type_has_unknown_cats(t):
                if is_overload_none(unknown_cat_arrs_t):
                    hoxew__pbiln = f'out_types_t[{tgpp__rgkh + 1}]'
                else:
                    hoxew__pbiln = (
                        f'unknown_cat_arrs_t[{aotv__ync[gpa__ond + tgpp__rgkh]}]'
                        )
            qgkd__rafw += f"""  out_{tgpp__rgkh} = info_to_array(info_from_table(cpp_table, {umjyw__rgcx}), {hoxew__pbiln})
"""
            ajhx__pakke.append(f'out_{tgpp__rgkh}')
    ffoq__alkne = ',' if len(ajhx__pakke) == 1 else ''
    qgkd__rafw += f"  return ({', '.join(ajhx__pakke)}{ffoq__alkne})\n"
    uzo__zxz.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'out_col_inds': list(kwgr__zbe), 'py_table_type': vda__oakrf})
    fqo__lhm = {}
    exec(qgkd__rafw, uzo__zxz, fqo__lhm)
    return fqo__lhm['impl']


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    vda__oakrf = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        py_table, uddd__bapid = args
        pdaw__gxov = cgutils.create_struct_proxy(vda__oakrf)(context,
            builder, py_table)
        if vda__oakrf.has_runtime_cols:
            oref__cnftd = lir.Constant(lir.IntType(64), 0)
            for vdg__chfyq, t in enumerate(vda__oakrf.arr_types):
                erlz__duutc = getattr(pdaw__gxov, f'block_{vdg__chfyq}')
                yaicl__ggfx = ListInstance(context, builder, types.List(t),
                    erlz__duutc)
                oref__cnftd = builder.add(oref__cnftd, yaicl__ggfx.size)
        else:
            oref__cnftd = lir.Constant(lir.IntType(64), len(vda__oakrf.
                arr_types))
        uddd__bapid, luf__okv = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), oref__cnftd)
        luf__okv.size = oref__cnftd
        if vda__oakrf.has_runtime_cols:
            dvyed__pxd = lir.Constant(lir.IntType(64), 0)
            for vdg__chfyq, t in enumerate(vda__oakrf.arr_types):
                erlz__duutc = getattr(pdaw__gxov, f'block_{vdg__chfyq}')
                yaicl__ggfx = ListInstance(context, builder, types.List(t),
                    erlz__duutc)
                ndf__ajrh = yaicl__ggfx.size
                with cgutils.for_range(builder, ndf__ajrh) as tfsa__mtavk:
                    tgpp__rgkh = tfsa__mtavk.index
                    arr = yaicl__ggfx.getitem(tgpp__rgkh)
                    kkrl__vsak = signature(array_info_type, t)
                    lzu__dax = arr,
                    zvv__qwfcq = array_to_info_codegen(context, builder,
                        kkrl__vsak, lzu__dax)
                    luf__okv.inititem(builder.add(dvyed__pxd, tgpp__rgkh),
                        zvv__qwfcq, incref=False)
                dvyed__pxd = builder.add(dvyed__pxd, ndf__ajrh)
        else:
            for t, vdg__chfyq in vda__oakrf.type_to_blk.items():
                ndf__ajrh = context.get_constant(types.int64, len(
                    vda__oakrf.block_to_arr_ind[vdg__chfyq]))
                erlz__duutc = getattr(pdaw__gxov, f'block_{vdg__chfyq}')
                yaicl__ggfx = ListInstance(context, builder, types.List(t),
                    erlz__duutc)
                vlb__xmzay = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(vda__oakrf.
                    block_to_arr_ind[vdg__chfyq], dtype=np.int64))
                jnn__nfg = context.make_array(types.Array(types.int64, 1, 'C')
                    )(context, builder, vlb__xmzay)
                with cgutils.for_range(builder, ndf__ajrh) as tfsa__mtavk:
                    tgpp__rgkh = tfsa__mtavk.index
                    pjvu__btud = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        jnn__nfg, tgpp__rgkh)
                    urr__vfuj = signature(types.none, vda__oakrf, types.
                        List(t), types.int64, types.int64)
                    rcu__uml = py_table, erlz__duutc, tgpp__rgkh, pjvu__btud
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, urr__vfuj, rcu__uml)
                    arr = yaicl__ggfx.getitem(tgpp__rgkh)
                    kkrl__vsak = signature(array_info_type, t)
                    lzu__dax = arr,
                    zvv__qwfcq = array_to_info_codegen(context, builder,
                        kkrl__vsak, lzu__dax)
                    luf__okv.inititem(pjvu__btud, zvv__qwfcq, incref=False)
        quhc__stewx = luf__okv.value
        sjrdy__ryy = signature(table_type, types.List(array_info_type))
        dhvg__zspg = quhc__stewx,
        cpp_table = arr_info_list_to_table_codegen(context, builder,
            sjrdy__ryy, dhvg__zspg)
        context.nrt.decref(builder, types.List(array_info_type), quhc__stewx)
        return cpp_table
    return table_type(vda__oakrf, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def py_data_to_cpp_table(py_table, extra_arrs_tup, in_col_inds_t,
    n_table_cols_t):
    omqpy__iko = in_col_inds_t.instance_type.meta
    uzo__zxz = {}
    gpa__ond = get_overload_const_int(n_table_cols_t)
    cszl__elnuc = defaultdict(list)
    xtfr__vud = {}
    for tgpp__rgkh, rswq__prtg in enumerate(omqpy__iko):
        if rswq__prtg in xtfr__vud:
            cszl__elnuc[rswq__prtg].append(tgpp__rgkh)
        else:
            xtfr__vud[rswq__prtg] = tgpp__rgkh
    qgkd__rafw = (
        'def impl(py_table, extra_arrs_tup, in_col_inds_t, n_table_cols_t):\n')
    qgkd__rafw += (
        f'  cpp_arr_list = alloc_empty_list_type({len(omqpy__iko)}, array_info_type)\n'
        )
    if py_table != types.none:
        for vdg__chfyq in py_table.type_to_blk.values():
            ngkjj__zfusl = [xtfr__vud.get(tgpp__rgkh, -1) for tgpp__rgkh in
                py_table.block_to_arr_ind[vdg__chfyq]]
            uzo__zxz[f'out_inds_{vdg__chfyq}'] = np.array(ngkjj__zfusl, np.
                int64)
            uzo__zxz[f'arr_inds_{vdg__chfyq}'] = np.array(py_table.
                block_to_arr_ind[vdg__chfyq], np.int64)
            qgkd__rafw += (
                f'  arr_list_{vdg__chfyq} = get_table_block(py_table, {vdg__chfyq})\n'
                )
            qgkd__rafw += f'  for i in range(len(arr_list_{vdg__chfyq})):\n'
            qgkd__rafw += (
                f'    out_arr_ind_{vdg__chfyq} = out_inds_{vdg__chfyq}[i]\n')
            qgkd__rafw += f'    if out_arr_ind_{vdg__chfyq} == -1:\n'
            qgkd__rafw += f'      continue\n'
            qgkd__rafw += (
                f'    arr_ind_{vdg__chfyq} = arr_inds_{vdg__chfyq}[i]\n')
            qgkd__rafw += f"""    ensure_column_unboxed(py_table, arr_list_{vdg__chfyq}, i, arr_ind_{vdg__chfyq})
"""
            qgkd__rafw += f"""    cpp_arr_list[out_arr_ind_{vdg__chfyq}] = array_to_info(arr_list_{vdg__chfyq}[i])
"""
        for pks__pwjb, roicn__dhk in cszl__elnuc.items():
            if pks__pwjb < gpa__ond:
                vdg__chfyq = py_table.block_nums[pks__pwjb]
                ozsp__tqlss = py_table.block_offsets[pks__pwjb]
                for umjyw__rgcx in roicn__dhk:
                    qgkd__rafw += f"""  cpp_arr_list[{umjyw__rgcx}] = array_to_info(arr_list_{vdg__chfyq}[{ozsp__tqlss}])
"""
    for tgpp__rgkh in range(len(extra_arrs_tup)):
        ytqk__phgw = xtfr__vud.get(gpa__ond + tgpp__rgkh, -1)
        if ytqk__phgw != -1:
            ooq__xqt = [ytqk__phgw] + cszl__elnuc.get(gpa__ond + tgpp__rgkh, []
                )
            for umjyw__rgcx in ooq__xqt:
                qgkd__rafw += f"""  cpp_arr_list[{umjyw__rgcx}] = array_to_info(extra_arrs_tup[{tgpp__rgkh}])
"""
    qgkd__rafw += f'  return arr_info_list_to_table(cpp_arr_list)\n'
    uzo__zxz.update({'array_info_type': array_info_type,
        'alloc_empty_list_type': bodo.hiframes.table.alloc_empty_list_type,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'ensure_column_unboxed': bodo.hiframes.table.ensure_column_unboxed,
        'array_to_info': array_to_info, 'arr_info_list_to_table':
        arr_info_list_to_table})
    fqo__lhm = {}
    exec(qgkd__rafw, uzo__zxz, fqo__lhm)
    return fqo__lhm['impl']


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
        ywj__aklwu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='delete_table')
        builder.call(uddaa__eak, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='shuffle_table')
        ayqcb__xttas = builder.call(uddaa__eak, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return ayqcb__xttas
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
        ywj__aklwu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='delete_shuffle_info')
        return builder.call(uddaa__eak, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='reverse_shuffle_table')
        return builder.call(uddaa__eak, args)
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
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(64), lir.IntType(8).as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='hash_join_table')
        ayqcb__xttas = builder.call(uddaa__eak, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return ayqcb__xttas
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
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64), lir.
            IntType(8).as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='cross_join_table')
        ayqcb__xttas = builder.call(uddaa__eak, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return ayqcb__xttas
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.boolean, types.boolean, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.int64, types.voidptr, types.
        int64, types.voidptr), codegen


@intrinsic
def sort_values_table(typingctx, table_t, n_keys_t, vect_ascending_t,
    na_position_b_t, dead_keys_t, n_rows_t, bounds_t, parallel_t):
    assert table_t == table_type, 'C++ table type expected'

    def codegen(context, builder, sig, args):
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1)])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='sort_values_table')
        ayqcb__xttas = builder.call(uddaa__eak, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return ayqcb__xttas
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='sample_table')
        ayqcb__xttas = builder.call(uddaa__eak, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return ayqcb__xttas
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='shuffle_renormalization')
        ayqcb__xttas = builder.call(uddaa__eak, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return ayqcb__xttas
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='shuffle_renormalization_group')
        ayqcb__xttas = builder.call(uddaa__eak, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return ayqcb__xttas
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='drop_duplicates_table')
        ayqcb__xttas = builder.call(uddaa__eak, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return ayqcb__xttas
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
        ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        uddaa__eak = cgutils.get_or_insert_function(builder.module,
            ywj__aklwu, name='groupby_and_aggregate')
        ayqcb__xttas = builder.call(uddaa__eak, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return ayqcb__xttas
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
    hutol__sci = array_to_info(dict_arr)
    _drop_duplicates_local_dictionary(hutol__sci, sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(hutol__sci, bodo.dict_str_arr_type)
    return out_arr


_convert_local_dictionary_to_global = types.ExternalFunction(
    'convert_local_dictionary_to_global', types.void(array_info_type, types
    .bool_, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def convert_local_dictionary_to_global(dict_arr, sort_dictionary,
    is_parallel=False):
    hutol__sci = array_to_info(dict_arr)
    _convert_local_dictionary_to_global(hutol__sci, is_parallel,
        sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(hutol__sci, bodo.dict_str_arr_type)
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
    hxxcb__xkuj = array_to_info(in_arr)
    qqdvr__phyn = array_to_info(in_values)
    qlpl__eigys = array_to_info(out_arr)
    yfqj__uor = arr_info_list_to_table([hxxcb__xkuj, qqdvr__phyn, qlpl__eigys])
    _array_isin(qlpl__eigys, hxxcb__xkuj, qqdvr__phyn, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(yfqj__uor)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, match, pat, out_arr):
    hxxcb__xkuj = array_to_info(in_arr)
    qlpl__eigys = array_to_info(out_arr)
    _get_search_regex(hxxcb__xkuj, case, match, pat, qlpl__eigys)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    ockx__tnllv = col_array_typ.dtype
    if isinstance(ockx__tnllv, (types.Number, TimeType, bodo.libs.
        pd_datetime_arr_ext.PandasDatetimeTZDtype)) or ockx__tnllv in [bodo
        .datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:
        if isinstance(ockx__tnllv, bodo.libs.pd_datetime_arr_ext.
            PandasDatetimeTZDtype):
            ockx__tnllv = bodo.datetime64ns

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                qduk__qffb, gjotu__syrkb = args
                qduk__qffb = builder.bitcast(qduk__qffb, lir.IntType(8).
                    as_pointer().as_pointer())
                cmt__agvri = lir.Constant(lir.IntType(64), c_ind)
                hsz__etjxl = builder.load(builder.gep(qduk__qffb, [cmt__agvri])
                    )
                hsz__etjxl = builder.bitcast(hsz__etjxl, context.
                    get_data_type(ockx__tnllv).as_pointer())
                return context.unpack_value(builder, ockx__tnllv, builder.
                    gep(hsz__etjxl, [gjotu__syrkb]))
            return ockx__tnllv(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ in (bodo.string_array_type, bodo.binary_array_type):

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                qduk__qffb, gjotu__syrkb = args
                qduk__qffb = builder.bitcast(qduk__qffb, lir.IntType(8).
                    as_pointer().as_pointer())
                cmt__agvri = lir.Constant(lir.IntType(64), c_ind)
                hsz__etjxl = builder.load(builder.gep(qduk__qffb, [cmt__agvri])
                    )
                ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                ceutu__nij = cgutils.get_or_insert_function(builder.module,
                    ywj__aklwu, name='array_info_getitem')
                ahvl__ylvh = cgutils.alloca_once(builder, lir.IntType(64))
                args = hsz__etjxl, gjotu__syrkb, ahvl__ylvh
                hzjx__pxapj = builder.call(ceutu__nij, args)
                xti__jub = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    xti__jub, [hzjx__pxapj, builder.load(ahvl__ylvh)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                wrbb__scowl = lir.Constant(lir.IntType(64), 1)
                lfbb__sklwp = lir.Constant(lir.IntType(64), 2)
                qduk__qffb, gjotu__syrkb = args
                qduk__qffb = builder.bitcast(qduk__qffb, lir.IntType(8).
                    as_pointer().as_pointer())
                cmt__agvri = lir.Constant(lir.IntType(64), c_ind)
                hsz__etjxl = builder.load(builder.gep(qduk__qffb, [cmt__agvri])
                    )
                ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                bdnwt__pwkpe = cgutils.get_or_insert_function(builder.
                    module, ywj__aklwu, name='get_nested_info')
                args = hsz__etjxl, lfbb__sklwp
                mrriu__tfxpv = builder.call(bdnwt__pwkpe, args)
                ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                old__shdnf = cgutils.get_or_insert_function(builder.module,
                    ywj__aklwu, name='array_info_getdata1')
                args = mrriu__tfxpv,
                ojfaj__ffda = builder.call(old__shdnf, args)
                ojfaj__ffda = builder.bitcast(ojfaj__ffda, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                tpsbx__bfffq = builder.sext(builder.load(builder.gep(
                    ojfaj__ffda, [gjotu__syrkb])), lir.IntType(64))
                args = hsz__etjxl, wrbb__scowl
                ozo__ojs = builder.call(bdnwt__pwkpe, args)
                ywj__aklwu = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                ceutu__nij = cgutils.get_or_insert_function(builder.module,
                    ywj__aklwu, name='array_info_getitem')
                ahvl__ylvh = cgutils.alloca_once(builder, lir.IntType(64))
                args = ozo__ojs, tpsbx__bfffq, ahvl__ylvh
                hzjx__pxapj = builder.call(ceutu__nij, args)
                xti__jub = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    xti__jub, [hzjx__pxapj, builder.load(ahvl__ylvh)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{ockx__tnllv}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if isinstance(col_array_dtype, (IntegerArrayType, FloatingArrayType,
        bodo.TimeArrayType)) or col_array_dtype in (bodo.libs.bool_arr_ext.
        boolean_array, bodo.binary_array_type, bodo.datetime_date_array_type
        ) or is_str_arr_type(col_array_dtype):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                mdyc__coz, gjotu__syrkb = args
                mdyc__coz = builder.bitcast(mdyc__coz, lir.IntType(8).
                    as_pointer().as_pointer())
                cmt__agvri = lir.Constant(lir.IntType(64), c_ind)
                hsz__etjxl = builder.load(builder.gep(mdyc__coz, [cmt__agvri]))
                ngrr__ntv = builder.bitcast(hsz__etjxl, context.
                    get_data_type(types.bool_).as_pointer())
                cwra__scsb = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    ngrr__ntv, gjotu__syrkb)
                ewa__hvfd = builder.icmp_unsigned('!=', cwra__scsb, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(ewa__hvfd, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, (types.Array, bodo.DatetimeArrayType)):
        ockx__tnllv = col_array_dtype.dtype
        if ockx__tnllv in [bodo.datetime64ns, bodo.timedelta64ns
            ] or isinstance(ockx__tnllv, bodo.libs.pd_datetime_arr_ext.
            PandasDatetimeTZDtype):
            if isinstance(ockx__tnllv, bodo.libs.pd_datetime_arr_ext.
                PandasDatetimeTZDtype):
                ockx__tnllv = bodo.datetime64ns

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    qduk__qffb, gjotu__syrkb = args
                    qduk__qffb = builder.bitcast(qduk__qffb, lir.IntType(8)
                        .as_pointer().as_pointer())
                    cmt__agvri = lir.Constant(lir.IntType(64), c_ind)
                    hsz__etjxl = builder.load(builder.gep(qduk__qffb, [
                        cmt__agvri]))
                    hsz__etjxl = builder.bitcast(hsz__etjxl, context.
                        get_data_type(ockx__tnllv).as_pointer())
                    uezyq__ntkkw = builder.load(builder.gep(hsz__etjxl, [
                        gjotu__syrkb]))
                    ewa__hvfd = builder.icmp_unsigned('!=', uezyq__ntkkw,
                        lir.Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(ewa__hvfd, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(ockx__tnllv, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    qduk__qffb, gjotu__syrkb = args
                    qduk__qffb = builder.bitcast(qduk__qffb, lir.IntType(8)
                        .as_pointer().as_pointer())
                    cmt__agvri = lir.Constant(lir.IntType(64), c_ind)
                    hsz__etjxl = builder.load(builder.gep(qduk__qffb, [
                        cmt__agvri]))
                    hsz__etjxl = builder.bitcast(hsz__etjxl, context.
                        get_data_type(ockx__tnllv).as_pointer())
                    uezyq__ntkkw = builder.load(builder.gep(hsz__etjxl, [
                        gjotu__syrkb]))
                    inz__gta = signature(types.bool_, ockx__tnllv)
                    cwra__scsb = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, inz__gta, (uezyq__ntkkw,))
                    return builder.not_(builder.sext(cwra__scsb, lir.
                        IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
