from dataclasses import dataclass
from enum import Enum
from string import Template
from typing import Mapping, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
from sklearn import metrics

HAS_PLOTLY = True
try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    HAS_PLOTLY = False

DEFAULT_PLOTLY_MARGIN = {'t': 30, 'l': 0, 'r': 0, 'b': 0}


def check_plotly(func):

    def wrapper(*args, **kwargs):
        if not HAS_PLOTLY:
            raise ImportError(
                "We require Plotly. Consider installing via `pip install plotly`."
            )
        return func(*args, **kwargs)

    return wrapper


@check_plotly
def roc_plot(ys, ys_preds):
    fpr, tpr, thresholds = metrics.roc_curve(ys, ys_preds)
    roc_auc = metrics.auc(fpr, tpr)
    df = pd.DataFrame(np.array([fpr, tpr]).T, columns=["fpr", "tpr"])
    fig = px.line(
        df, x="fpr", y="tpr", title=f'ROC Curve. AUC: {round(roc_auc,2)}'
    )
    fig.show()


@check_plotly
def basic_scatter_plot(
    df: pd.DataFrame,
    x_column_name: str,
    y_column_name: str,
    title: str,
    figsize: Optional[Tuple[int, int]] = (700, 500),
    xlim: Optional[Tuple[int, int]] = None
) -> None:
    fig = px.scatter(
        df,
        x=x_column_name,
        y=y_column_name,
        title=title,
        width=figsize[0],
        height=figsize[1]
    )
    fig.update_layout(margin=DEFAULT_PLOTLY_MARGIN)
    if xlim is not None:
        fig.update_xaxes(range=xlim)
    fig.show()


@check_plotly
def basic_bar_graph(
    df: pd.DataFrame,
    x_column_name: str,
    y_column_name: str,
    title: str,
    figsize: Optional[Tuple[int, int]] = (700, 500),
    orientation='h'
) -> None:
    fig = px.bar(
        df,
        x=x_column_name,
        y=y_column_name,
        title=title,
        orientation=orientation,
        width=figsize[0],
        height=figsize[1]
    )
    fig.update_layout(margin=DEFAULT_PLOTLY_MARGIN)
    fig.show()


def plot_isp(feature, vals, qiis, figsize, xlim):
    df = pd.DataFrame()
    df["Feature Value"] = vals[feature].to_numpy()
    df["Influence"] = qiis[feature].to_numpy()
    basic_scatter_plot(
        df, "Feature Value", "Influence",
        f"Influence Sensitivity Plot: {feature}", figsize, xlim
    )


def plot_pdp(feature, vals, partial_dependencies, figsize, xlim):
    df = pd.DataFrame()
    df["Feature Value"] = vals[feature]
    df["Partial Dependence"] = partial_dependencies[feature]
    basic_scatter_plot(
        df, "Feature Value", "Partial Dependence",
        f"Partial Dependence Plot: {feature}", figsize, xlim
    )


@check_plotly
def stacked_line_chart(
    df: pd.DataFrame,
    x_axis_name: str,
    title: str,
    x_axis_title: str,
    y_axis_title: str,
    minimum_value: float = 0
):
    fig = go.Figure(
        layout={
            "title": {
                "text": title
            },
            "xaxis": {
                "title": {
                    "text": x_axis_title
                }
            },
            "yaxis": {
                "title": {
                    "text": y_axis_title
                }
            }
        }
    )
    x = list(df[x_axis_name])
    for i in df.columns:
        if i == x_axis_name:
            continue
        if max(df[i]) > minimum_value:
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=df[i],
                    hoverinfo='x+y',
                    mode='lines',
                    line=dict(width=0.5),
                    name=i,
                    stackgroup='one'  # define stack group
                )
            )
    fig.show()


@dataclass
class TableCell:
    """Class to represent the content of a cell in a table. See `custom_html_table`
    """
    value: Union[str, float]
    html_class: Optional[str] = None
    url: Optional[str] = None
    sort_order: Optional[int] = None
    is_diff: bool = False
    value_suffix: Optional[str] = None


class DiffResult(Enum):
    INCREASED = "▲"
    DECREASED = "▼"


def custom_html_table(
    title: str,
    column_names: Sequence[str],
    rows: Sequence[Sequence[TableCell]],
    css: Optional[str] = None
) -> str:
    """Returns a html str representation of a nicely formatted table.
        title: Title of the table
        column_names: Sequence of column names
        rows: Each element is a sequence of TableCell with field 'value' and optionally 'html_class' (for styling purpose) and/or 'url' (to create a hyperlink)
            Example of rows: [[{'value': a}, {'value': b, 'html_class': 'custom_id1'}], [{'value': x, 'html_class': 'custom_id2'}, {'value': y, 'url': 'http://truera.com'}]]
        css: Style. Can be used to style individual cell in table (by making use of 'html_class')
            Example of css:
                .custom_id1 { background-color: pink; }
                .custom_id2 { background-color: yellow; }
        }
    """
    MAX_DECIMALS_IN_FLOATS = 4
    html_template = Template(
        """
        <html>
        <head>
        <style>
        table, th, td {
            border-radius: 5px;
        }
        .header {
            font-weight: bold;
            font-size: 14px;
        }
        caption {
            font-weight: bolder;
            font-size: 16px;
            background-color: powderblue;
            color: black;
            border-radius: 5px;
        }
        $css
        </style>
        </head>
        <body>
        <table>
            <caption>$table_title</caption>
            $table_header
            $table_rows
        </table>
        </body>
        </html>
        """
    )
    table_header = '<tr class="header">'
    for i in column_names:
        table_header += f"<td>{i}</td>"
    table_header += "</tr>"

    table_rows = []
    for row in rows:
        tr_str = "<tr>"
        for col in row:
            value = col.value
            if isinstance(value, float) or isinstance(value, int):
                value = round(value, MAX_DECIMALS_IN_FLOATS)
                if col.is_diff:
                    value_str = str(value)
                    if value != 0:
                        value_str = DiffResult.INCREASED.value if value > 0 else DiffResult.DECREASED.value
                        value_str += f" {abs(value)}"
                    value = value_str
            if col.value_suffix:
                value = f"{value} {col.value_suffix}"
            html_class = col.html_class
            url = col.url
            tr_str += "<td "
            if html_class:
                tr_str += f'class="{html_class}">'
            else:
                tr_str += ">"

            if url:
                tr_str += f'<a href="{url}" target="_blank">{value}</a></td>'
            else:
                tr_str += f'{value}</td>'
        tr_str += "</tr>"
        table_rows.append(tr_str)
    table_rows = "".join(table_rows)
    if not css:
        css = ""
    html_str = html_template.substitute(
        table_title=title,
        table_header=table_header,
        table_rows=table_rows,
        css=css
    )
    return html_str
