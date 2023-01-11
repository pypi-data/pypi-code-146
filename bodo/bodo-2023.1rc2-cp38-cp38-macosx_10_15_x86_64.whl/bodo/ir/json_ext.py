import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
from numba.extending import intrinsic
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.utils.utils import check_and_propagate_cpp_exception, check_java_installation, sanitize_varname


class JsonReader(ir.Stmt):

    def __init__(self, df_out, loc, out_vars, out_types, file_name,
        df_colnames, orient, convert_dates, precise_float, lines,
        compression, storage_options):
        self.connector_typ = 'json'
        self.df_out = df_out
        self.loc = loc
        self.out_vars = out_vars
        self.out_types = out_types
        self.file_name = file_name
        self.df_colnames = df_colnames
        self.orient = orient
        self.convert_dates = convert_dates
        self.precise_float = precise_float
        self.lines = lines
        self.compression = compression
        self.storage_options = storage_options

    def __repr__(self):
        return ('{} = ReadJson(file={}, col_names={}, types={}, vars={})'.
            format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars))


import llvmlite.binding as ll
from bodo.io import json_cpp
ll.add_symbol('json_file_chunk_reader', json_cpp.json_file_chunk_reader)


@intrinsic
def json_file_chunk_reader(typingctx, fname_t, lines_t, is_parallel_t,
    nrows_t, compression_t, bucket_region_t, storage_options_t):
    assert storage_options_t == storage_options_dict_type, "Storage options don't match expected type"

    def codegen(context, builder, sig, args):
        vqeal__pwlf = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        hbqws__nnbsn = cgutils.get_or_insert_function(builder.module,
            vqeal__pwlf, name='json_file_chunk_reader')
        nqjyi__wcy = builder.call(hbqws__nnbsn, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        emzqo__qftwi = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        rdzb__awzvs = context.get_python_api(builder)
        emzqo__qftwi.meminfo = rdzb__awzvs.nrt_meminfo_new_from_pyobject(
            context.get_constant_null(types.voidptr), nqjyi__wcy)
        emzqo__qftwi.pyobj = nqjyi__wcy
        rdzb__awzvs.decref(nqjyi__wcy)
        return emzqo__qftwi._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.bool_,
        types.int64, types.voidptr, types.voidptr, storage_options_dict_type
        ), codegen


def remove_dead_json(json_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    uilw__ethhf = []
    uzgrp__sxy = []
    tkel__qpnt = []
    for jixzi__poi, dlglk__szzhj in enumerate(json_node.out_vars):
        if dlglk__szzhj.name in lives:
            uilw__ethhf.append(json_node.df_colnames[jixzi__poi])
            uzgrp__sxy.append(json_node.out_vars[jixzi__poi])
            tkel__qpnt.append(json_node.out_types[jixzi__poi])
    json_node.df_colnames = uilw__ethhf
    json_node.out_vars = uzgrp__sxy
    json_node.out_types = tkel__qpnt
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        lwzc__dmakg = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        tfz__oxa = json_node.loc.strformat()
        rtaoh__eoki = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', lwzc__dmakg,
            tfz__oxa, rtaoh__eoki)
        kxddm__yqrcy = [tvnt__tjtur for jixzi__poi, tvnt__tjtur in
            enumerate(json_node.df_colnames) if isinstance(json_node.
            out_types[jixzi__poi], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if kxddm__yqrcy:
            nwrqx__cwu = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', nwrqx__cwu,
                tfz__oxa, kxddm__yqrcy)
    parallel = False
    if array_dists is not None:
        parallel = True
        for ppyec__xhiq in json_node.out_vars:
            if array_dists[ppyec__xhiq.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                ppyec__xhiq.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    wwii__ipyv = len(json_node.out_vars)
    lbc__lae = ', '.join('arr' + str(jixzi__poi) for jixzi__poi in range(
        wwii__ipyv))
    zakr__kkaah = 'def json_impl(fname):\n'
    zakr__kkaah += '    ({},) = _json_reader_py(fname)\n'.format(lbc__lae)
    dxdw__gqc = {}
    exec(zakr__kkaah, {}, dxdw__gqc)
    imohc__zkr = dxdw__gqc['json_impl']
    bmr__ufq = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    xfw__tvvcr = compile_to_numba_ir(imohc__zkr, {'_json_reader_py':
        bmr__ufq}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(xfw__tvvcr, [json_node.file_name])
    keu__tzuc = xfw__tvvcr.body[:-3]
    for jixzi__poi in range(len(json_node.out_vars)):
        keu__tzuc[-len(json_node.out_vars) + jixzi__poi
            ].target = json_node.out_vars[jixzi__poi]
    return keu__tzuc


numba.parfors.array_analysis.array_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[JsonReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[JsonReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[JsonReader] = remove_dead_json
numba.core.analysis.ir_extension_usedefs[JsonReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[JsonReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[JsonReader] = json_distributed_run
compiled_funcs = []


def _gen_json_reader_py(col_names, col_typs, typingctx, targetctx, parallel,
    orient, convert_dates, precise_float, lines, compression, storage_options):
    gqs__puvye = [sanitize_varname(tvnt__tjtur) for tvnt__tjtur in col_names]
    tlg__uylqx = ', '.join(str(jixzi__poi) for jixzi__poi, kbh__rmqg in
        enumerate(col_typs) if kbh__rmqg.dtype == types.NPDatetime('ns'))
    cnolr__ircmu = ', '.join(["{}='{}'".format(vhwsf__orrq, bodo.ir.csv_ext
        ._get_dtype_str(kbh__rmqg)) for vhwsf__orrq, kbh__rmqg in zip(
        gqs__puvye, col_typs)])
    njgo__lczt = ', '.join(["'{}':{}".format(jabmj__byyu, bodo.ir.csv_ext.
        _get_pd_dtype_str(kbh__rmqg)) for jabmj__byyu, kbh__rmqg in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    zakr__kkaah = 'def json_reader_py(fname):\n'
    zakr__kkaah += '  df_typeref_2 = df_typeref\n'
    zakr__kkaah += '  check_java_installation(fname)\n'
    zakr__kkaah += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    zakr__kkaah += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    zakr__kkaah += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    zakr__kkaah += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    zakr__kkaah += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    zakr__kkaah += "      raise FileNotFoundError('File does not exist')\n"
    zakr__kkaah += f'  with objmode({cnolr__ircmu}):\n'
    zakr__kkaah += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    zakr__kkaah += f'       convert_dates = {convert_dates}, \n'
    zakr__kkaah += f'       precise_float={precise_float}, \n'
    zakr__kkaah += f'       lines={lines}, \n'
    zakr__kkaah += '       dtype={{{}}},\n'.format(njgo__lczt)
    zakr__kkaah += '       )\n'
    zakr__kkaah += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for vhwsf__orrq, jabmj__byyu in zip(gqs__puvye, col_names):
        zakr__kkaah += '    if len(df) > 0:\n'
        zakr__kkaah += "        {} = df['{}'].values\n".format(vhwsf__orrq,
            jabmj__byyu)
        zakr__kkaah += '    else:\n'
        zakr__kkaah += '        {} = np.array([])\n'.format(vhwsf__orrq)
    zakr__kkaah += '  return ({},)\n'.format(', '.join(uziiu__bwufv for
        uziiu__bwufv in gqs__puvye))
    yhi__tps = globals()
    yhi__tps.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode': objmode,
        'check_java_installation': check_java_installation, 'df_typeref':
        bodo.DataFrameType(tuple(col_typs), bodo.RangeIndexType(None),
        tuple(col_names)), 'get_storage_options_pyobject':
        get_storage_options_pyobject})
    dxdw__gqc = {}
    exec(zakr__kkaah, yhi__tps, dxdw__gqc)
    bmr__ufq = dxdw__gqc['json_reader_py']
    fjno__cbg = numba.njit(bmr__ufq)
    compiled_funcs.append(fjno__cbg)
    return fjno__cbg
