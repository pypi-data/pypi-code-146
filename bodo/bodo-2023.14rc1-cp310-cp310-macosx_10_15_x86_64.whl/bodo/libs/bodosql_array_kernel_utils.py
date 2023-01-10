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
    otw__oolr = text.splitlines()[0]
    i = len(otw__oolr) - len(otw__oolr.lstrip())
    return '\n'.join([(' ' * indentation + ywk__lbwgk[i:]) for ywk__lbwgk in
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
    isz__fdvhl = [bodo.utils.utils.is_array_typ(hdhy__kfdw, True) for
        hdhy__kfdw in arg_types]
    wfiip__msm = not any(isz__fdvhl)
    crb__zpje = any([propagate_null[i] for i in range(len(arg_types)) if 
        arg_types[i] == bodo.none])
    fwrg__ibc = False
    if synthesize_dict_if_vector is not None:
        assert synthesize_dict_setup_text is not None, 'synthesize_dict_setup_text must be provided if synthesize_dict_if_vector is provided'
        assert synthesize_dict_scalar_text is not None, 'synthesize_dict_scalar_text must be provided if synthesize_dict_if_vector is provided'
        fwrg__ibc = True
        for i in range(len(arg_types)):
            if isz__fdvhl[i] and synthesize_dict_if_vector[i] == 'S':
                fwrg__ibc = False
            if not isz__fdvhl[i] and synthesize_dict_if_vector[i] == 'V':
                fwrg__ibc = False
    zey__ushbf = 0
    iuvsv__kyib = -1
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            zey__ushbf += 1
            if arg_types[i] == bodo.dict_str_arr_type:
                iuvsv__kyib = i
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            zey__ushbf += 1
            if arg_types[i].data == bodo.dict_str_arr_type:
                iuvsv__kyib = i
    nqpn__dvvun = (support_dict_encoding and zey__ushbf == 1 and 
        iuvsv__kyib >= 0)
    momth__fre = nqpn__dvvun and out_dtype == bodo.string_array_type and (any
        (arg_types[i] == bodo.none and propagate_null[i] for i in range(len
        (arg_types))) or 'bodo.libs.array_kernels.setna' in scalar_text)
    if arg_string is None:
        arg_string = ', '.join(arg_names)
    eacxi__ebb = f'def impl({arg_string}):\n'
    if arg_sources is not None:
        for hdro__vuuak, pzn__ajd in arg_sources.items():
            eacxi__ebb += f'   {hdro__vuuak} = {pzn__ajd}\n'
    if wfiip__msm and array_override == None:
        if crb__zpje:
            eacxi__ebb += '   return None'
        else:
            eacxi__ebb += indent_block(prefix_code, 3)
            for i in range(len(arg_names)):
                eacxi__ebb += f'   arg{i} = {arg_names[i]}\n'
            yinmt__lwqjq = scalar_text.replace('res[i] =', 'answer =').replace(
                'bodo.libs.array_kernels.setna(res, i)', 'return None')
            eacxi__ebb += indent_block(yinmt__lwqjq, 3)
            eacxi__ebb += '   return answer'
    else:
        for i in range(len(arg_names)):
            if bodo.hiframes.pd_series_ext.is_series_type(arg_types[i]):
                eacxi__ebb += f"""   {arg_names[i]} = bodo.hiframes.pd_series_ext.get_series_data({arg_names[i]})
"""
        if array_override != None:
            iqx__zio = f'len({array_override})'
        else:
            for i in range(len(arg_names)):
                if isz__fdvhl[i]:
                    iqx__zio = f'len({arg_names[i]})'
                    break
        if nqpn__dvvun:
            if out_dtype == bodo.string_array_type:
                eacxi__ebb += (
                    f'   indices = {arg_names[iuvsv__kyib]}._indices.copy()\n')
                eacxi__ebb += (
                    f'   has_global = {arg_names[iuvsv__kyib]}._has_global_dictionary\n'
                    )
                if may_cause_duplicate_dict_array_values:
                    eacxi__ebb += f'   is_dict_unique = False\n'
                else:
                    eacxi__ebb += f"""   is_dict_unique = {arg_names[iuvsv__kyib]}._has_deduped_local_dictionary
"""
                eacxi__ebb += (
                    f'   {arg_names[i]} = {arg_names[iuvsv__kyib]}._data\n')
            else:
                eacxi__ebb += (
                    f'   indices = {arg_names[iuvsv__kyib]}._indices\n')
                eacxi__ebb += (
                    f'   {arg_names[i]} = {arg_names[iuvsv__kyib]}._data\n')
        eacxi__ebb += f'   n = {iqx__zio}\n'
        if prefix_code is not None and not crb__zpje:
            eacxi__ebb += indent_block(prefix_code, 3)
        if fwrg__ibc:
            eacxi__ebb += indent_block(synthesize_dict_setup_text, 3)
            out_dtype = bodo.libs.dict_arr_ext.dict_indices_arr_type
            eacxi__ebb += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            eacxi__ebb += '   numba.parfors.parfor.init_prange()\n'
            eacxi__ebb += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        elif nqpn__dvvun:
            qvcll__hccwi = 'n' if propagate_null[iuvsv__kyib] else '(n + 1)'
            if not propagate_null[iuvsv__kyib]:
                rtvj__tppw = arg_names[iuvsv__kyib]
                eacxi__ebb += f"""   {rtvj__tppw} = bodo.libs.array_kernels.concat([{rtvj__tppw}, bodo.libs.array_kernels.gen_na_array(1, {rtvj__tppw})])
"""
            if out_dtype == bodo.string_array_type:
                eacxi__ebb += f"""   res = bodo.libs.str_arr_ext.pre_alloc_string_array({qvcll__hccwi}, -1)
"""
            else:
                eacxi__ebb += f"""   res = bodo.utils.utils.alloc_type({qvcll__hccwi}, out_dtype, (-1,))
"""
            eacxi__ebb += f'   for i in range({qvcll__hccwi}):\n'
        elif res_list:
            eacxi__ebb += '   res = []\n'
            eacxi__ebb += '   for i in range(n):\n'
        else:
            eacxi__ebb += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            eacxi__ebb += '   numba.parfors.parfor.init_prange()\n'
            eacxi__ebb += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        if crb__zpje:
            eacxi__ebb += f'      bodo.libs.array_kernels.setna(res, i)\n'
        else:
            for i in range(len(arg_names)):
                if isz__fdvhl[i]:
                    if propagate_null[i]:
                        eacxi__ebb += (
                            f'      if bodo.libs.array_kernels.isna({arg_names[i]}, i):\n'
                            )
                        if res_list:
                            eacxi__ebb += '         res.append(None)\n'
                        else:
                            eacxi__ebb += (
                                '         bodo.libs.array_kernels.setna(res, i)\n'
                                )
                        eacxi__ebb += '         continue\n'
            for i in range(len(arg_names)):
                if isz__fdvhl[i]:
                    if alloc_array_scalars:
                        eacxi__ebb += f'      arg{i} = {arg_names[i]}[i]\n'
                else:
                    eacxi__ebb += f'      arg{i} = {arg_names[i]}\n'
            if not fwrg__ibc:
                eacxi__ebb += indent_block(scalar_text, 6)
            else:
                eacxi__ebb += indent_block(synthesize_dict_scalar_text, 6)
        if nqpn__dvvun:
            if momth__fre:
                eacxi__ebb += '   numba.parfors.parfor.init_prange()\n'
                eacxi__ebb += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                eacxi__ebb += (
                    '      if not bodo.libs.array_kernels.isna(indices, i):\n')
                eacxi__ebb += '         loc = indices[i]\n'
                eacxi__ebb += (
                    '         if bodo.libs.array_kernels.isna(res, loc):\n')
                eacxi__ebb += (
                    '            bodo.libs.array_kernels.setna(indices, i)\n')
            if out_dtype == bodo.string_array_type:
                eacxi__ebb += """   res = bodo.libs.dict_arr_ext.init_dict_arr(res, indices, has_global, is_dict_unique)
"""
            else:
                eacxi__ebb += """   res2 = bodo.utils.utils.alloc_type(len(indices), out_dtype, (-1,))
"""
                eacxi__ebb += '   numba.parfors.parfor.init_prange()\n'
                eacxi__ebb += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                if propagate_null[iuvsv__kyib]:
                    eacxi__ebb += (
                        '      if bodo.libs.array_kernels.isna(indices, i):\n')
                    eacxi__ebb += (
                        '         bodo.libs.array_kernels.setna(res2, i)\n')
                    eacxi__ebb += '         continue\n'
                    eacxi__ebb += '      loc = indices[i]\n'
                else:
                    eacxi__ebb += """      loc = n if bodo.libs.array_kernels.isna(indices, i) else indices[i]
"""
                eacxi__ebb += (
                    '      if bodo.libs.array_kernels.isna(res, loc):\n')
                eacxi__ebb += (
                    '         bodo.libs.array_kernels.setna(res2, i)\n')
                eacxi__ebb += '      else:\n'
                eacxi__ebb += '         res2[i] = res[loc]\n'
                eacxi__ebb += '   res = res2\n'
        eacxi__ebb += indent_block(suffix_code, 3)
        if fwrg__ibc:
            eacxi__ebb += f"""   return bodo.libs.dict_arr_ext.init_dict_arr(dict_res, res, {synthesize_dict_global}, {synthesize_dict_unique})
"""
        else:
            eacxi__ebb += '   return res'
    wzuz__nbdfz = {}
    mag__usqo = {'bodo': bodo, 'math': math, 'numba': numba, 're': re, 'np':
        np, 'out_dtype': out_dtype, 'pd': pd}
    if not extra_globals is None:
        mag__usqo.update(extra_globals)
    exec(eacxi__ebb, mag__usqo, wzuz__nbdfz)
    lbni__bximf = wzuz__nbdfz['impl']
    return lbni__bximf


def unopt_argument(func_name, arg_names, i, container_arg=0,
    container_length=None):
    if container_length != None:
        cgp__lqxw = [(f'{arg_names[i]}{[pihes__flo]}' if pihes__flo !=
            container_arg else 'None') for pihes__flo in range(
            container_length)]
        aku__yzur = ',' if container_length != 0 else ''
        ypz__osbv = f"({', '.join(cgp__lqxw)}{aku__yzur})"
        cee__vvj = [(f'{arg_names[i]}{[pihes__flo]}' if pihes__flo !=
            container_arg else
            f'bodo.utils.indexing.unoptional({arg_names[i]}[{pihes__flo}])'
            ) for pihes__flo in range(container_length)]
        brwv__meaqm = f"({', '.join(cee__vvj)}{aku__yzur})"
        ute__xfpij = [(arg_names[pihes__flo] if pihes__flo != i else
            ypz__osbv) for pihes__flo in range(len(arg_names))]
        ynlv__hvf = [(arg_names[pihes__flo] if pihes__flo != i else
            brwv__meaqm) for pihes__flo in range(len(arg_names))]
        eacxi__ebb = f"def impl({', '.join(arg_names)}):\n"
        eacxi__ebb += f'   if {arg_names[i]}[{container_arg}] is None:\n'
        eacxi__ebb += f"      return {func_name}({', '.join(ute__xfpij)})\n"
        eacxi__ebb += f'   else:\n'
        eacxi__ebb += f"      return {func_name}({', '.join(ynlv__hvf)})\n"
    else:
        cgp__lqxw = [(arg_names[pihes__flo] if pihes__flo != i else 'None') for
            pihes__flo in range(len(arg_names))]
        cee__vvj = [(arg_names[pihes__flo] if pihes__flo != i else
            f'bodo.utils.indexing.unoptional({arg_names[pihes__flo]})') for
            pihes__flo in range(len(arg_names))]
        eacxi__ebb = f"def impl({', '.join(arg_names)}):\n"
        eacxi__ebb += f'   if {arg_names[i]} is None:\n'
        eacxi__ebb += f"      return {func_name}({', '.join(cgp__lqxw)})\n"
        eacxi__ebb += f'   else:\n'
        eacxi__ebb += f"      return {func_name}({', '.join(cee__vvj)})\n"
    wzuz__nbdfz = {}
    exec(eacxi__ebb, {'bodo': bodo, 'numba': numba}, wzuz__nbdfz)
    lbni__bximf = wzuz__nbdfz['impl']
    return lbni__bximf


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
    ccm__mdh = is_valid_string_arg(arg)
    gvovb__asnxc = is_valid_binary_arg(arg)
    if ccm__mdh or gvovb__asnxc:
        return ccm__mdh
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
    owyyr__wck = []
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            owyyr__wck.append(arg_types[i])
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            owyyr__wck.append(arg_types[i].data)
        else:
            owyyr__wck.append(arg_types[i])
    if len(owyyr__wck) == 0:
        return bodo.none
    elif len(owyyr__wck) == 1:
        if bodo.utils.utils.is_array_typ(owyyr__wck[0]):
            return bodo.utils.typing.to_nullable_type(owyyr__wck[0])
        elif owyyr__wck[0] == bodo.none:
            return bodo.none
        else:
            return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
                dtype_to_array_type(owyyr__wck[0]))
    else:
        rmi__ncd = []
        for i in range(len(arg_types)):
            if bodo.utils.utils.is_array_typ(arg_types[i]):
                rmi__ncd.append(owyyr__wck[i].dtype)
            elif owyyr__wck[i] == bodo.none:
                pass
            else:
                rmi__ncd.append(owyyr__wck[i])
        if len(rmi__ncd) == 0:
            return bodo.none
        zmw__aaj, fssk__zoe = bodo.utils.typing.get_common_scalar_dtype(
            rmi__ncd)
        if not fssk__zoe:
            raise_bodo_error(
                f'Cannot call {func_name} on columns with different dtypes')
        return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
            dtype_to_array_type(zmw__aaj))


def vectorized_sol(args, scalar_fn, dtype, manual_coercion=False):
    fwxe__qxjn = -1
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            fwxe__qxjn = len(arg)
            break
    if fwxe__qxjn == -1:
        return dtype(scalar_fn(*args)) if manual_coercion else scalar_fn(*args)
    hcydn__pale = []
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            hcydn__pale.append(arg)
        else:
            hcydn__pale.append([arg] * fwxe__qxjn)
    if manual_coercion:
        return pd.Series([dtype(scalar_fn(*azagu__qvqf)) for azagu__qvqf in
            zip(*hcydn__pale)])
    else:
        return pd.Series([scalar_fn(*azagu__qvqf) for azagu__qvqf in zip(*
            hcydn__pale)], dtype=dtype)


def gen_windowed(calculate_block, constant_block, out_dtype, setup_block=
    None, enter_block=None, exit_block=None, empty_block=None):
    eyka__dwfv = calculate_block.splitlines()
    fsnyi__ktwy = len(eyka__dwfv[0]) - len(eyka__dwfv[0].lstrip())
    if constant_block != None:
        rgtik__ejuvh = constant_block.splitlines()
        dfjr__gwmc = len(rgtik__ejuvh[0]) - len(rgtik__ejuvh[0].lstrip())
    if setup_block != None:
        uwtf__prazi = setup_block.splitlines()
        fvlm__jmy = len(uwtf__prazi[0]) - len(uwtf__prazi[0].lstrip())
    if enter_block != None:
        puru__osg = enter_block.splitlines()
        mwtmu__tkk = len(puru__osg[0]) - len(puru__osg[0].lstrip())
    if exit_block != None:
        ubqtn__bqv = exit_block.splitlines()
        nxtd__sbor = len(ubqtn__bqv[0]) - len(ubqtn__bqv[0].lstrip())
    if empty_block == None:
        empty_block = 'bodo.libs.array_kernels.setna(res, i)'
    mdnf__yndm = empty_block.splitlines()
    xnd__qnpu = len(mdnf__yndm[0]) - len(mdnf__yndm[0].lstrip())
    eacxi__ebb = 'def impl(S, lower_bound, upper_bound):\n'
    eacxi__ebb += '   n = len(S)\n'
    eacxi__ebb += '   arr = bodo.utils.conversion.coerce_to_array(S)\n'
    eacxi__ebb += '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n'
    eacxi__ebb += '   if upper_bound < lower_bound:\n'
    eacxi__ebb += '      for i in range(n):\n'
    eacxi__ebb += '         bodo.libs.array_kernels.setna(res, i)\n'
    if constant_block != None:
        eacxi__ebb += '   elif lower_bound <= -n+1 and n-1 <= upper_bound:\n'
        eacxi__ebb += '      if S.count() == 0:\n'
        eacxi__ebb += '         for i in range(n):\n'
        eacxi__ebb += '\n'.join([(' ' * 12 + ywk__lbwgk[xnd__qnpu:]) for
            ywk__lbwgk in mdnf__yndm]) + '\n'
        eacxi__ebb += '      else:\n'
        eacxi__ebb += '\n'.join([(' ' * 9 + ywk__lbwgk[dfjr__gwmc:]) for
            ywk__lbwgk in rgtik__ejuvh]) + '\n'
        eacxi__ebb += '         for i in range(n):\n'
        eacxi__ebb += '            res[i] = constant_value\n'
    eacxi__ebb += '   else:\n'
    eacxi__ebb += '      exiting = lower_bound\n'
    eacxi__ebb += '      entering = upper_bound\n'
    eacxi__ebb += '      in_window = 0\n'
    if setup_block != None:
        eacxi__ebb += '\n'.join([(' ' * 6 + ywk__lbwgk[fvlm__jmy:]) for
            ywk__lbwgk in uwtf__prazi]) + '\n'
    eacxi__ebb += (
        '      for i in range(min(max(0, exiting), n), min(max(0, entering + 1), n)):\n'
        )
    eacxi__ebb += '         if not bodo.libs.array_kernels.isna(arr, i):\n'
    eacxi__ebb += '            in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            eacxi__ebb += '            elem = arr[i]\n'
        eacxi__ebb += '\n'.join([(' ' * 12 + ywk__lbwgk[mwtmu__tkk:]) for
            ywk__lbwgk in puru__osg]) + '\n'
    eacxi__ebb += '      for i in range(n):\n'
    eacxi__ebb += '         if in_window == 0:\n'
    eacxi__ebb += '\n'.join([(' ' * 12 + ywk__lbwgk[xnd__qnpu:]) for
        ywk__lbwgk in mdnf__yndm]) + '\n'
    eacxi__ebb += '         else:\n'
    eacxi__ebb += '\n'.join([(' ' * 12 + ywk__lbwgk[fsnyi__ktwy:]) for
        ywk__lbwgk in eyka__dwfv]) + '\n'
    eacxi__ebb += '         if 0 <= exiting < n:\n'
    eacxi__ebb += (
        '            if not bodo.libs.array_kernels.isna(arr, exiting):\n')
    eacxi__ebb += '               in_window -= 1\n'
    if exit_block != None:
        if 'elem' in exit_block:
            eacxi__ebb += '               elem = arr[exiting]\n'
        eacxi__ebb += '\n'.join([(' ' * 15 + ywk__lbwgk[nxtd__sbor:]) for
            ywk__lbwgk in ubqtn__bqv]) + '\n'
    eacxi__ebb += '         exiting += 1\n'
    eacxi__ebb += '         entering += 1\n'
    eacxi__ebb += '         if 0 <= entering < n:\n'
    eacxi__ebb += (
        '            if not bodo.libs.array_kernels.isna(arr, entering):\n')
    eacxi__ebb += '               in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            eacxi__ebb += '               elem = arr[entering]\n'
        eacxi__ebb += '\n'.join([(' ' * 15 + ywk__lbwgk[mwtmu__tkk:]) for
            ywk__lbwgk in puru__osg]) + '\n'
    eacxi__ebb += '   return res'
    wzuz__nbdfz = {}
    exec(eacxi__ebb, {'bodo': bodo, 'numba': numba, 'np': np, 'out_dtype':
        out_dtype, 'pd': pd}, wzuz__nbdfz)
    lbni__bximf = wzuz__nbdfz['impl']
    return lbni__bximf
