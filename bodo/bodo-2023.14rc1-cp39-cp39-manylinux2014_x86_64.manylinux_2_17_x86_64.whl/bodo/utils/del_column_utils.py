"""Helper information to keep table column deletion
pass organized. This contains information about all
table operations for optimizations.
"""
from typing import Dict, Tuple
from numba.core import ir, types
from bodo.hiframes.table import TableType
table_usecol_funcs = {('get_table_data', 'bodo.hiframes.table'), (
    'table_filter', 'bodo.hiframes.table'), ('table_subset',
    'bodo.hiframes.table'), ('set_table_data', 'bodo.hiframes.table'), (
    'set_table_data_null', 'bodo.hiframes.table'), (
    'generate_mappable_table_func', 'bodo.utils.table_utils'), (
    'table_astype', 'bodo.utils.table_utils'), ('generate_table_nbytes',
    'bodo.utils.table_utils'), ('table_concat', 'bodo.utils.table_utils'),
    ('py_data_to_cpp_table', 'bodo.libs.array'), ('logical_table_to_table',
    'bodo.hiframes.table')}


def is_table_use_column_ops(fdef: Tuple[str, str], args, typemap):
    return fdef in table_usecol_funcs and len(args) > 0 and isinstance(typemap
        [args[0].name], TableType)


def get_table_used_columns(fdef: Tuple[str, str], call_expr: ir.Expr,
    typemap: Dict[str, types.Type]):
    if fdef == ('get_table_data', 'bodo.hiframes.table'):
        cwotf__tlw = typemap[call_expr.args[1].name].literal_value
        return {cwotf__tlw}
    elif fdef in {('table_filter', 'bodo.hiframes.table'), ('table_astype',
        'bodo.utils.table_utils'), ('generate_mappable_table_func',
        'bodo.utils.table_utils'), ('set_table_data', 'bodo.hiframes.table'
        ), ('set_table_data_null', 'bodo.hiframes.table')}:
        pznhd__wnx = dict(call_expr.kws)
        if 'used_cols' in pznhd__wnx:
            agxb__etqu = pznhd__wnx['used_cols']
            ohuzt__qfujk = typemap[agxb__etqu.name]
            ohuzt__qfujk = ohuzt__qfujk.instance_type
            return set(ohuzt__qfujk.meta)
    elif fdef == ('table_concat', 'bodo.utils.table_utils'):
        agxb__etqu = call_expr.args[1]
        ohuzt__qfujk = typemap[agxb__etqu.name]
        ohuzt__qfujk = ohuzt__qfujk.instance_type
        return set(ohuzt__qfujk.meta)
    elif fdef == ('table_subset', 'bodo.hiframes.table'):
        wrrsd__jmj = call_expr.args[1]
        unrvp__bjwt = typemap[wrrsd__jmj.name]
        unrvp__bjwt = unrvp__bjwt.instance_type
        lya__rawhr = unrvp__bjwt.meta
        pznhd__wnx = dict(call_expr.kws)
        if 'used_cols' in pznhd__wnx:
            agxb__etqu = pznhd__wnx['used_cols']
            ohuzt__qfujk = typemap[agxb__etqu.name]
            ohuzt__qfujk = ohuzt__qfujk.instance_type
            qcjg__zjszy = set(ohuzt__qfujk.meta)
            xzhy__shq = set()
            for ldl__nue, awuxn__kde in enumerate(lya__rawhr):
                if ldl__nue in qcjg__zjszy:
                    xzhy__shq.add(awuxn__kde)
            return xzhy__shq
        else:
            return set(lya__rawhr)
    elif fdef == ('py_data_to_cpp_table', 'bodo.libs.array'):
        jhey__faln = typemap[call_expr.args[2].name].instance_type.meta
        kmp__ass = len(typemap[call_expr.args[0].name].arr_types)
        return set(ldl__nue for ldl__nue in jhey__faln if ldl__nue < kmp__ass)
    elif fdef == ('logical_table_to_table', 'bodo.hiframes.table'):
        qpkf__kbz = typemap[call_expr.args[2].name].instance_type.meta
        cqqac__vtj = len(typemap[call_expr.args[0].name].arr_types)
        pznhd__wnx = dict(call_expr.kws)
        if 'used_cols' in pznhd__wnx:
            qcjg__zjszy = set(typemap[pznhd__wnx['used_cols'].name].
                instance_type.meta)
            xta__rent = set()
            for ysunu__gxfgr, xjo__wit in enumerate(qpkf__kbz):
                if ysunu__gxfgr in qcjg__zjszy and xjo__wit < cqqac__vtj:
                    xta__rent.add(xjo__wit)
            return xta__rent
        else:
            return set(ldl__nue for ldl__nue in qpkf__kbz if ldl__nue <
                cqqac__vtj)
    return None
