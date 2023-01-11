#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from typing import List

from fast_tracker import config
from fast_tracker.utils.lang import b64encode, b64decode


class CarrierItem(object):
    def __init__(self, key: str = "", val: str = ""):
        self.key = key  # type: str
        self.val = val  # type: str

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key: str):
        self.__key = key

    @property
    def val(self):
        return self.__val

    @val.setter
    def val(self, val: str):
        self.__val = val


class Carrier(CarrierItem):
    def __init__(
        self,
        trace_id: str = "",
        segment_id: str = "",
        span_id: str = "",
        service: str = "",
        service_instance: str = "",
        endpoint: str = "",
        client_address: str = "",
        correlation: dict = None,
    ):  # pyre-ignore
        tracker_name = config.get_tracker_name()
        super(Carrier, self).__init__(key=tracker_name)
        self.trace_id = trace_id  # type: str
        self.segment_id = segment_id  # type: str
        self.span_id = span_id  # type: str
        self.service = service  # type: str
        self.service_instance = service_instance  # type: str
        self.endpoint = endpoint  # type: str
        self.client_address = client_address  # type: str
        self.correlation_carrier = FastCorrelationCarrier()
        self.items = [self.correlation_carrier, self]  # type: List[CarrierItem]
        self.__iter_index = 0  # type: int
        if correlation is not None:
            self.correlation_carrier.correlation = correlation

    @property
    def val(self) -> str:
        return "-".join(
            [
                b64encode(self.trace_id),
                self.span_id,
                b64encode(self.segment_id),
                b64encode(self.service),
                b64encode(self.service_instance),
                b64encode(self.endpoint),
                b64encode(self.client_address),
            ]
        )

    @val.setter
    def val(self, val: str):
        self.__val = val
        if not val:
            return
        parts = val.split("-")
        if len(parts) != 7:
            return
        self.trace_id = b64decode(parts[0])
        self.span_id = parts[1]
        self.segment_id = b64decode(parts[2])
        self.service = b64decode(parts[3])
        self.service_instance = b64decode(parts[4])
        self.endpoint = b64decode(parts[5])
        self.client_address = b64decode(parts[6])

    def set_frontend_trace_id(self, trace_id):
        self.trace_id = trace_id

    @property
    def is_valid(self):
        # type: () -> bool
        return (
            # 修改其校验数据规则，因前端传入数据时，如x-fast-trace-id传入只会有trace_id而不会有其他内容
            len(self.trace_id) > 0
            # and len(self.segment_id) > 0
            # and len(self.service) > 0
            # and len(self.service_instance) > 0
            # and len(self.endpoint) > 0
            # and len(self.client_address) > 0
            # and self.span_id.isnumeric()
        )

    def __iter__(self):
        self.__iter_index = 0
        return self

    def __next__(self):
        if self.__iter_index >= len(self.items):
            raise StopIteration
        n = self.items[self.__iter_index]
        self.__iter_index += 1
        return n


class FastCorrelationCarrier(CarrierItem):
    def __init__(self):
        super(FastCorrelationCarrier, self).__init__(key="fast-correlation")
        self.correlation = {}  # type: dict

    @property
    def val(self) -> str:
        if self.correlation is None or len(self.correlation) == 0:
            return ""

        return ",".join([b64encode(k) + ":" + b64encode(v) for k, v in self.correlation.items()])

    @val.setter
    def val(self, val: str):
        self.__val = val
        if not val:
            return
        for per in val.split(","):
            if len(self.correlation) > config.correlation_element_max_number:
                break
            parts = per.split(":")
            if len(parts) != 2:
                continue
            self.correlation[b64decode(parts[0])] = b64decode(parts[1])
