"""
This module implements the Telemetry Health view for the application.

NOTE: This is just a dummy implementation of a MainView in order to shown the
mechanism provided by the `core_components` package.
"""
import txp.common.utils.firestore_utils
from txp.web.core_components.app_profiles import AppProfile
from txp.web.core_components.main_view import MainView
import logging
from typing import Dict
import streamlit as st
import pandas as pd
from txp.web.core_components.app_component import Card

# TODO: This might be a problem. The logging configuration is being taken from `txp` package
from txp.common.config import settings

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class TelemetryHealthView(MainView):
    """The Telemetry Health View"""

    def __init__(self):
        super(TelemetryHealthView, self).__init__(component_key="telemetry_health_view")
        self.data = None
        self.edges = None
        self.current_machine = None
        self.current_machines_groups = None
        self.default_edge_state = "Disconnected"
        self.formatted_asset_name = None

    def get_associated_profile(self) -> AppProfile:
        return AppProfile.RESUMEN

    def implements_submenu(self) -> bool:
        return True

    @classmethod
    def get_display_name(cls) -> str:
        return "Salud de Telemetría"

    def get_data(self):
        if self.data is None:
            db = txp.common.utils.firestore_utils.get_authenticated_client(
                self.app_state.authentication_info.role_service_account_credentials
            )

            data = txp.common.utils.firestore_utils.pull_recent_project_data(db, self._tenant_id)
            self.data = self._formatted_data(data)
            machines = list(self.data["machines"].keys())
            machines_groups = list(self.data["machines_groups"].keys())
            self.current_machines_groups = machines_groups[0]
            self.current_machine = machines[0]
            self.formatted_asset_name = self.formatting_readable_strings(self.current_machine)
            self.edges = self._edges_status_mapping(self.data["machines"][self.current_machine])
            db.close()

    def _build_submenu_state(self) -> Dict:
        pass

    def _build_content_state(self) -> Dict:
        pass

    def _update_machine(self):
        machine = st.session_state[f"{self.__class__.__name__}_machine_selectbox"]
        self.current_machine = machine
        self.edges = self._edges_status_mapping(self.data["machines"][machine])
        self.formatted_asset_name = self.formatting_readable_strings(self.current_machine)

    def _update_machines_groups(self):
        machines_groups = st.session_state[
            f"{self.__class__.__name__}_machine_groups_selectbox"
        ]
        self.current_machines_groups = machines_groups

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

    def _render_submenu(self):
        self.get_data()
        activos = list(self.data["machines"].keys())
        st.selectbox(
            label="Selecciona un activo",
            options=activos,
            key=f"{self.__class__.__name__}_machine_selectbox",
            on_change=self._update_machine,
            index=0
        )
        st.markdown("-------")
        st.markdown("**<p align='center'>Estado general</p>**", unsafe_allow_html=True)
        st.markdown(f"⚙️ **Dispositivos configurados:** {len(self.edges.Dispositivo)}")
        st.markdown(
            f"✅ **Dispositivos conectados:** {len(self.edges.loc[(self.edges['Actividad'] == 'Conectado')])+len(self.edges.loc[(self.edges['Actividad'] == 'Recolectando datos')])}"
        )
        st.markdown(
            f"📥 **Dispositivos recolectando datos:** {len(self.edges.loc[(self.edges['Actividad'] == 'Recolectando datos')])}"
        )

    def _edges_status_mapping(self, current_machine):
        """
        Given the current machine, returns a DataFrame with the edges state and gateway-id
        """
        edges = []
        edges_state = []
        gateways = []

        for e in current_machine["associated_with_edges"]:
            edge_name = e.get().to_dict().get("logical_id")
            edge_state = e.get().to_dict().get("state")
            edge_type = e.get().to_dict().get("device_type")
            if edge_type == 'ACTUATOR_DEVICE':
                pass
            else:
                if edge_state is not None:
                    driver_status = edge_state.get("driver_state")
                    edges.append(edge_name)
                    edges_state.append(self._edge_states_sp[driver_status])
                else:
                    edges.append(edge_name)
                    edges_state.append(self._edge_states_sp[self.default_edge_state])
        for g in self.data["gateways"]:
            gateway = self.data["gateways"][g]
            machines_in_gateway = gateway.get("machines")
            for machine in machines_in_gateway:
                machine_in_gateway_name = machine.get().to_dict().get("machine_id")
                if machine_in_gateway_name == current_machine.get("machine_id"):
                    gateway_name = gateway.get("gateway_id")
                    for i in range(len(edges)):
                        operation = "" + gateway_name
                        gateways.append(operation)

        if not edges_state:
            for i in range(len(edges)):
                edges_state.append(self._edge_states_sp[self.default_edge_state])
            df = pd.DataFrame(
                list(zip(edges, edges_state, gateways)),
                columns=[
                    "Dispositivo",
                    "Actividad",
                    "Conectado al gateway",
                ],
            )
            return df
        else:
            df = pd.DataFrame(
                list(zip(edges, edges_state, gateways)),
                columns=[
                    "Dispositivo",
                    "Actividad",
                    "Conectado al gateway",
                ],
            )
            return df

    def _render_content(self):
        # helper functions
        self.get_data()
        st.header("Salud de Telemetría")
        st.subheader("Resumen")
        machine = self.current_machine
        machines_groups = self.current_machines_groups

        device_state = Card(
            card_row=1,
            card_column_start=1,
            card_column_end=1,
            card_subheader="Estado de los dispositivos",
            content=self.edges.to_dict("list"),
            labels=[
                    "Dispositivo",
                    "Actividad",
                    "Conectado al gateway",
            ],
            vertical_style=False,
        )
        metadata_of_asset = Card(
            card_row=1,
            card_column_start=2,
            card_column_end=2,
            card_subheader=f"{self.formatted_asset_name}",
            content=
            f"**Grupo de activos**: {self.data['machines_groups'][machines_groups]['name']}  \n"
            f"**Manufactura**: {self.data['machines'][machine]['manufacturer']}  \n"
            f"**Modelo**: {self.data['machines'][machine]['model']}  \n",
        )
        self.render_card([metadata_of_asset, device_state])
