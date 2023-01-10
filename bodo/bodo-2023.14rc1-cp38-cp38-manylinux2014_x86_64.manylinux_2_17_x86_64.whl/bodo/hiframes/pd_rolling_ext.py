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
            pql__oriw = 'Series'
        else:
            pql__oriw = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{pql__oriw}.rolling()')
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
        mqhjx__ervbv = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, mqhjx__ervbv)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    ndn__xfw = dict(win_type=win_type, axis=axis, closed=closed)
    qxdxq__wyvms = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', ndn__xfw, qxdxq__wyvms,
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
    ndn__xfw = dict(win_type=win_type, axis=axis, closed=closed)
    qxdxq__wyvms = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', ndn__xfw, qxdxq__wyvms,
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
        xmaxs__hsgme, coxv__iaa, lrx__bxjqc, savbf__ssrv, zwy__nhdo = args
        cdfce__aghh = signature.return_type
        uwt__euk = cgutils.create_struct_proxy(cdfce__aghh)(context, builder)
        uwt__euk.obj = xmaxs__hsgme
        uwt__euk.window = coxv__iaa
        uwt__euk.min_periods = lrx__bxjqc
        uwt__euk.center = savbf__ssrv
        context.nrt.incref(builder, signature.args[0], xmaxs__hsgme)
        context.nrt.incref(builder, signature.args[1], coxv__iaa)
        context.nrt.incref(builder, signature.args[2], lrx__bxjqc)
        context.nrt.incref(builder, signature.args[3], savbf__ssrv)
        return uwt__euk._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    cdfce__aghh = RollingType(obj_type, window_type, on, selection, False)
    return cdfce__aghh(obj_type, window_type, min_periods_type, center_type,
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
    cxfww__ten = not isinstance(rolling.window_type, types.Integer)
    glx__oao = 'variable' if cxfww__ten else 'fixed'
    ixx__kqldy = 'None'
    if cxfww__ten:
        ixx__kqldy = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    yvqa__tijua = []
    ncd__fpic = 'on_arr, ' if cxfww__ten else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{glx__oao}(bodo.hiframes.pd_series_ext.get_series_data(df), {ncd__fpic}index_arr, window, minp, center, func, raw)'
            , ixx__kqldy, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    kmjbl__kenvs = rolling.obj_type.data
    out_cols = []
    for djtqh__oav in rolling.selection:
        wrga__dxhhf = rolling.obj_type.columns.index(djtqh__oav)
        if djtqh__oav == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            jxu__akfgr = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {wrga__dxhhf})'
                )
            out_cols.append(djtqh__oav)
        else:
            if not isinstance(kmjbl__kenvs[wrga__dxhhf].dtype, (types.
                Boolean, types.Number)):
                continue
            jxu__akfgr = (
                f'bodo.hiframes.rolling.rolling_{glx__oao}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {wrga__dxhhf}), {ncd__fpic}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(djtqh__oav)
        yvqa__tijua.append(jxu__akfgr)
    return ', '.join(yvqa__tijua), ixx__kqldy, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    ndn__xfw = dict(engine=engine, engine_kwargs=engine_kwargs, args=args,
        kwargs=kwargs)
    qxdxq__wyvms = dict(engine=None, engine_kwargs=None, args=None, kwargs=None
        )
    check_unsupported_args('Rolling.apply', ndn__xfw, qxdxq__wyvms,
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
    ndn__xfw = dict(win_type=win_type, axis=axis, closed=closed, method=method)
    qxdxq__wyvms = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', ndn__xfw, qxdxq__wyvms,
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
        qgu__jhxo = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        iabd__zlt = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{rxy__nqo}'" if
                isinstance(rxy__nqo, str) else f'{rxy__nqo}' for rxy__nqo in
                rolling.selection if rxy__nqo != rolling.on))
        ulzm__fbq = jgp__mir = ''
        if fname == 'apply':
            ulzm__fbq = 'func, raw, args, kwargs'
            jgp__mir = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            ulzm__fbq = jgp__mir = 'other, pairwise'
        if fname == 'cov':
            ulzm__fbq = jgp__mir = 'other, pairwise, ddof'
        gghr__ghq = (
            f'lambda df, window, minp, center, {ulzm__fbq}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {iabd__zlt}){selection}.{fname}({jgp__mir})'
            )
        qgu__jhxo += f"""  return rolling.obj.apply({gghr__ghq}, rolling.window, rolling.min_periods, rolling.center, {ulzm__fbq})
"""
        ihg__prer = {}
        exec(qgu__jhxo, {'bodo': bodo}, ihg__prer)
        impl = ihg__prer['impl']
        return impl
    ryeeo__boyfy = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if ryeeo__boyfy else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if ryeeo__boyfy else rolling.obj_type.columns
        other_cols = None if ryeeo__boyfy else other.columns
        yvqa__tijua, ixx__kqldy = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        yvqa__tijua, ixx__kqldy, out_cols = _gen_df_rolling_out_data(rolling)
    myeo__xstu = ryeeo__boyfy or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    iezx__mkd = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    iezx__mkd += '  df = rolling.obj\n'
    iezx__mkd += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if ryeeo__boyfy else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    pql__oriw = 'None'
    if ryeeo__boyfy:
        pql__oriw = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif myeo__xstu:
        djtqh__oav = (set(out_cols) - set([rolling.on])).pop()
        pql__oriw = f"'{djtqh__oav}'" if isinstance(djtqh__oav, str) else str(
            djtqh__oav)
    iezx__mkd += f'  name = {pql__oriw}\n'
    iezx__mkd += '  window = rolling.window\n'
    iezx__mkd += '  center = rolling.center\n'
    iezx__mkd += '  minp = rolling.min_periods\n'
    iezx__mkd += f'  on_arr = {ixx__kqldy}\n'
    if fname == 'apply':
        iezx__mkd += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        iezx__mkd += f"  func = '{fname}'\n"
        iezx__mkd += f'  index_arr = None\n'
        iezx__mkd += f'  raw = False\n'
    if myeo__xstu:
        iezx__mkd += (
            f'  return bodo.hiframes.pd_series_ext.init_series({yvqa__tijua}, index, name)'
            )
        ihg__prer = {}
        ziv__gbrcr = {'bodo': bodo}
        exec(iezx__mkd, ziv__gbrcr, ihg__prer)
        impl = ihg__prer['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(iezx__mkd, out_cols,
        yvqa__tijua)


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
        csehf__vgg = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(csehf__vgg)


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
    qln__wpnl = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(qln__wpnl) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    cxfww__ten = not isinstance(window_type, types.Integer)
    ixx__kqldy = 'None'
    if cxfww__ten:
        ixx__kqldy = 'bodo.utils.conversion.index_to_array(index)'
    ncd__fpic = 'on_arr, ' if cxfww__ten else ''
    yvqa__tijua = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {ncd__fpic}window, minp, center)'
            , ixx__kqldy)
    for djtqh__oav in out_cols:
        if djtqh__oav in df_cols and djtqh__oav in other_cols:
            itid__ssbmm = df_cols.index(djtqh__oav)
            avzcg__sbu = other_cols.index(djtqh__oav)
            jxu__akfgr = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {itid__ssbmm}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {avzcg__sbu}), {ncd__fpic}window, minp, center)'
                )
        else:
            jxu__akfgr = 'np.full(len(df), np.nan)'
        yvqa__tijua.append(jxu__akfgr)
    return ', '.join(yvqa__tijua), ixx__kqldy


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    dyjmg__gllxl = {'pairwise': pairwise, 'ddof': ddof}
    yhwlf__dzafp = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        dyjmg__gllxl, yhwlf__dzafp, package_name='pandas', module_name='Window'
        )
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    dyjmg__gllxl = {'ddof': ddof, 'pairwise': pairwise}
    yhwlf__dzafp = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        dyjmg__gllxl, yhwlf__dzafp, package_name='pandas', module_name='Window'
        )
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, hfb__dhpxs = args
        if isinstance(rolling, RollingType):
            qln__wpnl = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(hfb__dhpxs, (tuple, list)):
                if len(set(hfb__dhpxs).difference(set(qln__wpnl))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(hfb__dhpxs).difference(set(qln__wpnl))))
                selection = list(hfb__dhpxs)
            else:
                if hfb__dhpxs not in qln__wpnl:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(hfb__dhpxs))
                selection = [hfb__dhpxs]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            lhsut__hqge = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(lhsut__hqge, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        qln__wpnl = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            qln__wpnl = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            qln__wpnl = rolling.obj_type.columns
        if attr in qln__wpnl:
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
    tmjlo__lhxh = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    kmjbl__kenvs = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in tmjlo__lhxh):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        wbhdy__jzhra = kmjbl__kenvs[tmjlo__lhxh.index(get_literal_value(on))]
        if not isinstance(wbhdy__jzhra, types.Array
            ) or wbhdy__jzhra.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(ovuwq__zbwsb.dtype, (types.Boolean, types.Number)
        ) for ovuwq__zbwsb in kmjbl__kenvs):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
