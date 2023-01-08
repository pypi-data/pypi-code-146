from dataclasses import dataclass


@dataclass
class HardwareInfo:
    pass


@dataclass
class SoftwareInfo:
    pass


@dataclass
class NetworkAddress:
    pass


@dataclass
class SessionInfo:
    pass


@dataclass
class LatestSoftwareVersion:
    pass


@dataclass
class SystemUsageHistory:
    pass


class System:
    def __init__(self, deeper) -> None:

        self.deeper = deeper
        self.refUrl = f"{self.deeper.hostIp}/system"

    @property
    def hardwareInfo(self) -> HardwareInfo:
        """get hardware information

        Returns:
            HardwareInfo:
        """
        desc = {
            "serviceName": "hardwareInfo",
            "refUrl": self.refUrl,
            "apiRoute": "system-info/hardware-info",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "SN": str,
                "cpuCount": int,
                "cpuModel": str,
                "deviceId": str,
                "totalMem": int,
            },
            "responseAlias": {},
            "returnType": HardwareInfo,
        }

        return self.deeper._api_call(desc)

    @property
    def softwareInfo(self) -> SoftwareInfo:
        """get hardware information

        Returns:
            HardwareInfo:
        """
        desc = {
            "serviceName": "hardwareInfo",
            "refUrl": self.refUrl,
            "apiRoute": "system-info/software-info",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "appSigVersion": str,
                "softwareVersion": str,
                "urlSigVersion": str,
            },
            "responseAlias": {},
            "returnType": SoftwareInfo,
        }

        return self.deeper._api_call(desc)

    @property
    def networkAddress(self) -> NetworkAddress:
        """get hardware information

        Returns:
            HardwareInfo:
        """
        desc = {
            "serviceName": "networkAddress",
            "refUrl": self.refUrl,
            "apiRoute": "system-info/network-address",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "gatewayMac": str,
                "ip": str,
                "routerMac": str,
            },
            "responseAlias": {},
            "returnType": NetworkAddress,
        }

        return self.deeper._api_call(desc)

    @property
    def sessionInfo(self) -> SessionInfo:
        """get hardware information

        Returns:
            HardwareInfo:
        """
        desc = {
            "serviceName": "sessionInfo",
            "refUrl": self.refUrl,
            "apiRoute": "system-info/session-info",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "currSessionNum": int,
                "icmpSessionNum": int,
                "maxSessionNum": int,
                "tcpSessionNum": int,
                "tunnelSessionNum": int,
                "udpSessionNum": int,
            },
            "responseAlias": {},
            "returnType": SessionInfo,
        }

        return self.deeper._api_call(desc)

    @property
    def autoUpdate(self) -> bool:
        """get the status of auto update function

        Returns:
            SystemUsageHistory:
        """
        desc = {
            "serviceName": "systemUsageHistory",
            "refUrl": self.refUrl,
            "apiRoute": "system-info/get-autoupdate",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "autoUpdate": bool,
            },
            "responseAlias": {},
            "returnType": bool,
        }

        return self.deeper._api_call(desc)

    @autoUpdate.setter
    def autoUpdate(self, value: bool) -> dict:
        """set the status of auto update function

        Returns:
            dict:
        """
        if not isinstance(value, bool):
            raise ValueError("autoUpdate must be True or False")

        desc = {
            "serviceName": "set_autoUpdate",
            "refUrl": self.refUrl,
            "apiRoute": f"system-info/set-autoupdate?autoUpdate={int(value)}",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {"code": bool, "desc": str},
            "responseAlias": {},
            "returnType": dict,
            "setValue": True,
        }

        self.deeper.lastUpdate = self.deeper._api_call(desc)

    @property
    def latestSoftwareVersion(self) -> LatestSoftwareVersion:
        """get the current installed and latest avalible software version
        Returns:
            LatestSoftwareVersion:
        """
        desc = {
            "serviceName": "latestSoftwareVersion",
            "refUrl": self.refUrl,
            "apiRoute": "system-info/get-latestversion",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "currentVersion": str,
                "latestVersion": str,
            },
            "responseAlias": {},
            "returnType": LatestSoftwareVersion,
        }

        return self.deeper._api_call(desc)

    @property
    def systemUsageHistory(self) -> SystemUsageHistory:
        """get 24 hour history of cpu and memory usage

        Returns:
            SystemUsageHistory:
        """
        desc = {
            "serviceName": "systemUsageHistory",
            "refUrl": self.refUrl,
            "apiRoute": "system-info/usage",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "cpuUsageData": list,
                "memUsageData": list,
                "xData": list,
            },
            "responseAlias": {},
            "returnType": SystemUsageHistory,
        }

        return self.deeper._api_call(desc)
