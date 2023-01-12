import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Tuple, Any, Union, Dict, Callable
from uuid import UUID

import requests
from box import Box
from dataclasses_json import dataclass_json, LetterCase
from requests import HTTPError, ReadTimeout

from pycarlo.features.pii import PiiService, PiiFilterer
from pycarlo.common import get_logger, http
from pycarlo.common.files import BytesFileReader, JsonFileReader, to_path
from pycarlo.common.utils import chunks
from pycarlo.core import Client
from pycarlo.features.dbt.queries import (
    GET_DBT_UPLOAD_URL,
    IMPORT_DBT_MANIFEST,
    IMPORT_DBT_RUN_RESULTS,
    SEND_DBT_ARTIFACTS_EVENT,
    UPLOAD_DBT_MANIFEST,
    UPLOAD_DBT_RUN_RESULTS,
)
from pycarlo.features.user import UserService

logger = get_logger(__name__)


class InvalidArtifactsException(Exception):
    pass


class InvalidFileFormatException(Exception):
    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DbtArtifacts:
    manifest: str
    run_results: str
    logs: Optional[str]


class DbtImporter:
    """
    Import dbt run artifacts to Monte Carlo
    """
    DEFAULT_PROJECT_NAME = 'default-project'
    DEFAULT_JOB_NAME = 'default-job'

    def __init__(self,
                 mc_client: Optional[Client] = None,
                 user_service: Optional[UserService] = None,
                 pii_service: Optional[PiiService] = None,
                 print_func: Optional[Callable] = logger.info):
        self._mc_client = mc_client or Client()
        self._user_service = user_service or UserService(mc_client=self._mc_client)
        self._pii_service = pii_service or PiiService(mc_client=self._mc_client)
        self._print_func = print_func
        self._pii_filterer = self._init_pii_filterer()

    def import_run(self,
                   manifest_path: Union[Path, str],
                   run_results_path: Union[Path, str],
                   logs_path: Optional[Union[Path, str]] = None,
                   project_name: str = DEFAULT_PROJECT_NAME,
                   job_name: str = DEFAULT_JOB_NAME,
                   resource_id: Optional[Union[str, UUID]] = None):
        """
        Import artifacts from a single dbt command execution.

        :param manifest_path: local path to the dbt manifest file (manifest.json)
        :param run_results_path: local path to the dbt run results file (run_results.json)
        :param logs_path: local path to a file containing dbt run logs
        :param project_name: Project name (perhaps a logical group of dbt models, analogous to a project in dbt Cloud)
        :param job_name: Job name (perhaps a logical sequence of dbt commands, analogous to a job in dbt Cloud)
        :param resource_id: identifier of a Monte Carlo resource (warehouse or lake) to use to resolve dbt models to
                            tables, this will be required if you have more than one
        """
        # get resource
        resource = self._user_service.get_resource(resource_id)

        # read local artifacts
        manifest = JsonFileReader(manifest_path).read()
        run_results = JsonFileReader(run_results_path).read()
        logs = BytesFileReader(logs_path).read() if logs_path else None

        # extract dbt invocation id (and verify it is the same for each artifact)
        invocation_id = self._get_invocation_id(
            manifest_path=manifest_path,
            manifest=manifest,
            run_results_path=run_results_path,
            run_results=run_results
        )

        # upload artifacts to S3 (using pre-signed URLs)
        artifacts = DbtArtifacts(
            manifest=self._upload_artifact(
                project_name=project_name,
                invocation_id=invocation_id,
                file_path=to_path(manifest_path),
                content=manifest
            ),
            run_results=self._upload_artifact(
                project_name=project_name,
                invocation_id=invocation_id,
                file_path=to_path(run_results_path),
                content=run_results
            ),
            logs=self._upload_artifact(
                project_name=project_name,
                invocation_id=invocation_id,
                file_path=to_path(logs_path),
                content=logs
            ) if logs else None
        )

        # publish event indicating run artifacts are ready for processing
        self._mc_client(
            query=SEND_DBT_ARTIFACTS_EVENT,
            variables=dict(
                projectName=project_name,
                jobName=job_name,
                invocationId=invocation_id,
                artifacts=artifacts.to_dict(),
                resourceId=str(resource.id)
            )
        )

        self._print_func('Finished sending run artifacts to Monte Carlo')

    def _get_invocation_id(self,
                           manifest_path: Union[Path, str],
                           manifest: Dict,
                           run_results_path: Union[Path, str],
                           run_results: Dict) -> str:

        manifest_invocation_id = self._extract_invocation_id(path=manifest_path, data=manifest)
        run_results_invocation_id = self._extract_invocation_id(path=run_results_path, data=run_results)

        if manifest_invocation_id != run_results_invocation_id:
            raise InvalidArtifactsException('dbt invocation ids do not match between manifest and run results files')

        return manifest_invocation_id

    @staticmethod
    def _extract_invocation_id(path: Union[Path, str],
                               data: Dict) -> str:
        try:
            return data['metadata']['invocation_id']
        except KeyError:
            raise InvalidArtifactsException(f"Unable to get dbt invocation id from '{path}'. Unexpected file format")

    def _upload_artifact(self,
                         project_name: str,
                         invocation_id: str,
                         file_path: Path,
                         content: Union[bytes, str, Dict]) -> str:

        self._print_func(f'Uploading {file_path.name}...')
        http.upload(
            method='put',
            url=self._get_presigned_url(
                project_name=project_name,
                invocation_id=invocation_id,
                file_name=file_path.name
            ),
            content=self._pii_filterer.filter_content(content)
        )
        return file_path.name

    def _get_presigned_url(self,
                           project_name: str,
                           invocation_id: str,
                           file_name: str) -> str:

        response = self._mc_client(
            query=GET_DBT_UPLOAD_URL,
            variables=dict(
                projectName=project_name,
                invocationId=invocation_id,
                fileName=file_name
            )
        )

        return response.get_dbt_upload_url

    def import_dbt_manifest(self,
                            dbt_manifest: Union[str, Dict],
                            project_name: Optional[str] = None,
                            batch_size: int = 10,
                            default_resource: Optional[str] = None) -> List[str]:
        """
        Import a dbt manifest

        DEPRECATED: this API will be removed in a future release. Please use `import_run` instead.

        :param dbt_manifest: either str indicating filename, or dict conforming to dbt manifest schema
        :param project_name: project_name to associate with manifest
        :param batch_size: import in batches of `batch_size` manifest elements
        :param default_resource: if account has multiple warehouses, define default_resource to choose
                                 the warehouse to associate with this dbt manifest. Can be either the
                                 warehouse's name or UUID

        :return: List of dbt node ID's that were successfully imported
        """
        dbt_schema_version, _, nodes = self._load_dbt_manifest(dbt_manifest)
        self._print_func(f"\nImporting {len(nodes)} DBT objects into Monte Carlo catalog. Please wait...")

        node_ids_imported = []
        all_bad_responses = []
        for nodes_batch in chunks(nodes, batch_size):
            node_ids, bad_responses = self._do_make_import_request(
                dbt_schema_version,
                nodes_batch,
                project_name,
                default_resource)

            if len(node_ids) > 0:
                node_ids_imported.extend(node_ids)
                self._print_func(f"Imported {len(node_ids_imported)} objects")

            all_bad_responses.extend(bad_responses)

        if all_bad_responses:
            self._print_func("\nEncountered invalid responses.", all_bad_responses)

        return node_ids_imported

    @staticmethod
    def _load_dbt_manifest(dbt_manifest: Union[str, Dict]) -> Tuple[str, str, List]:
        if isinstance(dbt_manifest, str):
            with open(dbt_manifest, 'r') as f:
                manifest = Box(json.load(f))
        else:
            manifest = Box(dbt_manifest)

        try:
            return manifest.metadata.dbt_schema_version, manifest.metadata.invocation_id, list(manifest.nodes.items())
        except KeyError:
            raise InvalidFileFormatException("Unexpected format of input file. Ensure that input file is a valid DBT manifest.json file")

    def _do_make_import_request(self,
                                dbt_schema_version: str,
                                nodes: List,
                                project_name: Optional[str],
                                default_resource: Optional[str] = None) -> Tuple[List[str], List[Any]]:
        try:
            response = self._mc_client(
                query=IMPORT_DBT_MANIFEST,
                variables=dict(
                    dbtSchemaVersion=dbt_schema_version,
                    manifestNodesJson=json.dumps(dict(nodes)),
                    projectName=project_name,
                    defaultResource=default_resource
                )
            )

            try:
                return response.import_dbt_manifest.response.node_ids_imported, []
            except KeyError:
                return [], [response]

        except (HTTPError, ReadTimeout) as e:
            if isinstance(e, ReadTimeout) or \
                    (isinstance(e, HTTPError) and e.response.status_code == requests.codes.gateway_timeout):
                self._print_func(f"Import timed out with {e}, trying again with smaller batches.")

                if len(nodes) == 1:
                    raise RuntimeError("Could not split batch any further, exiting!")

                # Possible for the request to time out if there is too much data
                # Just send each one-by-one
                all_node_ids, all_bad_requests = [], []
                for single_node_batch in chunks(nodes, 1):
                    node_ids, bad_requests = self._do_make_import_request(dbt_schema_version, single_node_batch, project_name)
                    all_node_ids.extend(node_ids)
                    all_bad_requests.extend(all_bad_requests)

                return all_node_ids, all_bad_requests
            else:
                raise

    def upload_dbt_manifest(self,
                            dbt_manifest: Union[str, Dict],
                            project_name: Optional[str] = None,
                            batch_size: int = 10,
                            default_resource: Optional[str] = None):
        """
        Upload a dbt manifest

        DEPRECATED: this API will be removed in a future release. Please use `import_run` instead.

        This is an asynchronous alternative to `import_dbt_manifest`.

        :param dbt_manifest: either str indicating filename, or dict conforming to dbt manifest schema
        :param project_name: project_name to associate with manifest
        :param batch_size: import in batches of `batch_size` manifest elements
        :param default_resource: if account has multiple warehouses, define default_resource to choose
                                 the warehouse to associate with this dbt manifest. Can be either the
                                 warehouse's name or UUID
        """
        dbt_schema_version, invocation_id, nodes = self._load_dbt_manifest(dbt_manifest)
        self._print_func(f'Uploading {len(nodes)} DBT objects to Monte Carlo for processing. Please wait...')

        total_uploaded = 0
        for batch_index, nodes_batch in enumerate(chunks(nodes, batch_size)):
            self._do_make_upload_request(
                invocation_id,
                batch_index + 1,
                dbt_schema_version,
                nodes_batch,
                project_name,
                default_resource)

            total_uploaded += len(nodes_batch)
            self._print_func(f'Uploaded {total_uploaded} objects')

    def _do_make_upload_request(self,
                                invocation_id: str,
                                batch: int,
                                dbt_schema_version: str,
                                nodes: List,
                                project_name: Optional[str],
                                default_resource: Optional[str] = None):
        self._mc_client(
            query=UPLOAD_DBT_MANIFEST,
            variables=dict(
                invocationId=invocation_id,
                batch=batch,
                dbtSchemaVersion=dbt_schema_version,
                manifestNodesJson=json.dumps(dict(nodes)),
                projectName=project_name,
                defaultResource=default_resource
            )
        )

    @staticmethod
    def _load_dbt_run_results(dbt_run_results: Union[str, Dict]) -> Tuple[str, str, int, Dict]:
        if isinstance(dbt_run_results, str):
            with open(dbt_run_results, 'r') as f:
                dbt_run_results = Box(json.load(f))
        else:
            dbt_run_results = Box(dbt_run_results)

        try:
            return dbt_run_results.metadata.dbt_schema_version, dbt_run_results.metadata.invocation_id,\
                   len(dbt_run_results.results), dbt_run_results
        except KeyError:
            raise InvalidFileFormatException("Unexpected format of input file. "
                                             "Ensure that input file is a valid DBT run_results.json file")

    def import_run_results(self,
                           dbt_run_results: Union[str, Dict],
                           project_name: Optional[str] = None,
                           run_id: Optional[str] = None,
                           run_logs: Optional[str] = None) -> int:
        """
        Import dbt run results

        DEPRECATED: this API will be removed in a future release. Please use `import_run` instead.

        :param dbt_run_results: either str indicating filename, or dict conforming to dbt run results
        :param project_name: project_name to associate with run results (Optional)
        :param run_id: run_id to associate with run results (Optional)
        :param run_logs: dbt run log output to store with run (Optional)

        :return: number of run results imported
        """
        dbt_schema_version, _, _, run_results = self._load_dbt_run_results(dbt_run_results)
        response = self._mc_client(
            query=IMPORT_DBT_RUN_RESULTS,
            variables=dict(
                dbtSchemaVersion=dbt_schema_version,
                runResultsJson=json.dumps(self._pii_filterer.filter_message(run_results)),
                projectName=project_name,
                runId=run_id,
                runLogs=self._pii_filterer.filter_str(run_logs) if run_logs else None
            )
        )

        try:
            num_results_imported = response.import_dbt_run_results.response.num_results_imported
        except KeyError:
            num_results_imported = 0

        self._print_func(f"\nImported a total of {num_results_imported} DBT run results into Monte Carlo\n")

        return num_results_imported

    def upload_run_results(self,
                           dbt_run_results: Union[str, Dict],
                           project_name: Optional[str] = None,
                           run_id: Optional[str] = None,
                           run_logs: Optional[str] = None):
        """
        Upload dbt run results

        DEPRECATED: this API will be removed in a future release. Please use `import_run` instead.

        This is an asynchronous alternative to `import_run_results`.

        :param dbt_run_results: either str indicating filename, or dict conforming to dbt run results
        :param project_name: project_name to associate with run results (Optional)
        :param run_id: run_id to associate with run results (Optional)
        :param run_logs: dbt run log output to store with run (Optional)
        """
        dbt_schema_version, invocation_id, num_results, run_results = self._load_dbt_run_results(dbt_run_results)
        self._print_func('Uploading DBT run results to Monte Carlo for processing. Please wait...')
        self._mc_client(
            query=UPLOAD_DBT_RUN_RESULTS,
            variables=dict(
                dbtSchemaVersion=dbt_schema_version,
                runResultsJson=json.dumps(self._pii_filterer.filter_message(dict(run_results))),
                invocationId=invocation_id,
                projectName=project_name,
                runId=run_id,
                runLogs=run_logs,
            )
        )
        self._print_func(f'\nUploaded a total of {num_results} DBT run results to Monte Carlo for processing\n')

    def _init_pii_filterer(self):
        pii_filters = self._pii_service.get_pii_filters_config()
        return PiiFilterer(filters_config=pii_filters)
