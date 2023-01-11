import os
from pathlib import Path
import sys

import flask
from sumtypes import match
import yaml

from truera.authn.usercontext import RequestContextHelper
from truera.client.errors import AuthorizationDenied
import truera.client.private.metarepo as mr
from truera.client.private.rbac import ProjectAuth
from truera.protobuf.public import metadata_message_types_pb2 as md_proto
from truera.rnn.general.service.container import Locator
from truera.rnn.general.service.sync_service import SyncService
from truera.rnn.general.utils import log
from truera.utils import config_util


class MetarepoSyncService(SyncService):
    '''
    Interface to communicate with the local repo and metarepo where appropriate.
    '''

    def __init__(self, config):
        super(MetarepoSyncService,
              self).__init__(config, needs_local_proxy_cache=False)
        ailens_home_value = os.environ.get("AILENS_HOME", None)
        config_dir = os.path.join(ailens_home_value, "config")
        client_config_file = os.path.join(config_dir, "clients.yaml")
        auth_config_file = os.path.join(config_dir, "auth_config.yaml")
        with open(client_config_file) as fp:
            self.clients_config = yaml.safe_load(fp)
        with open(auth_config_file) as fp:
            auth_config = yaml.safe_load(fp)
        metarepo_url = config_util.get_config_value(
            self.clients_config, "metarepo", "url"
        )

        # TODO: Update all endpoints to V2
        self.metarepo_client = mr.MetaRepo(metarepo_url, "v1")

        self.request_ctx_helper = MetarepoSyncService.setup_request_ctx_helper(
            auth_config
        )
        log.info('Started metarepo client')

    @staticmethod
    def setup_request_ctx_helper(config) -> RequestContextHelper:
        return RequestContextHelper(
            config_util.get_config_value(config, "auth_modes", None)
        )

    def check_permission(self, project_id):
        req_ctx = self.fetch_request_ctx()
        (
            ProjectAuth().set_rbac(
                self.clients_config
            ).set_request_context(req_ctx).set_project_id(project_id
                                                         ).check_analyzable()
        )

    def fetch_request_ctx(self):
        context = flask.request.headers
        request_ctx = self.request_ctx_helper.create_request_context_http(
            context
        )

        return request_ctx

    def _listdir(self, fp):
        '''
        Lists files in a given directory, ignoring hidden files. 
        '''
        return [f for f in os.listdir(fp) if not f.startswith('.')]

    def push(self, locator: Locator):
        '''
        Pushes the items specified by the locator from the local cache to the backing storage
        Since the backing storage is the same as the cache, this is a no-op
        '''
        return

    def pull(self, locator: Locator):
        '''
        Pulls the items specified by the locator from the backing storage to the local cache
        Since the backing storage is the same as the cache, this is a no-op
        '''
        return

    def list_projects(self, context=None):
        '''
        returns project folders, ignoring hidden directories
        '''
        request_ctx = self.fetch_request_ctx()

        time_series_projects = [
            project['name']
            for project in self.metarepo_client.
            get_entities(entity="project", request_ctx=request_ctx)
            if project["input_data_format"] ==
            md_proto.InputDataFormat.TIME_SERIES_TABULAR
        ]
        auth_projects = []

        for project in time_series_projects:
            project_id = self._get_project_id(project, request_ctx)
            try:
                self.check_permission(project_id)
                auth_projects.append(project)
            except AuthorizationDenied:
                continue
        return auth_projects

    def list_artifacts(self, project):
        '''
        returns each artifact as a list of [data_collection, split, model]
        '''
        request_ctx = self.fetch_request_ctx()
        project_id = self._get_project_id(project, request_ctx)
        try:
            self.check_permission(project_id)
        except AuthorizationDenied as denied_error:
            log.error(
                f"list artifacts for {project} failed: {str(denied_error)}"
            )
            return []
        artifacts = list(
            filter(
                lambda x: x['model_id']['project_id'] == project_id,
                self.metarepo_client.get_entities(
                    entity="explanationcache", request_ctx=request_ctx
                )
            )
        )
        filtered = []
        for artifact in artifacts:
            split = self.metarepo_client.get_entity(
                entity="datasplit",
                entity_id=artifact["model_input_spec"]["split_id"],
                request_ctx=request_ctx
            )

            split_name = split["name"]
            dataset_name = self.metarepo_client.get_entity(
                entity="dataset",
                entity_id=split["dataset_id"],
                request_ctx=request_ctx
            )["name"]
            model_name = self.metarepo_client.get_entity(
                entity="model",
                entity_id=artifact["model_id"]["model_id"],
                request_ctx=request_ctx
            )["name"]
            filtered.append([dataset_name, split_name, model_name])

        return filtered

    def list_data_collections(self, project):
        request_ctx = self.fetch_request_ctx()
        project_id = self._get_project_id(project, request_ctx)
        try:
            self.check_permission(project_id)
        except AuthorizationDenied as denied_error:
            log.error(
                f"list data collections for {project} failed: {str(denied_error)}"
            )
            return []
        return [
            data_collection['name']
            for data_collection in self.metarepo_client.get_entities(
                entity="dataset",
                params={"project_id": project_id},
                request_ctx=request_ctx
            )
        ]

    def list_datasplits(self, project, data_collection):
        request_ctx = self.fetch_request_ctx()
        project_id = self._get_project_id(project, request_ctx)
        try:
            self.check_permission(project_id)
        except AuthorizationDenied as denied_error:
            log.error(
                f"list data splits for {project} failed: {str(denied_error)}"
            )
            return []
        data_collection_id = self._get_dataset_id(
            project_id, data_collection, request_ctx
        )

        return [
            datasplit['name']
            for datasplit in self.metarepo_client.get_entities(
                entity="datasplit",
                params={
                    "project_id": project_id,
                    "dataset_id": data_collection_id
                },
                request_ctx=request_ctx
            )
        ]

    def list_models(self, project, use_artifact=False):
        request_ctx = self.fetch_request_ctx()
        project_id = self._get_project_id(project, request_ctx)
        try:
            self.check_permission(project_id)
        except AuthorizationDenied as denied_error:
            log.error(f"list models for {project} failed: {str(denied_error)}")
            return []
        return [
            model['name'] for model in self.metarepo_client.get_entities(
                entity="model",
                params={"project_id": project_id},
                request_ctx=request_ctx
            )
        ]

    def _get_project_id(self, project_name, request_ctx):
        if project_name is None:
            return None
        projects = self.metarepo_client.get_entities(
            entity="project",
            params={"name": project_name},
            request_ctx=request_ctx
        )
        if not projects:
            log.info(f"No project metadata found for project: {project_name}")
            return None
        if len(projects) > 1:
            log.warning(
                f"Multiple projects found with project name: {project_name}"
            )
        return projects[0]['id']

    def _get_dataset_id(self, project_id, dataset_name, request_ctx):
        datasets = self.metarepo_client.get_entities(
            entity="dataset",
            params={
                "name": dataset_name,
                "project_id": project_id
            },
            request_ctx=request_ctx
        )
        if not datasets:
            log.info(
                f"No dataset metadata for project: {project_id} dataset: {dataset_name}"
            )
        return datasets[0]["id"]

    def _get_split_id(self, project_id, dataset_id, split_name, request_ctx):
        splits = self.metarepo_client.get_entities(
            entity="datasplit",
            params={
                "name": split_name,
                "project_id": project_id,
                "dataset_id": dataset_id
            },
            request_ctx=request_ctx
        )
        if not splits:
            log.info(
                f"No datasplit metadata for project: {project_id} dataset: {dataset_id} split: {split_name}"
            )
            return None
        return splits[0]["id"]

    def _get_model_id(self, project_id, model_name, request_ctx):
        models = self.metarepo_client.get_entities(
            entity="model",
            params={
                "name": model_name,
                "project_id": project_id
            },
            request_ctx=request_ctx
        )
        if not models:
            log.info(
                f"No dataset metadata for project: {project_id} dataset: {model_name}"
            )
        return models[0]["id"]

    def get_repo_path(self, locator: Locator, prefix):
        # Override base sync_service method to use MR
        # Uses base class behavior if no metadata found
        base = super(MetarepoSyncService, self)

        @match(Locator)
        class imp(object):

            def Artifact(project, model, data_collection, split):
                request_ctx = self.fetch_request_ctx()
                if data_collection is None or split is None or model is None:
                    raise Exception(
                        'Data collection, Split, and Model parameters must not be none'
                    )

                project_id = self._get_project_id(project, request_ctx)
                try:
                    self.check_permission(project_id)
                except AuthorizationDenied as denied_error:
                    log.error(
                        f"locate artifact for {project} failed: {str(denied_error)}"
                    )
                    return None
                model_id = self._get_model_id(project_id, model, request_ctx)
                data_collection_id = self._get_dataset_id(
                    project_id, data_collection, request_ctx
                )
                split_id = self._get_split_id(
                    project_id, data_collection_id, split, request_ctx
                )

                if split_id is None:
                    return base.get_repo_path(locator, prefix)

                artifacts = self.metarepo_client.get_entities(
                    entity="explanationcache",
                    params={
                        "model_id.project_id": project_id,
                        "model_id.model_id": model_id,
                        "model_input_spec.split_id": split_id
                    },
                    request_ctx=request_ctx
                )

                filtered = []
                for a in artifacts:
                    a_dataset_id = self.metarepo_client.get_entity(
                        entity="datasplit",
                        entity_id=split_id,
                        request_ctx=request_ctx
                    )['dataset_id']
                    if a_dataset_id == data_collection_id:
                        filtered.append(a)
                if filtered:
                    if len(filtered) > 1:
                        log.warning(
                            f"Multiple artifacts found for this datasplit {split}"
                        )
                    log.info(
                        f"Successfully found artifact metadata for project: {project_id} model: {model_id} split: {split} location: {filtered[0]['location']}"
                    )
                    return filtered[0]['location'] + split + '/'

                log.info(
                    f"No artifact metadata found for project: {project} split: {split}"
                )
                return base.get_repo_path(locator, prefix)

            def Split(project, data_collection, split):
                request_ctx = self.fetch_request_ctx()
                if data_collection is None or split is None:
                    raise Exception(
                        'Data collection and Split parameters must not be none'
                    )

                project_id = self._get_project_id(project, request_ctx)
                try:
                    self.check_permission(project_id)
                except AuthorizationDenied as denied_error:
                    log.error(
                        f"locate split for {project} failed: {str(denied_error)}"
                    )
                    return None
                data_collection_id = self._get_dataset_id(
                    project_id, data_collection, request_ctx
                )

                datasplits = self.metarepo_client.get_entities(
                    entity="datasplit",
                    params={
                        "project_id": project_id,
                        "name": split,
                        "dataset_id": data_collection_id
                    },
                    request_ctx=request_ctx
                )
                if datasplits:
                    if len(datasplits) > 1:
                        log.warning(
                            f"Multiple splits found for this project: {project} split: {split}"
                        )
                    return datasplits[0]['preprocessed_locator']

                log.info(
                    f"No datasplit metadata found for project: {project} split: {split}"
                )
                return base.get_repo_path(locator, prefix)

            def DataCollection(project, data_collection):
                # Metadata locator does not exist for this. Keeping as-is, should be deprecated
                return base.get_repo_path(locator, prefix)

            def Model(project, model):
                request_ctx = self.fetch_request_ctx()
                if model is None:
                    raise Exception('Model parameter must not be none')

                project_id = self._get_project_id(project, request_ctx)
                try:
                    self.check_permission(project_id)
                except AuthorizationDenied as denied_error:
                    log.error(
                        f"locate model for {project} failed: {str(denied_error)}"
                    )
                    return None
                models = self.metarepo_client.get_entities(
                    entity="model",
                    params={
                        "project_id": project_id,
                        "name": model
                    },
                    request_ctx=request_ctx
                )
                if not models:
                    log.info(
                        f"No model metadata found for project: {project} model: {model}"
                    )
                    return base.get_repo_path(locator, prefix)
                if len(models) > 1:
                    log.warning(
                        f"Multiple models found project: {project} model: {model}"
                    )

                log.info(
                    f"Model metadata found with locator: {models[0]['locator']}"
                )
                return models[0]["locator"]

            def Export(project, model, data_collection, split, filename):
                #TODO: AZ#3181 TBD on how to interact with artifact client
                return base.get_repo_path(locator, prefix)

        return imp(locator)
