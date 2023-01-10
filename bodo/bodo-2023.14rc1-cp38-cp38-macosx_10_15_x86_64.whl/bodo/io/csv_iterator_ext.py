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
        crtkl__ucobi = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(crtkl__ucobi)
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
        blxy__uosj = [('csv_reader', types.stream_reader_type), ('index',
            types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, blxy__uosj)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    jcni__jsev = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    sdh__bprp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()])
    htm__jburv = cgutils.get_or_insert_function(builder.module, sdh__bprp,
        name='initialize_csv_reader')
    ttr__cpspb = cgutils.create_struct_proxy(types.stream_reader_type)(context,
        builder, value=jcni__jsev.csv_reader)
    builder.call(htm__jburv, [ttr__cpspb.pyobj])
    builder.store(context.get_constant(types.uint64, 0), jcni__jsev.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [cvk__coth] = sig.args
    [bstti__kdm] = args
    jcni__jsev = cgutils.create_struct_proxy(cvk__coth)(context, builder,
        value=bstti__kdm)
    sdh__bprp = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()])
    htm__jburv = cgutils.get_or_insert_function(builder.module, sdh__bprp,
        name='update_csv_reader')
    ttr__cpspb = cgutils.create_struct_proxy(types.stream_reader_type)(context,
        builder, value=jcni__jsev.csv_reader)
    tha__vfg = builder.call(htm__jburv, [ttr__cpspb.pyobj])
    result.set_valid(tha__vfg)
    with builder.if_then(tha__vfg):
        fmgf__esuxb = builder.load(jcni__jsev.index)
        lpzmy__ltpkc = types.Tuple([sig.return_type.first_type, types.int64])
        elwqz__bsis = gen_read_csv_objmode(sig.args[0])
        nhg__mmbr = signature(lpzmy__ltpkc, types.stream_reader_type, types
            .int64)
        dvnso__hird = context.compile_internal(builder, elwqz__bsis,
            nhg__mmbr, [jcni__jsev.csv_reader, fmgf__esuxb])
        zzrpi__ougf, jyuo__ekb = cgutils.unpack_tuple(builder, dvnso__hird)
        fgc__kqg = builder.add(fmgf__esuxb, jyuo__ekb, flags=['nsw'])
        builder.store(fgc__kqg, jcni__jsev.index)
        result.yield_(zzrpi__ougf)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        opv__dtu = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        context.nrt.incref(builder, signature.args[0], args[0])
        opv__dtu.csv_reader = args[0]
        ajs__kuma = context.get_constant(types.uintp, 0)
        opv__dtu.index = cgutils.alloca_once_value(builder, ajs__kuma)
        return opv__dtu._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    tcl__wohz = csv_iterator_typeref.instance_type
    sig = signature(tcl__wohz, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    hcj__hrnhf = 'def read_csv_objmode(f_reader):\n'
    rrp__qfwdv = [sanitize_varname(sor__xzyaa) for sor__xzyaa in
        csv_iterator_type._out_colnames]
    pro__xord = ir_utils.next_label()
    eni__knzei = globals()
    out_types = csv_iterator_type._out_types
    eni__knzei[f'table_type_{pro__xord}'] = TableType(tuple(out_types))
    eni__knzei[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    hzcjg__xsr = list(range(len(csv_iterator_type._usecols)))
    hcj__hrnhf += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        rrp__qfwdv, out_types, csv_iterator_type._usecols, hzcjg__xsr,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, pro__xord, eni__knzei, parallel
        =False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    qulp__rirqa = bodo.ir.csv_ext._gen_parallel_flag_name(rrp__qfwdv)
    vqe__gja = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [qulp__rirqa]
    hcj__hrnhf += f"  return {', '.join(vqe__gja)}"
    eni__knzei = globals()
    qau__earhu = {}
    exec(hcj__hrnhf, eni__knzei, qau__earhu)
    fta__deb = qau__earhu['read_csv_objmode']
    ikq__dzmv = numba.njit(fta__deb)
    bodo.ir.csv_ext.compiled_funcs.append(ikq__dzmv)
    rxl__fvudu = 'def read_func(reader, local_start):\n'
    rxl__fvudu += f"  {', '.join(vqe__gja)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        rxl__fvudu += f'  local_len = len(T)\n'
        rxl__fvudu += '  total_size = local_len\n'
        rxl__fvudu += f'  if ({qulp__rirqa}):\n'
        rxl__fvudu += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        rxl__fvudu += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        sxf__jkb = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        rxl__fvudu += '  total_size = 0\n'
        sxf__jkb = (
            f'bodo.utils.conversion.convert_to_index({vqe__gja[1]}, {csv_iterator_type._index_name!r})'
            )
    rxl__fvudu += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({vqe__gja[0]},), {sxf__jkb}, __col_name_meta_value_read_csv_objmode), total_size)
"""
    exec(rxl__fvudu, {'bodo': bodo, 'objmode_func': ikq__dzmv, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        '__col_name_meta_value_read_csv_objmode': ColNamesMetaType(
        csv_iterator_type.yield_type.columns)}, qau__earhu)
    return qau__earhu['read_func']
