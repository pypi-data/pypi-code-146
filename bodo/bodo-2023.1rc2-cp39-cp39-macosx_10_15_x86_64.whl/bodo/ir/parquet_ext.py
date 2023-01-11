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
        hqcq__safec = lhs.scope
        loc = lhs.loc
        xnw__nwl = None
        if lhs.name in self.locals:
            xnw__nwl = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        nacfk__rejks = {}
        if lhs.name + ':convert' in self.locals:
            nacfk__rejks = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if xnw__nwl is None:
            dlu__rbm = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            jpoc__gae = get_const_value(file_name, self.func_ir, dlu__rbm,
                arg_types=self.args, file_info=ParquetFileInfo(columns,
                storage_options=storage_options, input_file_name_col=
                input_file_name_col, read_as_dict_cols=read_as_dict_cols,
                use_hive=use_hive))
            wnx__smcwt = guard(get_definition, self.func_ir, file_name)
            if isinstance(wnx__smcwt, ir.Arg) and isinstance(self.args[
                wnx__smcwt.index], FilenameType):
                typ: FilenameType = self.args[wnx__smcwt.index]
                (col_names, rhi__keiz, hjxpj__vzkv, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = typ.schema
            else:
                (col_names, rhi__keiz, hjxpj__vzkv, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = (
                    parquet_file_schema(jpoc__gae, columns, storage_options,
                    input_file_name_col, read_as_dict_cols, use_hive))
        else:
            zyg__wzejd: List[str] = list(xnw__nwl.keys())
            rmxks__rupzp = {c: vdhfc__env for vdhfc__env, c in enumerate(
                zyg__wzejd)}
            sod__zbb = [gyrkq__pxam for gyrkq__pxam in xnw__nwl.values()]
            col_names: List[str] = zyg__wzejd if columns is None else columns
            col_indices = [rmxks__rupzp[c] for c in col_names]
            rhi__keiz = [sod__zbb[rmxks__rupzp[c]] for c in col_names]
            hjxpj__vzkv = next((hzwn__cpdr for hzwn__cpdr in col_names if
                hzwn__cpdr.startswith('__index_level_')), None)
            partition_names = []
            unsupported_columns = []
            unsupported_arrow_types = []
            arrow_schema = numba_to_pyarrow_schema(DataFrameType(data=tuple
                (rhi__keiz), columns=tuple(col_names)))
        rmwk__nlb = None if isinstance(hjxpj__vzkv, dict
            ) or hjxpj__vzkv is None else hjxpj__vzkv
        index_column_index = None
        index_column_type = types.none
        if rmwk__nlb:
            lnd__ggwu = col_names.index(rmwk__nlb)
            index_column_index = col_indices.pop(lnd__ggwu)
            index_column_type = rhi__keiz.pop(lnd__ggwu)
            col_names.pop(lnd__ggwu)
        for vdhfc__env, c in enumerate(col_names):
            if c in nacfk__rejks:
                rhi__keiz[vdhfc__env] = nacfk__rejks[c]
        ncvv__hkzk = [ir.Var(hqcq__safec, mk_unique_var('pq_table'), loc),
            ir.Var(hqcq__safec, mk_unique_var('pq_index'), loc)]
        fbbk__uux = [ParquetReader(file_name, lhs.name, col_names,
            col_indices, rhi__keiz, ncvv__hkzk, loc, partition_names,
            storage_options, index_column_index, index_column_type,
            input_file_name_col, unsupported_columns,
            unsupported_arrow_types, arrow_schema, use_hive)]
        return (col_names, ncvv__hkzk, hjxpj__vzkv, fbbk__uux, rhi__keiz,
            index_column_type)


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
    ftjx__fvdy = pq_node.out_vars[0].name
    qqkwi__etcm = pq_node.out_vars[1].name
    if ftjx__fvdy not in lives and qqkwi__etcm not in lives:
        return None
    elif ftjx__fvdy not in lives:
        pq_node.col_indices = []
        pq_node.df_colnames = []
        pq_node.out_used_cols = []
        pq_node.is_live_table = False
    elif qqkwi__etcm not in lives:
        pq_node.index_column_index = None
        pq_node.index_column_type = types.none
    return pq_node


def pq_remove_dead_column(pq_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(pq_node,
        column_live_map, equiv_vars, typemap, 'ParquetReader', pq_node.
        col_indices, require_one_column=False)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, is_independent=False, meta_head_only_info=None):
    ufl__hjif = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    tgwb__fvbg, dzyn__zuo = bodo.ir.connector.generate_filter_map(pq_node.
        filters)
    extra_args = ', '.join(tgwb__fvbg.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, tgwb__fvbg, dzyn__zuo, pq_node.
        original_df_colnames, pq_node.partition_names, pq_node.
        original_out_types, typemap, 'parquet', output_dnf=False)
    vnz__wrtiy = ', '.join(f'out{vdhfc__env}' for vdhfc__env in range(
        ufl__hjif))
    wkh__tcc = f'def pq_impl(fname, {extra_args}):\n'
    wkh__tcc += (
        f'    (total_rows, {vnz__wrtiy},) = _pq_reader_py(fname, {extra_args})\n'
        )
    sfbpj__kvjtk = {}
    exec(wkh__tcc, {}, sfbpj__kvjtk)
    rec__bofk = sfbpj__kvjtk['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        earxr__crx = pq_node.loc.strformat()
        czbd__rlvex = []
        dhn__bnor = []
        for vdhfc__env in pq_node.out_used_cols:
            akp__kbkmj = pq_node.df_colnames[vdhfc__env]
            czbd__rlvex.append(akp__kbkmj)
            if isinstance(pq_node.out_types[vdhfc__env], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dhn__bnor.append(akp__kbkmj)
        mzpy__ktz = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', mzpy__ktz,
            earxr__crx, czbd__rlvex)
        if dhn__bnor:
            xsfe__jbw = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', xsfe__jbw,
                earxr__crx, dhn__bnor)
    zhwb__dqn = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        ixo__orbut = set(pq_node.out_used_cols)
        xeywq__qih = set(pq_node.unsupported_columns)
        ciurc__znmlf = ixo__orbut & xeywq__qih
        if ciurc__znmlf:
            daex__muore = sorted(ciurc__znmlf)
            qdhsg__tuc = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            rkd__kimzr = 0
            for ynamk__yyswk in daex__muore:
                while pq_node.unsupported_columns[rkd__kimzr] != ynamk__yyswk:
                    rkd__kimzr += 1
                qdhsg__tuc.append(
                    f"Column '{pq_node.df_colnames[ynamk__yyswk]}' with unsupported arrow type {pq_node.unsupported_arrow_types[rkd__kimzr]}"
                    )
                rkd__kimzr += 1
            ewz__tpj = '\n'.join(qdhsg__tuc)
            raise BodoError(ewz__tpj, loc=pq_node.loc)
    qxovr__ofdv = _gen_pq_reader_py(pq_node.df_colnames, pq_node.
        col_indices, pq_node.out_used_cols, pq_node.out_types, pq_node.
        storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, zhwb__dqn, meta_head_only_info,
        pq_node.index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col, not pq_node.is_live_table, pq_node.
        arrow_schema, pq_node.use_hive)
    une__odf = typemap[pq_node.file_name.name]
    tozl__cuwx = (une__odf,) + tuple(typemap[ighyh__mqp.name] for
        ighyh__mqp in dzyn__zuo)
    pxhad__fukxm = compile_to_numba_ir(rec__bofk, {'_pq_reader_py':
        qxovr__ofdv}, typingctx=typingctx, targetctx=targetctx, arg_typs=
        tozl__cuwx, typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(pxhad__fukxm, [pq_node.file_name] + dzyn__zuo)
    fbbk__uux = pxhad__fukxm.body[:-3]
    if meta_head_only_info:
        fbbk__uux[-3].target = meta_head_only_info[1]
    fbbk__uux[-2].target = pq_node.out_vars[0]
    fbbk__uux[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        is_live_table
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        fbbk__uux.pop(-1)
    elif not pq_node.is_live_table:
        fbbk__uux.pop(-2)
    return fbbk__uux


def _gen_pq_reader_py(col_names, col_indices, out_used_cols, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col, is_dead_table, pyarrow_schema:
    pa.Schema, use_hive: bool):
    msni__gut = next_label()
    xids__mgqlv = ',' if extra_args else ''
    wkh__tcc = f'def pq_reader_py(fname,{extra_args}):\n'
    wkh__tcc += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    wkh__tcc += f"    ev.add_attribute('g_fname', fname)\n"
    wkh__tcc += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{xids__mgqlv}))
"""
    wkh__tcc += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    wkh__tcc += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    vttfi__nmq = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        vttfi__nmq = meta_head_only_info[0]
    eao__vwuic = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in out_used_cols else None
    plk__sjudq = {c: vdhfc__env for vdhfc__env, c in enumerate(col_indices)}
    wqyv__sft = {c: vdhfc__env for vdhfc__env, c in enumerate(eao__vwuic)}
    asoim__vjkab = []
    awt__zysr = set()
    azcx__mxs = partition_names + [input_file_name_col]
    for vdhfc__env in out_used_cols:
        if eao__vwuic[vdhfc__env] not in azcx__mxs:
            asoim__vjkab.append(col_indices[vdhfc__env])
        elif not input_file_name_col or eao__vwuic[vdhfc__env
            ] != input_file_name_col:
            awt__zysr.add(col_indices[vdhfc__env])
    if index_column_index is not None:
        asoim__vjkab.append(index_column_index)
    asoim__vjkab = sorted(asoim__vjkab)
    pnzw__zrmwm = {c: vdhfc__env for vdhfc__env, c in enumerate(asoim__vjkab)}
    nho__bsmq = [(int(is_nullable(out_types[plk__sjudq[vlwp__qklz]])) if 
        vlwp__qklz != index_column_index else int(is_nullable(
        index_column_type))) for vlwp__qklz in asoim__vjkab]
    lzs__iyr = []
    for vlwp__qklz in asoim__vjkab:
        if vlwp__qklz == index_column_index:
            gyrkq__pxam = index_column_type
        else:
            gyrkq__pxam = out_types[plk__sjudq[vlwp__qklz]]
        if gyrkq__pxam == dict_str_arr_type:
            lzs__iyr.append(vlwp__qklz)
    vufa__ljwgk = []
    hcpc__iegm = {}
    edo__gaw = []
    gljw__jpw = []
    for vdhfc__env, wxp__mpv in enumerate(partition_names):
        try:
            agt__qpsxz = wqyv__sft[wxp__mpv]
            if col_indices[agt__qpsxz] not in awt__zysr:
                continue
        except (KeyError, ValueError) as rrdsk__aikl:
            continue
        hcpc__iegm[wxp__mpv] = len(vufa__ljwgk)
        vufa__ljwgk.append(wxp__mpv)
        edo__gaw.append(vdhfc__env)
        kulu__cnh = out_types[agt__qpsxz].dtype
        yps__kayms = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            kulu__cnh)
        gljw__jpw.append(numba_to_c_type(yps__kayms))
    wkh__tcc += f"""    total_rows_np = np.array([0], dtype=np.int64)
    out_table = pq_read(
        fname_py,
        {is_parallel},
        dnf_filters,
        expr_filters,
        storage_options_py,
        pyarrow_schema_{msni__gut},
        {vttfi__nmq},
        selected_cols_arr_{msni__gut}.ctypes,
        {len(asoim__vjkab)},
        nullable_cols_arr_{msni__gut}.ctypes,
"""
    if len(edo__gaw) > 0:
        wkh__tcc += f"""        np.array({edo__gaw}, dtype=np.int32).ctypes,
        np.array({gljw__jpw}, dtype=np.int32).ctypes,
        {len(edo__gaw)},
"""
    else:
        wkh__tcc += f'        0, 0, 0,\n'
    if len(lzs__iyr) > 0:
        wkh__tcc += (
            f'        np.array({lzs__iyr}, dtype=np.int32).ctypes, {len(lzs__iyr)},\n'
            )
    else:
        wkh__tcc += f'        0, 0,\n'
    wkh__tcc += f'        total_rows_np.ctypes,\n'
    wkh__tcc += f'        {input_file_name_col is not None},\n'
    wkh__tcc += f'        {use_hive},\n'
    wkh__tcc += f'    )\n'
    wkh__tcc += f'    check_and_propagate_cpp_exception()\n'
    wkh__tcc += f'    total_rows = total_rows_np[0]\n'
    if is_parallel:
        wkh__tcc += f"""    local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
    else:
        wkh__tcc += f'    local_rows = total_rows\n'
    yfa__opzol = index_column_type
    bdh__afcr = TableType(tuple(out_types))
    if is_dead_table:
        bdh__afcr = types.none
    if is_dead_table:
        okdl__fcyg = None
    else:
        okdl__fcyg = []
        kbijj__heibi = 0
        mvs__kqdqh = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for vdhfc__env, ynamk__yyswk in enumerate(col_indices):
            if kbijj__heibi < len(out_used_cols
                ) and vdhfc__env == out_used_cols[kbijj__heibi]:
                mxm__wqdbv = col_indices[vdhfc__env]
                if mvs__kqdqh and mxm__wqdbv == mvs__kqdqh:
                    okdl__fcyg.append(len(asoim__vjkab) + len(vufa__ljwgk))
                elif mxm__wqdbv in awt__zysr:
                    zizf__fna = eao__vwuic[vdhfc__env]
                    okdl__fcyg.append(len(asoim__vjkab) + hcpc__iegm[zizf__fna]
                        )
                else:
                    okdl__fcyg.append(pnzw__zrmwm[ynamk__yyswk])
                kbijj__heibi += 1
            else:
                okdl__fcyg.append(-1)
        okdl__fcyg = np.array(okdl__fcyg, dtype=np.int64)
    if is_dead_table:
        wkh__tcc += '    T = None\n'
    else:
        wkh__tcc += f"""    T = cpp_table_to_py_table(out_table, table_idx_{msni__gut}, py_table_type_{msni__gut})
"""
        if len(out_used_cols) == 0:
            wkh__tcc += f'    T = set_table_len(T, local_rows)\n'
    if index_column_index is None:
        wkh__tcc += '    index_arr = None\n'
    else:
        zlps__prk = pnzw__zrmwm[index_column_index]
        wkh__tcc += f"""    index_arr = info_to_array(info_from_table(out_table, {zlps__prk}), index_arr_type)
"""
    wkh__tcc += f'    delete_table(out_table)\n'
    wkh__tcc += f'    ev.finalize()\n'
    wkh__tcc += f'    return (total_rows, T, index_arr)\n'
    sfbpj__kvjtk = {}
    pksr__zxvrw = {f'py_table_type_{msni__gut}': bdh__afcr,
        f'table_idx_{msni__gut}': okdl__fcyg,
        f'selected_cols_arr_{msni__gut}': np.array(asoim__vjkab, np.int32),
        f'nullable_cols_arr_{msni__gut}': np.array(nho__bsmq, np.int32),
        f'pyarrow_schema_{msni__gut}': pyarrow_schema.remove_metadata(),
        'index_arr_type': yfa__opzol, 'cpp_table_to_py_table':
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
    exec(wkh__tcc, pksr__zxvrw, sfbpj__kvjtk)
    qxovr__ofdv = sfbpj__kvjtk['pq_reader_py']
    ztiks__egvs = numba.njit(qxovr__ofdv, no_cpython_wrapper=True)
    return ztiks__egvs


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
