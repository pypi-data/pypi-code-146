# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast
from contrast.api.dtm_pb2 import HttpRequest
from contrast.api.user_input import UserInput
from contrast.utils.decorators import fail_quietly
from contrast.utils.string_utils import ensure_string
from contrast.utils.timer import now_ms
from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")

class ProtectResponse:
    NO_ACTION = 0
    BLOCKED = 1
    MONITORED = 2
    PROBED = 3
    BLOCKED_AT_PERIMETER = 4
    SUSPICIOUS = 6

    _RESPONSE_TO_STR = {
        MONITORED: "MONITORED",
        BLOCKED: "BLOCKED",
        BLOCKED_AT_PERIMETER: "BLOCKED AT PERIMETER",
        NO_ACTION: "NO ACTION",
        SUSPICIOUS: "SUSPICIOUS",
    }
    _RESPONSE_TO_TS_NODE = {
        MONITORED: "exploited",
        BLOCKED: "blocked",
        PROBED: "ineffective",
        SUSPICIOUS: "suspicious",
    }
    @classmethod
    def to_str(cls, response: int) -> str:
        """
        Convert int to str response
        """
        return cls._RESPONSE_TO_STR.get(response, "")

    @classmethod
    def to_ts_node(cls, response: int) -> str:
        """
        Convert int to TS-approved node str
        """
        return cls._RESPONSE_TO_TS_NODE.get(response)





class Attack:
    """
    Class storing all data necessary to report a protect attack.
    """
    def __init__(self, rule_id):
        self.rule_id = rule_id
        self.samples = []
        self.response = None
        self.start_time_ms = contrast.CS__CONTEXT_TRACKER.current().request.timestamp_ms
        self.response = None

    @property
    def blocked(self):
        return self.response == ProtectResponse.BLOCKED

    def add_sample(self, sample):
        self.samples.append(sample)

    def set_response(self, response):
        self.response = response

    def _convert_samples(self, request_dtm: HttpRequest):
        DOCUMENT_TYPES = {
            0: "NORMAL",
            1: "JSON",
            2: "XML",
        }

        path, _, querystring = request_dtm.raw.partition("?")
        return [
            {
                "blocked": self.blocked,
                "input": {
                    "documentPath": sample.user_input.path,
                    "documentType": DOCUMENT_TYPES.get(sample.user_input.document_type),
                    "filters": sample.user_input.matcher_ids,
                    "name": sample.user_input.key,
                    "time": sample.timestamp_ms,
                    "type": UserInput.type_to_str(sample.user_input.input_type),
                    "value": sample.user_input.value,
                },
                "details": sample.details,
                "request": {
                    "body": ensure_string(request_dtm.request_body_binary),
                    # the WSGI environ supports only one value per request header. However
                    # the server decides to handle multiple headers, we're guaranteed to
                    # have only unique keys in request.request_headers (since we iterate
                    # over webob's EnvironHeaders). Thus, each value list here is length-1.
                    "headers": {
                        k: [v] for k, v in request_dtm.request_headers.items()
                    },
                    "method": request_dtm.method,
                    "parameters": {
                        h.key: list(h.values)
                        for h in request_dtm.normalized_request_params.values()
                    },
                    "port": request_dtm.receiver.port,
                    "protocol": request_dtm.protocol,
                    "queryString": querystring,
                    "uri": path,
                    "version": request_dtm.version,
                },
                "stack": self._convert_stacks(sample.stack_trace_elements),
                "timestamp": {
                    "start": sample.timestamp_ms,  # in ms
                    "elapsed": (now_ms() - sample.timestamp_ms),  # in ms which is the format TS accepts
                },
            }
            for sample in self.samples
        ]

    def _convert_stacks(self, stacks_dtm):
        return [
            {
                "declaringClass": stack.declaring_class,
                "methodName": stack.method_name,
                "fileName": stack.file_name,
                "lineNumber": stack.line_number,
            }
            for stack in stacks_dtm
        ]

    @fail_quietly("Unable to create time map", return_value={})
    def _create_time_map(self, samples):
        """
        For the list of samples, createa dict of:

        second since attack start => attacks in that second.
        """
        time_map = {}

        for sample in samples:
            elapsed_secs = sample["timestamp"]["elapsed"]
            time_map.setdefault(elapsed_secs, 0)
            time_map[elapsed_secs] += 1

        return time_map

    def to_json(self, request_dtm: HttpRequest):
        common_fields = {
            "startTime": 0,
            "total": 0,
        }
        json = {
            "startTime": self.start_time_ms,
            "blocked": common_fields,
            "exploited": common_fields,
            "ineffective": common_fields,
            "suspicious": common_fields,
        }

        relevant_mode = ProtectResponse.to_ts_node(self.response)
        if relevant_mode is None:
            # Don't know what response is so just report default info so we can debug.
            return json

        samples = self._convert_samples(request_dtm)

        json[relevant_mode] = {
            "total": 1,  # always 1 until batching happens
            "startTime": self.start_time_ms,
            "attackTimeMap": self._create_time_map(samples),
            "samples": samples,
        }

        return json
