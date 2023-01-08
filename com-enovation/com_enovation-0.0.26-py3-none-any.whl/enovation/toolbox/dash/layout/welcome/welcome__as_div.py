from inspect import stack
from logging import Logger, getLogger
from dash import html

from com.enovation.toolbox.dash.session import Session
from com.enovation.toolbox.dash.widget import WidgetAsDiv


class WelcomeAsDiv(WidgetAsDiv):
    """
    Return the welcome widget such as:
    <div class="jumbotron">
        <h1>Welcome Dude!</h1>
        <p class="lead">
            Welcome to the com.enovation application, powered by Dash and Plotly.
        </p>
        <hr class="my-2">
        <p>Explanation of how it works here...</p>
    </div>
    """
    _logger: Logger = getLogger(__name__)

    def __init__(
            self,
            dict_config: dict,
            dict_context: dict,
            session: Session
    ):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")
        super().__init__(
            dict_config=dict_config,
            dict_context=dict_context,
            session=session,
            children=[
                html.H1("Welcome Dude!"),
                html.P(
                    "Welcome to the com.enovation application, powered by Dash and Plotly.",
                    className="lead",
                ),
                html.Hr(className="my-2"),
                html.P(
                    "Explanation of how it works here..."
                )
            ],
            className="jumbotron",
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
