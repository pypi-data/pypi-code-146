"""
This module defines temporary mocking of the expected
information sent by the Gateway to the streamlit application.

TODO: Remove this mocking when the Gateway basic flow of production-Sampling is completed.
"""
# ======================== imports ===========================
from txp.devices.ux.ux_states_protocol import *
from txp.devices.gateway_states_enums import *
from txp.common.configuration import SamplingWindow
from txp.common.configuration import GatewayConfig
from txp.common.edge import MachineMetadata
import streamlit as st
# from streamlit.report_thread import add_report_ctx
from streamlit.script_run_context import add_script_run_ctx as add_report_ctx
import threading
import time
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

# ======================== Fixed Data ===========================
gateway_id: str = ""

project_id: str = "txp-mvp-heinz"

registry_id: str = ""

cloud_region: str = "us-central1"

machines_id: List[str] = ["TXP-CONVX-001"]

edges_id: List[str] = []

sampling_windows: List[SamplingWindow] = [SamplingWindow(15, 5)]

gateway_conf: "GatewayConfig" = GatewayConfig(
    gateway_id, registry_id, project_id, cloud_region, machines_id, ""
)

machines_metadata: List[MachineMetadata] = [
    MachineMetadata(machines_id[0], "Conveyor X321", "Tranxpert", edges_id)
]

collected_packages: int = 0
sent_packages: int = 0
completed_packages_cycles: int = 0
packages_received_by_edge: Dict[str, int] = {}


# ======================== Mocked States transitions ===========================
def pair_device_mock():
    """Mock the pairing of the selected device."""
    time.sleep(4)
    log.info(f"Pairing device: {st.session_state.gateway_state.device_to_pair}")

    new_state = UxDevicePairingState(
        GatewayStates.DevicesPairing,
        DevicePairingStatus.SelectDeviceToPair,
        None,
        st.session_state.gateway_state.gateway_conf,
        st.session_state.gateway_state.machines,
        st.session_state.gateway_state.edges,
        st.session_state.gateway_state.paired_devices.union(
            [st.session_state.gateway_state.device_to_pair]
        ),
        st.session_state.gateway_state.expected_devices,
        None,
        {"status": "Success", "Details": "The device was paired"},
    )

    st.session_state.gateway_state = new_state


def ready_sampling_mock_loop():
    global collected_packages, sent_packages, completed_packages_cycles, packages_received_by_edge, edges_id

    def loop():
        global collected_packages, sent_packages, completed_packages_cycles, packages_received_by_edge,edges_id
        while True:
            if st.session_state.gateway_state.state == GatewayStates.Ready:
                log.info("Mocking to Sampling State...")
                new_state = UxSamplingState(
                    st.session_state.gateway_state.gateway_conf.gateway_id,
                    st.session_state.gateway_state.gateway_conf.registry_id,
                    GatewayStates.Sampling,
                    GatewaySamplingStatus.Sampling,
                    st.session_state.gateway_state.gateway_conf,
                    st.session_state.gateway_state.machines,
                    st.session_state.gateway_state.edges,
                    st.session_state.gateway_state.paired_devices,
                    st.session_state.gateway_state.expected_devices,
                    st.session_state.gateway_state.collected_packages,
                    st.session_state.gateway_state.sent_packages,
                    st.session_state.gateway_state.completed_package_cycles,
                    st.session_state.gateway_state.packages_received_by_edge,
                )
                time.sleep(sampling_windows[0].sampling_time)
            else:
                log.info("Mocking to Ready State...")
                packages_received_by_edge[edges_id[0]] += 4
                packages_received_by_edge[edges_id[1]] += 3
                collected_packages = collected_packages + 7
                sent_packages = sent_packages + 7
                completed_packages_cycles = collected_packages + 1
                new_state = UxReadyState(
                    st.session_state.gateway_state.gateway_conf.gateway_id,
                    st.session_state.gateway_state.gateway_conf.registry_id,
                    GatewayStates.Ready,
                    ReadyStatus.SchedulingSampling,
                    st.session_state.gateway_state.gateway_conf,
                    st.session_state.gateway_state.machines,
                    st.session_state.gateway_state.edges,
                    st.session_state.gateway_state.paired_devices,
                    st.session_state.gateway_state.expected_devices,
                    collected_packages,
                    sent_packages,
                    completed_packages_cycles,
                    packages_received_by_edge,
                )
                time.sleep(
                    sampling_windows[0].observation_time
                    - sampling_windows[0].sampling_time
                )

            st.session_state.gateway_state = new_state

    packages_received_by_edge = {
        st.session_state.gateway_state.edges[0].logical_id: 0,
        st.session_state.gateway_state.edges[1].logical_id: 0,
        st.session_state.gateway_state.edges[2].logical_id: 0
    }

    edges_id = list(map(
        lambda descriptor: descriptor.logical_id,
        st.session_state.gateway_state.edges
    ))

    state = UxReadyState(
        st.session_state.gateway_state.gateway_conf.gateway_id,
        st.session_state.gateway_state.gateway_conf.registry_id,
        GatewayStates.Ready,
        ReadyStatus.SchedulingSampling,
        st.session_state.gateway_state.gateway_conf,
        st.session_state.gateway_state.machines,
        st.session_state.gateway_state.edges,
        st.session_state.gateway_state.paired_devices,
        st.session_state.gateway_state.expected_devices,
        collected_packages,
        sent_packages,
        completed_packages_cycles,
        packages_received_by_edge,
    )

    st.session_state.gateway_state = state

    thread = threading.Thread(target=loop, name="ReadySamplingLoopMock", daemon=True)
    add_report_ctx(thread)
    thread.start()

