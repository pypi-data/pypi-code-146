from ..base import (SOAPAction)
import xmltodict
import logging


logger = logging.getLogger(__name__)

class SOAPActionVersion(SOAPAction):
    ACTION = 'Version'
    soap_body = """<v1:Version/>"""

    def __init__(self, ) -> None:
        super().__init__()

    def make_soap_body(self) -> str:
        """
        Make SOAP body for Version action
        """
        self.data += self.soap_body

    def parse_success_response(self, response: str) -> object:
        """
        Parse response from SOAP API and return object

        """
        response_object = xmltodict.parse(response)
        return {'version': response_object['VersionResponse']['VersionResult']}
