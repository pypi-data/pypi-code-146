"""
This module implements the Computer Vision Analytics View for the application.

NOTE: This is just a dummy implementation of a MainView in order to shown the
mechanism provided by the `core_components` package.
"""
import pytz
import txp.common.utils.bigquery_utils
from txp.common.config import settings
from pylab import *
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from txp.common.ml.annotation import AnnotationLabel
from txp.common.utils.authentication_utils import AuthenticationInfo

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


def get_images_and_dates(signals_from_interval):
    if signals_from_interval is not None:
        images = []
        dates = []
        labels = []
        start = time.perf_counter()
        for signal in signals_from_interval:
            ts = signal["observation_timestamp"]
            utc = pytz.timezone("UTC")
            timezone = pytz.timezone("America/Mexico_City")
            date_time = pd.to_datetime(int(ts))
            localized_timestamp = utc.localize(date_time)
            new_timezone = localized_timestamp.astimezone(timezone)
            image = txp.common.utils.bigquery_utils.get_image_from_raw_data(signal["data"])
            if image is not None:
                images.append(image)
                try:
                    labels_data = AnnotationLabel.parse_raw(signal["label"])
                    labels.append(f"{labels_data.label_value}")
                    dates.append(new_timezone.strftime("%H:%M:%S"))
                except:
                    dates.append(new_timezone.strftime("%H:%M:%S"))
                    labels.append(None)
            else:
                pass
        end = time.perf_counter()
        logging.info(
            f"La conversión total de las {len(images)} imagenes tardó {(end - start)}"
        )
        if not images:
            return None, None, None
        else:
            return images, dates, labels
    else:
        logging.info(f"No hay data disponible")
        return None, None, None


def get_animation(user, images, name, step_names, data_format, labels):
    """
    from PIL images shows a plotly fig.
    """
    imgs = []
    dates = []
    annotations = []
    fig = make_subplots(rows=1, cols=1)
    traces_added = False
    img_width = 640
    img_height = 480
    start = time.perf_counter()
    frames = []

    for img, date, label in list(zip(images, step_names, labels)):
        try:
            plot_fig = px.imshow(np.asarray(img))
            imgs.append(plot_fig)
            if not traces_added:
                fig.add_trace(imgs[0].data[0], row=1, col=1)
                traces_added = True
            dates.append(date)
            annotations.append(label)
            if user == AuthenticationInfo.UserRole.Admin:
                if label is not None:
                    layout_i = go.Layout(
                        annotations=[
                            go.layout.Annotation(
                                x=300,
                                y=50,
                                text=label,
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

                frames.append(
                    go.Frame(
                        name=str(date),
                        data=[
                            plot_fig.data[0],
                        ],
                        layout=layout_i,
                    )
                )
            else:
                frames.append(
                    go.Frame(
                        name=str(date),
                        data=[
                            plot_fig.data[0],
                        ],
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
                                "frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True,
                                "transition": {
                                    "duration": 300,
                                    "easing": "quadratic-in-out",
                                },
                            },
                        ],
                        "label": "▶▶",
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
                "pad": {"r": 10, "t": 40},
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
        height=img_height,
        width=img_width,
        margin=dict(l=10, r=10, b=10, t=10, pad=4),
    )
    # Configure axes
    fig.update_xaxes(visible=False)

    fig.update_yaxes(
        visible=False,
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x",
    )
    end = time.perf_counter()
    logging.info(f"La construcción del grafico {data_format} tardó {(end - start)}")
    return fig


def get_images_analysis(
    user,
    normal_data,
    thermographic_data,
    range_time,
    data_format,
    images_data_format,
    timages_data_format,
    animation_data_format,
    images_charts
):
    normal_images, normal_dates, normal_labels = get_images_and_dates(normal_data)
    (
        thermographic_images,
        thermographic_dates,
        thermographic_labels,
    ) = get_images_and_dates(thermographic_data)

    if normal_images:
        images_charts.normal_imgs_chat = get_animation(
            user,
            normal_images,
            images_data_format,
            normal_dates,
            data_format,
            normal_labels,
        )
    else:
        images_charts.normal_imgs_chat = None

    log.info("Normal Images returned")

    if thermographic_images:
        images_charts.thermographic_imgs_datacharts = get_animation(
            user,
            thermographic_images,
            timages_data_format,
            thermographic_dates,
            data_format,
            thermographic_labels,
        )
    else:
        images_charts.thermographic_imgs_datacharts = None

    log.info("Thermographic Images returned")
