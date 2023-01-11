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
            wygdy__cvr = 'Series'
        else:
            wygdy__cvr = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{wygdy__cvr}.rolling()')
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
        mqd__kxtk = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, mqd__kxtk)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    pztqk__mwqo = dict(win_type=win_type, axis=axis, closed=closed)
    nquly__ivh = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', pztqk__mwqo, nquly__ivh,
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
    pztqk__mwqo = dict(win_type=win_type, axis=axis, closed=closed)
    nquly__ivh = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', pztqk__mwqo, nquly__ivh,
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
        rpq__kgaa, pgthz__syq, edqgr__wffbp, pidp__fco, hvavq__snz = args
        bkb__mfkgr = signature.return_type
        afb__uediu = cgutils.create_struct_proxy(bkb__mfkgr)(context, builder)
        afb__uediu.obj = rpq__kgaa
        afb__uediu.window = pgthz__syq
        afb__uediu.min_periods = edqgr__wffbp
        afb__uediu.center = pidp__fco
        context.nrt.incref(builder, signature.args[0], rpq__kgaa)
        context.nrt.incref(builder, signature.args[1], pgthz__syq)
        context.nrt.incref(builder, signature.args[2], edqgr__wffbp)
        context.nrt.incref(builder, signature.args[3], pidp__fco)
        return afb__uediu._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    bkb__mfkgr = RollingType(obj_type, window_type, on, selection, False)
    return bkb__mfkgr(obj_type, window_type, min_periods_type, center_type,
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
    skm__yxcft = not isinstance(rolling.window_type, types.Integer)
    meo__mplpi = 'variable' if skm__yxcft else 'fixed'
    xca__nvbzo = 'None'
    if skm__yxcft:
        xca__nvbzo = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    moz__hjm = []
    pfe__hwkg = 'on_arr, ' if skm__yxcft else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{meo__mplpi}(bodo.hiframes.pd_series_ext.get_series_data(df), {pfe__hwkg}index_arr, window, minp, center, func, raw)'
            , xca__nvbzo, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    wgum__yhcsk = rolling.obj_type.data
    out_cols = []
    for aqyb__mgxrt in rolling.selection:
        iqth__salc = rolling.obj_type.columns.index(aqyb__mgxrt)
        if aqyb__mgxrt == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            auyvw__fbbtu = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {iqth__salc})'
                )
            out_cols.append(aqyb__mgxrt)
        else:
            if not isinstance(wgum__yhcsk[iqth__salc].dtype, (types.Boolean,
                types.Number)):
                continue
            auyvw__fbbtu = (
                f'bodo.hiframes.rolling.rolling_{meo__mplpi}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {iqth__salc}), {pfe__hwkg}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(aqyb__mgxrt)
        moz__hjm.append(auyvw__fbbtu)
    return ', '.join(moz__hjm), xca__nvbzo, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    pztqk__mwqo = dict(engine=engine, engine_kwargs=engine_kwargs, args=
        args, kwargs=kwargs)
    nquly__ivh = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', pztqk__mwqo, nquly__ivh,
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
    pztqk__mwqo = dict(win_type=win_type, axis=axis, closed=closed, method=
        method)
    nquly__ivh = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', pztqk__mwqo, nquly__ivh,
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
        nque__jadx = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        qhi__qmgdl = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{cmgjf__oofj}'" if
                isinstance(cmgjf__oofj, str) else f'{cmgjf__oofj}' for
                cmgjf__oofj in rolling.selection if cmgjf__oofj != rolling.on))
        rfh__gez = qqw__lao = ''
        if fname == 'apply':
            rfh__gez = 'func, raw, args, kwargs'
            qqw__lao = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            rfh__gez = qqw__lao = 'other, pairwise'
        if fname == 'cov':
            rfh__gez = qqw__lao = 'other, pairwise, ddof'
        mhh__vmsai = (
            f'lambda df, window, minp, center, {rfh__gez}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {qhi__qmgdl}){selection}.{fname}({qqw__lao})'
            )
        nque__jadx += f"""  return rolling.obj.apply({mhh__vmsai}, rolling.window, rolling.min_periods, rolling.center, {rfh__gez})
"""
        wkxk__lgqzf = {}
        exec(nque__jadx, {'bodo': bodo}, wkxk__lgqzf)
        impl = wkxk__lgqzf['impl']
        return impl
    qrjuw__ckfig = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if qrjuw__ckfig else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if qrjuw__ckfig else rolling.obj_type.columns
        other_cols = None if qrjuw__ckfig else other.columns
        moz__hjm, xca__nvbzo = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        moz__hjm, xca__nvbzo, out_cols = _gen_df_rolling_out_data(rolling)
    oxtc__ggmdr = qrjuw__ckfig or len(rolling.selection) == (1 if rolling.
        on is None else 2) and rolling.series_select
    oouwn__csbyk = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    oouwn__csbyk += '  df = rolling.obj\n'
    oouwn__csbyk += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if qrjuw__ckfig else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    wygdy__cvr = 'None'
    if qrjuw__ckfig:
        wygdy__cvr = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif oxtc__ggmdr:
        aqyb__mgxrt = (set(out_cols) - set([rolling.on])).pop()
        wygdy__cvr = f"'{aqyb__mgxrt}'" if isinstance(aqyb__mgxrt, str
            ) else str(aqyb__mgxrt)
    oouwn__csbyk += f'  name = {wygdy__cvr}\n'
    oouwn__csbyk += '  window = rolling.window\n'
    oouwn__csbyk += '  center = rolling.center\n'
    oouwn__csbyk += '  minp = rolling.min_periods\n'
    oouwn__csbyk += f'  on_arr = {xca__nvbzo}\n'
    if fname == 'apply':
        oouwn__csbyk += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        oouwn__csbyk += f"  func = '{fname}'\n"
        oouwn__csbyk += f'  index_arr = None\n'
        oouwn__csbyk += f'  raw = False\n'
    if oxtc__ggmdr:
        oouwn__csbyk += (
            f'  return bodo.hiframes.pd_series_ext.init_series({moz__hjm}, index, name)'
            )
        wkxk__lgqzf = {}
        bjvz__lavwy = {'bodo': bodo}
        exec(oouwn__csbyk, bjvz__lavwy, wkxk__lgqzf)
        impl = wkxk__lgqzf['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(oouwn__csbyk, out_cols,
        moz__hjm)


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
        jchuf__iqly = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(jchuf__iqly)


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
    wpzgh__muxjj = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(wpzgh__muxjj) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    skm__yxcft = not isinstance(window_type, types.Integer)
    xca__nvbzo = 'None'
    if skm__yxcft:
        xca__nvbzo = 'bodo.utils.conversion.index_to_array(index)'
    pfe__hwkg = 'on_arr, ' if skm__yxcft else ''
    moz__hjm = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {pfe__hwkg}window, minp, center)'
            , xca__nvbzo)
    for aqyb__mgxrt in out_cols:
        if aqyb__mgxrt in df_cols and aqyb__mgxrt in other_cols:
            pnf__vdoe = df_cols.index(aqyb__mgxrt)
            xfu__fnvj = other_cols.index(aqyb__mgxrt)
            auyvw__fbbtu = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {pnf__vdoe}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {xfu__fnvj}), {pfe__hwkg}window, minp, center)'
                )
        else:
            auyvw__fbbtu = 'np.full(len(df), np.nan)'
        moz__hjm.append(auyvw__fbbtu)
    return ', '.join(moz__hjm), xca__nvbzo


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    qqj__yzg = {'pairwise': pairwise, 'ddof': ddof}
    axnb__pghvu = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        qqj__yzg, axnb__pghvu, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    qqj__yzg = {'ddof': ddof, 'pairwise': pairwise}
    axnb__pghvu = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        qqj__yzg, axnb__pghvu, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, top__bqjw = args
        if isinstance(rolling, RollingType):
            wpzgh__muxjj = rolling.obj_type.selection if isinstance(rolling
                .obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(top__bqjw, (tuple, list)):
                if len(set(top__bqjw).difference(set(wpzgh__muxjj))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(top__bqjw).difference(set(wpzgh__muxjj))))
                selection = list(top__bqjw)
            else:
                if top__bqjw not in wpzgh__muxjj:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(top__bqjw))
                selection = [top__bqjw]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            kyp__hrimj = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(kyp__hrimj, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        wpzgh__muxjj = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            wpzgh__muxjj = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            wpzgh__muxjj = rolling.obj_type.columns
        if attr in wpzgh__muxjj:
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
    din__swq = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    wgum__yhcsk = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in din__swq):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        nny__jnvjn = wgum__yhcsk[din__swq.index(get_literal_value(on))]
        if not isinstance(nny__jnvjn, types.Array
            ) or nny__jnvjn.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(myb__fcg.dtype, (types.Boolean, types.Number)) for
        myb__fcg in wgum__yhcsk):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
