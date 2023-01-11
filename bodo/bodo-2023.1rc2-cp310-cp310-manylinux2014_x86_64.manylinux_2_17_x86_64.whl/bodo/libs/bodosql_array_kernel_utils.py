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
    xkhfs__hvrz = text.splitlines()[0]
    i = len(xkhfs__hvrz) - len(xkhfs__hvrz.lstrip())
    return '\n'.join([(' ' * indentation + rpxq__jegeg[i:]) for rpxq__jegeg in
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
    pdrux__usq = [bodo.utils.utils.is_array_typ(pnmd__vlg, True) for
        pnmd__vlg in arg_types]
    hahp__kjh = not any(pdrux__usq)
    qxsnq__vos = any([propagate_null[i] for i in range(len(arg_types)) if 
        arg_types[i] == bodo.none])
    pzo__mlvxb = False
    if synthesize_dict_if_vector is not None:
        assert synthesize_dict_setup_text is not None, 'synthesize_dict_setup_text must be provided if synthesize_dict_if_vector is provided'
        assert synthesize_dict_scalar_text is not None, 'synthesize_dict_scalar_text must be provided if synthesize_dict_if_vector is provided'
        pzo__mlvxb = True
        for i in range(len(arg_types)):
            if pdrux__usq[i] and synthesize_dict_if_vector[i] == 'S':
                pzo__mlvxb = False
            if not pdrux__usq[i] and synthesize_dict_if_vector[i] == 'V':
                pzo__mlvxb = False
    tyqiw__jgvjc = 0
    irdb__ttzpv = -1
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            tyqiw__jgvjc += 1
            if arg_types[i] == bodo.dict_str_arr_type:
                irdb__ttzpv = i
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            tyqiw__jgvjc += 1
            if arg_types[i].data == bodo.dict_str_arr_type:
                irdb__ttzpv = i
    sna__srqjr = (support_dict_encoding and tyqiw__jgvjc == 1 and 
        irdb__ttzpv >= 0)
    tvbzc__aupco = sna__srqjr and out_dtype == bodo.string_array_type and (any
        (arg_types[i] == bodo.none and propagate_null[i] for i in range(len
        (arg_types))) or 'bodo.libs.array_kernels.setna' in scalar_text)
    if arg_string is None:
        arg_string = ', '.join(arg_names)
    jkp__tlwwi = f'def impl({arg_string}):\n'
    if arg_sources is not None:
        for gfeg__raprg, hpz__asu in arg_sources.items():
            jkp__tlwwi += f'   {gfeg__raprg} = {hpz__asu}\n'
    if hahp__kjh and array_override == None:
        if qxsnq__vos:
            jkp__tlwwi += '   return None'
        else:
            jkp__tlwwi += indent_block(prefix_code, 3)
            for i in range(len(arg_names)):
                jkp__tlwwi += f'   arg{i} = {arg_names[i]}\n'
            zzhr__ovqpl = scalar_text.replace('res[i] =', 'answer =').replace(
                'bodo.libs.array_kernels.setna(res, i)', 'return None')
            jkp__tlwwi += indent_block(zzhr__ovqpl, 3)
            jkp__tlwwi += '   return answer'
    else:
        for i in range(len(arg_names)):
            if bodo.hiframes.pd_series_ext.is_series_type(arg_types[i]):
                jkp__tlwwi += f"""   {arg_names[i]} = bodo.hiframes.pd_series_ext.get_series_data({arg_names[i]})
"""
        if array_override != None:
            mkqhf__qvhi = f'len({array_override})'
        else:
            for i in range(len(arg_names)):
                if pdrux__usq[i]:
                    mkqhf__qvhi = f'len({arg_names[i]})'
                    break
        if sna__srqjr:
            if out_dtype == bodo.string_array_type:
                jkp__tlwwi += (
                    f'   indices = {arg_names[irdb__ttzpv]}._indices.copy()\n')
                jkp__tlwwi += (
                    f'   has_global = {arg_names[irdb__ttzpv]}._has_global_dictionary\n'
                    )
                if may_cause_duplicate_dict_array_values:
                    jkp__tlwwi += f'   is_dict_unique = False\n'
                else:
                    jkp__tlwwi += f"""   is_dict_unique = {arg_names[irdb__ttzpv]}._has_deduped_local_dictionary
"""
                jkp__tlwwi += (
                    f'   {arg_names[i]} = {arg_names[irdb__ttzpv]}._data\n')
            else:
                jkp__tlwwi += (
                    f'   indices = {arg_names[irdb__ttzpv]}._indices\n')
                jkp__tlwwi += (
                    f'   {arg_names[i]} = {arg_names[irdb__ttzpv]}._data\n')
        jkp__tlwwi += f'   n = {mkqhf__qvhi}\n'
        if prefix_code is not None and not qxsnq__vos:
            jkp__tlwwi += indent_block(prefix_code, 3)
        if pzo__mlvxb:
            jkp__tlwwi += indent_block(synthesize_dict_setup_text, 3)
            out_dtype = bodo.libs.dict_arr_ext.dict_indices_arr_type
            jkp__tlwwi += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            jkp__tlwwi += '   numba.parfors.parfor.init_prange()\n'
            jkp__tlwwi += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        elif sna__srqjr:
            fpr__vkcug = 'n' if propagate_null[irdb__ttzpv] else '(n + 1)'
            if not propagate_null[irdb__ttzpv]:
                agjsq__qgu = arg_names[irdb__ttzpv]
                jkp__tlwwi += f"""   {agjsq__qgu} = bodo.libs.array_kernels.concat([{agjsq__qgu}, bodo.libs.array_kernels.gen_na_array(1, {agjsq__qgu})])
"""
            if out_dtype == bodo.string_array_type:
                jkp__tlwwi += f"""   res = bodo.libs.str_arr_ext.pre_alloc_string_array({fpr__vkcug}, -1)
"""
            else:
                jkp__tlwwi += f"""   res = bodo.utils.utils.alloc_type({fpr__vkcug}, out_dtype, (-1,))
"""
            jkp__tlwwi += f'   for i in range({fpr__vkcug}):\n'
        elif res_list:
            jkp__tlwwi += '   res = []\n'
            jkp__tlwwi += '   for i in range(n):\n'
        else:
            jkp__tlwwi += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            jkp__tlwwi += '   numba.parfors.parfor.init_prange()\n'
            jkp__tlwwi += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        if qxsnq__vos:
            jkp__tlwwi += f'      bodo.libs.array_kernels.setna(res, i)\n'
        else:
            for i in range(len(arg_names)):
                if pdrux__usq[i]:
                    if propagate_null[i]:
                        jkp__tlwwi += (
                            f'      if bodo.libs.array_kernels.isna({arg_names[i]}, i):\n'
                            )
                        if res_list:
                            jkp__tlwwi += '         res.append(None)\n'
                        else:
                            jkp__tlwwi += (
                                '         bodo.libs.array_kernels.setna(res, i)\n'
                                )
                        jkp__tlwwi += '         continue\n'
            for i in range(len(arg_names)):
                if pdrux__usq[i]:
                    if alloc_array_scalars:
                        jkp__tlwwi += f'      arg{i} = {arg_names[i]}[i]\n'
                else:
                    jkp__tlwwi += f'      arg{i} = {arg_names[i]}\n'
            if not pzo__mlvxb:
                jkp__tlwwi += indent_block(scalar_text, 6)
            else:
                jkp__tlwwi += indent_block(synthesize_dict_scalar_text, 6)
        if sna__srqjr:
            if tvbzc__aupco:
                jkp__tlwwi += '   numba.parfors.parfor.init_prange()\n'
                jkp__tlwwi += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                jkp__tlwwi += (
                    '      if not bodo.libs.array_kernels.isna(indices, i):\n')
                jkp__tlwwi += '         loc = indices[i]\n'
                jkp__tlwwi += (
                    '         if bodo.libs.array_kernels.isna(res, loc):\n')
                jkp__tlwwi += (
                    '            bodo.libs.array_kernels.setna(indices, i)\n')
            if out_dtype == bodo.string_array_type:
                jkp__tlwwi += """   res = bodo.libs.dict_arr_ext.init_dict_arr(res, indices, has_global, is_dict_unique)
"""
            else:
                jkp__tlwwi += """   res2 = bodo.utils.utils.alloc_type(len(indices), out_dtype, (-1,))
"""
                jkp__tlwwi += '   numba.parfors.parfor.init_prange()\n'
                jkp__tlwwi += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                if propagate_null[irdb__ttzpv]:
                    jkp__tlwwi += (
                        '      if bodo.libs.array_kernels.isna(indices, i):\n')
                    jkp__tlwwi += (
                        '         bodo.libs.array_kernels.setna(res2, i)\n')
                    jkp__tlwwi += '         continue\n'
                    jkp__tlwwi += '      loc = indices[i]\n'
                else:
                    jkp__tlwwi += """      loc = n if bodo.libs.array_kernels.isna(indices, i) else indices[i]
"""
                jkp__tlwwi += (
                    '      if bodo.libs.array_kernels.isna(res, loc):\n')
                jkp__tlwwi += (
                    '         bodo.libs.array_kernels.setna(res2, i)\n')
                jkp__tlwwi += '      else:\n'
                jkp__tlwwi += '         res2[i] = res[loc]\n'
                jkp__tlwwi += '   res = res2\n'
        jkp__tlwwi += indent_block(suffix_code, 3)
        if pzo__mlvxb:
            jkp__tlwwi += f"""   return bodo.libs.dict_arr_ext.init_dict_arr(dict_res, res, {synthesize_dict_global}, {synthesize_dict_unique})
"""
        else:
            jkp__tlwwi += '   return res'
    dxdfi__awgk = {}
    gbeyk__uqv = {'bodo': bodo, 'math': math, 'numba': numba, 're': re,
        'np': np, 'out_dtype': out_dtype, 'pd': pd}
    if not extra_globals is None:
        gbeyk__uqv.update(extra_globals)
    exec(jkp__tlwwi, gbeyk__uqv, dxdfi__awgk)
    agj__jah = dxdfi__awgk['impl']
    return agj__jah


def unopt_argument(func_name, arg_names, i, container_arg=0,
    container_length=None):
    if container_length != None:
        eubx__xpo = [(f'{arg_names[i]}{[ficwi__czmbd]}' if ficwi__czmbd !=
            container_arg else 'None') for ficwi__czmbd in range(
            container_length)]
        kinmg__wazh = ',' if container_length != 0 else ''
        vgm__xcjp = f"({', '.join(eubx__xpo)}{kinmg__wazh})"
        lrj__khyju = [(f'{arg_names[i]}{[ficwi__czmbd]}' if ficwi__czmbd !=
            container_arg else
            f'bodo.utils.indexing.unoptional({arg_names[i]}[{ficwi__czmbd}])'
            ) for ficwi__czmbd in range(container_length)]
        auurt__erzx = f"({', '.join(lrj__khyju)}{kinmg__wazh})"
        ntzxp__gjvhg = [(arg_names[ficwi__czmbd] if ficwi__czmbd != i else
            vgm__xcjp) for ficwi__czmbd in range(len(arg_names))]
        sxo__zvtf = [(arg_names[ficwi__czmbd] if ficwi__czmbd != i else
            auurt__erzx) for ficwi__czmbd in range(len(arg_names))]
        jkp__tlwwi = f"def impl({', '.join(arg_names)}):\n"
        jkp__tlwwi += f'   if {arg_names[i]}[{container_arg}] is None:\n'
        jkp__tlwwi += f"      return {func_name}({', '.join(ntzxp__gjvhg)})\n"
        jkp__tlwwi += f'   else:\n'
        jkp__tlwwi += f"      return {func_name}({', '.join(sxo__zvtf)})\n"
    else:
        eubx__xpo = [(arg_names[ficwi__czmbd] if ficwi__czmbd != i else
            'None') for ficwi__czmbd in range(len(arg_names))]
        lrj__khyju = [(arg_names[ficwi__czmbd] if ficwi__czmbd != i else
            f'bodo.utils.indexing.unoptional({arg_names[ficwi__czmbd]})') for
            ficwi__czmbd in range(len(arg_names))]
        jkp__tlwwi = f"def impl({', '.join(arg_names)}):\n"
        jkp__tlwwi += f'   if {arg_names[i]} is None:\n'
        jkp__tlwwi += f"      return {func_name}({', '.join(eubx__xpo)})\n"
        jkp__tlwwi += f'   else:\n'
        jkp__tlwwi += f"      return {func_name}({', '.join(lrj__khyju)})\n"
    dxdfi__awgk = {}
    exec(jkp__tlwwi, {'bodo': bodo, 'numba': numba}, dxdfi__awgk)
    agj__jah = dxdfi__awgk['impl']
    return agj__jah


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
    bnj__hwxic = is_valid_string_arg(arg)
    qsnxz__jtgat = is_valid_binary_arg(arg)
    if bnj__hwxic or qsnxz__jtgat:
        return bnj__hwxic
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
    paw__bfb = []
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            paw__bfb.append(arg_types[i])
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            paw__bfb.append(arg_types[i].data)
        else:
            paw__bfb.append(arg_types[i])
    if len(paw__bfb) == 0:
        return bodo.none
    elif len(paw__bfb) == 1:
        if bodo.utils.utils.is_array_typ(paw__bfb[0]):
            return bodo.utils.typing.to_nullable_type(paw__bfb[0])
        elif paw__bfb[0] == bodo.none:
            return bodo.none
        else:
            return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
                dtype_to_array_type(paw__bfb[0]))
    else:
        ncm__lid = []
        for i in range(len(arg_types)):
            if bodo.utils.utils.is_array_typ(arg_types[i]):
                ncm__lid.append(paw__bfb[i].dtype)
            elif paw__bfb[i] == bodo.none:
                pass
            else:
                ncm__lid.append(paw__bfb[i])
        if len(ncm__lid) == 0:
            return bodo.none
        igk__kyt, pxhbr__bzwcy = bodo.utils.typing.get_common_scalar_dtype(
            ncm__lid)
        if not pxhbr__bzwcy:
            raise_bodo_error(
                f'Cannot call {func_name} on columns with different dtypes')
        return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
            dtype_to_array_type(igk__kyt))


def vectorized_sol(args, scalar_fn, dtype, manual_coercion=False):
    pssik__fjcge = -1
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            pssik__fjcge = len(arg)
            break
    if pssik__fjcge == -1:
        return dtype(scalar_fn(*args)) if manual_coercion else scalar_fn(*args)
    rymz__aknyb = []
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            rymz__aknyb.append(arg)
        else:
            rymz__aknyb.append([arg] * pssik__fjcge)
    if manual_coercion:
        return pd.Series([dtype(scalar_fn(*ant__gviuq)) for ant__gviuq in
            zip(*rymz__aknyb)])
    else:
        return pd.Series([scalar_fn(*ant__gviuq) for ant__gviuq in zip(*
            rymz__aknyb)], dtype=dtype)


def gen_windowed(calculate_block, constant_block, out_dtype, setup_block=
    None, enter_block=None, exit_block=None, empty_block=None):
    qss__gzmh = calculate_block.splitlines()
    pdorm__tnrgn = len(qss__gzmh[0]) - len(qss__gzmh[0].lstrip())
    if constant_block != None:
        zulm__rjwj = constant_block.splitlines()
        ogt__sqjoh = len(zulm__rjwj[0]) - len(zulm__rjwj[0].lstrip())
    if setup_block != None:
        nue__xnl = setup_block.splitlines()
        xouu__twbyt = len(nue__xnl[0]) - len(nue__xnl[0].lstrip())
    if enter_block != None:
        upan__rcd = enter_block.splitlines()
        xntq__gsw = len(upan__rcd[0]) - len(upan__rcd[0].lstrip())
    if exit_block != None:
        tslk__dpkj = exit_block.splitlines()
        sww__noua = len(tslk__dpkj[0]) - len(tslk__dpkj[0].lstrip())
    if empty_block == None:
        empty_block = 'bodo.libs.array_kernels.setna(res, i)'
    vcms__erpo = empty_block.splitlines()
    dxsj__cjs = len(vcms__erpo[0]) - len(vcms__erpo[0].lstrip())
    jkp__tlwwi = 'def impl(S, lower_bound, upper_bound):\n'
    jkp__tlwwi += '   n = len(S)\n'
    jkp__tlwwi += '   arr = bodo.utils.conversion.coerce_to_array(S)\n'
    jkp__tlwwi += '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n'
    jkp__tlwwi += '   if upper_bound < lower_bound:\n'
    jkp__tlwwi += '      for i in range(n):\n'
    jkp__tlwwi += '         bodo.libs.array_kernels.setna(res, i)\n'
    if constant_block != None:
        jkp__tlwwi += '   elif lower_bound <= -n+1 and n-1 <= upper_bound:\n'
        jkp__tlwwi += '      if S.count() == 0:\n'
        jkp__tlwwi += '         for i in range(n):\n'
        jkp__tlwwi += '\n'.join([(' ' * 12 + rpxq__jegeg[dxsj__cjs:]) for
            rpxq__jegeg in vcms__erpo]) + '\n'
        jkp__tlwwi += '      else:\n'
        jkp__tlwwi += '\n'.join([(' ' * 9 + rpxq__jegeg[ogt__sqjoh:]) for
            rpxq__jegeg in zulm__rjwj]) + '\n'
        jkp__tlwwi += '         for i in range(n):\n'
        jkp__tlwwi += '            res[i] = constant_value\n'
    jkp__tlwwi += '   else:\n'
    jkp__tlwwi += '      exiting = lower_bound\n'
    jkp__tlwwi += '      entering = upper_bound\n'
    jkp__tlwwi += '      in_window = 0\n'
    if setup_block != None:
        jkp__tlwwi += '\n'.join([(' ' * 6 + rpxq__jegeg[xouu__twbyt:]) for
            rpxq__jegeg in nue__xnl]) + '\n'
    jkp__tlwwi += (
        '      for i in range(min(max(0, exiting), n), min(max(0, entering + 1), n)):\n'
        )
    jkp__tlwwi += '         if not bodo.libs.array_kernels.isna(arr, i):\n'
    jkp__tlwwi += '            in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            jkp__tlwwi += '            elem = arr[i]\n'
        jkp__tlwwi += '\n'.join([(' ' * 12 + rpxq__jegeg[xntq__gsw:]) for
            rpxq__jegeg in upan__rcd]) + '\n'
    jkp__tlwwi += '      for i in range(n):\n'
    jkp__tlwwi += '         if in_window == 0:\n'
    jkp__tlwwi += '\n'.join([(' ' * 12 + rpxq__jegeg[dxsj__cjs:]) for
        rpxq__jegeg in vcms__erpo]) + '\n'
    jkp__tlwwi += '         else:\n'
    jkp__tlwwi += '\n'.join([(' ' * 12 + rpxq__jegeg[pdorm__tnrgn:]) for
        rpxq__jegeg in qss__gzmh]) + '\n'
    jkp__tlwwi += '         if 0 <= exiting < n:\n'
    jkp__tlwwi += (
        '            if not bodo.libs.array_kernels.isna(arr, exiting):\n')
    jkp__tlwwi += '               in_window -= 1\n'
    if exit_block != None:
        if 'elem' in exit_block:
            jkp__tlwwi += '               elem = arr[exiting]\n'
        jkp__tlwwi += '\n'.join([(' ' * 15 + rpxq__jegeg[sww__noua:]) for
            rpxq__jegeg in tslk__dpkj]) + '\n'
    jkp__tlwwi += '         exiting += 1\n'
    jkp__tlwwi += '         entering += 1\n'
    jkp__tlwwi += '         if 0 <= entering < n:\n'
    jkp__tlwwi += (
        '            if not bodo.libs.array_kernels.isna(arr, entering):\n')
    jkp__tlwwi += '               in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            jkp__tlwwi += '               elem = arr[entering]\n'
        jkp__tlwwi += '\n'.join([(' ' * 15 + rpxq__jegeg[xntq__gsw:]) for
            rpxq__jegeg in upan__rcd]) + '\n'
    jkp__tlwwi += '   return res'
    dxdfi__awgk = {}
    exec(jkp__tlwwi, {'bodo': bodo, 'numba': numba, 'np': np, 'out_dtype':
        out_dtype, 'pd': pd}, dxdfi__awgk)
    agj__jah = dxdfi__awgk['impl']
    return agj__jah
