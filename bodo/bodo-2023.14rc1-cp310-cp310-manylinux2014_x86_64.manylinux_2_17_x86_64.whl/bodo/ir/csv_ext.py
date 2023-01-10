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
    ytlxy__ohzxt = typemap[node.file_name.name]
    if types.unliteral(ytlxy__ohzxt) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {ytlxy__ohzxt}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        bmric__kltu = typemap[node.skiprows.name]
        if isinstance(bmric__kltu, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(bmric__kltu, types.Integer) and not (isinstance
            (bmric__kltu, (types.List, types.Tuple)) and isinstance(
            bmric__kltu.dtype, types.Integer)) and not isinstance(bmric__kltu,
            (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {bmric__kltu}."
                , loc=node.skiprows.loc)
        elif isinstance(bmric__kltu, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        pfswo__kntq = typemap[node.nrows.name]
        if not isinstance(pfswo__kntq, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {pfswo__kntq}."
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
        zrs__xyf = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(64),
            lir.IntType(1)])
        blor__shxb = cgutils.get_or_insert_function(builder.module,
            zrs__xyf, name='csv_file_chunk_reader')
        ypwwn__ukhug = builder.call(blor__shxb, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        knvv__gml = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        fwb__jtlnp = context.get_python_api(builder)
        knvv__gml.meminfo = fwb__jtlnp.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), ypwwn__ukhug)
        knvv__gml.pyobj = ypwwn__ukhug
        fwb__jtlnp.decref(ypwwn__ukhug)
        return knvv__gml._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.
        voidptr, types.int64, types.bool_, types.voidptr, types.voidptr,
        storage_options_dict_type, types.int64, types.bool_, types.int64,
        types.bool_), codegen


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        rvb__tuklm = csv_node.out_vars[0]
        if rvb__tuklm.name not in lives:
            return None
    else:
        dhzkk__jky = csv_node.out_vars[0]
        wmyjl__qwb = csv_node.out_vars[1]
        if dhzkk__jky.name not in lives and wmyjl__qwb.name not in lives:
            return None
        elif wmyjl__qwb.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif dhzkk__jky.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.out_used_cols = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    bmric__kltu = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            carbu__pml = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            nees__ottn = csv_node.loc.strformat()
            pnhcx__jjr = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', carbu__pml,
                nees__ottn, pnhcx__jjr)
            hsy__gwfc = csv_node.out_types[0].yield_type.data
            qto__mznh = [rtl__ajzqg for xvfu__gdxvx, rtl__ajzqg in
                enumerate(csv_node.df_colnames) if isinstance(hsy__gwfc[
                xvfu__gdxvx], bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if qto__mznh:
                sagrv__uejy = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    sagrv__uejy, nees__ottn, qto__mznh)
        if array_dists is not None:
            vvbw__hwopc = csv_node.out_vars[0].name
            parallel = array_dists[vvbw__hwopc] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        zlm__fathn = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        zlm__fathn += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        zlm__fathn += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        gqj__znhps = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(zlm__fathn, {}, gqj__znhps)
        oxev__tybel = gqj__znhps['csv_iterator_impl']
        muu__miep = 'def csv_reader_init(fname, nrows, skiprows):\n'
        muu__miep += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        muu__miep += '  return f_reader\n'
        exec(muu__miep, globals(), gqj__znhps)
        wymqp__zek = gqj__znhps['csv_reader_init']
        hpy__cych = numba.njit(wymqp__zek)
        compiled_funcs.append(hpy__cych)
        wnm__lpnl = compile_to_numba_ir(oxev__tybel, {'_csv_reader_init':
            hpy__cych, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, bmric__kltu), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(wnm__lpnl, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        grtly__imff = wnm__lpnl.body[:-3]
        grtly__imff[-1].target = csv_node.out_vars[0]
        return grtly__imff
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    zlm__fathn = 'def csv_impl(fname, nrows, skiprows):\n'
    zlm__fathn += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    gqj__znhps = {}
    exec(zlm__fathn, {}, gqj__znhps)
    zvc__srfm = gqj__znhps['csv_impl']
    loxqc__kzgkb = csv_node.usecols
    if loxqc__kzgkb:
        loxqc__kzgkb = [csv_node.usecols[xvfu__gdxvx] for xvfu__gdxvx in
            csv_node.out_used_cols]
    if bodo.user_logging.get_verbose_level() >= 1:
        carbu__pml = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        nees__ottn = csv_node.loc.strformat()
        pnhcx__jjr = []
        qto__mznh = []
        if loxqc__kzgkb:
            for xvfu__gdxvx in csv_node.out_used_cols:
                stsv__ipr = csv_node.df_colnames[xvfu__gdxvx]
                pnhcx__jjr.append(stsv__ipr)
                if isinstance(csv_node.out_types[xvfu__gdxvx], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    qto__mznh.append(stsv__ipr)
        bodo.user_logging.log_message('Column Pruning', carbu__pml,
            nees__ottn, pnhcx__jjr)
        if qto__mznh:
            sagrv__uejy = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                sagrv__uejy, nees__ottn, qto__mznh)
    hudjg__abe = _gen_csv_reader_py(csv_node.df_colnames, csv_node.
        out_types, loxqc__kzgkb, csv_node.out_used_cols, csv_node.sep,
        parallel, csv_node.header, csv_node.compression, csv_node.
        is_skiprows_list, csv_node.pd_low_memory, csv_node.escapechar,
        csv_node.storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    wnm__lpnl = compile_to_numba_ir(zvc__srfm, {'_csv_reader_py':
        hudjg__abe}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, bmric__kltu), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(wnm__lpnl, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    grtly__imff = wnm__lpnl.body[:-3]
    grtly__imff[-1].target = csv_node.out_vars[1]
    grtly__imff[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not loxqc__kzgkb
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        grtly__imff.pop(-1)
    elif not loxqc__kzgkb:
        grtly__imff.pop(-2)
    return grtly__imff


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
    nxz__widxn = t.dtype
    if isinstance(nxz__widxn, PDCategoricalDtype):
        ikrl__fvrd = CategoricalArrayType(nxz__widxn)
        pha__yakxd = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, pha__yakxd, ikrl__fvrd)
        return pha__yakxd
    if nxz__widxn == types.NPDatetime('ns'):
        nxz__widxn = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        bonqk__ksb = 'int_arr_{}'.format(nxz__widxn)
        setattr(types, bonqk__ksb, t)
        return bonqk__ksb
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if nxz__widxn == types.bool_:
        nxz__widxn = 'bool_'
    if nxz__widxn == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(nxz__widxn, (
        StringArrayType, ArrayItemArrayType)):
        tiwfj__ckk = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, tiwfj__ckk, t)
        return tiwfj__ckk
    return '{}[::1]'.format(nxz__widxn)


def _get_pd_dtype_str(t):
    nxz__widxn = t.dtype
    if isinstance(nxz__widxn, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(nxz__widxn.categories)
    if nxz__widxn == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type or t == bodo.dict_str_arr_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if nxz__widxn.signed else 'U',
            nxz__widxn.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(nxz__widxn, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(nxz__widxn)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    xvy__ckz = ''
    from collections import defaultdict
    wpw__dyoq = defaultdict(list)
    for hwdev__qvx, vbuq__rhazl in typemap.items():
        wpw__dyoq[vbuq__rhazl].append(hwdev__qvx)
    dhzdg__arw = df.columns.to_list()
    bbg__licrx = []
    for vbuq__rhazl, qzgdl__srqus in wpw__dyoq.items():
        try:
            bbg__licrx.append(df.loc[:, qzgdl__srqus].astype(vbuq__rhazl,
                copy=False))
            df = df.drop(qzgdl__srqus, axis=1)
        except (ValueError, TypeError) as tuhck__amz:
            xvy__ckz = (
                f"Caught the runtime error '{tuhck__amz}' on columns {qzgdl__srqus}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    sxlq__mkpm = bool(xvy__ckz)
    if parallel:
        zkiu__wvyd = MPI.COMM_WORLD
        sxlq__mkpm = zkiu__wvyd.allreduce(sxlq__mkpm, op=MPI.LOR)
    if sxlq__mkpm:
        olnw__ieh = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if xvy__ckz:
            raise TypeError(f'{olnw__ieh}\n{xvy__ckz}')
        else:
            raise TypeError(
                f'{olnw__ieh}\nPlease refer to errors on other ranks.')
    df = pd.concat(bbg__licrx + [df], axis=1)
    ypb__nwty = df.loc[:, dhzdg__arw]
    return ypb__nwty


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    nwn__rbaxl = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        zlm__fathn = '  skiprows = sorted(set(skiprows))\n'
    else:
        zlm__fathn = '  skiprows = [skiprows]\n'
    zlm__fathn += '  skiprows_list_len = len(skiprows)\n'
    zlm__fathn += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    zlm__fathn += '  check_java_installation(fname)\n'
    zlm__fathn += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    zlm__fathn += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    zlm__fathn += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    zlm__fathn += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, nwn__rbaxl, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    zlm__fathn += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    zlm__fathn += "      raise FileNotFoundError('File does not exist')\n"
    return zlm__fathn


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    out_used_cols, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    vmyr__bvj = [str(xvfu__gdxvx) for xvfu__gdxvx, ebi__hsi in enumerate(
        usecols) if col_typs[out_used_cols[xvfu__gdxvx]].dtype == types.
        NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        vmyr__bvj.append(str(idx_col_index))
    mxq__fkjts = ', '.join(vmyr__bvj)
    zza__zlg = _gen_parallel_flag_name(sanitized_cnames)
    qnsfl__jga = f"{zza__zlg}='bool_'" if check_parallel_runtime else ''
    xuk__fkag = [_get_pd_dtype_str(col_typs[out_used_cols[xvfu__gdxvx]]) for
        xvfu__gdxvx in range(len(usecols))]
    uvk__vwisk = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    ldt__yge = [ebi__hsi for xvfu__gdxvx, ebi__hsi in enumerate(usecols) if
        xuk__fkag[xvfu__gdxvx] == 'str']
    if idx_col_index is not None and uvk__vwisk == 'str':
        ldt__yge.append(idx_col_index)
    allnd__nxp = np.array(ldt__yge, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = allnd__nxp
    zlm__fathn = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    quqrs__ddey = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = quqrs__ddey
    zlm__fathn += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    ljj__lulu = np.array(out_used_cols, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = ljj__lulu
        zlm__fathn += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    kvr__ynw = defaultdict(list)
    for xvfu__gdxvx, ebi__hsi in enumerate(usecols):
        if xuk__fkag[xvfu__gdxvx] == 'str':
            continue
        kvr__ynw[xuk__fkag[xvfu__gdxvx]].append(ebi__hsi)
    if idx_col_index is not None and uvk__vwisk != 'str':
        kvr__ynw[uvk__vwisk].append(idx_col_index)
    for xvfu__gdxvx, nod__ssg in enumerate(kvr__ynw.values()):
        glbs[f't_arr_{xvfu__gdxvx}_{call_id}'] = np.asarray(nod__ssg)
        zlm__fathn += (
            f'  t_arr_{xvfu__gdxvx}_{call_id}_2 = t_arr_{xvfu__gdxvx}_{call_id}\n'
            )
    if idx_col_index != None:
        zlm__fathn += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {qnsfl__jga}):
"""
    else:
        zlm__fathn += (
            f'  with objmode(T=table_type_{call_id}, {qnsfl__jga}):\n')
    zlm__fathn += f'    typemap = {{}}\n'
    for xvfu__gdxvx, ajgr__dao in enumerate(kvr__ynw.keys()):
        zlm__fathn += f"""    typemap.update({{i:{ajgr__dao} for i in t_arr_{xvfu__gdxvx}_{call_id}_2}})
"""
    zlm__fathn += '    if f_reader.get_chunk_size() == 0:\n'
    zlm__fathn += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    zlm__fathn += '    else:\n'
    zlm__fathn += '      df = pd.read_csv(f_reader,\n'
    zlm__fathn += '        header=None,\n'
    zlm__fathn += '        parse_dates=[{}],\n'.format(mxq__fkjts)
    zlm__fathn += (
        f"        dtype={{i:'string[pyarrow]' for i in str_col_nums_{call_id}_2}},\n"
        )
    zlm__fathn += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        zlm__fathn += f'    {zza__zlg} = f_reader.is_parallel()\n'
    else:
        zlm__fathn += f'    {zza__zlg} = {parallel}\n'
    zlm__fathn += f'    df = astype(df, typemap, {zza__zlg})\n'
    if idx_col_index != None:
        jknft__mvtju = sorted(quqrs__ddey).index(idx_col_index)
        zlm__fathn += f'    idx_arr = df.iloc[:, {jknft__mvtju}].values\n'
        zlm__fathn += (
            f'    df.drop(columns=df.columns[{jknft__mvtju}], inplace=True)\n')
    if len(usecols) == 0:
        zlm__fathn += f'    T = None\n'
    else:
        zlm__fathn += f'    arrs = []\n'
        zlm__fathn += f'    for i in range(df.shape[1]):\n'
        zlm__fathn += f'      arrs.append(df.iloc[:, i].values)\n'
        zlm__fathn += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return zlm__fathn


def _gen_parallel_flag_name(sanitized_cnames):
    zza__zlg = '_parallel_value'
    while zza__zlg in sanitized_cnames:
        zza__zlg = '_' + zza__zlg
    return zza__zlg


def _gen_csv_reader_py(col_names, col_typs, usecols, out_used_cols, sep,
    parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(rtl__ajzqg) for rtl__ajzqg in
        col_names]
    zlm__fathn = 'def csv_reader_py(fname, nrows, skiprows):\n'
    zlm__fathn += _gen_csv_file_reader_init(parallel, header, compression, 
        -1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    nfd__gnym = globals()
    if idx_col_typ != types.none:
        nfd__gnym[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        nfd__gnym[f'table_type_{call_id}'] = types.none
    else:
        nfd__gnym[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    zlm__fathn += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, out_used_cols, sep, escapechar, storage_options,
        call_id, nfd__gnym, parallel=parallel, check_parallel_runtime=False,
        idx_col_index=idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        zlm__fathn += '  return (T, idx_arr)\n'
    else:
        zlm__fathn += '  return (T, None)\n'
    gqj__znhps = {}
    nfd__gnym['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(zlm__fathn, nfd__gnym, gqj__znhps)
    hudjg__abe = gqj__znhps['csv_reader_py']
    hpy__cych = numba.njit(hudjg__abe)
    compiled_funcs.append(hpy__cych)
    return hpy__cych
