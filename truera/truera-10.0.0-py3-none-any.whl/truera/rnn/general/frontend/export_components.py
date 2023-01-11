import os

from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from truera.rnn.general.docs.doc_utils import read_markdown
from truera.rnn.general.selection.swap_selection import SwapComparisons
from truera.rnn.general.utils import log
import truera.rnn.general.utils.colors as Colors
from truera.rnn.general.utils.export import ExportBackend

from . import App
from .component import Component


class ExportOptions(Component):

    def __init__(self, *argv, **kwargs):
        Component.__init__(
            self, *argv, element_names=[
                'backend',
                'bucket',
                'prefix',
            ]
        )

    def render(self, app: App = None):
        backend_dropdown = dcc.Dropdown(
            id=self._element_id("backend"),
            options=[
                dict(label=backend_name.lower(), value=backend_name)
                for backend_name in
                [ExportBackend.LOCAL.name, ExportBackend.S3.name]
            ],
            value=ExportBackend.S3.name
        )

        fieldClasses = "col-12 col-md-6 mt-1 mb-1"

        return [
            dbc.DropdownMenuItem(
                className="m-0 p-0",
                header=True,
                style={
                    'min-width': '35vw',
                    'max-width': '100vw',
                    'white-space': 'normal',
                },
                children=[
                    dbc.Row(
                        className="m-0 p-0",
                        children=[
                            dbc.Col(
                                className=fieldClasses,
                                children=[
                                    html.Label("Export To"), backend_dropdown
                                ]
                            ),
                            dbc.Col(
                                id=self._element_id('bucket-col'),
                                className=fieldClasses,
                                children=[
                                    html.Label("bucket"),
                                    dbc.Input(
                                        id=self._element_id('bucket'),
                                        type='text'
                                    )
                                ]
                            ),
                            dbc.Col(
                                id=self._element_id('prefix-col'),
                                className=fieldClasses,
                                children=[
                                    html.Label("prefix"),
                                    dbc.Input(
                                        id=self._element_id('prefix'),
                                        type='text'
                                    )
                                ]
                            ),
                        ]
                    ),
                ]
            )
        ]

    def deregister(self, app: App):
        pass

    def register(self, app: App):

        @app.callback(
            [
                self.output('bucket-col', field='style'),
                self.output('prefix-col', field='style')
            ], [self.input('backend', field='value')]
        )
        def show_supplemental_options(backend):
            log.info(backend)
            if (backend == ExportBackend.LOCAL.name):
                return [{'display': 'none'}] * 2
            else:
                return [{'display': 'block'}] * 2


class ExportFilename(Component):

    def __init__(self, id, ext):
        Component.__init__(
            self, id, element_names=['filename', 'button', 'message', 'ext']
        )
        self.ext = ext

    def render(self):
        return dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                id=self._element_id('filename'),
                                type='text',
                                placeholder='filename'
                            ),
                            width=5
                        ),
                        dbc.Col(
                            html.P(
                                id=self._element_id('ext'), children=[self.ext]
                            ),
                            width=2
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Export",
                                style={'color': Colors.TRUERA_GREEN},
                                id=self._element_id('button'),
                                n_clicks=0,
                                color="light"
                            ),
                            width=4
                        )
                    ]
                ),
                dbc.Row(
                    html.P(
                        "",
                        id=self._element_id('message'),
                        style={
                            "marginLeft": 20,
                            "marginRight": 20
                        }
                    )
                ),
            ],
            width=5
        )

    def register(self, app: App):
        pass

    def deregister(self, app: App):
        pass


class ExportModalComponent:

    def __init__(
        self, component_id, card_title, card_filepath, export_component
    ):
        self.component_id = component_id
        self.card_title = card_title
        self.card_filepath = card_filepath
        self.modal_id = 'export-{}-modal'.format(self.component_id)
        self.button_id = 'export-{}-btn'.format(self.component_id)
        self.modal_close_id = 'export-{}-modal-close'.format(self.component_id)
        self.export_component = export_component

    def _read_markdown(self):
        return read_markdown(os.path.join('help_cards', self.card_filepath))

    def render(self, app):
        return html.Div(
            [
                html.I(
                    id=self.button_id,
                    n_clicks=0,
                    className="fa fa-download fa-lg",
                    style={'color': Colors.TRUERA_GREEN}
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            [
                                self.card_title,
                                html.I(
                                    id=self.modal_close_id,
                                    className="fa fa-times",
                                    style={
                                        "verticalAlign": "middle",
                                        "position": "absolute",
                                        "right": "20px"
                                    }
                                )
                            ]
                        ),
                        dbc.ModalBody(dcc.Markdown(self._read_markdown())),
                        dbc.Container(
                            dbc.Row([self.export_component.render()])
                        ),
                        dbc.ModalFooter(
                            [
                                html.Span(
                                    [
                                        'For more information, check out our ',
                                        html.A(
                                            'reference documentation.',
                                            href=f'{app.path}documentation'
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    id=self.modal_id,
                    centered=True,
                    size='lg'
                )
            ]
        )

    def register(self, app):

        @app.callback(
            Output(self.modal_id, "is_open"), [
                Input(self.button_id, "n_clicks"),
                Input(self.modal_close_id, "n_clicks")
            ], [State(self.modal_id, "is_open")]
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open
