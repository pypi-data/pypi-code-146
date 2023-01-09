from cryptotoolbox.risk_metrics import riskmetrics
import pandas as pd

from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.graph_objects as go

import numpy as np
from datetime import datetime

def compute_caving_stage_characteristic(phase_df):
    if phase_df.shape[0] < 4:
        return np.nan
    min_reached = 100. - phase_df['drawdown_to_display'].min()
    date_min_reached = phase_df['drawdown_to_display'].idxmin()
    time_to_low = date_min_reached - phase_df.index[0]
    time_to_high = phase_df.index[-1] - date_min_reached
    time_period = phase_df.index[-1] - phase_df.index[0]
    results = {
        'max loss': min_reached,
        'max loss date': date_min_reached,
        'loss time': time_to_low,
        'recovery time': time_to_high,
        'time period': time_period,
        'period start': phase_df.index[0],
        'period end': phase_df.index[-1]

    }
    return results

def plot_drawdown(data_df, column_name, error_message = 'no data'):
    if data_df is None:
        fig = make_subplots(rows=1, cols=1)
        fig.update_layout(height=600, width=1000, title_text=error_message)
        return fig
    fig = make_subplots(rows=1, cols=1)
    trace_sig = go.Scatter(
        x=data_df.index,
        y=data_df[column_name],
        name="drawdown",
        opacity=0.8)
    fig.append_trace(trace_sig, row=1, col=1)
    fig.update_layout(height=600, width=1600, title_text="Drawdown chart",showlegend=True,legend = dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ))
    fig.update_xaxes(rangeslider_visible=True)
    return fig

def dd_filter_daily(dataframe):
    dataframe['day'] = (dataframe.index.hour == 23) & (dataframe.index.minute == 0)
    daily_aggregated_df = dataframe[dataframe['day']].copy()
    daily_aggregated_df['date'] = daily_aggregated_df.index

    def truncate_date(row):
        datet = row['date']
        return datetime(datet.year, datet.month, datet.day)

    daily_aggregated_df['trunc_date'] = daily_aggregated_df.apply(truncate_date, axis=1)
    daily_aggregated_df = daily_aggregated_df.set_index('trunc_date')
    daily_aggregated_df = daily_aggregated_df.drop(columns=['date','day'])
    return daily_aggregated_df


def investigate_drawdown(data_df, column_toinvestigate = 'close'):
    data_df['normalized_strategy'] = data_df[column_toinvestigate]
    daily_data_df = dd_filter_daily(data_df[['normalized_strategy']].copy())

    ############# strategy drawdown
    dd_norm = riskmetrics.drawdown(daily_data_df['normalized_strategy'])

    daily_data_df['drawdown'] = dd_norm
    daily_data_df['drawdown_to_display'] = 100. * (1. - dd_norm)
    fig = plot_drawdown(daily_data_df, 'drawdown_to_display')


    drawdown_df = daily_data_df[['drawdown_to_display']].copy()
    drawdown_df = drawdown_df.dropna()

    drawdown_df['ATH'] = drawdown_df['drawdown_to_display']>=99.999
    drawdown_df['phase_number'] = drawdown_df['ATH'].cumsum()

    caving_stage_df = drawdown_df[drawdown_df['ATH'] == False].copy()




    caving_phases_metrics_df = caving_stage_df.groupby(['phase_number']).apply(compute_caving_stage_characteristic)
    caving_phases_metrics_df_temp = caving_phases_metrics_df.dropna()

    caving_phases_metrics_df = pd.DataFrame().from_records(caving_phases_metrics_df_temp.values)

    drawdown_df = drawdown_df.rename(columns = {'drawdown_to_display':f'dd_{column_toinvestigate}'})
    return drawdown_df[[f'dd_{column_toinvestigate}']].copy(), caving_phases_metrics_df, fig

