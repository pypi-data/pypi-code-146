import configparser, os
from sca3s_cli.classes.errors import OKException
from sca3s_cli.classes.status import Status


def get_token(scope='default'):
    """
    Retrieves the API token from the SCA3S config file
    based on a given scope.
    """
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform = str # Pass case sensitive values
    try:
        config.read(os.path.expanduser('~') + '/.sca3s/config')
    except FileNotFoundError:
        raise OKException(Status.CONFIG_NOT_FOUND)
    except:
        raise OKException(Status.CONFIG_PARSE_ERROR)
    try:
        return list(config[scope].keys())[0]
    except:
        raise OKException(Status.ENVIRONMENT_NOT_FOUND)
