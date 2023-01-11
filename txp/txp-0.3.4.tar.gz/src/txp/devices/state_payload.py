"""
This module declares the dataclass to be sent as the Gateway State to
the Cloud.
"""
# ============================ imports =========================================
from dataclasses import dataclass
from txp.devices.gateway_states_enums import GatewayStates
from txp.devices.drivers.driver import StateReport
from txp.common.utils.json_complex_encoder import ComplexEncoderSerializable
from datetime import datetime
from typing import List, Dict
from txp.common.config import settings
import json


@dataclass
class GatewayStatePayload(ComplexEncoderSerializable):
    """This GatewayStatePayload encapsulates the information sent to the cloud
    by the Gateway as the State report in the MQTT State topic.
    """
    state: GatewayStates
    edges_states: List[StateReport]
    boot_time: datetime
    ngrok_tcp_address: str
    local_ip: str
    tenant_id: str

    def reprJSON(self) -> Dict:
        edges_payload = {
            report.logical_id: {
                "driver_state": report.driver_state.human_readable_value,
                "since_datetime": report.since_datetime.strftime(
                    settings.time.datetime_format
                ),
                "driver_context": json.dumps(report.driver_context, default=str)
            } for report in self.edges_states
        }

        return dict(
            tenant_id=self.tenant_id,
            edges=edges_payload,
            state=str(self.state),
            boot_time=self.boot_time,
            ngrok_tcp_address=self.ngrok_tcp_address,
            local_ip=self.local_ip
        )
