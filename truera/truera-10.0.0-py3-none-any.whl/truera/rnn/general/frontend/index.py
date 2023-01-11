import sys

from dash import dcc
from dash import html
from dash.dash import no_update
from dash.dependencies import ALL
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from truera.rnn.general.utils import log
import truera.rnn.general.utils.colors as Colors
from truera.rnn.general.utils.errors import FeatureFlag
from truera.rnn.general.utils.mem import MemUtil
from truera.rnn.general.utils.mem import MemUtilDeps
from truera.rnn.general.utils.paths import parse_search_string

from . import App
from . import selector
from .apps import app_diagnostic
from .apps import app_documentation
from .apps import app_export
from .apps import app_features
from .apps import app_fnc
from .apps import app_global
from .apps import app_local
from .apps import app_overview
from .export_components import ExportOptions
from .filters import CategoricalDataFilter
from .filters import Filters
from .filters import OutputFilter
from .qoi_options import QoIOptions
from .record_options import RecordOptions

PAGE_LIST = [
    ('Performance', 'performance', app_overview, FeatureFlag.BETA),
    ('Global explanations', 'global', app_global, FeatureFlag.BETA),
    ('Features', 'features', app_features, FeatureFlag.BETA),
    ('Records', 'records', app_local, FeatureFlag.BETA),
    ('Model Diagnostics', 'diagnostics', app_diagnostic, FeatureFlag.BETA),
    ('Feature Interaction', 'feature_interaction', app_fnc, FeatureFlag.BETA),
    ('Export', 'export', app_export, FeatureFlag.BETA),
    ('Documentation', 'documentation', app_documentation, FeatureFlag.BETA)
]

page_cache = {}


class Index(App):

    def __init__(self, *argv, **kwargs):
        self.enable_alpha_features = kwargs.get('enable_alpha_features', False)
        del kwargs['enable_alpha_features'
                  ]  # avoid passing in TruEra-specific kwarg into Dash App
        App.__init__(self, *argv, **kwargs)
        self.path = kwargs.get("setup_path", "/rnn/")
        page_list = PAGE_LIST[:]
        if not self.enable_alpha_features:
            page_list = [p for p in page_list if p[3] != FeatureFlag.ALPHA]
        self.pages = {
            link: app_name for title, link, app_name, flag in page_list
        }
        self.project_selector = selector.ProjectSelector(id="project-selector")
        self.base_selector = selector.RestSelector(id="base-selector")
        self.compare_selector = selector.RestSelector(
            id="compare-selector",
            comparison_filter=True,
            initialize_value=False
        )
        self.record_options = RecordOptions("record-options")
        self.qoi_options = QoIOptions("qoi-options")

        self.filters = Filters(
            filter_classes=[OutputFilter, OutputFilter, CategoricalDataFilter]
        )

        self.export_options = ExportOptions("export-options")

        # All tool bars. This is used for hiding them on a per-page basis. See visible_bars below
        # and on each page.
        self.page_bars: Set[Component] = set(
            [
                self.project_selector, self.base_selector,
                self.compare_selector, self.record_options, self.qoi_options,
                self.export_options, self.filters
            ]
        )

        temp = "pr-2 pb-2"

        self.title = 'Truera Neural Networks Platform'

        controls_navbar = dbc.Navbar(
            className="pb-0 pt-0",
            expand="lg",
            color=Colors.BACKGROUND_95,
            dark=True,
            fixed="top",
            style={'z-index': '1000'},
            children=[
                html.A(
                    className="d-none d-sm-block pl-0 pr-2 ml-0 mr-0",
                    children=dbc.NavbarBrand(
                        className="pb-0 pt-0 m-0 p-0",
                        children=html.Img(src='assets/logo.svg')
                    ),
                    href="/"
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(
                    className="navbar pt-0 pt-xl-3 mt-0 ml-0 mr-0 pl-0 pr-0",
                    id="navbar-collapse",
                    navbar=True,
                    children=[
                        dbc.Row(
                            className="p-0 ml-auto mr-auto",
                            children=[
                                html.Div(
                                    id=self.project_selector.
                                    _element_id("container"),
                                    children=dbc.DropdownMenu(
                                        className=temp,
                                        label="Project",
                                        color="secondary",
                                        children=self.project_selector.render()
                                    )
                                ),
                                html.Div(
                                    id=self.base_selector.
                                    _element_id("container"),
                                    children=dbc.DropdownMenu(
                                        id=self.base_selector.
                                        _element_id('menu'),
                                        className=temp,
                                        color="secondary",
                                        label="Base Model",
                                        children=self.base_selector.render()
                                    )
                                ),
                                html.Div(
                                    id=self.compare_selector.
                                    _element_id("container"),
                                    children=dbc.DropdownMenu(
                                        id=self.compare_selector.
                                        _element_id('menu'),
                                        className=temp,
                                        color="secondary",
                                        label="Compare Model",
                                        children=self.compare_selector.render()
                                    )
                                ),
                                html.Div(
                                    id=self.qoi_options.
                                    _element_id("container"),
                                    children=dbc.DropdownMenu(
                                        className=temp,
                                        color="info",
                                        label="QoI",
                                        children=self.qoi_options.render()
                                    )
                                ),
                                html.Div(
                                    id=self.record_options.
                                    _element_id("container"),
                                    children=dbc.DropdownMenu(
                                        className=temp,
                                        color="info",
                                        label="Records",
                                        children=self.record_options.render()
                                    )
                                ),
                                html.Div(
                                    id=self.filters._element_id("container"),
                                    children=dbc.DropdownMenu(
                                        className=temp,
                                        color="info",
                                        label="Filters",
                                        children=sum(
                                            [
                                                [
                                                    dbc.Row(
                                                        html.
                                                        Label("Output Filters"),
                                                        className="p-0 m-2"
                                                    )
                                                ],
                                                self.filters.elements.filter0.
                                                render(),
                                                self.filters.elements.filter1.
                                                render(),
                                                [
                                                    dbc.Row(
                                                        html.
                                                        Label("Data Filters"),
                                                        className="p-0 m-2"
                                                    )
                                                ],
                                                self.filters.elements.filter2.
                                                render()
                                            ], []
                                        )
                                    )
                                ),
                                html.Div(
                                    id=self.export_options.
                                    _element_id("container"),
                                    children=[
                                        dbc.DropdownMenu(
                                            className=temp,
                                            color="info",
                                            label="Export Options",
                                            children=self.export_options.render(
                                            )
                                        )
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
            ]
        )

        page_navbar = dbc.Navbar(
            expand="md",
            color=Colors.BACKGROUND_95,
            dark=True,
            fixed="top",
            children=[
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                title,
                                id={
                                    'type': 'page-tab-nav',
                                    'index': i
                                },
                                href=self.path + "{}".format(link),
                                external_link=False
                            ),
                            style={
                                'font-size': '0.85em',
                            }
                        ) for i, (title, link, app_name,
                                  flag) in enumerate(page_list)
                    ],
                    pills=True,
                    style={'padding-bottom': '0px'}
                )
            ],
            style={
                'padding-top': '70px',
                'padding-bottom': '0px',
                'z-index': '1000'
            }
        )

        self.record_change_alert_bar = dbc.Alert(
            "The number of loaded records have been auto-selected because of a project or data collection change or fresh page load.",
            id="record-change-alert-bar",
            is_open=False,
            color="warning",
            dismissable=True,
            style={
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto"
            }
        )

        self.record_ui_overload_alert = dbc.Alert(
            "The number of selected records exceeds the capacity of the display.",
            id="record-ui-overload-alert-bar",
            is_open=False,
            color="danger",
            dismissable=True,
            style={
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto"
            }
        )

        self.layout = dbc.Container(
            children=[
                dcc.Location(id="url", refresh=False),
                dcc.Interval(
                    id='interval-component',
                    interval=60 * 1000,  # in milliseconds
                    n_intervals=0
                ),
                dbc.Row(
                    children=[
                        dbc.Row(dbc.Col(page_navbar)),
                        dbc.Row(dbc.Col(controls_navbar)),
                    ]
                ),
                dbc.Row(className="d-block", style=dict(height="150px")),
                dbc.
                Row(className="d-block d-xl-none", style=dict(height="40px")),
                dbc.Row(self.record_change_alert_bar),
                dbc.Row(self.record_ui_overload_alert),
                dbc.Row(
                    children=[
                        dbc.Col(
                            className="col-12",
                            children=html.Div(id="page-content")
                        )
                    ]
                ),
            ]
        )

        @self.callback(
            Output("navbar-collapse", "is_open"),
            [Input("navbar-toggler", "n_clicks")],
            [State("navbar-collapse", "is_open")],
        )
        def toggle_navbar_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        self.project_selector.register(self)
        self.base_selector.register(self, self.project_selector)
        self.compare_selector.register(self, self.project_selector)
        self.record_options.register(self)
        self.qoi_options.register(self)
        self.filters.register(self)
        self.export_options.register(self)

        # This has to be done ahead of time as registering callbacks inside callbacks does not seem
        # to work.
        for page in self.pages.values():
            page.register(self)

        @self.callback(
            [
                Output("page-content", "children"), *[
                    c.output('container', field='className')
                    for c in self.page_bars
                ],
                Output({
                    'type': 'page-tab-nav',
                    'index': ALL
                }, 'style')
            ], [
                Input("url", "pathname"),
                Input("url", "hash"),
                Input("url", "search")
            ], [State({
                'type': 'page-tab-nav',
                'index': ALL
            }, 'href')]
        )
        def render_page_content(
            pathname, page_hash, page_search, page_tab_hrefs
        ):
            log.info(f"rendering page: {pathname}")
            default_styles = [
                {
                    'border-bottom':
                        '2px solid {}'.format(Colors.BACKGROUND_95),
                    'color':
                        'black',
                    'border-radius':
                        '0px'
                } for _ in range(len(page_tab_hrefs))
            ]

            visible_bars = set(self.page_bars)
            visibilities = [
                '' if c in visible_bars else 'd-none' for c in self.page_bars
            ]

            if pathname == "/" or pathname is None or pathname == self.path:
                pathname = self.path + list(self.pages.keys())[0]
            if not page_hash is None and page_hash.startswith('#'):
                page_hash = page_hash[1:]
            page_search_dict = parse_search_string(page_search)

            try:
                pagename = pathname.split("/").pop()
                page = self.pages[pagename]
                page_render = page.render(
                    self, page_hash=page_hash, page_search=page_search_dict
                )
                if not isinstance(page_render, list):
                    page_render = [page_render]
                # Diagnostics page has registered long callbacks that will be polled (but not executed) and will throw errors if not rendered.
                if pagename != 'diagnostics':
                    page_render = page_render + [
                        html.Div(
                            self.pages['diagnostics'].render(self),
                            style={'display': 'none'}
                        )
                    ]
                page_rendered = page_cache.get((page, page_hash), page_render)
                page_cache[(page, page_hash)] = page_rendered
                visible_bars = page.visible_bars(self)
                visibilities = [
                    '' if c in visible_bars else 'd-none'
                    for c in self.page_bars
                ]
                selected_tab = page_tab_hrefs.index(pathname)
                default_styles[selected_tab]['border-bottom'
                                            ] = '2px solid {}'.format(
                                                Colors.TRUERA_GREEN
                                            )

                return [page_rendered, *visibilities, default_styles]

            except Exception as e:
                # If the user tries to reach a different page, return a 404 message
                return [
                    dbc.Jumbotron(
                        [
                            html.H1("404: Not found", className="text-danger"),
                            html.Hr(),
                            html.P(str(e))
                        ]
                    ), *visibilities, default_styles
                ]

        @self.callback(
            [
                self.base_selector.output('menu', field='disabled'),
                self.compare_selector.output('menu', field='disabled')
            ], [self.project_selector.input('project')]
        )
        def show_hide_model_selectors(project):
            if project is None:
                return [True, True]

            try:
                self.sync_client.sync_service.list_data_collections(
                    project=project
                )

            except Exception as e:
                log.debug(
                    f"failed to get data collections for this project: {project}\n{e}"
                )
                return [True, True]

            return [False, False]

        @self.callback(
            [
                self.record_options.output(
                    'num_records_no_attrs', field='style'
                ),
                self.record_options.output(
                    'num_records_input_attrs', field='style'
                ),
                self.record_options.output(
                    'num_records_internal_attrs', field='style'
                ),
                Output('record-ui-overload-alert-bar', 'is_open')
            ], [
                self.record_options.input(
                    'num_records_no_attrs', field='value'
                ),
                self.record_options.input(
                    'num_records_input_attrs', field='value'
                ),
                self.record_options.input(
                    'num_records_internal_attrs', field='value'
                ),
            ]
        )
        def validate_frontend_data_limits(
            num_records_no_attrs, num_records_input_attrs,
            num_records_internal_attrs
        ):
            show_alert = False
            num_records = [
                num_records_no_attrs, num_records_input_attrs,
                num_records_internal_attrs
            ]
            if any([x is None for x in num_records]):
                raise PreventUpdate
            styles = [{} for _ in range(len(num_records))]
            for i, num_record in enumerate(num_records):
                if num_record > MemUtil.MAX_DATAPOINTS_UI:
                    styles[i] = {'border-color': 'red'}
                    show_alert = True
            return styles + [show_alert]

        @self.callback(
            [
                self.record_options.output(
                    'num_records_no_attrs', field='value'
                ),
                self.record_options.output('num_records_no_attrs', field='max'),
                self.record_options.output(
                    'num_records_no_attrs', field='disabled'
                ),
                self.record_options.output(
                    'num_records_input_attrs', field='value'
                ),
                self.record_options.output(
                    'num_records_input_attrs', field='max'
                ),
                self.record_options.output(
                    'num_records_input_attrs', field='disabled'
                ),
                self.record_options.output(
                    'num_records_internal_attrs', field='value'
                ),
                self.record_options.output(
                    'num_records_internal_attrs', field='max'
                ),
                self.record_options.output(
                    'num_records_internal_attrs', field='disabled'
                ),
                self.record_options.output('total_records', field='data'),
                self.qoi_options.output('total_timesteps', field='data'),
                Output('record-change-alert-bar', 'is_open'),
            ],
            [
                Input(
                    "url", "pathname"
                ),  # triggered so on page change, batchsize change alert can disappear
                self.project_selector.input('project'),
                self.base_selector.input('model'),
                self.base_selector.input('data_collection'),
                self.base_selector.input('split'),
                self.compare_selector.input('model'),
                self.compare_selector.input('data_collection'),
                self.compare_selector.input('split'),
            ],
            [
                self.record_options.state(
                    'num_records_no_attrs', field='value'
                ),
                self.record_options.state(
                    'num_records_input_attrs', field='value'
                ),
                self.record_options.state(
                    'num_records_internal_attrs', field='value'
                ),
            ]
        )
        def set_application_num_records(
            pathname, project, model, data_collection, split, compare_model,
            compare_data_collection, compare_split, curr_records_no_attrs,
            curr_records_input_attrs, curr_records_internal_attrs
        ):
            '''
            Updates max records dynamically as application, model, or data_collection changes.
            '''

            artifacts_container = self.get_artifacts_container(
                project=project,
                model=model,
                data_collection=data_collection,
                split=split
            )
            if compare_split is not None:
                artifacts_container_compare = self.get_artifacts_container(
                    project=project,
                    model=compare_model,
                    data_collection=compare_data_collection,
                    split=compare_split
                )
            else:
                artifacts_container_compare = None

            ret = []
            force_record_alert = False
            app_total_timesteps = self.viz.get_total_timesteps(
                artifacts_container
            )
            current_num_records = [
                curr_records_no_attrs, curr_records_input_attrs,
                curr_records_internal_attrs
            ]
            dep_levels = [
                MemUtilDeps.NO_ATTRS, MemUtilDeps.INPUT_ATTRS,
                MemUtilDeps.INTERNAL_ATTRS
            ]
            for dep_level, curr_num_record in zip(
                dep_levels, current_num_records
            ):
                try:
                    base_max_batchsize, base_total_records = self.viz.get_max_batchsize(
                        artifacts_container, dep_level
                    )
                    compare_max_batchsize, compare_total_records = self.viz.get_max_batchsize(artifacts_container_compare, dep_level) \
                        if artifacts_container_compare else (sys.maxsize, sys.maxsize)
                    app_max_batchsize = min(
                        base_max_batchsize, compare_max_batchsize
                    )
                    app_total_records = min(
                        base_total_records, compare_total_records
                    )

                    # following is a constant based on general UI speed.
                    # balancing number of items to load and batch processing speed
                    if dep_level == MemUtilDeps.NO_ATTRS:
                        default_num_batches_to_load = 8
                    else:
                        # Attributions are generally more memory intensive
                        default_num_batches_to_load = 1
                    recommended_records = min(
                        app_total_records,
                        app_max_batchsize * default_num_batches_to_load
                    )
                    num_records = no_update if (
                        curr_num_record is not None and (
                            curr_num_record <= 2 * recommended_records and
                            curr_num_record > 0.5 * recommended_records
                        )
                    ) else recommended_records
                    force_record_alert = (
                        force_record_alert or (num_records != no_update)
                    )
                    ret += [num_records, app_total_records, False]
                except FileNotFoundError:  # attribution type not calculated for this model
                    ret += [None, None, True]
                    log.info(
                        "{} unavailable. Disabling record selection.".
                        format(dep_level)
                    )
                except:  # catch-all for other errors
                    ret += [None, None, False]
                    log.error(
                        "Error with attributions of type {}".format(dep_level),
                        exc_info=True
                    )

            ret += [app_total_records, app_total_timesteps, force_record_alert]
            return ret

    def callback_located(
        self,
        outputs=[],
        inputs=[],
        state=[],
        debug=False,
        long_callback=False,
        running=[],
        cancel=[],
    ):
        '''
        A callback prepopulated with project/datacollection/model and many common UI components.

        Parameters
        ===============
        outputs - Same as plotly outputs, but allows Components from components.py
        inputs - Same as plotly inputs, but allows Components from components.py
        state - Same as plotly state, but allows Components from components.py
        debug - Prints the wrapped callback function name
        long_callback - converts the callback into plotly long callback
        running - same as plotly long callback running, but allows Components from components.py
        cancel - same as plotly long callback cancel, but allows Components from components.py
        '''

        def f(method):

            def wrap(
                project, model, data_collection, split, compare_model,
                compare_data_collection, compare_split,
                val_num_records_no_attrs, val_num_records_input_attrs,
                val_num_records_internal_attrs, num_records_no_attrs_disabled,
                num_records_input_attrs_disabled,
                num_records_internal_attrs_disabled, batch_overload_ui, *rest
            ):
                if debug:
                    log.debug(f"wrapping {method}")
                # input validation
                num_records_no_attrs_validated = num_records_no_attrs_disabled or (
                    val_num_records_no_attrs is not None
                )
                num_records_input_attrs_validated = num_records_input_attrs_disabled or (
                    val_num_records_input_attrs is not None
                )
                num_records_internal_attrs_validated = num_records_internal_attrs_disabled or (
                    val_num_records_internal_attrs is not None
                )
                num_records_validated = (
                    num_records_no_attrs_validated and
                    num_records_input_attrs_validated and
                    num_records_internal_attrs_validated
                )
                if not long_callback:
                    # Long callbacks cannot recover from prevent update
                    if not num_records_validated:
                        raise PreventUpdate
                    if batch_overload_ui:
                        raise PreventUpdate
                    container = self.get_artifacts_container(
                        project, model, data_collection, split
                    )
                else:
                    try:
                        container = self.get_artifacts_container(
                            project, model, data_collection, split
                        )
                    except:
                        container = None
                    if not num_records_validated:
                        container = None
                    if batch_overload_ui:
                        container = None
                try:
                    compare_container = self.get_artifacts_container(
                        project, compare_model, compare_data_collection,
                        compare_split
                    )
                except:
                    compare_container = None

                return method(container, compare_container, *rest)

            self.component_callback(
                outputs, [
                    self.project_selector.input('project'),
                    self.base_selector.input('model'),
                    self.base_selector.input('data_collection'),
                    self.base_selector.input('split'),
                    self.compare_selector.input('model'),
                    self.compare_selector.input('data_collection'),
                    self.compare_selector.input('split'),
                    self.record_options.input('num_records_no_attrs'),
                    self.record_options.input('num_records_input_attrs'),
                    self.record_options.input('num_records_internal_attrs'),
                    self.record_options.input(
                        'num_records_no_attrs', field='disabled'
                    ),
                    self.record_options.input(
                        'num_records_input_attrs', field='disabled'
                    ),
                    self.record_options.input(
                        'num_records_internal_attrs', field='disabled'
                    ),
                    Input('record-ui-overload-alert-bar', 'is_open'), *inputs
                ],
                state,
                long_callback=long_callback,
                running=running,
                cancel=cancel
            )(wrap)

        return f

    def get_default_page_bars(
        self, disable_compare=False, disable_filters=False
    ):
        default_bars = self.page_bars
        if disable_compare:
            default_bars = default_bars - {self.compare_selector}
        if disable_filters:
            default_bars = default_bars - {self.filters}
        return default_bars
