"""
Fiddler Client Module
=====================

A Python client for Fiddler service.

TODO: Add Licence.
"""
import configparser
import functools
from collections import namedtuple
from pathlib import Path
from typing import Any, Dict, Iterable, List, NamedTuple, Optional, Tuple, Union

import pandas as pd

from fiddler.api.monitoring import Monitoring
from fiddler.project import Project
from fiddler.v2.schema.alert import (
    AlertCondition,
    AlertType,
    BinSize,
    ComparePeriod,
    CompareTo,
    Metric,
    Priority,
)

from . import utils
from ._version import __version__
from .client import Fiddler, PredictionEventBundle
from .core_objects import (
    ArtifactStatus,
    BatchPublishType,
    Column,
    CustomFeature,
    DatasetInfo,
    DataType,
    DeploymentOptions,
    DeploymentType,
    ExplanationMethod,
    FiddlerPublishSchema,
    FiddlerTimestamp,
    MLFlowParams,
    ModelDeploymentParams,
    ModelInfo,
    ModelInputType,
    ModelTask,
)
from .fiddler_api import FiddlerApi as FiddlerApiV1
from .file_processor.src.constants import (
    CSV_EXTENSION,
    PARQUET_COMPRESSION,
    PARQUET_ENGINE,
    PARQUET_EXTENSION,
    PARQUET_ROW_GROUP_SIZE,
)
from .packtools import gem
from .utils import ColorLogger
from .v1_v2_compat import V1V2Compat
from .v2.api.api import Client as FiddlerApiV2
from .v2.api.explainability_mixin import (
    DatasetDataSource,
    RowDataSource,
    SqlSliceQueryDataSource,
)
from .v2.constants import ServerDeploymentMode
from .v2.schema.job import JobStatus
from .v2.schema.model_deployment import DeploymentParams, ModelDeployment
from .v2.schema.server_info import ServerInfo
from .v2.utils.helpers import match_semvar
from .validator import PackageValidator, ValidationChainSettings, ValidationModule

logger = utils.logging.getLogger(__name__)

VERSIONS = [1, 2]


class FiddlerApi:
    """Client of all connections to the Fiddler API.
    :param url:         The base URL of the API to connect to. Usually either
        https://<yourorg>.fiddler.ai (cloud) or http://localhost:4100 (onebox)
    :param org_id:      The name of your organization in the Fiddler platform
    :param auth_token:  Token used to authenticate. Your token can be
        created, found, and changed at <FIDDLER URL>/settings/credentials.
    :param proxies:     Optionally, a dict of proxy URLs. e.g.,
                    proxies = {'http' : 'http://proxy.example.com:1234',
                               'https': 'https://proxy.example.com:5678'}
    :param verbose:     if True, api calls will be logged verbosely,
                    *warning: all information required for debugging will be
                    logged including the auth_token.
    :param timeout:     How long to wait for the server to respond before giving up
    :param version:     Version of the client you want to instantiate. Options [1,2]
    """

    def __new__(
        cls,
        url: Optional[str] = None,
        org_id: Optional[str] = None,
        auth_token: Optional[str] = None,
        proxies: Optional[dict] = None,
        verbose: Optional[bool] = False,
        timeout: int = 1200,  # sec
        version: int = 2,
    ):
        url, org_id, auth_token = cls._get_connection_parameters(
            cls, url, org_id, auth_token, version
        )

        # Validation of version, org_id is handled by FiddlerApiV1.
        client_v1 = FiddlerApiV1(
            url=url,
            org_id=org_id,
            auth_token=auth_token,
            proxies=proxies,
            verbose=verbose,
            timeout=timeout,
        )
        # @todo: Handle proxies in v2
        client_v2 = FiddlerApiV2(
            url=url, organization_name=org_id, auth_token=auth_token, timeout=timeout
        )
        supported_features = cls._get_supported_features(cls, client_v1, org_id)

        # Setting server_info explicitly since /get_supported_features is not available in F2 construct
        client_v2.server_info = cls._get_server_info(cls, supported_features)

        server_deployment_mode = cls._get_server_deployment_mode(
            cls, supported_features
        )

        logger.info(f'Version deployed on the server side {server_deployment_mode}')

        compat_client = V1V2Compat(client_v2)

        if version == 2:
            logger.info('Default client is of client version 2')

            obj = lambda: None  # instantiate an empty object # noqa

            obj.list_datasets = compat_client.get_datasets
            obj.get_dataset_info = compat_client.get_dataset_info
            obj.get_dataset = compat_client.get_dataset_artifact
            obj.delete_dataset = compat_client.delete_dataset

            obj.list_projects = compat_client.get_projects
            obj.create_project = compat_client.add_project
            obj.delete_project = compat_client.delete_project

            obj.upload_dataset = (
                compat_client.upload_dataset_dataframe
            )  # this is uploading dataframe in v1 and csv in v2
            obj.upload_dataset_from_file = (
                compat_client.upload_dataset
            )  # currently only supports csv
            obj.upload_dataset_from_dir = compat_client.upload_dataset_from_dir
            # obj.process_csv = client_v1.process_csv
            # obj.process_avro = client_v1.process_avro

            obj.publish_event = compat_client.publish_event
            obj.publish_events_batch = compat_client.publish_events_batch
            # obj.publish_events_log = client_v1.publish_events_log #deprecated so not implemented
            obj.publish_events_batch_schema = compat_client.publish_events_batch_schema
            # obj.publish_parquet_s3 = client_v1.publish_parquet_s3
            obj.generate_sample_events = client_v1.generate_sample_events

            obj.upload_model_package = functools.partial(
                functools.partial(v1_upload_model_package, v1_client=client_v1),
                v2_client=client_v2,
            )
            obj.upload_model_package.__doc__ = client_v1.upload_model_package.__doc__

            obj.trigger_pre_computation = client_v1.trigger_pre_computation

            obj.register_model = functools.partial(
                functools.partial(v1_register_model, v1_client=client_v1),
                v2_client=client_v2,
            )
            obj.register_model.__doc__ = client_v1.register_model.__doc__

            obj.update_model = client_v1.update_model

            obj.add_model = functools.partial(
                functools.partial(add_model, v1_client=client_v1),
                v2_client=client_v2,
            )
            obj.add_model.__doc__ = add_model.__doc__

            obj.add_model_surrogate = functools.partial(
                _add_model_surrogate, client_v1, client_v2
            )
            obj.add_model_surrogate.__doc__ = _add_model_surrogate.__doc__

            obj.add_model_artifact = functools.partial(
                _add_model_artifact, client_v1, client_v2
            )
            obj.add_model_artifact.__doc__ = _add_model_artifact.__doc__

            obj.delete_model = functools.partial(_delete_model, client_v1, client_v2)
            obj.delete_model.__doc__ = client_v1.delete_model.__doc__

            obj.update_model_artifact = functools.partial(
                _update_model_artifact, client_v2
            )
            obj.update_model_artifact.__doc__ = _update_model_artifact.__doc__

            obj.get_model_deployment = functools.partial(
                _get_model_deployment, client_v2
            )
            obj.get_model_deployment.__doc__ = _get_model_deployment.__doc__

            obj.update_model_deployment = functools.partial(
                _update_model_deployment, client_v2
            )
            obj.update_model_deployment.__doc__ = _update_model_deployment.__doc__

            obj._trigger_model_predictions = client_v1._trigger_model_predictions

            if match_semvar(
                client_v2.server_info.server_version,
                client_v2.EXPLAINABILITY_SERVER_VERSION,
            ):
                # Explainability apis are available only after 22.12.0

                # Feature impact / importance
                obj.run_feature_importance = functools.partial(
                    _get_feature_importance, client_v2
                )
                obj.run_feature_importance.__doc__ = (
                    client_v1.run_feature_importance.__doc__
                )

                # Explain
                obj.run_explanation = functools.partial(_get_explanation, client_v2)
                obj.run_explanation.__doc__ = client_v1.run_explanation.__doc__

                # Fairness
                obj.run_fairness = functools.partial(_get_fairness, client_v2)
                obj.run_fairness.__doc__ = client_v1.run_fairness.__doc__

                # Slice query
                obj.get_slice = functools.partial(_run_slice_query, client_v2)
                obj.get_slice.__doc__ = client_v1.get_slice.__doc__

                # Predictions
                obj.run_model = functools.partial(_get_predictions, client_v2)
                obj.run_model.__doc__ = client_v1.run_model.__doc__
            else:
                obj.run_feature_importance = client_v1.run_feature_importance
                obj.run_explanation = client_v1.run_explanation
                obj.run_fairness = client_v1.run_fairness
                obj.get_slice = client_v1.get_slice
                obj.run_model = client_v1.run_model

            # explicitly binding non-conflicting v1 methods to the v2 obj
            # conflicting methods will use v2 method by default for this condition
            # obj.project = client_v1.project

            obj.list_models = compat_client.get_models
            obj.get_model_info = client_v1.get_model_info

            obj.get_mutual_information = client_v1.get_mutual_information

            # Alerts
            obj.get_alert_rules = client_v2.get_alert_rules
            obj.get_triggered_alerts = client_v2.get_triggered_alerts
            obj.add_alert_rule = client_v2.add_alert_rule
            obj.delete_alert_rule = client_v2.delete_alert_rule
            obj.build_notifications_config = client_v2.build_notifications_config

            # Baseline handling
            obj.add_baseline = client_v2.add_baseline
            obj.get_baseline = client_v2.get_baseline
            obj.get_baselines = client_v2.get_baselines
            obj.delete_baseline = client_v2.delete_baseline

            # The below methods are not used so not mapping them.
            # obj.share_project = client_v1.share_project
            # obj.unshare_project = client_v1.unshare_project
            # obj.list_org_roles = client_v1.list_org_roles
            # obj.list_project_roles = client_v1.list_project_roles
            # obj.list_teams = client_v1.list_teams

            # @todo make this available under client.v2
            # obj.initialize_monitoring = functools.partial(
            #     obj._initialize_monitoring, v1_connection=client_v1.connection
            # )

            # obj.add_monitoring_config = client_v1.add_monitoring_config
            # obj.list_segments = client_v1.list_segments
            # obj.upload_segment = client_v1.upload_segment
            # obj.activate_segment = client_v1.activate_segment
            # obj.deactivate_segment = client_v1.deactivate_segment
            # obj.delete_segment = client_v1.delete_segment
            # obj.get_segment_info = client_v1.get_segment_info
            # also retaining the sub-module approach
        else:
            logger.info('Default client is of client version 1')
            obj = client_v1
            if ServerDeploymentMode.F2 == server_deployment_mode:
                obj.publish_event = compat_client.publish_event
                obj.publish_events_batch = compat_client.publish_events_batch
                obj.publish_events_batch_schema = (
                    compat_client.publish_events_batch_schema
                )

        obj.v1 = client_v1
        obj.v2 = client_v2
        return obj

    def _get_connection_parameters(
        self, url: str, org_id: str, auth_token: str, version: int
    ) -> Tuple:
        if Path('fiddler.ini').is_file():
            config = configparser.ConfigParser()
            config.read('fiddler.ini')
            info = config['FIDDLER']
            if not url:
                url = info.get('url', None)
            if not org_id:
                org_id = info.get('org_id', None)
            if not auth_token:
                auth_token = info.get('auth_token', None)

        if not url:
            raise ValueError('Could not find url. Please enter a valid url')
        if not org_id:
            raise ValueError('Could not find org_id. Please enter a valid org_id')
        if not auth_token:
            raise ValueError(
                'Could not find auth_token. Please enter a valid auth_token'
            )
        if version not in VERSIONS:
            raise ValueError(
                f'version={version} not supported. Please enter a valid version. Supported versions={VERSIONS}'
            )

        return url, org_id, auth_token

    def _get_supported_features(self, client_v1: FiddlerApiV1, org_id: str) -> Dict:
        path: List['str'] = ['get_supported_features', org_id]
        return client_v1.connection.call(path, is_get_request=True)

    def _get_server_info(self, supported_features: Dict) -> ServerInfo:
        # @TODO refactor this once /get_supported_features is available as F2 endpoint

        server_info_dict = {
            'features': supported_features.get('features'),
            'server_version': supported_features.get('server_version'),
        }

        return ServerInfo(**server_info_dict)

    def _get_server_deployment_mode(
        self, supported_features: Dict
    ) -> ServerDeploymentMode:

        if supported_features.get('enable_fiddler_v2', False):
            return ServerDeploymentMode.F2

        return ServerDeploymentMode.F1


def v1_upload_model_package(
    artifact_path: Path,
    project_id: str,
    model_id: str,
    deployment_type: Optional[str] = DeploymentType.PREDICTOR,
    # model deployment type. One of {'predictor', 'executor'}
    image_uri: Optional[str] = None,  # image to be used for newly uploaded model
    namespace: Optional[str] = None,  # kubernetes namespace
    port: Optional[int] = 5100,  # port on which model is served
    replicas: Optional[int] = 1,  # number of replicas
    cpus: Optional[float] = 0.25,  # number of CPU cores
    memory: Optional[str] = '128m',  # amount of memory required.
    gpus: Optional[int] = 0,  # number of GPU cores
    await_deployment: Optional[bool] = True,  # wait for deployment
    is_sync=True,
    v2_client: FiddlerApiV2 = None,
    v1_client: FiddlerApiV1 = None,
):
    v1_client.upload_model_package(
        artifact_path,
        project_id,
        model_id,
        deployment_type,
        image_uri,
        namespace,
        port,
        replicas,
        cpus,
        memory,
        gpus,
        await_deployment,
    )

    call_init_monitoring(v1_client, v2_client, project_id, model_id, is_sync)


def v1_register_model(
    project_id: str,
    model_id: str,
    dataset_id: str,
    model_info: ModelInfo,
    deployment: Optional[DeploymentOptions] = None,
    cache_global_impact_importance: bool = True,
    cache_global_pdps: bool = False,
    cache_dataset: bool = True,
    is_sync=True,
    v2_client: FiddlerApiV2 = None,
    v1_client: FiddlerApiV1 = None,
):
    v1_client.register_model(
        project_id,
        model_id,
        dataset_id,
        model_info,
        deployment,
        cache_global_impact_importance,
        cache_global_pdps,
        cache_dataset,
    )
    call_init_monitoring(v1_client, v2_client, project_id, model_id, is_sync)


def add_model(
    project_id: str,
    model_id: str,
    dataset_id: str,
    model_info: ModelInfo = None,
    is_sync: Optional[bool] = True,
    v2_client: FiddlerApiV2 = None,
    v1_client: FiddlerApiV1 = None,
) -> None:
    """
    Function to add a model to fiddler for monitoring

    :param project_id: project name where the model will be added
    :type project_id: string
    :param model_id: name of the model
    :type model_id: string
    :param dataset_id: name of the dataset
    :type dataset_id: string
    :param model_info: model related information from user
    :type model_info: ModelInfo
    :param is_sync: perform add model synchronously
    :type is_sync: boolean
    """
    if model_info is None:
        raise ValueError('ModelInfo cannot be None')
    if not isinstance(model_info, ModelInfo):
        raise TypeError(
            'model_info is not an instance of fiddler.core_objects.ModelInfo'
        )

    dataset = v2_client.get_dataset(project_name=project_id, dataset_name=dataset_id)
    outputs = model_info.get_output_names()
    dataset_cols = set([col.name for col in dataset.info.columns])

    # @TODO: FDL-9002: Move output column validation to BE's ModelInfoValidator
    if not all(elem in dataset_cols for elem in outputs):
        raise ValueError(f'Dataset {dataset_id} does not have output columns')

    model = v2_client.add_model(
        model_name=model_id, project_name=project_id, info=model_info
    )
    call_init_monitoring(v1_client, v2_client, project_id, model_id, is_sync)
    logger.info(f'Successfully added model {model.name} to project {project_id}')


def _add_model_surrogate(
    client_v1: FiddlerApiV1,
    client_v2: FiddlerApiV2,
    project_id: str,
    model_id: str,
) -> None:
    """
    Trigger generation of surrogate model

    :param project_id: project name where the model will be added
    :type project_id: string
    :param model_id: name of the model
    :type model_id: string
    """
    if match_semvar(
        client_v2.server_info.server_version, client_v2.ADD_SURROGATE_MODEL_API_VERSION
    ):
        client_v2.add_model_surrogate(model_name=model_id, project_name=project_id)
        return

    model_info = Project(client_v1.connection, project_id).model(model_id).get_info()

    if (
        model_info.artifact_status
        and model_info.artifact_status.value != ArtifactStatus.NO_MODEL.value
    ):
        raise ValueError(
            f'Model {model_id} in project {project_id} already has artifact associated with it'
        )

    dataset_name = model_info.datasets[0]
    model_info.artifact_status = ArtifactStatus.SURROGATE
    client_v1.register_model(project_id, model_id, dataset_name, model_info)


def _add_model_artifact(
    client_v1: FiddlerApiV1,
    client_v2: FiddlerApiV2,
    project_id: str,
    model_id: str,
    model_dir: str,
    deployment_params: Optional[DeploymentParams] = None,
) -> None:
    """
    Upload a user model artifact to the specified model, with model binary and package.py from
    the specified model_dir

    Note: changes to model.yaml is not supported right now.

    :param project_id: project id
    :type project_id: string
    :param model_id: model id
    :type model_id: string
    :param model_dir: model directory
    :type model_dir: string
    :param deployment_params: Model deployment parameters
    :type deployment_params: DeploymentParams
    """
    if match_semvar(
        client_v2.server_info.server_version, client_v2.ADD_MODEL_ARTIFACT_API_VERSION
    ):
        client_v2.add_model_artifact(
            model_name=model_id,
            project_name=project_id,
            artifact_dir=model_dir,
            deployment_params=deployment_params,
        )
        return

    client_v1.update_model(
        project_id=project_id,
        model_id=model_id,
        model_dir=model_dir,
        force_pre_compute=True,
    )


def _delete_model(
    client_v1: FiddlerApiV1,
    client_v2: FiddlerApiV2,
    project_id: str,
    model_id: str,
    delete_prod=True,
    delete_pred=True,
) -> None:
    if match_semvar(
        client_v2.server_info.server_version, client_v2.DELETE_MODEL_API_VERSION
    ):
        client_v2.delete_model(model_name=model_id, project_name=project_id)
        return

    client_v1.delete_model(
        project_id=project_id,
        model_id=model_id,
        delete_prod=delete_prod,
        delete_pred=delete_pred,
    )


def call_init_monitoring(
    v1_client: FiddlerApiV1,
    v2_client: FiddlerApiV2,
    project_id: str,
    model_id: str,
    is_sync: bool,
):
    resp_uuid = Monitoring(
        v1_client.connection, project_id, model_id
    ).initialize_monitoring(False, False, 'fiddler2')

    if resp_uuid and is_sync:
        logger.info(
            'Model[%s/%s] - Init monitoring (UUID: %s) started',
            project_id,
            model_id,
            resp_uuid,
        )
        job_name = f'Model[{project_id}/{model_id}] - Init Monitoring'
        job_resp_final = v2_client.wait_for_job(uuid=resp_uuid, job_name=job_name)
        return job_resp_final.status == JobStatus.SUCCESS
    else:
        return resp_uuid


def _get_feature_importance(
    client_v2: FiddlerApiV2,
    project_id: str,
    model_id: str,
    dataset_id: str,
    dataset_splits: Optional[List[str]] = None,
    slice_query: Optional[str] = None,
    impact_not_importance: Optional[bool] = False,
    **kwargs,
) -> NamedTuple:
    """Get global feature importance for a model over a dataset.
    :param project_id: The unique identifier of the model's project on the
        Fiddler engine.
    :param model_id: The unique identifier of the model in the specified
        project on the Fiddler engine.
    :param dataset_id: The unique identifier of the dataset in the
        Fiddler engine.
    :param dataset_splits: If specified, importance will only be computed
        over these splits. Otherwise, all splits will be used. Only a
        single split is currently supported.
    :param slice_query: A special SQL query.
    :param impact_not_importance: Boolean flag to compute either impact or importance.
    False by default (compute feature importance).
    For text models, only feature impact is implemented.
    :param kwargs: Additional parameters to be passed to the importance
        algorithm. For example, `n_inputs`, `n_iterations`, `n_references`,
        `ci_confidence_level`.
    :return: A named tuple with the explanation results.
    """
    if (
        dataset_splits is not None
        and len(dataset_splits) > 1
        and not isinstance(dataset_splits, str)
    ):
        raise NotImplementedError(
            'Unfortunately, only a single split is '
            'currently supported for feature importance/impact'
        )

    source = (
        None
        if dataset_splits is None
        else dataset_splits
        if isinstance(dataset_splits, str)
        else dataset_splits[0]
    )

    fn_kwargs = {
        'model_name': model_id,
        'project_name': project_id,
        'num_iterations': kwargs.get('num_iterations'),
        'num_refs': kwargs.get('num_refs'),
        'ci_level': kwargs.get('ci_level'),
        'overwrite_cache': kwargs.get('overwrite_cache', False),
    }

    if slice_query:
        # Slice query data source
        fn_kwargs['data_source'] = SqlSliceQueryDataSource(
            query=slice_query, num_samples=kwargs.get('num_samples')
        )
    else:
        # Dataset data source
        fn_kwargs['data_source'] = DatasetDataSource(
            dataset_name=dataset_id,
            source=source,
            num_samples=kwargs.get('num_samples'),
        )

    if impact_not_importance:
        # Feature impact
        fn_kwargs['min_support'] = kwargs.get('min_support')
        fn_kwargs['output_columns'] = kwargs.get('output_columns')
        feature_impact = client_v2.get_feature_impact(**fn_kwargs)
        response = feature_impact._asdict()  # noqa

        # Pop new key/values
        response.pop('model_input_type')
        response.pop('model_task')

        return namedtuple('FeatureImpactResult', response)(**response)

    # Feature importance
    feature_importance = client_v2.get_feature_importance(**fn_kwargs)
    response = feature_importance._asdict()  # noqa

    # Pop new key/values
    response.pop('model_task')
    response.pop('model_input_type')

    # Rename keys to match F1 response
    response['all_obs_input_df_size'] = response.pop('total_input_samples')
    response['non_null_input_df_size'] = response.pop('valid_input_samples')

    return namedtuple('FeatureImportanceResult', response)(**response)


def _get_explanation(
    client_v2: FiddlerApiV2,
    project_id: str,
    model_id: str,
    df: pd.DataFrame,
    explanations: Union[str, Iterable[str]] = 'shap',
    dataset_id: Optional[str] = None,
    n_permutation: Optional[int] = None,
    n_background: Optional[int] = None,
    casting_type: Optional[bool] = False,
    return_raw_response=False,
    **kwargs,
) -> Any:
    if not isinstance(explanations, (str, list)):
        raise ValueError(
            'explanation can only be a string or a list of a single element'
        )

    if isinstance(explanations, list):
        if len(explanations) != 1:
            raise NotImplementedError('Only one explanation method can be used.')
        explanations = explanations[0]

    # Transform old explanation names to new ones:
    new_explanation_names = {
        'shap': 'SHAP',
        'fiddler_shapley_values': 'FIDDLER_SHAP',
        'ig_flex': 'IG',
        'permute': 'PERMUTE',
        'mean_reset': 'MEAN_RESET',
        'zero_reset': 'ZERO_RESET',
    }
    if explanations in new_explanation_names.keys():
        explanations = new_explanation_names[explanations]

    if casting_type:
        logger.warning('Casting data is deprecated.')

    fn_kwargs = {
        'model_name': model_id,
        'project_name': project_id,
        'num_permutations': n_permutation,
        'explanation_type': explanations,
        'ci_level': kwargs.get('ci_level'),
        'top_n_class': kwargs.get('top_n_class', None),
        'input_data_source': RowDataSource(row=df.to_dict(orient='records')[0]),
    }

    model_info = client_v2.get_model(project_name=project_id, model_name=model_id).info

    if (explanations in ['SHAP', 'FIDDLER_SHAP', 'PERMUTE', 'MEAN_RESET']) and (
        model_info['input-type'] != ModelInputType.TEXT.value
    ):
        # Only for non text inputs and some explanation methods
        # we need the reference dataset
        fn_kwargs['ref_data_source'] = DatasetDataSource(
            dataset_name=dataset_id, source=None, num_samples=n_background
        )

    explanation = client_v2.get_explanation(**fn_kwargs)
    response = explanation._asdict()  # noqa

    if return_raw_response:
        return response

    if len(response.keys()) == 1:
        return namedtuple('AttributionExplanation', response)(**response)

    return namedtuple('MulticlassAttributionExplanation', response)(**response)


def _get_fairness(
    client_v2: FiddlerApiV2,
    project_id: str,
    model_id: str,
    dataset_id: str,
    protected_features: List[str],
    positive_outcome: Union[str, int, float, bool],
    slice_query: Optional[str] = None,
    score_threshold: Optional[float] = 0.5,
) -> Any:
    if isinstance(protected_features, str):
        protected_features = [protected_features]

    fn_kwargs = {
        'model_name': model_id,
        'project_name': project_id,
        'score_threshold': score_threshold,
        'protected_features': protected_features,
        'positive_outcome': positive_outcome,
    }

    if slice_query:
        # Slice query data source
        fn_kwargs['data_source'] = SqlSliceQueryDataSource(query=slice_query)
    else:
        # Dataset data source
        fn_kwargs['data_source'] = DatasetDataSource(dataset_name=dataset_id)

    fairness = client_v2.get_fairness(**fn_kwargs)
    response = fairness._asdict()  # noqa

    return namedtuple('FairnessResult', response)(**response)


def _run_slice_query(
    client_v2: FiddlerApiV2,
    sql_query: str,
    project_id: str,
    columns_override: Optional[List[str]] = None,
) -> pd.DataFrame:
    fn_kwargs = {
        'project_name': project_id,
        'query': sql_query,
        'columns': columns_override,
    }

    slice_query = client_v2.run_slice_query(**fn_kwargs)

    return slice_query


def _get_predictions(
    client_v2: FiddlerApiV2,
    project_id: str,
    model_id: str,
    df: pd.DataFrame,
    log_events=False,
    casting_type=False,
) -> pd.DataFrame:
    if log_events:
        logger.warning('Log_events is deprecated.')
    if casting_type:
        logger.warning('Casting data is deprecated.')

    fn_kwargs = {
        'project_name': project_id,
        'model_name': model_id,
        'input_df': df,
    }

    predictions = client_v2.get_predictions(**fn_kwargs)

    return predictions


def _update_model_artifact(
    client_v2: FiddlerApiV2,
    project_id: str,
    model_id: str,
    artifact_dir: str,
    deployment_params: Optional[DeploymentParams] = None,
    wait: bool = True,
) -> str:
    """
    Update model artifact of an existing model
    :param model_id: Model name
    :param project_id: Project name
    :param artifact_dir: Model artifact directory
    :param deployment_params: Model deployment parameters
    :param wait: Whether to wait for async job to finish or return
    :return: Async job uuid
    """
    return client_v2.update_model_artifact(
        model_name=model_id,
        project_name=project_id,
        artifact_dir=artifact_dir,
        deployment_params=deployment_params,
        wait=wait,
    )


def _get_model_deployment(
    client_v2: FiddlerApiV2,
    project_id: str,
    model_id: str,
) -> ModelDeployment:
    """
    Get model deployment object
    :param model_id: Model name
    :param project_id: Project name
    :return: Model deployment object
    """
    return client_v2.get_model_deployment(
        model_name=model_id,
        project_name=project_id,
    )


def _update_model_deployment(
    client_v2: FiddlerApiV2,
    project_id: str,
    model_id: str,
    active: Optional[bool] = None,
    replicas: Optional[int] = None,
    cpu: Optional[int] = None,
    memory: Optional[int] = None,
    wait: bool = True,
) -> ModelDeployment:
    """
    Update model deployment fields like replicas, cpu, memory
    :param model_id: Model name
    :param project_id: Project name
    :param active: Set False to scale down model deployment and True to scale up
    :param replicas: Number of model deployment replicas to run
    :param cpu: Amount of milli cpus to allocate for each replica
    :param memory: Amount of mebibytes memory to allocate for each replica
    :param wait: Whether to wait for async job to finish or return
    :return: Model deployment object
    """
    return client_v2.update_model_deployment(
        model_name=model_id,
        project_name=project_id,
        active=active,
        replicas=replicas,
        cpu=cpu,
        memory=memory,
        wait=wait,
    )


__all__ = [
    '__version__',
    'BatchPublishType',
    'Column',
    'CustomFeature',
    'ColorLogger',
    'DatasetInfo',
    'DataType',
    'Fiddler',
    'FiddlerApi',
    'FiddlerTimestamp',
    'FiddlerPublishSchema',
    'gem',
    'MLFlowParams',
    'ModelDeploymentParams',
    'ModelInfo',
    'ModelInputType',
    'ModelTask',
    'ExplanationMethod',
    'PredictionEventBundle',
    'PackageValidator',
    'ValidationChainSettings',
    'ValidationModule',
    'utils',
    # Exposing constants
    'CSV_EXTENSION',
    'PARQUET_EXTENSION',
    'PARQUET_ROW_GROUP_SIZE',
    'PARQUET_ENGINE',
    'PARQUET_COMPRESSION',
]
