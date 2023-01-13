"""
# Coronado configuration handlers
"""

import logging
import json
import os

import appdirs


# --- constants ---

API_NAME = 'coronado' # lower case by design; used also as a namespace
CONFIGURATION_PATH = appdirs.user_config_dir(API_NAME)
CONFIGURATION_FILE_NAME = 'config.json'
CONFIGURATION_FILE_PATH = os.path.join(CONFIGURATION_PATH, CONFIGURATION_FILE_NAME)
DEFAULT_LOG_FILE_NAME = 'coronado.log'
LOG_PATH = appdirs.user_log_dir(API_NAME)
LOG_FILE_NAME = 'coronado.log'
LOG_FILE_PATH = os.path.join(LOG_PATH, LOG_FILE_NAME)


# +++ globals +++


_config = None


# --- functions ---

def _logInit(config, fileName = None):
    # fileName used only for unit tests
    os.makedirs(LOG_PATH, exist_ok = True)
    logLevel = getattr(logging, config.get('loglevel', 'INFO').upper(), logging.INFO)
    logFileName = fileName if fileName else LOG_FILE_PATH
    logging.basicConfig(filename = logFileName,
                        filemode = 'w',
                        format = '%(asctime)s %(name)s %(levelname)s %(message)s',
                        level = logLevel)


def envConfig() -> dict:
    """
    Gets the authentication and other configuration parameters from environment
    variables:

    - CORONADO_CLIENT_ID
    - CORONADO_SECRET
    - CORONADO_SERVICE_URL
    - CORONADO_TOKEN_URL

    Returns
    -------
    A Coronado configuration dictionary identical to the response from
    `coronado.config.loadConfig()` with all the keys set to the corresponding
    values set in the environment variables.

    Any value not set results in `None`.
    """
    config = {
        'clientID': os.environ.get('CORONADO_CLIENT_ID', None),
        'secret': os.environ.get('CORONADO_SECRET', None),
        'serviceURL': os.environ.get('CORONADO_SERVICE_URL', None),
        'tokenURL': os.environ.get('CORONADO_TOKEN_URL', None),
    }
    return config


def loadConfig(fileName: str = None,
               testConfig: dict = None) -> dict:
    """
    Load the configuration from the system-dependent config path for the current
    user.  The configuration is stored in A JSON file at CONFIGURATION_FILE_PATH.

    Arguments
    ---------
        fileName
    The configuration file name in the form `config-XXXX.json`, where `XXXX` is
    a string that describes the arbitrary configuration name.  For example, if
    this is Joe's configuration file, `XXXX ::= joe` or if this were a bank name
    then this could be `XXXX ::= mybank` resulting in `config-joe.json` or
    `config-mybank.json`.  The actual name is 100% arbitrary, so file name can
    be `kofigurashion.json` or any other valid file name accepted by the file
    system.

    If `fileName` is specified, the file will be located at: `$CONFIGURATION_PATH/$fileName`.
    `CONFIGURATION_PATH` is system-dependent and resolves **at run-time** to
    these values:

    - macOS:  `$HOME/Library/Application Support/coronado`
    - Linux:  `$HOME/.config/coronado`

        testConfig
    A dictionary, test configuration used for unit testing.  Ignore under normal
    use or contact the developers if needed.

    Return
    ------
    A dictionary of configuration parameters.
    """
    global _config

    if testConfig:
        _config = testConfig
        if fileName:
            _config['testFileName'] = os.path.join(CONFIGURATION_PATH, fileName)
    else:
        for key in os.environ.keys():
            if 'CORONADO_' in key:
                _config = envConfig()
                return _config

        configFilePath = os.path.join(CONFIGURATION_PATH, fileName) \
            if fileName \
            else CONFIGURATION_FILE_PATH

        os.makedirs(CONFIGURATION_PATH, exist_ok = True)
        with open(configFilePath, 'r') as inputStream:
            _config = json.load(inputStream)

    _logInit(_config)

    return _config


def emptyConfig() -> dict:
    """
    Configuration generator builds an empty configuration to fill in the details.

    **configuration**

    ```python
    {
        "clientID": "",
        "clientName": "",
        "loglevel": "INFO",
        "secret": "",
        "serviceURL": "", # API service URL
        "token": "",
        "tokenURL": ""
    }
    ```


    Return
    ------
    A dictionary of configuration parameters, all the values are empty.
    """
    return { "clientID": "",
             "clientName": "",
             "loglevel": "INFO",
             "secret": "",
             "serviceURL": "", # API service URL
             "token": "",
             "tokenURL": ""}

