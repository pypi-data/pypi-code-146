import os
from inspect import stack
from logging import Logger, getLogger
from pathlib import Path

from dash import Dash
import dash_bootstrap_components as dbc

from com.enovation.toolbox.dash.layout.layout.layout__as_div import LayoutAsDiv
from com.enovation.toolbox.dash.session import Session
from com.enovation.toolbox.dash.sheet import SheetAsDiv
from com.enovation.toolbox.dash.widget import Widget
from com.enovation.toolbox.dash.widgets.bubbles.bubbles__as_div import BubblesAsDiv
from typing import Type, Optional


class DashApplication:
    """
    The master dash application, that can be called from command lines.

    The "__init__" function prepares the framework:
    - TODO: Consolidate the list of all widgets: the default ones from com.enovation, and the ones implemented outside
    - TODO: Instantiate the ConfigChecker: used whenever the application is launched to check the application and
      widgets configurations are correct

    Then, the function "launch" launches the application:
    - TODO: Instantiate the sheets containing one or more widget(s)
    - TODO: Instantiate the dash application, and launch it

    The application is composed of 3 parts:
    - The header navbar, that contains menus to navigate across the sheets
    - The content, which displays a sheet (which itself contains widgets)
    - The footer, which contains some additional information.

    Application is configured as a json:
        {
            "properties": {
                ... the dash application properties ...
                "str_url_brand_logo": ... the url to the logo ...
                "str_brand": ... the title/ brand name that is used as the title to the logo and in the navbar ...
                "str_url_brand_site": ... the url to the brand website ...
            },
            "sheets": {
                "a name for the sheet": {
                    "properties": {
                        ... the sheet properties ...
                    },
                    "widgets": [
                        {
                            "id": "the widget id (aka "$id" from the json schema) to instantiate",
                            "properties": {
                                ... the widget properties ...
                            }
                        }
                    ]
                }
            }
        }

    """
    _logger: Logger = getLogger(__name__)

    # ##################################################################################################################
    # CONSTANTS
    # ##################################################################################################################

    # Link to the directory "assets", where web site's assets are stored (css, pictures, etc)
    const_str_relative_path_to_assets: str = '../../../../../assets/'

    # The labels in the configuration file
    const_str__config_label__dict_properties: str = "properties"
    const_str__config_label__dict_sheets: str = "sheets"
    const_str__config_label__list_widgets: str = "widgets"

    const_str__config_label__str_url_brand_logo: str = "str_url_brand_logo"
    const_str__config_label__str_brand: str = "str_brand"
    const_str__config_label__str_url_brand_site: str = "str_url_brand_site"

    const_str__config_label__str_widget_id: str = "id"

    # The wid for the default generic widgets
    const_str__wid__navbar_navbar: str = "navbar"
    const_str__wid__div_debug: str = "debug"
    const_str__wid__footer_footer: str = "footer"

    # ##################################################################################################################
    # INSTANCE PROPERTIES
    # ##################################################################################################################

    @property  # The instance of the Dash server
    def dash_server(self) -> Dash:
        return self._dash_server

    @property  # Whether in the layout, we trace debug messages
    def b_debug(self) -> bool:
        return self._b_debug

    # This is the repository of all the possible widgets:
    # - The ones proposed by com.enovation packaging
    # - Along with the custom ones that are provided while instantiating the dash application.
    # It is structured as a dictionary:
    # - Key: the widget id (aka "$id" from the json schema)
    # - Value: the widget class
    @property
    def dict_widgets_implementations_repository(self) -> dict[str, Type[Widget]]:
        return self._dict_widgets_implementations_repository

    @property
    def dict_config(self) -> dict:
        return self._dict_config

    @property
    def dict_context(self) -> dict:
        return self._dict_context

    @property
    def dict_sheets(self) -> dict[str, SheetAsDiv]:
        return self._dict_sheets

    @property
    def session(self) -> Session:
        return self._session

    def __init__(
            self,
            lst_custom_widgets_implementations: list[Type[Widget]] = None
    ):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # We check that the directory "assets" exists...
        if not Path(__file__, "../", self.const_str_relative_path_to_assets).resolve().is_dir():
            raise Exception(
                f'When trying to instantiate the Dash application, we could not find the directory assets":'
                f'\n\t- From current file path "{Path(__file__)}"'
                f'\n\t- Adding relative path "{self.const_str_relative_path_to_assets}"'
                f'\n\t- Leading to non existing directory '
                f'"{Path(__file__, "../", self.const_str_relative_path_to_assets).resolve()}'
            )

        # We initialize the list of widgets
        # - We screen the sub-directory "widgets" to identify the default widgets coming from com-enovation
        # - We consolidate with the custom widgets which are provided by consumers.
        self._dict_widgets_implementations_repository: dict[str, Type[Widget]] = \
            self._init_widgets_implementations_repository(
                lst_custom_widgets_implementations=lst_custom_widgets_implementations
            )

        # We declare the other instance properties (initialized in the function "launch")
        self._b_debug: Optional[bool] = None
        self._dash_server: Optional[Dash] = None
        self._dict_config: Optional[dict] = None
        self._dict_context: Optional[dict] = None
        self._dict_sheets: Optional[dict[str, SheetAsDiv]] = None
        self._session: Optional[Session] = None

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

    def _init_widgets_implementations_repository(
            self,
            lst_custom_widgets_implementations: list[Type[Widget]]
    ) -> dict[str, Type[Widget]]:
        """
        TODO: to be enriched:
        - We screen the sub-directory "widgets" to identify the default widgets coming from com-enovation
        - We consolidate with the custom widgets which are provided by consumers.

        :param lst_custom_widgets_implementations:
        :return:
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        dict_the_return: dict[str, Type[Widget]] = {}

        if lst_custom_widgets_implementations is None:
            self._logger.info(f"No lst_custom_widgets_implementations provided...")

        else:
            raise Exception(f"Not yet implemented...")

        dict_the_return["https://enovation.com/dash_application/bubbles"] = BubblesAsDiv

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
        return dict_the_return

    def launch(
            self,
            dict_config: dict,
            dict_context: dict,
            b_debug: bool = False
    ):
        """
        Main function call to instantiate and launch dash application:
        - The layout is prepared:
          - The Navbar, the footer and the main content
            - If debug, the main content displays the debug widget
          - The various widgets, according to their configurations

        Exception:
        - When there is already a Dash app instantiated
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        if self.dash_server is not None:
            raise Exception(f"The property dash_server is not null, which is not expected.")

        # We set the instance properties
        self._b_debug = b_debug
        self._dict_context = dict_context
        self._dict_config = dict_config
        self._session = Session(dash_application=self)

        _the_asset_folder = os.path.join(os.path.dirname(__file__), self.const_str_relative_path_to_assets)
        if os.path.isdir(_the_asset_folder) is False:
            self._logger.error(f"The asset directory could not be found at '{_the_asset_folder}'. Assets will be "
                               f"ignored.")
            _the_asset_folder = None

        # We instantiate the Dash application
        self._dash_server = Dash(
            name=__name__,
            assets_folder=os.path.join(os.path.dirname(__file__), self.const_str_relative_path_to_assets),
            external_stylesheets=[
                dbc.themes.JOURNAL,
            ],
            title=self.const_str__config_label__str_brand,

            # The below setting is to avoid the following errors:
            # Attempting to connect a callback Input item to component: "widget id"
            # but no components with that id exist in the layout.
            #
            # If you are assigning callbacks to components that are
            # generated by other callbacks (and therefore not in the
            # initial layout), you can suppress this exception by setting
            # `suppress_callback_exceptions=True`.
            suppress_callback_exceptions=True
        )

        # We instantiate the widgets
        self._dict_sheets = self._instantiate_sheets(
            dict_widgets_implementations_repository=self.dict_widgets_implementations_repository,
            dict_config=self.dict_config[self.const_str__config_label__dict_sheets],
            dict_context=self.dict_context,
            session=self.session
        )

        # We eventually instantiate the overall layout to load
        self._dash_server.layout = LayoutAsDiv(
            dict_sheets=self._dict_sheets,
            dict_config=self.dict_config.get(self.const_str__config_label__dict_properties, {}),
            session=self.session,
            dict_context=dict_context
        )

        self._dash_server.run_server(debug=True, use_reloader=False)
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

    def _instantiate_sheets(
            self,
            dict_widgets_implementations_repository: dict[str, Type[Widget]],
            dict_config: dict,
            dict_context: dict,
            session: Session
    ) -> dict[str, SheetAsDiv]:
        """
        Function that instantiates the sheets:
        - The configuration is the overall configuration of the overall dash application
        - The context is the overall Click context, which is not reduced to the parameters expected by the widget.

        The logic is the following:
        - For each widget from "dict_config['widgets']"
        - Get the widget id, which is the key
        - From this widget id, get the associated class from "dict_repository_of_widgets"
        - Instantiate the widget, and add it to the dictionary to return

        :param dict_widgets_implementations_repository: the repository of the widgets, consisting in a widget id
          (similar to the id in the widget json schema
        :param dict_config: the dash application configuration, that contains a node "widgets" in which all the widgets
          to be loaded are listed, along with their configuration
        :param dict_context: the click context that contains all the loaded objects
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        dict_the_return: dict[str, SheetAsDiv] = {}

        # We loop through each configured sheet
        for k_sheet, v_sheet in dict_config.items():
            dict_the_return[k_sheet] = self._instantiate_sheet(
                dict_widgets_implementations_repository=dict_widgets_implementations_repository,
                dict_config=v_sheet,
                dict_context=dict_context,
                str_sheet_name=k_sheet,
                session=session
            )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        return dict_the_return

    def _instantiate_sheet(
            self,
            dict_widgets_implementations_repository: dict[str, Type[Widget]],
            dict_config: dict,
            dict_context: dict,
            str_sheet_name: str,
            session: Session
    ) -> SheetAsDiv:
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        lst_the_widgets: list[Widget] = self._instantiate_widgets(
            dict_widgets_implementations_repository=dict_widgets_implementations_repository,
            list_widgets_configs=dict_config.get(self.const_str__config_label__list_widgets, []),
            dict_context=dict_context,
            session=session
        )

        sheet_the_return: SheetAsDiv = SheetAsDiv(
            lst_widgets=lst_the_widgets,
            str_label=str_sheet_name,
            dict_properties=dict_config.get(self.const_str__config_label__dict_properties, {})
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        return sheet_the_return

    def _instantiate_widgets(
            self,
            dict_widgets_implementations_repository: dict[str, Type[Widget]],
            list_widgets_configs: list[dict],
            dict_context: dict,
            session: Session
    ) -> list[Widget]:
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        lst_the_return: list[Widget] = []

        for i_widget_config in list_widgets_configs:
            lst_the_return.append(
                self._instantiate_widget(
                    dict_widgets_implementations_repository=dict_widgets_implementations_repository,
                    dict_config=i_widget_config,
                    dict_context=dict_context,
                    session=session
                )
            )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        return lst_the_return

    def _instantiate_widget(
            self,
            dict_widgets_implementations_repository: dict[str, Type[Widget]],
            dict_config: dict,
            dict_context: dict,
            session: Session
    ) -> Widget:
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        if dict_config[self.const_str__config_label__str_widget_id] not in\
                dict_widgets_implementations_repository:
            raise Exception(
                f"Widget id '{dict_config[self.const_str__config_label__str_widget_id]}' does not exist... Only "
                f"the following widgets exist: '{', '.join(dict_widgets_implementations_repository)}'.")

        widget_the_return: Widget = \
            dict_widgets_implementations_repository[dict_config[self.const_str__config_label__str_widget_id]](
                dict_context=dict_context,
                dict_config=dict_config.get(self.const_str__config_label__dict_properties, {}),
                session=session
            )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        return widget_the_return
