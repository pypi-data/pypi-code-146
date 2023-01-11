import datetime
import enum
import os
import typing

import pydantic
import requests
from pydantic.typing import Literal

from .exceptions import PricehubbleRequestError

if typing.TYPE_CHECKING:
    from requests import Response


__all__ = ["ETWSettings", "EFHSettings", "MFHSettings"]

DATA_TYPE = str | list | dict | None


class _ApiRequests(pydantic.BaseModel):
    API_LOGIN_URL: str
    API_USERNAME: str
    API_PASSWORD: str
    API_TOKEN: str = None
    API_TOKEN_EXPIRE_TIME: datetime.datetime = datetime.datetime.now()

    def _get_new_token(self) -> str:
        token = requests.post(
            self.API_LOGIN_URL,
            json={
                "username": self.API_USERNAME,
                "password": self.API_PASSWORD,
            },
            headers={
                "content-type": "application/json",
                "accept": "application/json",
            },
        ).json()
        self.API_TOKEN = token["access_token"]
        self.API_TOKEN_EXPIRE_TIME = (
            datetime.datetime.now()
            + datetime.timedelta(seconds=token["expires_in"])
        )
        return self.API_TOKEN

    def run_request(
        self,
        func: typing.Callable[..., "Response"],
        url: str,
        data: DATA_TYPE = None,
    ) -> "Response":

        if (
            self.API_TOKEN_EXPIRE_TIME - datetime.datetime.now()
        ).total_seconds() < 300:
            self._get_new_token()

        try:
            return func(
                url,
                timeout=60,  # Needs to be this high to allow for an all-objects query
                headers={
                    "Accept": "application/json",
                    "Accept-Language": "en",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.API_TOKEN}",
                },
                json=data,
            )
        except Exception as e:
            raise PricehubbleRequestError(
                f"Could not connect to IDM: IDM not reachable!\n{e}"
            )

    def post_request(self, url: str, data: DATA_TYPE) -> "Response":
        return self.run_request(requests.post, url, data)


class _ApiDossier(_ApiRequests):
    API_DOSSIER_URL: str

    def get_dossier(self, id: str) -> "Response":
        return super().post_request(
            os.path.join(self.API_DOSSIER_URL, id, "valuation"),
            None,
        )

    def create_dossier(self, data: DATA_TYPE) -> "Response":
        return super().post_request(
            self.API_DOSSIER_URL,
            data,
        )


class _QualityChoices(enum.Enum):
    simple = "simple"
    normal = "normal"
    high_quality = "high_quality"
    luxury = "luxury"


class _ConditionChoices(enum.Enum):
    renovation_needed = "renovation_needed"
    well_maintained = "well_maintained"
    new_or_recently_renovated = "new_or_recently_renovated"


class _SharedSettings(pydantic.BaseModel):
    street: str
    houseNumber: str
    postCode: str
    city: str


class _SharedETWEFHSettings(pydantic.BaseModel):
    dealType: Literal["Sale", "Rent", "Sale & Rent"] = "Sale & Rent"
    buildingYear: str
    livingArea: str
    renovationYear: str = None
    energyLabel: Literal[
        "A++", "A+", "A", "B", "C", "D", "E", "F", "G", "H"
    ] = None
    numberOfFloorsInBuilding: str = None
    numberOfRooms: str = None
    numberOfBathrooms: str = None
    balconyArea: str = None
    gardenArea: str = None
    numberOfIndoorParkingSpaces: str = None
    numberOfOutdoorParkingSpaces: str = None
    isNew: bool = None

    kitchenStandard: _QualityChoices = None
    kitchenCondition: _ConditionChoices = None
    bathroomStandard: _QualityChoices = None
    bathroomCondition: _ConditionChoices = None
    flooringStandard: _QualityChoices = None
    flooringCondition: _ConditionChoices = None
    windowsStandard: _QualityChoices = None
    windowsCondition: _ConditionChoices = None


class EFHSettings(_SharedSettings, _SharedETWEFHSettings, _ApiDossier):
    subcode: Literal[
        "house_detached",
        "house_semi_detached",
        "house_row_corner",
        "house_row_middle",
        "house_farm",
    ] = None
    landArea: str
    hasPool: bool = None
    hasSauna: bool = None

    roofStandard: _QualityChoices = None
    roofCondition: _ConditionChoices = None


class ETWSettings(_SharedSettings, _SharedETWEFHSettings, _ApiDossier):
    subcode: Literal[
        "apartment_normal",
        "apartment_maisonette",
        "apartment_attic",
        "apartment_penthouse",
        "apartment_terraced",
        "apartment_studio",
    ] = None
    hasLift: bool = None


class MFHSettings(_SharedSettings, _ApiDossier):
    buildingYear: str
    numberOfUnits: str
    livingArea: str
    landArea: str = None
    annualRentIncome: str = None

    buildingStandard: _QualityChoices = None
    buildingCondition: _ConditionChoices = None
