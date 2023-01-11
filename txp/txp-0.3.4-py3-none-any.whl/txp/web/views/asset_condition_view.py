import txp.common.utils.bigquery_utils
import txp.common.utils.firestore_utils
from txp.web.core_components.main_view import MainView
from txp.web.core_components.app_profiles import AppProfile
import logging
from typing import Dict
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pytz
from txp.web.core_components.app_component import Card
from txp.common.config import settings
import datetime

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class AssetConditionsView(MainView):
    """The Device Health View"""

    def __init__(self):
        super(AssetConditionsView, self).__init__(component_key="asset_conditions_view")
        self.current_machine = None
        self.current_selected_assets = None
        self.current_machines_groups = None
        self.data = None
        self.report_type = None
        self.events = {}
        self.states = {}
        self.states_proportion = {}
        self._global_report = "Reporte global"
        self._specific_report = "Reporte por activo"
        self._default_value_report = f"Sin registro en los últimos {self._days_report} días"
        self.now = None
        self._monitoring_start = None
        self.color_map = {
            'Óptima': '3D62F6',
            'Buena': '79CF24',
            'Operativa': 'F6F03D',
            'Indefinida': '808080',
            'Crítica': 'F64F3D'
        }
        self.formatted_asset_name = None

        # The control attributes defined below are required for optimization purposes
        #   across streamlit reruns
        self._redraw_required: bool = True
        self._assets_resume_table: Card = None
        self._conditions_poltly_fig: go.Figure = None

    def get_associated_profile(self) -> AppProfile:
        return AppProfile.RESUMEN

    def implements_submenu(self) -> bool:
        return True

    @classmethod
    def get_display_name(cls) -> str:
        return "Condición de los Activos"

    def _build_submenu_state(self) -> Dict:
        return {}

    def _build_content_state(self) -> Dict:
        return {}

    def _formatted_data(self, data):
        """
        takes the project data and returns a formatted Dict.
        """
        machines_groups = {d["name"]: d for d in data["machines_groups"]}
        machines = {d["machine_id"]: d for d in data["machines"]}
        gateways = {d["gateway_id"]: d for d in data["gateways"]}
        edges = {d["logical_id"]: d for d in data["edges"]}

        data = {
            "machines_groups": machines_groups,
            "machines": machines,
            "gateways": gateways,
            "edges": edges,
        }
        return data

    def update_button_clicked(self):
        self._redraw_required = True
        self.get_data()

    def get_data(self):
        if self.data is None:
            db = txp.common.utils.firestore_utils.get_authenticated_client(
                self.app_state.authentication_info.role_service_account_credentials
            )

            data = txp.common.utils.firestore_utils.pull_recent_project_data(db, self._tenant_id)
            self.data = self._formatted_data(data)
            machines = list(self.data["machines"].keys())
            self.current_selected_assets = machines
            machines_groups = list(self.data["machines_groups"].keys())
            self.current_machines_groups = machines_groups[0]
            self.current_machine = machines[0]
            self.formatted_asset_name = self.formatting_readable_strings(self.current_machine)
            db.close()

            self.bqclient = txp.common.utils.bigquery_utils.get_authenticated_client(
                self.app_state.authentication_info.role_service_account_credentials
            )

        self._monitoring_start, self.now = self.monitoring_range()
        log.info(f"Your intervals for asset conditions: {self._monitoring_start} - {self.now}")

        # TODO: We can improve this with only 1 query !!!!
        #   And then just 'groupby' the received dataset

        for asset in self.data["machines"].keys():
            to_states_distribution = txp.common.utils.bigquery_utils.get_all_task_predictions_within_interval(
                    self._tenant_id,
                    self._states_dataset,
                    asset,
                    self._monitoring_start.astimezone(pytz.utc),
                    self.now.astimezone(pytz.utc),
                    self.bqclient
                )
            self.states_proportion.update({asset: to_states_distribution})

        for asset in self.data["machines"].keys():
            last_asset_state = txp.common.utils.bigquery_utils.get_last_task_prediction_for_asset(
                self._tenant_id,
                self._states_dataset,
                asset,
                self._days_report,
                self.bqclient
            )

            self.states.update({asset: last_asset_state})

    def monitoring_range(self):
        timezone = pytz.timezone("America/Mexico_City")
        mex_now = datetime.datetime.now(tz=timezone)
        mex_now_midnight = datetime.datetime.combine(
            mex_now.date(),
            datetime.time(hour=0, minute=0, second=0, microsecond=0)
        )
        mex_now_midnight = timezone.localize(mex_now_midnight)
        return mex_now_midnight, mex_now

    def change_utc_timezone(self, timestamp, date=True):
        timezone = pytz.timezone("America/Mexico_City")
        date_time = pd.to_datetime(timestamp, utc=True)
        new_timezone = date_time.astimezone(timezone)
        if date is False:
            strtime = new_timezone.strftime("%H:%M:%S")
        else:
            strtime = new_timezone.strftime("%m/%d/%Y %H:%M:%S")
        return strtime

    def utc_timestamp_to_local_datetime(self, timestamp):
        timezone = pytz.timezone("America/Mexico_City")
        date_time = pd.to_datetime(timestamp, utc=True)
        new_timezone = date_time.astimezone(timezone)
        return new_timezone

    def _render_submenu(self) -> None:
        st.markdown('\n')
        st.markdown('\n')
        assets = self.data['machines'].keys()
        st.markdown("**<p align='center'>Estado general</p>**", unsafe_allow_html=True)
        st.markdown('\n')
        st.markdown(f"**Activos monitoreados**: {len(assets)}")

        self.download_data_info_message()

        m = st.markdown("""
        <style>
        div.stButton > button:first-child {
        color: #0000CD;
        box-sizing: 5%;
        height: 2em;
        width: 100%;
        font-size:20px;
        border: 2px solid;
        border-color: #D3D3D3;
        border-radius: 10px;
        box-shadow: 1px 1px 1px 1px 
        rgba(0, 0, 0, 0.1);
        padding-top: 0px;
        padding-bottom: 0px;
        }
        .center {
        margin-left: auto;
        margin-right: auto;
        }
        </style>""", unsafe_allow_html=True)

        st.button('Actualizar', on_click=self.get_data)

    def get_last_event_for_state(self, events):
        event_timestamps = [pd.to_datetime(event['observation_timestamp']) for event in events]
        for event in events:
            event_timestamp = pd.to_datetime(event['observation_timestamp'])
            if event_timestamp == max(event_timestamps):
                return event
            else:
                pass

    def resume_table(self):
        if self._redraw_required:
            conditions = []
            dates = []

            for asset, state in self.states.items():
                if not state:
                    condition = self._default_value_report
                    date = self._default_value_report
                else:
                    condition = state['condition']
                    date = self.change_utc_timezone(state['observation_timestamp'])
                conditions.append(condition)
                dates.append(date)

            condition_list = []
            for condition in conditions:
                if not condition == self._default_value_report:
                    condition_list.append(self.app_state.condition_report.conditions_mapping[condition])
                else:
                    condition_list.append(self._default_value_report)

            resumen = {
                "Activo": [self.formatting_readable_strings(f_asset) for f_asset in self.states.keys()],
                "Condition": condition_list,
                "Date": dates,
            }

            self._assets_resume_table = Card(
                card_row=1,
                card_column_start=1,
                card_column_end=4,
                card_subheader="Resumen de los activos",
                content=resumen,
                labels=[
                    "Activo",
                    "Condición",
                    "Fecha de cambio de condición",
                ],
                vertical_style=False,
            )

        self.render_card(
            [
                self._assets_resume_table,
            ]
        )

    def download_data_info_message(self):
        strtime = self.now.strftime("%m/%d/%Y, %H:%M:%S")
        st.caption(f"Última actualización {strtime}")

    def states_proportion_plot(self, asset):
        if not self.states_proportion[asset].empty:
            if self._redraw_required:
                states_counts_serie: pd.Series = self.states_proportion[asset].condition.value_counts()
                states_count_dict = states_counts_serie.to_dict()
                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=list(states_count_dict.keys()),

                            values=list(states_count_dict.values()),
                            pull=[0.1, 0],
                        )
                    ]
                )
                fig.update_layout(
                    height=350,
                    width=450,
                    margin=dict(l=0, r=0, t=0, b=0),
                    font=dict(size=20)
                )
                generated_values_color_map = {}
                colors = np.array([''] * len(list(states_count_dict.values())), dtype=object)
                for i, (k, v) in enumerate(states_count_dict.items()):
                    generated_values_color_map[v] = self.color_map[self._asset_states_sp[k]]
                    colors[i] = generated_values_color_map[v]

                fig.update_traces(marker=dict(colors=colors))
                fig.update_layout(legend=dict(
                    xanchor="left",
                    yanchor="top",
                    x=-0.15,
                    font=dict(
                        size=16,
                        color="black"
                    ),
                ))
                fig.update_layout(
                    height=350,
                    width=450,
                    margin=dict(l=0, r=0, t=0, b=0),
                    font=dict(size=20))

                self._conditions_poltly_fig = fig

            # Draw the figure
            first_condition = self.states_proportion[asset]._get_value(0, 'observation_timestamp')
            log.info(f"The start raw timestamp is: {first_condition}")
            strtime: datetime.datetime = self.utc_timestamp_to_local_datetime(first_condition)
            log.info(f"The value of your strtime based on your timestamp is: {strtime}")
            last_condition = self.states_proportion[asset].iloc[-1]['observation_timestamp']
            strlasttime = self.utc_timestamp_to_local_datetime(last_condition)
            st.markdown(f"#### Registro de {strtime.strftime('%H:%M:%S')} a {strlasttime.strftime('%H:%M:%S')} del "
                        f"{strlasttime.strftime('%d-%m-%Y')}")
            st.markdown("##### Distribución de las condiciones", unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("***")

        else:
            st.markdown("Sin registro en el último día")

    def _render_content(self) -> None:
        if self.data is None:
            self.get_data()
        e = st.empty()
        with e.container():
            st.markdown(f"## {self._global_report} de la condición de los activos")
            self.resume_table()
            st.markdown(f"## {self._specific_report} de la condición de los activos")
            assets = self.data['machines'].keys()
            formated_assets = [self.formatting_readable_strings(f_asset) for f_asset in assets]
            for formated_asset, asset in list(zip(formated_assets, assets)):
                st.markdown(f"### {formated_asset}")
                self.states_proportion_plot(asset)
