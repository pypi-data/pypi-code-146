import base64

from dash import dcc, callback, Output, Input, no_update

import dash_bootstrap_components as dbc

from inspect import stack
from logging import Logger, getLogger

from dash import html
from urllib.parse import unquote

from com.enovation.toolbox.dash.session import Session
from com.enovation.toolbox.dash.sheet import Sheet, SheetAsDiv
from com.enovation.toolbox.dash.widget import Widget


class NavigationAsNavbar(Widget, dbc.Navbar):

    _logger: Logger = getLogger(__name__)

    # ##################################################################################################################
    # CONSTANTS
    # ##################################################################################################################

    const_str_default_navbar_brand: str = "eNOVAtion"
    const_str_default_str_logo: str = "images/com-enovation.square.png"

    # The labels in the configuration file
    const_str__config_label__dict_properties: str = "properties"
    const_str__config_label__str_navbar_brand: str = "navbar_brand"
    const_str__config_label__url_logo: str = "logo"
    const_str__config_label__str_title: str = "title"

    # The wid for the default generic widgets
    const_str__wid__div_debug: str = "debug"
    const_str__wid__location_url: str = "url"
    const_str__wid__navbar_header: str = "header"

    """ 
    Return the navigation bar, along with the callback function to load the enov-content__as_main part
    - An image as the logo
    - A brand, which is used as well as the title for the logo
    - Menus to various widgets available.

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

    def __init__(
            self,
            dict_sheet: dict[str, Sheet],
            dict_config: dict,
            dict_context: dict,
            str__wid__main_content: str,
            session: Session
    ):

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _str_the_title: str = dict_config.get(
            self.const_str__config_label__dict_properties, {}
        ).get(self.const_str__config_label__str_title, self.const_str_default_navbar_brand)

        if self.const_str__config_label__url_logo in dict_config.get(
                self.const_str__config_label__dict_properties, {}
        ):
            _img_the_logo: html.Img = html.Img(
                src='data:image/png;base64,{}'.format(
                    base64.b64encode(
                        open(
                            dict_config[
                                self.const_str__config_label__dict_properties
                            ][
                                self.const_str__config_label__url_logo
                            ],
                            'rb'
                        ).read()
                    )
                ),
                height="30px",
                title=_str_the_title
            )
        else:
            _img_the_logo: html.Img = html.Img(
                src=session.dash_application.dash_server.get_asset_url(self.const_str_default_str_logo),
                height="30px",
                title=_str_the_title
            )

        Widget.__init__(
            self,
            dict_config=dict_config,
            dict_context=dict_context,
            session=session
        )

        dbc.Navbar.__init__(
            self,
            children=[
                # To get the url loaded
                dcc.Location(id=self.const_str__wid__location_url),

                dbc.NavItem(
                    html.A(
                        dbc.Row(
                            [
                                dbc.Col(_img_the_logo),
                                dbc.Col(
                                    dbc.NavbarBrand(dict_config.get(
                                        self.const_str__config_label__dict_properties, {}
                                    ).get(
                                        self.const_str__config_label__str_navbar_brand,
                                        self.const_str_default_navbar_brand)
                                    )
                                ),
                            ],
                            align="center",
                        ),
                        href="https://pypi.org/project/com-enovation/"
                    )
                )
            ] + [
                dbc.NavItem(dbc.NavLink(i_widget, href="#"+i_widget))
                for i_widget in dict_sheet
            ] + [
                dbc.NavItem(dbc.NavLink("The default dp_grapher for the date predictability module...", disabled=True))
            ],
            color="dark",
            dark=True,
            id=self.const_str__wid__navbar_header,
            className="fixed-top"
        )

        @callback(
            Output(str__wid__main_content, 'children'),
            Input(self.const_str__wid__location_url, 'hash'),
            prevent_initial_call=True
        )
        def _callback_navigate_and_load_content(url_hash: str) -> html.Div:
            """
            Callback function:
            - When we click in a menu in the navigation bar, it refreshes the page with an updated URL
              "https://xxx/#whatever"
            - When such URL update happens, the widget "url as location" is refreshed
            - Using this refresh, we load the area "content as main" with the new target widget.

            :param url_hash: the link to an element with a specified id within the page
            :return: the widget to load in the area "content as main"
            """
            getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

            if url_hash == '':
                return no_update

            _dict_the_sheets: dict[str, SheetAsDiv] = self.session.dash_application.dict_sheets

            if unquote(url_hash)[1:] not in _dict_the_sheets:
                raise Exception(f"Unexpected url_hash '{unquote(url_hash)}'.")

            div_the_return: html.Div = _dict_the_sheets[unquote(url_hash)[1:]]

            self.session.debug(
                debug_trace=f"Click navigation menus to update main content: {unquote(url_hash)}, returned an "
                            f"object of type '{type(div_the_return)}'"
            )

            getLogger(__name__).debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

            return div_the_return

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
