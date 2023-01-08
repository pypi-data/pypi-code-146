from inspect import stack
from logging import Logger, getLogger

from dash import html

from com.enovation.toolbox.dash.layout.debug.debug__as_div import DebugAsDiv
from com.enovation.toolbox.dash.layout.footer.footer__as_footer import FooterAsFooter
from com.enovation.toolbox.dash.layout.navigation.navigation__as_navbar import NavigationAsNavbar
from com.enovation.toolbox.dash.layout.welcome.welcome__as_div import WelcomeAsDiv
from com.enovation.toolbox.dash.session import Session
from com.enovation.toolbox.dash.sheet import Sheet
import dash_bootstrap_components as dbc

from com.enovation.toolbox.dash.widget import WidgetAsDiv


class LayoutAsDiv(WidgetAsDiv):
    _logger: Logger = getLogger(__name__)

    @property
    def dict_sheets(self) -> dict[str, Sheet]:
        return self._dict_sheets

    # The widget IDs to be used
    # Naming convention:
    # - should start by "const_str__wid__"
    # - as the application will screen all the widget ids, across widgets, to ensure there is no ambiguity, aka same
    #   widget id across different widgets
    const_str__wid__main_content: str = "content"

    def __init__(
            self,
            dict_sheets: dict[str, Sheet],
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

                # The navigation bar at the top of the screen
                NavigationAsNavbar(
                    dict_sheet=dict_sheets,
                    str__wid__main_content=self.const_str__wid__main_content,
                    dict_config=dict_config,
                    dict_context=dict_context,
                    session=session
                ),

                # The main page in a container
                dbc.Container(
                    children=[
                        html.Main(
                            id=self.const_str__wid__main_content,
                            className="container",
                            children=WelcomeAsDiv(
                                dict_config=dict_config,
                                dict_context=dict_context,
                                session=session
                            ),
                        ),

                        DebugAsDiv(
                            dict_config=dict_config,
                            dict_context=dict_context,
                            session=session,
                        ),
                    ],
                ),

                # The footer
                FooterAsFooter(
                    dict_config=dict_config,
                    dict_context=dict_context,
                    session=session
                )
            ])

        self._dict_sheets = dict_sheets

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
