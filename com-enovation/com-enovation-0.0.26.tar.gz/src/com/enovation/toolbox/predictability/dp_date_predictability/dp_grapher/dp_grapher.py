import os
from inspect import stack
from logging import Logger, getLogger
from pathlib import Path

from dash import Dash
import dash.html as html
import dash_bootstrap_components as dbc
from dash import dcc

import com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.dp_grapher_wid as wid
from com.enovation.toolbox.predictability.bean import PredictabilityBean
from com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.dp_grapher_session import Session
from com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.tab_debug.tab_debug__as_div import TabDebug
from com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.tab_p1_welcome.tab_welcome__as_div \
    import TabWelcomeAsDiv


class DpGrapher_DashApplication:
    _logger: Logger = getLogger(__name__)

    # CONSTANTS
    # Link to the directory "assets", where web site's assets are stored (css, pictures, etc)
    str_the_relative_path_to_assets: str = '../../../../../../../assets/'
    # The application name
    str_the_application_title: str = "com.enovation"

    # The Dash application
    _dash_app: Dash = None

    # Debug
    _b_debug: bool = False

    def __init__(
            self,
            obj_predictability: PredictabilityBean,
            b_debug: bool = False,
    ):
        """
        We instantiate the dash application, along with the different widgets, including their callbacks
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # ##############################################################################################################
        # Callbacks should be imported here... Otherwise, we face "unknown id" as callbacks get registered even though
        # the widgets are not used...
        # noinspection PyUnresolvedReferences
        import com.enovation.toolbox.predictability.dp_date_predictability.dp_grapher.dp_grapher_callbacks
        # ##############################################################################################################

        self._b_debug = b_debug

        Session.set_predictability_bean(obj_predictability_bean=obj_predictability)
        Session.debug(
            f"'{stack()[0].filename} - {stack()[0].function}' loaded a predictability bean with the following "
            f"characteristics:"
            f"\n\t- df_by_key:"
            f"\n\t\t- shape: {obj_predictability.df_by_key.shape}"
            f"\n\t\t- columns: {obj_predictability.df_by_key.columns}"
            f"\n\t- df_by_measure:"
            f"\n\t\t- shape: {obj_predictability.df_by_measure.shape}"
            f"\n\t\t- columns: {obj_predictability.df_by_measure.columns}"
            f"\n\t- df_historical:"
            f"\n\t\t- shape: {obj_predictability.df_historical.shape}"
            f"\n\t\t- columns: {obj_predictability.df_historical.columns}"
        )

        # We check that the directory "assets" exists...
        if not Path(__file__, "../", self.str_the_relative_path_to_assets).resolve().is_dir():
            raise Exception(
                f'When trying to instantiate the Dash application, we could not find the directory assets":'
                f'\n\t- From current file path "{Path(__file__)}"'
                f'\n\t- Adding relative path "{self.str_the_relative_path_to_assets}"'
                f'\n\t- Leading to non existing directory '
                f'"{Path(__file__, "../", self.str_the_relative_path_to_assets).resolve()}'
            )

        # We instantiate the Dash application
        self._dash_app = Dash(
            name=__name__,
            assets_folder=os.path.join(os.path.dirname(__file__), self.str_the_relative_path_to_assets),
            external_stylesheets=[
                dbc.themes.JOURNAL,
            ],
            title=self.str_the_application_title,
            suppress_callback_exceptions=True
        )

        # We instantiate the main widgets
        self._widget_header__as_navbar = self._instantiate_widget__enov_header__as_navbar()
        self._widget_footer__as_footer = self._instantiate_widget__enov_footer__as_footer()
        self._widget_content__debug__as_div = TabDebug()

        # We eventually instantiate the overall layout to load
        self._dash_app.layout = self._instantiate_widget__enov_layout__as_div()

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

    def _instantiate_widget__enov_layout__as_div(self) -> html.Div:
        """
        Return the overall layout for the application.

        The produced HTML is of this kind:
        TODO
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # We instantiate the navbar
        div_the_return: html.Div = html.Div([

            # To get the url loaded
            dcc.Location(id=wid.str_the_wid__url_as_location),

            # The navigation bar at the top of the screen
            self._widget_header__as_navbar,

            # The main page in a container
            dbc.Container(
                children=[
                    html.Main(
                        id=wid.str_the_wid__content_as_main,
                        className="container",
                        children=TabWelcomeAsDiv()
                    ),
                    self._widget_content__debug__as_div,
                ],
            ),

            # The footer
            self._widget_footer__as_footer
        ])
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return div_the_return

    def _instantiate_widget__enov_header__as_navbar(self) -> dbc.Navbar:
        """
        Return the navigation bar, along with the callback function to load the enov-content__as_main part.

        The produced HTML is of this kind:
        <nav id="enov-header__as_navbar" class="fixed-top navbar navbar-expand-md navbar-dark bg-dark">
            <div class="nav-item">
                <a href="https://pypi.org/project/com-enovation/">
                    <div class="align-items-center row">
                        <div class="col">
                            <img height="30px" src="/assets/images/com-enovation.square.png" title="com.enovation">
                        </div>
                        <div class="col">
                            <span class="navbar-brand">eNOVAtion</span>
                        </div>
                    </div>
                </a>
            </div>
            <div class="nav-item">
                <a href="#welcome" class="nav-link">welcome</a>
            </div>
            <div class="nav-item">
                <a href="#explore" class="nav-link">explore</a>
            </div>
            <div class="nav-item">
                <a class="nav-link disabled" disabled="">The default dp_grapher for date predictability module...</a>
            </div>
        </nav>
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # We instantiate the navbar
        nav_the_return: dbc.Navbar = dbc.Navbar(
            children=[
                dbc.NavItem(
                    html.A(
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Img(
                                        src=self._dash_app.get_asset_url("images/com-enovation.square.png"),
                                        height="30px",
                                        title=self.str_the_application_title
                                    )
                                ),
                                dbc.Col(dbc.NavbarBrand("eNOVAtion")),
                            ],
                            align="center",
                        ),
                        href="https://pypi.org/project/com-enovation/"
                    )
                ),
                dbc.NavItem(dbc.NavLink("welcome", href="#welcome")),
                dbc.NavItem(dbc.NavLink("explore", href="#explore")),
                dbc.NavItem(dbc.NavLink("The default dp_grapher for the date predictability module...", disabled=True))
            ],
            color="dark",
            dark=True,
            id=wid.str_the_wid__header_as_navbar,
            className="fixed-top"
        )

        return nav_the_return

    def _instantiate_widget__enov_footer__as_footer(self) -> html.Footer:
        """
        Return the footer such as:
        <footer class="footer" id="enov-footer__as_footer">
            <div class="container">
                <span class="text-muted">Copyright © 2022 Jean-Sébastien Guillard. All rights reserved.</span>
            </div>
        </footer>
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # We instantiate the footer
        footer_the_return: html.Footer = html.Footer(
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
            className="footer",
            id=wid.str_the_wid__footer_as_footer,
        )
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

        return footer_the_return

    def graph_predictability(
            self,
    ):
        """
        Main function call to instantiate and launch dash application.
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")
        self._dash_app.run_server(debug=True, use_reloader=False)
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
