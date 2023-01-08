#  Copyright (c) modalic 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

"""Custom Configuration object."""
from __future__ import annotations

import copy
import dataclasses
from dataclasses import dataclass
from logging import DEBUG, WARNING
from typing import Any, Dict, List, Optional

import toml

from modalic.logging.logging import logger


@dataclass
class Conf(object):
    r"""Configuration object class that stores the parameters regarding the federated learning process.

    :param server_address: (Default: ``'http://127.0.0.1:8080'``) HTTP endpoint for the aggregation server.
    :param client_id: (Default: ``0``) Client identifier which must be unique.
    :param timeout: (Default: ``0``) Defines a timeout length in seconds which is mainly used
        for simulating some waiting periode after each training round. Should always be non-negative.
    :param training_rounds: (Default: ``0``) Number of training rounds that should be performed.
    :param data_type: (Default: ``'F32'``) Models data type which defines the (de-)serialization of the model.
        Type is determined automatically for the endpoints.
    :param certificates: (Default: ``''``) TLS certificates for establishing secure channel with server.
    :param save_state: (Default: ``False``) Defines if the serialized state of a client
        should be saved. For this option to work, MinIO is required to up & running.
    :param backoff_interval: (Default: ``1.0``) Retrying period. Defines the time interval in seconds
        in that the client pings the server.

    :Example:

    Two main ways to construct a Conf object.
        >>> # via dictionary
        >>> custom_dict = {
        >>>     "api": {"server_address": "http://127.0.0.1:8080"},
        >>>     "process":
        >>>         {"training_rounds": 10, "timeout": 5.0},
        >>> }
        >>> conf = Conf.create_conf(custom_dict)
        >>> # ----------------------------------------------
        >>> # via .toml (example config.toml below)
        >>> [api]
        >>> server_address = "http://127.0.0.1:8080"
        >>>
        >>> [process]
        >>> training_rounds = 10
        >>> participants = 3
        >>> strategy = "FedAvg"
        >>> #
        >>> conf = Conf.merge_from_toml(path)
    """
    server_address: str = "http://127.0.0.1:8080"
    client_id: int = 0
    timeout: float = 0.0
    training_rounds: int = 0
    data_type: str = "F32"
    certificates: str = ""
    save_state: bool = False
    backoff_interval: float = 1.0

    def _set_params(self, conf: dict[str, dict[str, Any]]) -> None:
        r"""Overwrites default parameters with external is stated.

        :param conf: Produced by .toml config. Dict which contains dicts. The values
            of conf will overwrite the default values.
        """
        if conf is not None:
            if value := self._find_keys(conf, "server_address"):
                self.server_address = self._check_and_coerce_conf_value_type(
                    value, self.server_address
                )
            if value := self._find_keys(conf, "client_id"):
                self.client_id = self._check_and_coerce_conf_value_type(
                    value, self.client_id
                )
            if value := self._find_keys(conf, "timeout"):
                self.timeout = self._check_and_coerce_conf_value_type(
                    value, self.timeout
                )
            if value := self._find_keys(conf, "training_rounds"):
                self.training_rounds = self._check_and_coerce_conf_value_type(
                    value, self.training_rounds
                )
            if value := self._find_keys(conf, "data_type"):
                self.data_type = self._check_and_coerce_conf_value_type(
                    value, self.data_type
                )
            if value := self._find_keys(conf, "certificates"):
                self.certificates = self._check_and_coerce_conf_value_type(
                    value, self.certificates
                )
            if value := self._find_keys(conf, "save_state"):
                self.certificates = self._check_and_coerce_conf_value_type(
                    value, self.save_state
                )

    def _find_keys(self, blob: Dict[str, dict[str, Any]], key_str: str = "") -> Any:
        r"""Finds the value for certain key in dictionary with arbitrary depth.

        :param blob: Dictionary in which the key value pair is searched for.
        :param key_str: Key that is searched for.
        :returns: Any value that belongs to the key.
        """
        value = None
        for (k, v) in blob.items():
            if k == key_str:
                return v
            if isinstance(v, dict):
                value = self._find_keys(v, key_str)
        return value

    @classmethod
    def create_conf(
        cls, conf: dict[str, dict[str, Any]] = None, cid: Optional[int] = None
    ) -> Conf:
        r"""Constructs a (default) conig object with external conf if given.

        :param conf: Produced by .toml config. Dict which contains dicts. The values
            of conf will overwrite the default values.
        :param cid: (Optional) Option to overwrite client_id when creating a conf.
        """
        instance = cls()
        instance._set_params(conf)
        if cid:
            instance.client_id = cid
        return instance

    @classmethod
    def merge_from_toml(cls, path: str, cid: Optional[int] = None) -> Conf:
        r"""Constructs a conig object from external .toml configuration file.

        :param path: String path to .toml config file.
        :param cid: (Optional) Option to overwrite client_id when creating a conf.
        """
        instance = cls()
        with open(path) as tfile:
            try:
                instance._set_params(toml.load(tfile))
                if cid:
                    instance.client_id = cid
            except FileNotFoundError:
                logger.log(
                    WARNING,
                    f"Config .toml via path '{path}' cannot be found. Default configuration parameters are used.",
                )
        return instance

    def clone(self):
        r"""Recursively copies this Conf object."""
        return copy.deepcopy(self)

    def __str__(self) -> str:
        r"""Custom output string."""
        s = ", ".join(
            f"{field.name}={getattr(self, field.name)!r}"
            for field in dataclasses.fields(self)
            if field.name != "certificates"
        )
        return f"{type(self).__name__}({s})"

    def __iter__(self):
        r"""Makes Conf an iterator."""
        yield self.__dataclass_fields__

    @staticmethod
    def _check_and_coerce_conf_value_type(
        replacement: Any,
        original: Any,
        casts: List[List[Any]] = [[(tuple, list), (list, tuple)]],
        valid_types: Dict = {tuple, list, dict, str, int, float, bool, type(None)},
    ) -> Any:
        """Checks that `replacement`, which is intended to replace `original` is of
        the right type. The type is correct if it matches exactly or is one of a few
        cases in which the type can be easily coerced.

        :param replacement: Intended replacement parameter.
        :param original: Value to be replaced.
        :param casts:
        :param valid_types:
        """
        original_type = type(original)
        replacement_type = type(replacement)

        if replacement_type == original_type:
            return replacement
        elif (
            isinstance(replacement_type, type(None)) and original_type in valid_types
        ) or (
            isinstance(original_type, type(None)) and replacement_type in valid_types
        ):
            return replacement
        else:

            def conditional_cast(from_type, to_type):
                """Cast replacement from from_type to to_type if the replacement and original
                types match from_type and to_type."""
                if replacement_type == from_type and original_type == to_type:
                    return True, to_type(replacement)
                else:
                    return False, None

            for cast_pair in casts:
                for (from_type, to_type) in cast_pair:
                    converted, converted_value = conditional_cast(from_type, to_type)
                    if converted:
                        return converted_value

            logger.log(
                DEBUG,
                f"Type mismatch ({original_type} vs. {replacement_type}) with\
                 values ({original} vs. {replacement}) for Conf.",
            )
            return original
