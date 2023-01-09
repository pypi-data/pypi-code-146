import ipaddress
import jinja2
from datetime import datetime
import xml.etree.ElementTree as ET
import os


class Route(object):
    def __init__(
        self,
        prefix: str,
        description: str,
        origin_as: str,
        netHandle: str,
        orgHandle: str,
        admin_handle: str,
        tech_handle: str,
    ):

        prefix = self.format_prefix(prefix)
        self.descr = description.split("\n")
        self.prefix = ipaddress.ip_network(prefix)
        self.net_handle = netHandle
        self.org_handle = orgHandle
        self.admin_handle = admin_handle
        self.tech_handle = tech_handle
        self.origin_as = origin_as
        self.date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def to_xml(self):
        """outputs the object in ARIN payload XML format"""

        # TODO: When we start creating more objects move this environment
        #       createtion to a BaseObject class that can be inherited.
        file_path = os.path.dirname(__file__)
        tpl_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(f"{file_path}/templates"), trim_blocks=True
        )
        self.template = tpl_env.get_template("route.j2")
        return self.template.render(data=self.__dict__)

    @classmethod
    def from_xml(cls, xml_doc: str):
        """takes the route payload from arin and converts it to an object"""
        ET.register_namespace("", "http://www.arin.net/regrws/core/v1")
        dn = "{http://www.arin.net/regrws/core/v1}"
        route_elem = ET.fromstring(xml_doc)

        org_handle = route_elem.find(f"{dn}orgHandle").text
        prefix = route_elem.find(f"{dn}prefix").text
        origin_as = route_elem.find(f"{dn}originAS").text
        net_handle = route_elem.find(f"{dn}netHandle").text

        # handle the description lines
        lines = []
        for line in route_elem.find(f"{dn}description"):
            lines.append(line.text)

        descr = "\n".join(lines)

        # sort out the POC refs
        for pocRef in route_elem.find(f"{dn}pocLinks"):
            if pocRef.get("description") == "Admin":
                admin_handle = pocRef.get("handle")
            elif pocRef.get("description") == "Tech":
                tech_handle = pocRef.get("handle")

        return cls(
            prefix, descr, origin_as, net_handle, org_handle, admin_handle, tech_handle
        )

    def format_prefix(self, prefix: str) -> str:
        subnet, cidr = prefix.split("/")
        octets = subnet.split(".")
        octets = [int(o) for o in octets]
        octets = [str(o) for o in octets]
        subnet = ".".join(octets)
        return f"{subnet}/{cidr}"

    @property
    def url(self):
        return f"/rest/irr/route/{ self.prefix.with_prefixlen }/{ self.origin_as }"

    def __str__(self):
        return f"{ self.prefix.with_prefixlen } | { self.origin_as }"
