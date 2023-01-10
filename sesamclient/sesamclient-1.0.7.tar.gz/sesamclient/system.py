# Copyright (C) Bouvet ASA - All Rights Reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
import json
import logging
import copy

from .exceptions import ConfigUploadFailed
from .entitybase import EntityBase
from . import utils


logger = logging.getLogger(__name__)


class System(EntityBase):
    """
    This class represents a system.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def delete(self, **kwargs):
        """Deletes this system from the sesam-node.
        """
        url = self._connection.get_system_url(self.id)
        response = self._connection.do_delete_request(url, allowable_response_status_codes=[200], **kwargs)

        self.update_raw_jsondata(response.content.decode("utf-8"))

    def modify(self, system_config, force=False, **kwargs):
        """Modifies the system with the specified configuration."""
        request_params = {"force": "true" if force else "false"}

        system_config = copy.deepcopy(system_config)
        system_config["_id"] = self.id
        response = self._connection.do_put_request(self._connection.get_system_config_url(self.id),
                                                   allowable_response_status_codes=[200, 400],
                                                   json=system_config,
                                                   params=request_params, **kwargs)

        if response.status_code == 400:
            raise ConfigUploadFailed(response=response)

        self.update_raw_jsondata(response.content.decode("utf-8"))

    @property
    def runtime(self):
        return copy.deepcopy(self._raw_jsondata["runtime"])

    def get_source_prototypes(self, **kwargs):
        url = self._connection.get_system_source_prototypes_url(self.id)
        response = self._connection.do_get_request(url, allowable_response_status_codes=[200], **kwargs)
        return response.json()

    def get_sink_prototypes(self, **kwargs):
        url = self._connection.get_system_sink_prototypes_url(self.id)
        response = self._connection.do_get_request(url, allowable_response_status_codes=[200], **kwargs)
        return response.json()

    def get_secrets(self, include_internal_secrets=False, **kwargs):
        """This returns a list with the names of the secrets."""
        request_params = {}
        if include_internal_secrets:
            request_params["include-internal-secrets"] = "true"

        response = self._connection.do_get_request(self._connection.get_secrets_url(system_id=self.id),
                                                   allowable_response_status_codes=[200],
                                                   params=request_params, **kwargs)
        secrets_info = utils.parse_json_response(response)
        return secrets_info

    def get_secrets_values(self, **kwargs):
        """This returns a dict with secretname=>secretvalue mappings. This is only available for nodes that
        are running in ci-test mode. In addition, the user has to have the "SystemAdmin" role."""
        request_params = {}
        response = self._connection.do_get_request(self._connection.get_secrets_values_url(system_id=self.id),
                                                   allowable_response_status_codes=[200],
                                                   params=request_params, **kwargs)
        secrets_info = utils.parse_json_response(response)
        return secrets_info

    def put_secrets(self, secrets_content, dont_encrypt=False, **kwargs):
        encrypt = dont_encrypt and "false" or "true"
        response = self._connection.do_put_request(self._connection.get_secrets_url(system_id=self.id),
                                                   allowable_response_status_codes=[200],
                                                   json=secrets_content, params=dict(encrypt=encrypt), **kwargs)

        secrets_info = utils.parse_json_response(response)
        return secrets_info

    def post_secrets(self, secrets_content, dont_encrypt=False, **kwargs):
        encrypt = dont_encrypt and "false" or "true"
        response = self._connection.do_post_request(self._connection.get_secrets_url(system_id=self.id),
                                                    allowable_response_status_codes=[200],
                                                    json=secrets_content, params=dict(encrypt=encrypt), **kwargs)

        secrets_info = utils.parse_json_response(response)
        return secrets_info

    def delete_secret(self, key, **kwargs):
        response = self._connection.do_delete_request(self._connection.get_secret_url(key, system_id=self.id),
                                                      allowable_response_status_codes=[200], **kwargs)
        secrets_info = utils.parse_json_response(response)

        return secrets_info

    def get_status(self, **kwargs):
        """This returns a dict with the system's status information."""
        request_params = {}
        response = self._connection.do_get_request(self._connection.get_system_status_url(self.id),
                                                   allowable_response_status_codes=[200],
                                                   params=request_params, **kwargs)
        status_info = utils.parse_json_response(response)

        return status_info

    @property
    def is_valid_config(self):
        return self._raw_jsondata["runtime"]["is-valid-config"]

    @property
    def config_errors(self):
        return self._raw_jsondata["runtime"]["config-errors"]
