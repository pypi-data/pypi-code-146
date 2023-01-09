# Copyright (C) 2022 Panther Labs, Inc.
#
# The Panther SaaS is licensed under the terms of the Panther Enterprise Subscription
# Agreement available at https://panther.com/enterprise-subscription-agreement/.
# All intellectual property rights in and to the Panther SaaS, including any and all
# rights to access the Panther SaaS, are governed by the Panther Enterprise Subscription Agreement.

# coding=utf-8
# *** WARNING: generated file
import os
import ast
import json
import types
import base64
import inspect
import logging
import textwrap
import datetime
import dataclasses
from typing import List, Dict, Any, Callable, Union, cast, Tuple

from panther_core.snapshots import snapshot_func


@dataclasses.dataclass(frozen=True)
class SDKNodeOrigin:
    pkg: str = "none"
    name: str = "none"

    def to_dict(self) -> Dict[str, str]:
        return dict(pkg=self.pkg, name=self.name)


def origin_factory() -> SDKNodeOrigin:
    stack = inspect.stack()
    frame = stack[2]

    if not frame:
        return SDKNodeOrigin()

    module = inspect.getmodule(frame[0])

    if not module:
        return SDKNodeOrigin()

    module_name = module.__name__ or "none"
    return SDKNodeOrigin(
        pkg=module.__package__ or "none",
        name=f"{module_name}.{frame.function}",
    )


@dataclasses.dataclass(frozen=True)
class SDKNode:
    _origin: SDKNodeOrigin = dataclasses.field(
        default_factory=origin_factory, init=False
    )

    def __post_init__(self) -> None:
        if self._output_key():
            cache.add(self._output_key(), self)

    def _typename(self) -> str:
        return "SDKNode"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> List[str]:
        return []


class _Cache:
    _data: Dict[str, List[SDKNode]]
    _cache_dir: str
    _cache_file: str

    def __init__(self) -> None:
        self._data = dict()
        self._cache_dir = os.path.abspath(
            os.environ.get("PANTHER_CACHE_DIR") or os.path.join(".", ".panther")
        )
        self.prep_cache_dir()

        cache_file_name = (
            os.environ.get("PANTHER_SDK_CACHE_FILENAME") or "panther-sdk-cache"
        )

        self._cache_file = os.path.join(self._cache_dir, cache_file_name)

        self.prep_cache_file()

    def prep_cache_dir(self) -> None:
        if not os.path.exists(self._cache_dir):
            os.mkdir(self._cache_dir)

    def prep_cache_file(self) -> None:
        with open(self._cache_file, "w") as f:
            pass

    def add(self, key: str, node: SDKNode) -> None:
        if self._cache_file is None:
            return

        with open(self._cache_file, "a") as f:
            f.write(
                json.dumps(
                    dict(
                        key=key,
                        created_at=datetime.datetime.now(
                            datetime.timezone.utc
                        ).strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                        panther_sdk_version="2022-08-17",
                        val=to_intermediate(node),
                    )
                )
            )
            f.write("\n")


cache = _Cache()


def to_intermediate(obj: Any) -> Any:
    if isinstance(obj, SDKNode):
        field_data = dict()

        for field_name in obj._fields():
            field_data[field_name] = to_intermediate(getattr(obj, field_name))

        return dict(
            o=obj._origin.to_dict(),
            t=obj._typename(),
            d=field_data,
        )

    if isinstance(obj, list):
        return [*map(to_intermediate, obj)]

    if isinstance(obj, types.FunctionType):
        snapshot, _ = snapshot_func(obj)
        return dict(
            src=base64.b64encode(snapshot.encode("utf-8")).decode("utf-8"),
            name=obj.__name__,
        )

    return obj
