import requests
import xmltodict
from sdc_dp_helpers.api_utilities.file_managers import load_file


class XMLReader:
    """
    Custom XML Reader
    """

    def __init__(self, config_filepath):
        self.config_path = config_filepath

        self.config = load_file(config_filepath)

        self.url = str(self.config.get("url"))
        self.client = str(self.config.get("client"))

    def xml_to_list(self, payload: bytes) -> list:
        """
        Converts bytes to json.
        :param payload: bytes obtained from xml
        :return: json dump of list
        """
        data_dict = xmltodict.parse(payload)
        data_list = self.get_list_in_dict(data_dict)

        return data_list

    @staticmethod
    def get_list_in_dict(data: dict) -> list:
        """
        Step into dictionary repeatedly until a list is reached.
        :param data: dictionary which needs to be stepped into
        :return: first list encounter in dictionary
        """
        not_list = True

        while not_list:
            if isinstance(data, dict):
                data = data[list(data.keys())[0]]
            elif isinstance(data, list):
                not_list = False
            else:
                raise Exception("List was not found")

        return data

    def _query_handler(self) -> bytes:
        """
        Fetch XML from url
        """
        return requests.get(self.url, timeout=30).content

    def run_query(self) -> list:

        data_bytes = self._query_handler()

        data_list = self.xml_to_list(data_bytes)

        return data_list
