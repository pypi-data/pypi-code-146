import dash
from dash import html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from . import App
from .component import Component


class LongCallbackControls(Component):

    def __init__(self, id):
        Component.__init__(self, id, element_names=['run', 'stop'])

    def render(self):
        return dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Button(
                                    'Run',
                                    id=self._element_id('run'),
                                    n_clicks=0,
                                    disabled=True,
                                    style={"width": "10vw"}
                                ),
                                dbc.Button(
                                    'Stop Run',
                                    id=self._element_id('stop'),
                                    n_clicks=0,
                                    disabled=True,
                                    style={
                                        "margin-left": "1vw",
                                        "width": "10vw"
                                    }
                                )
                            ],
                            width=5
                        ),
                    ]
                )
            ]
        )

    def register(self, app: App):
        pass

    def deregister(self, app: App):
        pass
