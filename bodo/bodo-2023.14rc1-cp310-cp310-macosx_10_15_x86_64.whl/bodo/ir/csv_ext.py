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
    qvdq__thk = typemap[node.file_name.name]
    if types.unliteral(qvdq__thk) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {qvdq__thk}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        tpdx__mupq = typemap[node.skiprows.name]
        if isinstance(tpdx__mupq, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(tpdx__mupq, types.Integer) and not (isinstance(
            tpdx__mupq, (types.List, types.Tuple)) and isinstance(
            tpdx__mupq.dtype, types.Integer)) and not isinstance(tpdx__mupq,
            (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {tpdx__mupq}."
                , loc=node.skiprows.loc)
        elif isinstance(tpdx__mupq, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        cmgwo__art = typemap[node.nrows.name]
        if not isinstance(cmgwo__art, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {cmgwo__art}."
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
        mcf__founz = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(64),
            lir.IntType(1)])
        jzb__ktjlf = cgutils.get_or_insert_function(builder.module,
            mcf__founz, name='csv_file_chunk_reader')
        qmch__ljv = builder.call(jzb__ktjlf, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        cfhbp__adrf = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        gpzh__bsn = context.get_python_api(builder)
        cfhbp__adrf.meminfo = gpzh__bsn.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), qmch__ljv)
        cfhbp__adrf.pyobj = qmch__ljv
        gpzh__bsn.decref(qmch__ljv)
        return cfhbp__adrf._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.
        voidptr, types.int64, types.bool_, types.voidptr, types.voidptr,
        storage_options_dict_type, types.int64, types.bool_, types.int64,
        types.bool_), codegen


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        liip__eviw = csv_node.out_vars[0]
        if liip__eviw.name not in lives:
            return None
    else:
        njhx__qbnq = csv_node.out_vars[0]
        qxovc__hvr = csv_node.out_vars[1]
        if njhx__qbnq.name not in lives and qxovc__hvr.name not in lives:
            return None
        elif qxovc__hvr.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif njhx__qbnq.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.out_used_cols = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    tpdx__mupq = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            yuyfb__tbgha = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            ubam__wbwew = csv_node.loc.strformat()
            gvauc__aut = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', yuyfb__tbgha,
                ubam__wbwew, gvauc__aut)
            qcvt__pwxr = csv_node.out_types[0].yield_type.data
            krnp__iet = [prty__hitd for yppz__frzbt, prty__hitd in
                enumerate(csv_node.df_colnames) if isinstance(qcvt__pwxr[
                yppz__frzbt], bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if krnp__iet:
                ydvwz__eyvfg = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    ydvwz__eyvfg, ubam__wbwew, krnp__iet)
        if array_dists is not None:
            gztl__hicc = csv_node.out_vars[0].name
            parallel = array_dists[gztl__hicc] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        xqta__boob = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        xqta__boob += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        xqta__boob += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        zfqk__qoie = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(xqta__boob, {}, zfqk__qoie)
        yvt__ulle = zfqk__qoie['csv_iterator_impl']
        kfnha__qus = 'def csv_reader_init(fname, nrows, skiprows):\n'
        kfnha__qus += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        kfnha__qus += '  return f_reader\n'
        exec(kfnha__qus, globals(), zfqk__qoie)
        ixten__apmbe = zfqk__qoie['csv_reader_init']
        dheix__rgc = numba.njit(ixten__apmbe)
        compiled_funcs.append(dheix__rgc)
        wovi__uwlwq = compile_to_numba_ir(yvt__ulle, {'_csv_reader_init':
            dheix__rgc, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, tpdx__mupq), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(wovi__uwlwq, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        pbajy__jgjq = wovi__uwlwq.body[:-3]
        pbajy__jgjq[-1].target = csv_node.out_vars[0]
        return pbajy__jgjq
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    xqta__boob = 'def csv_impl(fname, nrows, skiprows):\n'
    xqta__boob += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    zfqk__qoie = {}
    exec(xqta__boob, {}, zfqk__qoie)
    bfl__rmzm = zfqk__qoie['csv_impl']
    sdq__igq = csv_node.usecols
    if sdq__igq:
        sdq__igq = [csv_node.usecols[yppz__frzbt] for yppz__frzbt in
            csv_node.out_used_cols]
    if bodo.user_logging.get_verbose_level() >= 1:
        yuyfb__tbgha = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        ubam__wbwew = csv_node.loc.strformat()
        gvauc__aut = []
        krnp__iet = []
        if sdq__igq:
            for yppz__frzbt in csv_node.out_used_cols:
                btbf__bauzn = csv_node.df_colnames[yppz__frzbt]
                gvauc__aut.append(btbf__bauzn)
                if isinstance(csv_node.out_types[yppz__frzbt], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    krnp__iet.append(btbf__bauzn)
        bodo.user_logging.log_message('Column Pruning', yuyfb__tbgha,
            ubam__wbwew, gvauc__aut)
        if krnp__iet:
            ydvwz__eyvfg = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                ydvwz__eyvfg, ubam__wbwew, krnp__iet)
    kll__atnj = _gen_csv_reader_py(csv_node.df_colnames, csv_node.out_types,
        sdq__igq, csv_node.out_used_cols, csv_node.sep, parallel, csv_node.
        header, csv_node.compression, csv_node.is_skiprows_list, csv_node.
        pd_low_memory, csv_node.escapechar, csv_node.storage_options,
        idx_col_index=csv_node.index_column_index, idx_col_typ=csv_node.
        index_column_typ)
    wovi__uwlwq = compile_to_numba_ir(bfl__rmzm, {'_csv_reader_py':
        kll__atnj}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, tpdx__mupq), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(wovi__uwlwq, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    pbajy__jgjq = wovi__uwlwq.body[:-3]
    pbajy__jgjq[-1].target = csv_node.out_vars[1]
    pbajy__jgjq[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not sdq__igq
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        pbajy__jgjq.pop(-1)
    elif not sdq__igq:
        pbajy__jgjq.pop(-2)
    return pbajy__jgjq


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
    cheeh__olfja = t.dtype
    if isinstance(cheeh__olfja, PDCategoricalDtype):
        uvtcu__mpgyv = CategoricalArrayType(cheeh__olfja)
        pjil__qccua = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, pjil__qccua, uvtcu__mpgyv)
        return pjil__qccua
    if cheeh__olfja == types.NPDatetime('ns'):
        cheeh__olfja = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        quf__jgoir = 'int_arr_{}'.format(cheeh__olfja)
        setattr(types, quf__jgoir, t)
        return quf__jgoir
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if cheeh__olfja == types.bool_:
        cheeh__olfja = 'bool_'
    if cheeh__olfja == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(cheeh__olfja, (
        StringArrayType, ArrayItemArrayType)):
        rrppy__gby = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, rrppy__gby, t)
        return rrppy__gby
    return '{}[::1]'.format(cheeh__olfja)


def _get_pd_dtype_str(t):
    cheeh__olfja = t.dtype
    if isinstance(cheeh__olfja, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(cheeh__olfja.categories)
    if cheeh__olfja == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type or t == bodo.dict_str_arr_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if cheeh__olfja.signed else 'U',
            cheeh__olfja.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(cheeh__olfja, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(cheeh__olfja)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    xkk__jgjx = ''
    from collections import defaultdict
    soe__ifp = defaultdict(list)
    for afmd__uvffc, jult__pjae in typemap.items():
        soe__ifp[jult__pjae].append(afmd__uvffc)
    bse__pxxwz = df.columns.to_list()
    jgkue__pny = []
    for jult__pjae, xxera__xqytm in soe__ifp.items():
        try:
            jgkue__pny.append(df.loc[:, xxera__xqytm].astype(jult__pjae,
                copy=False))
            df = df.drop(xxera__xqytm, axis=1)
        except (ValueError, TypeError) as uke__dny:
            xkk__jgjx = (
                f"Caught the runtime error '{uke__dny}' on columns {xxera__xqytm}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    enqhs__btl = bool(xkk__jgjx)
    if parallel:
        lpyd__bbdp = MPI.COMM_WORLD
        enqhs__btl = lpyd__bbdp.allreduce(enqhs__btl, op=MPI.LOR)
    if enqhs__btl:
        niybr__xijg = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if xkk__jgjx:
            raise TypeError(f'{niybr__xijg}\n{xkk__jgjx}')
        else:
            raise TypeError(
                f'{niybr__xijg}\nPlease refer to errors on other ranks.')
    df = pd.concat(jgkue__pny + [df], axis=1)
    jkog__llo = df.loc[:, bse__pxxwz]
    return jkog__llo


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    wue__mwv = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        xqta__boob = '  skiprows = sorted(set(skiprows))\n'
    else:
        xqta__boob = '  skiprows = [skiprows]\n'
    xqta__boob += '  skiprows_list_len = len(skiprows)\n'
    xqta__boob += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    xqta__boob += '  check_java_installation(fname)\n'
    xqta__boob += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    xqta__boob += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    xqta__boob += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    xqta__boob += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, wue__mwv, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    xqta__boob += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    xqta__boob += "      raise FileNotFoundError('File does not exist')\n"
    return xqta__boob


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    out_used_cols, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    xfrp__lxld = [str(yppz__frzbt) for yppz__frzbt, fxp__xxt in enumerate(
        usecols) if col_typs[out_used_cols[yppz__frzbt]].dtype == types.
        NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        xfrp__lxld.append(str(idx_col_index))
    jltze__zgpbu = ', '.join(xfrp__lxld)
    wlvs__jghc = _gen_parallel_flag_name(sanitized_cnames)
    ptkse__hsc = f"{wlvs__jghc}='bool_'" if check_parallel_runtime else ''
    efwm__kjzx = [_get_pd_dtype_str(col_typs[out_used_cols[yppz__frzbt]]) for
        yppz__frzbt in range(len(usecols))]
    bsed__esrnl = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    zgnoc__hhhzf = [fxp__xxt for yppz__frzbt, fxp__xxt in enumerate(usecols
        ) if efwm__kjzx[yppz__frzbt] == 'str']
    if idx_col_index is not None and bsed__esrnl == 'str':
        zgnoc__hhhzf.append(idx_col_index)
    lhou__mzzda = np.array(zgnoc__hhhzf, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = lhou__mzzda
    xqta__boob = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    hhvdu__lebv = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = hhvdu__lebv
    xqta__boob += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    gzvi__odizo = np.array(out_used_cols, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = gzvi__odizo
        xqta__boob += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    kjhkv__izk = defaultdict(list)
    for yppz__frzbt, fxp__xxt in enumerate(usecols):
        if efwm__kjzx[yppz__frzbt] == 'str':
            continue
        kjhkv__izk[efwm__kjzx[yppz__frzbt]].append(fxp__xxt)
    if idx_col_index is not None and bsed__esrnl != 'str':
        kjhkv__izk[bsed__esrnl].append(idx_col_index)
    for yppz__frzbt, fiffd__avdn in enumerate(kjhkv__izk.values()):
        glbs[f't_arr_{yppz__frzbt}_{call_id}'] = np.asarray(fiffd__avdn)
        xqta__boob += (
            f'  t_arr_{yppz__frzbt}_{call_id}_2 = t_arr_{yppz__frzbt}_{call_id}\n'
            )
    if idx_col_index != None:
        xqta__boob += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {ptkse__hsc}):
"""
    else:
        xqta__boob += (
            f'  with objmode(T=table_type_{call_id}, {ptkse__hsc}):\n')
    xqta__boob += f'    typemap = {{}}\n'
    for yppz__frzbt, tctb__fosmw in enumerate(kjhkv__izk.keys()):
        xqta__boob += f"""    typemap.update({{i:{tctb__fosmw} for i in t_arr_{yppz__frzbt}_{call_id}_2}})
"""
    xqta__boob += '    if f_reader.get_chunk_size() == 0:\n'
    xqta__boob += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    xqta__boob += '    else:\n'
    xqta__boob += '      df = pd.read_csv(f_reader,\n'
    xqta__boob += '        header=None,\n'
    xqta__boob += '        parse_dates=[{}],\n'.format(jltze__zgpbu)
    xqta__boob += (
        f"        dtype={{i:'string[pyarrow]' for i in str_col_nums_{call_id}_2}},\n"
        )
    xqta__boob += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        xqta__boob += f'    {wlvs__jghc} = f_reader.is_parallel()\n'
    else:
        xqta__boob += f'    {wlvs__jghc} = {parallel}\n'
    xqta__boob += f'    df = astype(df, typemap, {wlvs__jghc})\n'
    if idx_col_index != None:
        phwj__sskv = sorted(hhvdu__lebv).index(idx_col_index)
        xqta__boob += f'    idx_arr = df.iloc[:, {phwj__sskv}].values\n'
        xqta__boob += (
            f'    df.drop(columns=df.columns[{phwj__sskv}], inplace=True)\n')
    if len(usecols) == 0:
        xqta__boob += f'    T = None\n'
    else:
        xqta__boob += f'    arrs = []\n'
        xqta__boob += f'    for i in range(df.shape[1]):\n'
        xqta__boob += f'      arrs.append(df.iloc[:, i].values)\n'
        xqta__boob += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return xqta__boob


def _gen_parallel_flag_name(sanitized_cnames):
    wlvs__jghc = '_parallel_value'
    while wlvs__jghc in sanitized_cnames:
        wlvs__jghc = '_' + wlvs__jghc
    return wlvs__jghc


def _gen_csv_reader_py(col_names, col_typs, usecols, out_used_cols, sep,
    parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(prty__hitd) for prty__hitd in
        col_names]
    xqta__boob = 'def csv_reader_py(fname, nrows, skiprows):\n'
    xqta__boob += _gen_csv_file_reader_init(parallel, header, compression, 
        -1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    ydg__ozh = globals()
    if idx_col_typ != types.none:
        ydg__ozh[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        ydg__ozh[f'table_type_{call_id}'] = types.none
    else:
        ydg__ozh[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    xqta__boob += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, out_used_cols, sep, escapechar, storage_options,
        call_id, ydg__ozh, parallel=parallel, check_parallel_runtime=False,
        idx_col_index=idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        xqta__boob += '  return (T, idx_arr)\n'
    else:
        xqta__boob += '  return (T, None)\n'
    zfqk__qoie = {}
    ydg__ozh['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(xqta__boob, ydg__ozh, zfqk__qoie)
    kll__atnj = zfqk__qoie['csv_reader_py']
    dheix__rgc = numba.njit(kll__atnj)
    compiled_funcs.append(dheix__rgc)
    return dheix__rgc
