import requests
import json

from dataclasses import dataclass

ERR_MSG = "error"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}


class DistrictException(BaseException):
    pass


@dataclass(init=False)
class District:
    id: int
    district_name: str
    district_app_name: str
    district_baseurl: str
    district_code: str
    state_code: str
    staff_login_url: str
    parent_login_url: str
    student_login_url: str
    earliest: bool

    def __init__(self, distict_name, state_abrv):
        self.district_name = distict_name
        self.state_code = state_abrv
        self.__session = requests.session()

    def __getattr__(self, __name: str) -> None:
        return None

    def validate(self) -> None:
        """
        Raises an error if the district could not be found.
        Adds all attributes returned by IC.
        """
        district_response = self.__session.get(
            "https://mobile.infinitecampus.com/mobile/searchDistrict?query={}&state={}".format(
                self.district_name, self.state_code
            ),
            headers=HEADERS,
        )
        dist_response_json = json.loads(district_response.text)

        if ERR_MSG in dist_response_json:
            raise DistrictException(dist_response_json[ERR_MSG])

        if not "data" in dist_response_json.keys():
            raise KeyError("District data was not found")

        dist_data = dist_response_json["data"][0]
        for k, v in dist_data.items():
            setattr(self, k, v)
