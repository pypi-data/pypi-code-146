"""IR node for the parquet data access"""
from typing import List
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, get_definition, guard, mk_unique_var, next_label, replace_arg_nodes
from numba.extending import NativeValue, models, register_model, unbox
import bodo
import bodo.ir.connector
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.table import Table, TableType
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.io.helpers import is_nullable, numba_to_pyarrow_schema, pyarrow_table_schema_type
from bodo.io.parquet_pio import ParquetFileInfo, get_filters_pyobject, parquet_file_schema, parquet_predicate_type
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.str_ext import unicode_to_utf8
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.transform import get_const_value
from bodo.utils.typing import BodoError, FilenameType
from bodo.utils.utils import check_and_propagate_cpp_exception, numba_to_c_type, sanitize_varname


class ReadParquetFilepathType(types.Opaque):

    def __init__(self):
        super(ReadParquetFilepathType, self).__init__(name=
            'ReadParquetFilepathType')


read_parquet_fpath_type = ReadParquetFilepathType()
types.read_parquet_fpath_type = read_parquet_fpath_type
register_model(ReadParquetFilepathType)(models.OpaqueModel)


@unbox(ReadParquetFilepathType)
def unbox_read_parquet_fpath_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None, use_hive=True):
        ncwvo__rkqbi = lhs.scope
        loc = lhs.loc
        kiq__eow = None
        if lhs.name in self.locals:
            kiq__eow = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        riwne__yjs = {}
        if lhs.name + ':convert' in self.locals:
            riwne__yjs = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if kiq__eow is None:
            rnz__fnicf = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            khk__lqjwp = get_const_value(file_name, self.func_ir,
                rnz__fnicf, arg_types=self.args, file_info=ParquetFileInfo(
                columns, storage_options=storage_options,
                input_file_name_col=input_file_name_col, read_as_dict_cols=
                read_as_dict_cols, use_hive=use_hive))
            xjrff__bweol = guard(get_definition, self.func_ir, file_name)
            if isinstance(xjrff__bweol, ir.Arg) and isinstance(self.args[
                xjrff__bweol.index], FilenameType):
                typ: FilenameType = self.args[xjrff__bweol.index]
                (col_names, nxr__osgjo, nxyrk__ryvgk, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = typ.schema
            else:
                (col_names, nxr__osgjo, nxyrk__ryvgk, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = (
                    parquet_file_schema(khk__lqjwp, columns,
                    storage_options, input_file_name_col, read_as_dict_cols,
                    use_hive))
        else:
            gpes__ugm: List[str] = list(kiq__eow.keys())
            dxrh__wjn = {c: fpek__nqk for fpek__nqk, c in enumerate(gpes__ugm)}
            iechm__xulsc = [rzond__xgug for rzond__xgug in kiq__eow.values()]
            col_names: List[str] = gpes__ugm if columns is None else columns
            col_indices = [dxrh__wjn[c] for c in col_names]
            nxr__osgjo = [iechm__xulsc[dxrh__wjn[c]] for c in col_names]
            nxyrk__ryvgk = next((wmvf__eyhqt for wmvf__eyhqt in col_names if
                wmvf__eyhqt.startswith('__index_level_')), None)
            partition_names = []
            unsupported_columns = []
            unsupported_arrow_types = []
            arrow_schema = numba_to_pyarrow_schema(DataFrameType(data=tuple
                (nxr__osgjo), columns=tuple(col_names)))
        ymqio__iky = None if isinstance(nxyrk__ryvgk, dict
            ) or nxyrk__ryvgk is None else nxyrk__ryvgk
        index_column_index = None
        index_column_type = types.none
        if ymqio__iky:
            hzq__kmpz = col_names.index(ymqio__iky)
            index_column_index = col_indices.pop(hzq__kmpz)
            index_column_type = nxr__osgjo.pop(hzq__kmpz)
            col_names.pop(hzq__kmpz)
        for fpek__nqk, c in enumerate(col_names):
            if c in riwne__yjs:
                nxr__osgjo[fpek__nqk] = riwne__yjs[c]
        qziym__rry = [ir.Var(ncwvo__rkqbi, mk_unique_var('pq_table'), loc),
            ir.Var(ncwvo__rkqbi, mk_unique_var('pq_index'), loc)]
        kedot__ktzr = [ParquetReader(file_name, lhs.name, col_names,
            col_indices, nxr__osgjo, qziym__rry, loc, partition_names,
            storage_options, index_column_index, index_column_type,
            input_file_name_col, unsupported_columns,
            unsupported_arrow_types, arrow_schema, use_hive)]
        return (col_names, qziym__rry, nxyrk__ryvgk, kedot__ktzr,
            nxr__osgjo, index_column_type)


class ParquetReader(ir.Stmt):

    def __init__(self, file_name, df_out, col_names, col_indices, out_types,
        out_vars, loc, partition_names, storage_options, index_column_index,
        index_column_type, input_file_name_col, unsupported_columns,
        unsupported_arrow_types, arrow_schema, use_hive):
        self.connector_typ = 'parquet'
        self.file_name = file_name
        self.df_out = df_out
        self.df_colnames = col_names
        self.col_indices = col_indices
        self.out_types = out_types
        self.original_out_types = out_types
        self.original_df_colnames = col_names
        self.out_vars = out_vars
        self.loc = loc
        self.partition_names = partition_names
        self.filters = None
        self.storage_options = storage_options
        self.index_column_index = index_column_index
        self.index_column_type = index_column_type
        self.out_used_cols = list(range(len(col_indices)))
        self.input_file_name_col = input_file_name_col
        self.unsupported_columns = unsupported_columns
        self.unsupported_arrow_types = unsupported_arrow_types
        self.arrow_schema = arrow_schema
        self.is_live_table = True
        self.use_hive = use_hive

    def __repr__(self):
        return (
            '({}) = ReadParquet({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'
            .format(self.df_out, self.file_name.name, self.df_colnames,
            self.col_indices, self.out_types, self.original_out_types, self
            .original_df_colnames, self.out_vars, self.partition_names,
            self.filters, self.storage_options, self.index_column_index,
            self.index_column_type, self.out_used_cols, self.
            input_file_name_col, self.unsupported_columns, self.
            unsupported_arrow_types, self.arrow_schema))


def remove_dead_pq(pq_node, lives_no_aliases, lives, arg_aliases, alias_map,
    func_ir, typemap):
    kap__mzz = pq_node.out_vars[0].name
    ohl__nkqrl = pq_node.out_vars[1].name
    if kap__mzz not in lives and ohl__nkqrl not in lives:
        return None
    elif kap__mzz not in lives:
        pq_node.col_indices = []
        pq_node.df_colnames = []
        pq_node.out_used_cols = []
        pq_node.is_live_table = False
    elif ohl__nkqrl not in lives:
        pq_node.index_column_index = None
        pq_node.index_column_type = types.none
    return pq_node


def pq_remove_dead_column(pq_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(pq_node,
        column_live_map, equiv_vars, typemap, 'ParquetReader', pq_node.
        col_indices, require_one_column=False)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, is_independent=False, meta_head_only_info=None):
    lkcyz__dwld = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    ccz__tkn, psvf__aqls = bodo.ir.connector.generate_filter_map(pq_node.
        filters)
    extra_args = ', '.join(ccz__tkn.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, ccz__tkn, psvf__aqls, pq_node.original_df_colnames,
        pq_node.partition_names, pq_node.original_out_types, typemap,
        'parquet', output_dnf=False)
    noa__kifv = ', '.join(f'out{fpek__nqk}' for fpek__nqk in range(lkcyz__dwld)
        )
    hbyvr__iep = f'def pq_impl(fname, {extra_args}):\n'
    hbyvr__iep += (
        f'    (total_rows, {noa__kifv},) = _pq_reader_py(fname, {extra_args})\n'
        )
    agq__syddk = {}
    exec(hbyvr__iep, {}, agq__syddk)
    ksgla__ebaf = agq__syddk['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        ecwh__gecd = pq_node.loc.strformat()
        uvd__vzgbg = []
        tywkc__hxe = []
        for fpek__nqk in pq_node.out_used_cols:
            wex__bkya = pq_node.df_colnames[fpek__nqk]
            uvd__vzgbg.append(wex__bkya)
            if isinstance(pq_node.out_types[fpek__nqk], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                tywkc__hxe.append(wex__bkya)
        unm__slevf = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', unm__slevf,
            ecwh__gecd, uvd__vzgbg)
        if tywkc__hxe:
            lgcl__iqh = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', lgcl__iqh,
                ecwh__gecd, tywkc__hxe)
    qsn__ywa = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        yhk__kiqba = set(pq_node.out_used_cols)
        osum__roo = set(pq_node.unsupported_columns)
        cpcx__pbyha = yhk__kiqba & osum__roo
        if cpcx__pbyha:
            edrd__bapp = sorted(cpcx__pbyha)
            jjdx__dtu = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            mlch__jdt = 0
            for ull__xzeru in edrd__bapp:
                while pq_node.unsupported_columns[mlch__jdt] != ull__xzeru:
                    mlch__jdt += 1
                jjdx__dtu.append(
                    f"Column '{pq_node.df_colnames[ull__xzeru]}' with unsupported arrow type {pq_node.unsupported_arrow_types[mlch__jdt]}"
                    )
                mlch__jdt += 1
            qimf__prmcn = '\n'.join(jjdx__dtu)
            raise BodoError(qimf__prmcn, loc=pq_node.loc)
    eyd__xiw = _gen_pq_reader_py(pq_node.df_colnames, pq_node.col_indices,
        pq_node.out_used_cols, pq_node.out_types, pq_node.storage_options,
        pq_node.partition_names, dnf_filter_str, expr_filter_str,
        extra_args, qsn__ywa, meta_head_only_info, pq_node.
        index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col, not pq_node.is_live_table, pq_node.
        arrow_schema, pq_node.use_hive)
    nhiuw__owoha = typemap[pq_node.file_name.name]
    pogdn__kypkw = (nhiuw__owoha,) + tuple(typemap[oticv__pgu.name] for
        oticv__pgu in psvf__aqls)
    wqp__mgypt = compile_to_numba_ir(ksgla__ebaf, {'_pq_reader_py':
        eyd__xiw}, typingctx=typingctx, targetctx=targetctx, arg_typs=
        pogdn__kypkw, typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(wqp__mgypt, [pq_node.file_name] + psvf__aqls)
    kedot__ktzr = wqp__mgypt.body[:-3]
    if meta_head_only_info:
        kedot__ktzr[-3].target = meta_head_only_info[1]
    kedot__ktzr[-2].target = pq_node.out_vars[0]
    kedot__ktzr[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        is_live_table
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        kedot__ktzr.pop(-1)
    elif not pq_node.is_live_table:
        kedot__ktzr.pop(-2)
    return kedot__ktzr


def _gen_pq_reader_py(col_names, col_indices, out_used_cols, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col, is_dead_table, pyarrow_schema:
    pa.Schema, use_hive: bool):
    bowys__qga = next_label()
    aggw__ejw = ',' if extra_args else ''
    hbyvr__iep = f'def pq_reader_py(fname,{extra_args}):\n'
    hbyvr__iep += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    hbyvr__iep += f"    ev.add_attribute('g_fname', fname)\n"
    hbyvr__iep += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{aggw__ejw}))
"""
    hbyvr__iep += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    hbyvr__iep += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    pltuz__myqi = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        pltuz__myqi = meta_head_only_info[0]
    bsrse__nspwb = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in out_used_cols else None
    rhfd__whmqs = {c: fpek__nqk for fpek__nqk, c in enumerate(col_indices)}
    dyb__nto = {c: fpek__nqk for fpek__nqk, c in enumerate(bsrse__nspwb)}
    nrgg__gga = []
    alzc__dopp = set()
    ufvf__yohtu = partition_names + [input_file_name_col]
    for fpek__nqk in out_used_cols:
        if bsrse__nspwb[fpek__nqk] not in ufvf__yohtu:
            nrgg__gga.append(col_indices[fpek__nqk])
        elif not input_file_name_col or bsrse__nspwb[fpek__nqk
            ] != input_file_name_col:
            alzc__dopp.add(col_indices[fpek__nqk])
    if index_column_index is not None:
        nrgg__gga.append(index_column_index)
    nrgg__gga = sorted(nrgg__gga)
    dpc__zdg = {c: fpek__nqk for fpek__nqk, c in enumerate(nrgg__gga)}
    auy__qxe = [(int(is_nullable(out_types[rhfd__whmqs[mixy__nzz]])) if 
        mixy__nzz != index_column_index else int(is_nullable(
        index_column_type))) for mixy__nzz in nrgg__gga]
    akoe__jwlr = []
    for mixy__nzz in nrgg__gga:
        if mixy__nzz == index_column_index:
            rzond__xgug = index_column_type
        else:
            rzond__xgug = out_types[rhfd__whmqs[mixy__nzz]]
        if rzond__xgug == dict_str_arr_type:
            akoe__jwlr.append(mixy__nzz)
    cpav__gbxnv = []
    oagkb__udn = {}
    gyn__usp = []
    aezxb__doq = []
    for fpek__nqk, xdh__tla in enumerate(partition_names):
        try:
            alu__kyoly = dyb__nto[xdh__tla]
            if col_indices[alu__kyoly] not in alzc__dopp:
                continue
        except (KeyError, ValueError) as jfhn__fccn:
            continue
        oagkb__udn[xdh__tla] = len(cpav__gbxnv)
        cpav__gbxnv.append(xdh__tla)
        gyn__usp.append(fpek__nqk)
        zkei__rgj = out_types[alu__kyoly].dtype
        grwl__xqu = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            zkei__rgj)
        aezxb__doq.append(numba_to_c_type(grwl__xqu))
    hbyvr__iep += f"""    total_rows_np = np.array([0], dtype=np.int64)
    out_table = pq_read(
        fname_py,
        {is_parallel},
        dnf_filters,
        expr_filters,
        storage_options_py,
        pyarrow_schema_{bowys__qga},
        {pltuz__myqi},
        selected_cols_arr_{bowys__qga}.ctypes,
        {len(nrgg__gga)},
        nullable_cols_arr_{bowys__qga}.ctypes,
"""
    if len(gyn__usp) > 0:
        hbyvr__iep += f"""        np.array({gyn__usp}, dtype=np.int32).ctypes,
        np.array({aezxb__doq}, dtype=np.int32).ctypes,
        {len(gyn__usp)},
"""
    else:
        hbyvr__iep += f'        0, 0, 0,\n'
    if len(akoe__jwlr) > 0:
        hbyvr__iep += (
            f'        np.array({akoe__jwlr}, dtype=np.int32).ctypes, {len(akoe__jwlr)},\n'
            )
    else:
        hbyvr__iep += f'        0, 0,\n'
    hbyvr__iep += f'        total_rows_np.ctypes,\n'
    hbyvr__iep += f'        {input_file_name_col is not None},\n'
    hbyvr__iep += f'        {use_hive},\n'
    hbyvr__iep += f'    )\n'
    hbyvr__iep += f'    check_and_propagate_cpp_exception()\n'
    hbyvr__iep += f'    total_rows = total_rows_np[0]\n'
    if is_parallel:
        hbyvr__iep += f"""    local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
    else:
        hbyvr__iep += f'    local_rows = total_rows\n'
    ffozb__gybv = index_column_type
    iia__sea = TableType(tuple(out_types))
    if is_dead_table:
        iia__sea = types.none
    if is_dead_table:
        broj__klwuz = None
    else:
        broj__klwuz = []
        gbmd__wilay = 0
        qpv__dxlej = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for fpek__nqk, ull__xzeru in enumerate(col_indices):
            if gbmd__wilay < len(out_used_cols) and fpek__nqk == out_used_cols[
                gbmd__wilay]:
                tbx__mpfz = col_indices[fpek__nqk]
                if qpv__dxlej and tbx__mpfz == qpv__dxlej:
                    broj__klwuz.append(len(nrgg__gga) + len(cpav__gbxnv))
                elif tbx__mpfz in alzc__dopp:
                    vnzg__fzur = bsrse__nspwb[fpek__nqk]
                    broj__klwuz.append(len(nrgg__gga) + oagkb__udn[vnzg__fzur])
                else:
                    broj__klwuz.append(dpc__zdg[ull__xzeru])
                gbmd__wilay += 1
            else:
                broj__klwuz.append(-1)
        broj__klwuz = np.array(broj__klwuz, dtype=np.int64)
    if is_dead_table:
        hbyvr__iep += '    T = None\n'
    else:
        hbyvr__iep += f"""    T = cpp_table_to_py_table(out_table, table_idx_{bowys__qga}, py_table_type_{bowys__qga})
"""
        if len(out_used_cols) == 0:
            hbyvr__iep += f'    T = set_table_len(T, local_rows)\n'
    if index_column_index is None:
        hbyvr__iep += '    index_arr = None\n'
    else:
        pab__nnn = dpc__zdg[index_column_index]
        hbyvr__iep += f"""    index_arr = info_to_array(info_from_table(out_table, {pab__nnn}), index_arr_type)
"""
    hbyvr__iep += f'    delete_table(out_table)\n'
    hbyvr__iep += f'    ev.finalize()\n'
    hbyvr__iep += f'    return (total_rows, T, index_arr)\n'
    agq__syddk = {}
    mmfn__jpntc = {f'py_table_type_{bowys__qga}': iia__sea,
        f'table_idx_{bowys__qga}': broj__klwuz,
        f'selected_cols_arr_{bowys__qga}': np.array(nrgg__gga, np.int32),
        f'nullable_cols_arr_{bowys__qga}': np.array(auy__qxe, np.int32),
        f'pyarrow_schema_{bowys__qga}': pyarrow_schema.remove_metadata(),
        'index_arr_type': ffozb__gybv, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo,
        'get_node_portion': bodo.libs.distributed_api.get_node_portion,
        'set_table_len': bodo.hiframes.table.set_table_len}
    exec(hbyvr__iep, mmfn__jpntc, agq__syddk)
    eyd__xiw = agq__syddk['pq_reader_py']
    qtwjx__xpc = numba.njit(eyd__xiw, no_cpython_wrapper=True)
    return qtwjx__xpc


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


numba.parfors.array_analysis.array_analysis_extensions[ParquetReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[ParquetReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[ParquetReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[ParquetReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[ParquetReader] = remove_dead_pq
numba.core.analysis.ir_extension_usedefs[ParquetReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[ParquetReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[ParquetReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[ParquetReader
    ] = bodo.ir.connector.build_connector_definitions
remove_dead_column_extensions[ParquetReader] = pq_remove_dead_column
ir_extension_table_column_use[ParquetReader
    ] = bodo.ir.connector.connector_table_column_use
distributed_pass.distributed_run_extensions[ParquetReader] = pq_distributed_run
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('pq_read', arrow_cpp.pq_read)
_pq_read = types.ExternalFunction('pq_read', table_type(
    read_parquet_fpath_type, types.boolean, parquet_predicate_type,
    parquet_predicate_type, storage_options_dict_type,
    pyarrow_table_schema_type, types.int64, types.voidptr, types.int32,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.voidptr,
    types.int32, types.voidptr, types.boolean, types.boolean))
