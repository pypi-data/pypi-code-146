from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import (
    Generic, Mapping, Optional, Sequence, Set, Tuple, TYPE_CHECKING, TypeVar,
    Union
)

import numpy as np
import pandas as pd

from truera.artifactrepo.utils.filter_utils import \
    parse_expression_to_filter_proto
from truera.client.client_utils import validate_feature_names
from truera.client.errors import NotFoundError
from truera.client.intelligence.bias import BiasResult
from truera.client.intelligence.segment import Segment
from truera.client.intelligence.segment import SegmentGroup
from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.aiq_http_communicator import \
    HttpAiqCommunicator
from truera.client.services.artifact_interaction_client import \
    ArtifactInteractionClient
from truera.client.services.artifactrepo_client import ArtifactMetaFetchMode
from truera.client.services.mrc_client import MrcClient
from truera.client.services.pending_operation_client import \
    PendingOperationClient
from truera.partial_dependence_plot.partial_dependence_representation_converter import \
    convert_PartialDependencePlotResponse_to_tuple
from truera.protobuf.public.aiq import accuracy_pb2 as acc_pb
from truera.protobuf.public.aiq import distance_pb2
from truera.protobuf.public.aiq import intelligence_service_pb2 as is_pb
# pylint: disable=no-name-in-module
from truera.protobuf.public.artifactrepo_pb2 import PingRequest
from truera.protobuf.public.data.filter_pb2 import FilterExpression
from truera.protobuf.public.data.filter_pb2 import FilterExpressionOperator
from truera.protobuf.public.data.filter_pb2 import FilterLeaf
from truera.protobuf.public.data.segment_pb2 import InterestingSegment
from truera.protobuf.public.qoi_pb2 import ExplanationAlgorithmType
from truera.protobuf.public.qoi_pb2 import QuantityOfInterest
# pylint: enable=no-name-in-module
from truera.utils import aiq_proto
from truera.utils import filter_constants
from truera.utils.data_utils import float_table_to_df
from truera.utils.data_utils import merge_split_data_responses
from truera.utils.data_utils import string_table_to_df
from truera.utils.data_utils import value_table_to_df
from truera.utils.data_utils import value_table_to_df_or_series
from truera.utils.filter_utils import FilterProcessor

if TYPE_CHECKING:
    # pylint: disable=no-name-in-module
    from truera.protobuf.public.data.segment_pb2 import Segment as _PBSegment

DISTANCE_NAME_TO_PB = {
    name: enum_value for name, enum_value in distance_pb2.DistanceType.items()
}
DISTANCE_NAME_TO_PB.pop('UNKNOWN_DISTANCE_TYPE')
DISTANCE_PB_TO_NAME = {DISTANCE_NAME_TO_PB[i]: i for i in DISTANCE_NAME_TO_PB}

T = TypeVar('T')

_DEFAULT_COMPARISON_SEGMENT_NAME = "Comparison Segment"


@dataclass
class AiqClientResponse(Generic[T]):

    def __init__(self, response: T, pending_operations: Sequence[str]):
        self.response = response
        self.pending_operations = pending_operations


@dataclass
class ModelOutputSpec:

    def __init__(
        self,
        model_id: str,
        data_split_id: str,
        segment: Optional[Segment] = None
    ):
        self.model_id = model_id
        self.data_split_id = data_split_id
        self.segment = segment


@dataclass
class ModelBiasRequest:

    def __init__(
        self,
        model_id: str,
        data_split_id: str,
        bias_types: Sequence[str],
        protected_segment: Segment,
        comparison_segment: Optional[Segment] = None,
        classification_threshold: Optional[float] = None,
        classification_threshold_score_type: Optional[str] = None,
    ):
        self.model_id = model_id
        self.data_split_id = data_split_id
        self.bias_types = bias_types
        self.protected_segment = protected_segment
        self.comparison_segment = comparison_segment
        self.classification_threshold = classification_threshold
        self.classification_threshold_score_type = classification_threshold_score_type


def _set_input_spec_from_segment(
    input_spec: is_pb.ModelInputSpec, segment: Segment
):
    if segment:
        input_spec.filter_expression.CopyFrom(
            segment._segment_proto.filter_expression
        )


def _set_df_index_to_point_index(
    df: Union[pd.DataFrame, pd.Series], start: Optional[int]
):
    if start is not None and start > 0:
        df.index = list(range(start, start + len(df)))


class AiqClient(PendingOperationClient):

    def __init__(
        self,
        connection_string: str = None,
        aiq_connection_string: str = None,
        mrc_connection_string: str = None,
        auth_details: AuthDetails = None,
        logger=None,
        use_http: bool = False,
        *,
        verify_cert: Union[bool, str] = True,
        artifact_interaction_client: Optional[ArtifactInteractionClient] = None
    ):
        if (aiq_connection_string is None) != (mrc_connection_string is None):
            raise ValueError(
                "Must supply both or neither of aiq_connection_string, mrc_connection_string!"
            )
        if (aiq_connection_string is None) == (connection_string is None):
            raise ValueError(
                "Must supply one of connection_string and (aiq_connection_string, mrc_connection_string)!"
            )
        if (not use_http):
            from truera.client.private.communicator.aiq_grpc_communicator import \
                GrpcAiqCommunicator

        self.logger = logger or logging.getLogger(__name__)
        self.auth_details = auth_details
        self.connection_string = aiq_connection_string or connection_string
        self.communicator = HttpAiqCommunicator(
            self.connection_string,
            auth_details,
            logger,
            verify_cert=verify_cert
        ) if use_http else GrpcAiqCommunicator(
            self.connection_string, auth_details, logger
        )
        if mrc_connection_string is None:
            mrc_connection_string = connection_string.rstrip("/")
            mrc_connection_string = f"{mrc_connection_string}/api/mrc"
        self.mrc_client = MrcClient(
            mrc_connection_string,
            auth_details,
            logger,
            verify_cert=verify_cert
        )
        # TODO: AZ#6664 (Remove dependency to artifact_interaction_client in aiq_client)
        self.artifact_interaction_client = artifact_interaction_client

    def ping(self, test_string: str) -> str:
        return self.communicator.ping(
            PingRequest(test_string=test_string)
        ).test_string_back

    def get_mrc_client(self) -> MrcClient:
        return self.mrc_client

    def get_split_metadata(
        self, project_id: str, data_split_id: str, data_collection_id: str
    ) -> is_pb.SplitMetaData:
        response = self._get_split_data(
            project_id, data_collection_id, data_split_id, 0, 1
        )
        return response.split_metadata

    def get_xs(
        self,
        project_id: str,
        data_split_id: str,
        data_collection_id: str = None,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        pre_processed_data_required: bool = True,
        extra_data: bool = False,
        get_post_processed_data: bool = False,
        system_data: bool = False,
        segment: Optional[Segment] = None,
        model_id: Optional[str] = None
    ) -> AiqClientResponse[pd.DataFrame]:
        response = self._get_split_data(
            project_id,
            data_collection_id,
            data_split_id,
            start,
            stop,
            pre_processed_data_required=pre_processed_data_required,
            extra_data=extra_data,
            system_data=system_data,
            get_post_processed_data=get_post_processed_data,
            segment=segment,
            model_id=model_id,
            wait=True
        )
        df = value_table_to_df(
            response.split_data,
            response.split_metadata.ordered_column_names.values
        )
        if response.split_extra_data:
            extra_data_df = value_table_to_df(
                response.split_extra_data,
                response.split_metadata.extra_data_ordered_column_names.values
            )
            # No guarantee that timestamps from pre + extra agree, so dangerous to join on both ID and timestamp.
            # Instead we drop timestamp from extra data and assume pre is what users want.
            timestamp_col_name = response.split_metadata.system_columns.timestamp_column_name
            if timestamp_col_name and timestamp_col_name in extra_data_df:
                extra_data_df.drop(
                    [timestamp_col_name], axis="columns", inplace=True
                )
            df = df.join(extra_data_df)
        if not response.split_data.row_labels:
            _set_df_index_to_point_index(df, start)
        return AiqClientResponse(
            response=df,
            pending_operations=response.pending_operations.
            waiting_on_operation_ids
        )

    def get_ys(
        self,
        project_id: str,
        data_split_id: str,
        data_collection_id: str = None,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False,
        segment: Optional[Segment] = None,
        model_id: Optional[str] = None
    ) -> AiqClientResponse[Union[pd.DataFrame, pd.Series]]:
        response = self._get_split_data(
            project_id,
            data_collection_id,
            data_split_id,
            start,
            stop,
            include_labels=True,
            exclude_feature_values=True,
            system_data=system_data,
            segment=segment,
            model_id=model_id,
            wait=True
        )
        if not response.split_labels.column_value_map:
            raise NotFoundError("Labels were not found for this data split.")
        labels = value_table_to_df_or_series(response.split_labels)
        if not response.split_labels.row_labels:
            _set_df_index_to_point_index(labels, start)
        return AiqClientResponse(
            response=labels,
            pending_operations=response.pending_operations.
            waiting_on_operation_ids
        )

    def get_ys_pred(
        self,
        project_id: str,
        model_id: str,
        data_split_id: str,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        segment: Optional[Segment] = None,
        include_system_data: bool = False,
        include_all_points: bool = False,
        score_type: Optional[QuantityOfInterest] = None,
        wait: bool = True
    ) -> AiqClientResponse[Union[pd.DataFrame, pd.Series]]:
        req = is_pb.ModelPredictionsRequest()
        req.model_id.model_id = model_id
        req.model_id.project_id = project_id
        req.input_spec.split_id = data_split_id
        if include_all_points:
            req.input_spec.all_available_inputs = True
        else:
            req.input_spec.dataset_index_range.start = start
            if stop is not None:
                req.input_spec.dataset_index_range.stop = stop  # pylint: disable=protobuf-type-error

        if score_type is not None:
            req.prediction_options.score_type = score_type  # pylint: disable=protobuf-type-error

        _set_input_spec_from_segment(req.input_spec, segment)
        req.include_system_data = include_system_data
        request_func = lambda: self.communicator.get_model_predictions(req)
        if wait:
            response = self._wait_till_complete(
                request_func, project_id, timeout=None
            )
        else:
            response = request_func()

        if response.HasField("pending_operations"):
            return AiqClientResponse(
                response=None,
                pending_operations=response.pending_operations.
                waiting_on_operation_ids
            )
        preds = value_table_to_df_or_series(response.predictions)
        if include_system_data and response.system_data:
            system_data_df = string_table_to_df(response.system_data)
            preds = pd.DataFrame(data=preds).join(system_data_df)
        if not response.predictions.row_labels:
            _set_df_index_to_point_index(preds, start)
        return AiqClientResponse(
            response=preds,
            pending_operations=response.pending_operations.
            waiting_on_operation_ids
        )

    def get_feature_influences(
        self,
        project_id: str,
        model_id: str,
        data_split_id: str,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        score_type: Optional[str] = None,
        segment: Optional[Segment] = None,
        include_system_data: bool = False,
        background_split_id: Optional[str] = None,
        wait: bool = True,
        return_algorithm_type: bool = False
    ) -> AiqClientResponse[Union[Optional[pd.DataFrame], Tuple[
        Optional[pd.DataFrame], ExplanationAlgorithmType]]]:
        response = self._get_feature_influences(
            project_id,
            model_id,
            data_split_id,
            start=start,
            stop=stop,
            score_type=score_type,
            segment=segment,
            include_system_data=include_system_data,
            background_split_id=background_split_id,
            wait=wait
        )
        infs = None
        if wait or (response.influences
                    is not None) or (response.influences.column_value_map):
            infs = float_table_to_df(
                response.influences, response.ordered_column_names.values
            )
            if include_system_data and response.system_data:
                system_data_df = string_table_to_df(response.system_data)
                infs = infs.join(system_data_df)
            if not response.influences.row_labels:
                _set_df_index_to_point_index(infs, start)

        response_val = infs
        if return_algorithm_type:
            response_val = (infs, response.explanation_algorithm_type)
        return AiqClientResponse(
            response=response_val,
            pending_operations=response.pending_operations.
            waiting_on_operation_ids
        )

    def _get_sorted_features(
        self,
        project_id: str,
        model_id: str,
        data_split_id: str,
        segment: Optional[Segment] = None,
        sort_method: is_pb.FeatureSortMethod = is_pb.FeatureSortMethod.
        ABSOLUTE_VALUE_SUM,
        wait: bool = True
    ) -> AiqClientResponse[Optional[pd.DataFrame]]:
        req = is_pb.ModelDataRequest()
        req.model_id.project_id = project_id
        req.model_id.model_id = model_id
        _set_input_spec_from_segment(req.input_spec, segment)
        req.input_spec.split_id = data_split_id
        req.input_spec.standard_bulk_inputs = True
        request_entry = is_pb.ModelDataRequestEntry()
        request_entry.type = is_pb.ModelDataRequestType.FEATURE_SORT
        request_entry.options.feature_sort_options.sort_methods.append(
            sort_method
        )
        req.request_entry.append(request_entry)
        request_func = lambda: self.communicator.get_model_data(req).entry[0]
        if wait:
            res = self._wait_till_complete(
                request_func, project_id, timeout=None
            )
        else:
            res = request_func()
        if res is None:
            df = None
        else:
            df = float_table_to_df(res.float_table)
        return AiqClientResponse(
            response=df,
            pending_operations=res.pending_operations.waiting_on_operation_ids
        )

    def get_global_feature_importances(
        self,
        project_id: str,
        model_id: str,
        data_split_id: str,
        score_type: Optional[str] = None,
        segment: Optional[Segment] = None,
        background_split_id: Optional[str] = None,
        wait: bool = True
    ) -> AiqClientResponse[Optional[pd.DataFrame]]:
        response = self._get_feature_influences(
            project_id,
            model_id,
            data_split_id,
            aggregate_to_global=True,
            score_type=score_type,
            segment=segment,
            background_split_id=background_split_id,
            wait=wait
        )
        df = None
        if wait or (response.influences
                    is not None) or (response.influences.column_value_map):
            df = float_table_to_df(
                response.influences, response.ordered_column_names.values
            )
        return AiqClientResponse(
            response=df,
            pending_operations=response.pending_operations.
            waiting_on_operation_ids
        )

    def _get_feature_influences(
        self,
        project_id: str,
        model_id: str,
        data_split_id: str,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        score_type: Optional[str] = None,
        segment: Optional[Segment] = None,
        aggregate_to_global: bool = False,
        include_system_data: bool = False,
        background_split_id: Optional[str] = None,
        wait: bool = True
    ) -> is_pb.ModelInfluencesResponse:
        req = is_pb.ModelInfluencesRequest()
        req.model_id.model_id = model_id
        req.model_id.project_id = project_id
        if score_type is not None:
            req.feature_influence_options.quantity_of_interest = aiq_proto.GetQuantityOfInterestFromScoreType(
                score_type
            )

        if background_split_id is not None:
            req.feature_influence_options.background_data_split_info.id = background_split_id
            req.feature_influence_options.background_data_split_info.all = True

        req.input_spec.dataset_index_range.start = start
        if stop is not None:
            req.input_spec.dataset_index_range.stop = stop  # pylint: disable=protobuf-type-error

        req.input_spec.split_id = data_split_id
        req.aggregate_to_global = aggregate_to_global
        req.include_system_data = include_system_data
        _set_input_spec_from_segment(req.input_spec, segment)
        request_func = lambda: self.communicator.get_model_influences(req)
        if wait:
            return self._wait_till_complete(
                request_func, project_id, timeout=None
            )
        else:
            return request_func()

    def get_partial_dependencies(
        self,
        project_id: str,
        model_id: str,
        data_split_id: str,
        segment: Optional[Segment] = None,
        wait: bool = True,
    ) -> AiqClientResponse[Tuple[Sequence[str], Mapping[str, Sequence], Mapping[
        str, Sequence]]]:
        if segment:
            raise NotImplementedError("PDPs are unsupported for segments!")
        request = is_pb.PartialDependencePlotRequest()
        request.model_id.project_id = project_id
        request.model_id.model_id = model_id
        request.background_data_split_info.id = data_split_id
        request.background_data_split_info.all = True
        request_func = lambda: self.communicator.get_partial_dependence_plot(
            request
        )
        if wait:
            res = self._wait_till_complete(
                request_func, project_id, timeout=None
            )
        else:
            res = request_func()
            if res.pending_operations and res.pending_operations.waiting_on_operation_ids:
                return AiqClientResponse(
                    None, res.pending_operations.waiting_on_operation_ids
                )
        return AiqClientResponse(
            response=convert_PartialDependencePlotResponse_to_tuple(res),
            pending_operations=res.pending_operations.waiting_on_operation_ids
        )

    def _get_segmentations(
        self,
        project_id: str,
        include_unaccepted_interesting_segments: bool = False,
    ) -> is_pb.GetManualSegmentationResponse:
        request = is_pb.GetManualSegmentationRequest()
        request.project_id = project_id
        request.include_unaccepted_interesting_segments = include_unaccepted_interesting_segments
        return self.communicator.get_segmentations(request)

    def get_wrapped_segmentations(
        self,
        project_id: str,
        convert_model_ids_to_model_names: bool = False,
        include_unaccepted_interesting_segments: bool = False,
        segmentation_ids: Optional[Set[str]] = None
    ) -> AiqClientResponse[Mapping[str, SegmentGroup]]:
        resp = self._get_segmentations(
            project_id, include_unaccepted_interesting_segments
        )
        ret = {}
        for segmentation in resp.segmentations:
            if (segmentation_ids
                is not None) and (segmentation.id not in segmentation_ids):
                continue
            if convert_model_ids_to_model_names:
                for segment in segmentation.segments:
                    self._replace_model_ids_with_model_names_in_filter(
                        project_id, segment.filter_expression
                    )
            project_id = segmentation.project_id
            segments = {
                segment.name: Segment(segment.name, project_id, segment)
                for segment in segmentation.segments
            }
            ret[segmentation.name] = SegmentGroup(
                segmentation.name, segmentation.id, segments, segmentation
            )
        return AiqClientResponse(response=ret, pending_operations=[])

    def _get_split_data(
        self,
        project_id: str,
        data_collection_id: str,
        data_split_id: str,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        pre_processed_data_required: bool = True,
        extra_data: bool = False,
        system_data: bool = False,
        include_labels: bool = False,
        exclude_feature_values: bool = False,
        get_post_processed_data: bool = False,
        segment: Optional[Segment] = None,
        timeout: Optional[int] = None,
        model_id: Optional[str] = None,
        wait: bool = False
    ) -> is_pb.SplitDataResponse:
        request = is_pb.SplitDataRequest(
            project_id=project_id,
            data_collection_id=data_collection_id,
            include_labels=include_labels,
            include_extra_data=extra_data,
            include_system_data=system_data,
            exclude_feature_values=exclude_feature_values,
            pre_processed_data_required=pre_processed_data_required,
            get_post_processed_data=get_post_processed_data,
            model_id=model_id
        )
        request.input_spec.split_id = data_split_id

        # set input spec
        _set_input_spec_from_segment(request.input_spec, segment)
        if start or stop is not None:
            # devnote: there is weird but expected behavior here where if start is provided but stop is not, then
            # for start = 3, stop = None, AIQ will return datapoints in the range (3, num_bulk_influences)
            # we could instead request all data points and slice from 3: client-side, but that
            # is more involved than necessary for now.
            request.input_spec.dataset_index_range.start = start  # pylint: disable=protobuf-type-error
            request.input_spec.dataset_index_range.stop = stop if stop is not None else 0  # pylint: disable=protobuf-type-error
        else:
            request.input_spec.all_available_inputs = True

        # return response
        if wait:
            responses = self._wait_till_streaming_complete(
                lambda ret: ret.pending_operations.waiting_on_operation_ids,
                lambda: self.communicator.get_split_data(request), project_id,
                timeout
            )
            return merge_split_data_responses(responses)
        else:
            responses = [
                response
                for response in self.communicator.get_split_data(request)
            ]
        return merge_split_data_responses(responses)

    def compute_performance(
        self,
        project_id: str,
        model_id: str,
        data_split_id: str,
        metric_types: Sequence[str],
        segment: Optional[Segment] = None,
        wait: bool = True,
        as_proto: bool = False
    ) -> AiqClientResponse[Sequence[Union[float, acc_pb.AccuracyResult]]]:
        request = is_pb.AccuracyRequest()
        for metric_type in metric_types:
            request.accuracy_types.append(
                getattr(acc_pb.AccuracyType, metric_type)
            )
        request.model_input_spec.all_available_inputs = True
        _set_input_spec_from_segment(request.model_input_spec, segment)
        response = self._compute_accuracy(
            project_id, model_id, data_split_id, request, wait=wait
        )
        if not response.accuracies:
            accuracy = [
                np.nan
            ]  # cannot compute accuracy due to missing labels.
        else:
            accuracy = response.accuracies
        if as_proto:
            accuracy = [
                response.accuracies_result_map[i]
                for i in request.accuracy_types
            ]

        return AiqClientResponse(
            response=accuracy,
            pending_operations=response.pending_operations.
            waiting_on_operation_ids
        )

    def compute_batched_performance(
        self,
        project_id: str,
        model_id: str,
        input_specs: Sequence[is_pb.ModelInputSpec],
        metric_type: str,
        as_proto: bool = False,
        wait: bool = True
    ) -> AiqClientResponse[Sequence[Union[float, acc_pb.AccuracyResult]]]:
        metric_type = getattr(acc_pb.AccuracyType, metric_type)
        request = is_pb.BatchAccuracyRequest(
            project_id=project_id, accuracy_types=[metric_type]
        )
        for input_spec in input_specs:
            model_data = request.model_data.add()
            model_data.model_id.model_id = model_id
            model_data.model_id.project_id = project_id
            model_data.model_input_spec.CopyFrom(input_spec)
        if wait:
            response = self._wait_till_complete_generic(
                lambda ret: sum(
                    [
                        list(acc.pending_operations.waiting_on_operation_ids)
                        for acc in ret.model_accuracies
                    ], []
                ), lambda: self.communicator.compute_batched_accuracy(request),
                project_id
            )
        else:
            response = self.communicator.compute_batched_accuracy(request)

        pending_op_ids = []
        accuracies = []
        for resp in response.model_accuracies:
            pending_op_ids.append(
                resp.pending_operations.waiting_on_operation_ids
            )
            accuracies.append(
                resp.accuracies_result_map.get(
                    metric_type, acc_pb.AccuracyResult(value=np.nan)
                )
            )
        if not as_proto:
            accuracies = [i.value for i in accuracies]
        return AiqClientResponse(
            response=accuracies, pending_operations=pending_op_ids
        )

    def _compute_compare_model_output(
        self,
        project_id: str,
        model_id: str,
        base_data_split_id: Optional[str],
        compare_data_split_id: str,
        score_type: Optional[str] = None,
        include_breakdown_by_feature: bool = False,
        segment: Optional[Segment] = None,
        wait: bool = True
    ) -> is_pb.CompareModelOutputResponse:
        request = is_pb.CompareModelOutputRequest()
        request.output_spec1.model_id.project_id = project_id
        request.output_spec1.model_id.model_id = model_id
        if include_breakdown_by_feature:
            request.output_spec1.model_input_spec.standard_bulk_inputs = True
        else:
            request.output_spec1.model_input_spec.all_available_inputs = True

        _set_input_spec_from_segment(
            request.output_spec1.model_input_spec, segment
        )
        if score_type is not None:
            quantity_of_interest = aiq_proto.GetQuantityOfInterestFromScoreType(
                score_type
            )
            request.output_spec1.score_type = quantity_of_interest
        request.output_spec2.CopyFrom(request.output_spec1)
        request.options.include_breakdown_by_feature = include_breakdown_by_feature
        request.output_spec1.model_input_spec.split_id = base_data_split_id
        request.output_spec2.model_input_spec.split_id = compare_data_split_id
        if wait:
            return self._wait_till_complete(
                lambda: self.communicator.
                compute_model_score_instability(request), project_id
            )
        else:
            return self.communicator.compute_model_score_instability(request)

    def compute_model_score_instability(
        self,
        project_id: str,
        model_id: str,
        base_data_split_id: Optional[str],
        compare_data_split_id: str,
        score_type: Optional[str] = None,
        distance_type: Optional[str] = None,
        segment: Optional[Segment] = None,
        wait: bool = True
    ) -> AiqClientResponse[float]:
        response = self._compute_compare_model_output(
            project_id,
            model_id,
            base_data_split_id,
            compare_data_split_id,
            score_type=score_type,
            segment=segment,
            wait=wait
        )
        stability_scores = {
            comparison.distance_type: comparison.distance_value
            for comparison in response.distribution_comparisons
        }
        distance_type = distance_type or "DIFFERENCE_OF_MEAN"
        return AiqClientResponse(
            response=stability_scores.get(
                distance_pb2.DistanceType.Value(distance_type)
            ),
            pending_operations=response.pending_operations.
            waiting_on_operation_ids
        )

    def batch_compute_model_score_instability(
        self,
        project_id: str,
        distance_type_to_output_specs: Mapping[str, Sequence[Tuple[
            ModelOutputSpec, ModelOutputSpec]]],
        as_proto: bool = False,
        wait: bool = True
    ) -> AiqClientResponse[Mapping[int, Sequence[Union[
        float, is_pb.BatchCompareModelOutputResponse.ResponseEntry]]]]:
        req_distance_type_to_output_specs = {}
        for distance_type, output_spec_pairs in distance_type_to_output_specs.items(
        ):
            req_output_spec_pairs = []
            for output_spec_pair in output_spec_pairs:
                req_output_spec_pair = is_pb.BatchCompareModelOutputRequest.OutputSpecPair(
                )
                req_output_spec_pair.output_spec1.model_id.project_id = project_id
                req_output_spec_pair.output_spec1.model_id.model_id = output_spec_pair[
                    0].model_id
                req_output_spec_pair.output_spec1.model_input_spec.split_id = output_spec_pair[
                    0].data_split_id
                req_output_spec_pair.output_spec1.model_input_spec.all_available_inputs = True
                _set_input_spec_from_segment(
                    req_output_spec_pair.output_spec1.model_input_spec,
                    output_spec_pair[0].segment
                )
                req_output_spec_pair.output_spec2.model_id.project_id = project_id
                req_output_spec_pair.output_spec2.model_id.model_id = output_spec_pair[
                    1].model_id
                req_output_spec_pair.output_spec2.model_input_spec.split_id = output_spec_pair[
                    1].data_split_id
                req_output_spec_pair.output_spec2.model_input_spec.all_available_inputs = True
                _set_input_spec_from_segment(
                    req_output_spec_pair.output_spec2.model_input_spec,
                    output_spec_pair[1].segment
                )
                req_output_spec_pairs.append(req_output_spec_pair)
            req_distance_type_to_output_specs[distance_pb2.DistanceType.Value(distance_type)] = \
                is_pb.BatchCompareModelOutputRequest.ListOfOutputSpecPairs(
                    output_spec_pairs=req_output_spec_pairs
                )

        request = is_pb.BatchCompareModelOutputRequest(
            project_id=project_id,
            distance_type_to_output_specs=req_distance_type_to_output_specs
        )
        if wait:
            response = self._wait_till_complete_generic(
                lambda ret: sum(
                    [
                        list(
                            resp_entry.pending_operations.
                            waiting_on_operation_ids
                        ) for distance_type in ret.
                        distance_type_to_comparison_results for resp_entry in
                        ret.distance_type_to_comparison_results[
                            distance_type].comparison_results
                    ], []
                ), lambda: self.communicator.
                batch_compute_model_score_instability(request), project_id
            )
        else:
            response = self.communicator.batch_compute_model_score_instability(
                request
            )

        distance_type_to_comparison_results = {}
        for distance_type in distance_type_to_output_specs:
            comparison_results = response.distance_type_to_comparison_results.get(
                distance_pb2.DistanceType.Value(distance_type)
            ).comparison_results
            if as_proto:
                distance_type_to_comparison_results[distance_type] = list(
                    comparison_results
                )
            else:
                distance_type_to_comparison_results[distance_type] = [
                    result.distance_value for result in comparison_results
                ]
        return AiqClientResponse(
            response=distance_type_to_comparison_results,
            pending_operations=sum(
                    [
                        list(
                            resp_entry.pending_operations.
                            waiting_on_operation_ids
                        ) for distance_type in response.distance_type_to_comparison_results
                        for resp_entry in response.distance_type_to_comparison_results[distance_type].comparison_results
                    ], []
                )
        )\

    def compute_feature_contributors_to_instability(
        self,
        project_id: str,
        model_id: str,
        base_data_split_id: str,
        compare_data_split_id: str,
        score_type: Optional[str] = None,
        use_difference_of_means: bool = False,
        segment: Optional[Segment] = None,
        wait: bool = True
    ) -> AiqClientResponse[float]:
        response = self._compute_compare_model_output(
            project_id,
            model_id,
            base_data_split_id,
            compare_data_split_id,
            score_type=score_type,
            include_breakdown_by_feature=True,
            segment=segment,
            wait=wait
        )

        contributors_map = {
            comparison.distance_type:
            pd.Series(comparison.feature_breakdown).to_frame().T
            for comparison in response.distribution_comparisons
        }
        return AiqClientResponse(
            response=contributors_map[
                distance_pb2.DistanceType.
                DIFFERENCE_OF_MEAN if use_difference_of_means else distance_pb2.
                DistanceType.NUMERICAL_WASSERSTEIN],
            pending_operations=response.pending_operations.
            waiting_on_operation_ids
        )

    def compute_estimated_performance(
        self,
        project_id: str,
        model_id: str,
        data_split_id: str,
        metric_type: str,
        segment: Optional[Segment] = None,
        wait: bool = True
    ) -> AiqClientResponse[Tuple[float, str]]:

        request = is_pb.AccuracyRequest()
        request.accuracy_types.append(getattr(acc_pb.AccuracyType, metric_type))
        request.model_input_spec.standard_bulk_inputs = True
        request.estimate_type = acc_pb.EstimateType.FORCE_ESTIMATE
        response = self._compute_accuracy(
            project_id,
            model_id,
            data_split_id,
            request,
            segment=segment,
            wait=wait
        )
        assert response.is_estimate
        estimate_confidence = acc_pb.AccuracyEstimateConfidence.Confidence.Name(
            response.estimate_confidence
        )  # convert to string rep of enum
        return AiqClientResponse(
            response=(response.accuracies[0], estimate_confidence),
            pending_operations=response.pending_operations.
            waiting_on_operation_ids
        )

    def _compute_accuracy(
        self,
        project_id: str,
        model_id: str,
        data_split_id: str,
        request: is_pb.AccuracyRequest(),
        segment: Optional[Segment] = None,
        wait: bool = True
    ) -> is_pb.AccuracyResponse:
        request.model_id.project_id = project_id
        request.model_id.model_id = model_id
        request.model_input_spec.split_id = data_split_id
        _set_input_spec_from_segment(request.model_input_spec, segment)
        if wait:
            return self._wait_till_complete(
                lambda: self.communicator.compute_accuracy(request), project_id
            )
        else:
            return self.communicator.compute_accuracy(request)

    def list_performance_metrics(self) -> Sequence[str]:
        # TODO(DC-74): This isn't correct!
        return acc_pb.AccuracyType.Type.keys()[
            1:]  # do not return default "UNKNOWN" accuracy type

    def list_fairness_metrics(self) -> Sequence[str]:
        return is_pb.BiasType.Type.keys()[
            1:]  # do not return default "UNKNOWN" bias type

    def compute_fairness(
        self,
        project_id: str,
        model_id: str,
        split_id: str,
        segmentation_name: str,
        segment1_name: str,
        segment2_name: Optional[str] = None,
        fairness_type: Optional[str] = "DISPARATE_IMPACT_RATIO",
        threshold: Optional[float] = None,
        threshold_score_type: Optional[str] = None,
        wait: bool = True
    ) -> AiqClientResponse[BiasResult]:
        all_segmentations = self._get_segmentations(project_id)
        all_segmentation_names = [
            s.name for s in all_segmentations.segmentations
        ]
        segmentation = all_segmentations.segmentations[
            all_segmentation_names.index(segmentation_name)]
        segment_names = [s.name for s in segmentation.segments]
        segment1 = segmentation.segments[segment_names.index(segment1_name)]
        segment2 = None
        if segment2_name:
            segment2 = segmentation.segments[segment_names.index(segment2_name)]

        req = is_pb.GetModelBiasRequest()
        req.model_id.project_id = project_id
        req.model_id.model_id = model_id
        req.bias_types.append(getattr(is_pb.BiasType, fairness_type))

        mis1, mis2 = self._create_input_specs_for_fairness(
            split_id=split_id, segment1_pb=segment1, segment2_pb=segment2
        )
        req.segment1.CopyFrom(mis1)
        req.segment2.CopyFrom(mis2)
        threshold_config = self._create_threshold_config_request(
            threshold, threshold_score_type
        )
        if threshold_config is not None:
            req.threshold_config.CopyFrom(threshold_config)
        if wait:
            response = self._wait_till_complete(
                lambda: self.communicator.compute_fairness(req), project_id
            )
        else:
            response = self.communicator.compute_fairness(req)

        if response.HasField("pending_operations"):
            return AiqClientResponse(
                None,
                pending_operations=response.pending_operations.
                waiting_on_operation_ids
            )
        bias_result = self._parse_bias_results_from_proto(
            segment1_name=segment1_name,
            segment2_name=segment2_name,
            bias_results_pb=response.bias_results
        )[0]
        return AiqClientResponse(
            response=bias_result,
            pending_operations=response.pending_operations.
            waiting_on_operation_ids
        )

    def batch_compute_fairness(
        self,
        project_id: str,
        bias_requests: Sequence[ModelBiasRequest],
        wait: bool = True
    ) -> AiqClientResponse[Sequence[Sequence[BiasResult]]]:
        req = is_pb.GetBatchModelBiasRequest()
        req.project_id = project_id
        for bias_request in bias_requests:
            bias_types = [
                getattr(is_pb.BiasType, i) for i in bias_request.bias_types
            ]
            mis1, mis2 = self._create_input_specs_for_fairness(
                split_id=bias_request.data_split_id,
                segment1_pb=bias_request.protected_segment._segment_proto,
                segment2_pb=bias_request.comparison_segment._segment_proto
                if bias_request.comparison_segment else None
            )
            threshold_config = self._create_threshold_config_request(
                bias_request.classification_threshold,
                bias_request.classification_threshold_score_type
            )
            bias_request_proto = is_pb.GetModelBiasRequest(
                model_id=is_pb.ModelId(
                    project_id=project_id, model_id=bias_request.model_id
                ),
                segment1=mis1,
                segment2=mis2,
                bias_types=bias_types
            )
            if threshold_config is not None:
                bias_request_proto.threshold_config.CopyFrom(threshold_config)
            req.bias_requests.append(bias_request_proto)
        if wait:
            response = self._wait_till_complete_generic(
                lambda ret: sum(
                    [
                        list(
                            bias_resp.pending_operations.
                            waiting_on_operation_ids
                        ) for bias_resp in ret.bias_responses
                    ], []
                ), lambda: self.communicator.batch_compute_fairness(req),
                project_id
            )
        else:
            response = self.communicator.batch_compute_fairness(req)

        batch_bias_results: Sequence[Sequence[BiasResult]] = []
        pending_op_ids = []
        for i, bias_request in enumerate(bias_requests):
            bias_results = self._parse_bias_results_from_proto(
                segment1_name=bias_request.protected_segment.name,
                segment2_name=bias_request.comparison_segment.name
                if bias_request.comparison_segment else
                _DEFAULT_COMPARISON_SEGMENT_NAME,
                bias_results_pb=response.bias_responses[i].bias_results
            )
            batch_bias_results.append(bias_results)
            pending_op_ids.append(
                response.bias_responses[i].pending_operations.
                waiting_on_operation_ids
            )

        return AiqClientResponse(
            response=batch_bias_results, pending_operations=pending_op_ids
        )

    def _create_input_specs_for_fairness(
        self,
        split_id: str,
        segment1_pb: _PBSegment,
        segment2_pb: Optional[_PBSegment] = None
    ) -> Tuple[is_pb.ModelInputSpec, is_pb.ModelInputSpec]:
        mis1 = is_pb.ModelInputSpec(
            all_available_inputs=True, split_id=split_id
        )
        mis2 = is_pb.ModelInputSpec()
        mis2.CopyFrom(mis1)
        mis1.filter_expression.CopyFrom(segment1_pb.filter_expression)
        if segment2_pb:
            mis2.filter_expression.CopyFrom(segment2_pb.filter_expression)
        else:
            complement_filter_expression = FilterExpression()
            complement_filter_expression.sub_expressions.append(
                segment1_pb.filter_expression
            )
            complement_filter_expression.operator = FilterExpressionOperator.FEO_NOT
            mis2.filter_expression.CopyFrom(complement_filter_expression)
        return mis1, mis2

    def _create_threshold_config_request(
        self, threshold: float, threshold_score_type: str
    ):
        if threshold is None:
            return
        threshold_config = is_pb.ModelThresholdConfigRequest()
        threshold_config.threshold_request_type = is_pb.ModelThresholdConfigRequest.ModelThresholdRequestType.MANUAL_THRESHOLDS
        threshold_config.manual_threshold_options.classifier_thresholds.append(  # pylint: disable=protobuf-type-error
            threshold)
        if threshold_score_type == 'probits':
            threshold_config.manual_threshold_options.threshold_score_type = is_pb.ModelThresholdScoreType.Type.PROBITS
        elif threshold_score_type == 'logits':
            threshold_config.manual_threshold_options.threshold_score_type = is_pb.ModelThresholdScoreType.Type.LOGITS
        return threshold_config

    def _parse_bias_results_from_proto(
        self, segment1_name: str, segment2_name: str,
        bias_results_pb: Sequence[is_pb.BiasResult]
    ) -> Sequence[BiasResult]:
        bias_results: Sequence[BiasResult] = []
        segment2_name = segment2_name or _DEFAULT_COMPARISON_SEGMENT_NAME
        for bias_result_proto in bias_results_pb:
            favored_segment_name = segment1_name if bias_result_proto.segment1_favored else segment2_name
            if bias_result_proto.segment1_metric == bias_result_proto.segment2_metric:
                favored_segment_name = None
            bias_results.append(
                BiasResult(
                    segment1_name=segment1_name,
                    segment2_name=segment2_name,
                    aggregate_metric=bias_result_proto.aggregate_metric,
                    segment1_metric=bias_result_proto.segment1_metric,
                    segment2_metric=bias_result_proto.segment2_metric,
                    favored_segment=favored_segment_name,
                    metric_name=is_pb.BiasType.Type.Name(
                        bias_result_proto.bias_type
                    ),
                    result_type=bias_result_proto.result_type,
                    error_message=bias_result_proto.error_message,
                )
            )
        return bias_results

    def compute_feature_drift(
        self,
        project_id: str,
        split1_id: str,
        data_collection1_id: str,
        split2_id: str,
        data_collection2_id: str,
        distance_metrics: Sequence[str] = None,
        feature_names: Sequence[str] = None
    ) -> AiqClientResponse[pd.DataFrame]:
        self._validate_distance_metrics(distance_metrics)
        self._validate_feature_names(
            feature_names, project_id, data_collection1_id, split1_id
        )
        self._validate_feature_names(
            feature_names, project_id, data_collection2_id, split2_id
        )
        mis1 = is_pb.ModelInputSpec(
            split_id=split1_id, all_available_inputs=True
        )
        mis2 = is_pb.ModelInputSpec(
            split_id=split2_id, all_available_inputs=True
        )

        distance_metrics = [] if not distance_metrics else [
            DISTANCE_NAME_TO_PB.get(i) for i in distance_metrics
        ]
        feature_names = [] if not feature_names else feature_names
        request = is_pb.FeatureDriftRequest(
            input_spec1=mis1,
            input_spec2=mis2,
            distances=distance_metrics,
            features=feature_names
        )
        response = self.communicator.compute_feature_drift(request)
        distances_map = {}
        for i in response.drifts:
            distance_type = DISTANCE_PB_TO_NAME[i.distance_type]
            if distance_type not in distances_map:
                distances_map[distance_type] = {}
            distances_map[distance_type][i.feature] = i.distance_value
        result = pd.DataFrame(distances_map)
        # TODO(AB#7202): Add pending operations to feature drift response.
        return AiqClientResponse(response=result, pending_operations=[])

    def suggest_high_error_segments(
        self,
        project_id: str,
        model_id: str,
        data_split_id: str,
        comparison_model_id: Optional[str],
        comparison_data_split_id: Optional[str],
        interesting_segment_type: InterestingSegment.Type,
        num_features: int,
        max_num_responses: int,
        num_samples: int,
        minimum_size: int,
        size_exponent: float,
        random_state: int,
        wait: bool = False
    ) -> AiqClientResponse[Optional[Mapping[str, SegmentGroup]]]:
        request = is_pb.InterestingSegmentsRequest(
            project_id=project_id,
            model_ids=[model_id],
            model_input_specs=[
                is_pb.ModelInputSpec(
                    all_available_inputs=
                    True,  # TODO(JIRA#DC-51): fix this so it can be given the segment.
                    split_id=data_split_id,
                )
            ],
            interesting_segment_type=interesting_segment_type,
            num_features=num_features,
            max_num_responses=max_num_responses,
            pointwise_metrics_aggregator=is_pb.InterestingSegmentsRequest.
            PointwiseMetricsAggregator(
                minimum_size=minimum_size, size_exponent=size_exponent
            ),
            random_state=random_state,
            num_samples=num_samples,
        )
        if comparison_model_id:
            request.model_ids.append(comparison_model_id)
            request.model_input_specs.append(
                is_pb.ModelInputSpec(
                    all_available_inputs=
                    True,  # TODO(JIRA#DC-51): fix this so it can be given the segment.
                    split_id=comparison_data_split_id,
                )
            )
        request_func = lambda: self.communicator.get_interesting_segments(
            request
        )
        if wait:
            response = self._wait_till_complete(
                request_func, project_id, timeout=None
            )
        else:
            response = request_func()

        if response.HasField("pending_operations"):
            return AiqClientResponse(
                response=None,
                pending_operations=response.pending_operations.
                waiting_on_operation_ids
            )
        return self.get_wrapped_segmentations(
            project_id=project_id,
            convert_model_ids_to_model_names=True,
            include_unaccepted_interesting_segments=True,
            segmentation_ids=set(response.segmentation_ids)
        )

    def add_segment_group(
        self,
        project_id: str,
        segment_group_name: str,
        segment_definitions: Mapping[str, str],
        data_collection_id: str,
        split_id: Optional[str] = None,
        score_type: Optional[str] = None
    ) -> None:
        # If split_id is provided, will check that the feature names are valid
        request = is_pb.UpdateManualSegmentationRequest(project_id=project_id)
        segmentation = request.segmentation
        segmentation.name = segment_group_name
        segmentation.project_id = project_id
        for segment_name in segment_definitions:
            segment = segmentation.segments.add()
            segment.name = segment_name
            filter_expression = parse_expression_to_filter_proto(
                segment_definitions[segment_name], self.logger
            )
            filter_requirements = FilterProcessor.get_filter_requirements(
                filter_expression
            )
            models_in_filter = filter_requirements.model_ids_to_score_type.keys(
            ) - {filter_constants.GENERIC_MODEL_ID}
            if models_in_filter:
                models_in_dc = self.artifact_interaction_client.get_all_models_in_project(
                    project_id,
                    data_collection_id=data_collection_id,
                    ar_meta_fetch_mode=ArtifactMetaFetchMode.NAMES
                )
                nonexistent_model_names = models_in_filter - set(models_in_dc)
                if nonexistent_model_names:
                    data_collection = self.artifact_interaction_client.get_data_collection_metadata_by_id(
                        project_id, data_collection_id
                    )
                    raise NotFoundError(
                        f"The provided `segment_definitions` contains model(s) that doesn't exist: {nonexistent_model_names} in data collection \"{data_collection['name']}\"."
                    )

            self._replace_model_names_with_model_ids_in_filter(
                project_id, filter_expression
            )
            if data_collection_id and split_id:
                self._validate_feature_names(
                    filter_requirements.column_names,
                    project_id,
                    data_collection_id,
                    split_id,
                    extra_data=True,
                    allow_label_or_model_column=True,
                    score_type=score_type
                )
            segment.filter_expression.CopyFrom(filter_expression)
        self.communicator.update_manual_segmentation(request)

    def set_as_protected_segment(
        self, project_id: str, segment_group_id: str, segment_name: str
    ):
        get_request = is_pb.GetManualSegmentationRequest(
            project_id=project_id, segmentation_id=segment_group_id
        )
        get_response = self.communicator.get_segmentations(get_request)
        segmentation = get_response.segmentations[0]
        for segment in segmentation.segments:
            if segment_name == segment.name:
                segment.is_protected = True

        update_request = is_pb.UpdateManualSegmentationRequest(
            project_id=project_id, segmentation=segmentation
        )
        self.communicator.update_manual_segmentation(update_request)

    def upload_segment_group(
        self,
        project_id: str,
        segment_group: SegmentGroup,
    ) -> None:
        request = is_pb.UpdateManualSegmentationRequest(project_id=project_id)
        segmentation = request.segmentation
        segmentation.name = segment_group.name
        segmentation.project_id = project_id
        segments = segment_group.get_segments()
        for segment_name in segments:
            segment = segmentation.segments.add()
            segment.name = segment_name
            segment.filter_expression.CopyFrom(
                segments[segment_name]._segment_proto.filter_expression
            )
            self._replace_model_names_with_model_ids_in_filter(
                project_id, segment.filter_expression
            )
        self.communicator.update_manual_segmentation(request)

    def delete_segment_group(
        self, project_id: str, segment_group_name: str
    ) -> None:
        segment_groups = self.get_wrapped_segmentations(project_id).response
        if segment_group_name not in segment_groups:
            raise NotFoundError(
                f"Segment group \"{segment_group_name}\" does not exist in project \"{project_id}\""
            )
        request = is_pb.UpdateManualSegmentationRequest(project_id=project_id)
        request.segmentation_id_to_delete = segment_groups[segment_group_name
                                                          ].id
        self.communicator.update_manual_segmentation(request)

    def _validate_distance_metrics(
        self, distance_metrics: Sequence[str]
    ) -> None:
        if distance_metrics:
            for metric_name in distance_metrics:
                if not metric_name in DISTANCE_NAME_TO_PB:
                    raise ValueError(
                        f"Metric \"{metric_name}\" is not in list of supported metrics: {list(DISTANCE_NAME_TO_PB.keys())}."
                    )

    def _validate_feature_names(
        self,
        feature_names: Sequence[str],
        project_id: str,
        data_collection_id: str,
        split_id: str,
        extra_data: bool = False,
        allow_label_or_model_column: bool = False,
        score_type: Optional[str] = None
    ) -> None:
        valid_names = set(
            self.get_xs(
                project_id=project_id,
                data_split_id=split_id,
                data_collection_id=data_collection_id,
                start=0,
                stop=1,
                extra_data=extra_data,
                pre_processed_data_required=False
            ).response.columns
        )
        validate_feature_names(
            feature_names=feature_names,
            valid_feature_names=valid_names,
            score_type=score_type,
            allow_label_or_model_column=allow_label_or_model_column
        )

    def _replace_model_names_with_model_ids_in_filter(
        self, project_id: str, filter_expression: FilterExpression
    ) -> None:
        if filter_expression.WhichOneof("value") == "filter_leaf":
            if filter_expression.filter_leaf.value_type == FilterLeaf.FilterLeafValueType.OUTPUT:
                if filter_expression.filter_leaf.model_id:
                    model_metadata = self.artifact_interaction_client.get_model_metadata(
                        project_id,
                        model_name=filter_expression.filter_leaf.model_id
                    )
                    filter_expression.filter_leaf.model_id = model_metadata["id"
                                                                           ]
        else:
            for sub_filter in filter_expression.sub_expressions:
                self._replace_model_names_with_model_ids_in_filter(
                    project_id, sub_filter
                )

    def _replace_model_ids_with_model_names_in_filter(
        self, project_id: str, filter_expression: FilterExpression
    ) -> None:
        if filter_expression.WhichOneof("value") == "filter_leaf":
            if filter_expression.filter_leaf.value_type == FilterLeaf.FilterLeafValueType.OUTPUT:
                if filter_expression.filter_leaf.model_id:
                    model_metadata = self.artifact_interaction_client.get_model_metadata(
                        project_id,
                        model_id=filter_expression.filter_leaf.model_id
                    )
                    filter_expression.filter_leaf.model_id = model_metadata[
                        "name"]
        else:
            for sub_filter in filter_expression.sub_expressions:
                self._replace_model_ids_with_model_names_in_filter(
                    project_id, sub_filter
                )
