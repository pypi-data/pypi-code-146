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
        wflhs__ilmvw = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(wflhs__ilmvw)
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
        kdzc__tlx = [('csv_reader', types.stream_reader_type), ('index',
            types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, kdzc__tlx)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    ttt__tcrj = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    ncztc__qggfc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer()])
    cbft__jcv = cgutils.get_or_insert_function(builder.module, ncztc__qggfc,
        name='initialize_csv_reader')
    gsr__hobd = cgutils.create_struct_proxy(types.stream_reader_type)(context,
        builder, value=ttt__tcrj.csv_reader)
    builder.call(cbft__jcv, [gsr__hobd.pyobj])
    builder.store(context.get_constant(types.uint64, 0), ttt__tcrj.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [efo__bbdk] = sig.args
    [gkq__ndc] = args
    ttt__tcrj = cgutils.create_struct_proxy(efo__bbdk)(context, builder,
        value=gkq__ndc)
    ncztc__qggfc = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer()])
    cbft__jcv = cgutils.get_or_insert_function(builder.module, ncztc__qggfc,
        name='update_csv_reader')
    gsr__hobd = cgutils.create_struct_proxy(types.stream_reader_type)(context,
        builder, value=ttt__tcrj.csv_reader)
    kkko__xziyf = builder.call(cbft__jcv, [gsr__hobd.pyobj])
    result.set_valid(kkko__xziyf)
    with builder.if_then(kkko__xziyf):
        ydil__mzw = builder.load(ttt__tcrj.index)
        wgttq__tnnyq = types.Tuple([sig.return_type.first_type, types.int64])
        irtx__qqfwi = gen_read_csv_objmode(sig.args[0])
        yebj__vskk = signature(wgttq__tnnyq, types.stream_reader_type,
            types.int64)
        kzjg__cyhmd = context.compile_internal(builder, irtx__qqfwi,
            yebj__vskk, [ttt__tcrj.csv_reader, ydil__mzw])
        wjua__alr, usdn__zbzs = cgutils.unpack_tuple(builder, kzjg__cyhmd)
        zzrq__xezhd = builder.add(ydil__mzw, usdn__zbzs, flags=['nsw'])
        builder.store(zzrq__xezhd, ttt__tcrj.index)
        result.yield_(wjua__alr)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        dpx__atca = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        context.nrt.incref(builder, signature.args[0], args[0])
        dpx__atca.csv_reader = args[0]
        smqk__iojw = context.get_constant(types.uintp, 0)
        dpx__atca.index = cgutils.alloca_once_value(builder, smqk__iojw)
        return dpx__atca._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    ztcm__jvd = csv_iterator_typeref.instance_type
    sig = signature(ztcm__jvd, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    drjy__brq = 'def read_csv_objmode(f_reader):\n'
    uaya__vqj = [sanitize_varname(uul__vwr) for uul__vwr in
        csv_iterator_type._out_colnames]
    hrcr__sdcc = ir_utils.next_label()
    tjkbv__eucn = globals()
    out_types = csv_iterator_type._out_types
    tjkbv__eucn[f'table_type_{hrcr__sdcc}'] = TableType(tuple(out_types))
    tjkbv__eucn[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    apok__rxu = list(range(len(csv_iterator_type._usecols)))
    drjy__brq += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        uaya__vqj, out_types, csv_iterator_type._usecols, apok__rxu,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, hrcr__sdcc, tjkbv__eucn,
        parallel=False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    otxh__meksh = bodo.ir.csv_ext._gen_parallel_flag_name(uaya__vqj)
    rbjij__gnd = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [otxh__meksh]
    drjy__brq += f"  return {', '.join(rbjij__gnd)}"
    tjkbv__eucn = globals()
    vpm__tai = {}
    exec(drjy__brq, tjkbv__eucn, vpm__tai)
    lznm__obt = vpm__tai['read_csv_objmode']
    qkrew__jky = numba.njit(lznm__obt)
    bodo.ir.csv_ext.compiled_funcs.append(qkrew__jky)
    cczrt__nvgt = 'def read_func(reader, local_start):\n'
    cczrt__nvgt += f"  {', '.join(rbjij__gnd)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        cczrt__nvgt += f'  local_len = len(T)\n'
        cczrt__nvgt += '  total_size = local_len\n'
        cczrt__nvgt += f'  if ({otxh__meksh}):\n'
        cczrt__nvgt += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        cczrt__nvgt += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        tmxye__pfgp = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        cczrt__nvgt += '  total_size = 0\n'
        tmxye__pfgp = (
            f'bodo.utils.conversion.convert_to_index({rbjij__gnd[1]}, {csv_iterator_type._index_name!r})'
            )
    cczrt__nvgt += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({rbjij__gnd[0]},), {tmxye__pfgp}, __col_name_meta_value_read_csv_objmode), total_size)
"""
    exec(cczrt__nvgt, {'bodo': bodo, 'objmode_func': qkrew__jky, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        '__col_name_meta_value_read_csv_objmode': ColNamesMetaType(
        csv_iterator_type.yield_type.columns)}, vpm__tai)
    return vpm__tai['read_func']
