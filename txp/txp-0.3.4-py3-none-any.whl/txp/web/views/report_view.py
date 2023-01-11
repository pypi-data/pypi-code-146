from txp.web.core_components.main_view import MainView
from txp.web.core_components.app_profiles import AppProfile
import streamlit as st
from txp.common.utils import reports_utils, bigquery_utils, firestore_utils
from txp.common.reports.forecasting import *
from txp.common.reports.transitions import *
from txp.common.reports.transitions_lines import *
from txp.common.reports.anomaly_detection import *
from txp.common.reports.distribution import *

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class ReportView(MainView):
    """The Report View"""

    def __init__(self):
        super(ReportView, self).__init__(component_key="report_view")
        self.data = None
        self.asset = None
        self.sections = None
        self.bigquery_db = None
        self.firestore_db = None
        self.current_machine = None
        self.current_selected_assets = None
        self.current_machines_groups = None

        self._report_type_selectbox_key: str = "report_type_sb"
        self._default_value_report = (
            f"Sin registro en los últimos {self._days_report} días"
        )

        self.visualization = None
        self.images = {
            "OPTIMAL": self.image_html('optimal_condition.jpg', width=15),
            "GOOD": self.image_html('good_condition.jpg', width=15),
            "OPERATIVE": self.image_html('operational_condition.jpg', width=15),
            "CRITICAL": self.image_html('unstable_condition.jpg', width=15),
        }

    def get_associated_profile(self) -> AppProfile:
        return AppProfile.RESUMEN

    def implements_submenu(self) -> bool:
        return True

    @classmethod
    def get_display_name(cls) -> str:
        return "Reporte de estadísticas"

    def _build_submenu_state(self) -> Dict:
        return {}

    def _build_content_state(self) -> Dict:
        return {}

    def _formatted_data(self, data):
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

    def get_data(self):
        if self.data is None:
            self.bigquery_db = bigquery_utils.get_authenticated_client(
                self.app_state.authentication_info.role_service_account_credentials
            )
            self.firestore_db = firestore_utils.get_authenticated_client(
                self.app_state.authentication_info.role_service_account_credentials
            )

            self.data = self._formatted_data(self.app_state.project_model)
            machines = list(self.data["machines"].keys())
            self.current_selected_assets = machines
            machines_groups = list(self.data["machines_groups"].keys())
            self.current_machines_groups = machines_groups[0]
            self.asset = machines[0]
            tenant_doc = firestore_utils.pull_tenant_doc(self.firestore_db, self._tenant_id).to_dict()
            self.sections_config = tenant_doc["sections"]

            self._query_reports()


    def _asset_section_config(self):
        for report_id in self.sections.keys():
            for time in self.sections[report_id].keys():
                if time in self.sections[report_id]:
                    for section in self.sections[report_id][time]:
                        section['asset'] = self.sections_config[section['section_id']]['parameters']['assets']

    def _query_reports(self):
        timezone = pytz.timezone("America/Mexico_City")
        now = datetime.datetime.now(tz=timezone)
        self.end_datetime = datetime.datetime.strftime(now.astimezone(pytz.utc), settings.time.datetime_zoned_format)
        delta = datetime.timedelta(days=15)

        self.reports = reports_utils.get_available_reports_within_interval(
            self.firestore_db,
            self.bigquery_db,
            'tranxpert-mvp.reports.sections',
            self._tenant_id,
            datetime.datetime.strptime(
                self.end_datetime,
                settings.time.datetime_zoned_format
            ) - delta,
            datetime.datetime.strptime(
                self.end_datetime,
                settings.time.datetime_zoned_format
            ),
        )
        if self.reports:
             self.sections = {}
             for id, values in self.reports.items():
                 report_sections = {}
                 for value in values:
                     sections = reports_utils.get_report_sections(
                         self.firestore_db,
                         self.bigquery_db,
                         'tranxpert-mvp.reports.sections',
                         self._tenant_id,
                         id,
                         datetime.datetime.strptime(value['start'], settings.time.datetime_zoned_format),
                         datetime.datetime.strptime(value['end'], settings.time.datetime_zoned_format),
                     )
                     if sections:
                         time_value = datetime.datetime.strptime(value['start'], settings.time.datetime_zoned_format)
                         new_timezone = time_value.astimezone(timezone)
                         report_sections[datetime.datetime.strftime(new_timezone, settings.time.datetime_zoned_format)] = sections
                 self.sections.update({id: report_sections})
             self._asset_section_config()
             report_ids = list(self.sections.keys())
             self.current_report = report_ids[0]
             report_types = list(self.sections[self.current_report].keys())
             self.current_report_type = report_types[0]

        else:
             self.current_report = None


    def utc_timestamp_to_local_datetime(self, timestamp):
        timezone = pytz.timezone("America/Mexico_City")
        date_time = pd.to_datetime(timestamp, utc=True)
        new_timezone = date_time.astimezone(timezone)
        return new_timezone

    def _update_report(self):
        if self.reports:
            self.current_report = st.session_state["report"]
            report_types = list(self.sections[self.current_report].keys())
            self.current_report_type = report_types[0]
        else:
            self.current_report = None

    def _update_report_type(self):
        if self.reports:
            self.current_report_type = st.session_state["report_type"]
        else:
            self.current_report = None

    def _update_asset(self):
        self.asset = st.session_state["asset"]
        self._update_report()

    def report(self):
        distribution_row = st.empty()
        transitions_row = st.empty()
        transitions_lines_row = st.empty()
        anomaly_row = st.empty()
        forecasting_row = st.empty()

        if any(self.asset in section['asset'] for section in self.sections[self.current_report][self.current_report_type]):
            for section in self.sections[self.current_report][self.current_report_type]:
                if section['type'] == StatesDistribution.__name__:
                    sc = StatesDistribution.load(section)
                    fig = sc.get_dynamic_plot()
                    st.plotly_chart(fig, use_container_width=True)

                elif section['type'] == StatesTransitions.__name__:
                    sc = StatesTransitions.load(section)
                    fig = sc.get_dynamic_plot()
                    st.plotly_chart(fig, use_container_width=True)

                elif section['type'] == StatesTransitionsLines.__name__:
                    pass
                    # sc = StatesTransitionsLines.load(section)
                    # fig = sc.get_dynamic_plot()
                    # st.plotly_chart(fig, use_container_width=True)

                elif section['type'] == AnomalyDetectionStates.__name__:
                    sc = AnomalyDetectionStates.load(section)
                    fig = sc.get_dynamic_plot()
                    st.plotly_chart(fig, use_container_width=True)

                elif section['type'] == StatesForecasting.__name__:
                    sc = StatesForecasting.load(section)
                    fig = sc.get_dynamic_plot()
                    st.plotly_chart(fig, use_container_width=True)

                elif section['type'] == AnomalyDetectionRawData.__name__:
                    sc = AnomalyDetectionRawData.load(section)
                    fig = sc.get_dynamic_plot()
                    st.plotly_chart(fig, use_container_width=True)

                elif section['type'] == RawDataForecasting.__name__:
                    sc = RawDataForecasting.load(section)
                    fig = sc.get_dynamic_plot()
                    st.plotly_chart(fig,use_container_width=True)

                elif section['type'] == EventsDistribution.__name__:
                    sc = EventsDistribution.load(section)
                    fig = sc.get_dynamic_plot()
                    st.plotly_chart(fig, use_container_width=True)

                elif section['type'] == EventsTransitions.__name__:
                    sc = EventsTransitions.load(section)
                    fig = sc.get_dynamic_plot()
                    st.plotly_chart(fig, use_container_width=True)

                elif section['type'] == EventsTransitionsLines.__name__:
                    sc = EventsTransitionsLines.load(section)
                    fig = sc.get_dynamic_plot()
                    st.plotly_chart(fig, use_container_width=True)

                elif section['type'] == EventsForecasting.__name__:
                    sc = EventsForecasting.load(section)
                    fig = sc.get_dynamic_plot()
                    st.plotly_chart(fig, use_container_width=True)

                elif section['type'] == AnomalyDetectionEvents.__name__:
                    sc = AnomalyDetectionEvents.load(section)
                    fig = sc.get_dynamic_plot()
                    st.plotly_chart(fig, use_container_width=True)

        else:
            st.info('No hay reporte de este activo.')


    def extract_percentages_from_distribution_section(self, distribution_fig):
        total = distribution_fig.data[0]['values'].sum()
        percentages = {}
        for label, value in zip(distribution_fig.data[0]['labels'], distribution_fig.data[0]['values']):
            if label == 'Operative':
                label = 'OPERATIVE'
            elif label == 'Good':
                label = 'GOOD'
            else:
                pass
            percentages[label] = value / total * 100
        return percentages

    def _render_submenu(self) -> None:
        m = st.markdown("""
                        <style>
                        div.stButton > button:first-child {
                        color: #0000CD;
                        box-sizing: 5%;
                        height: 2em;
                        width: 100%;
                        font-size:18px;
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
                        </style>""", unsafe_allow_html=True)

        st.selectbox(
            label="Indique el activo:",
            options=self.current_selected_assets,
            index=0,
            key='asset',
            on_change=self._update_asset,
        )

        if self.reports:
            st.selectbox(
                label="Seleccione el reporte que desee visualizar:",
                options=self.sections.keys(),
                index=0,
                key='report',
                on_change=self._update_report,
            )
            st.selectbox(
                label="Seleccione la fecha:",
                options=self.sections[self.current_report].keys(),
                index=0,
                key='report_type',
                on_change=self._update_report_type,
            )

        st.button('Actualizar', on_click=self._query_reports)

        st.markdown('***')
        if self.reports:
            for section in self.sections[self.current_report][self.current_report_type]:
                if (
                        self.asset in section['asset']
                        and section['type'] == StatesDistribution.__name__
                ):
                    sc = StatesDistribution.load(section)
                    fig = sc.get_dynamic_plot()
                    percentages = self.extract_percentages_from_distribution_section(fig)
                    for key, percentage in percentages.items():
                        percentage_format = "{0:.1f}".format(percentage)
                        st.markdown(self.images[key], unsafe_allow_html=True)
                        st.metric(
                            label=key,
                            value=f'{percentage_format}%'
                        )
            else:
                pass

    def _render_content(self) -> None:
        if self.data is None:
            self.get_data()
        st.header(f"Reporte de {self.asset}")

        if self.current_report:
            self.report()
        else:
            st.info('Sin reporte.')