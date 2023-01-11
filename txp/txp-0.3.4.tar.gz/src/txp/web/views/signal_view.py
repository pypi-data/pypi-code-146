"""
This module provides a SignalView component for the app.
"""
import datetime
import streamlit as st
import txp.common.utils.firestore_utils
from txp.common.utils import plotter_utils
from txp.devices.drivers.mock.mock_driver import MockDriver, get_signals_per_dimension
import AppProfile
import MainView
from txp.common.edge import EdgeDescriptor
from txp.cloud import cloud_utils
from typing import Dict
import logging
from txp.common.config import settings
import matplotlib.pyplot as plt
from google.cloud import bigquery
import numpy as np
import cv2
import pytz

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class SignalView(MainView):
    """A Signal view that helps to test and see tasks data"""

    def __init__(self):

        self.fft_table = ".telemetrydataset01.fft"
        self.samples_table = ".telemetrydataset01.samples"
        super(SignalView, self).__init__(
            component_key="signal_view"
        )

    def get_associated_profile(self) -> AppProfile:
        return AppProfile.ANALYTICS

    @classmethod
    def get_display_name(cls) -> str:
        return 'Ver señales'

    def _build_submenu_state(self) -> Dict:
        # Hardcoded state for demonstration
        return {
            "edge_logical_id": None
        }

    def _build_content_state(self) -> Dict:
        return {}

    def _render_submenu(self) -> None:
        with st.form("date_form"):
            date = st.date_input("Pick a date", datetime.datetime.now(pytz.timezone("America/Mexico_City")))
            submitted_date = st.form_submit_button("refresh")

        if submitted_date:
            date += datetime.timedelta(days=1)
            date_time = datetime.datetime(date.year, date.month, date.day, tzinfo=pytz.timezone("America/Mexico_City"))
            self.pull_project_data(date_time, self.app_state.authentication_info.role_service_account_credentials)
            if "project_model" in st.session_state and st.session_state.project_model:
                st.session_state.project_model["query_data"] = {}
                st.session_state.project_model["selected_date"] = date_time

        if "project_model" in st.session_state and st.session_state.project_model:
            with st.form("task_form"):

                selected_date = st.session_state.project_model["selected_date"]
                selected_date -= datetime.timedelta(days=1)

                task_list = []
                for i, t in enumerate(st.session_state["project_model"]["job"]["tasks"]):
                    start = datetime.datetime.strptime(t["parameters"]["start_date"], '%Y-%m-%d')
                    end = datetime.datetime.strptime(t["parameters"]["end_date"], '%Y-%m-%d')
                    start = datetime.datetime(start.year, start.month, start.day,
                                              tzinfo=pytz.timezone("America/Mexico_City"))
                    end = datetime.datetime(end.year, end.month, end.day, tzinfo=pytz.timezone("America/Mexico_City"))
                    if start <= selected_date <= end:
                        task_list.append(f'{i}, from {t["parameters"]["start_date"]} to {t["parameters"]["end_date"]}')

                task = st.selectbox("Tasks", task_list)
                submitted_tasks = st.form_submit_button("refresh")
            if submitted_tasks:
                st.session_state.project_model["query_data"] = {}
                st.session_state.project_model["query_data"]["task"] = int(task.split(",")[0])

            with st.form("motor_form"):
                machine_list = []
                if "task" in st.session_state.project_model["query_data"]:
                    task = st.session_state.project_model["query_data"]["task"]
                    machine_list = [machine for machine in
                                    st.session_state["project_model"]["job"]["tasks"][task]["machines"]]
                machine = st.selectbox(
                    "Machine",
                    machine_list
                )
                submitted_machines = st.form_submit_button("refresh")
            if submitted_machines:
                st.session_state.project_model["query_data"].pop("edge", None)
                st.session_state.project_model["query_data"]["machine"] = machine

            with st.form("edge_form"):
                edge_list = []
                if "machine" in st.session_state.project_model["query_data"]:
                    machine_id = st.session_state.project_model["query_data"]["machine"]
                    machine_doc_ref = None
                    for machine in st.session_state.project_model['machines']:
                        if machine['machine_id'] == machine_id:
                            machine_doc_ref = machine
                            break

                    edge_list = list(map(
                        lambda edge_doc_ref: edge_doc_ref.get().get("logical_id"),
                        machine_doc_ref["associated_with_edges"]
                    ))
                edge = st.selectbox(
                    "edge",
                    edge_list
                )
                submitted_edges = st.form_submit_button("query")
            if submitted_edges:
                st.session_state.project_model["query_data"]["edge"] = edge

            with st.form("ok_label_form"):
                ok_label_set = False
                if "signal" in st.session_state.project_model:
                    element = st.session_state.project_model["signal"]
                    if element["label"] == "OK":
                        ok_label_set = True
                ok_label = st.checkbox("OK", ok_label_set)
                submitted = st.form_submit_button("Set label")
            if submitted:
                if "signal" in st.session_state.project_model:
                    label = "BAD"
                    if ok_label:
                        label = "OK"
                    credentials = self.app_state.authentication_info.role_service_account_credentials
                    project_id = credentials.project_id
                    client = bigquery.Client(credentials=credentials, project=project_id)
                    cloud_utils.set_label_for_signal(label, element, project_id + self.samples_table, client)

            if "edge" in st.session_state.project_model["query_data"]:
                self._submenu_state['edge_logical_id'] = st.session_state.project_model["query_data"]["edge"]
            else:
                self._submenu_state['edge_logical_id'] = None

    def _render_content(self) -> None:
        if "project_model" in st.session_state and st.session_state.project_model:
            st.markdown(f"#### {st.session_state.project_model['machines_groups'][0]['name']}")
            st.markdown("##### Última configuración")
            self._render_configuration()

            # Render BigQuery Form
            st.markdown("--------")
            st.markdown("#### Visualizar gráficas")

            with st.form("bigquery_form"):
                perceptions = []
                for edge in st.session_state.project_model["edges"]:
                    if edge["logical_id"] == self._submenu_state['edge_logical_id']:
                        perceptions = edge["is_of_kind_ref"].get().get("perceptions").keys()
                        break
                perception_name = st.selectbox(
                    "Tipo de percepción",
                    perceptions
                )

                logaritmic_scale = st.checkbox("Escala Logarítmica")
                number = st.number_input('X ticks, scala', min_value=-1)  # -1 means no scale given

                submitted = st.form_submit_button("Mostrar Grafica")
            project_id = self.app_state.authentication_info.role_service_account_credentials.project_id
            if submitted:
                self.plot_signals(
                    self._submenu_state['edge_logical_id'],
                    perception_name,
                    project_id + self.fft_table,
                    project_id + self.samples_table,
                    logaritmic_scale,
                    None if number == -1 else number
                )

    # =====================Helper Functions==================================
    def get_edge_descriptors(self):
        return [EdgeDescriptor(edge["logical_id"], edge["device_kind"],
                               edge["is_of_kind_ref"].get().get("type"),
                               edge["is_of_kind_ref"].get().get("parameters"),
                               edge["is_of_kind_ref"].get().get("perceptions"))
                for edge in st.session_state.project_model["edges"]]

    def pull_project_data(self, selected_date, service_account_role_credentials):
        db = txp.common.utils.firestore_utils.get_authenticated_client(
            self.app_state.authentication_info.role_service_account_credentials
        )

        st.session_state.project_model = txp.common.utils.firestore_utils.pull_project_data_by_date(
            db, selected_date
        )

        db.close()

    def _render_machine(self, machine: Dict):
        st.write(f"**Machine:** {machine['machine_id']}")
        st.write(f"**Manufacturer:** {machine['manufacturer']}")
        st.write(f"**Model:** {machine['model']}")
        with st.expander(f"Edges:"):
            for edge_ref in machine['associated_with_edges']:
                edge_snapshot = edge_ref.get()
                st.write(f'{edge_snapshot.get("logical_id")}')

    def _render_configuration(self):
        configuration = st.session_state.project_model['last_configuration']
        st.markdown(f"**Válida desde**: {configuration.get('since')}")

    def plot_all_fft(self, fft_bigquery_per_dimension, edge, perception_name, semilogy=False, x_scale=None):
        if edge.device_kind == MockDriver.device_name():
            signals_per_dimension = get_signals_per_dimension(edge)
            for i, signal in enumerate(signals_per_dimension):
                plotter_signal = plotter_utils.FFTPlotter(signal.signal_amplitude_axis, None, signal.sampling_frequency)
                fig = plotter_signal.plot(f"Expected signal, dimension {i}", semilogy, x_scale)
                st.pyplot(fig=fig)

        for i, dimension in enumerate(fft_bigquery_per_dimension):
            sampling_frequency = edge.perceptions[perception_name]["sampling_frequency"]
            plotter_bigquery = plotter_utils.FFTPlotter(None, dimension, sampling_frequency)
            fig = plotter_bigquery.plot(
                f"From cloud data fft. Edge: {edge.logical_id}, Perception: {perception_name}, Dimension {i}",
                semilogy, x_scale)
            st.pyplot(fig=fig)

    def plot_all_time(self, data_bigquery_per_dimension, edge, perception_name, semilogy=False):
        for i, dimension in enumerate(data_bigquery_per_dimension):
            fig = plt.figure(figsize=(23, 10))
            if semilogy:
                plt.semilogy(dimension)
            else:
                plt.plot(dimension, marker=".", markersize=50)
            fig.suptitle(
                f"From cloud data signal. Edge: {edge.logical_id}, Perception: {perception_name}, Dimension {i}",
                fontsize=20)
            st.pyplot(fig=fig)

    def plot_image(self, image_from_bigquery, edge, perception_name):
        image = [int(x) for x in image_from_bigquery[0]]
        image = np.frombuffer(bytes(image), dtype=np.uint8)
        image = cv2.imdecode(image, flags=1)
        fig = plt.figure(figsize=(23, 10))
        plt.imshow(image[:, :, ::-1])
        fig.suptitle(f"From cloud data image. Edge: {edge.logical_id}, Perception: {perception_name}",
                     fontsize=20)
        st.pyplot(fig=fig)
        pass

    def plot_signals(self, edge_logical_id, perception_name, table_fft, table_samples, semilogy=False, x_scale=None):
        edge = None
        for e in self.get_edge_descriptors():
            if e.logical_id == edge_logical_id:
                edge = e
                break
        client = bigquery.Client(
            credentials=self.app_state.authentication_info.role_service_account_credentials,
            project=self.app_state.authentication_info.role_service_account_credentials.project_id
        )
        if edge is not None:
            end_date = st.session_state.project_model["selected_date"]
            start_date = end_date
            start_date -= datetime.timedelta(days=1)
            if edge.perceptions[perception_name]["mode"] == "IMAGE":
                element = cloud_utils.get_signal_from_bigquery(perception_name, edge_logical_id, start_date, end_date,
                                                               table_samples, client)
                st.session_state.project_model["signal"] = element
                self.plot_image(element["data"], edge, perception_name)

            elif edge.perceptions[perception_name]["mode"] == "FFT":
                fft_element = cloud_utils.get_fft_from_bigquery(perception_name, edge_logical_id, start_date, end_date,
                                                                table_fft, table_samples, client)
                st.session_state.project_model["signal"] = fft_element
                self.plot_all_fft(fft_element["fft"], edge, perception_name, semilogy, x_scale)
            else:
                element = cloud_utils.get_signal_from_bigquery(perception_name, edge_logical_id, start_date, end_date,
                                                               table_samples, client)
                st.session_state.project_model["signal"] = element
                self.plot_all_time(element["data"], edge, perception_name, semilogy)
        else:
            raise Exception(f"edge_logical_id: {edge_logical_id} not found at configuration")
