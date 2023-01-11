"""
This module implements the MainView for the layout of the application.
The main view is composed of the view area and the submenu on the right.
"""
from txp.web.core_components.app_component import AppComponent, AppState
from txp.web.core_components.app_profiles import AppProfile
import abc
from typing import Dict
import streamlit as st


class MainView(AppComponent):
    """The MainView component for the application.

    A MainView represents the View for one selected panel.
    For example, some views are:
        - Under 'Resumen' profile, the 'Telemetry Health' view.
        - Under 'Resumen' profile, the 'Devices Health' view.

    Each MainView is composed of two columns:
        1) The content area column: Where the content is actually displayed. It's the wider section on screen.
        2) The submenu area column: The submenu shown on the Right hand side inside a smaller column.

    The _render method is a provided template which renders both columns on each streamlit rerun.
    Concrete implementations should be provided by child classes.
    """
    def __init__(self, component_key: str):
        super(MainView, self).__init__(
            component_key=component_key
        )
        self._submenu_state: Dict = self._build_submenu_state()
        self._content_state: Dict = self._build_content_state()

    @classmethod
    def _register_app_state(cls, state: AppState) -> None:
        raise NotImplemented

    @abc.abstractmethod
    def get_associated_profile(self) -> AppProfile:
        pass

    @abc.abstractmethod
    def _build_submenu_state(self) -> Dict:
        pass

    @abc.abstractmethod
    def _build_content_state(self) -> Dict:
        pass

    @abc.abstractmethod
    def _render_content(self) -> None:
        pass

    @abc.abstractmethod
    def _render_submenu(self) -> None:
        pass

    @classmethod
    @abc.abstractmethod
    def get_display_name(cls) -> str:
        """Returns the human readable name for this view, to be shown in the Menu of the application."""
        pass

    def implements_submenu(self) -> bool:
        """Returns True if the view will use a sidebar rendering based on
        streamlit columns."""
        pass

    def _render(self) -> None:
        if self.implements_submenu():
            main_view_col, submenu_col = st.columns([.75, .25])
            with main_view_col:
                self._render_content()
            with submenu_col:
                self._render_submenu()

        else:
            self._render_content()
