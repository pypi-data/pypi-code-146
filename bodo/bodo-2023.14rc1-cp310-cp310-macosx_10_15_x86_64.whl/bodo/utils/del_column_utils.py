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
        lhrza__svg = typemap[call_expr.args[1].name].literal_value
        return {lhrza__svg}
    elif fdef in {('table_filter', 'bodo.hiframes.table'), ('table_astype',
        'bodo.utils.table_utils'), ('generate_mappable_table_func',
        'bodo.utils.table_utils'), ('set_table_data', 'bodo.hiframes.table'
        ), ('set_table_data_null', 'bodo.hiframes.table')}:
        yqn__iism = dict(call_expr.kws)
        if 'used_cols' in yqn__iism:
            wrxr__byill = yqn__iism['used_cols']
            vso__jej = typemap[wrxr__byill.name]
            vso__jej = vso__jej.instance_type
            return set(vso__jej.meta)
    elif fdef == ('table_concat', 'bodo.utils.table_utils'):
        wrxr__byill = call_expr.args[1]
        vso__jej = typemap[wrxr__byill.name]
        vso__jej = vso__jej.instance_type
        return set(vso__jej.meta)
    elif fdef == ('table_subset', 'bodo.hiframes.table'):
        aeys__wzlv = call_expr.args[1]
        jycgi__pkfd = typemap[aeys__wzlv.name]
        jycgi__pkfd = jycgi__pkfd.instance_type
        kdloq__laufr = jycgi__pkfd.meta
        yqn__iism = dict(call_expr.kws)
        if 'used_cols' in yqn__iism:
            wrxr__byill = yqn__iism['used_cols']
            vso__jej = typemap[wrxr__byill.name]
            vso__jej = vso__jej.instance_type
            chcar__oaq = set(vso__jej.meta)
            fxvz__tznts = set()
            for zbmux__lkz, iial__aiudh in enumerate(kdloq__laufr):
                if zbmux__lkz in chcar__oaq:
                    fxvz__tznts.add(iial__aiudh)
            return fxvz__tznts
        else:
            return set(kdloq__laufr)
    elif fdef == ('py_data_to_cpp_table', 'bodo.libs.array'):
        wpd__yxc = typemap[call_expr.args[2].name].instance_type.meta
        olatc__ymed = len(typemap[call_expr.args[0].name].arr_types)
        return set(zbmux__lkz for zbmux__lkz in wpd__yxc if zbmux__lkz <
            olatc__ymed)
    elif fdef == ('logical_table_to_table', 'bodo.hiframes.table'):
        rqxt__xnugm = typemap[call_expr.args[2].name].instance_type.meta
        yqtmw__kjiyk = len(typemap[call_expr.args[0].name].arr_types)
        yqn__iism = dict(call_expr.kws)
        if 'used_cols' in yqn__iism:
            chcar__oaq = set(typemap[yqn__iism['used_cols'].name].
                instance_type.meta)
            gbziq__ncup = set()
            for zpwyd__qmmi, qtqh__vmghs in enumerate(rqxt__xnugm):
                if zpwyd__qmmi in chcar__oaq and qtqh__vmghs < yqtmw__kjiyk:
                    gbziq__ncup.add(qtqh__vmghs)
            return gbziq__ncup
        else:
            return set(zbmux__lkz for zbmux__lkz in rqxt__xnugm if 
                zbmux__lkz < yqtmw__kjiyk)
    return None
