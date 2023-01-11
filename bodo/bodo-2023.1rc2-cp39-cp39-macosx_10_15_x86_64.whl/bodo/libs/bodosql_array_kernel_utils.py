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
    bxter__msebu = text.splitlines()[0]
    i = len(bxter__msebu) - len(bxter__msebu.lstrip())
    return '\n'.join([(' ' * indentation + qgqph__agpn[i:]) for qgqph__agpn in
        text.splitlines()]) + '\n'


def gen_vectorized(arg_names, arg_types, propagate_null, scalar_text,
    out_dtype, arg_string=None, arg_sources=None, array_override=None,
    support_dict_encoding=True, may_cause_duplicate_dict_array_values=False,
    prefix_code=None, suffix_code=None, res_list=False, extra_globals=None,
    alloc_array_scalars=True, synthesize_dict_if_vector=None,
    synthesize_dict_setup_text=None, synthesize_dict_scalar_text=None,
    synthesize_dict_global=False, synthesize_dict_unique=False):
    assert not (res_list and support_dict_encoding
        ), 'Cannot use res_list with support_dict_encoding'
    sod__cujjr = [bodo.utils.utils.is_array_typ(zqse__ijvgb, True) for
        zqse__ijvgb in arg_types]
    xns__qlj = not any(sod__cujjr)
    gdhzv__stwh = any([propagate_null[i] for i in range(len(arg_types)) if 
        arg_types[i] == bodo.none])
    itfv__mda = False
    if synthesize_dict_if_vector is not None:
        assert synthesize_dict_setup_text is not None, 'synthesize_dict_setup_text must be provided if synthesize_dict_if_vector is provided'
        assert synthesize_dict_scalar_text is not None, 'synthesize_dict_scalar_text must be provided if synthesize_dict_if_vector is provided'
        itfv__mda = True
        for i in range(len(arg_types)):
            if sod__cujjr[i] and synthesize_dict_if_vector[i] == 'S':
                itfv__mda = False
            if not sod__cujjr[i] and synthesize_dict_if_vector[i] == 'V':
                itfv__mda = False
    fag__wgxpd = 0
    sabcw__agzr = -1
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            fag__wgxpd += 1
            if arg_types[i] == bodo.dict_str_arr_type:
                sabcw__agzr = i
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            fag__wgxpd += 1
            if arg_types[i].data == bodo.dict_str_arr_type:
                sabcw__agzr = i
    hlmr__agec = support_dict_encoding and fag__wgxpd == 1 and sabcw__agzr >= 0
    lptvj__ruzh = hlmr__agec and out_dtype == bodo.string_array_type and (any
        (arg_types[i] == bodo.none and propagate_null[i] for i in range(len
        (arg_types))) or 'bodo.libs.array_kernels.setna' in scalar_text)
    if arg_string is None:
        arg_string = ', '.join(arg_names)
    fhsv__gut = f'def impl({arg_string}):\n'
    if arg_sources is not None:
        for ymf__lkfo, hbkey__pjro in arg_sources.items():
            fhsv__gut += f'   {ymf__lkfo} = {hbkey__pjro}\n'
    if xns__qlj and array_override == None:
        if gdhzv__stwh:
            fhsv__gut += '   return None'
        else:
            fhsv__gut += indent_block(prefix_code, 3)
            for i in range(len(arg_names)):
                fhsv__gut += f'   arg{i} = {arg_names[i]}\n'
            ftvc__rshk = scalar_text.replace('res[i] =', 'answer =').replace(
                'bodo.libs.array_kernels.setna(res, i)', 'return None')
            fhsv__gut += indent_block(ftvc__rshk, 3)
            fhsv__gut += '   return answer'
    else:
        for i in range(len(arg_names)):
            if bodo.hiframes.pd_series_ext.is_series_type(arg_types[i]):
                fhsv__gut += f"""   {arg_names[i]} = bodo.hiframes.pd_series_ext.get_series_data({arg_names[i]})
"""
        if array_override != None:
            whkoh__gdcp = f'len({array_override})'
        else:
            for i in range(len(arg_names)):
                if sod__cujjr[i]:
                    whkoh__gdcp = f'len({arg_names[i]})'
                    break
        if hlmr__agec:
            if out_dtype == bodo.string_array_type:
                fhsv__gut += (
                    f'   indices = {arg_names[sabcw__agzr]}._indices.copy()\n')
                fhsv__gut += (
                    f'   has_global = {arg_names[sabcw__agzr]}._has_global_dictionary\n'
                    )
                if may_cause_duplicate_dict_array_values:
                    fhsv__gut += f'   is_dict_unique = False\n'
                else:
                    fhsv__gut += f"""   is_dict_unique = {arg_names[sabcw__agzr]}._has_deduped_local_dictionary
"""
                fhsv__gut += (
                    f'   {arg_names[i]} = {arg_names[sabcw__agzr]}._data\n')
            else:
                fhsv__gut += (
                    f'   indices = {arg_names[sabcw__agzr]}._indices\n')
                fhsv__gut += (
                    f'   {arg_names[i]} = {arg_names[sabcw__agzr]}._data\n')
        fhsv__gut += f'   n = {whkoh__gdcp}\n'
        if prefix_code is not None and not gdhzv__stwh:
            fhsv__gut += indent_block(prefix_code, 3)
        if itfv__mda:
            fhsv__gut += indent_block(synthesize_dict_setup_text, 3)
            out_dtype = bodo.libs.dict_arr_ext.dict_indices_arr_type
            fhsv__gut += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            fhsv__gut += '   numba.parfors.parfor.init_prange()\n'
            fhsv__gut += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        elif hlmr__agec:
            cxv__ncz = 'n' if propagate_null[sabcw__agzr] else '(n + 1)'
            if not propagate_null[sabcw__agzr]:
                gomm__fna = arg_names[sabcw__agzr]
                fhsv__gut += f"""   {gomm__fna} = bodo.libs.array_kernels.concat([{gomm__fna}, bodo.libs.array_kernels.gen_na_array(1, {gomm__fna})])
"""
            if out_dtype == bodo.string_array_type:
                fhsv__gut += f"""   res = bodo.libs.str_arr_ext.pre_alloc_string_array({cxv__ncz}, -1)
"""
            else:
                fhsv__gut += (
                    f'   res = bodo.utils.utils.alloc_type({cxv__ncz}, out_dtype, (-1,))\n'
                    )
            fhsv__gut += f'   for i in range({cxv__ncz}):\n'
        elif res_list:
            fhsv__gut += '   res = []\n'
            fhsv__gut += '   for i in range(n):\n'
        else:
            fhsv__gut += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            fhsv__gut += '   numba.parfors.parfor.init_prange()\n'
            fhsv__gut += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        if gdhzv__stwh:
            fhsv__gut += f'      bodo.libs.array_kernels.setna(res, i)\n'
        else:
            for i in range(len(arg_names)):
                if sod__cujjr[i]:
                    if propagate_null[i]:
                        fhsv__gut += (
                            f'      if bodo.libs.array_kernels.isna({arg_names[i]}, i):\n'
                            )
                        if res_list:
                            fhsv__gut += '         res.append(None)\n'
                        else:
                            fhsv__gut += (
                                '         bodo.libs.array_kernels.setna(res, i)\n'
                                )
                        fhsv__gut += '         continue\n'
            for i in range(len(arg_names)):
                if sod__cujjr[i]:
                    if alloc_array_scalars:
                        fhsv__gut += f'      arg{i} = {arg_names[i]}[i]\n'
                else:
                    fhsv__gut += f'      arg{i} = {arg_names[i]}\n'
            if not itfv__mda:
                fhsv__gut += indent_block(scalar_text, 6)
            else:
                fhsv__gut += indent_block(synthesize_dict_scalar_text, 6)
        if hlmr__agec:
            if lptvj__ruzh:
                fhsv__gut += '   numba.parfors.parfor.init_prange()\n'
                fhsv__gut += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                fhsv__gut += (
                    '      if not bodo.libs.array_kernels.isna(indices, i):\n')
                fhsv__gut += '         loc = indices[i]\n'
                fhsv__gut += (
                    '         if bodo.libs.array_kernels.isna(res, loc):\n')
                fhsv__gut += (
                    '            bodo.libs.array_kernels.setna(indices, i)\n')
            if out_dtype == bodo.string_array_type:
                fhsv__gut += """   res = bodo.libs.dict_arr_ext.init_dict_arr(res, indices, has_global, is_dict_unique)
"""
            else:
                fhsv__gut += """   res2 = bodo.utils.utils.alloc_type(len(indices), out_dtype, (-1,))
"""
                fhsv__gut += '   numba.parfors.parfor.init_prange()\n'
                fhsv__gut += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                if propagate_null[sabcw__agzr]:
                    fhsv__gut += (
                        '      if bodo.libs.array_kernels.isna(indices, i):\n')
                    fhsv__gut += (
                        '         bodo.libs.array_kernels.setna(res2, i)\n')
                    fhsv__gut += '         continue\n'
                    fhsv__gut += '      loc = indices[i]\n'
                else:
                    fhsv__gut += """      loc = n if bodo.libs.array_kernels.isna(indices, i) else indices[i]
"""
                fhsv__gut += (
                    '      if bodo.libs.array_kernels.isna(res, loc):\n')
                fhsv__gut += (
                    '         bodo.libs.array_kernels.setna(res2, i)\n')
                fhsv__gut += '      else:\n'
                fhsv__gut += '         res2[i] = res[loc]\n'
                fhsv__gut += '   res = res2\n'
        fhsv__gut += indent_block(suffix_code, 3)
        if itfv__mda:
            fhsv__gut += f"""   return bodo.libs.dict_arr_ext.init_dict_arr(dict_res, res, {synthesize_dict_global}, {synthesize_dict_unique})
"""
        else:
            fhsv__gut += '   return res'
    akhl__tmeo = {}
    tzxj__zvb = {'bodo': bodo, 'math': math, 'numba': numba, 're': re, 'np':
        np, 'out_dtype': out_dtype, 'pd': pd}
    if not extra_globals is None:
        tzxj__zvb.update(extra_globals)
    exec(fhsv__gut, tzxj__zvb, akhl__tmeo)
    btduy__qsp = akhl__tmeo['impl']
    return btduy__qsp


def unopt_argument(func_name, arg_names, i, container_arg=0,
    container_length=None):
    if container_length != None:
        ehgm__wdq = [(f'{arg_names[i]}{[cxkdi__wsz]}' if cxkdi__wsz !=
            container_arg else 'None') for cxkdi__wsz in range(
            container_length)]
        fnzn__ihea = ',' if container_length != 0 else ''
        xbj__widci = f"({', '.join(ehgm__wdq)}{fnzn__ihea})"
        vawxp__lqjt = [(f'{arg_names[i]}{[cxkdi__wsz]}' if cxkdi__wsz !=
            container_arg else
            f'bodo.utils.indexing.unoptional({arg_names[i]}[{cxkdi__wsz}])'
            ) for cxkdi__wsz in range(container_length)]
        kjl__dxpp = f"({', '.join(vawxp__lqjt)}{fnzn__ihea})"
        cqo__kdphx = [(arg_names[cxkdi__wsz] if cxkdi__wsz != i else
            xbj__widci) for cxkdi__wsz in range(len(arg_names))]
        frdhz__quwef = [(arg_names[cxkdi__wsz] if cxkdi__wsz != i else
            kjl__dxpp) for cxkdi__wsz in range(len(arg_names))]
        fhsv__gut = f"def impl({', '.join(arg_names)}):\n"
        fhsv__gut += f'   if {arg_names[i]}[{container_arg}] is None:\n'
        fhsv__gut += f"      return {func_name}({', '.join(cqo__kdphx)})\n"
        fhsv__gut += f'   else:\n'
        fhsv__gut += f"      return {func_name}({', '.join(frdhz__quwef)})\n"
    else:
        ehgm__wdq = [(arg_names[cxkdi__wsz] if cxkdi__wsz != i else 'None') for
            cxkdi__wsz in range(len(arg_names))]
        vawxp__lqjt = [(arg_names[cxkdi__wsz] if cxkdi__wsz != i else
            f'bodo.utils.indexing.unoptional({arg_names[cxkdi__wsz]})') for
            cxkdi__wsz in range(len(arg_names))]
        fhsv__gut = f"def impl({', '.join(arg_names)}):\n"
        fhsv__gut += f'   if {arg_names[i]} is None:\n'
        fhsv__gut += f"      return {func_name}({', '.join(ehgm__wdq)})\n"
        fhsv__gut += f'   else:\n'
        fhsv__gut += f"      return {func_name}({', '.join(vawxp__lqjt)})\n"
    akhl__tmeo = {}
    exec(fhsv__gut, {'bodo': bodo, 'numba': numba}, akhl__tmeo)
    btduy__qsp = akhl__tmeo['impl']
    return btduy__qsp


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
    dvpbz__scn = is_valid_string_arg(arg)
    vjg__aml = is_valid_binary_arg(arg)
    if dvpbz__scn or vjg__aml:
        return dvpbz__scn
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
    qqfh__ysq = []
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            qqfh__ysq.append(arg_types[i])
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            qqfh__ysq.append(arg_types[i].data)
        else:
            qqfh__ysq.append(arg_types[i])
    if len(qqfh__ysq) == 0:
        return bodo.none
    elif len(qqfh__ysq) == 1:
        if bodo.utils.utils.is_array_typ(qqfh__ysq[0]):
            return bodo.utils.typing.to_nullable_type(qqfh__ysq[0])
        elif qqfh__ysq[0] == bodo.none:
            return bodo.none
        else:
            return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
                dtype_to_array_type(qqfh__ysq[0]))
    else:
        negq__bhec = []
        for i in range(len(arg_types)):
            if bodo.utils.utils.is_array_typ(arg_types[i]):
                negq__bhec.append(qqfh__ysq[i].dtype)
            elif qqfh__ysq[i] == bodo.none:
                pass
            else:
                negq__bhec.append(qqfh__ysq[i])
        if len(negq__bhec) == 0:
            return bodo.none
        wzz__dcbc, exzco__gjek = bodo.utils.typing.get_common_scalar_dtype(
            negq__bhec)
        if not exzco__gjek:
            raise_bodo_error(
                f'Cannot call {func_name} on columns with different dtypes')
        return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
            dtype_to_array_type(wzz__dcbc))


def vectorized_sol(args, scalar_fn, dtype, manual_coercion=False):
    kcm__cgwn = -1
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            kcm__cgwn = len(arg)
            break
    if kcm__cgwn == -1:
        return dtype(scalar_fn(*args)) if manual_coercion else scalar_fn(*args)
    ytvw__lyz = []
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            ytvw__lyz.append(arg)
        else:
            ytvw__lyz.append([arg] * kcm__cgwn)
    if manual_coercion:
        return pd.Series([dtype(scalar_fn(*eysx__ybyer)) for eysx__ybyer in
            zip(*ytvw__lyz)])
    else:
        return pd.Series([scalar_fn(*eysx__ybyer) for eysx__ybyer in zip(*
            ytvw__lyz)], dtype=dtype)


def gen_windowed(calculate_block, constant_block, out_dtype, setup_block=
    None, enter_block=None, exit_block=None, empty_block=None):
    myio__ydq = calculate_block.splitlines()
    yxwjq__mjec = len(myio__ydq[0]) - len(myio__ydq[0].lstrip())
    if constant_block != None:
        ujtry__xakn = constant_block.splitlines()
        oonx__dxkct = len(ujtry__xakn[0]) - len(ujtry__xakn[0].lstrip())
    if setup_block != None:
        qnvtg__oflab = setup_block.splitlines()
        gdhwn__iynr = len(qnvtg__oflab[0]) - len(qnvtg__oflab[0].lstrip())
    if enter_block != None:
        lmhrv__rvbk = enter_block.splitlines()
        jdc__aai = len(lmhrv__rvbk[0]) - len(lmhrv__rvbk[0].lstrip())
    if exit_block != None:
        oko__ueqrz = exit_block.splitlines()
        hsn__swdw = len(oko__ueqrz[0]) - len(oko__ueqrz[0].lstrip())
    if empty_block == None:
        empty_block = 'bodo.libs.array_kernels.setna(res, i)'
    luxck__iijjk = empty_block.splitlines()
    lajvq__nrvvu = len(luxck__iijjk[0]) - len(luxck__iijjk[0].lstrip())
    fhsv__gut = 'def impl(S, lower_bound, upper_bound):\n'
    fhsv__gut += '   n = len(S)\n'
    fhsv__gut += '   arr = bodo.utils.conversion.coerce_to_array(S)\n'
    fhsv__gut += '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n'
    fhsv__gut += '   if upper_bound < lower_bound:\n'
    fhsv__gut += '      for i in range(n):\n'
    fhsv__gut += '         bodo.libs.array_kernels.setna(res, i)\n'
    if constant_block != None:
        fhsv__gut += '   elif lower_bound <= -n+1 and n-1 <= upper_bound:\n'
        fhsv__gut += '      if S.count() == 0:\n'
        fhsv__gut += '         for i in range(n):\n'
        fhsv__gut += '\n'.join([(' ' * 12 + qgqph__agpn[lajvq__nrvvu:]) for
            qgqph__agpn in luxck__iijjk]) + '\n'
        fhsv__gut += '      else:\n'
        fhsv__gut += '\n'.join([(' ' * 9 + qgqph__agpn[oonx__dxkct:]) for
            qgqph__agpn in ujtry__xakn]) + '\n'
        fhsv__gut += '         for i in range(n):\n'
        fhsv__gut += '            res[i] = constant_value\n'
    fhsv__gut += '   else:\n'
    fhsv__gut += '      exiting = lower_bound\n'
    fhsv__gut += '      entering = upper_bound\n'
    fhsv__gut += '      in_window = 0\n'
    if setup_block != None:
        fhsv__gut += '\n'.join([(' ' * 6 + qgqph__agpn[gdhwn__iynr:]) for
            qgqph__agpn in qnvtg__oflab]) + '\n'
    fhsv__gut += (
        '      for i in range(min(max(0, exiting), n), min(max(0, entering + 1), n)):\n'
        )
    fhsv__gut += '         if not bodo.libs.array_kernels.isna(arr, i):\n'
    fhsv__gut += '            in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            fhsv__gut += '            elem = arr[i]\n'
        fhsv__gut += '\n'.join([(' ' * 12 + qgqph__agpn[jdc__aai:]) for
            qgqph__agpn in lmhrv__rvbk]) + '\n'
    fhsv__gut += '      for i in range(n):\n'
    fhsv__gut += '         if in_window == 0:\n'
    fhsv__gut += '\n'.join([(' ' * 12 + qgqph__agpn[lajvq__nrvvu:]) for
        qgqph__agpn in luxck__iijjk]) + '\n'
    fhsv__gut += '         else:\n'
    fhsv__gut += '\n'.join([(' ' * 12 + qgqph__agpn[yxwjq__mjec:]) for
        qgqph__agpn in myio__ydq]) + '\n'
    fhsv__gut += '         if 0 <= exiting < n:\n'
    fhsv__gut += (
        '            if not bodo.libs.array_kernels.isna(arr, exiting):\n')
    fhsv__gut += '               in_window -= 1\n'
    if exit_block != None:
        if 'elem' in exit_block:
            fhsv__gut += '               elem = arr[exiting]\n'
        fhsv__gut += '\n'.join([(' ' * 15 + qgqph__agpn[hsn__swdw:]) for
            qgqph__agpn in oko__ueqrz]) + '\n'
    fhsv__gut += '         exiting += 1\n'
    fhsv__gut += '         entering += 1\n'
    fhsv__gut += '         if 0 <= entering < n:\n'
    fhsv__gut += (
        '            if not bodo.libs.array_kernels.isna(arr, entering):\n')
    fhsv__gut += '               in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            fhsv__gut += '               elem = arr[entering]\n'
        fhsv__gut += '\n'.join([(' ' * 15 + qgqph__agpn[jdc__aai:]) for
            qgqph__agpn in lmhrv__rvbk]) + '\n'
    fhsv__gut += '   return res'
    akhl__tmeo = {}
    exec(fhsv__gut, {'bodo': bodo, 'numba': numba, 'np': np, 'out_dtype':
        out_dtype, 'pd': pd}, akhl__tmeo)
    btduy__qsp = akhl__tmeo['impl']
    return btduy__qsp
