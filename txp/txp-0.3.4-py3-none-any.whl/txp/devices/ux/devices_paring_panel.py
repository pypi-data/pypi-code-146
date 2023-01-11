"""
This module defines the helper function to draw the devices pairing
panel in the browser.
"""
# =====================imports=============================================
import streamlit as st
import time
from txp.devices.ux.remote_gateway_client import remote_gateway_client
from txp.devices.gateway_states_enums import *
import txp.devices.ux.ux_states_protocol as ux_states
from txp.common.edge.common import EdgeDescriptor
import matplotlib.pyplot as plt
from typing import List, Set, Tuple
import cv2
import numpy as np
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# ==================== constant data ==========================================
_machines_ids: List[str] = []
_captured_virtual_pos: Set[str] = set()

# ==================== Helper functions ==========================================
def _get_captured_image(image_bytes):
    """Returns the matplotlib figure to render an image that is in memory a bytes"""
    image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image, flags=1)
    image = image[:, :, ::-1]
    return image


# ==================== Functions related to NON virtual pairing ====================
def _pair_normal_device_button_clicked(edge_logical_id: str):
    new_state = st.session_state.gateway_state.copy()
    new_state.status = DevicePairingStatus.PairingSelectedDevice
    new_state.props['device_to_pair'] = edge_logical_id
    remote_gateway_client.send_state_to_gateway(new_state)
    log.debug(f"Sending device to pair information to Gateway."
              f" Device ID: {edge_logical_id}")


def _confirm_normal_pairing_button_clicked():
    new_state: ux_states.UxDevicePairingState = st.session_state.gateway_state.copy()
    new_state.status = DevicePairingStatus.PairingConfirmed
    remote_gateway_client.send_state_to_gateway(new_state)
    log.debug(f"Sending device pairing confirmation to Gateway."
              f" Device ID: {new_state.props['device_to_pair']}")


def _cancel_normal_pairing_button_clicked():
    new_state: ux_states.UxDevicePairingState = st.session_state.gateway_state.copy()
    new_state.status = DevicePairingStatus.PairingCancelled
    new_state.props['device_to_pair'] = None
    remote_gateway_client.send_state_to_gateway(new_state)
    log.debug(f"Sending device pairing cancellation to Gateway.")


def _retry_normal_button_clicked():
    new_state: ux_states.UxDevicePairingState = st.session_state.gateway_state.copy()
    new_state.status = DevicePairingStatus.SelectDeviceToPair
    new_state.props['device_to_pair'] = None
    st.session_state.gateway_state = new_state
    remote_gateway_client.send_state_to_gateway(new_state)
    log.debug(f"Retry button was clicked for current device.")


# ==================== Functions related to VIRTUAL pairing ====================
def _virtual_camera_verification_clicked():
    new_state: ux_states.UxDevicePairingState = st.session_state.gateway_state.copy()
    new_state.status = DevicePairingStatus.VirtualCameraConnectionConfirmed
    remote_gateway_client.send_state_to_gateway(new_state)
    log.debug(f"User confirmed virtual camera connection."
              f" Sending information to Gateway")


def _virtual_thermocamera_verification_clicked():
    new_state: ux_states.UxDevicePairingState = st.session_state.gateway_state.copy()
    new_state.status = DevicePairingStatus.VirtualThermocameraConnectionConfirmed
    remote_gateway_client.send_state_to_gateway(new_state)
    log.debug(f"User confirmed virtual thermocamera connection."
              f" Sending information to Gateway")


def _enable_torque_button_clicked():
    start_time = time.time()
    new_state: ux_states.UxDevicePairingState = st.session_state.gateway_state.copy()
    new_state.status = DevicePairingStatus.VirtualEnableTorque
    end_time = time.time()
    log.info(f"Elapsed Time copying state in UX process: {end_time - start_time}s")
    remote_gateway_client.send_state_to_gateway(new_state)
    log.debug(f"User enabled torque. Sending information to Gateway")


def _disable_torque_button_clicked():
    start_time = time.time()
    new_state: ux_states.UxDevicePairingState = st.session_state.gateway_state.copy()
    new_state.status = DevicePairingStatus.VirtualDisableTorque
    end_time = time.time()
    log.info(f"Elapsed Time copying state in UX process: {end_time-start_time}s")
    remote_gateway_client.send_state_to_gateway(new_state)
    log.debug(f"User disabled torque. Sending information to Gateway")


def _capture_position_button_clicked():
    start_time = time.time()
    new_state: ux_states.UxDevicePairingState = st.session_state.gateway_state.copy()
    new_state.status = DevicePairingStatus.VirtualCapturePosition
    end_time = time.time()
    log.info(f"Elapsed Time copying state in UX process: {end_time-start_time}s")
    remote_gateway_client.send_state_to_gateway(new_state)
    log.debug(f"User selected to capture position. Sending information to Gateway")


def _discard_position_button_clicked():
    start_time = time.time()
    new_state: ux_states.UxDevicePairingState = st.session_state.gateway_state.copy()
    new_state.status = DevicePairingStatus.VirtualRejectCapturedPosition
    end_time = time.time()
    log.info(f"Elapsed Time copying state in UX process: {end_time - start_time}s")
    remote_gateway_client.send_state_to_gateway(new_state)
    log.debug(f"User selected to discard position. Sending information to Gateway")


def _confirm_position_button_clicked(position: Tuple):
    start_time = time.time()
    new_state: ux_states.UxDevicePairingState = st.session_state.gateway_state.copy()
    new_state.status = DevicePairingStatus.VirtualConfirmCapturedPosition
    end_time = time.time()
    machine = st.session_state.virtual_edge_selected_asset
    new_state.props["virtual_edge_asset"] = machine
    log.info(f"Elapsed Time copying state in UX process: {end_time - start_time}s")
    _captured_virtual_pos.add(EdgeDescriptor.get_hashed_virtual_id(position))
    st.session_state.gateway_state.props['virtual_production'].position_captured = tuple()
    remote_gateway_client.send_state_to_gateway(new_state)
    log.debug(f"User confirmed captured position. Sending information to Gateway.")


def _finish_virtual_pairing_button_clicked():
    new_state: ux_states.UxDevicePairingState = st.session_state.gateway_state.copy()
    new_state.status = DevicePairingStatus.VirtualConfirmAllPositions
    _captured_virtual_pos.clear()
    remote_gateway_client.send_state_to_gateway(new_state)
    log.debug(f"User confirmed ALL virtual position. Sending information to Gateway.")


# ==================== Rendering of devices pairing panel ====================
def render_devices_pairing():
    """The Devices Pairing panel is used to show interactive widgets
    when a pairing is required, that means when the Gateway State
    is Devices Pairing.
    """
    st.markdown("-------------")
    st.subheader("Emparejar Dispositivos")

    if not _machines_ids:
        for machine in st.session_state.gateway_state.machines:
            _machines_ids.append(machine.machine_id)

    # If Device Pairing is the Current State, then the widgets are shown.
    # The State should keep a track on how many devices have been paired,
    # to decide when all the devices are paired.
    if st.session_state.gateway_state.state == GatewayStates.DevicesPairing:
        paired_devices = st.session_state.gateway_state.props['paired_devices']
        expected_devices = st.session_state.gateway_state.props['expected_devices']
        st.markdown(
            f"**Dispositivos configurados**: {len(expected_devices)}"
        )
        st.markdown(
            f"**Dispositivos emparejados**: {len(paired_devices)}/{len(expected_devices)}"
        )

        # There are devices to pair
        if (
            len(paired_devices) < len(expected_devices)
        ):
            unpaired_devices = expected_devices - paired_devices  # set difference

            device = st.selectbox(
                label="Seleccionar dispoositivo para emparejar",
                key="pair_device_select_box",
                options=list(unpaired_devices),
            )

            # Status: User will select a device to pair
            if st.session_state.gateway_state.status == DevicePairingStatus.SelectDeviceToPair:
                pair_button = st.button(
                    label="Emparejar", key="pair_device_button",
                    on_click=_pair_normal_device_button_clicked, args=(device,)
                )

            # Status: User selected to pair a non-virtual device, and it's being paired by the
            # Gateway
            if st.session_state.gateway_state.status == DevicePairingStatus.PairingSelectedDevice:
                my_bar = st.progress(0)
                for percent_complete in range(10):
                    time.sleep(1)
                    my_bar.progress(percent_complete + 1)

            # The Gateway found successfully a non-virtual device, and request confirmation.
            if st.session_state.gateway_state.status == DevicePairingStatus.RequestConfirm:
                st.success(f"Se encontró un dispositivo conectado para el serial "
                           f"{st.session_state.gateway_state.props['device_to_pair']}")
                c1, c2 = st.columns([.2, 1])  # trick: https://discuss.streamlit.io/t/two-buttons-on-the-same-line/2749/4
                with c1:
                    st.button(
                        label="Confirmar",
                        key="confirm_pairing_button",
                        on_click=_confirm_normal_pairing_button_clicked,
                    )
                with c2:
                    st.button(
                        label="Cancelar",
                        key="cancel_pairing_button",
                        on_click=_cancel_normal_pairing_button_clicked,
                    )

            # The Gateway found an error pairing a non-virtual device
            if st.session_state.gateway_state.status == DevicePairingStatus.PairingError:
                st.error(f"Se encontró un error mientras se emparejaba el dispositivo. "
                         f"Verifique que solo hay 1 dispositivo conectado e intente nuevamente")
                st.button(label="Reintentar", on_click=_retry_normal_button_clicked)

            # ======================== Virtual pairing rendering =======================================
            # The Gateway request to the user the connection of the normal camera
            if st.session_state.gateway_state.status == DevicePairingStatus.RequestVirtualCameraConnection:
                st.markdown("El dispositivo es un dispositivo virtual."
                            " Empezará la producción del dispositivo virtual")
                st.info("Por favor conecte la camara fotográfica al puerto usb")
                verify_camera_btn = st.button(
                    "Verificar Camara",
                    key="virtual_camera_verification",
                    help="Presione este botón cuando haya conectado la cámara",
                    on_click=_virtual_camera_verification_clicked,
                )
                if verify_camera_btn:  # The button was pressed. The Gateway is trying to find the camera.
                    my_bar = st.progress(0)
                    for percent_complete in range(10):
                        time.sleep(1)
                        my_bar.progress(percent_complete + 1)

            # The Gateway successfully connected the normal camera for the virtual edge.
            if st.session_state.gateway_state.status == DevicePairingStatus.VirtualCameraProducedSuccessfully:
                st.success("La camara fotografica fue encontrada con éxito para el dispositivo robot")
                st.markdown("Espere mientras el Gateway procesa la información")

            # There was an error connecting the normal camera for the virtual edge.
            if st.session_state.gateway_state.status == DevicePairingStatus.VirtualCameraConnectionError:
                st.warning("Hubo un error detectando la cámara fotográfica")
                st.text("Espere mientras el Gateway procesa la información")

            # The Gateway now requested to the user the connection of Thermocamera
            if st.session_state.gateway_state.status == DevicePairingStatus.RequestVirtualThermocameraConnection:
                st.markdown("Por favor conecte la cámara termográfica al puerto usb")
                verify_thermocamera_btn = st.button(
                    "Verificar Termocamara", key="virtual_thermocamera_verification",
                    help="Presiones este botón cuando haya conectado la cámara termográfica",
                    on_click=_virtual_thermocamera_verification_clicked
                )
                if verify_thermocamera_btn:  # The button was pressed. The Gateway is trying to find the camera.
                    my_bar = st.progress(0)
                    for percent_complete in range(10):
                        time.sleep(1)
                        my_bar.progress(percent_complete + 1)

            # The thermographic camera was connected successfully
            if st.session_state.gateway_state.status == DevicePairingStatus.VirtualThermocameraProducedSuccessfully:
                st.success("La camara termográfica fue encontrada con éxito para el dispositivo robot")
                st.markdown("Espere mientras el Gateway procesa la información")

            if st.session_state.gateway_state.status == DevicePairingStatus.VirtualThermocameraConnectionError:
                st.warning("Hubo un error detectando la cámara termográfica")
                st.text("Espere mientras el Gateway procesa la información")

            # The Gateway now request the user for the next action in the virtual production
            # This is a "loop" of interactions with the user, until the user has produced all
            # the virtual edges.
            if st.session_state.gateway_state.status == DevicePairingStatus.VirtualRequestNextStepFromUser:
                col1, col2 = st.columns(2)
                production_state = st.session_state.gateway_state.props['virtual_production']
                is_torque_enabled = production_state.torque_enabled
                position_captured = bool(production_state.position_captured)
                at_least_one = bool(production_state.virtual_positions_produced)
                invalid_pos = False
                with col1:
                    st.text("Aquí se mostrará la imagen capturada")
                    if position_captured:
                        st.markdown(f"**Posición capturada**: {production_state.position_captured}")

                        if None in production_state.position_captured:  # The captured position has at least 1 None
                            st.warning("No es posible registrar la posición porque hay "
                                       "valores fuera de rango en los motores.")
                            invalid_pos = True

                        if EdgeDescriptor.get_hashed_virtual_id(production_state.position_captured) in _captured_virtual_pos:
                            st.warning("La posición capturada ya existe.")
                            invalid_pos = True

                        log.info("Rendering captured images in UI")
                        start_time = time.time()
                        if production_state.image_captured:
                            st.image(_get_captured_image(production_state.image_captured),
                                     caption='Imagen normal', output_format="JPEG")
                        else:
                            st.write("No se pudo captura imagen fotografica")

                        if production_state.thermographic_img_captured:
                            st.image(_get_captured_image(production_state.thermographic_img_captured),
                                     caption='Imagen Termográfica', output_format="JPEG")
                        else:
                            st.write("No se pudo capturar imagen termográfica")
                        end_time = time.time()
                        log.info(f"Total time spent rendering images: {end_time-start_time}")
                        st.selectbox(
                            "Asset asociado a la posición",
                            options=_machines_ids,
                            key="virtual_edge_selected_asset",
                        )

                    st.markdown("------")
                    st.markdown("**Posiciones Capturadas:**")
                    # TODO Format output.
                    st.markdown(f"""{list(map(
                        lambda entry: f'{entry[0].get_virtual_edge_information()}, Machine {entry[1]}',
                        production_state.virtual_positions_produced
                    ))}""")

                with col2:
                    st.button('Activar Torque', on_click=_enable_torque_button_clicked, disabled=is_torque_enabled)
                    st.button('Desactivar Torque', on_click=_disable_torque_button_clicked, disabled=not is_torque_enabled)
                    st.button('Capturar Posición', on_click=_capture_position_button_clicked, disabled=position_captured)
                    st.button('Descartar Posición', on_click=_discard_position_button_clicked, disabled=not position_captured)
                    st.button('Guardar Posición', on_click=_confirm_position_button_clicked,
                              args=(production_state.position_captured,),
                              disabled=not position_captured and invalid_pos)
                    st.markdown("-------")
                    st.button("Terminar", on_click=_finish_virtual_pairing_button_clicked, disabled=not at_least_one)

    else:
        # In this case pairing was completed in the past, and shows the feedback from those operations

        st.markdown(
            f"**Dispositivos configurados**: {len(st.session_state.gateway_state.edges)}"
        )
        st.markdown(
            f"**Dispositivos emparejados**: {len(st.session_state.gateway_state.edges)}/"
            f"{len(st.session_state.gateway_state.edges)}"
        )
