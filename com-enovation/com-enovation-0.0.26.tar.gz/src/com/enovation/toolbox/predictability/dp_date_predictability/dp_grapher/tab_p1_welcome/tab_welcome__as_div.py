from inspect import stack
from logging import Logger, getLogger
from dash import html
from dash.html import Div


class TabWelcomeAsDiv(Div):
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
    _logger: Logger = getLogger(__name__)

    def __init__(self):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")
        super().__init__(
            children=[
                html.H1("Date Predictability"),
                html.P(
                    "'Predictability' is about accurately predicting early enough the project outcomes "
                    "(incl. beyond own roles and responsibilities), to enable timely corrective actions "
                    "that increase the likelihood of achieving targets and reducing outcome variance.",
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
