from txp.common.configuration import JobConfig
from txp.common.utils.firestore_utils import ConfigurationSnapshotType, ProjectModel, \
    get_authenticated_client, get_current_project_model, create_configuration_snapshot, \
    pull_current_configuration_from_firestore
from txp.web.core_components.main_view import MainView
from txp.web.core_components.app_profiles import AppProfile
import streamlit as st
from txp.common.utils.json_complex_encoder import ComplexEncoder
from typing import Dict
import logging
import json

from txp.common.config import settings

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class EditConfigurationView(MainView):
    """This View implements use cases to upate configuration of the project model.

    Currently, it only supports the use case to update the Job of a Gateway device.
    """

    def __init__(self):
        super(EditConfigurationView, self).__init__(component_key="edit_configuration")
        self._project_configuration_data: ProjectModel = None
        self._current_gateway: str = ""
        self._text_area_unique_key = f"{id(self)}_job_for_gateway_text_area"
        self._gateway_selectbox_unique_key = f"{id(self)}_gateway_selectbox"
        self._show_invalid_json_alert: bool = False
        self._show_success_update: bool = False
        self._show_failure_update: bool = False
        self._show_outdated_configuration_warning: bool = False

    def implements_submenu(self) -> bool:
        return True

    def get_associated_profile(self) -> AppProfile:
        return AppProfile.CONFIGURATION

    @classmethod
    def get_display_name(cls) -> str:
        return "Editar Configuración del Sistema"

    def _build_submenu_state(self) -> Dict:
        return {}

    def _build_content_state(self) -> Dict:
        return {}

    def _get_project_configuration(self):
        db = get_authenticated_client(
            self.app_state.authentication_info.role_service_account_credentials
        )
        self._project_configuration_data = get_current_project_model(db, self._tenant_id)
        self._current_gateway = list(
            self._project_configuration_data.gateways_table.keys()
        )[0]

    def _on_job_json_change(self):
        json_str = st.session_state[self._text_area_unique_key]
        json_dict = json.loads(json_str)
        job_config = JobConfig.build_from_dict(json_dict)

        if not job_config:
            self._show_invalid_json_alert = True
            log.error("Could not parse the edited Job configuration JSON")
        else:
            self._show_invalid_json_alert = False

        log.info("Job Config changed. Updating local information")
        self._project_configuration_data.jobs_table_by_gateway[
            self._current_gateway
        ] = job_config

    def on_gateway_selection_change(self):
        self._current_gateway = st.session_state[self._gateway_selectbox_unique_key]

    def on_create_snapshot_click(self, snapshot_type: ConfigurationSnapshotType):
        db = get_authenticated_client(
            self.app_state.authentication_info.role_service_account_credentials
        )

        # Applies a sentinel to see if the local state is outdated
        current_cloud_configuration = pull_current_configuration_from_firestore(db, self._tenant_id)
        current_cloud_configuration_version = current_cloud_configuration.to_dict()["configuration_id"]

        if current_cloud_configuration_version != self._project_configuration_data.configuration_version:
            log.warning("Trying to update cloud configuration but the local App data is outdated")
            self._show_outdated_configuration_warning = True
            db.close()
            return

        updated = create_configuration_snapshot(
            db, self._project_configuration_data, snapshot_type, self._tenant_id
        )
        db.close()
        if updated:
            self._show_success_update = True
            self._get_project_configuration()
        else:
            self._show_failure_update = True

    def _render_content(self) -> None:
        if not self._project_configuration_data:
            self._get_project_configuration()

        if self._show_invalid_json_alert:
            st.warning(
                "No se pudo parsear la configuración introducida. Intente nuevamente"
            )

        st.subheader(f"Configuración de trabajo {self._current_gateway}")

        if self._show_outdated_configuration_warning:
            st.warning("No se pudo actualizar la configuración porque necesita "
                       "descargar la configuración más reciente. Recargue esta ventana")
            self._show_outdated_configuration_warning = False

        if self._show_success_update:
            st.success("Se aplicó con éxito su actualización")
            self._show_success_update = False

        elif self._show_failure_update:
            st.error("Hubo un error y su configuración no se pudo aplicar")
            self._show_failure_update = False

        st.markdown(
            f"**Versión de configuración:** {self._project_configuration_data.configuration_version}"
        )

        gateway_job_config = self._project_configuration_data.jobs_table_by_gateway[
            self._current_gateway
        ]
        job_json = json.dumps(gateway_job_config, cls=ComplexEncoder, indent=4)
        st.text_area(
            f"Editar configuración",
            value=job_json,
            key=self._text_area_unique_key,
            height=600,
            on_change=self._on_job_json_change,
        )

        st.button(
            label="Aplicar version preliminar",
            help="Aplicar configuración preliminar con version X.X",
            on_click=self.on_create_snapshot_click,
            args=(ConfigurationSnapshotType.PRELIMINARY,),
        )

        st.button(
            label="Aplicar version",
            help="Aplicar configuración con version X",
            on_click=self.on_create_snapshot_click,
            args=(ConfigurationSnapshotType.NORMAL,),
        )

    def _render_submenu(self) -> None:
        if not self._project_configuration_data:
            self._get_project_configuration()

        st.markdown("**Actualizar configuración de trabajo**")
        st.selectbox(
            label="Seleccione el Gateway",
            options=list(self._project_configuration_data.gateways_table.keys()),
            key=self._gateway_selectbox_unique_key,
            on_change=self.on_gateway_selection_change,
        )
