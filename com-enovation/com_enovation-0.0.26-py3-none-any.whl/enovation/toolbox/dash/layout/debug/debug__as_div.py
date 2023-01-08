from dash import html, dcc
from inspect import stack
from logging import Logger, getLogger

from dash import callback, Output, Input
from dash.html import P

from com.enovation.toolbox.dash.session import Session
from com.enovation.toolbox.dash.widget import WidgetAsDiv


class DebugAsDiv(WidgetAsDiv):
    _logger: Logger = getLogger(__name__)

    # The widget IDs to be used
    # Naming convention:
    # - should start by "const_str__wid__"
    # - as the application will screen all the widget ids, across widgets, to ensure there is no ambiguity, aka same
    #   widget id across different widgets
    const_str__wid__debug_as_div: str = "enov-content__debug__as_div"
    const_str__wid__debug_as_samp: str = "enov-content__debug__as_samp"
    const_str__wid__debug_as_interval: str = "enov-content__debug__as_interval"
    const_str__wid__debug_as_dcc_store: str = "enov-content__debug__as_dcc_store"

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

    def __init__(
            self,
            dict_config: dict,
            dict_context: dict,
            session: Session,
            *args, **kwargs
    ):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        super().__init__(
            dict_config=dict_config,
            dict_context=dict_context,
            session=session,
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
                            id=self.const_str__wid__debug_as_samp,
                        ),
                    ]
                ),
                dcc.Interval(
                    id=self.const_str__wid__debug_as_interval,
                    interval=1000,  # in milliseconds
                    n_intervals=0
                )
            ],
            id=self.const_str__wid__debug_as_div,
            className="container border bg-light",
            style={"margin-top": "1rem"}
        )

        @callback(
            Output(self.const_str__wid__debug_as_samp, 'children'),
            Input(self.const_str__wid__debug_as_interval, 'n_intervals'),
        )
        def _callback_debug(i_interval_n: int) -> list[P]:
            """
            Callback function to update the debug
            :param i_interval_n: number of seconds since the application started
            :return:
            """
            self._logger.debug(
                f"Function '{stack()[0].filename} - {stack()[0].function}' is called with parameter i_interval_n = "
                f"{i_interval_n}.")

            _lst_str_debug: list[str] = self.session.lst_str_debug_trace

            _lst_the_return: list[P] = [
                P(
                    f">> {i_str}",
                    className="m-0 m-0 p-0"
                ) for i_str in _lst_str_debug
            ]
            self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

            return _lst_the_return

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
