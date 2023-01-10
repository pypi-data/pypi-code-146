"""Library defining the interface to image builder jobs."""

import time
from typing import Any, Dict, List, Optional

from rime_sdk.internal.rest_error_handler import RESTErrorHandler
from rime_sdk.swagger.swagger_client import ApiClient, ImageRegistryApi
from rime_sdk.swagger.swagger_client.models import (
    ManagedImagePackageRequirement,
    ManagedImagePipRequirement,
    RimeManagedImage,
    RimeManagedImageStatus,
)


class RIMEImageBuilder:
    """An interface to a RIME image builder."""

    def __init__(
        self,
        api_client: ApiClient,
        name: str,
        requirements: Optional[List[ManagedImagePipRequirement]] = None,
        package_requirements: Optional[List[ManagedImagePackageRequirement]] = None,
        python_version: Optional[str] = None,
    ) -> None:
        """Create a new RIME image builder.

        Args:
            api_client: ApiClient
                The client used to query about the status of the job.
            name: str
                The name of the RIME managed image that this object monitors.
            requirements: Optional[List[ManagedImage.PipRequirement]] = None
                Optional list of pip requirements to be installed on this image.
            package_requirements: Optional[List[ManagedImage.PackageRequirement]] = None
                Optional list of system package requirements to be installed on
                this image.
            python_version: Optional[str]
                An optional version string specifying only the major and minor version
                for the python interpreter used. The string should be of the format
                X.Y and be present in the set of supported versions.
        """

        self._api_client = api_client
        self._name = name
        self._requirements = requirements
        self._package_requirements = package_requirements
        self._python_version = python_version

    def __eq__(self, obj: Any) -> bool:
        """Check if this builder is equivalent to 'obj'."""
        return isinstance(obj, RIMEImageBuilder) and self._name == obj._name

    def __str__(self) -> str:
        """Pretty-print the object."""
        ret = {"name": self._name}
        if self._requirements:
            ret["requirements"] = str(
                [f"{req.name}{req.version_specifier}" for req in self._requirements]
            )
        if self._package_requirements:
            ret["package_requirements"] = str(
                [
                    f"{req.name}{req.version_specifier}"
                    for req in self._package_requirements
                ]
            )
        if self._python_version:
            ret["python_version"] = self._python_version
        return f"RIMEImageBuilder {ret}"

    def get_status(
        self,
        verbose: bool = False,
        wait_until_finish: bool = False,
        poll_rate_sec: float = 5.0,
    ) -> Dict:
        """Query the ImageRegistry service for the image's build status.

        This query includes an option to wait until the image build is finished.
        It will either have succeeded or failed.

        Arguments:
            verbose: bool
                whether or not to print diagnostic information such as logs.
            wait_until_finish: bool
                whether or not to block until the image is READY or FAILED.
            poll_rate_sec: float
                the frequency with which to poll the image's build status.

        Returns:
            A dictionary representing the image's state.
        """
        # Create backend client stubs to use for the remainder of this session.
        image = RimeManagedImage(status=RimeManagedImageStatus.UNSPECIFIED)
        if verbose:
            print("Querying for RIME managed image '{}':".format(self._name))
        # Do not repeat if the job is finished or blocking is disabled.
        repeat = True
        poll_count = 0
        api = ImageRegistryApi(self._api_client)
        while repeat and not image.status in (
            RimeManagedImageStatus.FAILED,
            RimeManagedImageStatus.OUTDATED,
            RimeManagedImageStatus.READY,
        ):
            with RESTErrorHandler():
                image = api.image_registry_get_image(name=self._name).image
            if verbose:
                status_name = image.status
                print(
                    "\rStatus: {}, Poll Count: {}".format(status_name, poll_count),
                    end="",
                )
            if wait_until_finish:
                time.sleep(poll_rate_sec)
            else:
                repeat = False
            poll_count += 1

            # TODO(blaine): Add ability to get and print logging information from a
            # failed build.

        return image.to_dict()
