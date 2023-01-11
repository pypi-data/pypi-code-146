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
    eus__efpld = tuple(call_list)
    if eus__efpld in no_side_effect_call_tuples:
        return True
    if eus__efpld == (bodo.hiframes.pd_index_ext.init_range_index,):
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
    if len(eus__efpld) == 1 and tuple in getattr(eus__efpld[0], '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=False, add_default_globals=True):
    if replace_globals:
        uokg__mlsxh = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math}
    else:
        uokg__mlsxh = func.__globals__
    if extra_globals is not None:
        uokg__mlsxh.update(extra_globals)
    if add_default_globals:
        uokg__mlsxh.update({'numba': numba, 'np': np, 'bodo': bodo, 'pd':
            pd, 'math': math})
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, uokg__mlsxh, typingctx=typing_info
            .typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[tzxmg__psji.name] for tzxmg__psji in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, uokg__mlsxh)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        dpoke__oxip = tuple(typing_info.typemap[tzxmg__psji.name] for
            tzxmg__psji in args)
        hvkr__wbo = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, dpoke__oxip, {}, {}, flags)
        hvkr__wbo.run()
    orv__ljx = f_ir.blocks.popitem()[1]
    replace_arg_nodes(orv__ljx, args)
    usym__xsgz = orv__ljx.body[:-2]
    update_locs(usym__xsgz[len(args):], loc)
    for stmt in usym__xsgz[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        ampy__qtdub = orv__ljx.body[-2]
        assert is_assign(ampy__qtdub) and is_expr(ampy__qtdub.value, 'cast')
        bklm__lzd = ampy__qtdub.value.value
        usym__xsgz.append(ir.Assign(bklm__lzd, ret_var, loc))
    return usym__xsgz


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for scaq__aout in stmt.list_vars():
            scaq__aout.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        ctpe__eety = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        szkx__ylg, xzg__jkre = ctpe__eety(stmt)
        return xzg__jkre
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        cdp__stv = get_const_value_inner(func_ir, var, arg_types, typemap,
            file_info=file_info)
        if isinstance(cdp__stv, ir.UndefinedType):
            udta__bnw = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{udta__bnw}' is not defined", loc=loc)
    except GuardException as sbqn__gplju:
        raise BodoError(err_msg, loc=loc)
    return cdp__stv


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    ish__tkorb = get_definition(func_ir, var)
    nbv__isjvq = None
    if typemap is not None:
        nbv__isjvq = typemap.get(var.name, None)
    if isinstance(ish__tkorb, ir.Arg) and arg_types is not None:
        nbv__isjvq = arg_types[ish__tkorb.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(nbv__isjvq):
        return get_literal_value(nbv__isjvq)
    if isinstance(ish__tkorb, (ir.Const, ir.Global, ir.FreeVar)):
        cdp__stv = ish__tkorb.value
        return cdp__stv
    if literalize_args and isinstance(ish__tkorb, ir.Arg
        ) and can_literalize_type(nbv__isjvq, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({ish__tkorb.index}, loc=var
            .loc, file_infos={ish__tkorb.index: file_info} if file_info is not
            None else None)
    if is_expr(ish__tkorb, 'binop'):
        if file_info and ish__tkorb.fn == operator.add:
            try:
                reaa__gdtlr = get_const_value_inner(func_ir, ish__tkorb.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(reaa__gdtlr, True)
                yhfkr__imly = get_const_value_inner(func_ir, ish__tkorb.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return ish__tkorb.fn(reaa__gdtlr, yhfkr__imly)
            except (GuardException, BodoConstUpdatedError) as sbqn__gplju:
                pass
            try:
                yhfkr__imly = get_const_value_inner(func_ir, ish__tkorb.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(yhfkr__imly, False)
                reaa__gdtlr = get_const_value_inner(func_ir, ish__tkorb.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return ish__tkorb.fn(reaa__gdtlr, yhfkr__imly)
            except (GuardException, BodoConstUpdatedError) as sbqn__gplju:
                pass
        reaa__gdtlr = get_const_value_inner(func_ir, ish__tkorb.lhs,
            arg_types, typemap, updated_containers)
        yhfkr__imly = get_const_value_inner(func_ir, ish__tkorb.rhs,
            arg_types, typemap, updated_containers)
        return ish__tkorb.fn(reaa__gdtlr, yhfkr__imly)
    if is_expr(ish__tkorb, 'unary'):
        cdp__stv = get_const_value_inner(func_ir, ish__tkorb.value,
            arg_types, typemap, updated_containers)
        return ish__tkorb.fn(cdp__stv)
    if is_expr(ish__tkorb, 'getattr') and typemap:
        ycetn__jevy = typemap.get(ish__tkorb.value.name, None)
        if isinstance(ycetn__jevy, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and ish__tkorb.attr == 'columns':
            return pd.Index(ycetn__jevy.columns)
        if isinstance(ycetn__jevy, types.SliceType):
            ahf__dub = get_definition(func_ir, ish__tkorb.value)
            require(is_call(ahf__dub))
            ftnk__krp = find_callname(func_ir, ahf__dub)
            vuhy__tpjf = False
            if ftnk__krp == ('_normalize_slice', 'numba.cpython.unicode'):
                require(ish__tkorb.attr in ('start', 'step'))
                ahf__dub = get_definition(func_ir, ahf__dub.args[0])
                vuhy__tpjf = True
            require(find_callname(func_ir, ahf__dub) == ('slice', 'builtins'))
            if len(ahf__dub.args) == 1:
                if ish__tkorb.attr == 'start':
                    return 0
                if ish__tkorb.attr == 'step':
                    return 1
                require(ish__tkorb.attr == 'stop')
                return get_const_value_inner(func_ir, ahf__dub.args[0],
                    arg_types, typemap, updated_containers)
            if ish__tkorb.attr == 'start':
                cdp__stv = get_const_value_inner(func_ir, ahf__dub.args[0],
                    arg_types, typemap, updated_containers)
                if cdp__stv is None:
                    cdp__stv = 0
                if vuhy__tpjf:
                    require(cdp__stv == 0)
                return cdp__stv
            if ish__tkorb.attr == 'stop':
                assert not vuhy__tpjf
                return get_const_value_inner(func_ir, ahf__dub.args[1],
                    arg_types, typemap, updated_containers)
            require(ish__tkorb.attr == 'step')
            if len(ahf__dub.args) == 2:
                return 1
            else:
                cdp__stv = get_const_value_inner(func_ir, ahf__dub.args[2],
                    arg_types, typemap, updated_containers)
                if cdp__stv is None:
                    cdp__stv = 1
                if vuhy__tpjf:
                    require(cdp__stv == 1)
                return cdp__stv
    if is_expr(ish__tkorb, 'getattr'):
        return getattr(get_const_value_inner(func_ir, ish__tkorb.value,
            arg_types, typemap, updated_containers), ish__tkorb.attr)
    if is_expr(ish__tkorb, 'getitem'):
        value = get_const_value_inner(func_ir, ish__tkorb.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, ish__tkorb.index, arg_types,
            typemap, updated_containers)
        return value[index]
    nmmdb__lxbwh = guard(find_callname, func_ir, ish__tkorb, typemap)
    if nmmdb__lxbwh is not None and len(nmmdb__lxbwh) == 2 and nmmdb__lxbwh[0
        ] == 'keys' and isinstance(nmmdb__lxbwh[1], ir.Var):
        mgsq__heycr = ish__tkorb.func
        ish__tkorb = get_definition(func_ir, nmmdb__lxbwh[1])
        ykf__xzbk = nmmdb__lxbwh[1].name
        if updated_containers and ykf__xzbk in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                ykf__xzbk, updated_containers[ykf__xzbk]))
        require(is_expr(ish__tkorb, 'build_map'))
        vals = [scaq__aout[0] for scaq__aout in ish__tkorb.items]
        lnw__wmfy = guard(get_definition, func_ir, mgsq__heycr)
        assert isinstance(lnw__wmfy, ir.Expr) and lnw__wmfy.attr == 'keys'
        lnw__wmfy.attr = 'copy'
        return [get_const_value_inner(func_ir, scaq__aout, arg_types,
            typemap, updated_containers) for scaq__aout in vals]
    if is_expr(ish__tkorb, 'build_map'):
        return {get_const_value_inner(func_ir, scaq__aout[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            scaq__aout[1], arg_types, typemap, updated_containers) for
            scaq__aout in ish__tkorb.items}
    if is_expr(ish__tkorb, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, scaq__aout, arg_types,
            typemap, updated_containers) for scaq__aout in ish__tkorb.items)
    if is_expr(ish__tkorb, 'build_list'):
        return [get_const_value_inner(func_ir, scaq__aout, arg_types,
            typemap, updated_containers) for scaq__aout in ish__tkorb.items]
    if is_expr(ish__tkorb, 'build_set'):
        return {get_const_value_inner(func_ir, scaq__aout, arg_types,
            typemap, updated_containers) for scaq__aout in ish__tkorb.items}
    if nmmdb__lxbwh == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, ish__tkorb.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if nmmdb__lxbwh == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, ish__tkorb.args[0],
            arg_types, typemap, updated_containers))
    if nmmdb__lxbwh == ('range', 'builtins') and len(ish__tkorb.args) == 1:
        return range(get_const_value_inner(func_ir, ish__tkorb.args[0],
            arg_types, typemap, updated_containers))
    if nmmdb__lxbwh == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, scaq__aout,
            arg_types, typemap, updated_containers) for scaq__aout in
            ish__tkorb.args))
    if nmmdb__lxbwh == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, ish__tkorb.args[0],
            arg_types, typemap, updated_containers))
    if nmmdb__lxbwh == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, ish__tkorb.args[0],
            arg_types, typemap, updated_containers))
    if nmmdb__lxbwh == ('format', 'builtins'):
        tzxmg__psji = get_const_value_inner(func_ir, ish__tkorb.args[0],
            arg_types, typemap, updated_containers)
        uptw__zec = get_const_value_inner(func_ir, ish__tkorb.args[1],
            arg_types, typemap, updated_containers) if len(ish__tkorb.args
            ) > 1 else ''
        return format(tzxmg__psji, uptw__zec)
    if nmmdb__lxbwh in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, ish__tkorb.args[0],
            arg_types, typemap, updated_containers))
    if nmmdb__lxbwh == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, ish__tkorb.args[0],
            arg_types, typemap, updated_containers))
    if nmmdb__lxbwh == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, ish__tkorb.args
            [0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, ish__tkorb.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            ish__tkorb.args[2], arg_types, typemap, updated_containers))
    if nmmdb__lxbwh == ('len', 'builtins') and typemap and isinstance(typemap
        .get(ish__tkorb.args[0].name, None), types.BaseTuple):
        return len(typemap[ish__tkorb.args[0].name])
    if nmmdb__lxbwh == ('len', 'builtins'):
        tgw__pyh = guard(get_definition, func_ir, ish__tkorb.args[0])
        if isinstance(tgw__pyh, ir.Expr) and tgw__pyh.op in ('build_tuple',
            'build_list', 'build_set', 'build_map'):
            return len(tgw__pyh.items)
        return len(get_const_value_inner(func_ir, ish__tkorb.args[0],
            arg_types, typemap, updated_containers))
    if nmmdb__lxbwh == ('CategoricalDtype', 'pandas'):
        kws = dict(ish__tkorb.kws)
        aywj__ewxe = get_call_expr_arg('CategoricalDtype', ish__tkorb.args,
            kws, 0, 'categories', '')
        opzk__wtt = get_call_expr_arg('CategoricalDtype', ish__tkorb.args,
            kws, 1, 'ordered', False)
        if opzk__wtt is not False:
            opzk__wtt = get_const_value_inner(func_ir, opzk__wtt, arg_types,
                typemap, updated_containers)
        if aywj__ewxe == '':
            aywj__ewxe = None
        else:
            aywj__ewxe = get_const_value_inner(func_ir, aywj__ewxe,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(aywj__ewxe, opzk__wtt)
    if nmmdb__lxbwh == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, ish__tkorb.args[0],
            arg_types, typemap, updated_containers))
    if nmmdb__lxbwh is not None and nmmdb__lxbwh[1
        ] == 'numpy' and nmmdb__lxbwh[0] in _np_type_names:
        return getattr(np, nmmdb__lxbwh[0])(get_const_value_inner(func_ir,
            ish__tkorb.args[0], arg_types, typemap, updated_containers))
    if nmmdb__lxbwh is not None and len(nmmdb__lxbwh) == 2 and nmmdb__lxbwh[1
        ] == 'pandas' and nmmdb__lxbwh[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, nmmdb__lxbwh[0])()
    if nmmdb__lxbwh is not None and len(nmmdb__lxbwh) == 2 and isinstance(
        nmmdb__lxbwh[1], ir.Var):
        cdp__stv = get_const_value_inner(func_ir, nmmdb__lxbwh[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, scaq__aout, arg_types,
            typemap, updated_containers) for scaq__aout in ish__tkorb.args]
        kws = {rgn__qyv[0]: get_const_value_inner(func_ir, rgn__qyv[1],
            arg_types, typemap, updated_containers) for rgn__qyv in
            ish__tkorb.kws}
        return getattr(cdp__stv, nmmdb__lxbwh[0])(*args, **kws)
    if nmmdb__lxbwh is not None and len(nmmdb__lxbwh) == 2 and nmmdb__lxbwh[1
        ] == 'bodo' and nmmdb__lxbwh[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, scaq__aout, arg_types,
            typemap, updated_containers) for scaq__aout in ish__tkorb.args)
        kwargs = {udta__bnw: get_const_value_inner(func_ir, scaq__aout,
            arg_types, typemap, updated_containers) for udta__bnw,
            scaq__aout in dict(ish__tkorb.kws).items()}
        return getattr(bodo, nmmdb__lxbwh[0])(*args, **kwargs)
    if is_call(ish__tkorb) and typemap and isinstance(typemap.get(
        ish__tkorb.func.name, None), types.Dispatcher):
        py_func = typemap[ish__tkorb.func.name].dispatcher.py_func
        require(ish__tkorb.vararg is None)
        args = tuple(get_const_value_inner(func_ir, scaq__aout, arg_types,
            typemap, updated_containers) for scaq__aout in ish__tkorb.args)
        kwargs = {udta__bnw: get_const_value_inner(func_ir, scaq__aout,
            arg_types, typemap, updated_containers) for udta__bnw,
            scaq__aout in dict(ish__tkorb.kws).items()}
        arg_types = tuple(bodo.typeof(scaq__aout) for scaq__aout in args)
        kw_types = {jkfm__hyxhk: bodo.typeof(scaq__aout) for jkfm__hyxhk,
            scaq__aout in kwargs.items()}
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
    f_ir, typemap, esp__tiy, esp__tiy = bodo.compiler.get_func_type_info(
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
                    xjne__snkh = guard(get_definition, f_ir, rhs.func)
                    if isinstance(xjne__snkh, ir.Const) and isinstance(
                        xjne__snkh.value, numba.core.dispatcher.
                        ObjModeLiftedWith):
                        return False
                    wzx__rlpx = guard(find_callname, f_ir, rhs)
                    if wzx__rlpx is None:
                        return False
                    func_name, egbb__uhpi = wzx__rlpx
                    if egbb__uhpi == 'pandas' and func_name.startswith('read_'
                        ):
                        return False
                    if wzx__rlpx in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if wzx__rlpx == ('File', 'h5py'):
                        return False
                    if isinstance(egbb__uhpi, ir.Var):
                        nbv__isjvq = typemap[egbb__uhpi.name]
                        if isinstance(nbv__isjvq, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(nbv__isjvq, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(nbv__isjvq, bodo.LoggingLoggerType):
                            return False
                        if str(nbv__isjvq).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            egbb__uhpi), ir.Arg)):
                            return False
                    if egbb__uhpi in ('numpy.random', 'time', 'logging',
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
        nxa__jwaq = func.literal_value.code
        arkbc__xnqa = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            arkbc__xnqa = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(arkbc__xnqa, nxa__jwaq)
        fix_struct_return(f_ir)
        typemap, nekq__emnxc, uod__zwt, esp__tiy = (numba.core.typed_passes
            .type_inference_stage(typing_context, target_context, f_ir,
            arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, uod__zwt, nekq__emnxc = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, uod__zwt, nekq__emnxc = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, uod__zwt, nekq__emnxc = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(nekq__emnxc, types.DictType):
        tgh__dtcpx = guard(get_struct_keynames, f_ir, typemap)
        if tgh__dtcpx is not None:
            nekq__emnxc = StructType((nekq__emnxc.value_type,) * len(
                tgh__dtcpx), tgh__dtcpx)
    if is_udf and isinstance(nekq__emnxc, (SeriesType, HeterogeneousSeriesType)
        ):
        epgh__pmahr = numba.core.registry.cpu_target.typing_context
        pjhem__lkzzm = numba.core.registry.cpu_target.target_context
        qni__vvwtt = bodo.transforms.series_pass.SeriesPass(f_ir,
            epgh__pmahr, pjhem__lkzzm, typemap, uod__zwt, {})
        rufej__mqqwc = qni__vvwtt.run()
        if rufej__mqqwc:
            rufej__mqqwc = qni__vvwtt.run()
            if rufej__mqqwc:
                qni__vvwtt.run()
        bdy__fzy = compute_cfg_from_blocks(f_ir.blocks)
        hggi__ktd = [guard(_get_const_series_info, f_ir.blocks[zjx__kzzqi],
            f_ir, typemap) for zjx__kzzqi in bdy__fzy.exit_points() if
            isinstance(f_ir.blocks[zjx__kzzqi].body[-1], ir.Return)]
        if None in hggi__ktd or len(pd.Series(hggi__ktd).unique()) != 1:
            nekq__emnxc.const_info = None
        else:
            nekq__emnxc.const_info = hggi__ktd[0]
    return nekq__emnxc


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    cpnr__xvwfw = block.body[-1].value
    oyudv__iib = get_definition(f_ir, cpnr__xvwfw)
    require(is_expr(oyudv__iib, 'cast'))
    oyudv__iib = get_definition(f_ir, oyudv__iib.value)
    require(is_call(oyudv__iib) and find_callname(f_ir, oyudv__iib) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    ijti__xptl = oyudv__iib.args[1]
    gkkow__lgzw = tuple(get_const_value_inner(f_ir, ijti__xptl, typemap=
        typemap))
    if isinstance(typemap[cpnr__xvwfw.name], HeterogeneousSeriesType):
        return len(typemap[cpnr__xvwfw.name].data), gkkow__lgzw
    duowv__tkohn = oyudv__iib.args[0]
    zqzr__oeu = get_definition(f_ir, duowv__tkohn)
    func_name, sva__exq = find_callname(f_ir, zqzr__oeu)
    if is_call(zqzr__oeu) and bodo.utils.utils.is_alloc_callname(func_name,
        sva__exq):
        vel__vwt = zqzr__oeu.args[0]
        jka__mru = get_const_value_inner(f_ir, vel__vwt, typemap=typemap)
        return jka__mru, gkkow__lgzw
    if is_call(zqzr__oeu) and find_callname(f_ir, zqzr__oeu) in [('asarray',
        'numpy'), ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'), (
        'build_nullable_tuple', 'bodo.libs.nullable_tuple_ext')]:
        duowv__tkohn = zqzr__oeu.args[0]
        zqzr__oeu = get_definition(f_ir, duowv__tkohn)
    require(is_expr(zqzr__oeu, 'build_tuple') or is_expr(zqzr__oeu,
        'build_list'))
    return len(zqzr__oeu.items), gkkow__lgzw


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    bzbkj__bqmq = []
    kjw__mre = []
    values = []
    for jkfm__hyxhk, scaq__aout in build_map.items:
        ielbz__tbog = find_const(f_ir, jkfm__hyxhk)
        require(isinstance(ielbz__tbog, str))
        kjw__mre.append(ielbz__tbog)
        bzbkj__bqmq.append(jkfm__hyxhk)
        values.append(scaq__aout)
    pmo__nlbe = ir.Var(scope, mk_unique_var('val_tup'), loc)
    itxc__fyf = ir.Assign(ir.Expr.build_tuple(values, loc), pmo__nlbe, loc)
    f_ir._definitions[pmo__nlbe.name] = [itxc__fyf.value]
    udz__gxn = ir.Var(scope, mk_unique_var('key_tup'), loc)
    jdtw__ctel = ir.Assign(ir.Expr.build_tuple(bzbkj__bqmq, loc), udz__gxn, loc
        )
    f_ir._definitions[udz__gxn.name] = [jdtw__ctel.value]
    if typemap is not None:
        typemap[pmo__nlbe.name] = types.Tuple([typemap[scaq__aout.name] for
            scaq__aout in values])
        typemap[udz__gxn.name] = types.Tuple([typemap[scaq__aout.name] for
            scaq__aout in bzbkj__bqmq])
    return kjw__mre, pmo__nlbe, itxc__fyf, udz__gxn, jdtw__ctel


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    yod__uoez = block.body[-1].value
    aua__vfld = guard(get_definition, f_ir, yod__uoez)
    require(is_expr(aua__vfld, 'cast'))
    oyudv__iib = guard(get_definition, f_ir, aua__vfld.value)
    require(is_expr(oyudv__iib, 'build_map'))
    require(len(oyudv__iib.items) > 0)
    loc = block.loc
    scope = block.scope
    kjw__mre, pmo__nlbe, itxc__fyf, udz__gxn, jdtw__ctel = (
        extract_keyvals_from_struct_map(f_ir, oyudv__iib, loc, scope))
    ndncb__wptwu = ir.Var(scope, mk_unique_var('conv_call'), loc)
    eycu__udmf = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), ndncb__wptwu, loc)
    f_ir._definitions[ndncb__wptwu.name] = [eycu__udmf.value]
    prw__qog = ir.Var(scope, mk_unique_var('struct_val'), loc)
    pvtxl__pvj = ir.Assign(ir.Expr.call(ndncb__wptwu, [pmo__nlbe, udz__gxn],
        {}, loc), prw__qog, loc)
    f_ir._definitions[prw__qog.name] = [pvtxl__pvj.value]
    aua__vfld.value = prw__qog
    oyudv__iib.items = [(jkfm__hyxhk, jkfm__hyxhk) for jkfm__hyxhk,
        esp__tiy in oyudv__iib.items]
    block.body = block.body[:-2] + [itxc__fyf, jdtw__ctel, eycu__udmf,
        pvtxl__pvj] + block.body[-2:]
    return tuple(kjw__mre)


def get_struct_keynames(f_ir, typemap):
    bdy__fzy = compute_cfg_from_blocks(f_ir.blocks)
    uae__drpr = list(bdy__fzy.exit_points())[0]
    block = f_ir.blocks[uae__drpr]
    require(isinstance(block.body[-1], ir.Return))
    yod__uoez = block.body[-1].value
    aua__vfld = guard(get_definition, f_ir, yod__uoez)
    require(is_expr(aua__vfld, 'cast'))
    oyudv__iib = guard(get_definition, f_ir, aua__vfld.value)
    require(is_call(oyudv__iib) and find_callname(f_ir, oyudv__iib) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[oyudv__iib.args[1].name])


def fix_struct_return(f_ir):
    muw__xqce = None
    bdy__fzy = compute_cfg_from_blocks(f_ir.blocks)
    for uae__drpr in bdy__fzy.exit_points():
        muw__xqce = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            uae__drpr], uae__drpr)
    return muw__xqce


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    zthho__hctar = ir.Block(ir.Scope(None, loc), loc)
    zthho__hctar.body = node_list
    build_definitions({(0): zthho__hctar}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(scaq__aout) for scaq__aout in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    nsrmb__sbe = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(nsrmb__sbe, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for jcf__ppuu in range(len(vals) - 1, -1, -1):
        scaq__aout = vals[jcf__ppuu]
        if isinstance(scaq__aout, str) and scaq__aout.startswith(
            NESTED_TUP_SENTINEL):
            iaauf__pzrv = int(scaq__aout[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:jcf__ppuu]) + (
                tuple(vals[jcf__ppuu + 1:jcf__ppuu + iaauf__pzrv + 1]),) +
                tuple(vals[jcf__ppuu + iaauf__pzrv + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    tzxmg__psji = None
    if len(args) > arg_no and arg_no >= 0:
        tzxmg__psji = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        tzxmg__psji = kws[arg_name]
    if tzxmg__psji is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return tzxmg__psji


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
    uokg__mlsxh = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        uokg__mlsxh.update(extra_globals)
    func.__globals__.update(uokg__mlsxh)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            zwhj__dhcd = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[zwhj__dhcd.name] = types.literal(default)
            except:
                pass_info.typemap[zwhj__dhcd.name] = numba.typeof(default)
            dan__usx = ir.Assign(ir.Const(default, loc), zwhj__dhcd, loc)
            pre_nodes.append(dan__usx)
            return zwhj__dhcd
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    dpoke__oxip = tuple(pass_info.typemap[scaq__aout.name] for scaq__aout in
        args)
    if const:
        rbx__izfsa = []
        for jcf__ppuu, tzxmg__psji in enumerate(args):
            cdp__stv = guard(find_const, pass_info.func_ir, tzxmg__psji)
            if cdp__stv:
                rbx__izfsa.append(types.literal(cdp__stv))
            else:
                rbx__izfsa.append(dpoke__oxip[jcf__ppuu])
        dpoke__oxip = tuple(rbx__izfsa)
    return ReplaceFunc(func, dpoke__oxip, args, uokg__mlsxh,
        inline_bodo_calls, run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(yeg__vayu) for yeg__vayu in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        jbds__tof = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {jbds__tof} = 0\n', (jbds__tof,)
    if isinstance(t, ArrayItemArrayType):
        fnomd__hqlz, yum__ytx = gen_init_varsize_alloc_sizes(t.dtype)
        jbds__tof = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {jbds__tof} = 0\n' + fnomd__hqlz, (jbds__tof,) + yum__ytx
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
        return 1 + sum(get_type_alloc_counts(yeg__vayu.dtype) for yeg__vayu in
            t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(yeg__vayu) for yeg__vayu in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(yeg__vayu) for yeg__vayu in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    aecwq__aiy = typing_context.resolve_getattr(obj_dtype, func_name)
    if aecwq__aiy is None:
        mjl__rze = types.misc.Module(np)
        try:
            aecwq__aiy = typing_context.resolve_getattr(mjl__rze, func_name)
        except AttributeError as sbqn__gplju:
            aecwq__aiy = None
        if aecwq__aiy is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return aecwq__aiy


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    aecwq__aiy = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(aecwq__aiy, types.BoundFunction):
        if axis is not None:
            cmw__zvur = aecwq__aiy.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            cmw__zvur = aecwq__aiy.get_call_type(typing_context, (), {})
        return cmw__zvur.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(aecwq__aiy):
            cmw__zvur = aecwq__aiy.get_call_type(typing_context, (obj_dtype
                ,), {})
            return cmw__zvur.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    aecwq__aiy = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(aecwq__aiy, types.BoundFunction):
        crbw__zglgg = aecwq__aiy.template
        if axis is not None:
            return crbw__zglgg._overload_func(obj_dtype, axis=axis)
        else:
            return crbw__zglgg._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    hozs__svg = get_definition(func_ir, dict_var)
    require(isinstance(hozs__svg, ir.Expr))
    require(hozs__svg.op == 'build_map')
    vfk__vzzki = hozs__svg.items
    bzbkj__bqmq = []
    values = []
    srhfn__guaxf = False
    for jcf__ppuu in range(len(vfk__vzzki)):
        ufd__xklf, value = vfk__vzzki[jcf__ppuu]
        try:
            scnl__enjo = get_const_value_inner(func_ir, ufd__xklf,
                arg_types, typemap, updated_containers)
            bzbkj__bqmq.append(scnl__enjo)
            values.append(value)
        except GuardException as sbqn__gplju:
            require_const_map[ufd__xklf] = label
            srhfn__guaxf = True
    if srhfn__guaxf:
        raise GuardException
    return bzbkj__bqmq, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        bzbkj__bqmq = tuple(get_const_value_inner(func_ir, t[0], args) for
            t in build_map.items)
    except GuardException as sbqn__gplju:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in bzbkj__bqmq):
        raise BodoError(err_msg, loc)
    return bzbkj__bqmq


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    bzbkj__bqmq = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    anouq__zej = []
    wbjdj__qgwjw = [bodo.transforms.typing_pass._create_const_var(
        jkfm__hyxhk, 'dict_key', scope, loc, anouq__zej) for jkfm__hyxhk in
        bzbkj__bqmq]
    zsy__esgnt = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        uimza__swes = ir.Var(scope, mk_unique_var('sentinel'), loc)
        pubn__zrx = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        anouq__zej.append(ir.Assign(ir.Const('__bodo_tup', loc),
            uimza__swes, loc))
        ypqqr__zsi = [uimza__swes] + wbjdj__qgwjw + zsy__esgnt
        anouq__zej.append(ir.Assign(ir.Expr.build_tuple(ypqqr__zsi, loc),
            pubn__zrx, loc))
        return (pubn__zrx,), anouq__zej
    else:
        doo__jax = ir.Var(scope, mk_unique_var('values_tup'), loc)
        zcqfl__ultl = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        anouq__zej.append(ir.Assign(ir.Expr.build_tuple(zsy__esgnt, loc),
            doo__jax, loc))
        anouq__zej.append(ir.Assign(ir.Expr.build_tuple(wbjdj__qgwjw, loc),
            zcqfl__ultl, loc))
        return (doo__jax, zcqfl__ultl), anouq__zej
