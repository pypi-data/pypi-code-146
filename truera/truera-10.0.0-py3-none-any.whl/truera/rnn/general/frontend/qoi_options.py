from dash import dcc
from dash import html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import numpy as np

from truera.rnn.general.container import ArtifactsContainer
from truera.rnn.general.utils import log

from . import App
from . import index
from .component import Component


class QoIOptions(Component):

    def __init__(self, *argv, **kwargs):
        Component.__init__(
            self,
            *argv,
            ui_element_names=['container', 'total_timesteps'],
            element_names=[
                'qoi',
                'model_class',
                'model_class_qoi_compare',
                'qoi_timestep',
            ]
        )

    def render(self, app: App = None):
        qoi_dropdown = dcc.Dropdown(
            id=self._element_id("qoi"),
            options=[
                dict(label=d, value=d) for d in [
                    'average', 'last', 'timestep',
                    'first default (ground_truth)', 'first default (prediction)'
                ]
            ],
            value='last'
        )

        model_class_dropdown = dcc.Dropdown(
            id=self._element_id("model_class"),
            options=[dict(label="Class: 0", value=0)],
            value=0
        )

        model_class_qoi_compare_dropdown = dcc.Dropdown(
            id=self._element_id('model_class_qoi_compare'),
            options=[dict(label="(None)", value=-1)],
            value=-1
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
                            dcc.Store(id=self._element_id('total_timesteps')),
                            dbc.Col(
                                className=fieldClasses,
                                children=[html.Label("QoI"), qoi_dropdown]
                            ),
                            dbc.Col(
                                className=fieldClasses,
                                children=[
                                    html.Label("Output Class"),
                                    model_class_dropdown
                                ]
                            ),
                            dbc.Col(
                                className=fieldClasses,
                                children=[
                                    html.Label("Compare Class"),
                                    model_class_qoi_compare_dropdown
                                ]
                            ),
                            dbc.Col(
                                className=fieldClasses,
                                children=[
                                    html.Label("QoI Timestep"),
                                    dbc.Input(
                                        id=self._element_id('qoi_timestep'),
                                        type='number',
                                        value=0,
                                        min=0
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

        def update_model_class_options(artifact_locator, add_none=False):
            artifact_path = artifact_locator.get_path()

            try:
                input_attrs_shape = np.load(
                    artifact_path + 'input_attrs_per_timestep_shape.npy'
                )
            except Exception as e:
                log.debug(e)
                return []

            model_class_options = [
                {
                    'label': 'Class: ' + str(i),
                    'value': i
                } for i in range(input_attrs_shape[-1])
            ]

            if add_none:
                model_class_options.insert(0, {'label': '(None)', 'value': -1})

            return model_class_options

        @app.callback_located(self.output('model_class', field='options'))
        def update_model_class_options_core(
            artifacts_container: ArtifactsContainer,
            compare_artifacts_container: ArtifactsContainer
        ):
            return update_model_class_options(artifacts_container)

        @app.callback_located(
            self.output('model_class_qoi_compare', field='options')
        )
        def update_model_class_options_qoi_compare(
            artifacts_container: ArtifactsContainer,
            compare_artifacts_container: ArtifactsContainer
        ):
            return update_model_class_options(
                artifacts_container, add_none=True
            )

        @app.component_callback(
            self.output('model_class', field='value'),
            [self.input('model_class', field='options')],
            [self.state('model_class', field='value')]
        )
        def update_model_class(options, selected_value):
            return App.update_selection_of_updated_options(
                options, selected_value
            )

        @app.component_callback(
            self.output('model_class_qoi_compare', field='value'),
            [self.input('model_class_qoi_compare', field='options')],
            [self.state('model_class_qoi_compare', field='value')]
        )
        def update_model_class_qoi_compare(options, selected_value):
            return App.update_selection_of_updated_options(
                options, selected_value
            )

        @app.component_callback(
            self.output('qoi_timestep', field='max'),
            [self.input('total_timesteps', field='data')]
        )
        def update_max_qoi_timestep(total_timesteps):
            if total_timesteps is None or not isinstance(total_timesteps, int):
                raise PreventUpdate
            return total_timesteps - 1
