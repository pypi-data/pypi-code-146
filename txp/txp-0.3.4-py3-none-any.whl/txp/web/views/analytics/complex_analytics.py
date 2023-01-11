"""
This module implements the Computer Vision Analytics View for the application.

NOTE: This is just a dummy implementation of a MainView in order to shown the
mechanism provided by the `core_components` package.
"""
import pytz
from txp.common.config import settings
from pylab import *
import pandas as pd
import plotly.express as px
import txp.web.views.analytics.computer_vision_analytics as computer_vision_utils
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from txp.common.utils.authentication_utils import AuthenticationInfo

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


def change_utc_timezone(timestamp):
    utc = pytz.timezone("UTC")
    timezone = pytz.timezone("America/Mexico_City")
    date_time = pd.to_datetime(timestamp)
    localized_timestamp = utc.localize(date_time)
    new_timezone = localized_timestamp.astimezone(timezone)
    return new_timezone.strftime('%Y-%m-%d %H:%M:%S')


def plot_asset_temperatures(temperature_values, temperature_dates, max_min_temp):
    """Creates a scatter plot with only temperature data
    https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scatter.html
    """
    if not temperature_values is None:
        strtimes = temperature_dates

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=strtimes[::-1],
                y=temperature_values[::-1],
                marker=dict(
                    cmax=max_min_temp[0],
                    cmin=max_min_temp[1],
                    size=10,
                    color=temperature_values[::-1],
                    colorscale="portland",
                    colorbar=dict(
                        title="Temperatura",
                        tickvals=max_min_temp,
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

        fig.update_layout(width=900, margin=dict(l=0, r=0, b=0, t=0), showlegend=False)
        fig.update_yaxes(range=max_min_temp)
        return fig
    else:
        return None


def _get_temperatures(signals_from_interval):
    if not signals_from_interval:
        logging.info(f"No hay data disponible")
        return None, None
    else:
        temperatures = []
        dates = []
        start = time.perf_counter()
        for signal in signals_from_interval:
            dates.append(change_utc_timezone(signal["observation_timestamp"]))
            for dimension in signal["data"]:
                temperatures.append(float(dimension["values"][0]))
        end = time.perf_counter()
        logging.info(
            f"La descarga total de las {len(temperatures)} imagenes tardó {(end - start)}"
        )
        return temperatures, dates


def get_complex_bar_animation(
    user, images, name, step_names, temperatures_values, current_machine, labels
):
    """Creates a subplot animation with images and temperature bar chart
     in the same row.
    https://plotly.com/python-api-reference/generated/plotly.subplots.make_subplots.html
    https://plotly.com/python-api-reference/generated/plotly.graph_objects.Bar.html
    https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Image.html
    Its called complex because it displays data of different perceptions.
    """
    if temperatures_values is None:
        fig = make_subplots(rows=1, cols=1)
    else:
        fig = make_subplots(
            rows=1,
            cols=2,
            column_widths=[0.90, 0.10],
            horizontal_spacing=0.15,
            subplot_titles=(f"{name}  \n", "Temperaturas  \n"),
        )

    imgs = []
    dates = []
    annotations = []
    temperatures = []
    traces_added = False
    img_width = 600
    img_height = 600
    frames = []
    spots = [f"{current_machine}"] * len(temperatures_values)

    for i, (img, date, temp, label) in enumerate(list(
        zip(images, step_names, temperatures_values, labels)
    )):
        try:
            plot_fig = px.imshow(np.asarray(img))
            imgs.append(plot_fig)
            if not traces_added:
                fig.add_trace(imgs[0].data[0], row=1, col=1)
                if temperatures_values is not None:
                    fig.add_trace(
                        go.Bar(
                            x=np.asarray(spots[0]),
                            y=np.asarray(temperatures_values[0]),
                            text=temperatures_values[0],
                            textposition="auto",
                        ),
                        row=1,
                        col=2,
                    )
                traces_added = True
            dates.append(date)
            annotations.append(label)
            temperatures.append(temp)

            if user == AuthenticationInfo.UserRole.Admin:
                if label is not None:
                    layout_i = go.Layout(
                        annotations=[
                            go.layout.Annotation(
                                x=0.5,
                                y=0.9,
                                text=label,
                                xref="paper",
                                yref="paper",
                                showarrow=False,
                                font_size=20,
                                font_color="black",
                                bgcolor="white",
                                opacity=0.85,
                            )
                        ]
                    )
                else:
                    layout_i = go.Layout(
                        annotations=[
                            go.layout.Annotation(
                                x=300,
                                y=50,
                                text="Sin etiqueta",
                                showarrow=False,
                                font_size=20,
                                font_color="black",
                                bgcolor="white",
                                opacity=0.85,
                            )
                        ]
                    )
            else:
                layout_i = fig.layout

            if temperatures is not None:
                frames.append(
                    dict(
                        name=str(date),
                        layout=layout_i,
                        data=[
                            plot_fig.data[0],
                            go.Bar(
                                y=np.asarray(temperatures[i]),
                                text=f"{temperatures[i]}°",
                            ),
                        ],
                        traces=[0, 1],
                    )
                )

            else:
                frames.append(
                    dict(
                        name=str(date),
                        layout=layout_i,
                        data=[
                            plot_fig.data[0],
                        ],
                        traces=[0],
                    )
                )
        except Exception as e:
            log.error(f"Error catched: {e}. Probably a truncated image was found.")

    fig.frames = frames
    fig.update_layout(
        sliders=[
            {
                "active": 0,
                "x": 0.1,
                "y": 0,
                "len": 0.9,
                "pad": {"b": 10, "t": 40, "r": 10, "l": 10},
                "steps": [
                    {
                        "args": [
                            [fr.name],
                            {
                                "frame": {"duration": 0, "redraw": True},
                                "mode": "immediate",
                                "fromcurrent": True,
                            },
                        ],
                        "label": fr.name,
                        "method": "animate",
                    }
                    for fr in fig.frames
                ],
            }
        ],
    )

    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [
                            None,
                            {
                                "frame": {"duration": 700, "redraw": True},
                                "fromcurrent": True,
                                "mode": "inmediate",
                                "transition": {
                                    "duration": 0,
                                    "easing": "quadratic-in-out",
                                },
                            },
                        ],
                        "label": "►►",
                        "method": "animate",
                    },
                {
                    "args": [
                        None,
                        {
                            "frame": {"duration": 1200, "redraw": True},
                            "fromcurrent": True,
                            "transition": {
                                "duration": 200,
                                "easing": "quadratic-in-out",
                            },
                        },
                    ],
                    "label": "▶",
                    "method": "animate",
                },
                    {
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 0},
                            },
                        ],
                        "label": "■",
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 15},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top",
            }
        ]
    )
    fig.update_layout(
        margin=dict(l=0, r=100, b=50, t=60), height=img_height, width=img_width
    )

    # Configure axes
    fig.update_xaxes(visible=False, row=1, col=1)
    fig.update_yaxes(
        visible=False,
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x",
        row=1,
        col=1,
    )
    fig.update_yaxes(range=[min(temperatures) - 2, max(temperatures) + 2], row=1, col=2)
    fig.update_xaxes(visible=False, row=1, col=2)

    return fig


def get_images_and_temperature_analysis(
    user,
    normal_data,
    thermographic_data,
    range_time,
    data_format,
    images_data_format,
    timages_data_format,
    animation_data_format,
    temperatures_values,
    temperatures_dates,
    current_machine,
    images_charts,
    temperature_charts,
    max_min_temp
):
    temperature_data_format = "Temperaturas"
    (
        normal_images,
        normal_dates,
        normal_labels,
    ) = computer_vision_utils.get_images_and_dates(normal_data)
    (
        thermographic_images,
        thermographic_dates,
        thermographic_labels,
    ) = computer_vision_utils.get_images_and_dates(thermographic_data)

    if normal_images:
        images_charts.normal_imgs_chat = get_complex_bar_animation(
            user,
            normal_images,
            images_data_format,
            normal_dates,
            temperatures_values,
            current_machine,
            normal_labels,
        )

    else:
        images_charts.normal_imgs_chat = None

    if thermographic_images:
        images_charts.thermographic_imgs_datacharts = get_complex_bar_animation(
            user,
            thermographic_images,
            timages_data_format,
            thermographic_dates,
            temperatures_values,
            current_machine,
            thermographic_labels,
        )

    else:
        images_charts.thermographic_imgs_datacharts = None

    if temperatures_values:
        temperature_charts.temp_chart = plot_asset_temperatures(
            temperatures_values, temperatures_dates, max_min_temp
        )
    else:
        temperature_charts.temp_chart = None
