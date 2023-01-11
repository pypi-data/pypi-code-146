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
        zmns__jvce = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(zmns__jvce)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kohj__zgjf = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, kohj__zgjf)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        ueqn__gzjkk, = args
        hupmi__rdzm = signature.return_type
        gky__wzjx = cgutils.create_struct_proxy(hupmi__rdzm)(context, builder)
        gky__wzjx.obj = ueqn__gzjkk
        context.nrt.incref(builder, signature.args[0], ueqn__gzjkk)
        return gky__wzjx._getvalue()
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
        yrie__jcu = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        ccx__nvnyo = ['year', 'quarter', 'month', 'week', 'day', 'hour',
            'minute', 'second', 'microsecond']
        if field not in ccx__nvnyo:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{field}')
        gxkk__mymi = 'def impl(S_dt):\n'
        gxkk__mymi += '    S = S_dt._obj\n'
        gxkk__mymi += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        gxkk__mymi += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        gxkk__mymi += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        gxkk__mymi += '    numba.parfors.parfor.init_prange()\n'
        gxkk__mymi += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            gxkk__mymi += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            gxkk__mymi += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        gxkk__mymi += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        gxkk__mymi += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        gxkk__mymi += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        gxkk__mymi += '            continue\n'
        if not yrie__jcu:
            gxkk__mymi += (
                '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
                )
            gxkk__mymi += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            if field == 'weekday':
                gxkk__mymi += '        out_arr[i] = ts.weekday()\n'
            else:
                gxkk__mymi += '        out_arr[i] = ts.' + field + '\n'
        else:
            gxkk__mymi += '        out_arr[i] = arr[i].{}\n'.format(field)
        gxkk__mymi += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        fgq__qbzog = {}
        exec(gxkk__mymi, {'bodo': bodo, 'numba': numba, 'np': np}, fgq__qbzog)
        impl = fgq__qbzog['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        bpd__pahdm = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(bpd__pahdm)


_install_date_fields()


def create_date_method_overload(method):
    macvv__rvj = method in ['day_name', 'month_name']
    if macvv__rvj:
        gxkk__mymi = 'def overload_method(S_dt, locale=None):\n'
        gxkk__mymi += '    unsupported_args = dict(locale=locale)\n'
        gxkk__mymi += '    arg_defaults = dict(locale=None)\n'
        gxkk__mymi += '    bodo.utils.typing.check_unsupported_args(\n'
        gxkk__mymi += f"        'Series.dt.{method}',\n"
        gxkk__mymi += '        unsupported_args,\n'
        gxkk__mymi += '        arg_defaults,\n'
        gxkk__mymi += "        package_name='pandas',\n"
        gxkk__mymi += "        module_name='Series',\n"
        gxkk__mymi += '    )\n'
    else:
        gxkk__mymi = 'def overload_method(S_dt):\n'
        gxkk__mymi += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    gxkk__mymi += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    gxkk__mymi += '        return\n'
    if macvv__rvj:
        gxkk__mymi += '    def impl(S_dt, locale=None):\n'
    else:
        gxkk__mymi += '    def impl(S_dt):\n'
    gxkk__mymi += '        S = S_dt._obj\n'
    gxkk__mymi += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    gxkk__mymi += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    gxkk__mymi += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    gxkk__mymi += '        numba.parfors.parfor.init_prange()\n'
    gxkk__mymi += '        n = len(arr)\n'
    if macvv__rvj:
        gxkk__mymi += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        gxkk__mymi += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    gxkk__mymi += '        for i in numba.parfors.parfor.internal_prange(n):\n'
    gxkk__mymi += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    gxkk__mymi += '                bodo.libs.array_kernels.setna(out_arr, i)\n'
    gxkk__mymi += '                continue\n'
    gxkk__mymi += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    gxkk__mymi += f'            method_val = ts.{method}()\n'
    if macvv__rvj:
        gxkk__mymi += '            out_arr[i] = method_val\n'
    else:
        gxkk__mymi += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    gxkk__mymi += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    gxkk__mymi += '    return impl\n'
    fgq__qbzog = {}
    exec(gxkk__mymi, {'bodo': bodo, 'numba': numba, 'np': np}, fgq__qbzog)
    overload_method = fgq__qbzog['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        bpd__pahdm = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            bpd__pahdm)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        bgdcx__afa = S_dt._obj
        vzhj__svwpt = bodo.hiframes.pd_series_ext.get_series_data(bgdcx__afa)
        pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(bgdcx__afa)
        zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(bgdcx__afa)
        numba.parfors.parfor.init_prange()
        pqq__xah = len(vzhj__svwpt)
        caeb__xmirl = (bodo.hiframes.datetime_date_ext.
            alloc_datetime_date_array(pqq__xah))
        for fzpmb__mrtx in numba.parfors.parfor.internal_prange(pqq__xah):
            iuv__nuyd = vzhj__svwpt[fzpmb__mrtx]
            ddl__ody = bodo.utils.conversion.box_if_dt64(iuv__nuyd)
            caeb__xmirl[fzpmb__mrtx] = datetime.date(ddl__ody.year,
                ddl__ody.month, ddl__ody.day)
        return bodo.hiframes.pd_series_ext.init_series(caeb__xmirl,
            pqv__vxrld, zmns__jvce)
    return impl


def create_series_dt_df_output_overload(attr):

    def series_dt_df_output_overload(S_dt):
        if not (attr == 'components' and S_dt.stype.dtype == types.
            NPTimedelta('ns') or attr == 'isocalendar' and (S_dt.stype.
            dtype == types.NPDatetime('ns') or isinstance(S_dt.stype.dtype,
            PandasDatetimeTZDtype))):
            return
        yrie__jcu = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        if attr != 'isocalendar':
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{attr}')
        if attr == 'components':
            gkm__xoz = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            xbo__ehfox = 'convert_numpy_timedelta64_to_pd_timedelta'
            oif__crcg = 'np.empty(n, np.int64)'
            pvo__eayp = attr
        elif attr == 'isocalendar':
            gkm__xoz = ['year', 'week', 'day']
            if yrie__jcu:
                xbo__ehfox = None
            else:
                xbo__ehfox = 'convert_datetime64_to_timestamp'
            oif__crcg = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            pvo__eayp = attr + '()'
        gxkk__mymi = 'def impl(S_dt):\n'
        gxkk__mymi += '    S = S_dt._obj\n'
        gxkk__mymi += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        gxkk__mymi += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        gxkk__mymi += '    numba.parfors.parfor.init_prange()\n'
        gxkk__mymi += '    n = len(arr)\n'
        for field in gkm__xoz:
            gxkk__mymi += '    {} = {}\n'.format(field, oif__crcg)
        gxkk__mymi += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        gxkk__mymi += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in gkm__xoz:
            gxkk__mymi += ('            bodo.libs.array_kernels.setna({}, i)\n'
                .format(field))
        gxkk__mymi += '            continue\n'
        cck__oeh = '(' + '[i], '.join(gkm__xoz) + '[i])'
        if xbo__ehfox:
            sjy__fffk = f'bodo.hiframes.pd_timestamp_ext.{xbo__ehfox}(arr[i])'
        else:
            sjy__fffk = 'arr[i]'
        gxkk__mymi += f'        {cck__oeh} = {sjy__fffk}.{pvo__eayp}\n'
        qaf__qce = '(' + ', '.join(gkm__xoz) + ')'
        gxkk__mymi += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, __col_name_meta_value_series_dt_df_output)
"""
            .format(qaf__qce))
        fgq__qbzog = {}
        exec(gxkk__mymi, {'bodo': bodo, 'numba': numba, 'np': np,
            '__col_name_meta_value_series_dt_df_output': ColNamesMetaType(
            tuple(gkm__xoz))}, fgq__qbzog)
        impl = fgq__qbzog['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    fzbt__vntqr = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, hwi__juzso in fzbt__vntqr:
        bpd__pahdm = create_series_dt_df_output_overload(attr)
        hwi__juzso(SeriesDatetimePropertiesType, attr, inline='always')(
            bpd__pahdm)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        gxkk__mymi = 'def impl(S_dt):\n'
        gxkk__mymi += '    S = S_dt._obj\n'
        gxkk__mymi += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        gxkk__mymi += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        gxkk__mymi += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        gxkk__mymi += '    numba.parfors.parfor.init_prange()\n'
        gxkk__mymi += '    n = len(A)\n'
        gxkk__mymi += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        gxkk__mymi += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        gxkk__mymi += '        if bodo.libs.array_kernels.isna(A, i):\n'
        gxkk__mymi += '            bodo.libs.array_kernels.setna(B, i)\n'
        gxkk__mymi += '            continue\n'
        gxkk__mymi += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            gxkk__mymi += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            gxkk__mymi += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            gxkk__mymi += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            gxkk__mymi += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        gxkk__mymi += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        fgq__qbzog = {}
        exec(gxkk__mymi, {'numba': numba, 'np': np, 'bodo': bodo}, fgq__qbzog)
        impl = fgq__qbzog['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        gxkk__mymi = 'def impl(S_dt):\n'
        gxkk__mymi += '    S = S_dt._obj\n'
        gxkk__mymi += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        gxkk__mymi += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        gxkk__mymi += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        gxkk__mymi += '    numba.parfors.parfor.init_prange()\n'
        gxkk__mymi += '    n = len(A)\n'
        if method == 'total_seconds':
            gxkk__mymi += '    B = np.empty(n, np.float64)\n'
        else:
            gxkk__mymi += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        gxkk__mymi += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        gxkk__mymi += '        if bodo.libs.array_kernels.isna(A, i):\n'
        gxkk__mymi += '            bodo.libs.array_kernels.setna(B, i)\n'
        gxkk__mymi += '            continue\n'
        gxkk__mymi += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            gxkk__mymi += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            gxkk__mymi += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            gxkk__mymi += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            gxkk__mymi += '    return B\n'
        fgq__qbzog = {}
        exec(gxkk__mymi, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, fgq__qbzog)
        impl = fgq__qbzog['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        bpd__pahdm = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(bpd__pahdm)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        bpd__pahdm = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            bpd__pahdm)


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
        bgdcx__afa = S_dt._obj
        xhqij__oanfw = bodo.hiframes.pd_series_ext.get_series_data(bgdcx__afa)
        pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(bgdcx__afa)
        zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(bgdcx__afa)
        numba.parfors.parfor.init_prange()
        pqq__xah = len(xhqij__oanfw)
        hod__uvfl = bodo.libs.str_arr_ext.pre_alloc_string_array(pqq__xah, -1)
        for owrke__mhyr in numba.parfors.parfor.internal_prange(pqq__xah):
            if bodo.libs.array_kernels.isna(xhqij__oanfw, owrke__mhyr):
                bodo.libs.array_kernels.setna(hod__uvfl, owrke__mhyr)
                continue
            hod__uvfl[owrke__mhyr] = bodo.utils.conversion.box_if_dt64(
                xhqij__oanfw[owrke__mhyr]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(hod__uvfl,
            pqv__vxrld, zmns__jvce)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        bgdcx__afa = S_dt._obj
        vpdjr__xef = get_series_data(bgdcx__afa).tz_convert(tz)
        pqv__vxrld = get_series_index(bgdcx__afa)
        zmns__jvce = get_series_name(bgdcx__afa)
        return init_series(vpdjr__xef, pqv__vxrld, zmns__jvce)
    return impl


def create_timedelta_freq_overload(method):

    def freq_overload(S_dt, freq, ambiguous='raise', nonexistent='raise'):
        if S_dt.stype.dtype != types.NPTimedelta('ns'
            ) and S_dt.stype.dtype != types.NPDatetime('ns'
            ) and not isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype):
            return
        qetea__avn = isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype)
        dionn__afpvs = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        mthzn__zau = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', dionn__afpvs,
            mthzn__zau, package_name='pandas', module_name='Series')
        gxkk__mymi = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        gxkk__mymi += '    S = S_dt._obj\n'
        gxkk__mymi += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        gxkk__mymi += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        gxkk__mymi += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        gxkk__mymi += '    numba.parfors.parfor.init_prange()\n'
        gxkk__mymi += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            gxkk__mymi += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        elif qetea__avn:
            gxkk__mymi += """    B = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(n, tz_literal)
"""
        else:
            gxkk__mymi += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        gxkk__mymi += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        gxkk__mymi += '        if bodo.libs.array_kernels.isna(A, i):\n'
        gxkk__mymi += '            bodo.libs.array_kernels.setna(B, i)\n'
        gxkk__mymi += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            oou__cecau = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            udiqg__dyur = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            oou__cecau = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            udiqg__dyur = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        if qetea__avn:
            gxkk__mymi += f'        B[i] = A[i].{method}(freq)\n'
        else:
            gxkk__mymi += ('        B[i] = {}({}(A[i]).{}(freq).value)\n'.
                format(udiqg__dyur, oou__cecau, method))
        gxkk__mymi += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        fgq__qbzog = {}
        nca__ooko = None
        if qetea__avn:
            nca__ooko = S_dt.stype.dtype.tz
        exec(gxkk__mymi, {'numba': numba, 'np': np, 'bodo': bodo,
            'tz_literal': nca__ooko}, fgq__qbzog)
        impl = fgq__qbzog['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    byijt__mhbld = ['ceil', 'floor', 'round']
    for method in byijt__mhbld:
        bpd__pahdm = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            bpd__pahdm)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            azwml__uci = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ldscc__lqsca = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                lle__btg = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ldscc__lqsca)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kjqx__lioj = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                puaot__bqyf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kjqx__lioj)
                pqq__xah = len(lle__btg)
                bgdcx__afa = np.empty(pqq__xah, timedelta64_dtype)
                bzcf__rzhfm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    azwml__uci)
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    uhvpw__vorc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(lle__btg[fzpmb__mrtx]))
                    aofc__pasv = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(puaot__bqyf[fzpmb__mrtx]))
                    if uhvpw__vorc == bzcf__rzhfm or aofc__pasv == bzcf__rzhfm:
                        uue__wvci = bzcf__rzhfm
                    else:
                        uue__wvci = op(uhvpw__vorc, aofc__pasv)
                    bgdcx__afa[fzpmb__mrtx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        uue__wvci)
                return bodo.hiframes.pd_series_ext.init_series(bgdcx__afa,
                    pqv__vxrld, zmns__jvce)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            azwml__uci = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                lez__bim = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                vzhj__svwpt = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    lez__bim)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                puaot__bqyf = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                pqq__xah = len(vzhj__svwpt)
                bgdcx__afa = np.empty(pqq__xah, dt64_dtype)
                bzcf__rzhfm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    azwml__uci)
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    qgfq__fan = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vzhj__svwpt[fzpmb__mrtx])
                    zps__vvlj = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(puaot__bqyf[fzpmb__mrtx]))
                    if qgfq__fan == bzcf__rzhfm or zps__vvlj == bzcf__rzhfm:
                        uue__wvci = bzcf__rzhfm
                    else:
                        uue__wvci = op(qgfq__fan, zps__vvlj)
                    bgdcx__afa[fzpmb__mrtx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        uue__wvci)
                return bodo.hiframes.pd_series_ext.init_series(bgdcx__afa,
                    pqv__vxrld, zmns__jvce)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            azwml__uci = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                lez__bim = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vzhj__svwpt = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    lez__bim)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                puaot__bqyf = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                pqq__xah = len(vzhj__svwpt)
                bgdcx__afa = np.empty(pqq__xah, dt64_dtype)
                bzcf__rzhfm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    azwml__uci)
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    qgfq__fan = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vzhj__svwpt[fzpmb__mrtx])
                    zps__vvlj = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(puaot__bqyf[fzpmb__mrtx]))
                    if qgfq__fan == bzcf__rzhfm or zps__vvlj == bzcf__rzhfm:
                        uue__wvci = bzcf__rzhfm
                    else:
                        uue__wvci = op(qgfq__fan, zps__vvlj)
                    bgdcx__afa[fzpmb__mrtx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        uue__wvci)
                return bodo.hiframes.pd_series_ext.init_series(bgdcx__afa,
                    pqv__vxrld, zmns__jvce)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            azwml__uci = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                lez__bim = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                vzhj__svwpt = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    lez__bim)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                pqq__xah = len(vzhj__svwpt)
                bgdcx__afa = np.empty(pqq__xah, timedelta64_dtype)
                bzcf__rzhfm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    azwml__uci)
                dlil__lszxp = rhs.value
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    qgfq__fan = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vzhj__svwpt[fzpmb__mrtx])
                    if qgfq__fan == bzcf__rzhfm or dlil__lszxp == bzcf__rzhfm:
                        uue__wvci = bzcf__rzhfm
                    else:
                        uue__wvci = op(qgfq__fan, dlil__lszxp)
                    bgdcx__afa[fzpmb__mrtx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        uue__wvci)
                return bodo.hiframes.pd_series_ext.init_series(bgdcx__afa,
                    pqv__vxrld, zmns__jvce)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            azwml__uci = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                lez__bim = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vzhj__svwpt = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    lez__bim)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                pqq__xah = len(vzhj__svwpt)
                bgdcx__afa = np.empty(pqq__xah, timedelta64_dtype)
                bzcf__rzhfm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    azwml__uci)
                dlil__lszxp = lhs.value
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    qgfq__fan = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vzhj__svwpt[fzpmb__mrtx])
                    if dlil__lszxp == bzcf__rzhfm or qgfq__fan == bzcf__rzhfm:
                        uue__wvci = bzcf__rzhfm
                    else:
                        uue__wvci = op(dlil__lszxp, qgfq__fan)
                    bgdcx__afa[fzpmb__mrtx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        uue__wvci)
                return bodo.hiframes.pd_series_ext.init_series(bgdcx__afa,
                    pqv__vxrld, zmns__jvce)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            azwml__uci = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                lez__bim = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                vzhj__svwpt = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    lez__bim)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                pqq__xah = len(vzhj__svwpt)
                bgdcx__afa = np.empty(pqq__xah, dt64_dtype)
                bzcf__rzhfm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    azwml__uci)
                vrzbq__ylfki = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                zps__vvlj = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(vrzbq__ylfki))
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    qgfq__fan = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vzhj__svwpt[fzpmb__mrtx])
                    if qgfq__fan == bzcf__rzhfm or zps__vvlj == bzcf__rzhfm:
                        uue__wvci = bzcf__rzhfm
                    else:
                        uue__wvci = op(qgfq__fan, zps__vvlj)
                    bgdcx__afa[fzpmb__mrtx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        uue__wvci)
                return bodo.hiframes.pd_series_ext.init_series(bgdcx__afa,
                    pqv__vxrld, zmns__jvce)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            azwml__uci = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                lez__bim = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vzhj__svwpt = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    lez__bim)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                pqq__xah = len(vzhj__svwpt)
                bgdcx__afa = np.empty(pqq__xah, dt64_dtype)
                bzcf__rzhfm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    azwml__uci)
                vrzbq__ylfki = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                zps__vvlj = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(vrzbq__ylfki))
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    qgfq__fan = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vzhj__svwpt[fzpmb__mrtx])
                    if qgfq__fan == bzcf__rzhfm or zps__vvlj == bzcf__rzhfm:
                        uue__wvci = bzcf__rzhfm
                    else:
                        uue__wvci = op(qgfq__fan, zps__vvlj)
                    bgdcx__afa[fzpmb__mrtx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        uue__wvci)
                return bodo.hiframes.pd_series_ext.init_series(bgdcx__afa,
                    pqv__vxrld, zmns__jvce)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            azwml__uci = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                lez__bim = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                vzhj__svwpt = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    lez__bim)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                pqq__xah = len(vzhj__svwpt)
                bgdcx__afa = np.empty(pqq__xah, timedelta64_dtype)
                bzcf__rzhfm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    azwml__uci)
                dnoo__angj = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                qgfq__fan = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    dnoo__angj)
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    kceh__izafn = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(vzhj__svwpt[fzpmb__mrtx]))
                    if kceh__izafn == bzcf__rzhfm or qgfq__fan == bzcf__rzhfm:
                        uue__wvci = bzcf__rzhfm
                    else:
                        uue__wvci = op(kceh__izafn, qgfq__fan)
                    bgdcx__afa[fzpmb__mrtx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        uue__wvci)
                return bodo.hiframes.pd_series_ext.init_series(bgdcx__afa,
                    pqv__vxrld, zmns__jvce)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            azwml__uci = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                lez__bim = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vzhj__svwpt = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    lez__bim)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                pqq__xah = len(vzhj__svwpt)
                bgdcx__afa = np.empty(pqq__xah, timedelta64_dtype)
                bzcf__rzhfm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    azwml__uci)
                dnoo__angj = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                qgfq__fan = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    dnoo__angj)
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    kceh__izafn = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(vzhj__svwpt[fzpmb__mrtx]))
                    if qgfq__fan == bzcf__rzhfm or kceh__izafn == bzcf__rzhfm:
                        uue__wvci = bzcf__rzhfm
                    else:
                        uue__wvci = op(qgfq__fan, kceh__izafn)
                    bgdcx__afa[fzpmb__mrtx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        uue__wvci)
                return bodo.hiframes.pd_series_ext.init_series(bgdcx__afa,
                    pqv__vxrld, zmns__jvce)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            azwml__uci = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vzhj__svwpt = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                pqq__xah = len(vzhj__svwpt)
                bgdcx__afa = np.empty(pqq__xah, timedelta64_dtype)
                bzcf__rzhfm = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(azwml__uci))
                vrzbq__ylfki = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                zps__vvlj = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(vrzbq__ylfki))
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    ntb__lbm = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(vzhj__svwpt[fzpmb__mrtx]))
                    if zps__vvlj == bzcf__rzhfm or ntb__lbm == bzcf__rzhfm:
                        uue__wvci = bzcf__rzhfm
                    else:
                        uue__wvci = op(ntb__lbm, zps__vvlj)
                    bgdcx__afa[fzpmb__mrtx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        uue__wvci)
                return bodo.hiframes.pd_series_ext.init_series(bgdcx__afa,
                    pqv__vxrld, zmns__jvce)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            azwml__uci = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vzhj__svwpt = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                pqq__xah = len(vzhj__svwpt)
                bgdcx__afa = np.empty(pqq__xah, timedelta64_dtype)
                bzcf__rzhfm = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(azwml__uci))
                vrzbq__ylfki = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                zps__vvlj = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(vrzbq__ylfki))
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    ntb__lbm = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(vzhj__svwpt[fzpmb__mrtx]))
                    if zps__vvlj == bzcf__rzhfm or ntb__lbm == bzcf__rzhfm:
                        uue__wvci = bzcf__rzhfm
                    else:
                        uue__wvci = op(zps__vvlj, ntb__lbm)
                    bgdcx__afa[fzpmb__mrtx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        uue__wvci)
                return bodo.hiframes.pd_series_ext.init_series(bgdcx__afa,
                    pqv__vxrld, zmns__jvce)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            xjdwk__wbrqt = True
        else:
            xjdwk__wbrqt = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            azwml__uci = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vzhj__svwpt = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                pqq__xah = len(vzhj__svwpt)
                caeb__xmirl = bodo.libs.bool_arr_ext.alloc_bool_array(pqq__xah)
                bzcf__rzhfm = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(azwml__uci))
                eyg__gmpo = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                jua__exwoy = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(eyg__gmpo))
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    rwns__epw = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(vzhj__svwpt[fzpmb__mrtx]))
                    if rwns__epw == bzcf__rzhfm or jua__exwoy == bzcf__rzhfm:
                        uue__wvci = xjdwk__wbrqt
                    else:
                        uue__wvci = op(rwns__epw, jua__exwoy)
                    caeb__xmirl[fzpmb__mrtx] = uue__wvci
                return bodo.hiframes.pd_series_ext.init_series(caeb__xmirl,
                    pqv__vxrld, zmns__jvce)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            azwml__uci = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vzhj__svwpt = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                pqq__xah = len(vzhj__svwpt)
                caeb__xmirl = bodo.libs.bool_arr_ext.alloc_bool_array(pqq__xah)
                bzcf__rzhfm = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(azwml__uci))
                hgku__sur = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                rwns__epw = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(hgku__sur))
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    jua__exwoy = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(vzhj__svwpt[fzpmb__mrtx]))
                    if rwns__epw == bzcf__rzhfm or jua__exwoy == bzcf__rzhfm:
                        uue__wvci = xjdwk__wbrqt
                    else:
                        uue__wvci = op(rwns__epw, jua__exwoy)
                    caeb__xmirl[fzpmb__mrtx] = uue__wvci
                return bodo.hiframes.pd_series_ext.init_series(caeb__xmirl,
                    pqv__vxrld, zmns__jvce)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            azwml__uci = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                lez__bim = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                vzhj__svwpt = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    lez__bim)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                pqq__xah = len(vzhj__svwpt)
                caeb__xmirl = bodo.libs.bool_arr_ext.alloc_bool_array(pqq__xah)
                bzcf__rzhfm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    azwml__uci)
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    rwns__epw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vzhj__svwpt[fzpmb__mrtx])
                    if rwns__epw == bzcf__rzhfm or rhs.value == bzcf__rzhfm:
                        uue__wvci = xjdwk__wbrqt
                    else:
                        uue__wvci = op(rwns__epw, rhs.value)
                    caeb__xmirl[fzpmb__mrtx] = uue__wvci
                return bodo.hiframes.pd_series_ext.init_series(caeb__xmirl,
                    pqv__vxrld, zmns__jvce)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.
            pd_timestamp_tz_naive_type and bodo.hiframes.pd_series_ext.
            is_dt64_series_typ(rhs)):
            azwml__uci = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                lez__bim = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vzhj__svwpt = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    lez__bim)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                pqq__xah = len(vzhj__svwpt)
                caeb__xmirl = bodo.libs.bool_arr_ext.alloc_bool_array(pqq__xah)
                bzcf__rzhfm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    azwml__uci)
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    jua__exwoy = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(vzhj__svwpt[fzpmb__mrtx]))
                    if jua__exwoy == bzcf__rzhfm or lhs.value == bzcf__rzhfm:
                        uue__wvci = xjdwk__wbrqt
                    else:
                        uue__wvci = op(lhs.value, jua__exwoy)
                    caeb__xmirl[fzpmb__mrtx] = uue__wvci
                return bodo.hiframes.pd_series_ext.init_series(caeb__xmirl,
                    pqv__vxrld, zmns__jvce)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            azwml__uci = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                lez__bim = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                vzhj__svwpt = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    lez__bim)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                pqq__xah = len(vzhj__svwpt)
                caeb__xmirl = bodo.libs.bool_arr_ext.alloc_bool_array(pqq__xah)
                bzcf__rzhfm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    azwml__uci)
                rzuv__eoqi = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                xsu__mlc = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    rzuv__eoqi)
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    rwns__epw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vzhj__svwpt[fzpmb__mrtx])
                    if rwns__epw == bzcf__rzhfm or xsu__mlc == bzcf__rzhfm:
                        uue__wvci = xjdwk__wbrqt
                    else:
                        uue__wvci = op(rwns__epw, xsu__mlc)
                    caeb__xmirl[fzpmb__mrtx] = uue__wvci
                return bodo.hiframes.pd_series_ext.init_series(caeb__xmirl,
                    pqv__vxrld, zmns__jvce)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            azwml__uci = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                lez__bim = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vzhj__svwpt = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    lez__bim)
                pqv__vxrld = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                zmns__jvce = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                pqq__xah = len(vzhj__svwpt)
                caeb__xmirl = bodo.libs.bool_arr_ext.alloc_bool_array(pqq__xah)
                bzcf__rzhfm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    azwml__uci)
                rzuv__eoqi = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                xsu__mlc = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    rzuv__eoqi)
                for fzpmb__mrtx in numba.parfors.parfor.internal_prange(
                    pqq__xah):
                    dnoo__angj = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(vzhj__svwpt[fzpmb__mrtx]))
                    if dnoo__angj == bzcf__rzhfm or xsu__mlc == bzcf__rzhfm:
                        uue__wvci = xjdwk__wbrqt
                    else:
                        uue__wvci = op(xsu__mlc, dnoo__angj)
                    caeb__xmirl[fzpmb__mrtx] = uue__wvci
                return bodo.hiframes.pd_series_ext.init_series(caeb__xmirl,
                    pqv__vxrld, zmns__jvce)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for igeim__yffi in series_dt_unsupported_attrs:
        verg__oizb = 'Series.dt.' + igeim__yffi
        overload_attribute(SeriesDatetimePropertiesType, igeim__yffi)(
            create_unsupported_overload(verg__oizb))
    for nwu__axiw in series_dt_unsupported_methods:
        verg__oizb = 'Series.dt.' + nwu__axiw
        overload_method(SeriesDatetimePropertiesType, nwu__axiw,
            no_unliteral=True)(create_unsupported_overload(verg__oizb))


_install_series_dt_unsupported()
