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
        ibr__kdy = typemap[call_expr.args[1].name].literal_value
        return {ibr__kdy}
    elif fdef in {('table_filter', 'bodo.hiframes.table'), ('table_astype',
        'bodo.utils.table_utils'), ('generate_mappable_table_func',
        'bodo.utils.table_utils'), ('set_table_data', 'bodo.hiframes.table'
        ), ('set_table_data_null', 'bodo.hiframes.table')}:
        hffje__xhr = dict(call_expr.kws)
        if 'used_cols' in hffje__xhr:
            cueb__giapx = hffje__xhr['used_cols']
            diqw__mixeb = typemap[cueb__giapx.name]
            diqw__mixeb = diqw__mixeb.instance_type
            return set(diqw__mixeb.meta)
    elif fdef == ('table_concat', 'bodo.utils.table_utils'):
        cueb__giapx = call_expr.args[1]
        diqw__mixeb = typemap[cueb__giapx.name]
        diqw__mixeb = diqw__mixeb.instance_type
        return set(diqw__mixeb.meta)
    elif fdef == ('table_subset', 'bodo.hiframes.table'):
        klzi__ditbn = call_expr.args[1]
        ilrja__xee = typemap[klzi__ditbn.name]
        ilrja__xee = ilrja__xee.instance_type
        aqj__xtvn = ilrja__xee.meta
        hffje__xhr = dict(call_expr.kws)
        if 'used_cols' in hffje__xhr:
            cueb__giapx = hffje__xhr['used_cols']
            diqw__mixeb = typemap[cueb__giapx.name]
            diqw__mixeb = diqw__mixeb.instance_type
            evhc__sbd = set(diqw__mixeb.meta)
            acq__kgw = set()
            for xqd__sjrcr, yix__eogq in enumerate(aqj__xtvn):
                if xqd__sjrcr in evhc__sbd:
                    acq__kgw.add(yix__eogq)
            return acq__kgw
        else:
            return set(aqj__xtvn)
    elif fdef == ('py_data_to_cpp_table', 'bodo.libs.array'):
        xun__dsp = typemap[call_expr.args[2].name].instance_type.meta
        bdan__zng = len(typemap[call_expr.args[0].name].arr_types)
        return set(xqd__sjrcr for xqd__sjrcr in xun__dsp if xqd__sjrcr <
            bdan__zng)
    elif fdef == ('logical_table_to_table', 'bodo.hiframes.table'):
        lidqx__wai = typemap[call_expr.args[2].name].instance_type.meta
        zimkn__ijfvb = len(typemap[call_expr.args[0].name].arr_types)
        hffje__xhr = dict(call_expr.kws)
        if 'used_cols' in hffje__xhr:
            evhc__sbd = set(typemap[hffje__xhr['used_cols'].name].
                instance_type.meta)
            zoxp__iysp = set()
            for iccfy__lkvgo, puvm__wxe in enumerate(lidqx__wai):
                if iccfy__lkvgo in evhc__sbd and puvm__wxe < zimkn__ijfvb:
                    zoxp__iysp.add(puvm__wxe)
            return zoxp__iysp
        else:
            return set(xqd__sjrcr for xqd__sjrcr in lidqx__wai if 
                xqd__sjrcr < zimkn__ijfvb)
    return None
