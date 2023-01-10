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
        foac__pip = context.make_helper(builder, arr_type, in_arr)
        in_arr = foac__pip.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        kwyzn__krh = context.make_helper(builder, arr_type, in_arr)
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='list_string_array_to_info')
        return builder.call(fnp__rau, [kwyzn__krh.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                dus__reo = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for dcdj__oboim in arr_typ.data:
                    dus__reo += get_types(dcdj__oboim)
                return dus__reo
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
                pmj__xwbb = context.make_helper(builder, arr_typ, value=arr)
                qnn__njzy = get_lengths(_get_map_arr_data_type(arr_typ),
                    pmj__xwbb.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                gjnbm__drlw = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                qnn__njzy = get_lengths(arr_typ.dtype, gjnbm__drlw.data)
                qnn__njzy = cgutils.pack_array(builder, [gjnbm__drlw.
                    n_arrays] + [builder.extract_value(qnn__njzy,
                    sszns__uqeoj) for sszns__uqeoj in range(qnn__njzy.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                gjnbm__drlw = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                qnn__njzy = []
                for sszns__uqeoj, dcdj__oboim in enumerate(arr_typ.data):
                    irzo__rcoj = get_lengths(dcdj__oboim, builder.
                        extract_value(gjnbm__drlw.data, sszns__uqeoj))
                    qnn__njzy += [builder.extract_value(irzo__rcoj,
                        xxwx__pqy) for xxwx__pqy in range(irzo__rcoj.type.
                        count)]
                qnn__njzy = cgutils.pack_array(builder, [length, context.
                    get_constant(types.int64, -1)] + qnn__njzy)
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType, types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                qnn__njzy = cgutils.pack_array(builder, [length])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return qnn__njzy

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                pmj__xwbb = context.make_helper(builder, arr_typ, value=arr)
                dctw__wjnai = get_buffers(_get_map_arr_data_type(arr_typ),
                    pmj__xwbb.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                gjnbm__drlw = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                rsnb__cbl = get_buffers(arr_typ.dtype, gjnbm__drlw.data)
                gzjjw__ygfnd = context.make_array(types.Array(offset_type, 
                    1, 'C'))(context, builder, gjnbm__drlw.offsets)
                fxxqa__pmct = builder.bitcast(gzjjw__ygfnd.data, lir.
                    IntType(8).as_pointer())
                rckkp__svmyd = context.make_array(types.Array(types.uint8, 
                    1, 'C'))(context, builder, gjnbm__drlw.null_bitmap)
                vywkr__jicd = builder.bitcast(rckkp__svmyd.data, lir.
                    IntType(8).as_pointer())
                dctw__wjnai = cgutils.pack_array(builder, [fxxqa__pmct,
                    vywkr__jicd] + [builder.extract_value(rsnb__cbl,
                    sszns__uqeoj) for sszns__uqeoj in range(rsnb__cbl.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                gjnbm__drlw = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                rsnb__cbl = []
                for sszns__uqeoj, dcdj__oboim in enumerate(arr_typ.data):
                    tobh__sqs = get_buffers(dcdj__oboim, builder.
                        extract_value(gjnbm__drlw.data, sszns__uqeoj))
                    rsnb__cbl += [builder.extract_value(tobh__sqs,
                        xxwx__pqy) for xxwx__pqy in range(tobh__sqs.type.count)
                        ]
                rckkp__svmyd = context.make_array(types.Array(types.uint8, 
                    1, 'C'))(context, builder, gjnbm__drlw.null_bitmap)
                vywkr__jicd = builder.bitcast(rckkp__svmyd.data, lir.
                    IntType(8).as_pointer())
                dctw__wjnai = cgutils.pack_array(builder, [vywkr__jicd] +
                    rsnb__cbl)
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType)) or arr_typ in (boolean_array,
                datetime_date_array_type):
                zff__gfkef = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    zff__gfkef = int128_type
                elif arr_typ == datetime_date_array_type:
                    zff__gfkef = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                mnrp__iey = context.make_array(types.Array(zff__gfkef, 1, 'C')
                    )(context, builder, arr.data)
                rckkp__svmyd = context.make_array(types.Array(types.uint8, 
                    1, 'C'))(context, builder, arr.null_bitmap)
                xoqa__ibs = builder.bitcast(mnrp__iey.data, lir.IntType(8).
                    as_pointer())
                vywkr__jicd = builder.bitcast(rckkp__svmyd.data, lir.
                    IntType(8).as_pointer())
                dctw__wjnai = cgutils.pack_array(builder, [vywkr__jicd,
                    xoqa__ibs])
            elif arr_typ in (string_array_type, binary_array_type):
                gjnbm__drlw = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                meatt__axtg = context.make_helper(builder, offset_arr_type,
                    gjnbm__drlw.offsets).data
                data = context.make_helper(builder, char_arr_type,
                    gjnbm__drlw.data).data
                qqtj__zfref = context.make_helper(builder,
                    null_bitmap_arr_type, gjnbm__drlw.null_bitmap).data
                dctw__wjnai = cgutils.pack_array(builder, [builder.bitcast(
                    meatt__axtg, lir.IntType(8).as_pointer()), builder.
                    bitcast(qqtj__zfref, lir.IntType(8).as_pointer()),
                    builder.bitcast(data, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                xoqa__ibs = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                tzu__nvowd = lir.Constant(lir.IntType(8).as_pointer(), None)
                dctw__wjnai = cgutils.pack_array(builder, [tzu__nvowd,
                    xoqa__ibs])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return dctw__wjnai

        def get_field_names(arr_typ):
            dlssx__tyyim = []
            if isinstance(arr_typ, StructArrayType):
                for rzkv__xth, hkng__brf in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    dlssx__tyyim.append(rzkv__xth)
                    dlssx__tyyim += get_field_names(hkng__brf)
            elif isinstance(arr_typ, ArrayItemArrayType):
                dlssx__tyyim += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                dlssx__tyyim += get_field_names(_get_map_arr_data_type(arr_typ)
                    )
            return dlssx__tyyim
        dus__reo = get_types(arr_type)
        ucftj__jvg = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in dus__reo])
        qiubs__iyh = cgutils.alloca_once_value(builder, ucftj__jvg)
        qnn__njzy = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, qnn__njzy)
        dctw__wjnai = get_buffers(arr_type, in_arr)
        mkkwu__vki = cgutils.alloca_once_value(builder, dctw__wjnai)
        dlssx__tyyim = get_field_names(arr_type)
        if len(dlssx__tyyim) == 0:
            dlssx__tyyim = ['irrelevant']
        eabt__iei = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in dlssx__tyyim])
        mof__vhwec = cgutils.alloca_once_value(builder, eabt__iei)
        if isinstance(arr_type, MapArrayType):
            hlixn__cdf = _get_map_arr_data_type(arr_type)
            uubk__mqcr = context.make_helper(builder, arr_type, value=in_arr)
            fav__efc = uubk__mqcr.data
        else:
            hlixn__cdf = arr_type
            fav__efc = in_arr
        lrs__tyi = context.make_helper(builder, hlixn__cdf, fav__efc)
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='nested_array_to_info')
        zqjhu__fvjrz = builder.call(fnp__rau, [builder.bitcast(qiubs__iyh,
            lir.IntType(32).as_pointer()), builder.bitcast(mkkwu__vki, lir.
            IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            mof__vhwec, lir.IntType(8).as_pointer()), lrs__tyi.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return zqjhu__fvjrz
    if arr_type in (string_array_type, binary_array_type):
        nna__hqwn = context.make_helper(builder, arr_type, in_arr)
        wva__gkg = ArrayItemArrayType(char_arr_type)
        kwyzn__krh = context.make_helper(builder, wva__gkg, nna__hqwn.data)
        gjnbm__drlw = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        meatt__axtg = context.make_helper(builder, offset_arr_type,
            gjnbm__drlw.offsets).data
        data = context.make_helper(builder, char_arr_type, gjnbm__drlw.data
            ).data
        qqtj__zfref = context.make_helper(builder, null_bitmap_arr_type,
            gjnbm__drlw.null_bitmap).data
        kru__ogl = builder.zext(builder.load(builder.gep(meatt__axtg, [
            gjnbm__drlw.n_arrays])), lir.IntType(64))
        eyg__khch = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='string_array_to_info')
        return builder.call(fnp__rau, [gjnbm__drlw.n_arrays, kru__ogl, data,
            meatt__axtg, qqtj__zfref, kwyzn__krh.meminfo, eyg__khch])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        szcny__enwmo = arr.data
        xiggi__bkpi = arr.indices
        sig = array_info_type(arr_type.data)
        xxbi__wdv = array_to_info_codegen(context, builder, sig, (
            szcny__enwmo,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        sudr__zgddx = array_to_info_codegen(context, builder, sig, (
            xiggi__bkpi,), False)
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(32), lir.IntType(32)])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='dict_str_array_to_info')
        vffd__tazv = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        mca__ghkyk = builder.zext(arr.has_deduped_local_dictionary, lir.
            IntType(32))
        return builder.call(fnp__rau, [xxbi__wdv, sudr__zgddx, vffd__tazv,
            mca__ghkyk])
    emo__qazr = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        ouo__mem = context.compile_internal(builder, lambda a: len(a.dtype.
            categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        wsm__jfg = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(wsm__jfg, 1, 'C')
        emo__qazr = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if emo__qazr:
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
        fnp__vdb = arr_type.dtype
        jcb__yqha = numba_to_c_type(fnp__vdb)
        irj__env = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), jcb__yqha))
        if emo__qazr:
            zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(64), lir.IntType(8).as_pointer()])
            fnp__rau = cgutils.get_or_insert_function(builder.module,
                zea__zvu, name='categorical_array_to_info')
            return builder.call(fnp__rau, [length, builder.bitcast(arr.data,
                lir.IntType(8).as_pointer()), builder.load(irj__env),
                ouo__mem, arr.meminfo])
        else:
            zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer()])
            fnp__rau = cgutils.get_or_insert_function(builder.module,
                zea__zvu, name='numpy_array_to_info')
            return builder.call(fnp__rau, [length, builder.bitcast(arr.data,
                lir.IntType(8).as_pointer()), builder.load(irj__env), arr.
                meminfo])
    if isinstance(arr_type, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, TimeArrayType)) or arr_type in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        fnp__vdb = arr_type.dtype
        zff__gfkef = fnp__vdb
        if isinstance(arr_type, DecimalArrayType):
            zff__gfkef = int128_type
        if arr_type == datetime_date_array_type:
            zff__gfkef = types.int64
        mnrp__iey = context.make_array(types.Array(zff__gfkef, 1, 'C'))(context
            , builder, arr.data)
        length = builder.extract_value(mnrp__iey.shape, 0)
        rzilm__ilrpg = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        jcb__yqha = numba_to_c_type(fnp__vdb)
        irj__env = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), jcb__yqha))
        if isinstance(arr_type, DecimalArrayType):
            zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
            fnp__rau = cgutils.get_or_insert_function(builder.module,
                zea__zvu, name='decimal_array_to_info')
            return builder.call(fnp__rau, [length, builder.bitcast(
                mnrp__iey.data, lir.IntType(8).as_pointer()), builder.load(
                irj__env), builder.bitcast(rzilm__ilrpg.data, lir.IntType(8
                ).as_pointer()), mnrp__iey.meminfo, rzilm__ilrpg.meminfo,
                context.get_constant(types.int32, arr_type.precision),
                context.get_constant(types.int32, arr_type.scale)])
        elif isinstance(arr_type, TimeArrayType):
            zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32)])
            fnp__rau = cgutils.get_or_insert_function(builder.module,
                zea__zvu, name='time_array_to_info')
            return builder.call(fnp__rau, [length, builder.bitcast(
                mnrp__iey.data, lir.IntType(8).as_pointer()), builder.load(
                irj__env), builder.bitcast(rzilm__ilrpg.data, lir.IntType(8
                ).as_pointer()), mnrp__iey.meminfo, rzilm__ilrpg.meminfo,
                lir.Constant(lir.IntType(32), arr_type.precision)])
        else:
            zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer()])
            fnp__rau = cgutils.get_or_insert_function(builder.module,
                zea__zvu, name='nullable_array_to_info')
            return builder.call(fnp__rau, [length, builder.bitcast(
                mnrp__iey.data, lir.IntType(8).as_pointer()), builder.load(
                irj__env), builder.bitcast(rzilm__ilrpg.data, lir.IntType(8
                ).as_pointer()), mnrp__iey.meminfo, rzilm__ilrpg.meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        jthiz__jqxxq = context.make_array(arr_type.arr_type)(context,
            builder, arr.left)
        gtrs__mbyu = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        length = builder.extract_value(jthiz__jqxxq.shape, 0)
        jcb__yqha = numba_to_c_type(arr_type.arr_type.dtype)
        irj__env = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), jcb__yqha))
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='interval_array_to_info')
        return builder.call(fnp__rau, [length, builder.bitcast(jthiz__jqxxq
            .data, lir.IntType(8).as_pointer()), builder.bitcast(gtrs__mbyu
            .data, lir.IntType(8).as_pointer()), builder.load(irj__env),
            jthiz__jqxxq.meminfo, gtrs__mbyu.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    dovfs__cink = cgutils.alloca_once(builder, lir.IntType(64))
    xoqa__ibs = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    yblwg__lvsih = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    zea__zvu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer(
        ), lir.IntType(64).as_pointer(), lir.IntType(8).as_pointer().
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
        name='info_to_numpy_array')
    builder.call(fnp__rau, [in_info, dovfs__cink, xoqa__ibs, yblwg__lvsih])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    dsi__ndur = context.get_value_type(types.intp)
    wfqzx__pxanw = cgutils.pack_array(builder, [builder.load(dovfs__cink)],
        ty=dsi__ndur)
    ztd__yonl = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    cof__sxn = cgutils.pack_array(builder, [ztd__yonl], ty=dsi__ndur)
    data = builder.bitcast(builder.load(xoqa__ibs), context.get_data_type(
        arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=data, shape=wfqzx__pxanw,
        strides=cof__sxn, itemsize=ztd__yonl, meminfo=builder.load(
        yblwg__lvsih))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    fryye__nsb = context.make_helper(builder, arr_type)
    zea__zvu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer(
        ), lir.IntType(8).as_pointer().as_pointer()])
    fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
        name='info_to_list_string_array')
    builder.call(fnp__rau, [in_info, fryye__nsb._get_ptr_by_name('meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return fryye__nsb._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    gqcvx__ivy = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        qbdy__dpsk = lengths_pos
        lghr__fgv = infos_pos
        jxpu__dhg, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        ael__eeaf = ArrayItemArrayPayloadType(arr_typ)
        bzmzg__wtm = context.get_data_type(ael__eeaf)
        owg__xzbbj = context.get_abi_sizeof(bzmzg__wtm)
        gcua__jtswh = define_array_item_dtor(context, builder, arr_typ,
            ael__eeaf)
        vshai__ztkx = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, owg__xzbbj), gcua__jtswh)
        qgli__ujfr = context.nrt.meminfo_data(builder, vshai__ztkx)
        uvjg__fkj = builder.bitcast(qgli__ujfr, bzmzg__wtm.as_pointer())
        gjnbm__drlw = cgutils.create_struct_proxy(ael__eeaf)(context, builder)
        gjnbm__drlw.n_arrays = builder.extract_value(builder.load(
            lengths_ptr), qbdy__dpsk)
        gjnbm__drlw.data = jxpu__dhg
        akz__xmdke = builder.load(array_infos_ptr)
        ozix__dlsy = builder.bitcast(builder.extract_value(akz__xmdke,
            lghr__fgv), gqcvx__ivy)
        gjnbm__drlw.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, ozix__dlsy)
        mhei__grpw = builder.bitcast(builder.extract_value(akz__xmdke, 
            lghr__fgv + 1), gqcvx__ivy)
        gjnbm__drlw.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, mhei__grpw)
        builder.store(gjnbm__drlw._getvalue(), uvjg__fkj)
        kwyzn__krh = context.make_helper(builder, arr_typ)
        kwyzn__krh.meminfo = vshai__ztkx
        return kwyzn__krh._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        xxtdx__ukln = []
        lghr__fgv = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for jtr__tdqay in arr_typ.data:
            jxpu__dhg, lengths_pos, infos_pos = nested_to_array(context,
                builder, jtr__tdqay, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            xxtdx__ukln.append(jxpu__dhg)
        ael__eeaf = StructArrayPayloadType(arr_typ.data)
        bzmzg__wtm = context.get_value_type(ael__eeaf)
        owg__xzbbj = context.get_abi_sizeof(bzmzg__wtm)
        gcua__jtswh = define_struct_arr_dtor(context, builder, arr_typ,
            ael__eeaf)
        vshai__ztkx = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, owg__xzbbj), gcua__jtswh)
        qgli__ujfr = context.nrt.meminfo_data(builder, vshai__ztkx)
        uvjg__fkj = builder.bitcast(qgli__ujfr, bzmzg__wtm.as_pointer())
        gjnbm__drlw = cgutils.create_struct_proxy(ael__eeaf)(context, builder)
        gjnbm__drlw.data = cgutils.pack_array(builder, xxtdx__ukln
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, xxtdx__ukln)
        akz__xmdke = builder.load(array_infos_ptr)
        mhei__grpw = builder.bitcast(builder.extract_value(akz__xmdke,
            lghr__fgv), gqcvx__ivy)
        gjnbm__drlw.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, mhei__grpw)
        builder.store(gjnbm__drlw._getvalue(), uvjg__fkj)
        gbwk__dpiq = context.make_helper(builder, arr_typ)
        gbwk__dpiq.meminfo = vshai__ztkx
        return gbwk__dpiq._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        akz__xmdke = builder.load(array_infos_ptr)
        dtbzg__xcau = builder.bitcast(builder.extract_value(akz__xmdke,
            infos_pos), gqcvx__ivy)
        nna__hqwn = context.make_helper(builder, arr_typ)
        wva__gkg = ArrayItemArrayType(char_arr_type)
        kwyzn__krh = context.make_helper(builder, wva__gkg)
        zea__zvu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='info_to_string_array')
        builder.call(fnp__rau, [dtbzg__xcau, kwyzn__krh._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        nna__hqwn.data = kwyzn__krh._getvalue()
        return nna__hqwn._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        akz__xmdke = builder.load(array_infos_ptr)
        tfh__wmp = builder.bitcast(builder.extract_value(akz__xmdke, 
            infos_pos + 1), gqcvx__ivy)
        return _lower_info_to_array_numpy(arr_typ, context, builder, tfh__wmp
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType)) or arr_typ in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        zff__gfkef = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            zff__gfkef = int128_type
        elif arr_typ == datetime_date_array_type:
            zff__gfkef = types.int64
        akz__xmdke = builder.load(array_infos_ptr)
        mhei__grpw = builder.bitcast(builder.extract_value(akz__xmdke,
            infos_pos), gqcvx__ivy)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, mhei__grpw)
        tfh__wmp = builder.bitcast(builder.extract_value(akz__xmdke, 
            infos_pos + 1), gqcvx__ivy)
        arr.data = _lower_info_to_array_numpy(types.Array(zff__gfkef, 1,
            'C'), context, builder, tfh__wmp)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, iai__ihm = args
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
                return 1 + sum([get_num_arrays(jtr__tdqay) for jtr__tdqay in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(jtr__tdqay) for jtr__tdqay in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            hwp__keb = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            hwp__keb = _get_map_arr_data_type(arr_type)
        else:
            hwp__keb = arr_type
        uwa__liyg = get_num_arrays(hwp__keb)
        qnn__njzy = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), 0) for iai__ihm in range(uwa__liyg)])
        lengths_ptr = cgutils.alloca_once_value(builder, qnn__njzy)
        tzu__nvowd = lir.Constant(lir.IntType(8).as_pointer(), None)
        mngh__woej = cgutils.pack_array(builder, [tzu__nvowd for iai__ihm in
            range(get_num_infos(hwp__keb))])
        array_infos_ptr = cgutils.alloca_once_value(builder, mngh__woej)
        zea__zvu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='info_to_nested_array')
        builder.call(fnp__rau, [in_info, builder.bitcast(lengths_ptr, lir.
            IntType(64).as_pointer()), builder.bitcast(array_infos_ptr, lir
            .IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, iai__ihm, iai__ihm = nested_to_array(context, builder,
            hwp__keb, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            foac__pip = context.make_helper(builder, arr_type)
            foac__pip.data = arr
            context.nrt.incref(builder, hwp__keb, arr)
            arr = foac__pip._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, hwp__keb)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        nna__hqwn = context.make_helper(builder, arr_type)
        wva__gkg = ArrayItemArrayType(char_arr_type)
        kwyzn__krh = context.make_helper(builder, wva__gkg)
        zea__zvu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='info_to_string_array')
        builder.call(fnp__rau, [in_info, kwyzn__krh._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        nna__hqwn.data = kwyzn__krh._getvalue()
        return nna__hqwn._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='get_nested_info')
        xxbi__wdv = builder.call(fnp__rau, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        sudr__zgddx = builder.call(fnp__rau, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        qal__butav = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        qal__butav.data = info_to_array_codegen(context, builder, sig, (
            xxbi__wdv, context.get_constant_null(arr_type.data)))
        knyr__hbi = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = knyr__hbi(array_info_type, knyr__hbi)
        qal__butav.indices = info_to_array_codegen(context, builder, sig, (
            sudr__zgddx, context.get_constant_null(knyr__hbi)))
        zea__zvu = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='get_has_global_dictionary')
        vffd__tazv = builder.call(fnp__rau, [in_info])
        qal__butav.has_global_dictionary = builder.trunc(vffd__tazv,
            cgutils.bool_t)
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='get_has_deduped_local_dictionary')
        mca__ghkyk = builder.call(fnp__rau, [in_info])
        qal__butav.has_deduped_local_dictionary = builder.trunc(mca__ghkyk,
            cgutils.bool_t)
        return qal__butav._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        wsm__jfg = get_categories_int_type(arr_type.dtype)
        pkpy__uqerx = types.Array(wsm__jfg, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(pkpy__uqerx, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            ogfiz__smzyi = bodo.utils.utils.create_categorical_type(arr_type
                .dtype.categories, arr_type.dtype.data.data, is_ordered)
            new_cats_tup = MetaType(tuple(ogfiz__smzyi))
            int_type = arr_type.dtype.int_type
            ofibg__mkbum = arr_type.dtype.data.data
            tiich__qncr = context.get_constant_generic(builder,
                ofibg__mkbum, ogfiz__smzyi)
            fnp__vdb = context.compile_internal(builder, lambda c_arr: bodo
                .hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(ofibg__mkbum), [tiich__qncr])
        else:
            fnp__vdb = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, fnp__vdb)
        out_arr.dtype = fnp__vdb
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
        zff__gfkef = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            zff__gfkef = int128_type
        elif arr_type == datetime_date_array_type:
            zff__gfkef = types.int64
        adro__kdi = types.Array(zff__gfkef, 1, 'C')
        mnrp__iey = context.make_array(adro__kdi)(context, builder)
        eqad__nwur = types.Array(types.uint8, 1, 'C')
        bujn__ylnsz = context.make_array(eqad__nwur)(context, builder)
        dovfs__cink = cgutils.alloca_once(builder, lir.IntType(64))
        sbtz__fle = cgutils.alloca_once(builder, lir.IntType(64))
        xoqa__ibs = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        oruk__amoh = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        yblwg__lvsih = cgutils.alloca_once(builder, lir.IntType(8).as_pointer()
            )
        appvf__csc = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        zea__zvu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='info_to_nullable_array')
        builder.call(fnp__rau, [in_info, dovfs__cink, sbtz__fle, xoqa__ibs,
            oruk__amoh, yblwg__lvsih, appvf__csc])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        dsi__ndur = context.get_value_type(types.intp)
        wfqzx__pxanw = cgutils.pack_array(builder, [builder.load(
            dovfs__cink)], ty=dsi__ndur)
        ztd__yonl = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(zff__gfkef)))
        cof__sxn = cgutils.pack_array(builder, [ztd__yonl], ty=dsi__ndur)
        data = builder.bitcast(builder.load(xoqa__ibs), context.
            get_data_type(zff__gfkef).as_pointer())
        numba.np.arrayobj.populate_array(mnrp__iey, data=data, shape=
            wfqzx__pxanw, strides=cof__sxn, itemsize=ztd__yonl, meminfo=
            builder.load(yblwg__lvsih))
        arr.data = mnrp__iey._getvalue()
        wfqzx__pxanw = cgutils.pack_array(builder, [builder.load(sbtz__fle)
            ], ty=dsi__ndur)
        ztd__yonl = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(types.uint8)))
        cof__sxn = cgutils.pack_array(builder, [ztd__yonl], ty=dsi__ndur)
        data = builder.bitcast(builder.load(oruk__amoh), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(bujn__ylnsz, data=data, shape=
            wfqzx__pxanw, strides=cof__sxn, itemsize=ztd__yonl, meminfo=
            builder.load(appvf__csc))
        arr.null_bitmap = bujn__ylnsz._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        jthiz__jqxxq = context.make_array(arr_type.arr_type)(context, builder)
        gtrs__mbyu = context.make_array(arr_type.arr_type)(context, builder)
        dovfs__cink = cgutils.alloca_once(builder, lir.IntType(64))
        prrp__ppbok = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        hjama__ymlo = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        cujff__gad = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        wjnn__chrg = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        zea__zvu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='info_to_interval_array')
        builder.call(fnp__rau, [in_info, dovfs__cink, prrp__ppbok,
            hjama__ymlo, cujff__gad, wjnn__chrg])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        dsi__ndur = context.get_value_type(types.intp)
        wfqzx__pxanw = cgutils.pack_array(builder, [builder.load(
            dovfs__cink)], ty=dsi__ndur)
        ztd__yonl = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(arr_type.arr_type.dtype)))
        cof__sxn = cgutils.pack_array(builder, [ztd__yonl], ty=dsi__ndur)
        cxm__smi = builder.bitcast(builder.load(prrp__ppbok), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(jthiz__jqxxq, data=cxm__smi, shape
            =wfqzx__pxanw, strides=cof__sxn, itemsize=ztd__yonl, meminfo=
            builder.load(cujff__gad))
        arr.left = jthiz__jqxxq._getvalue()
        rubn__nqgt = builder.bitcast(builder.load(hjama__ymlo), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(gtrs__mbyu, data=rubn__nqgt, shape
            =wfqzx__pxanw, strides=cof__sxn, itemsize=ztd__yonl, meminfo=
            builder.load(wjnn__chrg))
        arr.right = gtrs__mbyu._getvalue()
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
        length, iai__ihm = args
        jcb__yqha = numba_to_c_type(array_type.dtype)
        irj__env = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), jcb__yqha))
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='alloc_numpy')
        return builder.call(fnp__rau, [length, builder.load(irj__env)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        length, jvddp__tbyb = args
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='alloc_string_array')
        return builder.call(fnp__rau, [length, jvddp__tbyb])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    qqlx__hhf, = args
    amr__mqno = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], qqlx__hhf)
    zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(8
        ).as_pointer().as_pointer(), lir.IntType(64)])
    fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
        name='arr_info_list_to_table')
    return builder.call(fnp__rau, [amr__mqno.data, amr__mqno.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='info_from_table')
        return builder.call(fnp__rau, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    ktnf__xmp = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        cpp_table, aug__hqkrn, iai__ihm = args
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='info_from_table')
        bqbnh__mqq = cgutils.create_struct_proxy(ktnf__xmp)(context, builder)
        bqbnh__mqq.parent = cgutils.get_null_value(bqbnh__mqq.parent.type)
        usyiy__ruqxb = context.make_array(table_idx_arr_t)(context, builder,
            aug__hqkrn)
        nbvxq__mjws = context.get_constant(types.int64, -1)
        wum__dvw = context.get_constant(types.int64, 0)
        rbrb__lvu = cgutils.alloca_once_value(builder, wum__dvw)
        for t, kbhdt__jvisr in ktnf__xmp.type_to_blk.items():
            baw__dlsp = context.get_constant(types.int64, len(ktnf__xmp.
                block_to_arr_ind[kbhdt__jvisr]))
            iai__ihm, vth__rcho = ListInstance.allocate_ex(context, builder,
                types.List(t), baw__dlsp)
            vth__rcho.size = baw__dlsp
            nsb__egc = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(ktnf__xmp.block_to_arr_ind[
                kbhdt__jvisr], dtype=np.int64))
            edxcz__povwa = context.make_array(types.Array(types.int64, 1, 'C')
                )(context, builder, nsb__egc)
            with cgutils.for_range(builder, baw__dlsp) as zpb__gju:
                sszns__uqeoj = zpb__gju.index
                ncej__jzipb = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    edxcz__povwa, sszns__uqeoj)
                nmlu__wnoqd = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, usyiy__ruqxb, ncej__jzipb)
                tyhf__dpo = builder.icmp_unsigned('!=', nmlu__wnoqd,
                    nbvxq__mjws)
                with builder.if_else(tyhf__dpo) as (kkyub__wbncm, ghd__qtg):
                    with kkyub__wbncm:
                        nqh__sbeb = builder.call(fnp__rau, [cpp_table,
                            nmlu__wnoqd])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            nqh__sbeb])
                        vth__rcho.inititem(sszns__uqeoj, arr, incref=False)
                        length = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(length, rbrb__lvu)
                    with ghd__qtg:
                        dnzm__klbdg = context.get_constant_null(t)
                        vth__rcho.inititem(sszns__uqeoj, dnzm__klbdg,
                            incref=False)
            setattr(bqbnh__mqq, f'block_{kbhdt__jvisr}', vth__rcho.value)
        bqbnh__mqq.len = builder.load(rbrb__lvu)
        return bqbnh__mqq._getvalue()
    return ktnf__xmp(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def cpp_table_to_py_data(cpp_table, out_col_inds_t, out_types_t, n_rows_t,
    n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
    bqim__gti = out_col_inds_t.instance_type.meta
    ktnf__xmp = unwrap_typeref(out_types_t.types[0])
    sdv__fmo = [unwrap_typeref(out_types_t.types[sszns__uqeoj]) for
        sszns__uqeoj in range(1, len(out_types_t.types))]
    gqudn__vrxp = {}
    ygmg__mhbv = get_overload_const_int(n_table_cols_t)
    qxmol__gqax = {bmz__luj: sszns__uqeoj for sszns__uqeoj, bmz__luj in
        enumerate(bqim__gti)}
    if not is_overload_none(unknown_cat_arrs_t):
        pxq__zao = {zotr__rqhf: sszns__uqeoj for sszns__uqeoj, zotr__rqhf in
            enumerate(cat_inds_t.instance_type.meta)}
    nscj__eng = []
    pgrf__xvmov = """def impl(cpp_table, out_col_inds_t, out_types_t, n_rows_t, n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
"""
    if isinstance(ktnf__xmp, bodo.TableType):
        pgrf__xvmov += f'  py_table = init_table(py_table_type, False)\n'
        pgrf__xvmov += f'  py_table = set_table_len(py_table, n_rows_t)\n'
        for gzueh__hzftv, kbhdt__jvisr in ktnf__xmp.type_to_blk.items():
            lpsnb__acix = [qxmol__gqax.get(sszns__uqeoj, -1) for
                sszns__uqeoj in ktnf__xmp.block_to_arr_ind[kbhdt__jvisr]]
            gqudn__vrxp[f'out_inds_{kbhdt__jvisr}'] = np.array(lpsnb__acix,
                np.int64)
            gqudn__vrxp[f'out_type_{kbhdt__jvisr}'] = gzueh__hzftv
            gqudn__vrxp[f'typ_list_{kbhdt__jvisr}'] = types.List(gzueh__hzftv)
            cpmj__szir = f'out_type_{kbhdt__jvisr}'
            if type_has_unknown_cats(gzueh__hzftv):
                if is_overload_none(unknown_cat_arrs_t):
                    pgrf__xvmov += f"""  in_arr_list_{kbhdt__jvisr} = get_table_block(out_types_t[0], {kbhdt__jvisr})
"""
                    cpmj__szir = f'in_arr_list_{kbhdt__jvisr}[i]'
                else:
                    gqudn__vrxp[f'cat_arr_inds_{kbhdt__jvisr}'] = np.array([
                        pxq__zao.get(sszns__uqeoj, -1) for sszns__uqeoj in
                        ktnf__xmp.block_to_arr_ind[kbhdt__jvisr]], np.int64)
                    cpmj__szir = (
                        f'unknown_cat_arrs_t[cat_arr_inds_{kbhdt__jvisr}[i]]')
            baw__dlsp = len(ktnf__xmp.block_to_arr_ind[kbhdt__jvisr])
            pgrf__xvmov += f"""  arr_list_{kbhdt__jvisr} = alloc_list_like(typ_list_{kbhdt__jvisr}, {baw__dlsp}, False)
"""
            pgrf__xvmov += f'  for i in range(len(arr_list_{kbhdt__jvisr})):\n'
            pgrf__xvmov += (
                f'    cpp_ind_{kbhdt__jvisr} = out_inds_{kbhdt__jvisr}[i]\n')
            pgrf__xvmov += f'    if cpp_ind_{kbhdt__jvisr} == -1:\n'
            pgrf__xvmov += f'      continue\n'
            pgrf__xvmov += f"""    arr_{kbhdt__jvisr} = info_to_array(info_from_table(cpp_table, cpp_ind_{kbhdt__jvisr}), {cpmj__szir})
"""
            pgrf__xvmov += (
                f'    arr_list_{kbhdt__jvisr}[i] = arr_{kbhdt__jvisr}\n')
            pgrf__xvmov += f"""  py_table = set_table_block(py_table, arr_list_{kbhdt__jvisr}, {kbhdt__jvisr})
"""
        nscj__eng.append('py_table')
    elif ktnf__xmp != types.none:
        frolx__bko = qxmol__gqax.get(0, -1)
        if frolx__bko != -1:
            gqudn__vrxp[f'arr_typ_arg0'] = ktnf__xmp
            cpmj__szir = f'arr_typ_arg0'
            if type_has_unknown_cats(ktnf__xmp):
                if is_overload_none(unknown_cat_arrs_t):
                    cpmj__szir = f'out_types_t[0]'
                else:
                    cpmj__szir = f'unknown_cat_arrs_t[{pxq__zao[0]}]'
            pgrf__xvmov += f"""  out_arg0 = info_to_array(info_from_table(cpp_table, {frolx__bko}), {cpmj__szir})
"""
            nscj__eng.append('out_arg0')
    for sszns__uqeoj, t in enumerate(sdv__fmo):
        frolx__bko = qxmol__gqax.get(ygmg__mhbv + sszns__uqeoj, -1)
        if frolx__bko != -1:
            gqudn__vrxp[f'extra_arr_type_{sszns__uqeoj}'] = t
            cpmj__szir = f'extra_arr_type_{sszns__uqeoj}'
            if type_has_unknown_cats(t):
                if is_overload_none(unknown_cat_arrs_t):
                    cpmj__szir = f'out_types_t[{sszns__uqeoj + 1}]'
                else:
                    cpmj__szir = (
                        f'unknown_cat_arrs_t[{pxq__zao[ygmg__mhbv + sszns__uqeoj]}]'
                        )
            pgrf__xvmov += f"""  out_{sszns__uqeoj} = info_to_array(info_from_table(cpp_table, {frolx__bko}), {cpmj__szir})
"""
            nscj__eng.append(f'out_{sszns__uqeoj}')
    jut__dpyal = ',' if len(nscj__eng) == 1 else ''
    pgrf__xvmov += f"  return ({', '.join(nscj__eng)}{jut__dpyal})\n"
    gqudn__vrxp.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'out_col_inds': list(bqim__gti), 'py_table_type': ktnf__xmp})
    ecb__ata = {}
    exec(pgrf__xvmov, gqudn__vrxp, ecb__ata)
    return ecb__ata['impl']


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    ktnf__xmp = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        py_table, iai__ihm = args
        awpp__oae = cgutils.create_struct_proxy(ktnf__xmp)(context, builder,
            py_table)
        if ktnf__xmp.has_runtime_cols:
            znb__bghf = lir.Constant(lir.IntType(64), 0)
            for kbhdt__jvisr, t in enumerate(ktnf__xmp.arr_types):
                nxygl__aeo = getattr(awpp__oae, f'block_{kbhdt__jvisr}')
                xiff__nwxya = ListInstance(context, builder, types.List(t),
                    nxygl__aeo)
                znb__bghf = builder.add(znb__bghf, xiff__nwxya.size)
        else:
            znb__bghf = lir.Constant(lir.IntType(64), len(ktnf__xmp.arr_types))
        iai__ihm, mqvp__zzd = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), znb__bghf)
        mqvp__zzd.size = znb__bghf
        if ktnf__xmp.has_runtime_cols:
            vjssg__zwwad = lir.Constant(lir.IntType(64), 0)
            for kbhdt__jvisr, t in enumerate(ktnf__xmp.arr_types):
                nxygl__aeo = getattr(awpp__oae, f'block_{kbhdt__jvisr}')
                xiff__nwxya = ListInstance(context, builder, types.List(t),
                    nxygl__aeo)
                baw__dlsp = xiff__nwxya.size
                with cgutils.for_range(builder, baw__dlsp) as zpb__gju:
                    sszns__uqeoj = zpb__gju.index
                    arr = xiff__nwxya.getitem(sszns__uqeoj)
                    khfx__gmu = signature(array_info_type, t)
                    csd__gjew = arr,
                    xuza__cchbq = array_to_info_codegen(context, builder,
                        khfx__gmu, csd__gjew)
                    mqvp__zzd.inititem(builder.add(vjssg__zwwad,
                        sszns__uqeoj), xuza__cchbq, incref=False)
                vjssg__zwwad = builder.add(vjssg__zwwad, baw__dlsp)
        else:
            for t, kbhdt__jvisr in ktnf__xmp.type_to_blk.items():
                baw__dlsp = context.get_constant(types.int64, len(ktnf__xmp
                    .block_to_arr_ind[kbhdt__jvisr]))
                nxygl__aeo = getattr(awpp__oae, f'block_{kbhdt__jvisr}')
                xiff__nwxya = ListInstance(context, builder, types.List(t),
                    nxygl__aeo)
                nsb__egc = context.make_constant_array(builder, types.Array
                    (types.int64, 1, 'C'), np.array(ktnf__xmp.
                    block_to_arr_ind[kbhdt__jvisr], dtype=np.int64))
                edxcz__povwa = context.make_array(types.Array(types.int64, 
                    1, 'C'))(context, builder, nsb__egc)
                with cgutils.for_range(builder, baw__dlsp) as zpb__gju:
                    sszns__uqeoj = zpb__gju.index
                    ncej__jzipb = _getitem_array_single_int(context,
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), edxcz__povwa, sszns__uqeoj)
                    mfznr__clzo = signature(types.none, ktnf__xmp, types.
                        List(t), types.int64, types.int64)
                    maus__csl = py_table, nxygl__aeo, sszns__uqeoj, ncej__jzipb
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, mfznr__clzo, maus__csl)
                    arr = xiff__nwxya.getitem(sszns__uqeoj)
                    khfx__gmu = signature(array_info_type, t)
                    csd__gjew = arr,
                    xuza__cchbq = array_to_info_codegen(context, builder,
                        khfx__gmu, csd__gjew)
                    mqvp__zzd.inititem(ncej__jzipb, xuza__cchbq, incref=False)
        rykh__xpws = mqvp__zzd.value
        jjzo__wopb = signature(table_type, types.List(array_info_type))
        qdk__hiq = rykh__xpws,
        cpp_table = arr_info_list_to_table_codegen(context, builder,
            jjzo__wopb, qdk__hiq)
        context.nrt.decref(builder, types.List(array_info_type), rykh__xpws)
        return cpp_table
    return table_type(ktnf__xmp, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def py_data_to_cpp_table(py_table, extra_arrs_tup, in_col_inds_t,
    n_table_cols_t):
    oinby__acz = in_col_inds_t.instance_type.meta
    gqudn__vrxp = {}
    ygmg__mhbv = get_overload_const_int(n_table_cols_t)
    zrl__rxqhb = defaultdict(list)
    qxmol__gqax = {}
    for sszns__uqeoj, bmz__luj in enumerate(oinby__acz):
        if bmz__luj in qxmol__gqax:
            zrl__rxqhb[bmz__luj].append(sszns__uqeoj)
        else:
            qxmol__gqax[bmz__luj] = sszns__uqeoj
    pgrf__xvmov = (
        'def impl(py_table, extra_arrs_tup, in_col_inds_t, n_table_cols_t):\n')
    pgrf__xvmov += (
        f'  cpp_arr_list = alloc_empty_list_type({len(oinby__acz)}, array_info_type)\n'
        )
    if py_table != types.none:
        for kbhdt__jvisr in py_table.type_to_blk.values():
            lpsnb__acix = [qxmol__gqax.get(sszns__uqeoj, -1) for
                sszns__uqeoj in py_table.block_to_arr_ind[kbhdt__jvisr]]
            gqudn__vrxp[f'out_inds_{kbhdt__jvisr}'] = np.array(lpsnb__acix,
                np.int64)
            gqudn__vrxp[f'arr_inds_{kbhdt__jvisr}'] = np.array(py_table.
                block_to_arr_ind[kbhdt__jvisr], np.int64)
            pgrf__xvmov += f"""  arr_list_{kbhdt__jvisr} = get_table_block(py_table, {kbhdt__jvisr})
"""
            pgrf__xvmov += f'  for i in range(len(arr_list_{kbhdt__jvisr})):\n'
            pgrf__xvmov += (
                f'    out_arr_ind_{kbhdt__jvisr} = out_inds_{kbhdt__jvisr}[i]\n'
                )
            pgrf__xvmov += f'    if out_arr_ind_{kbhdt__jvisr} == -1:\n'
            pgrf__xvmov += f'      continue\n'
            pgrf__xvmov += (
                f'    arr_ind_{kbhdt__jvisr} = arr_inds_{kbhdt__jvisr}[i]\n')
            pgrf__xvmov += f"""    ensure_column_unboxed(py_table, arr_list_{kbhdt__jvisr}, i, arr_ind_{kbhdt__jvisr})
"""
            pgrf__xvmov += f"""    cpp_arr_list[out_arr_ind_{kbhdt__jvisr}] = array_to_info(arr_list_{kbhdt__jvisr}[i])
"""
        for ajl__vmr, vhot__our in zrl__rxqhb.items():
            if ajl__vmr < ygmg__mhbv:
                kbhdt__jvisr = py_table.block_nums[ajl__vmr]
                yjm__hon = py_table.block_offsets[ajl__vmr]
                for frolx__bko in vhot__our:
                    pgrf__xvmov += f"""  cpp_arr_list[{frolx__bko}] = array_to_info(arr_list_{kbhdt__jvisr}[{yjm__hon}])
"""
    for sszns__uqeoj in range(len(extra_arrs_tup)):
        lccq__wlkd = qxmol__gqax.get(ygmg__mhbv + sszns__uqeoj, -1)
        if lccq__wlkd != -1:
            lda__opgba = [lccq__wlkd] + zrl__rxqhb.get(ygmg__mhbv +
                sszns__uqeoj, [])
            for frolx__bko in lda__opgba:
                pgrf__xvmov += f"""  cpp_arr_list[{frolx__bko}] = array_to_info(extra_arrs_tup[{sszns__uqeoj}])
"""
    pgrf__xvmov += f'  return arr_info_list_to_table(cpp_arr_list)\n'
    gqudn__vrxp.update({'array_info_type': array_info_type,
        'alloc_empty_list_type': bodo.hiframes.table.alloc_empty_list_type,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'ensure_column_unboxed': bodo.hiframes.table.ensure_column_unboxed,
        'array_to_info': array_to_info, 'arr_info_list_to_table':
        arr_info_list_to_table})
    ecb__ata = {}
    exec(pgrf__xvmov, gqudn__vrxp, ecb__ata)
    return ecb__ata['impl']


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
        zea__zvu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='delete_table')
        builder.call(fnp__rau, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='shuffle_table')
        zqjhu__fvjrz = builder.call(fnp__rau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return zqjhu__fvjrz
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
        zea__zvu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='delete_shuffle_info')
        return builder.call(fnp__rau, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='reverse_shuffle_table')
        return builder.call(fnp__rau, args)
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
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(64), lir.IntType(8).as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='hash_join_table')
        zqjhu__fvjrz = builder.call(fnp__rau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return zqjhu__fvjrz
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
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64), lir.
            IntType(8).as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='cross_join_table')
        zqjhu__fvjrz = builder.call(fnp__rau, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return zqjhu__fvjrz
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.boolean, types.boolean, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.int64, types.voidptr, types.
        int64, types.voidptr), codegen


@intrinsic
def sort_values_table(typingctx, table_t, n_keys_t, vect_ascending_t,
    na_position_b_t, dead_keys_t, n_rows_t, bounds_t, parallel_t):
    assert table_t == table_type, 'C++ table type expected'

    def codegen(context, builder, sig, args):
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1)])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='sort_values_table')
        zqjhu__fvjrz = builder.call(fnp__rau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return zqjhu__fvjrz
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='sample_table')
        zqjhu__fvjrz = builder.call(fnp__rau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return zqjhu__fvjrz
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='shuffle_renormalization')
        zqjhu__fvjrz = builder.call(fnp__rau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return zqjhu__fvjrz
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='shuffle_renormalization_group')
        zqjhu__fvjrz = builder.call(fnp__rau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return zqjhu__fvjrz
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='drop_duplicates_table')
        zqjhu__fvjrz = builder.call(fnp__rau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return zqjhu__fvjrz
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
        zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        fnp__rau = cgutils.get_or_insert_function(builder.module, zea__zvu,
            name='groupby_and_aggregate')
        zqjhu__fvjrz = builder.call(fnp__rau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return zqjhu__fvjrz
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
    tuder__gnzm = array_to_info(dict_arr)
    _drop_duplicates_local_dictionary(tuder__gnzm, sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(tuder__gnzm, bodo.dict_str_arr_type)
    return out_arr


_convert_local_dictionary_to_global = types.ExternalFunction(
    'convert_local_dictionary_to_global', types.void(array_info_type, types
    .bool_, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def convert_local_dictionary_to_global(dict_arr, sort_dictionary,
    is_parallel=False):
    tuder__gnzm = array_to_info(dict_arr)
    _convert_local_dictionary_to_global(tuder__gnzm, is_parallel,
        sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(tuder__gnzm, bodo.dict_str_arr_type)
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
    uqfu__vcn = array_to_info(in_arr)
    bxy__ttgk = array_to_info(in_values)
    qhlu__ezee = array_to_info(out_arr)
    uaarp__uus = arr_info_list_to_table([uqfu__vcn, bxy__ttgk, qhlu__ezee])
    _array_isin(qhlu__ezee, uqfu__vcn, bxy__ttgk, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(uaarp__uus)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, match, pat, out_arr):
    uqfu__vcn = array_to_info(in_arr)
    qhlu__ezee = array_to_info(out_arr)
    _get_search_regex(uqfu__vcn, case, match, pat, qhlu__ezee)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    naz__mljtz = col_array_typ.dtype
    if isinstance(naz__mljtz, (types.Number, TimeType, bodo.libs.
        pd_datetime_arr_ext.PandasDatetimeTZDtype)) or naz__mljtz in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:
        if isinstance(naz__mljtz, bodo.libs.pd_datetime_arr_ext.
            PandasDatetimeTZDtype):
            naz__mljtz = bodo.datetime64ns

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                bqbnh__mqq, hpps__apk = args
                bqbnh__mqq = builder.bitcast(bqbnh__mqq, lir.IntType(8).
                    as_pointer().as_pointer())
                aer__kzkjo = lir.Constant(lir.IntType(64), c_ind)
                xrl__vko = builder.load(builder.gep(bqbnh__mqq, [aer__kzkjo]))
                xrl__vko = builder.bitcast(xrl__vko, context.get_data_type(
                    naz__mljtz).as_pointer())
                return context.unpack_value(builder, naz__mljtz, builder.
                    gep(xrl__vko, [hpps__apk]))
            return naz__mljtz(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ in (bodo.string_array_type, bodo.binary_array_type):

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                bqbnh__mqq, hpps__apk = args
                bqbnh__mqq = builder.bitcast(bqbnh__mqq, lir.IntType(8).
                    as_pointer().as_pointer())
                aer__kzkjo = lir.Constant(lir.IntType(64), c_ind)
                xrl__vko = builder.load(builder.gep(bqbnh__mqq, [aer__kzkjo]))
                zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                vrt__sdl = cgutils.get_or_insert_function(builder.module,
                    zea__zvu, name='array_info_getitem')
                ttlia__mjrh = cgutils.alloca_once(builder, lir.IntType(64))
                args = xrl__vko, hpps__apk, ttlia__mjrh
                xoqa__ibs = builder.call(vrt__sdl, args)
                wzcww__vxb = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    wzcww__vxb, [xoqa__ibs, builder.load(ttlia__mjrh)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                jexq__ebau = lir.Constant(lir.IntType(64), 1)
                xwk__uiho = lir.Constant(lir.IntType(64), 2)
                bqbnh__mqq, hpps__apk = args
                bqbnh__mqq = builder.bitcast(bqbnh__mqq, lir.IntType(8).
                    as_pointer().as_pointer())
                aer__kzkjo = lir.Constant(lir.IntType(64), c_ind)
                xrl__vko = builder.load(builder.gep(bqbnh__mqq, [aer__kzkjo]))
                zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64)])
                jzia__wdskh = cgutils.get_or_insert_function(builder.module,
                    zea__zvu, name='get_nested_info')
                args = xrl__vko, xwk__uiho
                nuvf__rdx = builder.call(jzia__wdskh, args)
                zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer()])
                zki__gjvmd = cgutils.get_or_insert_function(builder.module,
                    zea__zvu, name='array_info_getdata1')
                args = nuvf__rdx,
                evsz__fik = builder.call(zki__gjvmd, args)
                evsz__fik = builder.bitcast(evsz__fik, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                cxxs__mpi = builder.sext(builder.load(builder.gep(evsz__fik,
                    [hpps__apk])), lir.IntType(64))
                args = xrl__vko, jexq__ebau
                jbf__csxxa = builder.call(jzia__wdskh, args)
                zea__zvu = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                vrt__sdl = cgutils.get_or_insert_function(builder.module,
                    zea__zvu, name='array_info_getitem')
                ttlia__mjrh = cgutils.alloca_once(builder, lir.IntType(64))
                args = jbf__csxxa, cxxs__mpi, ttlia__mjrh
                xoqa__ibs = builder.call(vrt__sdl, args)
                wzcww__vxb = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    wzcww__vxb, [xoqa__ibs, builder.load(ttlia__mjrh)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{naz__mljtz}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if isinstance(col_array_dtype, (IntegerArrayType, FloatingArrayType,
        bodo.TimeArrayType)) or col_array_dtype in (bodo.libs.bool_arr_ext.
        boolean_array, bodo.binary_array_type, bodo.datetime_date_array_type
        ) or is_str_arr_type(col_array_dtype):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                sgu__jsn, hpps__apk = args
                sgu__jsn = builder.bitcast(sgu__jsn, lir.IntType(8).
                    as_pointer().as_pointer())
                aer__kzkjo = lir.Constant(lir.IntType(64), c_ind)
                xrl__vko = builder.load(builder.gep(sgu__jsn, [aer__kzkjo]))
                qqtj__zfref = builder.bitcast(xrl__vko, context.
                    get_data_type(types.bool_).as_pointer())
                gyu__dqefi = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    qqtj__zfref, hpps__apk)
                voo__xvd = builder.icmp_unsigned('!=', gyu__dqefi, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(voo__xvd, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, (types.Array, bodo.DatetimeArrayType)):
        naz__mljtz = col_array_dtype.dtype
        if naz__mljtz in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            naz__mljtz, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype):
            if isinstance(naz__mljtz, bodo.libs.pd_datetime_arr_ext.
                PandasDatetimeTZDtype):
                naz__mljtz = bodo.datetime64ns

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    bqbnh__mqq, hpps__apk = args
                    bqbnh__mqq = builder.bitcast(bqbnh__mqq, lir.IntType(8)
                        .as_pointer().as_pointer())
                    aer__kzkjo = lir.Constant(lir.IntType(64), c_ind)
                    xrl__vko = builder.load(builder.gep(bqbnh__mqq, [
                        aer__kzkjo]))
                    xrl__vko = builder.bitcast(xrl__vko, context.
                        get_data_type(naz__mljtz).as_pointer())
                    bkg__glbm = builder.load(builder.gep(xrl__vko, [hpps__apk])
                        )
                    voo__xvd = builder.icmp_unsigned('!=', bkg__glbm, lir.
                        Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(voo__xvd, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(naz__mljtz, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    bqbnh__mqq, hpps__apk = args
                    bqbnh__mqq = builder.bitcast(bqbnh__mqq, lir.IntType(8)
                        .as_pointer().as_pointer())
                    aer__kzkjo = lir.Constant(lir.IntType(64), c_ind)
                    xrl__vko = builder.load(builder.gep(bqbnh__mqq, [
                        aer__kzkjo]))
                    xrl__vko = builder.bitcast(xrl__vko, context.
                        get_data_type(naz__mljtz).as_pointer())
                    bkg__glbm = builder.load(builder.gep(xrl__vko, [hpps__apk])
                        )
                    iyorj__cecq = signature(types.bool_, naz__mljtz)
                    gyu__dqefi = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, iyorj__cecq, (bkg__glbm,))
                    return builder.not_(builder.sext(gyu__dqefi, lir.
                        IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
