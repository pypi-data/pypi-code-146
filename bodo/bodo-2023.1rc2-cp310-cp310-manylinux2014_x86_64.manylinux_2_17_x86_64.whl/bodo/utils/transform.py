"""
Helper functions for transformations.
"""
import itertools
import math
import operator
import types as pytypes
from collections import namedtuple
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, types
from numba.core.ir_utils import GuardException, build_definitions, compile_to_numba_ir, compute_cfg_from_blocks, find_callname, find_const, get_definition, guard, is_setitem, mk_unique_var, replace_arg_nodes, require
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import fold_arguments
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoConstUpdatedError, BodoError, can_literalize_type, get_literal_value, get_overload_const_bool, get_overload_const_list, is_literal_type, is_overload_constant_bool
from bodo.utils.utils import is_array_typ, is_assign, is_call, is_expr
ReplaceFunc = namedtuple('ReplaceFunc', ['func', 'arg_types', 'args',
    'glbls', 'inline_bodo_calls', 'run_full_pipeline', 'pre_nodes'])
bodo_types_with_params = {'ArrayItemArrayType', 'CSRMatrixType',
    'CategoricalArrayType', 'CategoricalIndexType', 'DataFrameType',
    'DatetimeIndexType', 'Decimal128Type', 'DecimalArrayType',
    'IntegerArrayType', 'FloatingArrayType', 'IntervalArrayType',
    'IntervalIndexType', 'List', 'MapArrayType', 'NumericIndexType',
    'PDCategoricalDtype', 'PeriodIndexType', 'RangeIndexType', 'SeriesType',
    'StringIndexType', 'BinaryIndexType', 'StructArrayType',
    'TimedeltaIndexType', 'TupleArrayType'}
container_update_method_names = ('clear', 'pop', 'popitem', 'update', 'add',
    'difference_update', 'discard', 'intersection_update', 'remove',
    'symmetric_difference_update', 'append', 'extend', 'insert', 'reverse',
    'sort')
no_side_effect_call_tuples = {(int,), (list,), (set,), (dict,), (min,), (
    max,), (abs,), (len,), (bool,), (str,), ('ceil', math), ('Int32Dtype',
    pd), ('Int64Dtype', pd), ('Timestamp', pd), ('Week', 'offsets',
    'tseries', pd), ('init_series', 'pd_series_ext', 'hiframes', bodo), (
    'get_series_data', 'pd_series_ext', 'hiframes', bodo), (
    'get_series_index', 'pd_series_ext', 'hiframes', bodo), (
    'get_series_name', 'pd_series_ext', 'hiframes', bodo), (
    'get_index_data', 'pd_index_ext', 'hiframes', bodo), ('get_index_name',
    'pd_index_ext', 'hiframes', bodo), ('init_binary_str_index',
    'pd_index_ext', 'hiframes', bodo), ('init_numeric_index',
    'pd_index_ext', 'hiframes', bodo), ('init_categorical_index',
    'pd_index_ext', 'hiframes', bodo), ('_dti_val_finalize', 'pd_index_ext',
    'hiframes', bodo), ('init_datetime_index', 'pd_index_ext', 'hiframes',
    bodo), ('init_timedelta_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_range_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_heter_index', 'pd_index_ext', 'hiframes', bodo), (
    'get_int_arr_data', 'int_arr_ext', 'libs', bodo), ('get_int_arr_bitmap',
    'int_arr_ext', 'libs', bodo), ('init_integer_array', 'int_arr_ext',
    'libs', bodo), ('alloc_int_array', 'int_arr_ext', 'libs', bodo), (
    'init_float_array', 'float_arr_ext', 'libs', bodo), (
    'alloc_float_array', 'float_arr_ext', 'libs', bodo), ('inplace_eq',
    'str_arr_ext', 'libs', bodo), ('get_bool_arr_data', 'bool_arr_ext',
    'libs', bodo), ('get_bool_arr_bitmap', 'bool_arr_ext', 'libs', bodo), (
    'init_bool_array', 'bool_arr_ext', 'libs', bodo), ('alloc_bool_array',
    'bool_arr_ext', 'libs', bodo), ('datetime_date_arr_to_dt64_arr',
    'pd_timestamp_ext', 'hiframes', bodo), ('alloc_pd_datetime_array',
    'pd_datetime_arr_ext', 'libs', bodo), (bodo.libs.bool_arr_ext.
    compute_or_body,), (bodo.libs.bool_arr_ext.compute_and_body,), (
    'alloc_datetime_date_array', 'datetime_date_ext', 'hiframes', bodo), (
    'alloc_datetime_timedelta_array', 'datetime_timedelta_ext', 'hiframes',
    bodo), ('cat_replace', 'pd_categorical_ext', 'hiframes', bodo), (
    'init_categorical_array', 'pd_categorical_ext', 'hiframes', bodo), (
    'alloc_categorical_array', 'pd_categorical_ext', 'hiframes', bodo), (
    'get_categorical_arr_codes', 'pd_categorical_ext', 'hiframes', bodo), (
    '_sum_handle_nan', 'series_kernels', 'hiframes', bodo), ('_box_cat_val',
    'series_kernels', 'hiframes', bodo), ('_mean_handle_nan',
    'series_kernels', 'hiframes', bodo), ('_var_handle_mincount',
    'series_kernels', 'hiframes', bodo), ('_compute_var_nan_count_ddof',
    'series_kernels', 'hiframes', bodo), ('_sem_handle_nan',
    'series_kernels', 'hiframes', bodo), ('dist_return', 'distributed_api',
    'libs', bodo), ('rep_return', 'distributed_api', 'libs', bodo), (
    'init_dataframe', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_data', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_all_data', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_table', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_column_names', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_table_data', 'table', 'hiframes', bodo), ('get_dataframe_index',
    'pd_dataframe_ext', 'hiframes', bodo), ('init_rolling',
    'pd_rolling_ext', 'hiframes', bodo), ('init_groupby', 'pd_groupby_ext',
    'hiframes', bodo), ('calc_nitems', 'array_kernels', 'libs', bodo), (
    'concat', 'array_kernels', 'libs', bodo), ('unique', 'array_kernels',
    'libs', bodo), ('nunique', 'array_kernels', 'libs', bodo), ('quantile',
    'array_kernels', 'libs', bodo), ('explode', 'array_kernels', 'libs',
    bodo), ('explode_no_index', 'array_kernels', 'libs', bodo), (
    'get_arr_lens', 'array_kernels', 'libs', bodo), (
    'str_arr_from_sequence', 'str_arr_ext', 'libs', bodo), (
    'get_str_arr_str_length', 'str_arr_ext', 'libs', bodo), (
    'parse_datetime_str', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_dt64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'dt64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'timedelta64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_timedelta64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'npy_datetimestruct_to_datetime', 'pd_timestamp_ext', 'hiframes', bodo),
    ('isna', 'array_kernels', 'libs', bodo), (bodo.libs.str_arr_ext.
    num_total_chars,), ('num_total_chars', 'str_arr_ext', 'libs', bodo), (
    'copy',), ('from_iterable_impl', 'typing', 'utils', bodo), ('chain',
    itertools), ('groupby',), ('rolling',), (pd.CategoricalDtype,), (bodo.
    hiframes.pd_categorical_ext.get_code_for_value,), ('asarray', np), (
    'int32', np), ('int64', np), ('float64', np), ('float32', np), ('bool_',
    np), ('full', np), ('round', np), ('isnan', np), ('isnat', np), (
    'arange', np), ('internal_prange', 'parfor', numba), ('internal_prange',
    'parfor', 'parfors', numba), ('empty_inferred', 'ndarray', 'unsafe',
    numba), ('_slice_span', 'unicode', numba), ('_normalize_slice',
    'unicode', numba), ('init_session_builder', 'pyspark_ext', 'libs', bodo
    ), ('init_session', 'pyspark_ext', 'libs', bodo), ('init_spark_df',
    'pyspark_ext', 'libs', bodo), ('h5size', 'h5_api', 'io', bodo), (
    'pre_alloc_struct_array', 'struct_arr_ext', 'libs', bodo), (bodo.libs.
    struct_arr_ext.pre_alloc_struct_array,), ('pre_alloc_tuple_array',
    'tuple_arr_ext', 'libs', bodo), (bodo.libs.tuple_arr_ext.
    pre_alloc_tuple_array,), ('pre_alloc_array_item_array',
    'array_item_arr_ext', 'libs', bodo), (bodo.libs.array_item_arr_ext.
    pre_alloc_array_item_array,), ('dist_reduce', 'distributed_api', 'libs',
    bodo), (bodo.libs.distributed_api.dist_reduce,), (
    'pre_alloc_string_array', 'str_arr_ext', 'libs', bodo), (bodo.libs.
    str_arr_ext.pre_alloc_string_array,), ('pre_alloc_binary_array',
    'binary_arr_ext', 'libs', bodo), (bodo.libs.binary_arr_ext.
    pre_alloc_binary_array,), ('pre_alloc_map_array', 'map_arr_ext', 'libs',
    bodo), (bodo.libs.map_arr_ext.pre_alloc_map_array,), (
    'convert_dict_arr_to_int', 'dict_arr_ext', 'libs', bodo), (
    'cat_dict_str', 'dict_arr_ext', 'libs', bodo), ('str_replace',
    'dict_arr_ext', 'libs', bodo), ('dict_arr_to_numeric', 'dict_arr_ext',
    'libs', bodo), ('dict_arr_eq', 'dict_arr_ext', 'libs', bodo), (
    'dict_arr_ne', 'dict_arr_ext', 'libs', bodo), ('str_startswith',
    'dict_arr_ext', 'libs', bodo), ('str_endswith', 'dict_arr_ext', 'libs',
    bodo), ('str_contains_non_regex', 'dict_arr_ext', 'libs', bodo), (
    'str_series_contains_regex', 'dict_arr_ext', 'libs', bodo), (
    'str_capitalize', 'dict_arr_ext', 'libs', bodo), ('str_lower',
    'dict_arr_ext', 'libs', bodo), ('str_swapcase', 'dict_arr_ext', 'libs',
    bodo), ('str_title', 'dict_arr_ext', 'libs', bodo), ('str_upper',
    'dict_arr_ext', 'libs', bodo), ('str_center', 'dict_arr_ext', 'libs',
    bodo), ('str_get', 'dict_arr_ext', 'libs', bodo), ('str_repeat_int',
    'dict_arr_ext', 'libs', bodo), ('str_lstrip', 'dict_arr_ext', 'libs',
    bodo), ('str_rstrip', 'dict_arr_ext', 'libs', bodo), ('str_strip',
    'dict_arr_ext', 'libs', bodo), ('str_zfill', 'dict_arr_ext', 'libs',
    bodo), ('str_ljust', 'dict_arr_ext', 'libs', bodo), ('str_rjust',
    'dict_arr_ext', 'libs', bodo), ('str_find', 'dict_arr_ext', 'libs',
    bodo), ('str_rfind', 'dict_arr_ext', 'libs', bodo), ('str_index',
    'dict_arr_ext', 'libs', bodo), ('str_rindex', 'dict_arr_ext', 'libs',
    bodo), ('str_slice', 'dict_arr_ext', 'libs', bodo), ('str_extract',
    'dict_arr_ext', 'libs', bodo), ('str_extractall', 'dict_arr_ext',
    'libs', bodo), ('str_extractall_multi', 'dict_arr_ext', 'libs', bodo),
    ('str_len', 'dict_arr_ext', 'libs', bodo), ('str_count', 'dict_arr_ext',
    'libs', bodo), ('str_isalnum', 'dict_arr_ext', 'libs', bodo), (
    'str_isalpha', 'dict_arr_ext', 'libs', bodo), ('str_isdigit',
    'dict_arr_ext', 'libs', bodo), ('str_isspace', 'dict_arr_ext', 'libs',
    bodo), ('str_islower', 'dict_arr_ext', 'libs', bodo), ('str_isupper',
    'dict_arr_ext', 'libs', bodo), ('str_istitle', 'dict_arr_ext', 'libs',
    bodo), ('str_isnumeric', 'dict_arr_ext', 'libs', bodo), (
    'str_isdecimal', 'dict_arr_ext', 'libs', bodo), ('str_match',
    'dict_arr_ext', 'libs', bodo), ('prange', bodo), (bodo.prange,), (
    'objmode', bodo), (bodo.objmode,), ('get_label_dict_from_categories',
    'pd_categorial_ext', 'hiframes', bodo), (
    'get_label_dict_from_categories_no_duplicates', 'pd_categorial_ext',
    'hiframes', bodo), ('build_nullable_tuple', 'nullable_tuple_ext',
    'libs', bodo), ('generate_mappable_table_func', 'table_utils', 'utils',
    bodo), ('table_astype', 'table_utils', 'utils', bodo), ('table_concat',
    'table_utils', 'utils', bodo), ('table_filter', 'table', 'hiframes',
    bodo), ('table_subset', 'table', 'hiframes', bodo), (
    'logical_table_to_table', 'table', 'hiframes', bodo), ('set_table_data',
    'table', 'hiframes', bodo), ('set_table_null', 'table', 'hiframes',
    bodo), ('startswith',), ('endswith',), ('upper',), ('lower',), (
    '__bodosql_replace_columns_dummy', 'dataframe_impl', 'hiframes', bodo)}
_np_type_names = {'int8', 'int16', 'int32', 'int64', 'uint8', 'uint16',
    'uint32', 'uint64', 'float32', 'float64', 'bool_'}


def remove_hiframes(rhs, lives, call_list):
    qqjt__lqjbr = tuple(call_list)
    if qqjt__lqjbr in no_side_effect_call_tuples:
        return True
    if qqjt__lqjbr == (bodo.hiframes.pd_index_ext.init_range_index,):
        return True
    if len(call_list) == 4 and call_list[1:] == ['conversion', 'utils', bodo]:
        return True
    if isinstance(call_list[-1], pytypes.ModuleType) and call_list[-1
        ].__name__ == 'bodosql':
        return True
    if call_list[1:] == ['bodosql_array_kernels', 'libs', bodo]:
        return True
    if len(call_list) == 2 and call_list[0] == 'copy':
        return True
    if call_list == ['h5read', 'h5_api', 'io', bodo] and rhs.args[5
        ].name not in lives:
        return True
    if call_list == ['move_str_binary_arr_payload', 'str_arr_ext', 'libs', bodo
        ] and rhs.args[0].name not in lives:
        return True
    if call_list in (['setna', 'array_kernels', 'libs', bodo], [
        'copy_array_element', 'array_kernels', 'libs', bodo], [
        'get_str_arr_item_copy', 'str_arr_ext', 'libs', bodo]) and rhs.args[0
        ].name not in lives:
        return True
    if call_list == ['ensure_column_unboxed', 'table', 'hiframes', bodo
        ] and rhs.args[0].name not in lives and rhs.args[1].name not in lives:
        return True
    if call_list == ['generate_table_nbytes', 'table_utils', 'utils', bodo
        ] and rhs.args[1].name not in lives:
        return True
    if len(qqjt__lqjbr) == 1 and tuple in getattr(qqjt__lqjbr[0], '__mro__', ()
        ):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=False, add_default_globals=True):
    if replace_globals:
        uwj__wjivc = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math}
    else:
        uwj__wjivc = func.__globals__
    if extra_globals is not None:
        uwj__wjivc.update(extra_globals)
    if add_default_globals:
        uwj__wjivc.update({'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math})
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, uwj__wjivc, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[utg__xkq.name] for utg__xkq in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, uwj__wjivc)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        jkni__bsuv = tuple(typing_info.typemap[utg__xkq.name] for utg__xkq in
            args)
        lsxsz__tkclh = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, jkni__bsuv, {}, {}, flags)
        lsxsz__tkclh.run()
    iugf__opmdw = f_ir.blocks.popitem()[1]
    replace_arg_nodes(iugf__opmdw, args)
    odr__ccxcr = iugf__opmdw.body[:-2]
    update_locs(odr__ccxcr[len(args):], loc)
    for stmt in odr__ccxcr[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        ayun__bqfs = iugf__opmdw.body[-2]
        assert is_assign(ayun__bqfs) and is_expr(ayun__bqfs.value, 'cast')
        bnizd__oiuvq = ayun__bqfs.value.value
        odr__ccxcr.append(ir.Assign(bnizd__oiuvq, ret_var, loc))
    return odr__ccxcr


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for fjw__vtrvd in stmt.list_vars():
            fjw__vtrvd.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        xycpm__pcspf = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        khjdw__qdlpm, pzdto__foy = xycpm__pcspf(stmt)
        return pzdto__foy
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        lvmto__borel = get_const_value_inner(func_ir, var, arg_types,
            typemap, file_info=file_info)
        if isinstance(lvmto__borel, ir.UndefinedType):
            ixe__bpvp = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{ixe__bpvp}' is not defined", loc=loc)
    except GuardException as mdmpn__wmsh:
        raise BodoError(err_msg, loc=loc)
    return lvmto__borel


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    gum__iquq = get_definition(func_ir, var)
    fpyv__utwn = None
    if typemap is not None:
        fpyv__utwn = typemap.get(var.name, None)
    if isinstance(gum__iquq, ir.Arg) and arg_types is not None:
        fpyv__utwn = arg_types[gum__iquq.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(fpyv__utwn):
        return get_literal_value(fpyv__utwn)
    if isinstance(gum__iquq, (ir.Const, ir.Global, ir.FreeVar)):
        lvmto__borel = gum__iquq.value
        return lvmto__borel
    if literalize_args and isinstance(gum__iquq, ir.Arg
        ) and can_literalize_type(fpyv__utwn, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({gum__iquq.index}, loc=var.
            loc, file_infos={gum__iquq.index: file_info} if file_info is not
            None else None)
    if is_expr(gum__iquq, 'binop'):
        if file_info and gum__iquq.fn == operator.add:
            try:
                uuw__pqb = get_const_value_inner(func_ir, gum__iquq.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(uuw__pqb, True)
                acgk__xlfxl = get_const_value_inner(func_ir, gum__iquq.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return gum__iquq.fn(uuw__pqb, acgk__xlfxl)
            except (GuardException, BodoConstUpdatedError) as mdmpn__wmsh:
                pass
            try:
                acgk__xlfxl = get_const_value_inner(func_ir, gum__iquq.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(acgk__xlfxl, False)
                uuw__pqb = get_const_value_inner(func_ir, gum__iquq.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return gum__iquq.fn(uuw__pqb, acgk__xlfxl)
            except (GuardException, BodoConstUpdatedError) as mdmpn__wmsh:
                pass
        uuw__pqb = get_const_value_inner(func_ir, gum__iquq.lhs, arg_types,
            typemap, updated_containers)
        acgk__xlfxl = get_const_value_inner(func_ir, gum__iquq.rhs,
            arg_types, typemap, updated_containers)
        return gum__iquq.fn(uuw__pqb, acgk__xlfxl)
    if is_expr(gum__iquq, 'unary'):
        lvmto__borel = get_const_value_inner(func_ir, gum__iquq.value,
            arg_types, typemap, updated_containers)
        return gum__iquq.fn(lvmto__borel)
    if is_expr(gum__iquq, 'getattr') and typemap:
        ifqx__nywx = typemap.get(gum__iquq.value.name, None)
        if isinstance(ifqx__nywx, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and gum__iquq.attr == 'columns':
            return pd.Index(ifqx__nywx.columns)
        if isinstance(ifqx__nywx, types.SliceType):
            dqjq__ykxj = get_definition(func_ir, gum__iquq.value)
            require(is_call(dqjq__ykxj))
            dpkx__mnz = find_callname(func_ir, dqjq__ykxj)
            iwvx__wkh = False
            if dpkx__mnz == ('_normalize_slice', 'numba.cpython.unicode'):
                require(gum__iquq.attr in ('start', 'step'))
                dqjq__ykxj = get_definition(func_ir, dqjq__ykxj.args[0])
                iwvx__wkh = True
            require(find_callname(func_ir, dqjq__ykxj) == ('slice', 'builtins')
                )
            if len(dqjq__ykxj.args) == 1:
                if gum__iquq.attr == 'start':
                    return 0
                if gum__iquq.attr == 'step':
                    return 1
                require(gum__iquq.attr == 'stop')
                return get_const_value_inner(func_ir, dqjq__ykxj.args[0],
                    arg_types, typemap, updated_containers)
            if gum__iquq.attr == 'start':
                lvmto__borel = get_const_value_inner(func_ir, dqjq__ykxj.
                    args[0], arg_types, typemap, updated_containers)
                if lvmto__borel is None:
                    lvmto__borel = 0
                if iwvx__wkh:
                    require(lvmto__borel == 0)
                return lvmto__borel
            if gum__iquq.attr == 'stop':
                assert not iwvx__wkh
                return get_const_value_inner(func_ir, dqjq__ykxj.args[1],
                    arg_types, typemap, updated_containers)
            require(gum__iquq.attr == 'step')
            if len(dqjq__ykxj.args) == 2:
                return 1
            else:
                lvmto__borel = get_const_value_inner(func_ir, dqjq__ykxj.
                    args[2], arg_types, typemap, updated_containers)
                if lvmto__borel is None:
                    lvmto__borel = 1
                if iwvx__wkh:
                    require(lvmto__borel == 1)
                return lvmto__borel
    if is_expr(gum__iquq, 'getattr'):
        return getattr(get_const_value_inner(func_ir, gum__iquq.value,
            arg_types, typemap, updated_containers), gum__iquq.attr)
    if is_expr(gum__iquq, 'getitem'):
        value = get_const_value_inner(func_ir, gum__iquq.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, gum__iquq.index, arg_types,
            typemap, updated_containers)
        return value[index]
    uvp__xwsy = guard(find_callname, func_ir, gum__iquq, typemap)
    if uvp__xwsy is not None and len(uvp__xwsy) == 2 and uvp__xwsy[0
        ] == 'keys' and isinstance(uvp__xwsy[1], ir.Var):
        gyxr__brf = gum__iquq.func
        gum__iquq = get_definition(func_ir, uvp__xwsy[1])
        kfbqo__txw = uvp__xwsy[1].name
        if updated_containers and kfbqo__txw in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                kfbqo__txw, updated_containers[kfbqo__txw]))
        require(is_expr(gum__iquq, 'build_map'))
        vals = [fjw__vtrvd[0] for fjw__vtrvd in gum__iquq.items]
        xfzm__hqjkv = guard(get_definition, func_ir, gyxr__brf)
        assert isinstance(xfzm__hqjkv, ir.Expr) and xfzm__hqjkv.attr == 'keys'
        xfzm__hqjkv.attr = 'copy'
        return [get_const_value_inner(func_ir, fjw__vtrvd, arg_types,
            typemap, updated_containers) for fjw__vtrvd in vals]
    if is_expr(gum__iquq, 'build_map'):
        return {get_const_value_inner(func_ir, fjw__vtrvd[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            fjw__vtrvd[1], arg_types, typemap, updated_containers) for
            fjw__vtrvd in gum__iquq.items}
    if is_expr(gum__iquq, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, fjw__vtrvd, arg_types,
            typemap, updated_containers) for fjw__vtrvd in gum__iquq.items)
    if is_expr(gum__iquq, 'build_list'):
        return [get_const_value_inner(func_ir, fjw__vtrvd, arg_types,
            typemap, updated_containers) for fjw__vtrvd in gum__iquq.items]
    if is_expr(gum__iquq, 'build_set'):
        return {get_const_value_inner(func_ir, fjw__vtrvd, arg_types,
            typemap, updated_containers) for fjw__vtrvd in gum__iquq.items}
    if uvp__xwsy == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, gum__iquq.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if uvp__xwsy == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, gum__iquq.args[0],
            arg_types, typemap, updated_containers))
    if uvp__xwsy == ('range', 'builtins') and len(gum__iquq.args) == 1:
        return range(get_const_value_inner(func_ir, gum__iquq.args[0],
            arg_types, typemap, updated_containers))
    if uvp__xwsy == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, fjw__vtrvd,
            arg_types, typemap, updated_containers) for fjw__vtrvd in
            gum__iquq.args))
    if uvp__xwsy == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, gum__iquq.args[0],
            arg_types, typemap, updated_containers))
    if uvp__xwsy == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, gum__iquq.args[0],
            arg_types, typemap, updated_containers))
    if uvp__xwsy == ('format', 'builtins'):
        utg__xkq = get_const_value_inner(func_ir, gum__iquq.args[0],
            arg_types, typemap, updated_containers)
        uxia__ncmij = get_const_value_inner(func_ir, gum__iquq.args[1],
            arg_types, typemap, updated_containers) if len(gum__iquq.args
            ) > 1 else ''
        return format(utg__xkq, uxia__ncmij)
    if uvp__xwsy in (('init_binary_str_index', 'bodo.hiframes.pd_index_ext'
        ), ('init_numeric_index', 'bodo.hiframes.pd_index_ext'), (
        'init_categorical_index', 'bodo.hiframes.pd_index_ext'), (
        'init_datetime_index', 'bodo.hiframes.pd_index_ext'), (
        'init_timedelta_index', 'bodo.hiframes.pd_index_ext'), (
        'init_heter_index', 'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, gum__iquq.args[0],
            arg_types, typemap, updated_containers))
    if uvp__xwsy == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, gum__iquq.args[0],
            arg_types, typemap, updated_containers))
    if uvp__xwsy == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, gum__iquq.args[
            0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, gum__iquq.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            gum__iquq.args[2], arg_types, typemap, updated_containers))
    if uvp__xwsy == ('len', 'builtins') and typemap and isinstance(typemap.
        get(gum__iquq.args[0].name, None), types.BaseTuple):
        return len(typemap[gum__iquq.args[0].name])
    if uvp__xwsy == ('len', 'builtins'):
        bsbk__ksmpb = guard(get_definition, func_ir, gum__iquq.args[0])
        if isinstance(bsbk__ksmpb, ir.Expr) and bsbk__ksmpb.op in (
            'build_tuple', 'build_list', 'build_set', 'build_map'):
            return len(bsbk__ksmpb.items)
        return len(get_const_value_inner(func_ir, gum__iquq.args[0],
            arg_types, typemap, updated_containers))
    if uvp__xwsy == ('CategoricalDtype', 'pandas'):
        kws = dict(gum__iquq.kws)
        rwj__xxfo = get_call_expr_arg('CategoricalDtype', gum__iquq.args,
            kws, 0, 'categories', '')
        sub__cgl = get_call_expr_arg('CategoricalDtype', gum__iquq.args,
            kws, 1, 'ordered', False)
        if sub__cgl is not False:
            sub__cgl = get_const_value_inner(func_ir, sub__cgl, arg_types,
                typemap, updated_containers)
        if rwj__xxfo == '':
            rwj__xxfo = None
        else:
            rwj__xxfo = get_const_value_inner(func_ir, rwj__xxfo, arg_types,
                typemap, updated_containers)
        return pd.CategoricalDtype(rwj__xxfo, sub__cgl)
    if uvp__xwsy == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, gum__iquq.args[0],
            arg_types, typemap, updated_containers))
    if uvp__xwsy is not None and uvp__xwsy[1] == 'numpy' and uvp__xwsy[0
        ] in _np_type_names:
        return getattr(np, uvp__xwsy[0])(get_const_value_inner(func_ir,
            gum__iquq.args[0], arg_types, typemap, updated_containers))
    if uvp__xwsy is not None and len(uvp__xwsy) == 2 and uvp__xwsy[1
        ] == 'pandas' and uvp__xwsy[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, uvp__xwsy[0])()
    if uvp__xwsy is not None and len(uvp__xwsy) == 2 and isinstance(uvp__xwsy
        [1], ir.Var):
        lvmto__borel = get_const_value_inner(func_ir, uvp__xwsy[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, fjw__vtrvd, arg_types,
            typemap, updated_containers) for fjw__vtrvd in gum__iquq.args]
        kws = {ymxt__wlno[0]: get_const_value_inner(func_ir, ymxt__wlno[1],
            arg_types, typemap, updated_containers) for ymxt__wlno in
            gum__iquq.kws}
        return getattr(lvmto__borel, uvp__xwsy[0])(*args, **kws)
    if uvp__xwsy is not None and len(uvp__xwsy) == 2 and uvp__xwsy[1
        ] == 'bodo' and uvp__xwsy[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, fjw__vtrvd, arg_types,
            typemap, updated_containers) for fjw__vtrvd in gum__iquq.args)
        kwargs = {ixe__bpvp: get_const_value_inner(func_ir, fjw__vtrvd,
            arg_types, typemap, updated_containers) for ixe__bpvp,
            fjw__vtrvd in dict(gum__iquq.kws).items()}
        return getattr(bodo, uvp__xwsy[0])(*args, **kwargs)
    if is_call(gum__iquq) and typemap and isinstance(typemap.get(gum__iquq.
        func.name, None), types.Dispatcher):
        py_func = typemap[gum__iquq.func.name].dispatcher.py_func
        require(gum__iquq.vararg is None)
        args = tuple(get_const_value_inner(func_ir, fjw__vtrvd, arg_types,
            typemap, updated_containers) for fjw__vtrvd in gum__iquq.args)
        kwargs = {ixe__bpvp: get_const_value_inner(func_ir, fjw__vtrvd,
            arg_types, typemap, updated_containers) for ixe__bpvp,
            fjw__vtrvd in dict(gum__iquq.kws).items()}
        arg_types = tuple(bodo.typeof(fjw__vtrvd) for fjw__vtrvd in args)
        kw_types = {zod__nitp: bodo.typeof(fjw__vtrvd) for zod__nitp,
            fjw__vtrvd in kwargs.items()}
        require(_func_is_pure(py_func, arg_types, kw_types))
        return py_func(*args, **kwargs)
    raise GuardException('Constant value not found')


def _func_is_pure(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.ir.csv_ext import CsvReader
    from bodo.ir.json_ext import JsonReader
    from bodo.ir.parquet_ext import ParquetReader
    from bodo.ir.sql_ext import SqlReader
    f_ir, typemap, xfx__sijcf, xfx__sijcf = bodo.compiler.get_func_type_info(
        py_func, arg_types, kw_types)
    for block in f_ir.blocks.values():
        for stmt in block.body:
            if isinstance(stmt, ir.Print):
                return False
            if isinstance(stmt, (CsvReader, JsonReader, ParquetReader,
                SqlReader)):
                return False
            if is_setitem(stmt) and isinstance(guard(get_definition, f_ir,
                stmt.target), ir.Arg):
                return False
            if is_assign(stmt):
                rhs = stmt.value
                if isinstance(rhs, ir.Yield):
                    return False
                if is_call(rhs):
                    doiz__ryo = guard(get_definition, f_ir, rhs.func)
                    if isinstance(doiz__ryo, ir.Const) and isinstance(doiz__ryo
                        .value, numba.core.dispatcher.ObjModeLiftedWith):
                        return False
                    umrbi__ygbum = guard(find_callname, f_ir, rhs)
                    if umrbi__ygbum is None:
                        return False
                    func_name, yqu__efg = umrbi__ygbum
                    if yqu__efg == 'pandas' and func_name.startswith('read_'):
                        return False
                    if umrbi__ygbum in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if umrbi__ygbum == ('File', 'h5py'):
                        return False
                    if isinstance(yqu__efg, ir.Var):
                        fpyv__utwn = typemap[yqu__efg.name]
                        if isinstance(fpyv__utwn, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(fpyv__utwn, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(fpyv__utwn, bodo.LoggingLoggerType):
                            return False
                        if str(fpyv__utwn).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir, yqu__efg
                            ), ir.Arg)):
                            return False
                    if yqu__efg in ('numpy.random', 'time', 'logging',
                        'matplotlib.pyplot'):
                        return False
    return True


def fold_argument_types(pysig, args, kws):

    def normal_handler(index, param, value):
        return value

    def default_handler(index, param, default):
        return types.Omitted(default)

    def stararg_handler(index, param, values):
        return types.StarArgTuple(values)
    args = fold_arguments(pysig, args, kws, normal_handler, default_handler,
        stararg_handler)
    return args


def get_const_func_output_type(func, arg_types, kw_types, typing_context,
    target_context, is_udf=True):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
    py_func = None
    if isinstance(func, types.MakeFunctionLiteral):
        tbzai__emp = func.literal_value.code
        gbmt__lei = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            gbmt__lei = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(gbmt__lei, tbzai__emp)
        fix_struct_return(f_ir)
        typemap, oboe__mman, xssys__jeqw, xfx__sijcf = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, xssys__jeqw, oboe__mman = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, xssys__jeqw, oboe__mman = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, xssys__jeqw, oboe__mman = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(oboe__mman, types.DictType):
        euc__jkj = guard(get_struct_keynames, f_ir, typemap)
        if euc__jkj is not None:
            oboe__mman = StructType((oboe__mman.value_type,) * len(euc__jkj
                ), euc__jkj)
    if is_udf and isinstance(oboe__mman, (SeriesType, HeterogeneousSeriesType)
        ):
        merh__vuwxu = numba.core.registry.cpu_target.typing_context
        razag__wjj = numba.core.registry.cpu_target.target_context
        rnf__hlo = bodo.transforms.series_pass.SeriesPass(f_ir, merh__vuwxu,
            razag__wjj, typemap, xssys__jeqw, {})
        xtlk__uko = rnf__hlo.run()
        if xtlk__uko:
            xtlk__uko = rnf__hlo.run()
            if xtlk__uko:
                rnf__hlo.run()
        mgbv__fom = compute_cfg_from_blocks(f_ir.blocks)
        hici__bmafp = [guard(_get_const_series_info, f_ir.blocks[wmx__glxr],
            f_ir, typemap) for wmx__glxr in mgbv__fom.exit_points() if
            isinstance(f_ir.blocks[wmx__glxr].body[-1], ir.Return)]
        if None in hici__bmafp or len(pd.Series(hici__bmafp).unique()) != 1:
            oboe__mman.const_info = None
        else:
            oboe__mman.const_info = hici__bmafp[0]
    return oboe__mman


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    gsbnf__ivf = block.body[-1].value
    ccaae__ujxvk = get_definition(f_ir, gsbnf__ivf)
    require(is_expr(ccaae__ujxvk, 'cast'))
    ccaae__ujxvk = get_definition(f_ir, ccaae__ujxvk.value)
    require(is_call(ccaae__ujxvk) and find_callname(f_ir, ccaae__ujxvk) ==
        ('init_series', 'bodo.hiframes.pd_series_ext'))
    peich__ygyp = ccaae__ujxvk.args[1]
    jgeyt__havmt = tuple(get_const_value_inner(f_ir, peich__ygyp, typemap=
        typemap))
    if isinstance(typemap[gsbnf__ivf.name], HeterogeneousSeriesType):
        return len(typemap[gsbnf__ivf.name].data), jgeyt__havmt
    uxauj__bzlz = ccaae__ujxvk.args[0]
    imym__unrkt = get_definition(f_ir, uxauj__bzlz)
    func_name, pvuz__trdl = find_callname(f_ir, imym__unrkt)
    if is_call(imym__unrkt) and bodo.utils.utils.is_alloc_callname(func_name,
        pvuz__trdl):
        kcm__mvi = imym__unrkt.args[0]
        qryq__xnxh = get_const_value_inner(f_ir, kcm__mvi, typemap=typemap)
        return qryq__xnxh, jgeyt__havmt
    if is_call(imym__unrkt) and find_callname(f_ir, imym__unrkt) in [(
        'asarray', 'numpy'), ('str_arr_from_sequence',
        'bodo.libs.str_arr_ext'), ('build_nullable_tuple',
        'bodo.libs.nullable_tuple_ext')]:
        uxauj__bzlz = imym__unrkt.args[0]
        imym__unrkt = get_definition(f_ir, uxauj__bzlz)
    require(is_expr(imym__unrkt, 'build_tuple') or is_expr(imym__unrkt,
        'build_list'))
    return len(imym__unrkt.items), jgeyt__havmt


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    tpo__auco = []
    uyzku__hxo = []
    values = []
    for zod__nitp, fjw__vtrvd in build_map.items:
        bhxhy__lss = find_const(f_ir, zod__nitp)
        require(isinstance(bhxhy__lss, str))
        uyzku__hxo.append(bhxhy__lss)
        tpo__auco.append(zod__nitp)
        values.append(fjw__vtrvd)
    yun__zqgfy = ir.Var(scope, mk_unique_var('val_tup'), loc)
    xhml__eixl = ir.Assign(ir.Expr.build_tuple(values, loc), yun__zqgfy, loc)
    f_ir._definitions[yun__zqgfy.name] = [xhml__eixl.value]
    lqfnp__mqopj = ir.Var(scope, mk_unique_var('key_tup'), loc)
    neio__tvg = ir.Assign(ir.Expr.build_tuple(tpo__auco, loc), lqfnp__mqopj,
        loc)
    f_ir._definitions[lqfnp__mqopj.name] = [neio__tvg.value]
    if typemap is not None:
        typemap[yun__zqgfy.name] = types.Tuple([typemap[fjw__vtrvd.name] for
            fjw__vtrvd in values])
        typemap[lqfnp__mqopj.name] = types.Tuple([typemap[fjw__vtrvd.name] for
            fjw__vtrvd in tpo__auco])
    return uyzku__hxo, yun__zqgfy, xhml__eixl, lqfnp__mqopj, neio__tvg


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    vgfv__vic = block.body[-1].value
    yrmn__vjsgx = guard(get_definition, f_ir, vgfv__vic)
    require(is_expr(yrmn__vjsgx, 'cast'))
    ccaae__ujxvk = guard(get_definition, f_ir, yrmn__vjsgx.value)
    require(is_expr(ccaae__ujxvk, 'build_map'))
    require(len(ccaae__ujxvk.items) > 0)
    loc = block.loc
    scope = block.scope
    uyzku__hxo, yun__zqgfy, xhml__eixl, lqfnp__mqopj, neio__tvg = (
        extract_keyvals_from_struct_map(f_ir, ccaae__ujxvk, loc, scope))
    tynq__vdpn = ir.Var(scope, mk_unique_var('conv_call'), loc)
    revp__gmdhh = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), tynq__vdpn, loc)
    f_ir._definitions[tynq__vdpn.name] = [revp__gmdhh.value]
    wqd__ppntt = ir.Var(scope, mk_unique_var('struct_val'), loc)
    ujunq__qmwl = ir.Assign(ir.Expr.call(tynq__vdpn, [yun__zqgfy,
        lqfnp__mqopj], {}, loc), wqd__ppntt, loc)
    f_ir._definitions[wqd__ppntt.name] = [ujunq__qmwl.value]
    yrmn__vjsgx.value = wqd__ppntt
    ccaae__ujxvk.items = [(zod__nitp, zod__nitp) for zod__nitp, xfx__sijcf in
        ccaae__ujxvk.items]
    block.body = block.body[:-2] + [xhml__eixl, neio__tvg, revp__gmdhh,
        ujunq__qmwl] + block.body[-2:]
    return tuple(uyzku__hxo)


def get_struct_keynames(f_ir, typemap):
    mgbv__fom = compute_cfg_from_blocks(f_ir.blocks)
    fhrxe__ktpqt = list(mgbv__fom.exit_points())[0]
    block = f_ir.blocks[fhrxe__ktpqt]
    require(isinstance(block.body[-1], ir.Return))
    vgfv__vic = block.body[-1].value
    yrmn__vjsgx = guard(get_definition, f_ir, vgfv__vic)
    require(is_expr(yrmn__vjsgx, 'cast'))
    ccaae__ujxvk = guard(get_definition, f_ir, yrmn__vjsgx.value)
    require(is_call(ccaae__ujxvk) and find_callname(f_ir, ccaae__ujxvk) ==
        ('struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[ccaae__ujxvk.args[1].name])


def fix_struct_return(f_ir):
    dle__zcs = None
    mgbv__fom = compute_cfg_from_blocks(f_ir.blocks)
    for fhrxe__ktpqt in mgbv__fom.exit_points():
        dle__zcs = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            fhrxe__ktpqt], fhrxe__ktpqt)
    return dle__zcs


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    vjq__otfn = ir.Block(ir.Scope(None, loc), loc)
    vjq__otfn.body = node_list
    build_definitions({(0): vjq__otfn}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(fjw__vtrvd) for fjw__vtrvd in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    ckoog__qdu = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(ckoog__qdu, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for xlop__jxrnf in range(len(vals) - 1, -1, -1):
        fjw__vtrvd = vals[xlop__jxrnf]
        if isinstance(fjw__vtrvd, str) and fjw__vtrvd.startswith(
            NESTED_TUP_SENTINEL):
            xuax__rmanj = int(fjw__vtrvd[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:xlop__jxrnf]) + (
                tuple(vals[xlop__jxrnf + 1:xlop__jxrnf + xuax__rmanj + 1]),
                ) + tuple(vals[xlop__jxrnf + xuax__rmanj + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    utg__xkq = None
    if len(args) > arg_no and arg_no >= 0:
        utg__xkq = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        utg__xkq = kws[arg_name]
    if utg__xkq is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return utg__xkq


def set_call_expr_arg(var, args, kws, arg_no, arg_name, add_if_missing=False):
    if len(args) > arg_no:
        args[arg_no] = var
    elif add_if_missing or arg_name in kws:
        kws[arg_name] = var
    else:
        raise BodoError('cannot set call argument since does not exist')


def avoid_udf_inline(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    f_ir = numba.core.compiler.run_frontend(py_func, inline_closures=True)
    if '_bodo_inline' in kw_types and is_overload_constant_bool(kw_types[
        '_bodo_inline']):
        return not get_overload_const_bool(kw_types['_bodo_inline'])
    if any(isinstance(t, DataFrameType) for t in arg_types + tuple(kw_types
        .values())):
        return True
    for block in f_ir.blocks.values():
        if isinstance(block.body[-1], (ir.Raise, ir.StaticRaise)):
            return True
        for stmt in block.body:
            if isinstance(stmt, ir.EnterWith):
                return True
    return False


def replace_func(pass_info, func, args, const=False, pre_nodes=None,
    extra_globals=None, pysig=None, kws=None, inline_bodo_calls=False,
    run_full_pipeline=False):
    uwj__wjivc = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        uwj__wjivc.update(extra_globals)
    func.__globals__.update(uwj__wjivc)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            niowj__asuu = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[niowj__asuu.name] = types.literal(default)
            except:
                pass_info.typemap[niowj__asuu.name] = numba.typeof(default)
            nrc__zid = ir.Assign(ir.Const(default, loc), niowj__asuu, loc)
            pre_nodes.append(nrc__zid)
            return niowj__asuu
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    jkni__bsuv = tuple(pass_info.typemap[fjw__vtrvd.name] for fjw__vtrvd in
        args)
    if const:
        agyd__idch = []
        for xlop__jxrnf, utg__xkq in enumerate(args):
            lvmto__borel = guard(find_const, pass_info.func_ir, utg__xkq)
            if lvmto__borel:
                agyd__idch.append(types.literal(lvmto__borel))
            else:
                agyd__idch.append(jkni__bsuv[xlop__jxrnf])
        jkni__bsuv = tuple(agyd__idch)
    return ReplaceFunc(func, jkni__bsuv, args, uwj__wjivc,
        inline_bodo_calls, run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(pbz__ewac) for pbz__ewac in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        iht__uhe = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {iht__uhe} = 0\n', (iht__uhe,)
    if isinstance(t, ArrayItemArrayType):
        uozxj__aar, nbsiy__lpus = gen_init_varsize_alloc_sizes(t.dtype)
        iht__uhe = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {iht__uhe} = 0\n' + uozxj__aar, (iht__uhe,) + nbsiy__lpus
    return '', ()


def gen_varsize_item_sizes(t, item, var_names):
    if t == string_array_type:
        return '    {} += bodo.libs.str_arr_ext.get_utf8_size({})\n'.format(
            var_names[0], item)
    if isinstance(t, ArrayItemArrayType):
        return '    {} += len({})\n'.format(var_names[0], item
            ) + gen_varsize_array_counts(t.dtype, item, var_names[1:])
    return ''


def gen_varsize_array_counts(t, item, var_names):
    if t == string_array_type:
        return ('    {} += bodo.libs.str_arr_ext.get_num_total_chars({})\n'
            .format(var_names[0], item))
    return ''


def get_type_alloc_counts(t):
    if isinstance(t, (StructArrayType, TupleArrayType)):
        return 1 + sum(get_type_alloc_counts(pbz__ewac.dtype) for pbz__ewac in
            t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(pbz__ewac) for pbz__ewac in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(pbz__ewac) for pbz__ewac in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    cacu__jll = typing_context.resolve_getattr(obj_dtype, func_name)
    if cacu__jll is None:
        hdahu__aduv = types.misc.Module(np)
        try:
            cacu__jll = typing_context.resolve_getattr(hdahu__aduv, func_name)
        except AttributeError as mdmpn__wmsh:
            cacu__jll = None
        if cacu__jll is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return cacu__jll


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    cacu__jll = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(cacu__jll, types.BoundFunction):
        if axis is not None:
            ftmge__zqmnz = cacu__jll.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            ftmge__zqmnz = cacu__jll.get_call_type(typing_context, (), {})
        return ftmge__zqmnz.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(cacu__jll):
            ftmge__zqmnz = cacu__jll.get_call_type(typing_context, (
                obj_dtype,), {})
            return ftmge__zqmnz.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    cacu__jll = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(cacu__jll, types.BoundFunction):
        btu__blgs = cacu__jll.template
        if axis is not None:
            return btu__blgs._overload_func(obj_dtype, axis=axis)
        else:
            return btu__blgs._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    beq__posd = get_definition(func_ir, dict_var)
    require(isinstance(beq__posd, ir.Expr))
    require(beq__posd.op == 'build_map')
    tsxjo__bxjw = beq__posd.items
    tpo__auco = []
    values = []
    cefm__slbo = False
    for xlop__jxrnf in range(len(tsxjo__bxjw)):
        eddnp__kya, value = tsxjo__bxjw[xlop__jxrnf]
        try:
            rnxz__jjb = get_const_value_inner(func_ir, eddnp__kya,
                arg_types, typemap, updated_containers)
            tpo__auco.append(rnxz__jjb)
            values.append(value)
        except GuardException as mdmpn__wmsh:
            require_const_map[eddnp__kya] = label
            cefm__slbo = True
    if cefm__slbo:
        raise GuardException
    return tpo__auco, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        tpo__auco = tuple(get_const_value_inner(func_ir, t[0], args) for t in
            build_map.items)
    except GuardException as mdmpn__wmsh:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in tpo__auco):
        raise BodoError(err_msg, loc)
    return tpo__auco


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    tpo__auco = _get_const_keys_from_dict(args, func_ir, build_map, err_msg,
        loc)
    svde__uqfil = []
    epeda__qdp = [bodo.transforms.typing_pass._create_const_var(zod__nitp,
        'dict_key', scope, loc, svde__uqfil) for zod__nitp in tpo__auco]
    uip__dchfm = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        tjr__dzrj = ir.Var(scope, mk_unique_var('sentinel'), loc)
        wbrnp__rsyf = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        svde__uqfil.append(ir.Assign(ir.Const('__bodo_tup', loc), tjr__dzrj,
            loc))
        njntk__qjcya = [tjr__dzrj] + epeda__qdp + uip__dchfm
        svde__uqfil.append(ir.Assign(ir.Expr.build_tuple(njntk__qjcya, loc),
            wbrnp__rsyf, loc))
        return (wbrnp__rsyf,), svde__uqfil
    else:
        fnmx__cdwl = ir.Var(scope, mk_unique_var('values_tup'), loc)
        kvch__zhe = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        svde__uqfil.append(ir.Assign(ir.Expr.build_tuple(uip__dchfm, loc),
            fnmx__cdwl, loc))
        svde__uqfil.append(ir.Assign(ir.Expr.build_tuple(epeda__qdp, loc),
            kvch__zhe, loc))
        return (fnmx__cdwl, kvch__zhe), svde__uqfil
