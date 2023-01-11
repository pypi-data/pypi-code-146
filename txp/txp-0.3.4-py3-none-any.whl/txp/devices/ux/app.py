"""
This module currently defines the mocked streamlit application
for a Gateway.

The application view is organized in "Panels". The user can change
between Panels by using the Sidebar and the radio button for each
Panel.
When a Panel is selected, then the main view of the webpage will
be composed of the elements defined to be render in that Panel and
in the current UxState.

The current UxState is always available in the streamlit session state.

Each Panel is rendered by a helper function defined in this script, and inside
that function, the appropriate view is rendered according to the UxState.
"""
# =====================import==================================
import streamlit as st
from typing import List

import txp.devices.ux.remote_gateway_client
from txp.devices.gateway_states_enums import *
from txp.devices.ux.configuration_panel import render_configuration_panel
from txp.devices.ux.devices_paring_panel import render_devices_pairing
from txp.devices.ux.package_collection_panel import render_package_collection
from txp.devices.ux.render_fatal_error import render_fatal_error
import txp.devices.ux.ux_states_protocol as ux_states
from txp.devices.ux.remote_gateway_client import remote_gateway_client
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

# =====================Data==================================

# Buttons labels for the Sidebar views
CONFIGURATION_SIDEBAR_BUTTON_LABEL = "Configuración"
DEVICE_PAIRING_SIDEBAR_BUTTON_LABEL = "Emparejar Dispositivos"
PACKAGE_COLLECTION_SIDEBAR_BUTTON_LABEL = "Recolección de Paquetes"

BUTTON_EMOJI_DICT = {
    CONFIGURATION_SIDEBAR_BUTTON_LABEL: "",
    DEVICE_PAIRING_SIDEBAR_BUTTON_LABEL: "",
    PACKAGE_COLLECTION_SIDEBAR_BUTTON_LABEL: ""
}

# =====================Initialize app==================================
def initialize_app():
    """Initializes the app in the first run.

    TODO. When integration with the Gateway, here the initial state/ recovered state
        should be assigned.
    """

    if "initialized" not in st.session_state:
        st.session_state.gateway_state = (
            remote_gateway_client.last_known_state
        )
        remote_gateway_client.start_refresh_loop()

        # Flag to track the sidebar index for the default radio button
        st.session_state.sidebar_radio_index = 0
        st.session_state.configuration_view_first_time = True
        st.session_state.devices_pairing_view_first_time = True
        st.session_state.package_collection_first_time = True

        st.session_state.initialized = True


# ==================== Sidebar ==========================================
def render_sidebar():
    """Render the sidebar of the application. The sidebar allows to change
    between Panels."""
    gateway_state = st.session_state.gateway_state

    # UX Valid views based on the current state.
    # The list of Ux Valid Views is the list of selectable views to show in the sidebar.
    # By design, if a Gateway production process has an error, it'll be replaced.
    # Then, it's safe to add valid views based on the CURRENT state.
    ux_valid_views: List[str] = []

    if isinstance(
        gateway_state,
        (
            ux_states.UxStartupState,
            ux_states.UxConfigurationReceptionState,
            ux_states.UxConfigurationValidationState,
        ),
    ):
        ux_valid_views.append(CONFIGURATION_SIDEBAR_BUTTON_LABEL)
        BUTTON_EMOJI_DICT[CONFIGURATION_SIDEBAR_BUTTON_LABEL] = '⬅️'
        if st.session_state.configuration_view_first_time:
            st.session_state.sidebar_radio_index = 0
            st.session_state.configuration_view_first_time = False

    elif isinstance(gateway_state, ux_states.UxDevicePairingState):
        ux_valid_views.extend(
            [CONFIGURATION_SIDEBAR_BUTTON_LABEL, DEVICE_PAIRING_SIDEBAR_BUTTON_LABEL]
        )
        BUTTON_EMOJI_DICT[CONFIGURATION_SIDEBAR_BUTTON_LABEL] = '✅'
        BUTTON_EMOJI_DICT[DEVICE_PAIRING_SIDEBAR_BUTTON_LABEL] = '⬅️'
        if st.session_state.devices_pairing_view_first_time:
            st.session_state.sidebar_radio_index = 1
            st.session_state.devices_pairing_view_first_time = False

    elif isinstance(gateway_state,
                    (ux_states.UxReadyState, ux_states.UxSamplingState, ux_states.UxPreparingDevicesState)):
        ux_valid_views.extend(
            [
                CONFIGURATION_SIDEBAR_BUTTON_LABEL,
                DEVICE_PAIRING_SIDEBAR_BUTTON_LABEL,
                PACKAGE_COLLECTION_SIDEBAR_BUTTON_LABEL,
            ]
        )
        BUTTON_EMOJI_DICT[CONFIGURATION_SIDEBAR_BUTTON_LABEL] = '✅'
        BUTTON_EMOJI_DICT[DEVICE_PAIRING_SIDEBAR_BUTTON_LABEL] = '✅'
        BUTTON_EMOJI_DICT[PACKAGE_COLLECTION_SIDEBAR_BUTTON_LABEL] = '⬅️'
        if st.session_state.package_collection_first_time:
            st.session_state.sidebar_radio_index = 2
            st.session_state.devices_pairing_view_first_time = False

    st.sidebar.subheader("Estado del Gateway")
    if gateway_state.state == GatewayStates.Ready:
        st.sidebar.markdown(f"{gateway_state.state}-{str(gateway_state.status)}")
    else:
        st.sidebar.markdown(f"{gateway_state.state}")
    st.sidebar.markdown("---------------")

    st.sidebar.markdown("**Pasos**")

    st.sidebar.radio(
        label="Seleccionar Panel", options=ux_valid_views, key="sidebar_panel_radio",
        format_func=lambda label: label + ' ' + BUTTON_EMOJI_DICT[label],
        index=st.session_state.sidebar_radio_index,
    )

# =====================App declarative flow==================================

# This snippet of html will hide the streamlit burguer button
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

initialize_app()
render_sidebar()

if st.session_state.gateway_state.state == GatewayStates.Error:
    if st.session_state.gateway_state.status == GatewayErrorStatus.ProductionNotCompleted:
        render_fatal_error()

elif st.session_state.sidebar_panel_radio == "Configuración":
    render_configuration_panel()

elif st.session_state.sidebar_panel_radio == "Emparejar Dispositivos":
    render_devices_pairing()

elif st.session_state.sidebar_panel_radio == "Recolección de Paquetes":
    render_package_collection()
