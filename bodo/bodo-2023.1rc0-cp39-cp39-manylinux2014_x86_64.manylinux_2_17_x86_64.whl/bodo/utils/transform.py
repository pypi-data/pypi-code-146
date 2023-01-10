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
    qlipu__qbyd = tuple(call_list)
    if qlipu__qbyd in no_side_effect_call_tuples:
        return True
    if qlipu__qbyd == (bodo.hiframes.pd_index_ext.init_range_index,):
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
    if len(qlipu__qbyd) == 1 and tuple in getattr(qlipu__qbyd[0], '__mro__', ()
        ):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=False, add_default_globals=True):
    if replace_globals:
        obj__uxum = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math}
    else:
        obj__uxum = func.__globals__
    if extra_globals is not None:
        obj__uxum.update(extra_globals)
    if add_default_globals:
        obj__uxum.update({'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math})
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, obj__uxum, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[zfl__wjcu.name] for zfl__wjcu in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, obj__uxum)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        brow__azpfg = tuple(typing_info.typemap[zfl__wjcu.name] for
            zfl__wjcu in args)
        vyvvf__aoyjm = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, brow__azpfg, {}, {}, flags)
        vyvvf__aoyjm.run()
    oxhfx__tyzkt = f_ir.blocks.popitem()[1]
    replace_arg_nodes(oxhfx__tyzkt, args)
    hdz__nnvhb = oxhfx__tyzkt.body[:-2]
    update_locs(hdz__nnvhb[len(args):], loc)
    for stmt in hdz__nnvhb[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        wzcr__isxrm = oxhfx__tyzkt.body[-2]
        assert is_assign(wzcr__isxrm) and is_expr(wzcr__isxrm.value, 'cast')
        pol__qwh = wzcr__isxrm.value.value
        hdz__nnvhb.append(ir.Assign(pol__qwh, ret_var, loc))
    return hdz__nnvhb


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for buas__lqir in stmt.list_vars():
            buas__lqir.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        ncejr__zfosc = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        ptgw__tgdz, bblrz__hbz = ncejr__zfosc(stmt)
        return bblrz__hbz
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        wlt__njj = get_const_value_inner(func_ir, var, arg_types, typemap,
            file_info=file_info)
        if isinstance(wlt__njj, ir.UndefinedType):
            hfn__zyvi = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{hfn__zyvi}' is not defined", loc=loc)
    except GuardException as grlwf__dxand:
        raise BodoError(err_msg, loc=loc)
    return wlt__njj


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    soqlc__xbq = get_definition(func_ir, var)
    rju__ygq = None
    if typemap is not None:
        rju__ygq = typemap.get(var.name, None)
    if isinstance(soqlc__xbq, ir.Arg) and arg_types is not None:
        rju__ygq = arg_types[soqlc__xbq.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(rju__ygq):
        return get_literal_value(rju__ygq)
    if isinstance(soqlc__xbq, (ir.Const, ir.Global, ir.FreeVar)):
        wlt__njj = soqlc__xbq.value
        return wlt__njj
    if literalize_args and isinstance(soqlc__xbq, ir.Arg
        ) and can_literalize_type(rju__ygq, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({soqlc__xbq.index}, loc=var
            .loc, file_infos={soqlc__xbq.index: file_info} if file_info is not
            None else None)
    if is_expr(soqlc__xbq, 'binop'):
        if file_info and soqlc__xbq.fn == operator.add:
            try:
                bxf__trk = get_const_value_inner(func_ir, soqlc__xbq.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(bxf__trk, True)
                nqhh__tvpk = get_const_value_inner(func_ir, soqlc__xbq.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return soqlc__xbq.fn(bxf__trk, nqhh__tvpk)
            except (GuardException, BodoConstUpdatedError) as grlwf__dxand:
                pass
            try:
                nqhh__tvpk = get_const_value_inner(func_ir, soqlc__xbq.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(nqhh__tvpk, False)
                bxf__trk = get_const_value_inner(func_ir, soqlc__xbq.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return soqlc__xbq.fn(bxf__trk, nqhh__tvpk)
            except (GuardException, BodoConstUpdatedError) as grlwf__dxand:
                pass
        bxf__trk = get_const_value_inner(func_ir, soqlc__xbq.lhs, arg_types,
            typemap, updated_containers)
        nqhh__tvpk = get_const_value_inner(func_ir, soqlc__xbq.rhs,
            arg_types, typemap, updated_containers)
        return soqlc__xbq.fn(bxf__trk, nqhh__tvpk)
    if is_expr(soqlc__xbq, 'unary'):
        wlt__njj = get_const_value_inner(func_ir, soqlc__xbq.value,
            arg_types, typemap, updated_containers)
        return soqlc__xbq.fn(wlt__njj)
    if is_expr(soqlc__xbq, 'getattr') and typemap:
        ngjo__cwzpq = typemap.get(soqlc__xbq.value.name, None)
        if isinstance(ngjo__cwzpq, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and soqlc__xbq.attr == 'columns':
            return pd.Index(ngjo__cwzpq.columns)
        if isinstance(ngjo__cwzpq, types.SliceType):
            zqtff__ecym = get_definition(func_ir, soqlc__xbq.value)
            require(is_call(zqtff__ecym))
            nkvlh__fqm = find_callname(func_ir, zqtff__ecym)
            xkk__ujyra = False
            if nkvlh__fqm == ('_normalize_slice', 'numba.cpython.unicode'):
                require(soqlc__xbq.attr in ('start', 'step'))
                zqtff__ecym = get_definition(func_ir, zqtff__ecym.args[0])
                xkk__ujyra = True
            require(find_callname(func_ir, zqtff__ecym) == ('slice',
                'builtins'))
            if len(zqtff__ecym.args) == 1:
                if soqlc__xbq.attr == 'start':
                    return 0
                if soqlc__xbq.attr == 'step':
                    return 1
                require(soqlc__xbq.attr == 'stop')
                return get_const_value_inner(func_ir, zqtff__ecym.args[0],
                    arg_types, typemap, updated_containers)
            if soqlc__xbq.attr == 'start':
                wlt__njj = get_const_value_inner(func_ir, zqtff__ecym.args[
                    0], arg_types, typemap, updated_containers)
                if wlt__njj is None:
                    wlt__njj = 0
                if xkk__ujyra:
                    require(wlt__njj == 0)
                return wlt__njj
            if soqlc__xbq.attr == 'stop':
                assert not xkk__ujyra
                return get_const_value_inner(func_ir, zqtff__ecym.args[1],
                    arg_types, typemap, updated_containers)
            require(soqlc__xbq.attr == 'step')
            if len(zqtff__ecym.args) == 2:
                return 1
            else:
                wlt__njj = get_const_value_inner(func_ir, zqtff__ecym.args[
                    2], arg_types, typemap, updated_containers)
                if wlt__njj is None:
                    wlt__njj = 1
                if xkk__ujyra:
                    require(wlt__njj == 1)
                return wlt__njj
    if is_expr(soqlc__xbq, 'getattr'):
        return getattr(get_const_value_inner(func_ir, soqlc__xbq.value,
            arg_types, typemap, updated_containers), soqlc__xbq.attr)
    if is_expr(soqlc__xbq, 'getitem'):
        value = get_const_value_inner(func_ir, soqlc__xbq.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, soqlc__xbq.index, arg_types,
            typemap, updated_containers)
        return value[index]
    pmjco__lic = guard(find_callname, func_ir, soqlc__xbq, typemap)
    if pmjco__lic is not None and len(pmjco__lic) == 2 and pmjco__lic[0
        ] == 'keys' and isinstance(pmjco__lic[1], ir.Var):
        gytzm__ydtjj = soqlc__xbq.func
        soqlc__xbq = get_definition(func_ir, pmjco__lic[1])
        ryq__did = pmjco__lic[1].name
        if updated_containers and ryq__did in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                ryq__did, updated_containers[ryq__did]))
        require(is_expr(soqlc__xbq, 'build_map'))
        vals = [buas__lqir[0] for buas__lqir in soqlc__xbq.items]
        kkn__kzjdd = guard(get_definition, func_ir, gytzm__ydtjj)
        assert isinstance(kkn__kzjdd, ir.Expr) and kkn__kzjdd.attr == 'keys'
        kkn__kzjdd.attr = 'copy'
        return [get_const_value_inner(func_ir, buas__lqir, arg_types,
            typemap, updated_containers) for buas__lqir in vals]
    if is_expr(soqlc__xbq, 'build_map'):
        return {get_const_value_inner(func_ir, buas__lqir[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            buas__lqir[1], arg_types, typemap, updated_containers) for
            buas__lqir in soqlc__xbq.items}
    if is_expr(soqlc__xbq, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, buas__lqir, arg_types,
            typemap, updated_containers) for buas__lqir in soqlc__xbq.items)
    if is_expr(soqlc__xbq, 'build_list'):
        return [get_const_value_inner(func_ir, buas__lqir, arg_types,
            typemap, updated_containers) for buas__lqir in soqlc__xbq.items]
    if is_expr(soqlc__xbq, 'build_set'):
        return {get_const_value_inner(func_ir, buas__lqir, arg_types,
            typemap, updated_containers) for buas__lqir in soqlc__xbq.items}
    if pmjco__lic == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, soqlc__xbq.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if pmjco__lic == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, soqlc__xbq.args[0],
            arg_types, typemap, updated_containers))
    if pmjco__lic == ('range', 'builtins') and len(soqlc__xbq.args) == 1:
        return range(get_const_value_inner(func_ir, soqlc__xbq.args[0],
            arg_types, typemap, updated_containers))
    if pmjco__lic == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, buas__lqir,
            arg_types, typemap, updated_containers) for buas__lqir in
            soqlc__xbq.args))
    if pmjco__lic == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, soqlc__xbq.args[0],
            arg_types, typemap, updated_containers))
    if pmjco__lic == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, soqlc__xbq.args[0],
            arg_types, typemap, updated_containers))
    if pmjco__lic == ('format', 'builtins'):
        zfl__wjcu = get_const_value_inner(func_ir, soqlc__xbq.args[0],
            arg_types, typemap, updated_containers)
        gcq__gmbu = get_const_value_inner(func_ir, soqlc__xbq.args[1],
            arg_types, typemap, updated_containers) if len(soqlc__xbq.args
            ) > 1 else ''
        return format(zfl__wjcu, gcq__gmbu)
    if pmjco__lic in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, soqlc__xbq.args[0],
            arg_types, typemap, updated_containers))
    if pmjco__lic == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, soqlc__xbq.args[0],
            arg_types, typemap, updated_containers))
    if pmjco__lic == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, soqlc__xbq.args
            [0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, soqlc__xbq.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            soqlc__xbq.args[2], arg_types, typemap, updated_containers))
    if pmjco__lic == ('len', 'builtins') and typemap and isinstance(typemap
        .get(soqlc__xbq.args[0].name, None), types.BaseTuple):
        return len(typemap[soqlc__xbq.args[0].name])
    if pmjco__lic == ('len', 'builtins'):
        zltz__zkts = guard(get_definition, func_ir, soqlc__xbq.args[0])
        if isinstance(zltz__zkts, ir.Expr) and zltz__zkts.op in ('build_tuple',
            'build_list', 'build_set', 'build_map'):
            return len(zltz__zkts.items)
        return len(get_const_value_inner(func_ir, soqlc__xbq.args[0],
            arg_types, typemap, updated_containers))
    if pmjco__lic == ('CategoricalDtype', 'pandas'):
        kws = dict(soqlc__xbq.kws)
        gnyaw__swa = get_call_expr_arg('CategoricalDtype', soqlc__xbq.args,
            kws, 0, 'categories', '')
        uvhvd__mlp = get_call_expr_arg('CategoricalDtype', soqlc__xbq.args,
            kws, 1, 'ordered', False)
        if uvhvd__mlp is not False:
            uvhvd__mlp = get_const_value_inner(func_ir, uvhvd__mlp,
                arg_types, typemap, updated_containers)
        if gnyaw__swa == '':
            gnyaw__swa = None
        else:
            gnyaw__swa = get_const_value_inner(func_ir, gnyaw__swa,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(gnyaw__swa, uvhvd__mlp)
    if pmjco__lic == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, soqlc__xbq.args[0],
            arg_types, typemap, updated_containers))
    if pmjco__lic is not None and pmjco__lic[1] == 'numpy' and pmjco__lic[0
        ] in _np_type_names:
        return getattr(np, pmjco__lic[0])(get_const_value_inner(func_ir,
            soqlc__xbq.args[0], arg_types, typemap, updated_containers))
    if pmjco__lic is not None and len(pmjco__lic) == 2 and pmjco__lic[1
        ] == 'pandas' and pmjco__lic[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, pmjco__lic[0])()
    if pmjco__lic is not None and len(pmjco__lic) == 2 and isinstance(
        pmjco__lic[1], ir.Var):
        wlt__njj = get_const_value_inner(func_ir, pmjco__lic[1], arg_types,
            typemap, updated_containers)
        args = [get_const_value_inner(func_ir, buas__lqir, arg_types,
            typemap, updated_containers) for buas__lqir in soqlc__xbq.args]
        kws = {zwfoe__bctt[0]: get_const_value_inner(func_ir, zwfoe__bctt[1
            ], arg_types, typemap, updated_containers) for zwfoe__bctt in
            soqlc__xbq.kws}
        return getattr(wlt__njj, pmjco__lic[0])(*args, **kws)
    if pmjco__lic is not None and len(pmjco__lic) == 2 and pmjco__lic[1
        ] == 'bodo' and pmjco__lic[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, buas__lqir, arg_types,
            typemap, updated_containers) for buas__lqir in soqlc__xbq.args)
        kwargs = {hfn__zyvi: get_const_value_inner(func_ir, buas__lqir,
            arg_types, typemap, updated_containers) for hfn__zyvi,
            buas__lqir in dict(soqlc__xbq.kws).items()}
        return getattr(bodo, pmjco__lic[0])(*args, **kwargs)
    if is_call(soqlc__xbq) and typemap and isinstance(typemap.get(
        soqlc__xbq.func.name, None), types.Dispatcher):
        py_func = typemap[soqlc__xbq.func.name].dispatcher.py_func
        require(soqlc__xbq.vararg is None)
        args = tuple(get_const_value_inner(func_ir, buas__lqir, arg_types,
            typemap, updated_containers) for buas__lqir in soqlc__xbq.args)
        kwargs = {hfn__zyvi: get_const_value_inner(func_ir, buas__lqir,
            arg_types, typemap, updated_containers) for hfn__zyvi,
            buas__lqir in dict(soqlc__xbq.kws).items()}
        arg_types = tuple(bodo.typeof(buas__lqir) for buas__lqir in args)
        kw_types = {lcg__zolcd: bodo.typeof(buas__lqir) for lcg__zolcd,
            buas__lqir in kwargs.items()}
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
    f_ir, typemap, kox__njdd, kox__njdd = bodo.compiler.get_func_type_info(
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
                    lgg__dfev = guard(get_definition, f_ir, rhs.func)
                    if isinstance(lgg__dfev, ir.Const) and isinstance(lgg__dfev
                        .value, numba.core.dispatcher.ObjModeLiftedWith):
                        return False
                    iomnz__mtxgo = guard(find_callname, f_ir, rhs)
                    if iomnz__mtxgo is None:
                        return False
                    func_name, mfle__vyg = iomnz__mtxgo
                    if mfle__vyg == 'pandas' and func_name.startswith('read_'):
                        return False
                    if iomnz__mtxgo in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if iomnz__mtxgo == ('File', 'h5py'):
                        return False
                    if isinstance(mfle__vyg, ir.Var):
                        rju__ygq = typemap[mfle__vyg.name]
                        if isinstance(rju__ygq, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(rju__ygq, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(rju__ygq, bodo.LoggingLoggerType):
                            return False
                        if str(rju__ygq).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            mfle__vyg), ir.Arg)):
                            return False
                    if mfle__vyg in ('numpy.random', 'time', 'logging',
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
        gdbbp__nwrz = func.literal_value.code
        uun__sfasa = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            uun__sfasa = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(uun__sfasa, gdbbp__nwrz)
        fix_struct_return(f_ir)
        typemap, wfd__sdzvp, woyw__clt, kox__njdd = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, woyw__clt, wfd__sdzvp = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, woyw__clt, wfd__sdzvp = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, woyw__clt, wfd__sdzvp = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(wfd__sdzvp, types.DictType):
        mux__kpn = guard(get_struct_keynames, f_ir, typemap)
        if mux__kpn is not None:
            wfd__sdzvp = StructType((wfd__sdzvp.value_type,) * len(mux__kpn
                ), mux__kpn)
    if is_udf and isinstance(wfd__sdzvp, (SeriesType, HeterogeneousSeriesType)
        ):
        euql__estl = numba.core.registry.cpu_target.typing_context
        tuo__cez = numba.core.registry.cpu_target.target_context
        lff__ibqz = bodo.transforms.series_pass.SeriesPass(f_ir, euql__estl,
            tuo__cez, typemap, woyw__clt, {})
        wkoi__hbs = lff__ibqz.run()
        if wkoi__hbs:
            wkoi__hbs = lff__ibqz.run()
            if wkoi__hbs:
                lff__ibqz.run()
        iqq__rxbp = compute_cfg_from_blocks(f_ir.blocks)
        ibly__apdxa = [guard(_get_const_series_info, f_ir.blocks[tzb__zcpv],
            f_ir, typemap) for tzb__zcpv in iqq__rxbp.exit_points() if
            isinstance(f_ir.blocks[tzb__zcpv].body[-1], ir.Return)]
        if None in ibly__apdxa or len(pd.Series(ibly__apdxa).unique()) != 1:
            wfd__sdzvp.const_info = None
        else:
            wfd__sdzvp.const_info = ibly__apdxa[0]
    return wfd__sdzvp


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    zbbd__tggtr = block.body[-1].value
    evjp__htb = get_definition(f_ir, zbbd__tggtr)
    require(is_expr(evjp__htb, 'cast'))
    evjp__htb = get_definition(f_ir, evjp__htb.value)
    require(is_call(evjp__htb) and find_callname(f_ir, evjp__htb) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    xhnc__lqyfc = evjp__htb.args[1]
    jsk__jbcf = tuple(get_const_value_inner(f_ir, xhnc__lqyfc, typemap=typemap)
        )
    if isinstance(typemap[zbbd__tggtr.name], HeterogeneousSeriesType):
        return len(typemap[zbbd__tggtr.name].data), jsk__jbcf
    orgtm__ksn = evjp__htb.args[0]
    rrf__szwbd = get_definition(f_ir, orgtm__ksn)
    func_name, szya__zcgjl = find_callname(f_ir, rrf__szwbd)
    if is_call(rrf__szwbd) and bodo.utils.utils.is_alloc_callname(func_name,
        szya__zcgjl):
        dhgk__zxmgc = rrf__szwbd.args[0]
        fwjeu__zvkw = get_const_value_inner(f_ir, dhgk__zxmgc, typemap=typemap)
        return fwjeu__zvkw, jsk__jbcf
    if is_call(rrf__szwbd) and find_callname(f_ir, rrf__szwbd) in [(
        'asarray', 'numpy'), ('str_arr_from_sequence',
        'bodo.libs.str_arr_ext'), ('build_nullable_tuple',
        'bodo.libs.nullable_tuple_ext')]:
        orgtm__ksn = rrf__szwbd.args[0]
        rrf__szwbd = get_definition(f_ir, orgtm__ksn)
    require(is_expr(rrf__szwbd, 'build_tuple') or is_expr(rrf__szwbd,
        'build_list'))
    return len(rrf__szwbd.items), jsk__jbcf


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    sgqlo__ctd = []
    ptqnh__madgr = []
    values = []
    for lcg__zolcd, buas__lqir in build_map.items:
        icjgv__gdj = find_const(f_ir, lcg__zolcd)
        require(isinstance(icjgv__gdj, str))
        ptqnh__madgr.append(icjgv__gdj)
        sgqlo__ctd.append(lcg__zolcd)
        values.append(buas__lqir)
    ypoyk__idq = ir.Var(scope, mk_unique_var('val_tup'), loc)
    hcqay__xesb = ir.Assign(ir.Expr.build_tuple(values, loc), ypoyk__idq, loc)
    f_ir._definitions[ypoyk__idq.name] = [hcqay__xesb.value]
    pfd__yoxe = ir.Var(scope, mk_unique_var('key_tup'), loc)
    qnv__azk = ir.Assign(ir.Expr.build_tuple(sgqlo__ctd, loc), pfd__yoxe, loc)
    f_ir._definitions[pfd__yoxe.name] = [qnv__azk.value]
    if typemap is not None:
        typemap[ypoyk__idq.name] = types.Tuple([typemap[buas__lqir.name] for
            buas__lqir in values])
        typemap[pfd__yoxe.name] = types.Tuple([typemap[buas__lqir.name] for
            buas__lqir in sgqlo__ctd])
    return ptqnh__madgr, ypoyk__idq, hcqay__xesb, pfd__yoxe, qnv__azk


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    eflr__ryj = block.body[-1].value
    wetw__wjbx = guard(get_definition, f_ir, eflr__ryj)
    require(is_expr(wetw__wjbx, 'cast'))
    evjp__htb = guard(get_definition, f_ir, wetw__wjbx.value)
    require(is_expr(evjp__htb, 'build_map'))
    require(len(evjp__htb.items) > 0)
    loc = block.loc
    scope = block.scope
    ptqnh__madgr, ypoyk__idq, hcqay__xesb, pfd__yoxe, qnv__azk = (
        extract_keyvals_from_struct_map(f_ir, evjp__htb, loc, scope))
    kxrpv__hfgep = ir.Var(scope, mk_unique_var('conv_call'), loc)
    dqqro__ewdw = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), kxrpv__hfgep, loc)
    f_ir._definitions[kxrpv__hfgep.name] = [dqqro__ewdw.value]
    qvh__uvq = ir.Var(scope, mk_unique_var('struct_val'), loc)
    vthew__pyuo = ir.Assign(ir.Expr.call(kxrpv__hfgep, [ypoyk__idq,
        pfd__yoxe], {}, loc), qvh__uvq, loc)
    f_ir._definitions[qvh__uvq.name] = [vthew__pyuo.value]
    wetw__wjbx.value = qvh__uvq
    evjp__htb.items = [(lcg__zolcd, lcg__zolcd) for lcg__zolcd, kox__njdd in
        evjp__htb.items]
    block.body = block.body[:-2] + [hcqay__xesb, qnv__azk, dqqro__ewdw,
        vthew__pyuo] + block.body[-2:]
    return tuple(ptqnh__madgr)


def get_struct_keynames(f_ir, typemap):
    iqq__rxbp = compute_cfg_from_blocks(f_ir.blocks)
    qjaih__uuxkm = list(iqq__rxbp.exit_points())[0]
    block = f_ir.blocks[qjaih__uuxkm]
    require(isinstance(block.body[-1], ir.Return))
    eflr__ryj = block.body[-1].value
    wetw__wjbx = guard(get_definition, f_ir, eflr__ryj)
    require(is_expr(wetw__wjbx, 'cast'))
    evjp__htb = guard(get_definition, f_ir, wetw__wjbx.value)
    require(is_call(evjp__htb) and find_callname(f_ir, evjp__htb) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[evjp__htb.args[1].name])


def fix_struct_return(f_ir):
    ijhj__wibgq = None
    iqq__rxbp = compute_cfg_from_blocks(f_ir.blocks)
    for qjaih__uuxkm in iqq__rxbp.exit_points():
        ijhj__wibgq = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            qjaih__uuxkm], qjaih__uuxkm)
    return ijhj__wibgq


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    lnw__nsbhs = ir.Block(ir.Scope(None, loc), loc)
    lnw__nsbhs.body = node_list
    build_definitions({(0): lnw__nsbhs}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(buas__lqir) for buas__lqir in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    lda__xwpi = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(lda__xwpi, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for rjvwj__dxv in range(len(vals) - 1, -1, -1):
        buas__lqir = vals[rjvwj__dxv]
        if isinstance(buas__lqir, str) and buas__lqir.startswith(
            NESTED_TUP_SENTINEL):
            rnfys__idxd = int(buas__lqir[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:rjvwj__dxv]) + (
                tuple(vals[rjvwj__dxv + 1:rjvwj__dxv + rnfys__idxd + 1]),) +
                tuple(vals[rjvwj__dxv + rnfys__idxd + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    zfl__wjcu = None
    if len(args) > arg_no and arg_no >= 0:
        zfl__wjcu = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        zfl__wjcu = kws[arg_name]
    if zfl__wjcu is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return zfl__wjcu


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
    obj__uxum = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        obj__uxum.update(extra_globals)
    func.__globals__.update(obj__uxum)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            xwgkv__crslf = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[xwgkv__crslf.name] = types.literal(default)
            except:
                pass_info.typemap[xwgkv__crslf.name] = numba.typeof(default)
            ezc__gvj = ir.Assign(ir.Const(default, loc), xwgkv__crslf, loc)
            pre_nodes.append(ezc__gvj)
            return xwgkv__crslf
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    brow__azpfg = tuple(pass_info.typemap[buas__lqir.name] for buas__lqir in
        args)
    if const:
        posy__lem = []
        for rjvwj__dxv, zfl__wjcu in enumerate(args):
            wlt__njj = guard(find_const, pass_info.func_ir, zfl__wjcu)
            if wlt__njj:
                posy__lem.append(types.literal(wlt__njj))
            else:
                posy__lem.append(brow__azpfg[rjvwj__dxv])
        brow__azpfg = tuple(posy__lem)
    return ReplaceFunc(func, brow__azpfg, args, obj__uxum,
        inline_bodo_calls, run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(gwn__kmoq) for gwn__kmoq in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        fizfi__llo = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {fizfi__llo} = 0\n', (fizfi__llo,)
    if isinstance(t, ArrayItemArrayType):
        brn__lshie, idnu__hgtmq = gen_init_varsize_alloc_sizes(t.dtype)
        fizfi__llo = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {fizfi__llo} = 0\n' + brn__lshie, (fizfi__llo,
            ) + idnu__hgtmq
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
        return 1 + sum(get_type_alloc_counts(gwn__kmoq.dtype) for gwn__kmoq in
            t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(gwn__kmoq) for gwn__kmoq in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(gwn__kmoq) for gwn__kmoq in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    fxzdm__uwe = typing_context.resolve_getattr(obj_dtype, func_name)
    if fxzdm__uwe is None:
        gzlo__vwie = types.misc.Module(np)
        try:
            fxzdm__uwe = typing_context.resolve_getattr(gzlo__vwie, func_name)
        except AttributeError as grlwf__dxand:
            fxzdm__uwe = None
        if fxzdm__uwe is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return fxzdm__uwe


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    fxzdm__uwe = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(fxzdm__uwe, types.BoundFunction):
        if axis is not None:
            shi__tqwdk = fxzdm__uwe.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            shi__tqwdk = fxzdm__uwe.get_call_type(typing_context, (), {})
        return shi__tqwdk.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(fxzdm__uwe):
            shi__tqwdk = fxzdm__uwe.get_call_type(typing_context, (
                obj_dtype,), {})
            return shi__tqwdk.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    fxzdm__uwe = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(fxzdm__uwe, types.BoundFunction):
        qimt__yxb = fxzdm__uwe.template
        if axis is not None:
            return qimt__yxb._overload_func(obj_dtype, axis=axis)
        else:
            return qimt__yxb._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    hnqti__bqgvh = get_definition(func_ir, dict_var)
    require(isinstance(hnqti__bqgvh, ir.Expr))
    require(hnqti__bqgvh.op == 'build_map')
    wwrt__zhxxz = hnqti__bqgvh.items
    sgqlo__ctd = []
    values = []
    ywam__oco = False
    for rjvwj__dxv in range(len(wwrt__zhxxz)):
        fjm__pmd, value = wwrt__zhxxz[rjvwj__dxv]
        try:
            lgt__igeb = get_const_value_inner(func_ir, fjm__pmd, arg_types,
                typemap, updated_containers)
            sgqlo__ctd.append(lgt__igeb)
            values.append(value)
        except GuardException as grlwf__dxand:
            require_const_map[fjm__pmd] = label
            ywam__oco = True
    if ywam__oco:
        raise GuardException
    return sgqlo__ctd, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        sgqlo__ctd = tuple(get_const_value_inner(func_ir, t[0], args) for t in
            build_map.items)
    except GuardException as grlwf__dxand:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in sgqlo__ctd):
        raise BodoError(err_msg, loc)
    return sgqlo__ctd


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    sgqlo__ctd = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    oecej__rjhb = []
    ljjj__iqlcf = [bodo.transforms.typing_pass._create_const_var(lcg__zolcd,
        'dict_key', scope, loc, oecej__rjhb) for lcg__zolcd in sgqlo__ctd]
    gard__ibebc = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        eoy__tsr = ir.Var(scope, mk_unique_var('sentinel'), loc)
        aeg__fex = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        oecej__rjhb.append(ir.Assign(ir.Const('__bodo_tup', loc), eoy__tsr,
            loc))
        mzkt__zgb = [eoy__tsr] + ljjj__iqlcf + gard__ibebc
        oecej__rjhb.append(ir.Assign(ir.Expr.build_tuple(mzkt__zgb, loc),
            aeg__fex, loc))
        return (aeg__fex,), oecej__rjhb
    else:
        lmp__iotei = ir.Var(scope, mk_unique_var('values_tup'), loc)
        ctye__kftq = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        oecej__rjhb.append(ir.Assign(ir.Expr.build_tuple(gard__ibebc, loc),
            lmp__iotei, loc))
        oecej__rjhb.append(ir.Assign(ir.Expr.build_tuple(ljjj__iqlcf, loc),
            ctye__kftq, loc))
        return (lmp__iotei, ctye__kftq), oecej__rjhb
