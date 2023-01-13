from pyPPL.models.package import (Package)
from ..base import (SOAPAction)
import xmltodict
import logging


logger = logging.getLogger(__name__)

class SOAPActionCancelPackage(SOAPAction):
    """
    CancelPackage SOAP action
    Action for canceling package with given pack number
    """

    ACTION = 'CancelPackage'
    auth_token = ""
    packages = []
    soap_body = """<v1:CancelPackage> 
        <v1:Auth>
            <v1:AuthToken>{}</v1:AuthToken> 
        </v1:Auth>
        <v1:Cancel>{}</v1:Cancel>
    </v1:CancelPackage>"""

    def __init__(self, auth_token: str, pack_number: str) -> None:
        """
        Init SOAP action CancelPackage
        @param pack_number: ID of package to cancel
        @param auth_token: auth token for SOAP API
        """
        self.auth_token = auth_token
        self.pack_number = pack_number
        super().__init__()

    def make_cancel_body(self) -> str:
        """
        Make packages body for CancelPackage action
        """
        cancel_body = ""
        if self.pack_number:
            cancel_body += """
                <v1:PackNumber>{}</v1:PackNumber>
            """.format(
                self.pack_number
            )
        return cancel_body

    def make_soap_body(self) -> str:
        """
        Make SOAP body for CreatePackages action
        """
        self.data += self.soap_body.format(
            self.auth_token,
            self.make_cancel_body(),
        )


    def parse_success_response(self, response: str) -> object:
        """
        Parse response from SOAP API and return object

        """
        response_object = xmltodict.parse(response)
        # pri
        print(response)
        # return response_object
        return {'canceled': response_object['CancelPackageResponse']['IsHealtlyResult']}

