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
        ehze__wuhz = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        eqp__rnfbc = cgutils.get_or_insert_function(builder.module,
            ehze__wuhz, name='json_file_chunk_reader')
        ded__gucge = builder.call(eqp__rnfbc, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        xsxwx__cft = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        awgq__kqqf = context.get_python_api(builder)
        xsxwx__cft.meminfo = awgq__kqqf.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), ded__gucge)
        xsxwx__cft.pyobj = ded__gucge
        awgq__kqqf.decref(ded__gucge)
        return xsxwx__cft._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.bool_,
        types.int64, types.voidptr, types.voidptr, storage_options_dict_type
        ), codegen


def remove_dead_json(json_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    licu__twy = []
    suwy__hyez = []
    uugcy__yfe = []
    for axjt__bwq, gnoj__qhz in enumerate(json_node.out_vars):
        if gnoj__qhz.name in lives:
            licu__twy.append(json_node.df_colnames[axjt__bwq])
            suwy__hyez.append(json_node.out_vars[axjt__bwq])
            uugcy__yfe.append(json_node.out_types[axjt__bwq])
    json_node.df_colnames = licu__twy
    json_node.out_vars = suwy__hyez
    json_node.out_types = uugcy__yfe
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        vutmy__nfh = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        hlapp__gjtky = json_node.loc.strformat()
        tyrvp__vzls = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', vutmy__nfh,
            hlapp__gjtky, tyrvp__vzls)
        ujbue__xgjp = [poihm__mvg for axjt__bwq, poihm__mvg in enumerate(
            json_node.df_colnames) if isinstance(json_node.out_types[
            axjt__bwq], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if ujbue__xgjp:
            nxf__ghtzz = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', nxf__ghtzz,
                hlapp__gjtky, ujbue__xgjp)
    parallel = False
    if array_dists is not None:
        parallel = True
        for vao__tlnch in json_node.out_vars:
            if array_dists[vao__tlnch.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                vao__tlnch.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    osoc__witg = len(json_node.out_vars)
    ekg__oehc = ', '.join('arr' + str(axjt__bwq) for axjt__bwq in range(
        osoc__witg))
    xfrg__vome = 'def json_impl(fname):\n'
    xfrg__vome += '    ({},) = _json_reader_py(fname)\n'.format(ekg__oehc)
    qzast__eef = {}
    exec(xfrg__vome, {}, qzast__eef)
    yqm__dpksi = qzast__eef['json_impl']
    uofq__jww = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    vvzl__olwvt = compile_to_numba_ir(yqm__dpksi, {'_json_reader_py':
        uofq__jww}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(vvzl__olwvt, [json_node.file_name])
    cie__ivyn = vvzl__olwvt.body[:-3]
    for axjt__bwq in range(len(json_node.out_vars)):
        cie__ivyn[-len(json_node.out_vars) + axjt__bwq
            ].target = json_node.out_vars[axjt__bwq]
    return cie__ivyn


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
    crj__tlzaq = [sanitize_varname(poihm__mvg) for poihm__mvg in col_names]
    uqgpm__rngzs = ', '.join(str(axjt__bwq) for axjt__bwq, xurb__ediew in
        enumerate(col_typs) if xurb__ediew.dtype == types.NPDatetime('ns'))
    psoak__ccz = ', '.join(["{}='{}'".format(lnj__jrdo, bodo.ir.csv_ext.
        _get_dtype_str(xurb__ediew)) for lnj__jrdo, xurb__ediew in zip(
        crj__tlzaq, col_typs)])
    riolc__zsua = ', '.join(["'{}':{}".format(gtil__pigul, bodo.ir.csv_ext.
        _get_pd_dtype_str(xurb__ediew)) for gtil__pigul, xurb__ediew in zip
        (col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    xfrg__vome = 'def json_reader_py(fname):\n'
    xfrg__vome += '  df_typeref_2 = df_typeref\n'
    xfrg__vome += '  check_java_installation(fname)\n'
    xfrg__vome += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    xfrg__vome += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    xfrg__vome += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    xfrg__vome += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    xfrg__vome += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    xfrg__vome += "      raise FileNotFoundError('File does not exist')\n"
    xfrg__vome += f'  with objmode({psoak__ccz}):\n'
    xfrg__vome += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    xfrg__vome += f'       convert_dates = {convert_dates}, \n'
    xfrg__vome += f'       precise_float={precise_float}, \n'
    xfrg__vome += f'       lines={lines}, \n'
    xfrg__vome += '       dtype={{{}}},\n'.format(riolc__zsua)
    xfrg__vome += '       )\n'
    xfrg__vome += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for lnj__jrdo, gtil__pigul in zip(crj__tlzaq, col_names):
        xfrg__vome += '    if len(df) > 0:\n'
        xfrg__vome += "        {} = df['{}'].values\n".format(lnj__jrdo,
            gtil__pigul)
        xfrg__vome += '    else:\n'
        xfrg__vome += '        {} = np.array([])\n'.format(lnj__jrdo)
    xfrg__vome += '  return ({},)\n'.format(', '.join(qjgo__gnmy for
        qjgo__gnmy in crj__tlzaq))
    ndaib__sdqye = globals()
    ndaib__sdqye.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode':
        objmode, 'check_java_installation': check_java_installation,
        'df_typeref': bodo.DataFrameType(tuple(col_typs), bodo.
        RangeIndexType(None), tuple(col_names)),
        'get_storage_options_pyobject': get_storage_options_pyobject})
    qzast__eef = {}
    exec(xfrg__vome, ndaib__sdqye, qzast__eef)
    uofq__jww = qzast__eef['json_reader_py']
    qbz__odw = numba.njit(uofq__jww)
    compiled_funcs.append(qbz__odw)
    return qbz__odw
