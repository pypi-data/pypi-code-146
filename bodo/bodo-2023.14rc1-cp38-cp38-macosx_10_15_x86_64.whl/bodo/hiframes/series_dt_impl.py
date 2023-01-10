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
        ilj__edzep = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(ilj__edzep)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        injiv__fgp = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, injiv__fgp)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        avule__bovcq, = args
        afzw__cvbps = signature.return_type
        ivzbr__vrlhy = cgutils.create_struct_proxy(afzw__cvbps)(context,
            builder)
        ivzbr__vrlhy.obj = avule__bovcq
        context.nrt.incref(builder, signature.args[0], avule__bovcq)
        return ivzbr__vrlhy._getvalue()
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
        zwq__ooe = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        lqnl__vvnhv = ['year', 'quarter', 'month', 'week', 'day', 'hour',
            'minute', 'second', 'microsecond']
        if field not in lqnl__vvnhv:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{field}')
        nhtcw__rar = 'def impl(S_dt):\n'
        nhtcw__rar += '    S = S_dt._obj\n'
        nhtcw__rar += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        nhtcw__rar += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        nhtcw__rar += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        nhtcw__rar += '    numba.parfors.parfor.init_prange()\n'
        nhtcw__rar += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            nhtcw__rar += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            nhtcw__rar += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        nhtcw__rar += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        nhtcw__rar += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        nhtcw__rar += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        nhtcw__rar += '            continue\n'
        if not zwq__ooe:
            nhtcw__rar += (
                '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
                )
            nhtcw__rar += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            if field == 'weekday':
                nhtcw__rar += '        out_arr[i] = ts.weekday()\n'
            else:
                nhtcw__rar += '        out_arr[i] = ts.' + field + '\n'
        else:
            nhtcw__rar += '        out_arr[i] = arr[i].{}\n'.format(field)
        nhtcw__rar += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        ydcp__fxvg = {}
        exec(nhtcw__rar, {'bodo': bodo, 'numba': numba, 'np': np}, ydcp__fxvg)
        impl = ydcp__fxvg['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        ueaum__ruf = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(ueaum__ruf)


_install_date_fields()


def create_date_method_overload(method):
    mseqd__hene = method in ['day_name', 'month_name']
    if mseqd__hene:
        nhtcw__rar = 'def overload_method(S_dt, locale=None):\n'
        nhtcw__rar += '    unsupported_args = dict(locale=locale)\n'
        nhtcw__rar += '    arg_defaults = dict(locale=None)\n'
        nhtcw__rar += '    bodo.utils.typing.check_unsupported_args(\n'
        nhtcw__rar += f"        'Series.dt.{method}',\n"
        nhtcw__rar += '        unsupported_args,\n'
        nhtcw__rar += '        arg_defaults,\n'
        nhtcw__rar += "        package_name='pandas',\n"
        nhtcw__rar += "        module_name='Series',\n"
        nhtcw__rar += '    )\n'
    else:
        nhtcw__rar = 'def overload_method(S_dt):\n'
        nhtcw__rar += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    nhtcw__rar += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    nhtcw__rar += '        return\n'
    if mseqd__hene:
        nhtcw__rar += '    def impl(S_dt, locale=None):\n'
    else:
        nhtcw__rar += '    def impl(S_dt):\n'
    nhtcw__rar += '        S = S_dt._obj\n'
    nhtcw__rar += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    nhtcw__rar += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    nhtcw__rar += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    nhtcw__rar += '        numba.parfors.parfor.init_prange()\n'
    nhtcw__rar += '        n = len(arr)\n'
    if mseqd__hene:
        nhtcw__rar += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        nhtcw__rar += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    nhtcw__rar += '        for i in numba.parfors.parfor.internal_prange(n):\n'
    nhtcw__rar += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    nhtcw__rar += '                bodo.libs.array_kernels.setna(out_arr, i)\n'
    nhtcw__rar += '                continue\n'
    nhtcw__rar += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    nhtcw__rar += f'            method_val = ts.{method}()\n'
    if mseqd__hene:
        nhtcw__rar += '            out_arr[i] = method_val\n'
    else:
        nhtcw__rar += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    nhtcw__rar += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    nhtcw__rar += '    return impl\n'
    ydcp__fxvg = {}
    exec(nhtcw__rar, {'bodo': bodo, 'numba': numba, 'np': np}, ydcp__fxvg)
    overload_method = ydcp__fxvg['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        ueaum__ruf = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            ueaum__ruf)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        dzerc__qwx = S_dt._obj
        mmtt__cvuvz = bodo.hiframes.pd_series_ext.get_series_data(dzerc__qwx)
        lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(dzerc__qwx)
        ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(dzerc__qwx)
        numba.parfors.parfor.init_prange()
        mwy__jrbdz = len(mmtt__cvuvz)
        icx__jxqv = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            mwy__jrbdz)
        for wep__qomme in numba.parfors.parfor.internal_prange(mwy__jrbdz):
            pvd__yieej = mmtt__cvuvz[wep__qomme]
            lgyb__pzrj = bodo.utils.conversion.box_if_dt64(pvd__yieej)
            icx__jxqv[wep__qomme] = datetime.date(lgyb__pzrj.year,
                lgyb__pzrj.month, lgyb__pzrj.day)
        return bodo.hiframes.pd_series_ext.init_series(icx__jxqv,
            lcvag__xric, ilj__edzep)
    return impl


def create_series_dt_df_output_overload(attr):

    def series_dt_df_output_overload(S_dt):
        if not (attr == 'components' and S_dt.stype.dtype == types.
            NPTimedelta('ns') or attr == 'isocalendar' and (S_dt.stype.
            dtype == types.NPDatetime('ns') or isinstance(S_dt.stype.dtype,
            PandasDatetimeTZDtype))):
            return
        zwq__ooe = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        if attr != 'isocalendar':
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{attr}')
        if attr == 'components':
            hnbt__oxau = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            tat__uga = 'convert_numpy_timedelta64_to_pd_timedelta'
            hxc__ckd = 'np.empty(n, np.int64)'
            jjc__sjcdh = attr
        elif attr == 'isocalendar':
            hnbt__oxau = ['year', 'week', 'day']
            if zwq__ooe:
                tat__uga = None
            else:
                tat__uga = 'convert_datetime64_to_timestamp'
            hxc__ckd = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            jjc__sjcdh = attr + '()'
        nhtcw__rar = 'def impl(S_dt):\n'
        nhtcw__rar += '    S = S_dt._obj\n'
        nhtcw__rar += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        nhtcw__rar += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        nhtcw__rar += '    numba.parfors.parfor.init_prange()\n'
        nhtcw__rar += '    n = len(arr)\n'
        for field in hnbt__oxau:
            nhtcw__rar += '    {} = {}\n'.format(field, hxc__ckd)
        nhtcw__rar += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        nhtcw__rar += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in hnbt__oxau:
            nhtcw__rar += ('            bodo.libs.array_kernels.setna({}, i)\n'
                .format(field))
        nhtcw__rar += '            continue\n'
        nzxf__tyyi = '(' + '[i], '.join(hnbt__oxau) + '[i])'
        if tat__uga:
            lxhz__jtd = f'bodo.hiframes.pd_timestamp_ext.{tat__uga}(arr[i])'
        else:
            lxhz__jtd = 'arr[i]'
        nhtcw__rar += f'        {nzxf__tyyi} = {lxhz__jtd}.{jjc__sjcdh}\n'
        eoh__tan = '(' + ', '.join(hnbt__oxau) + ')'
        nhtcw__rar += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, __col_name_meta_value_series_dt_df_output)
"""
            .format(eoh__tan))
        ydcp__fxvg = {}
        exec(nhtcw__rar, {'bodo': bodo, 'numba': numba, 'np': np,
            '__col_name_meta_value_series_dt_df_output': ColNamesMetaType(
            tuple(hnbt__oxau))}, ydcp__fxvg)
        impl = ydcp__fxvg['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    hgbs__dmy = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, tgjf__byxe in hgbs__dmy:
        ueaum__ruf = create_series_dt_df_output_overload(attr)
        tgjf__byxe(SeriesDatetimePropertiesType, attr, inline='always')(
            ueaum__ruf)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        nhtcw__rar = 'def impl(S_dt):\n'
        nhtcw__rar += '    S = S_dt._obj\n'
        nhtcw__rar += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        nhtcw__rar += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        nhtcw__rar += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        nhtcw__rar += '    numba.parfors.parfor.init_prange()\n'
        nhtcw__rar += '    n = len(A)\n'
        nhtcw__rar += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        nhtcw__rar += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        nhtcw__rar += '        if bodo.libs.array_kernels.isna(A, i):\n'
        nhtcw__rar += '            bodo.libs.array_kernels.setna(B, i)\n'
        nhtcw__rar += '            continue\n'
        nhtcw__rar += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            nhtcw__rar += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            nhtcw__rar += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            nhtcw__rar += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            nhtcw__rar += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        nhtcw__rar += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        ydcp__fxvg = {}
        exec(nhtcw__rar, {'numba': numba, 'np': np, 'bodo': bodo}, ydcp__fxvg)
        impl = ydcp__fxvg['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        nhtcw__rar = 'def impl(S_dt):\n'
        nhtcw__rar += '    S = S_dt._obj\n'
        nhtcw__rar += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        nhtcw__rar += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        nhtcw__rar += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        nhtcw__rar += '    numba.parfors.parfor.init_prange()\n'
        nhtcw__rar += '    n = len(A)\n'
        if method == 'total_seconds':
            nhtcw__rar += '    B = np.empty(n, np.float64)\n'
        else:
            nhtcw__rar += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        nhtcw__rar += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        nhtcw__rar += '        if bodo.libs.array_kernels.isna(A, i):\n'
        nhtcw__rar += '            bodo.libs.array_kernels.setna(B, i)\n'
        nhtcw__rar += '            continue\n'
        nhtcw__rar += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            nhtcw__rar += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            nhtcw__rar += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            nhtcw__rar += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            nhtcw__rar += '    return B\n'
        ydcp__fxvg = {}
        exec(nhtcw__rar, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, ydcp__fxvg)
        impl = ydcp__fxvg['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        ueaum__ruf = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(ueaum__ruf)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        ueaum__ruf = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            ueaum__ruf)


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
        dzerc__qwx = S_dt._obj
        cvmy__kbpu = bodo.hiframes.pd_series_ext.get_series_data(dzerc__qwx)
        lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(dzerc__qwx)
        ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(dzerc__qwx)
        numba.parfors.parfor.init_prange()
        mwy__jrbdz = len(cvmy__kbpu)
        qcmda__pgzx = bodo.libs.str_arr_ext.pre_alloc_string_array(mwy__jrbdz,
            -1)
        for tfgkx__pbqm in numba.parfors.parfor.internal_prange(mwy__jrbdz):
            if bodo.libs.array_kernels.isna(cvmy__kbpu, tfgkx__pbqm):
                bodo.libs.array_kernels.setna(qcmda__pgzx, tfgkx__pbqm)
                continue
            qcmda__pgzx[tfgkx__pbqm] = bodo.utils.conversion.box_if_dt64(
                cvmy__kbpu[tfgkx__pbqm]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(qcmda__pgzx,
            lcvag__xric, ilj__edzep)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        dzerc__qwx = S_dt._obj
        rjglv__qpez = get_series_data(dzerc__qwx).tz_convert(tz)
        lcvag__xric = get_series_index(dzerc__qwx)
        ilj__edzep = get_series_name(dzerc__qwx)
        return init_series(rjglv__qpez, lcvag__xric, ilj__edzep)
    return impl


def create_timedelta_freq_overload(method):

    def freq_overload(S_dt, freq, ambiguous='raise', nonexistent='raise'):
        if S_dt.stype.dtype != types.NPTimedelta('ns'
            ) and S_dt.stype.dtype != types.NPDatetime('ns'
            ) and not isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype):
            return
        duz__npp = isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype)
        ykht__xxn = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        tiab__erk = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', ykht__xxn, tiab__erk,
            package_name='pandas', module_name='Series')
        nhtcw__rar = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        nhtcw__rar += '    S = S_dt._obj\n'
        nhtcw__rar += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        nhtcw__rar += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        nhtcw__rar += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        nhtcw__rar += '    numba.parfors.parfor.init_prange()\n'
        nhtcw__rar += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            nhtcw__rar += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        elif duz__npp:
            nhtcw__rar += """    B = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(n, tz_literal)
"""
        else:
            nhtcw__rar += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        nhtcw__rar += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        nhtcw__rar += '        if bodo.libs.array_kernels.isna(A, i):\n'
        nhtcw__rar += '            bodo.libs.array_kernels.setna(B, i)\n'
        nhtcw__rar += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            lhn__qgk = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            uodxi__sfdx = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            lhn__qgk = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            uodxi__sfdx = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        if duz__npp:
            nhtcw__rar += f'        B[i] = A[i].{method}(freq)\n'
        else:
            nhtcw__rar += ('        B[i] = {}({}(A[i]).{}(freq).value)\n'.
                format(uodxi__sfdx, lhn__qgk, method))
        nhtcw__rar += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        ydcp__fxvg = {}
        brclj__lklih = None
        if duz__npp:
            brclj__lklih = S_dt.stype.dtype.tz
        exec(nhtcw__rar, {'numba': numba, 'np': np, 'bodo': bodo,
            'tz_literal': brclj__lklih}, ydcp__fxvg)
        impl = ydcp__fxvg['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    aukb__njj = ['ceil', 'floor', 'round']
    for method in aukb__njj:
        ueaum__ruf = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            ueaum__ruf)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            wehkl__pfv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                agnz__syqkp = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                hbrj__bhbm = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    agnz__syqkp)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                unz__svgs = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                xdewo__icvv = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    unz__svgs)
                mwy__jrbdz = len(hbrj__bhbm)
                dzerc__qwx = np.empty(mwy__jrbdz, timedelta64_dtype)
                kzwrr__dsxii = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wehkl__pfv)
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    kigz__efbc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(hbrj__bhbm[wep__qomme]))
                    jnetv__ofrz = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(xdewo__icvv[wep__qomme]))
                    if (kigz__efbc == kzwrr__dsxii or jnetv__ofrz ==
                        kzwrr__dsxii):
                        pjhk__zot = kzwrr__dsxii
                    else:
                        pjhk__zot = op(kigz__efbc, jnetv__ofrz)
                    dzerc__qwx[wep__qomme
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        pjhk__zot)
                return bodo.hiframes.pd_series_ext.init_series(dzerc__qwx,
                    lcvag__xric, ilj__edzep)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            wehkl__pfv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vgl__ogct = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                mmtt__cvuvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vgl__ogct)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xdewo__icvv = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                dzerc__qwx = np.empty(mwy__jrbdz, dt64_dtype)
                kzwrr__dsxii = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wehkl__pfv)
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    oqmx__oqyzh = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(mmtt__cvuvz[wep__qomme]))
                    abn__npodf = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(xdewo__icvv[wep__qomme]))
                    if (oqmx__oqyzh == kzwrr__dsxii or abn__npodf ==
                        kzwrr__dsxii):
                        pjhk__zot = kzwrr__dsxii
                    else:
                        pjhk__zot = op(oqmx__oqyzh, abn__npodf)
                    dzerc__qwx[wep__qomme
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        pjhk__zot)
                return bodo.hiframes.pd_series_ext.init_series(dzerc__qwx,
                    lcvag__xric, ilj__edzep)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            wehkl__pfv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vgl__ogct = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                mmtt__cvuvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vgl__ogct)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                xdewo__icvv = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                dzerc__qwx = np.empty(mwy__jrbdz, dt64_dtype)
                kzwrr__dsxii = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wehkl__pfv)
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    oqmx__oqyzh = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(mmtt__cvuvz[wep__qomme]))
                    abn__npodf = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(xdewo__icvv[wep__qomme]))
                    if (oqmx__oqyzh == kzwrr__dsxii or abn__npodf ==
                        kzwrr__dsxii):
                        pjhk__zot = kzwrr__dsxii
                    else:
                        pjhk__zot = op(oqmx__oqyzh, abn__npodf)
                    dzerc__qwx[wep__qomme
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        pjhk__zot)
                return bodo.hiframes.pd_series_ext.init_series(dzerc__qwx,
                    lcvag__xric, ilj__edzep)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            wehkl__pfv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vgl__ogct = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                mmtt__cvuvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vgl__ogct)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                dzerc__qwx = np.empty(mwy__jrbdz, timedelta64_dtype)
                kzwrr__dsxii = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wehkl__pfv)
                ymwhp__qbu = rhs.value
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    oqmx__oqyzh = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if (oqmx__oqyzh == kzwrr__dsxii or ymwhp__qbu ==
                        kzwrr__dsxii):
                        pjhk__zot = kzwrr__dsxii
                    else:
                        pjhk__zot = op(oqmx__oqyzh, ymwhp__qbu)
                    dzerc__qwx[wep__qomme
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        pjhk__zot)
                return bodo.hiframes.pd_series_ext.init_series(dzerc__qwx,
                    lcvag__xric, ilj__edzep)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            wehkl__pfv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vgl__ogct = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                mmtt__cvuvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vgl__ogct)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                dzerc__qwx = np.empty(mwy__jrbdz, timedelta64_dtype)
                kzwrr__dsxii = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wehkl__pfv)
                ymwhp__qbu = lhs.value
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    oqmx__oqyzh = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if (ymwhp__qbu == kzwrr__dsxii or oqmx__oqyzh ==
                        kzwrr__dsxii):
                        pjhk__zot = kzwrr__dsxii
                    else:
                        pjhk__zot = op(ymwhp__qbu, oqmx__oqyzh)
                    dzerc__qwx[wep__qomme
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        pjhk__zot)
                return bodo.hiframes.pd_series_ext.init_series(dzerc__qwx,
                    lcvag__xric, ilj__edzep)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            wehkl__pfv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vgl__ogct = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                mmtt__cvuvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vgl__ogct)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                dzerc__qwx = np.empty(mwy__jrbdz, dt64_dtype)
                kzwrr__dsxii = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wehkl__pfv)
                pdek__yfdw = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                abn__npodf = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(pdek__yfdw))
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    oqmx__oqyzh = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if (oqmx__oqyzh == kzwrr__dsxii or abn__npodf ==
                        kzwrr__dsxii):
                        pjhk__zot = kzwrr__dsxii
                    else:
                        pjhk__zot = op(oqmx__oqyzh, abn__npodf)
                    dzerc__qwx[wep__qomme
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        pjhk__zot)
                return bodo.hiframes.pd_series_ext.init_series(dzerc__qwx,
                    lcvag__xric, ilj__edzep)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            wehkl__pfv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vgl__ogct = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                mmtt__cvuvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vgl__ogct)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                dzerc__qwx = np.empty(mwy__jrbdz, dt64_dtype)
                kzwrr__dsxii = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wehkl__pfv)
                pdek__yfdw = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                abn__npodf = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(pdek__yfdw))
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    oqmx__oqyzh = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if (oqmx__oqyzh == kzwrr__dsxii or abn__npodf ==
                        kzwrr__dsxii):
                        pjhk__zot = kzwrr__dsxii
                    else:
                        pjhk__zot = op(oqmx__oqyzh, abn__npodf)
                    dzerc__qwx[wep__qomme
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        pjhk__zot)
                return bodo.hiframes.pd_series_ext.init_series(dzerc__qwx,
                    lcvag__xric, ilj__edzep)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            wehkl__pfv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vgl__ogct = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                mmtt__cvuvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vgl__ogct)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                dzerc__qwx = np.empty(mwy__jrbdz, timedelta64_dtype)
                kzwrr__dsxii = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wehkl__pfv)
                ucp__ithfx = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                oqmx__oqyzh = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ucp__ithfx)
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    hhueb__tsr = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if (hhueb__tsr == kzwrr__dsxii or oqmx__oqyzh ==
                        kzwrr__dsxii):
                        pjhk__zot = kzwrr__dsxii
                    else:
                        pjhk__zot = op(hhueb__tsr, oqmx__oqyzh)
                    dzerc__qwx[wep__qomme
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        pjhk__zot)
                return bodo.hiframes.pd_series_ext.init_series(dzerc__qwx,
                    lcvag__xric, ilj__edzep)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            wehkl__pfv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vgl__ogct = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                mmtt__cvuvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vgl__ogct)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                dzerc__qwx = np.empty(mwy__jrbdz, timedelta64_dtype)
                kzwrr__dsxii = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wehkl__pfv)
                ucp__ithfx = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                oqmx__oqyzh = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ucp__ithfx)
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    hhueb__tsr = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if (oqmx__oqyzh == kzwrr__dsxii or hhueb__tsr ==
                        kzwrr__dsxii):
                        pjhk__zot = kzwrr__dsxii
                    else:
                        pjhk__zot = op(oqmx__oqyzh, hhueb__tsr)
                    dzerc__qwx[wep__qomme
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        pjhk__zot)
                return bodo.hiframes.pd_series_ext.init_series(dzerc__qwx,
                    lcvag__xric, ilj__edzep)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            wehkl__pfv = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                mmtt__cvuvz = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                dzerc__qwx = np.empty(mwy__jrbdz, timedelta64_dtype)
                kzwrr__dsxii = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(wehkl__pfv))
                pdek__yfdw = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                abn__npodf = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(pdek__yfdw))
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    ntd__cui = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if abn__npodf == kzwrr__dsxii or ntd__cui == kzwrr__dsxii:
                        pjhk__zot = kzwrr__dsxii
                    else:
                        pjhk__zot = op(ntd__cui, abn__npodf)
                    dzerc__qwx[wep__qomme
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        pjhk__zot)
                return bodo.hiframes.pd_series_ext.init_series(dzerc__qwx,
                    lcvag__xric, ilj__edzep)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            wehkl__pfv = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                mmtt__cvuvz = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                dzerc__qwx = np.empty(mwy__jrbdz, timedelta64_dtype)
                kzwrr__dsxii = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(wehkl__pfv))
                pdek__yfdw = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                abn__npodf = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(pdek__yfdw))
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    ntd__cui = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if abn__npodf == kzwrr__dsxii or ntd__cui == kzwrr__dsxii:
                        pjhk__zot = kzwrr__dsxii
                    else:
                        pjhk__zot = op(abn__npodf, ntd__cui)
                    dzerc__qwx[wep__qomme
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        pjhk__zot)
                return bodo.hiframes.pd_series_ext.init_series(dzerc__qwx,
                    lcvag__xric, ilj__edzep)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            ard__cbrp = True
        else:
            ard__cbrp = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            wehkl__pfv = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                mmtt__cvuvz = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                icx__jxqv = bodo.libs.bool_arr_ext.alloc_bool_array(mwy__jrbdz)
                kzwrr__dsxii = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(wehkl__pfv))
                llac__cwxv = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                dqaau__skm = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(llac__cwxv))
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    vhnj__cozt = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if (vhnj__cozt == kzwrr__dsxii or dqaau__skm ==
                        kzwrr__dsxii):
                        pjhk__zot = ard__cbrp
                    else:
                        pjhk__zot = op(vhnj__cozt, dqaau__skm)
                    icx__jxqv[wep__qomme] = pjhk__zot
                return bodo.hiframes.pd_series_ext.init_series(icx__jxqv,
                    lcvag__xric, ilj__edzep)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            wehkl__pfv = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                mmtt__cvuvz = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                icx__jxqv = bodo.libs.bool_arr_ext.alloc_bool_array(mwy__jrbdz)
                kzwrr__dsxii = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(wehkl__pfv))
                ucm__ummv = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                vhnj__cozt = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ucm__ummv))
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    dqaau__skm = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if (vhnj__cozt == kzwrr__dsxii or dqaau__skm ==
                        kzwrr__dsxii):
                        pjhk__zot = ard__cbrp
                    else:
                        pjhk__zot = op(vhnj__cozt, dqaau__skm)
                    icx__jxqv[wep__qomme] = pjhk__zot
                return bodo.hiframes.pd_series_ext.init_series(icx__jxqv,
                    lcvag__xric, ilj__edzep)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            wehkl__pfv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vgl__ogct = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                mmtt__cvuvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vgl__ogct)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                icx__jxqv = bodo.libs.bool_arr_ext.alloc_bool_array(mwy__jrbdz)
                kzwrr__dsxii = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wehkl__pfv)
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    vhnj__cozt = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if vhnj__cozt == kzwrr__dsxii or rhs.value == kzwrr__dsxii:
                        pjhk__zot = ard__cbrp
                    else:
                        pjhk__zot = op(vhnj__cozt, rhs.value)
                    icx__jxqv[wep__qomme] = pjhk__zot
                return bodo.hiframes.pd_series_ext.init_series(icx__jxqv,
                    lcvag__xric, ilj__edzep)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.
            pd_timestamp_tz_naive_type and bodo.hiframes.pd_series_ext.
            is_dt64_series_typ(rhs)):
            wehkl__pfv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vgl__ogct = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                mmtt__cvuvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vgl__ogct)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                mwy__jrbdz = len(mmtt__cvuvz)
                icx__jxqv = bodo.libs.bool_arr_ext.alloc_bool_array(mwy__jrbdz)
                kzwrr__dsxii = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wehkl__pfv)
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    dqaau__skm = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if dqaau__skm == kzwrr__dsxii or lhs.value == kzwrr__dsxii:
                        pjhk__zot = ard__cbrp
                    else:
                        pjhk__zot = op(lhs.value, dqaau__skm)
                    icx__jxqv[wep__qomme] = pjhk__zot
                return bodo.hiframes.pd_series_ext.init_series(icx__jxqv,
                    lcvag__xric, ilj__edzep)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            wehkl__pfv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                vgl__ogct = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                mmtt__cvuvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vgl__ogct)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                mwy__jrbdz = len(mmtt__cvuvz)
                icx__jxqv = bodo.libs.bool_arr_ext.alloc_bool_array(mwy__jrbdz)
                kzwrr__dsxii = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wehkl__pfv)
                aaey__vcn = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                ymsy__wqrm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    aaey__vcn)
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    vhnj__cozt = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if (vhnj__cozt == kzwrr__dsxii or ymsy__wqrm ==
                        kzwrr__dsxii):
                        pjhk__zot = ard__cbrp
                    else:
                        pjhk__zot = op(vhnj__cozt, ymsy__wqrm)
                    icx__jxqv[wep__qomme] = pjhk__zot
                return bodo.hiframes.pd_series_ext.init_series(icx__jxqv,
                    lcvag__xric, ilj__edzep)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            wehkl__pfv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                vgl__ogct = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                mmtt__cvuvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vgl__ogct)
                lcvag__xric = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ilj__edzep = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                mwy__jrbdz = len(mmtt__cvuvz)
                icx__jxqv = bodo.libs.bool_arr_ext.alloc_bool_array(mwy__jrbdz)
                kzwrr__dsxii = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wehkl__pfv)
                aaey__vcn = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                ymsy__wqrm = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    aaey__vcn)
                for wep__qomme in numba.parfors.parfor.internal_prange(
                    mwy__jrbdz):
                    ucp__ithfx = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(mmtt__cvuvz[wep__qomme]))
                    if (ucp__ithfx == kzwrr__dsxii or ymsy__wqrm ==
                        kzwrr__dsxii):
                        pjhk__zot = ard__cbrp
                    else:
                        pjhk__zot = op(ymsy__wqrm, ucp__ithfx)
                    icx__jxqv[wep__qomme] = pjhk__zot
                return bodo.hiframes.pd_series_ext.init_series(icx__jxqv,
                    lcvag__xric, ilj__edzep)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for rdj__lmgi in series_dt_unsupported_attrs:
        ggorm__knp = 'Series.dt.' + rdj__lmgi
        overload_attribute(SeriesDatetimePropertiesType, rdj__lmgi)(
            create_unsupported_overload(ggorm__knp))
    for bstu__fkekz in series_dt_unsupported_methods:
        ggorm__knp = 'Series.dt.' + bstu__fkekz
        overload_method(SeriesDatetimePropertiesType, bstu__fkekz,
            no_unliteral=True)(create_unsupported_overload(ggorm__knp))


_install_series_dt_unsupported()
