"""
This module implements an Integrated Analytics View for the application.

NOTE: This is just a dummy implementation of a MainView in order to shown the
mechanism provided by the `core_components` package.
"""

import pytz
import txp.common.utils.bigquery_utils
from txp.common.utils.authentication_utils import AuthenticationInfo
from txp.web.core_components.app_profiles import AppProfile
from txp.web.core_components.main_view import MainView
from typing import Dict
import streamlit as st
from txp.web.core_components.annotation_widget import AnnotationWidget
from txp.common.ml.tasks import AssetTask
import json
from txp.common.config import settings
from pylab import *
import txp.web.views.analytics.computer_vision_analytics as computer_vision_utils
import txp.web.views.analytics.vibration_analytics as vibration_utils
import txp.web.views.analytics.complex_analytics as complex_utils
import txp.web.views.analytics.temperature_analytics_view as temperature_utils
import plotly.graph_objects as go
from dataclasses import dataclass, field
from google.cloud.bigquery import Client
import pandas as pd

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

_MAX_IMAGES_ALLOWED_RANGE = 3600
_IMAGES_RANGE_TIME_EXCEEDED = False


@dataclass
class DataRequest:
    """
    DataRequest manages the different data requests needed for render content in this view.
    Args:
         range_time: date, start and end time for data request
         edge_kind(str): edge kind from selected edge for data request
         tz: timezone
         bigquery_dataset(str): bigquery dataset name
         tenant_id(str): tenant id name
         edge(str): edge name for data request
         perception(str): perception name for data request
         bqclient: bigquery client for performing queries
         order_key(str): order key used in bigquery.get_all_records_within_interval() method


    """

    range_time: Dict[str, datetime.datetime] = field(default_factory=dict)
    edge_kind: str = None
    tz = pytz.timezone("America/Mexico_City")
    bigquery_dataset: str = None
    tenant_id: str = None
    edge: str = None
    perception: str = None
    bqclient: Client = None
    order_key: str = "observation_timestamp"

    def _get_full_start_date(self):
        """
        returns the full start date localized
        """
        full_start_date = self.tz.localize(
            datetime.datetime.combine(self.range_time["date"], self.range_time["start"])
        )
        return full_start_date.astimezone(pytz.utc)

    def _get_full_end_date(self):
        """
        returns the full end date localized
        """
        full_end_date = self.tz.localize(
            datetime.datetime.combine(self.range_time["date"], self.range_time["end"])
        )
        return full_end_date.astimezone(pytz.utc)

    def get_data_from_table_in_dataset(self, table, user_role: AuthenticationInfo.UserRole):
        """
        returns the data from a table if data, else return None
        """
        full_start_date = self._get_full_start_date()
        full_end_date = self._get_full_end_date()
        global _IMAGES_RANGE_TIME_EXCEEDED
        # Don't allow Client users to download pictures from 1 hour or more.
        if (
            user_role != AuthenticationInfo.UserRole.Admin
            and (full_end_date - full_start_date).total_seconds() > _MAX_IMAGES_ALLOWED_RANGE
            and self.perception in { 'Image', 'ThermalImage' }
        ):
            log.info("Client user trying to get Images over an hour")
            _IMAGES_RANGE_TIME_EXCEEDED = True
            return None
        elif self.perception in { 'Image', 'ThermalImage' }:
            _IMAGES_RANGE_TIME_EXCEEDED = False

        signals_from_interval = self._get_data_from_table_in_dataset(table)
        if not signals_from_interval or len(signals_from_interval) == 0:
            logging.info(f"No hay data disponible")
            return None
        else:
            return signals_from_interval

    def _get_data_from_table_in_dataset(self, table):
        """
        returns the data in a table from a bigquery dataset.
        Args:
            table(str): bigquery table name.
        """
        full_start_date = self._get_full_start_date()
        full_end_date = self._get_full_end_date()
        return txp.common.utils.bigquery_utils.get_all_signals_within_interval(
            tenant_id=self.tenant_id,
            table_name=f"{self.bigquery_dataset}.{table}",
            edge_logical_id=self.edge,
            perception_name=self.perception,
            start_datetime=full_start_date,
            end_datetime=full_end_date,
            client=self.bqclient,
        )

    def _get_data_from_table_in_dataset_ordered_by_value(
            self, table
    ):
        """
        returns the data in a table from a bigquery dataset ordered by the key included as self.order_by.
        Args:
            table(str): bigquery table name.
        """
        full_start_date = self._get_full_start_date()
        full_end_date = self._get_full_end_date()

        df = txp.common.utils.bigquery_utils.get_all_records_within_interval(
            tenant_id=self.tenant_id,
            table_name=f"{self.bigquery_dataset}.{table}",
            edge_logical_id=self.edge,
            perception_name=self.perception,
            start_datetime=full_start_date,
            end_datetime=full_end_date,
            order_key=self.order_key,
            client=self.bqclient,
        )
        if df.empty:
            return None
        else:
            return df


@dataclass
class VibrationDataCharts:
    fft_chart: go.Figure = None
    fft_metrics_df: pd.DataFrame = None
    psd_chart: go.Figure = None
    psd_metrics_df: pd.DataFrame = None


@dataclass
class ImagesDataCharts:
    normal_imgs_chat: go.Figure = None
    thermographic_imgs_datacharts: go.Figure = None
    chart_length_exceeded: bool = False


@dataclass
class TemperatureDataCharts:
    temp_chart: go.Figure = None


class AnalyticsView(MainView):
    """The Analytics View"""

    def __init__(self):
        super(AnalyticsView, self).__init__(component_key="analytics_view")
        self.widget = None
        self.current_machine = None
        self.current_machines_groups = None
        self.data = None
        self.data_request: DataRequest
        self.edges = None
        self.edge = None
        self.current_readable_names_map = None
        self.formatted_asset_name = None
        self.edge_kind = None
        self.current_perception = None
        self.sheet = None
        # attributes related to images
        self.data_format = None
        self._animation_data_format = "Animación"
        self._images_data_format = "Imágenes"
        self._timages_data_format = "Imágenes termográficas"
        self._thermographic_perception = "ThermalImage"
        self.normal_data = None
        self.thermographic_data = None
        self._image_perception = "Image"
        self._images_kind = {"ArmRobot"}
        # attributes related to vibration
        self.edges_data = None
        self.vibrational_perceptions = None
        self.vibration_data = None
        self.fft_metrics_df = None
        self.psd_metrics_df = None
        self._vibrational_kind = {"Icomox", "Mock"}
        # attribuets related to complex and temperature
        self._complex_kind = {"ThermoArm"}
        self._temperature_kind = {"Generic"}
        self._temperature_perception = "Temperature"
        self.temperature_data = None
        # attribuets related to temperature
        self.last_temperatures_values = None
        self._per_time_sheet = "Registro por tiempo"
        self._per_last_signals = "Últimos registros"
        self._per_condition = "Registro por condición"

        # The control attributes defined below helps in performance because allows to
        #   know when is necessary to repaint something.
        self._redraw_required: bool = False
        self._vibration_charts: VibrationDataCharts = VibrationDataCharts()
        self._images_charts: ImagesDataCharts = ImagesDataCharts()
        self._temperature_charts: TemperatureDataCharts = TemperatureDataCharts()

    def get_associated_profile(self) -> AppProfile:
        return AppProfile.ANALYTICS

    def implements_submenu(self) -> bool:
        return True

    @classmethod
    def get_display_name(cls) -> str:
        return "Análisis de Datos"

    def _build_submenu_state(self) -> Dict:
        pass

    def _build_content_state(self) -> Dict:
        pass

    def get_kind_from_edge(self):
        kind = self.data["edges"][self.edge]["device_kind"]
        return kind

    def formatted_data(self, data):
        """
        takes the project data and returns a formatted Dict.
        """
        machines = {d.machine_id: d.reprJSON() for d in data.machines_table.values()}
        gateways = {d.gateway_id: d.reprJSON() for d in data.gateways_table.values()}
        edges = {d.logical_id: d.reprJSON() for d in data.edges_table.values()}
        machines_groups = {d["name"]: d for d in data.machines_groups_table.values()}
        f_data = {
            "machines_groups": machines_groups,
            "machines": machines,
            "gateways": gateways,
            "edges": edges,
        }
        return f_data

    def names_human_readable(self):
        """
        filters the human readable map with the current machines edges
        """
        readable_names_map = {}
        readable_names_map_list = json.loads(st.secrets["edges_names"])
        for k, v in readable_names_map_list.items():
            if k in self.edges:
                readable_names_map.update({k: v})
        return readable_names_map

    def get_data(self):
        if self.data is None:
            self.data = self.formatted_data(self.app_state.project_model)
            machines = list(self.data["machines"].keys())
            machines_groups = list(self.data["machines_groups"].keys())
            self.current_machines_groups = machines_groups[0]
            self.current_machine = machines[0]
            self.edges = self.get_edges_from_asset(
                self.data["machines"][self.current_machine]
            )
            self.current_readable_names_map = self.names_human_readable()
            if not self.edges:
                self.edge = None
            else:
                self.edge = self.edges[0]
                self.edge_kind = self.get_kind_from_edge()
            self.sheet = self._per_time_sheet
            self.bqclient = txp.common.utils.bigquery_utils.get_authenticated_client(
                self.app_state.authentication_info.role_service_account_credentials
            )
            self.edges_data = {
                machine.machine_id: vibration_utils.mapping_data_from_data_parent(
                    self.app_state.project_model.edges_table.values()
                )
                for machine in self.app_state.project_model.machines_table.values()
            }

            self.data_request = DataRequest()

            if self.edge_kind in self._vibrational_kind:
                self.vibrational_analysis_assets = (
                    vibration_utils.get_machines_with_vibration_analysis(
                        self.edges_data
                    )
                )
                self.vibrational_perceptions = vibration_utils.vibrational_perceptions(
                    edges_data=self.edges_data,
                    current_machine=self.current_machine,
                    current_edge=self.edge,
                    project_data=self.app_state.project_model,
                )
                self.current_perception = self.vibrational_perceptions[0]
            elif self.edge_kind in self._images_kind:
                self.data_format = self._animation_data_format
            elif self.edge_kind in self._complex_kind:
                self.data_format = self._animation_data_format
            else:
                log.info("No data updated")

    def get_edges_from_asset(self, current_asset):
        edges = []
        for edge_name in current_asset["edges_ids"]:
            edge_type = (
                self.data['edges'].get('type', None)
            )  # there are edges with device_type and type in firestore
            if edge_type:
                if edge_type == "ACTUATOR_DEVICE":
                    pass
                else:
                    edges.append(edge_name)
            else:
                edge_type = (
                    self.data['edges'].get('device_type', None)
                )  # there are edges with device_type and type in firestore
                if edge_type == "ACTUATOR_DEVICE":
                    pass
                else:
                    edges.append(edge_name)
        return edges

    def get_perceptions_for_robot_devices(self):
        """
        In robot devices, returns a list with the perceptions according to the current edge kind.
        """
        if self.edge_kind in self._images_kind:
            return [self._image_perception, self._thermographic_perception]
        elif self.edge_kind in self._complex_kind:
            return [
                self._image_perception,
                self._thermographic_perception,
                self._temperature_perception,
            ]

    def _render_submenu(self):
        self.get_data()
        machines = list(self.data["machines"].keys())
        timezone = pytz.timezone("America/Mexico_City")
        st.selectbox(
            label="Activo",
            options=machines,
            key=f"{self.__class__.__name__}_machine_selectbox",
            on_change=self._update_asset,
            index=0,
        )
        if self.edge is not None:
            st.selectbox(
                label="Dispositivo",
                options=self.current_readable_names_map.values(),
                key=f"{self.__class__.__name__}_edge_selectbox",
                on_change=self._update_edge,
                index=0,
            )
            if self.edge_kind in self._temperature_kind:
                st.radio(
                    label="\n",
                    options=(
                        self._per_last_signals,
                        self._per_time_sheet,
                    ),
                    index=1,
                    key=f"{self.__class__.__name__}_sheet_radio",
                    on_change=self._update_sheet,
                )

            with st.form("range_form"):
                st.markdown(
                    "**<p align='center'>Configura tu visualización de data</p>**",
                    unsafe_allow_html=True,
                )
                st.date_input(
                    "Introduce una fecha",
                    datetime.datetime.today()
                    if "date" not in self.data_request.range_time
                    else self.data_request.range_time["date"],
                    key=f"{self.__class__.__name__}_date_input",
                )
                st.time_input(
                    "Desde:",
                    timezone.localize(datetime.datetime.now())
                    if "start" not in self.data_request.range_time
                    else self.data_request.range_time["start"],
                    key=f"{self.__class__.__name__}_start_time_input",
                )
                st.time_input(
                    "Hasta:",
                    timezone.localize(datetime.datetime.now())
                    if "end" not in self.data_request.range_time
                    else self.data_request.range_time["end"],
                    key=f"{self.__class__.__name__}_end_time_input",
                )

                if self.edge_kind in self._images_kind:
                    st.selectbox(
                        label="Tipo de formato",
                        options=(self._animation_data_format, ),
                        index=0,
                        key=f"{self.__class__.__name__}_format_selectbox",
                    )

                elif self.edge_kind in self._vibrational_kind:
                    self.vibrational_perceptions = (
                        vibration_utils.vibrational_perceptions(
                            edges_data=self.edges_data,
                            current_machine=self.current_machine,
                            current_edge=self.edge,
                            project_data=self.app_state.project_model,
                        )
                    )
                    st.selectbox(
                        label="Dimensión de percepción",
                        options=self.vibrational_perceptions,
                        index=0,
                        key=f"{self.__class__.__name__}_perception_selectbox",
                    )
                else:
                    pass

                st.form_submit_button("Aceptar", on_click=self._update_range_time)
        else:
            pass

    def _update_edge(self):
        self.edge = st.session_state[f"{self.__class__.__name__}_edge_selectbox"]
        print(f"Current edge set to {self.edge}")
        for non_readable, readable in self.current_readable_names_map.items():
            if self.edge == readable:
                self.edge = non_readable
        self.edge_kind = self.get_kind_from_edge()

    def _update_asset(self):
        machine = st.session_state[f"{self.__class__.__name__}_machine_selectbox"]
        self.current_machine = machine
        self.edges = self.get_edges_from_asset(self.data["machines"][machine])
        self.current_readable_names_map = self.names_human_readable()
        if not self.edges:
            self.edge = None
        else:
            self.edge = self.edges[0]
            self.edge_kind = self.get_kind_from_edge()

        self.widget = None
        self._images_charts = ImagesDataCharts()
        self._vibration_charts = VibrationDataCharts()
        self._temperature_charts = TemperatureDataCharts()
        self.data_request = DataRequest()

    def _update_sheet(self):
        sheet = st.session_state[f"{self.__class__.__name__}_sheet_radio"]
        self.sheet = sheet

    def _update_perceptions(self):
        perception = st.session_state[f"{self.__class__.__name__}_perception_selectbox"]
        self.current_perception = perception

    def _update_range_time(self):
        self._update_edge()
        self._redraw_required = True
        if self.edge_kind not in self._vibrational_kind:
            data_to_render = {}
            perceptions = self.get_perceptions_for_robot_devices()
            for perception in perceptions:
                self.data_request = DataRequest(
                    range_time={
                        "date": st.session_state[
                            f"{self.__class__.__name__}_date_input"
                        ],
                        "start": st.session_state[
                            f"{self.__class__.__name__}_start_time_input"
                        ],
                        "end": st.session_state[
                            f"{self.__class__.__name__}_end_time_input"
                        ],
                    },
                    edge_kind=self.edge_kind,
                    bigquery_dataset=self._bigquery_dataset,
                    tenant_id=self._tenant_id,
                    edge=self.edge,
                    perception=perception,
                    bqclient=self.bqclient,
                )
                time_data = self.data_request.get_data_from_table_in_dataset("time", self.app_state.authentication_info.user_role)
                data_to_render.update({perception: time_data})
            self.formatted_asset_name = self.formatting_readable_strings(
                self.current_machine
            )
            if self.edge_kind in self._images_kind:
                self.data_format = st.session_state[
                    f"{self.__class__.__name__}_format_selectbox"
                ]
                self.normal_data = data_to_render[self._image_perception]
                self.thermographic_data = data_to_render[self._thermographic_perception]
                data_to_annotate = self.normal_data
            elif self.edge_kind in self._complex_kind:
                self.normal_data = data_to_render[self._image_perception]
                self.thermographic_data = data_to_render[self._thermographic_perception]
                self.normal_data = data_to_render[self._image_perception]

                self.temperature_data = complex_utils._get_temperatures(
                    data_to_render[self._temperature_perception]
                )
                data_to_annotate = self.normal_data
            elif self.edge_kind in self._temperature_kind:
                if self.sheet == self._per_last_signals:
                    data_last_temperature_values = (
                        temperature_utils.get_last_temperature_values(
                            self._tenant_id,
                            f"{self._bigquery_dataset}.time",
                            self.edge,
                            self.current_perception,
                            self.data_request.bqclient
                        )
                    )
                    self.last_temperatures_values = (
                        data_last_temperature_values.values()
                    )
                    self.last_temperatures_dates = data_last_temperature_values.keys()
                    data_to_annotate = None
                else:
                    self.temperature_data = complex_utils._get_temperatures(
                        data_to_render[self._temperature_perception]
                    )
                    data_to_annotate = data_to_render[self._temperature_perception]
        else:
            perception = st.session_state[
                f"{self.__class__.__name__}_perception_selectbox"
            ]
            self.current_perception = perception
            self.data_request = DataRequest(
                range_time={
                    "date": st.session_state[f"{self.__class__.__name__}_date_input"],
                    "start": st.session_state[
                        f"{self.__class__.__name__}_start_time_input"
                    ],
                    "end": st.session_state[
                        f"{self.__class__.__name__}_end_time_input"
                    ],
                },
                edge_kind=self.edge_kind,
                bigquery_dataset=self._bigquery_dataset,
                tenant_id=self._tenant_id,
                edge=self.edge,
                perception=perception,
                bqclient=self.bqclient,
            )
            if self.current_perception == self._temperature_perception:
                temperature_signals = self.data_request.get_data_from_table_in_dataset(
                    "time",  self.app_state.authentication_info.user_role
                )
                self.temperature_data = complex_utils._get_temperatures(
                    temperature_signals
                )
                data_to_annotate = temperature_signals
            else:
                self.vibration_data = self.data_request.get_data_from_table_in_dataset(
                    "time",  self.app_state.authentication_info.user_role
                )
                self.fft_metrics_df = (
                    self.data_request._get_data_from_table_in_dataset_ordered_by_value(
                        "fft_metrics"
                    )
                )
                self.psd_metrics_df = (
                    self.data_request._get_data_from_table_in_dataset_ordered_by_value(
                        "psd_metrics"
                    )
                )
                data_to_annotate = self.vibration_data

        if (
            data_to_annotate
            and self.app_state.authentication_info.user_role == AuthenticationInfo.UserRole.Admin
            and len(self.data['machines'][self.current_machine]['tasks'].keys())
        ):
            # Note: assumes 1 task only.
            asset_tasks = self.data['machines'][self.current_machine]['tasks']
            task: AssetTask = AssetTask(**list(asset_tasks.values())[0])
            self.widget = AnnotationWidget(
                task.label_def,
                self.edges_data[self.current_machine],
                data_to_annotate,
                self._bigquery_dataset,
                self.data_request.bqclient,
            )
        else:
            self.widget = None

    def _render_content(self):
        log.info("Starting rendering of Analytics...")
        self.get_data()
        annotation_row = None
        self.formatted_asset_name = self.formatting_readable_strings(
            self.current_machine
        )
        padding = 0
        st.markdown(
            """
        <style>
        .big-font {
            font-size:8px !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f""" <style>
                                                    .reportview-container .main .block-container{{
                                                        padding-bottom: {padding}rem;
                                                    }} </style> """,
            unsafe_allow_html=True,
        )
        if self.edge is None:
            st.header(f"{self.formatted_asset_name}")
            st.info(
                f"No hay dispositivos monitoreando en {self.formatted_asset_name}"
            )
        else:
            if self.edge_kind in self._images_kind:
                c = st.empty()
                with c.container():
                    st.header(f"Análisis de imagenes")
                    st.subheader(f"{self.formatted_asset_name}")
                    c = st.empty()
                    if "end" not in self.data_request.range_time:
                        with c.container():
                            st.success(
                                "Introduce un intervalo de tiempo para visualizar los datos."
                            )
                    else:
                        annotation_row = st.empty()
                        if self._redraw_required:
                            computer_vision_utils.get_images_analysis(
                                user=self.app_state.authentication_info.user_role,
                                normal_data=self.normal_data,
                                thermographic_data=self.thermographic_data,
                                range_time=self.data_request.range_time,
                                data_format=self.data_format,
                                images_data_format=self._images_data_format,
                                timages_data_format=self._timages_data_format,
                                animation_data_format=self._animation_data_format,
                                images_charts=self._images_charts
                            )
                            self._redraw_required = False

                        self._draw_images_data()

            elif self.edge_kind in self._vibrational_kind:
                if self.current_perception != self._temperature_perception:
                    st.header(f"Análisis de vibraciones")
                    st.subheader(f"{self.sheet}: {self.formatted_asset_name}")
                    c = st.empty()
                    if "end" not in self.data_request.range_time:
                        with c.container():
                            st.success(
                                "Introduce un intervalo de tiempo para visualizar los datos."
                            )
                    else:
                        with c.container():
                            st.markdown(f"##### {self.current_perception}")
                            annotation_row = st.empty()
                            if self._redraw_required:
                                vibration_utils.plotting_time_data(
                                    self.app_state.project_model,
                                    self.current_perception,
                                    self.vibration_data,
                                    self.fft_metrics_df,
                                    self.psd_metrics_df,
                                    self.app_state.authentication_info.user_role,
                                    self._vibration_charts
                                )
                                self._redraw_required = False
                            self._draw_vibrational_data()

                else:
                    st.header(f"Análisis de temperatura")
                    st.subheader(f"{self.sheet}: {self.formatted_asset_name}")
                    if self.sheet == self._per_last_signals:
                        if self.last_temperatures_values is None:
                            st.info(f"Sin registro en la última hora.")
                        else:
                            st.markdown(
                                f"#### Temperatura actual de {self.formatted_asset_name}"
                            )
                            temperature_utils.actual_machine_temperature(
                                self.last_temperatures_values
                            )
                            st.markdown("\n")
                            st.markdown("\n")
                            if self._redraw_required:
                                self._temperature_charts.temp_chart = temperature_utils.plot_asset_temperatures(
                                    temperature_values=self.last_temperatures_values,
                                    temperature_dates=self.last_temperatures_dates,
                                    name="Temperatura",
                                )
                                self._redraw_required = False
                            self._draw_temperature_data()
                    else:
                        c = st.empty()
                        if "end" not in self.data_request.range_time:
                            with c.container():
                                st.success(
                                    "Introduzca un intervalo de tiempo para visualizar los datos."
                                )
                        else:
                            with c.container():
                                if not self.temperature_data[0] is None:
                                    annotation_row = st.empty()
                                    if self._redraw_required:
                                        self._temperature_charts.temp_chart = temperature_utils.plot_asset_temperatures(
                                            temperature_values=self.temperature_data[0],
                                            temperature_dates=self.temperature_data[1],
                                            name=f"Temperatura de {self.current_machine}",
                                        )
                                        self._redraw_required = False

                                    self._draw_temperature_data()

                                else:
                                    st.text("No hay data en ese intervalo")
            elif self.edge_kind in self._complex_kind:
                st.header("Análisis compuesto")
                st.subheader(f"{self.formatted_asset_name}")
                c = st.empty()
                if "end" not in self.data_request.range_time:
                    with c.container():
                        st.success(
                            "Introduce un intervalo de tiempo para visualizar los datos."
                        )
                else:
                    annotation_row = st.empty()
                    if self._redraw_required:
                        self._redraw_required = False
                        complex_utils.get_images_and_temperature_analysis(
                            user=self.app_state.authentication_info.user_role,
                            normal_data=self.normal_data,
                            thermographic_data=self.thermographic_data,
                            range_time=self.data_request.range_time,
                            data_format=self.data_format,
                            images_data_format=self._images_data_format,
                            timages_data_format=self._timages_data_format,
                            animation_data_format=self._animation_data_format,
                            temperatures_values=self.temperature_data[0],
                            temperatures_dates=self.temperature_data[1],
                            current_machine=self.current_machine,
                            images_charts=self._images_charts,
                            temperature_charts=self._temperature_charts,
                            max_min_temp=st.secrets['max_min_temp']
                        )
                    self._draw_temperature_data()
                    self._draw_images_data()

            elif self.edge_kind == "Mock":
                st.header("Análisis Mock")
                st.subheader(f"{self.formatted_asset_name}")
                c = st.empty()
                if "end" not in self.data_request.range_time:
                    with c.container():
                        st.success(
                            "Introduce un intervalo de tiempo para visualizar los datos."
                        )
                else:
                    with c.container():
                        st.markdown(f"##### {self.current_perception}")
                        annotation_row = st.empty()
                        if self._redraw_required:
                            vibration_utils.plotting_time_data(
                                self.app_state.project_model,
                                self.current_perception,
                                self.vibration_data,
                                self.fft_metrics_df,
                                self.psd_metrics_df,
                                self.app_state.authentication_info.user_role,
                                self._vibration_charts
                            )
                            self._redraw_required = False
                        self._draw_vibrational_data()
            else:
                st.error("Escoge otro asset para visualizar sus datos")
            if (
                annotation_row
                and self.app_state.authentication_info.user_role
                == AuthenticationInfo.UserRole.Admin
            ):
                with annotation_row:
                    if self.widget:
                        self.widget._render()

    def _draw_vibrational_data(self):
        if not self._vibration_charts.fft_metrics_df is None:
            st.markdown("#### FFT")
            st.plotly_chart(self._vibration_charts.fft_chart, use_container_width=True)
            st.markdown("#### Métricas de la FFT")
            vibration_utils.metrics_visualization(df=self._vibration_charts.fft_metrics_df)
            st.markdown("***")

        if not self._vibration_charts.psd_metrics_df is None:
            st.markdown("#### PSD")
            st.plotly_chart(self._vibration_charts.psd_chart, use_container_width=True)
            st.markdown("#### Métricas de la PSD")
            vibration_utils.metrics_visualization(df=self._vibration_charts.psd_metrics_df)

    def _draw_images_data(self):
        # draw normal images
        log.info("Start to draw images on browser...")
        st.markdown(f"#### Imágenes fotográficas")
        global _IMAGES_RANGE_TIME_EXCEEDED

        if _IMAGES_RANGE_TIME_EXCEEDED:
            st.warning("La cantidad de imágenes encontradas es muy grande. Ingrese un intervalo menor "
                     "para visualizar las imágenes.")
            return

        if self._images_charts.normal_imgs_chat:
            st.plotly_chart(self._images_charts.normal_imgs_chat,
                            use_container_width=True)
        else:
            st.info(
                f"No hay data para mostrar en {self.data_request.range_time['date'].strftime('%Y/%m/%d')} "
                f"de las {self.data_request.range_time['start'].strftime('%H:%M')} a "
                f"las {self.data_request.range_time['end'].strftime('%H:%M')}"
            )

        st.markdown("#### Imágenes termográficas")
        if self._images_charts.thermographic_imgs_datacharts:
            st.plotly_chart(self._images_charts.thermographic_imgs_datacharts,
                            use_container_width=True)
        else:
            st.info(
                f"No hay data para mostrar en {self.data_request.range_time['date'].strftime('%Y/%m/%d')} "
                f"de las {self.data_request.range_time['start'].strftime('%H:%M')} a "
                f"las {self.data_request.range_time['end'].strftime('%H:%M')}"
            )

    def _draw_temperature_data(self):
        log.info("Start to draw images on browser...")

        st.subheader("Temperaturas")
        if self._temperature_charts.temp_chart:
            st.plotly_chart(self._temperature_charts.temp_chart,
                            use_container_width=True)
        else:
            st.text("No se consiguió datos para graficar temperatura")
