from inspect import stack
from logging import Logger, getLogger

from dash import html

from com.enovation.toolbox.dash.session import Session
from com.enovation.toolbox.dash.widget import Widget


class FooterAsFooter(Widget, html.Footer):
    """

    Return the footer such as:
    <footer class="footer" id="enov-footer__as_footer">
        <div class="container">
            <span class="text-muted">Copyright © 2022 Jean-Sébastien Guillard. All rights reserved.</span>
        </div>
    </footer>
    """
    _logger: Logger = getLogger(__name__)

    # The widget IDs to be used
    # Naming convention:
    # - should start by "const_str__wid__"
    # - as the application will screen all the widget ids, across widgets, to ensure there is no ambiguity, aka same
    #   widget id across different widgets
    const_str__wid__footer_footer: str = "footer"

    def __init__(
            self,
            dict_config: dict,
            dict_context: dict,
            session: Session
    ):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        Widget.__init__(
            self,
            dict_config=dict_config,
            dict_context=dict_context,
            session=session
        )

        html.Footer.__init__(
            self,

            children=[
                html.Div(
                    [
                        html.Span(
                            [
                                "Copyright © 2022 Jean-Sébastien Guillard. All rights reserved."
                            ],
                            className="text-muted"
                        )
                    ],
                    className="container",
                ),
            ],
            className="footer",
            id=self.const_str__wid__footer_footer,

        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
