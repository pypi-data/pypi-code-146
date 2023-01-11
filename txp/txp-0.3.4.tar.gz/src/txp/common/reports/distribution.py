import logging
import pandas as pd
import plotly.express as px
from PIL import Image
from typing import List, Dict, Union
from txp.common.config import settings
import txp.common.reports.section as sections
import numpy as np
import pytz
import datetime
log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class StatesDistribution(sections.DataframeSection):
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
            dataframe: pd.DataFrame,
            **kwargs
    ):
        super(StatesDistribution, self).__init__(
            tenant_id, section_id, start_datetime, end_datetime, dataframe, **kwargs
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

        distribution = cls.get_distribution_df(states_data)

        section: StatesDistribution = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            distribution
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )


    def get_dynamic_plot(self) -> Union[px.pie]:
        fig = px.pie(
            self.dataframe,
            names='condition',
            values='occurrence',
        )

        states = self.dataframe.to_dict('list')
        generated_values_color_map = {}
        colors = np.array([''] * len(states['condition']), dtype=object)
        for i, v in enumerate(states['condition']):
            if v == 'Good':
                value = 'GOOD'
            elif v == 'Operative':
                value = 'OPERATIVE'
            else:
                value = v
            generated_values_color_map[value] = self._color_map[value]
            colors[i] = generated_values_color_map[value]
        fig.update_traces(marker=dict(colors=colors))

        fig.update_layout(
            height=350,
            width=450,
        )

        fig.update_layout(
            title='Distribución de los estados',
            )

        return fig

    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']

        fig = px.pie(
            section.dataframe,
            names='condition',
            values='occurrence',
        )

        states = section.dataframe.to_dict('list')
        generated_values_color_map = {}
        colors = np.array([''] * len(states['condition']), dtype=object)
        for i, v in enumerate(states['condition']):
            if v == 'Good':
                value = 'GOOD'
            elif v == 'Operative':
                value = 'OPERATIVE'
            else:
                value = v
            generated_values_color_map[value] = section._color_map[value]
            colors[i] = generated_values_color_map[value]
        fig.update_traces(marker=dict(colors=colors))

        fig.update_layout(
            title='Distribución de los estados',
            )

        img = cls._convert_plotly_to_pil(fig)

        return img

    @classmethod
    def get_distribution_df(cls, conditions_df: pd.DataFrame) -> pd.DataFrame:
        df = pd.DataFrame(columns=["occurrence", "condition"])
        states_counts_serie: pd.Series = conditions_df.condition.value_counts()
        states_count_dict = states_counts_serie.to_dict()

        for key, value in states_count_dict.items():
            df = df.append(
                {
                    "occurrence": value,
                    "condition": key
                },
                ignore_index=True
            )
        return df


class EventsDistribution(sections.DataframeSection):

    def __init__(
            self,
            tenant_id,
            section_id,
            start_datetime: str,
            end_datetime: str,
            dataframe: pd.DataFrame,
            **kwargs
    ):
        super(EventsDistribution, self).__init__(
            tenant_id, section_id, start_datetime, end_datetime, dataframe, **kwargs
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

        distribution = cls.get_distribution_df(events_data)

        section: EventsDistribution = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            distribution
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )


    def get_dynamic_plot(self) -> Union[px.pie]:
        fig = px.pie(
            self.dataframe,
            names='event',
            values='occurrence',
        )

        fig.update_layout(
            title='Distribución de los eventos',
            legend=dict(
            font=dict(
                color="black"
            ),
        ))

        return fig

    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']

        fig = px.pie(
            section.dataframe,
            names='event',
            values='occurrence',
        )

        fig.update_layout(
            title='Distribución de los eventos',
            legend=dict(
                font=dict(
                    color="black"
                ),
            ))

        img = cls._convert_plotly_to_pil(fig)

        return img

    @classmethod
    def get_distribution_df(cls, events_df: pd.DataFrame) -> pd.DataFrame:
        df = pd.DataFrame(columns=["occurrence", "event"])
        events_counts_serie: pd.Series = events_df.event.value_counts()
        events_count_dict = events_counts_serie.to_dict()

        chars = '[,"]"'
        for key, value in events_count_dict.items():
            event = key.translate(str.maketrans('', '', chars))
            multilabel_asimilation = event.replace(' ', '/')
            df = df.append(
                {
                    "occurrence": value,
                    "event": multilabel_asimilation
                },
                ignore_index=True
            )

        return df