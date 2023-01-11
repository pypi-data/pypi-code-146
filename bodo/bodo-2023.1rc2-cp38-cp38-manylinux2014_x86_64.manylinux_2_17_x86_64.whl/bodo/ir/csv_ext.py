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
    ads__yda = typemap[node.file_name.name]
    if types.unliteral(ads__yda) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {ads__yda}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        xzwak__yxtrp = typemap[node.skiprows.name]
        if isinstance(xzwak__yxtrp, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(xzwak__yxtrp, types.Integer) and not (isinstance
            (xzwak__yxtrp, (types.List, types.Tuple)) and isinstance(
            xzwak__yxtrp.dtype, types.Integer)) and not isinstance(xzwak__yxtrp
            , (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {xzwak__yxtrp}."
                , loc=node.skiprows.loc)
        elif isinstance(xzwak__yxtrp, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        vsoz__tzta = typemap[node.nrows.name]
        if not isinstance(vsoz__tzta, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {vsoz__tzta}."
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
        domlw__igwcw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(64),
            lir.IntType(1)])
        gxadv__vzsa = cgutils.get_or_insert_function(builder.module,
            domlw__igwcw, name='csv_file_chunk_reader')
        tvprs__ftf = builder.call(gxadv__vzsa, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        odwl__aenj = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        qad__qqqyj = context.get_python_api(builder)
        odwl__aenj.meminfo = qad__qqqyj.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), tvprs__ftf)
        odwl__aenj.pyobj = tvprs__ftf
        qad__qqqyj.decref(tvprs__ftf)
        return odwl__aenj._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.
        voidptr, types.int64, types.bool_, types.voidptr, types.voidptr,
        storage_options_dict_type, types.int64, types.bool_, types.int64,
        types.bool_), codegen


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        ecok__mize = csv_node.out_vars[0]
        if ecok__mize.name not in lives:
            return None
    else:
        eer__tgggw = csv_node.out_vars[0]
        neapx__dvkr = csv_node.out_vars[1]
        if eer__tgggw.name not in lives and neapx__dvkr.name not in lives:
            return None
        elif neapx__dvkr.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif eer__tgggw.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.out_used_cols = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    xzwak__yxtrp = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            ubw__ijbd = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            hgkt__vfd = csv_node.loc.strformat()
            wun__kfvrv = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', ubw__ijbd,
                hgkt__vfd, wun__kfvrv)
            ugwrc__nxxwh = csv_node.out_types[0].yield_type.data
            gnzg__mlkk = [bcgh__gls for lpesj__uqb, bcgh__gls in enumerate(
                csv_node.df_colnames) if isinstance(ugwrc__nxxwh[lpesj__uqb
                ], bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if gnzg__mlkk:
                ztgdj__ski = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    ztgdj__ski, hgkt__vfd, gnzg__mlkk)
        if array_dists is not None:
            uxpuk__xccyq = csv_node.out_vars[0].name
            parallel = array_dists[uxpuk__xccyq] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        okpvc__ityld = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        okpvc__ityld += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        okpvc__ityld += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        ernee__imuj = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(okpvc__ityld, {}, ernee__imuj)
        nsowa__bhsom = ernee__imuj['csv_iterator_impl']
        daf__hvfd = 'def csv_reader_init(fname, nrows, skiprows):\n'
        daf__hvfd += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        daf__hvfd += '  return f_reader\n'
        exec(daf__hvfd, globals(), ernee__imuj)
        eesvn__gtztb = ernee__imuj['csv_reader_init']
        ofou__yfc = numba.njit(eesvn__gtztb)
        compiled_funcs.append(ofou__yfc)
        fkpm__jyf = compile_to_numba_ir(nsowa__bhsom, {'_csv_reader_init':
            ofou__yfc, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, xzwak__yxtrp), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(fkpm__jyf, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        vxsl__drho = fkpm__jyf.body[:-3]
        vxsl__drho[-1].target = csv_node.out_vars[0]
        return vxsl__drho
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    okpvc__ityld = 'def csv_impl(fname, nrows, skiprows):\n'
    okpvc__ityld += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    ernee__imuj = {}
    exec(okpvc__ityld, {}, ernee__imuj)
    tfp__potd = ernee__imuj['csv_impl']
    sni__ucwor = csv_node.usecols
    if sni__ucwor:
        sni__ucwor = [csv_node.usecols[lpesj__uqb] for lpesj__uqb in
            csv_node.out_used_cols]
    if bodo.user_logging.get_verbose_level() >= 1:
        ubw__ijbd = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        hgkt__vfd = csv_node.loc.strformat()
        wun__kfvrv = []
        gnzg__mlkk = []
        if sni__ucwor:
            for lpesj__uqb in csv_node.out_used_cols:
                ubyvf__hgjn = csv_node.df_colnames[lpesj__uqb]
                wun__kfvrv.append(ubyvf__hgjn)
                if isinstance(csv_node.out_types[lpesj__uqb], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    gnzg__mlkk.append(ubyvf__hgjn)
        bodo.user_logging.log_message('Column Pruning', ubw__ijbd,
            hgkt__vfd, wun__kfvrv)
        if gnzg__mlkk:
            ztgdj__ski = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', ztgdj__ski,
                hgkt__vfd, gnzg__mlkk)
    ygzj__pfg = _gen_csv_reader_py(csv_node.df_colnames, csv_node.out_types,
        sni__ucwor, csv_node.out_used_cols, csv_node.sep, parallel,
        csv_node.header, csv_node.compression, csv_node.is_skiprows_list,
        csv_node.pd_low_memory, csv_node.escapechar, csv_node.
        storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    fkpm__jyf = compile_to_numba_ir(tfp__potd, {'_csv_reader_py': ygzj__pfg
        }, typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
        types.int64, xzwak__yxtrp), typemap=typemap, calltypes=calltypes
        ).blocks.popitem()[1]
    replace_arg_nodes(fkpm__jyf, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    vxsl__drho = fkpm__jyf.body[:-3]
    vxsl__drho[-1].target = csv_node.out_vars[1]
    vxsl__drho[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not sni__ucwor
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        vxsl__drho.pop(-1)
    elif not sni__ucwor:
        vxsl__drho.pop(-2)
    return vxsl__drho


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
    lle__sqg = t.dtype
    if isinstance(lle__sqg, PDCategoricalDtype):
        lxkab__vglf = CategoricalArrayType(lle__sqg)
        wiyi__sbk = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, wiyi__sbk, lxkab__vglf)
        return wiyi__sbk
    if lle__sqg == types.NPDatetime('ns'):
        lle__sqg = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        dfb__fyp = 'int_arr_{}'.format(lle__sqg)
        setattr(types, dfb__fyp, t)
        return dfb__fyp
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if lle__sqg == types.bool_:
        lle__sqg = 'bool_'
    if lle__sqg == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(lle__sqg, (
        StringArrayType, ArrayItemArrayType)):
        akd__ufdta = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, akd__ufdta, t)
        return akd__ufdta
    return '{}[::1]'.format(lle__sqg)


def _get_pd_dtype_str(t):
    lle__sqg = t.dtype
    if isinstance(lle__sqg, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(lle__sqg.categories)
    if lle__sqg == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type or t == bodo.dict_str_arr_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if lle__sqg.signed else 'U', lle__sqg.
            bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(lle__sqg, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(lle__sqg)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    njab__vqw = ''
    from collections import defaultdict
    xktzu__xyxpu = defaultdict(list)
    for gyrko__cgcf, dgqoh__gagu in typemap.items():
        xktzu__xyxpu[dgqoh__gagu].append(gyrko__cgcf)
    bov__qlk = df.columns.to_list()
    lbd__ufrl = []
    for dgqoh__gagu, xgmbm__hzbw in xktzu__xyxpu.items():
        try:
            lbd__ufrl.append(df.loc[:, xgmbm__hzbw].astype(dgqoh__gagu,
                copy=False))
            df = df.drop(xgmbm__hzbw, axis=1)
        except (ValueError, TypeError) as afe__ayry:
            njab__vqw = (
                f"Caught the runtime error '{afe__ayry}' on columns {xgmbm__hzbw}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    pgp__gmto = bool(njab__vqw)
    if parallel:
        uizyq__aywj = MPI.COMM_WORLD
        pgp__gmto = uizyq__aywj.allreduce(pgp__gmto, op=MPI.LOR)
    if pgp__gmto:
        cvhl__zax = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if njab__vqw:
            raise TypeError(f'{cvhl__zax}\n{njab__vqw}')
        else:
            raise TypeError(
                f'{cvhl__zax}\nPlease refer to errors on other ranks.')
    df = pd.concat(lbd__ufrl + [df], axis=1)
    qlt__wzvvz = df.loc[:, bov__qlk]
    return qlt__wzvvz


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    ettwb__bkzge = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        okpvc__ityld = '  skiprows = sorted(set(skiprows))\n'
    else:
        okpvc__ityld = '  skiprows = [skiprows]\n'
    okpvc__ityld += '  skiprows_list_len = len(skiprows)\n'
    okpvc__ityld += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    okpvc__ityld += '  check_java_installation(fname)\n'
    okpvc__ityld += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    okpvc__ityld += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    okpvc__ityld += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    okpvc__ityld += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, ettwb__bkzge, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    okpvc__ityld += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    okpvc__ityld += "      raise FileNotFoundError('File does not exist')\n"
    return okpvc__ityld


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    out_used_cols, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    cga__wobk = [str(lpesj__uqb) for lpesj__uqb, tumz__bkx in enumerate(
        usecols) if col_typs[out_used_cols[lpesj__uqb]].dtype == types.
        NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        cga__wobk.append(str(idx_col_index))
    gokg__rfd = ', '.join(cga__wobk)
    eyhjx__qua = _gen_parallel_flag_name(sanitized_cnames)
    opy__emj = f"{eyhjx__qua}='bool_'" if check_parallel_runtime else ''
    fgu__ltz = [_get_pd_dtype_str(col_typs[out_used_cols[lpesj__uqb]]) for
        lpesj__uqb in range(len(usecols))]
    bds__yjer = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    mtotc__ppxox = [tumz__bkx for lpesj__uqb, tumz__bkx in enumerate(
        usecols) if fgu__ltz[lpesj__uqb] == 'str']
    if idx_col_index is not None and bds__yjer == 'str':
        mtotc__ppxox.append(idx_col_index)
    ddtpb__tqae = np.array(mtotc__ppxox, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = ddtpb__tqae
    okpvc__ityld = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    vbrxz__uqs = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = vbrxz__uqs
    okpvc__ityld += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    xwpo__zgrtc = np.array(out_used_cols, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = xwpo__zgrtc
        okpvc__ityld += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    zyjg__vebq = defaultdict(list)
    for lpesj__uqb, tumz__bkx in enumerate(usecols):
        if fgu__ltz[lpesj__uqb] == 'str':
            continue
        zyjg__vebq[fgu__ltz[lpesj__uqb]].append(tumz__bkx)
    if idx_col_index is not None and bds__yjer != 'str':
        zyjg__vebq[bds__yjer].append(idx_col_index)
    for lpesj__uqb, ukhd__kdd in enumerate(zyjg__vebq.values()):
        glbs[f't_arr_{lpesj__uqb}_{call_id}'] = np.asarray(ukhd__kdd)
        okpvc__ityld += (
            f'  t_arr_{lpesj__uqb}_{call_id}_2 = t_arr_{lpesj__uqb}_{call_id}\n'
            )
    if idx_col_index != None:
        okpvc__ityld += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {opy__emj}):
"""
    else:
        okpvc__ityld += (
            f'  with objmode(T=table_type_{call_id}, {opy__emj}):\n')
    okpvc__ityld += f'    typemap = {{}}\n'
    for lpesj__uqb, nrur__lmblx in enumerate(zyjg__vebq.keys()):
        okpvc__ityld += f"""    typemap.update({{i:{nrur__lmblx} for i in t_arr_{lpesj__uqb}_{call_id}_2}})
"""
    okpvc__ityld += '    if f_reader.get_chunk_size() == 0:\n'
    okpvc__ityld += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    okpvc__ityld += '    else:\n'
    okpvc__ityld += '      df = pd.read_csv(f_reader,\n'
    okpvc__ityld += '        header=None,\n'
    okpvc__ityld += '        parse_dates=[{}],\n'.format(gokg__rfd)
    okpvc__ityld += (
        f"        dtype={{i:'string[pyarrow]' for i in str_col_nums_{call_id}_2}},\n"
        )
    okpvc__ityld += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        okpvc__ityld += f'    {eyhjx__qua} = f_reader.is_parallel()\n'
    else:
        okpvc__ityld += f'    {eyhjx__qua} = {parallel}\n'
    okpvc__ityld += f'    df = astype(df, typemap, {eyhjx__qua})\n'
    if idx_col_index != None:
        bzymd__lcgux = sorted(vbrxz__uqs).index(idx_col_index)
        okpvc__ityld += f'    idx_arr = df.iloc[:, {bzymd__lcgux}].values\n'
        okpvc__ityld += (
            f'    df.drop(columns=df.columns[{bzymd__lcgux}], inplace=True)\n')
    if len(usecols) == 0:
        okpvc__ityld += f'    T = None\n'
    else:
        okpvc__ityld += f'    arrs = []\n'
        okpvc__ityld += f'    for i in range(df.shape[1]):\n'
        okpvc__ityld += f'      arrs.append(df.iloc[:, i].values)\n'
        okpvc__ityld += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return okpvc__ityld


def _gen_parallel_flag_name(sanitized_cnames):
    eyhjx__qua = '_parallel_value'
    while eyhjx__qua in sanitized_cnames:
        eyhjx__qua = '_' + eyhjx__qua
    return eyhjx__qua


def _gen_csv_reader_py(col_names, col_typs, usecols, out_used_cols, sep,
    parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(bcgh__gls) for bcgh__gls in col_names]
    okpvc__ityld = 'def csv_reader_py(fname, nrows, skiprows):\n'
    okpvc__ityld += _gen_csv_file_reader_init(parallel, header, compression,
        -1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    evwu__lpby = globals()
    if idx_col_typ != types.none:
        evwu__lpby[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        evwu__lpby[f'table_type_{call_id}'] = types.none
    else:
        evwu__lpby[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    okpvc__ityld += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, out_used_cols, sep, escapechar, storage_options,
        call_id, evwu__lpby, parallel=parallel, check_parallel_runtime=
        False, idx_col_index=idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        okpvc__ityld += '  return (T, idx_arr)\n'
    else:
        okpvc__ityld += '  return (T, None)\n'
    ernee__imuj = {}
    evwu__lpby['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(okpvc__ityld, evwu__lpby, ernee__imuj)
    ygzj__pfg = ernee__imuj['csv_reader_py']
    ofou__yfc = numba.njit(ygzj__pfg)
    compiled_funcs.append(ofou__yfc)
    return ofou__yfc
