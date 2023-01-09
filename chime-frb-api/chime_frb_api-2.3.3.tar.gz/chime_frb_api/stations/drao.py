#!/usr/bin/env python
"""CHIME/FRB DRAO Backend."""

import logging

from chime_frb_api.backends import distributor, frb_master
from chime_frb_api.core import API

log = logging.getLogger(__name__)


class DRAO:
    """CHIME/FRB DRAO Backend."""

    def __init__(self, **kwargs):
        """CHIME/FRB DRAO Initialization.

        Args:
            base_url (str): Base URL at which the backend is exposed
            **kwargs (dict): Additional arguments
        """
        # Instantiate FRB/Master Core API
        self.API = API(**kwargs)
        # Instantiate FRB Master Components
        self.distributor = distributor.Distributor(**kwargs)
        self.frb_master = frb_master.FRBMaster(**kwargs)
