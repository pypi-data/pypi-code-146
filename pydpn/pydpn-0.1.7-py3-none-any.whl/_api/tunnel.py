from dataclasses import dataclass
from pydpn._api.api_base import ApiBase


class Tunnel(ApiBase):
    @property
    def listTunnels(self) -> list:
        """get list of tunnels

        Returns:
            DpnMode: dpn Mode
        """
        desc = {
            "serviceName": "listTunnels",
            "refUrl": self.refUrl,
            "apiRoute": "smartRoute/listTunnels",
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

    def delete_tunnels(self, tunnels: list[str]) -> bool:
        """delete a tunnel

        Args:
            tunnels (list[str]): list of tunnels described by regionCountryTexts like ["DE", "DK"]...

        Returns:
            bool: success
        """
        if isinstance(tunnels, list):
            postData = list([f for f in tunnels if isinstance(f, str)])

        desc = {
            "serviceName": "delete_tunnels",
            "refUrl": self.refUrl,
            "apiRoute": "smartRoute/deleteTunnel",
            "requestMethod": "POST",
            "responseType": dict,
            "responseContent": {"success": bool},
            "returnType": bool,
            "setValue": True,
            "postData": postData,
        }

        return self.deeper._api_call(desc)

    def add_tunnel(self, region: str, country: str) -> dict:

        if not all([isinstance(region, str), isinstance(country, str)]):
            raise TypeError("region and country must be of type string")

        postData = {"regionCode": region, "countryCode": country}

        desc = {
            "serviceName": "add_tunnel",
            "refUrl": self.refUrl,
            "apiRoute": "smartRoute/addTunnel",
            "requestMethod": "POST",
            "responseType": dict,
            "responseContent": {"data": dict, "reason": str, "success": bool},
            "returnType": dict,
            "setValue": True,
            "postData": postData,
        }

        return self.deeper._api_call(desc)

    def switch_node(self, tunnelCode: str, currentIp: str) -> dict:

        if not all([isinstance(tunnelCode, str), isinstance(currentIp, str)]):
            raise TypeError("tunnelCode and currentIp must be of type string")

        postData = {"tunnelCode": tunnelCode, "currentIp": currentIp}
        desc = {
            "serviceName": "switch_node",
            "refUrl": self.refUrl,
            "apiRoute": "smartRoute/switchNode",
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

    def refresh_tunnel(self, tunnelCode: str) -> bool:

        postData = {"tunnelCode": tunnelCode}
        desc = {
            "serviceName": "refresh_tunnel",
            "refUrl": self.refUrl,
            "apiRoute": "smartRoute/refreshTunnel",
            "requestMethod": "POST",
            "responseType": dict,
            "responseContent": {"success": bool},
            "returnType": bool,
            "setValue": True,
            "postData": postData,
        }

        return self.deeper._api_call(desc)
