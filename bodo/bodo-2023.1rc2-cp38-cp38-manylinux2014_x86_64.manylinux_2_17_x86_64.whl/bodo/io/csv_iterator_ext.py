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
        gcjwb__gqft = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(gcjwb__gqft)
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
        sgbs__vxsk = [('csv_reader', types.stream_reader_type), ('index',
            types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, sgbs__vxsk)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    sgu__ldub = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    qdzh__rnlm = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()]
        )
    ibk__pjkk = cgutils.get_or_insert_function(builder.module, qdzh__rnlm,
        name='initialize_csv_reader')
    ejzzi__aewec = cgutils.create_struct_proxy(types.stream_reader_type)(
        context, builder, value=sgu__ldub.csv_reader)
    builder.call(ibk__pjkk, [ejzzi__aewec.pyobj])
    builder.store(context.get_constant(types.uint64, 0), sgu__ldub.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [zfsb__grkd] = sig.args
    [fiq__oaq] = args
    sgu__ldub = cgutils.create_struct_proxy(zfsb__grkd)(context, builder,
        value=fiq__oaq)
    qdzh__rnlm = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()]
        )
    ibk__pjkk = cgutils.get_or_insert_function(builder.module, qdzh__rnlm,
        name='update_csv_reader')
    ejzzi__aewec = cgutils.create_struct_proxy(types.stream_reader_type)(
        context, builder, value=sgu__ldub.csv_reader)
    wdthz__ehs = builder.call(ibk__pjkk, [ejzzi__aewec.pyobj])
    result.set_valid(wdthz__ehs)
    with builder.if_then(wdthz__ehs):
        dybo__ilwzh = builder.load(sgu__ldub.index)
        qovbk__cppaz = types.Tuple([sig.return_type.first_type, types.int64])
        pprma__rlf = gen_read_csv_objmode(sig.args[0])
        whbps__smn = signature(qovbk__cppaz, types.stream_reader_type,
            types.int64)
        xmjjy__boons = context.compile_internal(builder, pprma__rlf,
            whbps__smn, [sgu__ldub.csv_reader, dybo__ilwzh])
        ssn__uazzk, yefjw__hval = cgutils.unpack_tuple(builder, xmjjy__boons)
        lkwpl__itska = builder.add(dybo__ilwzh, yefjw__hval, flags=['nsw'])
        builder.store(lkwpl__itska, sgu__ldub.index)
        result.yield_(ssn__uazzk)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        eiw__skqa = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        context.nrt.incref(builder, signature.args[0], args[0])
        eiw__skqa.csv_reader = args[0]
        awc__hunnl = context.get_constant(types.uintp, 0)
        eiw__skqa.index = cgutils.alloca_once_value(builder, awc__hunnl)
        return eiw__skqa._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    zky__nbfl = csv_iterator_typeref.instance_type
    sig = signature(zky__nbfl, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    zhir__sojm = 'def read_csv_objmode(f_reader):\n'
    acr__wgn = [sanitize_varname(alv__shfd) for alv__shfd in
        csv_iterator_type._out_colnames]
    wkwpn__orfc = ir_utils.next_label()
    jldub__cttob = globals()
    out_types = csv_iterator_type._out_types
    jldub__cttob[f'table_type_{wkwpn__orfc}'] = TableType(tuple(out_types))
    jldub__cttob[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    nwyq__pef = list(range(len(csv_iterator_type._usecols)))
    zhir__sojm += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        acr__wgn, out_types, csv_iterator_type._usecols, nwyq__pef,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, wkwpn__orfc, jldub__cttob,
        parallel=False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    qvl__otfjr = bodo.ir.csv_ext._gen_parallel_flag_name(acr__wgn)
    rcfpt__gxgof = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [qvl__otfjr]
    zhir__sojm += f"  return {', '.join(rcfpt__gxgof)}"
    jldub__cttob = globals()
    hwuqn__ombri = {}
    exec(zhir__sojm, jldub__cttob, hwuqn__ombri)
    ldl__pmwa = hwuqn__ombri['read_csv_objmode']
    crb__zjpl = numba.njit(ldl__pmwa)
    bodo.ir.csv_ext.compiled_funcs.append(crb__zjpl)
    wufo__ukhl = 'def read_func(reader, local_start):\n'
    wufo__ukhl += f"  {', '.join(rcfpt__gxgof)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        wufo__ukhl += f'  local_len = len(T)\n'
        wufo__ukhl += '  total_size = local_len\n'
        wufo__ukhl += f'  if ({qvl__otfjr}):\n'
        wufo__ukhl += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        wufo__ukhl += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        epu__pbn = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        wufo__ukhl += '  total_size = 0\n'
        epu__pbn = (
            f'bodo.utils.conversion.convert_to_index({rcfpt__gxgof[1]}, {csv_iterator_type._index_name!r})'
            )
    wufo__ukhl += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({rcfpt__gxgof[0]},), {epu__pbn}, __col_name_meta_value_read_csv_objmode), total_size)
"""
    exec(wufo__ukhl, {'bodo': bodo, 'objmode_func': crb__zjpl, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        '__col_name_meta_value_read_csv_objmode': ColNamesMetaType(
        csv_iterator_type.yield_type.columns)}, hwuqn__ombri)
    return hwuqn__ombri['read_func']
