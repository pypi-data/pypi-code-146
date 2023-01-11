"""
This module defines the helper function to draw the package collection
panel in the browser.
"""
# =====================imports=============================================
import streamlit as st
import gateway_mocking as mocking
from txp.devices.gateway_states_enums import *
from txp.common.config import settings
import txp.devices.ux.ux_states_protocol as ux_states
from txp.devices.ux.configuration_panel import render_configuration_panel
import pandas as pd


# ==================== Functions ==========================================
def _print_details(details: ux_states.UxDetails):
    if details.kind == ux_states.UxDetails.Kind.Warning:
        st.warning(details.message)

    elif details.kind == ux_states.UxDetails.Kind.Info:
        st.info(details.message)
    else:
        st.error(details.message)


def _print_table_of_devices_states():
    st.markdown("**Tabla de estado de dispositivos**")
    table = pd.DataFrame(columns=["Serial", "Estado"])
    table.set_index("Serial", inplace=True)
    for serial, state in st.session_state.gateway_state.devices_connection_table.items():
        table.loc[serial] = str(state)
    st.table(table)


def render_package_collection():
    """The Package Collection panel is used to show stats about
    package collection stats.
    """
    st.markdown("### Recolección de Paquetes")
    gateway_state = st.session_state.gateway_state

    if isinstance(gateway_state, (ux_states.UxReadyState, ux_states.UxSamplingState)):
        st.markdown(
            f"**Total de Paquetes recolectados**: {gateway_state.collected_packages}"
        )
        st.markdown(f"**Total de Paquetes enviados:** {gateway_state.sent_packages}")

        _print_table_of_devices_states()

        st.markdown("**Paquetes recolectados por dispositivos**")
        table = pd.DataFrame(columns=["Serial", "Paquetes"])
        table.set_index("Serial", inplace=True)
        for edge in gateway_state.edges:
            table.loc[edge.logical_id] = gateway_state.packages_received_by_edge[
                edge.logical_id
            ]

        st.write(table)

        _print_details(gateway_state.details)

    if isinstance(gateway_state, ux_states.UxPreparingDevicesState):
        _print_details(gateway_state.details)
        _print_table_of_devices_states()

