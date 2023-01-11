"""
This module implements the MainAppComponent object which is the
object that contains the global state of the app and the main components:
- left sidebar
- Main View implementations
- Right Sidebar

The global state of the app is shared to the child components.
"""
from txp.common.utils.authentication_utils import AuthenticationInfo
from txp.web.core_components.app_component import AppComponent, AppState
from txp.web.core_components.sidebar import Sidebar
from txp.web.core_components.main_view import MainView
from txp.web.core_components.authentication import AuthenticationComponent
from txp.web.core_components.app_profiles import AppProfile
import streamlit as st
from typing import Dict
import logging
# TODO: This might be a problem. The logging configuration is being taken from `txp` package
from txp.common.config import settings
from txp.web.views import CommitView, EditConfigurationView, TrainingView, ManagementModelsView, PreAnnotateView

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class MainAppComponent(AppComponent):
    """The Main Application component. All the other components must be children of this component,
    directly or indirectly.

    - Any state with global context should be initialized here in this class:
        - Login information
        - Current selected profile
        - Current selected view

    This component has two direct kind of children:

        - The _sidebar_component, which is the left sidebar that acts as the "menu" of the app.

        - _main_active_components: Instances of the MainView that are available in the application,
            When new MainView's are added to the Application, a single instance of those views should be
            handled to this MainAppComponent at initialization time of the streamlit session for the app.
    """
    def __init__(self, default_profile: AppProfile = AppProfile.CONFIGURATION):
        super(MainAppComponent, self).__init__(
            component_key='app_layout'
        )
        # Children components
        self._sidebar_component: Sidebar = Sidebar()
        self._authentication_component: AuthenticationComponent = AuthenticationComponent()
        # A dict of MainView components, one of which will be rendered in the next streamlit run based
        # on the current state.
        self._main_active_components: Dict[str, MainView] = {}
        self._register_app_state(AppState())
        self._admin_views_created: bool = False

    def add_child_component(self, component: MainView, make_current: bool = False):
        """Adds the MainView component instance to the internal main active components.

        Args:
            component(MainView): A MainView component instance.
            make_current: True to set the current view to the passed component
        """
        if make_current:
            self.app_state.current_view = component.get_display_name()
            self.app_state.current_profile = component.get_associated_profile()
        self._main_active_components[component.get_display_name()] = component
        profile = component.get_associated_profile().get_display_value()
        self.app_state.views_for_profile[profile].append(component.get_display_name())

    def _render(self) -> None:
        if self.app_state.authentication_info.is_user_logged_in():

            if not self.app_state.project_model:
                progress_continer = st.empty()
                logging.info("Project Model data not downloaded. Donwloading project data.")
                with progress_continer.container():
                    st.text("Cargando información...☕")
                    progress = st.progress(0)
                    self._donwload_project_data(progress)
                progress_continer.empty()
                st.experimental_rerun()

            if self.app_state.authentication_info.user_role == AuthenticationInfo.UserRole.Admin \
                    and not self._admin_views_created:
                self.add_child_component(CommitView())
                self.add_child_component(ManagementModelsView())
                self.add_child_component(EditConfigurationView())
                self.add_child_component(TrainingView())
                self.add_child_component(PreAnnotateView())
                self._admin_views_created = True

            self._sidebar_component.render()
            main_view_to_render = self._main_active_components.get(self.app_state.current_view, None)

            if (not main_view_to_render or main_view_to_render.get_display_name() not
                    in self.app_state.views_for_profile[self.app_state.current_profile.get_display_value()]):
                st.warning("Vista no disponible")

            else:
                main_view_to_render.render()

        else:
            self._authentication_component.render()