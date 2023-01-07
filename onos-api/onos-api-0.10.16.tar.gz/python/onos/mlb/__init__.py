# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: onos/mlb/mlb.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import Dict

import betterproto
import grpclib


@dataclass(eq=False, repr=False)
class GetMlbParamRequest(betterproto.Message):
    pass

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class GetMlbParamResponse(betterproto.Message):
    interval: int = betterproto.int32_field(1)
    overload_threshold: int = betterproto.int32_field(2)
    target_threshold: int = betterproto.int32_field(3)
    delta_ocn: int = betterproto.int32_field(4)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class SetMlbParamRequest(betterproto.Message):
    interval: int = betterproto.int32_field(1)
    overload_threshold: int = betterproto.int32_field(2)
    target_threshold: int = betterproto.int32_field(3)
    delta_ocn: int = betterproto.int32_field(4)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class SetMlbParamResponse(betterproto.Message):
    success: bool = betterproto.bool_field(1)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class GetOcnRequest(betterproto.Message):
    pass

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class GetOcnResponse(betterproto.Message):
    ocn_map: Dict[str, "OcnRecord"] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class OcnRecord(betterproto.Message):
    ocn_record: Dict[str, int] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_INT32
    )

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class OcnIDs(betterproto.Message):
    pass

    def __post_init__(self) -> None:
        super().__post_init__()


class MlbStub(betterproto.ServiceStub):
    async def get_mlb_params(self) -> "GetMlbParamResponse":
        """GetMlbParams gets MLB parameters"""

        request = GetMlbParamRequest()

        return await self._unary_unary(
            "/onos.mlb.Mlb/GetMlbParams", request, GetMlbParamResponse
        )

    async def set_mlb_params(
        self,
        *,
        interval: int = 0,
        overload_threshold: int = 0,
        target_threshold: int = 0,
        delta_ocn: int = 0,
    ) -> "SetMlbParamResponse":
        """SetMlbParams sets MLB parameters"""

        request = SetMlbParamRequest()
        request.interval = interval
        request.overload_threshold = overload_threshold
        request.target_threshold = target_threshold
        request.delta_ocn = delta_ocn

        return await self._unary_unary(
            "/onos.mlb.Mlb/SetMlbParams", request, SetMlbParamResponse
        )

    async def get_ocn(self) -> "GetOcnResponse":
        """GetOcn gets Ocn map"""

        request = GetOcnRequest()

        return await self._unary_unary("/onos.mlb.Mlb/GetOcn", request, GetOcnResponse)
