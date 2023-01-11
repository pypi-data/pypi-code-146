"""
This module implements the left Sidebar for the layout of the application.
"""
from txp.web.core_components.app_component import AppComponent, AppState
from txp.web.core_components.app_profiles import AppProfile
from txp.web.resources.resources_management import ImageManagement
from typing import Dict, List, Callable
import streamlit as st
import logging
import os
# TODO: This might be a problem. The logging configuration is being taken from `txp` package
from txp.common.config import settings
log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class Sidebar(AppComponent):
    """The left Sidebar component for the layout of the application.

    This component is the `Main Menu` for the user to interact with.

    This component shows Menu widgets and updates the MainComponentApp state when
    those widgets change their state. This allows to the MainComponentApp to determine
    which MainView children components to render.
    """
    def __init__(self):
        """
        Args:
            _update_profile_callback: callback to be called when the profile widget
                change its value.

            _update_selected_view: callback to be called when the selected view change
                its value.
        """
        super(Sidebar, self).__init__(
            component_key='sidebar'
        )

    @classmethod
    def _register_app_state(cls, state: AppState) -> None:
        raise NotImplemented

    def _current_profile_change(self):
        new_profile = st.session_state["current_profile_selectbox"]
        self.app_state.current_profile = AppProfile(new_profile)
        log.debug(f'Current profile changed to: {new_profile}')

    def _current_view_change(self):
        new_view = st.session_state["current_view_radio"]
        self.app_state.current_view = new_view
        log.debug(f'Current view changed to: {new_view}')

    def _render(self) -> None:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        st.sidebar.image(f'{current_directory}/../resources/images/txp_logo_1.png', output_format="PNG")

        # st.sidebar.selectbox(
        #     label="Perfil Actual",
        #     options=AppProfile.get_display_values(),
        #     key="current_profile_selectbox",
        #     on_change=self._current_profile_change,
        # )

        profile = "Resumen"
        views_profile = self.app_state.views_for_profile[profile]



        last_radio_value = st.sidebar.radio(
            label="Opciones Disponibles",
            options=views_profile,
            key="current_view_radio"
        )

        self._current_view_change()  # Updates last radio value to cover all cases of interaction
