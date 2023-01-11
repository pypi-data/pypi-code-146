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
        hwkr__sqzhq = typemap[call_expr.args[1].name].literal_value
        return {hwkr__sqzhq}
    elif fdef in {('table_filter', 'bodo.hiframes.table'), ('table_astype',
        'bodo.utils.table_utils'), ('generate_mappable_table_func',
        'bodo.utils.table_utils'), ('set_table_data', 'bodo.hiframes.table'
        ), ('set_table_data_null', 'bodo.hiframes.table')}:
        wqvds__tjnq = dict(call_expr.kws)
        if 'used_cols' in wqvds__tjnq:
            xstdj__rsn = wqvds__tjnq['used_cols']
            pfya__tgf = typemap[xstdj__rsn.name]
            pfya__tgf = pfya__tgf.instance_type
            return set(pfya__tgf.meta)
    elif fdef == ('table_concat', 'bodo.utils.table_utils'):
        xstdj__rsn = call_expr.args[1]
        pfya__tgf = typemap[xstdj__rsn.name]
        pfya__tgf = pfya__tgf.instance_type
        return set(pfya__tgf.meta)
    elif fdef == ('table_subset', 'bodo.hiframes.table'):
        ptfzf__phj = call_expr.args[1]
        vqf__vdje = typemap[ptfzf__phj.name]
        vqf__vdje = vqf__vdje.instance_type
        ldxi__mvojl = vqf__vdje.meta
        wqvds__tjnq = dict(call_expr.kws)
        if 'used_cols' in wqvds__tjnq:
            xstdj__rsn = wqvds__tjnq['used_cols']
            pfya__tgf = typemap[xstdj__rsn.name]
            pfya__tgf = pfya__tgf.instance_type
            gvnjq__eaow = set(pfya__tgf.meta)
            bdgxb__cdipr = set()
            for zya__crvau, kadud__rtq in enumerate(ldxi__mvojl):
                if zya__crvau in gvnjq__eaow:
                    bdgxb__cdipr.add(kadud__rtq)
            return bdgxb__cdipr
        else:
            return set(ldxi__mvojl)
    elif fdef == ('py_data_to_cpp_table', 'bodo.libs.array'):
        lpt__eak = typemap[call_expr.args[2].name].instance_type.meta
        csud__jlz = len(typemap[call_expr.args[0].name].arr_types)
        return set(zya__crvau for zya__crvau in lpt__eak if zya__crvau <
            csud__jlz)
    elif fdef == ('logical_table_to_table', 'bodo.hiframes.table'):
        wsur__wyx = typemap[call_expr.args[2].name].instance_type.meta
        npglv__xkz = len(typemap[call_expr.args[0].name].arr_types)
        wqvds__tjnq = dict(call_expr.kws)
        if 'used_cols' in wqvds__tjnq:
            gvnjq__eaow = set(typemap[wqvds__tjnq['used_cols'].name].
                instance_type.meta)
            eiuvv__uhs = set()
            for qcnly__xdh, ncxx__qvrc in enumerate(wsur__wyx):
                if qcnly__xdh in gvnjq__eaow and ncxx__qvrc < npglv__xkz:
                    eiuvv__uhs.add(ncxx__qvrc)
            return eiuvv__uhs
        else:
            return set(zya__crvau for zya__crvau in wsur__wyx if zya__crvau <
                npglv__xkz)
    return None
