from dash.html import Div

from com.enovation.toolbox.dash.session import Session


class Widget:

    @property
    def session(self):
        return self._session

    @property
    def dict_config(self) -> dict:
        return self._dict_config

    @property
    def dict_context(self) -> dict:
        return self._dict_context

    def __init__(
            self,
            dict_config: dict,
            dict_context: dict,
            session: Session
    ):

        self._dict_config: dict = dict_config
        self._dict_context: dict = dict_context
        self._session: Session = session


class WidgetAsDiv(Widget, Div):

    def __init__(
            self,
            dict_config: dict,
            dict_context: dict,
            session: Session,
            *args, **kwargs
    ):
        # We initialize the widget
        Widget.__init__(
            self,
            dict_config=dict_config,
            dict_context=dict_context,
            session=session
        )

        # We initialize the Div object...
        Div.__init__(
            self,
            *args,
            **kwargs
        )
