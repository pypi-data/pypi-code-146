"""
This module implements the Generic common AppComponent interface
for all the components shown in the application:
    - Main App component
    - Sidebar Component (left)
    - Main View Component
"""
import abc
import logging
import threading
from typing import Dict, List, Union

import txp.common.utils.firestore_utils
from txp.common.utils.firestore_utils import ProjectModel
from txp.web.core_components.app_profiles import AppProfile
from txp.common.utils.authentication_utils import AuthenticationInfo
from txp.web.core_components.states_and_events_report import *
from collections import defaultdict
from txp.web.resources.resources_management import ImageManagement, VideoManagement
from txp.web.controllers.conveyors_dashboard import TransportationLine
import pandas as pd
import markdown

# TODO: This might be a problem. The logging configuration is being taken from `txp` package
from txp.common.config import settings

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


@dataclasses.dataclass
class AppState:
    current_profile: AppProfile = None
    current_view: str = ""
    views_for_profile: Dict[str, List[str]] = dataclasses.field(default_factory=dict)
    authentication_info: AuthenticationInfo = dataclasses.field(
        default_factory=AuthenticationInfo
    )
    condition_report: ConditionReport = dataclasses.field(
        default_factory=ConditionReport
    )
    event_report: EventReport = dataclasses.field(default_factory=EventReport)
    project_model: ProjectModel = None
    conveyors_dashboard: Dict[str, TransportationLine] = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        self.views_for_profile = defaultdict(list)

        # background threaded download information
        self._background_thread: threading.Thread = None
        self._stop_background_thread_event: threading.Event = threading.Event()

    def donwload_project_data(self, tenant_id, progress_bar_streamlit) -> None:
        """Donwloads the project model snapshot from Firestore and stores it
        in the AppState singleton."""
        db = txp.common.utils.firestore_utils.get_authenticated_client(
            self.authentication_info.role_service_account_credentials
        )
        progress_bar_streamlit.progress(10)
        self.project_model = txp.common.utils.firestore_utils.get_current_project_model(
            db, tenant_id
        )
        progress_bar_streamlit.progress(50)

        for machines_grp in self.project_model.machines_groups_table:
            progress_bar_streamlit.progress(80)
            self.conveyors_dashboard[machines_grp] = TransportationLine(
                machines_grp,
                len(self.project_model.machines_groups_table[machines_grp]['machines']),
                self.project_model,
                self.authentication_info.role_service_account_credentials,
            )

    def start_background_download(self):
        log.info(f"Starting background download of information")
        self._stop_background_thread_event.clear()
        st.session_state.download_thread = threading.Thread(
            name='pull_data_thread',
            target=self._donwload_conveyors_data,
            daemon=True
        )
        st.script_run_context.add_script_run_ctx(st.session_state.download_thread)
        st.session_state.download_thread.start()

    def stop_background_download(self):
        log.info(f"Requesting to stop background download of information")
        self._stop_background_thread_event.set()

    def background_download_active(self) -> bool:
        return st.session_state.download_thread.is_alive()

    def _donwload_conveyors_data(self):
        for machines_grp, transportation_line in self.conveyors_dashboard.items():
            if self._stop_background_thread_event.is_set():
                break

            log.info(f"Download information for {machines_grp}")
            transportation_line._pull_information_from_db()

        log.info("Stopped background download of information")


@dataclasses.dataclass
class GridCell:
    """A GridCell currently can hold:
        - Markdown

    In theory, anything that can be injected in HTML can be shown in the grid.
    """

    css_class: str
    grid_column_start: int
    grid_column_end: int
    grid_row_start: int
    grid_row_end: int
    width: str = "auto"

    def __post_init__(self):
        self.inner_html = ""

    def _to_style(self) -> str:
        """Returns the grid related css style for this class"""
        return f"""
        .{self.css_class} {{
            grid-column-start: {self.grid_column_start};
            grid-column-end: {self.grid_column_end};
            grid-row-start: {self.grid_row_start};
            grid-row-end: {self.grid_row_end};
        }}
        """

    def text(self, text: str = ""):
        """Renders text in HTML as plain text"""
        self.inner_html = text

    def markdown(self, text: str = ""):
        self.inner_html = markdown.markdown(
            text, extensions=["tables"]
        )  # tables support

    def image(self, source, alt="Image", width=100, height=100):
        """
        Render an HTML img object.
        """
        self.inner_html = (
            f"""<div><img src={source} width={width} height={height} alt={alt}></div>"""
        )

    def _to_html(self):
        return f"""<div class="box {self.css_class}">{self.inner_html}</div>"""


@dataclasses.dataclass
class Grid:
    """A class to handle a CSS Grid

    The idea for this implementation was taken from here:
        https://github.com/MarcSkovMadsen/awesome-streamlit/blob/be454e29c35a9a1a760b1737a5176a47f4f9717b/gallery/layout_experiments/app.py#L79

    This grid can render not only markdown, but other types of web content.
    """

    template_column: str
    gap_between_columns: int
    background_color: str
    color: str
    font_size: str
    tables_font_size: str
    cells: List

    def __enter__(self):
        """__enter__ method to allow `with` statement"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """After a `with` statement, writes the styles to the html"""
        st.markdown(self._get_grid_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_html(), unsafe_allow_html=True)

    def _get_grid_style(self):
        return f"""
        <style>
            .wrapper {{
            display: grid;
            grid-template-columns: {self.template_column};
            grid-gap: {self.gap_between_columns};
            background-color: white;
            color: {self.color};
            width: auto;
            }}
            .box {{
            min-height: 20px
            background-color: white;
            color: black;
            border-radius: 0px;
            padding: 10px;
            margin-top: 0px;
            margin-left: 5px;
            margin-right: 5px;
            margin-bottom: 0px,
            font-size: {self.font_size};
            }}
            table {{
                color: {self.color};
                font-size: {self.tables_font_size};
                width: 100%;
            }}
            /* content-table css class is inserted by DataFrame.to_html() in Card class */
            .content-table thead tr {{
            background-color: #313131;
            color: #ffffff;
            font-weight: bold;
            }}
            .content-table th,
            .content-table td {{
            text-align: center;
            }}
            .content-table tbody tr {{
            border-bottom: 1px solid #d1c9ca;
            }}
            .centrado {{
            width:100%;
            max-width:600px;
            }}
            
        </style>
        """

    def _get_cells_style(self):
        return (
            "<style>"
            + "\n".join([cell._to_style() for cell in self.cells])
            + "</style>"
        )

    def _get_cells_html(self):
        return (
            '<div class="wrapper">'
            + "\n".join([cell._to_html() for cell in self.cells])
            + "</div>"
        )

    def add_cell(
        self,
        css_class: str,
        grid_column_start,
        grid_column_end,
        grid_row_start,
        grid_row_end,
    ):
        cell = GridCell(
            css_class=css_class,
            grid_column_start=grid_column_start,
            grid_column_end=grid_column_end,
            grid_row_start=grid_row_start,
            grid_row_end=grid_row_end,
        )
        self.cells.append(cell)
        return cell


@dataclasses.dataclass
class Card:
    """A class for standardizing the view composition.
    Parameters:
        card_row(int): row number of the view where the card will be painted.
        card_column_end(int): column number of the view where the card will end.
        card_subheader(str): card subheader.
        labels(list): list of labels for the content table.
        content(dict): dict of items for the content table.
        vertical_style(boolean): if the value is True, the table will have
                the labels in the index.
    """

    def __init__(
        self,
        card_row: int,
        card_column_start: int,
        card_column_end: int,
        card_subheader: str,
        content: Union[str, dict],
        labels=[],
        vertical_style=False,
    ):
        self.row = card_row
        self.column_start = card_column_start
        self.column_end = card_column_end
        self.card_subheader = card_subheader
        self.content = content

        if type(self.content) == dict:
            self.table = self._get_table_component(labels, self.content, vertical_style)

    def _get_table_component(
        self,
        labels,
        content,
        vertical_style,
    ):
        """Method to build the table of contents with the labels and items.
        Parameters:
                labels(list): list of column names for the content table.
                content(dict): dict of items for de content table.
                vertical_style(boolean): if the value is True, the table will have
                the labels in the index.
        Returns:
            content table for card.
        """
        df = pd.DataFrame(content)
        df.columns = labels

        if vertical_style:
            df_t = df.transpose()
            df_t.columns = [""] * len(df_t.columns)
            table = df_t.to_html(
                classes="content-table",
                escape=False,
            )
            return f"""
{table}"""
        else:
            table = df.to_html(classes="content-table", escape=False, index=False)
            return f"""
{table}"""

    def _build_card(self):
        """Method to build a card.
        Returns:
              f-string with components of card."""

        if type(self.content) == dict:
            content = f"""{self.table}"""

        else:
            content = self.content

        subheader_card = f"""##### {self.card_subheader}  \n"""
        card = subheader_card + content
        return card


class AppComponent(abc.ABC):
    def __init__(self, component_key: str):
        """
        Args:
            component_key(str): The component key to be used in logging and as
                key in the streamlit state if necessary.
        """
        self._component_key = component_key
        self._components: Dict[str, AppComponent] = {}
        st.session_state[
            self._component_key
        ] = self  # adds the component to streamlit state

        # Load from the secrets all the useful parameters for the components internal workings.
        self._tenant_id: str = st.secrets["tenant_id"]
        self._bigquery_dataset: str = st.secrets['big_query_dataset']
        self._events_dataset: str = st.secrets["events_dataset"]
        self._states_dataset: str = st.secrets["states_dataset"]
        self._days_report: int = st.secrets["days_report"]
        self._edge_states_sp = {
            "Disconnected": "Desconectado",
            "Connected": "Conectado",
            "Sampling": "Recolectando datos",
            "Recovering": "Recuperandose"
        }
        self._asset_states_sp = {
            "OPTIMAL": "Óptima",
            "GOOD": "Buena",
            "UNDEFINED": "Indefinida",
            "OPERATIONAL": "Operativa",
            "CRITICAL": "Crítica",
        }

    # App Global State handling methods
    @property
    def app_state(self) -> AppState:
        """Gets the global state of the application"""
        return st.session_state["app_state"]

    @classmethod
    def _register_app_state(cls, state: AppState) -> None:
        st.session_state["app_state"] = state

    def render(self) -> None:
        """Renders this component next in the streamlit app run."""
        log.debug(f"Calling render of component {self._component_key}")
        self._render()

    @abc.abstractmethod
    def _render(self) -> None:
        """This method implementation defines the visual drawing of the component
        in the browser, in a sequential way.

        When this method is called, streamlit will render according to the instructions
        declared in the method.
        """
        pass

    def render_grid(
        self,
        template_column: str = "1 1 1",
        gap_between_columns="5px",
        background_color="rgb(255, 255, 255)",
        color="black",
        font_size="125%",
        tables_font_size="15px",
    ) -> Grid:
        """Returns a Grid to render a grid of cells."""
        return Grid(
            template_column,
            gap_between_columns,
            background_color,
            color,
            font_size,
            tables_font_size,
            [],
        )

    def render_card(self, cards: list):
        """Method to paint one or more cards in a row view.
        Parameters:
                cards (list): list of cards.

        Returns:
                row of view with one or more cards."""

        with self.render_grid() as grid:
            for index, card in enumerate(cards):
                grid.add_cell(
                    css_class=f"card_{index}",
                    grid_column_start=card.column_start,
                    grid_column_end=card.column_end,
                    grid_row_start=card.row,
                    grid_row_end=card.row,
                ).markdown(f"""{card._build_card()}"""),

        st.markdown("***")

    def image_html(self, file_name, responsive=False, width=60):
        """
        returns an image html tag from a file_name
        """
        if responsive:
            resources = ImageManagement(file_name)
            html_responsive_resource = resources.get_local_html_responsive_resource(
                width
            )
            return html_responsive_resource
        else:
            resources = ImageManagement(file_name)
            html_resource = resources.get_local_html_resource(width)
            return html_resource

    def video_html(self, file_name, width):
        """
        returns an video html tag from a file_name
        """
        resources = VideoManagement(file_name)
        html_resource = resources.get_local_html_resource(width)
        return html_resource

    def image_html_and_text(self, file_name, text, width=60):
        """
        returns an image html tag from a file_name and includes the possibility of add text
        """
        img = self.image_html(file_name, width)
        return img + f"""<br>{text}"""

    def formatting_readable_strings(self, input):
        """
        uses the str.replace() to avoid the underscore in names
        """
        changed_str = input.replace("_", " ")
        return changed_str

    def formatting_strings(self, input):
        """
        uses the str.replace() to returns the underscore in names
        """
        changed_str = input.replace(" ", "_")
        return changed_str

    def _donwload_project_data(self, progress_bar) -> None:
        """Donwloads the project model snapshot from Firestore and stores it
        in the AppState singleton."""
        self.app_state.donwload_project_data(self._tenant_id, progress_bar)
