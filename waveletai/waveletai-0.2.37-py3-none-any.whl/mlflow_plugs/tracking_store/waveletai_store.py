# @Time    : 2021/6/5 10:24
# @Author  : Boyang
# @Site    :
# @File    : tracking_store.py
# @Software: PyCharm
import simplejson as json

import waveletai
import uuid
import math

from typing import Any

from mlflow.store.tracking.abstract_store import AbstractStore
from mlflow.entities import (Experiment, RunTag, Metric, Param, Run, RunInfo, RunData,
                             RunStatus, ExperimentTag, LifecycleStage, ViewType, SourceType)
from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import (INVALID_PARAMETER_VALUE, INVALID_STATE, INTERNAL_ERROR,
                                          RESOURCE_DOES_NOT_EXIST)
from mlflow.utils.mlflow_tags import MLFLOW_LOGGED_MODELS
from mlflow.utils.uri import append_to_uri_path
from mlflow.utils.validation import _validate_batch_log_limits, _validate_batch_log_data, \
    _validate_run_id, _validate_metric, _validate_experiment_tag, _validate_tag


class WaveletAIStore(AbstractStore):
    ARTIFACTS_FOLDER_NAME = "artifacts"

    def __init__(self, store_uri: str = None, artifact_uri: str = None):
        self.is_plugin = True
        self.artifact_root_uri = artifact_uri
        super(WaveletAIStore, self).__init__()

    def _hit_to_mlflow_experiment(self, hit: Any) -> Experiment:
        return Experiment(experiment_id=hit.experiment_id, name=hit.name,
                          artifact_location=hit.artifact_location,
                          lifecycle_stage=hit.lifecycle_stage)

    def _hit_to_mlflow_run(self, hit: Any, columns_to_whitelist_key_dict: dict = None) -> Run:
        return Run(run_info=self._hit_to_mlflow_run_info(hit),
                   run_data=self._hit_to_mlflow_run_data(hit, columns_to_whitelist_key_dict))

    def _hit_to_mlflow_run_info(self, hit: Any) -> RunInfo:
        return RunInfo(run_uuid=hit.run_id, run_id=hit.run_id,
                       experiment_id=str(hit.experiment_id),
                       user_id=hit.user_id,
                       status=hit.status,
                       start_time=hit.start_time,
                       end_time=hit.end_time if hasattr(hit, 'end_time') else None,
                       lifecycle_stage=hit.lifecycle_stage if
                       hasattr(hit, 'lifecycle_stage') else None,
                       artifact_uri=hit.artifact_uri
                       if hasattr(hit, 'artifact_uri') else None)

    def _hit_to_mlflow_run_data(self, hit: Any, columns_to_whitelist_key_dict: dict) -> RunData:
        metrics = [self._hit_to_mlflow_metric(m) for m in
                   (hit.latest_metrics if hasattr(hit, 'latest_metrics') else [])
                   if (columns_to_whitelist_key_dict is None or
                       m.key in columns_to_whitelist_key_dict["metrics"])]
        params = [self._hit_to_mlflow_param(p) for p in
                  (hit.params if hasattr(hit, 'params') else [])
                  if (columns_to_whitelist_key_dict is None or
                      p.key in columns_to_whitelist_key_dict["params"])]
        tags = [self._hit_to_mlflow_tag(t) for t in
                (hit.tags if hasattr(hit, 'tags') else [])
                if (columns_to_whitelist_key_dict is None or
                    t.key in columns_to_whitelist_key_dict["tags"])]
        return RunData(metrics=metrics, params=params, tags=tags)

    def _hit_to_mlflow_metric(self, hit: Any) -> Metric:
        return Metric(key=hit.key,
                      value=hit.value if not (hasattr(hit, 'is_nan')
                                              and hit.is_nan) else float("nan"),
                      timestamp=hit.timestamp, step=hit.step)

    def _hit_to_mlflow_param(self, hit: Any) -> Param:
        return Param(key=hit.key, value=hit.value)

    def _hit_to_mlflow_tag(self, hit: Any) -> RunTag:
        return RunTag(key=hit.key, value=hit.value)

    def list_experiments(self, view_type=ViewType.ACTIVE_ONLY):
        raise NotImplemented

    def create_experiment(self, name, artifact_location):
        if name is None or name == '':
            raise MlflowException('Invalid experiment name', INVALID_PARAMETER_VALUE)

        return waveletai.create_mlflow_experiment(name, artifact_location)

    def get_experiment(self, experiment_id):
        wai_experiment = waveletai.get_experiment_by_mlflow_experiment(experiment_id)
        experiment = wai_experiment.mlflow_experiment
        return experiment.to_mlflow_entity()

    def delete_experiment(self, experiment_id):
        pass

    def restore_experiment(self, experiment_id):
        pass

    def rename_experiment(self, experiment_id, new_name):
        pass

    def get_run(self, run_id):
        wai_experiment = waveletai.get_experiment_by_mlflow_run(run_id)
        run = wai_experiment.get_mlflow_run(run_id)

        return run.to_mlflow_entity()

    def update_run_info(self, run_id, run_status, end_time):
        wai_experiment = waveletai.get_experiment_by_mlflow_run(run_id)
        run = wai_experiment.get_mlflow_run(run_id)
        self._check_run_is_active(run)
        run.status = RunStatus.to_string(run_status)
        run.end_time = end_time
        run = wai_experiment.update_run_info(run)
        return run.to_mlflow_entity().info

    def create_run(self, experiment_id, user_id, start_time, tags):
        wai_experiment = waveletai.get_experiment_by_mlflow_experiment(experiment_id)
        experiment = wai_experiment.mlflow_experiment
        self._check_experiment_is_active(experiment)

        run_id = uuid.uuid4().hex
        artifact_location = append_to_uri_path(experiment.artifact_location, run_id,
                                               WaveletAIStore.ARTIFACTS_FOLDER_NAME)

        run = wai_experiment.create_mlflow_run(name="", artifact_uri=artifact_location, run_uuid=run_id,
                                               experiment_id=experiment_id,
                                               source_type=SourceType.to_string(SourceType.UNKNOWN),
                                               source_name="", entry_point_name="",
                                               user_id=user_id, status=RunStatus.to_string(RunStatus.RUNNING),
                                               start_time=start_time, end_time=None,
                                               source_version="", lifecycle_stage=LifecycleStage.ACTIVE)
        wai_experiment.set_tags(run_id, tags)

        return run.to_mlflow_entity()

    def delete_run(self, run_id):
        pass

    def restore_run(self, run_id):
        pass

    def get_metric_history(self, run_id, metric_key):
        pass

    def _search_runs(self, experiment_ids, filter_string, run_view_type, max_results, order_by, page_token):
        pass

    def log_param(self, run_id, param):
        wai_experiment = waveletai.get_experiment_by_mlflow_run(run_id)
        run = wai_experiment.get_mlflow_run(run_id)
        self._check_run_is_active(run)
        wai_experiment.log_params(run_id, [param])

    def log_metric(self, run_id, metric):
        _validate_metric(metric.key, metric.value, metric.timestamp, metric.step)
        is_nan = math.isnan(metric.value)
        if is_nan:
            value = 0
        elif math.isinf(metric.value):
            #  NB: Sql can not represent Infs = > We replace +/- Inf with max/min 64b float value
            value = 1.7976931348623157e308 if metric.value > 0 else -1.7976931348623157e308
        else:
            value = metric.value

        wai_experiment = waveletai.get_experiment_by_mlflow_run(run_id)
        run = wai_experiment.get_mlflow_run(run_id)
        self._check_run_is_active(run)
        _metric = {
            'key': metric.key,
            'value': value,
            'timestamp': metric.timestamp,
            'step': metric.step,
            'is_nan': is_nan
        }
        wai_experiment.log_metrics(run_id, [_metric])
        # _update_latest_metric_if_necessary 注意: 更新最新的metric操作放在服务端自动判断了

    def set_tag(self, run_id, tag):
        _validate_tag(tag.key, tag.value)
        wai_experiment = waveletai.get_experiment_by_mlflow_run(run_id)
        run = wai_experiment.get_mlflow_run(run_id)
        self._check_run_is_active(run)
        wai_experiment.set_tags(run_id, [tag])

    def _log_params(self, run_id, params):
        wai_experiment = waveletai.get_experiment_by_mlflow_run(run_id)
        run = wai_experiment.get_mlflow_run(run_id)
        self._check_run_is_active(run)
        wai_experiment.log_params(run_id, params)

    def _log_metrics(self, run_id, metrics):
        _metrics = []
        for metric in metrics:
            _validate_metric(metric.key, metric.value, metric.timestamp, metric.step)
            is_nan = math.isnan(metric.value)
            if is_nan:
                value = 0
            elif math.isinf(metric.value):
                #  NB: Sql can not represent Infs = > We replace +/- Inf with max/min 64b float value
                value = 1.7976931348623157e308 if metric.value > 0 else -1.7976931348623157e308
            else:
                value = metric.value

            _metrics.append({
                'key': metric.key,
                'value': value,
                'timestamp': metric.timestamp,
                'step': metric.step,
                'is_nan': is_nan
            })
        wai_experiment = waveletai.get_experiment_by_mlflow_run(run_id)
        run = wai_experiment.get_mlflow_run(run_id)
        self._check_run_is_active(run)
        wai_experiment.log_metrics(run_id, _metrics)

    def _set_tags(self, run_id, tags):
        for tag in tags:
            _validate_tag(tag.key, tag.value)
        wai_experiment = waveletai.get_experiment_by_mlflow_run(run_id)
        run = wai_experiment.get_mlflow_run(run_id)
        self._check_run_is_active(run)
        wai_experiment.set_tags(run_id, tags)

    def log_batch(self, run_id, metrics, params, tags):
        _validate_run_id(run_id)
        _validate_batch_log_data(metrics, params, tags)
        _validate_batch_log_limits(metrics, params, tags)
        wai_experiment = waveletai.get_experiment_by_mlflow_run(run_id)
        run = wai_experiment.get_mlflow_run(run_id)
        self._check_run_is_active(run)
        try:
            self._log_params(run_id, params)
            self._log_metrics(run_id, metrics)
            self._set_tags(run_id, tags)
        except MlflowException as e:
            raise e
        except Exception as e:
            raise MlflowException(e, INTERNAL_ERROR)

    def record_logged_model(self, run_id, mlflow_model):
        from mlflow.models import Model

        if not isinstance(mlflow_model, Model):
            raise TypeError(
                "Argument 'mlflow_model' should be mlflow.models.Model, got '{}'".format(
                    type(mlflow_model)
                )
            )
        model_dict = mlflow_model.to_dict()
        wai_experiment = waveletai.get_experiment_by_mlflow_run(run_id)
        run = wai_experiment.get_mlflow_run(run_id)
        self._check_run_is_active(run)
        previous_tag = [t for t in run.tags if t.key == MLFLOW_LOGGED_MODELS]
        if previous_tag:
            value = json.dumps(json.loads(previous_tag[0].value) + [model_dict])
        else:
            value = json.dumps([model_dict])
        _validate_tag(MLFLOW_LOGGED_MODELS, value)
        wai_experiment.record_logged_model(key=MLFLOW_LOGGED_MODELS, value=value, run_id=run_id)

    def _check_experiment_is_active(self, experiment):
        if experiment.lifecycle_stage != LifecycleStage.ACTIVE:
            raise MlflowException("The experiment {} must be in the 'active' state. "
                                  "Current state is {}."
                                  .format(experiment.experiment_id, experiment.lifecycle_stage),
                                  INVALID_PARAMETER_VALUE)

    def _check_run_is_active(self, run):
        if run.lifecycle_stage != LifecycleStage.ACTIVE:
            raise MlflowException("The run {} must be in the 'active' state. Current state is {}."
                                  .format(run.run_uuid, run.lifecycle_stage),
                                  INVALID_PARAMETER_VALUE)
