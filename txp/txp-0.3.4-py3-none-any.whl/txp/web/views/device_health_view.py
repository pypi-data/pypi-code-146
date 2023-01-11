import txp.common.utils.firestore_utils
from txp.web.core_components.main_view import MainView
from txp.web.core_components.app_profiles import AppProfile
from txp.web.core_components.app_component import Card
import txp.common.utils.iot_core_utils as iot_controller
from txp.common.utils.firestore_utils import pull_current_configuration_from_firestore
import logging
from typing import Dict
import streamlit as st
import datetime
import pytz
import pandas as pd

from txp.common.config import settings

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class DeviceHealthView(MainView):
    """The Device Health View"""

    def __init__(self):
        super(DeviceHealthView, self).__init__(component_key="device_health_view")
        self.gateways_data = None
        self.edges_data = None
        self.config: None
        self.machine_per_edges = None
        self.jobs_data = None
        self.gateway_to_render = None
        self.current_edges = None
        self._data_built = False

    def implements_submenu(self) -> bool:
        return True

    def get_associated_profile(self) -> AppProfile:
        return AppProfile.RESUMEN

    @classmethod
    def get_display_name(cls) -> str:
        return "Salud de Dispositivo"

    def _build_submenu_state(self) -> Dict:
        # Hardcoded state for demonstration
        pass

    def _build_content_state(self) -> Dict:
        pass

    def _update_edges(self):
        selected_edges = st.session_state[f"{self.__class__.__name__}_edge_multibox"]
        self.current_edges = selected_edges

    def _update_gateway(self):
        gateway = st.session_state[f"{self.__class__.__name__}_gateway_selectbox"]
        self.gateway_to_render = gateway
        self.current_edges = [
            edge["logical_id"] for edge in self.mapping_edges_that_send_data_to_gateway()
        ]

    def mapping_edges_that_send_data_to_gateway(self):
        current_edges = []
        for machine in self.gateways_data[self.gateway_to_render]["machines_ids"]:
            data = self.app_state.project_model.machines_table[machine].reprJSON()
            for edge in data['edges_ids']:
                edge_dict = self.app_state.project_model.edges_table[edge].reprJSON()
                if edge_dict not in current_edges:
                    current_edges.append(edge_dict)
        return current_edges

    def build_state(self):
        if not self._data_built:
            db = txp.common.utils.firestore_utils.get_authenticated_client(
                self.app_state.authentication_info.role_service_account_credentials
            )
            self.config = pull_current_configuration_from_firestore(db, self._tenant_id).to_dict()
            db.close()

            self.gateways_data = {
                key: self.app_state.project_model.gateways_table[key].reprJSON() for key in self.app_state.project_model.gateways_table.keys()
            }

            self.edges_data = {key: self.app_state.project_model.edges_table[key].reprJSON() for key in self.app_state.project_model.edges_table.keys()}

            self.jobs_data = {
                key: self.app_state.project_model.jobs_table_by_gateway[key].reprJSON()
                for key in self.app_state.project_model.gateways_table.keys()
            }

            self.machine_per_edges = self.get_machine_to_edge()

            self.gateway_to_render = next(iter(self.gateways_data))

            self.current_edges = [
                 edge["logical_id"] for edge in self.mapping_edges_that_send_data_to_gateway()
            ]

            self.iot = iot_controller.get_authenticate_client(
                 self.app_state.authentication_info.role_service_account_credentials
            )

            self.device_state = {key: iot_controller.get_device_state(
                 self.iot, self.gateways_data[key]['project_id'],
                 self.gateways_data[key]['cloud_region'],
                 self.gateways_data[key]['registry_id'],
                 self.gateways_data[key]['gateway_id']) for key in self.app_state.project_model.gateways_table.keys()}

            self._data_built = True

    def change_utc_timezone(self, timestamp):
        utc = pytz.timezone('UTC')
        timezone = pytz.timezone("America/Mexico_City")
        date_time = pd.to_datetime(timestamp)
        localized_timestamp = utc.localize(date_time)
        new_timezone = localized_timestamp.astimezone(timezone)
        strtime = new_timezone.strftime("%m/%d/%Y, %H:%M:%S")
        return strtime

    def _render_submenu(self) -> None:

        st.selectbox(
            label="Gateways de este proyecto",
            options=self.gateways_data.keys(),
            key=f"{self.__class__.__name__}_gateway_selectbox",
            on_change=self._update_gateway,
        )

        label = f"Dispositivos vinculados a {self.gateway_to_render}"

        edges = [
            edge["logical_id"] for edge in self.mapping_edges_that_send_data_to_gateway()
        ]

        st.multiselect(
            label,
            options=edges,
            key=f"{self.__class__.__name__}_edge_multibox",
            on_change=self._update_edges,
            default=self.current_edges,
        )
        st.markdown("* * *")
        st.markdown("**<p align='center'>Estado general</p>**", unsafe_allow_html=True)

        tasks = self.jobs_data[self.gateway_to_render]["tasks"]
        st.write(f"📥 Paquetes recibidos: **50**")
        st.write(f"🕚 Paquetes en cola: **10**")

        st.write(f"🔗 Total de dispositivos vinculados: **{len(self.current_edges)}**")

        st.write(
            f"📡 Total de activos monitoreados: **{len(self.gateways_data[self.gateway_to_render]['machines_ids'])}**"
        )

    def last_gateway_task(self):
        tz = pytz.timezone("America/Mexico_City")
        tasks = self.jobs_data[self.gateway_to_render]["tasks"]
        task_info = {}
        for i, task in enumerate(tasks):
            start_date = datetime.datetime.strptime(
                    task["parameters"]["start_date"], "%Y-%m-%d"
                ).date()
            start_time= datetime.datetime.strptime(
                    task["parameters"]["start_time"], "%H:%M"
                ).time()
            end_date = datetime.datetime.strptime(
                task["parameters"]["end_date"], "%Y-%m-%d"
            ).date()
            end_time = datetime.datetime.strptime(
                task["parameters"]["end_time"], "%H:%M"
            ).time()
            full_start_datetime = tz.localize(datetime.datetime.combine(start_date,start_time))
            full_end_datetime = tz.localize(datetime.datetime.combine(end_date, end_time))
            task_info['start_datetime'] = full_start_datetime.strftime("%Y-%m-%d %H:%M:%S")
            task_info['end_datetime'] = full_end_datetime.strftime("%Y-%m-%d %H:%M:%S")
            task_info['observation_time'] = task['parameters']['sampling_window'].observation_time
            task_info['sampling_time'] = task['parameters']['sampling_window'].sampling_time
            task_info['machines'] = task['machines']
        return task_info

    def get_last_actualization_gateway(self):
        conected_edges = []
        for edge,state in self.app_state.project_model.edges_states_table.items():
            if edge in self.current_edges:
                if not state is None:
                    conected_edges.append(state)

        if any(d["driver_state"] == "Disconnected" for d in conected_edges):
            st.warning("Estado: se registraron dispositivos desconectados")
        # TODO computing the Gateway State should be a logic on its own, and should consider all edge cases
        # elif any("state" not in d and not d.get('type', None) =='ACTUATOR_DEVICE' for d in conected_edges):
        #     st.warning("Estado: se registraron dispositivos sin información de estado")
        else:
            st.success("Estado: CONECTADO")

        cards=[]
        if self.device_state[self.gateway_to_render]:
            heartbeat = self.change_utc_timezone(self.device_state[self.gateway_to_render].heartbeat)
            last_state_time = self.change_utc_timezone(self.device_state[self.gateway_to_render].last_state_time)
            last_config_ack = self.change_utc_timezone(self.device_state[self.gateway_to_render].last_config_ack)
            last_error_time = self.change_utc_timezone(self.device_state[self.gateway_to_render].last_error_time)


            last_actualization_card = Card(
                card_row=1,
                card_column_start=1,
                card_column_end=3,
                card_subheader="Última actividad",
                content={"Señal de monitoreo": [heartbeat],
                         "Último estado del gateway": [last_state_time],
                         "Envío de configuración": [last_config_ack],
                         "Versión de la configuración": [self.config["configuration_id"]],
                         "Último error recibido": [last_error_time],
                         "Mensaje de error": [self.device_state[self.gateway_to_render].last_error_msg],
                         },
                labels=[
                    "Señal de monitoreo",
                    "Último estado del gateway",
                    "Envío de configuración",
                    "Versión de la configuración",
                    "Último error recibido",
                    "Mensaje de error",
                ],
                vertical_style=True,
            )
            cards.append(last_actualization_card)
        else:
            st.info('Este dispositivo no está conectado a IoT')

        last_task_info = self.last_gateway_task()

        tasks_of_gateway_card = Card(
                card_row=2,
                card_column_start=1,
                card_column_end=3,
                card_subheader="Configuración de la última tarea",
                content=last_task_info,
                labels=[
                    "Fecha de inicio",
                    "Fecha de finalización",
                    "Tiempo de observación",
                    "Tiempo de muestreo",
                    "Máquinas"
                ],
                vertical_style=False,
        )
        cards.append(tasks_of_gateway_card)

        self.render_card(
            cards
        )

        st.text("\n")
        return None

    def get_machine_to_edge(self):
        machines_with_edges = {
            machine: self.app_state.project_model.machines_table[machine].edges_ids
            for machine in self.app_state.project_model.machines_table.keys()
        }
        edges_and_monitored_machines = {}
        for motor, edges in machines_with_edges.items():
            for edge in edges:
                edges_and_monitored_machines.setdefault(edge, []).append(motor)

        return edges_and_monitored_machines


    def get_last_actualization_edge(self, edge):
        st.markdown(f'### **Dispositivo**: {edge["logical_id"]}.')
        with st.expander("Estado", expanded=True):
            state_dict = self.app_state.project_model.edges_states_table[edge['logical_id']]
            if state_dict:
                if "driver_state" in state_dict:
                    if state_dict["driver_state"] == "Connected":
                        st.success("DriverState.CONECTADO")
                        st.caption(f'Desde: {state_dict["since_datetime"]}')
                    elif state_dict["driver_state"] == "Sampling":
                        st.success("DriverState.RECOLECTANDO DATOS")
                        st.caption(f'Desde: {state_dict["since_datetime"]}')
                    elif edge.get('type', 'ACTUATOR_DEVICE'):
                        st.success("DriverState.CONECTADO")
                    else:
                        st.warning("Sin información del estado")
            else:
                st.error("DriverState.DESCONECTADO")
            st.write(f'**Tipo de dispositivo**: {edge["device_kind"]}')
            st.write(
                f'**Última recepción de evento de telemetría**: {self.config["since"]}'
            )
            st.write(f"**Magnitudes de percepción:**")
            for perception in edge["perceptions"]:
                st.write(f"{perception}")

            monitored_machines = []
            for m in self.gateways_data[self.gateway_to_render]["machines_ids"]:
                monitored_machines.append(m)

            for machine in monitored_machines:
                if machine in self.machine_per_edges[edge["logical_id"]]:
                    id = f"**Activo**: {machine}"
                    if self.app_state.project_model.machines_table[machine].model != 'No Aplica':
                        st.caption(
                            f"{id}, modelo {self.app_state.project_model.machines_table[machine].model}"
                        )
                    else:
                        st.caption(
                            f"{id}"
                        )

    def _render_content(self) -> None:

        self.build_state()

        st.header("Salud de los Dispositivos")

        st.markdown(f"#### **Gateway**: {self.gateway_to_render}.")

        self.get_last_actualization_gateway()
        st.markdown("* * *")

        for edge in self.current_edges:
            self.get_last_actualization_edge(self.edges_data[edge])
