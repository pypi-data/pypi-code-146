from typing import Literal
from dataclasses import dataclass
from pydpn._api.api_base import ApiBase
from pydpn._utils.misc import valid_ip

from re import match


class Routing(ApiBase):
    def get_routings(
        self,
        routeType: Literal["ip", "domain"],
        mode: Literal["smart", "direct"],
        page: int = 1,
        size: int = 1000,
    ) -> list:

        if mode == "smart":
            smartDirectSelect = "getRoutingWhitelist"

        elif mode == "direct":
            smartDirectSelect = "getRoutingBlacklist"

        desc = {
            "serviceName": "get_routings",
            "refUrl": f"{self.deeper.hostIp}/{routeType}Config",
            "apiRoute": f"smartRoute/{smartDirectSelect}/{routeType}?pageNo={page}&pageSize={size}",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {"total": int, "list": list},
            "returnType": list,
        }

        return self.deeper._api_call(desc)

    def add_route(self, domainIp, tunnelCode: str = ""):

        if match("^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", domainIp):
            domainIpSelect = "ip"

        else:
            domainIpSelect = "domain"

        if tunnelCode:
            smartDirectSelect = "addToWhitelist"

        else:
            smartDirectSelect = "addToBlacklist"

        postData = {domainIpSelect: domainIp}
        desc = {
            "serviceName": "switch_node",
            "refUrl": f"{self.deeper.hostIp}/{domainIpSelect}Config",
            "apiRoute": f"smartRoute/{smartDirectSelect}/{domainIpSelect}",
            "requestMethod": "POST",
            "responseType": dict,
            "responseContent": {
                "activeIp": str,
                "activeNum": int,
                "success": bool,
            },
            "returnType": dict,
            "setValue": True,
            "postData": postData,
        }

        return self.deeper._api_call(desc)

    def delete_route(
        self, route: list[str], mode: Literal["smart", "direct"]
    ) -> bool:

        evalInput = [valid_ip(f) for f in route]
        if all(evalInput):
            domainIpSelect = "ip"

        elif any(evalInput):
            raise ValueError("Input must be all ip or all domain not mixed")

        else:
            domainIpSelect = "domain"

        if mode == "smart":
            smartDirectSelect = "deleteFromWhitelist"

        elif mode == "direct":
            smartDirectSelect = "deleteFromBlacklist"

        postData = route
        desc = {
            "serviceName": "switch_node",
            "refUrl": f"{self.deeper.hostIp}/{domainIpSelect}Config",
            "apiRoute": f"smartRoute/{smartDirectSelect}/{domainIpSelect}",
            "requestMethod": "POST",
            "responseType": dict,
            "responseContent": {
                "success": bool,
            },
            "returnType": dict,
            "setValue": True,
            "postData": postData,
        }

        return self.deeper._api_call(desc)
