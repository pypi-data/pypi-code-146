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
        aes__lcn = lhs.scope
        loc = lhs.loc
        xmi__eymve = None
        if lhs.name in self.locals:
            xmi__eymve = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        azvc__ria = {}
        if lhs.name + ':convert' in self.locals:
            azvc__ria = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if xmi__eymve is None:
            bwedh__oyo = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            dtbsf__ueue = get_const_value(file_name, self.func_ir,
                bwedh__oyo, arg_types=self.args, file_info=ParquetFileInfo(
                columns, storage_options=storage_options,
                input_file_name_col=input_file_name_col, read_as_dict_cols=
                read_as_dict_cols, use_hive=use_hive))
            nvln__alz = guard(get_definition, self.func_ir, file_name)
            if isinstance(nvln__alz, ir.Arg) and isinstance(self.args[
                nvln__alz.index], FilenameType):
                typ: FilenameType = self.args[nvln__alz.index]
                (col_names, aisku__pwcw, ebo__unhsg, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = typ.schema
            else:
                (col_names, aisku__pwcw, ebo__unhsg, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = (
                    parquet_file_schema(dtbsf__ueue, columns,
                    storage_options, input_file_name_col, read_as_dict_cols,
                    use_hive))
        else:
            vyl__dug: List[str] = list(xmi__eymve.keys())
            tobox__tgk = {c: jruj__jif for jruj__jif, c in enumerate(vyl__dug)}
            gef__jwxy = [jnadz__rmq for jnadz__rmq in xmi__eymve.values()]
            col_names: List[str] = vyl__dug if columns is None else columns
            col_indices = [tobox__tgk[c] for c in col_names]
            aisku__pwcw = [gef__jwxy[tobox__tgk[c]] for c in col_names]
            ebo__unhsg = next((stvfc__vyp for stvfc__vyp in col_names if
                stvfc__vyp.startswith('__index_level_')), None)
            partition_names = []
            unsupported_columns = []
            unsupported_arrow_types = []
            arrow_schema = numba_to_pyarrow_schema(DataFrameType(data=tuple
                (aisku__pwcw), columns=tuple(col_names)))
        pqjwf__xdfg = None if isinstance(ebo__unhsg, dict
            ) or ebo__unhsg is None else ebo__unhsg
        index_column_index = None
        index_column_type = types.none
        if pqjwf__xdfg:
            xkn__bryqw = col_names.index(pqjwf__xdfg)
            index_column_index = col_indices.pop(xkn__bryqw)
            index_column_type = aisku__pwcw.pop(xkn__bryqw)
            col_names.pop(xkn__bryqw)
        for jruj__jif, c in enumerate(col_names):
            if c in azvc__ria:
                aisku__pwcw[jruj__jif] = azvc__ria[c]
        jzito__vrr = [ir.Var(aes__lcn, mk_unique_var('pq_table'), loc), ir.
            Var(aes__lcn, mk_unique_var('pq_index'), loc)]
        azhl__ffr = [ParquetReader(file_name, lhs.name, col_names,
            col_indices, aisku__pwcw, jzito__vrr, loc, partition_names,
            storage_options, index_column_index, index_column_type,
            input_file_name_col, unsupported_columns,
            unsupported_arrow_types, arrow_schema, use_hive)]
        return (col_names, jzito__vrr, ebo__unhsg, azhl__ffr, aisku__pwcw,
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
    fgs__piqds = pq_node.out_vars[0].name
    nkvnd__zbhu = pq_node.out_vars[1].name
    if fgs__piqds not in lives and nkvnd__zbhu not in lives:
        return None
    elif fgs__piqds not in lives:
        pq_node.col_indices = []
        pq_node.df_colnames = []
        pq_node.out_used_cols = []
        pq_node.is_live_table = False
    elif nkvnd__zbhu not in lives:
        pq_node.index_column_index = None
        pq_node.index_column_type = types.none
    return pq_node


def pq_remove_dead_column(pq_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(pq_node,
        column_live_map, equiv_vars, typemap, 'ParquetReader', pq_node.
        col_indices, require_one_column=False)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, is_independent=False, meta_head_only_info=None):
    msz__vvoo = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    ikohk__aglb, dhr__sfm = bodo.ir.connector.generate_filter_map(pq_node.
        filters)
    extra_args = ', '.join(ikohk__aglb.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, ikohk__aglb, dhr__sfm, pq_node.
        original_df_colnames, pq_node.partition_names, pq_node.
        original_out_types, typemap, 'parquet', output_dnf=False)
    thnhy__uujg = ', '.join(f'out{jruj__jif}' for jruj__jif in range(msz__vvoo)
        )
    uwur__bkb = f'def pq_impl(fname, {extra_args}):\n'
    uwur__bkb += (
        f'    (total_rows, {thnhy__uujg},) = _pq_reader_py(fname, {extra_args})\n'
        )
    oxwk__beski = {}
    exec(uwur__bkb, {}, oxwk__beski)
    sry__lyg = oxwk__beski['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        twcc__sakx = pq_node.loc.strformat()
        viwk__dipjt = []
        ttfdq__ztdl = []
        for jruj__jif in pq_node.out_used_cols:
            qekk__xfq = pq_node.df_colnames[jruj__jif]
            viwk__dipjt.append(qekk__xfq)
            if isinstance(pq_node.out_types[jruj__jif], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                ttfdq__ztdl.append(qekk__xfq)
        unkf__avfv = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', unkf__avfv,
            twcc__sakx, viwk__dipjt)
        if ttfdq__ztdl:
            llcrv__tbgfa = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                llcrv__tbgfa, twcc__sakx, ttfdq__ztdl)
    kem__rjwnt = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        hkd__cajgi = set(pq_node.out_used_cols)
        mptr__qkpm = set(pq_node.unsupported_columns)
        wsbps__bqi = hkd__cajgi & mptr__qkpm
        if wsbps__bqi:
            fqcam__uodw = sorted(wsbps__bqi)
            cjy__frtte = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            hcmlk__vonp = 0
            for kjj__osa in fqcam__uodw:
                while pq_node.unsupported_columns[hcmlk__vonp] != kjj__osa:
                    hcmlk__vonp += 1
                cjy__frtte.append(
                    f"Column '{pq_node.df_colnames[kjj__osa]}' with unsupported arrow type {pq_node.unsupported_arrow_types[hcmlk__vonp]}"
                    )
                hcmlk__vonp += 1
            wemae__aado = '\n'.join(cjy__frtte)
            raise BodoError(wemae__aado, loc=pq_node.loc)
    zxj__vgmk = _gen_pq_reader_py(pq_node.df_colnames, pq_node.col_indices,
        pq_node.out_used_cols, pq_node.out_types, pq_node.storage_options,
        pq_node.partition_names, dnf_filter_str, expr_filter_str,
        extra_args, kem__rjwnt, meta_head_only_info, pq_node.
        index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col, not pq_node.is_live_table, pq_node.
        arrow_schema, pq_node.use_hive)
    djt__pac = typemap[pq_node.file_name.name]
    vaj__lyek = (djt__pac,) + tuple(typemap[cutt__efg.name] for cutt__efg in
        dhr__sfm)
    jkllp__hclj = compile_to_numba_ir(sry__lyg, {'_pq_reader_py': zxj__vgmk
        }, typingctx=typingctx, targetctx=targetctx, arg_typs=vaj__lyek,
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(jkllp__hclj, [pq_node.file_name] + dhr__sfm)
    azhl__ffr = jkllp__hclj.body[:-3]
    if meta_head_only_info:
        azhl__ffr[-3].target = meta_head_only_info[1]
    azhl__ffr[-2].target = pq_node.out_vars[0]
    azhl__ffr[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        is_live_table
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        azhl__ffr.pop(-1)
    elif not pq_node.is_live_table:
        azhl__ffr.pop(-2)
    return azhl__ffr


def _gen_pq_reader_py(col_names, col_indices, out_used_cols, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col, is_dead_table, pyarrow_schema:
    pa.Schema, use_hive: bool):
    ajrbh__fswk = next_label()
    rgkl__mrgl = ',' if extra_args else ''
    uwur__bkb = f'def pq_reader_py(fname,{extra_args}):\n'
    uwur__bkb += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    uwur__bkb += f"    ev.add_attribute('g_fname', fname)\n"
    uwur__bkb += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{rgkl__mrgl}))
"""
    uwur__bkb += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    uwur__bkb += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    nska__zpq = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        nska__zpq = meta_head_only_info[0]
    bgdd__svsml = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in out_used_cols else None
    rchwh__efiys = {c: jruj__jif for jruj__jif, c in enumerate(col_indices)}
    ownzl__bjb = {c: jruj__jif for jruj__jif, c in enumerate(bgdd__svsml)}
    oxhl__khsfj = []
    swja__bdxgg = set()
    cdxjf__iqc = partition_names + [input_file_name_col]
    for jruj__jif in out_used_cols:
        if bgdd__svsml[jruj__jif] not in cdxjf__iqc:
            oxhl__khsfj.append(col_indices[jruj__jif])
        elif not input_file_name_col or bgdd__svsml[jruj__jif
            ] != input_file_name_col:
            swja__bdxgg.add(col_indices[jruj__jif])
    if index_column_index is not None:
        oxhl__khsfj.append(index_column_index)
    oxhl__khsfj = sorted(oxhl__khsfj)
    yvgnn__dnqb = {c: jruj__jif for jruj__jif, c in enumerate(oxhl__khsfj)}
    qnvzf__jpm = [(int(is_nullable(out_types[rchwh__efiys[gqs__wnyw]])) if 
        gqs__wnyw != index_column_index else int(is_nullable(
        index_column_type))) for gqs__wnyw in oxhl__khsfj]
    tcs__mgnh = []
    for gqs__wnyw in oxhl__khsfj:
        if gqs__wnyw == index_column_index:
            jnadz__rmq = index_column_type
        else:
            jnadz__rmq = out_types[rchwh__efiys[gqs__wnyw]]
        if jnadz__rmq == dict_str_arr_type:
            tcs__mgnh.append(gqs__wnyw)
    pyl__kdmd = []
    yuge__ikn = {}
    tgvq__zgil = []
    kvo__ktbj = []
    for jruj__jif, svfj__fwtv in enumerate(partition_names):
        try:
            iwbxt__kqsy = ownzl__bjb[svfj__fwtv]
            if col_indices[iwbxt__kqsy] not in swja__bdxgg:
                continue
        except (KeyError, ValueError) as ggt__obbue:
            continue
        yuge__ikn[svfj__fwtv] = len(pyl__kdmd)
        pyl__kdmd.append(svfj__fwtv)
        tgvq__zgil.append(jruj__jif)
        mye__rikmf = out_types[iwbxt__kqsy].dtype
        vyb__pod = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            mye__rikmf)
        kvo__ktbj.append(numba_to_c_type(vyb__pod))
    uwur__bkb += f"""    total_rows_np = np.array([0], dtype=np.int64)
    out_table = pq_read(
        fname_py,
        {is_parallel},
        dnf_filters,
        expr_filters,
        storage_options_py,
        pyarrow_schema_{ajrbh__fswk},
        {nska__zpq},
        selected_cols_arr_{ajrbh__fswk}.ctypes,
        {len(oxhl__khsfj)},
        nullable_cols_arr_{ajrbh__fswk}.ctypes,
"""
    if len(tgvq__zgil) > 0:
        uwur__bkb += f"""        np.array({tgvq__zgil}, dtype=np.int32).ctypes,
        np.array({kvo__ktbj}, dtype=np.int32).ctypes,
        {len(tgvq__zgil)},
"""
    else:
        uwur__bkb += f'        0, 0, 0,\n'
    if len(tcs__mgnh) > 0:
        uwur__bkb += (
            f'        np.array({tcs__mgnh}, dtype=np.int32).ctypes, {len(tcs__mgnh)},\n'
            )
    else:
        uwur__bkb += f'        0, 0,\n'
    uwur__bkb += f'        total_rows_np.ctypes,\n'
    uwur__bkb += f'        {input_file_name_col is not None},\n'
    uwur__bkb += f'        {use_hive},\n'
    uwur__bkb += f'    )\n'
    uwur__bkb += f'    check_and_propagate_cpp_exception()\n'
    uwur__bkb += f'    total_rows = total_rows_np[0]\n'
    if is_parallel:
        uwur__bkb += f"""    local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
    else:
        uwur__bkb += f'    local_rows = total_rows\n'
    odeqr__jvbo = index_column_type
    uor__aywrr = TableType(tuple(out_types))
    if is_dead_table:
        uor__aywrr = types.none
    if is_dead_table:
        rssl__mirov = None
    else:
        rssl__mirov = []
        qpt__uuqnw = 0
        lkvj__ghpk = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for jruj__jif, kjj__osa in enumerate(col_indices):
            if qpt__uuqnw < len(out_used_cols) and jruj__jif == out_used_cols[
                qpt__uuqnw]:
                gur__ctmc = col_indices[jruj__jif]
                if lkvj__ghpk and gur__ctmc == lkvj__ghpk:
                    rssl__mirov.append(len(oxhl__khsfj) + len(pyl__kdmd))
                elif gur__ctmc in swja__bdxgg:
                    czz__rpkj = bgdd__svsml[jruj__jif]
                    rssl__mirov.append(len(oxhl__khsfj) + yuge__ikn[czz__rpkj])
                else:
                    rssl__mirov.append(yvgnn__dnqb[kjj__osa])
                qpt__uuqnw += 1
            else:
                rssl__mirov.append(-1)
        rssl__mirov = np.array(rssl__mirov, dtype=np.int64)
    if is_dead_table:
        uwur__bkb += '    T = None\n'
    else:
        uwur__bkb += f"""    T = cpp_table_to_py_table(out_table, table_idx_{ajrbh__fswk}, py_table_type_{ajrbh__fswk})
"""
        if len(out_used_cols) == 0:
            uwur__bkb += f'    T = set_table_len(T, local_rows)\n'
    if index_column_index is None:
        uwur__bkb += '    index_arr = None\n'
    else:
        mmwn__jwvfy = yvgnn__dnqb[index_column_index]
        uwur__bkb += f"""    index_arr = info_to_array(info_from_table(out_table, {mmwn__jwvfy}), index_arr_type)
"""
    uwur__bkb += f'    delete_table(out_table)\n'
    uwur__bkb += f'    ev.finalize()\n'
    uwur__bkb += f'    return (total_rows, T, index_arr)\n'
    oxwk__beski = {}
    bpjkx__pjup = {f'py_table_type_{ajrbh__fswk}': uor__aywrr,
        f'table_idx_{ajrbh__fswk}': rssl__mirov,
        f'selected_cols_arr_{ajrbh__fswk}': np.array(oxhl__khsfj, np.int32),
        f'nullable_cols_arr_{ajrbh__fswk}': np.array(qnvzf__jpm, np.int32),
        f'pyarrow_schema_{ajrbh__fswk}': pyarrow_schema.remove_metadata(),
        'index_arr_type': odeqr__jvbo, 'cpp_table_to_py_table':
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
    exec(uwur__bkb, bpjkx__pjup, oxwk__beski)
    zxj__vgmk = oxwk__beski['pq_reader_py']
    dfb__bfguw = numba.njit(zxj__vgmk, no_cpython_wrapper=True)
    return dfb__bfguw


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
