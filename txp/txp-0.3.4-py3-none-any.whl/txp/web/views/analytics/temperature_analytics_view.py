import datetime
import matplotlib.pyplot as plt
import pytz
import logging
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import os
import pandas as pd
import txp.common.utils.bigquery_utils

plt.rcParams.update({"font.size": 6.5})
current_directory = os.getcwd()

# TODO: This might be a problem. The logging configuration is being taken from `txp` package
from txp.common.config import settings

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


def mapping_data_from_data_parent(parent):
    list_of_element = []
    for element in parent:
        data = element.get().to_dict()
        list_of_element.append(data)
    return list_of_element


def change_utc_timezone(timestamp):
    utc = pytz.timezone("UTC")
    timezone = pytz.timezone("America/Mexico_City")
    date_time = pd.to_datetime(timestamp)
    localized_timestamp = utc.localize(date_time)
    new_timezone = localized_timestamp.astimezone(timezone)
    return new_timezone


def get_last_temperature_values(
    tenant_id, table_name, current_edge, current_perception, client,
):
    timezone = pytz.timezone("America/Mexico_City")

    last_hour = datetime.datetime.now() - datetime.timedelta(hours=1)
    localized_last_hour = timezone.localize(last_hour)

    now = timezone.localize(datetime.datetime.now())

    df_temperature_values = txp.common.utils.bigquery_utils.get_all_records_within_interval(
        tenant_id,
        table_name,
        current_edge,
        current_perception,
        localized_last_hour.astimezone(pytz.utc),
        now.astimezone(pytz.utc),
        "observation_timestamp",
        client,
    )
    if not df_temperature_values.empty:
        temperature_values = {}
        for index, row in df_temperature_values.iterrows():
            timestamp = change_utc_timezone(row['package_timestamp'])
            for dimension in row["data"]:
                temperature_values[timestamp] = float(dimension["values"])
        return temperature_values
    else:
        logging.info(f"No hay data disponible")
        return None


def actual_machine_temperature(last_temperature_values):
    if not last_temperature_values is None:
        oldest_value = min(last_temperature_values.keys())
        youngest_value = max(last_temperature_values.keys())

        actual_and_last_temperature_difference = np.subtract(
            last_temperature_values[youngest_value],
            last_temperature_values[oldest_value],
        )
        st.metric(
            label="\n",
            value=f"{last_temperature_values[youngest_value]} °C",
            delta=f"{actual_and_last_temperature_difference} °C",
            delta_color="inverse",
        )
    else:
        st.info(f"Sin registro en la última hora.")


def plot_asset_temperatures(name, temperature_values, temperature_dates):
    if not temperature_values is None:
        strtimes = temperature_dates

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=strtimes[::-1],
                y=temperature_values[::-1],
                marker=dict(
                    size=16,
                    color=temperature_values[::-1],
                    colorscale="portland",
                    colorbar=dict(
                        title="Temperatura",
                        tickvals=[min(temperature_values), max(temperature_values)],
                        ticktext=["high", "low"],
                        ticks="outside",
                    ),
                ),
                mode="markers",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=strtimes[::-1],
                y=temperature_values[::-1],
                mode="lines",
                line=dict(color="grey", width=2, dash="dash"),
            )
        )

        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), showlegend=False)
        fig.update_yaxes(range=[20, max(temperature_values)+10])
        return fig

    else:
        return None
