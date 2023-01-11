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
    zfd__gjgow = typemap[node.file_name.name]
    if types.unliteral(zfd__gjgow) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {zfd__gjgow}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        sitd__xno = typemap[node.skiprows.name]
        if isinstance(sitd__xno, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(sitd__xno, types.Integer) and not (isinstance(
            sitd__xno, (types.List, types.Tuple)) and isinstance(sitd__xno.
            dtype, types.Integer)) and not isinstance(sitd__xno, (types.
            LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {sitd__xno}."
                , loc=node.skiprows.loc)
        elif isinstance(sitd__xno, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        ezat__pgbls = typemap[node.nrows.name]
        if not isinstance(ezat__pgbls, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {ezat__pgbls}."
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
        hxib__lqzik = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(64),
            lir.IntType(1)])
        rpd__fmhi = cgutils.get_or_insert_function(builder.module,
            hxib__lqzik, name='csv_file_chunk_reader')
        uffbj__kgp = builder.call(rpd__fmhi, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        ogk__ada = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        qyhut__myzdl = context.get_python_api(builder)
        ogk__ada.meminfo = qyhut__myzdl.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), uffbj__kgp)
        ogk__ada.pyobj = uffbj__kgp
        qyhut__myzdl.decref(uffbj__kgp)
        return ogk__ada._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.
        voidptr, types.int64, types.bool_, types.voidptr, types.voidptr,
        storage_options_dict_type, types.int64, types.bool_, types.int64,
        types.bool_), codegen


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        gpsvj__who = csv_node.out_vars[0]
        if gpsvj__who.name not in lives:
            return None
    else:
        xdkkd__ssgum = csv_node.out_vars[0]
        rmj__ellh = csv_node.out_vars[1]
        if xdkkd__ssgum.name not in lives and rmj__ellh.name not in lives:
            return None
        elif rmj__ellh.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif xdkkd__ssgum.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.out_used_cols = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    sitd__xno = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            bjde__ynjch = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            vinp__uls = csv_node.loc.strformat()
            apz__pzodb = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', bjde__ynjch,
                vinp__uls, apz__pzodb)
            ofsq__chn = csv_node.out_types[0].yield_type.data
            smua__kdb = [qyoa__zabf for ddphc__aqc, qyoa__zabf in enumerate
                (csv_node.df_colnames) if isinstance(ofsq__chn[ddphc__aqc],
                bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if smua__kdb:
                ubqwm__ulkoe = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    ubqwm__ulkoe, vinp__uls, smua__kdb)
        if array_dists is not None:
            slvjb__guvf = csv_node.out_vars[0].name
            parallel = array_dists[slvjb__guvf] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        rvpu__goh = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        rvpu__goh += f'    reader = _csv_reader_init(fname, nrows, skiprows)\n'
        rvpu__goh += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        kbms__aass = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(rvpu__goh, {}, kbms__aass)
        yeiq__uoa = kbms__aass['csv_iterator_impl']
        ihtli__fku = 'def csv_reader_init(fname, nrows, skiprows):\n'
        ihtli__fku += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        ihtli__fku += '  return f_reader\n'
        exec(ihtli__fku, globals(), kbms__aass)
        tlfxo__hhym = kbms__aass['csv_reader_init']
        rij__ehnf = numba.njit(tlfxo__hhym)
        compiled_funcs.append(rij__ehnf)
        valfz__xfemj = compile_to_numba_ir(yeiq__uoa, {'_csv_reader_init':
            rij__ehnf, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, sitd__xno), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(valfz__xfemj, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        bpsjo__mldf = valfz__xfemj.body[:-3]
        bpsjo__mldf[-1].target = csv_node.out_vars[0]
        return bpsjo__mldf
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    rvpu__goh = 'def csv_impl(fname, nrows, skiprows):\n'
    rvpu__goh += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    kbms__aass = {}
    exec(rvpu__goh, {}, kbms__aass)
    jdfa__nnba = kbms__aass['csv_impl']
    mctxo__qpkh = csv_node.usecols
    if mctxo__qpkh:
        mctxo__qpkh = [csv_node.usecols[ddphc__aqc] for ddphc__aqc in
            csv_node.out_used_cols]
    if bodo.user_logging.get_verbose_level() >= 1:
        bjde__ynjch = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        vinp__uls = csv_node.loc.strformat()
        apz__pzodb = []
        smua__kdb = []
        if mctxo__qpkh:
            for ddphc__aqc in csv_node.out_used_cols:
                brs__guogn = csv_node.df_colnames[ddphc__aqc]
                apz__pzodb.append(brs__guogn)
                if isinstance(csv_node.out_types[ddphc__aqc], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    smua__kdb.append(brs__guogn)
        bodo.user_logging.log_message('Column Pruning', bjde__ynjch,
            vinp__uls, apz__pzodb)
        if smua__kdb:
            ubqwm__ulkoe = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                ubqwm__ulkoe, vinp__uls, smua__kdb)
    yxy__juywg = _gen_csv_reader_py(csv_node.df_colnames, csv_node.
        out_types, mctxo__qpkh, csv_node.out_used_cols, csv_node.sep,
        parallel, csv_node.header, csv_node.compression, csv_node.
        is_skiprows_list, csv_node.pd_low_memory, csv_node.escapechar,
        csv_node.storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    valfz__xfemj = compile_to_numba_ir(jdfa__nnba, {'_csv_reader_py':
        yxy__juywg}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, sitd__xno), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(valfz__xfemj, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    bpsjo__mldf = valfz__xfemj.body[:-3]
    bpsjo__mldf[-1].target = csv_node.out_vars[1]
    bpsjo__mldf[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not mctxo__qpkh
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        bpsjo__mldf.pop(-1)
    elif not mctxo__qpkh:
        bpsjo__mldf.pop(-2)
    return bpsjo__mldf


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
    vbuu__mrcoy = t.dtype
    if isinstance(vbuu__mrcoy, PDCategoricalDtype):
        vjklq__pon = CategoricalArrayType(vbuu__mrcoy)
        bkxdv__kfe = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, bkxdv__kfe, vjklq__pon)
        return bkxdv__kfe
    if vbuu__mrcoy == types.NPDatetime('ns'):
        vbuu__mrcoy = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        kimoy__dihk = 'int_arr_{}'.format(vbuu__mrcoy)
        setattr(types, kimoy__dihk, t)
        return kimoy__dihk
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if vbuu__mrcoy == types.bool_:
        vbuu__mrcoy = 'bool_'
    if vbuu__mrcoy == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(vbuu__mrcoy, (
        StringArrayType, ArrayItemArrayType)):
        pcc__xyq = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, pcc__xyq, t)
        return pcc__xyq
    return '{}[::1]'.format(vbuu__mrcoy)


def _get_pd_dtype_str(t):
    vbuu__mrcoy = t.dtype
    if isinstance(vbuu__mrcoy, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(vbuu__mrcoy.categories)
    if vbuu__mrcoy == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type or t == bodo.dict_str_arr_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if vbuu__mrcoy.signed else 'U',
            vbuu__mrcoy.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(vbuu__mrcoy, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(vbuu__mrcoy)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    jvwqr__ilr = ''
    from collections import defaultdict
    frwy__uyijc = defaultdict(list)
    for xihwh__ojv, taeza__aog in typemap.items():
        frwy__uyijc[taeza__aog].append(xihwh__ojv)
    gqj__egf = df.columns.to_list()
    zswyg__ukoz = []
    for taeza__aog, udrbo__hdfo in frwy__uyijc.items():
        try:
            zswyg__ukoz.append(df.loc[:, udrbo__hdfo].astype(taeza__aog,
                copy=False))
            df = df.drop(udrbo__hdfo, axis=1)
        except (ValueError, TypeError) as igy__epv:
            jvwqr__ilr = (
                f"Caught the runtime error '{igy__epv}' on columns {udrbo__hdfo}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    opl__fejnq = bool(jvwqr__ilr)
    if parallel:
        pmup__mir = MPI.COMM_WORLD
        opl__fejnq = pmup__mir.allreduce(opl__fejnq, op=MPI.LOR)
    if opl__fejnq:
        sfivj__juavp = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if jvwqr__ilr:
            raise TypeError(f'{sfivj__juavp}\n{jvwqr__ilr}')
        else:
            raise TypeError(
                f'{sfivj__juavp}\nPlease refer to errors on other ranks.')
    df = pd.concat(zswyg__ukoz + [df], axis=1)
    fwavn__ysdy = df.loc[:, gqj__egf]
    return fwavn__ysdy


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    wkrn__wxq = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        rvpu__goh = '  skiprows = sorted(set(skiprows))\n'
    else:
        rvpu__goh = '  skiprows = [skiprows]\n'
    rvpu__goh += '  skiprows_list_len = len(skiprows)\n'
    rvpu__goh += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    rvpu__goh += '  check_java_installation(fname)\n'
    rvpu__goh += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    rvpu__goh += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    rvpu__goh += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    rvpu__goh += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, wkrn__wxq, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    rvpu__goh += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    rvpu__goh += "      raise FileNotFoundError('File does not exist')\n"
    return rvpu__goh


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    out_used_cols, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    ppmq__gbt = [str(ddphc__aqc) for ddphc__aqc, stnc__pxvl in enumerate(
        usecols) if col_typs[out_used_cols[ddphc__aqc]].dtype == types.
        NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        ppmq__gbt.append(str(idx_col_index))
    eko__rvz = ', '.join(ppmq__gbt)
    mxkpk__cwjhm = _gen_parallel_flag_name(sanitized_cnames)
    qwj__disxd = f"{mxkpk__cwjhm}='bool_'" if check_parallel_runtime else ''
    gms__nyda = [_get_pd_dtype_str(col_typs[out_used_cols[ddphc__aqc]]) for
        ddphc__aqc in range(len(usecols))]
    eaohx__qjc = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    wxkb__ggm = [stnc__pxvl for ddphc__aqc, stnc__pxvl in enumerate(usecols
        ) if gms__nyda[ddphc__aqc] == 'str']
    if idx_col_index is not None and eaohx__qjc == 'str':
        wxkb__ggm.append(idx_col_index)
    dtbd__irxz = np.array(wxkb__ggm, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = dtbd__irxz
    rvpu__goh = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    vic__bvi = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = vic__bvi
    rvpu__goh += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    bwe__ichxy = np.array(out_used_cols, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = bwe__ichxy
        rvpu__goh += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    uwrtm__hax = defaultdict(list)
    for ddphc__aqc, stnc__pxvl in enumerate(usecols):
        if gms__nyda[ddphc__aqc] == 'str':
            continue
        uwrtm__hax[gms__nyda[ddphc__aqc]].append(stnc__pxvl)
    if idx_col_index is not None and eaohx__qjc != 'str':
        uwrtm__hax[eaohx__qjc].append(idx_col_index)
    for ddphc__aqc, xxo__eitw in enumerate(uwrtm__hax.values()):
        glbs[f't_arr_{ddphc__aqc}_{call_id}'] = np.asarray(xxo__eitw)
        rvpu__goh += (
            f'  t_arr_{ddphc__aqc}_{call_id}_2 = t_arr_{ddphc__aqc}_{call_id}\n'
            )
    if idx_col_index != None:
        rvpu__goh += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {qwj__disxd}):
"""
    else:
        rvpu__goh += f'  with objmode(T=table_type_{call_id}, {qwj__disxd}):\n'
    rvpu__goh += f'    typemap = {{}}\n'
    for ddphc__aqc, hwt__eguek in enumerate(uwrtm__hax.keys()):
        rvpu__goh += f"""    typemap.update({{i:{hwt__eguek} for i in t_arr_{ddphc__aqc}_{call_id}_2}})
"""
    rvpu__goh += '    if f_reader.get_chunk_size() == 0:\n'
    rvpu__goh += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    rvpu__goh += '    else:\n'
    rvpu__goh += '      df = pd.read_csv(f_reader,\n'
    rvpu__goh += '        header=None,\n'
    rvpu__goh += '        parse_dates=[{}],\n'.format(eko__rvz)
    rvpu__goh += (
        f"        dtype={{i:'string[pyarrow]' for i in str_col_nums_{call_id}_2}},\n"
        )
    rvpu__goh += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        rvpu__goh += f'    {mxkpk__cwjhm} = f_reader.is_parallel()\n'
    else:
        rvpu__goh += f'    {mxkpk__cwjhm} = {parallel}\n'
    rvpu__goh += f'    df = astype(df, typemap, {mxkpk__cwjhm})\n'
    if idx_col_index != None:
        aum__inxv = sorted(vic__bvi).index(idx_col_index)
        rvpu__goh += f'    idx_arr = df.iloc[:, {aum__inxv}].values\n'
        rvpu__goh += (
            f'    df.drop(columns=df.columns[{aum__inxv}], inplace=True)\n')
    if len(usecols) == 0:
        rvpu__goh += f'    T = None\n'
    else:
        rvpu__goh += f'    arrs = []\n'
        rvpu__goh += f'    for i in range(df.shape[1]):\n'
        rvpu__goh += f'      arrs.append(df.iloc[:, i].values)\n'
        rvpu__goh += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return rvpu__goh


def _gen_parallel_flag_name(sanitized_cnames):
    mxkpk__cwjhm = '_parallel_value'
    while mxkpk__cwjhm in sanitized_cnames:
        mxkpk__cwjhm = '_' + mxkpk__cwjhm
    return mxkpk__cwjhm


def _gen_csv_reader_py(col_names, col_typs, usecols, out_used_cols, sep,
    parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(qyoa__zabf) for qyoa__zabf in
        col_names]
    rvpu__goh = 'def csv_reader_py(fname, nrows, skiprows):\n'
    rvpu__goh += _gen_csv_file_reader_init(parallel, header, compression, -
        1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    wvax__kvjlt = globals()
    if idx_col_typ != types.none:
        wvax__kvjlt[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        wvax__kvjlt[f'table_type_{call_id}'] = types.none
    else:
        wvax__kvjlt[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    rvpu__goh += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, out_used_cols, sep, escapechar, storage_options,
        call_id, wvax__kvjlt, parallel=parallel, check_parallel_runtime=
        False, idx_col_index=idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        rvpu__goh += '  return (T, idx_arr)\n'
    else:
        rvpu__goh += '  return (T, None)\n'
    kbms__aass = {}
    wvax__kvjlt['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(rvpu__goh, wvax__kvjlt, kbms__aass)
    yxy__juywg = kbms__aass['csv_reader_py']
    rij__ehnf = numba.njit(yxy__juywg)
    compiled_funcs.append(rij__ehnf)
    return rij__ehnf
