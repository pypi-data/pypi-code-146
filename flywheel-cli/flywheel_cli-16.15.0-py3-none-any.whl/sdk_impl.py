"""Provides flywheel-sdk implementations of common abstract classes"""
import copy
import json
import logging
import os
import time

import flywheel
import requests

from .importers import ContainerResolver, Uploader
from .util import get_upload_ticket_suggested_headers, pluralize

TICKETED_UPLOAD_PATH = "/{ContainerType}/{ContainerId}/files"

log = logging.getLogger(__name__)


class SdkUploadWrapper(Uploader, ContainerResolver):
    """SDK upload wrapper class

    For now we skip subjects, replacing them (effectively) with the project layer,
    and treating them as if they always exist.
    """

    def __init__(self, fw):
        # pylint: disable=super-init-not-called
        self.fw = fw
        self.fw.api_client.set_default_header("X-Accept-Feature", "Subject-Container")
        self._supports_signed_url = None
        # Session for signed-url uploads
        self._upload_session = requests.Session()

    def supports_signed_url(self):
        """Get signed url feature"""
        if self._supports_signed_url is None:
            config = self.fw.get_config()

            # Support the new and legacy method of feature advertisement, respectively
            features = config.get("features")
            f1 = features.get("signed_url", False) if features else False
            f2 = config.get("signed_url", False)

            self._supports_signed_url = f1 or f2
        return self._supports_signed_url

    def resolve_path(self, container_type, path):
        """Resolve path"""
        try:
            if (
                os.environ.get("FW_CLI_NO_RESOLVE_PROJECT") == "true"
                and container_type == "project"
            ):
                group_id, project_label = path
                # Find project by label
                container = self.fw.projects.find_first(
                    filter=f'parents.group={group_id},label="{project_label}"'
                )
            else:
                container = self.fw.lookup(path)
            return container.id, container.get("uid")
        except flywheel.ApiException:
            log.debug(f"Resolve {container_type}: {path} - NOT FOUND")
            return None, None

    def resolve_children(self, container_type, path):
        """Resolve children path"""
        try:
            result = self.fw.resolve(path)
            log.debug(
                f"Resolve {container_type}: {path} - returned: {len(result.children)} children"
            )
            return result.children
        except flywheel.ApiException:
            log.debug(f"Resolve {container_type}: {path} - NOT FOUND")
            return []

    def create_container(self, parent, container):
        """Create container"""
        create_fn = getattr(self.fw, f"add_{container.container_type}", None)
        if not create_fn:
            raise ValueError(f"Unsupported container type: {container.container_type}")
        create_doc = copy.deepcopy(container.context)

        if container.container_type == "session":
            # Add subject to session
            create_doc["project"] = parent.parent.id
            create_doc["subject"] = {"_id": parent.id}
            # Copy subject label to code
            create_doc["subject"].setdefault("code", parent.context.get("label", None))
        elif parent:
            create_doc[parent.container_type] = parent.id

        new_id = create_fn(create_doc)
        log.debug(f"Created container: {create_doc} as {new_id}")
        return new_id

    def check_unique_uids(self, request):
        try:
            return self.fw.check_uids_exist(request)
        except flywheel.ApiException as exc:
            if exc.status == 404:
                raise NotImplementedError(
                    "Unique UID check is not supported by the server"
                ) from exc
            raise

    def upload(self, container, name, fileobj, metadata=None):
        upload_fn = getattr(self.fw, f"upload_file_to_{container.container_type}", None)

        if not upload_fn:
            print(
                f"Skipping unsupported upload to container: {container.container_type}"
            )
            return

        log.debug(f"Uploading file {name} to {container.container_type}={container.id}")
        if self.supports_signed_url():
            self.signed_url_upload(container, name, fileobj, metadata=metadata)
        else:
            upload_fn(
                container.id,
                flywheel.FileSpec(name, fileobj),
                metadata=json.dumps(metadata),
            )

    def file_exists(self, container, name):
        cont = self.fw.get(container.id)
        if not cont:
            return False
        for file_entry in cont.get("files", []):
            if file_entry["name"] == name:
                return True
        return False

    def signed_url_upload(self, container, name, fileobj, metadata=None):
        """Upload fileobj to container as name, using signed-urls"""
        # Create ticketed upload
        path_params = {
            "ContainerType": pluralize(container.container_type),
            "ContainerId": container.id,
        }
        ticket, upload_url, headers = self.create_upload_ticket(
            path_params, name, metadata=metadata
        )

        log.debug(
            f"Upload url for {name} on {container.container_type}={container.id}: {ticket} (ticket={upload_url})"
        )

        # Perform the upload
        resp = self._upload_session.put(upload_url, data=fileobj, headers=headers)
        max_retries = 3
        retry_num = 0
        if resp.status_code == 429 or 500 <= resp.status_code < 600:
            while retry_num < max_retries:
                log.info("Upload failed, retrying...")
                time.sleep(2**retry_num)
                retry_num += 1
                resp = self._upload_session.put(
                    upload_url, data=fileobj, headers=headers
                )

        resp.raise_for_status()
        resp.close()

        # Complete the upload
        self.complete_upload_ticket(path_params, ticket)

    def create_upload_ticket(self, path_params, name, metadata=None):
        """Create upload ticket"""
        body = {"metadata": metadata or {}, "filenames": [name]}

        response = self.call_api(
            TICKETED_UPLOAD_PATH,
            "POST",
            path_params=path_params,
            query_params=[("ticket", "")],
            body=body,
            response_type=object,
        )
        headers = get_upload_ticket_suggested_headers(response)
        return response["ticket"], response["urls"][name], headers

    def complete_upload_ticket(self, path_params, ticket):
        """Complete upload ticket"""
        self.call_api(
            TICKETED_UPLOAD_PATH,
            "POST",
            path_params=path_params,
            query_params=[("ticket", ticket)],
        )

    def call_api(self, resource_path, method, **kwargs):
        """Call api"""
        kwargs.setdefault("auth_settings", ["ApiKey"])
        kwargs.setdefault("_return_http_data_only", True)
        kwargs.setdefault("_preload_content", True)

        return self.fw.api_client.call_api(resource_path, method, **kwargs)
