# vim: set fileencoding=utf-8:


from coronado import TripleObject
from coronado import __VERSION__
from coronado.auth import Auth
from coronado.config import loadConfig
from coronado.tools import die

import json
import logging
import sys

import coronado.auth as auth


# +++ constants +++

SERVICE_PATH = '/partner/whoami'


# +++ globals +++

log = logging.getLogger(__name__)


# +++ implementation +++

class Selfie(TripleObject):
    """
    Reports information about the current triple API logged in user.

    Returns
    -------
        TripleObject
    A triple object with at least these attributes set:

    - `clientID`
    - `portfolioManager`
    - `publisher`
    - `contentProvider`

    The Selfie objects are recommended for internal use only and their
    properties will change between versions.

    **Use and rely on `Selfie` at your own risk.**
    """
    requiredAttributes = [
        'clientID',
    ]


    def __init__(self):
        TripleObject.__init__(self, None)


    @classmethod
    def snapshot(klass) -> object:
        response = super().list()

        selfie = TripleObject(json.loads(response.content))
        selfie.coronadoVersion = __VERSION__
        return selfie

# +++ functions +++


def main(unitTest: bool = False) -> dict:
    """
    Report the current triple API user's information in the command line and
    service log.

    This function is the main entry point for an executable that will be
    installed to `/usr/local/bin/triplwhoami` or equivalent depending on whether
    the Coronado package was installed to the systemwide Python configuration or
    to a virtual environment.

    See `man coronado` for details.

    Arguments
    ---------
        unitTest
    Set it to True for running this function in a unit tests

    Returns
    -------
        dict
    `None` if the underlying endpoint call fails; check the log for details.
    Various selfie properties if successful.  See https://api.partners.dev.tripleupdev.com/docs#operation/whoami
    for details.
    """

    _config = loadConfig()

    _auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])

    Selfie.initialize(_config['serviceURL'], SERVICE_PATH, _auth)
    selfie = Selfie.snapshot()

    info = _config['serviceURL']
    print(info)
    log.info(info)
    print(selfie)
    log.info(info)

    if unitTest:
        return selfie.__dict__

