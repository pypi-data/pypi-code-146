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
            hxgpd__teqks = 'Series'
        else:
            hxgpd__teqks = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{hxgpd__teqks}.rolling()')
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
        kuzbw__bftz = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, kuzbw__bftz)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    fpzgv__ahf = dict(win_type=win_type, axis=axis, closed=closed)
    eyy__frnwq = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', fpzgv__ahf, eyy__frnwq,
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
    fpzgv__ahf = dict(win_type=win_type, axis=axis, closed=closed)
    eyy__frnwq = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', fpzgv__ahf, eyy__frnwq,
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
        wfwi__emsli, ouyd__crda, oir__prvhz, nvgo__botio, ghjzi__kxggs = args
        prxzp__hfm = signature.return_type
        kamv__adwc = cgutils.create_struct_proxy(prxzp__hfm)(context, builder)
        kamv__adwc.obj = wfwi__emsli
        kamv__adwc.window = ouyd__crda
        kamv__adwc.min_periods = oir__prvhz
        kamv__adwc.center = nvgo__botio
        context.nrt.incref(builder, signature.args[0], wfwi__emsli)
        context.nrt.incref(builder, signature.args[1], ouyd__crda)
        context.nrt.incref(builder, signature.args[2], oir__prvhz)
        context.nrt.incref(builder, signature.args[3], nvgo__botio)
        return kamv__adwc._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    prxzp__hfm = RollingType(obj_type, window_type, on, selection, False)
    return prxzp__hfm(obj_type, window_type, min_periods_type, center_type,
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
    abw__uadm = not isinstance(rolling.window_type, types.Integer)
    ajqy__ovbyg = 'variable' if abw__uadm else 'fixed'
    rreez__qkp = 'None'
    if abw__uadm:
        rreez__qkp = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    fpf__tbxl = []
    emt__swvtk = 'on_arr, ' if abw__uadm else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{ajqy__ovbyg}(bodo.hiframes.pd_series_ext.get_series_data(df), {emt__swvtk}index_arr, window, minp, center, func, raw)'
            , rreez__qkp, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    crm__otc = rolling.obj_type.data
    out_cols = []
    for jgwj__vlsnj in rolling.selection:
        fjfdu__lde = rolling.obj_type.columns.index(jgwj__vlsnj)
        if jgwj__vlsnj == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            txvrs__pgyw = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {fjfdu__lde})'
                )
            out_cols.append(jgwj__vlsnj)
        else:
            if not isinstance(crm__otc[fjfdu__lde].dtype, (types.Boolean,
                types.Number)):
                continue
            txvrs__pgyw = (
                f'bodo.hiframes.rolling.rolling_{ajqy__ovbyg}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {fjfdu__lde}), {emt__swvtk}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(jgwj__vlsnj)
        fpf__tbxl.append(txvrs__pgyw)
    return ', '.join(fpf__tbxl), rreez__qkp, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    fpzgv__ahf = dict(engine=engine, engine_kwargs=engine_kwargs, args=args,
        kwargs=kwargs)
    eyy__frnwq = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', fpzgv__ahf, eyy__frnwq,
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
    fpzgv__ahf = dict(win_type=win_type, axis=axis, closed=closed, method=
        method)
    eyy__frnwq = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', fpzgv__ahf, eyy__frnwq,
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
        khkzh__gjl = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        mav__zez = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{stvh__bzu}'" if
                isinstance(stvh__bzu, str) else f'{stvh__bzu}' for
                stvh__bzu in rolling.selection if stvh__bzu != rolling.on))
        zybsd__mdfd = fetg__xoyoy = ''
        if fname == 'apply':
            zybsd__mdfd = 'func, raw, args, kwargs'
            fetg__xoyoy = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            zybsd__mdfd = fetg__xoyoy = 'other, pairwise'
        if fname == 'cov':
            zybsd__mdfd = fetg__xoyoy = 'other, pairwise, ddof'
        vldeg__cjxtk = (
            f'lambda df, window, minp, center, {zybsd__mdfd}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {mav__zez}){selection}.{fname}({fetg__xoyoy})'
            )
        khkzh__gjl += f"""  return rolling.obj.apply({vldeg__cjxtk}, rolling.window, rolling.min_periods, rolling.center, {zybsd__mdfd})
"""
        tmn__kdcd = {}
        exec(khkzh__gjl, {'bodo': bodo}, tmn__kdcd)
        impl = tmn__kdcd['impl']
        return impl
    epyfd__epq = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if epyfd__epq else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if epyfd__epq else rolling.obj_type.columns
        other_cols = None if epyfd__epq else other.columns
        fpf__tbxl, rreez__qkp = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        fpf__tbxl, rreez__qkp, out_cols = _gen_df_rolling_out_data(rolling)
    cazv__bkuk = epyfd__epq or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    biyyv__xkvq = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    biyyv__xkvq += '  df = rolling.obj\n'
    biyyv__xkvq += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if epyfd__epq else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    hxgpd__teqks = 'None'
    if epyfd__epq:
        hxgpd__teqks = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif cazv__bkuk:
        jgwj__vlsnj = (set(out_cols) - set([rolling.on])).pop()
        hxgpd__teqks = f"'{jgwj__vlsnj}'" if isinstance(jgwj__vlsnj, str
            ) else str(jgwj__vlsnj)
    biyyv__xkvq += f'  name = {hxgpd__teqks}\n'
    biyyv__xkvq += '  window = rolling.window\n'
    biyyv__xkvq += '  center = rolling.center\n'
    biyyv__xkvq += '  minp = rolling.min_periods\n'
    biyyv__xkvq += f'  on_arr = {rreez__qkp}\n'
    if fname == 'apply':
        biyyv__xkvq += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        biyyv__xkvq += f"  func = '{fname}'\n"
        biyyv__xkvq += f'  index_arr = None\n'
        biyyv__xkvq += f'  raw = False\n'
    if cazv__bkuk:
        biyyv__xkvq += (
            f'  return bodo.hiframes.pd_series_ext.init_series({fpf__tbxl}, index, name)'
            )
        tmn__kdcd = {}
        rvl__flbjk = {'bodo': bodo}
        exec(biyyv__xkvq, rvl__flbjk, tmn__kdcd)
        impl = tmn__kdcd['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(biyyv__xkvq, out_cols,
        fpf__tbxl)


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
        dxsiv__gbg = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(dxsiv__gbg)


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
    own__mptz = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(own__mptz) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    abw__uadm = not isinstance(window_type, types.Integer)
    rreez__qkp = 'None'
    if abw__uadm:
        rreez__qkp = 'bodo.utils.conversion.index_to_array(index)'
    emt__swvtk = 'on_arr, ' if abw__uadm else ''
    fpf__tbxl = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {emt__swvtk}window, minp, center)'
            , rreez__qkp)
    for jgwj__vlsnj in out_cols:
        if jgwj__vlsnj in df_cols and jgwj__vlsnj in other_cols:
            dtnd__nha = df_cols.index(jgwj__vlsnj)
            wrv__hhe = other_cols.index(jgwj__vlsnj)
            txvrs__pgyw = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {dtnd__nha}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {wrv__hhe}), {emt__swvtk}window, minp, center)'
                )
        else:
            txvrs__pgyw = 'np.full(len(df), np.nan)'
        fpf__tbxl.append(txvrs__pgyw)
    return ', '.join(fpf__tbxl), rreez__qkp


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    gymja__nrsx = {'pairwise': pairwise, 'ddof': ddof}
    lctbp__bdc = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        gymja__nrsx, lctbp__bdc, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    gymja__nrsx = {'ddof': ddof, 'pairwise': pairwise}
    lctbp__bdc = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        gymja__nrsx, lctbp__bdc, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, nnobx__nyc = args
        if isinstance(rolling, RollingType):
            own__mptz = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(nnobx__nyc, (tuple, list)):
                if len(set(nnobx__nyc).difference(set(own__mptz))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(nnobx__nyc).difference(set(own__mptz))))
                selection = list(nnobx__nyc)
            else:
                if nnobx__nyc not in own__mptz:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(nnobx__nyc))
                selection = [nnobx__nyc]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            nnlg__ubb = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(nnlg__ubb, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        own__mptz = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            own__mptz = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            own__mptz = rolling.obj_type.columns
        if attr in own__mptz:
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
    ejin__qmxt = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    crm__otc = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in ejin__qmxt):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        zrfk__coqy = crm__otc[ejin__qmxt.index(get_literal_value(on))]
        if not isinstance(zrfk__coqy, types.Array
            ) or zrfk__coqy.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(zix__xdcc.dtype, (types.Boolean, types.Number)) for
        zix__xdcc in crm__otc):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
