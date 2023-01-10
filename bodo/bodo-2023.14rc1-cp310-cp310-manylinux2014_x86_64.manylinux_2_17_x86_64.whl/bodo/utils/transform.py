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
    oxe__xrup = tuple(call_list)
    if oxe__xrup in no_side_effect_call_tuples:
        return True
    if oxe__xrup == (bodo.hiframes.pd_index_ext.init_range_index,):
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
    if len(oxe__xrup) == 1 and tuple in getattr(oxe__xrup[0], '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=False, add_default_globals=True):
    if replace_globals:
        jbf__bae = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math}
    else:
        jbf__bae = func.__globals__
    if extra_globals is not None:
        jbf__bae.update(extra_globals)
    if add_default_globals:
        jbf__bae.update({'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math})
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, jbf__bae, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[cvh__mom.name] for cvh__mom in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, jbf__bae)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        dzas__pkd = tuple(typing_info.typemap[cvh__mom.name] for cvh__mom in
            args)
        lrv__zer = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, dzas__pkd, {}, {}, flags)
        lrv__zer.run()
    dvgq__bwx = f_ir.blocks.popitem()[1]
    replace_arg_nodes(dvgq__bwx, args)
    kjda__lgp = dvgq__bwx.body[:-2]
    update_locs(kjda__lgp[len(args):], loc)
    for stmt in kjda__lgp[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        esve__ygf = dvgq__bwx.body[-2]
        assert is_assign(esve__ygf) and is_expr(esve__ygf.value, 'cast')
        uylv__zes = esve__ygf.value.value
        kjda__lgp.append(ir.Assign(uylv__zes, ret_var, loc))
    return kjda__lgp


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for xmowx__zay in stmt.list_vars():
            xmowx__zay.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        qxonu__bkwej = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        pgwwe__dzx, zpbp__nwq = qxonu__bkwej(stmt)
        return zpbp__nwq
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        kaunz__mxmc = get_const_value_inner(func_ir, var, arg_types,
            typemap, file_info=file_info)
        if isinstance(kaunz__mxmc, ir.UndefinedType):
            vxeb__hxq = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{vxeb__hxq}' is not defined", loc=loc)
    except GuardException as afiu__cjt:
        raise BodoError(err_msg, loc=loc)
    return kaunz__mxmc


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    mru__lutj = get_definition(func_ir, var)
    eir__ttea = None
    if typemap is not None:
        eir__ttea = typemap.get(var.name, None)
    if isinstance(mru__lutj, ir.Arg) and arg_types is not None:
        eir__ttea = arg_types[mru__lutj.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(eir__ttea):
        return get_literal_value(eir__ttea)
    if isinstance(mru__lutj, (ir.Const, ir.Global, ir.FreeVar)):
        kaunz__mxmc = mru__lutj.value
        return kaunz__mxmc
    if literalize_args and isinstance(mru__lutj, ir.Arg
        ) and can_literalize_type(eir__ttea, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({mru__lutj.index}, loc=var.
            loc, file_infos={mru__lutj.index: file_info} if file_info is not
            None else None)
    if is_expr(mru__lutj, 'binop'):
        if file_info and mru__lutj.fn == operator.add:
            try:
                rbcbw__sdgv = get_const_value_inner(func_ir, mru__lutj.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(rbcbw__sdgv, True)
                jtwa__fzqh = get_const_value_inner(func_ir, mru__lutj.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return mru__lutj.fn(rbcbw__sdgv, jtwa__fzqh)
            except (GuardException, BodoConstUpdatedError) as afiu__cjt:
                pass
            try:
                jtwa__fzqh = get_const_value_inner(func_ir, mru__lutj.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(jtwa__fzqh, False)
                rbcbw__sdgv = get_const_value_inner(func_ir, mru__lutj.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return mru__lutj.fn(rbcbw__sdgv, jtwa__fzqh)
            except (GuardException, BodoConstUpdatedError) as afiu__cjt:
                pass
        rbcbw__sdgv = get_const_value_inner(func_ir, mru__lutj.lhs,
            arg_types, typemap, updated_containers)
        jtwa__fzqh = get_const_value_inner(func_ir, mru__lutj.rhs,
            arg_types, typemap, updated_containers)
        return mru__lutj.fn(rbcbw__sdgv, jtwa__fzqh)
    if is_expr(mru__lutj, 'unary'):
        kaunz__mxmc = get_const_value_inner(func_ir, mru__lutj.value,
            arg_types, typemap, updated_containers)
        return mru__lutj.fn(kaunz__mxmc)
    if is_expr(mru__lutj, 'getattr') and typemap:
        inrc__sivo = typemap.get(mru__lutj.value.name, None)
        if isinstance(inrc__sivo, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and mru__lutj.attr == 'columns':
            return pd.Index(inrc__sivo.columns)
        if isinstance(inrc__sivo, types.SliceType):
            cgzd__lde = get_definition(func_ir, mru__lutj.value)
            require(is_call(cgzd__lde))
            homut__gjq = find_callname(func_ir, cgzd__lde)
            antb__wqc = False
            if homut__gjq == ('_normalize_slice', 'numba.cpython.unicode'):
                require(mru__lutj.attr in ('start', 'step'))
                cgzd__lde = get_definition(func_ir, cgzd__lde.args[0])
                antb__wqc = True
            require(find_callname(func_ir, cgzd__lde) == ('slice', 'builtins'))
            if len(cgzd__lde.args) == 1:
                if mru__lutj.attr == 'start':
                    return 0
                if mru__lutj.attr == 'step':
                    return 1
                require(mru__lutj.attr == 'stop')
                return get_const_value_inner(func_ir, cgzd__lde.args[0],
                    arg_types, typemap, updated_containers)
            if mru__lutj.attr == 'start':
                kaunz__mxmc = get_const_value_inner(func_ir, cgzd__lde.args
                    [0], arg_types, typemap, updated_containers)
                if kaunz__mxmc is None:
                    kaunz__mxmc = 0
                if antb__wqc:
                    require(kaunz__mxmc == 0)
                return kaunz__mxmc
            if mru__lutj.attr == 'stop':
                assert not antb__wqc
                return get_const_value_inner(func_ir, cgzd__lde.args[1],
                    arg_types, typemap, updated_containers)
            require(mru__lutj.attr == 'step')
            if len(cgzd__lde.args) == 2:
                return 1
            else:
                kaunz__mxmc = get_const_value_inner(func_ir, cgzd__lde.args
                    [2], arg_types, typemap, updated_containers)
                if kaunz__mxmc is None:
                    kaunz__mxmc = 1
                if antb__wqc:
                    require(kaunz__mxmc == 1)
                return kaunz__mxmc
    if is_expr(mru__lutj, 'getattr'):
        return getattr(get_const_value_inner(func_ir, mru__lutj.value,
            arg_types, typemap, updated_containers), mru__lutj.attr)
    if is_expr(mru__lutj, 'getitem'):
        value = get_const_value_inner(func_ir, mru__lutj.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, mru__lutj.index, arg_types,
            typemap, updated_containers)
        return value[index]
    naj__eqee = guard(find_callname, func_ir, mru__lutj, typemap)
    if naj__eqee is not None and len(naj__eqee) == 2 and naj__eqee[0
        ] == 'keys' and isinstance(naj__eqee[1], ir.Var):
        xjcv__mcs = mru__lutj.func
        mru__lutj = get_definition(func_ir, naj__eqee[1])
        lsomq__npe = naj__eqee[1].name
        if updated_containers and lsomq__npe in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                lsomq__npe, updated_containers[lsomq__npe]))
        require(is_expr(mru__lutj, 'build_map'))
        vals = [xmowx__zay[0] for xmowx__zay in mru__lutj.items]
        mde__yax = guard(get_definition, func_ir, xjcv__mcs)
        assert isinstance(mde__yax, ir.Expr) and mde__yax.attr == 'keys'
        mde__yax.attr = 'copy'
        return [get_const_value_inner(func_ir, xmowx__zay, arg_types,
            typemap, updated_containers) for xmowx__zay in vals]
    if is_expr(mru__lutj, 'build_map'):
        return {get_const_value_inner(func_ir, xmowx__zay[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            xmowx__zay[1], arg_types, typemap, updated_containers) for
            xmowx__zay in mru__lutj.items}
    if is_expr(mru__lutj, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, xmowx__zay, arg_types,
            typemap, updated_containers) for xmowx__zay in mru__lutj.items)
    if is_expr(mru__lutj, 'build_list'):
        return [get_const_value_inner(func_ir, xmowx__zay, arg_types,
            typemap, updated_containers) for xmowx__zay in mru__lutj.items]
    if is_expr(mru__lutj, 'build_set'):
        return {get_const_value_inner(func_ir, xmowx__zay, arg_types,
            typemap, updated_containers) for xmowx__zay in mru__lutj.items}
    if naj__eqee == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, mru__lutj.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if naj__eqee == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, mru__lutj.args[0],
            arg_types, typemap, updated_containers))
    if naj__eqee == ('range', 'builtins') and len(mru__lutj.args) == 1:
        return range(get_const_value_inner(func_ir, mru__lutj.args[0],
            arg_types, typemap, updated_containers))
    if naj__eqee == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, xmowx__zay,
            arg_types, typemap, updated_containers) for xmowx__zay in
            mru__lutj.args))
    if naj__eqee == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, mru__lutj.args[0],
            arg_types, typemap, updated_containers))
    if naj__eqee == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, mru__lutj.args[0],
            arg_types, typemap, updated_containers))
    if naj__eqee == ('format', 'builtins'):
        cvh__mom = get_const_value_inner(func_ir, mru__lutj.args[0],
            arg_types, typemap, updated_containers)
        amepu__arf = get_const_value_inner(func_ir, mru__lutj.args[1],
            arg_types, typemap, updated_containers) if len(mru__lutj.args
            ) > 1 else ''
        return format(cvh__mom, amepu__arf)
    if naj__eqee in (('init_binary_str_index', 'bodo.hiframes.pd_index_ext'
        ), ('init_numeric_index', 'bodo.hiframes.pd_index_ext'), (
        'init_categorical_index', 'bodo.hiframes.pd_index_ext'), (
        'init_datetime_index', 'bodo.hiframes.pd_index_ext'), (
        'init_timedelta_index', 'bodo.hiframes.pd_index_ext'), (
        'init_heter_index', 'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, mru__lutj.args[0],
            arg_types, typemap, updated_containers))
    if naj__eqee == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, mru__lutj.args[0],
            arg_types, typemap, updated_containers))
    if naj__eqee == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, mru__lutj.args[
            0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, mru__lutj.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            mru__lutj.args[2], arg_types, typemap, updated_containers))
    if naj__eqee == ('len', 'builtins') and typemap and isinstance(typemap.
        get(mru__lutj.args[0].name, None), types.BaseTuple):
        return len(typemap[mru__lutj.args[0].name])
    if naj__eqee == ('len', 'builtins'):
        apws__bvebu = guard(get_definition, func_ir, mru__lutj.args[0])
        if isinstance(apws__bvebu, ir.Expr) and apws__bvebu.op in (
            'build_tuple', 'build_list', 'build_set', 'build_map'):
            return len(apws__bvebu.items)
        return len(get_const_value_inner(func_ir, mru__lutj.args[0],
            arg_types, typemap, updated_containers))
    if naj__eqee == ('CategoricalDtype', 'pandas'):
        kws = dict(mru__lutj.kws)
        gee__aqkmg = get_call_expr_arg('CategoricalDtype', mru__lutj.args,
            kws, 0, 'categories', '')
        puwzr__kqgb = get_call_expr_arg('CategoricalDtype', mru__lutj.args,
            kws, 1, 'ordered', False)
        if puwzr__kqgb is not False:
            puwzr__kqgb = get_const_value_inner(func_ir, puwzr__kqgb,
                arg_types, typemap, updated_containers)
        if gee__aqkmg == '':
            gee__aqkmg = None
        else:
            gee__aqkmg = get_const_value_inner(func_ir, gee__aqkmg,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(gee__aqkmg, puwzr__kqgb)
    if naj__eqee == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, mru__lutj.args[0],
            arg_types, typemap, updated_containers))
    if naj__eqee is not None and naj__eqee[1] == 'numpy' and naj__eqee[0
        ] in _np_type_names:
        return getattr(np, naj__eqee[0])(get_const_value_inner(func_ir,
            mru__lutj.args[0], arg_types, typemap, updated_containers))
    if naj__eqee is not None and len(naj__eqee) == 2 and naj__eqee[1
        ] == 'pandas' and naj__eqee[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, naj__eqee[0])()
    if naj__eqee is not None and len(naj__eqee) == 2 and isinstance(naj__eqee
        [1], ir.Var):
        kaunz__mxmc = get_const_value_inner(func_ir, naj__eqee[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, xmowx__zay, arg_types,
            typemap, updated_containers) for xmowx__zay in mru__lutj.args]
        kws = {qrxk__jzuh[0]: get_const_value_inner(func_ir, qrxk__jzuh[1],
            arg_types, typemap, updated_containers) for qrxk__jzuh in
            mru__lutj.kws}
        return getattr(kaunz__mxmc, naj__eqee[0])(*args, **kws)
    if naj__eqee is not None and len(naj__eqee) == 2 and naj__eqee[1
        ] == 'bodo' and naj__eqee[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, xmowx__zay, arg_types,
            typemap, updated_containers) for xmowx__zay in mru__lutj.args)
        kwargs = {vxeb__hxq: get_const_value_inner(func_ir, xmowx__zay,
            arg_types, typemap, updated_containers) for vxeb__hxq,
            xmowx__zay in dict(mru__lutj.kws).items()}
        return getattr(bodo, naj__eqee[0])(*args, **kwargs)
    if is_call(mru__lutj) and typemap and isinstance(typemap.get(mru__lutj.
        func.name, None), types.Dispatcher):
        py_func = typemap[mru__lutj.func.name].dispatcher.py_func
        require(mru__lutj.vararg is None)
        args = tuple(get_const_value_inner(func_ir, xmowx__zay, arg_types,
            typemap, updated_containers) for xmowx__zay in mru__lutj.args)
        kwargs = {vxeb__hxq: get_const_value_inner(func_ir, xmowx__zay,
            arg_types, typemap, updated_containers) for vxeb__hxq,
            xmowx__zay in dict(mru__lutj.kws).items()}
        arg_types = tuple(bodo.typeof(xmowx__zay) for xmowx__zay in args)
        kw_types = {blaj__wrpzs: bodo.typeof(xmowx__zay) for blaj__wrpzs,
            xmowx__zay in kwargs.items()}
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
    f_ir, typemap, nocj__ljgee, nocj__ljgee = bodo.compiler.get_func_type_info(
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
                    bzjil__bkbs = guard(get_definition, f_ir, rhs.func)
                    if isinstance(bzjil__bkbs, ir.Const) and isinstance(
                        bzjil__bkbs.value, numba.core.dispatcher.
                        ObjModeLiftedWith):
                        return False
                    gslga__fcn = guard(find_callname, f_ir, rhs)
                    if gslga__fcn is None:
                        return False
                    func_name, mcwqz__dvy = gslga__fcn
                    if mcwqz__dvy == 'pandas' and func_name.startswith('read_'
                        ):
                        return False
                    if gslga__fcn in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if gslga__fcn == ('File', 'h5py'):
                        return False
                    if isinstance(mcwqz__dvy, ir.Var):
                        eir__ttea = typemap[mcwqz__dvy.name]
                        if isinstance(eir__ttea, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(eir__ttea, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(eir__ttea, bodo.LoggingLoggerType):
                            return False
                        if str(eir__ttea).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            mcwqz__dvy), ir.Arg)):
                            return False
                    if mcwqz__dvy in ('numpy.random', 'time', 'logging',
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
        stii__dol = func.literal_value.code
        phso__hcbr = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            phso__hcbr = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(phso__hcbr, stii__dol)
        fix_struct_return(f_ir)
        typemap, kdewx__vmrdn, heofv__vvxy, nocj__ljgee = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, heofv__vvxy, kdewx__vmrdn = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, heofv__vvxy, kdewx__vmrdn = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, heofv__vvxy, kdewx__vmrdn = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(kdewx__vmrdn, types.DictType):
        tore__jfht = guard(get_struct_keynames, f_ir, typemap)
        if tore__jfht is not None:
            kdewx__vmrdn = StructType((kdewx__vmrdn.value_type,) * len(
                tore__jfht), tore__jfht)
    if is_udf and isinstance(kdewx__vmrdn, (SeriesType,
        HeterogeneousSeriesType)):
        jet__wtst = numba.core.registry.cpu_target.typing_context
        vbfd__bbqs = numba.core.registry.cpu_target.target_context
        sgti__uczhs = bodo.transforms.series_pass.SeriesPass(f_ir,
            jet__wtst, vbfd__bbqs, typemap, heofv__vvxy, {})
        qow__yalo = sgti__uczhs.run()
        if qow__yalo:
            qow__yalo = sgti__uczhs.run()
            if qow__yalo:
                sgti__uczhs.run()
        uqict__pci = compute_cfg_from_blocks(f_ir.blocks)
        shor__hhd = [guard(_get_const_series_info, f_ir.blocks[ide__pdv],
            f_ir, typemap) for ide__pdv in uqict__pci.exit_points() if
            isinstance(f_ir.blocks[ide__pdv].body[-1], ir.Return)]
        if None in shor__hhd or len(pd.Series(shor__hhd).unique()) != 1:
            kdewx__vmrdn.const_info = None
        else:
            kdewx__vmrdn.const_info = shor__hhd[0]
    return kdewx__vmrdn


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    ivbsl__fmyk = block.body[-1].value
    wqni__jpkl = get_definition(f_ir, ivbsl__fmyk)
    require(is_expr(wqni__jpkl, 'cast'))
    wqni__jpkl = get_definition(f_ir, wqni__jpkl.value)
    require(is_call(wqni__jpkl) and find_callname(f_ir, wqni__jpkl) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    ffph__ldjc = wqni__jpkl.args[1]
    ajur__lpbj = tuple(get_const_value_inner(f_ir, ffph__ldjc, typemap=typemap)
        )
    if isinstance(typemap[ivbsl__fmyk.name], HeterogeneousSeriesType):
        return len(typemap[ivbsl__fmyk.name].data), ajur__lpbj
    sztyi__olkjj = wqni__jpkl.args[0]
    blpnq__suaik = get_definition(f_ir, sztyi__olkjj)
    func_name, tgveg__hrt = find_callname(f_ir, blpnq__suaik)
    if is_call(blpnq__suaik) and bodo.utils.utils.is_alloc_callname(func_name,
        tgveg__hrt):
        xdo__qgl = blpnq__suaik.args[0]
        cfp__driyl = get_const_value_inner(f_ir, xdo__qgl, typemap=typemap)
        return cfp__driyl, ajur__lpbj
    if is_call(blpnq__suaik) and find_callname(f_ir, blpnq__suaik) in [(
        'asarray', 'numpy'), ('str_arr_from_sequence',
        'bodo.libs.str_arr_ext'), ('build_nullable_tuple',
        'bodo.libs.nullable_tuple_ext')]:
        sztyi__olkjj = blpnq__suaik.args[0]
        blpnq__suaik = get_definition(f_ir, sztyi__olkjj)
    require(is_expr(blpnq__suaik, 'build_tuple') or is_expr(blpnq__suaik,
        'build_list'))
    return len(blpnq__suaik.items), ajur__lpbj


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    jsvmz__otrl = []
    cpata__zofj = []
    values = []
    for blaj__wrpzs, xmowx__zay in build_map.items:
        hbf__etl = find_const(f_ir, blaj__wrpzs)
        require(isinstance(hbf__etl, str))
        cpata__zofj.append(hbf__etl)
        jsvmz__otrl.append(blaj__wrpzs)
        values.append(xmowx__zay)
    vcu__pbdtj = ir.Var(scope, mk_unique_var('val_tup'), loc)
    ufs__caz = ir.Assign(ir.Expr.build_tuple(values, loc), vcu__pbdtj, loc)
    f_ir._definitions[vcu__pbdtj.name] = [ufs__caz.value]
    djcwh__xdsd = ir.Var(scope, mk_unique_var('key_tup'), loc)
    hkpn__ptxlo = ir.Assign(ir.Expr.build_tuple(jsvmz__otrl, loc),
        djcwh__xdsd, loc)
    f_ir._definitions[djcwh__xdsd.name] = [hkpn__ptxlo.value]
    if typemap is not None:
        typemap[vcu__pbdtj.name] = types.Tuple([typemap[xmowx__zay.name] for
            xmowx__zay in values])
        typemap[djcwh__xdsd.name] = types.Tuple([typemap[xmowx__zay.name] for
            xmowx__zay in jsvmz__otrl])
    return cpata__zofj, vcu__pbdtj, ufs__caz, djcwh__xdsd, hkpn__ptxlo


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    tuh__ywyrd = block.body[-1].value
    unkrj__nzryu = guard(get_definition, f_ir, tuh__ywyrd)
    require(is_expr(unkrj__nzryu, 'cast'))
    wqni__jpkl = guard(get_definition, f_ir, unkrj__nzryu.value)
    require(is_expr(wqni__jpkl, 'build_map'))
    require(len(wqni__jpkl.items) > 0)
    loc = block.loc
    scope = block.scope
    cpata__zofj, vcu__pbdtj, ufs__caz, djcwh__xdsd, hkpn__ptxlo = (
        extract_keyvals_from_struct_map(f_ir, wqni__jpkl, loc, scope))
    esxgu__anvf = ir.Var(scope, mk_unique_var('conv_call'), loc)
    wzz__uan = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), esxgu__anvf, loc)
    f_ir._definitions[esxgu__anvf.name] = [wzz__uan.value]
    rekmi__kaa = ir.Var(scope, mk_unique_var('struct_val'), loc)
    orae__lfikd = ir.Assign(ir.Expr.call(esxgu__anvf, [vcu__pbdtj,
        djcwh__xdsd], {}, loc), rekmi__kaa, loc)
    f_ir._definitions[rekmi__kaa.name] = [orae__lfikd.value]
    unkrj__nzryu.value = rekmi__kaa
    wqni__jpkl.items = [(blaj__wrpzs, blaj__wrpzs) for blaj__wrpzs,
        nocj__ljgee in wqni__jpkl.items]
    block.body = block.body[:-2] + [ufs__caz, hkpn__ptxlo, wzz__uan,
        orae__lfikd] + block.body[-2:]
    return tuple(cpata__zofj)


def get_struct_keynames(f_ir, typemap):
    uqict__pci = compute_cfg_from_blocks(f_ir.blocks)
    cjug__ibw = list(uqict__pci.exit_points())[0]
    block = f_ir.blocks[cjug__ibw]
    require(isinstance(block.body[-1], ir.Return))
    tuh__ywyrd = block.body[-1].value
    unkrj__nzryu = guard(get_definition, f_ir, tuh__ywyrd)
    require(is_expr(unkrj__nzryu, 'cast'))
    wqni__jpkl = guard(get_definition, f_ir, unkrj__nzryu.value)
    require(is_call(wqni__jpkl) and find_callname(f_ir, wqni__jpkl) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[wqni__jpkl.args[1].name])


def fix_struct_return(f_ir):
    huylv__hqiw = None
    uqict__pci = compute_cfg_from_blocks(f_ir.blocks)
    for cjug__ibw in uqict__pci.exit_points():
        huylv__hqiw = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            cjug__ibw], cjug__ibw)
    return huylv__hqiw


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    yuy__nrsi = ir.Block(ir.Scope(None, loc), loc)
    yuy__nrsi.body = node_list
    build_definitions({(0): yuy__nrsi}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(xmowx__zay) for xmowx__zay in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    fghms__yzr = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(fghms__yzr, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for gdra__mnepo in range(len(vals) - 1, -1, -1):
        xmowx__zay = vals[gdra__mnepo]
        if isinstance(xmowx__zay, str) and xmowx__zay.startswith(
            NESTED_TUP_SENTINEL):
            iaew__ljp = int(xmowx__zay[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:gdra__mnepo]) + (
                tuple(vals[gdra__mnepo + 1:gdra__mnepo + iaew__ljp + 1]),) +
                tuple(vals[gdra__mnepo + iaew__ljp + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    cvh__mom = None
    if len(args) > arg_no and arg_no >= 0:
        cvh__mom = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        cvh__mom = kws[arg_name]
    if cvh__mom is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return cvh__mom


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
    jbf__bae = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        jbf__bae.update(extra_globals)
    func.__globals__.update(jbf__bae)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            mzjk__svvz = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[mzjk__svvz.name] = types.literal(default)
            except:
                pass_info.typemap[mzjk__svvz.name] = numba.typeof(default)
            afmqs__xpqxx = ir.Assign(ir.Const(default, loc), mzjk__svvz, loc)
            pre_nodes.append(afmqs__xpqxx)
            return mzjk__svvz
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    dzas__pkd = tuple(pass_info.typemap[xmowx__zay.name] for xmowx__zay in args
        )
    if const:
        tyepq__raf = []
        for gdra__mnepo, cvh__mom in enumerate(args):
            kaunz__mxmc = guard(find_const, pass_info.func_ir, cvh__mom)
            if kaunz__mxmc:
                tyepq__raf.append(types.literal(kaunz__mxmc))
            else:
                tyepq__raf.append(dzas__pkd[gdra__mnepo])
        dzas__pkd = tuple(tyepq__raf)
    return ReplaceFunc(func, dzas__pkd, args, jbf__bae, inline_bodo_calls,
        run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(jqhm__msf) for jqhm__msf in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        nki__sall = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {nki__sall} = 0\n', (nki__sall,)
    if isinstance(t, ArrayItemArrayType):
        wfl__acpk, oatd__nikb = gen_init_varsize_alloc_sizes(t.dtype)
        nki__sall = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {nki__sall} = 0\n' + wfl__acpk, (nki__sall,) + oatd__nikb
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
        return 1 + sum(get_type_alloc_counts(jqhm__msf.dtype) for jqhm__msf in
            t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(jqhm__msf) for jqhm__msf in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(jqhm__msf) for jqhm__msf in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    yopf__pab = typing_context.resolve_getattr(obj_dtype, func_name)
    if yopf__pab is None:
        gsie__tbrp = types.misc.Module(np)
        try:
            yopf__pab = typing_context.resolve_getattr(gsie__tbrp, func_name)
        except AttributeError as afiu__cjt:
            yopf__pab = None
        if yopf__pab is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return yopf__pab


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    yopf__pab = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(yopf__pab, types.BoundFunction):
        if axis is not None:
            byn__uujr = yopf__pab.get_call_type(typing_context, (), {'axis':
                axis})
        else:
            byn__uujr = yopf__pab.get_call_type(typing_context, (), {})
        return byn__uujr.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(yopf__pab):
            byn__uujr = yopf__pab.get_call_type(typing_context, (obj_dtype,
                ), {})
            return byn__uujr.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    yopf__pab = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(yopf__pab, types.BoundFunction):
        ncasu__ezdd = yopf__pab.template
        if axis is not None:
            return ncasu__ezdd._overload_func(obj_dtype, axis=axis)
        else:
            return ncasu__ezdd._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    jyu__xii = get_definition(func_ir, dict_var)
    require(isinstance(jyu__xii, ir.Expr))
    require(jyu__xii.op == 'build_map')
    btvt__rizo = jyu__xii.items
    jsvmz__otrl = []
    values = []
    ayu__gbyxf = False
    for gdra__mnepo in range(len(btvt__rizo)):
        urbf__sgb, value = btvt__rizo[gdra__mnepo]
        try:
            smjv__spcgg = get_const_value_inner(func_ir, urbf__sgb,
                arg_types, typemap, updated_containers)
            jsvmz__otrl.append(smjv__spcgg)
            values.append(value)
        except GuardException as afiu__cjt:
            require_const_map[urbf__sgb] = label
            ayu__gbyxf = True
    if ayu__gbyxf:
        raise GuardException
    return jsvmz__otrl, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        jsvmz__otrl = tuple(get_const_value_inner(func_ir, t[0], args) for
            t in build_map.items)
    except GuardException as afiu__cjt:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in jsvmz__otrl):
        raise BodoError(err_msg, loc)
    return jsvmz__otrl


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    jsvmz__otrl = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    vnfa__swbl = []
    iwgl__vbkh = [bodo.transforms.typing_pass._create_const_var(blaj__wrpzs,
        'dict_key', scope, loc, vnfa__swbl) for blaj__wrpzs in jsvmz__otrl]
    kczk__xxzw = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        khpwj__kejvl = ir.Var(scope, mk_unique_var('sentinel'), loc)
        rwow__zlyap = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        vnfa__swbl.append(ir.Assign(ir.Const('__bodo_tup', loc),
            khpwj__kejvl, loc))
        mrpw__rjbp = [khpwj__kejvl] + iwgl__vbkh + kczk__xxzw
        vnfa__swbl.append(ir.Assign(ir.Expr.build_tuple(mrpw__rjbp, loc),
            rwow__zlyap, loc))
        return (rwow__zlyap,), vnfa__swbl
    else:
        fmasy__aizq = ir.Var(scope, mk_unique_var('values_tup'), loc)
        zkgcw__builo = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        vnfa__swbl.append(ir.Assign(ir.Expr.build_tuple(kczk__xxzw, loc),
            fmasy__aizq, loc))
        vnfa__swbl.append(ir.Assign(ir.Expr.build_tuple(iwgl__vbkh, loc),
            zkgcw__builo, loc))
        return (fmasy__aizq, zkgcw__builo), vnfa__swbl
