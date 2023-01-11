import os

from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
import dash_bootstrap_components as dbc

from truera.rnn.general.docs.doc_utils import read_markdown
import truera.rnn.general.utils.colors as Colors


class HelpCardComponent:

    def __init__(self, card_title, component_id, card_filepath):
        self.component_id = component_id
        self.card_filepath = card_filepath
        self.card_title = card_title
        self.modal_id = 'help-{}-modal'.format(self.component_id)
        self.button_id = 'help-{}-btn'.format(self.component_id)
        self.modal_close_id = 'help-{}-modal-close'.format(self.component_id)

    def _read_markdown(self):
        return read_markdown(os.path.join('help_cards', self.card_filepath))

    def render(self, app):
        return html.Div(
            [
                html.I(
                    id=self.button_id,
                    n_clicks=0,
                    className="fa fa-question-circle fa-lg",
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
