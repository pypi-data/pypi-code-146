from pkg_resources import get_distribution, DistributionNotFound, packaging
import requests
import warnings
import os

def version_compatible():
    """Check if installed client version is compatible to server."""
    try:
        # query latest version from pypi
        package="quantagonia-api-client"
        response = requests.get(f"https://api.quantagonia.com/checkclientversion",
            timeout=1, params={
                "version" : str(__version__),
                "language" : "PYTHON"
            })

        is_latest = bool(response.json()["is_latest"])
        is_supported = bool(response.json()["is_supported"])

        latest_version = response.json()["latest"]
        breaking_version = response.json()["latest_breaking"]


        # throw error if installed version not compatible
        if not is_supported:
            msg = f"Installed version {__version__} of quantagonia-api-client is not compatible due to breaking changes in version {breaking_version}. "
            msg += f"Please update to the latest version {latest_version}."

            return False, msg

        # print warning if update available
        elif not is_latest:
            msg = f"WARNING: "
            msg += f"Installed version {__version__} of quantagonia-api-client is outdated. "
            msg += f"Consider updating to the latest version {latest_version}."

            return True, msg
        # no warning, if latest version
        else:
            return True, ""

    except:
        # catch all, the check for updates should never fail
        return True, "Unable to collect latest version information, skipping check."

try:
    # skip version check for development
    if "SKIP_VERSION_CHECK" not in os.environ or os.environ["SKIP_VERSION_CHECK"] != "1":

        __version__ = get_distribution("quantagonia-api-client").version
        supported, msg = version_compatible()
        if not supported:
            raise ImportError(msg)
        elif msg != "":
            # print warning
            warnings.warn("quantagonia-api-client: " + msg)

except DistributionNotFound:
    __version__ = "dev"
    # don't check for updates in this case
