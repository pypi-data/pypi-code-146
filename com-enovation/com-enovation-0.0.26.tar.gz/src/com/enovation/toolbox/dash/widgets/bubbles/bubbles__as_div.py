from inspect import stack
from logging import Logger, getLogger
from random import choice

import pandas as pd
from dash import html, dcc, callback, Output, Input, State
from dash_extensions import EventListener

# from pandas import DataFrame
from pandas import DataFrame
from plotly.express import scatter
from plotly.graph_objects import Figure

from com.enovation.toolbox.dash.session import Session
from com.enovation.toolbox.dash.widget import WidgetAsDiv


class BubblesAsDiv(WidgetAsDiv):
    """
    python3 ./src/enov.py --verbose df-load-xls ../2022-11-28.HistoricalPipelineForBubbles.xlsx df_raw dict-load-json ../config.json.txt config ds-dash config

    """
    _logger: Logger = getLogger(__name__)

    # The widget IDs to be used
    # Naming convention:
    # - should start by "const_str__wid__"
    # - as the application will screen all the widget ids, across widgets, to ensure there is no ambiguity, aka same
    #   widget id across different widgets
    const_str__wid__bubbles_as_div: str = "enov-content__bubbles__as_div"
    const_str__wid__bubbles_as_dcc_store__data: str = "enov-content__bubbles__as_dcc_store__data"
    const_str__wid__bubbles_as_dcc_store__filters: str = "enov-content__bubbles__as_dcc_store__filters"
    const_str__wid__bubbles_as_graph: str = "enov-content__bubbles__as_graph"

    const_str__config_label__dict_px_scatter_parameters: str = "px.scatter"
    const_str__config_label__str_dataframe_name_in_context: str = "data"

    """
    Return the bubbles widget such as:
    TODO
    """

    def __init__(
            self,
            dict_config: dict,
            dict_context: dict,
            session: Session
    ):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        # ##############################################################################################################
        # Callbacks should be imported here... Otherwise, we face "unknown id" as callbacks get registered even though
        # the widgets are not used...
        # noinspection PyUnresolvedReferences
        # import com.enovation.toolbox.dash.widgets.bubbles.bubbles_callbacks
        # ##############################################################################################################

        # df_data: DataFrame = DataFrame()
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        super().__init__(
            dict_config=dict_config,
            dict_context=dict_context,
            session=session,
            children=[
                dcc.RadioItems(
                    id='selection',
                    options=["GDP - Scatter", "Population - Bar"],
                    value='GDP - Scatter',
                ),
                html.Div(
                    dcc.Loading(
                        dcc.Graph(
                            id=self.const_str__wid__bubbles_as_graph,
                            style={'height': '90vh'}
                        ),
                        type="cube"),
                    id="container"
                ),

                EventListener(
                    id='eventlistener',
                    children=html.Div("Click here!", className="stuff"),
                    events=[
                        {
                            "event": "click", "props": ["srcElement.className"]
                        }
                    ],
                    logging=True
                ),
                html.Div(id="jsg"), html.Div(id="n_events"),

                # dcc.Store for the data to be loaded from the server, and then displayed
                dcc.Store(id=self.const_str__wid__bubbles_as_dcc_store__data),
            ],
            id=BubblesAsDiv.const_str__wid__bubbles_as_div,
            className="container border bg-light",
            style={"margin-top": "1rem", 'height': '90vh'}
        )

        session.dash_application.dash_server.clientside_callback(
            """

            function(n_events, event){
                
                if( typeof event === 'undefined' ) {
                    return "";
                }
                
                if( event["srcElement.className"] == "stuff" ) {

                    // if already full screen; exit
                    // else go fullscreen
                    if (
                        document.fullscreenElement ||
                        document.webkitFullscreenElement ||
                        document.mozFullScreenElement ||
                        document.msFullscreenElement
                    ) {
                        if (document.exitFullscreen) {
                            document.exitFullscreen();
                        } else if (document.mozCancelFullScreen) {
                            document.mozCancelFullScreen();
                        } else if (document.webkitExitFullscreen) {
                            document.webkitExitFullscreen();
                        } else if (document.msExitFullscreen) {
                            document.msExitFullscreen();
                        }
                    } else {
                        element = document.getElementById("container");
                        if (element.requestFullscreen) {
                            element.requestFullscreen();
                        } else if (element.mozRequestFullScreen) {
                            element.mozRequestFullScreen();
                        } else if (element.webkitRequestFullscreen) {
                            element.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
                        } else if (element.msRequestFullscreen) {
                            element.msRequestFullscreen();
                        }
                    }

                    return "ZOOM!!"+n_events+" - "+JSON.stringify(event);
                }

                return "NOTHING!!"+n_events+" - "+JSON.stringify(event);
            }
            """,
            Output("jsg", "children"),
            Input("eventlistener", "n_events"),
            State("eventlistener", "event")
        )

        @callback(
            Output(BubblesAsDiv.const_str__wid__bubbles_as_graph, "figure"),
            Input("selection", "value")
        )
        def display_animated_graph(selection):

            self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

            _df_the_data: DataFrame = self.session.dict_context.get(
                self.dict_config.get(self.const_str__config_label__str_dataframe_name_in_context)
            )

            jsg = self.jsg()

            _the_timestamps = _df_the_data["Sp - Snapshot Date"].unique()

            _the_opp_ids = _df_the_data["Opp - ID"].unique()


            # We randomly set text position for each opportunity id
            _df_the_opp_ids_and_text_position: DataFrame = DataFrame()
            _df_the_opp_ids_and_text_position["Opp - ID"] = _the_opp_ids
            _df_the_opp_ids_and_text_position["position"] = _df_the_opp_ids_and_text_position.apply(
                lambda row: choice(
                    [
                        'top left',
                        'top center',
                        'top right',
                        'bottom left',
                        'bottom center',
                        'bottom right',
                        'middle left',
                        'middle center',
                        'middle right',
                    ]
                ), axis=1
            )
            _df_the_data = _df_the_data.merge(right=_df_the_opp_ids_and_text_position, how="left", on="Opp - ID")

            # Make the list of BUs
            _the_bus = _df_the_data["Cpy - BU"].unique()

            # make figure
            _dict_the_figure: dict = {
                "data": [],
                "layout": {},
                "frames": []
            }

            # fill in most of layout
            _dict_the_figure["layout"]["xaxis"] = {"range": ["2022-06-01", "2023-05-31"], "title": "kick off"}
            _dict_the_figure["layout"]["yaxis"] = {"range": [-0.2, 1.2], "title": "Confidence level"}
            _dict_the_figure["layout"]["hovermode"] = "closest"
            _dict_the_figure["layout"]["updatemenus"] = [
                {
                    "buttons": [
                        {
                            "args": [None, {"frame": {"duration": 1000, "redraw": False},
                                            "fromcurrent": True, "transition": {"duration": 1000,
                                                                                "easing": "linear"}}],
                            "label": "Play",
                            "method": "animate"
                        },
                        {
                            "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate",
                                              "transition": {"duration": 0}}],
                            "label": "Pause",
                            "method": "animate"
                        }
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 87},
                    "showactive": False,
                    "type": "buttons",
                    "x": 0.1,
                    "xanchor": "right",
                    "y": 0,
                    "yanchor": "top"
                }
            ]

            _dict_the_sliders = {
                "active": 0,
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "font": {"size": 20},
                    "prefix": "Timestamp:",
                    "visible": True,
                    "xanchor": "right"
                },
                "transition": {"duration": 0, "easing": "cubic-in-out"},
                "pad": {"b": 10, "t": 50},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": []
            }

            # make data
            _time_the_timestamp = min(_df_the_data["Sp - Snapshot Date"])
            for i_bu in _the_bus:
                _df_the_data_by_timestamp = _df_the_data[_df_the_data["Sp - Snapshot Date"] == _time_the_timestamp]
                _df_the_data_by_timestamp_and_bu = _df_the_data_by_timestamp[
                    _df_the_data_by_timestamp["Cpy - BU"] == i_bu]

                _dict_the_data: dict = {
                    "x": list(_df_the_data_by_timestamp_and_bu["Sp - Kick Off Date"]),
                    "y": list(_df_the_data_by_timestamp_and_bu["Sp - Conf Lvl"]),
                    "mode": "markers+text",
                    "text": list(_df_the_data_by_timestamp_and_bu["Opp - ID"]),
                    "textposition": list(_df_the_data_by_timestamp_and_bu["position"]),
                    "marker": {
                        "sizemode": "area",
                        "sizeref": 1,
                        "size": list(_df_the_data_by_timestamp_and_bu["Sp - Effort"])
                    },
                    "name": i_bu
                }

                _dict_the_figure["data"].append(_dict_the_data)

            _dict_the_figure["data"].append(
                    {
                        "x": [_time_the_timestamp, _time_the_timestamp],
                        "y": [-0.2, 1.2],
                        "mode": "lines",
                        "name": "lines",
                        "ids": ["timestamp1", "timestamp2"]
                    }
            )

            # make frames
            for i_timestamp in _the_timestamps:
                _the_frame = {"data": [], "name": str(i_timestamp)}

                for i_bu in _the_bus:
                    _df_the_data_by_timestamp = _df_the_data[_df_the_data["Sp - Snapshot Date"] == i_timestamp]

                    _jsg = DataFrame()
                    _jsg["Opp - ID"] = _the_opp_ids
                    _jsg = pd.merge(
                        how="left",
                        right=_df_the_data_by_timestamp,
                        left=_jsg,
                        on="Opp - ID"
                    )

                    # _df_the_data_by_timestamp_and_bu = _df_the_data_by_timestamp[
                    #     _df_the_data_by_timestamp["Cpy - BU"] == i_bu]

                    _df_the_data_by_timestamp_and_bu = _jsg[
                        _jsg["Cpy - BU"] == i_bu]

                    _dict_the_data: dict = {
                        "x": list(_df_the_data_by_timestamp_and_bu["Sp - Kick Off Date"]),
                        "y": list(_df_the_data_by_timestamp_and_bu["Sp - Conf Lvl"]),
                        "mode": "markers+text",
                        "text": list(_df_the_data_by_timestamp_and_bu["Opp - ID"]),
                        "textposition": list(_df_the_data_by_timestamp_and_bu["position"]),
                        "marker": {
                            "sizemode": "area",
                            "sizeref": 1,
                            "size": list(_df_the_data_by_timestamp_and_bu["Sp - Effort"])
                        },
                        "name": i_bu,
                        "ids": list(_df_the_data_by_timestamp_and_bu["Opp - ID"])
                    }
                    _the_frame["data"].append(_dict_the_data)

                _the_frame["data"].append(
                    {
                        "x": [i_timestamp, i_timestamp],
                        "y": [-0.2, 1.2],
                        "mode": "lines",
                        "ids": ["timestamp1", "timestamp2"]
                    }
                )

                _dict_the_figure["frames"].append(_the_frame)

                _dict_the_slider_step = {"args": [
                    [str(i_timestamp)],
                    {"frame": {"duration": 1000, "redraw": False},
                     "mode": "immediate",
                     "transition": {"duration": 1000}}
                ],
                    "label": str(i_timestamp)[:10],
                    "method": "animate"}
                _dict_the_sliders["steps"].append(_dict_the_slider_step)

            _dict_the_figure["layout"]["sliders"] = [_dict_the_sliders]

            _figure_the_return: Figure = Figure(_dict_the_figure)

            #_figure_the_return.update_traces(textposition='top center')

            self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

            # return animations[selection]
            return _figure_the_return

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

    # Version that works... But I cannot
    # @callback(
    #     Output(BubblesAsDiv.const_str__wid__bubbles_as_graph, "figure"),
    #     Input("selection", "value")
    # )
    def jsg(self):

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called.")

        _df_the_data: DataFrame = self.session.dict_context.get(
            self.dict_config.get(self.const_str__config_label__str_dataframe_name_in_context)
        )

        _fun_parameters: dict = self.dict_config.get(self.const_str__config_label__dict_px_scatter_parameters, {})
        _df_the_data[_fun_parameters["animation_frame"]] = \
            _df_the_data[_fun_parameters["animation_frame"]].astype(str)
        # ["animation_frame"] = _df_the_data[_fun_parameters["animation_frame"]].astype(str)

        if _fun_parameters.get("range_x", "") == "auto":
            _fun_parameters["range_x"] = [
                min(_df_the_data[_fun_parameters["x"]]),
                max(_df_the_data[_fun_parameters["x"]])
            ]

        if _fun_parameters.get("range_y", "") == "auto":
            _fun_parameters["range_y"] = [
                min(_df_the_data[_fun_parameters["y"]]),
                max(_df_the_data[_fun_parameters["y"]])
            ]

        _figure_the_return: Figure = scatter(
            **{
                "data_frame": _df_the_data,
                **_fun_parameters
            }
        )

        _figure_the_return.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 100

        # df = px.data.gapminder()  # replace with your own data source
        # _local: Session = self.session
        #
        # animations = {
        #     'GDP - Scatter': px.scatter(
        #         df, x="gdpPercap", y="lifeExp", animation_frame="year",
        #         animation_group="country", size="pop", color="continent",
        #         hover_name="country", log_x=True, size_max=55,
        #         range_x=[100, 100000], range_y=[25, 90]),
        #     'Population - Bar': px.bar(
        #         df, x="continent", y="pop", color="continent",
        #         animation_frame="year", animation_group="country",
        #         range_y=[0, 4000000000]),
        # }
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning.")

        # return animations[selection]
        return _figure_the_return
