import functools

from dash import dcc
from dash.dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
import dash_bootstrap_components as dbc

from truera.rnn.general.selection.filter_selection import FilterType

from . import App
from . import index
from .component import Component


class Filters(Component):

    def __init__(self, filter_classes=[], *argv, **kwargs):
        Component.__init__(
            self,
            *argv,
            ui_element_names=[],
            element_names=[f'filter{i}' for i in range(len(filter_classes))],
            **kwargs
        )

        self.elements = self.Data(
            *[
                filter_class(id=self._element_id(f"filter{i}"))
                for i, filter_class in enumerate(filter_classes)
            ]
        )

        self.filters = self.elements

    def render(self):
        children = functools.reduce(
            lambda l, f: l + f.render(), self.filters, list()
        )
        return children

    def register(self, app: App):
        for f in self.filters:
            f.register(app)

    def deregister(self, app: App):
        pass


class Filter(Component):

    def __init__(self, *argv, **kwargs):
        Component.__init__(
            self,
            *argv,
            ui_element_names=[],
            element_names=['lhs', 'predicate', 'rhs'],
            **kwargs
        )
        self.lhs = None
        self.predicate = None
        self.rhs = None

    def render(self):
        children = [
            dbc.DropdownMenuItem(
                header=True,
                style={
                    'min-width': '500px',
                    'max-width': '100vw',
                    'white-space': 'normal'
                },
                className="p-0 m-0",
                children=[
                    dbc.Row(
                        className="p-0 m-2",
                        children=[
                            dbc.Col(className="col-5 p-1", children=self.lhs),
                            dbc.Col(
                                className="col-2 p-1", children=self.predicate
                            ),
                            dbc.Col(className="col-5 p-1", children=self.rhs)
                        ]
                    )
                ]
            )
        ]
        return children

    def register(self, app: App):
        pass

    def deregister(self, app: App):
        pass


class OutputFilter(Filter):
    """
    Defines filters for outputs (model outputs and ground truth labels).
    """

    def __init__(self, *argv, **kwargs):
        Filter.__init__(self, *argv, **kwargs)

        self.rhs = dbc.Input(
            id=self._element_id("rhs"), type='number', value=0, debounce=True
        )
        self.lhs = dcc.Dropdown(
            id=self._element_id("lhs"),
            options=[
                {
                    'label': 'Average Prediction',
                    'value': FilterType.AVERAGE_PRED_THRESH.value
                }, {
                    'label': 'Most Recent Prediction',
                    'value': FilterType.LAST_STEP_PRED_THRESH.value
                }, {
                    'label': 'Average Label',
                    'value': FilterType.AVERAGE_LABEL.value
                }, {
                    'label': 'Most Recent Label',
                    'value': FilterType.LAST_STEP_LABEL.value
                }
            ],
            value=0
        )
        self.predicate = dcc.Dropdown(
            id=self._element_id("predicate"),
            options=[{
                'label': '>=',
                'value': 0
            }, {
                'label': '<',
                'value': 1
            }],
            value=0
        )

    def get_filter_type(self, lhs):
        return FilterType(lhs)


class CategoricalDataFilter(Filter):
    """
    Defines filters on input categorical features.
    """

    def __init__(self, *argv, **kwargs):
        Filter.__init__(self, *argv, **kwargs)
        self.rhs = dcc.Dropdown(
            id=self._element_id("rhs"), options=[], value=None
        )
        self.lhs = dcc.Dropdown(
            id=self._element_id("lhs"), options=[], value=None
        )
        self.predicate = dcc.Dropdown(
            id=self._element_id("predicate"),
            options=[
                {
                    'label': 'is',
                    'value': 0
                }, {
                    'label': 'is not',
                    'value': 1
                }
            ],
            value=0
        )

    def register(self, app: App):

        @app.callback_located(
            [
                Output(self._element_id("lhs"), 'options'),
                Output(self._element_id("lhs"), 'value'),
            ], [], [State(self._element_id("lhs"), 'value')]
        )
        def update_categorical_feature_options(
            artifacts_container, compare_container, curr_value
        ):
            self.categorical_map = app.viz.get_nonnumeric_feature_map(
                artifacts_container
            )
            value = no_update if curr_value in self.categorical_map else None
            return [dict(label=f, value=f) for f in self.categorical_map], value

        @app.callback(
            [
                Output(self._element_id("rhs"), 'options'),
                Output(self._element_id("rhs"), 'value'),
            ], [
                Input(self._element_id("lhs"), 'value'),
            ]
        )
        def update_categorical_feature_values(feature_name):
            if feature_name is None:
                return [], None
            options = [
                dict(label=name, value=number)
                for number, name in self.categorical_map[feature_name].items()
            ]
            value = options[0]['value'] if options else None
            return options, value

    def get_filter_type(self, lhs):
        return FilterType.FEATURE_VAL_CATEGORICAL
