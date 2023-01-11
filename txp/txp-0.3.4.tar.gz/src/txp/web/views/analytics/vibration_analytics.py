import datetime

import txp.common.utils.bigquery_utils
from txp.common.ml.annotation import AnnotationLabel
from txp.common.utils.authentication_utils import AuthenticationInfo
from txp.web.core_components.app_component import Card
import matplotlib.pyplot as plt
from txp.common.utils.plotter_utils import FFTPlotter, PSDPlotter
from txp.common.utils import metrics
import pytz
import time
import logging
import streamlit as st
import plotly
import plotly.graph_objects as go
import numpy as np
import os
import pandas as pd

plt.rcParams.update({"font.size": 6.5})
current_directory = os.getcwd()

# TODO: This might be a problem. The logging configuration is being taken from `txp` package
from txp.common.config import settings

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


def mapping_data_from_data_parent(parent):
    list_of_element = []
    for element in parent:
        data = element.reprJSON()
        list_of_element.append(data)
    return list_of_element


def get_machines_with_vibration_analysis(edges_data):
    vibrational_assets = {}
    for machine_id, edges in edges_data.items():
        if any(edge["device_kind"] == "Icomox" for edge in edges):
            machine = machine_id
            v_edges = []
            for edge in edges:
                if edge["device_kind"] == "Icomox":
                    v_edges.append(edge["logical_id"])
            vibrational_assets[machine] = v_edges

    return vibrational_assets


def vibrational_perceptions(edges_data, current_machine, current_edge, project_data):
    for edge in edges_data[current_machine]:
        if edge["logical_id"] == current_edge:
            for device in project_data.device_kinds_table.values():
                if edge["device_kind"] == device["kind"]:
                    return list(device["perceptions"].keys())


def add_trace(format_type, timestamps, data, current_perception, labels, user):
    """Adds traces per sampling window data and set visibility buttons."""

    traces = []
    for timestamp, objects, label in zip(timestamps, data, labels):
        if label is not None and user == AuthenticationInfo.UserRole.Admin:
            name = f"{label}: "
            x_value = name + timestamp.strftime("%H:%M:%S")
        else:
            x_value = timestamp.strftime("%H:%M:%S")
        for object, visibility in zip(objects, [True, False, False]):
            if format_type == "fft":
                trace = go.Scatter3d(
                    x=[x_value] * len(object.frequency_axis),
                    y=object.frequency_axis,
                    z=object.sample_count
                    * np.abs(object.signal_frequency_amplitude_axis),
                    mode="lines",
                    name=f"{x_value}",
                    visible=visibility,
                )
                traces.append(trace)
            elif format_type == "psd":
                trace = go.Scatter3d(
                    x=[x_value] * len(object.frequency),
                    y=object.frequency,
                    z=object.psd,
                    mode="lines",
                    name=f"{x_value}",
                    visible=visibility,
                )
                traces.append(trace)

    if not current_perception == "Microphone":
        layout = dict(
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=True,
                    buttons=list(
                        [
                            dict(
                                label="x",
                                method="update",
                                args=[{"visible": [True, False, False] * len(data)}],
                            ),
                            dict(
                                label="y",
                                method="update",
                                args=[{"visible": [False, True, False] * len(data)}],
                            ),
                            dict(
                                label="z",
                                method="update",
                                args=[{"visible": [False, False, True] * len(data)}],
                            ),
                        ]
                    ),
                )
            ],
        )
    else:
        layout = dict(height=650)
    fig = go.Figure(data=traces, layout=layout)
    return fig


def plot_per_condition(format_type, object_data, current_perception):
    fig = go.Figure()
    if format_type == "fft":
        fig.add_trace(
            go.Scatter(
                x=object_data[0].frequency_axis,
                y=object_data[0].sample_count
                * np.abs(object_data[0].signal_frequency_amplitude_axis),
            )
        )

    elif format_type == "psd":
        fig.add_trace(
            go.Scatter(
                x=object_data[0].frequency,
                y=object_data[0].psd,
            )
        )

    if not current_perception == "Microphone":
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=True,
                    buttons=list(
                        [
                            dict(
                                label="x",
                                method="update",
                                args=[
                                    {
                                        "y": [
                                            object_data[0].sample_count
                                            * np.abs(
                                                object_data[
                                                    0
                                                ].signal_frequency_amplitude_axis
                                            )
                                            if format_type == "fft"
                                            else object_data[0].psd,
                                        ],
                                        "x": [
                                            object_data[0].frequency_axis
                                            if format_type == "fft"
                                            else object_data[0].frequency
                                        ],
                                    }
                                ],
                            ),
                            dict(
                                label="y",
                                method="update",
                                args=[
                                    {
                                        "y": [
                                            object_data[1].sample_count
                                            * np.abs(
                                                object_data[
                                                    1
                                                ].signal_frequency_amplitude_axis
                                            )
                                            if format_type == "fft"
                                            else object_data[1].psd
                                        ],
                                        "x": [
                                            object_data[1].frequency_axis
                                            if format_type == "fft"
                                            else object_data[1].frequency
                                        ],
                                    }
                                ],
                            ),
                            dict(
                                label="z",
                                method="update",
                                args=[
                                    {
                                        "y": [
                                            object_data[2].sample_count
                                            * np.abs(
                                                object_data[
                                                    2
                                                ].signal_frequency_amplitude_axis
                                            )
                                            if format_type == "fft"
                                            else object_data[2].psd,
                                        ],
                                        "x": [
                                            object_data[2].frequency_axis
                                            if format_type == "fft"
                                            else object_data[2].frequency
                                        ],
                                    }
                                ],
                            ),
                        ]
                    ),
                )
            ],
        )
    else:
        pass
    return fig


def change_utc_timezone(timestamp):
    utc = pytz.timezone("UTC")
    timezone = pytz.timezone("America/Mexico_City")
    date_time = pd.to_datetime(timestamp)
    localized_timestamp = utc.localize(date_time)
    new_timezone = localized_timestamp.astimezone(timezone)
    return new_timezone


def separate_df_per_dimension(df):
    x = df.loc[df["dimension"] == 0]
    y = df.loc[df["dimension"] == 1]
    z = df.loc[df["dimension"] == 2]

    sorted_dfs = []
    for df in [x, y, z]:
        df_drop = df.drop(columns=["dimension"])
        df_drop["observation_timestamp"] = (
            pd.to_datetime(df_drop["observation_timestamp"])
            .dt.tz_localize("UTC")
            .dt.tz_convert("America/Mexico_City")
        )
        sorted_df = df_drop.sort_values(by="observation_timestamp").reset_index(
            drop=True
        )
        sorted_dfs.append(sorted_df)
    return sorted_dfs[0], sorted_dfs[1], sorted_dfs[2]


def metrics_visualization(df):
    df = df.drop(
        columns=[
            "edge_logical_id",
            "package_timestamp",
            "perception_name",
            "signal_timestamp",
            "configuration_id",
            "partition_timestamp",
            "tenant_id",
            "dataset_versions",
        ],
        errors="ignore",
    )

    xdf, ydf, zdf = separate_df_per_dimension(df)
    column_names = list(xdf.columns.values)
    column_names.remove("observation_timestamp")

    fig = plotly.subplots.make_subplots(
        rows=len(column_names), cols=1, vertical_spacing=0.03
    )

    for index, colname in enumerate(column_names):
        fig.add_trace(
            go.Scatter(
                name=f"X-{colname}",
                x=xdf["observation_timestamp"][::-1],
                y=xdf[colname][::-1],
                visible=True,
            ),
            row=index + 1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                name=f"Y-{colname}",
                x=ydf["observation_timestamp"][::-1],
                y=ydf[colname][::-1],
                visible=False,
            ),
            row=index + 1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                name=f"Z-{colname}",
                x=zdf["observation_timestamp"][::-1],
                y=zdf[colname][::-1],
                visible=False,
            ),
            row=index + 1,
            col=1,
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        width=500,
        height=900,
        updatemenus=[
            dict(
                type="buttons",
                showactive=True,
                buttons=list(
                    [
                        dict(
                            label="Líneas",
                            method="restyle",
                            args=["type", "markers"],
                        ),
                        dict(
                            label="Barras",
                            method="restyle",
                            args=["type", "bar"],
                        ),
                    ]
                ),
            ),
            dict(
                type="buttons",
                showactive=True,
                yanchor="top",
                x=0.1,
                y=1.09,
                direction="right",
                pad={"r": 10, "t": 10},
                xanchor="left",
                buttons=list(
                    [
                        dict(
                            label="x",
                            method="restyle",
                            args=[{"visible": [True, False, False] * len(xdf.columns)}],
                        ),
                        dict(
                            label="y",
                            method="restyle",
                            args=[{"visible": [False, True, False] * len(xdf.columns)}],
                        ),
                        dict(
                            label="z",
                            method="restyle",
                            args=[{"visible": [False, False, True] * len(xdf.columns)}],
                        ),
                    ]
                ),
            ),
        ],
    )
    fig.update_layout(
        annotations=[
            dict(
                text="Ejes",
                x=0,
                xref="paper",
                y=1.07,
                yref="paper",
                align="left",
                showarrow=False,
            )
        ]
    )

    st.plotly_chart(fig, use_container_width=True)


def get_element_cloud_to_condition_perspective(
    tenant_id,
    vibrations_time_dataset,
    current_edge,
    current_perception,
    client,
):
    timezone = pytz.timezone("America/Mexico_City")

    last_hour = datetime.datetime.now() - datetime.timedelta(hours=1)
    localized_last_hour = timezone.localize(last_hour)

    now = timezone.localize(datetime.datetime.now())

    element = txp.common.utils.bigquery_utils.get_last_signal_from_bigquery(
        tenant_id,
        f"{vibrations_time_dataset}.time",
        current_edge,
        current_perception,
        localized_last_hour.astimezone(pytz.utc),
        now.astimezone(pytz.utc),
        client,
    )
    return element


def plotting_cloud_data_for_condition_perspective(
    format_type,
    element,
    project_data,
    current_perception,
):

    if not element is None:
        for i in project_data["devices"]:
            if i["kind"] == "Icomox":
                sampling_frequency = i["perceptions"][current_perception][
                    "sampling_frequency"
                ]
        if len(element) == 0:
            st.info("No se registran datos")
            return None
        else:
            data = []
            for dimension in range(0, len(element["data"])):
                if format_type == "fft":
                    data_object = FFTPlotter(
                        element["data"][dimension]["values"], None, sampling_frequency
                    )

                else:
                    f, psd = metrics.get_psd(
                        element["data"][dimension]["values"], sampling_frequency
                    )
                    data_object = PSDPlotter(f, psd)
                data.append(data_object)
            plot = plot_per_condition(
                format_type=format_type,
                object_data=data,
                current_perception=current_perception,
            )

            plot.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                height=200,
            )
        return plot
    else:
        pass


def plotting_cloud_data_for_time_perspective(
    project_data,
    current_perception,
    data,
    format_type,
    user
):
    for i in project_data.device_kinds_table.values():
        # TODO: Change this. Not need to iterate since the data is in table form.
        #   We should be able to select things.
        if current_perception == "VibrationMock" and i["kind"] == "Mock":
            sampling_frequency = i["perceptions"][current_perception][
                "sampling_frequency"
            ]

        elif i["kind"] == "Icomox" and current_perception != "VibrationMock":
            sampling_frequency = i["perceptions"][current_perception][
                "sampling_frequency"
            ]

    start = time.perf_counter()
    logging.info(f"Agregando trazos a la gráfica {format_type}")

    x_range = []
    labels = []
    plts = []
    for element in data:
        sub = []
        for dimension in range(0, len(element["data"])):
            if format_type == "fft":
                plt = FFTPlotter(
                    element["data"][dimension]["values"], None, sampling_frequency
                )
            else:
                f, psd = metrics.get_psd(
                    element["data"][dimension]["values"], sampling_frequency
                )
                plt = PSDPlotter(f, psd)
            sub.append(plt)
        plts.append(sub)
        timestamp = change_utc_timezone(element["observation_timestamp"])
        x_range.append(timestamp)
        try:
            labels_data = AnnotationLabel.parse_raw(element["label"])
            labels.append(labels_data.label_value)
        except:
            labels.append(None)

    fig = add_trace(format_type, x_range, plts, current_perception, labels, user)

    camera = dict(eye=dict(x=2, y=2, z=0.1))
    fig.update_layout(
        annotations=[dict(x=0, y=0.75, text=" ", showarrow=False)],
        autosize=False,
        margin=dict(l=0, r=0, t=0, b=0),
        width=650,
        height=650,
        scene=dict(aspectmode="manual", aspectratio=dict(x=2.5, y=1.8, z=1)),
        scene_camera=camera,
    )

    logging.info(f"Se ha agregado todos los trazos a la gráfica {format_type}")
    end = time.perf_counter()

    logging.info(f"Graficar {format_type} tardó {(end - start)}")
    return fig


def plotting_time_data(
    project_data,
    perception,
    vibration_data,
    fft_metrics_df,
    psd_metrics_df,
    user,
    vibration_charts
):
    if not vibration_data is None:
        fft = plotting_cloud_data_for_time_perspective(
            project_data, perception, vibration_data, "fft", user
        )
        vibration_charts.fft_chart = fft
        vibration_charts.fft_metrics_df = fft_metrics_df
        psd = plotting_cloud_data_for_time_perspective(
            project_data, perception, vibration_data, "psd", user
        )
        vibration_charts.psd_chart = psd
        vibration_charts.psd_metrics_df = psd_metrics_df

    else:
        st.info("No se encuentran registros para la fecha y hora seleccionada.")


def get_condition_metrics_dataframe(
    metrics_table, tenant_id, current_edge, current_perception, client
):
    timezone = pytz.timezone("America/Mexico_City")

    last_hour = datetime.datetime.now() - datetime.timedelta(hours=1)
    localized_last_hour = timezone.localize(last_hour)

    now = timezone.localize(datetime.datetime.now())

    df = txp.common.utils.bigquery_utils.get_all_records_within_interval(
        tenant_id,
        metrics_table,
        current_edge,
        current_perception,
        localized_last_hour.astimezone(pytz.utc),
        now.astimezone(pytz.utc),
        "observation_timestamp",
        client,
    )

    return df.tail(1)


def plotting_condition_data(
    vibrations_time_dataset,
    render_card,
    project_data,
    current_perception,
    tenant_id,
    current_edge,
    client,
):
    element = get_element_cloud_to_condition_perspective(
        tenant_id,
        vibrations_time_dataset,
        current_edge,
        current_perception,
        client,
    )
    fft = plotting_cloud_data_for_condition_perspective(
        "fft",
        element,
        project_data,
        current_perception,
    )

    psd = plotting_cloud_data_for_condition_perspective(
        "psd",
        element,
        project_data,
        current_perception,
    )

    fft_metrics = get_condition_metrics_dataframe(
        f"{vibrations_time_dataset}.fft_metrics",
        tenant_id,
        current_edge,
        current_perception,
        client,
    )
    psd_metrics = get_condition_metrics_dataframe(
        f"{vibrations_time_dataset}.psd_metrics",
        tenant_id,
        current_edge,
        current_perception,
        client,
    )
    if fft_metrics.empty and psd_metrics.empty:
        pass
    else:
        strtime = change_utc_timezone(
            fft_metrics["observation_timestamp"].values[0]
        ).strftime("%d/%m/%Y, %H:%M:%S")

        fft_summary_card = Card(
            1,
            1,
            1,
            "Métricas",
            {
                "FFT": strtime,
                "Pico": fft_metrics["peak"].tolist(),
                "RMS": fft_metrics["rms"].tolist(),
                "Desviación estándar": fft_metrics["standard_deviation"].tolist(),
                "Factor de cresta": fft_metrics["crest_factor"].tolist(),
            },
            ["FFT", "Pico", "RMS", "Desviación estándar", "Factor de cresta"],
            vertical_style=False,
        )
        psd_summary_card = Card(
            1,
            1,
            3,
            "Métricas",
            {
                "PSD": pd.to_datetime(fft_metrics["observation_timestamp"]).astype(str),
                "Pico de frecuencia": psd_metrics["peak_frequency"].tolist(),
                "Pico de amplitud": psd_metrics["peak_amplitude"].tolist(),
                "RMS": psd_metrics["rms"].tolist(),
                "Desviacion estandar": psd_metrics["standard_deviation"].tolist(),
                "Factor de cresta": psd_metrics["crest_factor"].tolist(),
            },
            [
                "PSD",
                "Pico de frecuencia",
                "Pico de amplitud",
                "RMS",
                "Desviacion estandar",
                "Factor de cresta",
            ],
            vertical_style=False,
        )
    c = st.empty()
    with c.container():
        if element is not None:
            st.success("Condición del motor: Óptima")
            st.markdown("Datos registrados al momento de último cambio de condición")
            st.markdown("##### FFT")
            st.plotly_chart(fft, use_container_width=True)

            if not fft_metrics.empty:
                render_card([fft_summary_card])

            st.markdown("#### PSD")
            st.plotly_chart(psd, use_container_width=True)
            if not fft_metrics.empty:
                render_card([psd_summary_card])
        else:
            st.info("Sin data para mostrar.")
