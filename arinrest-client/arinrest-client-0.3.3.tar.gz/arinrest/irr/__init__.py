from arinrest.common.connection import ArinRestConnection
import ipaddress


class IRRClient(object):
    def __init__(self, connection: ArinRestConnection):
        self.connection = connection
        self.objects = []

    def add_object(self, object):
        # need to figure out the url
        # if we are adding the objects to the
        # session.
        # the objects information creates the url
        # maybe obj.url
        self.objects.append(object)

    def get_route(self, prefix: str, origin_as: str):
        ip_network = ipaddress.ip_network(prefix)

        url = f"/rest/irr/route/{ip_network.network_address}/{ip_network.prefixlen}/{origin_as}"
        resp = self.connection.get(url)

        return resp

    def get_routes_for_net(self, net_handle: str):
        pass

    def get_routes_for_org(self, org_handle: str):
        pass

    def submit(self):
        for obj in self.objects:
            self.connection.post(obj.url, body=obj.body)
