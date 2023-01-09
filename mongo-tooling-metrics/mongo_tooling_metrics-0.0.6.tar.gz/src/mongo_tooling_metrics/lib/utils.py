import os

MONGOD_INTENRAL_DISTRO_FILEPATH = '/etc/mongodb-distro-name'


def is_virtual_workstation() -> bool:
    """Detect whether this is a MongoDB internal virtual workstation."""
    try:
        with open(MONGOD_INTENRAL_DISTRO_FILEPATH, 'r') as file:
            return file.read().strip() == 'ubuntu1804-workstation'
    except Exception as _:  # pylint: disable=broad-except
        return False


TOOLING_METRICS_OPT_OUT = "TOOLING_METRICS_OPT_OUT"


def has_metrics_opt_out() -> bool:
    """Check whether the opt out environment variable is set."""
    return os.environ.get(TOOLING_METRICS_OPT_OUT, None) == '1'
