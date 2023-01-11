from typing import Dict, List
import pandas as pd
from txp.web.core_components.app_component import AppComponent
from txp.common.ml.models import (
    ModelStateValue, ModelRegistry, ModelMetadata,
    ErrorModelFeedback, SuccessModelFeedback, DefaultModelFeedback
)
from txp.common.utils.firestore_utils import ProjectModel, get_authenticated_client, get_current_project_model
from txp.ml.training_service.common import TrainCommand
from txp.web.core_components.main_view import MainView
from txp.web.core_components.app_profiles import AppProfile
import txp.common.utils.model_registry_utils as models_utils
import txp.common.utils.bigquery_utils as bq_utils
from fastapi import status
import streamlit as st
import requests
import logging
from txp.common.config import settings
from google.cloud import firestore
import json
from st_aggrid import AgGrid
import pytz as pytz
import datetime
from txp.common.utils.signals_utils import merge_signal_chunks


log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class FeedbackRenderer(AppComponent):
    def __init__(self, tenant_id: str, task_id: str, asset_id: str, model_registry: ModelRegistry, project_model: ProjectModel):
        super(FeedbackRenderer, self).__init__(component_key="feedback_renderer")
        self._model_entry: ModelRegistry = model_registry
        self._tenant_id: str = tenant_id
        self._task_id: str = task_id
        self._asset_id: str = asset_id
        self._project_model_ref: ProjectModel = project_model

        if hasattr(self._model_entry.metadata.feedback, 'failed_predictions'):
            self._wrong_predictions = list(map(
                lambda d: d['observation_timestamp'],
                self._model_entry.metadata.feedback.failed_predictions
            ))
        else:
            self._wrong_predictions = []

        self._pull_samples_requested: bool = False
        self._observation_timestamp_to_pull: int = None

    def _pull_observation_timestamp(self, edges: List[str], partition_datetime, perceptions):
        client = bq_utils.get_authenticated_client(
            self.app_state.authentication_info.role_service_account_credentials
        )
        df = bq_utils.get_all_records_for_observation_timestamp(
            tenant_id=self._tenant_id,
            table_name=f"telemetry.time",
            edge_logical_ids=edges,
            perception_names=perceptions,
            observation_timestamp=self._observation_timestamp_to_pull,
            start_datetime=partition_datetime,
            end_datetime=partition_datetime,
            order_key="observation_timestamp",
            client=client,
        )

        perceptions_per_edge: Dict = {}
        for edge_logical_id, raw_signals_df in df.groupby(by='edge_logical_id'):
            perceptions_per_edge[edge_logical_id] = {}
            for signal_timestamp, signal_df in df.groupby("signal_timestamp"):
                all_chunks = signal_df.to_dict('records')
                signal = merge_signal_chunks(all_chunks)
                perception_name = all_chunks[0]['perception_name']
                perceptions_per_edge[edge_logical_id][perception_name] = signal

        return perceptions_per_edge

    def _render(self):
        st.markdown(f"**Resultados del entrenamiento**")
        if isinstance(self._model_entry.metadata.feedback, ErrorModelFeedback):
            st.markdown(f"**Error**: {self._model_entry.metadata.feedback.error_message}")

        elif isinstance(self._model_entry.metadata.feedback, SuccessModelFeedback):
            st.markdown(f"""**Metrics:**""")
            st.json(json.dumps(self._model_entry.metadata.feedback.metrics))
            failed_entries_df: pd.DataFrame = pd.DataFrame.from_records(
                self._model_entry.metadata.feedback.failed_predictions
            )
            AgGrid(failed_entries_df)

            with st.form(key="_view_incorrect_prediction_data_form"):
                st.write("Seleccione una muestra fallida para visualizar percepciones")
                observation_timestamp = st.selectbox(
                    "Observation timestamp",
                    options=list(self._wrong_predictions)
                )
                st.form_submit_button(
                    "Renderizar",
                    on_click=self._update_observation_timestamp_to_pull,
                    args=(observation_timestamp,)
                )

                preview_section = st.empty()

                if self._pull_samples_requested:
                    with preview_section.container():
                        self._pull_samples_requested = False

                        try:

                            edges = self._project_model_ref.tasks_by_asset[self._asset_id][self._task_id].edges
                            perceptions = set()
                            # Get all possible perceptions from task
                            for entry in self._project_model_ref.tasks_by_asset[self._asset_id][self._task_id].schema_.values():
                                perceptions.update(entry.keys())

                            partition_datetime_upper = datetime.datetime.fromtimestamp(
                                int(self._observation_timestamp_to_pull) / 1e9
                            )

                            perceptions_per_edge = self._pull_observation_timestamp(
                                edges, partition_datetime_upper, list(perceptions)
                            )

                            for edge in edges:
                                st.markdown(f"### {edge}:")
                                for perception, signal in perceptions_per_edge[edge].items():
                                    if perception in {"Image", "ThermalImage"}:
                                        img = bq_utils.get_image_from_raw_data(
                                            signal['data']
                                        )
                                        st.markdown(f"**{perception}**")
                                        st.image(img)

                                    else:
                                        st.markdown(f"Renderizado de {perception} no soportado")
                        except Exception as e:
                            st.warning("Hubo un error renderizando el preview de las muestras.")
                            log.error(f"Error trying to render failed prediction samples: {e}")


    def _update_observation_timestamp_to_pull(self, observation_timestamp):
        self._pull_samples_requested = True
        self._observation_timestamp_to_pull = observation_timestamp


class TrainingView(MainView):
    """This view is used for training models based on datasets available
    in the data warehouse."""

    def __init__(self):
        super(TrainingView, self).__init__(component_key="training_view")
        self._asset_selectbox_val: str = ""
        self._asset_selectbox_key: str = "asset_sb"
        self._task_selectbox_val: str = ""
        self._task_selectbox_key: str = "task_sb"
        self._dataset_name_val: str = ""
        self._dataset_name_key: str = "dataset_name_key"
        self._versions_val: List[str] = []
        self._versions_key: str = "versions_form_key"

        self._task_parameters_val: Dict = {}
        self._task_parameters_key = "tasks_parameters_key"
        self._invalid_parameters_json = False

        self._project_configuration_data: ProjectModel = None
        self._model_registry_col: str = "txp_models_registry"
        self._pulled_model: ModelRegistry = None
        self._feedback_explorer: FeedbackRenderer = None

    def get_associated_profile(self) -> AppProfile:
        return AppProfile.ANALYTICS

    def implements_submenu(self) -> bool:
        return True

    @classmethod
    def get_display_name(cls) -> str:
        return "Entrenar Task"

    def _build_submenu_state(self) -> Dict:
        return {}

    def _build_content_state(self) -> Dict:
        return {}

    def _on_json_parameters_change(self):
        json_str = st.session_state[self._task_parameters_key]

        try:
            json.loads(json_str)
        except Exception as e:
            log.error(f"Unexpected exception while parsing "
                      f"task parameters json: {e}")
            self._invalid_parameters_json = True

        else:
            self._invalid_parameters_json = False
            self._task_parameters_val = json_str

    def _get_project_configuration(self):
        db = get_authenticated_client(
            self.app_state.authentication_info.role_service_account_credentials
        )
        self._project_configuration_data = get_current_project_model(
            db, self._tenant_id
        )
        self._current_gateway = list(
            self._project_configuration_data.gateways_table.keys()
        )[0]

    def _register_asset_value(self):
        self._asset_selectbox_val = st.session_state[self._asset_selectbox_key]

    def _register_dataset_name_value(self):
        self._dataset_name_val = st.session_state[self._dataset_name_key]

    def _register_dataset_versions_values(self):
        self._versions_val = (
            st.session_state[self._versions_key].replace(" ", "").split(",")
        )

    def _register_task_value(self):
        self._task_selectbox_val = st.session_state[self._task_selectbox_key]

    def _validate_training_allowed(
        self, dataset_name: str, dataset_versions: List[str]
    ) -> bool:
        firestore_db: firestore.Client = get_authenticated_client(
            self.app_state.authentication_info.role_service_account_credentials
        )
        model_registry_name = models_utils.get_gcs_dataset_prefix(
            dataset_name, dataset_versions
        )
        model = models_utils.get_ml_model(
            firestore_db,
            self._tenant_id,
            self._asset_selectbox_val,
            self._task_selectbox_val,
            model_registry_name,
            self._model_registry_col,
        )
        firestore_db.close()
        if not model:
            return True

        if model.state.value.value == ModelStateValue.TRAINING.value:
            return False

        else:
            return True

    def _train_model(self, train_payload: TrainCommand):
        headers = {"Authorization": f"Bearer {st.secrets['service_auth_token']}"}
        response = requests.post(
            f"{st.secrets.service_url}/training/train", json=train_payload.dict(),
            headers=headers
        )
        if response.status_code == status.HTTP_200_OK:
            st.success("Su modelo se ha empezado a entrenar correctamente")

        elif response.status_code == status.HTTP_404_NOT_FOUND:
            st.warning(f"Error al lanzar entrenamiento: {response.json()['Error']}")
        else:
            st.warning(f"Error desconocido al lanzar entrenamiento: ")
            st.json(response)

    def _publish_model(self, publish_payload: TrainCommand):
        headers = {"Authorization": f"Bearer {st.secrets['service_auth_token']}"}
        response = requests.post(
            f"{st.secrets.service_url}/training/publish", json=publish_payload.dict(),
            headers=headers
        )
        if response.status_code == status.HTTP_200_OK:
            st.success("Su modelo ha sido promovido correctamente al servicio de predicción")
            self._pulled_model = None  # Clear the memory from memory

        elif response.status_code == status.HTTP_404_NOT_FOUND:
            st.warning("Su modelo no existe o ya esta publicado en el servicio de predicción")
            st.text("Si el problema persiste, contacte a soporte.")

    def _render_content(self) -> None:
        if not self._project_configuration_data:
            self._get_project_configuration()

        st.markdown("Entrenar Task para un Activo")
        logging.info(f"Rendering selected active: {self._asset_selectbox_val}")
        logging.info(f"Rendering selected task: {self._task_selectbox_val}")

        self._asset_selectbox_val = st.selectbox(
            label="Seleccione Activo",
            options=list(self._project_configuration_data.machines_table.keys()),
            key=self._asset_selectbox_key,
            on_change=self._register_asset_value,
            index=0,
        )

        self._task_selectbox_val = st.selectbox(
            label="Seleccione Task",
            options=list(
                self._project_configuration_data.tasks_by_asset[
                    self._asset_selectbox_val
                ].keys()
            ),
            on_change=self._register_task_value,
            key=self._task_selectbox_key,
            index=0,
        )

        with st.form(key="dataset_info_form"):
            dataset_name = st.text_input(
                label="Ingrese el nombre del dataset",
                help="El nombre del dataset acordado por el equipo de anotación",
                key=self._dataset_name_key,
            )

            dataset_versions = st.text_input(
                label="Ingrese las versiones separadas por coma", key=self._versions_key
            )

            task_parameters_text = st.text_area(
                label="Diccionario de parámetros",
                value="{}",
                key=self._task_parameters_key,
                help="Introduzca parámetros al modelo en formato JSON",

            )

            st.form_submit_button("Entrenar", on_click=self._start_train)

            see_result_clicked = st.form_submit_button(
                "Ver resultado",
                on_click=self._check_train_result,
            )

        if self._pulled_model:
            st.markdown("**Resumen del modelo:**")
            st.markdown(f"Tenant: {self._pulled_model.metadata.tenant_id}")
            st.markdown(f"Task: {self._pulled_model.metadata.task_id}")
            st.markdown(f"Asset: {self._pulled_model.metadata.machine_id}")
            st.markdown(f"Estado del modelo:")
            st.json(self._pulled_model.state.json())
            st.markdown(f"Feedback del modelo:")
            self._feedback_explorer.render()

            if self._pulled_model.state.value == ModelStateValue.ACKNOWLEDGE or \
                    self._pulled_model.state.value == ModelStateValue.OLD:
                st.info(
                    "El modelo ha terminado de entrenar, y puede ser promovido a predicción"
                )
                st.button("Promover", on_click=self._approve_ack_model)

    def _render_pulled_model(self):
        st.markdown("***********")
        st.markdown(f"## Modelo entrenado {self._pulled_model.metadata.task_id}")
        st.markdown(f"**Tenant:** {self._pulled_model.metadata.tenant_id}")
        st.markdown(f"**Task:** {self._pulled_model.metadata.task_id}")
        st.markdown(f"**Asset:** {self._pulled_model.metadata.machine_id}")
        st.markdown(f"**Estado del modelo:** {self._pulled_model.state.value}")
        st.markdown(f"**Ruta del modelo:** {self._pulled_model.file_path}")

        # Render Feedback logic
    def _start_train(self):
        st.info("Starting training process...")
        self._register_asset_value()
        self._register_task_value()
        self._register_dataset_versions_values()
        self._register_dataset_name_value()

        self._on_json_parameters_change()
        if self._invalid_parameters_json:
            st.warning("El JSON de parámetros tiene errores de sintaxis.")
            return

        training_allowed = self._validate_training_allowed(
            self._dataset_name_val, self._versions_val
        )
        if not training_allowed:
            st.warning(
                "Actualmente su Task se encuentra entrenando. "
                "Espere a que el task termine de entrenar"
            )
        else:
            train_payload = TrainCommand(
                dataset_name=self._dataset_name_val,
                dataset_versions=self._versions_val,
                tenant_id=self._tenant_id,
                machine_id=self._asset_selectbox_val,
                task_id=self._task_selectbox_val,
                task_params=self._task_parameters_val
            )
            self._train_model(train_payload)
            self._pulled_model = None

    def _check_train_result(self):
        self._register_asset_value()
        self._register_task_value()
        self._register_dataset_versions_values()
        self._register_dataset_name_value()
        firestore_db: firestore.Client = get_authenticated_client(
            self.app_state.authentication_info.role_service_account_credentials
        )
        model_reg_name = models_utils.get_gcs_dataset_prefix(
            self._dataset_name_val, self._versions_val
        )
        logging.info(
            "Requesting model from models registry for: \n"
            f"Tenant: {self._tenant_id} \n"
            f"Asset: {self._asset_selectbox_val} \n"
            f"Task: {self._task_selectbox_val} \n"
            f"Model Registry: {model_reg_name}"
        )
        model = models_utils.get_ml_model(
            firestore_db,
            self._tenant_id,
            self._asset_selectbox_val,
            self._task_selectbox_val,
            model_reg_name,
            self._model_registry_col,
        )
        if model is None:
            st.error(
                "No se pudo encontrar registros para el modelo. Si el problema persiste, "
                "contacte a soporte"
            )
            self._pulled_model = None
            return

        else:
            self._pulled_model = model
            self._feedback_explorer = FeedbackRenderer(
                self._tenant_id, self._task_selectbox_val,
                self._asset_selectbox_val, self._pulled_model,
                self.app_state.project_model
            )

    def _approve_ack_model(self):
        self._register_asset_value()
        self._register_task_value()
        self._register_dataset_versions_values()
        self._register_dataset_name_value()
        self._on_json_parameters_change()
        train_payload = TrainCommand(
            dataset_name=self._dataset_name_val,
            dataset_versions=self._versions_val,
            tenant_id=self._tenant_id,
            machine_id=self._asset_selectbox_val,
            task_id=self._task_selectbox_val,
            task_params=self._task_parameters_val
        )
        self._publish_model(train_payload)

    def _render_submenu(self) -> None:
        if not self._project_configuration_data:
            self._get_project_configuration()
