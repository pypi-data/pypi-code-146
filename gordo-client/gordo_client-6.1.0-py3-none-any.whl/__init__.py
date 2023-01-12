from pkgutil import extend_path

from pkg_resources import DistributionNotFound, get_distribution

from gordo_client.client import Client
from gordo_client.utils import influx_client_from_uri

try:
    __version__ = get_distribution("gordo_client").version
except DistributionNotFound:
    # TODO try to find a better solution for fixing this issue
    # This exception appears if gordo_client is not installed as a package
    # for example in a development environment
    __version__ = "0.0.0"
