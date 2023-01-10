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
    gjzud__xfoy = tuple(call_list)
    if gjzud__xfoy in no_side_effect_call_tuples:
        return True
    if gjzud__xfoy == (bodo.hiframes.pd_index_ext.init_range_index,):
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
    if len(gjzud__xfoy) == 1 and tuple in getattr(gjzud__xfoy[0], '__mro__', ()
        ):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=False, add_default_globals=True):
    if replace_globals:
        vyti__uhq = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math}
    else:
        vyti__uhq = func.__globals__
    if extra_globals is not None:
        vyti__uhq.update(extra_globals)
    if add_default_globals:
        vyti__uhq.update({'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math})
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, vyti__uhq, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[gphd__pqabj.name] for gphd__pqabj in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, vyti__uhq)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        deqq__xrw = tuple(typing_info.typemap[gphd__pqabj.name] for
            gphd__pqabj in args)
        pvf__ceig = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, deqq__xrw, {}, {}, flags)
        pvf__ceig.run()
    fsdl__ppkby = f_ir.blocks.popitem()[1]
    replace_arg_nodes(fsdl__ppkby, args)
    ojkt__kfig = fsdl__ppkby.body[:-2]
    update_locs(ojkt__kfig[len(args):], loc)
    for stmt in ojkt__kfig[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        esy__qelv = fsdl__ppkby.body[-2]
        assert is_assign(esy__qelv) and is_expr(esy__qelv.value, 'cast')
        hysig__xsce = esy__qelv.value.value
        ojkt__kfig.append(ir.Assign(hysig__xsce, ret_var, loc))
    return ojkt__kfig


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for ydk__tpsk in stmt.list_vars():
            ydk__tpsk.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        ydiig__sdsx = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        hss__grd, yktuu__ncchf = ydiig__sdsx(stmt)
        return yktuu__ncchf
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        lss__joyvu = get_const_value_inner(func_ir, var, arg_types, typemap,
            file_info=file_info)
        if isinstance(lss__joyvu, ir.UndefinedType):
            vbpid__axc = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{vbpid__axc}' is not defined", loc=loc)
    except GuardException as dostf__xxuyt:
        raise BodoError(err_msg, loc=loc)
    return lss__joyvu


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    xcaik__tmsw = get_definition(func_ir, var)
    xtafw__luk = None
    if typemap is not None:
        xtafw__luk = typemap.get(var.name, None)
    if isinstance(xcaik__tmsw, ir.Arg) and arg_types is not None:
        xtafw__luk = arg_types[xcaik__tmsw.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(xtafw__luk):
        return get_literal_value(xtafw__luk)
    if isinstance(xcaik__tmsw, (ir.Const, ir.Global, ir.FreeVar)):
        lss__joyvu = xcaik__tmsw.value
        return lss__joyvu
    if literalize_args and isinstance(xcaik__tmsw, ir.Arg
        ) and can_literalize_type(xtafw__luk, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({xcaik__tmsw.index}, loc=
            var.loc, file_infos={xcaik__tmsw.index: file_info} if file_info
             is not None else None)
    if is_expr(xcaik__tmsw, 'binop'):
        if file_info and xcaik__tmsw.fn == operator.add:
            try:
                gql__ppa = get_const_value_inner(func_ir, xcaik__tmsw.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(gql__ppa, True)
                cxs__qprs = get_const_value_inner(func_ir, xcaik__tmsw.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return xcaik__tmsw.fn(gql__ppa, cxs__qprs)
            except (GuardException, BodoConstUpdatedError) as dostf__xxuyt:
                pass
            try:
                cxs__qprs = get_const_value_inner(func_ir, xcaik__tmsw.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(cxs__qprs, False)
                gql__ppa = get_const_value_inner(func_ir, xcaik__tmsw.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return xcaik__tmsw.fn(gql__ppa, cxs__qprs)
            except (GuardException, BodoConstUpdatedError) as dostf__xxuyt:
                pass
        gql__ppa = get_const_value_inner(func_ir, xcaik__tmsw.lhs,
            arg_types, typemap, updated_containers)
        cxs__qprs = get_const_value_inner(func_ir, xcaik__tmsw.rhs,
            arg_types, typemap, updated_containers)
        return xcaik__tmsw.fn(gql__ppa, cxs__qprs)
    if is_expr(xcaik__tmsw, 'unary'):
        lss__joyvu = get_const_value_inner(func_ir, xcaik__tmsw.value,
            arg_types, typemap, updated_containers)
        return xcaik__tmsw.fn(lss__joyvu)
    if is_expr(xcaik__tmsw, 'getattr') and typemap:
        iiwig__ymwth = typemap.get(xcaik__tmsw.value.name, None)
        if isinstance(iiwig__ymwth, bodo.hiframes.pd_dataframe_ext.
            DataFrameType) and xcaik__tmsw.attr == 'columns':
            return pd.Index(iiwig__ymwth.columns)
        if isinstance(iiwig__ymwth, types.SliceType):
            aynw__lhn = get_definition(func_ir, xcaik__tmsw.value)
            require(is_call(aynw__lhn))
            uao__cvo = find_callname(func_ir, aynw__lhn)
            ksfx__uxxk = False
            if uao__cvo == ('_normalize_slice', 'numba.cpython.unicode'):
                require(xcaik__tmsw.attr in ('start', 'step'))
                aynw__lhn = get_definition(func_ir, aynw__lhn.args[0])
                ksfx__uxxk = True
            require(find_callname(func_ir, aynw__lhn) == ('slice', 'builtins'))
            if len(aynw__lhn.args) == 1:
                if xcaik__tmsw.attr == 'start':
                    return 0
                if xcaik__tmsw.attr == 'step':
                    return 1
                require(xcaik__tmsw.attr == 'stop')
                return get_const_value_inner(func_ir, aynw__lhn.args[0],
                    arg_types, typemap, updated_containers)
            if xcaik__tmsw.attr == 'start':
                lss__joyvu = get_const_value_inner(func_ir, aynw__lhn.args[
                    0], arg_types, typemap, updated_containers)
                if lss__joyvu is None:
                    lss__joyvu = 0
                if ksfx__uxxk:
                    require(lss__joyvu == 0)
                return lss__joyvu
            if xcaik__tmsw.attr == 'stop':
                assert not ksfx__uxxk
                return get_const_value_inner(func_ir, aynw__lhn.args[1],
                    arg_types, typemap, updated_containers)
            require(xcaik__tmsw.attr == 'step')
            if len(aynw__lhn.args) == 2:
                return 1
            else:
                lss__joyvu = get_const_value_inner(func_ir, aynw__lhn.args[
                    2], arg_types, typemap, updated_containers)
                if lss__joyvu is None:
                    lss__joyvu = 1
                if ksfx__uxxk:
                    require(lss__joyvu == 1)
                return lss__joyvu
    if is_expr(xcaik__tmsw, 'getattr'):
        return getattr(get_const_value_inner(func_ir, xcaik__tmsw.value,
            arg_types, typemap, updated_containers), xcaik__tmsw.attr)
    if is_expr(xcaik__tmsw, 'getitem'):
        value = get_const_value_inner(func_ir, xcaik__tmsw.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, xcaik__tmsw.index, arg_types,
            typemap, updated_containers)
        return value[index]
    dspk__olv = guard(find_callname, func_ir, xcaik__tmsw, typemap)
    if dspk__olv is not None and len(dspk__olv) == 2 and dspk__olv[0
        ] == 'keys' and isinstance(dspk__olv[1], ir.Var):
        iaxj__rcxvc = xcaik__tmsw.func
        xcaik__tmsw = get_definition(func_ir, dspk__olv[1])
        rmpws__kyu = dspk__olv[1].name
        if updated_containers and rmpws__kyu in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                rmpws__kyu, updated_containers[rmpws__kyu]))
        require(is_expr(xcaik__tmsw, 'build_map'))
        vals = [ydk__tpsk[0] for ydk__tpsk in xcaik__tmsw.items]
        bnpn__tqny = guard(get_definition, func_ir, iaxj__rcxvc)
        assert isinstance(bnpn__tqny, ir.Expr) and bnpn__tqny.attr == 'keys'
        bnpn__tqny.attr = 'copy'
        return [get_const_value_inner(func_ir, ydk__tpsk, arg_types,
            typemap, updated_containers) for ydk__tpsk in vals]
    if is_expr(xcaik__tmsw, 'build_map'):
        return {get_const_value_inner(func_ir, ydk__tpsk[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            ydk__tpsk[1], arg_types, typemap, updated_containers) for
            ydk__tpsk in xcaik__tmsw.items}
    if is_expr(xcaik__tmsw, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, ydk__tpsk, arg_types,
            typemap, updated_containers) for ydk__tpsk in xcaik__tmsw.items)
    if is_expr(xcaik__tmsw, 'build_list'):
        return [get_const_value_inner(func_ir, ydk__tpsk, arg_types,
            typemap, updated_containers) for ydk__tpsk in xcaik__tmsw.items]
    if is_expr(xcaik__tmsw, 'build_set'):
        return {get_const_value_inner(func_ir, ydk__tpsk, arg_types,
            typemap, updated_containers) for ydk__tpsk in xcaik__tmsw.items}
    if dspk__olv == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, xcaik__tmsw.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if dspk__olv == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, xcaik__tmsw.args[0],
            arg_types, typemap, updated_containers))
    if dspk__olv == ('range', 'builtins') and len(xcaik__tmsw.args) == 1:
        return range(get_const_value_inner(func_ir, xcaik__tmsw.args[0],
            arg_types, typemap, updated_containers))
    if dspk__olv == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, ydk__tpsk,
            arg_types, typemap, updated_containers) for ydk__tpsk in
            xcaik__tmsw.args))
    if dspk__olv == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, xcaik__tmsw.args[0],
            arg_types, typemap, updated_containers))
    if dspk__olv == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, xcaik__tmsw.args[0],
            arg_types, typemap, updated_containers))
    if dspk__olv == ('format', 'builtins'):
        gphd__pqabj = get_const_value_inner(func_ir, xcaik__tmsw.args[0],
            arg_types, typemap, updated_containers)
        zmb__ifyfr = get_const_value_inner(func_ir, xcaik__tmsw.args[1],
            arg_types, typemap, updated_containers) if len(xcaik__tmsw.args
            ) > 1 else ''
        return format(gphd__pqabj, zmb__ifyfr)
    if dspk__olv in (('init_binary_str_index', 'bodo.hiframes.pd_index_ext'
        ), ('init_numeric_index', 'bodo.hiframes.pd_index_ext'), (
        'init_categorical_index', 'bodo.hiframes.pd_index_ext'), (
        'init_datetime_index', 'bodo.hiframes.pd_index_ext'), (
        'init_timedelta_index', 'bodo.hiframes.pd_index_ext'), (
        'init_heter_index', 'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, xcaik__tmsw.args[0],
            arg_types, typemap, updated_containers))
    if dspk__olv == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, xcaik__tmsw.args[0],
            arg_types, typemap, updated_containers))
    if dspk__olv == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, xcaik__tmsw.
            args[0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, xcaik__tmsw.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            xcaik__tmsw.args[2], arg_types, typemap, updated_containers))
    if dspk__olv == ('len', 'builtins') and typemap and isinstance(typemap.
        get(xcaik__tmsw.args[0].name, None), types.BaseTuple):
        return len(typemap[xcaik__tmsw.args[0].name])
    if dspk__olv == ('len', 'builtins'):
        zjoy__yrgs = guard(get_definition, func_ir, xcaik__tmsw.args[0])
        if isinstance(zjoy__yrgs, ir.Expr) and zjoy__yrgs.op in ('build_tuple',
            'build_list', 'build_set', 'build_map'):
            return len(zjoy__yrgs.items)
        return len(get_const_value_inner(func_ir, xcaik__tmsw.args[0],
            arg_types, typemap, updated_containers))
    if dspk__olv == ('CategoricalDtype', 'pandas'):
        kws = dict(xcaik__tmsw.kws)
        vbc__gry = get_call_expr_arg('CategoricalDtype', xcaik__tmsw.args,
            kws, 0, 'categories', '')
        hbbku__fnbew = get_call_expr_arg('CategoricalDtype', xcaik__tmsw.
            args, kws, 1, 'ordered', False)
        if hbbku__fnbew is not False:
            hbbku__fnbew = get_const_value_inner(func_ir, hbbku__fnbew,
                arg_types, typemap, updated_containers)
        if vbc__gry == '':
            vbc__gry = None
        else:
            vbc__gry = get_const_value_inner(func_ir, vbc__gry, arg_types,
                typemap, updated_containers)
        return pd.CategoricalDtype(vbc__gry, hbbku__fnbew)
    if dspk__olv == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, xcaik__tmsw.args[0],
            arg_types, typemap, updated_containers))
    if dspk__olv is not None and dspk__olv[1] == 'numpy' and dspk__olv[0
        ] in _np_type_names:
        return getattr(np, dspk__olv[0])(get_const_value_inner(func_ir,
            xcaik__tmsw.args[0], arg_types, typemap, updated_containers))
    if dspk__olv is not None and len(dspk__olv) == 2 and dspk__olv[1
        ] == 'pandas' and dspk__olv[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, dspk__olv[0])()
    if dspk__olv is not None and len(dspk__olv) == 2 and isinstance(dspk__olv
        [1], ir.Var):
        lss__joyvu = get_const_value_inner(func_ir, dspk__olv[1], arg_types,
            typemap, updated_containers)
        args = [get_const_value_inner(func_ir, ydk__tpsk, arg_types,
            typemap, updated_containers) for ydk__tpsk in xcaik__tmsw.args]
        kws = {dyii__kvc[0]: get_const_value_inner(func_ir, dyii__kvc[1],
            arg_types, typemap, updated_containers) for dyii__kvc in
            xcaik__tmsw.kws}
        return getattr(lss__joyvu, dspk__olv[0])(*args, **kws)
    if dspk__olv is not None and len(dspk__olv) == 2 and dspk__olv[1
        ] == 'bodo' and dspk__olv[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, ydk__tpsk, arg_types,
            typemap, updated_containers) for ydk__tpsk in xcaik__tmsw.args)
        kwargs = {vbpid__axc: get_const_value_inner(func_ir, ydk__tpsk,
            arg_types, typemap, updated_containers) for vbpid__axc,
            ydk__tpsk in dict(xcaik__tmsw.kws).items()}
        return getattr(bodo, dspk__olv[0])(*args, **kwargs)
    if is_call(xcaik__tmsw) and typemap and isinstance(typemap.get(
        xcaik__tmsw.func.name, None), types.Dispatcher):
        py_func = typemap[xcaik__tmsw.func.name].dispatcher.py_func
        require(xcaik__tmsw.vararg is None)
        args = tuple(get_const_value_inner(func_ir, ydk__tpsk, arg_types,
            typemap, updated_containers) for ydk__tpsk in xcaik__tmsw.args)
        kwargs = {vbpid__axc: get_const_value_inner(func_ir, ydk__tpsk,
            arg_types, typemap, updated_containers) for vbpid__axc,
            ydk__tpsk in dict(xcaik__tmsw.kws).items()}
        arg_types = tuple(bodo.typeof(ydk__tpsk) for ydk__tpsk in args)
        kw_types = {yjdme__iuhw: bodo.typeof(ydk__tpsk) for yjdme__iuhw,
            ydk__tpsk in kwargs.items()}
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
    f_ir, typemap, bzx__dhy, bzx__dhy = bodo.compiler.get_func_type_info(
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
                    jamk__ncjdw = guard(get_definition, f_ir, rhs.func)
                    if isinstance(jamk__ncjdw, ir.Const) and isinstance(
                        jamk__ncjdw.value, numba.core.dispatcher.
                        ObjModeLiftedWith):
                        return False
                    stsip__onkzz = guard(find_callname, f_ir, rhs)
                    if stsip__onkzz is None:
                        return False
                    func_name, mnmjz__bcb = stsip__onkzz
                    if mnmjz__bcb == 'pandas' and func_name.startswith('read_'
                        ):
                        return False
                    if stsip__onkzz in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if stsip__onkzz == ('File', 'h5py'):
                        return False
                    if isinstance(mnmjz__bcb, ir.Var):
                        xtafw__luk = typemap[mnmjz__bcb.name]
                        if isinstance(xtafw__luk, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(xtafw__luk, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(xtafw__luk, bodo.LoggingLoggerType):
                            return False
                        if str(xtafw__luk).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            mnmjz__bcb), ir.Arg)):
                            return False
                    if mnmjz__bcb in ('numpy.random', 'time', 'logging',
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
        txjh__zof = func.literal_value.code
        iftwf__uaikc = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            iftwf__uaikc = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(iftwf__uaikc, txjh__zof)
        fix_struct_return(f_ir)
        typemap, uxkd__pws, elt__bci, bzx__dhy = (numba.core.typed_passes.
            type_inference_stage(typing_context, target_context, f_ir,
            arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, elt__bci, uxkd__pws = bodo.compiler.get_func_type_info(
            py_func, arg_types, kw_types)
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, elt__bci, uxkd__pws = bodo.compiler.get_func_type_info(
            py_func, arg_types, kw_types)
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, elt__bci, uxkd__pws = bodo.compiler.get_func_type_info(
            py_func, arg_types, kw_types)
    if is_udf and isinstance(uxkd__pws, types.DictType):
        jsnqq__xjldd = guard(get_struct_keynames, f_ir, typemap)
        if jsnqq__xjldd is not None:
            uxkd__pws = StructType((uxkd__pws.value_type,) * len(
                jsnqq__xjldd), jsnqq__xjldd)
    if is_udf and isinstance(uxkd__pws, (SeriesType, HeterogeneousSeriesType)):
        mhj__hkxmm = numba.core.registry.cpu_target.typing_context
        gijch__ouwer = numba.core.registry.cpu_target.target_context
        ppq__kwvvd = bodo.transforms.series_pass.SeriesPass(f_ir,
            mhj__hkxmm, gijch__ouwer, typemap, elt__bci, {})
        jap__pwlb = ppq__kwvvd.run()
        if jap__pwlb:
            jap__pwlb = ppq__kwvvd.run()
            if jap__pwlb:
                ppq__kwvvd.run()
        tynx__rdt = compute_cfg_from_blocks(f_ir.blocks)
        hxmbq__ukyc = [guard(_get_const_series_info, f_ir.blocks[
            ymsu__qvogj], f_ir, typemap) for ymsu__qvogj in tynx__rdt.
            exit_points() if isinstance(f_ir.blocks[ymsu__qvogj].body[-1],
            ir.Return)]
        if None in hxmbq__ukyc or len(pd.Series(hxmbq__ukyc).unique()) != 1:
            uxkd__pws.const_info = None
        else:
            uxkd__pws.const_info = hxmbq__ukyc[0]
    return uxkd__pws


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    iair__oqqc = block.body[-1].value
    kob__zflp = get_definition(f_ir, iair__oqqc)
    require(is_expr(kob__zflp, 'cast'))
    kob__zflp = get_definition(f_ir, kob__zflp.value)
    require(is_call(kob__zflp) and find_callname(f_ir, kob__zflp) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    eym__kycd = kob__zflp.args[1]
    qfzgj__zbxi = tuple(get_const_value_inner(f_ir, eym__kycd, typemap=typemap)
        )
    if isinstance(typemap[iair__oqqc.name], HeterogeneousSeriesType):
        return len(typemap[iair__oqqc.name].data), qfzgj__zbxi
    mgmpl__dpv = kob__zflp.args[0]
    fxhlq__gvge = get_definition(f_ir, mgmpl__dpv)
    func_name, yhzs__tal = find_callname(f_ir, fxhlq__gvge)
    if is_call(fxhlq__gvge) and bodo.utils.utils.is_alloc_callname(func_name,
        yhzs__tal):
        pyn__fclex = fxhlq__gvge.args[0]
        mpiur__hxkc = get_const_value_inner(f_ir, pyn__fclex, typemap=typemap)
        return mpiur__hxkc, qfzgj__zbxi
    if is_call(fxhlq__gvge) and find_callname(f_ir, fxhlq__gvge) in [(
        'asarray', 'numpy'), ('str_arr_from_sequence',
        'bodo.libs.str_arr_ext'), ('build_nullable_tuple',
        'bodo.libs.nullable_tuple_ext')]:
        mgmpl__dpv = fxhlq__gvge.args[0]
        fxhlq__gvge = get_definition(f_ir, mgmpl__dpv)
    require(is_expr(fxhlq__gvge, 'build_tuple') or is_expr(fxhlq__gvge,
        'build_list'))
    return len(fxhlq__gvge.items), qfzgj__zbxi


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    bdwln__jpf = []
    vbpmw__wwf = []
    values = []
    for yjdme__iuhw, ydk__tpsk in build_map.items:
        sog__ilpns = find_const(f_ir, yjdme__iuhw)
        require(isinstance(sog__ilpns, str))
        vbpmw__wwf.append(sog__ilpns)
        bdwln__jpf.append(yjdme__iuhw)
        values.append(ydk__tpsk)
    iwq__dbrqw = ir.Var(scope, mk_unique_var('val_tup'), loc)
    xemya__uch = ir.Assign(ir.Expr.build_tuple(values, loc), iwq__dbrqw, loc)
    f_ir._definitions[iwq__dbrqw.name] = [xemya__uch.value]
    tas__bpadr = ir.Var(scope, mk_unique_var('key_tup'), loc)
    obc__iyr = ir.Assign(ir.Expr.build_tuple(bdwln__jpf, loc), tas__bpadr, loc)
    f_ir._definitions[tas__bpadr.name] = [obc__iyr.value]
    if typemap is not None:
        typemap[iwq__dbrqw.name] = types.Tuple([typemap[ydk__tpsk.name] for
            ydk__tpsk in values])
        typemap[tas__bpadr.name] = types.Tuple([typemap[ydk__tpsk.name] for
            ydk__tpsk in bdwln__jpf])
    return vbpmw__wwf, iwq__dbrqw, xemya__uch, tas__bpadr, obc__iyr


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    qzuaz__psi = block.body[-1].value
    vyttj__nqxc = guard(get_definition, f_ir, qzuaz__psi)
    require(is_expr(vyttj__nqxc, 'cast'))
    kob__zflp = guard(get_definition, f_ir, vyttj__nqxc.value)
    require(is_expr(kob__zflp, 'build_map'))
    require(len(kob__zflp.items) > 0)
    loc = block.loc
    scope = block.scope
    vbpmw__wwf, iwq__dbrqw, xemya__uch, tas__bpadr, obc__iyr = (
        extract_keyvals_from_struct_map(f_ir, kob__zflp, loc, scope))
    nbqfy__ixfrn = ir.Var(scope, mk_unique_var('conv_call'), loc)
    whba__vlm = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), nbqfy__ixfrn, loc)
    f_ir._definitions[nbqfy__ixfrn.name] = [whba__vlm.value]
    cckvl__lji = ir.Var(scope, mk_unique_var('struct_val'), loc)
    izaz__edlc = ir.Assign(ir.Expr.call(nbqfy__ixfrn, [iwq__dbrqw,
        tas__bpadr], {}, loc), cckvl__lji, loc)
    f_ir._definitions[cckvl__lji.name] = [izaz__edlc.value]
    vyttj__nqxc.value = cckvl__lji
    kob__zflp.items = [(yjdme__iuhw, yjdme__iuhw) for yjdme__iuhw, bzx__dhy in
        kob__zflp.items]
    block.body = block.body[:-2] + [xemya__uch, obc__iyr, whba__vlm, izaz__edlc
        ] + block.body[-2:]
    return tuple(vbpmw__wwf)


def get_struct_keynames(f_ir, typemap):
    tynx__rdt = compute_cfg_from_blocks(f_ir.blocks)
    pbid__ezex = list(tynx__rdt.exit_points())[0]
    block = f_ir.blocks[pbid__ezex]
    require(isinstance(block.body[-1], ir.Return))
    qzuaz__psi = block.body[-1].value
    vyttj__nqxc = guard(get_definition, f_ir, qzuaz__psi)
    require(is_expr(vyttj__nqxc, 'cast'))
    kob__zflp = guard(get_definition, f_ir, vyttj__nqxc.value)
    require(is_call(kob__zflp) and find_callname(f_ir, kob__zflp) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[kob__zflp.args[1].name])


def fix_struct_return(f_ir):
    eltvp__ohwif = None
    tynx__rdt = compute_cfg_from_blocks(f_ir.blocks)
    for pbid__ezex in tynx__rdt.exit_points():
        eltvp__ohwif = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            pbid__ezex], pbid__ezex)
    return eltvp__ohwif


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    nwuh__uqsq = ir.Block(ir.Scope(None, loc), loc)
    nwuh__uqsq.body = node_list
    build_definitions({(0): nwuh__uqsq}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(ydk__tpsk) for ydk__tpsk in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    elxin__panme = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(elxin__panme, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for enyar__rhs in range(len(vals) - 1, -1, -1):
        ydk__tpsk = vals[enyar__rhs]
        if isinstance(ydk__tpsk, str) and ydk__tpsk.startswith(
            NESTED_TUP_SENTINEL):
            crsf__kdbe = int(ydk__tpsk[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:enyar__rhs]) + (
                tuple(vals[enyar__rhs + 1:enyar__rhs + crsf__kdbe + 1]),) +
                tuple(vals[enyar__rhs + crsf__kdbe + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    gphd__pqabj = None
    if len(args) > arg_no and arg_no >= 0:
        gphd__pqabj = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        gphd__pqabj = kws[arg_name]
    if gphd__pqabj is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return gphd__pqabj


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
    vyti__uhq = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        vyti__uhq.update(extra_globals)
    func.__globals__.update(vyti__uhq)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            lfjy__rdnvi = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[lfjy__rdnvi.name] = types.literal(default)
            except:
                pass_info.typemap[lfjy__rdnvi.name] = numba.typeof(default)
            rxdh__neeyf = ir.Assign(ir.Const(default, loc), lfjy__rdnvi, loc)
            pre_nodes.append(rxdh__neeyf)
            return lfjy__rdnvi
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    deqq__xrw = tuple(pass_info.typemap[ydk__tpsk.name] for ydk__tpsk in args)
    if const:
        pwsc__lbx = []
        for enyar__rhs, gphd__pqabj in enumerate(args):
            lss__joyvu = guard(find_const, pass_info.func_ir, gphd__pqabj)
            if lss__joyvu:
                pwsc__lbx.append(types.literal(lss__joyvu))
            else:
                pwsc__lbx.append(deqq__xrw[enyar__rhs])
        deqq__xrw = tuple(pwsc__lbx)
    return ReplaceFunc(func, deqq__xrw, args, vyti__uhq, inline_bodo_calls,
        run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(xrr__znaxt) for xrr__znaxt in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        cra__pku = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {cra__pku} = 0\n', (cra__pku,)
    if isinstance(t, ArrayItemArrayType):
        blmwt__qpl, qrnp__lku = gen_init_varsize_alloc_sizes(t.dtype)
        cra__pku = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {cra__pku} = 0\n' + blmwt__qpl, (cra__pku,) + qrnp__lku
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
        return 1 + sum(get_type_alloc_counts(xrr__znaxt.dtype) for
            xrr__znaxt in t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(xrr__znaxt) for xrr__znaxt in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(xrr__znaxt) for xrr__znaxt in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    sqm__vwfr = typing_context.resolve_getattr(obj_dtype, func_name)
    if sqm__vwfr is None:
        mzhz__pcs = types.misc.Module(np)
        try:
            sqm__vwfr = typing_context.resolve_getattr(mzhz__pcs, func_name)
        except AttributeError as dostf__xxuyt:
            sqm__vwfr = None
        if sqm__vwfr is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return sqm__vwfr


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    sqm__vwfr = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(sqm__vwfr, types.BoundFunction):
        if axis is not None:
            nzj__rba = sqm__vwfr.get_call_type(typing_context, (), {'axis':
                axis})
        else:
            nzj__rba = sqm__vwfr.get_call_type(typing_context, (), {})
        return nzj__rba.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(sqm__vwfr):
            nzj__rba = sqm__vwfr.get_call_type(typing_context, (obj_dtype,), {}
                )
            return nzj__rba.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    sqm__vwfr = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(sqm__vwfr, types.BoundFunction):
        dbjkj__epwyj = sqm__vwfr.template
        if axis is not None:
            return dbjkj__epwyj._overload_func(obj_dtype, axis=axis)
        else:
            return dbjkj__epwyj._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    tomzd__ghotq = get_definition(func_ir, dict_var)
    require(isinstance(tomzd__ghotq, ir.Expr))
    require(tomzd__ghotq.op == 'build_map')
    caxz__ofc = tomzd__ghotq.items
    bdwln__jpf = []
    values = []
    dwxmw__bikd = False
    for enyar__rhs in range(len(caxz__ofc)):
        tgndu__eusz, value = caxz__ofc[enyar__rhs]
        try:
            rkqxw__bybw = get_const_value_inner(func_ir, tgndu__eusz,
                arg_types, typemap, updated_containers)
            bdwln__jpf.append(rkqxw__bybw)
            values.append(value)
        except GuardException as dostf__xxuyt:
            require_const_map[tgndu__eusz] = label
            dwxmw__bikd = True
    if dwxmw__bikd:
        raise GuardException
    return bdwln__jpf, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        bdwln__jpf = tuple(get_const_value_inner(func_ir, t[0], args) for t in
            build_map.items)
    except GuardException as dostf__xxuyt:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in bdwln__jpf):
        raise BodoError(err_msg, loc)
    return bdwln__jpf


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    bdwln__jpf = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    vhzk__upvpq = []
    ayhl__lvm = [bodo.transforms.typing_pass._create_const_var(yjdme__iuhw,
        'dict_key', scope, loc, vhzk__upvpq) for yjdme__iuhw in bdwln__jpf]
    vazoq__zfucq = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        pjdgn__nboua = ir.Var(scope, mk_unique_var('sentinel'), loc)
        elsd__lnil = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        vhzk__upvpq.append(ir.Assign(ir.Const('__bodo_tup', loc),
            pjdgn__nboua, loc))
        fapvv__shl = [pjdgn__nboua] + ayhl__lvm + vazoq__zfucq
        vhzk__upvpq.append(ir.Assign(ir.Expr.build_tuple(fapvv__shl, loc),
            elsd__lnil, loc))
        return (elsd__lnil,), vhzk__upvpq
    else:
        sedzq__zuu = ir.Var(scope, mk_unique_var('values_tup'), loc)
        iwiq__xds = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        vhzk__upvpq.append(ir.Assign(ir.Expr.build_tuple(vazoq__zfucq, loc),
            sedzq__zuu, loc))
        vhzk__upvpq.append(ir.Assign(ir.Expr.build_tuple(ayhl__lvm, loc),
            iwiq__xds, loc))
        return (sedzq__zuu, iwiq__xds), vhzk__upvpq
