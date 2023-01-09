from arinrest.common.connection import ArinRestConnection
from arinrest.common.rsa import RSASigner
from arinrest.rpki.roa import ROA
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List


class Rpki(object):
    def __init__(self, connection: ArinRestConnection, private_key: str):

        self.connection = connection
        self.roas = []
        self.signer = RSASigner(private_key)

    def add_roa(self, roa: ROA) -> None:
        """sign and add ROA to RPKI session"""

        # sign the object and b64encode it on
        # string creation of the roa
        roa.signature = self.signer.sign(str(roa))
        self.roas.append(roa)

        return

    def submit_roas(self, resource_class: str = "AR", org_handle: str = "TVC-11"):
        """send roa creation request to ARIN for all queued ROA objects"""

        url = f"/rest/roa/{org_handle};resourceClass={resource_class}"

        for roa in self.roas:
            self.connection.post(url, roa.to_xml())

    def get_roas(self, org_id: str) -> List[ROA]:
        url = f"/rest/roa/{org_id}"

        roas = []

        namespaces = {
            "ns0": "http://www.arin.net/regrws/core/v1",
            "ns1": "http://www.arin.net/regrws/rpki/v1",
        }
        data = ET.fromstring(self.connection.get(url))
        specs = data.findall("ns0:roaSpec", namespaces=namespaces)
        for s in specs:

            asNumber = s.find("ns1:asNumber", namespaces=namespaces).text
            name = s.find("ns1:name", namespaces=namespaces).text
            # make the dates datetime objects
            notValidAfter = s.find("ns1:notValidAfter", namespaces=namespaces).text
            notValidBefore = s.find("ns1:notValidBefore", namespaces=namespaces).text

            startDate = datetime.strptime(notValidBefore, "%Y-%m-%dT%H:%M:%S%z")
            endDate = datetime.strptime(notValidAfter, "%Y-%m-%dT%H:%M:%S%z")

            resources = s.find("ns1:resources", namespaces=namespaces)
            cidrLength = resources.find("ns1:cidrLength", namespaces=namespaces).text
            startAddress = resources.find(
                "ns1:startAddress", namespaces=namespaces
            ).text
            endAddress = resources.find("ns1:endAddress", namespaces=namespaces).text

            roas.append(
                ROA(
                    name,
                    asNumber,
                    startDate.strftime("%m-%d-%Y"),
                    endDate.strftime("%m-%d-%Y"),
                    f"{startAddress}/{cidrLength}",
                    "",
                )
            )

        return roas
