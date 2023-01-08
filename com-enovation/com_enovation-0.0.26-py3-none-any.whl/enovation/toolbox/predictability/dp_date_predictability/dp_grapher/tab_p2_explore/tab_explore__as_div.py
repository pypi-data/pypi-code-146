from inspect import stack
from logging import Logger, getLogger

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.html import Div

from com.enovation.toolbox.predictability.bean import PredictabilityBean
from com.enovation.toolbox.predictability.dp_date_predictability.dp_computer import DatePredictabilityComputer
from com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.dp_grapher_session import Session
import com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.dp_grapher_wid as wid


class TabExploreAsDiv(Div):
    """
    """
    _logger: Logger = getLogger(__name__)

    def __init__(self):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # ##############################################################################################################
        # Callbacks should be imported here... Otherwise, we face "unknown id" as callbacks get registered even though
        # the widgets are not used...
        # noinspection PyUnresolvedReferences
        import com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.tab_p2_explore.\
            tab_explore_callbacks
        # ##############################################################################################################

        # We retrieve the predictability bean
        obj_the_predictability_bean: PredictabilityBean = Session.get_predictability_bean()

        super().__init__(
            children=[
                # A title
                html.H3("Zoom on a given key"),

                # The filter to select a key (aka. a project, an opportunity, etc) to graph and zoom in
                dcc.Dropdown(
                    id=wid.str_the_wid__explore__key__as_drop_down,
                    placeholder="Select a key to graph and zoom in...",
                    options=[
                        {'label': x, 'value': x}
                        for x in
                        obj_the_predictability_bean.df_by_key[DatePredictabilityComputer.str__input__column_label__key]
                    ],
                ),

                html.Div(
                    children=[
                        html.Div(
                            id=wid.str_the_wid__explore__graph__as_div,
                            # by default, no key is selected, so the graph and table are not displayed
                            # style={"display": "none"},
                            children=[
                                dcc.Graph(id=wid.str_the_wid__explore__graph__as_graph)
                            ]
                        ),
                        html.Div(
                            id=wid.str_the_wid__explore__table__as_div,
                            children=[
                                # The table
                                dbc.Table(
                                    html.Tbody([
                                        html.Tr(
                                            [
                                                html.Td(i_col),
                                                html.Td(
                                                    "--",
                                                    id=(
                                                            wid.str_the_wid__explore__table__prefix_to_access_columns +
                                                            i_col +
                                                            wid.str_the_wid__explore__table__suffix_to_access_columns
                                                    )
                                                )
                                            ]
                                        )
                                        for i_col in obj_the_predictability_bean.df_by_key.columns
                                    ]),
                                    color="primary",
                                    bordered=True
                                )
                            ],
                            # by default, no key is selected, so the graph and table are not displayed
                            # style={"display": "none"}
                        ),
                    ]
                )
            ],
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
