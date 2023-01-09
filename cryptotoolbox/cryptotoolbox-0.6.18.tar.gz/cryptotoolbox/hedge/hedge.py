from scipy import stats
import pandas as pd
from numpy.lib.stride_tricks import as_strided as stride
from cryptotoolbox.realtime import realtime_plotting_utility
from cryptotoolbox.risk_metrics import riskmetrics
from cryptotoolbox.analyzer import market
import numpy as np
from cryptotoolbox.signal import signal_utility

def roll(df, w):
    v = df.values
    d0, d1 = v.shape
    s0, s1 = v.strides
    restricted_length = d0 - (w - 1)
    a = stride(v, (restricted_length, w, d1), (s0, s0, s1))
    rolled_df = pd.concat({
        row: pd.DataFrame(values, columns=df.columns)
        for row, values in zip(df.index[-restricted_length:], a)
    })
    return rolled_df.groupby(level=0)


def compute_alpha_signal_dynamical_ls_neutral_single_discrete_alpha_one(lo_df=None, core_tokens=['BTC'], extra_tokens=[],rebalancing_day=6, lookback_window =5, pente_window = 10, me_center = 0.9, me_threshold = 0.05, mix_lo = True, me_short = True,ls_signal_suffix = 'LS',aggregate_and_save = True,plot_subsignal_html = True,extract_subsignal_kpi = True):
    assert len(core_tokens) == 1

    ssjs =  core_tokens + extra_tokens
    univ = '_'.join(ssjs)
    aggregated_signals_df = None
    if 'rebalance' not in lo_df.columns:
        lo_df['weekday'] = lo_df.index.weekday
        lo_df['rebalance'] = lo_df.index.weekday == rebalancing_day

    for ssj in ssjs:
        current = f'univ{univ}_lookback_{lookback_window}_pente_{pente_window}_short_{me_short}_center_{me_center}.plkl'
        print('#########'+current)

        data_df = lo_df.copy()
        print('computing weekly signals')

        weekly_df = data_df.copy()
        weekly_df = weekly_df[weekly_df['rebalance']]

        def is_growing(a_np):
            return np.all(a_np[:-1] <= a_np[1:])

        def is_decreasing(a_np):
            return np.all(a_np[:-1] >= a_np[1:])

        def compute_ranked_slope_continuous(short, center, lagging_df):
            is_growingg = is_growing(lagging_df['rolling_slope'].values)
            is_decreasingg = is_decreasing(lagging_df['rolling_slope'].values)
            if is_growingg:
                return 1.
            if is_decreasingg:
                return -1.

            lagging_df['rolling_slope_rank'] = lagging_df['rolling_slope'].rank(pct=True)

            if short:
                lagging_df['rolling_slope_rank_ls'] = 2 * lagging_df['rolling_slope_rank'] - center
                lagging_df['rolling_slope_rank_ls'] = lagging_df['rolling_slope_rank_ls'].clip(-1, 1)
            else:
                lagging_df['rolling_slope_rank_ls'] = lagging_df['rolling_slope_rank']

            gen_sig = lagging_df['rolling_slope_rank_ls'].iloc[-1]
            return gen_sig

        def compute_ranked_slope(short, center, threshold, lagging_df):
            is_growingg = is_growing(lagging_df['rolling_slope'].values)
            is_decreasingg = is_decreasing(lagging_df['rolling_slope'].values)
            if is_growingg:
                return 1.
            if is_decreasingg:
                return -1.

            lagging_df['rolling_slope_rank'] = lagging_df['rolling_slope'].rank(pct=True)

            if short:
                lagging_df['rolling_slope_rank_ls'] = 2 * lagging_df['rolling_slope_rank'] - center
                lagging_df['rolling_slope_rank_ls'] = lagging_df['rolling_slope_rank_ls'].clip(-1, 1)
            else:
                lagging_df['rolling_slope_rank_ls'] = lagging_df['rolling_slope_rank']

            gen_sig = lagging_df['rolling_slope_rank_ls'].iloc[-1]
            if gen_sig > threshold:
                return 1.
            if gen_sig < -threshold:
                return -1.
            return 0.

        print('computing signals')

        def compute_slope(slope_df):
            y = slope_df.values
            slope = stats.linregress(np.arange(len(y)), y).slope
            return slope

        print('slope')
        weekly_df['rolling_slope'] = weekly_df[f'close_{ssj}'].rolling(window=pente_window).apply(compute_slope)

        #                        data_df = data_df.iloc[-500:]
        print('slope done')

        import functools
        go = functools.partial(compute_ranked_slope, me_short, me_center, me_threshold)
        signal_df = roll(weekly_df, lookback_window).apply(go)

        signal_df = signal_df.to_frame()
        signal_df.columns = ['signal_gen']
        data_df = pd.merge(data_df.copy(), signal_df.copy(),how='left', right_index=True, left_index=True)
        data_df['signal_gen']=data_df['signal_gen'].ffill()
        data_df['signal'] = data_df['signal_gen'].shift()

        gocont = functools.partial(compute_ranked_slope_continuous, me_short, me_center)
        signalcont_df = roll(weekly_df, lookback_window).apply(gocont)

        signalcont_df = signalcont_df.to_frame()
        signalcont_df.columns = ['signalcont_gen']
        data_df = pd.merge(data_df.copy(), signalcont_df.copy(),how='left', right_index=True, left_index=True)
        data_df['signalcont_gen']=data_df['signalcont_gen'].ffill()
        data_df['signalcont'] = data_df['signalcont_gen'].shift()

        if aggregate_and_save:
            sig_to_save = data_df[[f'close_{ssj}','signal','signalcont']].copy()
            if aggregated_signals_df is None:
                sig_to_save.columns = [f'close_{ssj}',f'S{ls_signal_suffix}{ssj}',f'SC{ls_signal_suffix}{ssj}']
                aggregated_signals_df = sig_to_save.copy()
            else :
                sig_to_save.columns = [f'close_{ssj}',f'S{ls_signal_suffix}{ssj}',f'SC{ls_signal_suffix}{ssj}']
                aggregated_signals_df = pd.merge(aggregated_signals_df.copy(), sig_to_save.copy(), left_index = True, right_index=True)

        data_df = data_df.dropna()
        data_df['epoch_number'] = data_df['rebalance'].cumsum()
        perf_df = data_df.copy()
        perf_df=perf_df.rename(columns={f'close_{ssj}':'close'})
        freqly_df, _ = signal_utility.reconstitute_signal_perf(data=perf_df, transaction_cost=True,
                                                               normalization=False)

        if plot_subsignal_html:
            fig = realtime_plotting_utility.plot_multiple_time_series(freqly_df[['signal']],logy = False,drop_na_inf = False, title = ssj)
            fig.show()
            fig = realtime_plotting_utility.plot_multiple_time_series(freqly_df[['reconstituted_perf', 'reconstituted_under']],put_on_same_scale = False, drop_na_inf = False, title = ssj)
            fig.show()
            fig1 = realtime_plotting_utility.plot_multiple_time_series(freqly_df[['reconstituted_perf', 'reconstituted_under']],logy = False, put_on_same_scale = False, drop_na_inf = False, title = ssj)
            fig1.show()

        if extract_subsignal_kpi:
            def compute_metrics(df, strat=None):
                kpi_df = riskmetrics.get_kpi(df[[strat]])
                return kpi_df.to_dict()[strat]

            me_strat = 'reconstituted_perf'
            go_comp_kpi = lambda x: compute_metrics(x, strat=me_strat)

            epochkpis_df = freqly_df[['epoch_number', me_strat]].groupby(['epoch_number']).apply(go_comp_kpi)
            epochkpis_df = epochkpis_df.sort_index()
            epochkpis_df = pd.DataFrame.from_records(epochkpis_df.to_dict()).T



            strat_data_df = freqly_df[['reconstituted_perf', 'reconstituted_under']].copy()
            #strat_data_df = strat_data_df[strat_data_df.index >= '2021-02-01'].copy()
            ma = market.MarketAnalyzer(strat_data_df, hourlyze = True)

            print(f'computing kpis for underlying {ssj}')
            kpi_df = ma.get_kpi().T
            kpi_df=kpi_df.dropna()
            kpi_df=kpi_df[~np.isnan(kpi_df.sharpe)]
            kpi_df = kpi_df[kpi_df.index == 'reconstituted_perf']
            print(kpi_df.head())

    def curate_signals(row,under='BTC'):
        if abs(row[f'close_{under}']) <= 1e-3:
            return np.nan
        else:
            return row[f'S{ls_signal_suffix}{ssj}']

    for ssj in ssjs:
        go_curate = lambda x: curate_signals(x, under=ssj)
        aggregated_signals_df[f'S{ls_signal_suffix}{ssj}'] = aggregated_signals_df.apply(go_curate, axis=1)

#    for extra_tok in extra_tokens :
#        aggregated_signals_df[f'S{ls_signal_suffix}{extra_tok}'] = aggregated_signals_df[f'S{ls_signal_suffix}{extra_tok}'].fillna(0.)

    aggregated_signals_df = aggregated_signals_df.dropna()
#    aggregated_signals_df = aggregated_signals_df[~aggregated_signals_df[f'S{ls_signal_suffix}BTC'].isna().values]
#    aggregated_signals_df = aggregated_signals_df.fillna(0.)

    if mix_lo:
        aggregated_signals_df = pd.merge(aggregated_signals_df.copy(), lo_df.copy(),suffixes=['','_lo'], how='left',
                                         left_index=True, right_index=True)
        def compute_mix_signals(row_df, core_tokens= None, extra_tokens= None):
            lo_expo = row_df['expo']
            if lo_expo > 0 :
                return {f'SF{tok}':row_df[f'SMIX{tok}'] for tok in core_tokens + extra_tokens}
            else :
                return {f'SF{tok}':row_df[f'SLS{tok}'] for tok in core_tokens + extra_tokens}

        go_mix = lambda x : compute_mix_signals(x, core_tokens=core_tokens, extra_tokens=extra_tokens)
        nex_signals_series = aggregated_signals_df.apply(go_mix, axis=1)
        nex_signals_df = pd.DataFrame().from_records(nex_signals_series.values)
        nex_signals_df.index = nex_signals_series.index
        aggregated_signals_df = pd.merge(nex_signals_df.copy(),aggregated_signals_df.copy(),left_index=True, right_index=True)
    else :
        for tok in core_tokens + extra_tokens:
            aggregated_signals_df[f'SF{tok}']=aggregated_signals_df[f'SLS{tok}']


    for me_tok in ssjs:
        aggregated_signals_df['return_{}'.format(me_tok)] = aggregated_signals_df['close_{}'.format(me_tok)].pct_change()
        columns_to_keep = [f'return_{me_tok}' for me_tok in ssjs] + [f'close_{me_tok}' for me_tok in ssjs]

    merged_df=aggregated_signals_df.copy()
    print('computing exposition')
    def compute_strat_ret(row_df, universe = None):
        aggregated_return = 0.
        for me_token in universe:
            aggregated_return = aggregated_return + row_df[f'return_{me_token}'] * row_df[f'SF{me_token}']
        return aggregated_return

    comp_ret = lambda x : compute_strat_ret(x, universe=ssjs)
    merged_df['STRAT_RETURN'] = merged_df.apply(comp_ret, axis=1)
    merged_df['STRAT_RETURN'] =  merged_df['STRAT_RETURN'].fillna(0.)
    merged_df['COMBO_STRAT'] = np.cumprod(1 + merged_df['STRAT_RETURN'].values)
    merged_df['DOLLAR_COMBO_STRAT'] = 10000. * np.cumprod(1 + merged_df['STRAT_RETURN'].values)
    return merged_df.copy(), data_df.copy()
