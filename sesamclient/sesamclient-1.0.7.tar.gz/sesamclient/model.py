# Copyright (C) Bouvet ASA - All Rights Reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

import json
import logging
import copy

from .exceptions import ConfigUploadFailed
from .entitybase import EntityBase
from . import utils


logger = logging.getLogger(__name__)


class Model(EntityBase):
    """
    This class represents a model.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def delete(self, **kwargs):
        """Deletes this system from the sesam-node.
        """
        url = self._connection.get_model_url(self.id)
        response = self._connection.do_delete_request(url, allowable_response_status_codes=[200],
                                                      **kwargs)
        self.update_raw_jsondata(response.content.decode("utf-8"))

    @property
    def config(self):
        return self.get_config()

    def get_config(self, do_transit_decoding=False):
        return self.as_json_object(do_transit_decoding=do_transit_decoding)
