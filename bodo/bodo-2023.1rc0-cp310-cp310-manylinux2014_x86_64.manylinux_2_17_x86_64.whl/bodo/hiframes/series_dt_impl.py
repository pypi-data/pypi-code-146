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
        umpcq__qaydy = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(umpcq__qaydy)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        sbboc__ztnj = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, sbboc__ztnj)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        gkldp__dweah, = args
        dqd__mwm = signature.return_type
        ctku__qrnxd = cgutils.create_struct_proxy(dqd__mwm)(context, builder)
        ctku__qrnxd.obj = gkldp__dweah
        context.nrt.incref(builder, signature.args[0], gkldp__dweah)
        return ctku__qrnxd._getvalue()
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
        aixu__pmk = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        uhne__bvja = ['year', 'quarter', 'month', 'week', 'day', 'hour',
            'minute', 'second', 'microsecond']
        if field not in uhne__bvja:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{field}')
        oxfn__dzzvb = 'def impl(S_dt):\n'
        oxfn__dzzvb += '    S = S_dt._obj\n'
        oxfn__dzzvb += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        oxfn__dzzvb += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        oxfn__dzzvb += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        oxfn__dzzvb += '    numba.parfors.parfor.init_prange()\n'
        oxfn__dzzvb += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            oxfn__dzzvb += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            oxfn__dzzvb += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        oxfn__dzzvb += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        oxfn__dzzvb += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        oxfn__dzzvb += (
            '            bodo.libs.array_kernels.setna(out_arr, i)\n')
        oxfn__dzzvb += '            continue\n'
        if not aixu__pmk:
            oxfn__dzzvb += """        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])
"""
            oxfn__dzzvb += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            if field == 'weekday':
                oxfn__dzzvb += '        out_arr[i] = ts.weekday()\n'
            else:
                oxfn__dzzvb += '        out_arr[i] = ts.' + field + '\n'
        else:
            oxfn__dzzvb += '        out_arr[i] = arr[i].{}\n'.format(field)
        oxfn__dzzvb += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        bofi__rgmnv = {}
        exec(oxfn__dzzvb, {'bodo': bodo, 'numba': numba, 'np': np}, bofi__rgmnv
            )
        impl = bofi__rgmnv['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        curcl__bkt = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(curcl__bkt)


_install_date_fields()


def create_date_method_overload(method):
    toszk__shxer = method in ['day_name', 'month_name']
    if toszk__shxer:
        oxfn__dzzvb = 'def overload_method(S_dt, locale=None):\n'
        oxfn__dzzvb += '    unsupported_args = dict(locale=locale)\n'
        oxfn__dzzvb += '    arg_defaults = dict(locale=None)\n'
        oxfn__dzzvb += '    bodo.utils.typing.check_unsupported_args(\n'
        oxfn__dzzvb += f"        'Series.dt.{method}',\n"
        oxfn__dzzvb += '        unsupported_args,\n'
        oxfn__dzzvb += '        arg_defaults,\n'
        oxfn__dzzvb += "        package_name='pandas',\n"
        oxfn__dzzvb += "        module_name='Series',\n"
        oxfn__dzzvb += '    )\n'
    else:
        oxfn__dzzvb = 'def overload_method(S_dt):\n'
        oxfn__dzzvb += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    oxfn__dzzvb += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    oxfn__dzzvb += '        return\n'
    if toszk__shxer:
        oxfn__dzzvb += '    def impl(S_dt, locale=None):\n'
    else:
        oxfn__dzzvb += '    def impl(S_dt):\n'
    oxfn__dzzvb += '        S = S_dt._obj\n'
    oxfn__dzzvb += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    oxfn__dzzvb += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    oxfn__dzzvb += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    oxfn__dzzvb += '        numba.parfors.parfor.init_prange()\n'
    oxfn__dzzvb += '        n = len(arr)\n'
    if toszk__shxer:
        oxfn__dzzvb += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        oxfn__dzzvb += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    oxfn__dzzvb += (
        '        for i in numba.parfors.parfor.internal_prange(n):\n')
    oxfn__dzzvb += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    oxfn__dzzvb += (
        '                bodo.libs.array_kernels.setna(out_arr, i)\n')
    oxfn__dzzvb += '                continue\n'
    oxfn__dzzvb += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    oxfn__dzzvb += f'            method_val = ts.{method}()\n'
    if toszk__shxer:
        oxfn__dzzvb += '            out_arr[i] = method_val\n'
    else:
        oxfn__dzzvb += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    oxfn__dzzvb += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    oxfn__dzzvb += '    return impl\n'
    bofi__rgmnv = {}
    exec(oxfn__dzzvb, {'bodo': bodo, 'numba': numba, 'np': np}, bofi__rgmnv)
    overload_method = bofi__rgmnv['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        curcl__bkt = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            curcl__bkt)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        vvjox__utx = S_dt._obj
        gveb__ekcpx = bodo.hiframes.pd_series_ext.get_series_data(vvjox__utx)
        mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(vvjox__utx)
        umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(vvjox__utx)
        numba.parfors.parfor.init_prange()
        deep__pfxch = len(gveb__ekcpx)
        jji__wcch = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            deep__pfxch)
        for zoxx__xwx in numba.parfors.parfor.internal_prange(deep__pfxch):
            gtaz__itjrb = gveb__ekcpx[zoxx__xwx]
            znwc__rkg = bodo.utils.conversion.box_if_dt64(gtaz__itjrb)
            jji__wcch[zoxx__xwx] = datetime.date(znwc__rkg.year, znwc__rkg.
                month, znwc__rkg.day)
        return bodo.hiframes.pd_series_ext.init_series(jji__wcch,
            mrhk__vczh, umpcq__qaydy)
    return impl


def create_series_dt_df_output_overload(attr):

    def series_dt_df_output_overload(S_dt):
        if not (attr == 'components' and S_dt.stype.dtype == types.
            NPTimedelta('ns') or attr == 'isocalendar' and (S_dt.stype.
            dtype == types.NPDatetime('ns') or isinstance(S_dt.stype.dtype,
            PandasDatetimeTZDtype))):
            return
        aixu__pmk = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        if attr != 'isocalendar':
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{attr}')
        if attr == 'components':
            zlflq__vou = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            cyz__gmp = 'convert_numpy_timedelta64_to_pd_timedelta'
            ecbr__beh = 'np.empty(n, np.int64)'
            aahez__bbpl = attr
        elif attr == 'isocalendar':
            zlflq__vou = ['year', 'week', 'day']
            if aixu__pmk:
                cyz__gmp = None
            else:
                cyz__gmp = 'convert_datetime64_to_timestamp'
            ecbr__beh = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            aahez__bbpl = attr + '()'
        oxfn__dzzvb = 'def impl(S_dt):\n'
        oxfn__dzzvb += '    S = S_dt._obj\n'
        oxfn__dzzvb += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        oxfn__dzzvb += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        oxfn__dzzvb += '    numba.parfors.parfor.init_prange()\n'
        oxfn__dzzvb += '    n = len(arr)\n'
        for field in zlflq__vou:
            oxfn__dzzvb += '    {} = {}\n'.format(field, ecbr__beh)
        oxfn__dzzvb += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        oxfn__dzzvb += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in zlflq__vou:
            oxfn__dzzvb += (
                '            bodo.libs.array_kernels.setna({}, i)\n'.format
                (field))
        oxfn__dzzvb += '            continue\n'
        vshe__hei = '(' + '[i], '.join(zlflq__vou) + '[i])'
        if cyz__gmp:
            mpmgf__ypl = f'bodo.hiframes.pd_timestamp_ext.{cyz__gmp}(arr[i])'
        else:
            mpmgf__ypl = 'arr[i]'
        oxfn__dzzvb += f'        {vshe__hei} = {mpmgf__ypl}.{aahez__bbpl}\n'
        vpr__smui = '(' + ', '.join(zlflq__vou) + ')'
        oxfn__dzzvb += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, __col_name_meta_value_series_dt_df_output)
"""
            .format(vpr__smui))
        bofi__rgmnv = {}
        exec(oxfn__dzzvb, {'bodo': bodo, 'numba': numba, 'np': np,
            '__col_name_meta_value_series_dt_df_output': ColNamesMetaType(
            tuple(zlflq__vou))}, bofi__rgmnv)
        impl = bofi__rgmnv['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    ztgd__waei = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, zus__ifz in ztgd__waei:
        curcl__bkt = create_series_dt_df_output_overload(attr)
        zus__ifz(SeriesDatetimePropertiesType, attr, inline='always')(
            curcl__bkt)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        oxfn__dzzvb = 'def impl(S_dt):\n'
        oxfn__dzzvb += '    S = S_dt._obj\n'
        oxfn__dzzvb += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        oxfn__dzzvb += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        oxfn__dzzvb += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        oxfn__dzzvb += '    numba.parfors.parfor.init_prange()\n'
        oxfn__dzzvb += '    n = len(A)\n'
        oxfn__dzzvb += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        oxfn__dzzvb += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        oxfn__dzzvb += '        if bodo.libs.array_kernels.isna(A, i):\n'
        oxfn__dzzvb += '            bodo.libs.array_kernels.setna(B, i)\n'
        oxfn__dzzvb += '            continue\n'
        oxfn__dzzvb += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            oxfn__dzzvb += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            oxfn__dzzvb += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            oxfn__dzzvb += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            oxfn__dzzvb += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        oxfn__dzzvb += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        bofi__rgmnv = {}
        exec(oxfn__dzzvb, {'numba': numba, 'np': np, 'bodo': bodo}, bofi__rgmnv
            )
        impl = bofi__rgmnv['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        oxfn__dzzvb = 'def impl(S_dt):\n'
        oxfn__dzzvb += '    S = S_dt._obj\n'
        oxfn__dzzvb += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        oxfn__dzzvb += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        oxfn__dzzvb += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        oxfn__dzzvb += '    numba.parfors.parfor.init_prange()\n'
        oxfn__dzzvb += '    n = len(A)\n'
        if method == 'total_seconds':
            oxfn__dzzvb += '    B = np.empty(n, np.float64)\n'
        else:
            oxfn__dzzvb += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        oxfn__dzzvb += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        oxfn__dzzvb += '        if bodo.libs.array_kernels.isna(A, i):\n'
        oxfn__dzzvb += '            bodo.libs.array_kernels.setna(B, i)\n'
        oxfn__dzzvb += '            continue\n'
        oxfn__dzzvb += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            oxfn__dzzvb += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            oxfn__dzzvb += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            oxfn__dzzvb += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            oxfn__dzzvb += '    return B\n'
        bofi__rgmnv = {}
        exec(oxfn__dzzvb, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, bofi__rgmnv)
        impl = bofi__rgmnv['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        curcl__bkt = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(curcl__bkt)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        curcl__bkt = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            curcl__bkt)


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
        vvjox__utx = S_dt._obj
        fkjl__zet = bodo.hiframes.pd_series_ext.get_series_data(vvjox__utx)
        mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(vvjox__utx)
        umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(vvjox__utx)
        numba.parfors.parfor.init_prange()
        deep__pfxch = len(fkjl__zet)
        sdqpm__ogft = bodo.libs.str_arr_ext.pre_alloc_string_array(deep__pfxch,
            -1)
        for vsif__mimy in numba.parfors.parfor.internal_prange(deep__pfxch):
            if bodo.libs.array_kernels.isna(fkjl__zet, vsif__mimy):
                bodo.libs.array_kernels.setna(sdqpm__ogft, vsif__mimy)
                continue
            sdqpm__ogft[vsif__mimy] = bodo.utils.conversion.box_if_dt64(
                fkjl__zet[vsif__mimy]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(sdqpm__ogft,
            mrhk__vczh, umpcq__qaydy)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        vvjox__utx = S_dt._obj
        gvpfg__baro = get_series_data(vvjox__utx).tz_convert(tz)
        mrhk__vczh = get_series_index(vvjox__utx)
        umpcq__qaydy = get_series_name(vvjox__utx)
        return init_series(gvpfg__baro, mrhk__vczh, umpcq__qaydy)
    return impl


def create_timedelta_freq_overload(method):

    def freq_overload(S_dt, freq, ambiguous='raise', nonexistent='raise'):
        if S_dt.stype.dtype != types.NPTimedelta('ns'
            ) and S_dt.stype.dtype != types.NPDatetime('ns'
            ) and not isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype):
            return
        vqurn__kpsn = isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype)
        teg__hzr = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        tbgd__juf = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', teg__hzr, tbgd__juf,
            package_name='pandas', module_name='Series')
        oxfn__dzzvb = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        oxfn__dzzvb += '    S = S_dt._obj\n'
        oxfn__dzzvb += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        oxfn__dzzvb += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        oxfn__dzzvb += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        oxfn__dzzvb += '    numba.parfors.parfor.init_prange()\n'
        oxfn__dzzvb += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            oxfn__dzzvb += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        elif vqurn__kpsn:
            oxfn__dzzvb += """    B = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(n, tz_literal)
"""
        else:
            oxfn__dzzvb += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        oxfn__dzzvb += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        oxfn__dzzvb += '        if bodo.libs.array_kernels.isna(A, i):\n'
        oxfn__dzzvb += '            bodo.libs.array_kernels.setna(B, i)\n'
        oxfn__dzzvb += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            hgby__ddtk = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            fmglm__bepdu = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            hgby__ddtk = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            fmglm__bepdu = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        if vqurn__kpsn:
            oxfn__dzzvb += f'        B[i] = A[i].{method}(freq)\n'
        else:
            oxfn__dzzvb += ('        B[i] = {}({}(A[i]).{}(freq).value)\n'.
                format(fmglm__bepdu, hgby__ddtk, method))
        oxfn__dzzvb += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        bofi__rgmnv = {}
        bbmwn__hduqj = None
        if vqurn__kpsn:
            bbmwn__hduqj = S_dt.stype.dtype.tz
        exec(oxfn__dzzvb, {'numba': numba, 'np': np, 'bodo': bodo,
            'tz_literal': bbmwn__hduqj}, bofi__rgmnv)
        impl = bofi__rgmnv['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    uewwl__axm = ['ceil', 'floor', 'round']
    for method in uewwl__axm:
        curcl__bkt = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            curcl__bkt)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            qvpw__uhdd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vxopc__luip = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                rwig__pdmjo = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vxopc__luip)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                uufq__idw = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                gqbq__moq = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    uufq__idw)
                deep__pfxch = len(rwig__pdmjo)
                vvjox__utx = np.empty(deep__pfxch, timedelta64_dtype)
                cvwz__bqny = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qvpw__uhdd)
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    ldca__ggj = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        rwig__pdmjo[zoxx__xwx])
                    syi__ozbm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        gqbq__moq[zoxx__xwx])
                    if ldca__ggj == cvwz__bqny or syi__ozbm == cvwz__bqny:
                        grofb__godj = cvwz__bqny
                    else:
                        grofb__godj = op(ldca__ggj, syi__ozbm)
                    vvjox__utx[zoxx__xwx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        grofb__godj)
                return bodo.hiframes.pd_series_ext.init_series(vvjox__utx,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            qvpw__uhdd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                derdh__penxc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                gveb__ekcpx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    derdh__penxc)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                gqbq__moq = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                deep__pfxch = len(gveb__ekcpx)
                vvjox__utx = np.empty(deep__pfxch, dt64_dtype)
                cvwz__bqny = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qvpw__uhdd)
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    gllrt__futfz = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(gveb__ekcpx[zoxx__xwx]))
                    eim__xyits = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(gqbq__moq[zoxx__xwx]))
                    if gllrt__futfz == cvwz__bqny or eim__xyits == cvwz__bqny:
                        grofb__godj = cvwz__bqny
                    else:
                        grofb__godj = op(gllrt__futfz, eim__xyits)
                    vvjox__utx[zoxx__xwx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        grofb__godj)
                return bodo.hiframes.pd_series_ext.init_series(vvjox__utx,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            qvpw__uhdd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                derdh__penxc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                gveb__ekcpx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    derdh__penxc)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                gqbq__moq = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                deep__pfxch = len(gveb__ekcpx)
                vvjox__utx = np.empty(deep__pfxch, dt64_dtype)
                cvwz__bqny = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qvpw__uhdd)
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    gllrt__futfz = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(gveb__ekcpx[zoxx__xwx]))
                    eim__xyits = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(gqbq__moq[zoxx__xwx]))
                    if gllrt__futfz == cvwz__bqny or eim__xyits == cvwz__bqny:
                        grofb__godj = cvwz__bqny
                    else:
                        grofb__godj = op(gllrt__futfz, eim__xyits)
                    vvjox__utx[zoxx__xwx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        grofb__godj)
                return bodo.hiframes.pd_series_ext.init_series(vvjox__utx,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            qvpw__uhdd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                derdh__penxc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                gveb__ekcpx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    derdh__penxc)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                deep__pfxch = len(gveb__ekcpx)
                vvjox__utx = np.empty(deep__pfxch, timedelta64_dtype)
                cvwz__bqny = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qvpw__uhdd)
                mtavy__eymq = rhs.value
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    gllrt__futfz = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(gveb__ekcpx[zoxx__xwx]))
                    if gllrt__futfz == cvwz__bqny or mtavy__eymq == cvwz__bqny:
                        grofb__godj = cvwz__bqny
                    else:
                        grofb__godj = op(gllrt__futfz, mtavy__eymq)
                    vvjox__utx[zoxx__xwx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        grofb__godj)
                return bodo.hiframes.pd_series_ext.init_series(vvjox__utx,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            qvpw__uhdd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                derdh__penxc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                gveb__ekcpx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    derdh__penxc)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                deep__pfxch = len(gveb__ekcpx)
                vvjox__utx = np.empty(deep__pfxch, timedelta64_dtype)
                cvwz__bqny = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qvpw__uhdd)
                mtavy__eymq = lhs.value
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    gllrt__futfz = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(gveb__ekcpx[zoxx__xwx]))
                    if mtavy__eymq == cvwz__bqny or gllrt__futfz == cvwz__bqny:
                        grofb__godj = cvwz__bqny
                    else:
                        grofb__godj = op(mtavy__eymq, gllrt__futfz)
                    vvjox__utx[zoxx__xwx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        grofb__godj)
                return bodo.hiframes.pd_series_ext.init_series(vvjox__utx,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            qvpw__uhdd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                derdh__penxc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                gveb__ekcpx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    derdh__penxc)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                deep__pfxch = len(gveb__ekcpx)
                vvjox__utx = np.empty(deep__pfxch, dt64_dtype)
                cvwz__bqny = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qvpw__uhdd)
                blt__ohet = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                eim__xyits = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(blt__ohet))
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    gllrt__futfz = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(gveb__ekcpx[zoxx__xwx]))
                    if gllrt__futfz == cvwz__bqny or eim__xyits == cvwz__bqny:
                        grofb__godj = cvwz__bqny
                    else:
                        grofb__godj = op(gllrt__futfz, eim__xyits)
                    vvjox__utx[zoxx__xwx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        grofb__godj)
                return bodo.hiframes.pd_series_ext.init_series(vvjox__utx,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            qvpw__uhdd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                derdh__penxc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                gveb__ekcpx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    derdh__penxc)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                deep__pfxch = len(gveb__ekcpx)
                vvjox__utx = np.empty(deep__pfxch, dt64_dtype)
                cvwz__bqny = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qvpw__uhdd)
                blt__ohet = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                eim__xyits = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(blt__ohet))
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    gllrt__futfz = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(gveb__ekcpx[zoxx__xwx]))
                    if gllrt__futfz == cvwz__bqny or eim__xyits == cvwz__bqny:
                        grofb__godj = cvwz__bqny
                    else:
                        grofb__godj = op(gllrt__futfz, eim__xyits)
                    vvjox__utx[zoxx__xwx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        grofb__godj)
                return bodo.hiframes.pd_series_ext.init_series(vvjox__utx,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            qvpw__uhdd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                derdh__penxc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                gveb__ekcpx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    derdh__penxc)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                deep__pfxch = len(gveb__ekcpx)
                vvjox__utx = np.empty(deep__pfxch, timedelta64_dtype)
                cvwz__bqny = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qvpw__uhdd)
                hovlb__zqwew = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                gllrt__futfz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hovlb__zqwew)
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    ymz__yha = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        gveb__ekcpx[zoxx__xwx])
                    if ymz__yha == cvwz__bqny or gllrt__futfz == cvwz__bqny:
                        grofb__godj = cvwz__bqny
                    else:
                        grofb__godj = op(ymz__yha, gllrt__futfz)
                    vvjox__utx[zoxx__xwx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        grofb__godj)
                return bodo.hiframes.pd_series_ext.init_series(vvjox__utx,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            qvpw__uhdd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                derdh__penxc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                gveb__ekcpx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    derdh__penxc)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                deep__pfxch = len(gveb__ekcpx)
                vvjox__utx = np.empty(deep__pfxch, timedelta64_dtype)
                cvwz__bqny = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qvpw__uhdd)
                hovlb__zqwew = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                gllrt__futfz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hovlb__zqwew)
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    ymz__yha = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        gveb__ekcpx[zoxx__xwx])
                    if gllrt__futfz == cvwz__bqny or ymz__yha == cvwz__bqny:
                        grofb__godj = cvwz__bqny
                    else:
                        grofb__godj = op(gllrt__futfz, ymz__yha)
                    vvjox__utx[zoxx__xwx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        grofb__godj)
                return bodo.hiframes.pd_series_ext.init_series(vvjox__utx,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            qvpw__uhdd = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                gveb__ekcpx = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                deep__pfxch = len(gveb__ekcpx)
                vvjox__utx = np.empty(deep__pfxch, timedelta64_dtype)
                cvwz__bqny = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(qvpw__uhdd))
                blt__ohet = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                eim__xyits = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(blt__ohet))
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    ngddm__vvt = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(gveb__ekcpx[zoxx__xwx]))
                    if eim__xyits == cvwz__bqny or ngddm__vvt == cvwz__bqny:
                        grofb__godj = cvwz__bqny
                    else:
                        grofb__godj = op(ngddm__vvt, eim__xyits)
                    vvjox__utx[zoxx__xwx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        grofb__godj)
                return bodo.hiframes.pd_series_ext.init_series(vvjox__utx,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            qvpw__uhdd = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                gveb__ekcpx = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                deep__pfxch = len(gveb__ekcpx)
                vvjox__utx = np.empty(deep__pfxch, timedelta64_dtype)
                cvwz__bqny = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(qvpw__uhdd))
                blt__ohet = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                eim__xyits = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(blt__ohet))
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    ngddm__vvt = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(gveb__ekcpx[zoxx__xwx]))
                    if eim__xyits == cvwz__bqny or ngddm__vvt == cvwz__bqny:
                        grofb__godj = cvwz__bqny
                    else:
                        grofb__godj = op(eim__xyits, ngddm__vvt)
                    vvjox__utx[zoxx__xwx
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        grofb__godj)
                return bodo.hiframes.pd_series_ext.init_series(vvjox__utx,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            mhxlv__san = True
        else:
            mhxlv__san = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            qvpw__uhdd = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                gveb__ekcpx = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                deep__pfxch = len(gveb__ekcpx)
                jji__wcch = bodo.libs.bool_arr_ext.alloc_bool_array(deep__pfxch
                    )
                cvwz__bqny = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(qvpw__uhdd))
                qfac__jiban = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                kne__xzv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(qfac__jiban))
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    zqj__nvdm = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(gveb__ekcpx[zoxx__xwx]))
                    if zqj__nvdm == cvwz__bqny or kne__xzv == cvwz__bqny:
                        grofb__godj = mhxlv__san
                    else:
                        grofb__godj = op(zqj__nvdm, kne__xzv)
                    jji__wcch[zoxx__xwx] = grofb__godj
                return bodo.hiframes.pd_series_ext.init_series(jji__wcch,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            qvpw__uhdd = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                gveb__ekcpx = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                deep__pfxch = len(gveb__ekcpx)
                jji__wcch = bodo.libs.bool_arr_ext.alloc_bool_array(deep__pfxch
                    )
                cvwz__bqny = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(qvpw__uhdd))
                wcqt__blo = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                zqj__nvdm = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(wcqt__blo))
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    kne__xzv = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(gveb__ekcpx[zoxx__xwx]))
                    if zqj__nvdm == cvwz__bqny or kne__xzv == cvwz__bqny:
                        grofb__godj = mhxlv__san
                    else:
                        grofb__godj = op(zqj__nvdm, kne__xzv)
                    jji__wcch[zoxx__xwx] = grofb__godj
                return bodo.hiframes.pd_series_ext.init_series(jji__wcch,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            qvpw__uhdd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                derdh__penxc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                gveb__ekcpx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    derdh__penxc)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                deep__pfxch = len(gveb__ekcpx)
                jji__wcch = bodo.libs.bool_arr_ext.alloc_bool_array(deep__pfxch
                    )
                cvwz__bqny = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qvpw__uhdd)
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    zqj__nvdm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        gveb__ekcpx[zoxx__xwx])
                    if zqj__nvdm == cvwz__bqny or rhs.value == cvwz__bqny:
                        grofb__godj = mhxlv__san
                    else:
                        grofb__godj = op(zqj__nvdm, rhs.value)
                    jji__wcch[zoxx__xwx] = grofb__godj
                return bodo.hiframes.pd_series_ext.init_series(jji__wcch,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.
            pd_timestamp_tz_naive_type and bodo.hiframes.pd_series_ext.
            is_dt64_series_typ(rhs)):
            qvpw__uhdd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                derdh__penxc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                gveb__ekcpx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    derdh__penxc)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                deep__pfxch = len(gveb__ekcpx)
                jji__wcch = bodo.libs.bool_arr_ext.alloc_bool_array(deep__pfxch
                    )
                cvwz__bqny = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qvpw__uhdd)
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    kne__xzv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        gveb__ekcpx[zoxx__xwx])
                    if kne__xzv == cvwz__bqny or lhs.value == cvwz__bqny:
                        grofb__godj = mhxlv__san
                    else:
                        grofb__godj = op(lhs.value, kne__xzv)
                    jji__wcch[zoxx__xwx] = grofb__godj
                return bodo.hiframes.pd_series_ext.init_series(jji__wcch,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            qvpw__uhdd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                derdh__penxc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                gveb__ekcpx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    derdh__penxc)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                deep__pfxch = len(gveb__ekcpx)
                jji__wcch = bodo.libs.bool_arr_ext.alloc_bool_array(deep__pfxch
                    )
                cvwz__bqny = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qvpw__uhdd)
                venfz__jgwpt = (bodo.hiframes.pd_timestamp_ext.
                    parse_datetime_str(rhs))
                qow__qvjf = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    venfz__jgwpt)
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    zqj__nvdm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        gveb__ekcpx[zoxx__xwx])
                    if zqj__nvdm == cvwz__bqny or qow__qvjf == cvwz__bqny:
                        grofb__godj = mhxlv__san
                    else:
                        grofb__godj = op(zqj__nvdm, qow__qvjf)
                    jji__wcch[zoxx__xwx] = grofb__godj
                return bodo.hiframes.pd_series_ext.init_series(jji__wcch,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            qvpw__uhdd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                derdh__penxc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                gveb__ekcpx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    derdh__penxc)
                mrhk__vczh = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                umpcq__qaydy = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                deep__pfxch = len(gveb__ekcpx)
                jji__wcch = bodo.libs.bool_arr_ext.alloc_bool_array(deep__pfxch
                    )
                cvwz__bqny = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qvpw__uhdd)
                venfz__jgwpt = (bodo.hiframes.pd_timestamp_ext.
                    parse_datetime_str(lhs))
                qow__qvjf = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    venfz__jgwpt)
                for zoxx__xwx in numba.parfors.parfor.internal_prange(
                    deep__pfxch):
                    hovlb__zqwew = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(gveb__ekcpx[zoxx__xwx]))
                    if hovlb__zqwew == cvwz__bqny or qow__qvjf == cvwz__bqny:
                        grofb__godj = mhxlv__san
                    else:
                        grofb__godj = op(qow__qvjf, hovlb__zqwew)
                    jji__wcch[zoxx__xwx] = grofb__godj
                return bodo.hiframes.pd_series_ext.init_series(jji__wcch,
                    mrhk__vczh, umpcq__qaydy)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for cqbna__gcs in series_dt_unsupported_attrs:
        cnqyd__jfjf = 'Series.dt.' + cqbna__gcs
        overload_attribute(SeriesDatetimePropertiesType, cqbna__gcs)(
            create_unsupported_overload(cnqyd__jfjf))
    for kyum__hku in series_dt_unsupported_methods:
        cnqyd__jfjf = 'Series.dt.' + kyum__hku
        overload_method(SeriesDatetimePropertiesType, kyum__hku,
            no_unliteral=True)(create_unsupported_overload(cnqyd__jfjf))


_install_series_dt_unsupported()
