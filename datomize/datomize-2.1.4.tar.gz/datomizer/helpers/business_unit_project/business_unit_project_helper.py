import requests
from datomizer import Datomizer
from typing import Tuple
from datomizer.utils.constants import MANAGEMENT_GET_ALL_BUSINESS_UNIT_URL
from datomizer.utils.general import ID


def get_default_business_unit_project(datomizer: Datomizer) -> Tuple[int, int]:
    business_units = datomizer.get_response_json(method=requests.get,
                                                 url=MANAGEMENT_GET_ALL_BUSINESS_UNIT_URL,
                                                 params={"filterProjectAdminOrMember": True})
    return business_units[0][ID], business_units[0]['projects'][0][ID]
