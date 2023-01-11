from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from truera.rnn.general.selection.swap_selection import SwapComparisons
from truera.rnn.general.utils import log
from truera.rnn.general.utils.paths import parse_search_string

from . import App
from .component import Component


class ProjectSelector(Component):

    def __init__(self, *argv, **kwargs):
        Component.__init__(
            self,
            *argv,
            element_names=['project'],
            ui_element_names=['container'],
            **kwargs
        )

    def render(self):
        return [
            dbc.DropdownMenuItem(
                header=True,
                style=dict(width="400px"),
                className="p-1 m-1",
                children=[
                    dcc.Dropdown(
                        className="p-1",
                        id=self._element_id("project"),
                        options=[],
                        placeholder="Select a project"
                    )
                ]
            )
        ]

    def register(self, app: App):

        @app.component_callback(
            [self.output("project")], [self.input("project", field="options")],
            [
                self.state("project"),
                State("url", "pathname"),
                State("url", "search")
            ]
        )
        def update_selected_project(
            options, selected_value, pathname, searchname
        ):
            url_search = parse_search_string(searchname)
            default = app.default_project
            if selected_value is None and pathname == app.path and 'projectName' in url_search:
                default = url_search['projectName'
                                    ]  # default to queried project
            return App.update_selection_of_updated_options(
                options, selected_value, default=default
            )

        @app.component_callback(
            [
                self.output('project', field='options'),
            ], [Input('interval-component', 'n_intervals')]
        )
        def update_project_options(n_intervals):
            log.info(f"update_project_options: interval: {n_intervals}")
            projects = app.sync_client.sync_service.list_projects()
            projects = sorted(set(projects))
            project_options = [
                {
                    'label': 'Project: ' + project,
                    'value': project
                } for project in projects
            ]

            return [project_options]

    def deregister(self, app: App):
        pass


class RestSelector(Component):

    def __init__(
        self,
        comparison_filter=False,  # include the comparison filter options
        initialize_value=True,  # initialize selected value (otherwise keep empty)
        *argv,
        **kwargs
    ):
        Component.__init__(
            self,
            *argv,
            element_names=['model', 'data_collection', 'split', 'pred_thresh'] +
            (['swap_comparison_filter'] if comparison_filter else []),
            **kwargs
        )
        self.comparison_filter = comparison_filter
        self.initialize_value = initialize_value

    def render(self):
        items = [
            dcc.Dropdown(
                id=self._element_id("model"),
                className="p-1",
                options=[],
                placeholder="Select a model",
            ),
            dcc.Dropdown(
                id=self._element_id("data_collection"),
                className="p-1",
                options=[],
                placeholder="Select a data collection",
            ),
            dcc.Dropdown(
                id=self._element_id("split"),
                className="p-1",
                options=[],
                placeholder="Select a split",
            ),
            dbc.Col(
                className="pt-2",
                children=[
                    html.Label("Classification Threshold"),
                    dbc.Input(
                        id=self._element_id('pred_thresh'),
                        type='number',
                        value=0.5,
                        step=0.01,
                        min=0.0,
                        max=1.0,
                        debounce=True
                    )
                ]
            )
        ]

        if self.comparison_filter:
            items.append(
                dbc.Col(
                    className="pt-2",
                    children=[
                        html.Label("Comparison Filter"),
                        dcc.Dropdown(
                            id=self._element_id("swap_comparison_filter"),
                            options=[
                                {
                                    'label': item.name,
                                    'value': item.value
                                } for item in list(SwapComparisons)
                            ],
                            value=SwapComparisons.NONE.value
                        )
                    ]
                ),
            )

        return dbc.DropdownMenuItem(
            header=True,
            style=dict(width="400px"),
            className="p-1 m-1",
            children=items
        )

    def register(self, app: App, ps: ProjectSelector):

        @app.component_callback(
            [self.output('model')], [self.input('model', field='options')],
            [self.state('model')]
        )
        def update_selected_model(options, selected_value):
            if self.initialize_value:
                return App.update_selection_of_updated_options(
                    options, selected_value
                )
            else:
                return [None]

        @app.component_callback(
            [self.output('data_collection')],
            [self.input('data_collection', field='options')],
            [self.state('data_collection')]
        )
        def update_selected_data_collection(options, selected_value):
            if self.initialize_value:
                return App.update_selection_of_updated_options(
                    options, selected_value
                )
            else:
                return [None]

        @app.component_callback(
            [self.output('split')], [self.input('split', field='options')],
            [self.state('split')]
        )
        def update_selected_split(options, selected_value):
            if self.initialize_value:
                return App.update_selection_of_updated_options(
                    options, selected_value
                )
            else:
                return [None]

        @app.component_callback(
            [self.output('data_collection', field='options')],
            [ps.input('project')]
        )
        def update_data_collection_options(project):
            if project is None:
                raise PreventUpdate

            data_collections = []

            try:
                data_collections = sorted(
                    set(
                        app.sync_client.sync_service.list_data_collections(
                            project=project
                        )
                    )
                )
            except Exception as e:
                log.debug(
                    f"failed to get data_collections for this project: {project}\n{e}"
                )

            data_collection_options = [
                {
                    'label': 'Data collection: ' + data_collection,
                    'value': data_collection
                } for data_collection in data_collections
            ]

            return [data_collection_options]

        @app.component_callback(
            [self.output('model', field='options')], [ps.input('project')]
        )
        def update_model_options(project):
            if project is None:
                raise PreventUpdate

            try:
                models = set(
                    app.sync_client.sync_service.list_models(
                        project, use_artifact=True
                    )
                )
            except Exception as e:
                log.debug(
                    f"failed to get models for this project: {project}\n{e}"
                )

            models = sorted(models)
            models_options = [
                {
                    'label': 'Model: ' + model,
                    'value': model
                } for model in models
            ]

            if self.comparison_filter:
                models_options.append({'label': '( None )', 'value': 'None'})

            return [models_options]

        @app.component_callback(
            [self.output('split', field='options')], [self.input('model')],
            [ps.state('project')]
        )
        def update_split_options(selected_model, project):
            log.info(f"update_split_options: {selected_model}")

            if selected_model is None or selected_model == "None":
                return [[]]

            if project is None:
                raise PreventUpdate

            model_to_splits = {}

            artifacts = []

            try:
                artifacts = app.sync_client.sync_service.list_artifacts(project)
            except Exception as e:
                log.debug(
                    f"failed to get artifacts for this project: {project}\n{e}"
                )
            for artifact in artifacts:
                data_collection = artifact[0]
                split = artifact[1]
                model = artifact[2]
                if model not in model_to_splits:
                    model_to_splits[model] = []

                model_to_splits[model].append((data_collection, split))

            splits_options = [
                {
                    'label': 'Split: ' + split,
                    'value': split
                }
                for (data_collection, split) in model_to_splits[selected_model]
            ]

            return [splits_options]

        @app.component_callback(
            [self.output('pred_thresh', field='value')], [
                ps.input('project'),
                self.input('model'),
                self.input('data_collection'),
                self.input('split'),
            ]
        )
        def update_split_options(project, model, data_collection, split):
            artifacts_container = app.get_artifacts_container(
                project, model, data_collection, split
            )
            return [app.viz.get_default_threshold(artifacts_container)]

    def deregister(self, app: App):
        pass
