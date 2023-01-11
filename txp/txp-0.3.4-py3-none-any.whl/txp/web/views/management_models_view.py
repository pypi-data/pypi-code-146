import txp.common.utils.firestore_utils
from txp.web.core_components.app_profiles import AppProfile
from txp.web.core_components.main_view import MainView
import logging
from typing import Dict
import streamlit as st
import pandas as pd
import requests
from fastapi import status
from txp.common.utils.model_registry_utils import get_all_model_registries
from txp.common.ml.models import ModelRegistry
from txp.ml.training_service.common import TrainCommand
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder


# TODO: This might be a problem. The logging configuration is being taken from `txp` package
from txp.common.config import settings

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class ManagementModelsView(MainView):
    """The management models View"""

    def __init__(self):
        super(ManagementModelsView, self).__init__(component_key="management_models_view")
        self.data = None
        self.assets = None
        self.tasks = None
        self.current_asset = None
        self.current_task = None
        self.model_registries = None
        self.models = None

    def implements_submenu(self) -> bool:
        return True

    def get_associated_profile(self) -> AppProfile:
        return AppProfile.ANALYTICS

    @classmethod
    def get_display_name(cls) -> str:
        return "Administrar modelos"

    def get_data(self):
        if self.data is None:
            self.db = txp.common.utils.firestore_utils.get_authenticated_client(
                self.app_state.authentication_info.role_service_account_credentials
            )

            self.data = txp.common.utils.firestore_utils.pull_recent_project_data(self.db, self._tenant_id)
            self.assets = {d["machine_id"]: d for d in self.data["machines"]}
            self.tasks = self.get_tasks_per_machines()
            self.current_asset = list(self.assets.keys())[0]
            self.current_task = self.tasks[self.current_asset][0]
            self.model_registries = self.get_all_model_registries_per_task()
            self.models = self.model_registries[self.current_task]
            self.url = st.secrets["service_url"]
            self.db.close()

    def get_all_model_registries_per_task(self):
        all_models = {}
        for asset, tasks in self.tasks.items():
            data_models_per_task = {task: get_all_model_registries(
                    self.db,
                    self._tenant_id,
                    asset,
                    task,
                    "txp_models_registry",
                ) for task in tasks}
            for task, data_model_dicts in data_models_per_task.items():
                dataclass_model_objects = [ModelRegistry(**data_model_dict) for data_model_dict in data_model_dicts]
                all_models.update({task: dataclass_model_objects})
        return all_models

    def get_tasks_per_machines(self):
        tasks_per_machine = {}
        for machine, values in self.assets.items():
            tasks = []
            if type(values["tasks"]) == dict:
                for task in values["tasks"].values():
                    tasks.append(task["task_id"])
            else:
                for task in values["tasks"]:
                    tasks.append(task['task_id'])
            tasks_per_machine.update({machine: tasks})
        return tasks_per_machine

    def _build_submenu_state(self) -> Dict:
        pass

    def _build_content_state(self) -> Dict:
        pass

    def update_asset(self):
        machine = st.session_state[f"{self.__class__.__name__}_asset_selectbox"]
        self.current_asset = machine
        self.current_task = self.tasks[machine][0]
        self.models = self.model_registries[self.current_task]

    def update_task(self):
        task = st.session_state[f"{self.__class__.__name__}_task_selectbox"]
        self.current_task = task
        self.models = self.model_registries[task]

    def _render_submenu(self):

        st.selectbox(
            "Activo",
            options=self.assets.keys(),
            key=f"{self.__class__.__name__}_asset_selectbox",
            on_change=self.update_asset,
        )

        st.selectbox(
            'Tarea',
            options=self.tasks[st.session_state[f"{self.__class__.__name__}_asset_selectbox"]],
            key=f"{self.__class__.__name__}_task_selectbox",
            on_change=self.update_task,
        )

    def _preprocessing_model_data(self, models):
        columns = ['filepath', 'task_id', 'value', 'feedback', 'creation_date', 'publishment_date', 'deprecation_date']
        model_record_list = []
        for model in models:
            model_dict = {}
            model_data = model.dict()
            for k, v in model_data['metadata'].items():
                if k in columns:
                    model_dict.update({k:v})
            for k, v in model_data['state'].items():
                if k in columns:
                    model_dict.update({k:v})
            model_dict.update({'filepath': model_data['file_path']})
            model_record_list.append(model_dict)

        model_records_with_desired_order_keys = []
        for model_record in model_record_list:
            reorder_model_record = {k: model_record[k] for k in columns}
            model_records_with_desired_order_keys.append(reorder_model_record)
        return model_records_with_desired_order_keys

    def _display_models(self, models):
        preprocessed_df = self._preprocessing_model_data(models)

        df = pd.DataFrame(preprocessed_df)
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(min_column_width=100)
        gb.configure_pagination()
        options = gb.build()
        AgGrid(df, gridOptions=options)

    def _config_model(self):
        new_task = st.session_state[f"{self.__class__.__name__}_config_model_selectbox"]
        dataset_name = st.session_state[f"{self.__class__.__name__}_dataset_name_input"]
        versions = st.session_state[f"{self.__class__.__name__}_dataset_version"].replace(" ", "").split(",")
        train_command = TrainCommand(
            dataset_name=dataset_name,
            dataset_version=versions,
            tenant_id=self._tenant_id,
            machine_id=self.current_asset,
            task_id=new_task
        )

        headers = {"Authorization": f"Bearer {st.secrets['service_auth_token']}"}
        response = requests.post(
            f"{self.url}/training/publish", json=train_command.dict(),
            headers=headers)

        if response.status_code == status.HTTP_201_CREATED:
            st.success(
                f'El task {new_task} fue publicado satisfactoriamente.'
            )
        elif response.status_code == status.HTTP_412_PRECONDITION_FAILED:
            st.warning(
                f"El task no puede ser publicado en este momento: {response.json()['Error']}"
            )
        else:
            st.error(
                f'No se pudo publicar el task {new_task}.'
            )
            st.json(response.json())

        self.model_registries = self.get_all_model_registries_per_task()
        self.models = self.model_registries[self.current_task]

    def _css_button(self):
        m = st.markdown("""
        <style>
        div.stButton > button:first-child {
        color: #0000CD;
        box-sizing: 5%;
        height: 2em;
        width: 300px;
        font-size:20px;
        border: 2px solid;
        border-color: #D3D3D3;
        border-radius: 10px;
        box-shadow: 1px 1px 1px 1px
        rgba(0, 0, 0, 0.1);
        padding-top: 0px;
        padding-bottom: 0px;
        right: 0px;
        position: absolute;
        }
        </style>""", unsafe_allow_html=True)

    def _render_content(self):
        self.get_data()
        self._css_button()
        st.header('Registro de modelos: lista de modelos disponibles')
        self._display_models(self.models)

        st.subheader('Configurar nueva tarea')
        st.selectbox(
                'Modelos disponibles:',
                options=self.tasks[self.current_asset],
                key=f"{self.__class__.__name__}_config_model_selectbox",
            )
        st.text_input(
            label="Ingrese el nombre del dataset",
            help="El nombre del dataset acordado por el equipo de anotación",
            key=f"{self.__class__.__name__}_dataset_name_input",
        )
        st.text_input(
            "Inserte el nombre de la versión:",
            help="Si desea especificar más de una version, ingrese los enunciados separados por coma.",
            key=f"{self.__class__.__name__}_dataset_version",
        )
        st.button('Actualizar', on_click=self._config_model)
