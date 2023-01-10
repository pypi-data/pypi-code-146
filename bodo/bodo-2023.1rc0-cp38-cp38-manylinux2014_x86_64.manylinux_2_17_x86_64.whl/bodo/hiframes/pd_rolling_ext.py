"""typing for rolling window functions
"""
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model
import bodo
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.hiframes.pd_groupby_ext import DataFrameGroupByType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.rolling import supported_rolling_funcs, unsupported_rolling_methods
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, get_literal_value, is_const_func_type, is_literal_type, is_overload_bool, is_overload_constant_str, is_overload_int, is_overload_none, raise_bodo_error


class RollingType(types.Type):

    def __init__(self, obj_type, window_type, on, selection,
        explicit_select=False, series_select=False):
        if isinstance(obj_type, bodo.SeriesType):
            qrqk__kurum = 'Series'
        else:
            qrqk__kurum = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{qrqk__kurum}.rolling()')
        self.obj_type = obj_type
        self.window_type = window_type
        self.on = on
        self.selection = selection
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(RollingType, self).__init__(name=
            f'RollingType({obj_type}, {window_type}, {on}, {selection}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return RollingType(self.obj_type, self.window_type, self.on, self.
            selection, self.explicit_select, self.series_select)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(RollingType)
class RollingModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        riw__buvw = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, riw__buvw)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    fchyi__nctgz = dict(win_type=win_type, axis=axis, closed=closed)
    igwo__tizl = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', fchyi__nctgz, igwo__tizl,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(df, window, min_periods, center, on)

    def impl(df, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(df, window,
            min_periods, center, on)
    return impl


@overload_method(SeriesType, 'rolling', inline='always', no_unliteral=True)
def overload_series_rolling(S, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    fchyi__nctgz = dict(win_type=win_type, axis=axis, closed=closed)
    igwo__tizl = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', fchyi__nctgz, igwo__tizl,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(S, window, min_periods, center, on)

    def impl(S, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(S, window,
            min_periods, center, on)
    return impl


@intrinsic
def init_rolling(typingctx, obj_type, window_type, min_periods_type,
    center_type, on_type=None):

    def codegen(context, builder, signature, args):
        xjo__xceai, wzdmd__rub, qfzl__wtrrv, njas__hyey, fwbh__gnfg = args
        fshje__sbfm = signature.return_type
        yjg__obnrp = cgutils.create_struct_proxy(fshje__sbfm)(context, builder)
        yjg__obnrp.obj = xjo__xceai
        yjg__obnrp.window = wzdmd__rub
        yjg__obnrp.min_periods = qfzl__wtrrv
        yjg__obnrp.center = njas__hyey
        context.nrt.incref(builder, signature.args[0], xjo__xceai)
        context.nrt.incref(builder, signature.args[1], wzdmd__rub)
        context.nrt.incref(builder, signature.args[2], qfzl__wtrrv)
        context.nrt.incref(builder, signature.args[3], njas__hyey)
        return yjg__obnrp._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    fshje__sbfm = RollingType(obj_type, window_type, on, selection, False)
    return fshje__sbfm(obj_type, window_type, min_periods_type, center_type,
        on_type), codegen


def _handle_default_min_periods(min_periods, window):
    return min_periods


@overload(_handle_default_min_periods)
def overload_handle_default_min_periods(min_periods, window):
    if is_overload_none(min_periods):
        if isinstance(window, types.Integer):
            return lambda min_periods, window: window
        else:
            return lambda min_periods, window: 1
    else:
        return lambda min_periods, window: min_periods


def _gen_df_rolling_out_data(rolling):
    gidh__ooe = not isinstance(rolling.window_type, types.Integer)
    hevpn__ndkpj = 'variable' if gidh__ooe else 'fixed'
    aus__pxyho = 'None'
    if gidh__ooe:
        aus__pxyho = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    rolja__ouas = []
    pcqf__ihxb = 'on_arr, ' if gidh__ooe else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{hevpn__ndkpj}(bodo.hiframes.pd_series_ext.get_series_data(df), {pcqf__ihxb}index_arr, window, minp, center, func, raw)'
            , aus__pxyho, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    pkh__fhsnw = rolling.obj_type.data
    out_cols = []
    for rzka__fgn in rolling.selection:
        tvv__tgrn = rolling.obj_type.columns.index(rzka__fgn)
        if rzka__fgn == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            jwk__yxc = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {tvv__tgrn})'
                )
            out_cols.append(rzka__fgn)
        else:
            if not isinstance(pkh__fhsnw[tvv__tgrn].dtype, (types.Boolean,
                types.Number)):
                continue
            jwk__yxc = (
                f'bodo.hiframes.rolling.rolling_{hevpn__ndkpj}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {tvv__tgrn}), {pcqf__ihxb}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(rzka__fgn)
        rolja__ouas.append(jwk__yxc)
    return ', '.join(rolja__ouas), aus__pxyho, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    fchyi__nctgz = dict(engine=engine, engine_kwargs=engine_kwargs, args=
        args, kwargs=kwargs)
    igwo__tizl = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', fchyi__nctgz, igwo__tizl,
        package_name='pandas', module_name='Window')
    if not is_const_func_type(func):
        raise BodoError(
            f"Rolling.apply(): 'func' parameter must be a function, not {func} (builtin functions not supported yet)."
            )
    if not is_overload_bool(raw):
        raise BodoError(
            f"Rolling.apply(): 'raw' parameter must be bool, not {raw}.")
    return _gen_rolling_impl(rolling, 'apply')


@overload_method(DataFrameGroupByType, 'rolling', inline='always',
    no_unliteral=True)
def groupby_rolling_overload(grp, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None, method='single'):
    fchyi__nctgz = dict(win_type=win_type, axis=axis, closed=closed, method
        =method)
    igwo__tizl = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', fchyi__nctgz, igwo__tizl,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(grp, window, min_periods, center, on)

    def _impl(grp, window, min_periods=None, center=False, win_type=None,
        on=None, axis=0, closed=None, method='single'):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(grp, window,
            min_periods, center, on)
    return _impl


def _gen_rolling_impl(rolling, fname, other=None):
    if isinstance(rolling.obj_type, DataFrameGroupByType):
        ridce__woa = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        pgc__midv = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{xdwy__ttv}'" if
                isinstance(xdwy__ttv, str) else f'{xdwy__ttv}' for
                xdwy__ttv in rolling.selection if xdwy__ttv != rolling.on))
        lbat__epma = qie__ojg = ''
        if fname == 'apply':
            lbat__epma = 'func, raw, args, kwargs'
            qie__ojg = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            lbat__epma = qie__ojg = 'other, pairwise'
        if fname == 'cov':
            lbat__epma = qie__ojg = 'other, pairwise, ddof'
        thrkr__soqv = (
            f'lambda df, window, minp, center, {lbat__epma}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {pgc__midv}){selection}.{fname}({qie__ojg})'
            )
        ridce__woa += f"""  return rolling.obj.apply({thrkr__soqv}, rolling.window, rolling.min_periods, rolling.center, {lbat__epma})
"""
        oyw__yrrj = {}
        exec(ridce__woa, {'bodo': bodo}, oyw__yrrj)
        impl = oyw__yrrj['impl']
        return impl
    cpa__cxf = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if cpa__cxf else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if cpa__cxf else rolling.obj_type.columns
        other_cols = None if cpa__cxf else other.columns
        rolja__ouas, aus__pxyho = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        rolja__ouas, aus__pxyho, out_cols = _gen_df_rolling_out_data(rolling)
    std__tekqr = cpa__cxf or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    awim__fna = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    awim__fna += '  df = rolling.obj\n'
    awim__fna += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if cpa__cxf else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    qrqk__kurum = 'None'
    if cpa__cxf:
        qrqk__kurum = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif std__tekqr:
        rzka__fgn = (set(out_cols) - set([rolling.on])).pop()
        qrqk__kurum = f"'{rzka__fgn}'" if isinstance(rzka__fgn, str) else str(
            rzka__fgn)
    awim__fna += f'  name = {qrqk__kurum}\n'
    awim__fna += '  window = rolling.window\n'
    awim__fna += '  center = rolling.center\n'
    awim__fna += '  minp = rolling.min_periods\n'
    awim__fna += f'  on_arr = {aus__pxyho}\n'
    if fname == 'apply':
        awim__fna += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        awim__fna += f"  func = '{fname}'\n"
        awim__fna += f'  index_arr = None\n'
        awim__fna += f'  raw = False\n'
    if std__tekqr:
        awim__fna += (
            f'  return bodo.hiframes.pd_series_ext.init_series({rolja__ouas}, index, name)'
            )
        oyw__yrrj = {}
        oszpa__cfee = {'bodo': bodo}
        exec(awim__fna, oszpa__cfee, oyw__yrrj)
        impl = oyw__yrrj['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(awim__fna, out_cols,
        rolja__ouas)


def _get_rolling_func_args(fname):
    if fname == 'apply':
        return (
            'func, raw=False, engine=None, engine_kwargs=None, args=None, kwargs=None\n'
            )
    elif fname == 'corr':
        return 'other=None, pairwise=None, ddof=1\n'
    elif fname == 'cov':
        return 'other=None, pairwise=None, ddof=1\n'
    return ''


def create_rolling_overload(fname):

    def overload_rolling_func(rolling):
        return _gen_rolling_impl(rolling, fname)
    return overload_rolling_func


def _install_rolling_methods():
    for fname in supported_rolling_funcs:
        if fname in ('apply', 'corr', 'cov'):
            continue
        wbrgn__rjny = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(wbrgn__rjny)


def _install_rolling_unsupported_methods():
    for fname in unsupported_rolling_methods:
        overload_method(RollingType, fname, no_unliteral=True)(
            create_unsupported_overload(
            f'pandas.core.window.rolling.Rolling.{fname}()'))


_install_rolling_methods()
_install_rolling_unsupported_methods()


def _get_corr_cov_out_cols(rolling, other, func_name):
    if not isinstance(other, DataFrameType):
        raise_bodo_error(
            f"DataFrame.rolling.{func_name}(): requires providing a DataFrame for 'other'"
            )
    lunv__guw = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(lunv__guw) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    gidh__ooe = not isinstance(window_type, types.Integer)
    aus__pxyho = 'None'
    if gidh__ooe:
        aus__pxyho = 'bodo.utils.conversion.index_to_array(index)'
    pcqf__ihxb = 'on_arr, ' if gidh__ooe else ''
    rolja__ouas = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {pcqf__ihxb}window, minp, center)'
            , aus__pxyho)
    for rzka__fgn in out_cols:
        if rzka__fgn in df_cols and rzka__fgn in other_cols:
            dcq__vhbq = df_cols.index(rzka__fgn)
            kfnkr__qiok = other_cols.index(rzka__fgn)
            jwk__yxc = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {dcq__vhbq}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {kfnkr__qiok}), {pcqf__ihxb}window, minp, center)'
                )
        else:
            jwk__yxc = 'np.full(len(df), np.nan)'
        rolja__ouas.append(jwk__yxc)
    return ', '.join(rolja__ouas), aus__pxyho


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    lacl__uou = {'pairwise': pairwise, 'ddof': ddof}
    xlft__qol = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        lacl__uou, xlft__qol, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    lacl__uou = {'ddof': ddof, 'pairwise': pairwise}
    xlft__qol = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        lacl__uou, xlft__qol, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, epmi__zjewy = args
        if isinstance(rolling, RollingType):
            lunv__guw = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(epmi__zjewy, (tuple, list)):
                if len(set(epmi__zjewy).difference(set(lunv__guw))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(epmi__zjewy).difference(set(lunv__guw))))
                selection = list(epmi__zjewy)
            else:
                if epmi__zjewy not in lunv__guw:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(epmi__zjewy))
                selection = [epmi__zjewy]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            bfh__rxhh = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(bfh__rxhh, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        lunv__guw = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            lunv__guw = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            lunv__guw = rolling.obj_type.columns
        if attr in lunv__guw:
            return RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, (attr,) if rolling.on is None else (attr,
                rolling.on), True, True)


def _validate_rolling_args(obj, window, min_periods, center, on):
    assert isinstance(obj, (SeriesType, DataFrameType, DataFrameGroupByType)
        ), 'invalid rolling obj'
    func_name = 'Series' if isinstance(obj, SeriesType
        ) else 'DataFrame' if isinstance(obj, DataFrameType
        ) else 'DataFrameGroupBy'
    if not (is_overload_int(window) or is_overload_constant_str(window) or 
        window == bodo.string_type or window in (pd_timedelta_type,
        datetime_timedelta_type)):
        raise BodoError(
            f"{func_name}.rolling(): 'window' should be int or time offset (str, pd.Timedelta, datetime.timedelta), not {window}"
            )
    if not is_overload_bool(center):
        raise BodoError(
            f'{func_name}.rolling(): center must be a boolean, not {center}')
    if not (is_overload_none(min_periods) or isinstance(min_periods, types.
        Integer)):
        raise BodoError(
            f'{func_name}.rolling(): min_periods must be an integer, not {min_periods}'
            )
    if isinstance(obj, SeriesType) and not is_overload_none(on):
        raise BodoError(
            f"{func_name}.rolling(): 'on' not supported for Series yet (can use a DataFrame instead)."
            )
    sta__mbjh = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    pkh__fhsnw = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in sta__mbjh):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        wbdl__nzwun = pkh__fhsnw[sta__mbjh.index(get_literal_value(on))]
        if not isinstance(wbdl__nzwun, types.Array
            ) or wbdl__nzwun.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(edzv__ngf.dtype, (types.Boolean, types.Number)) for
        edzv__ngf in pkh__fhsnw):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
