from inspect import stack
from logging import Logger, getLogger

from dash import html, dcc

import com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.dp_grapher_wid as wid


class TabDebug(html.Div):
    _logger: Logger = getLogger(__name__)

    """
    Return the welcome widget such as:
    <div class="jumbotron">
        <h1>Date Predictability</h1>
        <p class="lead">
            'Predictability' is about accurately predicting early enough the project outcomes (incl. beyond own
            roles and responsibilities), to enable timely corrective actions that increase the likelihood of
            achieving targets and reducing outcome variance.
        </p>
        <hr class="my-2">
        <p>Explanation of how it works here...</p>
    </div>
    """

    def __init__(self):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # ##############################################################################################################
        # Callbacks should be imported here... Otherwise, we face "unknown id" as callbacks get registered even though
        # the widgets are not used...
        # noinspection PyUnresolvedReferences
        import com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.tab_debug.tab_debug_callbacks
        # ##############################################################################################################

        super().__init__(
            children=[
                html.Div(
                    children="Debug",
                    className="bg-secondary",
                    style={
                        "margin-left": "-0.75rem",
                        "margin-right": "-0.75rem",
                        "padding-left": "0.75rem",
                    }
                ),
                html.Div(
                    children=[
                        html.Samp(
                            children=[],
                            style={"font-size": "50%"},
                            id=wid.str_the_wid__debug_as_samp,
                        )
                    ]
                ),
                dcc.Interval(
                    id=wid.str_the_wid__debug_as_interval,
                    interval=1000,  # in milliseconds
                    n_intervals=0
                )
            ],
            id=wid.str_the_wid__debug_as_div,
            className="container border bg-light",
            style={"margin-top": "1rem"}
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
