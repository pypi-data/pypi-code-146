import logging
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
from typing import List, Dict, Union
from txp.common.config import settings
import txp.common.reports.section as sections

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class StatesTransitions(sections.DataframeSection):
    _color_map = {
        'OPTIMAL': '#3D62F6',
        'GOOD': '#79CF24',
        'Good': '#79CF24',
        'Operative': '#F6F03D',
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
        super(StatesTransitions, self).__init__(
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

        # Groups by hrs
        daily_conditions_resample = cls._transform_daily_conditions_resample(states_data)
        daily_conditions_resample['observation_timestamp'] = daily_conditions_resample['observation_timestamp'].dt.strftime("%H:%M")


        section: StatesTransitions = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            daily_conditions_resample
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )

    def get_dynamic_plot(self) -> Union[go.Figure]:
        fig = px.bar(
            self.dataframe,
            x="observation_timestamp",
            y="occurrence",
            color="condition",
            color_discrete_map=self._color_map
        )
        fig.update_xaxes(title=' ')
        fig.update_xaxes(matches=None, type='category')
        fig.update_layout(title='Estados del activo')
        return fig


    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']
        fig = px.bar(
            section.dataframe,
            x="observation_timestamp",
            y="occurrence",
            color="condition",
            color_discrete_map=section._color_map
        )
        fig.update_xaxes(title=' ')
        fig.update_xaxes(matches=None, type='category')
        fig.update_layout(title='Estados del activo')

        img = cls._convert_plotly_to_pil(fig)

        return img


    @classmethod
    def _transform_daily_conditions_resample(cls, conditions_df: pd.DataFrame) -> pd.DataFrame:
        by_hour = pd.DataFrame(columns=["daily", "sub-daily", "observation_timestamp", "occurrence", "condition"])

        resample_df = conditions_df.resample(
            '15min',
            on='observation_timestamp'
        )['condition'].value_counts().unstack()

        fillna_df = resample_df.fillna(0)
        data = fillna_df.sort_values(
            by="observation_timestamp"
        )
        data["observation_timestamp"] = data.index
        states = data.to_dict('records')

        for record in states:
            for key, value in record.items():
                if key != 'observation_timestamp':
                    day_time = record['observation_timestamp']
                    if day_time.hour < 12:
                        daily = "morning"
                        if day_time.hour < 6:
                            sub_daily = "12am-6am"
                        else:
                            sub_daily = "6am-12pm"
                    else:
                        daily = "afternoon"
                        if day_time.hour < 18:
                            sub_daily = "12pm-6pm"
                        else:
                            sub_daily = "6pm-12am"
                    by_hour = by_hour.append(
                        {
                            "daily": daily, "sub-daily": sub_daily,
                            "observation_timestamp": record['observation_timestamp'],
                            "occurrence": value, "condition": key
                        }, ignore_index=True)
        return by_hour


class EventsTransitions(sections.DataframeSection):

    def __init__(
            self,
            tenant_id,
            section_id,
            start_datetime: str,
            end_datetime: str,
            dataframe: pd.DataFrame,
            **kwargs
    ):
        super(EventsTransitions, self).__init__(
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
            log.info(f"Not received states to compute {cls.__name__}")
            return {}

        events_data['observation_timestamp'] = (
            pd.to_datetime(events_data['observation_timestamp'], utc=True)
            .dt.tz_convert("America/Mexico_City")
        )

        daily_events_resample = cls._transform_daily_events_resample(events_data)
        daily_events_resample['observation_timestamp'] = daily_events_resample['observation_timestamp'].dt.strftime("%H:%M")

        section: EventsTransitions = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            daily_events_resample
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )

    def get_dynamic_plot(self) -> Union[go.Figure]:
        fig = px.bar(
            self.dataframe,
            x="observation_timestamp",
            y="occurrence",
            color="event"
        )
        fig.update_xaxes(title=' ')
        fig.update_xaxes(matches=None, type='category')
        fig.update_layout(title='Eventos del activo')
        return fig


    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']
        fig = px.bar(
            section.dataframe,
            x="observation_timestamp",
            y="occurrence",
            color="event",
        )
        fig.update_xaxes(title=' ')
        fig.update_xaxes(matches=None, type='category')
        fig.update_layout(title='Eventos del activo')

        img = cls._convert_plotly_to_pil(fig)

        return img


    @classmethod
    def _transform_daily_events_resample(cls, events_df: pd.DataFrame) -> pd.DataFrame:
        by_hour = pd.DataFrame(columns=["daily", "sub-daily", "observation_timestamp", "occurrence", "event"])

        chars = '[,"]"'

        resample_df = events_df.resample(
            '15min',
            on='observation_timestamp'
        )['event'].value_counts().unstack()

        fillna_df = resample_df.fillna(0)
        data = fillna_df.sort_values(
            by="observation_timestamp"
        )
        data["observation_timestamp"] = data.index
        states = data.to_dict('records')

        for record in states:
            for key, value in record.items():
                if key != 'observation_timestamp':
                    day_time = record['observation_timestamp']
                    if day_time.hour < 12:
                        daily = "morning"
                        if day_time.hour < 6:
                            sub_daily = "12am-6am"
                        else:
                            sub_daily = "6am-12pm"
                    else:
                        daily = "afternoon"
                        if day_time.hour < 18:
                            sub_daily = "12pm-6pm"
                        else:
                            sub_daily = "6pm-12am"
                    event = key.translate(str.maketrans('', '', chars))
                    multilabel_asimilation = event.replace(' ', '/')
                    by_hour = by_hour.append(
                        {
                            "daily": daily, "sub-daily": sub_daily,
                            "observation_timestamp": record['observation_timestamp'],
                            "occurrence": value, "event": multilabel_asimilation
                        }, ignore_index=True)
        return by_hour