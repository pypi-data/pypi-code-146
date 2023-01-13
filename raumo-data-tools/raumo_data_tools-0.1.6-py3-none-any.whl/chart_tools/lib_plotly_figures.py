import plotly.graph_objects as go
from plotly.subplots import make_subplots

months = {
    "1": "Januar",
    "2": "Februar",
    "3": "März",
    "4": "April",
    "5": "Mai",
    "6": "Juni",
    "7": "Juli",
    "8": "August",
    "9": "September",
    "10": "Oktober",
    "11": "November",
    "12": "Dezember"
}

def fig_indicator(values,title,subtitle):
    f = go.Figure()

    subtitle = "im " + months[str(values.index[-1].month)] + " " + str(values.index[-1].year)

    f.add_trace(go.Indicator(
        value = values.iloc[-1],
        delta = {'reference': values.iloc[-2], 'relative': True, 'valueformat': ".1%"},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 0, 'column': 0},
        title = {"text": title + "<br><span style='font-size:0.8em;color:gray'>" + subtitle + "</span>"}
        ))

    f.update_layout(
        grid = {'rows': 1, 'columns': 1, 'pattern': "independent"},
        template = {'data' : {'indicator': [{
            'title': {'text': title},
            'mode' : "number+delta",
            'delta' : {'reference': 90}}]
                            }})
    
    return f

def fig_yaxes_many(primary_traces, secondary_traces):
    """Plot figure with several traces on primary and secondary y axes.

    Args:
        primary_traces (list object with go traces): to go on prim y-axis
        secondary_traces (list object go traces): to go on sec y-axis

    Returns:
        _type_: plotly figure object
    """
    f = make_subplots(
        rows=1,cols=1,
        specs=[[{"type": "xy","secondary_y": True}]]
        )

    for trace in primary_traces:
        f.add_trace(trace,
                secondary_y=False,
                row=1, col=1)

    for trace in secondary_traces:
        f.add_trace(trace,
                secondary_y=True,
                row=1, col=1)

    return f


def single_bar_trace(df,col,name):
    trace=go.Bar(x=df.index, y=df[col], name=name)
    return trace

def kpi_trace(df,col,name):
    trace=go.Scatter(x=df.index, y=df[col], name=name)
    return trace

def layout_general(f):
    """_summary_: Update layout

    Args:
        f (plotly figure object): figure to apply layout to
        title (String): Plot title
        xlabel (String): Title of x axis
        ylabel (String): Title of primary y axis
        ylabel2 (String, optional): Title of secondary y axis, if existing. Defaults to None.
    """
    f.update_layout(
        legend_title="",
        font=dict(
            family="Roboto"
        ),
        title_font=dict(
            family="Roboto", 
            size=20
        ),
        legend=dict(
        yanchor="top",
        y=-0.3,
        xanchor="center",
        x=0.5
        ) 
    )

def layout(f, title, xlabel, ylabel, ylabel2=None):
    """_summary_: Update layout

    Args:
        f (plotly figure object): figure to apply layout to
        title (String): Plot title
        xlabel (String): Title of x axis
        ylabel (String): Title of primary y axis
        ylabel2 (String, optional): Title of secondary y axis, if existing. Defaults to None.
    """
    f.update_layout(
        title=title,
        xaxis_showgrid=False, 
        yaxis_showgrid=False,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        legend_title="",
        font=dict(
            family="Roboto"
        ),
        title_font=dict(
            family="Roboto", 
            size=20
        ),
        legend=dict(
        yanchor="top",
        y=-0.3,
        xanchor="center",
        x=0.5
        ) 
    )

    f.update_yaxes(title_text=ylabel, secondary_y=False)
    if ylabel2:
        f.update_yaxes(title_text=ylabel2, tickformat=".2%", secondary_y=True)