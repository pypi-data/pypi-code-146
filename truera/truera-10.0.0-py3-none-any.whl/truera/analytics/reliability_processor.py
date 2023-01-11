from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from sklearn.linear_model import LogisticRegression

from truera.utils.truera_status import TruEraInvalidArgumentError

if TYPE_CHECKING:
    from truera.aiq.intelligence_server_impl import IntelligenceServiceServicer

from truera.analytics.pending_operations_or import PendingOperationsOr
from truera.authn.usercontext import RequestContext
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    _RELIABILITYREQUEST_RELIABILITYMETRICTYPE  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    ModelId  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    ModelInputSpec  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    ReliabilityRequest  # pylint: disable=no-name-in-module
from truera.protobuf.public.common_pb2 import \
    FeatureInfluenceOptions  # pylint: disable=no-name-in-module
from truera.protobuf.public.qoi_pb2 import \
    QuantityOfInterest  # pylint: disable=no-name-in-module
from truera.public import feature_influence_constants as fi_constants


class ReliabilityProcessor(object):
    """Reliability processor for models and datasets.
    """

    def __init__(
        self, request_context: RequestContext, project_id: str,
        intelligence_service_servicer: IntelligenceServiceServicer
    ):
        self.request_context = request_context
        self.project_id = project_id
        self.intelligence_service_servicer = intelligence_service_servicer

    def _calibration_buckets(
        self,
        y_true: np.ndarray,
        y_score: np.ndarray,
        min_per_bucket: int = 500,
        min_per_class_per_bucket: int = 0
    ):
        # TODO(davidkurokawa): Try to vectorize this if possible.
        sorted_idxs = np.argsort(y_score)
        count_0 = [0]
        count_1 = [0]
        sum_score = [0]
        for idx in sorted_idxs:
            if y_true[idx] > 0:
                count_1[-1] += 1
            else:
                count_0[-1] += 1
            # TODO(davidkurokawa): Might want to add these using Kahan's summation algorithm to avoid precision errors.
            sum_score[-1] += y_score[idx]
            if count_0[-1] + count_1[-1] >= min_per_bucket and count_0[
                -1] >= min_per_class_per_bucket and count_1[
                    -1] >= min_per_class_per_bucket:
                count_0.append(0)
                count_1.append(0)
                sum_score.append(0)
        if len(sum_score) > 1:
            idx = len(sum_score) - 2
            count_0[idx] += count_0.pop()
            count_1[idx] += count_1.pop()
            sum_score[idx] += sum_score.pop()
        ret_true = np.zeros(len(sum_score))
        ret_pred = np.zeros(len(sum_score))
        for idx in range(len(sum_score)):
            denom = count_0[idx] + count_1[idx]
            ret_true[idx] = count_1[idx] / denom
            ret_pred[idx] = sum_score[idx] / denom
        return ret_true, ret_pred

    def compute_calibration_curve(
        self, model_id: str, split_id: str
    ) -> PendingOperationsOr:
        input_spec = ModelInputSpec(
            split_id=split_id, all_available_inputs=True
        )
        y_score_or_operations = self.intelligence_service_servicer.artifact_loader.GetModelPredictions(
            self.request_context,
            self.project_id,
            model_id,
            input_spec=input_spec,
            qoi=QuantityOfInterest.PROBITS_SCORE
        )

        y_calibrated_or_operations = self._compute_reliability_calibration_metric(
            model_id, input_spec, fi_constants.PREDICTOR_SCORE_TYPE_PROBITS
        )
        if y_score_or_operations.is_operations or y_calibrated_or_operations.is_operations:
            return PendingOperationsOr.from_pending_operations(
                [y_score_or_operations, y_calibrated_or_operations]
            )
        y_score = y_score_or_operations.value.to_numpy()
        y_calibrated = y_calibrated_or_operations.value
        y_true = self.intelligence_service_servicer.artifact_loader.GetLabelsForModel(
            self.request_context,
            self.project_id,
            model_id,
            input_spec=input_spec
        ).value.iloc[:, 0]
        prob_score_true, prob_score_pred = self._calibration_buckets(
            y_true, y_score
        )
        prob_calibrated_true, prob_calibrated_pred = self._calibration_buckets(
            y_true, y_calibrated
        )
        return PendingOperationsOr.from_value(
            (
                prob_score_pred, prob_score_true, prob_calibrated_pred,
                prob_calibrated_true
            )
        )

    def compute_reliability(
        self, model_id: str, input_spec: ModelInputSpec,
        reliability_metric_type: _RELIABILITYREQUEST_RELIABILITYMETRICTYPE,
        quantity_of_interest: QuantityOfInterest
    ):
        # pylint: disable=no-member
        reliability_metric_type_to_fn = {
            ReliabilityRequest.ReliabilityMetricType.CALIBRATION:
                self._compute_reliability_calibration_metric,
            ReliabilityRequest.ReliabilityMetricType.QII_L2:
                self._compute_reliability_qii_l2_metric,
            ReliabilityRequest.ReliabilityMetricType.QII_CLIPPING:
                self._compute_reliability_qii_clipping_metric,
        }
        if reliability_metric_type not in reliability_metric_type_to_fn:
            raise Exception(
                'Unknown reliability metric type: {}!'.
                format(reliability_metric_type)
            )
        if not input_spec.split_id:
            input_spec.split_id = self.intelligence_service_servicer.artifact_metadata_client.get_default_base_split_id_for_model(
                self.request_context, self.project_id, model_id
            )

        return reliability_metric_type_to_fn[reliability_metric_type](
            model_id, input_spec, quantity_of_interest
        )

    def _compute_reliability_calibration_metric(
        self,
        model_id: str,
        input_spec: ModelInputSpec,
        quantity_of_interest: QuantityOfInterest,
    ) -> PendingOperationsOr:
        if self.intelligence_service_servicer.artifact_metadata_client.is_regression_model(
            self.request_context, self.project_id, model_id
        ):
            return None

        input_spec_train = ModelInputSpec(
            split_id=input_spec.split_id, all_available_inputs=True
        )
        input_spec_train.filter_expression.CopyFrom(
            self.intelligence_service_servicer.
            _retrieve_appended_requirements_filter_expression(
                input_spec_train,
                filter_to_available_labels=self.intelligence_service_servicer.
                SILENTLY_USE_ONLY_LABELLED_DATA,
                filter_to_non_null_predictions=self.
                intelligence_service_servicer.SILENTLY_USE_NON_NAN_PREDICTIONS,
                filter_to_non_inf_predictions=self.
                intelligence_service_servicer.SILENTLY_USE_NON_INF_PREDICTIONS,
                qoi=QuantityOfInterest.PROBITS_SCORE
            )
        )

        labels_df_or_operation = self.intelligence_service_servicer.artifact_loader.GetLabelsForModel(
            self.request_context,
            self.project_id,
            model_id,
            input_spec=input_spec_train
        )
        if labels_df_or_operation is None:
            return None

        scores_or_operations = self.intelligence_service_servicer.artifact_loader.GetModelPredictions(
            self.request_context,
            self.project_id,
            model_id,
            input_spec_train,
            qoi=QuantityOfInterest.PROBITS_SCORE
        )
        res_or_operations = self.intelligence_service_servicer.artifact_loader.GetModelPredictions(
            self.request_context,
            self.project_id,
            model_id,
            input_spec,
            qoi=QuantityOfInterest.PROBITS_SCORE
        )

        preds_filter_or_operations = self.intelligence_service_servicer._retrieve_appended_requirements_filter(
            input_spec,
            self.request_context,
            ModelId(project_id=self.project_id, model_id=model_id),
            filter_to_non_null_predictions=self.intelligence_service_servicer.
            SILENTLY_USE_NON_NAN_PREDICTIONS,
            filter_to_non_inf_predictions=self.intelligence_service_servicer.
            SILENTLY_USE_NON_INF_PREDICTIONS,
            qoi=QuantityOfInterest.PROBITS_SCORE
        )

        pending_operations = [
            curr for curr in [
                scores_or_operations, res_or_operations,
                preds_filter_or_operations, labels_df_or_operation
            ] if curr is not None and curr.is_operations
        ]
        if pending_operations:
            return PendingOperationsOr.from_pending_operations(
                pending_operations
            )
        scores = scores_or_operations.value
        labels = labels_df_or_operation.value
        preds_filter = preds_filter_or_operations.value
        if len(scores) == 0:
            raise TruEraInvalidArgumentError(
                "Cannot compute reliability calibration metric! No available predictions or labels to train calibration."
            )
        labels = labels.to_numpy().reshape((-1, 1))
        scores = scores.to_numpy().reshape((-1, 1))
        plattScaler = LogisticRegression(solver="lbfgs")
        plattScaler.fit(scores, labels)
        res = res_or_operations.value.to_numpy().reshape((-1, 1))
        ret = np.empty(len(res))
        ret[:] = np.nan
        ret[preds_filter] = plattScaler.predict_proba(res[preds_filter])[:, 1]
        # TODO(davidkurokawa): Convert back to the provided score_type instead of just logit and probability.
        if quantity_of_interest == QuantityOfInterest.LOGITS_SCORE:
            ret = np.log(ret / (1 - ret))
        return PendingOperationsOr.from_value(ret)

    def _compute_reliability_qii_l2_metric(
        self, model_id: str, input_spec: ModelInputSpec,
        quantity_of_interest: QuantityOfInterest
    ) -> PendingOperationsOr:
        # TODO(davidkurokawa): Currently this computes the influences from [0, stop).
        input_spec_modified = ModelInputSpec()
        input_spec_modified.CopyFrom(input_spec)
        if input_spec.dataset_index_range.start != 0:
            input_spec_modified.dataset_index_range.start = 0
        qiis_or_operations = self.intelligence_service_servicer.artifact_loader.GetModelInfluences(
            self.request_context, self.project_id, model_id,
            input_spec_modified,
            FeatureInfluenceOptions(quantity_of_interest=quantity_of_interest)
        )
        if qiis_or_operations.is_operations:
            return qiis_or_operations
        qiis = qiis_or_operations.value.values
        # TODO(davidkurokawa): c = 0.05 is just a placeholder for now.
        return PendingOperationsOr.from_value(
            0.05 * np.linalg.
            norm(qiis[input_spec.dataset_index_range.start:], 2, axis=1)
        )

    def _compute_reliability_qii_clipping_metric(
        self, model_id: str, input_spec: ModelInputSpec,
        quantity_of_interest: QuantityOfInterest
    ) -> PendingOperationsOr[np.ndarray]:
        scores_or_operations = self.intelligence_service_servicer.artifact_loader.GetModelPredictions(
            self.request_context,
            self.project_id,
            model_id,
            input_spec,
            qoi=quantity_of_interest
        )
        input_spec_infs = ModelInputSpec()
        input_spec_infs.CopyFrom(input_spec)
        if input_spec_infs.dataset_index_range.start != 0:
            input_spec_infs.dataset_index_range.start = 0
        start_stop_qiis_or_operation = self.intelligence_service_servicer.artifact_loader.GetModelInfluences(
            self.request_context, self.project_id, model_id, input_spec_infs,
            FeatureInfluenceOptions(quantity_of_interest=quantity_of_interest)
        )
        baseline_qiis_or_operation = self.intelligence_service_servicer.artifact_loader.GetModelInfluences(
            self.request_context, self.project_id, model_id,
            ModelInputSpec(
                split_id=input_spec.split_id, standard_bulk_inputs=True
            ),
            FeatureInfluenceOptions(quantity_of_interest=quantity_of_interest)
        )

        all_ops = [
            scores_or_operations, start_stop_qiis_or_operation,
            baseline_qiis_or_operation
        ]
        if PendingOperationsOr.is_any_pending(all_ops):
            return PendingOperationsOr.from_pending_operations(all_ops)

        scores = scores_or_operations.value.to_numpy()
        baseline_qiis = baseline_qiis_or_operation.value
        start_stop_qiis = start_stop_qiis_or_operation.value.iloc[
            input_spec.dataset_index_range.start:]
        lower_bounds = np.quantile(baseline_qiis, 0.01, axis=0)
        upper_bounds = np.quantile(baseline_qiis, 0.99, axis=0)
        ret = []
        for i in range(len(start_stop_qiis)):
            offset = np.sum(start_stop_qiis.iloc[i, :]) - scores[i]
            clipped = start_stop_qiis.iloc[i, :]
            clipped = np.minimum(clipped, upper_bounds)
            clipped = np.maximum(clipped, lower_bounds)
            ret += [np.sum(clipped) - offset]
        return PendingOperationsOr.from_value(np.array(ret))
