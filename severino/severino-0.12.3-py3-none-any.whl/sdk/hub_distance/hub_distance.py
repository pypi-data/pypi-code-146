from uuid import UUID

from severino.sdk.helpers.http_requests import Http
from severino.settings import SEVERINO_API_URL


class HubDistanceCEP:
    http = None
    severino_api_url = ""
    path = ""

    def __init__(self):
        self.http = Http()
        self.severino_api_url = SEVERINO_API_URL
        self.path = "/hub-distance/cep"

    def get(self, cep: str):
        """Get CEP Info

        Args:
            cep (str)
        """
        return self.http.get(url=f"{self.severino_api_url}{self.path}/{cep}/")

    def create(
        self,
        latitude: str,
        longitude: str,
        cep: str,
        address: str = "",
        neighborhood: str = "",
        city: str = "",
        state: str = "",
    ):
        """Add new CEP info

        Args:
            latitude (str)
            longitude (str)
            cep (str)
            address (str, optional)
            neighborhood (str, optional)
            city (str, optional)
            state (str, optional)
        """

        if not "-" in cep:
            cep = cep[:5] + "-" + cep[-3:]

        data = {
            "latitude": latitude,
            "longitude": longitude,
            "cep": cep,
            "address": address,
            "neighborhood": neighborhood,
            "city": city,
            "state": state,
        }

        return self.http.post(
            url=f"{self.severino_api_url}{self.path}/",
            data=data,
        )

    def put(
        self,
        cep_id: UUID,
        latitude: str,
        longitude: str,
        cep: str,
        address: str = "",
        neighborhood: str = "",
        city: str = "",
        state: str = "",
    ):
        """Update CEP info

        Args:
            latitude (str)
            longitude (str)
            cep (str)
            address (str, optional)
            neighborhood (str, optional)
            city (str, optional)
            state (str, optional)
        """

        if not "-" in cep:
            cep = cep[:5] + "-" + cep[-3:]

        data = {
            "latitude": latitude,
            "longitude": longitude,
            "cep": cep,
            "address": address,
            "neighborhood": neighborhood,
            "city": city,
            "state": state,
        }

        return self.http.put(
            url=f"{self.severino_api_url}{self.path}/{cep_id}/",
            data=data,
        )


class HubDistance:
    def __init__(self):
        self.http = Http()
        self.severino_api_url = SEVERINO_API_URL
        self.path = "/hub-distance"

    def distance(self, cep: str):
        """Get the distance between CEP and Hub

        Args:
            cep (str): E.g: 06401-000

        Returns:
            object: Http requests object
        """
        return self.http.get(url=f"{self.severino_api_url}{self.path}/{cep}/")
