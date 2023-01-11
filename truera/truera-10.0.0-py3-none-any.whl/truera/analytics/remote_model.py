from abc import ABC
from abc import abstractmethod
import collections
from dataclasses import dataclass
from datetime import datetime
import json
import logging
from threading import Lock
from threading import Timer
import time
from typing import Mapping, Optional, Tuple, Type, Union

import numpy as np
import pandas as pd
from prometheus_client import Summary
import requests

from truera.aiq.realized_background_data_split_info import \
    RealizedBackgroundDataSplitInfo
from truera.analytics.dataset import Dataset
from truera.analytics.loader.explanation_config_loader import \
    ExplanationConfigLoader
from truera.authn.usercontext import RequestContext
from truera.modelrunner.client.models.dataset_split import DatasetSplit
from truera.modelrunner.client.models.feature_influence_options import \
    FeatureInfluenceOptions
from truera.modelrunner.client.models.feature_map import FeatureMap
from truera.modelrunner.client.models.feature_mapping_item import \
    FeatureMappingItem
from truera.modelrunner.client.models.format import Format
from truera.modelrunner.client.models.index_range import IndexRange
from truera.modelrunner.client.models.ingestion_mode import IngestionMode
from truera.modelrunner.client.models.model import Model
from truera.modelrunner.client.models.new_job import NewJob
from truera.modelrunner.client.models.new_run import NewRun
from truera.modelrunner.client.models.operation_type import OperationType
from truera.modelrunner.client.models.output_spec import OutputSpec
from truera.modelrunner.client.models.output_type import OutputType
from truera.modelrunner.client.models.partial_dependence_plot_options import \
    PartialDependencePlotOptions
from truera.modelrunner.client.models.prediction_options import \
    PredictionOptions
from truera.modelrunner.client.models.scorer_type import ScorerType
from truera.modelrunner.client.models.system_columns import SystemColumns
from truera.modelrunner.client.models.url_input_spec import UrlInputSpec
from truera.modelrunner.client.rest import ApiException
from truera.modelrunner.client_util import client_api_creator
from truera.modelrunner.daemon.client.api_client import ApiClient
from truera.modelrunner.daemon.client.models.daemon_mode_fi_request import \
    DaemonModeFIRequest
from truera.modelrunner.daemon.client.models.daemon_mode_fi_response import \
    DaemonModeFIResponse
from truera.modelrunner.daemon.client.models.daemon_mode_predict_request import \
    DaemonModePredictRequest
from truera.modelrunner.daemon.client.models.daemon_mode_predict_response import \
    DaemonModePredictResponse
from truera.modelrunner.daemon.client.models.split_data_frame_input_spec import \
    SplitDataFrameInputSpec
from truera.modelrunner.daemon.client.models.split_orient_data_frame import \
    SplitOrientDataFrame
from truera.protobuf.public.error_details_pb2 import \
    ErrorDetails  # pylint: disable=no-name-in-module
from truera.protobuf.public.model_output_type_pb2 import \
    ModelOutputType  # pylint: disable=no-name-in-module
from truera.public import feature_influence_constants as fi_constants
from truera.utils.grpc_interceptor.common.auth_interceptor import auth_context
from truera.utils.truera_status import TruEraInternalError
from truera.utils.truera_status import TruEraInvalidArgumentError

MR_ID_COLUMN_NAME = "id_mr"
MR_TIMESTAMP_COLUMN_NAME = "timestamp_mr"

# TODO: Explore - what are the limitations of auth_context.request_context?
# Can we use this version of local threading across other Python services/call to metarepo?


class RemoteModelCommunicator(ABC):

    def __init__(self, model_runner_uri: str):
        self._model_runner_uri: str = model_runner_uri
        self.logger = logging.getLogger(__name__)

    def request_client(self):
        return requests

    def get_data_from_response(self, response):
        if hasattr(response, 'text'):
            return response.text
        if hasattr(response, 'content'):
            return response.content
        if hasattr(response, 'data'):
            return response.data
        return ''

    def ping(self):
        response = self.request_client().get(self.ping_uri())
        return response.status_code == 200

    def predict(
        self,
        data: pd.DataFrame,
        system_columns: SystemColumns,
        options: PredictionOptions,
        include_system_data: bool = False
    ) -> np.ndarray:
        serialized_data, serialized_data_content_type = self.serialize_model_prediction_data(
            data, system_columns, options
        )

        headers = {'Content-type': serialized_data_content_type}

        response = self._post_request_model_runner(
            self.predict_uri(), serialized_data, headers
        )

        if response.status_code != 200:
            error = "Calling remote uri failed: %d, %s" % (
                response.status_code, self.get_data_from_response(response)
            )
            self.logger.error(error)
            raise Exception(f"Call to predict daemon mode API failed : {error}")

        return self.deserialize_model_prediction_response(
            self.get_data_from_response(response),
            include_system_data=include_system_data
        )

    def feature_influence(
        self,
        data: pd.DataFrame,
        targets: pd.DataFrame,
        system_columns: SystemColumns,
        options,
        include_system_data: bool = False
    ) -> pd.DataFrame:
        serialized_data, serialized_data_content_type = self.serialize_feature_influence_data(
            data, targets, system_columns, options
        )
        headers = {'Content-type': serialized_data_content_type}

        response = self._post_request_model_runner(
            self.feature_influence_uri(), serialized_data, headers
        )

        if response.status_code != 200:
            error = "Calling remote uri failed: %d, %s" % (
                response.status_code, self.get_data_from_response(response)
            )
            self.logger.error(error)
            raise Exception(f"Call to FI daemon mode API failed : {error}")
        return self.deserialize_feature_influence_response(
            self.get_data_from_response(response),
            include_system_data=include_system_data
        )

    def predict_uri(self) -> str:
        return "{}/invocations".format(self._model_runner_uri)

    def feature_influence_uri(self) -> str:
        return "{}/feature_influence".format(self._model_runner_uri)

    def ping_uri(self) -> str:
        return "{}/ping".format(self._model_runner_uri)

    @abstractmethod
    def serialize_model_prediction_data(
        self, data, system_columns: SystemColumns, options: PredictionOptions
    ) -> Tuple[str, str]:
        pass

    @abstractmethod
    def deserialize_model_prediction_response(
        self,
        serialized_data,
        include_system_data: bool = False
    ) -> pd.DataFrame:
        pass

    @abstractmethod
    def serialize_feature_influence_data(
        self, data, targets, system_columns: SystemColumns, options
    ) -> Tuple[str, str]:
        pass

    @abstractmethod
    def deserialize_feature_influence_response(
        self,
        serialized_data,
        include_system_data: bool = False
    ) -> pd.DataFrame:
        pass

    def _post_request_model_runner(self, uri: str, serialized_data, headers):
        self.logger.debug(
            "Called model runner with url: %s", self._model_runner_uri
        )
        self.logger.debug("Calling uri: %s", uri)
        response = self.request_client().post(
            uri, data=serialized_data, headers=headers
        )
        if (response.status_code != 200):
            error = "Calling remote uri failed: %d, %s" % (
                response.status_code, self.get_data_from_response(response)
            )
            self.logger.error(error)
            raise Exception(f"Failed to call predict API: {error}")
        return response


@dataclass
class BackgroundData:
    dataset_id: str
    split_id: str
    locator: str


class DaemonModelRunnerInfo:

    def __init__(self, run_id: str, request_context: RequestContext):
        if run_id is None or request_context is None:
            raise TruEraInternalError(
                "DaemonModelRunnerInfo was initialized with none "
                "run id or none request_context"
            )
        self.run_id = run_id
        self.request_context = request_context


class RemoteModel(ABC):
    """Abstraction for a remotely hosted model 
    """
    DAEMON_MODE_TIMEOUT_SECONDS = 120  # TODO(AU) plumb via config
    DAEMON_MODE_LEASE_EXTENSION_PERIOD_SECONDS = 60  # TODO(AU) plumb via config

    def __init__(
        self, model_id, model_uri, client_config: dict,
        output_type: ModelOutputType,
        remote_model_communicator_constructor: Type[RemoteModelCommunicator],
        feature_list_dao, **kwargs
    ):
        self.model_id = model_id
        # TODO(AU) the columns being passed here is a
        # hack as most of explanation code works with np arrays
        # and predict API expects pandas
        self.model_uri = model_uri
        self.dataset: Dataset = None
        self.logger = logging.getLogger('ailens.RemoteModel')
        self.remote_model_communicator_constructor = remote_model_communicator_constructor
        self.remote_model_communicator: RemoteModelCommunicator = None
        self.output_type = RemoteModel.convert_to_modelrunner_client_output_type(
            output_type
        )
        self.feature_list_dao = feature_list_dao
        host = client_config['remote-model']['url']
        self.mrc_connector = client_api_creator.ModelRunnerCoordinatorConnector(
            host
        )
        self._daemon_model_runner_info: Optional[DaemonModelRunnerInfo] = None
        self.project_id = kwargs['project_id']
        self.analytics_config_loader: ExplanationConfigLoader = kwargs[
            'analytics_config_loader']
        assert (
            self.analytics_config_loader
        ), "Analytics config loader not passed for (project:{},model:{})".format(
            self.project_id, self.model_id
        )
        self._daemon_runner_lock = Lock()
        self._last_daemon_run_access_time = datetime.utcnow()
        self._lease_extension_timer = Timer(
            RemoteModel.DAEMON_MODE_LEASE_EXTENSION_PERIOD_SECONDS,
            self._try_extend_lease_or_terminate_run
        )
        self._lease_extension_timer.start()

    def stop(self):
        self._daemon_runner_lock.acquire()
        try:
            self._lease_extension_timer.cancel()
        finally:
            self._daemon_runner_lock.release()

    predict_timer = Summary(
        'aiq_remote_model_request_processing_seconds_predict',
        'Time spent processing request'
    )

    def _ensure_daemon_runner_is_launched(
        self, request_ctx: RequestContext,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo
    ):
        self._daemon_runner_lock.acquire()
        try:
            if self._daemon_model_runner_info:
                run_id = self._daemon_model_runner_info.run_id
            else:
                self.logger.info(
                    "No daemon mode run id found, launching a daemon mode runner."
                )
                if not realized_background_data_split_info:
                    # Currently FI requests always pass a pointer to data, still good to log this for the future.
                    self.logger.warning(
                        "No background data passed to runner. FIs will be computed only if data is passed in request."
                    )
                run_id = self._launch_daemon_mode_job(
                    request_ctx, realized_background_data_split_info
                    is not None, realized_background_data_split_info
                )
            self._last_daemon_run_access_time = datetime.utcnow()
            return run_id
        finally:
            self._daemon_runner_lock.release()

    @staticmethod
    def convert_to_modelrunner_client_output_type(
        output_type: ModelOutputType
    ) -> str:
        if output_type == ModelOutputType.REGRESSION:
            return OutputType.REGRESSION
        return OutputType.CLASSIFICATION

    def launch_model_prediction_job(
        self, score_type, data_filepath, label_filepath, data_split_id, start,
        stop, filepath, system_columns, maximum_model_runner_failure_rate,
        ingestion_mode, scratch_path
    ) -> str:
        options = self._prediction_options(
            score_type, maximum_model_runner_failure_rate
        )
        return self._launch_job(
            data_filepath, label_filepath, data_split_id, start, stop, filepath,
            OperationType.PREDICTIONS, options, Format.CSV, system_columns,
            ingestion_mode, scratch_path
        )

    def launch_feature_influence_job(
        self, request_ctx: RequestContext, score_type, data_filepath,
        label_filepath, data_split_id,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo,
        start, stop, filepath, system_columns,
        maximum_model_runner_failure_rate: Optional[float],
        ingestion_mode: IngestionMode, scratch_path: str
    ) -> str:
        options = self._feature_influence_options(
            request_ctx, score_type, realized_background_data_split_info,
            maximum_model_runner_failure_rate
        )
        return self._launch_job(
            data_filepath, label_filepath, data_split_id, start, stop, filepath,
            OperationType.FEATURE_INFLUENCE, options, Format.CSV,
            system_columns, ingestion_mode, scratch_path
        )

    def launch_partial_dependence_plot_job(
        self, request_ctx: RequestContext, score_type, num,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo,
        filepath
    ) -> str:
        options = self._partial_dependence_plot_options(
            request_ctx, score_type, realized_background_data_split_info
        )
        return self._launch_job(
            "", None, realized_background_data_split_info.id, 0, num, filepath,
            OperationType.PARTIAL_DEPENDENCE_PLOT, options, Format.PROTO, None,
            False, None
        )

    def _launch_job(
        self, data_filepath, label_filepath, data_split_id, start, stop,
        filepath, op_type, options, output_format, system_columns,
        ingestion_mode, scratch_path
    ) -> str:
        if ingestion_mode == IngestionMode.DATASVC:
            # In the data service ingestion mode when model runner writing to scratch path
            # it has to give id and timestamp columns some name.
            # it can not be same as system columns because those are internal names will be given by data service.
            # MR ingestion is working as external ingestion in this mode.
            output_spec = OutputSpec(
                uri=None,
                scratch_path=scratch_path,
                format=output_format,
                ingestion_mode=IngestionMode.DATASVC,
                mr_id_column_name=MR_ID_COLUMN_NAME,
                mr_time_column_name=MR_TIMESTAMP_COLUMN_NAME,
                data_collection_id=self.dataset.dataset_id
            )
        else:
            output_spec = OutputSpec(
                uri=filepath,
                format=output_format,
                ingestion_mode=IngestionMode.DIRECT_WRITE
            )
        index_range = IndexRange(start=start, end=stop)
        input_spec = UrlInputSpec(
            uri=data_filepath,
            targets_uri=label_filepath,
            split_id=data_split_id,
            index_range=index_range,
            format=Format.CSV,
            system_columns=system_columns
        )
        job = NewJob(
            op_type=op_type,
            command_options=options,
            input_spec=input_spec,
            output_spec=output_spec
        )
        return self._launch_model(daemon=False, job_spec=job)

    def _score_type_str_to_api(self, score_type: str) -> ScorerType:
        score_type_str_map = {
            fi_constants.PREDICTOR_SCORE_TYPE_LOGITS:
                ScorerType.LOGITS,
            fi_constants.PREDICTOR_SCORE_TYPE_PROBITS:
                ScorerType.PROBITS,
            fi_constants.PREDICTOR_SCORE_TYPE_REGRESSION:
                ScorerType.REGRESSION,
            fi_constants.PREDICTOR_SCORE_TYPE_LOG_LOSS:
                ScorerType.LOG_LOSS,
            fi_constants.PREDICTOR_SCORE_TYPE_MAE_CLASSIFICATION:
                ScorerType.MEAN_ABSOLUTE_ERROR_FOR_CLASSIFICATION,
            fi_constants.PREDICTOR_SCORE_TYPE_MAE_REGRESSION:
                ScorerType.MEAN_ABSOLUTE_ERROR_FOR_REGRESSION,
            fi_constants.PREDICTOR_SCORE_TYPE_CLASSIFICATION:
                ScorerType.CLASSIFICATION,
            fi_constants.PREDICTOR_SCORE_TYPE_LOGITS_UNNORM:
                ScorerType.LOGITS_UNNORMALIZED
        }
        if score_type not in score_type_str_map:
            raise TruEraInternalError(f"Invalid score type: {score_type}")
        return score_type_str_map[score_type]

    def _get_job_spec_daemon_mode(
        self, request_ctx: RequestContext,
        is_feature_influence_computation: bool,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo
    ):
        if is_feature_influence_computation:
            feature_influence_options = self._feature_influence_options(
                request_ctx, None, realized_background_data_split_info, None
            )
            return NewJob(
                op_type=OperationType.FEATURE_INFLUENCE,
                command_options=feature_influence_options
            )
        return None

    def _feature_influence_options(
        self,
        request_ctx: RequestContext,
        score_type,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo,
        maximum_model_runner_failure_rate: Optional[float],
    ) -> FeatureInfluenceOptions:
        ret = FeatureInfluenceOptions()
        self._explanation_options(
            request_ctx, score_type, realized_background_data_split_info,
            maximum_model_runner_failure_rate, ret
        )
        return ret

    def _partial_dependence_plot_options(
        self,
        request_ctx: RequestContext,
        score_type,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo,
    ) -> PartialDependencePlotOptions:
        ret = PartialDependencePlotOptions()
        self._explanation_options(
            request_ctx, score_type, realized_background_data_split_info, None,
            ret
        )
        ret.num_xs = 1000  # TODO(davidkurokawa): Take this as a parameter.
        return ret

    def _explanation_options(
        self, request_ctx: RequestContext, score_type,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo,
        maximum_model_runner_failure_rate: Optional[float],
        ret: Union[FeatureInfluenceOptions, PartialDependencePlotOptions]
    ) -> None:
        analytics_config = self.analytics_config_loader.fetch_config(
            request_ctx, self.project_id
        )
        background_dataset_artifact = DatasetSplit(
            split_id=realized_background_data_split_info.id,
            dataset_id=self.dataset.dataset_id,
            url=realized_background_data_split_info.filepath,
            pretransform_url=realized_background_data_split_info.
            pretransformFilepath,
            system_columns=realized_background_data_split_info.system_columns,
            actual_indices=realized_background_data_split_info.actual_indices
        )
        feature_map = self._create_feature_map(
            self.feature_list_dao.get_by_params(
                request_ctx=request_ctx,
                params={
                    'data_collection_id': self.dataset.dataset_id,
                    # Devnote: Project id is needed since it is the authz scope.
                    'project_id': self.project_id
                }
            )
        )
        if not feature_map:
            self.logger.warning(
                "No feature map found for data_collection " +
                self.dataset.dataset_id + " in project " + self.project_id + "."
            )
        self._validate_input_dataset(
            feature_map, realized_background_data_split_info.id
        )
        scorer_type_api = None
        if score_type is not None:
            scorer_type_api = self._score_type_str_to_api(score_type)
        ret.scorer_type = scorer_type_api
        ret.num_samples = analytics_config.num_samples
        ret.background_dataset_split = background_dataset_artifact
        ret.feature_mapping_spec = feature_map
        if maximum_model_runner_failure_rate is not None:
            ret.maximum_failure_rate = maximum_model_runner_failure_rate

    def _prediction_options(
        self, scorer_type: str,
        maximum_model_runner_failure_rate: Optional[float]
    ) -> PredictionOptions:
        scorer_type_api = self._score_type_str_to_api(scorer_type)
        return PredictionOptions(
            scorer_type=scorer_type_api,
            maximum_failure_rate=maximum_model_runner_failure_rate
        )

    @predict_timer.time()
    def predict_proba_remote(
        self,
        request_ctx: RequestContext,
        data: pd.DataFrame,
        system_columns: SystemColumns,
        scorer_type: str,
        include_system_data: bool = False
    ) -> pd.DataFrame:
        self._ensure_daemon_runner_is_launched(request_ctx, None)
        options = self._prediction_options(scorer_type, None)
        ret = self.remote_model_communicator.predict(
            data,
            system_columns,
            options,
            include_system_data=include_system_data
        )
        # TODO(AB#2483) The return data columns are incompatible between python/java model runners.
        # Need to converge to a common standard, and then look at the same value across the stack.
        return ret

    fi_timer = Summary(
        'aiq_remote_model_request_processing_seconds_feature_importance',
        'Time spent processing request'
    )

    @fi_timer.time()
    def feature_influence_from_daemon(
        self,
        request_ctx: RequestContext,
        scorer_type,
        xs,
        ys,
        system_columns,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo,
        include_system_data: bool = False
    ) -> Mapping[str, float]:
        self._ensure_daemon_runner_is_launched(
            request_ctx, realized_background_data_split_info
        )
        self.logger.debug("Data: %s, %s", type(xs), xs)
        self.logger.info("Scorer Type : %s", scorer_type)
        options = FeatureInfluenceOptions()
        self._explanation_options(
            request_ctx, scorer_type, realized_background_data_split_info, None,
            options
        )
        self.logger.debug("Calling remote model")
        fi_pd = self.remote_model_communicator.feature_influence(
            xs,
            ys,
            system_columns,
            options,
            include_system_data=include_system_data
        )
        self.logger.debug("Called remote model")
        return fi_pd

    def _launch_daemon_mode_job(
        self, request_ctx: RequestContext,
        is_feature_influence_computation: bool,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo
    ) -> str:
        run_id = self._launch_model(
            daemon=True,
            job_spec=self._get_job_spec_daemon_mode(
                request_ctx, is_feature_influence_computation,
                realized_background_data_split_info
            )
        )
        self.logger.info(
            "Launched model in daemon mode with run id: %s", run_id
        )
        if not self._validate_model_runner_connectivity(
            run_id, timeout_sec=200
        ):
            raise RemoteModelError(
                "Could not validate model runner connectivity in time. RunId: %s"
                % run_id
            )
        self._daemon_model_runner_info = DaemonModelRunnerInfo(
            run_id=run_id, request_context=auth_context.request_context
        )
        return run_id

    def _try_extend_lease_or_terminate_run(self):
        self._daemon_runner_lock.acquire()
        try:
            if self._daemon_model_runner_info:
                if (
                    datetime.utcnow() - self._last_daemon_run_access_time
                ).seconds > RemoteModel.DAEMON_MODE_TIMEOUT_SECONDS:
                    self.logger.warning(
                        (
                            "Last daemon request received at %s UTC. "
                            "Daemon mode request timeout in seconds: %d. "
                            "Terminating the model runner with run id: %s"
                        ), self._last_daemon_run_access_time,
                        RemoteModel.DAEMON_MODE_TIMEOUT_SECONDS,
                        self._daemon_model_runner_info.run_id
                    )
                    self.terminate_daemon_mode_job()
                else:
                    self.logger.info(
                        "Extending daemon mode model runner lease for run id: %s",
                        self._daemon_model_runner_info.run_id
                    )
                    response = self.mrc_connector.api_for_current_credentials(
                        self._daemon_model_runner_info.request_context
                    ).extend_lease(self._daemon_model_runner_info.run_id)
                    self.logger.info("Done extending lease.")
            else:
                self.logger.debug(
                    "Extend lease called but no daemon mode run id found."
                )

            self._lease_extension_timer = Timer(
                RemoteModel.DAEMON_MODE_LEASE_EXTENSION_PERIOD_SECONDS,
                self._try_extend_lease_or_terminate_run
            )
            self._lease_extension_timer.start()
        except Exception:
            self.logger.exception(
                "Encountered error during daemon runner lease extension for run id "
                + self._daemon_model_runner_info.run_id
            )
        finally:
            self._daemon_runner_lock.release()

    def _validate_input_dataset(self, feature_map, background_data_split_id):
        split = self.dataset.get_split(background_data_split_id)
        if split.pre_transform_locator and split.post_transform_locator and not feature_map:
            if set(split.feature_names) != set(split.processed_feature_names):
                raise TruEraInvalidArgumentError(
                    "No feature map provided! Please provide feature map when pre- and post-transform columns are different."
                )

    launch_timer = Summary(
        'aiq_remote_model_request_processing_seconds_launch_model',
        'Time spent processing request'
    )

    @launch_timer.time()
    def _launch_model(self, *, daemon=False, job_spec: Optional[NewJob] = None):
        assert daemon or job_spec is not None
        model_artifact = Model(self.model_id, self.model_uri)
        self.logger.info(
            "Launching model %s of type %s, isDaemon: %d", self.model_id,
            self.__class__.__name__, daemon
        )
        new_run = NewRun(
            project_id=self.project_id,
            model=model_artifact,
            is_daemon=daemon,
            output_type=self.output_type,
            job_spec=job_spec
        )
        self.logger.info("Starting job: %s", new_run)

        try:
            run_details = self.mrc_connector.api_for_current_credentials(
            ).create_run(new_run)
            state = run_details.state
            if state == "Failed" or state == "Invalid":
                error_str = ""
                if run_details.job and run_details.job.task_status and run_details.job.task_status.error:
                    error_str = run_details.job.task_status.error
                self.logger.error(
                    "Waiting on job that has already failed. %s", run_details
                )
                raise TruEraInternalError(
                    f"Model Runner for model id {self.model_id} (runId: {run_details.id}) failed with state {run_details.state} with error {error_str}",
                    ErrorDetails(
                        source_service="truera.ModelRunner",
                        model_runner_job_id=run_details.id
                    )
                )
            else:
                self.logger.info("Run created with id %s", run_details.id)
        except ApiException as e:
            self.logger.error(
                "Exception when calling DefaultApi->create_run for model %s: %s\n",
                self.model_id, e
            )
            raise e
        return str(run_details.id)

    terminate_timer = Summary(
        'aiq_remote_model_request_processing_seconds_terminate_model',
        'Time spent processing request'
    )

    @terminate_timer.time()
    def terminate_daemon_mode_job(self):
        if self._daemon_model_runner_info is not None:
            try:
                response = self.mrc_connector.api_for_current_credentials(
                    self._daemon_model_runner_info.request_context
                ).delete_run(self._daemon_model_runner_info.run_id)
                self._launched = False
                self.remote_model_communicator = None
                self._daemon_model_runner_info = None
                self.logger.info(response)
            except ApiException as e:
                self.logger.error(
                    "Exception when calling DefaultApi->delete_run: %s\n" % e
                )
                raise

    def _validate_model_runner_connectivity(self, run_id, timeout_sec=20):
        assert run_id
        validation_start_time = time.time()
        while time.time() - validation_start_time < timeout_sec:
            endpoint = None
            try:
                run_details = self.mrc_connector.api_for_current_credentials(
                ).get_run_by_id(run_id)
                state = run_details.state
                self.logger.debug("Run details: %s\n, %s", state, run_details)
                if (state == "Failed" or state == "Invalid"):
                    # Failed is a terminal state, unlikely that we will recover.
                    self.logger.error("Model runner in bad state: " + state)
                    self.remote_model_communicator = None
                    self._launched = False
                    break

                if (run_details.state == "Running"):
                    assert len(run_details.endpoints) > 0
                    endpoint = run_details.endpoints[0]
            except:
                pass

            if endpoint:
                try:
                    remote_model_communicator_tmp = self.remote_model_communicator_constructor(
                        endpoint
                    )
                    if remote_model_communicator_tmp.ping():
                        self.remote_model_communicator = remote_model_communicator_tmp
                        self._launched = True
                        self.logger.info(
                            "Validation successful. Model %s is available",
                            self.model_id
                        )
                        return True
                    else:
                        self.remote_model_communicator = None
                except Exception as e:
                    pass

            # Either we failed to connect or status wasn't 200.
            # Try to refresh the model state and endpoint information
            # before we try to reconnect

            time.sleep(1)

        return False

    def _create_feature_map(self, feature_map_table_entry) -> FeatureMap:
        feature_mapping_items = []

        if feature_map_table_entry is None or not feature_map_table_entry.features:
            return None

        for feature in feature_map_table_entry.features:
            feature_mapping_items.append(
                FeatureMappingItem(
                    input_column_name=feature.name,
                    output_column_names=[
                        item for item in feature.derived_model_readable_columns
                    ]
                )
            )

        return FeatureMap(features=feature_mapping_items)


class SkLearnRemoteModel(RemoteModelCommunicator):
    _HEADER_CONTENT_TYPE_FI = 'application/json; format=pandas-split'

    def __init__(self, url):
        super().__init__(url)

    def deserialize_model_prediction_response(
        self,
        serialized_data,
        include_system_data: bool = False
    ) -> pd.DataFrame:
        self.logger.debug("Prediction response data : " + str(serialized_data))
        json_data = collections.namedtuple('json_data', 'data')
        response: DaemonModePredictResponse = ApiClient().deserialize(
            json_data(data=serialized_data), 'DaemonModePredictResponse'
        )
        system_columns = response.system_columns
        result_df = pd.DataFrame(
            data=response.predict_data_frame.data,
            columns=response.predict_data_frame.columns
        )
        if system_columns is not None:
            if system_columns.id_column_name:
                result_df.set_index(system_columns.id_column_name, inplace=True)
            if system_columns.timestamp_column_name and not include_system_data:
                result_df.drop(
                    system_columns.timestamp_column_name,
                    axis="columns",
                    inplace=True
                )
        return result_df

    def serialize_feature_influence_data(
        self, data, targets, system_columns: SystemColumns, options
    ) -> Tuple[str, str]:
        if system_columns is not None and system_columns.id_column_name:
            data = data.reset_index()
            if targets is not None:
                targets = targets.reset_index()

        input_data_frame = SplitOrientDataFrame(
            columns=data.columns.tolist(),
            index=data.index.tolist(),
            data=data.to_numpy().tolist()
        )
        if targets is not None:
            target_data_frame = SplitOrientDataFrame(
                columns=targets.columns.tolist(),
                index=targets.index.tolist(),
                data=targets.to_numpy().tolist()
            )
        else:
            target_data_frame = None

        input_spec = SplitDataFrameInputSpec(
            split_input_data_frame=input_data_frame,
            split_target_data_frame=target_data_frame,
            system_columns=system_columns
        )
        request = DaemonModeFIRequest(input_spec=input_spec, fi_options=options)
        # sanitize for serialization is called to keep the json in camel case.
        return json.dumps(
            ApiClient().sanitize_for_serialization(request)
        ), self._HEADER_CONTENT_TYPE_FI

    def serialize_model_prediction_data(
        self, data, system_columns: SystemColumns, options: PredictionOptions
    ) -> Tuple[str, str]:
        if system_columns is not None and system_columns.id_column_name:
            data = data.reset_index()
        input_data_frame = SplitOrientDataFrame(
            columns=data.columns.tolist(),
            index=data.index.tolist(),
            data=data.to_numpy().tolist()
        )
        input_spec = SplitDataFrameInputSpec(
            split_input_data_frame=input_data_frame,
            system_columns=system_columns
        )
        request = DaemonModePredictRequest(
            input_spec=input_spec, options=options
        )
        # sanitize for serialization is called here to keep json in camel case
        return json.dumps(
            ApiClient().sanitize_for_serialization(request)
        ), 'application/json'

    def deserialize_feature_influence_response(
        self,
        serialized_data,
        include_system_data: bool = False
    ) -> pd.DataFrame:
        self.logger.debug("FI response data : " + str(serialized_data))
        json_data = collections.namedtuple('json_data', 'data')
        response: DaemonModeFIResponse = ApiClient().deserialize(
            json_data(data=serialized_data), 'DaemonModeFIResponse'
        )
        response_df = pd.DataFrame(
            data=response.fi_data_frame.data,
            columns=response.fi_data_frame.columns
        )
        system_columns = response.system_columns
        if system_columns is not None:
            if system_columns.id_column_name:
                response_df.set_index(
                    system_columns.id_column_name, inplace=True
                )
            if system_columns.timestamp_column_name and not include_system_data:
                response_df.drop(
                    system_columns.timestamp_column_name,
                    axis="columns",
                    inplace=True
                )
        return response_df


class H2ORemoteModelCommunicator(RemoteModelCommunicator):
    _HEADER_CONTENT_TYPE = 'application/json'

    def deserialize_model_prediction_response(
        self,
        serialized_data,
        include_system_data: bool = False
    ) -> pd.DataFrame:
        self.logger.debug("Prediction response data : " + str(serialized_data))
        json_data = collections.namedtuple('json_data', 'data')
        response: DaemonModePredictResponse = ApiClient().deserialize(
            json_data(data=serialized_data), 'DaemonModePredictResponse'
        )
        return pd.DataFrame(
            data=response.predict_data_frame.data,
            columns=response.predict_data_frame.columns
        )

    def serialize_feature_influence_data(
        self, data, targets, system_columns: SystemColumns, options
    ) -> Tuple[str, str]:
        input_data_frame = SplitOrientDataFrame(
            data=data.to_numpy().tolist(),
            columns=data.columns.tolist(),
            index=data.index.tolist()
        )
        if targets is not None:
            target_data_frame = SplitOrientDataFrame(
                data=targets.to_numpy().tolist(),
                columns=targets.columns.tolist(),
                index=targets.index.tolist()
            )
        else:
            target_data_frame = None
        input_spec = SplitDataFrameInputSpec(
            split_input_data_frame=input_data_frame,
            split_target_data_frame=target_data_frame,
            system_columns=system_columns
        )
        # sanitize for serialization is called to keep the json in camel case.
        request = DaemonModeFIRequest(input_spec=input_spec, fi_options=options)
        return json.dumps(
            ApiClient().sanitize_for_serialization(request)
        ), self._HEADER_CONTENT_TYPE

    def deserialize_feature_influence_response(
        self,
        serialized_data,
        include_system_data: bool = False
    ) -> pd.DataFrame:
        self.logger.debug("FI response data : " + str(serialized_data))
        json_data = collections.namedtuple('json_data', 'data')
        response: DaemonModeFIResponse = ApiClient().deserialize(
            json_data(data=serialized_data), 'DaemonModeFIResponse'
        )
        return pd.DataFrame(
            data=response.fi_data_frame.data,
            columns=response.fi_data_frame.columns
        )

    def serialize_model_prediction_data(
        self, data, system_columns: SystemColumns, options: PredictionOptions
    ) -> Tuple[str, str]:
        input_data_frame = SplitOrientDataFrame(
            columns=data.columns.tolist(),
            index=data.index.tolist(),
            data=data.to_numpy().tolist()
        )
        input_spec = SplitDataFrameInputSpec(
            split_input_data_frame=input_data_frame,
            system_columns=system_columns
        )
        request = DaemonModePredictRequest(
            input_spec=input_spec, options=options
        )
        # sanitize for serialization is called here to keep json in camel case
        return json.dumps(
            ApiClient().sanitize_for_serialization(request)
        ), 'application/json'


class RemoteModelError(Exception):

    def __init__(self, message):
        self.message = message
