from enum import Enum
from pyPPL.models.package import (Package)
from typing import Tuple
from ..base import (SOAPAction)
import xmltodict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Filter(Enum):
    """
    Filter for GetPackages SOAP action
    """
    PACKAGE_NUMBER = 1
    DATE = 2

class SOAPActionGetPackages(SOAPAction):
    """
    GetPackages SOAP action
    Action for creating packages with defined tracking number.
    Generaly sending packages to customer.
    """

    ACTION = 'GetPackages'
    auth_token = ""
    packages = []
    soap_body = """<v1:GetPackages> 
        <v1:Auth>
            <v1:AuthToken>{}</v1:AuthToken> 
        </v1:Auth>
        <v1:Filter>{}</v1:Filter>
    </v1:GetPackages>"""

    def __init__(
        self, 
        auth_token: str, 
        package_numbers: list[str] = [], 
        date: Tuple[datetime, datetime] = (None, None), 
    ) -> None:
        """
        Init SOAP action GetPackages
        @param packages: list of packages to create
        """
        self.auth_token = auth_token
        self.package_numbers = package_numbers
        self.date = date

        # control if there is at least one filter
        # if there is no filter, raise exception
        if (not self.package_numbers or len(self.package_numbers) == 0) and (not self.date or len(self.date) == 0 or (len(self.date) == 2 and (not self.date[0] or not self.date[1]))):
            raise Exception("No filter defined")

        # control if there is more than one filter
        # if there is more than one filter, raise exception
        if (self.package_numbers and len(self.package_numbers) > 0) and (self.date and len(self.date) > 1 and self.date[0] and self.date[1]):
            raise Exception("You can define only one filter to be used")

        # choose the one to use
        if self.package_numbers:
            self.filter = Filter.PACKAGE_NUMBER
        elif self.date:
            self.filter = Filter.DATE

        if not self.filter:
            raise Exception("No filter defined")

        super().__init__()

    def make_fitler_body(self) -> str:
        """
        Make filter body for GetPackages action
        """
        filter_body = ""
        
        if self.filter == Filter.PACKAGE_NUMBER:
            # make packages body for package number filter
            # <v1:PackNumbers> of type ArrayOfstring
            filter_body += """
                <v1:PackNumbers>
            """

            for package_number in self.package_numbers:
                filter_body += """<arr:string>{}</arr:string>""".format(package_number)

            filter_body += """
                </v1:PackNumbers>
            """
        elif self.filter == Filter.DATE:
            # make packages body for date filter
            # <v1:DateFrom> and <v1:DateTo> of type string
            filter_body += """
                <v1:DateFrom>{}</v1:DateFrom>
                <v1:DateTo>{}</v1:DateTo>
            """.format(self.date[0].strftime("%Y-%m-%d"), self.date[1].strftime("%Y-%m-%d"))


        return filter_body

    def make_soap_body(self) -> str:
        """
        Make SOAP body for GetPackages action
        """
        self.data += self.soap_body.format(
            self.auth_token,
            self.make_fitler_body(),
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
