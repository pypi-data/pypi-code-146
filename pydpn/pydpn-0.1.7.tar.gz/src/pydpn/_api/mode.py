from dataclasses import dataclass
from pydpn._api.api_base import ApiBase


@dataclass
class DpnMode:
    dpnMode: str = ""
    tunnelCode: str = ""


class Mode(ApiBase):
    @property
    def dpnMode(self) -> DpnMode:
        """get the dpn mode

        Returns:
            DpnMode: dpn Mode
        """
        desc = {
            "serviceName": "dpnMode",
            "refUrl": self.refUrl,
            "apiRoute": "smartRoute/getDpnMode",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {"dpnMode": str, "tunnelCode": str},
            "returnType": DpnMode,
        }

        return self.deeper._api_call(desc)

    def set_dpnMode(self, value) -> bool:
        """set the dpn mode

        Returns:
            bool: request success
        """
        if isinstance(value, str):
            if value in ["disabled", "smart"]:
                postData = {"dpnMode": value}

            else:
                raise ValueError(
                    "dpnMode must be one of [disabled, smart, full]"
                )

        if isinstance(value, DpnMode):
            value = value.__dict__()

        if isinstance(value, dict):
            keys = value.keys()
            if "dpnMode" in keys:
                dpnMode = value["dpnMode"]
                if dpnMode in ["disabled", "smart"]:
                    postData = {"dpnMode": dpnMode}

                elif dpnMode == "full":
                    if "tunnelCode" in keys:
                        postData = {
                            "dpnMode": "full",
                            "tunnelCode": value["tunnelCode"],
                        }
                else:
                    raise ValueError(
                        "dpnMode must be one of [disabled, smart, full]"
                    )

            else:
                raise ValueError("missing key dpnMode")

        desc = {
            "serviceName": "dpnMode",
            "refUrl": self.refUrl,
            "apiRoute": "smartRoute/setDpnMode",
            "requestMethod": "POST",
            "responseType": dict,
            "responseContent": {"success": bool},
            "returnType": bool,
            "setValue": True,
            "postData": postData,
        }

        return self.deeper._api_call(desc)

    @property
    def tunnelOptions(self) -> list:
        """get list of tunnel options

        Returns:
            DpnMode: dpn Mode
        """
        desc = {
            "serviceName": "dpnMode",
            "refUrl": self.refUrl,
            "apiRoute": "smartRoute/listTunnelOptions",
            "requestMethod": "GET",
            "responseType": list,
            "responseContent": {
                "regionCode": str,
                "countryCode": str,
                "tunnelCode": str,
                "numOfUse": int,
                "addedByUser": bool,
            },
            "returnType": list,
        }

        return self.deeper._api_call(desc)
