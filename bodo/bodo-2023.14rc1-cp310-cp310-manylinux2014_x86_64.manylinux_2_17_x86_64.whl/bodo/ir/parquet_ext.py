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
        fjxw__hfrd = lhs.scope
        loc = lhs.loc
        avke__ukzm = None
        if lhs.name in self.locals:
            avke__ukzm = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        rmfbb__zasp = {}
        if lhs.name + ':convert' in self.locals:
            rmfbb__zasp = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if avke__ukzm is None:
            epyts__bnuwk = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            cwjbb__dweqp = get_const_value(file_name, self.func_ir,
                epyts__bnuwk, arg_types=self.args, file_info=
                ParquetFileInfo(columns, storage_options=storage_options,
                input_file_name_col=input_file_name_col, read_as_dict_cols=
                read_as_dict_cols, use_hive=use_hive))
            nyys__vrdw = guard(get_definition, self.func_ir, file_name)
            if isinstance(nyys__vrdw, ir.Arg) and isinstance(self.args[
                nyys__vrdw.index], FilenameType):
                typ: FilenameType = self.args[nyys__vrdw.index]
                (col_names, gobzh__slq, ltb__cbdc, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = typ.schema
            else:
                (col_names, gobzh__slq, ltb__cbdc, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = (
                    parquet_file_schema(cwjbb__dweqp, columns,
                    storage_options, input_file_name_col, read_as_dict_cols,
                    use_hive))
        else:
            xtd__oorax: List[str] = list(avke__ukzm.keys())
            tmwbl__usgps = {c: swwfe__yybca for swwfe__yybca, c in
                enumerate(xtd__oorax)}
            phy__rbjur = [guim__ijvk for guim__ijvk in avke__ukzm.values()]
            col_names: List[str] = xtd__oorax if columns is None else columns
            col_indices = [tmwbl__usgps[c] for c in col_names]
            gobzh__slq = [phy__rbjur[tmwbl__usgps[c]] for c in col_names]
            ltb__cbdc = next((gxep__xlme for gxep__xlme in col_names if
                gxep__xlme.startswith('__index_level_')), None)
            partition_names = []
            unsupported_columns = []
            unsupported_arrow_types = []
            arrow_schema = numba_to_pyarrow_schema(DataFrameType(data=tuple
                (gobzh__slq), columns=tuple(col_names)))
        bufao__ipcof = None if isinstance(ltb__cbdc, dict
            ) or ltb__cbdc is None else ltb__cbdc
        index_column_index = None
        index_column_type = types.none
        if bufao__ipcof:
            xzbin__maoq = col_names.index(bufao__ipcof)
            index_column_index = col_indices.pop(xzbin__maoq)
            index_column_type = gobzh__slq.pop(xzbin__maoq)
            col_names.pop(xzbin__maoq)
        for swwfe__yybca, c in enumerate(col_names):
            if c in rmfbb__zasp:
                gobzh__slq[swwfe__yybca] = rmfbb__zasp[c]
        ifg__zbi = [ir.Var(fjxw__hfrd, mk_unique_var('pq_table'), loc), ir.
            Var(fjxw__hfrd, mk_unique_var('pq_index'), loc)]
        thfn__xorp = [ParquetReader(file_name, lhs.name, col_names,
            col_indices, gobzh__slq, ifg__zbi, loc, partition_names,
            storage_options, index_column_index, index_column_type,
            input_file_name_col, unsupported_columns,
            unsupported_arrow_types, arrow_schema, use_hive)]
        return (col_names, ifg__zbi, ltb__cbdc, thfn__xorp, gobzh__slq,
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
    rvms__bagn = pq_node.out_vars[0].name
    lqbit__zkxww = pq_node.out_vars[1].name
    if rvms__bagn not in lives and lqbit__zkxww not in lives:
        return None
    elif rvms__bagn not in lives:
        pq_node.col_indices = []
        pq_node.df_colnames = []
        pq_node.out_used_cols = []
        pq_node.is_live_table = False
    elif lqbit__zkxww not in lives:
        pq_node.index_column_index = None
        pq_node.index_column_type = types.none
    return pq_node


def pq_remove_dead_column(pq_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(pq_node,
        column_live_map, equiv_vars, typemap, 'ParquetReader', pq_node.
        col_indices, require_one_column=False)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, is_independent=False, meta_head_only_info=None):
    inqw__xjv = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    bff__mou, kvd__wdw = bodo.ir.connector.generate_filter_map(pq_node.filters)
    extra_args = ', '.join(bff__mou.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, bff__mou, kvd__wdw, pq_node.original_df_colnames,
        pq_node.partition_names, pq_node.original_out_types, typemap,
        'parquet', output_dnf=False)
    wzbs__thkx = ', '.join(f'out{swwfe__yybca}' for swwfe__yybca in range(
        inqw__xjv))
    njul__edv = f'def pq_impl(fname, {extra_args}):\n'
    njul__edv += (
        f'    (total_rows, {wzbs__thkx},) = _pq_reader_py(fname, {extra_args})\n'
        )
    fmq__lok = {}
    exec(njul__edv, {}, fmq__lok)
    ejp__aik = fmq__lok['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        xwugl__johbm = pq_node.loc.strformat()
        gzt__xitut = []
        vgl__gzy = []
        for swwfe__yybca in pq_node.out_used_cols:
            cqydj__ssp = pq_node.df_colnames[swwfe__yybca]
            gzt__xitut.append(cqydj__ssp)
            if isinstance(pq_node.out_types[swwfe__yybca], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                vgl__gzy.append(cqydj__ssp)
        bex__hrzw = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', bex__hrzw,
            xwugl__johbm, gzt__xitut)
        if vgl__gzy:
            hvk__tftra = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', hvk__tftra,
                xwugl__johbm, vgl__gzy)
    qcgz__lumvx = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        ycz__wvmn = set(pq_node.out_used_cols)
        yapn__oum = set(pq_node.unsupported_columns)
        yhwi__dppt = ycz__wvmn & yapn__oum
        if yhwi__dppt:
            ivld__moffo = sorted(yhwi__dppt)
            ubool__qhkrw = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            kxfl__kxy = 0
            for oai__rtyhm in ivld__moffo:
                while pq_node.unsupported_columns[kxfl__kxy] != oai__rtyhm:
                    kxfl__kxy += 1
                ubool__qhkrw.append(
                    f"Column '{pq_node.df_colnames[oai__rtyhm]}' with unsupported arrow type {pq_node.unsupported_arrow_types[kxfl__kxy]}"
                    )
                kxfl__kxy += 1
            rnd__yfok = '\n'.join(ubool__qhkrw)
            raise BodoError(rnd__yfok, loc=pq_node.loc)
    upmxg__jcc = _gen_pq_reader_py(pq_node.df_colnames, pq_node.col_indices,
        pq_node.out_used_cols, pq_node.out_types, pq_node.storage_options,
        pq_node.partition_names, dnf_filter_str, expr_filter_str,
        extra_args, qcgz__lumvx, meta_head_only_info, pq_node.
        index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col, not pq_node.is_live_table, pq_node.
        arrow_schema, pq_node.use_hive)
    pqqmv__rile = typemap[pq_node.file_name.name]
    vubdz__povq = (pqqmv__rile,) + tuple(typemap[tnuq__sxapz.name] for
        tnuq__sxapz in kvd__wdw)
    boclh__ywhxw = compile_to_numba_ir(ejp__aik, {'_pq_reader_py':
        upmxg__jcc}, typingctx=typingctx, targetctx=targetctx, arg_typs=
        vubdz__povq, typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(boclh__ywhxw, [pq_node.file_name] + kvd__wdw)
    thfn__xorp = boclh__ywhxw.body[:-3]
    if meta_head_only_info:
        thfn__xorp[-3].target = meta_head_only_info[1]
    thfn__xorp[-2].target = pq_node.out_vars[0]
    thfn__xorp[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        is_live_table
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        thfn__xorp.pop(-1)
    elif not pq_node.is_live_table:
        thfn__xorp.pop(-2)
    return thfn__xorp


def _gen_pq_reader_py(col_names, col_indices, out_used_cols, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col, is_dead_table, pyarrow_schema:
    pa.Schema, use_hive: bool):
    ixcbf__zkat = next_label()
    ejzut__pqiq = ',' if extra_args else ''
    njul__edv = f'def pq_reader_py(fname,{extra_args}):\n'
    njul__edv += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    njul__edv += f"    ev.add_attribute('g_fname', fname)\n"
    njul__edv += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{ejzut__pqiq}))
"""
    njul__edv += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    njul__edv += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    eef__yol = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        eef__yol = meta_head_only_info[0]
    llnrr__fnv = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in out_used_cols else None
    wirff__vaqm = {c: swwfe__yybca for swwfe__yybca, c in enumerate(
        col_indices)}
    eyokw__uiwz = {c: swwfe__yybca for swwfe__yybca, c in enumerate(llnrr__fnv)
        }
    dfjhv__ynuv = []
    wdxfh__xmgdv = set()
    vuffs__icr = partition_names + [input_file_name_col]
    for swwfe__yybca in out_used_cols:
        if llnrr__fnv[swwfe__yybca] not in vuffs__icr:
            dfjhv__ynuv.append(col_indices[swwfe__yybca])
        elif not input_file_name_col or llnrr__fnv[swwfe__yybca
            ] != input_file_name_col:
            wdxfh__xmgdv.add(col_indices[swwfe__yybca])
    if index_column_index is not None:
        dfjhv__ynuv.append(index_column_index)
    dfjhv__ynuv = sorted(dfjhv__ynuv)
    wejh__veb = {c: swwfe__yybca for swwfe__yybca, c in enumerate(dfjhv__ynuv)}
    ktyj__yjvlj = [(int(is_nullable(out_types[wirff__vaqm[kom__par]])) if 
        kom__par != index_column_index else int(is_nullable(
        index_column_type))) for kom__par in dfjhv__ynuv]
    fbteg__lung = []
    for kom__par in dfjhv__ynuv:
        if kom__par == index_column_index:
            guim__ijvk = index_column_type
        else:
            guim__ijvk = out_types[wirff__vaqm[kom__par]]
        if guim__ijvk == dict_str_arr_type:
            fbteg__lung.append(kom__par)
    bkfwq__ckto = []
    jqwid__oey = {}
    vjmpu__jvmg = []
    vpcv__endyy = []
    for swwfe__yybca, uvfj__lsj in enumerate(partition_names):
        try:
            ypkyg__ojz = eyokw__uiwz[uvfj__lsj]
            if col_indices[ypkyg__ojz] not in wdxfh__xmgdv:
                continue
        except (KeyError, ValueError) as idvva__viw:
            continue
        jqwid__oey[uvfj__lsj] = len(bkfwq__ckto)
        bkfwq__ckto.append(uvfj__lsj)
        vjmpu__jvmg.append(swwfe__yybca)
        gkejj__dbk = out_types[ypkyg__ojz].dtype
        cjdt__ngiee = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            gkejj__dbk)
        vpcv__endyy.append(numba_to_c_type(cjdt__ngiee))
    njul__edv += f"""    total_rows_np = np.array([0], dtype=np.int64)
    out_table = pq_read(
        fname_py,
        {is_parallel},
        dnf_filters,
        expr_filters,
        storage_options_py,
        pyarrow_schema_{ixcbf__zkat},
        {eef__yol},
        selected_cols_arr_{ixcbf__zkat}.ctypes,
        {len(dfjhv__ynuv)},
        nullable_cols_arr_{ixcbf__zkat}.ctypes,
"""
    if len(vjmpu__jvmg) > 0:
        njul__edv += f"""        np.array({vjmpu__jvmg}, dtype=np.int32).ctypes,
        np.array({vpcv__endyy}, dtype=np.int32).ctypes,
        {len(vjmpu__jvmg)},
"""
    else:
        njul__edv += f'        0, 0, 0,\n'
    if len(fbteg__lung) > 0:
        njul__edv += f"""        np.array({fbteg__lung}, dtype=np.int32).ctypes, {len(fbteg__lung)},
"""
    else:
        njul__edv += f'        0, 0,\n'
    njul__edv += f'        total_rows_np.ctypes,\n'
    njul__edv += f'        {input_file_name_col is not None},\n'
    njul__edv += f'        {use_hive},\n'
    njul__edv += f'    )\n'
    njul__edv += f'    check_and_propagate_cpp_exception()\n'
    njul__edv += f'    total_rows = total_rows_np[0]\n'
    if is_parallel:
        njul__edv += f"""    local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
    else:
        njul__edv += f'    local_rows = total_rows\n'
    mipir__nwgiu = index_column_type
    ortt__jugcn = TableType(tuple(out_types))
    if is_dead_table:
        ortt__jugcn = types.none
    if is_dead_table:
        nfb__ksiyt = None
    else:
        nfb__ksiyt = []
        imccc__qanh = 0
        giyo__ough = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for swwfe__yybca, oai__rtyhm in enumerate(col_indices):
            if imccc__qanh < len(out_used_cols
                ) and swwfe__yybca == out_used_cols[imccc__qanh]:
                zmsf__blk = col_indices[swwfe__yybca]
                if giyo__ough and zmsf__blk == giyo__ough:
                    nfb__ksiyt.append(len(dfjhv__ynuv) + len(bkfwq__ckto))
                elif zmsf__blk in wdxfh__xmgdv:
                    avnv__fmoyd = llnrr__fnv[swwfe__yybca]
                    nfb__ksiyt.append(len(dfjhv__ynuv) + jqwid__oey[
                        avnv__fmoyd])
                else:
                    nfb__ksiyt.append(wejh__veb[oai__rtyhm])
                imccc__qanh += 1
            else:
                nfb__ksiyt.append(-1)
        nfb__ksiyt = np.array(nfb__ksiyt, dtype=np.int64)
    if is_dead_table:
        njul__edv += '    T = None\n'
    else:
        njul__edv += f"""    T = cpp_table_to_py_table(out_table, table_idx_{ixcbf__zkat}, py_table_type_{ixcbf__zkat})
"""
        if len(out_used_cols) == 0:
            njul__edv += f'    T = set_table_len(T, local_rows)\n'
    if index_column_index is None:
        njul__edv += '    index_arr = None\n'
    else:
        defy__npk = wejh__veb[index_column_index]
        njul__edv += f"""    index_arr = info_to_array(info_from_table(out_table, {defy__npk}), index_arr_type)
"""
    njul__edv += f'    delete_table(out_table)\n'
    njul__edv += f'    ev.finalize()\n'
    njul__edv += f'    return (total_rows, T, index_arr)\n'
    fmq__lok = {}
    kcpes__jusc = {f'py_table_type_{ixcbf__zkat}': ortt__jugcn,
        f'table_idx_{ixcbf__zkat}': nfb__ksiyt,
        f'selected_cols_arr_{ixcbf__zkat}': np.array(dfjhv__ynuv, np.int32),
        f'nullable_cols_arr_{ixcbf__zkat}': np.array(ktyj__yjvlj, np.int32),
        f'pyarrow_schema_{ixcbf__zkat}': pyarrow_schema.remove_metadata(),
        'index_arr_type': mipir__nwgiu, 'cpp_table_to_py_table':
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
    exec(njul__edv, kcpes__jusc, fmq__lok)
    upmxg__jcc = fmq__lok['pq_reader_py']
    xdhug__adlva = numba.njit(upmxg__jcc, no_cpython_wrapper=True)
    return xdhug__adlva


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
