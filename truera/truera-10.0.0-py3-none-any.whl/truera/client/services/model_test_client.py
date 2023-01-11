from __future__ import annotations

import logging
import time
from typing import (
    Callable, Mapping, Optional, Sequence, Tuple, TYPE_CHECKING, Union
)

from google.protobuf.json_format import MessageToDict

from truera.client.public.communicator.model_test_http_communicator import \
    HttpModelTestCommunicator
from truera.client.services.mrc_client import MrcClient
from truera.client.services.pending_operation_client import \
    TimeoutExceededException
from truera.client.util.absolute_progress_bar import AbsoluteProgressBars
# pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.accuracy_pb2 import \
    AccuracyType as _PBAccuracyType
from truera.protobuf.public.aiq.distance_pb2 import \
    DistanceType as _PBDistanceType
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    BiasType as _PBBiasType
from truera.protobuf.public.data.segment_pb2 import SegmentID as _PBSegmentID
from truera.protobuf.public.metadata_message_types_pb2 import DataSplitMetadata
# pylint: enable=no-name-in-module
from truera.protobuf.public.modeltest import modeltest_pb2
from truera.protobuf.public.modeltest import modeltest_service_pb2
# pylint: disable=no-name-in-module
from truera.protobuf.public.modeltest.modeltest_pb2 import \
    TestThreshold as _PBTestThreshold
# pylint: enable=no-name-in-module
from truera.public import feature_influence_constants as fi_constants

if TYPE_CHECKING:
    from truera.client.public.auth_details import AuthDetails

SINGLE_VALUE_THRESHOLD_TYPE_TO_PB = {
    "ABSOLUTE": _PBTestThreshold.ThresholdType.ABSOLUTE_SINGLE_VALUE,
    "RELATIVE": _PBTestThreshold.ThresholdType.RELATIVE_SINGLE_VALUE
}
VALUE_RANGE_THRESHOLD_TYPE_TO_PB = {
    "ABSOLUTE": _PBTestThreshold.ThresholdType.ABSOLUTE_VALUE_RANGE,
    "RELATIVE": _PBTestThreshold.ThresholdType.RELATIVE_VALUE_RANGE
}


def _create_test_threshold_pb(
    threshold_type: str,
    *,
    fail_if_less_than: Optional[float] = None,
    fail_if_greater_than: Optional[float] = None,
    fail_if_within: Optional[Tuple[float, float]] = None,
    fail_if_outside: Optional[Tuple[float, float]] = None,
    reference_split_id: Optional[str] = None,
    reference_model_id: Optional[str] = None
) -> _PBTestThreshold:
    test_threshold = _PBTestThreshold()
    if fail_if_less_than is not None or fail_if_greater_than is not None:
        test_threshold.threshold_type = SINGLE_VALUE_THRESHOLD_TYPE_TO_PB[
            threshold_type]
        # pylint: disable=protobuf-type-error
        test_threshold.value.value = fail_if_less_than if fail_if_less_than is not None else fail_if_greater_than
        test_threshold.value.condition = _PBTestThreshold.ThresholdValue.WARN_OR_FAIL_IF_LESS_THAN if fail_if_less_than is not None else _PBTestThreshold.ThresholdValue.WARN_OR_FAIL_IF_GREATER_THAN
    elif fail_if_within is not None or fail_if_outside is not None:
        test_threshold.threshold_type = VALUE_RANGE_THRESHOLD_TYPE_TO_PB[
            threshold_type]
        value_range = fail_if_within if fail_if_within is not None else fail_if_outside
        test_threshold.value_range.lower_bound = value_range[0]
        test_threshold.value_range.upper_bound = value_range[1]
        test_threshold.value_range.condition = _PBTestThreshold.ThresholdValueRange.WARN_OR_FAIL_IF_OUTSIDE if fail_if_outside is not None else _PBTestThreshold.ThresholdValueRange.WARN_OR_FAIL_IF_WITHIN
    if test_threshold.threshold_type == _PBTestThreshold.ThresholdType.RELATIVE_SINGLE_VALUE or test_threshold.threshold_type == _PBTestThreshold.ThresholdType.RELATIVE_VALUE_RANGE:
        if reference_split_id:
            # pylint: disable=protobuf-type-error
            test_threshold.reference_split_id = reference_split_id
        if reference_model_id:
            # pylint: disable=protobuf-type-error
            test_threshold.reference_model_id = reference_model_id
    return test_threshold


class ModelTestClient:

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails = None,
        logger=None,
        use_http: bool = False,
        *,
        verify_cert: Union[bool, str] = True
    ):
        if (not use_http):
            from truera.client.private.communicator.model_test_grpc_communicator import \
                GrpcModelTestCommunicator
        self.logger = logger or logging.getLogger(__name__)
        self.communicator = HttpModelTestCommunicator(
            connection_string, auth_details, logger, verify_cert=verify_cert
        ) if use_http else GrpcModelTestCommunicator(
            connection_string, auth_details, logger
        )
        self.mrc_client = MrcClient(
            f"{connection_string.rstrip('/')}/api/mrc",
            auth_details,
            logger,
            verify_cert=verify_cert
        )

    def create_tests_from_split(
        self, project_id: str, split_id: str
    ) -> Sequence[modeltest_pb2.ModelTest]:
        request = modeltest_service_pb2.CreateTestsFromSplitRequest(
            project_id=project_id, split_id=split_id
        )
        response = self.communicator.create_tests_from_split(request)
        return response.model_tests

    def start_test_creation_workflow(
        self, project_id: str, split_id: str
    ) -> str:
        request = modeltest_service_pb2.StartTestCreationWorkflowRequest(
            test_creation_request=modeltest_service_pb2.
            CreateTestsFromSplitRequest(
                project_id=project_id, split_id=split_id
            )
        )
        response = self.communicator.start_test_creation_workflow(request)
        return response.workflow_id

    def create_performance_test(
        self,
        project_id: str,
        split_id: str,
        metric: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        segmentation_id: Optional[str] = None,
        segment_name: Optional[str] = None,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        warn_threshold_type: str = "ABSOLUTE",
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None,
        fail_threshold_type: str = "ABSOLUTE",
        reference_split_id: Optional[str] = None,
        reference_model_id: Optional[str] = None,
        autorun: bool = True,
        overwrite: bool = False
    ) -> str:
        if not metric in _PBAccuracyType.Type.keys():
            raise ValueError(
                f"Provided performance metric \"{metric}\" is not supported. Supported metrics: {_PBAccuracyType.Type.keys()}"
            )

        request = modeltest_service_pb2.CreatePerformanceTestRequest(
            project_id=project_id,
            split_id=split_id,
            test_name=name,
            description=description,
            autorun=autorun,
            overwrite=overwrite
        )
        if segmentation_id:
            if not segment_name:
                raise ValueError(
                    f"Need to provide `segment_name` to create test using segment."
                )
            segment_id = _PBSegmentID(
                segmentation_id=segmentation_id, segment_name=segment_name
            )
            request.segment_id.CopyFrom(segment_id)
        threshold_warning, threshold_fail = self._validate_and_get_thresholds(
            warn_if_less_than=warn_if_less_than,
            warn_if_greater_than=warn_if_greater_than,
            warn_if_within=warn_if_within,
            warn_if_outside=warn_if_outside,
            warn_threshold_type=warn_threshold_type,
            fail_if_less_than=fail_if_less_than,
            fail_if_greater_than=fail_if_greater_than,
            fail_if_within=fail_if_within,
            fail_if_outside=fail_if_outside,
            fail_threshold_type=fail_threshold_type,
            reference_split_id=reference_split_id,
            reference_model_id=reference_model_id
        )

        test_definition = modeltest_pb2.PerformanceTest()
        test_definition.performance_metric_and_threshold.accuracy_type = _PBAccuracyType.Type.Value(
            metric
        )
        if threshold_warning:
            test_definition.performance_metric_and_threshold.threshold_warning.CopyFrom(
                threshold_warning
            )
        if threshold_fail:
            test_definition.performance_metric_and_threshold.threshold_fail.CopyFrom(
                threshold_fail
            )
        request.test_definition.CopyFrom(test_definition)
        response = self.communicator.create_performance_test(request)
        return response.test_id, response.test_group_id

    def create_performance_test_group(
        self,
        project_id: str,
        metric: str,
        *,
        split_ids: Optional[Sequence[str]] = None,
        split_name_regex: Optional[str] = None,
        data_collection_ids: Optional[Sequence[str]] = None,
        data_collection_name_regex: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        test_group_id: Optional[str] = None,
        segmentation_ids: Optional[Sequence[str]] = None,
        segment_names: Optional[Sequence[str]] = None,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        warn_threshold_type: str = "ABSOLUTE",
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None,
        fail_threshold_type: str = "ABSOLUTE",
        reference_split_id: Optional[str] = None,
        reference_model_id: Optional[str] = None
    ) -> str:
        if not metric in _PBAccuracyType.Type.keys():
            raise ValueError(
                f"Provided performance metric \"{metric}\" is not supported. Supported metrics: {_PBAccuracyType.Type.keys()}"
            )

        model_test_group = modeltest_service_pb2.ModelTestGroup(
            project_id=project_id,
            split_ids=split_ids,
            split_name_regex=split_name_regex,
            data_collection_ids=data_collection_ids,
            data_collection_name_regex=data_collection_name_regex,
            test_name=name,
            description=description,
            test_group_id=test_group_id
        )

        segment_ids = self._validate_segment_ids(
            segmentation_ids, segment_names
        )
        model_test_group.segment_ids.extend(segment_ids)
        threshold_warning, threshold_fail = self._validate_and_get_thresholds(
            warn_if_less_than=warn_if_less_than,
            warn_if_greater_than=warn_if_greater_than,
            warn_if_within=warn_if_within,
            warn_if_outside=warn_if_outside,
            warn_threshold_type=warn_threshold_type,
            fail_if_less_than=fail_if_less_than,
            fail_if_greater_than=fail_if_greater_than,
            fail_if_within=fail_if_within,
            fail_if_outside=fail_if_outside,
            fail_threshold_type=fail_threshold_type,
            reference_split_id=reference_split_id,
            reference_model_id=reference_model_id
        )

        test_definition = modeltest_pb2.PerformanceTest()
        test_definition.performance_metric_and_threshold.accuracy_type = _PBAccuracyType.Type.Value(
            metric
        )
        if threshold_warning:
            test_definition.performance_metric_and_threshold.threshold_warning.CopyFrom(
                threshold_warning
            )
        if threshold_fail:
            test_definition.performance_metric_and_threshold.threshold_fail.CopyFrom(
                threshold_fail
            )
        model_test_group.performance_test.CopyFrom(test_definition)
        request = modeltest_service_pb2.CreatePerformanceTestGroupRequest(
            model_test_group=model_test_group
        )
        response = self.communicator.create_performance_test_group(request)
        return response.test_group_id, response.test_ids

    def _validate_and_get_thresholds(
        self,
        *,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        warn_threshold_type: Optional[str] = None,
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None,
        fail_threshold_type: Optional[str] = None,
        reference_split_id: Optional[str] = "",
        reference_model_id: Optional[str] = "",
    ) -> Tuple[_PBTestThreshold, _PBTestThreshold]:
        if sum(
            [
                warn_if_less_than is not None, warn_if_greater_than is not None,
                warn_if_within is not None, warn_if_outside is not None
            ]
        ) > 1:
            raise ValueError(
                "Provided warning thresholds have conflicts! Please only provide one of [`warn_if_less_than`, `warn_if_greater_than`, `warn_if_within`, `warn_if_outside`]."
            )
        if sum(
            [
                fail_if_less_than is not None, fail_if_greater_than is not None,
                fail_if_within is not None, fail_if_outside is not None
            ]
        ) > 1:
            raise ValueError(
                "Provided fail thresholds have conflicts! Please only provide one of [`fail_if_less_than`, `fail_if_greater_than`, `fail_if_within`, `fail_if_outside`]."
            )

        if warn_if_within is not None or warn_if_outside is not None or fail_if_within is not None or fail_if_outside is not None:
            range_threshold = warn_if_within or warn_if_outside or fail_if_within or fail_if_outside
            if not isinstance(range_threshold,
                              Sequence) or len(range_threshold) != 2:
                raise ValueError(
                    "Range threshold needs to be a `Sequence` with 2 elements: `(lower_bound, upper_bound)`."
                )

        # SINGLE_VALUE_THRESHOLD_TYPE_TO_PB and VALUE_RANGE_THRESHOLD_TYPE_TO_PB have the same keys, so only check against one of them
        if warn_threshold_type not in SINGLE_VALUE_THRESHOLD_TYPE_TO_PB:
            raise ValueError(
                f"Warning threshold type need to be one of: {list(SINGLE_VALUE_THRESHOLD_TYPE_TO_PB.keys())}. Provided: \"{warn_threshold_type}\""
            )
        if fail_threshold_type not in SINGLE_VALUE_THRESHOLD_TYPE_TO_PB:
            raise ValueError(
                f"Fail threshold type need to be one of: {list(SINGLE_VALUE_THRESHOLD_TYPE_TO_PB.keys())}. Provided: \"{fail_threshold_type}\""
            )

        threshold_warning = _create_test_threshold_pb(
            threshold_type=warn_threshold_type,
            fail_if_less_than=warn_if_less_than,
            fail_if_greater_than=warn_if_greater_than,
            fail_if_within=warn_if_within,
            fail_if_outside=warn_if_outside,
            reference_split_id=reference_split_id,
            reference_model_id=reference_model_id
        )
        threshold_fail = _create_test_threshold_pb(
            threshold_type=fail_threshold_type,
            fail_if_less_than=fail_if_less_than,
            fail_if_greater_than=fail_if_greater_than,
            fail_if_within=fail_if_within,
            fail_if_outside=fail_if_outside,
            reference_split_id=reference_split_id,
            reference_model_id=reference_model_id
        )
        return threshold_warning, threshold_fail

    def create_stability_test(
        self,
        project_id: str,
        metric: str,
        comparison_data_split_id: str,
        base_data_split_id: Optional[str] = None,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        segmentation_id: Optional[str] = None,
        segment_name: Optional[str] = None,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None,
        autorun: bool = True,
        overwrite: bool = False,
    ) -> str:
        if not metric in _PBDistanceType.keys():
            raise ValueError(
                f"Provided stability metric \"{metric}\" is not supported. Supported metrics: {_PBDistanceType.keys()}"
            )

        request = modeltest_service_pb2.CreateStabilityTestRequest(
            project_id=project_id,
            split_id=comparison_data_split_id,
            test_name=name,
            description=description,
            autorun=autorun,
            overwrite=overwrite
        )
        if segmentation_id:
            if not segment_name:
                raise ValueError(
                    f"Need to provide `segment_name` to create test using segment."
                )
            segment_id = _PBSegmentID(
                segmentation_id=segmentation_id, segment_name=segment_name
            )
            request.segment_id.CopyFrom(segment_id)

        threshold_warning, threshold_fail = self._validate_and_get_thresholds(
            warn_if_less_than=warn_if_less_than,
            warn_if_greater_than=warn_if_greater_than,
            warn_if_within=warn_if_within,
            warn_if_outside=warn_if_outside,
            warn_threshold_type="ABSOLUTE",
            fail_if_less_than=fail_if_less_than,
            fail_if_greater_than=fail_if_greater_than,
            fail_if_within=fail_if_within,
            fail_if_outside=fail_if_outside,
            fail_threshold_type="ABSOLUTE"
        )

        test_definition = modeltest_pb2.StabilityTest()
        if base_data_split_id:
            test_definition.base_split_id = base_data_split_id or ""
        test_definition.stability_metric_and_threshold.distance_type = _PBDistanceType.Value(
            metric
        )
        if threshold_warning:
            test_definition.stability_metric_and_threshold.threshold_warning.CopyFrom(
                threshold_warning
            )
        if threshold_fail:
            test_definition.stability_metric_and_threshold.threshold_fail.CopyFrom(
                threshold_fail
            )
        request.test_definition.CopyFrom(test_definition)
        response = self.communicator.create_stability_test(request)
        return response.test_id, response.test_group_id

    def create_stability_test_group(
        self,
        project_id: str,
        metric: str,
        *,
        comparison_data_split_ids: Optional[Sequence[str]] = None,
        comparison_data_split_name_regex: Optional[str] = None,
        data_collection_id_to_base_split_id: Optional[Mapping[str, str]] = None,
        data_collection_ids: Optional[Sequence[str]] = None,
        data_collection_name_regex: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        test_group_id: Optional[str] = None,
        segmentation_ids: Optional[Sequence[str]] = None,
        segment_names: Optional[Sequence[str]] = None,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None,
        autorun: bool = True,
    ) -> str:
        if not metric in _PBDistanceType.keys():
            raise ValueError(
                f"Provided stability metric \"{metric}\" is not supported. Supported metrics: {_PBDistanceType.keys()}"
            )

        model_test_group = modeltest_service_pb2.ModelTestGroup(
            project_id=project_id,
            split_ids=comparison_data_split_ids,
            split_name_regex=comparison_data_split_name_regex,
            data_collection_ids=data_collection_ids,
            data_collection_id_to_base_split_id=
            data_collection_id_to_base_split_id,
            data_collection_name_regex=data_collection_name_regex,
            test_name=name,
            description=description,
            test_group_id=test_group_id
        )
        segment_ids = self._validate_segment_ids(
            segmentation_ids, segment_names
        )
        model_test_group.segment_ids.extend(segment_ids)

        threshold_warning, threshold_fail = self._validate_and_get_thresholds(
            warn_if_less_than=warn_if_less_than,
            warn_if_greater_than=warn_if_greater_than,
            warn_if_within=warn_if_within,
            warn_if_outside=warn_if_outside,
            warn_threshold_type="ABSOLUTE",
            fail_if_less_than=fail_if_less_than,
            fail_if_greater_than=fail_if_greater_than,
            fail_if_within=fail_if_within,
            fail_if_outside=fail_if_outside,
            fail_threshold_type="ABSOLUTE"
        )

        test_definition = modeltest_pb2.StabilityTest()
        test_definition.stability_metric_and_threshold.distance_type = _PBDistanceType.Value(
            metric
        )
        if threshold_warning:
            test_definition.stability_metric_and_threshold.threshold_warning.CopyFrom(
                threshold_warning
            )
        if threshold_fail:
            test_definition.stability_metric_and_threshold.threshold_fail.CopyFrom(
                threshold_fail
            )
        model_test_group.stability_test.CopyFrom(test_definition)
        request = modeltest_service_pb2.CreateStabilityTestGroupRequest(
            model_test_group=model_test_group
        )
        response = self.communicator.create_stability_test_group(request)
        return response.test_group_id, response.test_ids

    def create_fairness_test(
        self,
        project_id: str,
        split_id: str,
        segmentation_id: str,
        metric: str,
        protected_segment_name: str,
        comparison_segment_name: Optional[str] = None,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None,
        autorun: bool = True,
        overwrite: bool = False,
    ) -> str:
        if not metric in _PBBiasType.Type.keys():
            raise ValueError(
                f"Provided fairness metric \"{metric}\" is not supported. Supported metrics: {_PBBiasType.Type.keys()}"
            )

        request = modeltest_service_pb2.CreateFairnessTestRequest(
            project_id=project_id,
            split_id=split_id,
            test_name=name,
            description=description,
            autorun=autorun,
            overwrite=overwrite
        )
        threshold_warning, threshold_fail = self._validate_and_get_thresholds(
            warn_if_less_than=warn_if_less_than,
            warn_if_greater_than=warn_if_greater_than,
            warn_if_within=warn_if_within,
            warn_if_outside=warn_if_outside,
            warn_threshold_type="ABSOLUTE",
            fail_if_less_than=fail_if_less_than,
            fail_if_greater_than=fail_if_greater_than,
            fail_if_within=fail_if_within,
            fail_if_outside=fail_if_outside,
            fail_threshold_type="ABSOLUTE"
        )

        test_definition = modeltest_pb2.FairnessTest()
        test_definition.segment_id_protected.segmentation_id = segmentation_id
        test_definition.segment_id_protected.segment_name = protected_segment_name
        test_definition.segment_id_comparison.segmentation_id = segmentation_id
        if comparison_segment_name:
            test_definition.segment_id_comparison.segment_name = comparison_segment_name or ""
        test_definition.fairness_metric_and_threshold.bias_type = _PBBiasType.Type.Value(
            metric
        )
        if threshold_warning:
            test_definition.fairness_metric_and_threshold.threshold_warning.CopyFrom(
                threshold_warning
            )
        if threshold_fail:
            test_definition.fairness_metric_and_threshold.threshold_fail.CopyFrom(
                threshold_fail
            )
        request.test_definition.CopyFrom(test_definition)
        response = self.communicator.create_fairness_test(request)
        return response.test_id, response.test_group_id

    def create_fairness_test_group(
        self,
        project_id: str,
        metric: str,
        *,
        all_protected_segments: bool = False,
        protected_segment_ids: Optional[Sequence[_PBSegmentID]] = None,
        comparison_segment_ids: Optional[Sequence[_PBSegmentID]] = None,
        split_ids: Optional[Sequence[str]] = None,
        split_name_regex: Optional[str] = None,
        data_collection_ids: Optional[Sequence[str]] = None,
        data_collection_name_regex: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        test_group_id: Optional[str] = None,
        warn_if_less_than: Optional[float] = None,
        warn_if_greater_than: Optional[float] = None,
        warn_if_within: Optional[Tuple[float, float]] = None,
        warn_if_outside: Optional[Tuple[float, float]] = None,
        fail_if_less_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        fail_if_within: Optional[Tuple[float, float]] = None,
        fail_if_outside: Optional[Tuple[float, float]] = None
    ) -> str:
        if not metric in _PBBiasType.Type.keys():
            raise ValueError(
                f"Provided fairness metric \"{metric}\" is not supported. Supported metrics: {_PBBiasType.Type.keys()}"
            )

        model_test_group = modeltest_service_pb2.ModelTestGroup(
            project_id=project_id,
            split_ids=split_ids,
            split_name_regex=split_name_regex,
            data_collection_ids=data_collection_ids,
            data_collection_name_regex=data_collection_name_regex,
            test_name=name,
            description=description,
            protected_segment_ids=protected_segment_ids,
            comparison_segment_ids=comparison_segment_ids,
            test_group_id=test_group_id
        )
        threshold_warning, threshold_fail = self._validate_and_get_thresholds(
            warn_if_less_than=warn_if_less_than,
            warn_if_greater_than=warn_if_greater_than,
            warn_if_within=warn_if_within,
            warn_if_outside=warn_if_outside,
            warn_threshold_type="ABSOLUTE",
            fail_if_less_than=fail_if_less_than,
            fail_if_greater_than=fail_if_greater_than,
            fail_if_within=fail_if_within,
            fail_if_outside=fail_if_outside,
            fail_threshold_type="ABSOLUTE"
        )
        test_definition = modeltest_pb2.FairnessTest()
        test_definition.fairness_metric_and_threshold.bias_type = _PBBiasType.Type.Value(
            metric
        )
        if threshold_warning:
            test_definition.fairness_metric_and_threshold.threshold_warning.CopyFrom(
                threshold_warning
            )
        if threshold_fail:
            test_definition.fairness_metric_and_threshold.threshold_fail.CopyFrom(
                threshold_fail
            )
        if all_protected_segments:
            test_definition.protected_segment_name_regex = ".*"
        model_test_group.fairness_test.CopyFrom(test_definition)
        request = modeltest_service_pb2.CreateFairnessTestGroupRequest(
            model_test_group=model_test_group
        )
        response = self.communicator.create_fairness_test_group(request)
        return response.test_group_id, response.test_ids

    def create_feature_importance_test(
        self,
        project_id: str,
        split_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        background_split_id: str,
        min_importance_value: float,
        project_score_type: str,
        test_score_type: Optional[str] = None,
        segmentation_id: Optional[str] = None,
        segment_name: Optional[str] = None,
        warn_if_greater_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None,
        autorun: bool = True,
        overwrite: bool = False
    ) -> str:
        if project_score_type in fi_constants.VALID_SCORE_TYPES_FOR_REGRESSION:
            if test_score_type and test_score_type not in fi_constants.VALID_SCORE_TYPES_FOR_REGRESSION:
                raise ValueError(
                    f"`test_score_type` needs to be one of {fi_constants.VALID_SCORE_TYPES_FOR_REGRESSION}"
                )
        elif project_score_type in fi_constants.VALID_SCORE_TYPES_FOR_CLASSIFICATION:
            if test_score_type and test_score_type not in fi_constants.VALID_SCORE_TYPES_FOR_CLASSIFICATION:
                raise ValueError(
                    f"`test_score_type` needs to be one of {fi_constants.VALID_SCORE_TYPES_FOR_CLASSIFICATION}"
                )
        else:
            raise ValueError(
                f"`project_score_type` needs to be one of {fi_constants.VALID_SCORE_TYPES_FOR_REGRESSION + fi_constants.VALID_SCORE_TYPES_FOR_CLASSIFICATION}"
            )

        if min_importance_value <= 0 or min_importance_value >= 1:
            raise ValueError(
                "`min_importance_value` needs to be between 0 and 1."
            )

        request = modeltest_service_pb2.CreateFeatureImportanceTestRequest(
            project_id=project_id,
            split_id=split_id,
            test_name=name,
            description=description,
            autorun=autorun,
            overwrite=overwrite
        )
        if segmentation_id:
            if not segment_name:
                raise ValueError(
                    f"Need to provide `segment_name` to create test using segment."
                )
            segment_id = _PBSegmentID(
                segmentation_id=segmentation_id, segment_name=segment_name
            )
            request.segment_id.CopyFrom(segment_id)
        threshold_warning, threshold_fail = self._validate_and_get_thresholds(
            warn_if_greater_than=warn_if_greater_than,
            warn_threshold_type="ABSOLUTE",
            fail_if_greater_than=fail_if_greater_than,
            fail_threshold_type="ABSOLUTE"
        )

        test_definition = modeltest_pb2.FeatureImportanceTest(
            background_split_id=background_split_id
        )

        if not test_score_type:
            test_qoi = fi_constants.SCORE_TYPE_TO_QOI[project_score_type]
        else:
            test_qoi = fi_constants.SCORE_TYPE_TO_QOI[test_score_type]
        test_definition.options_and_threshold.qoi = test_qoi
        test_definition.options_and_threshold.min_importance_value = min_importance_value
        if threshold_warning:
            test_definition.options_and_threshold.threshold_warning.CopyFrom(
                threshold_warning
            )
        if threshold_fail:
            test_definition.options_and_threshold.threshold_fail.CopyFrom(
                threshold_fail
            )
        request.test_definition.CopyFrom(test_definition)
        response = self.communicator.create_feature_importance_test(request)
        return response.test_id, response.test_group_id

    def create_feature_importance_test_group(
        self,
        project_id: str,
        *,
        split_ids: Optional[Sequence[str]] = None,
        split_name_regex: Optional[str] = None,
        data_collection_ids: Optional[Sequence[str]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        test_group_id: Optional[str] = None,
        data_collection_id_to_background_split_id: Mapping[str, str],
        min_importance_value: float,
        project_score_type: str,
        test_score_type: Optional[str] = None,
        segment_ids: Optional[Sequence[_PBSegmentID]] = None,
        warn_if_greater_than: Optional[float] = None,
        fail_if_greater_than: Optional[float] = None
    ) -> str:
        if project_score_type in fi_constants.VALID_SCORE_TYPES_FOR_REGRESSION:
            if test_score_type and test_score_type not in fi_constants.VALID_SCORE_TYPES_FOR_REGRESSION:
                raise ValueError(
                    f"`test_score_type` needs to be one of {fi_constants.VALID_SCORE_TYPES_FOR_REGRESSION}"
                )
        elif project_score_type in fi_constants.VALID_SCORE_TYPES_FOR_CLASSIFICATION:
            if test_score_type and test_score_type not in fi_constants.VALID_SCORE_TYPES_FOR_CLASSIFICATION:
                raise ValueError(
                    f"`test_score_type` needs to be one of {fi_constants.VALID_SCORE_TYPES_FOR_CLASSIFICATION}"
                )
        else:
            raise ValueError(
                f"`project_score_type` needs to be one of {fi_constants.VALID_SCORE_TYPES_FOR_REGRESSION + fi_constants.VALID_SCORE_TYPES_FOR_CLASSIFICATION}"
            )

        if min_importance_value <= 0 or min_importance_value >= 1:
            raise ValueError(
                "`min_importance_value` needs to be between 0 and 1."
            )

        model_test_group = modeltest_service_pb2.ModelTestGroup(
            project_id=project_id,
            split_ids=split_ids,
            split_name_regex=split_name_regex,
            data_collection_ids=data_collection_ids,
            data_collection_id_to_base_split_id=
            data_collection_id_to_background_split_id,
            segment_ids=segment_ids,
            test_name=name,
            description=description,
            test_group_id=test_group_id
        )
        threshold_warning, threshold_fail = self._validate_and_get_thresholds(
            warn_if_greater_than=warn_if_greater_than,
            warn_threshold_type="ABSOLUTE",
            fail_if_greater_than=fail_if_greater_than,
            fail_threshold_type="ABSOLUTE"
        )

        test_definition = modeltest_pb2.FeatureImportanceTest()

        if not test_score_type:
            test_qoi = fi_constants.SCORE_TYPE_TO_QOI[project_score_type]
        else:
            test_qoi = fi_constants.SCORE_TYPE_TO_QOI[test_score_type]
        test_definition.options_and_threshold.qoi = test_qoi
        test_definition.options_and_threshold.min_importance_value = min_importance_value
        if threshold_warning:
            test_definition.options_and_threshold.threshold_warning.CopyFrom(
                threshold_warning
            )
        if threshold_fail:
            test_definition.options_and_threshold.threshold_fail.CopyFrom(
                threshold_fail
            )
        model_test_group.feature_importance_test.CopyFrom(test_definition)
        request = modeltest_service_pb2.CreateFeatureImportanceTestGroupRequest(
            model_test_group=model_test_group
        )
        response = self.communicator.create_feature_importance_test_group(
            request
        )
        return response.test_group_id, response.test_ids

    def delete_model_test(
        self,
        project_id: str,
        test_id: str,
        as_json: bool = False
    ) -> Union[Mapping, modeltest_pb2.ModelTest]:
        request = modeltest_service_pb2.DeleteModelTestRequest(
            project_id=project_id, test_id=test_id
        )
        response = self.communicator.delete_model_test(request)
        if as_json:
            MessageToDict(
                response.deleted_test,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            )
        return response.deleted_test

    def delete_model_test_group(self, project_id: str,
                                test_group_id: str) -> Sequence[str]:
        request = modeltest_service_pb2.DeleteModelTestGroupRequest(
            project_id=project_id, test_group_id=test_group_id
        )
        response = self.communicator.delete_model_test_group(request)
        return response.deleted_test_ids

    def get_model_tests(
        self,
        project_id: str,
        *,
        name: Optional[str] = None,
        model_test_type: Optional[modeltest_pb2.ModelTestType] = None,
        data_collection_id: Optional[str] = None,
        split_id: Optional[str] = None,
        segmentation_id: Optional[str] = None,
        segment_name: Optional[str] = None,
        metric: Optional[str] = None,
        test_id: Optional[str] = None,
        as_json: bool = False
    ) -> Union[Sequence[Mapping], Sequence[modeltest_pb2.ModelTest]]:
        if segment_name:
            if not segmentation_id:
                raise ValueError(
                    "Need to provide segment group to be able to filter results by `segment_name`."
                )
        request = modeltest_service_pb2.GetModelTestsRequest(
            project_id=project_id,
            test_name=name,
            test_type=model_test_type,
            data_collection_id=data_collection_id,
            split_id=split_id,
            test_id=test_id,
        )
        model_tests = self.communicator.get_model_tests(request).model_tests
        if segmentation_id:
            model_tests = [
                i for i in model_tests
                if i.segment_id.segmentation_id == segmentation_id
            ]
            if segment_name:
                model_tests = [
                    i for i in model_tests
                    if i.segment_id.segment_name == segment_name
                ]
        if metric:
            if not model_test_type:
                raise ValueError(
                    "Need to provide `model_test_type` to be able to filter results by `metric`."
                )
            if model_test_type == modeltest_pb2.ModelTestType.MODEL_TEST_TYPE_PERFORMANCE:
                # pylint: disable=protobuf-enum-value
                metric_enum = _PBAccuracyType.Type.Value(metric)
                model_tests = [
                    i for i in model_tests
                    if i.performance_test.performance_metric_and_threshold.
                    accuracy_type == metric_enum
                ]
            elif model_test_type == modeltest_pb2.ModelTestType.MODEL_TEST_TYPE_FAIRNESS:
                # pylint: disable=protobuf-enum-value
                metric_enum = _PBBiasType.Type.Value(metric)
                model_tests = [
                    i for i in model_tests
                    if i.fairness_test.fairness_metric_and_threshold.bias_type
                    == metric_enum
                ]
            elif model_test_type == modeltest_pb2.ModelTestType.MODEL_TEST_TYPE_STABILITY:
                # pylint: disable=protobuf-enum-value
                metric_enum = _PBDistanceType.Value(metric)
                model_tests = [
                    i for i in model_tests if i.stability_test.
                    stability_metric_and_threshold.distance_type == metric_enum
                ]

        if as_json:
            return [
                MessageToDict(
                    i,
                    including_default_value_fields=True,
                    preserving_proto_field_name=True
                ) for i in model_tests
            ]
        return model_tests

    def get_model_test_groups(
        self,
        project_id: str,
        *,
        name: Optional[str] = None,
        model_test_type: Optional[modeltest_pb2.ModelTestType] = None,
        data_collection_id: Optional[str] = None,
        split_id: Optional[str] = None,
        test_group_id: Optional[str] = None,
        as_json: bool = False
    ) -> Sequence[modeltest_service_pb2.modeltest_service_pb2.ModelTestGroup]:
        request = modeltest_service_pb2.GetModelTestGroupsRequest(
            project_id=project_id,
            test_name=name,
            test_type=model_test_type,
            data_collection_id=data_collection_id,
            split_id=split_id,
            test_group_id=test_group_id,
        )
        model_test_groups = self.communicator.get_model_test_groups(
            request
        ).model_test_groups

        if as_json:
            return [
                MessageToDict(
                    i,
                    including_default_value_fields=True,
                    preserving_proto_field_name=True
                ) for i in model_test_groups
            ]
        return model_test_groups

    def get_data_splits_from_regex(
        self,
        project_id: str,
        *,
        split_name_regex: str,
        data_collection_ids: Optional[Sequence[str]] = None,
        data_collection_name_regex: Optional[str] = None,
        as_json: bool = False
    ) -> Sequence[Union[Mapping, DataSplitMetadata]]:
        request = modeltest_service_pb2.GetDataSplitsFromRegexRequest(
            project_id=project_id,
            split_name_regex=split_name_regex,
            data_collection_ids=data_collection_ids,
            data_collection_name_regex=data_collection_name_regex
        )
        splits_metadata = self.communicator.get_data_splits_from_regex(
            request
        ).splits_metadata

        if as_json:
            return [
                MessageToDict(
                    i,
                    including_default_value_fields=True,
                    preserving_proto_field_name=True
                ) for i in splits_metadata
            ]
        return splits_metadata

    def delete_model_tests_for_split(
        self,
        project_id: str,
        split_id: str,
        as_json: bool = False
    ) -> Union[Sequence[Mapping], Sequence[modeltest_pb2.ModelTest]]:
        request = modeltest_service_pb2.DeleteModelTestsForSplitRequest(
            project_id=project_id, split_id=split_id
        )
        response = self.communicator.delete_model_test_for_split(request)
        if as_json:
            return [
                MessageToDict(
                    i,
                    including_default_value_fields=True,
                    preserving_proto_field_name=True
                ) for i in response.deleted_tests
            ]
        return response.deleted_tests

    def _wait_for_model_test_results(
        self,
        project_id: str,
        model_id: str,
        test_type: Optional[modeltest_pb2.ModelTestType] = None,
        split_id: Optional[str] = None,
        wait: bool = True
    ):
        request = modeltest_service_pb2.GetTestResultsForModelRequest(
            project_id=project_id,
            model_id=model_id,
            test_type=test_type,
            split_id=split_id
        )
        request_func = lambda: self.communicator.get_test_results_for_model(
            request
        )
        if wait:
            return self._wait_till_complete(request_func, timeout=None)
        else:
            return request_func()

    def get_test_results_for_model(
        self,
        project_id: str,
        model_id: str,
        *,
        test_type: Optional[modeltest_pb2.ModelTestType] = None,
        split_id: Optional[str] = None,
        as_json: bool = False,
        wait: bool = True
    ) -> modeltest_service_pb2.GetTestResultsForModelResponse:

        resp = self._wait_for_model_test_results(
            project_id,
            model_id=model_id,
            test_type=test_type,
            split_id=split_id,
            wait=wait
        )
        if as_json:
            return MessageToDict(
                resp,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            )
        return resp

    def _validate_segment_ids(
        self,
        segmentation_ids: Optional[Sequence[str]] = None,
        segment_names: Optional[Sequence[str]] = None
    ) -> Sequence[_PBSegmentID]:
        segment_ids = []
        if segmentation_ids:
            if len(segmentation_ids) != len(segment_names):
                raise ValueError(
                    f"Need to provide `segment_name` to create test using segment."
                )
            for i in range(len(segmentation_ids)):
                segment_id = _PBSegmentID(
                    segmentation_id=segmentation_ids[i],
                    segment_name=segment_names[i]
                )
                segment_ids.append(segment_id)
        return segment_ids

    def _wait_till_complete(
        self, request_func: Callable, timeout: Optional[float] = None
    ):
        time_start = time.time()
        ret = request_func()
        initial_pending_count = len(
            set(ret.pending_operations.waiting_on_operation_ids)
        )
        if initial_pending_count == 0:
            return ret
        with AbsoluteProgressBars() as progress_bars:
            while (timeout is None) or (time.time() - time_start < timeout):
                ret = request_func()
                cur_pending_count = len(
                    set(ret.pending_operations.waiting_on_operation_ids)
                )
                percentages = {
                    'status':
                        (initial_pending_count - cur_pending_count) /
                        initial_pending_count * 100
                }
                progress_bars.set_percentages(percentages)
                if cur_pending_count == 0:
                    return ret
                time.sleep(1)
            raise TimeoutExceededException(timeout)
