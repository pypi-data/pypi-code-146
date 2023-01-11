import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image
from typing import List, Dict, Union
from txp.common.config import settings
import txp.common.reports.section as sections
from prophet import Prophet
import json
import plotly

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class StatesForecasting(sections.Plot2dSection):
    _color_map = {
        'OPTIMAL': '#3D62F6',
        'GOOD': '#79CF24',
        'OPERATIVE': '#F6F03D',
        'UNDEFINED': '#808080',
        'CRITICAL': '#F64F3D'
    }

    def __init__(
            self,
            tenant_id,
            section_id,
            start_datetime: str,
            end_datetime: str,
            axes_names: List[str],
            lines,
            **kwargs
    ):
        super(StatesForecasting, self).__init__(
            tenant_id, section_id, start_datetime, end_datetime,
            axes_names, lines, **kwargs
        )

    @classmethod
    def required_inputs(cls) -> List[sections.SectionInputEnum]:
        return [sections.SectionInputEnum.STATES]

    @classmethod
    def compute(cls, inputs: Dict[sections.SectionInputEnum, pd.DataFrame], section_event_payload: Dict) -> Dict:
        # Converts Data timestamp to datetime objects
        states_data = inputs[sections.SectionInputEnum.STATES]

        if not states_data.size:
            log.info(f"Not received states to compute {cls.__name__}")
            return {}

        states_data['observation_timestamp'] = (
            pd.to_datetime(states_data['observation_timestamp'], utc=True)
            .dt.tz_convert("America/Mexico_City")
        )

        # Groups by hrs
        conditions_resample = cls._resample_conditions(states_data)
        forecasting_data = cls.getting_forecasting_data(conditions_resample)

        lines: List[cls.Plot2DLine] = []
        for state in cls._color_map.keys():
            if state in conditions_resample:
                forecasting_x_axis = forecasting_data["ds"].to_list()
                forecasting_y_axis = forecasting_data[f"forecasting_{state}"].to_list()

                str_x_axis = conditions_resample['observation_timestamp'].astype(str)
                x_axis = str_x_axis.to_list()
                y_axis = conditions_resample[state].to_list()

                lines.append(
                    cls.Plot2DLine(
                        x_axis, y_axis, state
                    )
                )
                lines.append(
                    cls.Plot2DLine(
                        forecasting_x_axis, forecasting_y_axis, f"forecasting_{state}"
                    )
                )


        section: StatesForecasting = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            ['Fecha', 'Pronóstico'],
            lines
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )

    def get_dynamic_plot(self) -> Union[go.Figure]:
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Datos previos", "Pronóstico"))

        for line in self.lines:
            if 'forecasting' in line.name:
                state = line.name.replace('forecasting_', '')
                fig.add_trace(
                        go.Scatter(
                            x=line.x_values,
                            y=line.y_values,
                            mode='lines',
                            line=dict(color=self._color_map[state]),
                            showlegend=False,
                        ),
                        row=1,
                        col=2,
                    )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        mode="lines",
                        line=dict(color=self._color_map[line.name]),
                        name=line.name
                    ),
                    row=1,
                    col=1,
                )

        fig.update_layout(
            title='Pronóstico de los estados',
            xaxis_title=self.axes_names[0],
            yaxis_title=self.axes_names[1],)

        return fig


    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Datos previos", "Pronóstico"))

        for line in section.lines:
            if 'forecasting' in line.name:
                state = line.name.replace('forecasting_', '')
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        mode='lines',
                        line=dict(color=section._color_map[state]),
                        showlegend=False,
                    ),
                    row=1,
                    col=2,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        mode="lines",
                        line=dict(color=section._color_map[line.name]),
                        name=line.name
                    ),
                    row=1,
                    col=1,
                )

        fig.update_layout(
            title='Pronóstico de los estados',
            xaxis_title=section.axes_names[0],
            yaxis_title=section.axes_names[1], )

        img = cls._convert_plotly_to_pil(fig)

        return img


    @classmethod
    def _resample_conditions(cls, conditions_df: pd.DataFrame) -> pd.DataFrame:
        resample_df =conditions_df.resample(
            '15min',
            on='observation_timestamp'
        )['condition'].value_counts().unstack()

        fillna_df = resample_df.fillna(0)
        data = fillna_df.sort_values(
            by="observation_timestamp"
        )
        data["observation_timestamp"] = data.index
        return data

    @classmethod
    def prophet_method(cls, previous_data, values_column):
        """Use prophet to get forecasting data."""
        periods = len(previous_data.index)
        previous_data.rename(
            columns={values_column: "y", "observation_timestamp": "ds"}, inplace=True
        )
        previous_data["ds"] = (previous_data['ds'] + pd.Timedelta(days=1)).dt.tz_localize(None)

        # setting max and min
        previous_data['cap'] = previous_data['y'].max()
        previous_data['floor'] = 0

        m = Prophet(changepoint_prior_scale=0.01, growth='logistic').fit(previous_data)
        future = m.make_future_dataframe(periods=periods, freq="15 min")
        future['floor'] = 0
        future['cap'] = previous_data['y'].max()

        forecast = m.predict(future)
        return [forecast["yhat"], forecast["ds"]]

    @classmethod
    def getting_forecasting_data(cls, grouped_by_hour: pd.DataFrame) -> pd.DataFrame:
        """Get forecasting data."""
        forecast_df = pd.DataFrame()

        for column_name in cls._color_map.keys():
            if column_name in grouped_by_hour.columns:
                forecast_by_condition = grouped_by_hour.loc[
                                        :, [column_name, "observation_timestamp"]
                                        ]

                if forecast_by_condition.size < 4:  # size returns num rows times num cols
                    log.info(f"Could not compute forecast for colum_name, because less than 2 rows")
                    continue

                forecasting_values = cls.prophet_method(forecast_by_condition, column_name)
                forecast_df[f"forecasting_{column_name}"] = forecasting_values[0]
                forecast_df["ds"] = forecasting_values[1]

                forecast_df['ds'] = forecast_df['ds'].astype(str)

        return forecast_df

class EventsForecasting(sections.Plot2dSection):

    _default_colors = plotly.colors.DEFAULT_PLOTLY_COLORS

    def __init__(
            self,
            tenant_id,
            section_id,
            start_datetime: str,
            end_datetime: str,
            axes_names: List[str],
            lines,
            **kwargs
    ):
        super(EventsForecasting, self).__init__(
            tenant_id, section_id, start_datetime, end_datetime,
            axes_names, lines, **kwargs
        )

    @classmethod
    def required_inputs(cls) -> List[sections.SectionInputEnum]:
        return [sections.SectionInputEnum.EVENTS]

    @classmethod
    def compute(cls, inputs: Dict[sections.SectionInputEnum, pd.DataFrame], section_event_payload: Dict) -> Dict:
        # Converts Data timestamp to datetime objects
        events_data = inputs[sections.SectionInputEnum.EVENTS]

        if not events_data.size:
            log.info(f"Not received events to compute {cls.__name__}")
            return {}

        events_data['observation_timestamp'] = (
            pd.to_datetime(events_data['observation_timestamp'], utc=True)
            .dt.tz_convert("America/Mexico_City")
        )

        events_resample = cls._resample_conditions(events_data)
        forecasting_data = cls.getting_forecasting_data(events_resample)

        lines: List[cls.Plot2DLine] = []
        for event in events_resample.columns:
            if event != 'observation_timestamp':
                forecasting_x_axis = forecasting_data["ds"].to_list()
                forecasting_y_axis = forecasting_data[f"forecasting_{event}"].to_list()

                str_x_axis = events_resample['observation_timestamp'].astype(str)
                x_axis = str_x_axis.to_list()
                y_axis = events_resample[event].to_list()

                lines.append(
                    cls.Plot2DLine(
                        x_axis, y_axis, event
                    )
                )
                lines.append(
                    cls.Plot2DLine(
                        forecasting_x_axis, forecasting_y_axis, f"forecasting_{event}"
                    )
                )


        section: EventsForecasting = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            ['Fecha', 'Pronóstico'],
            lines
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )

    @classmethod
    def create_color_map(cls, lines: List) -> Dict:
        _color_map = {}
        for i, line in enumerate(lines):
            if not 'forecasting' in line.name:
                _color_map.update({line.name: cls._default_colors[i]})
        return  _color_map

    def get_dynamic_plot(self) -> Union[go.Figure]:
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Datos previos", "Pronóstico"))
        _color_map = self.create_color_map(self.lines)

        for line in self.lines:
            if 'forecasting' in line.name:
                event = line.name.replace('forecasting_', '')
                fig.add_trace(
                        go.Scatter(
                            x=line.x_values,
                            y=line.y_values,
                            mode='lines',
                            name=event,
                            line={'color':_color_map[event]},
                            showlegend=False
                        ),
                        row=1,
                        col=2,
                    )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        mode="lines",
                        name=line.name,
                        line={'color': _color_map[line.name]},
                    ),
                    row=1,
                    col=1,
                )

        fig.update_layout(
            title='Pronóstico de los eventos',
            xaxis_title=self.axes_names[0],
            yaxis_title=self.axes_names[1],)

        return fig


    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Datos previos", "Pronóstico"))
        _color_map = cls.create_color_map(section.lines)

        for line in section.lines:
            if 'forecasting' in line.name:
                event = line.name.replace('forecasting_', '')
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        mode='lines',
                        line={'color': _color_map[event]},
                        showlegend=False,
                    ),
                    row=1,
                    col=2,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        mode="lines",
                        name=line.name,
                        line={'color': _color_map[line.name]},
                    ),
                    row=1,
                    col=1,
                )

        fig.update_layout(
            title='Pronóstico de los eventos',
            xaxis_title=section.axes_names[0],
            yaxis_title=section.axes_names[1], )

        img = cls._convert_plotly_to_pil(fig)

        return img


    @classmethod
    def _resample_conditions(cls, events_df: pd.DataFrame) -> pd.DataFrame:
        resample_df =events_df.resample(
            '15min',
            on='observation_timestamp'
        )['event'].value_counts().unstack()

        fillna_df = resample_df.fillna(0)
        data = fillna_df.sort_values(
            by="observation_timestamp"
        )
        data["observation_timestamp"] = data.index
        return data

    @classmethod
    def prophet_method(cls, previous_data, values_column):
        """Use prophet to get forecasting data."""
        periods = len(previous_data.index)
        previous_data.rename(
            columns={values_column: "y", "observation_timestamp": "ds"}, inplace=True
        )
        previous_data["ds"] = (previous_data['ds'] + pd.Timedelta(days=1)).dt.tz_localize(None)

        # setting max and min
        previous_data['cap'] = previous_data['y'].max()
        previous_data['floor'] = 0

        m = Prophet(changepoint_prior_scale=0.01, growth='logistic').fit(previous_data)
        future = m.make_future_dataframe(periods=periods, freq="15 min")
        future['cap'] = previous_data['y'].max()
        future['floor'] = 0

        forecast = m.predict(future)
        return [forecast["yhat"], forecast["ds"]]

    @classmethod
    def getting_forecasting_data(cls, grouped_by_hour: pd.DataFrame) -> pd.DataFrame:
        """Get forecasting data."""
        forecast_df = pd.DataFrame()

        for column_name in grouped_by_hour.columns:
            if column_name != 'observation_timestamp':
                forecast_by_event = grouped_by_hour.loc[
                                        :, [column_name, "observation_timestamp"]
                                        ]

                if forecast_by_event.size < 4:  # size returns num rows times num cols
                    log.info(f"Could not compute forecast for colum_name, because less than 2 rows")
                    continue

                forecasting_values = cls.prophet_method(forecast_by_event, column_name)
                forecast_df[f"forecasting_{column_name}"] = forecasting_values[0]
                forecast_df["ds"] = forecasting_values[1]

                forecast_df['ds'] = forecast_df['ds'].astype(str)

        return forecast_df

class RawDataForecasting(sections.Plot2dSection):

    def __init__(
            self,
            tenant_id,
            section_id,
            start_datetime: str,
            end_datetime: str,
            axes_names: List[str],
            lines,
            **kwargs
    ):
        super(RawDataForecasting, self).__init__(
            tenant_id, section_id, start_datetime, end_datetime,
            axes_names, lines, **kwargs
        )

    @classmethod
    def required_inputs(cls) -> List[sections.SectionInputEnum]:
        return [sections.SectionInputEnum.RAW_TIME]

    @classmethod
    def compute(cls, inputs: Dict[sections.SectionInputEnum, pd.DataFrame], section_event_payload: Dict) -> Dict:
        # Converts Data timestamp to datetime objects
        raw_data = inputs[sections.SectionInputEnum.RAW_TIME]

        if not raw_data.size:
            log.info(f"Not received states to compute {cls.__name__}")
            return {}

        raw_data['observation_timestamp'] = (
            pd.to_datetime(raw_data['observation_timestamp'], utc=True)
            .dt.tz_convert("America/Mexico_City")
        )

        data = cls._preprocessing_raw_data(raw_data)

        forecasting_data = cls.getting_forecasting_data(data)

        lines: List[cls.Plot2DLine] = []
        forecasting_x_axis = forecasting_data["ds"].astype(str).to_list()
        forecasting_y_axis = forecasting_data["forecasting_data"].to_list()

        str_x_axis = data['observation_timestamp'].astype(str)
        x_axis = str_x_axis.to_list()
        y_axis = data['data'].to_list()

        lines.append(
            cls.Plot2DLine(
                x_axis, y_axis, 'data previa'
            )
        )
        lines.append(
            cls.Plot2DLine(
                forecasting_x_axis, forecasting_y_axis, "forecasting"
            )
        )


        section: RawDataForecasting = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            ['Hora', 'Pronóstico'],
            lines
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )

    def get_dynamic_plot(self) -> Union[go.Figure]:
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Datos previos", "Pronóstico"))

        fig.add_trace(
            go.Scatter(
                x=self.lines[0].x_values,
                y=self.lines[0].y_values,
                mode='lines',
                name=self.lines[0].name,
                line=dict(color="rgb(246, 79, 61)"),
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=self.lines[1].x_values,
                y=self.lines[1].y_values,
                mode="lines",
                name=self.lines[1].name,
                line=dict(color="rgb(121, 207, 36)"),
            ),
            row=1,
            col=2,
        )

        fig.update_layout(
            title='Pronóstico de la temperatura',
            xaxis_title=self.axes_names[0],
            yaxis_title=self.axes_names[1], )

        return fig


    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Datos previos", "Pronóstico"))

        fig.add_trace(
            go.Scatter(
                x=section.lines[0].x_values,
                y=section.lines[0].y_values,
                mode='lines',
                name=section.lines[0].name,
                line=dict(color="rgb(246, 79, 61)"),
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=section.lines[1].x_values,
                y=section.lines[1].y_values,
                mode="lines",
                line=dict(color="rgb(246, 79, 61)"),
                showlegend=False
            ),
            row=1,
            col=2,
        )

        fig.update_layout(
            title='Pronóstico de la temperatura',
            xaxis_title=section.axes_names[0],
            yaxis_title=section.axes_names[1], )

        img = cls._convert_plotly_to_pil(fig)

        return img

    @classmethod
    def data_value_reformatting(self, value):
        """
        for temperature values, reformating values as an apply in Serie
        """
        raw_values = value[0]["values"][0]
        return float(raw_values)

    @classmethod
    def _preprocessing_raw_data(cls, raw_data_df: pd.DataFrame) -> pd.DataFrame:
        temperature = raw_data_df[raw_data_df['perception_name'] == 'Temperature']
        temperature["data"] = temperature["data"].apply(cls.data_value_reformatting)
        df = temperature.loc[:, ["data", 'observation_timestamp']]
        data = df.sort_values(by="observation_timestamp")
        return data

    @classmethod
    def prophet_method(cls, previous_data, values_column):
        """Use prophet to get forecasting data."""
        periods = len(previous_data.index)
        data = previous_data.rename(
            columns={values_column: "y", "observation_timestamp": "ds"}
        )
        data["ds"] = (data['ds'] + pd.Timedelta(hours=2)).dt.tz_localize(None)
        # setting max and min
        data['cap'] = data['y'].max()
        data['floor'] = data['y'].min()

        m = Prophet(changepoint_prior_scale=0.01, growth='logistic').fit(data)
        future = m.make_future_dataframe(periods=periods, freq="min")
        future['floor'] = data['y'].min()
        future['cap'] = data['y'].max()
        forecast = m.predict(future)
        return [forecast["yhat"], forecast["ds"]]

    @classmethod
    def getting_forecasting_data(cls, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Get forecasting data."""
        forecast_df = pd.DataFrame()

        forecasting_values = cls.prophet_method(raw_data, 'data')
        forecast_df["forecasting_data"] = forecasting_values[0]
        forecast_df["ds"] = forecasting_values[1]
        data = forecast_df.sort_values(by="ds")

        return data
