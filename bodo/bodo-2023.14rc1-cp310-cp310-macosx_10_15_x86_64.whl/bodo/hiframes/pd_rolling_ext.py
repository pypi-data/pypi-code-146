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
            qbp__qpcz = 'Series'
        else:
            qbp__qpcz = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{qbp__qpcz}.rolling()')
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
        kwknz__pili = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, kwknz__pili)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    yefaq__svy = dict(win_type=win_type, axis=axis, closed=closed)
    euj__grcm = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', yefaq__svy, euj__grcm,
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
    yefaq__svy = dict(win_type=win_type, axis=axis, closed=closed)
    euj__grcm = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', yefaq__svy, euj__grcm,
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
        qtlj__lak, mdbp__btvhx, jmgi__tywz, mnn__cef, olugl__kbhv = args
        pegag__luug = signature.return_type
        qsut__apj = cgutils.create_struct_proxy(pegag__luug)(context, builder)
        qsut__apj.obj = qtlj__lak
        qsut__apj.window = mdbp__btvhx
        qsut__apj.min_periods = jmgi__tywz
        qsut__apj.center = mnn__cef
        context.nrt.incref(builder, signature.args[0], qtlj__lak)
        context.nrt.incref(builder, signature.args[1], mdbp__btvhx)
        context.nrt.incref(builder, signature.args[2], jmgi__tywz)
        context.nrt.incref(builder, signature.args[3], mnn__cef)
        return qsut__apj._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    pegag__luug = RollingType(obj_type, window_type, on, selection, False)
    return pegag__luug(obj_type, window_type, min_periods_type, center_type,
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
    ihe__urg = not isinstance(rolling.window_type, types.Integer)
    oluxw__fda = 'variable' if ihe__urg else 'fixed'
    qvrgq__jme = 'None'
    if ihe__urg:
        qvrgq__jme = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    phyqs__sids = []
    ufrzl__vkr = 'on_arr, ' if ihe__urg else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{oluxw__fda}(bodo.hiframes.pd_series_ext.get_series_data(df), {ufrzl__vkr}index_arr, window, minp, center, func, raw)'
            , qvrgq__jme, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    hmqg__pikog = rolling.obj_type.data
    out_cols = []
    for gcbq__nib in rolling.selection:
        ytie__lvaba = rolling.obj_type.columns.index(gcbq__nib)
        if gcbq__nib == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            sxrrj__zgrm = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ytie__lvaba})'
                )
            out_cols.append(gcbq__nib)
        else:
            if not isinstance(hmqg__pikog[ytie__lvaba].dtype, (types.
                Boolean, types.Number)):
                continue
            sxrrj__zgrm = (
                f'bodo.hiframes.rolling.rolling_{oluxw__fda}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ytie__lvaba}), {ufrzl__vkr}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(gcbq__nib)
        phyqs__sids.append(sxrrj__zgrm)
    return ', '.join(phyqs__sids), qvrgq__jme, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    yefaq__svy = dict(engine=engine, engine_kwargs=engine_kwargs, args=args,
        kwargs=kwargs)
    euj__grcm = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', yefaq__svy, euj__grcm,
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
    yefaq__svy = dict(win_type=win_type, axis=axis, closed=closed, method=
        method)
    euj__grcm = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', yefaq__svy, euj__grcm,
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
        sfvvk__xft = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        uwjs__lbw = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{jmz__yyaj}'" if
                isinstance(jmz__yyaj, str) else f'{jmz__yyaj}' for
                jmz__yyaj in rolling.selection if jmz__yyaj != rolling.on))
        tnmjm__sirh = dwesb__mczvg = ''
        if fname == 'apply':
            tnmjm__sirh = 'func, raw, args, kwargs'
            dwesb__mczvg = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            tnmjm__sirh = dwesb__mczvg = 'other, pairwise'
        if fname == 'cov':
            tnmjm__sirh = dwesb__mczvg = 'other, pairwise, ddof'
        gukq__qpp = (
            f'lambda df, window, minp, center, {tnmjm__sirh}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {uwjs__lbw}){selection}.{fname}({dwesb__mczvg})'
            )
        sfvvk__xft += f"""  return rolling.obj.apply({gukq__qpp}, rolling.window, rolling.min_periods, rolling.center, {tnmjm__sirh})
"""
        zpnye__elcrn = {}
        exec(sfvvk__xft, {'bodo': bodo}, zpnye__elcrn)
        impl = zpnye__elcrn['impl']
        return impl
    fceeg__voudo = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if fceeg__voudo else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if fceeg__voudo else rolling.obj_type.columns
        other_cols = None if fceeg__voudo else other.columns
        phyqs__sids, qvrgq__jme = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        phyqs__sids, qvrgq__jme, out_cols = _gen_df_rolling_out_data(rolling)
    ydz__foau = fceeg__voudo or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    dfr__hnh = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    dfr__hnh += '  df = rolling.obj\n'
    dfr__hnh += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if fceeg__voudo else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    qbp__qpcz = 'None'
    if fceeg__voudo:
        qbp__qpcz = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif ydz__foau:
        gcbq__nib = (set(out_cols) - set([rolling.on])).pop()
        qbp__qpcz = f"'{gcbq__nib}'" if isinstance(gcbq__nib, str) else str(
            gcbq__nib)
    dfr__hnh += f'  name = {qbp__qpcz}\n'
    dfr__hnh += '  window = rolling.window\n'
    dfr__hnh += '  center = rolling.center\n'
    dfr__hnh += '  minp = rolling.min_periods\n'
    dfr__hnh += f'  on_arr = {qvrgq__jme}\n'
    if fname == 'apply':
        dfr__hnh += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        dfr__hnh += f"  func = '{fname}'\n"
        dfr__hnh += f'  index_arr = None\n'
        dfr__hnh += f'  raw = False\n'
    if ydz__foau:
        dfr__hnh += (
            f'  return bodo.hiframes.pd_series_ext.init_series({phyqs__sids}, index, name)'
            )
        zpnye__elcrn = {}
        sfoq__vqb = {'bodo': bodo}
        exec(dfr__hnh, sfoq__vqb, zpnye__elcrn)
        impl = zpnye__elcrn['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(dfr__hnh, out_cols,
        phyqs__sids)


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
        gngh__vqhep = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(gngh__vqhep)


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
    kol__dgqvd = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(kol__dgqvd) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    ihe__urg = not isinstance(window_type, types.Integer)
    qvrgq__jme = 'None'
    if ihe__urg:
        qvrgq__jme = 'bodo.utils.conversion.index_to_array(index)'
    ufrzl__vkr = 'on_arr, ' if ihe__urg else ''
    phyqs__sids = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {ufrzl__vkr}window, minp, center)'
            , qvrgq__jme)
    for gcbq__nib in out_cols:
        if gcbq__nib in df_cols and gcbq__nib in other_cols:
            bocjz__mdxvh = df_cols.index(gcbq__nib)
            fap__qxnya = other_cols.index(gcbq__nib)
            sxrrj__zgrm = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {bocjz__mdxvh}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {fap__qxnya}), {ufrzl__vkr}window, minp, center)'
                )
        else:
            sxrrj__zgrm = 'np.full(len(df), np.nan)'
        phyqs__sids.append(sxrrj__zgrm)
    return ', '.join(phyqs__sids), qvrgq__jme


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    wkahm__evz = {'pairwise': pairwise, 'ddof': ddof}
    ooxhf__abvpg = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        wkahm__evz, ooxhf__abvpg, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    wkahm__evz = {'ddof': ddof, 'pairwise': pairwise}
    ooxhf__abvpg = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        wkahm__evz, ooxhf__abvpg, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, evfqd__sdber = args
        if isinstance(rolling, RollingType):
            kol__dgqvd = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(evfqd__sdber, (tuple, list)):
                if len(set(evfqd__sdber).difference(set(kol__dgqvd))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(evfqd__sdber).difference(set(kol__dgqvd))))
                selection = list(evfqd__sdber)
            else:
                if evfqd__sdber not in kol__dgqvd:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(evfqd__sdber))
                selection = [evfqd__sdber]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            foto__ihcy = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(foto__ihcy, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        kol__dgqvd = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            kol__dgqvd = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            kol__dgqvd = rolling.obj_type.columns
        if attr in kol__dgqvd:
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
    zhh__omobx = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    hmqg__pikog = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in zhh__omobx):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        enh__act = hmqg__pikog[zhh__omobx.index(get_literal_value(on))]
        if not isinstance(enh__act, types.Array
            ) or enh__act.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(ezwxs__tpt.dtype, (types.Boolean, types.Number)) for
        ezwxs__tpt in hmqg__pikog):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
