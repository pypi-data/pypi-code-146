from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from . import App
from .component import Component


class RecordOptions(Component):

    def __init__(self, *argv, **kwargs):
        Component.__init__(
            self,
            *argv,
            ui_element_names=['container', 'total_records'],
            element_names=[
                'num_records_no_attrs', 'num_records_input_attrs',
                'num_records_internal_attrs'
            ]
        )

    def render(self, app: App = None):
        default_num_records = None
        default_max_records = 100000

        return [
            dbc.DropdownMenuItem(
                className="p-0 ml-auto mr-auto",
                header=True,
                style={
                    'min-width': '35vw',
                    'max-width': '100vw',
                    'white-space': 'normal',
                },
                children=[
                    dcc.Store(id=self._element_id('total_records')),
                    dbc.Row(
                        className="m-3",
                        children=html.P("Set number of records for figures:"),
                        style={
                            'font-weight': 'bold',
                            'cursor': 'pointer'
                        },
                        id='batchsize-instructions',
                    ),
                    dbc.Tooltip(
                        "The maximum amount of data that can be loaded in each visualization is dependent on the type of attribution the visualization uses.",
                        target="batchsize-instructions",
                        placement="right"
                    ),
                    dbc.Row(
                        className="m-3",
                        children=[
                            html.Label("Number of Records (No Attributions)"),
                            dbc.Input(
                                id=self._element_id('num_records_no_attrs'),
                                type='number',
                                min=1,
                                value=default_num_records,
                                max=default_max_records,
                                debounce=True
                            )
                        ]
                    ),
                    dbc.Row(
                        className="m-3",
                        children=[
                            html.
                            Label("Number of Records (Input Attributions)"),
                            dbc.Input(
                                id=self._element_id('num_records_input_attrs'),
                                type='number',
                                min=1,
                                value=default_num_records,
                                max=default_max_records,
                                debounce=True
                            )
                        ]
                    ),
                    dbc.Row(
                        className="m-3",
                        children=[
                            html.
                            Label("Number of Records (Internal Attributions)"),
                            dbc.Input(
                                id=self.
                                _element_id('num_records_internal_attrs'),
                                type='number',
                                min=1,
                                value=default_num_records,
                                max=default_max_records,
                                debounce=True
                            )
                        ]
                    ),
                ]
            )
        ]

    def deregister(self, app: App):
        pass

    def register(self, app: App):
        pass
