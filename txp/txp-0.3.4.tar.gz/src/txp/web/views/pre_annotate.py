from txp.web.core_components.main_view import MainView
from typing import List, Dict
from txp.common.utils.firestore_utils import ProjectModel, get_authenticated_client, get_current_project_model
from txp.web.core_components.app_profiles import AppProfile
from txp.ml.training_service.dataset_committer import DatasetCommitPayload
import streamlit as st
from google.cloud import firestore
import txp.common.utils.model_registry_utils as models_utils
from txp.common.ml.models import (
    ModelStateValue, ModelRegistry, ModelMetadata,
    ErrorModelFeedback, SuccessModelFeedback, DefaultModelFeedback
)
from fastapi import status
import requests
import pytz
import datetime


class PreAnnotateView(MainView):
    """This is used for make predictions on records, and pre-annotate those
    predictions in order for annotator to save annotation time while testing
    a production model"""

    def __init__(self):
        super(PreAnnotateView, self).__init__(component_key="pre_annotate_vew")
        self._asset_selectbox_val: str = ""
        self._asset_selectbox_key: str = "asset_sb"
        self._task_selectbox_val: str = ""
        self._task_selectbox_key: str = "task_sb"
        self._range_time = {}
        self._project_configuration_data: ProjectModel = None
        self._model_registry_col: str = "txp_models_registry"

    def _render_submenu(self) -> None:
        pass

    def implements_submenu(self) -> bool:
        return True

    def get_associated_profile(self) -> AppProfile:
        return AppProfile.ANALYTICS

    @classmethod
    def get_display_name(cls) -> str:
        return "Pre-anotar muestras"

    def _build_submenu_state(self) -> Dict:
        return {}

    def _build_content_state(self) -> Dict:
        return {}

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

    def _format_range_date(self):
        tz = pytz.timezone("America/Mexico_City")
        full_dates = []

        full_date_start = datetime.datetime.combine(
            date=self.range_time['start_date'],
            time=self.range_time['start_time']
        )
        full_date_end = datetime.datetime.combine(
            date=self.range_time['end_date'],
            time=self.range_time['end_time']
        )

        for full_date in [full_date_start, full_date_end]:
            localized_full_date: datetime.datetime = tz.localize(full_date)
            utc_full_date: datetime.datetime = localized_full_date.astimezone(pytz.utc)
            full_dates.append(utc_full_date.strftime("%Y-%m-%d %H:%M:%S.%f%z"))

        return full_dates[0], full_dates[1]

    def _register_task_value(self):
        self._task_selectbox_val = st.session_state[self._task_selectbox_key]

    def __restart_task(self):
        db = get_authenticated_client(
            self.app_state.authentication_info.role_service_account_credentials
        )
        models_utils.set_is_pre_annotating_ml_model(db, self._tenant_id, self._asset_selectbox_val,
                                                            self._asset_selectbox_val, False,
                                                    "txp_")

    def _pre_annotate_model(self):
        self.range_time = {
            'start_date': st.session_state[f"{self.__class__.__name__}_date_range"][0],
            'end_date': st.session_state[f"{self.__class__.__name__}_date_range"][1],
            'start_time': st.session_state[f"{self.__class__.__name__}_start"],
            'end_time': st.session_state[f"{self.__class__.__name__}_end"]
        }
        full_start, full_end = self._format_range_date()

        commit_json = {
            "asset_id": self._asset_selectbox_val,
            "task_id": self._task_selectbox_val,
            "dataset_name": "",
            "tenant_id": self._tenant_id,
            "dataset_versions": [],
            "start": full_start,
            "end": full_end,
            "bigquery_dataset": self._bigquery_dataset,
        }

        headers = {"Authorization": f"Bearer {st.secrets['service_auth_token']}"}
        response = requests.post(
            f"{st.secrets.service_url}/annotation/pre-annotate",
            json=commit_json,
            headers=headers
        )
        if response.status_code == status.HTTP_201_CREATED:
            st.success("Se ha iniciado el proceso de pre-anotación.")

        elif response.status_code == status.HTTP_412_PRECONDITION_FAILED:
            st.warning("No se puede iniciar el proceso de pre-anotación."
                       " Actualmente el task ya esta pre-anotando.")

        elif response.status_code == status.HTTP_404_NOT_FOUND:
            st.warning(f"Error al lanzar entrenamiento: {response.json()['Error']}")
        else:
            st.warning(f"Error desconocido al lanzar entrenamiento: ")
            st.json(response.json())

    def _render_content(self) -> None:
        if not self._project_configuration_data:
            self._get_project_configuration()

        timezone = pytz.timezone("America/Mexico_City")

        st.markdown("Pre Anotar muestras")

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

        with st.form("commit"):
            st.date_input(
                "Inserte un periodo:",
                key=f"{self.__class__.__name__}_date_range",
                value=(
                    datetime.datetime.today()
                    if "init_date" not in self._range_time
                    else self._range_time["start_date"],
                    datetime.datetime.today()
                    if "finish_date" not in self._range_time
                    else self._range_time["end_date"]
                ),
            )

            st.time_input(
                "Hora de inicio de la data:",
                key=f"{self.__class__.__name__}_start",
                value=datetime.datetime.now().astimezone(tz=timezone)
                if "start_time" not in self._range_time
                else self._range_time["start_time"],
            )
            st.time_input(
                "Hora de culminación de la data:",
                key=f"{self.__class__.__name__}_end",
                value=datetime.datetime.now().astimezone(tz=timezone)
                if "end_time" not in self._range_time
                else self._range_time["end_time"]
            )

            st.form_submit_button("Pre-anotar", on_click=self._pre_annotate_model)
