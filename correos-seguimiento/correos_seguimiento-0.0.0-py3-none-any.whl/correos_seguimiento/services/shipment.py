import requests
import os


class UndefinedCredentials(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class InvalidEndpoint(Exception):
    pass


class UnknownApiResponse(Exception):
    pass


class InvalidApiResponse(Exception):
    pass


class UnknownParcelState(Exception):
    pass


class TrackingShipment:
    def __init__(self, shipment_number):
        self.shipment_number = shipment_number

    def is_delivered(self):
        user = os.getenv("CORREOS_SEGUIMIENTO_USER")
        pwd = os.getenv("CORREOS_SEGUIMIENTO_PASSWORD")
        if not user or not pwd:
            raise UndefinedCredentials
        response = requests.get(
            "https://localizador.correos.es/"
            "canonico/eventos_envio_servicio_auth/"
            "{}?indUltEvento=S".format(self.shipment_number),
            auth=(user, pwd),
        )
        if response.status_code == 401:
            raise InvalidCredentials
        elif response.status_code != 200:
            raise InvalidEndpoint
        try:
            json = response.json()
        except requests.JSONDecodeError:
            raise InvalidApiResponse
        try:
            status = json[0]["eventos"][0]["fase"]
        except (IndexError, KeyError):
            raise UnknownApiResponse
        if status not in ["1", "2", "3", "4"]:
            raise UnknownParcelState
        return status == "4"
