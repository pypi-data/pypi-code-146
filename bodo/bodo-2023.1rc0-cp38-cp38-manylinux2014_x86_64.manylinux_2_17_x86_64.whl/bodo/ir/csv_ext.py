from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
from numba.extending import intrinsic
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.table import Table, TableType
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import check_and_propagate_cpp_exception, sanitize_varname


class CsvReader(ir.Stmt):

    def __init__(self, file_name, df_out, sep, df_colnames, out_vars,
        out_types, usecols, loc, header, compression, nrows, skiprows,
        chunksize, is_skiprows_list, low_memory, escapechar,
        storage_options=None, index_column_index=None, index_column_typ=
        types.none):
        self.connector_typ = 'csv'
        self.file_name = file_name
        self.df_out = df_out
        self.sep = sep
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.usecols = usecols
        self.loc = loc
        self.skiprows = skiprows
        self.nrows = nrows
        self.header = header
        self.compression = compression
        self.chunksize = chunksize
        self.is_skiprows_list = is_skiprows_list
        self.pd_low_memory = low_memory
        self.escapechar = escapechar
        self.storage_options = storage_options
        self.index_column_index = index_column_index
        self.index_column_typ = index_column_typ
        self.out_used_cols = list(range(len(usecols)))

    def __repr__(self):
        return (
            '{} = ReadCsv(file={}, col_names={}, types={}, vars={}, nrows={}, skiprows={}, chunksize={}, is_skiprows_list={}, pd_low_memory={}, escapechar={}, storage_options={}, index_column_index={}, index_colum_typ = {}, out_used_colss={})'
            .format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars, self.nrows, self.skiprows, self.
            chunksize, self.is_skiprows_list, self.pd_low_memory, self.
            escapechar, self.storage_options, self.index_column_index, self
            .index_column_typ, self.out_used_cols))


def check_node_typing(node, typemap):
    ogq__uqcsf = typemap[node.file_name.name]
    if types.unliteral(ogq__uqcsf) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {ogq__uqcsf}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        gwvk__trras = typemap[node.skiprows.name]
        if isinstance(gwvk__trras, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(gwvk__trras, types.Integer) and not (isinstance
            (gwvk__trras, (types.List, types.Tuple)) and isinstance(
            gwvk__trras.dtype, types.Integer)) and not isinstance(gwvk__trras,
            (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {gwvk__trras}."
                , loc=node.skiprows.loc)
        elif isinstance(gwvk__trras, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        tkb__nptog = typemap[node.nrows.name]
        if not isinstance(tkb__nptog, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {tkb__nptog}."
                , loc=node.nrows.loc)


import llvmlite.binding as ll
from bodo.io import csv_cpp
ll.add_symbol('csv_file_chunk_reader', csv_cpp.csv_file_chunk_reader)


@intrinsic
def csv_file_chunk_reader(typingctx, fname_t, is_parallel_t, skiprows_t,
    nrows_t, header_t, compression_t, bucket_region_t, storage_options_t,
    chunksize_t, is_skiprows_list_t, skiprows_list_len_t, pd_low_memory_t):
    assert storage_options_t == storage_options_dict_type, "Storage options don't match expected type"

    def codegen(context, builder, sig, args):
        khqel__bhm = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(64),
            lir.IntType(1)])
        xkn__jay = cgutils.get_or_insert_function(builder.module,
            khqel__bhm, name='csv_file_chunk_reader')
        nyzvq__jxgvc = builder.call(xkn__jay, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        slkqp__nbhfl = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        awcz__frylj = context.get_python_api(builder)
        slkqp__nbhfl.meminfo = awcz__frylj.nrt_meminfo_new_from_pyobject(
            context.get_constant_null(types.voidptr), nyzvq__jxgvc)
        slkqp__nbhfl.pyobj = nyzvq__jxgvc
        awcz__frylj.decref(nyzvq__jxgvc)
        return slkqp__nbhfl._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.
        voidptr, types.int64, types.bool_, types.voidptr, types.voidptr,
        storage_options_dict_type, types.int64, types.bool_, types.int64,
        types.bool_), codegen


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        uxj__digj = csv_node.out_vars[0]
        if uxj__digj.name not in lives:
            return None
    else:
        oimi__azesk = csv_node.out_vars[0]
        fxjzv__nqjm = csv_node.out_vars[1]
        if oimi__azesk.name not in lives and fxjzv__nqjm.name not in lives:
            return None
        elif fxjzv__nqjm.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif oimi__azesk.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.out_used_cols = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    gwvk__trras = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            nka__womhs = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            rwed__rpz = csv_node.loc.strformat()
            enae__ohz = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', nka__womhs,
                rwed__rpz, enae__ohz)
            htc__llh = csv_node.out_types[0].yield_type.data
            wbf__nux = [jhwrc__yurri for sanh__jiiwf, jhwrc__yurri in
                enumerate(csv_node.df_colnames) if isinstance(htc__llh[
                sanh__jiiwf], bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if wbf__nux:
                uycoz__ecry = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    uycoz__ecry, rwed__rpz, wbf__nux)
        if array_dists is not None:
            lfxkg__ketrk = csv_node.out_vars[0].name
            parallel = array_dists[lfxkg__ketrk] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        tyqvf__czhd = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        tyqvf__czhd += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        tyqvf__czhd += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        gyty__drx = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(tyqvf__czhd, {}, gyty__drx)
        rhnl__gjipy = gyty__drx['csv_iterator_impl']
        sbbd__rbbe = 'def csv_reader_init(fname, nrows, skiprows):\n'
        sbbd__rbbe += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        sbbd__rbbe += '  return f_reader\n'
        exec(sbbd__rbbe, globals(), gyty__drx)
        jrk__wvpj = gyty__drx['csv_reader_init']
        zyw__evaa = numba.njit(jrk__wvpj)
        compiled_funcs.append(zyw__evaa)
        lfx__ygrmf = compile_to_numba_ir(rhnl__gjipy, {'_csv_reader_init':
            zyw__evaa, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, gwvk__trras), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(lfx__ygrmf, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        dalp__zyh = lfx__ygrmf.body[:-3]
        dalp__zyh[-1].target = csv_node.out_vars[0]
        return dalp__zyh
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    tyqvf__czhd = 'def csv_impl(fname, nrows, skiprows):\n'
    tyqvf__czhd += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    gyty__drx = {}
    exec(tyqvf__czhd, {}, gyty__drx)
    eqq__ostvi = gyty__drx['csv_impl']
    wwtp__crprf = csv_node.usecols
    if wwtp__crprf:
        wwtp__crprf = [csv_node.usecols[sanh__jiiwf] for sanh__jiiwf in
            csv_node.out_used_cols]
    if bodo.user_logging.get_verbose_level() >= 1:
        nka__womhs = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        rwed__rpz = csv_node.loc.strformat()
        enae__ohz = []
        wbf__nux = []
        if wwtp__crprf:
            for sanh__jiiwf in csv_node.out_used_cols:
                zksav__zld = csv_node.df_colnames[sanh__jiiwf]
                enae__ohz.append(zksav__zld)
                if isinstance(csv_node.out_types[sanh__jiiwf], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    wbf__nux.append(zksav__zld)
        bodo.user_logging.log_message('Column Pruning', nka__womhs,
            rwed__rpz, enae__ohz)
        if wbf__nux:
            uycoz__ecry = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                uycoz__ecry, rwed__rpz, wbf__nux)
    hwlb__irdvs = _gen_csv_reader_py(csv_node.df_colnames, csv_node.
        out_types, wwtp__crprf, csv_node.out_used_cols, csv_node.sep,
        parallel, csv_node.header, csv_node.compression, csv_node.
        is_skiprows_list, csv_node.pd_low_memory, csv_node.escapechar,
        csv_node.storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    lfx__ygrmf = compile_to_numba_ir(eqq__ostvi, {'_csv_reader_py':
        hwlb__irdvs}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, gwvk__trras), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(lfx__ygrmf, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    dalp__zyh = lfx__ygrmf.body[:-3]
    dalp__zyh[-1].target = csv_node.out_vars[1]
    dalp__zyh[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not wwtp__crprf
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        dalp__zyh.pop(-1)
    elif not wwtp__crprf:
        dalp__zyh.pop(-2)
    return dalp__zyh


def csv_remove_dead_column(csv_node, column_live_map, equiv_vars, typemap):
    if csv_node.chunksize is not None:
        return False
    return bodo.ir.connector.base_connector_remove_dead_columns(csv_node,
        column_live_map, equiv_vars, typemap, 'CSVReader', csv_node.usecols)


numba.parfors.array_analysis.array_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[CsvReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[CsvReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[CsvReader] = remove_dead_csv
numba.core.analysis.ir_extension_usedefs[CsvReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[CsvReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[CsvReader] = csv_distributed_run
remove_dead_column_extensions[CsvReader] = csv_remove_dead_column
ir_extension_table_column_use[CsvReader
    ] = bodo.ir.connector.connector_table_column_use


def _get_dtype_str(t):
    hpew__vjmek = t.dtype
    if isinstance(hpew__vjmek, PDCategoricalDtype):
        ewsz__ziygl = CategoricalArrayType(hpew__vjmek)
        cetaj__ghx = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, cetaj__ghx, ewsz__ziygl)
        return cetaj__ghx
    if hpew__vjmek == types.NPDatetime('ns'):
        hpew__vjmek = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        grjle__anx = 'int_arr_{}'.format(hpew__vjmek)
        setattr(types, grjle__anx, t)
        return grjle__anx
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if hpew__vjmek == types.bool_:
        hpew__vjmek = 'bool_'
    if hpew__vjmek == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(hpew__vjmek, (
        StringArrayType, ArrayItemArrayType)):
        zmlg__vvdqa = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, zmlg__vvdqa, t)
        return zmlg__vvdqa
    return '{}[::1]'.format(hpew__vjmek)


def _get_pd_dtype_str(t):
    hpew__vjmek = t.dtype
    if isinstance(hpew__vjmek, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(hpew__vjmek.categories)
    if hpew__vjmek == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type or t == bodo.dict_str_arr_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if hpew__vjmek.signed else 'U',
            hpew__vjmek.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(hpew__vjmek, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(hpew__vjmek)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    hxl__lgzj = ''
    from collections import defaultdict
    zibg__wci = defaultdict(list)
    for rbc__ujmbt, wku__wdztp in typemap.items():
        zibg__wci[wku__wdztp].append(rbc__ujmbt)
    arq__wjboo = df.columns.to_list()
    ytx__lliph = []
    for wku__wdztp, uaolm__nvyrw in zibg__wci.items():
        try:
            ytx__lliph.append(df.loc[:, uaolm__nvyrw].astype(wku__wdztp,
                copy=False))
            df = df.drop(uaolm__nvyrw, axis=1)
        except (ValueError, TypeError) as wqp__dghb:
            hxl__lgzj = (
                f"Caught the runtime error '{wqp__dghb}' on columns {uaolm__nvyrw}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    fowhj__wbd = bool(hxl__lgzj)
    if parallel:
        fme__wdkhr = MPI.COMM_WORLD
        fowhj__wbd = fme__wdkhr.allreduce(fowhj__wbd, op=MPI.LOR)
    if fowhj__wbd:
        vnorf__fdp = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if hxl__lgzj:
            raise TypeError(f'{vnorf__fdp}\n{hxl__lgzj}')
        else:
            raise TypeError(
                f'{vnorf__fdp}\nPlease refer to errors on other ranks.')
    df = pd.concat(ytx__lliph + [df], axis=1)
    cghdd__fucfk = df.loc[:, arq__wjboo]
    return cghdd__fucfk


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    cgobi__esx = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        tyqvf__czhd = '  skiprows = sorted(set(skiprows))\n'
    else:
        tyqvf__czhd = '  skiprows = [skiprows]\n'
    tyqvf__czhd += '  skiprows_list_len = len(skiprows)\n'
    tyqvf__czhd += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    tyqvf__czhd += '  check_java_installation(fname)\n'
    tyqvf__czhd += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    tyqvf__czhd += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    tyqvf__czhd += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    tyqvf__czhd += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, cgobi__esx, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    tyqvf__czhd += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    tyqvf__czhd += "      raise FileNotFoundError('File does not exist')\n"
    return tyqvf__czhd


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    out_used_cols, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    slqg__ftb = [str(sanh__jiiwf) for sanh__jiiwf, gfam__kej in enumerate(
        usecols) if col_typs[out_used_cols[sanh__jiiwf]].dtype == types.
        NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        slqg__ftb.append(str(idx_col_index))
    akx__jmn = ', '.join(slqg__ftb)
    dni__nrx = _gen_parallel_flag_name(sanitized_cnames)
    midsi__cpa = f"{dni__nrx}='bool_'" if check_parallel_runtime else ''
    wmif__cqmk = [_get_pd_dtype_str(col_typs[out_used_cols[sanh__jiiwf]]) for
        sanh__jiiwf in range(len(usecols))]
    uohn__ead = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    lopz__onse = [gfam__kej for sanh__jiiwf, gfam__kej in enumerate(usecols
        ) if wmif__cqmk[sanh__jiiwf] == 'str']
    if idx_col_index is not None and uohn__ead == 'str':
        lopz__onse.append(idx_col_index)
    tze__rcp = np.array(lopz__onse, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = tze__rcp
    tyqvf__czhd = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    kpn__rucy = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = kpn__rucy
    tyqvf__czhd += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    xdfd__pzu = np.array(out_used_cols, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = xdfd__pzu
        tyqvf__czhd += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    tjq__cnw = defaultdict(list)
    for sanh__jiiwf, gfam__kej in enumerate(usecols):
        if wmif__cqmk[sanh__jiiwf] == 'str':
            continue
        tjq__cnw[wmif__cqmk[sanh__jiiwf]].append(gfam__kej)
    if idx_col_index is not None and uohn__ead != 'str':
        tjq__cnw[uohn__ead].append(idx_col_index)
    for sanh__jiiwf, gqzh__wug in enumerate(tjq__cnw.values()):
        glbs[f't_arr_{sanh__jiiwf}_{call_id}'] = np.asarray(gqzh__wug)
        tyqvf__czhd += (
            f'  t_arr_{sanh__jiiwf}_{call_id}_2 = t_arr_{sanh__jiiwf}_{call_id}\n'
            )
    if idx_col_index != None:
        tyqvf__czhd += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {midsi__cpa}):
"""
    else:
        tyqvf__czhd += (
            f'  with objmode(T=table_type_{call_id}, {midsi__cpa}):\n')
    tyqvf__czhd += f'    typemap = {{}}\n'
    for sanh__jiiwf, hfj__myggn in enumerate(tjq__cnw.keys()):
        tyqvf__czhd += f"""    typemap.update({{i:{hfj__myggn} for i in t_arr_{sanh__jiiwf}_{call_id}_2}})
"""
    tyqvf__czhd += '    if f_reader.get_chunk_size() == 0:\n'
    tyqvf__czhd += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    tyqvf__czhd += '    else:\n'
    tyqvf__czhd += '      df = pd.read_csv(f_reader,\n'
    tyqvf__czhd += '        header=None,\n'
    tyqvf__czhd += '        parse_dates=[{}],\n'.format(akx__jmn)
    tyqvf__czhd += (
        f"        dtype={{i:'string[pyarrow]' for i in str_col_nums_{call_id}_2}},\n"
        )
    tyqvf__czhd += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        tyqvf__czhd += f'    {dni__nrx} = f_reader.is_parallel()\n'
    else:
        tyqvf__czhd += f'    {dni__nrx} = {parallel}\n'
    tyqvf__czhd += f'    df = astype(df, typemap, {dni__nrx})\n'
    if idx_col_index != None:
        mjl__vho = sorted(kpn__rucy).index(idx_col_index)
        tyqvf__czhd += f'    idx_arr = df.iloc[:, {mjl__vho}].values\n'
        tyqvf__czhd += (
            f'    df.drop(columns=df.columns[{mjl__vho}], inplace=True)\n')
    if len(usecols) == 0:
        tyqvf__czhd += f'    T = None\n'
    else:
        tyqvf__czhd += f'    arrs = []\n'
        tyqvf__czhd += f'    for i in range(df.shape[1]):\n'
        tyqvf__czhd += f'      arrs.append(df.iloc[:, i].values)\n'
        tyqvf__czhd += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return tyqvf__czhd


def _gen_parallel_flag_name(sanitized_cnames):
    dni__nrx = '_parallel_value'
    while dni__nrx in sanitized_cnames:
        dni__nrx = '_' + dni__nrx
    return dni__nrx


def _gen_csv_reader_py(col_names, col_typs, usecols, out_used_cols, sep,
    parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(jhwrc__yurri) for jhwrc__yurri in
        col_names]
    tyqvf__czhd = 'def csv_reader_py(fname, nrows, skiprows):\n'
    tyqvf__czhd += _gen_csv_file_reader_init(parallel, header, compression,
        -1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    bsop__swj = globals()
    if idx_col_typ != types.none:
        bsop__swj[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        bsop__swj[f'table_type_{call_id}'] = types.none
    else:
        bsop__swj[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    tyqvf__czhd += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, out_used_cols, sep, escapechar, storage_options,
        call_id, bsop__swj, parallel=parallel, check_parallel_runtime=False,
        idx_col_index=idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        tyqvf__czhd += '  return (T, idx_arr)\n'
    else:
        tyqvf__czhd += '  return (T, None)\n'
    gyty__drx = {}
    bsop__swj['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(tyqvf__czhd, bsop__swj, gyty__drx)
    hwlb__irdvs = gyty__drx['csv_reader_py']
    zyw__evaa = numba.njit(hwlb__irdvs)
    compiled_funcs.append(zyw__evaa)
    return zyw__evaa
