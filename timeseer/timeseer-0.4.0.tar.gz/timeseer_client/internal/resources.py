"""Python client for Timeseer resources."""

import json
import time

from pathlib import Path
from typing import Dict, List, Optional, Union

import kukur.config

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from timeseer_client.internal import (
    JSONFlightClient,
    MissingModuleException,
    TimeoutException,
)


class Resources:
    """Resources are the main organizational structures within Timeseer.

    Args:
        client: the Timeseer Client
    """

    __client: JSONFlightClient

    def __init__(self, client: JSONFlightClient):
        self.__client = client

    def list(self, *, resource_type: Optional[str] = None) -> List[Dict]:
        """List all defined resources.

        Args:
            resources_types: Only list resources of this type (optional, keyword-only)

        Returns:
            A list of dictionaries of resource 'name' and 'type'.
        """
        body = {}
        if resource_type is not None:
            body["resourceType"] = resource_type
        return self.__client.do_action("resources/list", body)

    def create(
        self,
        resources: Optional[List[Dict]] = None,
        *,
        resource: Optional[Dict] = None,
        path: Optional[Union[Path, str]] = None,
    ):
        """Create or update resources by supplying one resource, multiple resources or a filename.

        Args:
            resources: A list containing the resource definitions.
            resource: One resource definition.
            path: A path to the file or filename of a resource definition.
                This can be in yaml, toml or json format.
        """
        all_resources = []
        if resources is not None:
            assert isinstance(resources, List)
            all_resources.extend(resources)
        if resource is not None:
            assert isinstance(resource, Dict)
            all_resources.append(resource)
        if path is not None:
            if isinstance(path, str):
                path = Path(path)
            if path.suffix in [".yml", ".yaml"]:
                if not HAS_YAML:
                    raise MissingModuleException("PyYAML")
                all_resources.extend(_read_yaml(path))
            elif path.suffix == ".toml":
                all_resources.extend(_read_toml(path))
            elif path.suffix == ".json":
                all_resources.extend(_read_json(path))
        body = dict(
            resources=all_resources,
        )

        self.__client.do_action("resources/create", body)

    def read(self, resource: Dict[str, str]) -> Dict:
        """Return a resource definition.

        Args:
            resource: Dictionary of resource 'type' and 'name'

        Returns:
            The resource definition.
        """
        return self.__client.do_action("resources/read", resource)

    def delete(
        self,
        resources: Optional[List[Dict]] = None,
        *,
        resource: Optional[Dict] = None,
        timeout_seconds: int = 60,
    ):
        """Remove resources.

        Some resources are removed asynchronously. This can prevent removal of other
        resources that are still in use. This method retries removal for the specified time.

        Args:
            resources: A list containing the resources to remove.
            resource: A dictionary of the resource to remove, type and name have to be present.
            timeout_seconds: The timeout before failing (optional, keyword-only).
        """
        all_resources = []
        if resources is not None:
            assert isinstance(resources, List)
            all_resources.extend(resources)

        if resource is not None:
            assert isinstance(resource, Dict)
            all_resources.append(resource)

        body = dict(
            resources=all_resources,
        )

        message = None
        while timeout_seconds > 0:
            response = self.__client.do_action("resources/delete", body)
            if response is None:
                return
            message = response.get("message")
            timeout_seconds = timeout_seconds - 1
            time.sleep(1)

        raise TimeoutException(message)


def _read_yaml(path: Path) -> List[Dict]:
    with path.open() as file:
        return yaml.safe_load(file)


def _read_toml(path) -> List[Dict]:
    config = kukur.config.from_toml(path)
    return config["resource"]


def _read_json(path: Path) -> List[Dict]:
    with path.open() as file:
        return json.load(file)
