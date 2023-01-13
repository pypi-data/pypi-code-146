from pyPPL.models.package import (Package)
from ..base import (SOAPAction)
import xmltodict
import logging


logger = logging.getLogger(__name__)

class SOAPActionCreatePackages(SOAPAction):
    """
    CreatePackages SOAP action
    Action for creating packages with defined tracking number.
    Generaly sending packages to customer.
    """

    ACTION = 'CreatePackages'
    auth_token = ""
    packages = []
    soap_body = """<v1:CreatePackages> 
        <v1:Auth>
            <v1:AuthToken>{}</v1:AuthToken> 
        </v1:Auth>
        <v1:Packages>{}</v1:Packages>
    </v1:CreatePackages>"""

    def __init__(self, auth_token: str, packages: list[Package]) -> None:
        """
        Init SOAP action CreatePackages
        @param packages: list of packages to create
        """
        self.auth_token = auth_token
        self.packages = packages
        super().__init__()

    def make_packages_body(self) -> str:
        """
        Make packages body for CreatePackages action
        """
        packages_body = ""
        for package in self.packages:
            packages_body += """
                <v1:MyApiPackageIn>{}</v1:MyApiPackageIn>
            """.format(
                package.to_xml()
            )
        return packages_body

    def make_soap_body(self) -> str:
        """
        Make SOAP body for CreatePackages action
        """
        self.data += self.soap_body.format(
            self.auth_token,
            self.make_packages_body(),
        )


    def parse_success_response(self, response: str) -> object:
        """
        Parse response from SOAP API and return object

        """
        response_object = xmltodict.parse(response)
        # pri
        print(response)
        return response_object

        # return {'healthy': response_object['IsHealtlyResponse']['IsHealtlyResult']}
