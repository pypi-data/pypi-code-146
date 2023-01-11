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
        ickz__gcf = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(ickz__gcf)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lnw__newhn = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, lnw__newhn)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        lsou__lzuxo, = args
        ytpia__afjs = signature.return_type
        ayl__otwb = cgutils.create_struct_proxy(ytpia__afjs)(context, builder)
        ayl__otwb.obj = lsou__lzuxo
        context.nrt.incref(builder, signature.args[0], lsou__lzuxo)
        return ayl__otwb._getvalue()
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
        iosw__zhnw = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        imy__zbdtx = ['year', 'quarter', 'month', 'week', 'day', 'hour',
            'minute', 'second', 'microsecond']
        if field not in imy__zbdtx:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{field}')
        yus__dvb = 'def impl(S_dt):\n'
        yus__dvb += '    S = S_dt._obj\n'
        yus__dvb += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        yus__dvb += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        yus__dvb += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        yus__dvb += '    numba.parfors.parfor.init_prange()\n'
        yus__dvb += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            yus__dvb += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            yus__dvb += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        yus__dvb += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        yus__dvb += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        yus__dvb += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        yus__dvb += '            continue\n'
        if not iosw__zhnw:
            yus__dvb += (
                '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
                )
            yus__dvb += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            if field == 'weekday':
                yus__dvb += '        out_arr[i] = ts.weekday()\n'
            else:
                yus__dvb += '        out_arr[i] = ts.' + field + '\n'
        else:
            yus__dvb += '        out_arr[i] = arr[i].{}\n'.format(field)
        yus__dvb += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        kxoy__plo = {}
        exec(yus__dvb, {'bodo': bodo, 'numba': numba, 'np': np}, kxoy__plo)
        impl = kxoy__plo['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        tliqe__uqxm = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(tliqe__uqxm)


_install_date_fields()


def create_date_method_overload(method):
    aij__rsng = method in ['day_name', 'month_name']
    if aij__rsng:
        yus__dvb = 'def overload_method(S_dt, locale=None):\n'
        yus__dvb += '    unsupported_args = dict(locale=locale)\n'
        yus__dvb += '    arg_defaults = dict(locale=None)\n'
        yus__dvb += '    bodo.utils.typing.check_unsupported_args(\n'
        yus__dvb += f"        'Series.dt.{method}',\n"
        yus__dvb += '        unsupported_args,\n'
        yus__dvb += '        arg_defaults,\n'
        yus__dvb += "        package_name='pandas',\n"
        yus__dvb += "        module_name='Series',\n"
        yus__dvb += '    )\n'
    else:
        yus__dvb = 'def overload_method(S_dt):\n'
        yus__dvb += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    yus__dvb += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    yus__dvb += '        return\n'
    if aij__rsng:
        yus__dvb += '    def impl(S_dt, locale=None):\n'
    else:
        yus__dvb += '    def impl(S_dt):\n'
    yus__dvb += '        S = S_dt._obj\n'
    yus__dvb += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    yus__dvb += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    yus__dvb += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    yus__dvb += '        numba.parfors.parfor.init_prange()\n'
    yus__dvb += '        n = len(arr)\n'
    if aij__rsng:
        yus__dvb += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        yus__dvb += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    yus__dvb += '        for i in numba.parfors.parfor.internal_prange(n):\n'
    yus__dvb += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    yus__dvb += '                bodo.libs.array_kernels.setna(out_arr, i)\n'
    yus__dvb += '                continue\n'
    yus__dvb += '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n'
    yus__dvb += f'            method_val = ts.{method}()\n'
    if aij__rsng:
        yus__dvb += '            out_arr[i] = method_val\n'
    else:
        yus__dvb += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    yus__dvb += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    yus__dvb += '    return impl\n'
    kxoy__plo = {}
    exec(yus__dvb, {'bodo': bodo, 'numba': numba, 'np': np}, kxoy__plo)
    overload_method = kxoy__plo['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        tliqe__uqxm = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            tliqe__uqxm)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        annyd__uykn = S_dt._obj
        qmnd__aqao = bodo.hiframes.pd_series_ext.get_series_data(annyd__uykn)
        wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(annyd__uykn)
        ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(annyd__uykn)
        numba.parfors.parfor.init_prange()
        tpsr__vjk = len(qmnd__aqao)
        umrug__mskfv = (bodo.hiframes.datetime_date_ext.
            alloc_datetime_date_array(tpsr__vjk))
        for xwmk__wjcja in numba.parfors.parfor.internal_prange(tpsr__vjk):
            jycc__psiic = qmnd__aqao[xwmk__wjcja]
            hcimh__cwrau = bodo.utils.conversion.box_if_dt64(jycc__psiic)
            umrug__mskfv[xwmk__wjcja] = datetime.date(hcimh__cwrau.year,
                hcimh__cwrau.month, hcimh__cwrau.day)
        return bodo.hiframes.pd_series_ext.init_series(umrug__mskfv,
            wzqst__bfk, ickz__gcf)
    return impl


def create_series_dt_df_output_overload(attr):

    def series_dt_df_output_overload(S_dt):
        if not (attr == 'components' and S_dt.stype.dtype == types.
            NPTimedelta('ns') or attr == 'isocalendar' and (S_dt.stype.
            dtype == types.NPDatetime('ns') or isinstance(S_dt.stype.dtype,
            PandasDatetimeTZDtype))):
            return
        iosw__zhnw = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        if attr != 'isocalendar':
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{attr}')
        if attr == 'components':
            rad__meuz = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            ecsft__eag = 'convert_numpy_timedelta64_to_pd_timedelta'
            ifwgd__hngzj = 'np.empty(n, np.int64)'
            gmmz__lxxf = attr
        elif attr == 'isocalendar':
            rad__meuz = ['year', 'week', 'day']
            if iosw__zhnw:
                ecsft__eag = None
            else:
                ecsft__eag = 'convert_datetime64_to_timestamp'
            ifwgd__hngzj = (
                'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)')
            gmmz__lxxf = attr + '()'
        yus__dvb = 'def impl(S_dt):\n'
        yus__dvb += '    S = S_dt._obj\n'
        yus__dvb += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        yus__dvb += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        yus__dvb += '    numba.parfors.parfor.init_prange()\n'
        yus__dvb += '    n = len(arr)\n'
        for field in rad__meuz:
            yus__dvb += '    {} = {}\n'.format(field, ifwgd__hngzj)
        yus__dvb += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        yus__dvb += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in rad__meuz:
            yus__dvb += ('            bodo.libs.array_kernels.setna({}, i)\n'
                .format(field))
        yus__dvb += '            continue\n'
        cjia__yqvfw = '(' + '[i], '.join(rad__meuz) + '[i])'
        if ecsft__eag:
            jbibd__taj = f'bodo.hiframes.pd_timestamp_ext.{ecsft__eag}(arr[i])'
        else:
            jbibd__taj = 'arr[i]'
        yus__dvb += f'        {cjia__yqvfw} = {jbibd__taj}.{gmmz__lxxf}\n'
        xahw__faqbr = '(' + ', '.join(rad__meuz) + ')'
        yus__dvb += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, __col_name_meta_value_series_dt_df_output)
"""
            .format(xahw__faqbr))
        kxoy__plo = {}
        exec(yus__dvb, {'bodo': bodo, 'numba': numba, 'np': np,
            '__col_name_meta_value_series_dt_df_output': ColNamesMetaType(
            tuple(rad__meuz))}, kxoy__plo)
        impl = kxoy__plo['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    lbqd__wyqm = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, himk__vglc in lbqd__wyqm:
        tliqe__uqxm = create_series_dt_df_output_overload(attr)
        himk__vglc(SeriesDatetimePropertiesType, attr, inline='always')(
            tliqe__uqxm)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        yus__dvb = 'def impl(S_dt):\n'
        yus__dvb += '    S = S_dt._obj\n'
        yus__dvb += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        yus__dvb += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        yus__dvb += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        yus__dvb += '    numba.parfors.parfor.init_prange()\n'
        yus__dvb += '    n = len(A)\n'
        yus__dvb += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        yus__dvb += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        yus__dvb += '        if bodo.libs.array_kernels.isna(A, i):\n'
        yus__dvb += '            bodo.libs.array_kernels.setna(B, i)\n'
        yus__dvb += '            continue\n'
        yus__dvb += (
            '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
            )
        if field == 'nanoseconds':
            yus__dvb += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            yus__dvb += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            yus__dvb += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            yus__dvb += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        yus__dvb += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        kxoy__plo = {}
        exec(yus__dvb, {'numba': numba, 'np': np, 'bodo': bodo}, kxoy__plo)
        impl = kxoy__plo['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        yus__dvb = 'def impl(S_dt):\n'
        yus__dvb += '    S = S_dt._obj\n'
        yus__dvb += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        yus__dvb += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        yus__dvb += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        yus__dvb += '    numba.parfors.parfor.init_prange()\n'
        yus__dvb += '    n = len(A)\n'
        if method == 'total_seconds':
            yus__dvb += '    B = np.empty(n, np.float64)\n'
        else:
            yus__dvb += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        yus__dvb += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        yus__dvb += '        if bodo.libs.array_kernels.isna(A, i):\n'
        yus__dvb += '            bodo.libs.array_kernels.setna(B, i)\n'
        yus__dvb += '            continue\n'
        yus__dvb += (
            '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
            )
        if method == 'total_seconds':
            yus__dvb += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            yus__dvb += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            yus__dvb += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            yus__dvb += '    return B\n'
        kxoy__plo = {}
        exec(yus__dvb, {'numba': numba, 'np': np, 'bodo': bodo, 'datetime':
            datetime}, kxoy__plo)
        impl = kxoy__plo['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        tliqe__uqxm = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(tliqe__uqxm)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        tliqe__uqxm = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            tliqe__uqxm)


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
        annyd__uykn = S_dt._obj
        meqqz__vfzuf = bodo.hiframes.pd_series_ext.get_series_data(annyd__uykn)
        wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(annyd__uykn)
        ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(annyd__uykn)
        numba.parfors.parfor.init_prange()
        tpsr__vjk = len(meqqz__vfzuf)
        bro__ouyne = bodo.libs.str_arr_ext.pre_alloc_string_array(tpsr__vjk, -1
            )
        for mvg__iun in numba.parfors.parfor.internal_prange(tpsr__vjk):
            if bodo.libs.array_kernels.isna(meqqz__vfzuf, mvg__iun):
                bodo.libs.array_kernels.setna(bro__ouyne, mvg__iun)
                continue
            bro__ouyne[mvg__iun] = bodo.utils.conversion.box_if_dt64(
                meqqz__vfzuf[mvg__iun]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(bro__ouyne,
            wzqst__bfk, ickz__gcf)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        annyd__uykn = S_dt._obj
        pedip__zarss = get_series_data(annyd__uykn).tz_convert(tz)
        wzqst__bfk = get_series_index(annyd__uykn)
        ickz__gcf = get_series_name(annyd__uykn)
        return init_series(pedip__zarss, wzqst__bfk, ickz__gcf)
    return impl


def create_timedelta_freq_overload(method):

    def freq_overload(S_dt, freq, ambiguous='raise', nonexistent='raise'):
        if S_dt.stype.dtype != types.NPTimedelta('ns'
            ) and S_dt.stype.dtype != types.NPDatetime('ns'
            ) and not isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype):
            return
        cvj__kmkg = isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype)
        spxg__smvb = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        uknd__ffbdd = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', spxg__smvb,
            uknd__ffbdd, package_name='pandas', module_name='Series')
        yus__dvb = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        yus__dvb += '    S = S_dt._obj\n'
        yus__dvb += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        yus__dvb += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        yus__dvb += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        yus__dvb += '    numba.parfors.parfor.init_prange()\n'
        yus__dvb += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            yus__dvb += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        elif cvj__kmkg:
            yus__dvb += """    B = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(n, tz_literal)
"""
        else:
            yus__dvb += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        yus__dvb += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        yus__dvb += '        if bodo.libs.array_kernels.isna(A, i):\n'
        yus__dvb += '            bodo.libs.array_kernels.setna(B, i)\n'
        yus__dvb += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            wtch__dqv = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            cllol__hhbjs = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            wtch__dqv = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            cllol__hhbjs = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        if cvj__kmkg:
            yus__dvb += f'        B[i] = A[i].{method}(freq)\n'
        else:
            yus__dvb += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
                cllol__hhbjs, wtch__dqv, method)
        yus__dvb += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        kxoy__plo = {}
        nrfh__nmar = None
        if cvj__kmkg:
            nrfh__nmar = S_dt.stype.dtype.tz
        exec(yus__dvb, {'numba': numba, 'np': np, 'bodo': bodo,
            'tz_literal': nrfh__nmar}, kxoy__plo)
        impl = kxoy__plo['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    plvv__tua = ['ceil', 'floor', 'round']
    for method in plvv__tua:
        tliqe__uqxm = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            tliqe__uqxm)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            swa__bwnjl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                gzw__hggk = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qyqj__ppr = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    gzw__hggk)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                udi__dqvo = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vupfe__qqiw = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    udi__dqvo)
                tpsr__vjk = len(qyqj__ppr)
                annyd__uykn = np.empty(tpsr__vjk, timedelta64_dtype)
                iomd__yregs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    swa__bwnjl)
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    nbfi__oacwj = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qyqj__ppr[xwmk__wjcja]))
                    qsad__ziz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        vupfe__qqiw[xwmk__wjcja])
                    if nbfi__oacwj == iomd__yregs or qsad__ziz == iomd__yregs:
                        vmlnv__yzzo = iomd__yregs
                    else:
                        vmlnv__yzzo = op(nbfi__oacwj, qsad__ziz)
                    annyd__uykn[xwmk__wjcja
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        vmlnv__yzzo)
                return bodo.hiframes.pd_series_ext.init_series(annyd__uykn,
                    wzqst__bfk, ickz__gcf)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            swa__bwnjl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kqj__dzqit = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qmnd__aqao = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kqj__dzqit)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                vupfe__qqiw = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                tpsr__vjk = len(qmnd__aqao)
                annyd__uykn = np.empty(tpsr__vjk, dt64_dtype)
                iomd__yregs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    swa__bwnjl)
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    yeezh__emjc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    cro__isri = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(vupfe__qqiw[xwmk__wjcja]))
                    if yeezh__emjc == iomd__yregs or cro__isri == iomd__yregs:
                        vmlnv__yzzo = iomd__yregs
                    else:
                        vmlnv__yzzo = op(yeezh__emjc, cro__isri)
                    annyd__uykn[xwmk__wjcja
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        vmlnv__yzzo)
                return bodo.hiframes.pd_series_ext.init_series(annyd__uykn,
                    wzqst__bfk, ickz__gcf)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            swa__bwnjl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kqj__dzqit = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qmnd__aqao = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kqj__dzqit)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                vupfe__qqiw = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                tpsr__vjk = len(qmnd__aqao)
                annyd__uykn = np.empty(tpsr__vjk, dt64_dtype)
                iomd__yregs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    swa__bwnjl)
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    yeezh__emjc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    cro__isri = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(vupfe__qqiw[xwmk__wjcja]))
                    if yeezh__emjc == iomd__yregs or cro__isri == iomd__yregs:
                        vmlnv__yzzo = iomd__yregs
                    else:
                        vmlnv__yzzo = op(yeezh__emjc, cro__isri)
                    annyd__uykn[xwmk__wjcja
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        vmlnv__yzzo)
                return bodo.hiframes.pd_series_ext.init_series(annyd__uykn,
                    wzqst__bfk, ickz__gcf)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            swa__bwnjl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kqj__dzqit = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qmnd__aqao = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kqj__dzqit)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tpsr__vjk = len(qmnd__aqao)
                annyd__uykn = np.empty(tpsr__vjk, timedelta64_dtype)
                iomd__yregs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    swa__bwnjl)
                ceqkd__lqul = rhs.value
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    yeezh__emjc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    if (yeezh__emjc == iomd__yregs or ceqkd__lqul ==
                        iomd__yregs):
                        vmlnv__yzzo = iomd__yregs
                    else:
                        vmlnv__yzzo = op(yeezh__emjc, ceqkd__lqul)
                    annyd__uykn[xwmk__wjcja
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        vmlnv__yzzo)
                return bodo.hiframes.pd_series_ext.init_series(annyd__uykn,
                    wzqst__bfk, ickz__gcf)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            swa__bwnjl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kqj__dzqit = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qmnd__aqao = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kqj__dzqit)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tpsr__vjk = len(qmnd__aqao)
                annyd__uykn = np.empty(tpsr__vjk, timedelta64_dtype)
                iomd__yregs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    swa__bwnjl)
                ceqkd__lqul = lhs.value
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    yeezh__emjc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    if (ceqkd__lqul == iomd__yregs or yeezh__emjc ==
                        iomd__yregs):
                        vmlnv__yzzo = iomd__yregs
                    else:
                        vmlnv__yzzo = op(ceqkd__lqul, yeezh__emjc)
                    annyd__uykn[xwmk__wjcja
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        vmlnv__yzzo)
                return bodo.hiframes.pd_series_ext.init_series(annyd__uykn,
                    wzqst__bfk, ickz__gcf)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            swa__bwnjl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kqj__dzqit = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qmnd__aqao = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kqj__dzqit)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tpsr__vjk = len(qmnd__aqao)
                annyd__uykn = np.empty(tpsr__vjk, dt64_dtype)
                iomd__yregs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    swa__bwnjl)
                rtsj__gjoek = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                cro__isri = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(rtsj__gjoek))
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    yeezh__emjc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    if yeezh__emjc == iomd__yregs or cro__isri == iomd__yregs:
                        vmlnv__yzzo = iomd__yregs
                    else:
                        vmlnv__yzzo = op(yeezh__emjc, cro__isri)
                    annyd__uykn[xwmk__wjcja
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        vmlnv__yzzo)
                return bodo.hiframes.pd_series_ext.init_series(annyd__uykn,
                    wzqst__bfk, ickz__gcf)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            swa__bwnjl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kqj__dzqit = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qmnd__aqao = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kqj__dzqit)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tpsr__vjk = len(qmnd__aqao)
                annyd__uykn = np.empty(tpsr__vjk, dt64_dtype)
                iomd__yregs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    swa__bwnjl)
                rtsj__gjoek = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                cro__isri = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(rtsj__gjoek))
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    yeezh__emjc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    if yeezh__emjc == iomd__yregs or cro__isri == iomd__yregs:
                        vmlnv__yzzo = iomd__yregs
                    else:
                        vmlnv__yzzo = op(yeezh__emjc, cro__isri)
                    annyd__uykn[xwmk__wjcja
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        vmlnv__yzzo)
                return bodo.hiframes.pd_series_ext.init_series(annyd__uykn,
                    wzqst__bfk, ickz__gcf)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            swa__bwnjl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kqj__dzqit = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qmnd__aqao = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kqj__dzqit)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tpsr__vjk = len(qmnd__aqao)
                annyd__uykn = np.empty(tpsr__vjk, timedelta64_dtype)
                iomd__yregs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    swa__bwnjl)
                uwnlr__pjb = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                yeezh__emjc = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uwnlr__pjb)
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    bkipl__ekqkp = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    if (bkipl__ekqkp == iomd__yregs or yeezh__emjc ==
                        iomd__yregs):
                        vmlnv__yzzo = iomd__yregs
                    else:
                        vmlnv__yzzo = op(bkipl__ekqkp, yeezh__emjc)
                    annyd__uykn[xwmk__wjcja
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        vmlnv__yzzo)
                return bodo.hiframes.pd_series_ext.init_series(annyd__uykn,
                    wzqst__bfk, ickz__gcf)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            swa__bwnjl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kqj__dzqit = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qmnd__aqao = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kqj__dzqit)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tpsr__vjk = len(qmnd__aqao)
                annyd__uykn = np.empty(tpsr__vjk, timedelta64_dtype)
                iomd__yregs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    swa__bwnjl)
                uwnlr__pjb = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                yeezh__emjc = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uwnlr__pjb)
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    bkipl__ekqkp = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    if (yeezh__emjc == iomd__yregs or bkipl__ekqkp ==
                        iomd__yregs):
                        vmlnv__yzzo = iomd__yregs
                    else:
                        vmlnv__yzzo = op(yeezh__emjc, bkipl__ekqkp)
                    annyd__uykn[xwmk__wjcja
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        vmlnv__yzzo)
                return bodo.hiframes.pd_series_ext.init_series(annyd__uykn,
                    wzqst__bfk, ickz__gcf)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            swa__bwnjl = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qmnd__aqao = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tpsr__vjk = len(qmnd__aqao)
                annyd__uykn = np.empty(tpsr__vjk, timedelta64_dtype)
                iomd__yregs = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(swa__bwnjl))
                rtsj__gjoek = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                cro__isri = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(rtsj__gjoek))
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    tytph__nekym = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    if cro__isri == iomd__yregs or tytph__nekym == iomd__yregs:
                        vmlnv__yzzo = iomd__yregs
                    else:
                        vmlnv__yzzo = op(tytph__nekym, cro__isri)
                    annyd__uykn[xwmk__wjcja
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        vmlnv__yzzo)
                return bodo.hiframes.pd_series_ext.init_series(annyd__uykn,
                    wzqst__bfk, ickz__gcf)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            swa__bwnjl = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qmnd__aqao = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tpsr__vjk = len(qmnd__aqao)
                annyd__uykn = np.empty(tpsr__vjk, timedelta64_dtype)
                iomd__yregs = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(swa__bwnjl))
                rtsj__gjoek = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                cro__isri = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(rtsj__gjoek))
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    tytph__nekym = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    if cro__isri == iomd__yregs or tytph__nekym == iomd__yregs:
                        vmlnv__yzzo = iomd__yregs
                    else:
                        vmlnv__yzzo = op(cro__isri, tytph__nekym)
                    annyd__uykn[xwmk__wjcja
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        vmlnv__yzzo)
                return bodo.hiframes.pd_series_ext.init_series(annyd__uykn,
                    wzqst__bfk, ickz__gcf)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            bknd__mhet = True
        else:
            bknd__mhet = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            swa__bwnjl = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qmnd__aqao = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tpsr__vjk = len(qmnd__aqao)
                umrug__mskfv = bodo.libs.bool_arr_ext.alloc_bool_array(
                    tpsr__vjk)
                iomd__yregs = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(swa__bwnjl))
                jnjk__dpyn = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                zck__ibo = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(jnjk__dpyn))
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    jaxx__iipde = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    if jaxx__iipde == iomd__yregs or zck__ibo == iomd__yregs:
                        vmlnv__yzzo = bknd__mhet
                    else:
                        vmlnv__yzzo = op(jaxx__iipde, zck__ibo)
                    umrug__mskfv[xwmk__wjcja] = vmlnv__yzzo
                return bodo.hiframes.pd_series_ext.init_series(umrug__mskfv,
                    wzqst__bfk, ickz__gcf)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            swa__bwnjl = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qmnd__aqao = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tpsr__vjk = len(qmnd__aqao)
                umrug__mskfv = bodo.libs.bool_arr_ext.alloc_bool_array(
                    tpsr__vjk)
                iomd__yregs = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(swa__bwnjl))
                clkew__ukvw = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                jaxx__iipde = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(clkew__ukvw))
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    zck__ibo = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    if jaxx__iipde == iomd__yregs or zck__ibo == iomd__yregs:
                        vmlnv__yzzo = bknd__mhet
                    else:
                        vmlnv__yzzo = op(jaxx__iipde, zck__ibo)
                    umrug__mskfv[xwmk__wjcja] = vmlnv__yzzo
                return bodo.hiframes.pd_series_ext.init_series(umrug__mskfv,
                    wzqst__bfk, ickz__gcf)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            swa__bwnjl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kqj__dzqit = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qmnd__aqao = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kqj__dzqit)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tpsr__vjk = len(qmnd__aqao)
                umrug__mskfv = bodo.libs.bool_arr_ext.alloc_bool_array(
                    tpsr__vjk)
                iomd__yregs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    swa__bwnjl)
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    jaxx__iipde = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    if jaxx__iipde == iomd__yregs or rhs.value == iomd__yregs:
                        vmlnv__yzzo = bknd__mhet
                    else:
                        vmlnv__yzzo = op(jaxx__iipde, rhs.value)
                    umrug__mskfv[xwmk__wjcja] = vmlnv__yzzo
                return bodo.hiframes.pd_series_ext.init_series(umrug__mskfv,
                    wzqst__bfk, ickz__gcf)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.
            pd_timestamp_tz_naive_type and bodo.hiframes.pd_series_ext.
            is_dt64_series_typ(rhs)):
            swa__bwnjl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kqj__dzqit = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qmnd__aqao = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kqj__dzqit)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tpsr__vjk = len(qmnd__aqao)
                umrug__mskfv = bodo.libs.bool_arr_ext.alloc_bool_array(
                    tpsr__vjk)
                iomd__yregs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    swa__bwnjl)
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    zck__ibo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        qmnd__aqao[xwmk__wjcja])
                    if zck__ibo == iomd__yregs or lhs.value == iomd__yregs:
                        vmlnv__yzzo = bknd__mhet
                    else:
                        vmlnv__yzzo = op(lhs.value, zck__ibo)
                    umrug__mskfv[xwmk__wjcja] = vmlnv__yzzo
                return bodo.hiframes.pd_series_ext.init_series(umrug__mskfv,
                    wzqst__bfk, ickz__gcf)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            swa__bwnjl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                kqj__dzqit = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qmnd__aqao = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kqj__dzqit)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                tpsr__vjk = len(qmnd__aqao)
                umrug__mskfv = bodo.libs.bool_arr_ext.alloc_bool_array(
                    tpsr__vjk)
                iomd__yregs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    swa__bwnjl)
                skkyy__zab = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                vzak__xjcf = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    skkyy__zab)
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    jaxx__iipde = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    if jaxx__iipde == iomd__yregs or vzak__xjcf == iomd__yregs:
                        vmlnv__yzzo = bknd__mhet
                    else:
                        vmlnv__yzzo = op(jaxx__iipde, vzak__xjcf)
                    umrug__mskfv[xwmk__wjcja] = vmlnv__yzzo
                return bodo.hiframes.pd_series_ext.init_series(umrug__mskfv,
                    wzqst__bfk, ickz__gcf)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            swa__bwnjl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                kqj__dzqit = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qmnd__aqao = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kqj__dzqit)
                wzqst__bfk = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ickz__gcf = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                tpsr__vjk = len(qmnd__aqao)
                umrug__mskfv = bodo.libs.bool_arr_ext.alloc_bool_array(
                    tpsr__vjk)
                iomd__yregs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    swa__bwnjl)
                skkyy__zab = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                vzak__xjcf = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    skkyy__zab)
                for xwmk__wjcja in numba.parfors.parfor.internal_prange(
                    tpsr__vjk):
                    uwnlr__pjb = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qmnd__aqao[xwmk__wjcja]))
                    if uwnlr__pjb == iomd__yregs or vzak__xjcf == iomd__yregs:
                        vmlnv__yzzo = bknd__mhet
                    else:
                        vmlnv__yzzo = op(vzak__xjcf, uwnlr__pjb)
                    umrug__mskfv[xwmk__wjcja] = vmlnv__yzzo
                return bodo.hiframes.pd_series_ext.init_series(umrug__mskfv,
                    wzqst__bfk, ickz__gcf)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for ohoeg__hqkv in series_dt_unsupported_attrs:
        bqj__vtbt = 'Series.dt.' + ohoeg__hqkv
        overload_attribute(SeriesDatetimePropertiesType, ohoeg__hqkv)(
            create_unsupported_overload(bqj__vtbt))
    for vqpn__nuoxc in series_dt_unsupported_methods:
        bqj__vtbt = 'Series.dt.' + vqpn__nuoxc
        overload_method(SeriesDatetimePropertiesType, vqpn__nuoxc,
            no_unliteral=True)(create_unsupported_overload(bqj__vtbt))


_install_series_dt_unsupported()
