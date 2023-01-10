"""
Common utilities for all BodoSQL array kernels
"""
import math
import re
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from numba.core import types
import bodo
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType
from bodo.hiframes.pd_series_ext import is_datetime_date_series_typ, is_timedelta64_series_typ, pd_timedelta_type, pd_timestamp_tz_naive_type
from bodo.utils.typing import is_overload_bool, is_overload_constant_bool, is_overload_constant_bytes, is_overload_constant_number, is_overload_constant_str, is_overload_float, is_overload_int, is_overload_none, raise_bodo_error


def indent_block(text, indentation):
    if text is None:
        return ''
    hwurv__mtt = text.splitlines()[0]
    i = len(hwurv__mtt) - len(hwurv__mtt.lstrip())
    return '\n'.join([(' ' * indentation + ojpxp__lsusf[i:]) for
        ojpxp__lsusf in text.splitlines()]) + '\n'


def gen_vectorized(arg_names, arg_types, propagate_null, scalar_text,
    out_dtype, arg_string=None, arg_sources=None, array_override=None,
    support_dict_encoding=True, may_cause_duplicate_dict_array_values=False,
    prefix_code=None, suffix_code=None, res_list=False, extra_globals=None,
    alloc_array_scalars=True, synthesize_dict_if_vector=None,
    synthesize_dict_setup_text=None, synthesize_dict_scalar_text=None,
    synthesize_dict_global=False, synthesize_dict_unique=False):
    assert not (res_list and support_dict_encoding
        ), 'Cannot use res_list with support_dict_encoding'
    qntr__edpgo = [bodo.utils.utils.is_array_typ(cxkyc__ywqtj, True) for
        cxkyc__ywqtj in arg_types]
    cshw__labwu = not any(qntr__edpgo)
    kfsaj__vmd = any([propagate_null[i] for i in range(len(arg_types)) if 
        arg_types[i] == bodo.none])
    zihq__nejnk = False
    if synthesize_dict_if_vector is not None:
        assert synthesize_dict_setup_text is not None, 'synthesize_dict_setup_text must be provided if synthesize_dict_if_vector is provided'
        assert synthesize_dict_scalar_text is not None, 'synthesize_dict_scalar_text must be provided if synthesize_dict_if_vector is provided'
        zihq__nejnk = True
        for i in range(len(arg_types)):
            if qntr__edpgo[i] and synthesize_dict_if_vector[i] == 'S':
                zihq__nejnk = False
            if not qntr__edpgo[i] and synthesize_dict_if_vector[i] == 'V':
                zihq__nejnk = False
    tnyb__siu = 0
    zuz__ayb = -1
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            tnyb__siu += 1
            if arg_types[i] == bodo.dict_str_arr_type:
                zuz__ayb = i
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            tnyb__siu += 1
            if arg_types[i].data == bodo.dict_str_arr_type:
                zuz__ayb = i
    sobd__fvowr = support_dict_encoding and tnyb__siu == 1 and zuz__ayb >= 0
    idi__xam = sobd__fvowr and out_dtype == bodo.string_array_type and (any
        (arg_types[i] == bodo.none and propagate_null[i] for i in range(len
        (arg_types))) or 'bodo.libs.array_kernels.setna' in scalar_text)
    if arg_string is None:
        arg_string = ', '.join(arg_names)
    wcba__igqei = f'def impl({arg_string}):\n'
    if arg_sources is not None:
        for tiw__asujv, wde__jue in arg_sources.items():
            wcba__igqei += f'   {tiw__asujv} = {wde__jue}\n'
    if cshw__labwu and array_override == None:
        if kfsaj__vmd:
            wcba__igqei += '   return None'
        else:
            wcba__igqei += indent_block(prefix_code, 3)
            for i in range(len(arg_names)):
                wcba__igqei += f'   arg{i} = {arg_names[i]}\n'
            bwea__qng = scalar_text.replace('res[i] =', 'answer =').replace(
                'bodo.libs.array_kernels.setna(res, i)', 'return None')
            wcba__igqei += indent_block(bwea__qng, 3)
            wcba__igqei += '   return answer'
    else:
        for i in range(len(arg_names)):
            if bodo.hiframes.pd_series_ext.is_series_type(arg_types[i]):
                wcba__igqei += f"""   {arg_names[i]} = bodo.hiframes.pd_series_ext.get_series_data({arg_names[i]})
"""
        if array_override != None:
            blod__nox = f'len({array_override})'
        else:
            for i in range(len(arg_names)):
                if qntr__edpgo[i]:
                    blod__nox = f'len({arg_names[i]})'
                    break
        if sobd__fvowr:
            if out_dtype == bodo.string_array_type:
                wcba__igqei += (
                    f'   indices = {arg_names[zuz__ayb]}._indices.copy()\n')
                wcba__igqei += (
                    f'   has_global = {arg_names[zuz__ayb]}._has_global_dictionary\n'
                    )
                if may_cause_duplicate_dict_array_values:
                    wcba__igqei += f'   is_dict_unique = False\n'
                else:
                    wcba__igqei += f"""   is_dict_unique = {arg_names[zuz__ayb]}._has_deduped_local_dictionary
"""
                wcba__igqei += (
                    f'   {arg_names[i]} = {arg_names[zuz__ayb]}._data\n')
            else:
                wcba__igqei += f'   indices = {arg_names[zuz__ayb]}._indices\n'
                wcba__igqei += (
                    f'   {arg_names[i]} = {arg_names[zuz__ayb]}._data\n')
        wcba__igqei += f'   n = {blod__nox}\n'
        if prefix_code is not None and not kfsaj__vmd:
            wcba__igqei += indent_block(prefix_code, 3)
        if zihq__nejnk:
            wcba__igqei += indent_block(synthesize_dict_setup_text, 3)
            out_dtype = bodo.libs.dict_arr_ext.dict_indices_arr_type
            wcba__igqei += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            wcba__igqei += '   numba.parfors.parfor.init_prange()\n'
            wcba__igqei += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        elif sobd__fvowr:
            wsxz__cuak = 'n' if propagate_null[zuz__ayb] else '(n + 1)'
            if not propagate_null[zuz__ayb]:
                wiq__njz = arg_names[zuz__ayb]
                wcba__igqei += f"""   {wiq__njz} = bodo.libs.array_kernels.concat([{wiq__njz}, bodo.libs.array_kernels.gen_na_array(1, {wiq__njz})])
"""
            if out_dtype == bodo.string_array_type:
                wcba__igqei += f"""   res = bodo.libs.str_arr_ext.pre_alloc_string_array({wsxz__cuak}, -1)
"""
            else:
                wcba__igqei += f"""   res = bodo.utils.utils.alloc_type({wsxz__cuak}, out_dtype, (-1,))
"""
            wcba__igqei += f'   for i in range({wsxz__cuak}):\n'
        elif res_list:
            wcba__igqei += '   res = []\n'
            wcba__igqei += '   for i in range(n):\n'
        else:
            wcba__igqei += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            wcba__igqei += '   numba.parfors.parfor.init_prange()\n'
            wcba__igqei += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        if kfsaj__vmd:
            wcba__igqei += f'      bodo.libs.array_kernels.setna(res, i)\n'
        else:
            for i in range(len(arg_names)):
                if qntr__edpgo[i]:
                    if propagate_null[i]:
                        wcba__igqei += f"""      if bodo.libs.array_kernels.isna({arg_names[i]}, i):
"""
                        if res_list:
                            wcba__igqei += '         res.append(None)\n'
                        else:
                            wcba__igqei += (
                                '         bodo.libs.array_kernels.setna(res, i)\n'
                                )
                        wcba__igqei += '         continue\n'
            for i in range(len(arg_names)):
                if qntr__edpgo[i]:
                    if alloc_array_scalars:
                        wcba__igqei += f'      arg{i} = {arg_names[i]}[i]\n'
                else:
                    wcba__igqei += f'      arg{i} = {arg_names[i]}\n'
            if not zihq__nejnk:
                wcba__igqei += indent_block(scalar_text, 6)
            else:
                wcba__igqei += indent_block(synthesize_dict_scalar_text, 6)
        if sobd__fvowr:
            if idi__xam:
                wcba__igqei += '   numba.parfors.parfor.init_prange()\n'
                wcba__igqei += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                wcba__igqei += (
                    '      if not bodo.libs.array_kernels.isna(indices, i):\n')
                wcba__igqei += '         loc = indices[i]\n'
                wcba__igqei += (
                    '         if bodo.libs.array_kernels.isna(res, loc):\n')
                wcba__igqei += (
                    '            bodo.libs.array_kernels.setna(indices, i)\n')
            if out_dtype == bodo.string_array_type:
                wcba__igqei += """   res = bodo.libs.dict_arr_ext.init_dict_arr(res, indices, has_global, is_dict_unique)
"""
            else:
                wcba__igqei += """   res2 = bodo.utils.utils.alloc_type(len(indices), out_dtype, (-1,))
"""
                wcba__igqei += '   numba.parfors.parfor.init_prange()\n'
                wcba__igqei += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                if propagate_null[zuz__ayb]:
                    wcba__igqei += (
                        '      if bodo.libs.array_kernels.isna(indices, i):\n')
                    wcba__igqei += (
                        '         bodo.libs.array_kernels.setna(res2, i)\n')
                    wcba__igqei += '         continue\n'
                    wcba__igqei += '      loc = indices[i]\n'
                else:
                    wcba__igqei += """      loc = n if bodo.libs.array_kernels.isna(indices, i) else indices[i]
"""
                wcba__igqei += (
                    '      if bodo.libs.array_kernels.isna(res, loc):\n')
                wcba__igqei += (
                    '         bodo.libs.array_kernels.setna(res2, i)\n')
                wcba__igqei += '      else:\n'
                wcba__igqei += '         res2[i] = res[loc]\n'
                wcba__igqei += '   res = res2\n'
        wcba__igqei += indent_block(suffix_code, 3)
        if zihq__nejnk:
            wcba__igqei += f"""   return bodo.libs.dict_arr_ext.init_dict_arr(dict_res, res, {synthesize_dict_global}, {synthesize_dict_unique})
"""
        else:
            wcba__igqei += '   return res'
    ncfaw__glp = {}
    boijo__jqjr = {'bodo': bodo, 'math': math, 'numba': numba, 're': re,
        'np': np, 'out_dtype': out_dtype, 'pd': pd}
    if not extra_globals is None:
        boijo__jqjr.update(extra_globals)
    exec(wcba__igqei, boijo__jqjr, ncfaw__glp)
    vojh__vtves = ncfaw__glp['impl']
    return vojh__vtves


def unopt_argument(func_name, arg_names, i, container_arg=0,
    container_length=None):
    if container_length != None:
        tfa__pga = [(f'{arg_names[i]}{[iszwc__emrb]}' if iszwc__emrb !=
            container_arg else 'None') for iszwc__emrb in range(
            container_length)]
        crd__xmgej = ',' if container_length != 0 else ''
        nbr__ofbvl = f"({', '.join(tfa__pga)}{crd__xmgej})"
        bigt__agwwg = [(f'{arg_names[i]}{[iszwc__emrb]}' if iszwc__emrb !=
            container_arg else
            f'bodo.utils.indexing.unoptional({arg_names[i]}[{iszwc__emrb}])'
            ) for iszwc__emrb in range(container_length)]
        fwqf__cnugh = f"({', '.join(bigt__agwwg)}{crd__xmgej})"
        pxsr__icfux = [(arg_names[iszwc__emrb] if iszwc__emrb != i else
            nbr__ofbvl) for iszwc__emrb in range(len(arg_names))]
        aclg__jxgne = [(arg_names[iszwc__emrb] if iszwc__emrb != i else
            fwqf__cnugh) for iszwc__emrb in range(len(arg_names))]
        wcba__igqei = f"def impl({', '.join(arg_names)}):\n"
        wcba__igqei += f'   if {arg_names[i]}[{container_arg}] is None:\n'
        wcba__igqei += f"      return {func_name}({', '.join(pxsr__icfux)})\n"
        wcba__igqei += f'   else:\n'
        wcba__igqei += f"      return {func_name}({', '.join(aclg__jxgne)})\n"
    else:
        tfa__pga = [(arg_names[iszwc__emrb] if iszwc__emrb != i else 'None'
            ) for iszwc__emrb in range(len(arg_names))]
        bigt__agwwg = [(arg_names[iszwc__emrb] if iszwc__emrb != i else
            f'bodo.utils.indexing.unoptional({arg_names[iszwc__emrb]})') for
            iszwc__emrb in range(len(arg_names))]
        wcba__igqei = f"def impl({', '.join(arg_names)}):\n"
        wcba__igqei += f'   if {arg_names[i]} is None:\n'
        wcba__igqei += f"      return {func_name}({', '.join(tfa__pga)})\n"
        wcba__igqei += f'   else:\n'
        wcba__igqei += f"      return {func_name}({', '.join(bigt__agwwg)})\n"
    ncfaw__glp = {}
    exec(wcba__igqei, {'bodo': bodo, 'numba': numba}, ncfaw__glp)
    vojh__vtves = ncfaw__glp['impl']
    return vojh__vtves


def is_valid_int_arg(arg):
    return not (arg != types.none and not isinstance(arg, types.Integer) and
        not (bodo.utils.utils.is_array_typ(arg, True) and isinstance(arg.
        dtype, types.Integer)) and not is_overload_int(arg))


def is_valid_float_arg(arg):
    return not (arg != types.none and not isinstance(arg, types.Float) and 
        not (bodo.utils.utils.is_array_typ(arg, True) and isinstance(arg.
        dtype, types.Float)) and not is_overload_float(arg))


def is_valid_numeric_bool(arg):
    return not (arg != types.none and not isinstance(arg, (types.Integer,
        types.Float, types.Boolean)) and not (bodo.utils.utils.is_array_typ
        (arg, True) and isinstance(arg.dtype, (types.Integer, types.Float,
        types.Boolean))) and not is_overload_constant_number(arg) and not
        is_overload_constant_bool(arg))


def verify_int_arg(arg, f_name, a_name):
    if not is_valid_int_arg(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be an integer, integer column, or null'
            )


def verify_int_float_arg(arg, f_name, a_name):
    if arg != types.none and not isinstance(arg, (types.Integer, types.
        Float, types.Boolean)) and not (bodo.utils.utils.is_array_typ(arg, 
        True) and isinstance(arg.dtype, (types.Integer, types.Float, types.
        Boolean))) and not is_overload_constant_number(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a numeric, numeric column, or null'
            )


def is_valid_string_arg(arg):
    arg = types.unliteral(arg)
    return not (arg not in (types.none, types.unicode_type) and not (bodo.
        utils.utils.is_array_typ(arg, True) and arg.dtype == types.
        unicode_type) and not is_overload_constant_str(arg))


def is_valid_binary_arg(arg):
    return not (arg != bodo.bytes_type and not (bodo.utils.utils.
        is_array_typ(arg, True) and arg.dtype == bodo.bytes_type) and not
        is_overload_constant_bytes(arg) and not isinstance(arg, types.Bytes))


def is_valid_datetime_or_date_arg(arg):
    return arg == pd_timestamp_tz_naive_type or bodo.utils.utils.is_array_typ(
        arg, True) and (is_datetime_date_series_typ(arg) or isinstance(arg,
        bodo.DatetimeArrayType) or arg.dtype == bodo.datetime64ns)


def is_valid_timedelta_arg(arg):
    return arg == pd_timedelta_type or bodo.utils.utils.is_array_typ(arg, True
        ) and (is_timedelta64_series_typ(arg) or isinstance(arg,
        PDTimeDeltaType) or arg.dtype == bodo.timedelta64ns)


def is_valid_boolean_arg(arg):
    return not (arg != types.boolean and not (bodo.utils.utils.is_array_typ
        (arg, True) and arg.dtype == types.boolean) and not
        is_overload_constant_bool(arg))


def verify_string_arg(arg, f_name, a_name):
    if not is_valid_string_arg(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a string, string column, or null'
            )


def verify_scalar_string_arg(arg, f_name, a_name):
    if arg not in (types.unicode_type, bodo.none) and not isinstance(arg,
        types.StringLiteral):
        raise_bodo_error(f'{f_name} {a_name} argument must be a scalar string')


def verify_binary_arg(arg, f_name, a_name):
    if not is_valid_binary_arg(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be binary data or null')


def verify_string_binary_arg(arg, f_name, a_name):
    luxl__kmoch = is_valid_string_arg(arg)
    njuz__qsc = is_valid_binary_arg(arg)
    if luxl__kmoch or njuz__qsc:
        return luxl__kmoch
    else:
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a binary data, string, string column, or null'
            )


def verify_string_numeric_arg(arg, f_name, a_name):
    if not is_valid_string_arg(arg) and not is_valid_numeric_bool(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a string, integer, float, boolean, string column, integer column, float column, or boolean column'
            )


def verify_boolean_arg(arg, f_name, a_name):
    if arg not in (types.none, types.boolean) and not (bodo.utils.utils.
        is_array_typ(arg, True) and arg.dtype == types.boolean
        ) and not is_overload_bool(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a boolean, boolean column, or null'
            )


def is_valid_date_arg(arg):
    return arg == bodo.datetime_date_type or bodo.utils.utils.is_array_typ(arg,
        True) and arg.dtype == bodo.datetime_date_type


def is_valid_tz_naive_datetime_arg(arg):
    return arg in (bodo.datetime64ns, bodo.pd_timestamp_tz_naive_type
        ) or bodo.utils.utils.is_array_typ(arg, True
        ) and arg.dtype == bodo.datetime64ns


def is_valid_tz_aware_datetime_arg(arg):
    return isinstance(arg, bodo.PandasTimestampType
        ) and arg.tz is not None or bodo.utils.utils.is_array_typ(arg, True
        ) and isinstance(arg.dtype, bodo.libs.pd_datetime_arr_ext.
        PandasDatetimeTZDtype)


def verify_datetime_arg(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_date_arg(arg) or
        is_valid_tz_naive_datetime_arg(arg)):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a datetime, datetime column, or null without a tz'
            )


def verify_datetime_arg_allow_tz(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_date_arg(arg) or
        is_valid_tz_naive_datetime_arg(arg) or
        is_valid_tz_aware_datetime_arg(arg)):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a datetime, datetime column, or null'
            )


def verify_datetime_arg_require_tz(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_tz_aware_datetime_arg(arg)):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a tz-aware datetime, datetime column, or null'
            )


def verify_sql_interval(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_timedelta_arg(arg) or arg ==
        bodo.date_offset_type):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a Timedelta scalar/column, DateOffset, or null'
            )


def get_tz_if_exists(arg):
    if is_valid_tz_aware_datetime_arg(arg):
        if bodo.utils.utils.is_array_typ(arg, True):
            return arg.dtype.tz
        else:
            return arg.tz
    return None


def is_valid_time_arg(arg):
    return isinstance(arg, bodo.TimeType) or bodo.utils.utils.is_array_typ(arg,
        True) and isinstance(arg.dtype, bodo.bodo.TimeType)


def verify_time_or_datetime_arg_allow_tz(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_date_arg(arg) or
        is_valid_time_arg(arg) or is_valid_tz_naive_datetime_arg(arg) or
        is_valid_tz_aware_datetime_arg(arg)):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a time/datetime, time/datetime column, or null without a tz'
            )


def get_common_broadcasted_type(arg_types, func_name):
    gtx__unxsl = []
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            gtx__unxsl.append(arg_types[i])
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            gtx__unxsl.append(arg_types[i].data)
        else:
            gtx__unxsl.append(arg_types[i])
    if len(gtx__unxsl) == 0:
        return bodo.none
    elif len(gtx__unxsl) == 1:
        if bodo.utils.utils.is_array_typ(gtx__unxsl[0]):
            return bodo.utils.typing.to_nullable_type(gtx__unxsl[0])
        elif gtx__unxsl[0] == bodo.none:
            return bodo.none
        else:
            return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
                dtype_to_array_type(gtx__unxsl[0]))
    else:
        unz__xhht = []
        for i in range(len(arg_types)):
            if bodo.utils.utils.is_array_typ(arg_types[i]):
                unz__xhht.append(gtx__unxsl[i].dtype)
            elif gtx__unxsl[i] == bodo.none:
                pass
            else:
                unz__xhht.append(gtx__unxsl[i])
        if len(unz__xhht) == 0:
            return bodo.none
        fukx__tus, gphpk__bimp = bodo.utils.typing.get_common_scalar_dtype(
            unz__xhht)
        if not gphpk__bimp:
            raise_bodo_error(
                f'Cannot call {func_name} on columns with different dtypes')
        return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
            dtype_to_array_type(fukx__tus))


def vectorized_sol(args, scalar_fn, dtype, manual_coercion=False):
    swbpt__edfb = -1
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            swbpt__edfb = len(arg)
            break
    if swbpt__edfb == -1:
        return dtype(scalar_fn(*args)) if manual_coercion else scalar_fn(*args)
    odr__wzeyk = []
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            odr__wzeyk.append(arg)
        else:
            odr__wzeyk.append([arg] * swbpt__edfb)
    if manual_coercion:
        return pd.Series([dtype(scalar_fn(*syb__fac)) for syb__fac in zip(*
            odr__wzeyk)])
    else:
        return pd.Series([scalar_fn(*syb__fac) for syb__fac in zip(*
            odr__wzeyk)], dtype=dtype)


def gen_windowed(calculate_block, constant_block, out_dtype, setup_block=
    None, enter_block=None, exit_block=None, empty_block=None):
    kqu__jmrwc = calculate_block.splitlines()
    vfbx__cfd = len(kqu__jmrwc[0]) - len(kqu__jmrwc[0].lstrip())
    if constant_block != None:
        byj__vvio = constant_block.splitlines()
        nvy__azimu = len(byj__vvio[0]) - len(byj__vvio[0].lstrip())
    if setup_block != None:
        uph__oir = setup_block.splitlines()
        qbfd__avqct = len(uph__oir[0]) - len(uph__oir[0].lstrip())
    if enter_block != None:
        nnii__lhuqa = enter_block.splitlines()
        uvcci__hgm = len(nnii__lhuqa[0]) - len(nnii__lhuqa[0].lstrip())
    if exit_block != None:
        jsynl__brcy = exit_block.splitlines()
        rtn__gpcdb = len(jsynl__brcy[0]) - len(jsynl__brcy[0].lstrip())
    if empty_block == None:
        empty_block = 'bodo.libs.array_kernels.setna(res, i)'
    qeb__pvhqo = empty_block.splitlines()
    frr__yfe = len(qeb__pvhqo[0]) - len(qeb__pvhqo[0].lstrip())
    wcba__igqei = 'def impl(S, lower_bound, upper_bound):\n'
    wcba__igqei += '   n = len(S)\n'
    wcba__igqei += '   arr = bodo.utils.conversion.coerce_to_array(S)\n'
    wcba__igqei += (
        '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
    wcba__igqei += '   if upper_bound < lower_bound:\n'
    wcba__igqei += '      for i in range(n):\n'
    wcba__igqei += '         bodo.libs.array_kernels.setna(res, i)\n'
    if constant_block != None:
        wcba__igqei += '   elif lower_bound <= -n+1 and n-1 <= upper_bound:\n'
        wcba__igqei += '      if S.count() == 0:\n'
        wcba__igqei += '         for i in range(n):\n'
        wcba__igqei += '\n'.join([(' ' * 12 + ojpxp__lsusf[frr__yfe:]) for
            ojpxp__lsusf in qeb__pvhqo]) + '\n'
        wcba__igqei += '      else:\n'
        wcba__igqei += '\n'.join([(' ' * 9 + ojpxp__lsusf[nvy__azimu:]) for
            ojpxp__lsusf in byj__vvio]) + '\n'
        wcba__igqei += '         for i in range(n):\n'
        wcba__igqei += '            res[i] = constant_value\n'
    wcba__igqei += '   else:\n'
    wcba__igqei += '      exiting = lower_bound\n'
    wcba__igqei += '      entering = upper_bound\n'
    wcba__igqei += '      in_window = 0\n'
    if setup_block != None:
        wcba__igqei += '\n'.join([(' ' * 6 + ojpxp__lsusf[qbfd__avqct:]) for
            ojpxp__lsusf in uph__oir]) + '\n'
    wcba__igqei += (
        '      for i in range(min(max(0, exiting), n), min(max(0, entering + 1), n)):\n'
        )
    wcba__igqei += '         if not bodo.libs.array_kernels.isna(arr, i):\n'
    wcba__igqei += '            in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            wcba__igqei += '            elem = arr[i]\n'
        wcba__igqei += '\n'.join([(' ' * 12 + ojpxp__lsusf[uvcci__hgm:]) for
            ojpxp__lsusf in nnii__lhuqa]) + '\n'
    wcba__igqei += '      for i in range(n):\n'
    wcba__igqei += '         if in_window == 0:\n'
    wcba__igqei += '\n'.join([(' ' * 12 + ojpxp__lsusf[frr__yfe:]) for
        ojpxp__lsusf in qeb__pvhqo]) + '\n'
    wcba__igqei += '         else:\n'
    wcba__igqei += '\n'.join([(' ' * 12 + ojpxp__lsusf[vfbx__cfd:]) for
        ojpxp__lsusf in kqu__jmrwc]) + '\n'
    wcba__igqei += '         if 0 <= exiting < n:\n'
    wcba__igqei += (
        '            if not bodo.libs.array_kernels.isna(arr, exiting):\n')
    wcba__igqei += '               in_window -= 1\n'
    if exit_block != None:
        if 'elem' in exit_block:
            wcba__igqei += '               elem = arr[exiting]\n'
        wcba__igqei += '\n'.join([(' ' * 15 + ojpxp__lsusf[rtn__gpcdb:]) for
            ojpxp__lsusf in jsynl__brcy]) + '\n'
    wcba__igqei += '         exiting += 1\n'
    wcba__igqei += '         entering += 1\n'
    wcba__igqei += '         if 0 <= entering < n:\n'
    wcba__igqei += (
        '            if not bodo.libs.array_kernels.isna(arr, entering):\n')
    wcba__igqei += '               in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            wcba__igqei += '               elem = arr[entering]\n'
        wcba__igqei += '\n'.join([(' ' * 15 + ojpxp__lsusf[uvcci__hgm:]) for
            ojpxp__lsusf in nnii__lhuqa]) + '\n'
    wcba__igqei += '   return res'
    ncfaw__glp = {}
    exec(wcba__igqei, {'bodo': bodo, 'numba': numba, 'np': np, 'out_dtype':
        out_dtype, 'pd': pd}, ncfaw__glp)
    vojh__vtves = ncfaw__glp['impl']
    return vojh__vtves
