# Pet Path Tester
import requests
import json
import pytest

_BASE_URL = "https://petstore3.swagger.io/api/v3/"
# _BASE_URL="https://api-sit.mars-de.dev.dicelab.net:8443/api/mars-de/av"
_API_KEY = ""


class TestPetStore:

    @pytest.fixture(scope="class")
    def setup_header(self):
        headers = {'accept': 'application/json', 'Content-Type': 'application/json', 'api_key': _API_KEY}
        return headers

    # need to populate:
    def test_findbystatus_get(self, setup_header):
        # response = requests.post(_BASE_URL, headers=setup_header)
        # TO-DO implement response validation
        # print(response.json()
        # TO-DO: implement
        pass

    def add_two(number):
        return number + 2
