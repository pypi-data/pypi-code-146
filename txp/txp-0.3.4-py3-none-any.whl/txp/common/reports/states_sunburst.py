import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
from typing import List, Dict, Union
from txp.common.config import settings
import txp.common.reports.section as sections

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class StatesSunburst(sections.DataframeSection):
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
        super(StatesSunburst, self).__init__(
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
        daily_conditions_by_hrs = cls._transform_daily_conditions_to_hours(states_data)
        daily_conditions_by_hrs['observation_timestamp'] = daily_conditions_by_hrs['observation_timestamp'].dt.strftime("%H:%M")


        section: StatesSunburst = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            daily_conditions_by_hrs
        )

        return section.get_table_registry(
            **{
                'section': section,
            }
        )

    def get_dynamic_plot(self) -> Union[go.Figure]:
        fig = px.sunburst(
            path=[self.dataframe['sub-daily'], self.dataframe['condition']],
            values=self.dataframe['occurrence'],
        )
        fig.update_traces(textinfo="label+percent parent")

        figure = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "domain"}, {"type": "table"}]],
            subplot_titles=("Estados del activo", "Estados criticos"),
            horizontal_spacing=0.01
        )

        figure.add_trace(go.Sunburst(
            labels=fig['data'][0]['labels'].tolist(),
            parents=fig['data'][0]['parents'].tolist(),
            values=fig['data'][0]['values'].tolist(),
            ids=fig['data'][0]['ids'].tolist(),
            branchvalues='total',
            textinfo='label+percent entry'), col=1, row=1)

        important = self.dataframe[self.dataframe.condition == 'CRITICAL']

        figure.add_trace(go.Table(
            header=dict(values=['TURNO', 'CONDICION', 'MOMENTO EXACTO']),
            cells=dict(values=[important['sub-daily'], important['condition'], important['observation_timestamp']])),
            row=1, col=2)

        figure.update_traces(textinfo="label+percent parent", col=1, row=1)
        figure.update_layout(
            title='Distribución de los estados por turnos')

        return figure


    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        section = kwargs['section']
        fig = px.sunburst(
            path=[section.dataframe['sub-daily'], section.dataframe['condition']], values=section.dataframe['occurrence'],
        )
        fig.update_traces(textinfo="label+percent parent")

        figure = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "domain"}, {"type": "table"}]],
            subplot_titles=("Estados del activo", "Estados criticos"),
            horizontal_spacing=0.01
        )

        figure.add_trace(go.Sunburst(
            labels=fig['data'][0]['labels'].tolist(),
            parents=fig['data'][0]['parents'].tolist(),
            values=fig['data'][0]['values'].tolist(),
            ids=fig['data'][0]['ids'].tolist(),
            branchvalues='total',
            textinfo='label+percent entry'),
            col=1, row=1)

        important = section.dataframe[section.dataframe.condition == 'CRITICAL']

        figure.add_trace(go.Table(
            header=dict(values=['TURNO', 'CONDICION', 'MOMENTO EXACTO']),
            cells=dict(values=[important['sub-daily'], important['condition'], important['observation_timestamp']])),
            row=1, col=2)

        figure.update_traces(textinfo="label+percent parent", col=1, row=1)
        figure.update_layout(
            title='Distribución de los estados por turnos')

        img = cls._convert_plotly_to_pil(figure)

        return img


    @classmethod
    def _transform_daily_conditions_to_hours(cls, conditions_df: pd.DataFrame) -> pd.DataFrame:
        by_hour = pd.DataFrame(columns=["daily", "sub-daily", "observation_timestamp", "occurrence", "condition"])

        for hour in range(0, 23):
            subset = conditions_df[conditions_df.observation_timestamp.dt.hour == hour]
            states_by_hour = subset['condition'].value_counts()
            states = states_by_hour.to_dict()

            for key, value in states.items():
                day_time = subset['observation_timestamp'].median()
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
                        "observation_timestamp": subset['observation_timestamp'].median(),
                        "occurrence": value, "condition": key
                    }, ignore_index=True)
        return by_hour
