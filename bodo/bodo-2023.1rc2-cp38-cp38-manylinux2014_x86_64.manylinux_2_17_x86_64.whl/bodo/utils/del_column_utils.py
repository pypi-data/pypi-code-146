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
        ptn__gry = typemap[call_expr.args[1].name].literal_value
        return {ptn__gry}
    elif fdef in {('table_filter', 'bodo.hiframes.table'), ('table_astype',
        'bodo.utils.table_utils'), ('generate_mappable_table_func',
        'bodo.utils.table_utils'), ('set_table_data', 'bodo.hiframes.table'
        ), ('set_table_data_null', 'bodo.hiframes.table')}:
        poh__gnulk = dict(call_expr.kws)
        if 'used_cols' in poh__gnulk:
            voc__qsd = poh__gnulk['used_cols']
            lhn__zxum = typemap[voc__qsd.name]
            lhn__zxum = lhn__zxum.instance_type
            return set(lhn__zxum.meta)
    elif fdef == ('table_concat', 'bodo.utils.table_utils'):
        voc__qsd = call_expr.args[1]
        lhn__zxum = typemap[voc__qsd.name]
        lhn__zxum = lhn__zxum.instance_type
        return set(lhn__zxum.meta)
    elif fdef == ('table_subset', 'bodo.hiframes.table'):
        olhpo__fku = call_expr.args[1]
        sqq__fnp = typemap[olhpo__fku.name]
        sqq__fnp = sqq__fnp.instance_type
        vtvpg__ukhlx = sqq__fnp.meta
        poh__gnulk = dict(call_expr.kws)
        if 'used_cols' in poh__gnulk:
            voc__qsd = poh__gnulk['used_cols']
            lhn__zxum = typemap[voc__qsd.name]
            lhn__zxum = lhn__zxum.instance_type
            ced__pruuh = set(lhn__zxum.meta)
            hnk__nke = set()
            for loro__muj, bvu__alut in enumerate(vtvpg__ukhlx):
                if loro__muj in ced__pruuh:
                    hnk__nke.add(bvu__alut)
            return hnk__nke
        else:
            return set(vtvpg__ukhlx)
    elif fdef == ('py_data_to_cpp_table', 'bodo.libs.array'):
        zqtg__ohgqc = typemap[call_expr.args[2].name].instance_type.meta
        bmy__pgg = len(typemap[call_expr.args[0].name].arr_types)
        return set(loro__muj for loro__muj in zqtg__ohgqc if loro__muj <
            bmy__pgg)
    elif fdef == ('logical_table_to_table', 'bodo.hiframes.table'):
        jrm__ixele = typemap[call_expr.args[2].name].instance_type.meta
        ghd__bomfv = len(typemap[call_expr.args[0].name].arr_types)
        poh__gnulk = dict(call_expr.kws)
        if 'used_cols' in poh__gnulk:
            ced__pruuh = set(typemap[poh__gnulk['used_cols'].name].
                instance_type.meta)
            guex__raexi = set()
            for bkf__lgdo, rnurz__kpg in enumerate(jrm__ixele):
                if bkf__lgdo in ced__pruuh and rnurz__kpg < ghd__bomfv:
                    guex__raexi.add(rnurz__kpg)
            return guex__raexi
        else:
            return set(loro__muj for loro__muj in jrm__ixele if loro__muj <
                ghd__bomfv)
    return None
