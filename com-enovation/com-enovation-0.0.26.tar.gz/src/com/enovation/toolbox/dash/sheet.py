from inspect import stack
from logging import Logger, getLogger

from dash.html import Div

from com.enovation.toolbox.dash.widget import Widget


class Sheet:
    """
    The sheet corresponds to one screen in the dash application. It contains:
    - A label: used in the menu in the dash application navigation bar
    - A list of widgets: which are displayed whener the user open the sheet
    """
    _logger: Logger = getLogger(__name__)

    @property
    def lst_widgets(self) -> list[Widget]:
        return self._lst_widgets

    @property
    def str_label(self) -> str:
        return self._str_label

    @property
    def dict_properties(self) -> dict:
        return self._dict_properties

    def __init__(
            self,
            lst_widgets: list[Widget] = None,
            str_label: str = None,
            dict_properties: dict = None,
            *args,
            **kwargs
    ):

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")
        self._lst_widgets: list[Widget] = lst_widgets
        self._str_label: str = str_label
        self._dict_properties: dict =dict_properties
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")


class SheetAsDiv(Sheet, Div):

    def __init__(
            self,
            lst_widgets: list[Widget] = None,
            str_label: str = None,
            dict_properties: dict = None,
            *args,
            **kwargs
    ):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        Sheet.__init__(
            self,
            lst_widgets=lst_widgets,
            str_label=str_label,
            dict_properties=dict_properties
        )

        if "children" in kwargs:
            raise Exception(f"Unexpected 'children' in kwargs...")

        Div.__init__(
            self,
            children=lst_widgets,
            *args,
            **kwargs
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")
