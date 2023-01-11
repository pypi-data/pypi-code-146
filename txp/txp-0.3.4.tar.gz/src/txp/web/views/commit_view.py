"""
This module implements the Telemetry Health view for the application.

NOTE: This is just a dummy implementation of a MainView in order to shown the
mechanism provided by the `core_components` package.
"""
import txp.common.utils.firestore_utils
from txp.web.core_components.app_profiles import AppProfile
from txp.web.core_components.main_view import MainView
import logging
import requests
from fastapi import status
from typing import Dict
import streamlit as st
import datetime
import pytz

# TODO: This might be a problem. The logging configuration is being taken from `txp` package
from txp.common.config import settings

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class CommitView(MainView):
    """The Telemetry Health View"""

    def __init__(self):
        super(CommitView, self).__init__(component_key="commit_view")
        self.data = None
        self.machines = None
        self.range_time = {}

    def implements_submenu(self) -> bool:
        return True

    def get_associated_profile(self) -> AppProfile:
        return AppProfile.ANALYTICS

    @classmethod
    def get_display_name(cls) -> str:
        return "Publicar dataset"

    def get_data(self):
        if self.data is None:
            db = txp.common.utils.firestore_utils.get_authenticated_client(
                self.app_state.authentication_info.role_service_account_credentials
            )

            self.data = txp.common.utils.firestore_utils.pull_recent_project_data(db, self._tenant_id)
            self.machines = {d["machine_id"]: d for d in self.data["machines"]}
            self.tasks = self.get_tasks_per_machines()
            self.current_machine = list(self.machines.keys())[0]
            self.task = self.tasks[self.current_machine][0]
            self.url = st.secrets["service_url"]
            db.close()

    def get_tasks_per_machines(self):
        tasks_per_machine = {}
        for machine, values in self.machines.items():
            tasks = []
            if type(values["tasks"]) == dict:
                for task in values["tasks"].values():
                    tasks.append(task["task_id"])
            else:
                for task in values["tasks"]:
                    tasks.append(task["task_id"])
            tasks_per_machine.update({machine: tasks})
        return tasks_per_machine

    def _build_submenu_state(self) -> Dict:
        pass

    def _build_content_state(self) -> Dict:
        pass

    def _render_submenu(self):
        pass

    def parsed_versions(self, versions):
        versions_list = versions.replace(" ", "").split(",")
        return versions_list

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

    def _commit(self):
        versions = self.parsed_versions(
            st.session_state[f"{self.__class__.__name__}_dataset_version"]
        )

        self.range_time = {
            'start_date': st.session_state[f"{self.__class__.__name__}_date_range"][0],
            'end_date': st.session_state[f"{self.__class__.__name__}_date_range"][1],
            'start_time': st.session_state[f"{self.__class__.__name__}_start"],
            'end_time': st.session_state[f"{self.__class__.__name__}_end"]
        }

        full_start, full_end = self._format_range_date()

        commit_json = {
            "asset_id": st.session_state[f"{self.__class__.__name__}_machine"],
            "task_id": st.session_state[f"{self.__class__.__name__}_task"],
            "dataset_name": st.session_state[f"{self.__class__.__name__}_dataset_name"],
            "tenant_id": self._tenant_id,
            "dataset_versions": versions,
            "start": full_start,
            "end": full_end,
            "bigquery_dataset": self._bigquery_dataset,
        }
        try:
            headers = {"Authorization": f"Bearer {st.secrets['service_auth_token']}"}
            response = requests.post(f"{self.url}/annotation/commit", json=commit_json, headers=headers)
        except (ConnectionError, ConnectionRefusedError) as ce:
            st.error("No se pudo establecer con el servidor de anotación. "
                     "Contacte a soporte.")
        except Exception as e:
            st.error("No se pudo establecer con el servidor de anotación. "
                     "Contacte a soporte.")
        else:
            json_response = response.json()
            if response.status_code == status.HTTP_201_CREATED:
                st.success(
                    f'El dataset {st.session_state[f"{self.__class__.__name__}_dataset_name"]} versión {str(versions)} inició '
                    f"su publicación satisfactoriamente."
                )
                print(json_response)
            elif response.status_code == status.HTTP_412_PRECONDITION_FAILED:
                st.warning(
                    f'El dataset no se puede generar en este momento, hay anotaciones procesandose. Intente más tarde.'
                )
            else:
                st.error(
                    f'No se pudo publicar el dataset {st.session_state[f"{self.__class__.__name__}_dataset_name"]} versión {str(versions)}.'
                )
                print(f"Unexpected error during commit request {response}, {json_response}")
                return None

    def _render_content(self):
        # helper functions
        self.get_data()
        timezone = pytz.timezone("America/Mexico_City")
        st.header("Publicar dataset de entrenamiento")

        m = st.markdown(
            """
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
                               </style>""",
            unsafe_allow_html=True,
        )

        st.selectbox(
            "Indique el activo:",
            options=list(self.machines.keys()),
            key=f"{self.__class__.__name__}_machine",
            index=0,
        )

        tasks = self.tasks[st.session_state[f"{self.__class__.__name__}_machine"]]

        with st.form("commit"):
            st.selectbox(
                "Escoja un task:",
                options=tasks,
                key=f"{self.__class__.__name__}_task",
                index=0,
            )

            st.date_input(
                "Inserte un periodo:",
                key=f"{self.__class__.__name__}_date_range",
                value=(
                    datetime.datetime.today()
                    if "init_date" not in self.range_time
                    else self.range_time["start_date"],
                    datetime.datetime.today()
                    if "finish_date" not in self.range_time
                    else self.range_time["end_date"]
                ),
            )
            st.time_input(
                "Hora de inicio de la data:",
                key=f"{self.__class__.__name__}_start",
                value=datetime.datetime.now().astimezone(tz=timezone)
                    if "start_time" not in self.range_time
                    else self.range_time["start_time"],
            )
            st.time_input(
                "Hora de culminación de la data:",
                key=f"{self.__class__.__name__}_end",
                value=datetime.datetime.now().astimezone(tz=timezone)
                    if "end_time" not in self.range_time
                    else self.range_time["end_time"]
            )

            st.text_input(
                "Inserte nombre de dataset:",
                key=f"{self.__class__.__name__}_dataset_name",
            )

            st.text_input(
                "Inserte el nombre de la versión. Si quiere especificar más de una version, ingrese los enunciados separados por coma:",
                key=f"{self.__class__.__name__}_dataset_version",
            )
            st.form_submit_button("Publicar dataset", on_click=self._commit)
