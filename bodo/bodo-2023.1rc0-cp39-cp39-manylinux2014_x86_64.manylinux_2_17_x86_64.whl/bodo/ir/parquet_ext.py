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
        qwwc__qwplt = lhs.scope
        loc = lhs.loc
        eqrpg__ylrty = None
        if lhs.name in self.locals:
            eqrpg__ylrty = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        bkznv__obtbi = {}
        if lhs.name + ':convert' in self.locals:
            bkznv__obtbi = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if eqrpg__ylrty is None:
            tesqx__glr = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            mpx__snmg = get_const_value(file_name, self.func_ir, tesqx__glr,
                arg_types=self.args, file_info=ParquetFileInfo(columns,
                storage_options=storage_options, input_file_name_col=
                input_file_name_col, read_as_dict_cols=read_as_dict_cols,
                use_hive=use_hive))
            lmls__ilfa = guard(get_definition, self.func_ir, file_name)
            if isinstance(lmls__ilfa, ir.Arg) and isinstance(self.args[
                lmls__ilfa.index], FilenameType):
                typ: FilenameType = self.args[lmls__ilfa.index]
                (col_names, cooip__javk, mxh__uvq, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = typ.schema
            else:
                (col_names, cooip__javk, mxh__uvq, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = (
                    parquet_file_schema(mpx__snmg, columns, storage_options,
                    input_file_name_col, read_as_dict_cols, use_hive))
        else:
            uwild__yyjib: List[str] = list(eqrpg__ylrty.keys())
            iyc__sfvyn = {c: uiyeb__iexq for uiyeb__iexq, c in enumerate(
                uwild__yyjib)}
            yec__tcs = [azzsd__vxc for azzsd__vxc in eqrpg__ylrty.values()]
            col_names: List[str] = uwild__yyjib if columns is None else columns
            col_indices = [iyc__sfvyn[c] for c in col_names]
            cooip__javk = [yec__tcs[iyc__sfvyn[c]] for c in col_names]
            mxh__uvq = next((aoaf__xojn for aoaf__xojn in col_names if
                aoaf__xojn.startswith('__index_level_')), None)
            partition_names = []
            unsupported_columns = []
            unsupported_arrow_types = []
            arrow_schema = numba_to_pyarrow_schema(DataFrameType(data=tuple
                (cooip__javk), columns=tuple(col_names)))
        npb__yuz = None if isinstance(mxh__uvq, dict
            ) or mxh__uvq is None else mxh__uvq
        index_column_index = None
        index_column_type = types.none
        if npb__yuz:
            awv__bfi = col_names.index(npb__yuz)
            index_column_index = col_indices.pop(awv__bfi)
            index_column_type = cooip__javk.pop(awv__bfi)
            col_names.pop(awv__bfi)
        for uiyeb__iexq, c in enumerate(col_names):
            if c in bkznv__obtbi:
                cooip__javk[uiyeb__iexq] = bkznv__obtbi[c]
        rovy__efad = [ir.Var(qwwc__qwplt, mk_unique_var('pq_table'), loc),
            ir.Var(qwwc__qwplt, mk_unique_var('pq_index'), loc)]
        znee__aoh = [ParquetReader(file_name, lhs.name, col_names,
            col_indices, cooip__javk, rovy__efad, loc, partition_names,
            storage_options, index_column_index, index_column_type,
            input_file_name_col, unsupported_columns,
            unsupported_arrow_types, arrow_schema, use_hive)]
        return (col_names, rovy__efad, mxh__uvq, znee__aoh, cooip__javk,
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
    kid__cpa = pq_node.out_vars[0].name
    fesul__hgtj = pq_node.out_vars[1].name
    if kid__cpa not in lives and fesul__hgtj not in lives:
        return None
    elif kid__cpa not in lives:
        pq_node.col_indices = []
        pq_node.df_colnames = []
        pq_node.out_used_cols = []
        pq_node.is_live_table = False
    elif fesul__hgtj not in lives:
        pq_node.index_column_index = None
        pq_node.index_column_type = types.none
    return pq_node


def pq_remove_dead_column(pq_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(pq_node,
        column_live_map, equiv_vars, typemap, 'ParquetReader', pq_node.
        col_indices, require_one_column=False)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, is_independent=False, meta_head_only_info=None):
    fak__kxef = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    awhe__tftg, qzws__wbza = bodo.ir.connector.generate_filter_map(pq_node.
        filters)
    extra_args = ', '.join(awhe__tftg.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, awhe__tftg, qzws__wbza, pq_node.
        original_df_colnames, pq_node.partition_names, pq_node.
        original_out_types, typemap, 'parquet', output_dnf=False)
    cyz__lcicx = ', '.join(f'out{uiyeb__iexq}' for uiyeb__iexq in range(
        fak__kxef))
    fwps__jkq = f'def pq_impl(fname, {extra_args}):\n'
    fwps__jkq += (
        f'    (total_rows, {cyz__lcicx},) = _pq_reader_py(fname, {extra_args})\n'
        )
    mil__wewq = {}
    exec(fwps__jkq, {}, mil__wewq)
    dibvx__lir = mil__wewq['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        pll__jvgkm = pq_node.loc.strformat()
        tykz__dus = []
        smfb__qqp = []
        for uiyeb__iexq in pq_node.out_used_cols:
            tch__aaoco = pq_node.df_colnames[uiyeb__iexq]
            tykz__dus.append(tch__aaoco)
            if isinstance(pq_node.out_types[uiyeb__iexq], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                smfb__qqp.append(tch__aaoco)
        guavb__jsw = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', guavb__jsw,
            pll__jvgkm, tykz__dus)
        if smfb__qqp:
            pdnnm__jog = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', pdnnm__jog,
                pll__jvgkm, smfb__qqp)
    saum__hpn = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        hvta__vqd = set(pq_node.out_used_cols)
        pho__fnw = set(pq_node.unsupported_columns)
        umnvq__vpyc = hvta__vqd & pho__fnw
        if umnvq__vpyc:
            qwkd__tfjj = sorted(umnvq__vpyc)
            drstr__thxr = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            uiv__gztu = 0
            for hevf__gzdjs in qwkd__tfjj:
                while pq_node.unsupported_columns[uiv__gztu] != hevf__gzdjs:
                    uiv__gztu += 1
                drstr__thxr.append(
                    f"Column '{pq_node.df_colnames[hevf__gzdjs]}' with unsupported arrow type {pq_node.unsupported_arrow_types[uiv__gztu]}"
                    )
                uiv__gztu += 1
            abto__jzox = '\n'.join(drstr__thxr)
            raise BodoError(abto__jzox, loc=pq_node.loc)
    wbn__iey = _gen_pq_reader_py(pq_node.df_colnames, pq_node.col_indices,
        pq_node.out_used_cols, pq_node.out_types, pq_node.storage_options,
        pq_node.partition_names, dnf_filter_str, expr_filter_str,
        extra_args, saum__hpn, meta_head_only_info, pq_node.
        index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col, not pq_node.is_live_table, pq_node.
        arrow_schema, pq_node.use_hive)
    jnea__ccqi = typemap[pq_node.file_name.name]
    xiskc__qxiy = (jnea__ccqi,) + tuple(typemap[tof__biwkw.name] for
        tof__biwkw in qzws__wbza)
    xdnw__vtte = compile_to_numba_ir(dibvx__lir, {'_pq_reader_py': wbn__iey
        }, typingctx=typingctx, targetctx=targetctx, arg_typs=xiskc__qxiy,
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(xdnw__vtte, [pq_node.file_name] + qzws__wbza)
    znee__aoh = xdnw__vtte.body[:-3]
    if meta_head_only_info:
        znee__aoh[-3].target = meta_head_only_info[1]
    znee__aoh[-2].target = pq_node.out_vars[0]
    znee__aoh[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        is_live_table
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        znee__aoh.pop(-1)
    elif not pq_node.is_live_table:
        znee__aoh.pop(-2)
    return znee__aoh


def _gen_pq_reader_py(col_names, col_indices, out_used_cols, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col, is_dead_table, pyarrow_schema:
    pa.Schema, use_hive: bool):
    eqgr__ioxt = next_label()
    uenu__dmf = ',' if extra_args else ''
    fwps__jkq = f'def pq_reader_py(fname,{extra_args}):\n'
    fwps__jkq += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    fwps__jkq += f"    ev.add_attribute('g_fname', fname)\n"
    fwps__jkq += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{uenu__dmf}))
"""
    fwps__jkq += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    fwps__jkq += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    lrtaw__nth = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        lrtaw__nth = meta_head_only_info[0]
    xjecr__rulp = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in out_used_cols else None
    wenis__zprxh = {c: uiyeb__iexq for uiyeb__iexq, c in enumerate(col_indices)
        }
    gkl__zcbeu = {c: uiyeb__iexq for uiyeb__iexq, c in enumerate(xjecr__rulp)}
    mmqfe__rdoc = []
    ocgz__lkctf = set()
    prd__wqsnb = partition_names + [input_file_name_col]
    for uiyeb__iexq in out_used_cols:
        if xjecr__rulp[uiyeb__iexq] not in prd__wqsnb:
            mmqfe__rdoc.append(col_indices[uiyeb__iexq])
        elif not input_file_name_col or xjecr__rulp[uiyeb__iexq
            ] != input_file_name_col:
            ocgz__lkctf.add(col_indices[uiyeb__iexq])
    if index_column_index is not None:
        mmqfe__rdoc.append(index_column_index)
    mmqfe__rdoc = sorted(mmqfe__rdoc)
    fzhek__tvi = {c: uiyeb__iexq for uiyeb__iexq, c in enumerate(mmqfe__rdoc)}
    kay__xwruh = [(int(is_nullable(out_types[wenis__zprxh[cfem__xmoa]])) if
        cfem__xmoa != index_column_index else int(is_nullable(
        index_column_type))) for cfem__xmoa in mmqfe__rdoc]
    piys__xuykc = []
    for cfem__xmoa in mmqfe__rdoc:
        if cfem__xmoa == index_column_index:
            azzsd__vxc = index_column_type
        else:
            azzsd__vxc = out_types[wenis__zprxh[cfem__xmoa]]
        if azzsd__vxc == dict_str_arr_type:
            piys__xuykc.append(cfem__xmoa)
    yck__caeh = []
    cltc__ajnk = {}
    rgx__mfp = []
    fhof__qrys = []
    for uiyeb__iexq, dsgl__aqm in enumerate(partition_names):
        try:
            jjme__tgcr = gkl__zcbeu[dsgl__aqm]
            if col_indices[jjme__tgcr] not in ocgz__lkctf:
                continue
        except (KeyError, ValueError) as ofog__rgyoq:
            continue
        cltc__ajnk[dsgl__aqm] = len(yck__caeh)
        yck__caeh.append(dsgl__aqm)
        rgx__mfp.append(uiyeb__iexq)
        cgcp__vhy = out_types[jjme__tgcr].dtype
        qffoh__nbaud = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(cgcp__vhy))
        fhof__qrys.append(numba_to_c_type(qffoh__nbaud))
    fwps__jkq += f"""    total_rows_np = np.array([0], dtype=np.int64)
    out_table = pq_read(
        fname_py,
        {is_parallel},
        dnf_filters,
        expr_filters,
        storage_options_py,
        pyarrow_schema_{eqgr__ioxt},
        {lrtaw__nth},
        selected_cols_arr_{eqgr__ioxt}.ctypes,
        {len(mmqfe__rdoc)},
        nullable_cols_arr_{eqgr__ioxt}.ctypes,
"""
    if len(rgx__mfp) > 0:
        fwps__jkq += f"""        np.array({rgx__mfp}, dtype=np.int32).ctypes,
        np.array({fhof__qrys}, dtype=np.int32).ctypes,
        {len(rgx__mfp)},
"""
    else:
        fwps__jkq += f'        0, 0, 0,\n'
    if len(piys__xuykc) > 0:
        fwps__jkq += f"""        np.array({piys__xuykc}, dtype=np.int32).ctypes, {len(piys__xuykc)},
"""
    else:
        fwps__jkq += f'        0, 0,\n'
    fwps__jkq += f'        total_rows_np.ctypes,\n'
    fwps__jkq += f'        {input_file_name_col is not None},\n'
    fwps__jkq += f'        {use_hive},\n'
    fwps__jkq += f'    )\n'
    fwps__jkq += f'    check_and_propagate_cpp_exception()\n'
    fwps__jkq += f'    total_rows = total_rows_np[0]\n'
    if is_parallel:
        fwps__jkq += f"""    local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
    else:
        fwps__jkq += f'    local_rows = total_rows\n'
    cel__wvar = index_column_type
    yayou__haqi = TableType(tuple(out_types))
    if is_dead_table:
        yayou__haqi = types.none
    if is_dead_table:
        rdxdd__smp = None
    else:
        rdxdd__smp = []
        bgx__cxj = 0
        uuin__kbs = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for uiyeb__iexq, hevf__gzdjs in enumerate(col_indices):
            if bgx__cxj < len(out_used_cols) and uiyeb__iexq == out_used_cols[
                bgx__cxj]:
                azqco__jkgkl = col_indices[uiyeb__iexq]
                if uuin__kbs and azqco__jkgkl == uuin__kbs:
                    rdxdd__smp.append(len(mmqfe__rdoc) + len(yck__caeh))
                elif azqco__jkgkl in ocgz__lkctf:
                    fyk__dvnpy = xjecr__rulp[uiyeb__iexq]
                    rdxdd__smp.append(len(mmqfe__rdoc) + cltc__ajnk[fyk__dvnpy]
                        )
                else:
                    rdxdd__smp.append(fzhek__tvi[hevf__gzdjs])
                bgx__cxj += 1
            else:
                rdxdd__smp.append(-1)
        rdxdd__smp = np.array(rdxdd__smp, dtype=np.int64)
    if is_dead_table:
        fwps__jkq += '    T = None\n'
    else:
        fwps__jkq += f"""    T = cpp_table_to_py_table(out_table, table_idx_{eqgr__ioxt}, py_table_type_{eqgr__ioxt})
"""
        if len(out_used_cols) == 0:
            fwps__jkq += f'    T = set_table_len(T, local_rows)\n'
    if index_column_index is None:
        fwps__jkq += '    index_arr = None\n'
    else:
        mhvx__ftwfj = fzhek__tvi[index_column_index]
        fwps__jkq += f"""    index_arr = info_to_array(info_from_table(out_table, {mhvx__ftwfj}), index_arr_type)
"""
    fwps__jkq += f'    delete_table(out_table)\n'
    fwps__jkq += f'    ev.finalize()\n'
    fwps__jkq += f'    return (total_rows, T, index_arr)\n'
    mil__wewq = {}
    msj__ycmm = {f'py_table_type_{eqgr__ioxt}': yayou__haqi,
        f'table_idx_{eqgr__ioxt}': rdxdd__smp,
        f'selected_cols_arr_{eqgr__ioxt}': np.array(mmqfe__rdoc, np.int32),
        f'nullable_cols_arr_{eqgr__ioxt}': np.array(kay__xwruh, np.int32),
        f'pyarrow_schema_{eqgr__ioxt}': pyarrow_schema.remove_metadata(),
        'index_arr_type': cel__wvar, 'cpp_table_to_py_table':
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
    exec(fwps__jkq, msj__ycmm, mil__wewq)
    wbn__iey = mil__wewq['pq_reader_py']
    rphgd__hmut = numba.njit(wbn__iey, no_cpython_wrapper=True)
    return rphgd__hmut


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
