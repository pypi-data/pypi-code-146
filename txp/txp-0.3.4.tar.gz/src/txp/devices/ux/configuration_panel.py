"""
This module defines the helper function to draw the configuration
panel in the browser.
"""
# =====================imports=====================================
import streamlit as st
import os
import gateway_mocking as mocking
from txp.devices.ux.remote_gateway_client import remote_gateway_client
from txp.devices.gateway_states_enums import *
import txp.devices.ux.ux_states_protocol as ux_states
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==================== Functions ==========================================
def _print_details(details: ux_states.UxDetails):
    if details.kind == ux_states.UxDetails.Kind.Warning:
        st.warning(details.message)

    elif details.kind == ux_states.UxDetails.Kind.Info:
        st.info(details.message)
    else:
        st.error(details.message)


def _render_logical_configuration():
    """Renders the logical configuration where called."""
    st.subheader("Máquinas")
    for machine in st.session_state.gateway_state.machines:
        exp = st.expander(machine.machine_id)
        exp.markdown(f"**Modelo**: {machine.model}")
        exp.markdown(f"**Fabricante**: {machine.manufacturer}")
        exp.markdown(f"**Dispositivos configurados:**")
        for edge_id in machine.edges_ids:
            exp.write(edge_id)

    st.subheader("Dispositivos Edge")
    for edge in st.session_state.gateway_state.edges:
        exp = st.expander(edge.logical_id)
        exp.markdown(f"**Dispositivo**: {edge.device_type}")
        exp.markdown(f"**Tipo de Edge**: {edge.device_kind}")
        exp.markdown(f"**Parámetros de configuración**:")
        exp.write(edge.edge_parameters)


def user_confirmed_settings_callback():
    """Callback to be called when the user confirms to proceed from
    ConfigurationValidation state to DevicePairing state"""
    gateway_state = st.session_state.gateway_state
    sent_state = ux_states.UxConfigurationValidationState(
        gateway_state.state, ConfigurationValidationStatus.UserConfirmedSettings,
        None, gateway_state.gateway_conf, gateway_state.machines, gateway_state.edges
    )
    remote_gateway_client.send_state_to_gateway(
        sent_state
    )
    log.info('Sending UxConfigurationValidation-UserConfirmedSettings to Gateway.')


def render_configuration_panel():
    """The General Panel is used to show Gateway general configuration information,
    and to server the UX in the initial states of the Gateway when configuration
    is required.

    Specifically, the general information shown in this panel is:
        - Gateway metadata such as serial and project ID.
        - Logical configuration of the Gateway divided in sections for:
            Machines, Edges (After receiving the configuration from cloud).

    Specifically, the UX shown in this panel is:
        - User input of initial files and initial values.
        - Info about the logical configuration receiving process.
        - Info about the configuration validation process.
    """
    gateway_state = st.session_state.gateway_state
    st.markdown("-------------")
    st.subheader("Configuración del Gateway")
    if not hasattr(gateway_state, 'gateway_conf'):
        st.markdown(f"**Serial**: {gateway_state.gateway_id}")
        st.markdown(f"**Registro**: {gateway_state.registry_id}")
    else:
        st.markdown(f"**Serial**: {gateway_state.gateway_conf.gateway_id}")
        st.markdown(f"**Registro**: {gateway_state.gateway_conf.registry_id}")

    # Here starts the logic for the current state to follow in the Configuration Panel

    """
    Configuration Panel - Startup State. 
    In this state, the UX should render the required input values until all of them 
    have been received. Specifically:
        - First: The Private Key certificate file of the Gateway.
        - In any order: Text inputs for:
            - Gateway Serial 
            - IoT Registry 
    """
    if isinstance(gateway_state, ux_states.UxStartupState):
        st.markdown("### Configurar información inicial")

        """
        This placeholder is used to show markdown messages dynamically in this 
        position, later on. 
        """
        st.session_state.startup_markdown_placeholder = st.empty()

        if gateway_state.details:
            _print_details(gateway_state.details)
            gateway_state.details = None  # Delete details to continue interaction

        if not gateway_state.private_key_received:
            st.session_state.private_key_file_uploader_placeholder = st.empty()
            uploadedfile = (
                st.session_state.private_key_file_uploader_placeholder.file_uploader(
                    label="Subir el archivo de clave privada del Gateway",
                    type=".pem",
                    help="El Gateway necesita configurar su clave privada",
                )
            )
            if uploadedfile is not None:
                with open(
                    os.path.abspath(settings.gateway.private_key_path), "wb"
                ) as f:
                    f.write(uploadedfile.getbuffer())
                    f.close()
                gateway_state.private_key_received = True
                st.session_state.private_key_file_uploader_placeholder.empty()
                del st.session_state.private_key_file_uploader_placeholder

        if gateway_state.private_key_received:
            if not gateway_state.gateway_serial_received:
                st.session_state.gateway_serial_input_placeholder = st.empty()
                gateway_serial = (
                    st.session_state.gateway_serial_input_placeholder.text_input(
                        label="Introduzca el serial del Gateway",
                        key="gateway_serial_input_text",
                        value="",
                    )
                )
                if gateway_serial != "":
                    # Set Mocking value. TODO: Remove when integrating.
                    mocking.gateway_id = gateway_serial
                    gateway_state.gateway_id = gateway_serial
                    gateway_state.gateway_serial_received = True
                    st.session_state.gateway_serial_input_placeholder.empty()
                    del st.session_state.gateway_serial_input_placeholder

            if not gateway_state.registry_name_received:
                st.session_state.registry_id_input_placeholder = st.empty()
                registry_name = st.session_state.registry_id_input_placeholder.text_input(
                    label="Introduzca el nombre del registro",
                    key="registry_name_input_text",
                    value="",
                    help="El nombre del registro en la nube en el cual está registrado el Gateway",
                )
                if registry_name != "":
                    mocking.registry_id = registry_name
                    gateway_state.registry_id = registry_name
                    gateway_state.registry_name_received = True
                    st.session_state.registry_id_input_placeholder.empty()
                    del st.session_state.registry_id_input_placeholder

            if not gateway_state.project_id_received:
                st.session_state.project_id_input_placeholder = st.empty()
                project_id = st.session_state.project_id_input_placeholder.text_input(
                    label="Introduzca el nombre del proyecto GCP",
                    key="registry_name_input_text",
                    value="",
                    help="El nombre del proyecto en GCP en la nube en el cual está registrado el Gateway",
                )
                if project_id != "":
                    gateway_state.project_id = project_id
                    gateway_state.project_id_received = True
                    st.session_state.project_id_input_placeholder.empty()
                    del st.session_state.project_id_input_placeholder

        with st.session_state.startup_markdown_placeholder.container():
            if gateway_state.private_key_received:
                st.markdown("Clave privada configurada :white_check_mark:")

            if gateway_state.gateway_serial_received:
                st.markdown("Serial configurado :white_check_mark:")

            if gateway_state.registry_name_received:
                st.markdown("Registro en la nube configurado :white_check_mark:")

            if gateway_state.project_id_received:
                st.markdown("ID del proyecto configurado :white_check_mark:")

        # Show that the information is being sent to the Gateway.
        # This step is real, it's currently integrated with the Gateway process.
        if (
            gateway_state.private_key_received
            and gateway_state.gateway_serial_received
            and gateway_state.registry_name_received
            and gateway_state.project_id_received
        ):
            new_state = ux_states.UxStartupState(
                gateway_state.state,
                StartupStatus.RequiredValuesReceived,
                None,
                gateway_state.gateway_id,
                gateway_state.registry_id,
                gateway_state.private_key_received,
                gateway_state.gateway_serial_received,
                gateway_state.registry_name_received,
                gateway_state.project_id_received,
                gateway_state.project_id
            )
            remote_gateway_client.send_state_to_gateway(new_state)
            st.info("La información está siendo procesada")

    # In configuration Reception, the Gateway will be waiting for the cloud messages.
    # It will send updates to the UxState about that progress.
    elif isinstance(gateway_state, ux_states.UxConfigurationReceptionState):
        if not gateway_state.all_received:
            st.markdown("-------------")
            st.session_state.startup_markdown_placeholder = st.empty()
            st.info(
                f"Recibiendo configuraciones remotas."
            )
            with st.session_state.startup_markdown_placeholder.container():
                if (
                    gateway_state.status
                    == ConfigurationReceptionStatus.EstablishCloudConnection
                ):
                    st.markdown("Estableciendo conexión con la nube:exclamation:")
                else:
                    st.markdown("Conexión con la nube establecida:white_check_mark:")

                if gateway_state.gateway_conf.machines_ids:
                    st.markdown("Configuración del Gateway recibida:white_check_mark:")
                else:
                    st.markdown("Esperando por configuración lógica :exclamation:")

                if gateway_state.machines:
                    st.markdown(
                        "Configuración de Máquinas recibidas :white_check_mark:"
                    )
                else:
                    st.markdown("Esperando por configuración de Máquinas :exclamation:")

                if gateway_state.edges:
                    st.markdown(
                        "Configuración de dispositivos Edge recibida :white_check_mark:"
                    )
                else:
                    st.markdown(
                        "Esperando por configuración de dispositivos Edge :exclamation:"
                    )

    # In the ConfigurationValidation state, the Gateway will be processing the received
    # logical configurations, and checking if there were previous configurations
    # and if those configurations are outdated
    elif isinstance(gateway_state, ux_states.UxConfigurationValidationState):
        st.info(f"Configuraciones recibidas.")
        _render_logical_configuration()

        # Rendering the button with a container. Doing so, it's possible
        # to clean the button while the gateway sends the new state, and avoid
        # a problematic interaction
        button_container = st.empty()
        pressed = button_container.button(
            "Continuar",
            key="continue_to_pairing_button",
            on_click=user_confirmed_settings_callback,
        )
        if pressed:
            button_container.info("Preparando emparejamiento") # Clears the button and shows the message

    else:  # In this case, Configuration states were passed an only shows the configured values
        _render_logical_configuration()

