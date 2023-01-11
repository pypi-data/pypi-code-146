from txp.common.utils import bigquery_utils
from txp.web.controllers.conveyors_dashboard import TransportationLineConnectivity
from txp.web.core_components.app_profiles import AppProfile
from txp.web.core_components.main_view import MainView
import txp.web.views.analytics.complex_analytics as complex_utils
from typing import Dict
import streamlit as st
import logging
import datetime
import pytz
import dataclasses
import pandas as pd
import txp.web.new_views.rpm_util as rpm
import enum
import os

# TODO: This might be a problem. The logging configuration is being taken from `txp` package
from txp.common.config import settings
from txp.web.views.analytics_view import DataRequest

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


_current_directory = os.path.dirname(os.path.realpath(__file__))

class LineHealthEnum(enum.Enum):
    """Todo: review this classification with system stakeholders"""

    HEALTHY = 0
    REGULAR = 1
    DANGER = 2


@dataclasses.dataclass
class EquipmentLinesTableEntry:
    """A dataclass to contain the Rows information shown in the
    machines lines table."""

    line: str
    num_equipments: int
    line_health: LineHealthEnum


class GeneralDashboard(MainView):
    def __init__(self):
        super(GeneralDashboard, self).__init__(component_key="general_dashboard")

    #####################################################
    # Data organization methods
    #####################################################
    def _get_equipment_lines_rows(self) -> pd.DataFrame:
        machines_groups_table = self.app_state.project_model.machines_groups_table
        pd_rows = []
        for group_name in machines_groups_table:
            pd_rows.append(
                {
                    "Línea": machines_groups_table[group_name]["name"],
                    "Número de Equipos": f"{len(machines_groups_table[group_name]['machines'])}",
                }
            )
        df = pd.DataFrame(data=pd_rows)
        return df

    def _get_line_machines_rows(self, line_name: str) -> pd.DataFrame:
        """Should return a Dataframe where each row corresponds
        to a Machine from the specified line"""
        machine_group = self.app_state.project_model.machines_groups_table[line_name]
        pd_rows = []
        for machine_name in machine_group["machines"]:
            rpm = (
                self.app_state.conveyors_dashboard[line_name]
                ._machine_metrics[machine_name]
                .last_rpm_value
            )
            temperature = (
                self.app_state.conveyors_dashboard[line_name]
                ._machine_metrics[machine_name]
                .last_temperature_value
            )
            last_seen_date = (
                self.app_state.conveyors_dashboard[line_name]
                ._machine_metrics[machine_name]
                .last_seen_date
            )
            total_worked_secs = (
                self.app_state.conveyors_dashboard[line_name]
                ._machine_metrics[machine_name]
                .total_worked_seconds
            )
            pd_rows.append(
                {
                    "Equipo": machine_name,
                    "Temperatura": f"{temperature:.2f} °C",
                    "Velocidad": f"{int(rpm)} RPM",
                    "Horas Trabajadas": f"{float(total_worked_secs/3600):.2f} Hrs",
                    "Visto Por Última vez": f"{last_seen_date}"
                    if last_seen_date
                    else "Hace más de 2 horas.",
                }
            )
        df = pd.DataFrame(data=pd_rows)
        return df

    #####################################################
    # Screen drawing methods
    #####################################################
    def _render_equipments_lines(self):
        # Hide the index col
        # CSS to inject contained in a string
        hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """

        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        # Actual content
        st.subheader("Líneas de producción")
        st.table(self._get_equipment_lines_rows())
        st.markdown("-----")

    def _render_line_connectivity(self, machine_group_name):
        hide_img_fs = """
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        """
        st.markdown(hide_img_fs, unsafe_allow_html=True)

        conn_status = self.app_state.conveyors_dashboard[
            machine_group_name
        ].get_connectivity()
        if conn_status == TransportationLineConnectivity.OPTIMAL:
            st.image(f"{_current_directory}/../resources/images/connectivity_signal/good_signal.jpg")
        elif conn_status == TransportationLineConnectivity.REGULAR:
            st.image(f"{_current_directory}/../resources/images/connectivity_signal/regular_signal.jpg")
        else:
            st.image(f"{_current_directory}/../resources/images/connectivity_signal/bad_signal.jpg")

    def _render_line_detailed_section(self, machine_group_name: str):
        """Renders the machine_group_name received"""
        machine_group = self.app_state.project_model.machines_groups_table[
            machine_group_name
        ]
        st.subheader(machine_group_name)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Número de Equipos", len(machine_group["machines"]))

        with c2:
            st.metric("Equipos Óptimos", len(machine_group["machines"]))

        with c3:
            st.metric("Equipos en Peligro", 0)

        with c4:
            st.markdown("Conectividad")
            self._render_line_connectivity(machine_group_name)

        st.table(self._get_line_machines_rows(machine_group_name))

    def _render_content(self) -> None:
        import time
        last_start = time.time()
        # we'll use a placeholder hack to allow streamlit to catch up interactions from within a loop
        self._render_equipments_lines()
        for machines_group in self.app_state.project_model.machines_groups_table:
            self._render_line_detailed_section(machines_group)

        with st.container():
            text_area_hack = st.empty()
            while True:
                log.info(len(st.session_state))
                if time.time() - last_start > st.secrets['main_dashboard_refresh_interval']:
                    logging.info(f"Rerun ro refresh main dashboard...")
                    logging.info(f"Downloading new data from persistence after refresh interval exceeded...")
                    self.app_state.start_background_download()
                    while self.app_state.background_download_active():
                        with text_area_hack:
                            st.write("")
                        text_area_hack.empty()
                        time.sleep(0.1)
                    st.experimental_rerun()

                time.sleep(0.1)
                with text_area_hack:
                    st.write("")
                text_area_hack.empty()

    def _render_submenu(self) -> None:
        pass

    def _build_content_state(self) -> Dict:
        pass

    def _build_submenu_state(self) -> Dict:
        pass

    def get_associated_profile(self) -> AppProfile:
        return AppProfile.RESUMEN

    def get_display_name(cls) -> str:
        return "Panel General"
