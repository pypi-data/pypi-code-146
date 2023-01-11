#  Copyright (c) 2020 Caliber Data Labs.
#  All rights reserved.
#
import collections
import imghdr
import io
import json
import math
import os
import random
import re
import time
from collections import defaultdict, OrderedDict
from copy import copy
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Type, Union, Callable, Any
from urllib.parse import quote

from dataclasses import asdict
from packaging import version

import requests
from deprecated import deprecated

from ..models.assets import TemplateOperation
from ..tools.asset_uploader import BulkImageUploader, BulkVideoUploader, BulkLidarUploader
from ..tools.streamable_sets import StreamableSet
from ..tools.asset_utils import get_asset_attributes_filename
from ..tools.misc import get_truncated_uid, deduplicate, get_nested_keys
from ..clients.job_manager_client import Job, wait_for_jobs, JobManagerClient
from ..constants import (AUXILIARY_KEY, TIMESTAMP_FIELD, SESSION_AUXILIARY_KEY,
                         AssetsConstants, COCOAnnotations, ConfigTypes,
                         EntityInfluenceTypes, EntityNames, EntityTypes,
                         JobConstants, MLModelConstants, SessionTypes,
                         SetsAssets, SetTags, ValidExtensions, AuxiliaryDataTypes, Sensors, AnnotationGroups,
                         MAX_THREADS, SummaryEntities, SessionStatuses, DEFAULT_SESSION_RESOLUTION, MAX_SESSION_LENGTH)
from ..custom_exceptions import (AssetError, IndexingException,
                                 InvalidArgumentsError, InvalidAuthorization,
                                 InvalidTimeError, JobError, ResponseError,
                                 SetsError, ThumbnailNotAvailableError, SimilaritySearchError, SessionError, JiraError,
                                 CampaignError, OperationError, ProjectError)
from ..models.annotation import (Annotation, BoundingBox,
                                 BoundingBoxAnnotation, Polygon,
                                 PolygonAnnotation)
from ..models.assets import Image, Embedding, Video, Lidar
from ..models.udf import Enricher, Script, Webhook, UDFError, UDF
from ..models.object_access import ObjectAccess
from ..tools.logger import get_logger
from ..tools.misc import (get_guid, parse_file_path, run_threaded, join, chunk_list)
from ..tools.naming import UriParser, get_similarity_index_name, standardize_name, convert_booleans_to_string
from ..tools.time_utils import (datetime_or_str_to_iso_utc,
                                str_or_datetime_to_datetime,
                                string_to_datetime)
from ..tools.video_utils import get_video_attributes
from ..tools.connections import KVStoreTemplate
from .asset_manager_client import DEFAULT_SEARCH_SIZE, AssetManagerClient
from .. import __version__ as local_version

ENTITIES_BUFFER_SIZE = 1000
VERSION_POSTFIX = "v1"
TIME_INDEX_FIELD = "time_index"
ENTITY_CHUNK_SIZE = 100
DEFAULT_PAGINATION = 5000

logger = get_logger(__name__)

try:
    import pandas as pd
except ImportError as e:
    logger.warning("Could not import package: {}".format(e))

try:
    import dill as pickle
except ImportError as e:
    logger.warning("Could not import package: {}".format(e))

try:
    from IPython import display
except ImportError as e:
    logger.warning("Could not import package: {}".format(e))

try:
    from IPython.display import Javascript
except ImportError as e:
    logger.warning("Could not import package: {}".format(e))

try:
    import numpy as np
except ImportError as e:
    logger.warning("Could not import package: {}".format(e))


def no_asset_provided_error():
    raise ValueError(
        "No asset_type provided and no default asset_type exists. Either provide or set with _set_asset_state("
        "<asset_type>, <metadata:only>)")


def invalid_set_asset_error(asset_type):
    raise ValueError(
        "The asset_type {} is not a valid set asset type. Valid set assets are: {}".format(
            asset_type, SetsAssets.VALID_ASSET_TYPES))


class SceneEngineClient(object):
    """Acts as the root client for all user-tasks on SceneBox."""

    def __init__(
            self,
            auth_token: Optional[str] = None,
            scene_engine_url: Optional[str] = None,
            asset_manager_url: Optional[str] = None,
            environment: Optional[str] = None,
            artifacts_path: str = ".",
            kv_store: Optional[KVStoreTemplate] = None,
            num_threads: int = MAX_THREADS,
    ):
        """Create a SceneEngineClient object. Used to interact with SceneBox's
           high-level REST APIs.

           Parameters
           ----------
           auth_token:
               Personal token associated with a valid SceneBox account. Find this token
               under user profile on the SceneBox web app.
           scene_engine_url:
               URL for the SceneEngine REST server.
           asset_manager_url:
               URL for the AssetManager associated with the SceneEngine server.
           environment:
               The environment that the client is going to use (dev or prod). It will override
           artifacts_path:
               SceneBox's output directory.
           kv_store:
               key-value store to use in asset-manager-client to cache bytes.
            max_threads:
                maximum number of threads to run internal processes in. Default specified in constants file.
        """
        FALLBACK_SCENE_ENGINE_URL = "https://scene-engine.prod.scenebox.ai/"
        self.environment = environment or os.environ.get("SCENEBOX_ENV")
        if not self.environment:
            self.scene_engine_url = scene_engine_url or \
                                    os.environ.get("SCENE_ENGINE_URL") or \
                                    FALLBACK_SCENE_ENGINE_URL
            self._fix_scene_engine_url()
            self.requests = SceneEngineRequestHandler(self.scene_engine_url, auth_token)
            self.front_end_url = self._get_frontend_url()
            self.asset_manager_url = asset_manager_url or self._get_asset_manager_url()
        else:
            self.environment = self.environment.lower()
            valid_environments = ["dev", "prod"]
            if self.environment not in valid_environments:
                raise ValueError("{} is not a valid Scenebox environment.".format(self.environment))
            ENV_URL_TEMPLATE = "https://{}.{}.scenebox.ai/"
            self.scene_engine_url = ENV_URL_TEMPLATE.format("scene-engine", self.environment) + VERSION_POSTFIX
            self._fix_scene_engine_url()
            self.asset_manager_url = ENV_URL_TEMPLATE.format("asset-manager", self.environment) + VERSION_POSTFIX
            self.front_end_url = ENV_URL_TEMPLATE.replace(
                "{}.", "", 1).format(self.environment)
            self.requests = SceneEngineRequestHandler(self.scene_engine_url, auth_token)

        self.amc_cache = {}
        self.auth_token = auth_token
        self.num_threads = num_threads
        self.artifacts_path = artifacts_path
        self.entities_buffer = collections.deque()

        if kv_store:
            self.kv_store = kv_store
        else:
            self.kv_store = None

    def _fix_scene_engine_url(self):
        """Get SceneEngine URL."""
        if not self.scene_engine_url:
            return
        if self.scene_engine_url.endswith("/{}".format(VERSION_POSTFIX)):
            pass
        elif self.scene_engine_url.endswith("/{}/".format(VERSION_POSTFIX)):
            self.scene_engine_url = self.scene_engine_url[:-1]
        elif self.scene_engine_url.endswith("/"):
            self.scene_engine_url += VERSION_POSTFIX
        else:
            self.scene_engine_url += "/{}".format(VERSION_POSTFIX)

    def _get_asset_manager_url(self, check_client_version: bool = True) -> str:
        """Obtain the url of asset-manager."""

        resp = self.requests.get("status", remove_version=True)
        resp.raise_for_status()

        asset_manager_url = resp.json().get("asset_manager_url")
        if asset_manager_url is None:
            ValueError("cannot get asset_manager_url")
        if check_client_version and local_version != 'unknown':
            supported_version = resp.json().get("supported_version")
            if supported_version:
                if version.parse(local_version) < version.parse(supported_version):
                    raise ValueError("your current SceneBox client version {} is not supported, you need > {}. "
                                     "Use pip install scenebox to get latest package ".format(local_version,
                                                                                              supported_version))

        return asset_manager_url

    def _get_frontend_url(self):
        try:
            resp = self.requests.get("status", remove_version=True)
            return resp.json().get("frontend_url")
        except Exception:
            return None

    def __serialize_class(self, input_class: Type[UDF]):
        '''

        Args:
            input_class: UDF class (if a more general type is needed, one way is to define type as objcet,
            then check if type(input_class)=="type" and hasattr("__module__"), or use typing.Generic or typing.TypeVar
            and define all classes you want to use)

        checks if class module is not "__main__", raise error. see
        https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled

        the reason is to avoid pickle.load failure due to this issue
        https://github.com/CaliberDataLabs/scenebox/pull/1753#issue-1101033608
        '''
        if input_class.__module__ != "__main__":
            raise UDFError("pickled objects and UDFs should be defined on a top level")

        pickled_obj = pickle.dumps(input_class)
        return pickled_obj

    def whoami(self) -> dict:
        '''
        Get logged-in user authentication details

        Returns
        -------
        dict
            A dictionary with the following keys: "version","build_host""token","username","role","organization"
        '''
        return self.requests.get("auth", remove_version=True).json()

    def with_auth(self,
                  auth_token: Optional[str] = None,
                  ):
        """Save auth_token into SceneEngineClient as an instance attribute. Authorizes the current SceneEngineClient
        object with the auth_token provided in this call or uses the auth_token the client was created with.

        Parameters
        ----------
        auth_token:
            Personal token associated with a valid SceneBox account. Find this token
            under user profile on the SceneBox web app.

        """
        if auth_token:
            self.auth_token = auth_token

        # Need to also call with_auth of AssetManagerClient in order
        # to update the asset cache

        self.requests.with_auth(
            auth_token=auth_token)

        return self

    def get_platform_version(self) -> str:
        """Get version of the SceneBox Client.

        Returns
        -------
        str
            SceneBox version number

        Raises
        ------
        ValueError
            If a valid version cannot be obtained from SceneBox.
        """
        resp = self.requests.get("status", remove_version=True)
        resp.raise_for_status()

        version = resp.json().get("version")
        if version is None:
            ValueError("cannot get version")

        return version

    def update_artifact_path(self, artifacts_path):
        """Updates the SceneEngineClient artifact path.

        Parameters
        ----------
        artifacts_path:
           Path that specifies the location to save output files.

        """
        self.artifacts_path = artifacts_path

    def get_job(self, job_id: str) -> Job:
        """Get the job_manager_client.Job object associated with the provided job ID.

        Can be a currently executing or finished Job.

        Parameters
        ----------
        job_id:
            The job ID associated with the Job of interest.

        Returns
        -------
        Job
            Job object with the job id ``job_id``.

        """
        metadata = self.get_asset_manager(
            AssetsConstants.JOBS_ASSET_ID).get_metadata(id=job_id)

        return Job(
            status=metadata.get("status"),
            id=job_id,
            progress=metadata.get("progress", 0.0),
            description=metadata.get("description"),
            stage=metadata.get("stage")
        )

    def _wait_for_job_completion(self,
                                 job_id: str,
                                 increments_sec: int = 10,
                                 max_wait_sec: Optional[int] = None,
                                 progress_callback: Optional[Callable] = None
                                 ):
        """Wait for a job to complete.

        Input a max waiting time before an unfinished job throws an Exception.  Choose to either poll while a job is in
        progress, or enact a callable function ``progress_callback()`` with every increment set by ``increments_sec``.

        Parameters
        ----------
        job_id:
            The ID of the job in progress.
        increments_sec:
            The amount of time to poll in between checking job status and calling progress_callback().
        max_wait_sec:
            The maximum amount of time to wait for a job to finish before throwing an exception.  Measured in seconds.
            If None (default), there will be no limit on wait.
        progress_callback:
            Callback function to log the progress of the inference job. The callback should accept a parameter of type
            float for progress and str for progress message.

        Raises
        ------
        JobError
            If job encounters an error, and could not complete.
            If job does not finish after ``max_wait_sec`` seconds.

        """
        # progress callable should take progress as an input and do "something" with it

        elapsed_time = 0
        job = self.get_job(job_id=job_id)
        try:
            while max_wait_sec is None or elapsed_time < max_wait_sec:
                elapsed_time += increments_sec
                job = self.get_job(job_id=job_id)
                if progress_callback:
                    progress_callback(job.progress, job.stage)
                logger.info(
                    "job_id {:40.40s}|Status:{:12.12s}|Progress:{:6.1f} Elapsed Time: {:5d} sec|Description: {} \r".format(
                        job_id,
                        job.status,
                        job.progress,
                        elapsed_time,
                        job.description))
                if job.status == JobConstants.STATUS_FINISHED:
                    logger.info(150 * "-" + "\r")
                    return
                elif job.status in {JobConstants.STATUS_ABORTED}:
                    job_metadata = self.get_asset_manager(
                        AssetsConstants.JOBS_ASSET_ID).get_metadata(job_id)
                    job_notes = job_metadata['notes']
                    raise JobError(
                        'Job {} encountered error with status {} with notes::: {}'.format(
                            job_id, job.status, job_notes))
                else:
                    time.sleep(increments_sec)
        except KeyboardInterrupt as e:
            resp = self.requests.put(
                "jobs/cancel/{}".format(job_id),
                trailing_slash=False)
            if not resp.ok:
                logger.error("Could not interrupt running job {} because {}".format(job_id,
                                                                                    resp.content))
            else:
                raise JobError("Job {} terminated by user".format(job_id))

        raise JobError(
            "Job {} is not finished after {} seconds".format(
                job_id, max_wait_sec))

    def _wait_for_operation_completion(self,
                                       operation_id: str,
                                       increments_sec: int = 10,
                                       enable_max_wait: bool = False,
                                       max_wait_sec: int = 300):

        """Wait for an operation to complete.

        Input a max waiting time before an unfinished operation throws an Exception.  Choose to either poll while a job is in
        progress, or enact a callable function ``progress_callback()`` with every increment set by ``increments_sec``.

        Parameters
        ----------
        operation_id:
            The ID of the job in progress.
        increments_sec:
            The amount of time to poll in between checking operation status.
        enable_max_wait:
            If True, immediately throws an Exception.  Intended for use when there is an external timing constraint.
            Otherwise, does nothing.
        max_wait_sec:
            The maximum amount of time to wait for a job to finish before throwing an exception.  Measured in seconds.

        Raises
        ------
        JobError
            If operation encounters an error, and could not complete.
            If operation does not finish after ``max_wait_sec`` seconds.

        """

        elapsed_time = 0
        try:
            while not enable_max_wait or elapsed_time < max_wait_sec:
                elapsed_time += increments_sec
                operation_status = self.get_operation_status(operation_id)
                status = operation_status.get("status")
                progress = operation_status.get("progress")
                logger.info(
                    "operation_id {:40.40s}|Status:{:12.12s}|Progress:{:6.1f} Elapsed Time: {:5d} sec\r".format(
                        operation_id, status, progress, elapsed_time))
                if status == JobConstants.STATUS_FINISHED:
                    logger.info(150 * "-" + "\r")
                    return
                elif status in {JobConstants.STATUS_ABORTED}:
                    op_job_id = self.get_asset_manager(
                        AssetsConstants.OPERATIONS_ASSET_ID).get_metadata(operation_id).get("job_id")
                    op_job_meta = self.get_asset_manager(
                        AssetsConstants.JOBS_ASSET_ID).get_metadata(op_job_id)
                    job_notes = op_job_meta['notes']
                    job_status = op_job_meta['status']
                    raise JobError(
                        'Operation {} with job {} encountered error with status {} with notes::: {}'.format(
                            operation_id, op_job_id, job_status, job_notes))
                else:
                    time.sleep(increments_sec)
        except KeyboardInterrupt as e:
            resp = self.requests.delete(
                "operations/control/{}".format(operation_id),
                trailing_slash=False)
            if not resp.ok:
                logger.error("Could not interrupt running operation {} because {}".format(operation_id,
                                                                                          resp.content))
            else:
                raise JobError("Operation {} terminated by user".format(operation_id))

        raise JobError(
            "Operation {} is not finished after {} seconds".format(
                operation_id, max_wait_sec))

    def create_project(
            self,
            name: str,
            tags: Optional[List[str]] = None) -> str:

        """Create a project.

            Projects are used to organize and create data workflows.  Once a project is made, users can add sets,
            and apply operations associated with object/embeddings/annotation extraction, and more.

            Parameters
            ----------
            name:
                Name for the created project.
            tags:
                A list of tags to associate this project with. Helpful for filtering them later.

            Returns
            -------
            str
                The ID of the created project.

            Raises
            ------
            ResponseError
                If the project could not be created.

            """

        options = {
            "name": name,
            "tags": tags if tags else []
        }
        resp = self.requests.post(
            "projects/add/",
            trailing_slash=True,
            json=options)
        if not resp.ok:
            raise ResponseError(
                "Could not create the project: {}".format(
                    resp.content))

        id = resp.json()["id"]
        return id

    def delete_project(
            self,
            project_id: str):
        """Delete a project.

            Delete a project.  Deleting a project will not delete any related sets (primary or curated) or annotation
            recipes.

            Parameters
            ----------
            project_id:
                The name of the project to delete.

            Raises
            ------
            ResponseError
                If the project could not be deleted.

            """
        resp = self.requests.delete(
            "projects/meta/{}".format(project_id),
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not delete the project: {}".format(
                    resp.content))

    def get_project_sets(
            self,
            name: str,
            stage: int) -> List[str]:
        """Get sets at a specific stage in a project.

            Get sets for a project.

            Parameters
            ----------
            name:
                The name of the project.

            stage:
                the stage of the sets

            """
        project_metas = self.get_asset_manager(asset_type=AssetsConstants.PROJECTS_ASSET_ID).search_meta(
            filters={"name": name})
        if len(project_metas) < 1:
            raise ProjectError(f"could not find a project with name {name}")
        elif len(project_metas) == 1:
            project_meta = project_metas[0]
        else:
            raise ProjectError(f"Found more than 1 project with name {name}")

        output_sets = []
        for _ in project_meta.get('set_stages', []):
            if _["stage"] == stage:
                output_sets.append(_["set_id"])

        return output_sets

    def create_operation(self,
                         name: str,
                         operation_type: str,
                         project_id: str,
                         config: dict,
                         stage: int = 0,
                         description: Optional[str] = None) -> str:

        """Create an operation inside a project.

            Operations are the custom workflows that can be created inside projects.  Several operations can be added to
            a single project.  Choose from annotation, dataset similarity search, consensus, object extraction, and
            model inference operation types.

            Parameters
            ----------
            name:
                The name of the operation to be created.
            operation_type:
                The type of the operation to execute.  Must match a constant in
                scenebox.constants.OperationTypes.VALID_TYPES.
            project_id:
                The ID of the project to add the operation to.
            config:
                Configurations for the operation to be added.  If ``operation_type`` is ``"annotation"``, then config
                must contain a dict entry with a key named "annotation_instruction_id" with the value of the relevant
                annotation instruction details.
            stage:
                The stage of the operation to be added.  Represents the order of the operations to be executed inside a
                project.
            description:
                A brief description outlining the purpose of the operation, what the operation will accomplish, etc.

            Returns
            -------
            str
                The ID of the created operation.

            Raises
            ------
            ResponseError:
                If the project could not be created.
            OperationError:
                If the provided operation type is not a valid operation type.

            """
        options = {
            "name": name,
            "type": operation_type,
            "stage": stage,
            "project_id": project_id,
            "config": config,
            "description": description
        }

        resp = self.requests.post(
            "operations/add/",
            trailing_slash=True,
            json=options)
        if not resp.ok:
            raise ResponseError(
                "Could not create the operation: {}".format(
                    resp.content))

        id = resp.json()["id"]
        return id

    def delete_operation(self, operation_id: str):

        """Delete an operation.

        Delete an operation from a project. Deleting an operation will not delete any related sets (primary or
        curated) or annotation recipes used by or generated by the operation.

        Parameters
        ----------
        operation_id:
            The ID of the operation to delete.

        Raises
        ------
        ResponseError
            If the operation could not be deleted.

        """

        resp = self.requests.delete(
            "operations/{}".format(operation_id),
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not delete the operation: {}".format(
                    resp.content))

    def start_operation(
            self,
            operation_id: str,
            operation_step: Optional[str] = None,
            wait_for_completion: bool = False) -> str:

        """Start an operation.

        Parameters
        ----------
        operation_id:
            The ID of the operation to execute.
        operation_step:
            If the operation is a CVAT or SuperAnnotate operation, chooses whether to send data to the given annotator,
            or receive annotations.  To send data to the annotator, pass ``send_data``.  To receive, input
            ``receive_annotations``.
            Otherwise, has no effect.
        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.

        Returns
        -------
        str
            The job ID of the Job that starts the operation.
        """
        if operation_step:
            params = {"operation_step": operation_step}
        else:
            params = None

        resp = self.requests.put(
            "operations/control/{}".format(operation_id),
            params=params,
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not start the operation: {}".format(
                    resp.content))

        job_id = resp.json().get("job_id")

        if wait_for_completion:
            self._wait_for_operation_completion(operation_id)

        return job_id

    def get_operation_status(self, operation_id: str) -> dict:

        """Get the status of an operation.

        Parameters
        ----------
        operation_id:
            The ID of the operation to execute.

        Returns
        -------
        dict
            The full status of the operation.

        """
        resp = self.requests.get("operations/{}/status/".format(operation_id))
        resp.raise_for_status()
        return resp.json()

    def add_sets_to_project(
            self,
            project_id: str,
            sets: List[str],
            stage: int = 0):

        """Add sets to a project.

        Specify sets to add to a project.  To run a given operation (associated with some project) on a set,
        the set must be added to the same project as the desired operation.

        Parameters
        ----------
        project_id:
            The ID of the project to add the given sets to.
        sets:
            List of IDs of sets to add to the project.
        stage:
            The stage associated with the set.  Match this with the stage of the desired operation to run.

        """
        options = {
            "sets": sets,
            "stage": stage,
        }

        resp = self.requests.post(
            "projects/{}/add_sets/".format(project_id),
            trailing_slash=True,
            json=options)
        resp.raise_for_status()

    def remove_sets_from_project(
            self,
            project_id: str,
            sets: List[dict]):
        """Remove sets from a project.

        Parameters
        ----------
        project_id:
            ID of the project to remove sets from.
        sets:
            A list of dictionaries listing sets to be removed.
            Dict format:
                [{"set_id": id_of_the_set_tobe_removed, "stage": "project_stage_for_the_set"}]

        """

        options = {
            "sets": sets,
        }

        resp = self.requests.post(
            "projects/{}/remove_sets/".format(project_id),
            trailing_slash=True,
            json=options)
        resp.raise_for_status()

    def create_set(
            self,
            name: str,
            asset_type: str,
            origin_set_id: Optional[str] = None,
            expected_count: Optional[int] = None,
            tags: Optional[List[str]] = None,
            id: Optional[str] = None,
            aux_metadata: Optional[dict] = None,
            is_primary: bool = False,
            raise_if_set_exists=False
    ) -> str:
        """Create a named dataset.

        Set creation is helpful for performing data operations on several assets at once (e.g. ingesting an
        entire set of images/videos/LIDARs/etc. into SceneBox). Each set can only contain one asset type.
        Can optionally raise a SetsError if a set by the given name already exists.

        Parameters
        ----------
        name:
            The name to give to the set.
        asset_type:
            The type of assets for the set to contain. e.g. images, videos, LIDARs, etc.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        origin_set_id:
            Id of the set, the new set is created from. Useful when creating a set by deriving its assets
            from other sets.
        expected_count:
            Estimated count of the number of assets this set is expected to contain.
        tags:
            Labels associated with the set.  Allows for easy set search.
        id:
            Optional unique id for set (needs to be a string)
        aux_metadata:
            Optional dictionary of key and values to be added to sets metadata
        is_primary:
            If true, Gives the set an additional "Primary" tag for easy set sorting.  Otherwise, does nothing.
        raise_if_set_exists:
            Raises a SetsError if the name parameter matches an existing set.

        Returns
        -------
        str
            The name of the successfully created set.

        Raises
        ------
        SetsError
            If raise_if_set_exists is True, then will raise an error if the given set name matches an
            existing set.

        """
        same_name_sets = self.get_asset_manager(asset_type=AssetsConstants.SETS_ASSET_ID).search_assets(
            filters={"name": [name]}
        )
        if same_name_sets:
            if raise_if_set_exists:
                raise SetsError("set name {} already exists".format(name))
            else:
                logger.warning("set name {} already exists. Doing nothing!".format(name))
                return same_name_sets[0]

        tags = tags or []

        if is_primary:
            tags.append(SetTags.PRIMARY_SET_TAG)

        if origin_set_id:
            assert self.get_asset_manager(
                asset_type=AssetsConstants.SETS_ASSET_ID).exists(
                id=origin_set_id), "Origin set id {} does not exist".format(origin_set_id)

        options = {
            "assets_type": asset_type,
            "name": name,
            "origin_set_id": origin_set_id,
            "expected_count": expected_count,
            "tags": tags or []
        }
        if id:
            options["id"] = id
        if aux_metadata:
            options["auxiliary"] = aux_metadata

        resp = self.requests.post(
            "sets/add/",
            trailing_slash=True,
            json=options
        )

        if not resp.ok:
            raise ResponseError(
                "Could not create the set: {}".format(
                    resp.content))

        id = resp.json()["id"]
        return id

    def get_set_id_by_name(
            self,
            name: str) -> str:
        """Get set with a its name

            Parameters
            ----------
            name:
                The name of the set.

            Returns
            -------
            str
                The ID of the set
            """
        set_ids = self.get_asset_manager(asset_type=AssetsConstants.SETS_ASSET_ID).search_assets(
            filters={"name": name})
        if len(set_ids) < 1:
            raise SetsError(f"could not find a set with name {name}")
        elif len(set_ids) == 1:
            set_id = set_ids[0]
        else:
            raise SetsError(f"Found more than 1 set with name {name}")

        return set_id

    def create_annotation_instruction(
            self,
            name: str,
            key: str,
            annotator: str,
            annotation_type: str,
            payload: dict,
            media_type: str = AssetsConstants.IMAGES_ASSET_ID,
            description: Optional[str] = None) -> str:
        """Create an annotation instruction.

        Annotation instructions hold the configurations for annotating assets with external annotators.
        When executing an operation of type "annotation", the relevant annotation instruction card is parsed.

        Parameters
        ----------
        name:
            Name of the annotation instruction to create.
        key:
            Authentication key to send to Scale or SuperAnnotate.
        annotator:
            Name of the annotator to use.  Choose an option from
            scenebox.constants.AnnotationProviders.VALID_PROVIDERS.
        annotation_type:
            Name of the annotation type to use.  Choose an option from
            scenebox.constants.AnnotationTypes.VALID_TYPES.
        payload:
            Configuration for the given annotator.
        media_type:
            Media type to send to the annotator.  Choose an option from
            scenebox.constants.AssetConstants.VALID_TYPES.
        description:
            A brief description of the annotation instruction's purpose, what it aims to
            accomplish, etc.

        Returns
        -------
        str
            The ID of the created annotation instruction.

        Raises
        ------
        ResponseError:
            If the annotation instruction could not be created.

        """
        options = {
            "name": name,
            "key": key,
            "annotator": annotator,
            "type": ConfigTypes.ANNOTATION_INSTRUCTION,
            "annotation_type": annotation_type,
            "config": payload,
            "media_type": media_type,
            "description": description,
        }
        resp = self.requests.post(
            "configs/add/",
            trailing_slash=True,
            json=options)

        if not resp.ok:
            raise ResponseError(
                "Could not create the annotation_instruction: {}".format(
                    resp.content))

        id = resp.json()["id"]
        return id

    def delete_annotation_instruction(self, annotation_instruction_id: str):
        """Delete an existing annotation instruction.

        Parameters
        ----------
        annotation_instruction_id:
            The ID of the annotation instruction to delete.

        Raises
        ------
        ResponseError:
            If the annotation instruction could not be deleted.

        """
        resp = self.requests.delete(
            "configs/meta/{}".format(annotation_instruction_id),
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not delete the annotation_instruction: {}".format(
                    resp.content))

    def create_config(
            self,
            name: str,
            type: str,
            config: dict,
            description: Optional[str] = None,
            id: Optional[str] = None,
            **kwarg) -> str:
        """Create a config.

        Parameters
        ----------
        name:
            Name of the configuration.
        type:
            Type of the config to create.  Choose an option from scenebox.constants.ConfigTypes.VALID_TYPES.
        config:
            Body of the config to create.  Form dependent on the configuration needs.
        description:
            A brief description of the config's purpose, settings, etc. Same as the payload argument for
            ``self.create_annotation_instruction``.
        id:
            optional unique identifier
        **kwarg:
            Any other misc. kwargs to save into the config.

        Returns
        -------
        str
            The ID of the created config.

        """
        options = kwarg
        options.update({
            "name": name,
            "type": type,
            "config": config,
            "description": description,
        })
        if id:
            options.update({"id": id})

        resp = self.requests.post(
            "configs/add/",
            trailing_slash=True,
            json=options)

        if not resp.ok:
            raise ResponseError(
                "Could not create the config: {}".format(
                    resp.content))

        id = resp.json()["id"]
        return id

    def delete_config(self, config_id: str):
        """Delete a config.

        Parameters
        ----------
        config_id:
            The ID of the config to delete.

        Raises
        ------
        ResponseError:
            If the config could not be deleted.

        """

        resp = self.requests.delete(
            "configs/meta/{}".format(config_id),
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not delete the config_id: {}".format(
                    resp.content))

    def get_config(self, config_id: str, complete_info=False) -> dict:
        """Get config metadata.

        Parameters
        ----------
        config_id:
            The ID of the config to receive the metadata of.
        complete_info:
            If True, returns the the entire metadata of the config
            (with the config parameters contained inside).  Otherwise,
            only returns the config parameters.

        Returns
        -------
        dict
            The metadata and/or parameters of the desired config.

        Raises
        ------
        ResponseError:
            If the config metadata could not be obtained.
        """
        resp = self.requests.get(
            "configs/meta/{}".format(config_id),
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not get the config metadata: {}".format(
                    resp.content))

        if complete_info:
            return resp.json()
        else:
            return resp.json().get("config", {})

    def set_lock(self, set_id: str) -> bool:
        """Lock a set.

        Locks a set from changes. Useful for protecting a set (i.e. marks a set as "in use")
        when performing a data operation on a set's assets.

        Parameters
        ----------
        set_id:
            The ID of the set to lock.

        Returns
        -------
        bool
            Always returns True.

        Raises
        ------
        HTTPError:
            If a server or client error occurs.

        """

        resp = self.requests.put("sets/{}/lock".format(set_id))
        resp.raise_for_status()

        return True

    def set_unlock(self, set_id: str) -> bool:
        """Unlocks a set.

        Releases a set from protection/external changes.

        Parameters
        ----------
        set_id:
            The ID of the set to unlock.

        Returns
        -------
        bool
            Always returns True.

        Raises
        ------
        HTTPError:
            If a server or client error occurs.

        """
        resp = self.requests.delete("sets/{}/lock".format(set_id))
        resp.raise_for_status()

        return True

    def set_is_locked(self, set_id: str) -> bool:
        """Check the lock status of a set.

        Parameters
        ----------
        set_id:
            The ID of the set to check the lock status of.

        Returns
        -------
        bool
            Returns True if the set is locked.
            Otherwise, returns False if the set is not locked.

        Raises
        ------
        HTTPError:
            If a server or client error occurs.

        """
        resp = self.requests.get("sets/{}/lock".format(set_id))
        resp.raise_for_status()

        return resp.json().get("locked")

    def delete_set(
            self,
            set_id: str,
            delete_content: bool = False,
            wait_for_completion: bool = False) -> str:

        """Delete a set.

        Parameters
        ----------
        set_id:
            The ID of the set to delete.
        delete_content:
            Should the content of the set be deleted or just the set itself. Set to False by default
            meaning the content wont be deleted.
        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.

        Returns
        -------
        str
            The ID of the Job that attempts to delete the set.

        """
        params = {"delete_content": delete_content}
        resp = self.requests.delete("sets/{}".format(set_id), params=params)
        resp.raise_for_status()
        if wait_for_completion:
            job_id = resp.json()["job_id"]
            self._wait_for_job_completion(job_id)
        return resp.json().get("job_id")

    def split_set(
            self,
            set_id: str,
            percentages_or_sections: Union[int, List[float]],
            subset_names: Optional[List[str]] = None,
            random_seed: Optional[int] = 42,
            wait_for_completion: bool = False) -> str:

        """ Split a set into subsets by randomly sampling and distributing constituent assets.

        Parameters
        ----------
        set_id:
            The ID of the parent set to split.

        percentages_or_sections:
            percentages_or_sections is an integer n or a list of floating point values.
            If percentages_or_sections is an integer n, the input set is split into n sections.
            If input set size is divisible by n, each section will be of equal size,
            input_set_size / n. If input set size is not divisible by n, the sizes of the
            first int(input_set_size % n) sections will have size
            int(input_set_size / n) + 1, and the rest will have size int(input_set_size / n).

            If percentages_or_sections is a list of floating point values, the input set is
            split into subsets with the amount of data in each split i as
            floor(percentage_or_sections[i] * input set size). Any leftover data due to the floor
            operation is equally redistributed into len(percentage_or_sections) subsets according
            to the same logic as with percentages_or_sections being an integer value.

        subset_names:
            Names for the subsets to be created. Subsets corresponding to the provided subset names
            should not previously exist.

        random_seed:
            Optional. Set a different seed to get a different random subsample of the data in each split.

        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.
            If numof splits is greater than 5, wait_for_completion cannot be set to False.

        Returns
        -------
        str
            The job ID that carried out the split set job.

        """
        split_sets_payload = {"set_id": set_id,
                              "random_seed": random_seed,
                              "wait_for_completion": wait_for_completion}

        if subset_names:
            split_sets_payload["subset_names"] = subset_names
        if isinstance(percentages_or_sections, list):
            split_sets_payload["percentages"] = percentages_or_sections
        if isinstance(percentages_or_sections, int):
            split_sets_payload["sections"] = percentages_or_sections

        resp = self.requests.post(
            "sets/split_sets/",
            trailing_slash=True,
            json=split_sets_payload)

        if wait_for_completion:
            job_id = resp.json()["job_id"]
            self._wait_for_job_completion(job_id)

        return resp.json()["job_id"]

    def get_set_status(self, set_id: str) -> dict:
        """Get the status of a set.

        Parameters
        ----------
        set_id:
            The ID of the set to get the status of.

        Returns
        -------
        dict
            The full status of the desired set.

        Raises
        ------
        HTTPError:
            If a server or client error occurs.

        """
        resp = self.requests.get("sets/{}/status/".format(set_id))
        resp.raise_for_status()
        return resp.json()

    def add_assets_to_set(
            self,
            set_id: str,
            search: Optional[dict] = None,
            ids: Optional[list] = None,
            limit: Optional[int] = None,
            wait_for_availability: bool = True,
            timeout: int = 30,
            wait_for_completion: bool = False,
    ) -> str:
        """Add assets to a set.

        Add assets to a set either with a search query, or by IDs.  Utilize only one of

        Parameters
        ----------
        search:
            Query to locate the data subset of interest.  Filters through existing
            assets according to the dictionary passed.
        ids:
            IDs of the assets to add to the given set.
        set_id:
            The ID of the set to add assets to.
        limit:
            The limit of the number of additions.  If the limit is reached,
            randomly down-sample the list of assets to add.
        wait_for_availability:
            If True and the specified set is locked, waits until ``timeout`` for the set
            to unlock.  Otherwise, if False, raises a SetsError if the set is locked.
        timeout:
            If ``wait_for_availability`` is True, represents the maximum amount of time
            for a set to unlock.  Otherwise, has no effect.
        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.

        Returns
        -------
        str
            ID of the Job that runs/ran the add assets job.

        Raises
        ------
        SetsError
            If ``wait_for_availability`` is False, and the specified set is locked.
            If neither ``ids`` or ``search`` are passed.
        TimeoutError
            If ``wait_for_availability`` is True, and timeout is reached before the desired
            set is unlocked.
        ResponseError
            If assets could not be added to the desired set.
        """
        if search is None and not ids: # either ids are not passed or empty
            return "no operations"

        if self.set_is_locked(set_id):
            if wait_for_availability:
                logger.info(
                    "Set {} is locked, waiting up to {} seconds to add assets".format(set_id, timeout))
                t_start = time.time()
                while True:
                    time.sleep(1)
                    if time.time() - t_start > timeout:
                        raise TimeoutError(
                            "Timeout waiting for set {} to unlock".format(set_id))
                    if not self.set_is_locked(set_id):
                        break
            else:
                raise SetsError("Set {} is locked".format(set_id))

        if search is not None:
            if limit:
                params = {"limit": limit}
            else:
                params = None
            resp = self.requests.post(
                "sets/{}/add_assets_query/".format(set_id),
                trailing_slash=True,
                json=search,
                params=params)
        elif ids is not None:
            assets_payload = {"asset_list": ids}
            resp = self.requests.post(
                "sets/{}/add_assets_list/".format(set_id),
                trailing_slash=True,
                json=assets_payload)
        else:
            raise SetsError(
                "Either ids or search should be specified for sets addition")

        if not resp.ok:
            raise ResponseError(
                "Could not add assets to set: {}, {}".format(
                    resp.content, resp.reason))

        if wait_for_completion:
            job_id = resp.json()["job_id"]
            self._wait_for_job_completion(job_id)

        return resp.json().get("job_id")

    def remove_assets_from_set(
            self,
            search: Optional[dict] = None,
            ids: Optional[list] = None,
            set_id: Optional[str] = None,
            wait_for_availability: bool = True,
            timeout: int = 30,
            wait_for_completion: bool = False,
    ) -> str:
        """Remove assets from a set either by query or by IDs.

        Parameters
        ----------
        search:
            Query to locate the data subset of interest.  Filters through existing
            assets according to the dictionary passed.
        ids:
            IDs of the assets to add to the given set.
        set_id:
            The ID of the set to add assets to.
        wait_for_availability:
          If True and the specified set is locked, waits until ``timeout`` for the set
          to unlock.  Otherwise, if False, raises a SetsError if the set is locked.
        timeout:
            If ``wait_for_availability`` is True, represents the maximum amount of time
            for a set to unlock.  Otherwise, has no effect.
        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.

        Returns
        -------
        str
            The ID of the job that runs/ran the Job to remove assets from a set.
        """

        if search is None and ids is None:
            raise ValueError(
                "Either a search query or a list of ids must be provided")

        if self.set_is_locked(set_id):
            if wait_for_availability:
                t_start = time.time()
                while True:
                    time.sleep(1)
                    if time.time() - t_start > timeout:
                        raise TimeoutError(
                            "Timeout waiting for set {} to unlock".format(set_id))
                    if not self.set_is_locked(set_id):
                        logger.info(
                            "Set {} is locked, waiting 1s to remove assets".format(set_id))
                        break
            else:
                raise SetsError("Set {} is locked".format(set_id))

        if search:
            resp = self.requests.post(
                "sets/{}/remove_assets_query/".format(set_id),
                trailing_slash=True,
                json=search)
        else:
            assets_payload = {"asset_list": ids}
            resp = self.requests.post(
                "sets/{}/remove_assets_list/".format(set_id),
                trailing_slash=True,
                json=assets_payload)

        if not resp.ok:
            raise ResponseError(
                "Could not remove assets from set: {}, {}".format(
                    resp.content, resp.reason))

        if wait_for_completion:
            job_id = resp.json()["job_id"]
            self._wait_for_job_completion(job_id)

        return resp.json().get("job_id")

    def assets_in_set(self, set_id: Optional[str] = None) -> List[str]:
        """List assets within a set.

        Parameters
        ----------
        set_id:
            The ID of the set to list assets from.

        Returns
        -------
        List[str]
            A list of the IDs of the assets contained in the specified set.
        """
        return self.search_within_set(set_id=set_id, show_meta=False)

    def search_within_set(
            self,
            set_id: str,
            search: Optional[dict] = None,
            show_meta: bool = True) -> List:
        """Search for assets within a set.

        Parameters
        ----------
        search:
            Search query to send to the endpoint.  Filters through existing
            sets according to the dictionary passed.
        set_id:
            The ID of the set to search.
        show_meta:
            If True, returns the metadata of each asset in the set.
            Otherwise, simply lists the IDs of each asset in the set.

        Returns
        -------
        List
            Contains asset IDs and/or metadata for the assets in the given set.

        Raises
        ------
        ResponseError
            If the search could not be performed.
        """
        search = search or {}
        if show_meta:
            resp = self.requests.post(
                "sets/{}/list_assets_meta/".format(set_id),
                trailing_slash=True,
                json=search)
        else:
            resp = self.requests.post(
                "sets/{}/list_assets/".format(set_id),
                trailing_slash=True,
                json=search)

        if not resp.ok:
            raise ResponseError(
                "Could not perform the search: {}".format(
                    resp.content))

        return resp.json()["results"]

    def zip_set(self, set_id: str) -> Tuple[str, str]:
        """Create a zipfile of a set.

        Parameters
        ----------
        set_id:
            The ID of the set to zip.

        Returns
        -------
        (str, str)
             The ID of the job that zipped the set,
             The zipfile ID of the zipped set).

        Raises
        -----
        ValueError
            If no set ID is provided.

        """

        resp = self.requests.post(
            "sets/{}/zip_all_assets/".format(set_id),
            trailing_slash=True)
        resp.raise_for_status()
        return resp.json().get("job_id"), resp.json().get("zip_id")

    def compare_sets(self,
                     sets: List[str],
                     index_name: str,
                     metric_type: Optional[str] = None,
                     metric_params: Optional[Dict] = None,
                     wait_for_completion: bool = True
                     ) -> str:
        """Compare sets based on a given metric_type in an embedding space with given index_name.

        Parameters
        ----------
        sets:
            The IDs of the sets to compare with each other.

        index_name:
            The name of the embedding space.

        metric_type:
            The metric type that the comparison is based on; if not given, default value is wasserstein.

        metric_params:
            key-values of any parameters that are needed to calculate the metric;
            if not given, default values for num_projections and num_seeds are 25 and 50, respectively,
            for wasserstein distance calculation.

        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.

        Returns
        -------
        str
             The ID of the job that compared sets.

        Raises
        -----
        ValueError
            If sets is empty or contains only one set id.
            If index_name is not provided.

        """
        payload = {
            "sets": sets,
            "index_name": index_name
        }

        if metric_type:
            payload.update(
                {
                    "metric_type": metric_type
                }
            )
        if metric_params:
            payload.update(
                {
                    "metric_params": metric_params
                }
            )
        resp = self.requests.post(
            "sets_comparisons/compare_sets/",
            trailing_slash=True,
            json=payload)

        if not resp.ok:
            raise ResponseError(
                "{} ::: {} with token::: {}".format(
                    resp.reason, resp.content, self.auth_token))

        job_id = resp.json().get("job_id")

        if wait_for_completion:
            self._wait_for_job_completion(job_id)

        return job_id

    def get_sets_comparison_matrix(self,
                                   search: Optional[dict] = None,
                                   index_name: Optional[str] = None,
                                   ) -> List[dict]:
        """Get the comparison matrix of an index.

        Parameters
        ----------
        search:
            Query to locate the data subset of interest.  Filters through existing
            assets according to the dictionary passed.
        index_name:
            index_name of the embeddings of interest.

        Returns
        -------
        List[dict]
            The requested comparison matrix.
        """
        payload = {
            "search": search,
            "index_name": index_name
        }

        resp = self.requests.post(
            "sets_comparisons/comparison_matrix/",
            trailing_slash=True,
            json=payload)

        if not resp.ok:
            raise ResponseError(
                "{} ::: {} with token::: {}".format(
                    resp.reason, resp.content, self.auth_token))

        return resp.json()

    def get_performance_metrics(self,
                                comparison_task_id: str,
                                search: Optional[dict] = None,
                                iou_threshold: float = 0.0
                                ) -> Dict[str, Any]:
        """Get performance metrics.

            Get performance metrics including precision, recall, and f1 score for a given search on annotations
            comparisons asset space and iou threshold.

        Parameters
        ----------
        comparison_task_id:
            id of the comparison task to calculate metrics for
        search:
            Query to locate the data subset of interest.  Filters through existing
            annotations comparisons according to the dictionary passed.

            .. code-block:: python

                # Search example
                search = {
                            "filters": [{"field": "sets", "values": ["some_set_id"]}]
                         }

        iou_threshold:
            iou threshold to use in confusion matrix calculation

        Returns
        -------
        Dict[str, Any]
            The requested performance metrics.

            .. code-block:: python

                # Example return
                {
                    "cat": {'precision': 0.75, 'recall': 0.47368421052631576, 'f1': 0.5806451612903226},
                    "dog": {'precision': 0, 'recall': 0, 'f1': N/A}
                }

        """
        aggregations = self.summary_meta(
            asset_type=AssetsConstants.ANNOTATIONS_COMPARISONS_ASSET_ID,
            summary_request={"dimensions": ["comparison_task_id"], "max_size_for_agg": 10000}
        ).get("aggregations")

        assert 0.0 <= iou_threshold <= 1.0, "iou_threshold should be between 0 and 1, {} is given".format(iou_threshold)
        assert aggregations, "comparison_task_id ::: {} doesn't exist".format(comparison_task_id)
        comparison_task_ids = [bucket["key"] for bucket in aggregations[0]["buckets"]]
        assert comparison_task_id in comparison_task_ids, \
            "comparison_task_id ::: {} doesn't exist. Following ids exist; {} ".format(comparison_task_id,
                                                                                       comparison_task_ids)

        search = search or {}
        filters = search.get("filters") or []
        filters.append(
            {
                "field": "comparison_task_id",
                "values": [comparison_task_id]
            }
        )
        search["filters"] = filters
        payload = {
            "search": search,
            "iou_threshold": iou_threshold
        }

        resp = self.requests.post(
            "annotations_comparisons/performance_metrics/",
            trailing_slash=True,
            json=payload)

        if not resp.ok:
            raise ResponseError(
                "{} ::: {} with token::: {}".format(
                    resp.reason, resp.content, self.auth_token))

        return resp.json()

    def get_performance_metrics_per_dimension(
            self,
            comparison_task_id: str,
            dimension: str,
            iou_threshold: float = 0.0,
            search: Optional[dict] = None,
            force_recalculation: bool = False
    ) -> Dict[str, Dict[str, Any]]:
        """Get performance metrics per dimension.

            Get performance metrics including precision, recall, and f1 score per
            existing buckets in a given dimension e.g. image ids.

        Parameters
        ----------
        comparison_task_id:
            id of the comparison task to calculate metrics for
        dimension:
            the dimension for which the performances should be calculated e.g. "id"
        iou_threshold:
            iou threshold to use in confusion matrix calculation
        search:
            Query images to locate the data subset of interest.

            .. code-block:: python

                # Search example:
                search = {
                            "filters": [{"field": "sensor", "values": ["camera_1"]}]
                         }

        force_recalculation:
            If True, cached results are ignored if available.

        Returns
        -------
        Dict[str, Dict[str, Any]]
             A dictionary that has 2 keys; job_id, and performances.

             The job_id key is mapped to the ID of the job that calculated the performances, and the performances key
             is mapped to the resultant performance.

            .. code-block:: python

                # Example return
                {
                    "job_id": "some_job_id",
                        "performances": {
                            "image_id_1": {
                                "cat": {'precision': 0.75, 'recall': 0.47368421052631576, 'f1': 0.5806451612903226},
                                "dog": {'precision': 0, 'recall': 0, 'f1': N/A}
                            },
                            "image_id_2": {
                                "cat": {'precision': 0.25, 'recall': 0.5, 'f1': 0.33333333333},
                                "dog": {'precision': 0.5, 'recall': 1.0, 'f1': 0.66666666666}
                            }
                        }
                    }

        """
        aggregations = self.summary_meta(
            asset_type=AssetsConstants.ANNOTATIONS_COMPARISONS_ASSET_ID,
            summary_request={"dimensions": ["comparison_task_id"], "max_size_for_agg": 10000}
        ).get("aggregations")

        assert 0.0 <= iou_threshold <= 1.0, "iou_threshold should be between 0 and 1, {} is given".format(iou_threshold)
        assert aggregations, "comparison_task_id ::: {} doesn't exist".format(comparison_task_id)
        comparison_task_ids = [bucket["key"] for bucket in aggregations[0]["buckets"]]
        assert comparison_task_id in comparison_task_ids, \
            "comparison_task_id ::: {} doesn't exist. Following ids exist; {} ".format(comparison_task_id,
                                                                                       comparison_task_ids)

        search = search or {}
        summary_request = {"search": search, "dimensions": [dimension]}

        payload = {
            "summary_request": summary_request,
            "iou_threshold": iou_threshold,
            "comparison_task_id": comparison_task_id,
            "force_recalculation": force_recalculation
        }

        resp = self.requests.post(
            "annotations_comparisons/performance_metrics_per_dimension/",
            trailing_slash=True,
            json=payload)

        if not resp.ok:
            raise ResponseError(
                "{} ::: {} with token::: {}".format(
                    resp.reason, resp.content, self.auth_token))

        job_id = resp.json().get("job_id")
        performances = resp.json().get("performances")

        if performances:
            return {
                "performances": performances,
                "job_id": job_id
            }

        self._wait_for_job_completion(job_id)

        payload["force_recalculation"] = False

        resp = self.requests.post(
            "annotations_comparisons/performance_metrics_per_dimension/",
            trailing_slash=True,
            json=payload)
        if not resp.ok:
            raise JobError(
                "job_id is None ::: {} with token::: {}".format(
                    resp.reason, resp.content, self.auth_token))

        return {
            "performances": resp.json().get("performances"),
            "job_id": resp.json().get("job_id")
        }

    def download_zipfile(self,
                         zip_id: str,
                         output_filename: Optional[str] = None) -> Union[str,
                                                                         io.BytesIO]:
        """Download a zipfile into either a bytesIO object or a file.

        Parameters
        ----------
        zip_id:
            The ID of the zipfile to download.
        output_filename:
            The filename to give the downloaded zipfile.

        Returns
        -------
        Union[str, io.BytesIO]
            If output_filename is provided, returns the path where the zipfile was locally saved as str.
            Otherwise, the zipfile is returned directly as a  io.BytesIO object.

        """
        data_bytes = self.get_asset_manager(
            asset_type=AssetsConstants.ZIPFILES_ASSET_ID).get_bytes(
            id=zip_id)
        if output_filename:
            if not output_filename.endswith(".zip"):
                output_filename += ".zip"
            fpath = os.path.join(self.artifacts_path, output_filename)
            with open(fpath, "wb") as f:
                f.write(data_bytes)
            return fpath
        else:
            bytes_file = io.BytesIO(data_bytes)
            return bytes_file

    def download_timeseries(self,
                            search_dic: Optional[Dict] = None,
                            fields: Optional[List[str]] = None) -> dict:
        """Download the timeseries using a search query.

        Parameters
        ----------
        search_dic:
            Query to locate the data subset of interest.  Filters through existing
            assets according to the dictionary passed.
        fields:
            Field names of fields to return from each session.

        Returns
        -------
        dict
            Mapping between session uids, and the returned timeseries data.
        """
        timeseries_data = defaultdict(list)
        json_payload = search_dic or {}
        resp = self.requests.post(
            "session_manager/search/",
            json=json_payload,
            trailing_slash=True)

        if not resp.ok:
            raise ResponseError(
                "{} ::: {} with token::: {}".format(
                    resp.reason, resp.content, self.auth_token))
        if fields and TIMESTAMP_FIELD not in fields:
            fields.append(TIMESTAMP_FIELD)
        session_interval_map = resp.json()
        for session_uid, v in session_interval_map.items():
            session_timeseries_data = {}
            intervals = v.get("intervals", [])
            for interval in intervals:
                session_timeseries_data["start_time"] = interval[0]
                session_timeseries_data["end_time"] = interval[1]
                search_dic["time_range"] = {
                    "start_time": interval[0],
                    "end_time": interval[1]
                }
                field_data = self.get_field_data(session_uid=session_uid,
                                                 search_dic=search_dic,
                                                 fields=fields)

                for field, data in field_data.items():
                    if field != TIME_INDEX_FIELD:
                        session_timeseries_data[field] = data
                timeseries_data[session_uid].append(session_timeseries_data)
        return dict(timeseries_data)

    def zip_set_and_download(self,
                             set_id: Optional[str] = None,
                             filename: Optional[str] = None) -> Union[str,
                                                                      io.BytesIO]:

        """Zip and download an existing set.

        The downloaded zip file contains several subfolders/files encapsulating the logged data on SceneBox.
        More specifically, this includes the following:
        -  Asset files with their original extension (images/videos/LIDARs, etc.)
        -  Asset metadata in .json format
        -  Annotation data in .json format (if available)

        Parameters
        ----------
        set_id:
            Set name of the set to zip and download
        filename:
            Name of the downloaded zip folder

        Returns
        -------
        Union[str, io.BytesIO]
            If filename is provided, returns the path where the zipfile was locally saved as str.
            Otherwise, the zipfile is returned directly as a  io.BytesIO object.

        Raises
        ------
        ValueError
            If no set_id is provided.
        """
        job_id, zip_id = self.zip_set(set_id)
        self._wait_for_job_completion(job_id)
        return self.download_zipfile(zip_id, output_filename=filename)

    def get_asset_manager(
            self,
            asset_type: str
    ) -> AssetManagerClient:
        """Set asset_manager state.

        Set the asset_manager state to access particular assets. This is often used in chaining:
        Eg. client.with_asset_state("images", True).search_files({})

        Parameters
        ----------
        asset_type:
            Desired AssetManagerClient asset type.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        Returns
        -------
        AssetManagerClient
            The AssetManagerClient associated with the specified asset.

        """
        key = asset_type + (self.auth_token or "")
        if key not in self.amc_cache:
            self.amc_cache[key] = AssetManagerClient(
                asset_type=asset_type,
                asset_manager_url=self.asset_manager_url,
                auth_token=self.auth_token,
                kv_store=self.kv_store,
                num_threads=self.num_threads,
            )
        return self.amc_cache[key]

    def get_job_manager(
            self,
            job_id: Optional[str] = None
    ) -> JobManagerClient:
        """Set asset_manager state.

        Set the asset_manager state to access particular assets. This is often used in chaining:
        Eg. client.with_asset_state("images", True).search_files({})

        Parameters
        ----------
        job_id:
            Optional. A job id for the job to manage. If not provided, a job manager is created
            with a guid for job id.
        Returns
        -------
        AssetManagerClient
            The AssetManagerClient associated with the specified asset.

        """
        job_manager = JobManagerClient(job_id=job_id,
                                       asset_manager_url=self.asset_manager_url,
                                       auth_token=self.auth_token)

        return job_manager

    def get_streamable_set(
            self,
            set_id: str,
            force_recreate: bool = False,
            shard_size: int = 50000,
    ) -> StreamableSet:
        """A StreamableSet is a SceneBox object that can be used to build dataloaders for a set.
        A dataloader enables fetching batches of tuples of data such as (images, annotations) from scenebox
        that can be used to in a machine learning models's training or testing loop.

        Parameters
        ----------
        set_id:
            String. ID of the set that you want to stream.

        force_recreate:
            Boolean. Default False. Flag for mandatory update of the StreamableSet object's data repository.

        shard_size:
            Integer. Maximum number of assets in a shard. Data will be split into multiple
            shards of shard_size.

        Returns
        -------
        StreamableSet
            A StreamableSet object that supports pytorch dataloader methods.

        """
        streamable_set = StreamableSet(set_id=set_id,
                                       sec_requests=self.requests,
                                       sec_wait_for_completion_func=self._wait_for_job_completion,
                                       force_recreate=force_recreate,
                                       zipfiles_amc=self.get_asset_manager(asset_type=AssetsConstants.ZIPFILES_ASSET_ID),
                                       sets_amc=self.get_asset_manager(asset_type=AssetsConstants.SETS_ASSET_ID),
                                       shard_size=shard_size)

        return streamable_set

    def register_rosbag_session(
            self,
            session_name: str,
            session_directory_path: Optional[str] = None,
            rosbag_ids: Optional[List[str]] = None,
            config_name: Optional[str] = None,
            wait_for_completion: bool = True,
    ) -> Tuple[str, str]:
        """Register a rosbag session with the SceneEngine.

        Parameters
        ----------
        session_name:
            Name of the session.
        session_directory_path:
            Local path (on ros-extractor) to a session directory.
        rosbag_ids:
            List of rosbag IDs belonging to the session.
        config_name:
            Name of the session configuration file.
        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.

        Returns
        -------
        Tuple[str, str]
            the Job ID that carried out the indexing job, and the session UID of the created session.
        """
        if session_directory_path is None and rosbag_ids is None:
            # Insufficient arguments provided
            raise ValueError(
                "Must provide either session_directory_path or rosbag_ids")

        json_payload = {
            'session_name': session_name,
            'session_directory_path': session_directory_path,
            'source_data': rosbag_ids,
            'session_configuration': config_name,
        }

        resp = self.requests.post(
            "indexing/register_rosbag_session/",
            trailing_slash=True,
            json=json_payload)

        job_id = resp.json()["job_id"]

        if wait_for_completion:
            self._wait_for_job_completion(job_id)

        session_uid = resp.json()["session_uid"]

        return job_id, session_uid

    def get_session_resolution_status(self, session_uid: str) -> str:
        """Get the status of the session resolution task (if it exists).

        Parameters
        ----------
        session_uid:
            The session uid to get the session resolution status of.

        Returns
        -------
        str
            The session resolution status.
        """
        resp = self.requests.get(
            "session_manager/resolution_status/{}".format(session_uid),
            trailing_slash=False
        )
        return resp.json()['status']

    def get_searchable_field_statistics(self, asset_type: str) -> dict:
        """Get the metadata searchable field statistics for a certain asset type.

        Parameters
        ----------
        asset_type:
            The asset type to receive the searchable field statistics of.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        Returns
        -------
        dict
            Dictionary with keys of the searchable statistics, and values of the
            min/max/count/defaults for that statistic.

        """
        return self.requests.get(
            route=join(
                asset_type,
                'meta',
                'searchable_field_statistics'),
            trailing_slash=True).json()

    def get_metadata(
            self,
            id: str,
            asset_type: str,
            with_session_metadata: bool = False) -> dict:
        """Get the metadata of an asset.

        Parameters
        ----------
        id:
            The ID of the asset to get metadata from.
        asset_type:
            The asset type of the asset to get metadata from.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        with_session_metadata:
            If True and the asset belongs to a session, also return session entities

        Returns
        -------
        dict
            The asset metadata.

        """
        if with_session_metadata is False:
            return self.get_asset_manager(
                asset_type=asset_type).get_metadata(id)
        else:
            resp = self.requests.get(
                route=join(
                    asset_type,
                    'meta',
                    id),
                trailing_slash=False,
                params={'with_session_metadata': True}
            )
            if not resp.ok:
                raise ResponseError(
                    "{} ::: {} with token::: {}".format(
                        resp.reason, resp.content, self.auth_token))
            return resp.json()

    def compress_images(self,
                        ids: List[str],
                        desired_shape: Optional[Tuple[int,
                                                      ...]] = None,
                        thumbnail_tag: Optional[str] = None,
                        use_preset: Optional[str] = None) -> Optional[str]:
        """Compress a list of images.

        Either specify desired_shape or use_preset to compress an image.

        Parameters
        ----------
        ids:
            The IDs of the images to compress.
        desired_shape:
            Specifies the desired output shape. Not used when use_preset is set.
        thumbnail_tag:
            Tag of the thumbnail to be created. Not used when use_preset is set.
        use_preset:
            Use a preset configuration for desired_shape & thumbnail tag.
            Must be included inside the config.

        Returns
        -------
        str
            The ID of the job that carries out the image compression.

        """
        resp = self.requests.post(
            "images/compress_images/",
            trailing_slash=True,
            json={
                "ids": ids,
                "desired_shape": desired_shape,  # h x w x ..
                "thumbnail_tag": thumbnail_tag,
                "use_preset": use_preset,
            }
        )

        job_id = resp.json().get("job_id")

        return job_id

    def compress_videos(self,
                        ids: List[str],
                        desired_shape: Optional[Tuple[int,
                                                      ...]] = None,
                        thumbnail_tag: Optional[str] = None,
                        use_preset: Optional[str] = None,
                        wait_for_completion: bool = False) -> str:
        """Compress a list of videos.

            Either specify desired_shape or use_preset to compress a video.

            Parameters
            ----------
            ids:
                The IDs of the videos to compress.
            desired_shape:
                Specifies the desired output shape. Not used when use_preset is set.
            thumbnail_tag:
                Tag of the thumbnail to be created. Not used when use_preset is set.
            use_preset:
                Use a preset configuration for desired_shape & thumbnail tag.
                Must be included inside the config.
            wait_for_completion:
                should wait for completion?

            Returns
            -------
            str
                job id of the compression

        """
        resp = self.requests.post(
            "videos/compress_videos/",
            trailing_slash=True,
            json={
                "ids": ids,
                "desired_shape": desired_shape,  # h x w x ..
                "thumbnail_tag": thumbnail_tag,
                "use_preset": use_preset
            }
        )

        job_id = resp.json()["job_id"]

        if wait_for_completion:
            self._wait_for_job_completion(job_id)

        return job_id

    def compress_lidars(self,
                        ids: List[str],
                        skip_factors: Optional[List[int]] = None,
                        gzip_compress: bool = True
                        ) -> dict:
        """Compress a list of videos.

        Either specify desired_shape or use_preset to compress a lidar.

        Parameters
        ----------
        ids:
            The IDs of the LIDARs to compress.
        skip_factors:
            Determines how many LIDAR points to skip.  Each point listed creates a new thumbnail.
            Defaults to [1, 10, 100].
        gzip_compress:
            Default True. Store a gzip compressed version of the lidars.
            Allows quicker loading on the webapp.

        Returns
        -------
        dict
            The job ID of the Job that carries out the LIDAR compression.

        """
        skip_factors = skip_factors or [1, 10, 100]
        resp = self.requests.post(
            "lidars/compress_lidars/",
            trailing_slash=True,
            json={
                "ids": ids,
                "skip_factors": skip_factors,
                "gzip_compress": gzip_compress
            }
        )

        return resp.json()

    def concatenate_videos(
            self,
            ids: List[str],
            output_video_id: str,
            video_metadata: dict,
            job_id: Optional[str] = None) -> dict:
        """Concatenate a list of videos into a single video.

        Parameters
        ----------
        ids:
            The IDs of the videos to concatenate.
        output_video_id:
            The ID of the concatenated video produced.
        video_metadata:
            Metadata of the concatenated video produced.
        job_id:
            If provided, creates a job with the given job_id.  Otherwise, automatically generates a job ID.

        Returns
        -------
        dict
            The job ID of the Job that carries out the video concatenation.

        """
        resp = self.requests.post(
            "videos/concatenate_videos/",
            trailing_slash=True,
            json={
                "ids": ids,
                "output_video_id": output_video_id,
                "video_metadata": video_metadata,
                "job_id": job_id
            }
        )

        return resp.json()

    @deprecated("Use `add_annotations` instead")
    def add_annotation(self,
                       annotation: Annotation,
                       update_asset: bool = True,
                       buffered_write: bool = False,
                       replace_sets: bool = False,
                       add_to_cache: bool = False,
                       annotation_to_objects: bool = False,
                       remove_asset_repeated_annotations: bool = False
                       ):

        """Add a single annotation.

        Add an annotation using a class from the ``scenebox.models.annotation`` module.

        Parameters
        ----------
        annotation:
            The formatted annotation to ingest.
        update_asset:
            If True, updates the metadata of the previously uploaded asset associated with the ``annotation``
        remove_asset_repeated_annotations:
            If update_asset is True and remove_asset_repeated_annotations is True, removes repeated annotation listings
            in the asset's metadata.
        buffered_write:
            If True, ingests annotation in a buffered fashion.
        replace_sets:
            If True and update_asset is False, appends to existing annotation metadata rather than replacing it.
            If False and update_asset is True, replaces existing annotation metadata with the inputted ``annotation``
            metadata.
        add_to_cache:
            If True, corresponding bytes will be added to cache for quick access.
        annotation_to_objects:
            If True, runs the annotations_to_objects async task after adding the annotations.

        """
        if annotation.masks:
            media_owner_organization_id = self.get_asset_manager(
                annotation.media_type).get_metadata(
                id=annotation.asset_id).get("owner")
            annotation.post_upload(annotations_amc=self.get_asset_manager(AssetsConstants.ANNOTATIONS_ASSET_ID),
                                   owner_organization_id=media_owner_organization_id)

        metadata = annotation.to_dic()
        self.get_asset_manager(
            asset_type=AssetsConstants.ANNOTATIONS_ASSET_ID).put_asset(
            metadata=metadata,
            id=annotation.id,
            folder=annotation.provider,
            file_object=annotation.raw_annotation_str,
            uri=annotation.raw_annotation_uri,
            url=annotation.raw_annotation_url,
            wait_for_completion=buffered_write,
            add_to_redis_cache=add_to_cache
        )

        if update_asset:
            self.get_asset_manager(
                asset_type=annotation.media_type).update_metadata(
                id=annotation.asset_id,
                metadata={
                    "annotations": [
                        annotation.id],
                    "annotations_meta": [{
                        "provider": annotation.provider,
                        "id": annotation.id,
                        "type": annotation.annotation_type,
                        "version": annotation.version, }]},
                replace_sets=replace_sets)

            if remove_asset_repeated_annotations:
                self.cleanup_assets_annotation_meta(asset_ids=[annotation.asset_id],
                                                    asset_type=annotation.media_type)

        if annotation_to_objects:
            self.annotations_to_objects(ids=[annotation.id],
                                        create_objects=True)

    def cleanup_assets_annotation_meta(self,
                                       asset_ids: List[str],
                                       asset_type: str):
        """Cleanup annotation lists by removing repeated and non-existent entries in an asset's metadata.
        asset_ids:
            List of asset ids to clean-up.
        asset_type:
            The type of asset.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        """
        asset_ids_chunked = chunk_list(asset_ids, chunk_size=1000)
        asset_amc = self.get_asset_manager(asset_type=asset_type)
        anno_amc = self.get_asset_manager(asset_type=AssetsConstants.ANNOTATIONS_ASSET_ID)

        def perform_cleanup(asset_ids_chunk):
            asset_metadata = asset_amc.get_metadata_in_batch(ids=asset_ids_chunk)

            cleaned_asset_id_metadata_map = {}
            for asset_id, asset_metadatum in asset_metadata.items():
                if not asset_metadatum:
                    continue
                anns_meta = asset_metadatum["annotations_meta"]
                ann_id_meta_dict = {ann_meta['id']: ann_meta for ann_meta in anns_meta}

                # Remove non-existent annotations
                ann_ids_list = list(ann_id_meta_dict.keys())
                exists_status = anno_amc.exists_multiple(ann_ids_list)
                if sum(exists_status) < len(exists_status):
                    non_existent_ids = [i for i, j in enumerate(exists_status) if not j]
                    for non_existent_id in non_existent_ids:
                        del ann_id_meta_dict[ann_ids_list[non_existent_id]]

                cleaned_asset_id_metadata_map[asset_id] = {
                    "annotations": list(ann_id_meta_dict.keys()),
                    "annotations_meta": list(ann_id_meta_dict.values())
                }

            asset_amc.update_metadata_batch(ids=list(cleaned_asset_id_metadata_map.keys()),
                                            metadata=list(cleaned_asset_id_metadata_map.values()),
                                            replace_sets=True)

        run_threaded(func=perform_cleanup,
                     iterable=asset_ids_chunked,
                     num_threads=self.num_threads,
                     desc="cleanup asset's annotations meta")

    def add_annotations(self,
                        annotations: List[Annotation],
                        buffered_write: bool = True,
                        update_asset: bool = True,
                        threading: bool = True,
                        disable_tqdm: bool = False,
                        replace_sets: bool = False,
                        cleanup_annotation_masks: bool = False,
                        remove_asset_repeated_annotations: bool = False,
                        session_uid: Optional[str] = None,
                        annotations_to_objects: bool = False,
                        add_to_cache: bool = False,
                        wait_for_annotations_to_objects_completion: bool = False
                        ):
        """Add several annotations at once.

        Parameters
        ----------
        annotations:
            The annotations to ingest.
        buffered_write:
            If True, ingests annotations in a buffered fashion.
        update_asset:
             If True, updates the metadata of the asset associated with each of the items in ``annotations``.
             Otherwise, does not update the metadata of the associated asset.
        raw_annotations:
            A list of the raw annotation files to ingest.  Gets uploaded as raw files.
        threading:
            If True, uses multithreading to speed up annotations ingestion.  Otherwise, does not use multithreading.
        disable_tqdm:
            If False, uses a progressbar wrapper that calculates and shows the progress of the threading process.
            Otherwise, disables/silences the tqdm progressbar wrapper.
        replace_sets:
            If True and update_asset is False, appends to existing annotation metadata rather than replacing it.
            If False and update_asset is True, replaces existing annotation metadata with the inputted ``annotation``
            metadata.
        cleanup_annotation_masks:
            If True, runs the cleanup_annotation_masks async task after adding all annotations.
        remove_asset_repeated_annotations:
            If update_asset is True and cleanup_asset_meta is True, removes repeated annotation
            listings in the asset's metadata.
        session_uid:
            If provided and annotations_to_objects is set to True, objects entities are added to the session during
            the annotations_to_objects async task.
        annotations_to_objects:
            If True, runs the annotations_to_objects async task after adding the annotations.
        wait_for_annotations_to_objects_completion:
            If True, wait for completion of the annotations_to_objects async task.
        add_to_cache:
            If True, corresponding bytes will be added to cache for quick access.
        """
        CHUNK_SIZE = 100

        def preprocess_and_index(annotations_chunk: List[Annotation],
                                 annotation_ids=None,
                                 media_types=None,
                                 asset_ids=None,
                                 asset_metadata=None):
            annotation_metadata = []
            for annotation in annotations_chunk:
                if annotation.masks:
                    media_owner_organization_id = self.get_asset_manager(
                        annotation.media_type).get_metadata(
                        id=annotation.asset_id).get("owner")
                    annotation.post_upload(
                        annotations_amc=self.get_asset_manager(AssetsConstants.ANNOTATIONS_ASSET_ID),
                        owner_organization_id=media_owner_organization_id)

            raw_annotations_str_chunk = []
            raw_annotations_url_chunk = []
            raw_annotations_uri_chunk = []
            ids = []
            folders = []
            for annotation in annotations_chunk:
                raw_annotations_str_chunk.append(annotation.raw_annotation_str)
                raw_annotations_url_chunk.append(annotation.raw_annotation_url)
                raw_annotations_uri_chunk.append(annotation.raw_annotation_uri)
                annotation_metadata.append(annotation.to_dic())
                annotation_ids.append(annotation.id)  # all annotation ids to be used later
                ids.append(annotation.id)  # subset of annotation ids used in this method call
                folders.append(annotation.provider)
                if update_asset:
                    media_types.append(annotation.media_type)
                    asset_ids.append(annotation.asset_id)
                    asset_metadatum = {
                        "annotations": [
                            annotation.id],
                        "annotations_meta": [{
                            "provider": annotation.provider,
                            "id": annotation.id,
                            "type": annotation.annotation_type,
                            "version": annotation.version}]}
                    asset_metadata.append(asset_metadatum)

            self.get_asset_manager(
                asset_type=AssetsConstants.ANNOTATIONS_ASSET_ID).put_assets_batch(
                metadata=annotation_metadata,
                ids=ids,
                folders=folders,
                file_objects=raw_annotations_str_chunk,
                urls=raw_annotations_url_chunk,
                uris=raw_annotations_uri_chunk,
                wait_for_completion=buffered_write,
                threading=threading,
                disable_tqdm=disable_tqdm,
                add_to_redis_cache=add_to_cache
            )

        if not annotations:
            return

        total_annotations = len(annotations)

        index_rounds = 1
        if threading and CHUNK_SIZE < total_annotations:
            # for 50k and chunk 100 and 50 workers, 50,000//100-->500 chunks --> 500 chunks//50 workers-->10 rounds
            index_rounds = max((total_annotations // CHUNK_SIZE // MAX_THREADS), 1)

        asset_count_per_round = total_annotations // index_rounds  # assets per round

        # at each round, #WORKERS number of workers, will preprocess and index a CHUNK_SIZE of annotations
        # after workers are done, updating images is done
        # DO NO update images in threads -- prone to race condition and version conflict in Elasticsearch
        for i in range(0, index_rounds):
            annotation_ids = []
            media_types = []
            asset_ids = []
            asset_metadata = []

            # logger.debug(f"Indexing annotations {i * asset_count_per_round}-{(i + 1) * asset_count_per_round}")
            annotations_chunks = chunk_list(annotations[i * asset_count_per_round:(i + 1) * asset_count_per_round],
                                            CHUNK_SIZE)
            if threading:
                run_threaded(func=preprocess_and_index, iterable=annotations_chunks,
                             num_threads=MAX_THREADS,
                             disable_tqdm=True,
                             annotation_ids=annotation_ids,
                             media_types=media_types, asset_ids=asset_ids,
                             asset_metadata=asset_metadata)

            else:
                preprocess_and_index(annotations, annotation_ids,
                                     media_types, asset_ids, asset_metadata)

            if update_asset:
                unique_media_type_list = list(set(media_types))
                if len(unique_media_type_list) != 1:
                    raise ValueError("Expected batch of annotations to have the same "
                                     "media type. Got {}".format(unique_media_type_list))

                media_type = unique_media_type_list[0]
                self.get_asset_manager(
                    asset_type=media_type).update_metadata_batch(
                    ids=asset_ids,
                    metadata=asset_metadata,
                    replace_sets=replace_sets)

                if remove_asset_repeated_annotations:
                    self.cleanup_assets_annotation_meta(asset_ids=asset_ids,
                                                        asset_type=media_type)

            # annotation_ids = [annotation.id for annotation in annotations]
            if cleanup_annotation_masks:
                self.cleanup_annotation_masks(ids=annotation_ids)

            if annotations_to_objects:
                self.annotations_to_objects(ids=annotation_ids,
                                            create_objects=True,
                                            session_uid=session_uid,
                                            add_to_session=True,
                                            wait_for_completion=wait_for_annotations_to_objects_completion)

    @staticmethod
    def is_coco_annotation_file_valid(
            file_path: str
    ) -> bool:
        """Tests if a COCO annotation file is valid.

        A valid COCO annotations file is a .json file that only contains keys listed in
        ``scenebox.constants.COCOAnnotations.KEYS``, and values that are all of type list.

        Parameters
        ----------
        file_path:
            Location of the COCO annotation file to validate.

        Returns
        -------
        bool
            Returns True if the COCO annotation file is valid (and can be ingested into SceneBox).
            Otherwise, returns False if the COCO annotation file is invalid.
        """

        with open(file_path, 'r') as f:
            data = json.load(f)

        for key in COCOAnnotations.KEYS:
            if key not in data.keys():
                return False
        for key, value in data.items():
            if not isinstance(value, list) and key in COCOAnnotations.KEYS:
                return False
        return True

    def add_coco_annotations_from_folder(
            self,
            file_path: str,
            provider: str,
            images_set_id: str,
            folder_path: Optional[str] = None,
            version: Optional[str] = None,
            annotation_group: Optional[str] = AnnotationGroups.GROUND_TRUTH,
            session_uid: Optional[str] = None,
            annotations_set_id: Optional[str] = None,
            use_image_id_as_annotation_id: Optional[bool] = False,
            preprocesses: Optional[List[str]] = None,
            thumbnailize_at_ingest: bool = False,
            annotation_to_objects: bool = False,
            wait_for_completion: bool = False
    ):
        """Add several images and/or COCO annotations.

        Upload several images and/or COCO annotations at once with the same local folder path.  This method is best
        used with local images that are all located in the same folder. For images not located in the same folder,
        or images that are not located on your local machine, check out ``self.add_image``.

        Parameters
        ----------
        file_path:
            The filepath to the file that contains the coco annotations.  Must be in json format.
        provider:
            Name of the provider that supplied the annotations.
        folder_path:
            The local path to the folder of images to upload.  If not provided, no new images are uploaded.
        version:
            The version of the model that supplied the annotations.
        annotation_group:
            The group that the annotation belongs to.
            It can be one of ground_truth, model_generated, or other
        session_uid:
            The session to associate with the images to upload.  If folder_path is not provided, has no effect.
        images_set_id:
            The set to add the images to.  If folder_path is not provided, has no effect.
        annotations_set_id:
            The set to add the COCO annotations to
        use_image_id_as_annotation_id:
            If True, appends each annotation's associated image_id onto the annotation's ID.
            Otherwise, makes the annotation IDs ``None``.
        preprocesses:
            Specifies which process to treat the image thumbnails with.
        thumbnailize_at_ingest:
            If True, create thumbnail at ingestion time.  Otherwise, create thumbnails "on the fly".
        annotation_to_objects:
            If True, extract objects from the annotations when adding them.
        wait_for_completion:
            If True, wait for the completion of the annotation to object process
        """

        assert images_set_id, "`images_set_id` is None. Images need to be associated with a set"
        if not self.is_coco_annotation_file_valid(file_path=file_path):
            logger.info(
                "{} is not a valid coco annotations file".format(file_path))
            return

        polygon_annotations = []
        bbox_annotations = []

        with open(file_path, 'r') as file:
            data = json.load(file)

        category_id_name_map = {
            category["id"]: category["name"] for category in data["categories"]}

        file_name_image_id_map = {}
        coco_id_image_id_map = {}
        for image in data["images"]:
            file_name = image["file_name"].split('/')[-1]
            coco_id = image["id"]
            image_id = standardize_name(file_name)
            file_name_image_id_map[file_name] = image_id
            coco_id_image_id_map[coco_id] = image_id

        if folder_path:
            self.add_images_from_folder(
                folder_path=folder_path,
                session_uid=session_uid,
                set_id=images_set_id,
                filename_image_id_map=file_name_image_id_map,
                preprocesses=preprocesses,
                thumbnailize_at_ingest=thumbnailize_at_ingest
            )
        image_id_annotation_map = defaultdict(list)

        for annotation in data["annotations"]:
            annotation_json = {}
            coco_id = annotation["image_id"]
            image_id = coco_id_image_id_map[coco_id]
            annotation_json["bbox"] = annotation["bbox"]
            annotation_json["category_id"] = annotation["category_id"]
            annotation_json["segmentation"] = annotation["segmentation"]
            annotation_json["attributes"] = convert_booleans_to_string(annotation.get("attributes", {}))
            image_id_annotation_map[image_id].append(annotation_json)

        for image_id, annotations in image_id_annotation_map.items():
            bboxes = []
            polygons = []
            for annotation in annotations:
                if annotation["bbox"]:
                    bboxes.append(
                        BoundingBox(x_min=annotation["bbox"][0],
                                    y_min=annotation["bbox"][1],
                                    x_max=annotation["bbox"][0] + annotation["bbox"][2],
                                    y_max=annotation["bbox"][1] + annotation["bbox"][3],
                                    label=category_id_name_map[annotation["category_id"]],
                                    category_id=annotation["category_id"],
                                    attributes=annotation["attributes"]
                                    )
                    )
                if annotation["segmentation"] and annotation["segmentation"][0]:
                    coordinates = []
                    for i in range(0, len(annotation["segmentation"][0]), 2):
                        coordinates.append(
                            (annotation["segmentation"][0][i], annotation["segmentation"][0][i + 1]))
                    polygons.append(
                        Polygon(
                            coordinates=coordinates,
                            label=category_id_name_map[annotation["category_id"]],
                            category_id=annotation["category_id"],
                            attributes=annotation["attributes"]
                        )
                    )
            if bboxes:
                bbox_annotations.append(
                    BoundingBoxAnnotation(
                        provider="{}_bbox".format(provider),
                        version=version,
                        bounding_boxes=bboxes,
                        image_id=image_id,
                        annotation_group=annotation_group,
                        set_id=annotations_set_id,
                        id="{}_bbox.ann".format(image_id) if use_image_id_as_annotation_id else None))
            if polygons:
                polygon_annotations.append(
                    PolygonAnnotation(
                        provider="{}_polygon".format(provider),
                        version=version,
                        polygons=polygons,
                        image_id=image_id,
                        annotation_group=annotation_group,
                        set_id=annotations_set_id,
                        id="{}_polygon.ann".format(image_id) if use_image_id_as_annotation_id else None))

        if polygon_annotations:
            self.add_annotations(annotations=polygon_annotations,
                                 annotations_to_objects=annotation_to_objects,
                                 wait_for_annotations_to_objects_completion=wait_for_completion,
                                 disable_tqdm=True)
            logger.info("{} polygon annotations are added".format(len(polygon_annotations)))
        if bbox_annotations:
            self.add_annotations(annotations=bbox_annotations,
                                 annotations_to_objects=annotation_to_objects,
                                 wait_for_annotations_to_objects_completion=wait_for_completion,
                                 disable_tqdm=True)
            logger.info("{} bbox annotations are added".format(len(bbox_annotations)))

    def delete_annotations(self,
                           ids: Optional[List[str]] = None,
                           search: Optional[dict] = None) -> List[str]:

        """Delete annotations using a list of ids or a search query, and updates metadata of corresponding assets.

        Parameters
        ----------
        ids:
            A list of annotation IDs to delete.
        search:
            Query to locate the data subset of interest.  Filters through existing
            assets according to the dictionary passed.
        Returns
        -------
        job_ids
            A list of job IDs. One for each job that carries out the deletion of a chunk of annotations.
        """
        annotations_amc = self.get_asset_manager(AssetsConstants.ANNOTATIONS_ASSET_ID)

        # Check if any annotations exist
        existing_ids = []
        if ids:
            # Check how many of these ids exist
            exists_statuses = annotations_amc.exists_multiple(ids=ids)
            existing_ids = [ids[i] for i, j in enumerate(exists_statuses) if j]
        elif search:
            existing_ids = annotations_amc.search_assets_large(query=search)

        if not existing_ids:
            logger.warning("No annotations to delete")
            return []

        # Then update the assets annotations meta field in chunks
        annotation_ids_chunked = chunk_list(existing_ids, chunk_size=10000)
        deletion_job_ids = []

        for annotation_ids_chunk in annotation_ids_chunked:
            search = {
                "filters": [{
                    "field": "id",
                    "values": annotation_ids_chunk,
                    "filter_out": False
                }],
                "source_selected_fields": [
                    "media_type", "asset_id"
                ]
            }
            annotations_metadata = annotations_amc.search_meta(query=search, scan=True)
            annotation_media_types = []
            annotation_asset_ids = []
            for annotation_metadatum in annotations_metadata:
                annotation_media_types.append(annotation_metadatum["media_type"])
                annotation_asset_ids.append(annotation_metadatum["asset_id"])

            unique_media_types = deduplicate(annotation_media_types)
            assert len(unique_media_types) == 1, "annotations to be deleted have to be " \
                                                 "from the same asset type. Found {}".format(unique_media_types)

            annotation_media_type = annotation_media_types[0]

            # First delete the annotations themselves
            job_id = annotations_amc.delete_with_list(assets_list=annotation_ids_chunk,
                                                      wait_for_completion=True)
            deletion_job_ids.append(job_id)

            self.cleanup_assets_annotation_meta(asset_ids=annotation_asset_ids,
                                                asset_type=annotation_media_type)

        return deletion_job_ids

    def delete_assets_annotations(self,
                                  asset_ids: List[str],
                                  annotation_type: str,
                                  annotation_group: Optional[str] = None,
                                  annotation_provider: Optional[str] = None,
                                  annotation_version: Optional[str] = None) -> List[str]:

        """Delete annotations using a list of asset ids, and updates metadata of corresponding assets.

        Parameters
        ----------
        asset_ids:
            A list of asset ids to clean the annotations of.
        annotation_type:
            Mandatory annotation type. if set to "all" it deletes everything. Examples: "polygon" "two_d_bounding_box"
        annotation_group:
            Optional annotation group. Example "ground_truth" "model_generated"
        annotation_provider:
            Optional annotation provider.
        annotation_version:
            Optional annotation version.
        Returns
        -------
        job_ids
            A list of job IDs. One for each job that carries out the deletion of a chunk of annotations.
        """

        if len(asset_ids) > 10000:
            raise AssetError("size of assets should be less than 10000")

        annotation_search = {
            "filters": [
                {
                    "field": "asset_id",
                    "values": asset_ids
                }
            ]
        }

        if annotation_type.lower() != "all":
            annotation_search["filters"].append({
                    "field": "annotation_type",
                    "values": [annotation_type]
                })

            if annotation_group:
                annotation_search["filters"].append({
                        "field": "annotation_group",
                        "values": [annotation_group]
                    })

            if annotation_provider:
                annotation_search["filters"].append({
                        "field": "provider",
                        "values": [annotation_provider]
                    })

            if annotation_group:
                annotation_search["filters"].append({
                        "field": "version",
                        "values": [annotation_version]
                    })

        return self.delete_annotations(search=annotation_search)

    def remove_annotation_sources(self,
                                  annotation_sources: List[dict],
                                  asset_type: str,
                                  asset_filters: Optional[dict] = None,
                                  wait_for_completion: bool = True) -> str:

        """Delete annotations using a list of ids or a search query, and updates metadata of corresponding assets.

        Parameters
        ----------
        annotation_sources:
            A list of dictionaries. Each dictionary defines an annotation source with the mandatory
            field: `provider` and optional fields: `version`, `annotation_type`, `annotation_group`.
            Can be collected from the `get_annotation_sources` method.
        asset_type:
            Asset media type for annotations provided by all annotation_sources.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        asset_filters:
            Query to locate the data subset of interest.  Filters through existing
            assets according to the dictionary passed.
        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.
            Default is True.
        Returns
        -------
        job_id
            The job ID of the Job that carries out the deletion of annotations.
        """

        # Validate annotation_sources
        assert annotation_sources and len(annotation_sources) > 0
        assert asset_type and asset_type in AssetsConstants.VALID_ASSETS

        json_resquest = {
            "annotation_sources": annotation_sources,
            "asset_type": asset_type
        }

        if asset_filters is not None:
            json_resquest["asset_filters"] = asset_filters

        resp = self.requests.post(
            "annotations/remove_sources/",
            trailing_slash=True,
            json=json_resquest
        )

        if wait_for_completion:
            job_id = resp.json()["job_id"]
            self._wait_for_job_completion(job_id)

        return resp.json()

    def _get_asset_response_model(self, asset_type: str):
        if asset_type not in AssetsConstants.VALID_ASSETS:
            raise ValueError("Invalid asset type {}".format(asset_type))
        return self.requests.get(
            route=join(asset_type, 'meta', 'response_model'),
            trailing_slash=True
        ).json()

    def add_session(self,
                    session_name: str,
                    session_type: str = SessionTypes.GENERIC_SESSION_ID,
                    set_id: Optional[str] = None,
                    resolution: Optional[float] = None,
                    session_aux_metadata: Optional[dict] = None,
                    status: str = SessionStatuses.READY,
                    raise_if_session_exists: bool = False) -> str:
        """Add a session.

        Parameters
        ----------
        session_name:
            The name to give to the session.
        session_type:
            The session type to give to the session. Choose from ``scenebox.constants.SessionTypes``.
        set_id:
            The session set to add the session to.
        resolution:
            The resolution at which to sample events on.  Measured in seconds.
            Ensure you choose a small enough resolution that none of your events get aliased to occur at a lower
            frequency than expected.
        session_aux_metadata:
            session auxiliary metadata including any metadata that are not primary on SceneBox
            and user wants to search sessions with
            Example:
                {
                    "key_1": 1,
                    "key_2": 1.0,
                    "key_3": "1",
                    "key_4": ["abc", "def"],
                    "key_5": {"a": 1, "b": 2}
                }
        status:
            Session status. By default, this is READY but can be IN PROGRESS as well.
        raise_if_session_exists:
            Raises a SessionError if the name parameter matches an existing set.
        Returns
        -------
        str
            The session UID of the added session.

        """
        same_name_sessions = self.get_asset_manager(asset_type=AssetsConstants.SESSIONS_ASSET_ID).search_assets(
            filters={"session_name": [session_name]}
        )

        if same_name_sessions:
            if raise_if_session_exists:
                raise SessionError("session name {} already exists".format(session_name))
            else:
                logger.warning("session name {} already exists. Doing nothing!".format(session_name))
                return same_name_sessions[0]

        payload = {
            "session_name": session_name,
            "session_type": session_type,
            "session_aux_metadata": session_aux_metadata or {},
            "status": status,
        }

        if set_id:
            set_meta = self.get_asset_manager(asset_type=AssetsConstants.SETS_ASSET_ID).get_metadata(set_id)
            if set_meta["assets_type"] != AssetsConstants.SESSIONS_ASSET_ID:
                raise SetsError("set_id {} is a {} set not a session set".format(set_id, set_meta["assets_type"]))
            payload["set_id"] = set_id

        if resolution:
            payload["resolution"] = resolution
        resp = self.requests.post(
            "sessions/add/",
            trailing_slash=True,
            json=payload)
        if not resp.ok:
            raise ResponseError("{} ::: {}".format(resp.reason, resp.content))
        return resp.json().get("session_uid")

    def slice_session(self,
                      session_uid: str,
                      start_time: Union[datetime, str],
                      end_time: Union[datetime, str],
                      session_name: Optional[str]=None) -> str:
        """slice an existing session with start and end time.

        Parameters
        ----------
        session_uid:
            session id to be sliced
        start_time:
            start time stamp of the slice
        end_time:
            end time stamp of the slice
        session_name:
            Optional new name for the silced_session
        Returns
        -------
        str
            The session UID of the added session.
        """
        payload = {
            "start_time": datetime_or_str_to_iso_utc(start_time),
            "end_time": datetime_or_str_to_iso_utc(end_time)
        }

        if session_name:
            payload["session_name"] = session_name

        resp = self.requests.post(
            f"sessions/{session_uid}/slice/",
            trailing_slash=True,
            json=payload)
        if not resp.ok:
            raise ResponseError("{} ::: {}".format(resp.reason, resp.content))
        return resp.json().get("session_uid")

    def update_time_span(
            self,
            session_uid: str,
            session_start_time: Union[datetime, str],
            session_end_time: Union[datetime, str]) -> dict:
        """Update the start/end times of a session.

        Parameters
        ----------
        session_uid:
            session uid of the session to change the start/end time for.
        session_start_time:
            The new session start time.
        session_end_time:
            The new session end time.

        Returns
        -------
        dict
            The updated metadata of the session after the timespan update.

        """
        logger.info(
            "session_start_time {} and session_end_time {}".format(
                session_start_time,
                session_end_time))
        resp = self.requests.post(
            "sessions/update_time_span/",
            trailing_slash=True,
            json={
                "session_uid": session_uid,
                "session_start_time": datetime_or_str_to_iso_utc(session_start_time),
                "session_end_time": datetime_or_str_to_iso_utc(session_end_time)})
        if not resp.ok:
            raise ResponseError("{} ::: {}".format(resp.reason, resp.content))
        return resp.json()

    def extend_time_span(
            self,
            session_uid: str,
            timestamps: List[Union[str, datetime, None]]) -> dict:
        """Extend the start time and end time of a session based on min/max of a list of timestamps.

        Parameters
        ----------
        session_uid:
            session uid of the session to change the start/end time for.
        timestamps:
            list of timestamps
        Returns
        -------
        dict
            The updated metadata of the session after the timespan update.

        """
        session_metadata = self.get_asset_manager(asset_type=AssetsConstants.SESSIONS_ASSET_ID).get_metadata(
            id=session_uid)
        all_timestamps = copy(timestamps)
        all_timestamps.extend([session_metadata.get("start_time"), session_metadata.get("end_time")])
        clean_timestamps = [str_or_datetime_to_datetime(_) for _ in all_timestamps if _ is not None]
        assert len(all_timestamps) > 1, "need at least 2 valid timestamps tu update sessions"

        return self.update_time_span(session_uid=session_uid,
                                     session_start_time=min(clean_timestamps),
                                     session_end_time=max(clean_timestamps))

    def add_source_data(
            self,
            session_uid: str,
            source_data: List[dict],
            sensors: List[dict],
            replace: Optional[bool] = True) -> dict:
        """Add source data to session metadata.

        Parameters
        ----------
        session_uid:
            The session UID of the session metadata to update.
        source_data:
            The source data to add to the session metadata.
            Example:
            [
                {
                  "sensor": "camera_1",
                  "id": "id_1",
                  "type": "videos"
                },
                {
                  "sensor": "camera_2",
                  "id": "id_2",
                  "type": "videos"
                }
            ]
        sensors:
            The sensors to be added to session metadata.  Describes what sensors were used to capture the data.
            Example:
            [
                {
                  "name": "camera_1",
                  "type": "camera"
                },
                {
                  "name": "camera_2",
                  "type": "camera"
                }
            ]

        replace:
            If True, overwrites existing source metadata with the supplied source data.
            Otherwise, appends the supplied source data to the existing source metadata.

        Returns
        -------
        dict
            The updated metadata of the session after the source data update.
        """
        resp = self.requests.post(
            "sessions/add_source_data/",
            trailing_slash=True,
            json={
                "session_uid": session_uid,
                "source_data": source_data,
                "sensors": sensors,
                "replace": replace})
        if not resp.ok:
            raise ResponseError("{} ::: {}".format(resp.reason, resp.content))
        return resp.json()

    def add_auxiliary_session_data(
            self,
            session_uid: str,
            auxiliary_data: List[dict],
            replace: Optional[bool] = True) -> dict:
        """Add auxiliary session data e.g. video data to metadata of a given session.

        Parameters
        ----------
        session_uid:
            The session UID Of the session to add auxiliary data to.
        auxiliary_data:
            The auxiliary data to add to the session metadata.
            Example:
            [
                {
                  "id": "id_1",
                  "type": "concatenated_video",
                  "tags": [
                    "camera_1"
                  ]
                },
                {
                  "id": "id_2",
                  "type": "concatenated_video",
                  "tags": [
                    "camera_2"
                  ]
                }
            ]
        replace:
            If True, overwrites existing auxiliary metadata with the supplied auxiliary data.
            Otherwise, appends the supplied auxiliary data to the existing auxiliary metadata.

        Returns
        -------
        dict
            The updated metadata of the session after the auxiliary session data update.
        """

        sessions_amc = self.get_asset_manager(asset_type=AssetsConstants.SESSIONS_ASSET_ID)
        metadata = sessions_amc.get_metadata(id=session_uid)
        if replace:
            updated_auxiliary_data = auxiliary_data
        else:
            updated_auxiliary_data = auxiliary_data + metadata.get("auxiliary_data")

        metadata["auxiliary_data"] = updated_auxiliary_data

        return sessions_amc.update_metadata(id=session_uid, metadata=metadata, replace_sets=True)

    def add_ego_pose(
            self,
            session_uid: str,
            ego_pose_data: Optional[dict] = None,
            ego_pose_path: Optional[str] = None,
            title: Optional[str] = None):

        """Add an ego pose file to a session. An ego pose file has a series of frames in which a list of timestamped
        objects with their ego position in "lat" and "lon" is given.
        Example:
                    [
                        {
                          "frame":0,
                          "timestamp":"2021-08-24T21:15:15.574000+00:00",
                          "objects":{
                             "0":{
                                "lat":33.6,
                                "lon":-0.15
                             },
                             "1":{
                                "lat":5.6,
                                "lon":-3.45
                             },
                             "2":{
                                "lat":23.25,
                                "lon":-3.85
                             },
                             "3":{
                                "lat":83.0,
                                "lon":-5.9
                             },
                             "4":{
                                "lat":198.55,
                                "lon":12.15
                             }
                          }
                        },
                        {
                          "frame":1,
                          "timestamp":"2021-08-24T21:15:15.599000+00:00",
                          "objects":{
                             "5":{
                                "lat":33.55,
                                "lon":-0.15
                             },
                             "6":{
                                "lat":5.7,
                                "lon":-3.45
                             },
                             "7":{
                                "lat":23.25,
                                "lon":-3.85
                             },
                             "8":{
                                "lat":82.45,
                                "lon":-5.9
                             },
                             "9":{
                                "lat":197.8,
                                "lon":12.15
                             }
                          }
                        }
                    ]

                Parameters
                ----------
                session_uid:
                    The session UID Of the session to add auxiliary ego pose of the objects.
                ego_pose_data:
                    dictionary for ego pose of the objects
                ego_pose_path:
                    path to a json file containing the json file for ego pose of the objects.
                title:
                    title of the ego pose attached to the session.

                """

        if ego_pose_data is None:
            assert ego_pose_path, "either ego_pose_path or ego_pose_data should be specified"
            if not os.path.exists(ego_pose_path):
                raise NotADirectoryError(f"{ego_pose_path} does not exist!")
            else:
                filename, _, _, _ = parse_file_path(ego_pose_path)
                file_object = open(ego_pose_path, 'rb')
                title = title or filename
            with open(ego_pose_path) as json_file:
                ego_pose_data = json.load(json_file)
        else:
            assert title, "title should be specified"
            file_object = json.dumps(ego_pose_data, indent=4).encode('utf-8')

        timestamps = []
        for frame_json in ego_pose_data:
            assert "timestamp" in frame_json
            timestamps.append(frame_json["timestamp"])
            assert "objects" in frame_json
            for k, value in frame_json["objects"].items():
                assert "lat" in value
                assert "lon" in value

        self.__check_entity_durations(session_uid=session_uid, timestamps=timestamps)

        self.extend_time_span(session_uid=session_uid, timestamps=timestamps)

        object_access = self.get_asset_manager(asset_type=AssetsConstants.ANNOTATIONS_ASSET_ID).put_file(
            file_object=file_object,
            retry=True,
            id=title,
            content_type="application/json"
        )

        auxiliary_data = [{
            "object_access": object_access.to_dic(),
            "type": "ego_pose"
        }]

        self.add_auxiliary_session_data(session_uid=session_uid, auxiliary_data=auxiliary_data, replace=False)

    def add_enrichments_configs(
            self,
            session_uid: str,
            enrichments_configs: List[dict],
            replace: Optional[bool] = True) -> dict:
        """Add enrichment configurations to session metadata.

        Parameters
        ----------
        session_uid:
            The session UID of the session to add the enrichment configurations to.
        enrichments_configs:
            The enrichments configuration to add to the session metadata.
            Example:
            [
                {
                    "input_event": "geo_locations",
                    "type": "location",
                    "configuration": {
                        "influence_type": "interval",
                        "influence_radius_in_seconds": 0.5
                    }
                },
                {
                    "input_event": "geo_locations",
                    "type": "visibility",
                    "configuration": {
                        "influence_type": "interval",
                        "influence_radius_in_seconds": 2.0
                    }
                },
                {
                    "input_event": "geo_locations",
                    "type": "weather",
                    "configuration": {
                        "influence_type": "interval",
                        "influence_radius_in_seconds": 2.0
                    }
                }
            ]
        replace:
            If True, overwrites existing enrichments config metadata with the supplied enrichments config.
            Otherwise, appends the supplied enrichments config to the existing enrichments config metadata.

        Returns
        -------
        dict
            The updated metadata of the session after adding the enrichments configs.

        """
        resp = self.requests.post(
            "sessions/add_enrichments_configs/",
            trailing_slash=True,
            json={
                "session_uid": session_uid,
                "enrichments_configs": enrichments_configs,
                "replace": replace})
        if not resp.ok:
            raise ResponseError("{} ::: {}".format(resp.reason, resp.content))
        return resp.json()

    @deprecated("Use `add_geolocation_entities` instead")
    def add_geolocation_entity(
            self,
            latitude: float,
            longitude: float,
            timestamp: Union[str, datetime],
            session_uid: str,
            buffered: bool = False
    ) -> dict:
        """Add a geolocation entity to a session.

        Parameters
        ----------
        latitude:
            The latitude of the geolocation.
        longitude:
            The longitude of the geolocation.
        timestamp:
            The timestamp of the geolocation.
        session_uid:
            The session uid of the session to add the geolocation entity to.
        buffered:
            Buffer write

        Returns
        -------
        dict
            A confirmation that the Job to add the entity was acknowledged.

        """
        entity_dict = {
            "session": session_uid,
            "timestamp": datetime_or_str_to_iso_utc(timestamp),
            "enrichments": ["visibility", "weather", "location"],
            "entity_id": get_guid(),
            "geolocation": {"lat": latitude, "lon": longitude},
            "entity_name": EntityNames.GEOLOCATION,
            "entity_value": [latitude, longitude],
            "entity_type": EntityTypes.GEO_ENTITY_TYPE,
            "influence": EntityInfluenceTypes.GEO_INTERPOLATION
        }
        response = self.add_entities(
            entity_dicts=[entity_dict], buffered=buffered)
        return response

    def add_geolocation_entities(
            self,
            latitudes: List[float],
            longitudes: List[float],
            timestamps: List[Union[str, datetime]],
            session_uid: str,
            buffered: bool = False) -> List[dict]:
        """Add geolocation entities to a session.

        Parameters
        ----------
        latitudes:
            A list of latitudes of the geolocations.
        longitudes:
            A list of longitudes of the geolocations.
        timestamps:
            A list of timestamps of the geolocations.
        session_uid:
            The session uid of the session to add the geolocation entities to.
        buffered:
            Buffer write

        Returns
        -------
        List
            A list of dictionaries containing confirmations that the Job to add the entity chunks were acknowledged.

        """

        self.__check_entity_durations(session_uid=session_uid, timestamps=timestamps)

        entity_dicts = [{
            "session": session_uid,
            "timestamp": datetime_or_str_to_iso_utc(timestamp),
            "enrichments": ["visibility", "weather", "location"],
            "entity_id": get_guid(),
            "geolocation": {"lat": latitude, "lon": longitude},
            "entity_name": EntityNames.GEOLOCATION,
            "entity_value": [latitude, longitude],
            "entity_type": EntityTypes.GEO_ENTITY_TYPE,
            "influence": EntityInfluenceTypes.GEO_INTERPOLATION
        } for timestamp, latitude, longitude in zip(timestamps, latitudes, longitudes)]

        chunked_entities = chunk_list(entity_dicts, chunk_size=ENTITY_CHUNK_SIZE)

        responses = []
        for chunk in chunked_entities:
            responses.append(self.add_entities(
                entity_dicts=chunk, buffered=buffered))

        return responses

    @deprecated("use add_entities() instead")
    def add_entity(self,
                   entity_dict: dict,
                   urgent: bool = False,
                   buffered: bool = False) -> dict:
        """Add an entity to the specified session.

        Parameters
        ----------
        entity_dict:
            The entity data to add.  Typically, has the following form:
            {
                "session": session_uid,
                "start_time": datetime_or_str_to_iso_utc(start_time),
                "end_time": datetime_or_str_to_iso_utc(end_time),
                "timestamp": datetime_or_str_to_iso_utc(start_time),
                "entity_id": entity_id,
                "entity_name": event_name,
                "entity_value": event_value,
                "entity_type": Choose from scenebox.constants.EntityTypes,
                "influence": Choose from scenebox.constants.EntityInfluenceTypes
                "extend_session": bool whether to extend a session to cover the influence interval
            }

        urgent:
            If True, entity is ingested immediately.  However, a manual resolution is needed afterwards
            to make the entity searchable.

        buffered:
            If true, ignores the urgent and uses a built-in buffer for writing.

        Returns
        -------
        dict
            A confirmation that the Job to add the entity was acknowledged.

        """
        # urgent messages are ingested immediately but a manual resolution is
        # needed after that to make them searchable
        self.__check_entity_durations(session_uid=entity_dict.get("session"),
                                      timestamps=[entity_dict.get("timestamp"),
                                                  entity_dict.get("start_time"),
                                                  entity_dict.get("end_time")])

        return self.add_entities(entity_dicts=[entity_dict], urgent=urgent, buffered=buffered)

    def add_entities(self,
                     entity_dicts: List[dict],
                     urgent: bool = False,
                     buffered: bool = False) -> dict:
        """Add a list of entities to the specified sessions.

        Parameters
        ----------
        entity_dicts:
            The entity data to add.  Typically, each list item has the following form:
            {
                "session": session_uid,
                "start_time": datetime_or_str_to_iso_utc(start_time),
                "end_time": datetime_or_str_to_iso_utc(end_time),
                "timestamp": datetime_or_str_to_iso_utc(start_time),
                "entity_id": entity_id,
                "entity_name": event_name,
                "entity_value": event_value,
                "entity_type": Choose from scenebox.constants.EntityTypes,
                "influence": Choose from scenebox.constants.EntityInfluenceTypes
                "extend_session": bool whether to extend a session to cover the influence interval
            }

        urgent:
            If True, entity is ingested immediately.  However, a manual resolution is needed afterwards
            to make the entity searchable.

        buffered:
            if True, the entities is written to the buffer and "urgent" is ignored.
            user should call flush_entities_buffer eventuially to write all the data.

        Returns
        -------
        dict
            A confirmation that the Job to add the entities was acknowledged.

        """

        if buffered:
            if urgent:
                logger.warning("urgent write is not supported when buffered write is enabled")
            self.entities_buffer.extend(entity_dicts)
            if len(self.entities_buffer) > ENTITIES_BUFFER_SIZE:
                self.flush_entities_buffer()
            return {"acknowledged": True}
        else:
            resp = self.requests.post(
                "session_manager/add_entities/",
                trailing_slash=True,
                json={"entity_dicts": entity_dicts},
                params={"urgent": urgent}
            )
            if not resp.ok:
                raise ResponseError("{} ::: {}".format(resp.reason, resp.content))
            return resp.json()

    def flush_entities_buffer(self):
        """
        write all of the entities in the buffer. If scene engine is exited without calling this, all of the unflushed
        entities are discarded.
        """
        while self.entities_buffer:
            logger.debug(f"writing {len(self.entities_buffer)} entities")
            entities_to_write = [self.entities_buffer.popleft()
                                 for _ in range(min(ENTITY_CHUNK_SIZE, len(self.entities_buffer)))]
            self.add_entities(entity_dicts=entities_to_write, urgent=False, buffered=False)

    def resolve_session(
            self,
            session_uid: str,
            resolution: Optional[float] = None,
            wait_for_completion: bool = False) -> dict:
        """Resolve a session.

        Project session events onto a single timeline. Events are sampled at the given ``resolution``.  A smaller
        resolution is recommended if events rapidly change in value.

        Parameters
        ----------
        session_uid:
            The session UID of the session to resolve.
        resolution:
            The resolution at which to sample session events.  Measured in seconds.
        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.

        Returns
        -------
        dict
            The ID of the Job that attempts to resolve the session.
        """
        if resolution:
            params = {"resolution": resolution}
        else:
            params = {}
        resp = self.requests.post(
            "session_manager/resolve_session/{}".format(session_uid),
            params=params)
        if not resp.ok:
            raise ResponseError("{} ::: {}".format(resp.reason, resp.content))
        if wait_for_completion:
            job_id = resp.json()["job_id"]
            self._wait_for_job_completion(job_id)
        return resp.json()

    def add_event_interval(self,
                           event_name: str,
                           event_value: Union[str, List[str]],
                           start_time: Union[str, datetime],
                           end_time: Union[str, datetime],
                           session_uid: str,
                           urgent: bool = False,
                           buffered: bool = False) -> str:
        """Add an event interval to a session.

        Adds a "state_set" entity to a specific session's timespan.

        Parameters
        ----------
        event_name:
            The name of the event interval to add to the session.
        event_value:
            The value(s) of the event over the timespan.
        start_time:
            The start time of the event.
        end_time:
            The end time of the event.
        session_uid:
            The session UID of the session to add the event to.
        urgent:
            If True, entity is ingested immediately.  However, a manual resolution is needed afterwards
            to make the entity searchable.
        buffered:
            buffered write

        Returns
        -------
        str
            The ID of the added entity.

        """
        if isinstance(start_time, datetime) and isinstance(end_time, datetime):
            if start_time > end_time:
                raise InvalidTimeError(
                    "start time cannot be after the end time")
        entity_id = get_guid()
        if isinstance(event_value, str):
            event_value = [event_value]
        elif not isinstance(event_value, list):
            raise TypeError("event value can be either str or a List[str]")
        entity_dict = {
            "session": session_uid,
            "start_time": datetime_or_str_to_iso_utc(start_time),
            "end_time": datetime_or_str_to_iso_utc(end_time),
            "timestamp": datetime_or_str_to_iso_utc(start_time),
            "entity_id": entity_id,
            "entity_name": event_name,
            "entity_value": event_value,
            "entity_type": EntityTypes.STATE_SET_ENTITY_TYPE,
            "influence": EntityInfluenceTypes.INTERVAL
        }

        self.add_entities(entity_dicts=[entity_dict], urgent=urgent, buffered=buffered)
        # self.resolve_session(session_uid=session_uid)

        return entity_id

    def add_comments(self,
                     comments: Union[str, List[str]],
                     start_time: Union[str, datetime],
                     end_time: Union[str, datetime],
                     session_uid: str,
                     wait_for_completion: bool = False) -> dict:

        """Add a comment to a time segment of a session.

        Parameters
        ----------
        comments:
            The comment(s) to add to the given timespan.
        start_time:
            The start time of the timespan to add the comment to.
        end_time:
            The end time of the timespan to add the comment to.
        session_uid:
            The session UID of the session to add the comment to.
        wait_for_completion:
             If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.

        Returns
        -------
        dict
            The ID of the Job that attempts to add the comment.

        """

        if isinstance(comments, str):
            comments = [comments]

        comment_json = {
            "intervals": [
                {
                    "start_time": datetime_or_str_to_iso_utc(start_time),
                    "end_time": datetime_or_str_to_iso_utc(end_time)
                }
            ],
            "texts": comments,
        }
        resp = self.requests.post(
            "sessions/{}/comments".format(session_uid),
            trailing_slash=False,
            json=comment_json
        )
        if wait_for_completion:
            job_id = resp.json()["job_id"]
            self._wait_for_job_completion(job_id)
        return resp.json()

    def get_field_data(self,
                       session_uid: str,
                       search_dic: dict = None,
                       fields: Union[List[str],
                                     str] = 'all') -> Dict[str,
                                                           list]:
        if not search_dic:
            search_dic = {}

        if isinstance(fields, str):
            if fields == 'all':
                fields = ['*']
            else:
                raise ValueError(
                    'Field {} is not valid. Must be a list of field names or `all`'.format(fields))

        resp = self.requests.post(
            "session_manager/field_data/{}".format(session_uid),
            trailing_slash=False,
            json={
                'search_dic': search_dic,
                'session_fields': fields
            }
        )
        return resp.json()

    def get_searchable_fields(self, asset_type: str) -> dict:
        return self.requests.get(
            route=join(
                asset_type,
                'meta',
                'search_fields'),
            trailing_slash=True).json()

    def __adjust_time_interval(self,
                               start_time: Union[datetime, str],
                               end_time: Union[datetime, str],
                               epsilon: float) -> (datetime, datetime):

        if isinstance(start_time, str):
            start_time_output = string_to_datetime(
                start_time) + timedelta(seconds=epsilon)
        elif isinstance(start_time, datetime):
            start_time_output = start_time + timedelta(seconds=epsilon)
        else:
            raise TypeError("time should be either datetime or string")

        if isinstance(end_time, str):
            end_time_output = string_to_datetime(
                end_time) - timedelta(seconds=epsilon)
        elif isinstance(end_time, datetime):
            end_time_output = end_time - timedelta(seconds=epsilon)
        else:
            raise TypeError("time should be either datetime or string")

        if start_time_output > end_time_output:
            raise InvalidTimeError(
                "start time cannot be after or within {} second of the end time".format(epsilon))
        return start_time_output, end_time_output

    def add_event_intervals(self,
                            event_name: str,
                            event_values: List[str],
                            start_times: List[Union[str, datetime]],
                            end_times: List[Union[str, datetime]],
                            session_uid: str,
                            urgent: bool = False,
                            extend_session: bool = True,
                            epsilon: float = 0,
                            buffered: bool = False) -> List[str]:
        """Add a list of several event intervals to a session.

        Adds several "state_set" entities to a specific session's timespan.

        Parameters
        ----------
        event_name:
            The name of the event interval to add to the session.
        event_values:
            The value(s) of the event over the timespan.
        start_times:
            The start time of each event.
        end_times:
            The end time of each event.
        session_uid:
            The session UID of the session to add the events to.
        urgent:
            If True, entity is ingested immediately.  However, a manual resolution is needed afterwards
            to make the entity searchable.
        extend_session:
            should extend the session to include this event (default to true)
        epsilon:
            Constant to increase the time-delta of entity start time and endtime.  Measured in seconds.
        buffered:
            buffered write

        Returns
        -------
        List[str]
            A list of the added entity IDs

        """

        if len(event_values) != len(start_times) or \
                len(event_values) != len(end_times):
            raise IndexError(
                "size of event_values, start_times, and end_times should be same")

        self.__check_entity_durations(session_uid=session_uid, timestamps=start_times + end_times)

        entity_ids = []
        entity_dicts = []
        for start_time, end_time, event_value in zip(
                start_times, end_times, event_values):
            start_time, end_time = self.__adjust_time_interval(
                start_time, end_time, epsilon)

            entity_id = get_guid()
            if not isinstance(event_value, str):
                raise TypeError("event value should be str")

            entity_dict = {
                "session": session_uid,
                "start_time": datetime_or_str_to_iso_utc(start_time),
                "end_time": datetime_or_str_to_iso_utc(end_time),
                "timestamp": datetime_or_str_to_iso_utc(start_time),
                "enrichments": [],
                "entity_id": entity_id,
                "entity_name": event_name,
                "entity_value": [event_value],
                "entity_type": EntityTypes.STATE_SET_ENTITY_TYPE,
                "influence": EntityInfluenceTypes.AFFECT_FORWARD,
                "extend_session": extend_session
            }
            entity_dicts.append(entity_dict)
            entity_ids.append(entity_id)

        self.add_entities(entity_dicts=entity_dicts, urgent=urgent, buffered=buffered)
        # self.resolve_session(session_uid=session_uid)

        return entity_ids

    def add_scalar_intervals(self,
                             measurement_name: str,
                             measurement_values: List[float],
                             start_times: List[Union[str, datetime]],
                             end_times: List[Union[str, datetime]],
                             session_uid: str,
                             epsilon: float = 0.001) -> List[str]:
        """Add a timeseries with interval values to a session.

        Parameters
        ----------
        measurement_name:
            The name to assign to the measurements.
        measurement_values:
            The numerical values of each interval.  Each interval can only have one value.
        start_times:
            The start times of each interval.
        end_times:
            The end times of each interval.
        session_uid:
            The UID of the session to add the timeseries to.
        epsilon:
            The amount of time to add to start times and subtract off end times. Prevents intervals from having
            undesired overlap.

        Returns
        -------
        List[str]
            The IDs of the created entities.
        """

        if len(measurement_values) != len(start_times) or \
                len(measurement_values) != len(end_times):
            raise IndexError(
                "size of event_values, start_times, and end_times should be same")

        timestamps = []
        unpacked_measurements = []

        for start_time, end_time, measurement_value in zip(
                start_times, end_times, measurement_values):
            start_time, end_time = self.__adjust_time_interval(
                start_time, end_time, epsilon)

            timestamps += [start_time, end_time]
            unpacked_measurements += [measurement_value, measurement_value]

        return self.add_scalar_measurements(
            measurement_name=measurement_name,
            measurement_values=unpacked_measurements,
            timestamps=timestamps,
            session_uid=session_uid)

    def add_scalar_measurements(self,
                                measurement_name: str,
                                measurement_values: List[float],
                                timestamps: List[Union[datetime, str]],
                                session_uid: str,
                                buffered: bool = False) -> List[str]:
        """Add a timeseries with point values ("scalars") to a session.

        Parameters
        ----------
        measurement_name:
            The name to assign to the measurements.
        measurement_values:
            The numerical values of each point.  Each point can only have one value.
        timestamps:
            The timestamps at which each measurement occurred.
        session_uid:
            The UID of the session to add the timeseries to.
        buffered:
            If True, writes events in a buffered fashion.

        Returns
        -------
        List[str]
            The IDs of the created entities.
        """

        self.__check_entity_durations(session_uid=session_uid, timestamps=timestamps)

        entity_ids = []
        entity_dicts = []
        if len(timestamps) != len(measurement_values):
            raise IndexError(
                "measurement_values and timestamps should have same length")

        for timestamp, measurement_value in zip(
                timestamps, measurement_values):
            entity_id = get_guid()
            entity_dict = {
                "session": session_uid,
                "timestamp": datetime_or_str_to_iso_utc(timestamp),
                "enrichments": [],
                "entity_id": entity_id,
                "entity_name": measurement_name,
                "entity_value": measurement_value,
                "entity_type": EntityTypes.SCALAR_ENTITY_TYPE,
                "influence": EntityInfluenceTypes.LINEAR_INTERPOLATION
            }
            entity_dicts.append(entity_dict)
            entity_ids.append(entity_id)

        chunked_entities = chunk_list(entity_dicts, chunk_size=ENTITY_CHUNK_SIZE)

        for chunk in chunked_entities:
            self.add_entities(entity_dicts=chunk, buffered=buffered)
        return entity_ids

    def add_point_events(self,
                         measurement_name: str,
                         measurement_values: List[str],
                         timestamps: List[Union[datetime, str]],
                         session_uid: str,
                         buffered: bool = False) -> List[str]:
        """Add a list of several point events to a session.

        Parameters
        ----------
        measurement_name:
            The name to assign to the measurements.
        measurement_values:
            The state of the event at each timestamp.
        timestamps:
            A list of timestamps at which the events occurred.
        session_uid:
            The UID of the session to add the events to.
        buffered:
            If True, writes events in a buffered fashion.

        Returns
        -------
        List[str]
            A list of the added entity IDs.
        """

        if len(timestamps) != len(measurement_values):
            raise IndexError(
                "measurement_values and timestamps should have same length")

        self.__check_entity_durations(session_uid=session_uid, timestamps=timestamps)

        entity_ids = []
        entity_dicts = []
        resolution = self.get_asset_manager(
            AssetsConstants.SESSIONS_ASSET_ID).get_metadata(
            id=session_uid).get("resolution")
        for timestamp, measurement_value in zip(
                timestamps, measurement_values):
            entity_id = get_guid()
            timestamp = str_or_datetime_to_datetime(timestamp)
            start_time = datetime_or_str_to_iso_utc(
                timestamp - timedelta(seconds=resolution))
            end_time = datetime_or_str_to_iso_utc(
                timestamp + timedelta(seconds=resolution))
            timestamp = datetime_or_str_to_iso_utc(timestamp)
            entity_dict = {
                "session": session_uid,
                "timestamp": timestamp,
                "start_time": start_time,
                "end_time": end_time,
                "enrichments": [],
                "entity_id": entity_id,
                "entity_name": measurement_name,
                "entity_value": measurement_value,
                "entity_type": EntityTypes.STATE_ENTITY_TYPE,
                "influence": EntityInfluenceTypes.INTERVAL
            }
            entity_dicts.append(entity_dict)
            entity_ids.append(entity_id)

        chunked_entities = chunk_list(entity_dicts, chunk_size=ENTITY_CHUNK_SIZE)
        for chunk in chunked_entities:
            self.add_entities(entity_dicts=chunk, buffered=buffered)
        return entity_ids

    def add_timeseries_csv(self,
                           session_uid: str,
                           csv_filepath: str,
                           df_labels: Optional[List[str]] = None,
                           ):
        """Add a timeseries from a CSV file.

        Add a measurement DataFrame to a session as scalar entities from a CSV. Creates a ``measurement_df`` Pandas
        DataFrame from the inputted CSV file, then passes this dataframe to ``self.add_df``.

        Parameters
        ----------
        session_uid:
            The session to add the timeseries to.
        csv_filepath:
            The filepath of the CSV to turn into a timeseries.
        df_labels:
            List of the CSV column names to use.
        """
        kwargs = {}
        if df_labels:
            kwargs["names"] = df_labels
        measurement_df = pd.read_csv(csv_filepath, **kwargs)

        self.add_df(
            measurement_df=measurement_df,
            session_uid=session_uid
        )

    def add_df(self,
               measurement_df,
               session_uid: str,
               timestamps: Optional[List[Union[datetime,
                                               str]]] = None):

        """Add a measurement DataFrame to a session as scalar entities.

        Add several measurements across time in a session by populating the ``measurement_df`` Pandas DataFrame
        argument. Can add an arbitrary number of named measurements, either numeric or non-numeric.  Timestamps must
        either be specified in the ``timestamps`` argument, or under a column named "timestamps" inside
        ``measurement_df``.

        Parameters
        ----------
        measurement_df:
            DataFrame holding the measurement(s) of interest.  Add an arbitrary number of named columns to represent
            different measurement types. If a column named "timestamp" specifying the timestamps of the
            measurements does not exist, must be specified under the ``timestamps`` method argument.

            If latitude/longitude columns are included in under the names "lat" and "lon" respectively,
            will automatically be added as geolocation entities.
        session_uid:
            The session UID to add the measurement(s) to.
        timestamps:
            A list of timestamps corresponding to the data measurements in ``measurement_df`

        """

        def add_numeric_df(column: str,
                           measurement_df: pd.DataFrame,
                           timestamps: List[datetime]):

            measurement_values = [
                float(x) for x in measurement_df[column].values]
            self.add_scalar_measurements(
                measurement_name=column.lower(),
                measurement_values=measurement_values,
                timestamps=timestamps,
                session_uid=session_uid)

        if TIMESTAMP_FIELD not in measurement_df.columns and not timestamps:
            raise KeyError(
                "dataframe must include a timestamp column or timestamps must be passed separately")
        if not timestamps:
            timestamps = [str_or_datetime_to_datetime(
                _) for _ in measurement_df.timestamp]
        if "lat" in measurement_df.columns and "lon" in measurement_df.columns:
            self.add_geolocation_entities(
                latitudes=measurement_df["lat"],
                longitudes=measurement_df["lon"],
                session_uid=session_uid,
                timestamps=timestamps
            )
            measurement_df.drop(['lon', 'lat'], axis='columns', inplace=True)

        numeric_df = measurement_df.select_dtypes(include=np.number)
        non_numeric_df = measurement_df.drop(labels=numeric_df.columns, axis=1)
        if TIMESTAMP_FIELD in non_numeric_df.columns:
            non_numeric_df.drop(labels=TIMESTAMP_FIELD, axis=1, inplace=True)

        self.__check_entity_durations(session_uid=session_uid, timestamps=timestamps)

        if not numeric_df.empty:
            run_threaded(func=add_numeric_df,
                         iterable=numeric_df.columns,
                         desc="adding scalar measurements",
                         num_threads=self.num_threads,
                         measurement_df=numeric_df,
                         timestamps=timestamps)
        if not non_numeric_df.empty:
            for column in non_numeric_df.columns:
                self.add_point_events(
                    measurement_name=column,
                    measurement_values=non_numeric_df[column],
                    session_uid=session_uid,
                    timestamps=timestamps)
        self.resolve_session(session_uid=session_uid)

    def entity_summary(
            self,
            session_uid: str,
            entity_names: Optional[List[str]] = None,
            start_time: Optional[Union[datetime, str]] = None,
            end_time: Optional[Union[datetime, str]] = None) -> dict:
        """Get the entity summary for a session."""

        entity_names = entity_names or SummaryEntities.DEFAULT_ENTITIES_TO_SUMMARIZE
        payload = {"entity_names": entity_names}

        if start_time:
            payload["start_time"] = datetime_or_str_to_iso_utc(start_time)
        if end_time:
            payload["end_time"] = datetime_or_str_to_iso_utc(end_time)

        resp = self.requests.post(
            f"session_manager/entity_summary/{session_uid}",
            trailing_slash=False,
            json=payload)
        return resp.json()

    def delete_session(self,
                       session_uid: str,
                       delete_assets_contents: bool = True,
                       wait_for_completion: bool = False):
        """Delete an existing session.

        Optionally delete the assets inside the session, as well.

        Parameters
        ----------
        session_uid:
            The UID of the session to delete.
        delete_assets_contents:
            If True, deletes the assets contained inside the specified session.
            Otherwise, does not delete the assets in the session.
        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.

        Returns:

        """
        resp = self.requests.delete(
            "session_manager/delete_session/{}".format(session_uid),
            trailing_slash=False,
            params={'delete_assets_contents': delete_assets_contents})
        if not resp.ok:
            raise ResponseError("{} ::: {}".format(resp.reason, resp.content))

        if wait_for_completion:
            job_id = resp.json()["job_id"]
            self._wait_for_job_completion(job_id)
        return resp.json()

    def add_event_with_search(self,
                              event_title: str,
                              search: dict,
                              wait_for_completion: bool = False):

        resp = self.requests.post("session_manager/add_event_with_search/",
                                  trailing_slash=False,
                                  json={
                                      "search": search,
                                      "event_title": event_title}
                                  )
        if not resp.ok:
            raise ResponseError("{} ::: {}".format(resp.reason, resp.content))

        if wait_for_completion:
            job_id = resp.json()["job_id"]
            self._wait_for_job_completion(job_id)
        return resp.json()

    def delete_events(self,
                      session_uids: List[str],
                      event_names: List[str],
                      start_time: Optional[str] = None,
                      end_time: Optional[str] = None,
                      wait_for_completion: bool = False):
        params = {'session_uids': session_uids,
                  'event_names': event_names}
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time

        resp = self.requests.delete(
            "session_manager/delete_event/",
            trailing_slash=False,
            json=params)
        if not resp.ok:
            raise ResponseError("{} ::: {}".format(resp.reason, resp.content))

        if wait_for_completion:
            job_id = resp.json()["job_id"]
            self._wait_for_job_completion(job_id)
        return resp.json()

    def search_assets(
            self,
            asset_type,
            search: Optional[dict] = None,
            size: Optional[int] = None,
            offset: Optional[int] = None,
            sort_field: Optional[str] = None,
            sort_order: Optional[str] = None,
            scan: bool = True) -> List[str]:
        """Retrieve asset IDs with a search query.

        Returns the top ``size`` matching hits.
        If a return of more than 10000 hits or all hits is desired, use the default values and only set the search if any.

        Parameters
        ----------
        asset_type:
            Asset type to filter for in the asset search.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        search:
            Query to locate the data subset of interest.  Filters through existing
            assets according to the dictionary passed.
        size:
            Specifies the Elasticsearch search size.  The maximum number of hits to return.
            Has no effect if ``scan`` is False.
        offset:
            Specifies the Elasticsearch search offset.  The number of hits to skip.
            Has no effect if ``scan`` is False.
        sort_field:
            Sorts for the specified name.
        sort_order:
            Specifies the Elasticsearch string sorting order.
        scan:
            If True, uses the Elasticsearch scan capability.
            Otherwise, uses the Elasticsearch search API.

        Returns
        -------
        List[str]
            A list of all IDs of the assets fulfilling the search query.

        """
        if size or sort_field or sort_order:
            search = search or {}
            params = {'size': size, 'offset': offset, 'scan': scan}
            if sort_field:
                params['sort_field'] = sort_field
            if sort_order:
                params['sort_order'] = sort_order

            resp = self.requests.post("{}/".format(asset_type),
                                      json=search,
                                      params=params,
                                      trailing_slash=False)
            if not resp.ok:
                raise AssetError(
                    'Could not search the files ::: {} -- {} -- {}'.format(
                        asset_type, resp.reason, resp.content))
            return resp.json()

        else:

            sort_field = "id"
            sort_order = "asc"
            params = {"size": DEFAULT_PAGINATION,
                      "offset": 0,
                      "scan": False,
                      "sort_field": sort_field,
                      "sort_order": sort_order,
                      }
            resp = self.requests.post("{}/".format(asset_type),
                                      json=search,
                                      params=params,
                                      trailing_slash=False)
            if not resp.ok:
                raise AssetError(
                    'Could not search the files ::: {} -- {} -- {}'.format(
                        asset_type, resp.reason, resp.content))
            results = resp.json()
            if results:
                search_after = None if len(results) != DEFAULT_PAGINATION else results[-1]
            else:
                return results
            while search_after is not None:
                params = {"size": DEFAULT_PAGINATION,
                          "offset": 0,
                          "scan": False,
                          "sort_field": sort_field,
                          "sort_order": sort_order,
                          "search_after": search_after
                          }
                resp = self.requests.post("{}/".format(asset_type),
                                      json=search,
                                      params=params,
                                      trailing_slash=False)
                if not resp.ok:
                    raise AssetError(
                        'Could not search the files ::: {} -- {} -- {}'.format(
                            asset_type, resp.reason, resp.content))
                if resp.json():
                    res = resp.json()
                    results += res
                    search_after = res[-1]
                else:
                    break
            return results

    def search_meta(
            self,
            asset_type,
            query: Optional[dict] = None,
            size: int = DEFAULT_SEARCH_SIZE,
            offset: int = 0,
            sort_field: Optional[str] = None,
            sort_order: Optional[str] = None,
            scan: bool = True,
            compress: bool = False) -> List[Dict]:
        """Retrieve asset metadata with a search query.

        Returns the top ``size`` matching hits.  If a return of more than 10000 hits is desired, please use
        AssetManagerClient.search_meta_large().

        Parameters
        ----------
        asset_type:
            Asset type to filter for in the asset metadata search.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        query:
            Query to locate the data subset of interest.  Filters through existing
            assets according to the dictionary passed.
        size:
            Specifies the Elasticsearch search size.  The maximum number of hits to return.
            Has no effect if ``scan`` is False.
        offset:
            Specifies the Elasticsearch search offset.  The number of hits to skip.
            Has no effect if ``scan`` is False.
        sort_field:
            Sorts for the specified name.
        sort_order:
            Specifies the Elasticsearch string sorting order.
        scan:
            If True, uses the Elasticsearch scan capability.
            Otherwise, uses the Elasticsearch search API.
        compress:
            Boolean. If set to True, a gzip compressed list of metadata is returned.
            Typically used in cases where the metadata returned is over 20MB.

        Returns
        -------
        List[Dict]
            A list of the metadata of the assets fulfilling the search query.

        """

        query = query or {}
        params = {'size': size, 'offset': offset, 'scan': scan}
        if sort_field:
            params['sort_field'] = sort_field
        if sort_order:
            params['sort_order'] = sort_order
        if compress:
            params['compress'] = compress

        resp = self.requests.post("{}/meta/".format(asset_type),
                                  json=query,
                                  params=params,
                                  trailing_slash=False)
        if not resp.ok:
            raise AssetError(
                'Could not search the files ::: {} -- {} -- {}'.format(
                    asset_type, resp.reason, resp.content))
        return resp.json()

    def count(self,
              asset_type: str,
              search: Optional[dict] = None) -> int:
        """Retrieve summary of asset metadata with a search query.

                Parameters
                ----------
                asset_type:
                    Asset type to collect metadata summary for.
                    To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
                search:
                    Query to locate the data subset of interest.  Filters through existing
                    assets according to the dictionary passed.
        """

        return self.summary_meta(
            asset_type=asset_type,
            summary_request={"search": search, "dimensions": []})["total"]

    def summary_meta(
            self,
            asset_type,
            summary_request: Dict) -> Dict:
        """Retrieve summary of asset metadata with a search query.

        Parameters
        ----------
        asset_type:
            Asset type to collect metadata summary for.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        summary_request:
            Includes:
                - search: (Dict) to locate the data subset of interest.
                - dimensions: (List[str]) to collect statistical summary of the desired dimensions
                - nested_dimensions: (List[str]) to collect statistical summary of the desired nested dimensions
            Example:
                {
                  "search": {
                    "filters": [
                      {
                        "field": "objects",
                        "values": [
                          "ball.camera_0.tester_manual_point"
                        ],
                        "filter_out": false
                      }
                    ]
                  },
                  "nested_dimensions": [
                    "annotations_meta.provider"
                  ]
                }
        Returns
        -------
        Dict
            Example:
            {
              "total": 3,
              "aggregations": [
                {
                  "dimension": "annotations_meta.provider",
                  "buckets": [
                    {
                      "key": "COCO_bounding_box",
                      "doc_count": 1
                    },
                    {
                      "key": "COCO_polygon",
                      "doc_count": 2
                    }
                  ]
                }
              ]
            }

        """
        resp = self.requests.post("{}/meta/summary".format(asset_type),
                                  json=summary_request,
                                  trailing_slash=True)
        if not resp.ok:
            raise AssetError(
                'Could not get meta summary for ::: {} -- {} -- {}'.format(
                    asset_type, resp.reason, resp.content))
        return resp.json()

    def add_embeddings(
            self,
            embeddings: List[Embedding],
            similarity_ingest: bool = True,
            create_umap: bool = True,
            wait_for_completion: bool = False,
            add_to_cache: bool = False,
            umap_params: Optional[dict] = None
    ) -> List[str]:
        """Add existing embeddings to an asset.

        Parameters
        ----------
        embeddings:
            List of embeddings objects that are created from Scenebox Embedding class.
        similarity_ingest:
            If True, enables similar image/object search by performing bulk indexing.  Otherwise, has no effect.
        create_umap:
            If True, the embeddings are going to be added to a new umap
        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.
        add_to_cache:
            If True, corresponding bytes will be added to cache for quick access.
        umap_params:
            umap parameters including: n_neighbors, min_dist and train_size. Default is
            {
                n_neighbors: 20
                min_dist: 0.3
                train_size: 10000
            }

        Returns
        -------
        List[str]
            The IDs of the successfully added embeddings
        """

        # Validate Input
        if not embeddings:
            logger.warning("Empty list of embeddings was passed")
            return []

        if len(embeddings) > 1:
            assert all([embedding.ndim == embeddings[0].ndim and
                        embedding.metadata.get("index_name") == embeddings[0].metadata.get(
                "index_name") for embedding in embeddings[1:]]), \
                "All the embeddings must have the same length and belong to the same asset_type, model, and version"

        similarity_index_name = embeddings[0].metadata.get("index_name") or get_similarity_index_name(
            media_type=embeddings[0].asset_type, model=embeddings[0].model, version=embeddings[0].version
        )

        asset_type = embeddings[0].asset_type

        # Dynamically choose the chunk size based on 8GB memory usage
        chunk_size = (8 * 1024 ** 2) // (embeddings[0].ndim * 8)

        # Chunk the list into smaller lists
        embeddings = chunk_list(embeddings, chunk_size)
        embedding_ids = []
        for chunk_id, embedding_list in enumerate(embeddings):
            embedding_id_list, embedding_byte_list, embedding_metadata_list = [], [], []
            asset_metadata_list, media_asset_ids = [], []
            logger.info("Processing chunk {}/{} with {} embeddings".format(
                chunk_id + 1, len(embeddings), len(embedding_list)))
            for embedding in embedding_list:
                embedding_id_list.append(embedding.id)
                embedding_byte_list.append(embedding.bytes)
                embedding_metadata_list.append(embedding.metadata)
                media_asset_ids.append(embedding.asset_id)
                asset_metadata_list.append({"embeddings":
                                                {similarity_index_name: embedding.id}})

            self.get_asset_manager(
                AssetsConstants.EMBEDDINGS_ASSET_ID).put_assets_batch(
                file_objects=embedding_byte_list,
                ids=embedding_id_list,
                metadata=embedding_metadata_list,
                disable_tqdm=False,
                retry=True,
                add_to_redis_cache=add_to_cache)

            logger.info("Updating the metadata")
            self.get_asset_manager(
                asset_type=asset_type).update_metadata_batch(
                ids=media_asset_ids,
                metadata=asset_metadata_list)
            embedding_ids.extend(embedding_id_list)

        if similarity_ingest:
            resp = self.requests.post(
                "similarity_search/bulk_index/",
                trailing_slash=False,
                json={"embedding_ids": embedding_ids})
            if not resp.ok:
                raise ResponseError(
                    "Could not clean_up the annotations: {}".format(
                        resp.content))

            job_id = resp.json()["job_id"]
            if wait_for_completion or create_umap:
                self._wait_for_job_completion(
                    job_id, max_wait_sec=max(
                        10 * len(embedding_ids), 60))
        if create_umap:
            umap_params = umap_params or {}
            self.create_umap(asset_type=asset_type,
                             index_name=similarity_index_name,
                             search_dic={},
                             wait_for_completion=wait_for_completion,
                             **umap_params)

        return embedding_ids

    def get_embeddings(
            self,
            embedding_space: str,
            asset_type: str = AssetsConstants.IMAGES_ASSET_ID,
            asset_ids: Optional[List[str]] = None,
            use_umap_as_embedding: bool = False,
            max_number_of_embeddings: int = 200000,
            search: Optional[dict] = None) -> List[Embedding]:

        """Retrieve asset embeddings.

                Parameters
                ----------
                embedding_space:
                    Mandatory Embedding space for obtaining the embeddings
                asset_type:
                    Asset types, default is images
                asset_ids:
                    ids of assets. By default, image ids. If not specified, fetch everything
                use_umap_as_embedding:
                    should use 2D umaps instead of high dimensional embeddings. Default is False
                max_number_of_embeddings:
                    Maximum number of embeddings to fetch. If exceeds, throw an error
                search:
                    search parameter. By default, search everything

                Returns
                -------
                List[Embedding]
                    Returns list of Embedding objects
                """
        assets_amc = self.get_asset_manager(asset_type=asset_type)
        if not search:
            search_ = {}
        else:
            search_ = copy(search)
        exists_filters = search_.get("exists_filters", [])
        if use_umap_as_embedding:
            embedding_key = "umap"
        else:
            embedding_key = "embeddings"
        exists_filters.append(
            {
                "field": f"{embedding_key}.{embedding_space}"
            }
        )
        search_["exists_filters"] = exists_filters

        if asset_ids:
            filters = search_.get("filters", [])
            filters.append(
                {
                    "id": asset_ids
                }
            )
            search_["filters"] = filters

        search_["source_selected_fields"] = ["id", f"{embedding_key}.{embedding_space}"]

        assets_meta = assets_amc.search_meta_large(query=search_)
        if len(assets_meta) > max_number_of_embeddings:
            raise AssetError(f"found {len(assets_meta)} embeddings. It is larger than max {max_number_of_embeddings}")
        embeddings = []
        if use_umap_as_embedding:
            for am in assets_meta:
                embeddings.append(
                    Embedding(data=am["umap"][embedding_space]["coordinates"], asset_id=am.get("id"),
                              asset_type=asset_type, model="umap",
                              timestamp=am.get("timestamp"), dtype=np.float32, ndim=2)
                )
        else:
            embedding_ids = [am["embeddings"][embedding_space] for am in assets_meta]
            embeddings_amc = self.get_asset_manager(asset_type=AssetsConstants.EMBEDDINGS_ASSET_ID)
            embedding_bytes = embeddings_amc.get_bytes_in_batch(ids=embedding_ids)
            embedding_metas = embeddings_amc.get_metadata_in_batch(ids=embedding_ids)
            for embedding_id, embedding_byte in embedding_bytes.items():
                embedding_meta = embedding_metas.get(embedding_id)
                if not embedding_meta:
                    logger.warning(f"embedding id {embedding_id} doesn't have a metadata")
                    continue
                ndim = embedding_meta.get("ndim")
                type_size = len(embedding_byte)/ndim
                if type_size == 4:
                    dtype_ = np.float32
                elif type_size == 8:
                    dtype_ = np.float64
                else:
                    logger.warning(f"embedding size {embedding_id} != 4 or 8.assuming a float32")
                    dtype_ = np.float32
                embeddings.append(Embedding(data=embedding_byte, asset_id=embedding_meta.get("asset_id"), asset_type=asset_type,
                                            version=embedding_meta.get("version"), model=embedding_meta.get("model"),
                                            timestamp=embedding_meta.get("timestamp"), layer=embedding_meta.get("layer"),
                                            dtype=dtype_, ndim=ndim))
        return embeddings

    @deprecated("Use `add_images` instead")
    def add_image(
            self,
            image_path: Optional[str] = None,
            id: Optional[str] = None,
            image_url: Optional[str] = None,
            image_uri: Optional[str] = None,
            image_bytes: Optional[Union[io.BytesIO, bytes, str]] = None,
            sensor: Optional[str] = None,
            timestamp: Optional[Union[str, datetime]] = None,
            session_uid: Optional[str] = None,
            set_id: Optional[Union[str, List[str]]] = None,
            annotations: Optional[List[Annotation]] = None,
            preprocesses: Optional[List[str]] = None,
            aux_metadata: Optional[dict] = None,
            geo_field: Optional[str] = None,
            shape_group_field: Optional[str] = None,
            nested_fields: Optional[List[str]] = None,
            enrichments: Optional[List[str]] = None,
            add_to_session: bool = False,
            thumbnailize_at_ingest: bool = False,
            buffered_write: bool = False,
            add_provider_to_labels: bool = True,
            overwrite: bool = True,
            add_to_cache: bool = False
    ) -> str:

        """Upload an image onto SceneBox.

               Upload an image with a local file path, URL, URI, or image bytes.  This method is best used with
               singular images, or images that are not all located in the same folder. For several images all located
               in the same folder, check out ``self.add_images_from_folder``.

               Parameters
               ----------
               image_path:
                   The local path to the image to upload. If not None, image_url, image_uri, and image_bytes should all
                   be None.
               id:
                   A unique image ID.  A common choice is the image filename.
               image_url:
                   The URL of the image to upload. Images must be publicly available.  If not None, image_url,
                   image_uri, and image_path should all be None.
               image_uri:
                   The URI of the image to upload. Can be from a private source.  If not None, image_url, image_path,
                   and image_bytes should all be None.
               image_bytes:
                   The image bytes to upload.  If not None, image_path, image_url, and image_uri should all be None.
               sensor:
                    The sensor associated with the image.
               timestamp:
                    The time at which the image was taken.
               session_uid:
                    The session associated with the image.
               set_id:
                    The set (str) or sets (List[str]) to add the image to.
               annotations:
                    Annotations associated with the image.  Each item in the passed list must be of a class from
                    scenebox.models.annotation.
               preprocesses:
                    Specifies which process to treat the image thumbnails with.
               aux_metadata:
                    Auxiliary metadata associated with the image (partitioned from primary metadata)
               geo_field:
                    Geolocation metadata associated with the image.
               shape_group_field:
                    Shape group metadata associated with the image (example: UMAP).
               nested_fields:
                    nested fields (example: "[annotations_meta]")
               enrichments:
                    The types of enrichments to add to the image.
               thumbnailize_at_ingest:
                    If True, create thumbnail at ingestion time.  Otherwise, create thumbnails "on the fly".
               buffered_write:
                    If True, writes images in a buffered fashion.
               add_to_session:
                    If True and session_uid is not None, add to the existing session with the passed session_uid.
               add_provider_to_labels:
                    If True the labels of the annotations in aux.label will included the provider as well. If False
                    only the labels will be ingested
               overwrite:
                    If True and id is not None, updates the metadata/annotations/etc. of a previously uploaded
                    image.
               add_to_cache:
                    If True, corresponding bytes will be added to cache for quick access.

               Returns
               -------
               str
                   The id of the added image.

               Raises
               ------
               SetsErrorInvalidArgumentsError:
                    If more than one of image_path, image_url, image_uri, and image_bytes is not None
               ValueError:
                    If image_path, image_bytes, image_uri, and image_url are all None

               """
        sets = []
        id = id or get_guid()
        if set_id:
            if isinstance(set_id, str):
                sets = [set_id]
            elif isinstance(set_id, list):
                sets = set_id

        if not overwrite and id is not None:
            if self.get_asset_manager(
                    asset_type=AssetsConstants.IMAGES_ASSET_ID).exists(id=id):
                if aux_metadata or preprocesses or set_id or annotations:
                    updated_meta = {}
                    if set_id:
                        updated_meta['sets'] = sets
                    if aux_metadata:
                        updated_meta[AUXILIARY_KEY] = aux_metadata
                    if preprocesses:
                        updated_meta['preprocesses'] = preprocesses
                    if annotations:
                        updated_meta["annotations"] = [
                            _.id for _ in annotations
                        ]
                        updated_meta["annotations_meta"] = [
                            {
                                "provider": _.provider,
                                "id": _.id,
                                "version": _.version,
                                "type": _.annotation_type
                            } for _ in annotations]
                        for annotation in annotations:
                            image_meta = self.get_asset_manager(
                                asset_type=AssetsConstants.IMAGES_ASSET_ID).get_metadata(
                                id=id)
                            annotation.timestamp = image_meta["timestamp"]
                            annotation.sensor = image_meta["sensor"]
                            annotation.session_uid = image_meta["session_uid"]
                        self.add_annotations(
                            annotations=annotations, update_asset=False)

                    self.get_asset_manager(
                        asset_type=AssetsConstants.IMAGES_ASSET_ID).update_metadata(
                        id=id, metadata=updated_meta)
                return id

        img_sources_count = 0
        extra_args = {"id": id}
        image_source = None
        source_type = None
        if image_path:
            image_source, source_type, img_sources_count = image_path, "path", img_sources_count + 1
        if image_bytes:
            image_source, source_type, img_sources_count = image_bytes, "bytes", img_sources_count + 1
        if image_url:
            image_source, source_type, img_sources_count = image_url, "url", img_sources_count + 1
        if image_uri:
            object_access = ObjectAccess(
                uri=image_uri
            )
            extra_args["url"] = self.get_asset_manager(
                AssetsConstants.IMAGES_ASSET_ID).get_url_from_object_access(
                object_access=object_access)
            image_source, source_type, img_sources_count = image_uri, "uri", img_sources_count + 1

        if img_sources_count != 1:
            raise InvalidArgumentsError(
                "Exactly one of image_path, image_url, image_uri, or image_bytes should be specified")

        image_attributes, filename = get_asset_attributes_filename(asset_type=AssetsConstants.IMAGES_ASSET_ID,
                                                                   asset_source=image_source,
                                                                   source_type=source_type,
                                                                   **extra_args)

        if not image_attributes:
            raise FileNotFoundError("no image attributes ::: "
                                    "for uri {}, url {},or path {}".format(image_uri, image_url, image_path))

        if timestamp is None:
            timestamp = datetime_or_str_to_iso_utc(datetime.utcnow())
        else:
            timestamp = datetime_or_str_to_iso_utc(timestamp)

        image_metadata = {
            "width": image_attributes.width,
            "height": image_attributes.height,
            "format": image_attributes.format,
            "sensor": sensor,
            "timestamp": timestamp,
            "sets": sets,
            "preprocesses": preprocesses or [],
        }
        if session_uid is not None:
            image_metadata["session_uid"] = session_uid

        if annotations:
            image_metadata["annotations"] = [
                _.id for _ in annotations
            ]
            image_metadata["annotations_meta"] = [
                {
                    "provider": _.provider,
                    "id": _.id,
                    "version": _.version,
                    "type": _.annotation_type
                } for _ in annotations]
            labels = set()
            if add_provider_to_labels:
                for annotation in annotations:
                    for ae in annotation.annotation_entities:
                        labels.add("{}_{}".format(ae.label, annotation.provider))
            else:
                for annotation in annotations:
                    for ae in annotation.annotation_entities:
                        labels.add(ae.label)

            labels = list(labels)

            if aux_metadata:
                aux_metadata["labels"] = labels
            else:
                aux_metadata = {"labels": labels}

        if aux_metadata:
            image_metadata[AUXILIARY_KEY] = aux_metadata
        if image_bytes or image_path:
            if "png" in image_attributes.format.lower():
                content_type = "image/png"
            elif "jpg" in image_attributes.format.lower() or "jpeg" in image_attributes.format.lower():
                content_type = "image/jpeg"
            else:
                content_type = None
            id = self.get_asset_manager(
                AssetsConstants.IMAGES_ASSET_ID).put_asset(
                file_object=image_bytes or None,
                file_path=image_path or None,
                filename=filename,
                id=id,
                metadata=image_metadata,
                geo_field=geo_field,
                shape_group_field=shape_group_field,
                nested_fields=nested_fields,
                wait_for_completion=not buffered_write,
                buffered_write=buffered_write,
                content_type=content_type,
                add_to_redis_cache=add_to_cache
            )
        else:
            id = self.get_asset_manager(
                AssetsConstants.IMAGES_ASSET_ID).put_asset(
                url=image_url,
                filename=filename,
                id=id,
                uri=image_uri,
                metadata=image_metadata,
                geo_field=geo_field,
                wait_for_completion=not buffered_write,
                buffered_write=buffered_write
            )

        # If session_uid does not exist skip creating and pushing the entity
        if session_uid and add_to_session:
            entity_dict = {
                "session": session_uid,
                "timestamp": timestamp,
                "enrichments": enrichments or [],
                "entity_name": EntityNames.IMAGE,
                "media_asset_id": id,
                "entity_value": id,
                "entity_id": get_guid(),
                "entity_type": EntityTypes.MEDIA,
                "influence": EntityInfluenceTypes.INTERVAL
            }
            self.add_entities(entity_dicts=[entity_dict])

        # create thumbnail at ingestion time. By default set to False to speed up ingestion. If false, it thumbnails
        # will be created on the fly
        if thumbnailize_at_ingest:

            for preset in ["small", "tiny", "full_size_png"]:
                self.compress_images(
                    ids=[id],
                    use_preset=preset
                )

        if annotations:
            for annotation in annotations:
                annotation.timestamp = timestamp
                annotation.sensor = sensor
                annotation.session_uid = session_uid

            self.add_annotations(
                annotations=annotations,
                update_asset=False,
                threading=False,
                disable_tqdm=True)
        return id

    def add_images_from_folder(
            self,
            folder_path: str,
            set_id: str,
            session_uid: Optional[str] = None,
            filename_image_id_map: Optional[dict] = None,
            preprocesses: Optional[List[str]] = None,
            thumbnailize_at_ingest: bool = False
    ):
        """Upload images from a single local folder path onto SceneBox.

           Upload several images at once with the same local folder path.  This method is best used with local images
           that are all located in the same folder. For images not located in the same folder, or images that are not
           located on your local machine, check out ``self.add_image``.

           Parameters
           ----------
           folder_path:
               The local path to the folder of images to upload.
           session_uid:
                The session associated with the image.
           set_id:
                The set to add the images to.
           filename_image_id_map:
                Provides a mapping from the image filenames to the desired image IDs.  If not specified, Image IDs are
                automatically assigned to a randomized, unique string.
           preprocesses:
                Specifies which process to images thumbnails with.
           thumbnailize_at_ingest:
                If True, create thumbnail at ingestion time.  Otherwise, create thumbnails "on the fly".
           Raises
           ------
           ValueError:
            "If image_path, image_bytes, image_uri, and image_url are all None"

           """
        folder_path_object = Path(folder_path)
        file_list = [str(fp) for fp in folder_path_object.glob("*")]
        if not file_list:
            logger.warning("Could not find any valid images under {}".format(folder_path))
            return
        valid_images = []
        for file_path in file_list:
            image_type = imghdr.what(file_path)
            if image_type in ValidExtensions.IMAGES:
                image_id = filename_image_id_map[file_path.split('/')[-1]] if filename_image_id_map else None
                valid_images.append(Image(
                    path=file_path,
                    id=image_id,
                    session_uid=session_uid
                ))
        if not valid_images:
            logger.warning("Could not find any valid images under {}".format(folder_path))
            return

        self.add_images(
            images=valid_images,
            set_id=set_id,
            preprocesses=preprocesses,
            thumbnailize_at_ingest=thumbnailize_at_ingest
        )

    def add_images(
            self,
            images: List[Image],
            set_id: Union[str, List[str]],
            geo_field: Optional[str] = None,
            shape_group_field: Optional[str] = None,
            nested_fields: Optional[List[str]] = None,
            preprocesses: Optional[List[str]] = None,
            add_to_session: bool = False,
            thumbnailize_at_ingest: bool = False,
            add_provider_to_labels: bool = True,
            add_to_cache: bool = False,
            overwrite: bool = True,
            disable_tqdm: bool = True
    ) -> List[str]:

        """Upload multiple images onto SceneBox.

            Upload an image with a local file path, URL, URI, or image bytes.  This method is best used with
            singular images, or images that are not all located in the same folder. For several images all located
            in the same folder, check out ``self.add_images_from_folder``.

            Parameters
            ----------
            images:
                A list of objects of the type Image defined in models.Image. For Image objects that exist,
                the metadata is overwritten with the information provided in this call. For updating metadata,
                refer to asset_manager_client.update_metadata().
            set_id:
                The set (str) or sets (List[str]) to add the images to.
            geo_field:
                Geolocation metadata associated with the image.
            shape_group_field:
                Shape group metadata associated with the image (example: UMAP).
            nested_fields:
                nested fields (example: "[annotations_meta]")
            preprocesses:
                Specifies which process to treat the image thumbnails with.
            thumbnailize_at_ingest:
                If True, create thumbnail at ingestion time.  Otherwise, create thumbnails "on the fly".
            add_to_session:
                If True and session_uid is not None, add to the existing session with the passed session_uid.
            add_provider_to_labels:
                If True the labels of the annotations in aux.label will included the provider as well. If False
                only the labels will be ingested
            add_to_cache:
                If True, corresponding bytes will be added to cache for quick access.
            overwrite:
                Only effective if the `id` is provided in the image. If True, and an asset with the same id exists on
                SceneBox, it overwrites the asset completely with new metadata. It removes it from the previous sets and
                adds to new sets.
                If False and asset with the same id exists on SceneBox, it only adds them to the new set. It will not
                affect the metadata and annotations.
            disable_tqdm:
                If False, TQDM is used to show progress.

            Returns
            -------
            List[str]
               List of ids of the added images.

            Raises
            ------
            SetsErrorInvalidArgumentsError:
                If more than one of image_path, image_url, image_uri, and image_bytes is not None
            ValueError:
                If image_path, image_bytes, image_uri, and image_url are all None

        """

        image_bulk_uploader = BulkImageUploader(sec=self, preprocesses=preprocesses,
                                                thumbnailize_at_ingest=thumbnailize_at_ingest)
        return image_bulk_uploader.preprocess_and_upload_bulk(
            assets=images,
            add_to_session=add_to_session,
            set_id=set_id,
            add_to_cache=add_to_cache,
            geo_field=geo_field,
            shape_group_field=shape_group_field,
            nested_fields=nested_fields,
            add_provider_to_labels=add_provider_to_labels,
            overwrite=overwrite,
            disable_tqdm=disable_tqdm
        )

    @deprecated("Use `add_videos` instead")
    def add_video(
            self,
            set_id: str,
            video_path: Optional[str] = None,
            video_url: Optional[str] = None,
            video_uri: Optional[str] = None,
            sensor: Optional[str] = None,
            start_timestamp: Optional[Union[datetime, str]] = None,
            session_uid: Optional[str] = None,
            id: Optional[str] = None,
            annotations: Optional[List[Annotation]] = None,
            aux_metadata: Optional[dict] = None,
            enrichments: Optional[List[str]] = None,
            tags: Optional[List[str]] = None,
            compress_video: bool = True,
            buffered_write: bool = False,
            add_to_session: bool = False,
            create_session: bool = False
    ) -> Union[str, Tuple[str, str]]:

        """Upload a video onto SceneBox.

           Upload a video with a local file path, URL, or URI.

           Parameters
           ----------
           video_path:
               The local path to the video to upload. If not None, video_uri and video_url should both be None.
           video_url:
               The URL of the video to upload. Video must be publicly available.  If not None, video_path and
               video_uri should both be None.
           video_uri:
               The URI of the video to upload. Can be from a private source.  If not None, video_path, and video_url,
               should both be None.
           sensor:
                The sensor associated with the image.
           start_timestamp:
                The time at which the video recording began.
           session_uid:
                The session associated with the video.
           id:
               A unique video ID.  A common choice is the video filename.
           set_id:
                The set to add the video to.
           annotations:
                    Annotations associated with the Video.  Each item in the passed list must be of a class from
                    scenebox.models.annotation.
           aux_metadata:
                    Auxiliary metadata associated with the image (partitioned from primary metadata)
           enrichments:
                The types of enrichments to add to the video.
           tags:
                Labels associated with the video.  Allows for easy video search.
           compress_video:
                If true, register compressed video thumbnails.
           buffered_write:
                If True, writes videos in a buffered fashion.
           add_to_session:
                If True and session_uid is not None, add to the existing session with the passed session_uid.
           create_session:
               If True and session_uid is None, create a single video session from the video with the video naming and
               the video start time and duration. Session resolution would be default (1.0 second) and video will be
               added as an aux_metadata. In this case, if the sensor name is not specified, it will be "main"

           Returns
           -------
           str
               The ID of the added video.

           Raises
           ------
           ValueError:
                If video_path, video_url, and video_uri are all None

           """

        assert set_id, "`set_id` is None. Videos need to be associated with a set"
        id = id or get_guid()

        if video_path:
            filename, _, _, _ = parse_file_path(video_path)
            video_attributes = get_video_attributes(video_path)
        elif video_url:
            filename = video_url.split("/")[-1]
            video_attributes = get_video_attributes(video_url)
        elif video_uri:
            filename = UriParser(uri=video_uri).key.split("/")[-1]
            object_access = ObjectAccess(
                uri=video_uri
            )
            video_attributes = get_video_attributes(
                self.get_asset_manager(
                    AssetsConstants.VIDEOS_ASSET_ID).get_url_from_object_access(
                    object_access=object_access))
        else:
            raise ValueError("Either video_path, video_url, or video_uri must be provided")

        if start_timestamp:
            start_timestamp_dt = str_or_datetime_to_datetime(start_timestamp)
        else:
            start_timestamp_dt = datetime.utcnow()

        if not session_uid and create_session:
            session_uid = self.add_session(session_name=standardize_name(filename) or id,
                                           session_type=SessionTypes.VIDEOS_SESSION_ID)
            add_to_session = True
            sensor = sensor or "main"

        video_metadata = {
            "timestamp": datetime_or_str_to_iso_utc(start_timestamp_dt),
            "width": video_attributes.width if video_attributes else None,
            "height": video_attributes.height if video_attributes else None,
            "sensor": sensor,
            "duration": float(video_attributes.duration) if video_attributes else None,
            "fps": video_attributes.fps if video_attributes else None,
            "sets": [set_id] if set_id else [],
            "start_time": datetime_or_str_to_iso_utc(start_timestamp_dt),
            "end_time": datetime_or_str_to_iso_utc(
                start_timestamp_dt
                + timedelta(
                    seconds=float(video_attributes.duration))) if video_attributes else None,
            "tags": tags or []
        }

        if session_uid is not None:
            video_metadata["session_uid"] = session_uid

        if annotations:
            video_metadata["annotations"] = [
                _.id for _ in annotations
            ]
            video_metadata["annotations_meta"] = [
                {
                    "provider": _.provider,
                    "id": _.id,
                    "version": _.version,
                    "type": _.annotation_type
                } for _ in annotations]
            labels = set()
            for annotation in annotations:
                for ae in annotation.annotation_entities:
                    labels.add("{}_{}".format(ae.label, annotation.provider))

            labels = list(labels)

            if aux_metadata:
                aux_metadata["labels"] = labels
            else:
                aux_metadata = {"labels": labels}

        if aux_metadata:
            video_metadata[AUXILIARY_KEY] = aux_metadata

        if video_path:
            id = self.get_asset_manager(
                AssetsConstants.VIDEOS_ASSET_ID).put_asset(
                file_path=video_path,
                filename=filename,
                metadata=video_metadata,
                id=id,
                wait_for_completion=not buffered_write,
                buffered_write=buffered_write
            )
        elif video_url or video_uri:
            id = self.get_asset_manager(
                AssetsConstants.VIDEOS_ASSET_ID).put_asset(
                url=video_url,
                uri=video_uri,
                metadata=video_metadata,
                id=id,
                wait_for_completion=not buffered_write,
                buffered_write=buffered_write
            )
        else:
            raise ValueError(
                "Either file path or url, or uri must be provided ")

        # If session_uid does not exist skip creating and pushing the entity
        if session_uid and add_to_session:
            entity_dict = {
                "session": video_metadata["session_uid"],
                "start_time": video_metadata["start_time"],
                "end_time": video_metadata["end_time"],
                "timestamp": video_metadata["timestamp"],
                "enrichments": enrichments or [],
                "entity_name": EntityNames.VIDEO,
                "entity_id": filename,
                "entity_type": EntityTypes.MEDIA,
                "entity_value": id,
                "media_asset_id": id,
                "influence": EntityInfluenceTypes.AFFECT_FORWARD,
                "extend_session": True
            }
            self.add_entities(entity_dicts=[entity_dict], urgent=True)
        if compress_video:
            for preset in ['small', 'tiny']:
                self.compress_videos(
                    ids=[id],
                    use_preset=preset,
                )
        if create_session:
            auxiliary_data = [{
                "id": id,
                "type": AuxiliaryDataTypes.CONCATENATED_VIDEO,
                "tags": [sensor]
            }]

            self.add_auxiliary_session_data(session_uid=session_uid,
                                            auxiliary_data=auxiliary_data)

            video_source_data = [{
                "id": id,
                "type": AssetsConstants.VIDEOS_ASSET_ID,
                "sensor": sensor
            }]
            self.add_source_data(
                session_uid=session_uid,
                source_data=video_source_data,
                sensors=[{
                    "name": sensor,
                    "type": Sensors.CAMERA
                }]
            )
            self.resolve_session(session_uid=session_uid, wait_for_completion=True)
            return id, session_uid
        else:
            return id

    def add_videos(
            self,
            videos: List[Video],
            set_id: Union[str, List[str]],
            add_to_session: bool = False,
            compress_videos: bool = True,
            add_to_cache: bool = False,
            overwrite: bool = True,
            wait_for_compression_completion: bool = False
    ) -> List[str]:
        """Upload multiple videos onto SceneBox.

            Parameters
            ----------
            videos:
                A list of objects of the type Video defined in models.Video. For Video objects that exist,
                the metadata is overwritten with the information provided in this call. For updating metadata,
                refer to asset_manager_client.update_metadata().
            set_id:
                The set (str) or sets (List[str]) to add the videos to.
            add_to_session:
                If True and session_uid is not None, add to the existing session with the passed session_uid.
            compress_videos:
                If true, register compressed video thumbnails.
            add_to_cache:
                If True, corresponding bytes will be added to cache for quick access.
            overwrite:
                If False and asset exists on SceneBox, adds the previously uploaded videos to the given set_id.
            wait_for_compression_completion:
                If True wait for compression to be completed
            Returns
            -------
            List[str]
               List of ids of the added videos.

            Raises
            ------
            SetsErrorInvalidArgumentsError:
                If more than one of video path, url, uri, and bytes is not None

        """
        bulk_uploader = BulkVideoUploader(sec=self,
                                          compress_videos=compress_videos,
                                          wait_for_compression_completion=wait_for_compression_completion)
        video_ids = bulk_uploader.preprocess_and_upload_bulk(assets=videos,
                                                             add_to_session=False, #adding video to session is handled separately by extending the session
                                                             set_id=set_id,
                                                             add_to_cache=add_to_cache,
                                                             overwrite=overwrite)

        if add_to_session:
            session_uid = None
            for video in videos:
                this_session_uid = video.session_uid
                if this_session_uid is None:
                    raise SessionError(f"video {video.id} does not have a session_uid")
                elif session_uid is None:
                    session_uid = this_session_uid
                else:
                    assert session_uid == this_session_uid, f"{session_uid} != {this_session_uid}"
            timestamps = []
            metadata_list = self.get_asset_manager(asset_type=AssetsConstants.VIDEOS_ASSET_ID).search_meta_large(
                filters={"id": video_ids}
            )
            for _ in metadata_list:
                timestamps.append(_.get("start_time"))
                timestamps.append(_.get("end_time"))

            self.extend_time_span(session_uid=session_uid, timestamps=timestamps)

        return video_ids

    def get_video_frame_thumbnail(
            self,
            video_id: str,
            frame: int,
            thumbnail_tag: str) -> str:

        """Get thumbnail png for requested frame fram a video.

            Parameters
            ----------
            video_id:
                ID of the video to fetch the frame from.
            frame:
                The number 'n' for the n-th frame from the beginning.
            thumbnail_tag:
                Tag of the thumbnail to be created.

            Returns
            -------
            str
                URL for the requested thumbnail
        """

        video_amc = self.get_asset_manager(asset_type=AssetsConstants.VIDEOS_ASSET_ID)
        metadata = video_amc.get_metadata(id=video_id)
        thumbnails = metadata.get("thumbnails", {})
        frame_thumbnail_tag = "{}_frame_{}".format(thumbnail_tag, frame)

        object_access_dict = thumbnails.get(
            frame_thumbnail_tag, {}).get("object_access")

        if object_access_dict:
            object_access = ObjectAccess.from_dict(object_access_dict)
            url = video_amc.get_url_from_object_access(object_access)
            return url
        else:
            raise ThumbnailNotAvailableError("put a good error here")

    def extract_frame_thumbnails(
            self,
            ids: List[str],
            frames: List[int],
            thumbnail_tags: Optional[List[str]] = None,
            wait_for_completion: bool = False) -> str:
        """Extract thumbnails for a list of frames in a video.

            Parameters
            ----------
            ids:
                IDs of the videos to extract frame thumbnails from.
            frames:
                A list of frame numbers starting from the beginning of each video.
            thumbnail_tags:
                List of types of thumbnails tags to extract.

            Returns
            -------
            str
                The job ID of the Job that running the operation.
        """

        thumbnail_tags = thumbnail_tags or ["small", "full_size_png"]
        payload = {
            "ids": ids,
            "thumbnail_tags": thumbnail_tags,
            "frames": frames
        }

        resp = self.requests.post(
            "videos/extract_frame_thumbnails/",
            trailing_slash=False,
            json=payload)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)
        return job_id

    @deprecated("Use `add_lidars` instead")
    def add_lidar(
            self,
            set_id: str,
            lidar_path: Optional[str] = None,
            lidar_url: Optional[str] = None,
            lidar_uri: Optional[str] = None,
            lidar_bytes: Optional[Union[io.BytesIO, bytes, str]] = None,
            sensor: Optional[str] = None,
            timestamp: Optional[Union[str, datetime]] = None,
            session_uid: Optional[str] = None,
            id: Optional[str] = None,
            format: str = "pcd",
            binary_format: Optional[str] = None,
            num_fields: Optional[int] = None,
            enrichments: Optional[List[str]] = None,
            buffered_write: bool = False,
            add_to_session: bool = False,
            add_to_cache: bool = False,
            aux_metadata: Dict[str, Any] = None
    ) -> str:

        """Upload a LIDAR onto SceneBox.

           Upload a LIDAR with a local file path, URL, or URI.

           Parameters
           ----------
           lidar_path:
               The local path to the LIDAR to upload. If not None, lidar_uri and lidar_url should both be None.
           lidar_url:
               The URL of the LIDAR to upload. LIDAR must be publicly available.  If not None, lidar_path and
               lidar_uri should both be None.
           lidar_uri:
               The URI of the LIDAR to upload. Can be from a private source.  If not None, lidar_path, and lidar_url,
               should both be None.
           sensor:
                The sensor associated with the LIDAR.
           timestamp:
                The time at which the LIDAR was taken.
           session_uid:
                The session associated with the LIDAR.
           id:
               A unique LIDAR ID.  A common choice is the LIDAR filename.
           format:
               The format in which the LIDAR was embedded. pcd|numpy|binary. Default is pcd. PCD files
               are expected to be valid. Support for binary files is experimental.
           binary_format:
                Experimental. For binary data, a decoder to decode each packet to x,y,z,intensity,epoch. Format should be compatible
                with struct (https://docs.python.org/3/library/struct.html) library.
           num_fields:
               The number of fields exists in LIDAR file to reshape numpy array for displaying. Required for numpy formats
           set_id:
                The set to add the LIDAR to.
           enrichments:
                The types of enrichments to add to the LIDAR.
           buffered_write:
                If True, writes images in a buffered fashion.
           add_to_session:
                If True and session_uid is not None, add to the existing session with the passed session_uid.
           add_to_cache:
                If True, corresponding bytes will be added to cache for quick access.
           aux_metadata:
                Auxiliary metadata associated with the image (partitioned from primary metadata)

           Returns
           -------
           str
               The ID of the added LIDAR.

           Raises
           ------
           ValueError:
                If lidar_path, lidar_url, and lidar_uri are all None.

           """
        assert set_id, "`set_id` is None. Lidars need to be associated with a set"

        if lidar_path:
            filename, _, _, lidar_format = parse_file_path(lidar_path)
        elif lidar_url:
            filename = lidar_url.split("/")[-1]
        elif lidar_uri:
            filename = UriParser(uri=lidar_uri).key.split("/")[-1]
        elif lidar_bytes is not None:
            filename = get_guid()
        else:
            raise ValueError("Either LIDAR file path, uri or url must be provided")

        if timestamp is None:
            timestamp = datetime.utcnow()
        else:
            timestamp = datetime_or_str_to_iso_utc(timestamp)

        if format == "numpy":
            assert num_fields, "num_fields is needed for numpy data"
        elif format == "binary":
            assert binary_format, "binary_format is needed for binary data"
        else:
            assert format == "pcd", "format should be pcd, numpy, or binary"

        lidar_metadata = {"format": format,
                          "binary_format": binary_format,
                          "sensor": sensor,
                          "timestamp": timestamp,
                          "sets": [set_id] if set_id else []}

        if session_uid is not None:
            lidar_metadata["session_uid"] = session_uid

        if num_fields:
            lidar_metadata.update({"num_fields": num_fields})

        if aux_metadata:
            lidar_metadata[AUXILIARY_KEY] = aux_metadata

        if lidar_path:
            id = self.get_asset_manager(
                AssetsConstants.LIDARS_ASSET_ID).put_asset(
                file_path=lidar_path,
                filename=filename,
                metadata=lidar_metadata,
                id=id,
                wait_for_completion=not buffered_write,
                buffered_write=buffered_write
            )
        elif lidar_url or lidar_uri:
            id = self.get_asset_manager(
                AssetsConstants.LIDARS_ASSET_ID).put_asset(
                url=lidar_url,
                uri=lidar_uri,
                metadata=lidar_metadata,
                id=id,
                wait_for_completion=not buffered_write,
                buffered_write=buffered_write
            )
        elif lidar_bytes is not None:
            id = self.get_asset_manager(
                AssetsConstants.LIDARS_ASSET_ID).put_asset(
                file_object=lidar_bytes,
                metadata=lidar_metadata,
                id=id,
                wait_for_completion=not buffered_write,
                buffered_write=buffered_write,
                add_to_redis_cache=add_to_cache
            )
        else:
            raise ValueError(
                "Either file path or url, or uri must be provided ")

        # If session_uid does not exist skip creating and pushing the entity
        if session_uid and add_to_session:
            entity_dict = {
                "session": session_uid,
                "timestamp": timestamp,
                "enrichments": enrichments or [],
                "entity_name": EntityNames.LIDAR,
                "media_asset_id": id,
                "entity_id": get_guid(),
                "entity_value": id,
                "entity_type": EntityTypes.MEDIA,
                "influence": EntityInfluenceTypes.INTERVAL
            }
            self.add_entities(entity_dicts=[entity_dict])

        self.compress_lidars(
            ids=[id],
            skip_factors=[1, 10, 100]
        )
        return id

    def add_lidars(
            self,
            lidars: List[Lidar],
            set_id: Union[str, List[str]],
            add_to_session: bool = False,
            add_to_cache: bool = False,
            overwrite: bool = True
    ) -> List[str]:
        """Upload multiple videos onto SceneBox.

            Parameters
            ----------
            lidars:
                A list of objects of the type Lidar defined in models.Lidar. For Lidar objects that exist,
                the metadata is overwritten with the information provided in this call. For updating metadata,
                refer to asset_manager_client.update_metadata().
            set_id:
                The set (str) or sets (List[str]) to add the lidars to.
            add_to_session:
                If True and session_uid is not None, add to the existing session with the passed session_uid.
            add_to_cache:
                If True, corresponding bytes will be added to cache for quick access.
            overwrite:
                If False and asset exists on SceneBox, adds the previously uploaded lidars to the given set_id.
            Returns
            -------
            List[str]
               List of ids of the added lidars.

            Raises
            ------
            SetsErrorInvalidArgumentsError:
                If more than one of lidar path, url, uri, and bytes is not None

        """
        bulk_uploader = BulkLidarUploader(sec=self, compress_lidars=True)
        return bulk_uploader.preprocess_and_upload_bulk(assets=lidars,
                                                        add_to_session=add_to_session,
                                                        set_id=set_id,
                                                        add_to_cache=add_to_cache,
                                                        overwrite=overwrite
                                                        )

    def extract_lidars_from_s8(
            self,
            folder_uri: str,
            sensor: Optional[str] = None,
            session_uid: Optional[str] = None,
            fps: Optional[float] = None,
            extract_start_time: Optional[Union[datetime, str]] = None,
            extract_end_time: Optional[Union[datetime, str]] = None,
            set_id: Optional[str] = None,
            wait_for_completion: bool = False
    ) -> str:

        payload = {"folder_uri": folder_uri, "sensor": sensor or folder_uri.split("/")[-1]}

        if session_uid:
            payload["session_uid"] = session_uid
        if extract_start_time:
            payload["extract_start_time"] = datetime_or_str_to_iso_utc(
                extract_start_time)
        if extract_end_time:
            payload["extract_end_time"] = datetime_or_str_to_iso_utc(
                extract_end_time)
        if fps:
            payload["fps"] = fps
        if set_id:
            payload["set_id"] = set_id
        resp = self.requests.post(
            "lidars/extract_lidars_s8/",
            trailing_slash=False,
            json=payload)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)
        return job_id

    def enable_webapp_features(self, features: List[str]):
        """Enable a list of features on SceneBox WebApp.

            Parameters
            ----------
            features:
                A list of features to enable on SceneBox WebApp.
                For example: ["UPLOAD_RECORDING"]

            Returns
            -------

            Raises
            ------
            AssetError:
                If multiple org_configs are found.
                If org config exists but the name does not have a supported format.

        """
        organization_id = self.whoami()["organization_id"]

        existing_org_configs = self.get_asset_manager(asset_type=AssetsConstants.CONFIGS_ASSET_ID).search_assets(
            query={
                "filters": [
                    {
                        "field": "type",
                        "values": [
                            ConfigTypes.ORG_CONFIG
                        ],
                        "filter_out": False
                    }
                ]
            })
        if existing_org_configs:
            if len(existing_org_configs) > 1:
                raise AssetError("Multiple org_configs are found with ids ::: {}".format(existing_org_configs))

            config_meta = self.get_config(config_id=existing_org_configs[0], complete_info=True)
            if config_meta["name"] != "org_config__{}".format(organization_id):
                raise AssetError(
                    "Existing config name {}, does not have the supported format {}. "
                    "Either delete the existing config with id {} or update its name"
                    .format(config_meta["name"],
                           "org_config__{}".format(organization_id),
                           config_meta["id"])
                )
            existing_config = config_meta["config"]
            available_feature = existing_config.get("available_feature") or []
            available_feature.extend(features)
            existing_config["available_feature"] = available_feature
            self.delete_config(config_id=existing_org_configs[0])
            self.create_config(
                name="org_config__{}".format(organization_id),
                id=existing_org_configs[0],
                type=ConfigTypes.ORG_CONFIG,
                config=existing_config
            )
        else:
            self.create_config(
                name="org_config__{}".format(organization_id),
                type=ConfigTypes.ORG_CONFIG,
                config={
                    "available_feature": features
                }
            )

    def disable_webapp_features(self, features: List[str]):
        """Disable a list of features on SceneBox WebApp.

            Parameters
            ----------
            features:
                A list of features to disable on SceneBox WebApp.
                For example: ["UPLOAD_RECORDING"]

            Returns
            -------

            Raises
            ------
            AssetError:
                If multiple org_configs are found.
                If org config exists but the name does not have a supported format.

        """
        organization_id = self.whoami()["organization_id"]
        configs_amc = self.get_asset_manager(asset_type=AssetsConstants.CONFIGS_ASSET_ID)
        existing_org_configs = configs_amc.search_assets(
            query={
                "filters": [
                    {
                        "field": "type",
                        "values": [
                            ConfigTypes.ORG_CONFIG
                        ],
                        "filter_out": False
                    }
                ]
            })
        if existing_org_configs:
            if len(existing_org_configs) > 1:
                raise AssetError("Multiple org_configs are found with ids ::: {}".format(existing_org_configs))

            config_meta = self.get_config(config_id=existing_org_configs[0], complete_info=True)

            if config_meta["name"] != "org_config__{}".format(organization_id):
                raise AssetError(
                    "Existing config name {}, does not have the supported format {}. "
                    "Either delete the existing config with id {} or update its name"
                    .format(config_meta["name"],
                            "org_config__{}".format(organization_id),
                            config_meta["id"])
                )
            existing_config = config_meta["config"]
            available_feature = existing_config.get("available_feature") or []
            updated_available_feature = [feature for feature in available_feature if feature not in features]
            existing_config["available_feature"] = updated_available_feature
            configs_amc.update_metadata(id=config_meta["id"],
                                        metadata={"config": json.dumps(existing_config)},
                                        replace_sets=True)

    def index_s3_images_batch(self,
                              bucket: str,
                              folder: str,
                              thumbnailize_at_ingest: bool = True,
                              overwrite: bool = True,
                              wait_for_completion: bool = False,
                              extensions: Optional[Union[List[str], str]] = ValidExtensions.IMAGES,
                              max_wait_sec: Optional[int] = None
                              ) -> str:
        """Index s3 images.

        Ingest images in a given s3 bucket and folder.

        Parameters
        ----------
        bucket:
            The bucket name containing images for example "my_bucket".
        folder:
            The folder containing images for example "folder" or "folder/sub_folder".
        thumbnailize_at_ingest:
            If True, create thumbnail at ingestion time.  Otherwise, create thumbnails "on the fly".
        overwrite:
            If True, re-index the image which will overwrite an existing image with the same id.
        wait_for_completion:
            If True, polls until job is complete.  Otherwise, continues execution and does not raise an error
            if the job does not complete.
        extensions:
            Extensions of images to ingest. Pass "*" to ingest all objects with/without any extension.
        max_wait_sec:
            If a value is given, the wait for job completion will be for that many seconds.
            If None (default), and wait_for_completion is True, there will be no limit on the wait for job completion.

        Returns
        -------
        str
            The associated job id

        """

        if isinstance(extensions, str):
            extensions = [extensions]

        payload = {
            "bucket": bucket,
            "folder": folder,
            "thumbnailize_at_ingest": thumbnailize_at_ingest,
            "overwrite": overwrite,
            "extensions": extensions
        }

        resp = self.requests.post(
            "indexing/index_s3_objects/",
            json=payload)

        if not resp.ok:
            raise ResponseError("index_s3-objects failed -- {}".format(resp.content))

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id, max_wait_sec=max_wait_sec)

        return job_id

    def index_recording(self,
                        path: str,
                        recording_name: Optional[str] = None,
                        session_set_id: Optional[str] = None,
                        session_aux_metadata: Optional[dict] = None,
                        wait_for_completion: bool = False,
                        max_wait_sec: Optional[int] = None
                        ) -> str:
        """Index Recording.

        Ingests recording data into scenebox including avi videos, etc.

        Parameters
        ----------
        path:
            The path containing all including the bucket e.g. bucket/a/b/recording_name or bucket/recording_name
        recording_name:
            The name of the recording to ingest. This will be used as session name. If not given, will get that info
            from path
        session_set_id:
            The id of the existing session set id to add the new session to.
        session_aux_metadata:
            The auxiliary metadata to be added to session's metadata
        wait_for_completion:
            If True, polls until job is complete.  Otherwise, continues execution and does not raise an error
            if the job does not complete.
        max_wait_sec:
            If a value is given, the wait for job completion will be for that many seconds.
            If None (default), and wait_for_completion is True, there will be no limit on the wait for job completion.

        Returns
        -------
        str
            The associated job id

        """

        payload = {
            "uri": f"s3://{path.strip('/')}",
            "bucket": path.strip('/').split('/')[0],
            "recording_name": recording_name or path.strip('/').split('/')[-1],
            "session_set_id": session_set_id,
            "session_aux_metadata": session_aux_metadata or {}
        }

        resp = self.requests.post(
            "indexing/index_recording/",
            json=payload)

        if not resp.ok:
            raise ResponseError("index_recording failed -- {}".format(resp.content))

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id, max_wait_sec=max_wait_sec)

        return job_id

    def index_rosbag(self,
                     sets_prefix: str,
                     rosbag_uri: Optional[str] = None,
                     rosbag_path: Optional[str] = None,
                     session_name: Optional[str] = None,
                     session_uid: Optional[str] = None,
                     session_set_id: Optional[str] = None,
                     session_aux_metadata: Optional[dict] = None,
                     index_session_aux_keys: bool = False,
                     deep_analysis: Optional[bool] = False,
                     models: Optional[list] = None,
                     sensors: Optional[list] = None,
                     topics: Optional[list] = None,
                     session_resolution: float = 1.0,
                     image_skip_factor: int = 10,
                     indexing_parameters: Optional[dict] = None,
                     wait_for_completion: bool = False,
                     max_wait_sec: Optional[int] = None) -> str:
        """Index Ros1 files.

        Ingests ros1 data into scenebox, then extracts all available images, videos, and other asset types.

        Parameters
        ----------
        sets_prefix:
            The prefix to append on all created set names.
        rosbag_uri:
            The uri location of the folder containing the rosbag file
            If not None, rosbag_path should be None.
        rosbag_path:
            The local path of the rosbag
            If not None, rosbag_uri should be None.
        session_name:
            The name to give to the session or added previously to SceneBox which is associated with the indexed rosbag.
        session_uid:
            The uid of the session added previously to SceneBox and will be associated with the indexed rosbag.
            If not provided, the session will be added.
        session_set_id:
            The id of the existing session set id to add the new rosbag session to.
        session_aux_metadata:
            The auxiliary metadata to be added to session's metadata
        index_session_aux_keys:
            If set to true, will collect all the keys from session_aux and index them under available_keys
        deep_analysis:
            Enables enrichments such as object extraction, image/object embeddings, and UMAP visualizaion.
        models:
            A list of the models to use to enrich the rosbag data.  Choose from the models listed in
            scenebox.constants.AssetsConstants.MLModelConstants.
        sensors:
            A list of the sensors (listed in image metadata) to create videos from.
        topics:
            A list topics to ingest.  If no topics passed, all topics will be ingested.
        session_resolution:
            resolution of the ingested session in seconds
        image_skip_factor:
            skip factor for image messages
        indexing_parameters:
            indexing parameters for the rosbag ingestion
        wait_for_completion:
            If True, polls until job is complete.  Otherwise, continues execution and does not raise an error
            if the job does not complete.
        max_wait_sec:
            If a value is given, the wait for job completion will be for that many seconds.
            If None (default), and wait_for_completion is True, there will be no limit on the wait for job completion.

        Returns
        -------
        str
            The associated job id

        """
        enrichment_configs = [
            {
                "input_event": "geo_locations",
                "type": "location",
                "configuration": {
                    "influence_type": "interval",
                    "influence_radius_in_seconds": max(session_resolution, 100)
                }
            },
            {
                "input_event": "geo_locations",
                "type": "visibility",
                "configuration": {
                    "influence_type": "interval",
                    "influence_radius_in_seconds": max(session_resolution, 100)
                }
            },
            {
                "input_event": "geo_locations",
                "type": "weather",
                "configuration": {
                    "influence_type": "interval",
                    "influence_radius_in_seconds": max(session_resolution, 100)
                }
            },
        ]

        images_set_id = self.create_set(
            name="{}_{}".format(sets_prefix, AssetsConstants.IMAGES_ASSET_ID),
            asset_type=AssetsConstants.IMAGES_ASSET_ID,
            is_primary=True
        )
        videos_set_id = self.create_set(
            name="{}_{}".format(sets_prefix, AssetsConstants.VIDEOS_ASSET_ID),
            asset_type=AssetsConstants.VIDEOS_ASSET_ID,
            is_primary=True
        )
        lidars_set_id = self.create_set(
            name="{}_{}".format(sets_prefix, AssetsConstants.LIDARS_ASSET_ID),
            asset_type=AssetsConstants.LIDARS_ASSET_ID,
            is_primary=True
        )

        if not session_name:
            session_name = sets_prefix

        if deep_analysis and not models:
            raise IndexingException(
                "Provide a model/models e.g. {} to perform deep_analysis".format(MLModelConstants.MASK_RCNN_MODEL))

        if not session_uid:
            if session_aux_metadata and index_session_aux_keys:
                session_aux_keys = get_nested_keys(session_aux_metadata)
                session_aux_metadata["all_keys"] = session_aux_keys
            session_uid = self.add_session(session_name=session_name,
                                           session_type=SessionTypes.ROSBAGS_SESSION_ID,
                                           session_aux_metadata=session_aux_metadata or {},
                                           resolution=session_resolution,
                                           status=SessionStatuses.IN_PROGRESS,
                                           set_id=session_set_id
                                           )
            self.add_enrichments_configs(session_uid=session_uid,
                                         enrichments_configs=enrichment_configs,
                                         replace=True)
        else:
            self.get_asset_manager(AssetsConstants.SESSIONS_ASSET_ID).update_metadata(
                id=session_uid,
                metadata={"status": SessionStatuses.IN_PROGRESS}
            )
        if session_uid and session_aux_metadata:
            self.get_asset_manager(AssetsConstants.SESSIONS_ASSET_ID).update_metadata(
                id=session_uid,
                metadata={SESSION_AUXILIARY_KEY: session_aux_metadata})

        # Do pre-checks
        if [rosbag_uri, rosbag_path].count(None) != 1:
            raise ValueError("Please specify exclusively one of rosbag_uri, rosbag_path")

        if rosbag_path:
            filename = os.path.normpath(rosbag_path).split("/")[-1]
            with open(rosbag_path, "rb") as f:
                file_object = self.get_asset_manager(
                    asset_type=AssetsConstants.ROSBAGS_ASSET_ID).put_file(file_object=f)
            file_object.filename = filename
        elif rosbag_uri:
            filename = os.path.normpath(rosbag_uri).split("/")[-1]
            file_object = ObjectAccess(filename=filename, uri=rosbag_uri)

        else:
            raise ValueError("Either Rosbag folder path or uri must be provided.")

        index_rosbag_json = {
            "file_objects_dicts": [file_object.to_dic()],
            "search": None,
            "sets_map": {
                "images": images_set_id,
                "videos": videos_set_id,
                "lidars": lidars_set_id,
            },
            "session_uid": session_uid,
            "deep_analysis": deep_analysis,
            "models": models,
            "sensors": sensors,
            "indexing_parameters": indexing_parameters,
            "topics": topics,
            "image_skip_factor": image_skip_factor
        }

        if deep_analysis:
            objects_set_id = self.create_set(
                name="{}_{}".format(sets_prefix, AssetsConstants.OBJECTS_ASSET_ID),
                asset_type=AssetsConstants.OBJECTS_ASSET_ID,
                is_primary=True
            )
            index_rosbag_json["sets_map"]["objects"] = objects_set_id
        if session_set_id:
            index_rosbag_json["sets_map"]["sessions"] = session_set_id

        resp = self.requests.post(
            "indexing/index_rosbag/",
            json=index_rosbag_json)

        if not resp.ok:
            self.delete_session(session_uid=session_uid, wait_for_completion=True)
            raise ResponseError("index_rosbag failed -- {}".format(resp.content))

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id, max_wait_sec=max_wait_sec)

        return job_id

    def index_rosbag2(self,
                      sets_prefix: str,
                      relative_file_paths: List[str],
                      folder_uri: Optional[str] = None,
                      folder_path: Optional[str] = None,
                      session_name: Optional[str] = None,
                      session_set_id: Optional[str] = None,
                      deep_analysis: Optional[bool] = False,
                      models: Optional[list] = None,
                      sensors: Optional[list] = None,
                      topics: Optional[list] = None,
                      indexing_parameters: Optional[dict] = None,
                      session_resolution: float = 1.0,
                      wait_for_completion: bool = False) -> str:
        """Index Ros2 files.

        Ingests ros2 data into scenebox, then extracts all available images, videos, and other asset types.

        Parameters
        ----------
        sets_prefix:
            The prefix to append on all created set names.
        relative_file_paths:
            The relative file paths of rosbag files to ingest (.yaml/db3 files).  Relative according to specified
        folder_uri:
            The uri location of the folder containing the rosbag db3 file and metadata yaml file.
            If not None, folder_path should be None.
        folder_path:
            The local folder path of the folder containing the rosbag db3 file and metadata yaml file.
            If not None, folder_uri should be None.
        session_name:
            The name to give to the session associated with the indexed ros2.
        session_set_id:
            The id of the existing session set id to add the new ros2 session to.
        deep_analysis:
            Enables enrichments such as object extraction, image/object embeddings, and UMAP visualizaion.
        models:
            A list of the models to use to enrich the ros2 data.  Choose from the models listed in
            scenebox.constants.AssetsConstants.MLModelConstants.
        sensors:
            A list of the sensors (listed in image metadata) to create videos from.
        topics:
            A list topics to ingest.  If no topics passed, all topics will be ingested.
        indexing_parameters:
            indexing parameters for the rosbag ingestion
        session_resolution:
            resolution of the ingested session in seconds
        wait_for_completion:
            If True, polls until job is complete.  Otherwise, continues execution and does not raise an error
            if the job does not complete.

        Returns
        -------
        dict
            A dictionary containing "job_id" as the key and the associated job id as the value.

        """
        enrichment_configs = [
            {
                "input_event": "geo_locations",
                "type": "location",
                "configuration": {
                    "influence_type": "interval",
                    "influence_radius_in_seconds": session_resolution
                }
            },
            {
                "input_event": "geo_locations",
                "type": "visibility",
                "configuration": {
                    "influence_type": "interval",
                    "influence_radius_in_seconds": session_resolution
                }
            },
            {
                "input_event": "geo_locations",
                "type": "weather",
                "configuration": {
                    "influence_type": "interval",
                    "influence_radius_in_seconds": session_resolution
                }
            },
        ]

        images_set_id = self.create_set(
            name="{}_{}".format(sets_prefix, AssetsConstants.IMAGES_ASSET_ID),
            asset_type=AssetsConstants.IMAGES_ASSET_ID,
            is_primary=True
        )
        videos_set_id = self.create_set(
            name="{}_{}".format(sets_prefix, AssetsConstants.VIDEOS_ASSET_ID),
            asset_type=AssetsConstants.VIDEOS_ASSET_ID,
            is_primary=True
        )
        if deep_analysis:
            objects_set_id = self.create_set(
                name="{}_{}".format(sets_prefix, AssetsConstants.OBJECTS_ASSET_ID),
                asset_type=AssetsConstants.OBJECTS_ASSET_ID,
                is_primary=True
            )

        if not session_name:
            session_name = sets_prefix

        session_uid = self.add_session(session_name=session_name,
                                       session_type=SessionTypes.GENERIC_SESSION_ID,
                                       resolution=session_resolution,
                                       set_id=session_set_id)

        self.add_enrichments_configs(session_uid=session_uid,
                                     enrichments_configs=enrichment_configs,
                                     replace=True)

        file_objects_dicts = self.add_rosbag2(folder_uri=folder_uri,
                                              folder_path=folder_path,
                                              relative_file_paths=relative_file_paths)

        logger.info("Calling the index_rosbag endpoint...")
        index_rosbag_json = {
            "search": None,
            "sets_map": {
                "images": images_set_id,
                "videos": videos_set_id},
            "session_uid": session_uid,
            "deep_analysis": deep_analysis,
            "models": models,
            "sensors": sensors,
            "file_objects_dicts": file_objects_dicts,
            "topics": topics,
            "indexing_parameters": indexing_parameters
        }

        if deep_analysis:
            index_rosbag_json["sets_map"]["objects"] = objects_set_id
        if session_set_id:
            index_rosbag_json["sets_map"]["sessions"] = session_set_id

        resp = self.requests.post(
            "indexing/index_rosbag2/",
            json=index_rosbag_json)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)

        return job_id

    def add_rosbag2(self,
                    relative_file_paths: List[str],
                    folder_uri: Optional[str] = None,
                    folder_path: Optional[str] = None,
                    session_uid: Optional[str] = None,
                    set_id: Optional[str] = None,
                    ) -> List[dict]:

        """Upload Rosbag2 onto SceneBox.

           Upload Rosbag2 with a local file path, URL, or URI.  Can only process ros2.

           Parameters
           ----------
           relative_file_paths:
             The relative file paths of rosbag files to ingest (.yaml/db3 files).  Relative according to specified
             folder uri or path.
           folder_uri:
               The uri location of the folder containing the rosbag db3 file and metadata yaml file.
               If not None, folder_path should be None.
           folder_path:
               The local folder path of the folder containing the rosbag db3 file and metadata yaml file.
               If not None, folder_uri should be None.
           session_uid:
               The UID of the session.
           set_id:
               The set id to associate with the ingested rosbag.

           Returns
           -------
           str
               The ID of the added Rosbag2 asset.


           """

        # Do pre-checks
        if [folder_uri, folder_path].count(None) != 1:
            raise ValueError("Please specify exclusively one of rosbag_path, rosbag_uri, rosbag_url, or rosbag_bytes.")

        rosbag_metadata = {"sets": [set_id] if set_id else []}
        if session_uid is not None:
            rosbag_metadata["session_uid"] = session_uid

        if folder_path:
            filename_dict = {os.path.normpath(relative_path).split("/")[-1]: os.path.join(folder_path, relative_path)
                             for relative_path in relative_file_paths}

            file_objects_dicts = []
            for filename, filepath in filename_dict.items():
                with open(filepath, "rb") as open_file:
                    file_object = self.get_asset_manager(
                        asset_type=AssetsConstants.ROSBAGS_ASSET_ID).put_file(file_object=open_file)
                    file_object.filename = filename
                file_objects_dicts.append(file_object.to_dic())
        elif folder_uri:
            filename_dict = {os.path.normpath(relative_path).split("/")[-1]: os.path.join(folder_uri, relative_path)
                             for relative_path in relative_file_paths}

            file_objects_dicts = [ObjectAccess(filename=filename,
                                               uri=file_uri).to_dic() for filename, file_uri in filename_dict.items()]

        else:
            raise ValueError("Either Rosbag folder path or uri must be provided.")

        return file_objects_dicts

    def cleanup_annotation_masks(self,
                                 ids: Optional[List[str]] = None,
                                 search: Optional[dict] = None,
                                 force_reclean: bool = False,
                                 wait_for_completion: bool = True) -> str:
        payload = {
            "force_reclean": force_reclean
        }
        if ids is not None:
            payload["ids"] = ids
        if search is not None:
            payload["search"] = search

        resp = self.requests.post(
            "annotations/cleanup_annotation_masks/",
            trailing_slash=False,
            json=payload)
        if not resp.ok:
            raise ResponseError(
                "Could not clean_up the annotations: {}".format(
                    resp.content))

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            if ids is not None:
                self._wait_for_job_completion(
                    job_id, max_wait_sec=max(
                        10 * len(ids), 60))
            else:
                self._wait_for_job_completion(job_id, increments_sec=5)
        return job_id

    def annotations_to_objects(self,
                               ids: Optional[List[str]] = None,
                               search: Optional[dict] = None,
                               create_objects: bool = False,
                               margin_ratio: float = 0.1,
                               output_set_id: str = None,
                               margin_pixels: Optional[int] = None,
                               source_annotation_type: Optional[Union[str, None]] = None,
                               session_uid: Optional[str] = None,
                               add_to_session: bool = True,
                               wait_for_completion: bool = True,
                               progress_callback: Optional[Callable] = None) -> str:

        """Extracts objects from annotations.

        Converts annotations to objects from annotations that have been previously ingested into
        SceneBox.  Gets labels from the asset's auxiliary metadata.

        Parameters
        ----------
        ids:
            IDs of the previously ingested annotations.
        search:
            Query to locate the data subset of interest.  Filters through existing
            assets according to the dictionary passed.
        create_objects:
            If False and if mask annotations are available for the given asset id, adds the area of each annotation
            to the asset's auxiliary metadata.  Else, additionally creates object entities from the existing
            annotation data associated with the passed ID.
        margin_ratio:
            Widens/shrinks the object's area of interest.  A larger number increases the object's margin.
            Minimum value 0.
        margin_pixels:
            Widens/shrinks the object's area of interest by this amount. Minimum value 0. If both margin_rotio and
            margin_pixels are specified, margin_pixes takes precedence.
        output_set_id:
            The name of the set to add the created objects to, if create_objects is True.  Otherwise, has no effect.
        source_annotation_type:
            If given, extracts objects from the annotation type specified.  Otherwise, extracts objects from the
            any/all of the existing annotation types: polygons, bounding boxes, poses
        session_uid:
            The session associated with the objects.  Adds an event interval (and thus, an entity) to the existing
            session.
        add_to_session:
            Whether to add the object to the session with session_uid for session search
        wait_for_completion:
            If True, polls until job is complete.  Raises an error if job fails to finish after (2 * #ids) seconds
            if IDs are supplied.  Otherwise, continues execution and does not raise an error if the job does not
            complete.
        progress_callback:
            Callback function to log the progress of the inference job. The callback should accept a parameter of type
            float for progress.

        Returns
        -------
        str
            ID of the Job that runs/ran the object extraction job.

        Raises
        ------
        ResponseError
             If endpoint call does not get a valid response
        """
        payload = {
            'create_objects': create_objects,
            'margin_ratio': margin_ratio,
            'margin_pixels': margin_pixels,
            'output_set_id': output_set_id,
            'source_annotation_type': source_annotation_type
        }

        if ids is not None:
            payload["ids"] = ids
        if search is not None:
            payload["search"] = search

        if session_uid:
            payload["session_uid"] = session_uid
            payload["add_to_session"] = add_to_session

        resp = self.requests.post(
            "annotations/annotations_to_objects/",
            trailing_slash=False,
            json=payload)
        if not resp.ok:
            raise ResponseError(
                "Could not create objects from annotations: {}".format(
                    resp.content))

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            if ids is not None:
                self._wait_for_job_completion(
                    job_id, max_wait_sec=10 + 8 * len(ids),
                    progress_callback=progress_callback)
            else:
                self._wait_for_job_completion(job_id, progress_callback=progress_callback,
                                              increments_sec=5)
        return job_id

    def compress_masks_batch(
            self,
            thumbnail_tag: str,
            ids: Optional[List[str]] = None,
            search: Optional[dict] = None,
            wait_for_completion: bool = True) -> str:

        payload = {}
        if ids is not None:
            payload["ids"] = ids
        if search is not None:
            payload["search"] = search

        payload["thumbnail_tag"] = thumbnail_tag

        resp = self.requests.post(
            "annotations/compress_masks_batch/",
            trailing_slash=False,
            json=payload)
        if not resp.ok:
            raise ResponseError(
                "Could not create objects from annotations: {}".format(
                    resp.content))

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)
        return job_id

    def get_annotation_sources(self,
                               search: Optional[dict] = None) -> List[Optional[dict]]:

        """Returns all sources of annotation for all images or images that satisfy a search query

        Parameters
        ----------
        search:
            Query to locate the data subset of interest.  Filters through existing
            assets (images) according to the dictionary passed.

        Returns
        -------
        List
            a list of dictionaries that include provider, version, annotation_group,
            and annotation_type information for existing annotation sources

        """
        payload = search if search is not None else {}

        resp = self.requests.post(
            "annotations/annotation_sources/",
            trailing_slash=False,
            json=payload)
        if not resp.ok:
            raise ResponseError(
                "Could not fetch annotation sources: {}".format(
                    resp.content))

        return resp.json()

    def get_annotation_labels(self,
                              search: Optional[dict] = None) -> List[str]:

        """Returns all labels for all images or images that satisfy a search query

        Parameters
        ----------
        search:
            Query to locate the data subset of interest.  Filters through existing
            assets (images) according to the dictionary passed.

        Returns
        -------
        List
            a list of strings which are labels of existing annotation entities

        """
        payload = search if search is not None else {}

        resp = self.requests.post(
            "annotations/annotation_labels/",
            trailing_slash=False,
            json=payload)
        if not resp.ok:
            raise ResponseError(
                "Could not fetch labels: {}".format(
                    resp.content))

        return resp.json()

    def model_inference(self,
                        asset_type: str = AssetsConstants.IMAGES_ASSET_ID,
                        ids: Optional[List[str]] = None,
                        search: Optional[dict] = None,
                        model: str = MLModelConstants.MASK_RCNN_MODEL,
                        obtain_mask: bool = False,
                        obtain_bbox: bool = False,
                        obtain_object_entities: bool = False,
                        obtain_embeddings: bool = False,
                        threshold: Optional[float] = None,
                        classes_of_interest: Optional[List[str]] = None,
                        wait_for_completion: bool = False,
                        progress_callback: Optional[Callable] = None,
                        additional_params: Optional[Dict] = None
                        ):

        """Perform inference from a list of supported models. See for supported models.

        Extracts inferences such as masks, bounding boxes, objects, and/or embeddings on an asset of choice using a
        model of choice.  Select from Mask RCNN, StarDist, or Image Intensity Histogram.

        Parameters
        ----------
        asset_type:
            The type of assets to perform model inference on.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        ids:
            IDs of the previously uploaded assets on which to perform a model inference.
        search:
            Query to locate the data subset of interest.  Filters through existing
            assets according to the dictionary passed.
        model:
            The model to perform the inference with.  Select from Mask RCNN ('mrcnn'), StarDist ('stardist'), or Image
            Intensity Histogram ('histogram')
        obtain_mask:
            If True and model is Mask RCNN or StarDist, infer segmentations and add masks as a
            scenebox.models.annotation.SegmentationAnnotation.
            Otherwise, do nothing but log an error if the model chosen is Image Intensity Histogram.
        obtain_bbox:
            If True and model is Mask RCNN or StarDist, infer bounding boxes from masks add the masks as a
            scenebox.models.annotation.BoundingBoxAnnotation.
            Otherwise, do nothing but log an error if the model chosen is Image Intensity Histogram.
        obtain_object_entities:
            If True and model is Mask RCNN, obtains and adds object entities.
            Otherwise, do nothing but log an error if the model chosen is Image Intensity Histogram or StarDist.
        obtain_embeddings:
            If True, extract asset embeddings with the chosen model.
        image_size:
            If not None, resizes the input images to the provided size
            before performing inference(s).
            Otherwise, do nothing.
        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.
        progress_callback:
            Callback function to log the progress of the inference job. The callback should accept a parameter of type
            float for progress.
        additional_params:
            A JSON formatted key-value pair structure for additional parameters such as threshold and
            classes of interest supported by the chosen model.
        """

        payload = {
            "model": model,
            "obtain_mask": obtain_mask,
            "obtain_bbox": obtain_bbox,
            "obtain_object_entities": obtain_object_entities,
            "obtain_embeddings": obtain_embeddings,
            "asset_type": asset_type,
            "ids": ids or []
        }
        if threshold is not None:
            payload["threshold"] = threshold

        if classes_of_interest is not None:
            payload["classes_of_interest"] = classes_of_interest

        if search is not None:
            payload["search"] = search

        if additional_params is not None:
            # Combine params dictionaries
            payload = {**payload, **additional_params}

        resp = self.requests.post(
            "models/model_inference/",
            trailing_slash=False,
            json=payload)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id, progress_callback=progress_callback,
                                          increments_sec=5)
        return job_id

    def image_properties_enrichment(self,
                                    asset_type: str = AssetsConstants.IMAGES_ASSET_ID,
                                    properties: List[str] = None,
                                    ids: Optional[List[str]] = None,
                                    search: Optional[dict] = None,
                                    wait_for_completion: bool = False,
                                    progress_callback: Optional[Callable] = None,
                                    additional_params: Optional[Dict] = None
                                    ):

        """Enrich images or objects with classical image processing features.

        Enrich image or object assets with classical image properties/features such as brightness or contrast
        and add this as auxiliary metadata for the asset.

        Parameters
        ----------
        asset_type:
            The type of assets to perform enrichment on.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        ids:
            IDs of the previously uploaded assets on which to perform a model inference.
        search:
            Query to locate the data subset of interest.  Filters through existing
            assets according to the dictionary passed.
        properties:
            A list of strings for each property to be added to the metadata of the asset.
            Choose from ['mean_brightness', 'rms_contrast', 'variance_of_laplacian'].
        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.
        progress_callback:
            Callback function to log the progress of the inference job. The callback should accept a parameter of type
            float for progress.
        additional_params:
            A JSON formatted key-value pair structure for additional parameters such as batch_size for the task.
        """

        payload = {
            "ids": ids or [],
            "properties": properties,
            "asset_type": asset_type,
        }

        if search is not None:
            payload["search"] = search

        if additional_params is not None:
            # Combine params dictionaries
            payload = {**payload, **additional_params}

        resp = self.requests.post(
            "images/image_properties_enrichment/",
            trailing_slash=False,
            json=payload)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id, progress_callback=progress_callback,
                                          increments_sec=5)
        return job_id

    def submit_enricher(self,
                        enricher_class: Type[Enricher]) -> str:
        if not issubclass(enricher_class, Enricher):
            raise AssetError("Problem with Enricher class")

        metadata = {
            "version": enricher_class.version,
            "type": "enricher",
            TIMESTAMP_FIELD: datetime.utcnow()
        }

        id = "{}_{}_{}".format(enricher_class.__name__, enricher_class.version, get_truncated_uid())

        return self.get_asset_manager(asset_type=AssetsConstants.UDFS_ASSET_ID).put_asset(
            metadata=metadata,
            file_object=self.__serialize_class(enricher_class),
            id=id
        )

    def enricher_dry_run(self,
                         enricher_class: Type[Enricher],
                         metadata: dict
                         ):

        enricher_id = self.submit_enricher(enricher_class=enricher_class)

        payload = {
            "udf_ids": [enricher_id],
            "metadata": metadata
        }

        resp = self.requests.post(
            "udfs/enricher_dry_run/",
            trailing_slash=False,
            json=payload)

        return resp.json()

    def enricher_batch(
            self,
            enricher_class: Type[Enricher],
            assets_type: str,
            ids: Optional[List[str]] = None,
            search: Optional[dict] = None,
            wait_for_completion: bool = False
    ) -> str:

        payload = {
            "ids": ids or []
        }

        if search is not None:
            payload["search"] = search

        enricher_id = self.submit_enricher(enricher_class=enricher_class)

        payload["udf_ids"] = [enricher_id]
        payload["assets_type"] = assets_type

        resp = self.requests.post(
            "udfs/batch_enrich/",
            trailing_slash=False,
            json=payload)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)
        return job_id

    def register_webhook(self,
                         webhook_class: Type[Webhook]) -> str:
        if not issubclass(webhook_class, Webhook):
            raise AssetError("Input is not a webhook class")

        metadata = {
            "version": webhook_class.version,
            "type": "webhook",
            TIMESTAMP_FIELD: datetime.utcnow()
        }
        webhook_id = self.get_asset_manager(asset_type=AssetsConstants.UDFS_ASSET_ID).put_asset(
            metadata=metadata,
            file_object=self.__serialize_class(webhook_class),
            id="{}_{}".format(webhook_class.__name__, webhook_class.version)
        )

        return webhook_id

    def run_script(self,
                   script_class: Type[Script],
                   wait_for_completion: bool = True,
                   **kwargs
                   ) -> str:
        if not issubclass(script_class, Script):
            raise AssetError("Input is not a script class")

        metadata = {
            "version": script_class.version,
            "type": "script",
            TIMESTAMP_FIELD: datetime.utcnow()
        }
        script_id = self.get_asset_manager(asset_type=AssetsConstants.UDFS_ASSET_ID).put_asset(
            metadata=metadata,
            file_object=self.__serialize_class(script_class),
            id=standardize_name("{}_{}_{}".format(script_class.__name__, script_class.version, get_truncated_uid()))
        )

        resp = self.requests.put(
            "udfs/run_script/{}".format(script_id),
            trailing_slash=False,
            json=kwargs)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)
        return job_id

    def extract_images_from_videos(
            self,
            video_id: str,
            extract_start_time: Optional[Union[datetime, str]] = None,
            extract_end_time: Optional[Union[datetime, str]] = None,
            fps: Optional[float] = None,
            set_id: Optional[id] = None,
            wait_for_completion: bool = False
    ) -> str:
        """
        Extract images from video

        Parameters
        ----------
        video_id:
            id of the video to extract images from
        extract_start_time:
            optional start timestamp for extraction interval.
            If not given, will be set to start timestamp of the video.
        extract_end_time:
            optional end timestamp for extraction interval.
            If not given, will be set to end timestamp of the video.
        fps:
            desired fps (frame per second) value for extraction
            If not given, default value of 1.0 / 3.0 will be used.
        set_id:
            The ID of the set to add the images to
        wait_for_completion:
            If True, polls until job is complete.  Raises an error if job fails to finish after (2 * #ids) seconds
            if IDs are supplied.  Otherwise, continues execution and does not raise an error if the job does not
            complete.

        Returns
        -------
        str
            The ID of the Job that attempts to perform image extraction.
        """

        payload = {
            "id": video_id
        }
        if extract_start_time:
            payload["extract_start_time"] = datetime_or_str_to_iso_utc(
                extract_start_time)

        if extract_end_time:
            payload["extract_end_time"] = datetime_or_str_to_iso_utc(
                extract_end_time)

        if fps:
            payload["fps"] = fps

        if set_id:
            payload["set_id"] = set_id

        resp = self.requests.post(
            "videos/extract_images/",
            trailing_slash=False,
            json=payload)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)
        return job_id

    def extract_images_s8(
            self,
            folder_uri: Optional[str] = None,
            sensor: Optional[str] = None,
            session_uid: Optional[str] = None,
            fps: Optional[float] = None,
            extract_start_time: Optional[Union[datetime, str]] = None,
            extract_end_time: Optional[Union[datetime, str]] = None,
            set_id: Optional[str] = None,
            wait_for_completion: bool = False
    ) -> str:

        payload = {}
        if extract_start_time:
            payload["extract_start_time"] = datetime_or_str_to_iso_utc(
                extract_start_time)

        if extract_end_time:
            payload["extract_end_time"] = datetime_or_str_to_iso_utc(
                extract_end_time)

        if folder_uri:
            payload["folder_uri"] = folder_uri

        if sensor:
            payload["sensor"] = sensor

        if session_uid:
            payload["session_uid"] = session_uid

        if fps:
            payload["fps"] = fps

        if set_id:
            payload["set_id"] = set_id

        resp = self.requests.post(
            "videos/extract_images_s8/",
            trailing_slash=False,
            json=payload)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)
        return job_id

    def extract_subclip_from_videos(
            self,
            video_id: str,
            subclip_id: Optional[str] = None,
            extract_start_time: Optional[Union[datetime, str]] = None,
            extract_end_time: Optional[Union[datetime, str]] = None,
            set_id: Optional[str] = None,
            wait_for_completion: bool = False
    ) -> str:
        """Create a subclip of a video.

        Parameters
        ----------
        video_id:
            The ID of the full-length video to extract from
        subclip_id:
            The ID of the generated subclip
        extract_start_time:
            The time in the full-length video to start the subclip from
        extract_end_time:
            The time in the full-length video to end the subclip at
        set_id:
            The ID of the set to place the generated subclip into
        wait_for_completion:
            If True, polls until job is complete.  Otherwise, continues execution and does not raise an error
            if the job does not complete.

        Returns
        -------
        str
            The job ID of the Job that tracks the subclip extraction.
        """

        payload = {
            "id": video_id
        }
        if extract_start_time:
            payload["extract_start_time"] = datetime_or_str_to_iso_utc(
                extract_start_time)

        if extract_end_time:
            payload["extract_end_time"] = datetime_or_str_to_iso_utc(
                extract_end_time)

        if subclip_id:
            payload["subclip_id"] = subclip_id

        if set_id:
            payload["set_id"] = set_id

        resp = self.requests.post(
            "videos/extract_subclip_video/",
            trailing_slash=False,
            json=payload)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)
        return job_id

    def extract_video_from_s8(
            self,
            folder_uri: str,
            sensor: Optional[str] = None,
            session_uid: Optional[str] = None,
            video_id: Optional[str] = None,
            extract_start_time: Optional[Union[datetime, str]] = None,
            extract_end_time: Optional[Union[datetime, str]] = None,
            tags: Optional[List[str]] = None,
            set_id: Optional[str] = None,
            skip_frame: int = 0,
            wait_for_completion: bool = False
    ) -> str:

        payload = {"folder_uri": folder_uri,
                   "sensor": sensor or folder_uri.split("/")[-1],
                   "skip_frame": skip_frame}

        if session_uid:
            payload["session_uid"] = session_uid
        if tags:
            payload["tags"] = tags
        if extract_start_time:
            payload["extract_start_time"] = datetime_or_str_to_iso_utc(
                extract_start_time)
        if extract_end_time:
            payload["extract_end_time"] = datetime_or_str_to_iso_utc(
                extract_end_time)
        if video_id:
            payload["video_id"] = video_id
        if set_id:
            payload["set_id"] = set_id
        resp = self.requests.post(
            "videos/extract_video_s8/",
            trailing_slash=False,
            json=payload)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)
        return job_id

    def make_video_from_image_uris(
            self,
            bucket: str,
            folder: str,
            cloud_storage: str,
            sensor: str,
            session_uid: Optional[str] = None,
            video_id: Optional[str] = None,
            tags: Optional[List[str]] = None,
            set_id: Optional[str] = None,
            image_skip_factor: int = 1,
            wait_for_completion: bool = False
    ) -> str:
        """
        Make video from frames in a given cloud_storage, bucket, and folder.
        The path "{cloud_storage}://{bucket}/{folder}/" should contain frames with the following format:
        Unix_timestamps_in_nanoseconds.extension e.g. 1664999890113942016.jpeg
        
        Parameters
        ----------
        bucket:
            bucket where the frames are located
        folder:
            folder where the frames are located. Note that bucket should not be included here.
        cloud_storage:
            cloud provider e.g. s3 or gs
        sensor:
            Sensor name associated with the image uris
        session_uid:
            The ID of the session that the images and video belong to
        video_id:
            The ID of the video
        tags:
            Tags to add to video metadata
        set_id:
            The ID of the set to add the video to
        image_skip_factor:
            An integer number to use, if user wants to skip images when making video. Default is 1; skiping no image.
        wait_for_completion:
            If True, polls until job is complete.  Raises an error if job fails to finish after (2 * #ids) seconds
            if IDs are supplied.  Otherwise, continues execution and does not raise an error if the job does not
            complete.

        Returns
        -------
        str
            The ID of the Job that attempts to perform video making.
        """

        payload = {"bucket": bucket,
                   "folder": folder,
                   "cloud_storage": cloud_storage,
                   "sensor": sensor,
                   "image_skip_factor": image_skip_factor}

        if session_uid:
            payload["session_uid"] = session_uid
        if tags:
            payload["tags"] = tags
        if video_id:
            payload["video_id"] = video_id
        if set_id:
            payload["set_id"] = set_id
        resp = self.requests.post(
            "videos/make_video_from_image_uris/",
            trailing_slash=False,
            json=payload)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)
        return job_id

    def make_video_with_annotations_from_uris(
            self,
            timestamps_image_uris_csv_filepath: str,
            sensor: str,
            width: int,
            height: int,
            image_format: str,
            session_uid: Optional[str] = None,
            video_id: Optional[str] = None,
            tags: Optional[List[str]] = None,
            set_id: Optional[str] = None,
            image_skip_factor: int = 1,
            wait_for_completion: bool = False
    ) -> str:
        """
        Make video with overlayed annotations from provided image uris and annotaion uris per provider

        Parameters
        ----------
        timestamps_image_uris_csv_filepath:
            filepath for the csv file that contains two columns; timestamp and image_uri
        sensor:
            Sensor name associated with the image uris
        width:
            Width of images
        height:
            Height of images
        image_format:
            Format of images e.g. png
        session_uid:
            The ID of the session that the images and video belong to
        video_id:
            The ID of the video
        tags:
            Tags to add to video metadata
        set_id:
            The ID of the set to add the video to
        image_skip_factor:
            An integer number to use, if user wants to skip images when making video. Default is 1; skiping no image.
        wait_for_completion:
            If True, polls until job is complete.  Raises an error if job fails to finish after (2 * #ids) seconds
            if IDs are supplied.  Otherwise, continues execution and does not raise an error if the job does not
            complete.

        Returns
        -------
        str
            The ID of the Job that attempts to perform video making.
        """
        with open(timestamps_image_uris_csv_filepath, 'rb') as f:
            file_object = f.read()
        object_access = self.get_asset_manager(
            asset_type=AssetsConstants.IMAGES_ASSET_ID).put_file(
            file_object=file_object
        )
        self.get_asset_manager(
            asset_type=AssetsConstants.SESSIONS_ASSET_ID).update_metadata(
            id=session_uid,
            metadata={
                "csv_object_access_{}".format(sensor): object_access.to_dic()
            }
        )
        payload = {"csv_object_access": object_access.to_dic(),
                   "width": width,
                   "height": height,
                   "image_format": image_format,
                   "sensor": sensor,
                   "image_skip_factor": image_skip_factor}

        if session_uid:
            payload["session_uid"] = session_uid
        if tags:
            payload["tags"] = tags
        if video_id:
            payload["video_id"] = video_id
        if set_id:
            payload["set_id"] = set_id
        resp = self.requests.post(
            "videos/make_video_with_annotations_from_uris/",
            trailing_slash=False,
            json=payload)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)
        return job_id

    def images_to_video(self,
                        video_set_id: str,
                        session_uid: str,
                        sensor: str,
                        fps: Optional[int] = None,
                        search: Optional[dict] = None,
                        image_format: Optional[str] = None,
                        video_id: Optional[str] = None,
                        wait_for_completion: bool = False) -> str:

        payload = {
            "id": video_id,
            "sensor": sensor,
            "search": search,
            "image_format": image_format,
            "session_uid": session_uid,
            "video_id": video_id or get_guid(),
            "fps": fps,
            "video_set_id": video_set_id
        }
        resp = self.requests.post(
            "videos/images_to_video/",
            trailing_slash=False,
            json=payload)
        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)
        return job_id

    def similarity_search_bulk_index(
            self,
            embedding_ids: Optional[List[str]] = None,
            search_dic: Optional[dict] = None,
            wait_for_completion: bool = False) -> str:
        """Bulk indexes embeddings to allow for similarity search.

        Existing embeddings are mapped to a high-dimensional vector space. Then a distance measure is applied to find
        which assets are the most similar. After running this method, similarity search is available for the assets
        associated with the inputted embeddings.

        Parameters
        ----------
        embedding_ids:
            The IDs of the embeddings to bulk index.
        search_dic:
            Query to locate the data subset of interest.  Filters through existing
            assets according to the dictionary passed.
        wait_for_completion:
            If True, polls until job is complete.  Raises an error if job fails to finish after (2 * #ids) seconds
            if IDs are supplied.  Otherwise, continues execution and does not raise an error if the job does not
            complete.

        Returns
        -------
        str
            The ID of the Job that attempts to perform bulk indexing.
        """

        payload = {}
        if embedding_ids is not None:
            payload["embedding_ids"] = embedding_ids
        if search_dic is not None:
            payload["search_dic"] = search_dic

        # logger.debug("Bulk index payload: {}".format(payload))

        resp = self.requests.post(
            "similarity_search/bulk_index/",
            trailing_slash=False,
            json=payload)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)

        return job_id

    def create_umap(
            self,
            asset_type: str,
            index_name: str,
            search_dic: Optional[dict] = None,
            n_neighbors: int = 20,
            min_dist: float = 0.3,
            train_size: int = 10000,
            progress_callback: Optional[Callable] = None,
            transform_only: bool = False,
            wait_for_completion: bool = False) -> str:

        """Applies UMAP onto existing asset indices.

        Applies UMAP (Uniform Manifold Approximation and Projection) to existing asset embeddings, and outputs a visual
        representation of the embeddings space.  Can be viewed from the "Embeddings" view on the SceneBox web app.

        .. note:: Embeddings must be indexed before this function can be used.

        Parameters
        ----------
        asset_type:
            The type of asset to apply UMAP on.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        index_name:
            index_name of the embeddings.  Used to filter through the embeddings metadata.
        search_dic:
            Query to locate the data subset of interest.  Filters through existing
            assets according to the dictionary passed.
        n_neighbors:
            Controls how UMAP balances local vs. global structure in data.  Low values of ``n_neighbours`` forces UMAP
            to concentrate on local structure, while high values push UMAP to look at larger neighbourhoods of each
            point.
        min_dist:
            Controls how tightly UMAP is allowed to pack points together.
        train_size:
            How much of the data should be used to train the umap. Default is 10000
        progress_callback:
            Callback function to log the progress of the inference job. The callback should accept a parameter of type
            float for progress.
        transform_only:
            If umap already exists and new data is needed to be transformed to the same embedding space, setting this
            parameter to True will take care of that.
        wait_for_completion:
            If True, polls until job is complete.
            Otherwise, continues execution and does not raise an error if the job does not complete.

        Returns
        -------
        str
            The job_id of the Job that applies UMAP.
        """

        payload = {
            "search": search_dic or {},
            "n_neighbors": n_neighbors,
            "min_dist": min_dist,
            "index_name": index_name,
            "asset_type": asset_type,
            "train_size": train_size,
            "transform_only": transform_only,
        }

        resp = self.requests.post(
            "embeddings/create_umap_from_assets/",
            trailing_slash=False,
            json=payload)

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id,
                                          progress_callback=progress_callback,
                                          increments_sec=5)

        return job_id

    def search_similar_assets(self,
                              id: str,
                              similar_asset_count: int = 10,
                              asset_type: str = AssetsConstants.IMAGES_ASSET_ID,
                              embedding_space: Optional[str] = None
                              ) -> List[str]:
        """Find top k similar assets to an existing asset with embeddings.

       Parameters
       ----------
       id:
           asset id.
       similar_asset_count:
           count of similar assets (10 by default)
       asset_type:
           type of assets (Images by default)
           To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
       embedding_space:
           embedding space in which similarity is performed on. Ineffective/optional if there is only one embedding
           space

       Returns
       -------
       list
           list of asset ids similar to the asset sorted by most to least similar.
       """

        metadata = self.get_asset_manager(asset_type=asset_type).get_metadata(id=id)
        embeddings = metadata.get("embeddings", {})

        if len(embeddings) == 1:
            embedding_space = list(embeddings.keys())[0]

        elif len(embeddings) > 1:
            if not embedding_space:
                raise SimilaritySearchError("embedding space should be specified")
            elif embedding_space not in embeddings:
                raise SimilaritySearchError("{} is not in the embeddings of asset".format(embedding_space))
        else:
            # len(embeddings) == 0:
            raise SimilaritySearchError("{} with id={} does not have embeddings".format(asset_type, id))

        payload = {
            "ids": [id],
            "similar_asset_count": similar_asset_count,
            "index_name": embedding_space,
            "asset_type": asset_type,
        }

        resp = self.requests.post(
            "similarity_search/similarity_search/",
            trailing_slash=False,
            json=payload)

        if not resp.ok:
            raise SimilaritySearchError(
                "finding {} assets similar to {} failed: {}".format(asset_type, id, resp.content))

        return resp.json()[0]

    def download_annotations(self,
                             ids: List[str],
                             folder_path: Optional[str] = None) -> Dict:
        """
        Download annotations to a destination folder including the mask files

        Parameters
        -----------
        ids:
            list of annotation ids
        folder_path:
            optional destination folder_path. If not given, all objects will be downloaded and returned as a result
        """
        annotations_amc = self.get_asset_manager(
            asset_type=AssetsConstants.ANNOTATIONS_ASSET_ID)
        annotations_meta = annotations_amc.search_meta_large(
            filters={"id": ids}
        )

        if not annotations_meta:
            logger.warning("could not find any annotations")
            return {}

        results = {}

        def fetch_annotation(annotation_meta):
            id = annotation_meta["id"]
            annotation_result = {"metadata": annotation_meta}

            masks = annotation_meta.get("masks", {})
            mask_result = {}
            for mask_id, object_access_dict in masks.items():
                mask_result[mask_id] = annotations_amc.get_bytes_from_object_access(
                    object_access=ObjectAccess(url=object_access_dict.get("url"),
                                               uri=object_access_dict.get("uri"))
                )
            if mask_result:
                annotation_result["masks"] = mask_result
            results[id] = annotation_result

        run_threaded(fetch_annotation, annotations_meta, desc="downloading annotations", unit="annotations")

        if folder_path:
            if not os.path.exists(folder_path):
                raise NotADirectoryError(f"{folder_path} does not exist!")

            for id, annotation_result in results.items():
                with open(os.path.join(folder_path, f"{id}.json"), "w") as f:
                    f.write(json.dumps(annotation_result["metadata"], ensure_ascii=False, indent=4))
                masks = annotation_result.get("masks", {})
                if masks:
                    masks_path = os.path.join(folder_path, id)
                    if not os.path.exists(masks_path):
                        os.makedirs(masks_path)
                    for mask_id, bytes_obj in masks.items():
                        with open(os.path.join(masks_path, mask_id), "wb") as f:
                            f.write(bytes_obj)
        return results

    def add_user(self,
                 email: str,
                 username: str,
                 role: str,
                 organization_id: str) -> Dict:
        """Add a new SceneBox user account to your organization.

        Parameters
        ----------
        email:
            E-mail of the user to add.
        username:
            Username of the user to add.
        role:
            Role of the user to add. Choose from admin, tester, health_checker, data_provider, data_user, or
            public_user. See the SceneBox user guides for more information.
        organization_id:
            Organization id to add the user to.

        Returns
        -------
        dict
            The successfully created user ``username``, ``email``, ``role``, and ``organization``.

        """
        req = self.requests.post(
            "identity_manager/user",
            json={
                "username": username,
                "email": email,
                "role": role,
                "organization_id": organization_id},
            remove_version=True
        )
        if not req.ok:
            raise InvalidAuthorization(
                "cannot add user {}-{}".format(username, req.text))
        doc = req.json()

        user_dict = {
            "username": username,
            "organization_id": doc.get("organization_id"),
            "token": doc.get("token"),
            "role": doc.get("role"),
            "email": doc.get("email")
        }

        return user_dict

    def modify_user(
            self,
            username: str,
            email: Optional[str] = None,
            role: Optional[str] = None,
            organization_id: Optional[str] = None):
        """Modify an existing user account.

        Please note that an existing user's username cannot be changed.

        Parameters
        ----------
        username:
            The user username to modify.
        email:
            The new user email.
        role:
            The new user role. Choose from admin, tester, health_checker, data_provider, data_user, or
            public_user. See the SceneBox user guides for more information.
        organization_id:
            The new user organization.
        """
        payload = {}

        if email:
            payload.update({"email": email})
        if role:
            payload.update({"role": role})
        if organization_id:
            payload.update({"organization_id": organization_id})

        req = self.requests.put(
            "identity_manager/user/{}".format(username),
            json=payload,
            remove_version=True
        )
        if not req.ok:
            raise InvalidAuthorization(
                "cannot modify user {}-{}".format(username, req.text))

    def delete_user(self, username: str):
        req = self.requests.delete(
            "identity_manager/user/{}".format(username),
            remove_version=True
        )
        if not req.ok:
            raise InvalidAuthorization(
                "cannot delete user {}-{}".format(username, req.text))

    def list_users(self) -> List[Dict]:
        """Returns a list of all users.

        Returns
        -------
        List[Dict]:
            Returns a dictionary of username, organization name, role, email, and token for each user.
        """
        req = self.requests.get("identity_manager/user", remove_version=True)
        return req.json()

    def add_organization(self, organization_name: str) -> dict:
        """Add a new SceneBox organization. Requires superadmin privilege.

        Parameters
        ----------
        organization_name:
            organization name.

        Returns
        -------
        dict
            The successfully created organization ``id``, ``name``.

        """
        req = self.requests.post(
            "identity_manager/organization",
            json={
                "organization_name": organization_name},
            remove_version=True
        )
        if not req.ok:
            raise InvalidAuthorization(
                "cannot add organization {}-{}".format(organization_name, req.text))
        doc = req.json()

        organization_dict = {
            "name": doc.get("name"),
            "id": doc.get("id")}

        return organization_dict

    def list_organizations(self) -> List[Dict]:
        """Returns a list of all organizations.

        Returns
        -------
        List[Dict]:
            Returns a list of dictionary of organization name and id.
        """
        req = self.requests.get("identity_manager/organization", remove_version=True)
        return req.json()

    def modify_organization(
            self,
            organization_id: str,
            organization_name: str):
        """Modify an existing organization.
        Parameters
        ----------
        organization_id:
            Organization id

        organization_name:
            The new organization name.
        """
        payload = {"organization_name": organization_name}

        req = self.requests.put(
            "identity_manager/organization/{}".format(organization_id),
            json=payload,
            remove_version=True
        )
        if not req.ok:
            raise InvalidAuthorization(
                "cannot modify organization {}-{}".format(organization_id, req.text))

    def delete_organization(self, organization_id: str):
        req = self.requests.delete(
            "identity_manager/organization/{}".format(organization_id),
            remove_version=True
        )
        if not req.ok:
            raise InvalidAuthorization(
                "cannot delete organization {}-{}".format(organization_id, req.text))

    def add_ownership(self, owner: str, access: str):
        req = self.requests.post(
            "identity_manager/ownership",
            json={
                "owner": owner,
                "access": access
            },
            remove_version=True
        )
        if not req.ok:
            raise InvalidAuthorization(
                "cannot add ownership for owner {} have access to {}-{}".format(owner, access, req.text))

    def revoke_ownership(self, owner: str, access: str):
        self.requests.delete("identity_manager/ownership",
                             json={
                                 "owner": owner,
                                 "access": access
                             },
                             remove_version=True)

    def list_ownerships(self) -> List[Dict]:
        """Returns a list of all ownerships.

        Returns
        -------
        List[Dict]
            A list of what ownerships the user associated with

        """
        req = self.requests.get(
            "identity_manager/ownership",
            remove_version=True)
        return req.json()

    def delete_all_data(self):
        self.requests.post(
            "maintenance/cleanup/",
            remove_version=True)

    def get_frontend_url(self,
                         path: str) -> str:
        safe_url = quote(path, safe="/:?=&")
        full_url = "{}/{}".format(self.front_end_url, safe_url)
        return full_url

    def __display_url(self,
                      url: str):
        try:
            full_url = self.get_frontend_url(path=url)
            display(Javascript('window.open("{url}");'.format(url=full_url)))
        except NameError:
            logger.error(
                "Cannot display in this environment- Please use Colab or Jupyter")

    def display_image(self, image_id: str):
        """Display a given image on the SceneBox web app.

        Note
        ----
        This method will only run properly from a Google Colab or Jupyter notebook.  Please also make sure
        that you are logged into the SceneBox web app, and that pop-ups are allowed in your browser.

        Parameters
        ----------
        image_id:
            The ID of the image to display on the SceneBox web app.
        """
        self.__display_url(url="images?image={}".format(image_id))

    def display_video(self, video_id: str):
        """Display a given image on the SceneBox web app.

        Note
        ----
        This method will only run properly from a Google Colab or Jupyter notebook.  Please also make sure
        that you are logged into the SceneBox web app, and that pop-ups are allowed in your browser.

        Parameters
        ----------
        video_id:
            The ID of the video to display on the SceneBox web app.
        """
        self.__display_url(url="videos?video={}".format(video_id))

    def display_object(self, object_id: str):
        """Display a given object on the SceneBox web app.

        Note
        ----
        This method will only run properly from a Google Colab or Jupyter notebook.  Please also make sure
        that you are logged into the SceneBox web app, and that pop-ups are allowed in your browser.

        Parameters
        ----------
        object_id:
            The ID of the object to display on the SceneBox web app.
        """
        self.__display_url(url="objects?object={}".format(object_id))

    def display_lidar(self, lidar_id: str):
        """Display a given Lidar on the SceneBox web app.

        Note
        ----
        This method will only run properly from a Google Colab or Jupyter notebook.  Please also make sure
        that you are logged into the SceneBox web app, and that pop-ups are allowed in your browser.

        Parameters
        ----------
        lidar_id:
            The ID of the Lidar to display on the SceneBox web app.
        """
        self.__display_url(url="lidars?lidar={}".format(lidar_id))

    def display_session(self, session_uid: str):
        """Display a given session on the SceneBox web app.

        Note
        ----
        This method will only run properly from a Google Colab or Jupyter notebook.  Please also make sure
        that you are logged into the SceneBox web app, and that pop-ups are allowed in your browser.

        Parameters
        ----------
        session_uid:
            The ID of the session to display on the SceneBox web app.
        """
        self.__display_url(url="sessions?session_uid={}".format(session_uid))

    def display_set(self, set_id: str):
        """Display a given set on the SceneBox web app.

        Note
        ----
        This method will only run properly from a Google Colab or Jupyter notebook.  Please also make sure
        that you are logged into the SceneBox web app, and that pop-ups are allowed in your browser.

        Parameters
        ----------
        set_id:
            The ID of the set to display on the SceneBox web app.
        """
        self.__display_url(url="sets?set={}".format(set_id))

    def display_projects(self, project_id: str):
        """Display a given project on the SceneBox web app.

        Note
        ----
        This method will only run properly from a Google Colab or Jupyter notebook.  Please also make sure
        that you are logged into the SceneBox web app, and that pop-ups are allowed in your browser.

        Parameters
        ----------
        project_id:
            The ID of the project to display on the SceneBox web app.
        """
        self.__display_url(url="projects?project={}".format(project_id))

    def display_dashboard(self, dashboard_name: str):
        """Display a given dashboard on the SceneBox web app.

        Note
        ----
        This method will only run properly from a Google Colab or Jupyter notebook.  Please also make sure
        that you are logged into the SceneBox web app, and that pop-ups are allowed in your browser.

        Parameters
        ----------
        dashboard_name:
            The Name of the dashboard to display on the SceneBox web app.
        """
        self.__display_url(url="dashboard?dashboard={}".format(dashboard_name))

    def clear_cache(self, all_organizations: bool = False, partitions: Optional[List[str]] = None):
        """
        Clears scene engine's Redis cache by organization
        Args:
            all_organizations: if True, Redis cache for all organization is cleared. Requires Admin privilege
            partitions: list of partitions (like images, sets, annotations) to clear their cache, if not set, all is cleared

        Returns:
            ACK_OK_RESPONSE on success
        """
        payload = {"partitions": partitions} if partitions else {}
        return self.requests.post("clear_cache", params={"all_organizations": all_organizations}, remove_version=True,
                                  json=payload).json()

    def jira_is_connected(self) -> bool:
        """Check Jira connection
        Returns
        -------
        bool
            is jira connected
        """
        try:
            resp = self.requests.get("jira/is_connected/", trailing_slash=True, remove_version=True)
            if resp.ok:
                return True
            else:
                return False
        except:
            return False

    def jira_create_issue(self,
                          summary: str,
                          jira_project: str,
                          type: str = "Task",
                          description: Optional[str] = None,
                          user_id: Optional[str] = None,
                          link_url: Optional[str] = None,
                          link_title: str = "attachment") -> str:
        """create a Jira issue

        Note
        ----
        This method only works if SceneBox and Jira are connected

        Parameters
        ----------
        summary:
            ticket summary or title
        jira_project:
            project to add the ticket under
        type:
            ticket type Task | Story | Bug
        description:
            ticket description
        user_id:
            optional assignee
        link_url:
            optional link url
        link_title:
            optional title for link

        Returns
        -------
        str
            url of the created Jira ticket

        """

        SUPPORTED_TYPES = ["Task", "Story", "Bug"]
        if type not in SUPPORTED_TYPES:
            raise JiraError(f"type f{type} is not supported. Should be one of {', '.join(SUPPORTED_TYPES)}")
        payload = {"summary": summary,
                   "type": type,
                   "project": jira_project}
        if description:
            payload["description"] = description

        if user_id:
            payload["user_id"] = user_id

        if link_url:
            payload["link_url"] = link_url
            payload["link_title"] = link_title

        resp = self.requests.post("jira/create_issue/", trailing_slash=True, remove_version=True, json=payload)
        return resp.json().get("url")

    def jira_link_new_issue_to_existing(self,
                                        existing_issue_key: str,
                                        summary: str,
                                        jira_project: str,
                                        type: str = "Task",
                                        link_type: str = "relates to",
                                        description: Optional[str] = None,
                                        user_id: Optional[str] = None,
                                        link_url: Optional[str] = None,
                                        link_title: str = "attachment",
                                        link_comment: str = None
                                        ) -> str:
        """create a new Jira issue and link to an existing one

        Note
        ----
        This method only works if SceneBox and Jira are connected

        Parameters
        ----------
        existing_issue_key:
            Key for an existing Jira issue
        summary:
            ticket summary or title
        jira_project:
            project to add the ticket under
        type:
            ticket type Task | Story | Bug
        description:
            ticket description
        user_id:
            optional assignee
        link_url:
            optional link url
        link_title:
            optional title for link
        link_comment:
            optional comment for link

        Returns
        -------
        str
            url of the created Jira ticket

        """

        SUPPORTED_TYPES = ["Task", "Story", "Bug"]
        if type not in SUPPORTED_TYPES:
            raise JiraError(f"type f{type} is not supported. Should be one of {', '.join(SUPPORTED_TYPES)}")

        payload = {"existing_issue_key": existing_issue_key,
                   "summary": summary,
                   "type": type,
                   "link_type": link_type,
                   "project": jira_project}
        if description:
            payload["description"] = description

        if user_id:
            payload["user_id"] = user_id

        if link_url:
            payload["link_url"] = link_url
            payload["link_title"] = link_title

        if link_comment:
            payload["link_comment"] = {"body": link_comment}

        resp = self.requests.post("jira/link_issue/", trailing_slash=True, remove_version=True, json=payload)
        return resp.json().get("url")

    def __check_entity_durations(self, session_uid: str, timestamps: List[Union[str, datetime, None]]):
        """
        check the entity duration and session duration and error if the entire duration is larger than maximum allowed
        """
        session_metadata = self.get_asset_manager(asset_type=AssetsConstants.SESSIONS_ASSET_ID).get_metadata(
            id=session_uid)
        all_timestamps = copy(timestamps)
        all_timestamps.extend([session_metadata.get("start_time"), session_metadata.get("end_time")])
        clean_timestamps = [str_or_datetime_to_datetime(_) for _ in all_timestamps if _ is not None]
        resolution = session_metadata.get("resolution") or DEFAULT_SESSION_RESOLUTION

        max_duration = MAX_SESSION_LENGTH * resolution
        if clean_timestamps:
            duration = (max(clean_timestamps) - min(clean_timestamps)).seconds
            if duration > max_duration:
                raise SessionError(
                    f"Expected length {duration} sec is larger than max {max_duration} sec for session {session_uid}.")


    ##########################
    # Campaign methods
    ##########################
    def save_campaign_operation_config(
            self,
            name: str,
            config: dict,
            operation_id: str,
            description: Optional[str] = None,
            id: Optional[str] = None,) -> str:
        """Create a config for a campaign operation.

        Parameters
        ----------
        name:
            Name of the configuration.
        config:
            Body of the config to create.  Form dependent on the configuration needs.
        description:
            A brief description of the config's purpose, settings, etc.
        id:
            optional unique identifier
        operation_id:
            String. The id of the campaign operation the config if meant for.
        Returns
        -------
        str
            The ID of the created config.

        """
        options = {}
        options.update({
            "name": name,
            "type": ConfigTypes.CAMPAIGN_OPERATION_CONFIG,
            "config": config,
            "description": description,
            "operation_id": operation_id
        })
        if id:
            options.update({"id": id})

        resp = self.requests.post(
            "configs/add/",
            trailing_slash=True,
            json=options)

        if not resp.ok:
            raise ResponseError(
                "Could not create the config: {}".format(
                    resp.content))

        id = resp.json()["id"]
        return id

    def delete_campaign_operation_config(self, config_id: str):
        """Delete a config.

        Parameters
        ----------
        config_id:
            The ID of the config to delete.

        Raises
        ------
        ResponseError:
            If the config could not be deleted.

        """

        resp = self.requests.delete(
            "configs/meta/{}".format(config_id),
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not delete the config_id: {}".format(
                    resp.content))

    def get_campaign_operation_config(self,
                                      config_id: str,
                                      complete_info=False) -> dict:
        """Get config metadata.

        Parameters
        ----------
        config_id:
            The ID of the config to receive the metadata of.
        complete_info:
            If True, returns the the entire metadata of the config
            (with the config parameters contained inside).  Otherwise,
            only returns the config parameters.

        Returns
        -------
        dict
            The metadata and/or parameters of the desired config.

        Raises
        ------
        ResponseError:
            If the config metadata could not be obtained.
        """
        resp = self.requests.get(
            "configs/meta/{}".format(config_id),
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not get the config metadata: {}".format(
                    resp.content))

        if complete_info:
            return resp.json()
        else:
            return resp.json().get("config", {})

    def create_campaign(self,
                        name: str,
                        operations_pipeline: List[TemplateOperation],
                        tags: List[str] = None) -> str:
        """Create a Campaign
        A Campaign is a collection of tasks to run on the raw data or metadata
        on SceneBox. Use this method to create a new campaign with a template pipeline for the campaign.
        A template pipeline is the blueprint of an operations pipeline that every new task added to
        a campaign will follow. A pipeline is made up of TemplateOperation objects that define
        the order of the operations in a task along with their configs.

        Parameters
        ----------
        name:
            A name to associate the campaign with. Needs to be unique for
            an organization.

        tags:
            List of strings. Attach a list of tags to a campaign to search / sort
            for them later.

        operations_pipeline:
            List of TemplateOperation objects. A list defining the order of the operations with
            their respective configs.

        Returns
        ------
        str
            A unique id of the campaign if creation was successful.

        Raises
        ------
        CampaignError
            If the campaign could not be created
        """

        req_payload = {"name": name}

        assert operations_pipeline, "Operations pipeline cannot be empty or None"
        pipeline_dict = []
        for i, template_operation in enumerate(operations_pipeline):
            assert template_operation.task_step == i, "Operation at position {} has task_step {}".format(
                i, template_operation.task_step)
            op_as_dict = asdict(template_operation)
            if not op_as_dict["config"]:
                del op_as_dict["config"]
            pipeline_dict.append(op_as_dict)

        req_payload["operations_pipeline"] = pipeline_dict

        if tags:
            req_payload["tags"] = tags

        resp = self.requests.post(
            "campaigns/create/",
            json=req_payload,
            trailing_slash=False)

        if not resp.ok:
            raise CampaignError("Could not create campaign {}. Error: {}".format(
                name, resp.content))

        return resp.json()["campaign_id"]

    def _get_campaign(self,
                      campaign_id: str) -> dict:
        """Get a campaign from the table
        Parameters
        ----------
        campaign_id:
            ID of the campaign to get

        Returns
        ------
        dict
            Campaign details as a dictionary. A ResponseError if the campaign
            could not be found.
        """

        resp = self.requests.get(
            "campaigns/{}/".format(campaign_id),
            trailing_slash=False)

        if not resp.ok:
            raise CampaignError("Could not get campaign: {}".format(resp.content))

        return resp.json()

    def delete_campaign(self,
                        campaign_id: str) -> str:
        """Delete a campaign
        Deleting a campaign will delete all tasks and by extension all operation
        runs contained in it.

        Parameters
        ----------
        campaign_id:
            ID of the campaign to delete

        Returns
        ------
         ResponseError
                If the campaign could not be found or could not be deleted.
        """
        resp = self.requests.delete(
            "campaigns/{}/".format(campaign_id),
            trailing_slash=False)

        if not resp.ok:
            raise CampaignError("Could not delete campaign: {}".format(resp.content))

        return resp.json()

    def search_campaigns(self,
                         filters: List[dict] = None,
                         return_fields: List[str] = None,
                         sort_field: str = None,
                         sort_order: str = None) -> List[dict]:
        """Search for campaigns that satisfy the filtering criteria

        Parameters
        ----------
        filters:
            A list of key-value dictionaries to impose a criteria on available campaigns.

        return_fields:
            List of strings. The fields to return from the available campaign metadata fields.

        sort_field:
            String. The field to sort the return record with. Must be a valid field in the
            campaigns metadata. By default, results are sorted by their timestamps.

        sort_order:
            String. One of ["asc", "desc"] to indicate the order in which to return
            the results. By default, results are sorted in the descending order.

        Returns
        ------
        List[dict]
            A list of campaign details as a dictionary. A ResponseError if the task
            could not be found.
        """
        req_payload = {}
        params = {}

        if filters:
            req_payload["filters"] = filters

        if return_fields:
            req_payload["return_fields"] = return_fields

        if sort_field:
            params["sort_field"] = sort_field

        if sort_order:
            assert sort_order in ["asc", "desc"]
            params["sort_order"] = sort_order

        resp = self.requests.post(
            "campaigns/search/",
            json=req_payload,
            params=params,
            trailing_slash=False)

        if not resp.ok:
            raise CampaignError("Could not search campaigns. Error: {}".format(resp.content))

        return resp.json()

    def update_campaign_pipeline(self,
                                 campaign_id: str,
                                 new_operations_pipeline: List[TemplateOperation]) -> dict:
        """Update a campaign's task pipeline
        Use this method to update a campaign's task pipeline. Specifically, this methods allows the
        update of any configs for the operations already contained in the pipline. Or, new operations
        can be added to extend the pipeline further. Existing operations cannot be removed or reordered.
        For these changes, please look into creating new campaigns.

        Parameters
        ----------
        campaign_id:
            ID of the campaign to update

        new_operations_pipeline:
            List of TemplateOperation objects to update the campaign with. A list defining the
            entire order of the operations with their respective configs. Should contain the entire
            chain even if not being updated.

        Raises
        ------
        CampaignError
            If the update was unsuccessful
        """

        req_payload = {}

        assert new_operations_pipeline, "New Operations pipeline cannot be empty or None"
        pipeline_dict = []
        for i, template_operation in enumerate(new_operations_pipeline):
            assert template_operation.task_step == i, "Operation at position {} has task_step {}".format(
                i, template_operation.task_step)
            op_as_dict = asdict(template_operation)
            if not op_as_dict["config"]:
                del op_as_dict["config"]
            pipeline_dict.append(op_as_dict)

        req_payload["new_operations_pipeline"] = pipeline_dict

        resp = self.requests.post(
            "campaigns/{}/".format(campaign_id),
            json=req_payload,
            trailing_slash=False)

        if not resp.ok:
            raise CampaignError("Could not update pipeline for campaign {}. Error: {}".format(
                campaign_id, resp.content))

        return resp.json()

    def add_task_to_campaign(self,
                             campaign_id: str,
                             input_payload: dict = None) -> [str, List[str]]:

        """Add new tasks to a campaign.
        Each new task will follow the blueprint pipeline of the operations and their configs defined
        as the campaign's template task.

        Parameters
        ----------
        campaign_id:
            String. ID of the campaign to define the template for.

        input_payload:
            Dictionary. Each dictionary key should conform to the input schema outlined for
            the first operation in the pipeline.

        Returns
        ------
        str
            ID of the task created

        Raises
        ------
        CampaignError
            If the task could not be created successfully.
        """

        req_payload = {"input_payload": input_payload}

        resp = self.requests.post(
            "campaigns/tasks/add/{}/".format(campaign_id),
            json=req_payload,
            trailing_slash=False)

        if not resp.ok:
            raise CampaignError("Could not add a task for campaign {}. Error: {}".format(
                campaign_id, resp.content))

        return resp.json()["task_id"], resp.json()["operation_instance_ids"]

    def _get_task(self,
                  task_id: str) -> dict:
        """Get a task from the table
        Parameters
        ----------
        task_id:
            ID of the task to get.

        Returns
        ------
        dict
            Task details as a dictionary. A ResponseError if the task
            could not be found.
        """

        resp = self.requests.get(
            "campaigns/tasks/{}/".format(task_id),
            trailing_slash=False)

        if not resp.ok:
            raise CampaignError("Could not get task {}. Error: {}".format(task_id, resp.content))

        return resp.json()

    def get_task_rundown(self,
                  task_id: str) -> dict:
        """Get a task run history including details such as config, input, output and phase payloads.
        Parameters
        ----------
        task_id:
            ID of the task to get.

        Returns
        ------
        dict
            Task details as list of dictionaries. A ResponseError if the task
            could not be found.
        """

        resp = self.requests.get(
            "campaigns/tasks/rundown/{}/".format(task_id),
            trailing_slash=False)

        if not resp.ok:
            raise CampaignError("Could not get task rundown {}. Error: {}".format(task_id, resp.content))

        return resp.json()

    def search_tasks(self,
                     filters: List[dict] = None,
                     return_fields: List[str] = None,
                     sort_field: str = None,
                     sort_order: str = None,
                     include_template_tasks: bool = False) -> List[dict]:
        """Search for tasks that satify the filtering criteria

        Parameters
        ----------
        filters:
            A list of key-value dictionaries to impose a criteria on available tasks.

        return_fields:
            List of strings. The fields to return from available task metadata fields.

        sort_field:
            String. The field to sort the return record with. Must be a valid field in the
            tasks metadata. By default, results are sorted by their timestamps.

        sort_order:
            String. One of ["asc", "desc"] to indicate the order in which to return
            the results. By default, results are sorted in the descending order.

        include_template_tasks:
            Boolean. Flag to indicate whether to search over template tasks set for a campaign.

        Returns
        ------
        List[dict]
            A list of task details as a dictionary. A ResponseError if the task
            could not be found.

        """
        req_payload = {}
        params = {}
        req_payload["include_template_tasks"] = include_template_tasks
        if filters:
            req_payload["filters"] = filters

        if return_fields:
            req_payload["return_fields"] = return_fields

        if sort_field:
            params["sort_field"] = sort_field

        if sort_order:
            params["sort_order"] = sort_order

        resp = self.requests.post(
            "campaigns/tasks/search/",
            json=req_payload,
            params=params,
            trailing_slash=False)

        if not resp.ok:
            raise CampaignError("Could not search tasks. Error: {}".format(resp.content))

        return resp.json()

    def delete_task(self,
                    task_id: str) -> str:
        """Delete a task
        Deleting a task will delete operation instances associated with it.

        Parameters
        ----------
        task_id:
            ID of the task to delete

        Returns
        ------
         ResponseError
                If the task could not be found or could not be deleted.
        """
        resp = self.requests.delete(
            "campaigns/tasks/{}/".format(task_id),
            trailing_slash=False)

        if not resp.ok:
            raise CampaignError("Could not delete task {}. Error: {}".format(task_id, resp.content))

        return resp.json()

    def list_operations(
            self,
            return_fields: List[str] = None
    ) -> dict:

        """Get specifications of an operation

            This method can be used to get about the definition and specification of an operation
            listed in the OpsStore.

            Parameters
            ----------
            return_fields:
                List of strings. The fields to return from the operation spec.

            Raises
            ------
            ResponseError
                If the operation could not be found.

            """
        url = self.requests._SceneEngineRequestHandler__get_scene_engine_url(
            route="operations/list/",
            trailing_slash=True, remove_version=False)
        # Update version to v2 for operations
        url = url.replace("v1", "v2")

        req_payload = {}
        if return_fields:
            req_payload["return_fields"] = return_fields

        params = {}
        if self.auth_token:
            params["token"] = self.auth_token
        resp = requests.post(url, params=params, json=req_payload)

        if not resp.ok:
            raise OperationError("Could not list operations. Error: {}".format(resp.content))

        return resp.json()

    def get_operation(
            self,
            operation_id: str
    ) -> dict:

        """Get specifications of an operation

            This method can be used to get about the definition and specification of an operation
            listed in the OpsStore.

            Parameters
            ----------
            operation_id:
                String. A unique string identifier for the operation.

            Raises
            ------
            ResponseError
                If the operation could not be found.

            """
        url = self.requests._SceneEngineRequestHandler__get_scene_engine_url(
            route="operations/{}/".format(operation_id),
            trailing_slash=True, remove_version=False)
        # Update version to v2 for operations
        url = url.replace("v1", "v2")

        params = {}
        if self.auth_token:
            params["token"] = self.auth_token
        resp = requests.get(url, params=params)

        if not resp.ok:
            raise OperationError("Could not find operation {}. Error: {}".format(operation_id, resp.content))

        return resp.json()

    def run_operation_instance(self,
                               operation_instance_id: str,
                               phase: Optional[str] = None,
                               phase_payload: Optional[dict] = None,
                               wait_for_completion: bool = False) -> str:

        """Run an individual instance of an operation contained in a task.
        An operation instance is a self-contained work unit of a task. Running a task will consume the
        input defined in its input payload according to its pre-defined config.

        Parameters
        ----------
        operation_instance_id:
            String. ID of the campaign to define the template for.

        phase:
            Optional string. An operation can have different run-time behaviours based on its phase.
            Refer to the operations Phase and Phase Payload Schema for details.

        phase_payload:
            Optional dictionary. A parameter key-value dictionary to provide phase-level configuration to
            the operation. Will be validated against the phase_payload_schema defined in the operation.

        wait_for_completion:
            If True, polls until job is complete. Otherwise, continues execution and returns job_id

        Returns
        ------
        str
            ID of the job running the operation.

        Raises
        ------
        OperationError
            If the operation could not be run successfully.
        """

        assert operation_instance_id, "Operation instance id required"

        req_payload = {}
        if phase:
            req_payload["phase"] = phase
            assert phase_payload, "Phase payload cannot be None"
            req_payload["phase_payload"] = phase_payload

        resp = self.requests.post(
            "campaigns/tasks/run_operation/{}/".format(operation_instance_id),
            json=req_payload,
            trailing_slash=False)

        if not resp.ok:
            raise OperationError("Could not run operation instance {}. Error: {}".format(
                operation_instance_id, resp.content))

        job_id = resp.json()["job_id"]
        if wait_for_completion:
            self._wait_for_job_completion(job_id)

        return job_id

    def _get_operation_instance(
            self,
            operation_instance_id: str) -> dict:

        """Retrieve an operation instance's metadata.

            An operation instance is a single working unit of a task. Use this method to retreive its
            metadata.

            Parameters
            ----------
            operation_instance_id:
                string id of the operation instance

            Returns
            -------
            dict
                Metadata dictionary for the given operation instance.s

            Raises
            ------
            ResponseError
                If the operation could not be found.

            """
        url = self.requests._SceneEngineRequestHandler__get_scene_engine_url(
            route="operations/instances/{}/".format(operation_instance_id),
            trailing_slash=True, remove_version=False)
        # Update version to v2 for operations
        url = url.replace("v1", "v2")

        params = {}
        if self.auth_token:
            params["token"] = self.auth_token
        resp = requests.get(url, params=params)

        if not resp.ok:
            raise OperationError("Could not get instance metadata: {}".format(resp.content))

        return resp.json()

    def _update_operation_instance(
            self,
            operation_instance_id: str,
            input_payload: dict = None,
            output_payload: dict = None,
            phase: str = None,
            phase_payload: dict = None,
            state_dict: dict = None,
    ) -> dict:

        """Update an operation instance's metadata.

            An operation instance is a single working unit of a task. Use this method to update an
            instance with its runtime outputs such as output_payload and logs.

            Parameters
            ----------
            operation_instance_id:
                string id of the operation instance

            input_payload:
                dict. Payload dictionary conforming to the schema defined in the operation class. Used
                to update the operation chain with input information from the previous step.

            output_payload:
                dict. Payload dictionary conforming to the schema defined in the operation class.

            phase:
                str. Update the phase information on the instance

            phase_payload:
                dict. Payload dictionary conforming to the phase payload schema for the current phase.

            state_dict:
                dict. A key-value dictionary to save current state of the operation and resume from later.

            Raises
            ------
            ResponseError
                If the operation could not be found.

            """
        url = self.requests._SceneEngineRequestHandler__get_scene_engine_url(
            route="operations/instances/{}/".format(operation_instance_id),
            trailing_slash=True, remove_version=False)
        # Update version to v2 for operations
        url = url.replace("v1", "v2")

        req_payload = {}
        if input_payload:
            req_payload["input_payload"] = input_payload

        if output_payload:
            req_payload["output_payload"] = output_payload

        if phase:
            assert phase_payload
            req_payload["phase"] = phase
            req_payload["phase_payload"] = phase_payload

        if state_dict:
            req_payload["state_dict"] = state_dict

        params = {}
        if self.auth_token:
            params["token"] = self.auth_token
        resp = requests.post(url, params=params, json=req_payload)

        if not resp.ok:
            raise OperationError("Could not update instance metadata: {}".format(resp.content))

        return resp.json()

    def _update_task_status(
            self,
            task_id: str,
            status: str = None,
    ) -> dict:

        """Update a task's status.

            A task is a collection of one or many operations. A tasks itself is contained in a campaign.
            This method manually updates the status of a task.

            Parameters
            ----------
            task_id:
                string id of the task

            status:
                string. One of the five allowed task statuses.
                ["initialized", "running", "finished", "waiting", "aborted"]

            Raises
            ------
            ResponseError
                If the task could not be found or updated.

            """
        if status:
            params = {"status": status}
        else:
            params = None

        resp = self.requests.put(
            "campaigns/tasks/{}/".format(task_id),
            params=params,
            trailing_slash=False)

        if not resp.ok:
            raise ResponseError("Could not update task status: {}".format(resp.content))

        return resp.json()

    def _update_campaign_activeness(
            self,
            campaign_id: str,
            active: bool,
    ):

        """Archive / Activate a campaign.

            Move a campaign to an archive. Or activate the archived campaigns.

            Parameters
            ----------
            campaign_id:
                string id of the campaign

            active:
                Boolean. Set True to activate a campaign, False to archive it.

            Raises
            ------
            ResponseError
                If the campaign could not be found or updated.

            """

        params = {"active": active}
        resp = self.requests.put(
            "campaigns/{}/".format(campaign_id),
            params=params,
            trailing_slash=False)

        if not resp.ok:
            raise ResponseError("Could not update campaign activeness: {}".format(resp.content))

        return resp.json()

    def add_comment_to_assets(
            self,
            asset_type: str,
            ids: List[str],
            comment: str) -> dict:
        """Add a comment to a list of assets.

        Parameters
        ----------
        asset_type:
            Asset type to add a comment to.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        ids:
            The IDs of the assets to add the comment to.
        comment:
            The comment to be added.
        """

        asset_comment = {"ids": ids, "comment": comment}

        resp = self.requests.post("{}/comments".format(asset_type),
                                  json=asset_comment,
                                  trailing_slash=True)
        if not resp.ok:
            raise AssetError(
                'Could not add the comment to the identifier ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def delete_comment_from_assets(
            self,
            asset_type: str,
            ids: List[str],
            comment: str) -> dict:
        """Delete a comment from a list of assets.

        Parameters
        ----------
        asset_type:
            Asset type to delete a comment from.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        ids:
            The IDs of the assets to add the comment to.
        comment:
            The comment to be deleted.
        """

        asset_comment = {"ids": ids, "comment": comment}

        resp = self.requests.post("{}/delete_comments".format(asset_type),
                                  json=asset_comment)
        if not resp.ok:
            raise AssetError(
                'Could not delete the comment from the identifier ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def get_comments(
            self,
            asset_type: str,
            ids: List[str]) -> dict:
        """Get (common) comments from a list of assets.

        Parameters
        ----------
        asset_type:
            Asset type to collect common comments from.
            To ensure using a valid asset_type, you can import AssetsConstants from scenebox.constants
        ids:
            The IDs of the assets.
        """

        asset_get_comment = {"ids": ids}

        resp = self.requests.post("{}/get_comments".format(asset_type),
                                  json=asset_get_comment)
        if not resp.ok:
            raise AssetError(
                'Could not get comments from the identifier ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

class SceneEngineRequestHandler:
    """Helper for making authenticated requests to the scene engine."""

    def __init__(
            self,
            scene_engine_url,
            auth_token=None):
        self.scene_engine_url = scene_engine_url
        self.auth_token = auth_token

    def with_auth(self,
                  auth_token: Optional[str] = None,
                  ):
        if auth_token:
            self.auth_token = auth_token

        return self

    def get(self,
            route,
            trailing_slash=False,
            params=None,
            headers=None,
            remove_version=False):
        return self.__make_scene_engine_request(
            method="get",
            route=route,
            trailing_slash=trailing_slash,
            params=params,
            headers=headers,
            remove_version=remove_version)

    def post(
            self,
            route,
            trailing_slash=False,
            params=None,
            json=None,
            headers=None,
            remove_version=False):
        return self.__make_scene_engine_request(
            method="post",
            route=route,
            trailing_slash=trailing_slash,
            params=params,
            json=json,
            headers=headers,
            remove_version=remove_version)

    def put(
            self,
            route,
            trailing_slash=False,
            params=None,
            json=None,
            headers=None,
            remove_version=False):
        return self.__make_scene_engine_request(
            method="put",
            route=route,
            trailing_slash=trailing_slash,
            params=params,
            json=json,
            headers=headers,
            remove_version=remove_version)

    def delete(
            self,
            route,
            trailing_slash=False,
            params=None,
            json=None,
            headers=None,
            remove_version=False):
        return self.__make_scene_engine_request(
            method="delete",
            route=route,
            trailing_slash=trailing_slash,
            params=params,
            json=json,
            headers=headers,
            remove_version=remove_version)

    def __make_scene_engine_request(
            self,
            method: str,
            route: str = "",
            trailing_slash: bool = False,
            params: Optional[dict] = None,
            json: Optional[dict] = None,
            headers: Optional[dict] = None,
            remove_version: bool = False):
        assert method in {"get", "post", "put", "delete"}
        url = self.__get_scene_engine_url(
            route, trailing_slash, remove_version)
        request_ = getattr(requests, method)
        if self.auth_token:
            if not params:
                params = {}
            params["token"] = self.auth_token
        resp = request_(
            url,
            params=params,
            json=json,
            headers=headers)
        if not resp.ok:
            raise ResponseError(
                "{} ::: {} with token::: {}".format(
                    resp.reason, resp.content, self.auth_token))
        return resp

    def __get_scene_engine_url(self, route, trailing_slash, remove_version):

        if remove_version:
            scene_engine_url_ = re.sub(
                "{}".format(VERSION_POSTFIX), "", self.scene_engine_url)
        else:
            scene_engine_url_ = self.scene_engine_url

        url = join(scene_engine_url_, route)
        if trailing_slash and not url.endswith("/"):
            url += "/"
        if not trailing_slash and url.endswith("/"):
            url = url[:-1]
        return url
