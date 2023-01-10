"""
Class information for DataFrame iterators returned by pd.read_csv. This is used
to handle situations in which pd.read_csv is used to return chunks with separate
read calls instead of just a single read.
"""
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir_utils, types
from numba.core.imputils import RefType, impl_ret_borrowed, iternext_impl
from numba.core.typing.templates import signature
from numba.extending import intrinsic, lower_builtin, models, register_model
import bodo
import bodo.ir.connector
import bodo.ir.csv_ext
from bodo import objmode
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.table import Table, TableType
from bodo.io import csv_cpp
from bodo.ir.csv_ext import _gen_read_csv_objmode, astype
from bodo.utils.typing import ColNamesMetaType
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname
ll.add_symbol('update_csv_reader', csv_cpp.update_csv_reader)
ll.add_symbol('initialize_csv_reader', csv_cpp.initialize_csv_reader)


class CSVIteratorType(types.SimpleIteratorType):

    def __init__(self, df_type, out_colnames, out_types, usecols, sep,
        index_ind, index_arr_typ, index_name, escapechar, storage_options):
        assert isinstance(df_type, DataFrameType
            ), 'CSVIterator must return a DataFrame'
        klm__mtplh = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(klm__mtplh)
        self._yield_type = df_type
        self._out_colnames = out_colnames
        self._out_types = out_types
        self._usecols = usecols
        self._sep = sep
        self._index_ind = index_ind
        self._index_arr_typ = index_arr_typ
        self._index_name = index_name
        self._escapechar = escapechar
        self._storage_options = storage_options

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(CSVIteratorType)
class CSVIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wfq__qriwo = [('csv_reader', types.stream_reader_type), ('index',
            types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, wfq__qriwo)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    dmu__srch = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    aytif__rgco = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer()])
    madvi__tkx = cgutils.get_or_insert_function(builder.module, aytif__rgco,
        name='initialize_csv_reader')
    eotc__tyzv = cgutils.create_struct_proxy(types.stream_reader_type)(context,
        builder, value=dmu__srch.csv_reader)
    builder.call(madvi__tkx, [eotc__tyzv.pyobj])
    builder.store(context.get_constant(types.uint64, 0), dmu__srch.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [gis__hyp] = sig.args
    [fhbb__ilrq] = args
    dmu__srch = cgutils.create_struct_proxy(gis__hyp)(context, builder,
        value=fhbb__ilrq)
    aytif__rgco = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer()])
    madvi__tkx = cgutils.get_or_insert_function(builder.module, aytif__rgco,
        name='update_csv_reader')
    eotc__tyzv = cgutils.create_struct_proxy(types.stream_reader_type)(context,
        builder, value=dmu__srch.csv_reader)
    hwjd__mah = builder.call(madvi__tkx, [eotc__tyzv.pyobj])
    result.set_valid(hwjd__mah)
    with builder.if_then(hwjd__mah):
        yzkh__taves = builder.load(dmu__srch.index)
        wqhc__tnuo = types.Tuple([sig.return_type.first_type, types.int64])
        jmnk__urv = gen_read_csv_objmode(sig.args[0])
        qmlwa__ypbj = signature(wqhc__tnuo, types.stream_reader_type, types
            .int64)
        kis__rbzv = context.compile_internal(builder, jmnk__urv,
            qmlwa__ypbj, [dmu__srch.csv_reader, yzkh__taves])
        pfsin__qbb, kbpkb__pny = cgutils.unpack_tuple(builder, kis__rbzv)
        ltb__jpt = builder.add(yzkh__taves, kbpkb__pny, flags=['nsw'])
        builder.store(ltb__jpt, dmu__srch.index)
        result.yield_(pfsin__qbb)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        ooyr__kna = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        context.nrt.incref(builder, signature.args[0], args[0])
        ooyr__kna.csv_reader = args[0]
        bdno__mra = context.get_constant(types.uintp, 0)
        ooyr__kna.index = cgutils.alloca_once_value(builder, bdno__mra)
        return ooyr__kna._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    uhif__vraim = csv_iterator_typeref.instance_type
    sig = signature(uhif__vraim, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    rynl__ovkl = 'def read_csv_objmode(f_reader):\n'
    ljslz__zbe = [sanitize_varname(xefn__bcii) for xefn__bcii in
        csv_iterator_type._out_colnames]
    ggwa__tuh = ir_utils.next_label()
    cro__wqui = globals()
    out_types = csv_iterator_type._out_types
    cro__wqui[f'table_type_{ggwa__tuh}'] = TableType(tuple(out_types))
    cro__wqui[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    zwe__hmtf = list(range(len(csv_iterator_type._usecols)))
    rynl__ovkl += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        ljslz__zbe, out_types, csv_iterator_type._usecols, zwe__hmtf,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, ggwa__tuh, cro__wqui, parallel=
        False, check_parallel_runtime=True, idx_col_index=csv_iterator_type
        ._index_ind, idx_col_typ=csv_iterator_type._index_arr_typ)
    cyko__nqxx = bodo.ir.csv_ext._gen_parallel_flag_name(ljslz__zbe)
    qbj__urif = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [cyko__nqxx]
    rynl__ovkl += f"  return {', '.join(qbj__urif)}"
    cro__wqui = globals()
    cvkir__ulez = {}
    exec(rynl__ovkl, cro__wqui, cvkir__ulez)
    bssuq__xgz = cvkir__ulez['read_csv_objmode']
    dkrz__eyfw = numba.njit(bssuq__xgz)
    bodo.ir.csv_ext.compiled_funcs.append(dkrz__eyfw)
    redax__cyz = 'def read_func(reader, local_start):\n'
    redax__cyz += f"  {', '.join(qbj__urif)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        redax__cyz += f'  local_len = len(T)\n'
        redax__cyz += '  total_size = local_len\n'
        redax__cyz += f'  if ({cyko__nqxx}):\n'
        redax__cyz += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        redax__cyz += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        dfy__mjums = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        redax__cyz += '  total_size = 0\n'
        dfy__mjums = (
            f'bodo.utils.conversion.convert_to_index({qbj__urif[1]}, {csv_iterator_type._index_name!r})'
            )
    redax__cyz += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({qbj__urif[0]},), {dfy__mjums}, __col_name_meta_value_read_csv_objmode), total_size)
"""
    exec(redax__cyz, {'bodo': bodo, 'objmode_func': dkrz__eyfw, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        '__col_name_meta_value_read_csv_objmode': ColNamesMetaType(
        csv_iterator_type.yield_type.columns)}, cvkir__ulez)
    return cvkir__ulez['read_func']
