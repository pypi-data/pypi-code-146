# Copyright (C) Bouvet ASA - All Rights Reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
import copy
import json
import logging

import io
import pprint
import textwrap
import time

from . import entity_json
from .exceptions import ConfigUploadFailed, ExceptionWithResponse
from .entitybase import EntityBase
from .pump import Pump

logger = logging.getLogger(__name__)


class Pipe(EntityBase):
    """
    This class represents a pipe.
    """

    def __str__(self):
        result = super().__str__()
        # TODO: add info about task, provider and sink.
        return result

    def get_pump(self, **kwargs):
        url = self._connection.get_pipe_pump_url(self.id)
        response = self._connection.do_get_request(url, allowable_response_status_codes=[200], **kwargs)
        pump_json = response.json()
        return Pump(self, self._connection, pump_json)

    @property
    def source_dataset_id(self):
        """Returns the id of the dataset that this pipe reads data from, or None if the pipe doesn't
        read data from a dataset."""
        effective_config = self._raw_jsondata["config"]["effective"]
        producer_config = effective_config.get("source")
        if producer_config is None:
            return None

        return producer_config.get("dataset")

    @property
    def sink_dataset_id(self):
        """Returns the id of the dataset that this pipe feeds data to, or None if the pipe doesn't
        feed data to a dataset."""
        effective_config = self._raw_jsondata["config"]["effective"]
        sink_config = effective_config.get("sink")
        if sink_config is None:
            return None

        return sink_config.get("dataset")

    @property
    def execution_dataset_id(self):
        """Returns the id of the dataset that this pipe logs to, or None if the pipe doesn't
        log to a dataset (this is the case for the pipes of the old sdshare server and client)."""
        runtime = self._raw_jsondata["runtime"]
        return runtime.get("execution-dataset")

    def get_log_entities(self, since=None, limit=None, start=None, history=True, deleted=True, reverse=False,
                         do_transit_decoding=True, accept="application/json", expected_node_id=None, method="GET",
                         **kwargs):
        """Returns the content of the execution dataset using the /pipes/{pipe}/log API """
        url = self._connection.get_pipe_log_url(self.id)

        params = {}
        if since is not None:
            params["since"] = since
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        if history is not None:
            params["history"] = history
        if deleted is not None:
            params["deleted"] = deleted
        if reverse is not None:
            params["reverse"] = reverse

        headers = {"ACCEPT": accept}
        if expected_node_id is not None:
            headers["X-Expected-Node-Id"] = expected_node_id

        # The entities are streamed from the server, so we have to enable streaming here.
        request_func = {
            "GET": self._connection.do_get_request,
            "OPTIONS": self._connection.do_options_request
        }[method]

        if request_func is None:
            raise AssertionError("Unsupported request-method '%s'!" % (method,))

        response = request_func(url, allowable_response_status_codes=[200], stream=True, params=params,
                                headers=headers, **kwargs)

        return entity_json.parse_json_stream(response.raw, do_transit_decoding=do_transit_decoding)

    @property
    def runtime(self):
        return copy.deepcopy(self._raw_jsondata["runtime"])

    @property
    def graph(self):
        return copy.deepcopy(self._raw_jsondata["graph"])

    def get_entities(self, since=None, limit=None, stage=None, do_transit_decoding=True, **kwargs):
        """This returns a generator for iterating over the entities of the specified stage
        of this pipe.
        :param do_transit_decoding: bool determining if transit decoding should be performed
        :param since:
        :param limit: The maximum number of entities to return. A value of None means return all the entities.
        :param stage:
        """
        url = self._connection.get_pipe_entities_url(self.id)

        params = {}
        if since is not None:
            params["since"] = since
        if limit is not None:
            params["limit"] = limit
        if stage is not None:
            params["stage"] = stage

        # The entities are streamed from the server, so we have to enable streaming here.
        response = self._connection.do_get_request(url, allowable_response_status_codes=[200],
                                                   stream=True, params=params, **kwargs)

        return entity_json.parse_json_stream(response.raw, do_transit_decoding=do_transit_decoding)

    def post_entities(self, entities,
                      is_full=None,
                      sequence_id=None,
                      request_id=None,
                      previous_request_id=None,
                      is_last=None,
                      is_first=None,
                      completeness=None,
                      headers=None,
                      **kwargs
                      ):
        """This posts the specified entities to the pipe. This only works for pipes that has a source
        of the type 'http_endpoint'.
        """
        url = self._connection.get_pipe_receiver_endpoint_url(self.id)

        # If the size of the entities is very large, we have to use chunked encoding; otherwise we will get
        # a "connection reset" error.
        if type(entities) is str:
            # The entities were already json-encoded.
            entities_as_json = entities
        else:
            entities_as_json = entity_json.entities_to_json(entities)

        class BytesIOWithNoLength(io.BytesIO):
            def __len__(self):
                raise io.UnsupportedOperation()

            def __bool__(self):
                return True

        entities_stream = BytesIOWithNoLength(entities_as_json.encode("utf-8"))

        params = {}
        if is_full is not None:
            params["is_full"] = True
        if sequence_id is not None:
            params["sequence_id"] = sequence_id
        if request_id is not None:
            params["request_id"] = request_id
        if previous_request_id is not None:
            params["previous_request_id"] = previous_request_id
        if is_last is not None:
            params["is_last"] = is_last
        if is_first is not None:
            params["is_first"] = is_first

        if headers is None:
            headers = {"Content-Type": "application/json"}
        if completeness is not None:
            headers["X-Dataset-Completeness"] = str(completeness)
        response = self._connection.do_post_request(url,
                                                    allowable_response_status_codes=[200],
                                                    headers=headers,
                                                    params=params,
                                                    data=entities_stream, **kwargs)

        return response.json()

    def delete(self, **kwargs):
        """Deletes this pipe from the sesam-node.
        """
        url = self._connection.get_pipe_url(self.id)
        response = self._connection.do_delete_request(url, allowable_response_status_codes=[200], **kwargs)

        self.update_raw_jsondata(response.content.decode("utf-8"))

    def modify(self, pipe_config, force=False, **kwargs):
        """Modifies the pipe with the specified configuration."""
        request_params = {"force": "true" if force else "false"}
        pipe_config = copy.deepcopy(pipe_config)
        response = self._connection.do_put_request(self._connection.get_pipe_config_url(self.id),
                                                   allowable_response_status_codes=[200, 400],
                                                   json=pipe_config,
                                                   params=request_params, **kwargs)

        if response.status_code == 400:
            raise ConfigUploadFailed(response=response)

        self.update_raw_jsondata(response.content.decode("utf-8"))

    def wait_for_pipe_to_be_deployed(self, timeout=300, **kwargs):
        starttime = time.monotonic()
        while True:
            try:
                self.update_raw_jsondata_from_url(self._connection.get_pipe_url(self.id), **kwargs)
            except ExceptionWithResponse as e:
                if e.response.status_code == 404:
                    # This pipe has been deleted according to the API, we can return
                    return
                elapsetime = time.monotonic() - starttime
                if elapsetime > timeout:
                    raise AssertionError(
                        f"Timed out while waiting for the config of the pipe '{self.id}' to be deployed. "
                        f"exception: {e}")
                time.sleep(1)
                continue

            runtime = self.runtime
            if "state" not in self.runtime:
                raise AssertionError(f"No 'state' property found in self.runtime! self.runtime: {runtime}")
            if self.runtime["state"] != "Deploying":
                try:
                    self.get_pump()
                    return
                except:
                    logger.warning(f"The pipe with id '{self.id}' has been deployed, but an error was raised while "
                                   f"accessing the pump. Will retry.")
                    pass
            elapsetime = time.monotonic() - starttime
            if elapsetime > timeout:
                raise AssertionError(
                    f"Timed out while waiting for the config of the pipe '{self.id}' to be deployed. "
                    f"self._raw_jsondata: {textwrap.indent(pprint.pformat(self._raw_jsondata), prefix='    ')}")
            time.sleep(1)

    def preview(self, pipe_config, source_entity):
        response = self._connection.do_post_request(self._connection.get_pipe_url(self.id) + "/preview",
                                                    allowable_response_status_codes=[200],
                                                    data={
                                                        "pipe-config": json.dumps(pipe_config),
                                                        "source": json.dumps(source_entity)})
        return response.json()
