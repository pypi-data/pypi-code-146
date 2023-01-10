"""
Support for Series.dt attributes and methods
"""
import datetime
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_series_ext import SeriesType, get_series_data, get_series_index, get_series_name, init_series
from bodo.libs.pd_datetime_arr_ext import PandasDatetimeTZDtype
from bodo.utils.typing import BodoError, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, raise_bodo_error
dt64_dtype = np.dtype('datetime64[ns]')
timedelta64_dtype = np.dtype('timedelta64[ns]')


class SeriesDatetimePropertiesType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        xywix__dbtzi = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(xywix__dbtzi)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        szmq__kxzv = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, szmq__kxzv)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        nry__jhe, = args
        hbve__fqxj = signature.return_type
        evjta__orzjw = cgutils.create_struct_proxy(hbve__fqxj)(context, builder
            )
        evjta__orzjw.obj = nry__jhe
        context.nrt.incref(builder, signature.args[0], nry__jhe)
        return evjta__orzjw._getvalue()
    return SeriesDatetimePropertiesType(obj)(obj), codegen


@overload_attribute(SeriesType, 'dt')
def overload_series_dt(s):
    if not (bodo.hiframes.pd_series_ext.is_dt64_series_typ(s) or bodo.
        hiframes.pd_series_ext.is_timedelta64_series_typ(s)):
        raise_bodo_error('Can only use .dt accessor with datetimelike values.')
    return lambda s: bodo.hiframes.series_dt_impl.init_series_dt_properties(s)


def create_date_field_overload(field):

    def overload_field(S_dt):
        if S_dt.stype.dtype != types.NPDatetime('ns') and not isinstance(S_dt
            .stype.dtype, PandasDatetimeTZDtype):
            return
        hklm__xbel = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        yehzg__sfe = ['year', 'quarter', 'month', 'week', 'day', 'hour',
            'minute', 'second', 'microsecond']
        if field not in yehzg__sfe:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{field}')
        htmg__zqui = 'def impl(S_dt):\n'
        htmg__zqui += '    S = S_dt._obj\n'
        htmg__zqui += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        htmg__zqui += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        htmg__zqui += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        htmg__zqui += '    numba.parfors.parfor.init_prange()\n'
        htmg__zqui += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            htmg__zqui += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            htmg__zqui += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        htmg__zqui += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        htmg__zqui += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        htmg__zqui += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        htmg__zqui += '            continue\n'
        if not hklm__xbel:
            htmg__zqui += (
                '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
                )
            htmg__zqui += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            if field == 'weekday':
                htmg__zqui += '        out_arr[i] = ts.weekday()\n'
            else:
                htmg__zqui += '        out_arr[i] = ts.' + field + '\n'
        else:
            htmg__zqui += '        out_arr[i] = arr[i].{}\n'.format(field)
        htmg__zqui += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        rkpcd__tyn = {}
        exec(htmg__zqui, {'bodo': bodo, 'numba': numba, 'np': np}, rkpcd__tyn)
        impl = rkpcd__tyn['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        bln__elsqk = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(bln__elsqk)


_install_date_fields()


def create_date_method_overload(method):
    osvlb__getxf = method in ['day_name', 'month_name']
    if osvlb__getxf:
        htmg__zqui = 'def overload_method(S_dt, locale=None):\n'
        htmg__zqui += '    unsupported_args = dict(locale=locale)\n'
        htmg__zqui += '    arg_defaults = dict(locale=None)\n'
        htmg__zqui += '    bodo.utils.typing.check_unsupported_args(\n'
        htmg__zqui += f"        'Series.dt.{method}',\n"
        htmg__zqui += '        unsupported_args,\n'
        htmg__zqui += '        arg_defaults,\n'
        htmg__zqui += "        package_name='pandas',\n"
        htmg__zqui += "        module_name='Series',\n"
        htmg__zqui += '    )\n'
    else:
        htmg__zqui = 'def overload_method(S_dt):\n'
        htmg__zqui += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    htmg__zqui += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    htmg__zqui += '        return\n'
    if osvlb__getxf:
        htmg__zqui += '    def impl(S_dt, locale=None):\n'
    else:
        htmg__zqui += '    def impl(S_dt):\n'
    htmg__zqui += '        S = S_dt._obj\n'
    htmg__zqui += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    htmg__zqui += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    htmg__zqui += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    htmg__zqui += '        numba.parfors.parfor.init_prange()\n'
    htmg__zqui += '        n = len(arr)\n'
    if osvlb__getxf:
        htmg__zqui += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        htmg__zqui += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    htmg__zqui += '        for i in numba.parfors.parfor.internal_prange(n):\n'
    htmg__zqui += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    htmg__zqui += '                bodo.libs.array_kernels.setna(out_arr, i)\n'
    htmg__zqui += '                continue\n'
    htmg__zqui += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    htmg__zqui += f'            method_val = ts.{method}()\n'
    if osvlb__getxf:
        htmg__zqui += '            out_arr[i] = method_val\n'
    else:
        htmg__zqui += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    htmg__zqui += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    htmg__zqui += '    return impl\n'
    rkpcd__tyn = {}
    exec(htmg__zqui, {'bodo': bodo, 'numba': numba, 'np': np}, rkpcd__tyn)
    overload_method = rkpcd__tyn['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        bln__elsqk = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            bln__elsqk)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        kobt__oje = S_dt._obj
        vbf__yxugd = bodo.hiframes.pd_series_ext.get_series_data(kobt__oje)
        ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(kobt__oje)
        xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(kobt__oje)
        numba.parfors.parfor.init_prange()
        zyar__mep = len(vbf__yxugd)
        net__lcmo = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            zyar__mep)
        for sqkat__xpdjc in numba.parfors.parfor.internal_prange(zyar__mep):
            aad__qrjeb = vbf__yxugd[sqkat__xpdjc]
            jmu__uqpci = bodo.utils.conversion.box_if_dt64(aad__qrjeb)
            net__lcmo[sqkat__xpdjc] = datetime.date(jmu__uqpci.year,
                jmu__uqpci.month, jmu__uqpci.day)
        return bodo.hiframes.pd_series_ext.init_series(net__lcmo,
            ssnqg__dyb, xywix__dbtzi)
    return impl


def create_series_dt_df_output_overload(attr):

    def series_dt_df_output_overload(S_dt):
        if not (attr == 'components' and S_dt.stype.dtype == types.
            NPTimedelta('ns') or attr == 'isocalendar' and (S_dt.stype.
            dtype == types.NPDatetime('ns') or isinstance(S_dt.stype.dtype,
            PandasDatetimeTZDtype))):
            return
        hklm__xbel = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        if attr != 'isocalendar':
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{attr}')
        if attr == 'components':
            tsdyf__eci = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            pyn__ahf = 'convert_numpy_timedelta64_to_pd_timedelta'
            bxo__gti = 'np.empty(n, np.int64)'
            uajr__qgy = attr
        elif attr == 'isocalendar':
            tsdyf__eci = ['year', 'week', 'day']
            if hklm__xbel:
                pyn__ahf = None
            else:
                pyn__ahf = 'convert_datetime64_to_timestamp'
            bxo__gti = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            uajr__qgy = attr + '()'
        htmg__zqui = 'def impl(S_dt):\n'
        htmg__zqui += '    S = S_dt._obj\n'
        htmg__zqui += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        htmg__zqui += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        htmg__zqui += '    numba.parfors.parfor.init_prange()\n'
        htmg__zqui += '    n = len(arr)\n'
        for field in tsdyf__eci:
            htmg__zqui += '    {} = {}\n'.format(field, bxo__gti)
        htmg__zqui += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        htmg__zqui += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in tsdyf__eci:
            htmg__zqui += ('            bodo.libs.array_kernels.setna({}, i)\n'
                .format(field))
        htmg__zqui += '            continue\n'
        fwzvx__omhsm = '(' + '[i], '.join(tsdyf__eci) + '[i])'
        if pyn__ahf:
            xlbx__ibfnj = f'bodo.hiframes.pd_timestamp_ext.{pyn__ahf}(arr[i])'
        else:
            xlbx__ibfnj = 'arr[i]'
        htmg__zqui += f'        {fwzvx__omhsm} = {xlbx__ibfnj}.{uajr__qgy}\n'
        bxv__tnm = '(' + ', '.join(tsdyf__eci) + ')'
        htmg__zqui += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, __col_name_meta_value_series_dt_df_output)
"""
            .format(bxv__tnm))
        rkpcd__tyn = {}
        exec(htmg__zqui, {'bodo': bodo, 'numba': numba, 'np': np,
            '__col_name_meta_value_series_dt_df_output': ColNamesMetaType(
            tuple(tsdyf__eci))}, rkpcd__tyn)
        impl = rkpcd__tyn['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    udch__iwd = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, eco__opxr in udch__iwd:
        bln__elsqk = create_series_dt_df_output_overload(attr)
        eco__opxr(SeriesDatetimePropertiesType, attr, inline='always')(
            bln__elsqk)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        htmg__zqui = 'def impl(S_dt):\n'
        htmg__zqui += '    S = S_dt._obj\n'
        htmg__zqui += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        htmg__zqui += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        htmg__zqui += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        htmg__zqui += '    numba.parfors.parfor.init_prange()\n'
        htmg__zqui += '    n = len(A)\n'
        htmg__zqui += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        htmg__zqui += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        htmg__zqui += '        if bodo.libs.array_kernels.isna(A, i):\n'
        htmg__zqui += '            bodo.libs.array_kernels.setna(B, i)\n'
        htmg__zqui += '            continue\n'
        htmg__zqui += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            htmg__zqui += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            htmg__zqui += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            htmg__zqui += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            htmg__zqui += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        htmg__zqui += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        rkpcd__tyn = {}
        exec(htmg__zqui, {'numba': numba, 'np': np, 'bodo': bodo}, rkpcd__tyn)
        impl = rkpcd__tyn['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        htmg__zqui = 'def impl(S_dt):\n'
        htmg__zqui += '    S = S_dt._obj\n'
        htmg__zqui += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        htmg__zqui += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        htmg__zqui += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        htmg__zqui += '    numba.parfors.parfor.init_prange()\n'
        htmg__zqui += '    n = len(A)\n'
        if method == 'total_seconds':
            htmg__zqui += '    B = np.empty(n, np.float64)\n'
        else:
            htmg__zqui += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        htmg__zqui += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        htmg__zqui += '        if bodo.libs.array_kernels.isna(A, i):\n'
        htmg__zqui += '            bodo.libs.array_kernels.setna(B, i)\n'
        htmg__zqui += '            continue\n'
        htmg__zqui += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            htmg__zqui += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            htmg__zqui += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            htmg__zqui += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            htmg__zqui += '    return B\n'
        rkpcd__tyn = {}
        exec(htmg__zqui, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, rkpcd__tyn)
        impl = rkpcd__tyn['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        bln__elsqk = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(bln__elsqk)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        bln__elsqk = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            bln__elsqk)


_install_S_dt_timedelta_methods()


@overload_method(SeriesDatetimePropertiesType, 'strftime', inline='always',
    no_unliteral=True)
def dt_strftime(S_dt, date_format):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return
    if types.unliteral(date_format) != types.unicode_type:
        raise BodoError(
            "Series.str.strftime(): 'date_format' argument must be a string")

    def impl(S_dt, date_format):
        kobt__oje = S_dt._obj
        qsdjb__mswnm = bodo.hiframes.pd_series_ext.get_series_data(kobt__oje)
        ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(kobt__oje)
        xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(kobt__oje)
        numba.parfors.parfor.init_prange()
        zyar__mep = len(qsdjb__mswnm)
        siyn__ebqfc = bodo.libs.str_arr_ext.pre_alloc_string_array(zyar__mep,
            -1)
        for byn__fwueb in numba.parfors.parfor.internal_prange(zyar__mep):
            if bodo.libs.array_kernels.isna(qsdjb__mswnm, byn__fwueb):
                bodo.libs.array_kernels.setna(siyn__ebqfc, byn__fwueb)
                continue
            siyn__ebqfc[byn__fwueb] = bodo.utils.conversion.box_if_dt64(
                qsdjb__mswnm[byn__fwueb]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(siyn__ebqfc,
            ssnqg__dyb, xywix__dbtzi)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        kobt__oje = S_dt._obj
        drp__ipv = get_series_data(kobt__oje).tz_convert(tz)
        ssnqg__dyb = get_series_index(kobt__oje)
        xywix__dbtzi = get_series_name(kobt__oje)
        return init_series(drp__ipv, ssnqg__dyb, xywix__dbtzi)
    return impl


def create_timedelta_freq_overload(method):

    def freq_overload(S_dt, freq, ambiguous='raise', nonexistent='raise'):
        if S_dt.stype.dtype != types.NPTimedelta('ns'
            ) and S_dt.stype.dtype != types.NPDatetime('ns'
            ) and not isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype):
            return
        vwli__cwj = isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype)
        wgqm__jiml = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        szxqc__nxbot = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', wgqm__jiml,
            szxqc__nxbot, package_name='pandas', module_name='Series')
        htmg__zqui = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        htmg__zqui += '    S = S_dt._obj\n'
        htmg__zqui += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        htmg__zqui += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        htmg__zqui += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        htmg__zqui += '    numba.parfors.parfor.init_prange()\n'
        htmg__zqui += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            htmg__zqui += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        elif vwli__cwj:
            htmg__zqui += """    B = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(n, tz_literal)
"""
        else:
            htmg__zqui += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        htmg__zqui += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        htmg__zqui += '        if bodo.libs.array_kernels.isna(A, i):\n'
        htmg__zqui += '            bodo.libs.array_kernels.setna(B, i)\n'
        htmg__zqui += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            jdb__ned = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            lhp__szi = 'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64'
        else:
            jdb__ned = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            lhp__szi = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        if vwli__cwj:
            htmg__zqui += f'        B[i] = A[i].{method}(freq)\n'
        else:
            htmg__zqui += ('        B[i] = {}({}(A[i]).{}(freq).value)\n'.
                format(lhp__szi, jdb__ned, method))
        htmg__zqui += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        rkpcd__tyn = {}
        qeibf__fzl = None
        if vwli__cwj:
            qeibf__fzl = S_dt.stype.dtype.tz
        exec(htmg__zqui, {'numba': numba, 'np': np, 'bodo': bodo,
            'tz_literal': qeibf__fzl}, rkpcd__tyn)
        impl = rkpcd__tyn['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    yhh__wuyur = ['ceil', 'floor', 'round']
    for method in yhh__wuyur:
        bln__elsqk = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            bln__elsqk)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            btsxl__fqi = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tzksh__xwbht = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                ache__vxnwg = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tzksh__xwbht)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                vxp__okq = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                ykzvt__hzj = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vxp__okq)
                zyar__mep = len(ache__vxnwg)
                kobt__oje = np.empty(zyar__mep, timedelta64_dtype)
                coqzg__dcmk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    btsxl__fqi)
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    auow__ddvi = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(ache__vxnwg[sqkat__xpdjc]))
                    mhsza__osv = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(ykzvt__hzj[sqkat__xpdjc]))
                    if auow__ddvi == coqzg__dcmk or mhsza__osv == coqzg__dcmk:
                        urca__yctgu = coqzg__dcmk
                    else:
                        urca__yctgu = op(auow__ddvi, mhsza__osv)
                    kobt__oje[sqkat__xpdjc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        urca__yctgu)
                return bodo.hiframes.pd_series_ext.init_series(kobt__oje,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            btsxl__fqi = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                swe__vvia = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                vbf__yxugd = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    swe__vvia)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                ykzvt__hzj = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zyar__mep = len(vbf__yxugd)
                kobt__oje = np.empty(zyar__mep, dt64_dtype)
                coqzg__dcmk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    btsxl__fqi)
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    lgqdb__xams = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(vbf__yxugd[sqkat__xpdjc]))
                    jjo__fqbt = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(ykzvt__hzj[sqkat__xpdjc]))
                    if lgqdb__xams == coqzg__dcmk or jjo__fqbt == coqzg__dcmk:
                        urca__yctgu = coqzg__dcmk
                    else:
                        urca__yctgu = op(lgqdb__xams, jjo__fqbt)
                    kobt__oje[sqkat__xpdjc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        urca__yctgu)
                return bodo.hiframes.pd_series_ext.init_series(kobt__oje,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            btsxl__fqi = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                swe__vvia = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vbf__yxugd = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    swe__vvia)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                ykzvt__hzj = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zyar__mep = len(vbf__yxugd)
                kobt__oje = np.empty(zyar__mep, dt64_dtype)
                coqzg__dcmk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    btsxl__fqi)
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    lgqdb__xams = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(vbf__yxugd[sqkat__xpdjc]))
                    jjo__fqbt = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(ykzvt__hzj[sqkat__xpdjc]))
                    if lgqdb__xams == coqzg__dcmk or jjo__fqbt == coqzg__dcmk:
                        urca__yctgu = coqzg__dcmk
                    else:
                        urca__yctgu = op(lgqdb__xams, jjo__fqbt)
                    kobt__oje[sqkat__xpdjc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        urca__yctgu)
                return bodo.hiframes.pd_series_ext.init_series(kobt__oje,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            btsxl__fqi = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                swe__vvia = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                vbf__yxugd = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    swe__vvia)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                zyar__mep = len(vbf__yxugd)
                kobt__oje = np.empty(zyar__mep, timedelta64_dtype)
                coqzg__dcmk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    btsxl__fqi)
                hrym__uhpkp = rhs.value
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    lgqdb__xams = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(vbf__yxugd[sqkat__xpdjc]))
                    if (lgqdb__xams == coqzg__dcmk or hrym__uhpkp ==
                        coqzg__dcmk):
                        urca__yctgu = coqzg__dcmk
                    else:
                        urca__yctgu = op(lgqdb__xams, hrym__uhpkp)
                    kobt__oje[sqkat__xpdjc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        urca__yctgu)
                return bodo.hiframes.pd_series_ext.init_series(kobt__oje,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            btsxl__fqi = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                swe__vvia = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vbf__yxugd = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    swe__vvia)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                zyar__mep = len(vbf__yxugd)
                kobt__oje = np.empty(zyar__mep, timedelta64_dtype)
                coqzg__dcmk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    btsxl__fqi)
                hrym__uhpkp = lhs.value
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    lgqdb__xams = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(vbf__yxugd[sqkat__xpdjc]))
                    if (hrym__uhpkp == coqzg__dcmk or lgqdb__xams ==
                        coqzg__dcmk):
                        urca__yctgu = coqzg__dcmk
                    else:
                        urca__yctgu = op(hrym__uhpkp, lgqdb__xams)
                    kobt__oje[sqkat__xpdjc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        urca__yctgu)
                return bodo.hiframes.pd_series_ext.init_series(kobt__oje,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            btsxl__fqi = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                swe__vvia = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                vbf__yxugd = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    swe__vvia)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                zyar__mep = len(vbf__yxugd)
                kobt__oje = np.empty(zyar__mep, dt64_dtype)
                coqzg__dcmk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    btsxl__fqi)
                punos__tlib = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                jjo__fqbt = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(punos__tlib))
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    lgqdb__xams = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(vbf__yxugd[sqkat__xpdjc]))
                    if lgqdb__xams == coqzg__dcmk or jjo__fqbt == coqzg__dcmk:
                        urca__yctgu = coqzg__dcmk
                    else:
                        urca__yctgu = op(lgqdb__xams, jjo__fqbt)
                    kobt__oje[sqkat__xpdjc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        urca__yctgu)
                return bodo.hiframes.pd_series_ext.init_series(kobt__oje,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            btsxl__fqi = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                swe__vvia = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vbf__yxugd = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    swe__vvia)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                zyar__mep = len(vbf__yxugd)
                kobt__oje = np.empty(zyar__mep, dt64_dtype)
                coqzg__dcmk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    btsxl__fqi)
                punos__tlib = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                jjo__fqbt = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(punos__tlib))
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    lgqdb__xams = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(vbf__yxugd[sqkat__xpdjc]))
                    if lgqdb__xams == coqzg__dcmk or jjo__fqbt == coqzg__dcmk:
                        urca__yctgu = coqzg__dcmk
                    else:
                        urca__yctgu = op(lgqdb__xams, jjo__fqbt)
                    kobt__oje[sqkat__xpdjc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        urca__yctgu)
                return bodo.hiframes.pd_series_ext.init_series(kobt__oje,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            btsxl__fqi = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                swe__vvia = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                vbf__yxugd = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    swe__vvia)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                zyar__mep = len(vbf__yxugd)
                kobt__oje = np.empty(zyar__mep, timedelta64_dtype)
                coqzg__dcmk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    btsxl__fqi)
                tvn__bus = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                lgqdb__xams = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    tvn__bus)
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    hlc__rxt = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vbf__yxugd[sqkat__xpdjc])
                    if hlc__rxt == coqzg__dcmk or lgqdb__xams == coqzg__dcmk:
                        urca__yctgu = coqzg__dcmk
                    else:
                        urca__yctgu = op(hlc__rxt, lgqdb__xams)
                    kobt__oje[sqkat__xpdjc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        urca__yctgu)
                return bodo.hiframes.pd_series_ext.init_series(kobt__oje,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            btsxl__fqi = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                swe__vvia = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vbf__yxugd = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    swe__vvia)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                zyar__mep = len(vbf__yxugd)
                kobt__oje = np.empty(zyar__mep, timedelta64_dtype)
                coqzg__dcmk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    btsxl__fqi)
                tvn__bus = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                lgqdb__xams = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    tvn__bus)
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    hlc__rxt = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vbf__yxugd[sqkat__xpdjc])
                    if lgqdb__xams == coqzg__dcmk or hlc__rxt == coqzg__dcmk:
                        urca__yctgu = coqzg__dcmk
                    else:
                        urca__yctgu = op(lgqdb__xams, hlc__rxt)
                    kobt__oje[sqkat__xpdjc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        urca__yctgu)
                return bodo.hiframes.pd_series_ext.init_series(kobt__oje,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            btsxl__fqi = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vbf__yxugd = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                zyar__mep = len(vbf__yxugd)
                kobt__oje = np.empty(zyar__mep, timedelta64_dtype)
                coqzg__dcmk = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(btsxl__fqi))
                punos__tlib = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                jjo__fqbt = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(punos__tlib))
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    vck__ogvan = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(vbf__yxugd[sqkat__xpdjc]))
                    if jjo__fqbt == coqzg__dcmk or vck__ogvan == coqzg__dcmk:
                        urca__yctgu = coqzg__dcmk
                    else:
                        urca__yctgu = op(vck__ogvan, jjo__fqbt)
                    kobt__oje[sqkat__xpdjc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        urca__yctgu)
                return bodo.hiframes.pd_series_ext.init_series(kobt__oje,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            btsxl__fqi = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vbf__yxugd = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                zyar__mep = len(vbf__yxugd)
                kobt__oje = np.empty(zyar__mep, timedelta64_dtype)
                coqzg__dcmk = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(btsxl__fqi))
                punos__tlib = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                jjo__fqbt = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(punos__tlib))
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    vck__ogvan = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(vbf__yxugd[sqkat__xpdjc]))
                    if jjo__fqbt == coqzg__dcmk or vck__ogvan == coqzg__dcmk:
                        urca__yctgu = coqzg__dcmk
                    else:
                        urca__yctgu = op(jjo__fqbt, vck__ogvan)
                    kobt__oje[sqkat__xpdjc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        urca__yctgu)
                return bodo.hiframes.pd_series_ext.init_series(kobt__oje,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            aanc__btuk = True
        else:
            aanc__btuk = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            btsxl__fqi = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vbf__yxugd = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                zyar__mep = len(vbf__yxugd)
                net__lcmo = bodo.libs.bool_arr_ext.alloc_bool_array(zyar__mep)
                coqzg__dcmk = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(btsxl__fqi))
                hlxmi__aym = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                atswf__hhq = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(hlxmi__aym))
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    sydl__tzn = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(vbf__yxugd[sqkat__xpdjc]))
                    if sydl__tzn == coqzg__dcmk or atswf__hhq == coqzg__dcmk:
                        urca__yctgu = aanc__btuk
                    else:
                        urca__yctgu = op(sydl__tzn, atswf__hhq)
                    net__lcmo[sqkat__xpdjc] = urca__yctgu
                return bodo.hiframes.pd_series_ext.init_series(net__lcmo,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            btsxl__fqi = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vbf__yxugd = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                zyar__mep = len(vbf__yxugd)
                net__lcmo = bodo.libs.bool_arr_ext.alloc_bool_array(zyar__mep)
                coqzg__dcmk = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(btsxl__fqi))
                one__pxo = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                sydl__tzn = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(one__pxo))
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    atswf__hhq = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(vbf__yxugd[sqkat__xpdjc]))
                    if sydl__tzn == coqzg__dcmk or atswf__hhq == coqzg__dcmk:
                        urca__yctgu = aanc__btuk
                    else:
                        urca__yctgu = op(sydl__tzn, atswf__hhq)
                    net__lcmo[sqkat__xpdjc] = urca__yctgu
                return bodo.hiframes.pd_series_ext.init_series(net__lcmo,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            btsxl__fqi = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                swe__vvia = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                vbf__yxugd = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    swe__vvia)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                zyar__mep = len(vbf__yxugd)
                net__lcmo = bodo.libs.bool_arr_ext.alloc_bool_array(zyar__mep)
                coqzg__dcmk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    btsxl__fqi)
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    sydl__tzn = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vbf__yxugd[sqkat__xpdjc])
                    if sydl__tzn == coqzg__dcmk or rhs.value == coqzg__dcmk:
                        urca__yctgu = aanc__btuk
                    else:
                        urca__yctgu = op(sydl__tzn, rhs.value)
                    net__lcmo[sqkat__xpdjc] = urca__yctgu
                return bodo.hiframes.pd_series_ext.init_series(net__lcmo,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.
            pd_timestamp_tz_naive_type and bodo.hiframes.pd_series_ext.
            is_dt64_series_typ(rhs)):
            btsxl__fqi = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                swe__vvia = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vbf__yxugd = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    swe__vvia)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                zyar__mep = len(vbf__yxugd)
                net__lcmo = bodo.libs.bool_arr_ext.alloc_bool_array(zyar__mep)
                coqzg__dcmk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    btsxl__fqi)
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    atswf__hhq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(vbf__yxugd[sqkat__xpdjc]))
                    if atswf__hhq == coqzg__dcmk or lhs.value == coqzg__dcmk:
                        urca__yctgu = aanc__btuk
                    else:
                        urca__yctgu = op(lhs.value, atswf__hhq)
                    net__lcmo[sqkat__xpdjc] = urca__yctgu
                return bodo.hiframes.pd_series_ext.init_series(net__lcmo,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            btsxl__fqi = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                swe__vvia = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                vbf__yxugd = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    swe__vvia)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                zyar__mep = len(vbf__yxugd)
                net__lcmo = bodo.libs.bool_arr_ext.alloc_bool_array(zyar__mep)
                coqzg__dcmk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    btsxl__fqi)
                vce__ddmyz = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                ojbtw__kzflx = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    vce__ddmyz)
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    sydl__tzn = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vbf__yxugd[sqkat__xpdjc])
                    if sydl__tzn == coqzg__dcmk or ojbtw__kzflx == coqzg__dcmk:
                        urca__yctgu = aanc__btuk
                    else:
                        urca__yctgu = op(sydl__tzn, ojbtw__kzflx)
                    net__lcmo[sqkat__xpdjc] = urca__yctgu
                return bodo.hiframes.pd_series_ext.init_series(net__lcmo,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            btsxl__fqi = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                swe__vvia = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vbf__yxugd = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    swe__vvia)
                ssnqg__dyb = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                xywix__dbtzi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                zyar__mep = len(vbf__yxugd)
                net__lcmo = bodo.libs.bool_arr_ext.alloc_bool_array(zyar__mep)
                coqzg__dcmk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    btsxl__fqi)
                vce__ddmyz = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                ojbtw__kzflx = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    vce__ddmyz)
                for sqkat__xpdjc in numba.parfors.parfor.internal_prange(
                    zyar__mep):
                    tvn__bus = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vbf__yxugd[sqkat__xpdjc])
                    if tvn__bus == coqzg__dcmk or ojbtw__kzflx == coqzg__dcmk:
                        urca__yctgu = aanc__btuk
                    else:
                        urca__yctgu = op(ojbtw__kzflx, tvn__bus)
                    net__lcmo[sqkat__xpdjc] = urca__yctgu
                return bodo.hiframes.pd_series_ext.init_series(net__lcmo,
                    ssnqg__dyb, xywix__dbtzi)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for ely__iljmc in series_dt_unsupported_attrs:
        kcmbt__nkafo = 'Series.dt.' + ely__iljmc
        overload_attribute(SeriesDatetimePropertiesType, ely__iljmc)(
            create_unsupported_overload(kcmbt__nkafo))
    for encxp__tnh in series_dt_unsupported_methods:
        kcmbt__nkafo = 'Series.dt.' + encxp__tnh
        overload_method(SeriesDatetimePropertiesType, encxp__tnh,
            no_unliteral=True)(create_unsupported_overload(kcmbt__nkafo))


_install_series_dt_unsupported()
