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
        bahcd__wrzz = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(bahcd__wrzz)
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
        yxywo__mtqs = [('csv_reader', types.stream_reader_type), ('index',
            types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, yxywo__mtqs)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    uyq__whc = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    isw__qua = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()])
    bhx__eej = cgutils.get_or_insert_function(builder.module, isw__qua,
        name='initialize_csv_reader')
    djun__sor = cgutils.create_struct_proxy(types.stream_reader_type)(context,
        builder, value=uyq__whc.csv_reader)
    builder.call(bhx__eej, [djun__sor.pyobj])
    builder.store(context.get_constant(types.uint64, 0), uyq__whc.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [xgd__aag] = sig.args
    [ayuiq__byati] = args
    uyq__whc = cgutils.create_struct_proxy(xgd__aag)(context, builder,
        value=ayuiq__byati)
    isw__qua = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()])
    bhx__eej = cgutils.get_or_insert_function(builder.module, isw__qua,
        name='update_csv_reader')
    djun__sor = cgutils.create_struct_proxy(types.stream_reader_type)(context,
        builder, value=uyq__whc.csv_reader)
    chyk__sjy = builder.call(bhx__eej, [djun__sor.pyobj])
    result.set_valid(chyk__sjy)
    with builder.if_then(chyk__sjy):
        ozzyv__baeed = builder.load(uyq__whc.index)
        ujxc__rqtvz = types.Tuple([sig.return_type.first_type, types.int64])
        ckfla__pslg = gen_read_csv_objmode(sig.args[0])
        ybew__rnoh = signature(ujxc__rqtvz, types.stream_reader_type, types
            .int64)
        kky__hskz = context.compile_internal(builder, ckfla__pslg,
            ybew__rnoh, [uyq__whc.csv_reader, ozzyv__baeed])
        oydg__wrys, fngsr__fgqf = cgutils.unpack_tuple(builder, kky__hskz)
        zeu__gqg = builder.add(ozzyv__baeed, fngsr__fgqf, flags=['nsw'])
        builder.store(zeu__gqg, uyq__whc.index)
        result.yield_(oydg__wrys)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        mms__lhj = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        context.nrt.incref(builder, signature.args[0], args[0])
        mms__lhj.csv_reader = args[0]
        gypsy__hyjc = context.get_constant(types.uintp, 0)
        mms__lhj.index = cgutils.alloca_once_value(builder, gypsy__hyjc)
        return mms__lhj._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    znfb__aqcs = csv_iterator_typeref.instance_type
    sig = signature(znfb__aqcs, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    hub__fxntv = 'def read_csv_objmode(f_reader):\n'
    mdpl__iecg = [sanitize_varname(tjv__fkdg) for tjv__fkdg in
        csv_iterator_type._out_colnames]
    dnd__pdzv = ir_utils.next_label()
    vpah__osafp = globals()
    out_types = csv_iterator_type._out_types
    vpah__osafp[f'table_type_{dnd__pdzv}'] = TableType(tuple(out_types))
    vpah__osafp[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    flcqb__wfyd = list(range(len(csv_iterator_type._usecols)))
    hub__fxntv += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        mdpl__iecg, out_types, csv_iterator_type._usecols, flcqb__wfyd,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, dnd__pdzv, vpah__osafp,
        parallel=False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    eipz__eioj = bodo.ir.csv_ext._gen_parallel_flag_name(mdpl__iecg)
    ojxn__glrwa = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [eipz__eioj]
    hub__fxntv += f"  return {', '.join(ojxn__glrwa)}"
    vpah__osafp = globals()
    kfr__qugr = {}
    exec(hub__fxntv, vpah__osafp, kfr__qugr)
    ubj__afl = kfr__qugr['read_csv_objmode']
    yfd__gadvp = numba.njit(ubj__afl)
    bodo.ir.csv_ext.compiled_funcs.append(yfd__gadvp)
    njq__joqb = 'def read_func(reader, local_start):\n'
    njq__joqb += f"  {', '.join(ojxn__glrwa)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        njq__joqb += f'  local_len = len(T)\n'
        njq__joqb += '  total_size = local_len\n'
        njq__joqb += f'  if ({eipz__eioj}):\n'
        njq__joqb += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        njq__joqb += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        rjm__rks = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        njq__joqb += '  total_size = 0\n'
        rjm__rks = (
            f'bodo.utils.conversion.convert_to_index({ojxn__glrwa[1]}, {csv_iterator_type._index_name!r})'
            )
    njq__joqb += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({ojxn__glrwa[0]},), {rjm__rks}, __col_name_meta_value_read_csv_objmode), total_size)
"""
    exec(njq__joqb, {'bodo': bodo, 'objmode_func': yfd__gadvp, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        '__col_name_meta_value_read_csv_objmode': ColNamesMetaType(
        csv_iterator_type.yield_type.columns)}, kfr__qugr)
    return kfr__qugr['read_func']
