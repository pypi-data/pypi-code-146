import logging
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from typing import List, Dict, Union
from txp.common.config import settings
import txp.common.reports.section as sections
import datetime

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class StatesTransitionsLines(sections.Plot2dSection):
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
        super(StatesTransitionsLines, self).__init__(
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
        data = states_data.sort_values(
            by="observation_timestamp"
        ).replace({'Good': 'GOOD', 'Operative': 'OPERATIVE'}).reset_index()

        data_with_consecutive_state_values = cls.add_consecutive_states_values(data)

        lines: List[cls.Plot2DLine] = []

        x_axis = data_with_consecutive_state_values['observation_timestamp'].astype(str).to_list()
        y_axis = data_with_consecutive_state_values['condition'].to_list()
        lines.append(
            cls.Plot2DLine(
                x_axis, y_axis, 'transiciones entre estados'
            )
        )

        section: StatesTransitionsLines = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            ['Hora', 'Estados'],
            lines
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )
    @classmethod
    def add_consecutive_states_values(cls, states_df: pd.DataFrame) -> pd.DataFrame:
        product_df = states_df
        delta = datetime.timedelta(seconds=30)
        for i, row in states_df.iterrows():
            previous_prediction = states_df.iloc[i]['observation_timestamp'].to_pydatetime()
            try:
                post_prediction = states_df.iloc[i + 1]['observation_timestamp'].to_pydatetime()
                difference = (post_prediction - previous_prediction)
                if difference > datetime.timedelta(minutes=2):
                    add_row = {}
                    data_row = states_df.iloc[i].to_dict()
                    for k, v in data_row.items():
                        if k != 'index' or k != 'observation_timestamp':
                            add_row[k] = v
                            add_row['observation_timestamp'] = states_df.iloc[i + 1]['observation_timestamp'] - delta
                    del add_row['index']
                    print(add_row.keys())
                    product_df = product_df.append(add_row, ignore_index=True)
                else:
                    pass
            except(IndexError):
                pass

        return product_df.sort_values(
            by="observation_timestamp"
        ).reset_index()

    def get_dynamic_plot(self) -> Union[go.Figure]:
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=self.lines[0].x_values,
                    y=self.lines[0].y_values,
                    mode='lines',
                    name=self.lines[0].name,
                    showlegend=False
                ),
            ])

        fig.update_yaxes(
            categoryorder="array",
            categoryarray=list(self._color_map.keys())
            )
        fig.update_layout(title='Transiciones entre estados del activo')
        return fig


    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=section.lines[0].x_values,
                    y=section.lines[0].y_values,
                    mode='lines',
                    name=section.lines[0].name,
                    showlegend=False,
                ),
            ])

        fig.update_yaxes(
            categoryorder="array",
            categoryarray=list(section._color_map.keys())
        )
        fig.update_layout(title='Transiciones entre estados del activo')

        img = cls._convert_plotly_to_pil(fig)

        return img


class EventsTransitionsLines(sections.Plot2dSection):

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
        super(EventsTransitionsLines, self).__init__(
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
        data = events_data.sort_values(
            by="observation_timestamp"
        )

        lines: List[cls.Plot2DLine] = []
        x_axis = data['observation_timestamp'].astype(str).to_list()
        y_axis = data['event'].to_list()
        lines.append(
            cls.Plot2DLine(
                x_axis, y_axis, 'eventos'
            )
        )


        section: EventsTransitionsLines = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            ['Hora', 'Estados'],
            lines
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )

    def get_dynamic_plot(self) -> Union[go.Figure]:
        fig = go.Figure(data=go.Scatter(
            x=self.lines[0].x_values,
            y=self.lines[0].y_values,
            mode='lines'))

        fig.update_layout(title='Transiciones entre eventos ocurridos')
        return fig


    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']

        fig = go.Figure(data=go.Scatter(
            x=section.lines[0].x_values,
            y=section.lines[0].y_values,
            mode='lines'))

        fig.update_layout(title='Transiciones entre eventos ocurridos')

        img = cls._convert_plotly_to_pil(fig)

        return img
