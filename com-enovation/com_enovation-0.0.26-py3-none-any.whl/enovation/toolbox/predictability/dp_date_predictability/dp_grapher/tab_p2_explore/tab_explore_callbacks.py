import json
from datetime import datetime

import dash
from dash._callback_context import CallbackContext
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots

from inspect import stack
from logging import Logger, getLogger

from dash import callback, Output, Input
from plotly.graph_objs import Figure, Scatter
import com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.dp_grapher_wid as wid
from com.enovation.toolbox.predictability.dp_date_predictability.dp_computer import DatePredictabilityComputer
from com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.dp_grapher_session import Session
from com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.tab_p2_explore.tab_explore__data_to_print \
    import DataToGraph, DataToTable


@callback(
    Output(wid.str_the_wid__explore__graph__as_graph, 'figure'),
    [
        Output(
            wid.str_the_wid__explore__table__prefix_to_access_columns +
            i_col +
            wid.str_the_wid__explore__table__suffix_to_access_columns,
            'children'
        )
        for i_col in DatePredictabilityComputer.lst__output__statistics_by_key__column_labels
    ],

    Input(wid.str_the_wid__explore__key__as_drop_down, 'value'),
    Input(wid.str_the_wid__explore__graph__as_graph, 'clickData'),
    prevent_initial_call=True
)
def _callback_to_update_graph(
        str_key: str,
        dict_click: dict
) -> list:
    """
    There are 2 events that could result in updating the graph:
    - We select in the drop down a new key: the whole graph is refreshed
    - We zoom into a predictability data point: in the upper graph, we click on the predictability curve. As a result
      this data point is emphasized, and the bottom part is refreshed
    :param str_key:
    :param dict_click:
    :return: the refreshed figure to display
    """

    _logger: Logger = getLogger(__name__)

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

    # We first determine which widget did trigger this callback
    str_the_trigger: str = _get_triggerer(log_the_logger=_logger)

    # If the trigger is the drop down "key": str_the_wid__explore__key__as_drop_down
    if str_the_trigger == wid.str_the_wid__explore__key__as_drop_down:

        Session.debug(f"User selected the key '{str_key}'.")

        # We prepare the data to easily build the figure and table to display
        obj_the_data_to_graph: DataToGraph = DataToGraph(
            obj_predictability=Session.get_predictability_bean(),
            str_filter_on_key=str_key,
        )
        fig_the_return: Figure = _instantiate_figure_to_return(
            log_the_logger=_logger,
            obj_the_data_to_graph=obj_the_data_to_graph
        )

        obj_the_data_to_table: DataToTable = DataToTable(
            obj_predictability=Session.get_predictability_bean(),
            str_filter_on_key=str_key,
        )
        lst_the_return: list = _instantiate_table_to_return(
            log_the_logger=_logger,
            obj_the_data_to_table=obj_the_data_to_table
        )

    # Else, the trigger is a click in the graph: str_the_wid__explore__graph__as_graph
    elif str_the_trigger == wid.str_the_wid__explore__graph__as_graph:

        # We prepare the data to easily build the figure and table to display
        obj_the_data_to_graph: DataToGraph = DataToGraph(
            obj_predictability=Session.get_predictability_bean(),
            str_filter_on_key=str_key,
            dt_as_of_date=datetime.strptime(
                dict_click["points"][0]["x"],
                '%Y-%m-%d'
            )
        )
        fig_the_return: Figure = _instantiate_figure_to_return(
            log_the_logger=_logger,
            obj_the_data_to_graph=obj_the_data_to_graph
        )

        obj_the_data_to_table: DataToTable = DataToTable(
            obj_predictability=Session.get_predictability_bean(),
            str_filter_on_key=str_key,
            dt_as_of_date=datetime.strptime(
                dict_click["points"][0]["x"],
                '%Y-%m-%d'
            )
        )
        lst_the_return: list = _instantiate_table_to_return(
            log_the_logger=_logger,
            obj_the_data_to_table=obj_the_data_to_table
        )

        fig_the_return.add_vline(
            x=datetime.strptime(
                dict_click["points"][0]["x"],
                '%Y-%m-%d'
            )
        )

    # Else, the trigger is unknown
    else:
        _logger.error(f"Callback triggerer is '{str_the_trigger}', which is not expected. We return PreventUpdate, as "
                      f"we do not know what to do...")
        raise PreventUpdate()

    return [fig_the_return] + lst_the_return


def _instantiate_table_to_return(
        log_the_logger: Logger,
        obj_the_data_to_table: DataToTable
) -> list[str]:
    log_the_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

    # Little bit of formatting...

    # Predictability as percentage
    obj_the_data_to_table.dict_values[
        DatePredictabilityComputer.str__statistics__column_label__predictability_last
    ] = "{:.0%}".format(
        obj_the_data_to_table.dict_values[
            DatePredictabilityComputer.str__statistics__column_label__predictability_last
        ]
    )

    # Dates as dd-mmm-yyyy
    for i_date in [
        DatePredictabilityComputer.str__statistics__column_label__date_first,
        DatePredictabilityComputer.str__statistics__column_label__date_last,
        DatePredictabilityComputer.str__statistics__column_label__measure_min,
        DatePredictabilityComputer.str__statistics__column_label__measure_max,
        DatePredictabilityComputer.str__statistics__column_label__measure_first,
        DatePredictabilityComputer.str__statistics__column_label__measure_last,
    ]:
        obj_the_data_to_table.dict_values[i_date] = obj_the_data_to_table.dict_values[i_date].strftime("%d-%b-%Y")

    lst_the_return: list[str] = [
        obj_the_data_to_table.dict_values[i_col]
        for i_col in DatePredictabilityComputer.lst__output__statistics_by_key__column_labels
    ]

    log_the_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

    return lst_the_return


def _instantiate_figure_to_return(
        log_the_logger: Logger,
        obj_the_data_to_graph: DataToGraph
) -> Figure:
    log_the_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

    # We instantiate the Figure object that will be rendered
    # It contains two parts:
    # - Row 1, the predictability over time
    # - Row 2, the measures and details leading to compute the predictability
    fig_the_return = make_subplots(
        rows=2,
        cols=1,
        vertical_spacing=0.02,
        shared_xaxes=True
    )

    # Add figure title
    fig_the_return.update_layout(
        title_text=obj_the_data_to_graph.str_figure_title
    )

    # We trace the predictability
    fig_the_return.add_trace(
        Scatter(
            x=obj_the_data_to_graph.s_predictabilities_dates,
            y=obj_the_data_to_graph.s_predictabilities_values,
            name=obj_the_data_to_graph.str_predictabilities_ordinate_label,
        ),
        row=1, col=1
    )

    # We trace the measures
    fig_the_return.add_trace(
        Scatter(
            x=obj_the_data_to_graph.s_measures_dates,
            y=obj_the_data_to_graph.s_measures_values,
            name=obj_the_data_to_graph.str_measures_name,
        ),
        row=2, col=1
    )

    # We trace the cone: the increasing, the decreasing and the final (as the horizontal line)
    fig_the_return.add_trace(
        Scatter(
            x=obj_the_data_to_graph.lst_increasing_cone_dates,
            y=obj_the_data_to_graph.lst_increasing_cone_values,
            name=obj_the_data_to_graph.str_increasing_cone_name,
        ),
        row=2, col=1
    )
    fig_the_return.add_trace(
        Scatter(
            x=obj_the_data_to_graph.lst_decreasing_cone_dates,
            y=obj_the_data_to_graph.lst_decreasing_cone_values,
            name=obj_the_data_to_graph.str_decreasing_cone_name,
        ),
        row=2, col=1
    )
    fig_the_return.add_trace(
        Scatter(
            x=obj_the_data_to_graph.lst_last_measure_dates,
            y=obj_the_data_to_graph.lst_last_measure_values,
            name=obj_the_data_to_graph.str_last_measure_name,
        ),
        row=2, col=1
    )

    # Set axis titles
    fig_the_return.update_xaxes(title_text=obj_the_data_to_graph.str_abscissa_label)
    fig_the_return.update_yaxes(
        title_text=obj_the_data_to_graph.str_predictabilities_ordinate_label,
        row=1, col=1,
        range=[0, 1]
    )
    fig_the_return.update_yaxes(
        title_text=obj_the_data_to_graph.str_measures_ordinate_label,
        row=2, col=1
    )

    fig_the_return.update_traces(mode='lines', hovertemplate=None)
    fig_the_return.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))

    log_the_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
    return fig_the_return


def _get_triggerer(log_the_logger: Logger) -> str:
    """
    Function that get from the dash context the widget ID that triggered the callback.

    Assumption: there is one and only trigger trigger.
    - If no trigger (or empty): we return PreventUpdate
    - If more than one trigger: only the first one is processed, and an error message is logged

    :param log_the_logger:
    :return: the widget id that triggered the callback
    """
    log_the_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

    ctx_the_dash_context: CallbackContext = dash.callback_context

    str_the_event: str = json.dumps(
        {
            'states': ctx_the_dash_context.states,
            'triggered': ctx_the_dash_context.triggered,
            'inputs': ctx_the_dash_context.inputs
        },
        indent=2
    )

    # If function called without any trigger, this is unexpected. We raise an error, and return "no_update"
    if not ctx_the_dash_context.triggered:
        log_the_logger.error(
            f"Function '{stack()[0].filename} - {stack()[0].function}' called while no trigger.\n{str_the_event}")
        raise PreventUpdate()

    # If the triggered property is not as expected
    if len(ctx_the_dash_context.triggered) < 1:
        log_the_logger.error(
            f"Property 'triggered' contains {len(ctx_the_dash_context.triggered)} record, while one is expected. "
            f"No update could be performed.\n{str_the_event}")
        raise PreventUpdate()
    if len(ctx_the_dash_context.triggered) > 1:
        log_the_logger.error(
            f"Property 'triggered' contains {len(ctx_the_dash_context.triggered)} records, while one is expected. "
            f"Only the first triggered element will be processed.\n{str_the_event}")

    # We get the source of the event
    str_the_trigger = ctx_the_dash_context.triggered[0]['prop_id'].split('.')[0]

    log_the_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning '{str_the_trigger}'.")

    return str_the_trigger
