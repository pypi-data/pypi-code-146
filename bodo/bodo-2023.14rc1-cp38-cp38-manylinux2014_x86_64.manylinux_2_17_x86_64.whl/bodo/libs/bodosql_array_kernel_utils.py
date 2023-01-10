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
    fffr__jbdae = text.splitlines()[0]
    i = len(fffr__jbdae) - len(fffr__jbdae.lstrip())
    return '\n'.join([(' ' * indentation + inced__owx[i:]) for inced__owx in
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
    eqbrn__kvly = [bodo.utils.utils.is_array_typ(mbryx__fuzl, True) for
        mbryx__fuzl in arg_types]
    mndff__oep = not any(eqbrn__kvly)
    vasn__sbw = any([propagate_null[i] for i in range(len(arg_types)) if 
        arg_types[i] == bodo.none])
    ukn__rkm = False
    if synthesize_dict_if_vector is not None:
        assert synthesize_dict_setup_text is not None, 'synthesize_dict_setup_text must be provided if synthesize_dict_if_vector is provided'
        assert synthesize_dict_scalar_text is not None, 'synthesize_dict_scalar_text must be provided if synthesize_dict_if_vector is provided'
        ukn__rkm = True
        for i in range(len(arg_types)):
            if eqbrn__kvly[i] and synthesize_dict_if_vector[i] == 'S':
                ukn__rkm = False
            if not eqbrn__kvly[i] and synthesize_dict_if_vector[i] == 'V':
                ukn__rkm = False
    ofpgu__jny = 0
    hybqu__npz = -1
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            ofpgu__jny += 1
            if arg_types[i] == bodo.dict_str_arr_type:
                hybqu__npz = i
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            ofpgu__jny += 1
            if arg_types[i].data == bodo.dict_str_arr_type:
                hybqu__npz = i
    bnz__anmt = support_dict_encoding and ofpgu__jny == 1 and hybqu__npz >= 0
    oyjb__dasq = bnz__anmt and out_dtype == bodo.string_array_type and (any
        (arg_types[i] == bodo.none and propagate_null[i] for i in range(len
        (arg_types))) or 'bodo.libs.array_kernels.setna' in scalar_text)
    if arg_string is None:
        arg_string = ', '.join(arg_names)
    eocx__wuove = f'def impl({arg_string}):\n'
    if arg_sources is not None:
        for gtt__nnsyx, ezy__fgs in arg_sources.items():
            eocx__wuove += f'   {gtt__nnsyx} = {ezy__fgs}\n'
    if mndff__oep and array_override == None:
        if vasn__sbw:
            eocx__wuove += '   return None'
        else:
            eocx__wuove += indent_block(prefix_code, 3)
            for i in range(len(arg_names)):
                eocx__wuove += f'   arg{i} = {arg_names[i]}\n'
            xokiz__xiq = scalar_text.replace('res[i] =', 'answer =').replace(
                'bodo.libs.array_kernels.setna(res, i)', 'return None')
            eocx__wuove += indent_block(xokiz__xiq, 3)
            eocx__wuove += '   return answer'
    else:
        for i in range(len(arg_names)):
            if bodo.hiframes.pd_series_ext.is_series_type(arg_types[i]):
                eocx__wuove += f"""   {arg_names[i]} = bodo.hiframes.pd_series_ext.get_series_data({arg_names[i]})
"""
        if array_override != None:
            cvvk__ufy = f'len({array_override})'
        else:
            for i in range(len(arg_names)):
                if eqbrn__kvly[i]:
                    cvvk__ufy = f'len({arg_names[i]})'
                    break
        if bnz__anmt:
            if out_dtype == bodo.string_array_type:
                eocx__wuove += (
                    f'   indices = {arg_names[hybqu__npz]}._indices.copy()\n')
                eocx__wuove += (
                    f'   has_global = {arg_names[hybqu__npz]}._has_global_dictionary\n'
                    )
                if may_cause_duplicate_dict_array_values:
                    eocx__wuove += f'   is_dict_unique = False\n'
                else:
                    eocx__wuove += f"""   is_dict_unique = {arg_names[hybqu__npz]}._has_deduped_local_dictionary
"""
                eocx__wuove += (
                    f'   {arg_names[i]} = {arg_names[hybqu__npz]}._data\n')
            else:
                eocx__wuove += (
                    f'   indices = {arg_names[hybqu__npz]}._indices\n')
                eocx__wuove += (
                    f'   {arg_names[i]} = {arg_names[hybqu__npz]}._data\n')
        eocx__wuove += f'   n = {cvvk__ufy}\n'
        if prefix_code is not None and not vasn__sbw:
            eocx__wuove += indent_block(prefix_code, 3)
        if ukn__rkm:
            eocx__wuove += indent_block(synthesize_dict_setup_text, 3)
            out_dtype = bodo.libs.dict_arr_ext.dict_indices_arr_type
            eocx__wuove += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            eocx__wuove += '   numba.parfors.parfor.init_prange()\n'
            eocx__wuove += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        elif bnz__anmt:
            lrs__ajc = 'n' if propagate_null[hybqu__npz] else '(n + 1)'
            if not propagate_null[hybqu__npz]:
                ullsj__obzoo = arg_names[hybqu__npz]
                eocx__wuove += f"""   {ullsj__obzoo} = bodo.libs.array_kernels.concat([{ullsj__obzoo}, bodo.libs.array_kernels.gen_na_array(1, {ullsj__obzoo})])
"""
            if out_dtype == bodo.string_array_type:
                eocx__wuove += f"""   res = bodo.libs.str_arr_ext.pre_alloc_string_array({lrs__ajc}, -1)
"""
            else:
                eocx__wuove += f"""   res = bodo.utils.utils.alloc_type({lrs__ajc}, out_dtype, (-1,))
"""
            eocx__wuove += f'   for i in range({lrs__ajc}):\n'
        elif res_list:
            eocx__wuove += '   res = []\n'
            eocx__wuove += '   for i in range(n):\n'
        else:
            eocx__wuove += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            eocx__wuove += '   numba.parfors.parfor.init_prange()\n'
            eocx__wuove += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        if vasn__sbw:
            eocx__wuove += f'      bodo.libs.array_kernels.setna(res, i)\n'
        else:
            for i in range(len(arg_names)):
                if eqbrn__kvly[i]:
                    if propagate_null[i]:
                        eocx__wuove += f"""      if bodo.libs.array_kernels.isna({arg_names[i]}, i):
"""
                        if res_list:
                            eocx__wuove += '         res.append(None)\n'
                        else:
                            eocx__wuove += (
                                '         bodo.libs.array_kernels.setna(res, i)\n'
                                )
                        eocx__wuove += '         continue\n'
            for i in range(len(arg_names)):
                if eqbrn__kvly[i]:
                    if alloc_array_scalars:
                        eocx__wuove += f'      arg{i} = {arg_names[i]}[i]\n'
                else:
                    eocx__wuove += f'      arg{i} = {arg_names[i]}\n'
            if not ukn__rkm:
                eocx__wuove += indent_block(scalar_text, 6)
            else:
                eocx__wuove += indent_block(synthesize_dict_scalar_text, 6)
        if bnz__anmt:
            if oyjb__dasq:
                eocx__wuove += '   numba.parfors.parfor.init_prange()\n'
                eocx__wuove += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                eocx__wuove += (
                    '      if not bodo.libs.array_kernels.isna(indices, i):\n')
                eocx__wuove += '         loc = indices[i]\n'
                eocx__wuove += (
                    '         if bodo.libs.array_kernels.isna(res, loc):\n')
                eocx__wuove += (
                    '            bodo.libs.array_kernels.setna(indices, i)\n')
            if out_dtype == bodo.string_array_type:
                eocx__wuove += """   res = bodo.libs.dict_arr_ext.init_dict_arr(res, indices, has_global, is_dict_unique)
"""
            else:
                eocx__wuove += """   res2 = bodo.utils.utils.alloc_type(len(indices), out_dtype, (-1,))
"""
                eocx__wuove += '   numba.parfors.parfor.init_prange()\n'
                eocx__wuove += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                if propagate_null[hybqu__npz]:
                    eocx__wuove += (
                        '      if bodo.libs.array_kernels.isna(indices, i):\n')
                    eocx__wuove += (
                        '         bodo.libs.array_kernels.setna(res2, i)\n')
                    eocx__wuove += '         continue\n'
                    eocx__wuove += '      loc = indices[i]\n'
                else:
                    eocx__wuove += """      loc = n if bodo.libs.array_kernels.isna(indices, i) else indices[i]
"""
                eocx__wuove += (
                    '      if bodo.libs.array_kernels.isna(res, loc):\n')
                eocx__wuove += (
                    '         bodo.libs.array_kernels.setna(res2, i)\n')
                eocx__wuove += '      else:\n'
                eocx__wuove += '         res2[i] = res[loc]\n'
                eocx__wuove += '   res = res2\n'
        eocx__wuove += indent_block(suffix_code, 3)
        if ukn__rkm:
            eocx__wuove += f"""   return bodo.libs.dict_arr_ext.init_dict_arr(dict_res, res, {synthesize_dict_global}, {synthesize_dict_unique})
"""
        else:
            eocx__wuove += '   return res'
    cognb__ahby = {}
    rrl__jiq = {'bodo': bodo, 'math': math, 'numba': numba, 're': re, 'np':
        np, 'out_dtype': out_dtype, 'pd': pd}
    if not extra_globals is None:
        rrl__jiq.update(extra_globals)
    exec(eocx__wuove, rrl__jiq, cognb__ahby)
    waqzm__xxx = cognb__ahby['impl']
    return waqzm__xxx


def unopt_argument(func_name, arg_names, i, container_arg=0,
    container_length=None):
    if container_length != None:
        rnz__uqjpp = [(f'{arg_names[i]}{[dava__djbfh]}' if dava__djbfh !=
            container_arg else 'None') for dava__djbfh in range(
            container_length)]
        xow__jcrf = ',' if container_length != 0 else ''
        mrmqk__bpg = f"({', '.join(rnz__uqjpp)}{xow__jcrf})"
        pey__ighre = [(f'{arg_names[i]}{[dava__djbfh]}' if dava__djbfh !=
            container_arg else
            f'bodo.utils.indexing.unoptional({arg_names[i]}[{dava__djbfh}])'
            ) for dava__djbfh in range(container_length)]
        fms__leveu = f"({', '.join(pey__ighre)}{xow__jcrf})"
        gnivz__peoda = [(arg_names[dava__djbfh] if dava__djbfh != i else
            mrmqk__bpg) for dava__djbfh in range(len(arg_names))]
        trs__awud = [(arg_names[dava__djbfh] if dava__djbfh != i else
            fms__leveu) for dava__djbfh in range(len(arg_names))]
        eocx__wuove = f"def impl({', '.join(arg_names)}):\n"
        eocx__wuove += f'   if {arg_names[i]}[{container_arg}] is None:\n'
        eocx__wuove += f"      return {func_name}({', '.join(gnivz__peoda)})\n"
        eocx__wuove += f'   else:\n'
        eocx__wuove += f"      return {func_name}({', '.join(trs__awud)})\n"
    else:
        rnz__uqjpp = [(arg_names[dava__djbfh] if dava__djbfh != i else
            'None') for dava__djbfh in range(len(arg_names))]
        pey__ighre = [(arg_names[dava__djbfh] if dava__djbfh != i else
            f'bodo.utils.indexing.unoptional({arg_names[dava__djbfh]})') for
            dava__djbfh in range(len(arg_names))]
        eocx__wuove = f"def impl({', '.join(arg_names)}):\n"
        eocx__wuove += f'   if {arg_names[i]} is None:\n'
        eocx__wuove += f"      return {func_name}({', '.join(rnz__uqjpp)})\n"
        eocx__wuove += f'   else:\n'
        eocx__wuove += f"      return {func_name}({', '.join(pey__ighre)})\n"
    cognb__ahby = {}
    exec(eocx__wuove, {'bodo': bodo, 'numba': numba}, cognb__ahby)
    waqzm__xxx = cognb__ahby['impl']
    return waqzm__xxx


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
    acc__lmixp = is_valid_string_arg(arg)
    seb__pbe = is_valid_binary_arg(arg)
    if acc__lmixp or seb__pbe:
        return acc__lmixp
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
    fxe__plcew = []
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            fxe__plcew.append(arg_types[i])
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            fxe__plcew.append(arg_types[i].data)
        else:
            fxe__plcew.append(arg_types[i])
    if len(fxe__plcew) == 0:
        return bodo.none
    elif len(fxe__plcew) == 1:
        if bodo.utils.utils.is_array_typ(fxe__plcew[0]):
            return bodo.utils.typing.to_nullable_type(fxe__plcew[0])
        elif fxe__plcew[0] == bodo.none:
            return bodo.none
        else:
            return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
                dtype_to_array_type(fxe__plcew[0]))
    else:
        jwc__msrqx = []
        for i in range(len(arg_types)):
            if bodo.utils.utils.is_array_typ(arg_types[i]):
                jwc__msrqx.append(fxe__plcew[i].dtype)
            elif fxe__plcew[i] == bodo.none:
                pass
            else:
                jwc__msrqx.append(fxe__plcew[i])
        if len(jwc__msrqx) == 0:
            return bodo.none
        xbm__vmyla, zjy__swdp = bodo.utils.typing.get_common_scalar_dtype(
            jwc__msrqx)
        if not zjy__swdp:
            raise_bodo_error(
                f'Cannot call {func_name} on columns with different dtypes')
        return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
            dtype_to_array_type(xbm__vmyla))


def vectorized_sol(args, scalar_fn, dtype, manual_coercion=False):
    dosn__svbnn = -1
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            dosn__svbnn = len(arg)
            break
    if dosn__svbnn == -1:
        return dtype(scalar_fn(*args)) if manual_coercion else scalar_fn(*args)
    ejgi__kkzrn = []
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            ejgi__kkzrn.append(arg)
        else:
            ejgi__kkzrn.append([arg] * dosn__svbnn)
    if manual_coercion:
        return pd.Series([dtype(scalar_fn(*cjepm__ubp)) for cjepm__ubp in
            zip(*ejgi__kkzrn)])
    else:
        return pd.Series([scalar_fn(*cjepm__ubp) for cjepm__ubp in zip(*
            ejgi__kkzrn)], dtype=dtype)


def gen_windowed(calculate_block, constant_block, out_dtype, setup_block=
    None, enter_block=None, exit_block=None, empty_block=None):
    neez__peys = calculate_block.splitlines()
    kofjb__moz = len(neez__peys[0]) - len(neez__peys[0].lstrip())
    if constant_block != None:
        sabli__uno = constant_block.splitlines()
        wqp__mjay = len(sabli__uno[0]) - len(sabli__uno[0].lstrip())
    if setup_block != None:
        dxd__xvv = setup_block.splitlines()
        zoy__yakx = len(dxd__xvv[0]) - len(dxd__xvv[0].lstrip())
    if enter_block != None:
        absbd__djb = enter_block.splitlines()
        maiaq__ynj = len(absbd__djb[0]) - len(absbd__djb[0].lstrip())
    if exit_block != None:
        tjvd__hnvg = exit_block.splitlines()
        xjis__eyhc = len(tjvd__hnvg[0]) - len(tjvd__hnvg[0].lstrip())
    if empty_block == None:
        empty_block = 'bodo.libs.array_kernels.setna(res, i)'
    yyh__fuk = empty_block.splitlines()
    cnqs__haz = len(yyh__fuk[0]) - len(yyh__fuk[0].lstrip())
    eocx__wuove = 'def impl(S, lower_bound, upper_bound):\n'
    eocx__wuove += '   n = len(S)\n'
    eocx__wuove += '   arr = bodo.utils.conversion.coerce_to_array(S)\n'
    eocx__wuove += (
        '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
    eocx__wuove += '   if upper_bound < lower_bound:\n'
    eocx__wuove += '      for i in range(n):\n'
    eocx__wuove += '         bodo.libs.array_kernels.setna(res, i)\n'
    if constant_block != None:
        eocx__wuove += '   elif lower_bound <= -n+1 and n-1 <= upper_bound:\n'
        eocx__wuove += '      if S.count() == 0:\n'
        eocx__wuove += '         for i in range(n):\n'
        eocx__wuove += '\n'.join([(' ' * 12 + inced__owx[cnqs__haz:]) for
            inced__owx in yyh__fuk]) + '\n'
        eocx__wuove += '      else:\n'
        eocx__wuove += '\n'.join([(' ' * 9 + inced__owx[wqp__mjay:]) for
            inced__owx in sabli__uno]) + '\n'
        eocx__wuove += '         for i in range(n):\n'
        eocx__wuove += '            res[i] = constant_value\n'
    eocx__wuove += '   else:\n'
    eocx__wuove += '      exiting = lower_bound\n'
    eocx__wuove += '      entering = upper_bound\n'
    eocx__wuove += '      in_window = 0\n'
    if setup_block != None:
        eocx__wuove += '\n'.join([(' ' * 6 + inced__owx[zoy__yakx:]) for
            inced__owx in dxd__xvv]) + '\n'
    eocx__wuove += (
        '      for i in range(min(max(0, exiting), n), min(max(0, entering + 1), n)):\n'
        )
    eocx__wuove += '         if not bodo.libs.array_kernels.isna(arr, i):\n'
    eocx__wuove += '            in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            eocx__wuove += '            elem = arr[i]\n'
        eocx__wuove += '\n'.join([(' ' * 12 + inced__owx[maiaq__ynj:]) for
            inced__owx in absbd__djb]) + '\n'
    eocx__wuove += '      for i in range(n):\n'
    eocx__wuove += '         if in_window == 0:\n'
    eocx__wuove += '\n'.join([(' ' * 12 + inced__owx[cnqs__haz:]) for
        inced__owx in yyh__fuk]) + '\n'
    eocx__wuove += '         else:\n'
    eocx__wuove += '\n'.join([(' ' * 12 + inced__owx[kofjb__moz:]) for
        inced__owx in neez__peys]) + '\n'
    eocx__wuove += '         if 0 <= exiting < n:\n'
    eocx__wuove += (
        '            if not bodo.libs.array_kernels.isna(arr, exiting):\n')
    eocx__wuove += '               in_window -= 1\n'
    if exit_block != None:
        if 'elem' in exit_block:
            eocx__wuove += '               elem = arr[exiting]\n'
        eocx__wuove += '\n'.join([(' ' * 15 + inced__owx[xjis__eyhc:]) for
            inced__owx in tjvd__hnvg]) + '\n'
    eocx__wuove += '         exiting += 1\n'
    eocx__wuove += '         entering += 1\n'
    eocx__wuove += '         if 0 <= entering < n:\n'
    eocx__wuove += (
        '            if not bodo.libs.array_kernels.isna(arr, entering):\n')
    eocx__wuove += '               in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            eocx__wuove += '               elem = arr[entering]\n'
        eocx__wuove += '\n'.join([(' ' * 15 + inced__owx[maiaq__ynj:]) for
            inced__owx in absbd__djb]) + '\n'
    eocx__wuove += '   return res'
    cognb__ahby = {}
    exec(eocx__wuove, {'bodo': bodo, 'numba': numba, 'np': np, 'out_dtype':
        out_dtype, 'pd': pd}, cognb__ahby)
    waqzm__xxx = cognb__ahby['impl']
    return waqzm__xxx
