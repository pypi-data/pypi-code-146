import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image
from typing import List, Dict, Union
import json
from txp.common.config import settings
import txp.common.reports.section as sections
from sklearn.ensemble import IsolationForest
log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class AnomalyDetectionStates(sections.Plot2dSection):
    _color_map = {
        'OPTIMAL': "rgb(61, 98, 246)",
        'GOOD': "rgb(121, 207, 36)",
        'OPERATIVE': "rgb(246, 240, 61)",
        'UNDEFINED': "rgb(246, 79, 61)",
        'CRITICAL': "rgb(246, 79, 61)",
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
        super(AnomalyDetectionStates, self).__init__(
            tenant_id, section_id, start_datetime, end_datetime,
            axes_names, lines, **kwargs
        )

    @classmethod
    def required_inputs(cls) -> List[sections.SectionInputEnum]:
        return [sections.SectionInputEnum.STATES]

    @classmethod
    def compute(cls, inputs: Dict[sections.SectionInputEnum, pd.DataFrame], section_event_payload: Dict) -> Dict:
        states_data = inputs[sections.SectionInputEnum.STATES]
        states_data['observation_timestamp'] = (
            pd.to_datetime(states_data['observation_timestamp'], utc=True)
            .dt.tz_convert("America/Mexico_City")
        )
        conditions_resample = cls._resample_conditions(states_data)
        anomaly_data = cls._get_anomaly_detection_data(conditions_resample)
        anomaly_detection = cls._anomaly_detection(anomaly_data)

        lines: List[cls.Plot2DLine] = []
        for state in cls._color_map.keys():
            if state in anomaly_detection:
                line_x_axis = anomaly_detection[state].index.astype(str).to_list()
                line_y_axis = anomaly_detection[state][state].to_list()

                anomalies_markers = anomaly_detection[state][anomaly_detection[state]["Outlier"] != 0.0]
                marker_x_axis = anomalies_markers.index.astype(str).to_list()
                marker_y_axis = anomalies_markers["Outlier"].to_list()

                lines.append(
                    cls.Plot2DLine(
                        line_x_axis, line_y_axis, f'line_{state}'
                    )
                )
                lines.append(
                    cls.Plot2DLine(
                        marker_x_axis, marker_y_axis, f'marker_{state}'
                    )
                )

        section: AnomalyDetectionStates = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            ['Hora', 'Ocurrencia de estados'],
            lines
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )


    @classmethod
    def _resample_conditions(cls, conditions_df: pd.DataFrame) -> pd.DataFrame:
        resample_df = conditions_df.resample(
            '15min',
            on='observation_timestamp'
        )['condition'].value_counts().unstack()

        fillna_df = resample_df.fillna(0)
        data = fillna_df.sort_values(
            by="observation_timestamp"
        )
        data["observation_timestamp"] = data.index
        data['observation_timestamp'] = data['observation_timestamp'].dt.strftime('%H:%M')
        return data

    @classmethod
    def _get_anomaly_detection_data(cls, hours_data: pd.DataFrame) -> Dict:
        data_by_hour = hours_data.set_index('observation_timestamp')
        anomaly_mapping_dict = {}
        for column in cls._color_map.keys():
            if column in data_by_hour.columns:
                test = pd.DataFrame()
                test[column] = data_by_hour[column]
                anomaly_mapping_dict.update({column: test})
        droped_nan_anomaly_mapping = {}
        for column in cls._color_map.keys():
            if column in anomaly_mapping_dict:
                data = anomaly_mapping_dict[column].dropna(subset=[column])
                droped_nan_anomaly_mapping.update({column: data})
        return droped_nan_anomaly_mapping

    @classmethod
    def _anomaly_detection(cls, droped_nan_anomaly_mapping: Dict):
        """
        Building dict for each data setting and getting anomaly detection
        """
        for column in cls._color_map.keys():
            if column in droped_nan_anomaly_mapping:
                if droped_nan_anomaly_mapping[column].empty:
                    print("empty")
                else:
                    # initializing Isolation Forest
                    clf = IsolationForest(max_samples="auto", contamination=0.01)

                    # training
                    clf.fit(droped_nan_anomaly_mapping[column])

                    # finding anomalies
                    droped_nan_anomaly_mapping[column]["Anomaly"] = clf.predict(
                        droped_nan_anomaly_mapping[column]
                    )

        for name, df in droped_nan_anomaly_mapping.items():
            df["Outlier"] = df.apply(
                    lambda x: x[name] if x["Anomaly"] == -1 else 0, axis=1
                )

        return droped_nan_anomaly_mapping

    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']
        fig = make_subplots(rows=1, cols=1)
        for line in section.lines:
            if 'line' in line.name:
                state = line.name.replace('line_', '')
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        name=state,
                        mode="lines",
                        line=dict(color=section._color_map[state]),
                    ),
                    row=1,
                    col=1,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        name="Anomalies",
                        mode="markers",
                        marker=dict(color="red", size=10, line=dict(color="red", width=1)),
                    )
                )
        names = set()
        fig.for_each_trace(
            lambda trace:
                trace.update(showlegend=False)
                if (trace.name in names) else names.add(trace.name)
        )

        fig.update_xaxes(matches=None, type='category')
        fig.update_layout(
            title='Anomalías detectadas',
            xaxis_title=section.axes_names[0],
            yaxis_title=section.axes_names[1])

        img = cls._convert_plotly_to_pil(fig)

        return img

    def get_dynamic_plot(self) -> Union[go.Figure]:
        fig = make_subplots(rows=1, cols=1)

        for line in self.lines:
            if 'line' in line.name:
                state = line.name.replace('line_', '')
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        name=state,
                        mode="lines",
                        line=dict(color=self._color_map[state]),
                    ),
                    row=1,
                    col=1,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        name="Anomalies",
                        mode="markers",
                        marker=dict(color="red", size=10, line=dict(color="red", width=1)),
                    )
                )

        names = set()
        fig.for_each_trace(
            lambda trace:
                trace.update(showlegend=False)
                if (trace.name in names) else names.add(trace.name)
        )

        fig.update_xaxes(matches=None, type='category')
        fig.update_layout(
            title='Anomalías detectadas',
            xaxis_title=self.axes_names[0],
            yaxis_title=self.axes_names[1],
            legend={'traceorder': 'normal'}
        )

        return fig


class AnomalyDetectionEvents(sections.Plot2dSection):

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
        super(AnomalyDetectionEvents, self).__init__(
            tenant_id, section_id, start_datetime, end_datetime,
            axes_names, lines, **kwargs
        )

    @classmethod
    def required_inputs(cls) -> List[sections.SectionInputEnum]:
        return [sections.SectionInputEnum.EVENTS]

    @classmethod
    def compute(cls, inputs: Dict[sections.SectionInputEnum, pd.DataFrame], section_event_payload: Dict) -> Dict:
        events_data = inputs[sections.SectionInputEnum.EVENTS]
        events_data['observation_timestamp'] = (
            pd.to_datetime(events_data['observation_timestamp'], utc=True)
            .dt.tz_convert("America/Mexico_City")
        )
        events_resample = cls._resample_conditions(events_data)
        anomaly_data = cls._get_anomaly_detection_data(events_resample)
        anomaly_detection = cls._anomaly_detection(anomaly_data)

        lines: List[cls.Plot2DLine] = []
        for event in events_resample.columns:
            if event != 'observation_timestamp':
                line_x_axis = anomaly_detection[event].index.astype(str).to_list()
                line_y_axis = anomaly_detection[event][event].to_list()

                anomalies_markers = anomaly_detection[event][anomaly_detection[event]["Outlier"] != 0.0]
                marker_x_axis = anomalies_markers.index.astype(str).to_list()
                marker_y_axis = anomalies_markers["Outlier"].to_list()

                lines.append(
                    cls.Plot2DLine(
                        line_x_axis, line_y_axis, f'line_{event}'
                    )
                )
                lines.append(
                    cls.Plot2DLine(
                        marker_x_axis, marker_y_axis, f'marker_{event}'
                    )
                )

        section: AnomalyDetectionEvents = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            ['Hora', 'Ocurrencia de eventos'],
            lines
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )


    @classmethod
    def _resample_conditions(cls, events_df: pd.DataFrame) -> pd.DataFrame:
        resample_df = events_df.resample(
            '15min',
            on='observation_timestamp'
        )['event'].value_counts().unstack()

        fillna_df = resample_df.fillna(0)
        data = fillna_df.sort_values(
            by="observation_timestamp"
        )
        data["observation_timestamp"] = data.index
        data['observation_timestamp'] = data['observation_timestamp'].dt.strftime('%H:%M')
        return data

    @classmethod
    def _get_anomaly_detection_data(cls, hours_data: pd.DataFrame) -> Dict:
        data_by_hour = hours_data.set_index('observation_timestamp')
        anomaly_mapping_dict = {}
        for column in data_by_hour.columns:
            if column != 'observation_timestamp':
                test = pd.DataFrame()
                test[column] = data_by_hour[column]
                anomaly_mapping_dict.update({column: test})
        droped_nan_anomaly_mapping = {}
        for column in anomaly_mapping_dict.keys():
            if column != 'observation_timestamp':
                data = anomaly_mapping_dict[column].dropna(subset=[column])
                droped_nan_anomaly_mapping.update({column: data})
        return droped_nan_anomaly_mapping

    @classmethod
    def _anomaly_detection(cls, droped_nan_anomaly_mapping: Dict):
        """
        Building dict for each data setting and getting anomaly detection
        """
        for event in droped_nan_anomaly_mapping.keys():
            if event != 'observation_timestamp':
                if droped_nan_anomaly_mapping[event].empty:
                    print("empty")
                else:
                    # initializing Isolation Forest
                    clf = IsolationForest(max_samples="auto", contamination=0.01)

                    # training
                    clf.fit(droped_nan_anomaly_mapping[event])

                    # finding anomalies
                    droped_nan_anomaly_mapping[event]["Anomaly"] = clf.predict(
                        droped_nan_anomaly_mapping[event]
                    )

        for name, df in droped_nan_anomaly_mapping.items():
            df["Outlier"] = df.apply(
                    lambda x: x[name] if x["Anomaly"] == -1 else 0, axis=1
                )

        return droped_nan_anomaly_mapping

    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']
        fig = make_subplots(rows=1, cols=1)
        for line in section.lines:
            if 'line' in line.name:
                state = line.name.replace('line_', '')
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        name=state,
                        mode="lines",
                    ),
                    row=1,
                    col=1,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        name="Anomalies",
                        mode="markers",
                        marker=dict(color="red", size=10, line=dict(color="red", width=1)),
                    )
                )
        names = set()
        fig.for_each_trace(
            lambda trace:
                trace.update(showlegend=False)
                if (trace.name in names) else names.add(trace.name)
        )

        fig.update_xaxes(matches=None, type='category')
        fig.update_layout(
            title='Anomalías detectadas',
            xaxis_title=section.axes_names[0],
            yaxis_title=section.axes_names[1])

        img = cls._convert_plotly_to_pil(fig)

        return img

    def get_dynamic_plot(self) -> Union[go.Figure]:
        fig = make_subplots(rows=1, cols=1)

        for line in self.lines:
            if 'line' in line.name:
                state = line.name.replace('line_', '')
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        name=state,
                        mode="lines",
                    ),
                    row=1,
                    col=1,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=line.x_values,
                        y=line.y_values,
                        name="Anomalies",
                        mode="markers",
                        marker=dict(color="red", size=10, line=dict(color="red", width=1)),
                    )
                )

        names = set()
        fig.for_each_trace(
            lambda trace:
                trace.update(showlegend=False)
                if (trace.name in names) else names.add(trace.name)
        )

        fig.update_xaxes(matches=None, type='category')
        fig.update_layout(
            title='Anomalías detectadas',
            xaxis_title=self.axes_names[0],
            yaxis_title=self.axes_names[1],
            legend={'traceorder': 'normal'}
        )

        return fig


class AnomalyDetectionRawData(sections.Plot2dSection):

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
        super(AnomalyDetectionRawData, self).__init__(
            tenant_id, section_id, start_datetime, end_datetime,
            axes_names, lines, **kwargs
        )

    @classmethod
    def required_inputs(cls) -> List[sections.SectionInputEnum]:
        return [sections.SectionInputEnum.RAW_TIME]

    @classmethod
    def compute(cls, inputs: Dict[sections.SectionInputEnum, pd.DataFrame], section_event_payload: Dict) -> Dict:
        raw_data = inputs[sections.SectionInputEnum.RAW_TIME]
        raw_data['observation_timestamp'] = (
            pd.to_datetime(raw_data['observation_timestamp'], utc=True)
                .dt.tz_convert("America/Mexico_City")
        )
        temperatures = cls._preprocessing_raw_data(raw_data)
        anomaly_detection = cls._anomaly_detection(temperatures)

        lines: List[cls.Plot2DLine] = []
        line_x_axis = anomaly_detection.index.astype(str).to_list()
        line_y_axis = anomaly_detection['data'].to_list()

        anomalies_markers = anomaly_detection[anomaly_detection["Outlier"] != 0.0]
        marker_x_axis = anomalies_markers.index.astype(str).to_list()
        marker_y_axis = anomalies_markers["Outlier"].to_list()

        lines.append(
            cls.Plot2DLine(
                line_x_axis, line_y_axis, 'line'
            )
        )
        lines.append(
            cls.Plot2DLine(
                marker_x_axis, marker_y_axis, 'marker'
            )
        )

        section: AnomalyDetectionRawData = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            ['Hora', 'Ocurrencia de estados'],
            lines
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )

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
    def _anomaly_detection(cls, hours_data: pd.DataFrame):
        """
        Building dict for each data setting and getting anomaly detection
        """
        data_by_hour = hours_data.set_index('observation_timestamp')

        # initializing Isolation Forest
        clf = IsolationForest(max_samples="auto", contamination=0.01)

        # training
        clf.fit(data_by_hour)

        # finding anomalies
        data_by_hour["Anomaly"] = clf.predict(
            data_by_hour
        )

        data_by_hour["Outlier"] = data_by_hour.apply(
            lambda x: x["data"] if x["Anomaly"] == -1 else 0, axis=1
        )
        return data_by_hour

    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']
        plot = go.Figure(data=[
            go.Scatter(
                x=section.lines[0].x_values,
                y=section.lines[0].y_values,
                mode="lines",
                name="Comportamiento"),
            go.Scatter(
                x=section.lines[1].x_values,
                y=section.lines[1].y_values,
                mode="markers",
                marker=dict(color="red", size=8, line=dict(color="red", width=1)),
                name="Anomalías")]
        )

        plot.update_layout(title='Anomalías detectadas en la temperatura')

        img = cls._convert_plotly_to_pil(plot)

        return img

    def get_dynamic_plot(self) -> Union[go.Figure]:
        plot = go.Figure(data=[
            go.Scatter(
                x=self.lines[0].x_values,
                y=self.lines[0].y_values,
                mode="lines",
                name="Comportamiento"),
            go.Scatter(
                x=self.lines[1].x_values,
                y=self.lines[1].y_values,
                mode="markers",
                marker=dict(color="red", size=8, line=dict(color="red", width=1)),
                name="Anomalías")]
        )

        plot.update_layout(title='Anomalías detectadas en la temperatura')

        return plot
