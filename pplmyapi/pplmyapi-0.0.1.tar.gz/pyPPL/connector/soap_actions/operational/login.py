from ..base import (SOAPAction)

import xmltodict
import logging
# from pyPPL.conf import (
#     SOAP_CUST_ID,
#     SOAP_PASSWORD,
#     SOAP_USERNAME,
# )


logger = logging.getLogger(__name__)


class SOAPActionLogin(SOAPAction):
    ACTION = 'Login'
    soap_body = """<v1:Login> 
            <v1:Auth>
                <v1:CustId>{}</v1:CustId> 
                <v1:Password>{}</v1:Password> 
                <v1:UserName>{}</v1:UserName>
            </v1:Auth> 
        </v1:Login>"""

    def __init__(self, cust_id: str, password: str, username: str) -> None:
        self.cust_id = cust_id
        self.password = password
        self.username = username
        super().__init__()

    def make_soap_body(self) -> str:
        """
        Make SOAP body for Login action
        input data: CustId, Password, UserName into soap_body
        """
        self.data += self.soap_body.format(
            self.cust_id,
            self.password,
            self.username,
        )

    def parse_success_response(self, response: str) -> object:
        """
        Parse response from SOAP API and return object

        """
        response_object = xmltodict.parse(response)
        return {'token': response_object['LoginResponse']['LoginResult']['AuthToken']}

