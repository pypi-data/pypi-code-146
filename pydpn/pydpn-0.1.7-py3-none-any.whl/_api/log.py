from dataclasses import dataclass
from pydpn._api.api_base import ApiBase


@dataclass
class Notifications:
    pass


class Log(ApiBase):
    @property
    def notifications(self) -> Notifications:
        """get the history of all notifications
        Returns:
            Notifications:
        """
        desc = {
            "serviceName": "notifications",
            "refUrl": self.refUrl,
            "apiRoute": "notifications",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {"CP": list, "DP": list, "MP": list},
            "returnType": Notifications,
        }

        return self.deeper._api_call(desc)
