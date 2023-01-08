from dataclasses import dataclass
from pydpn._api.api_base import ApiBase


@dataclass
class SessionSpeed:
    pass


@dataclass
class TotalTraffic:
    pass


@dataclass
class TrafficStatistics:
    pass


class Traffic(ApiBase):
    @property
    def sessionSpeed(self) -> SessionSpeed:
        """get the history of traffic speed
        Returns:
            SessionSpeed:
        """
        desc = {
            "serviceName": "sessionSpeed",
            "refUrl": self.refUrl,
            "apiRoute": "traffic/session-speed",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "timeline": list,
                "traffic": list,
            },
            "returnType": SessionSpeed,
        }

        return self.deeper._api_call(desc)

    @property
    def totalTraffic(self) -> TotalTraffic:
        """get the total traffic
        Returns:
            TotalTraffic:
        """
        desc = {
            "serviceName": "totalTraffic",
            "refUrl": self.refUrl,
            "apiRoute": "traffic/total-traffic",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "clientTraffic": dict,
                "localTraffic": dict,
                "serverTraffic": dict,
            },
            "returnType": TotalTraffic,
        }

        return self.deeper._api_call(desc)

    @property
    def totalStatistics(self) -> TrafficStatistics:
        """get the history of total traffic
        Returns:
            TrafficStatistics:
        """
        desc = {
            "serviceName": "totalStatistics",
            "refUrl": self.refUrl,
            "apiRoute": "traffic/total-statistics",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "bandwidthAppRatio": dict,
                "sessionAppRatio": dict,
            },
            "returnType": TrafficStatistics,
        }

        return self.deeper._api_call(desc)

    @property
    def selfStatistics(self) -> TrafficStatistics:
        """get the history of self-traffic
        Returns:
            TrafficStatistics:
        """
        desc = {
            "serviceName": "selfStatistics",
            "refUrl": self.refUrl,
            "apiRoute": "traffic/self-statistics",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "bandwidthAppRatio": dict,
                "sessionAppRatio": dict,
            },
            "returnType": TrafficStatistics,
        }

        return self.deeper._api_call(desc)

    @property
    def shareStatistics(self) -> TrafficStatistics:
        """get the history of self-traffic
        Returns:
            TrafficStatistics:
        """
        desc = {
            "serviceName": "shareStatistics",
            "refUrl": self.refUrl,
            "apiRoute": "traffic/share-statistics",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "bandwidthAppRatio": dict,
                "sessionAppRatio": dict,
            },
            "returnType": TrafficStatistics,
        }

        return self.deeper._api_call(desc)
