from __future__ import annotations

import logging
from typing import Mapping, Optional, Sequence, Union

import pandas as pd

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.data_quality_http_communicator import \
    HttpDataQualityCommunicator
from truera.protobuf.dataquality import dataquality_service_pb2 as dq_pb
from truera.protobuf.dataquality import metric_pb2 as dq_metric_pb
from truera.protobuf.dataquality import rule_pb2 as dq_rule_pb2

SUPPORTED_METRICS_MAP = {
    dq_metric_pb.MetricDefinition.MetricType.COLUMN_COMPLETENESS:
        "MISSING_VALUES",
    dq_metric_pb.MetricDefinition.MetricType.NUMERIC_VALUE_IN_RANGE:
        "OUT_OF_RANGE",
    dq_metric_pb.MetricDefinition.MetricType.FLOATING_COMPLETENESS:
        "NAN_VALUES",
    dq_metric_pb.MetricDefinition.MetricType.FLOATING_FINITENESS:
        "INFINITY_VALUES",
    dq_metric_pb.MetricDefinition.MetricType.UNIQUE_CATEGORICAL_VALUE:
        "NEW_CATEGORICAL_VALUES"
}
MODIFIABLE_METRICS = {
    dq_metric_pb.MetricDefinition.MetricType.NUMERIC_VALUE_IN_RANGE,
    dq_metric_pb.MetricDefinition.MetricType.UNIQUE_CATEGORICAL_VALUE
}

METRICS_NAME_TO_TYPE = {
    SUPPORTED_METRICS_MAP[i]: i for i in SUPPORTED_METRICS_MAP
}

SUPPORTED_RULE_THRESHOLD_OPERATORS = {
    "EQUALS":
        dq_rule_pb2.RuleDefinition.Operator.EQUALS,
    "LESS_THAN":
        dq_rule_pb2.RuleDefinition.Operator.LESS_THAN,
    "LESS_THAN_OR_EQUAL":
        dq_rule_pb2.RuleDefinition.Operator.LESS_THAN_OR_EQUAL,
    "GREATER_THAN":
        dq_rule_pb2.RuleDefinition.Operator.GREATER_THAN,
    "GREATER_THAN_OR_EQUAL":
        dq_rule_pb2.RuleDefinition.Operator.GREATER_THAN_OR_EQUAL
}


class DataQualityClient():

    def __init__(
        self,
        connection_string: str = None,
        auth_details: AuthDetails = None,
        logger=None,
        use_http: bool = False,
        *,
        verify_cert: Union[bool, str] = True
    ):
        if (not use_http):
            from truera.client.private.communicator.data_quality_grpc_communicator import \
                GrpcDataQualityCommunicator
        self.logger = logger or logging.getLogger(__name__)
        self.auth_details = auth_details
        self.communicator = HttpDataQualityCommunicator(
            connection_string, auth_details, logger, verify_cert=verify_cert
        ) if use_http else GrpcDataQualityCommunicator(
            connection_string, auth_details, logger
        )

    def get_data_quality_metrics_result(
        self,
        project_id: str,
        data_collection_id: str,
        data_split_ids: Sequence[str],
        feature_name: Optional[str] = None,
        metric_name: Optional[str] = None,
        normalize: bool = False
    ) -> Sequence[Union[pd.Series, pd.DataFrame]]:
        request = dq_pb.GetSplitRuleEvaluationResultsRequest(
            project_id=project_id,
            data_collection_id=data_collection_id,
            split_id=data_split_ids
        )
        if metric_name is not None:
            self._validate_metric_name(metric_name)
        response = self.communicator.get_split_rule_evaluation_results(request)
        parsed_results = {}
        for i in response.split_rule_evaluation_result:
            result = self._parse_data_quality_split_metrics_result(
                i.rule_evaluation_result, normalize
            )
            if feature_name is not None:
                if feature_name not in result.index:
                    raise ValueError(f"Feature {feature_name} does not exist")
                result = result.loc[feature_name]
            if metric_name is not None:
                if metric_name not in result:
                    raise ValueError(f"Metric {metric_name} does not exist")
                result = result[metric_name]
            parsed_results[i.split_id] = result
        return [parsed_results[i] for i in data_split_ids]

    def _parse_data_quality_split_metrics_result(
        self,
        split_metrics_result: dq_rule_pb2.RuleEvaluationResult,
        normalize: bool = False
    ) -> pd.DataFrame:
        parsed_result = {}
        split_size = 0
        for i in split_metrics_result:
            if i.metric_result.metric_type in SUPPORTED_METRICS_MAP:
                metric_name = SUPPORTED_METRICS_MAP[i.metric_result.metric_type]
                if not split_size and i.metric_result.metric_type == dq_metric_pb.MetricDefinition.MetricType.COLUMN_COMPLETENESS:
                    split_size = i.metric_result.violation_count + i.metric_result.compliance_count
                if i.metric_result.feature_name not in parsed_result:
                    parsed_result[i.metric_result.feature_name] = {}
                parsed_result[i.metric_result.feature_name
                             ][metric_name] = i.metric_result.violation_count
        df = pd.DataFrame(parsed_result).T
        df.index.names = ["Feature Names"]
        if normalize:
            df = df / split_size
        return df

    def get_data_quality_metrics_definition(
        self,
        project_id: str,
        data_collection_id: str,
        feature_name: str,
        metric_name: Optional[str] = None
    ) -> Union[str, Mapping[str, str]]:
        if metric_name is not None:
            self._validate_metric_name(metric_name)
        request = dq_pb.GetAllRuleDefinitionsRequest(
            project_id=project_id, data_collection_id=data_collection_id
        )
        response = self.communicator.get_all_rule_definitions(request)
        result = self._parse_data_quality_metrics_definition(
            response.rule_definition
        )
        if feature_name not in result:
            raise ValueError(f"Feature {feature_name} does not exist")
        result = result[feature_name]
        if metric_name is not None:
            if metric_name not in result:
                raise ValueError(
                    f"Data quality metric {metric_name} does not exist for feature {feature_name}"
                )
            result = result[metric_name]
        return result

    def get_data_quality_rule_threshold_and_operator(
        self,
        project_id: str,
        data_collection_id: str,
        feature_name: str,
        metric_name: Optional[str] = None
    ) -> Union[str, Mapping[str, str]]:
        if metric_name is not None:
            self._validate_metric_name(metric_name)
        rule_definitions = self._get_data_quality_rule_definition(
            project_id, data_collection_id, feature_name, metric_name
        )
        if metric_name:
            rule_definitions = [rule_definitions]
        parsed_result = {}
        for i in rule_definitions:
            parsed_result[SUPPORTED_METRICS_MAP[i.metric_definition.metric_type]
                         ] = {
                             'violation_threshold':
                                 i.violation_threshold,
                             'match_type':
                                 dq_rule_pb2.RuleDefinition.MatchType.Name(
                                     i.match_type
                                 ),
                             'operator':
                                 dq_rule_pb2.RuleDefinition.Operator.Name(
                                     i.operator
                                 )
                         }
        return parsed_result

    def _parse_data_quality_metrics_definition(
        self, dq_rules_definition: dq_pb.GetAllRuleDefinitionsResponse
    ) -> Mapping[str, Mapping[str, str]]:
        parsed_result = {}
        for i in dq_rules_definition:
            if i.metric_definition.metric_type in SUPPORTED_METRICS_MAP:
                metric_name = SUPPORTED_METRICS_MAP[
                    i.metric_definition.metric_type]
                feature_name = i.metric_definition.column_name
                if feature_name not in parsed_result:
                    parsed_result[i.metric_definition.column_name] = {}
                if i.metric_definition.metric_type == dq_metric_pb.MetricDefinition.MetricType.UNIQUE_CATEGORICAL_VALUE:
                    parsed_result[feature_name][
                        metric_name
                    ] = f"Feature value is not one of {i.metric_definition.value_constraint.allowed_string_values}"
                elif i.metric_definition.metric_type == dq_metric_pb.MetricDefinition.MetricType.NUMERIC_VALUE_IN_RANGE:
                    parsed_result[feature_name][
                        metric_name
                    ] = f"Feature value is outside the min-max range of {i.metric_definition.value_constraint.numeric_range.min_value}-{i.metric_definition.value_constraint.numeric_range.max_value}"
                elif i.metric_definition.metric_type == dq_metric_pb.MetricDefinition.MetricType.FLOATING_COMPLETENESS:
                    parsed_result[feature_name][
                        metric_name] = f"Feature value is not a number"
                elif i.metric_definition.metric_type == dq_metric_pb.MetricDefinition.MetricType.FLOATING_FINITENESS:
                    parsed_result[feature_name][metric_name
                                               ] = f"Feature value is infinity"
                elif i.metric_definition.metric_type == dq_metric_pb.MetricDefinition.MetricType.COLUMN_COMPLETENESS:
                    parsed_result[feature_name][metric_name
                                               ] = f"Feature value is missing"
                else:
                    parsed_result[feature_name][metric_name] = metric_name
        return parsed_result

    def _get_data_quality_rule_definition(
        self,
        project_id: str,
        data_collection_id: str,
        feature_name: str,
        metric_name: Optional[str] = None
    ) -> Union[dq_rule_pb2.RuleDefinition,
               Sequence[dq_rule_pb2.dq_rule_pb2.RuleDefinition]]:
        request = dq_pb.GetAllRuleDefinitionsRequest(
            project_id=project_id, data_collection_id=data_collection_id
        )
        result = []
        response = self.communicator.get_all_rule_definitions(request)
        for i in response.rule_definition:
            if i.metric_definition.metric_type in SUPPORTED_METRICS_MAP and i.metric_definition.column_name == feature_name:
                if metric_name:
                    if SUPPORTED_METRICS_MAP[i.metric_definition.metric_type
                                            ] == metric_name:
                        return i
                else:
                    result.append(i)
        if metric_name:
            raise ValueError(
                f"Data quality metric {metric_name} does not exist for feature {feature_name}"
            )
        return result

    def _validate_update_metric_constraint(
        self,
        metric_name: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        categorical_values: Optional[Sequence] = None
    ) -> bool:
        metric_type = METRICS_NAME_TO_TYPE.get(metric_name)
        if not metric_type in MODIFIABLE_METRICS:
            raise ValueError(
                f"Constraint for metric {metric_name} cannot be updated! "
                f"Only constraint for metrics {[SUPPORTED_METRICS_MAP[i] for i in MODIFIABLE_METRICS]} can be updated."
            )
        if metric_type == dq_metric_pb.MetricDefinition.MetricType.NUMERIC_VALUE_IN_RANGE:
            if min_value is None or max_value is None:
                raise ValueError(
                    f"Please supply `min_value` and max_value` when updating {SUPPORTED_METRICS_MAP[dq_metric_pb.MetricDefinition.MetricType.NUMERIC_VALUE_IN_RANGE]}"
                )
        elif metric_type == dq_metric_pb.MetricDefinition.MetricType.UNIQUE_CATEGORICAL_VALUE:
            if categorical_values is None:
                raise ValueError(
                    f"Please supply `categorical_values` when updating {SUPPORTED_METRICS_MAP[dq_metric_pb.MetricDefinition.MetricType.UNIQUE_CATEGORICAL_VALUE]}"
                )
        return True

    def _create_value_constraint_for_metric(
        self,
        metric_type,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        categorical_values: Optional[Sequence] = None
    ) -> dq_metric_pb.MetricDefinition.ValueConstraint:
        if metric_type == dq_metric_pb.MetricDefinition.MetricType.NUMERIC_VALUE_IN_RANGE:
            return dq_metric_pb.MetricDefinition.ValueConstraint(
                numeric_range=dq_metric_pb.MetricDefinition.ValueConstraint.
                NumericRange(min_value=min_value, max_value=max_value)
            )

        elif metric_type == dq_metric_pb.MetricDefinition.MetricType.UNIQUE_CATEGORICAL_VALUE:
            return dq_metric_pb.MetricDefinition.ValueConstraint(
                allowed_string_values=categorical_values
            )
        raise ValueError(
            f"Creating value constraint for metric {metric_type} is unsupported!"
        )

    def update_data_quality_metric_constraint(
        self,
        project_id: str,
        data_collection_id: str,
        feature_name: str,
        metric_name: str,
        *,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        categorical_values: Optional[Sequence] = None
    ):
        self._validate_update_metric_constraint(
            metric_name, min_value, max_value, categorical_values
        )
        metric_type = METRICS_NAME_TO_TYPE.get(metric_name)
        value_constraint = self._create_value_constraint_for_metric(
            metric_type, min_value, max_value, categorical_values
        )
        rule_definition = self._get_data_quality_rule_definition(
            project_id, data_collection_id, feature_name, metric_name
        )
        new_metric_constraint = dq_pb.MetricDefinitionConstraint(
            scope_type=dq_metric_pb.MetricDefinition.ScopeType.COLUMN,
            column_name=feature_name,
            metric_type=METRICS_NAME_TO_TYPE.get(metric_name),
            updated_value_constraint=value_constraint
        )
        request = dq_pb.UpdateMetricDefinitionRequest(
            project_id=project_id,
            data_collection_id=data_collection_id,
            rule_id=rule_definition.rule_id,
            metric_id=rule_definition.metric_definition.metric_id,
            updated_constraint=new_metric_constraint
        )
        self.communicator.update_metric_definition(request)

    def _validate_update_rule_threshold_and_operator(
        self, violation_threshold: float, operator: str,
        treat_threshold_as_raw_count: bool
    ) -> bool:
        if treat_threshold_as_raw_count and not violation_threshold.is_integer(
        ):
            raise ValueError(
                f"Please provide integer `violation_threshold` when `treat_threshold_as_raw_count` is equal to `True`"
            )
        if operator not in SUPPORTED_RULE_THRESHOLD_OPERATORS:
            raise ValueError(
                f"Rule operator need to be one of {list(SUPPORTED_RULE_THRESHOLD_OPERATORS.keys())}. Supplied operator: {operator}"
            )
        if not treat_threshold_as_raw_count and (
            violation_threshold > 1 or violation_threshold < 0
        ):
            raise ValueError(
                f"`violation_threshold` need to be between `[0, 1]`"
            )

    def update_data_quality_rule_threshold_and_operator(
        self,
        project_id: str,
        data_collection_id: str,
        feature_name: str,
        metric_name: str,
        violation_threshold: float,
        operator: str,
        treat_threshold_as_raw_count: bool = False
    ):
        self._validate_metric_name(metric_name)
        self._validate_update_rule_threshold_and_operator(
            violation_threshold, operator, treat_threshold_as_raw_count
        )
        rule_definition = self._get_data_quality_rule_definition(
            project_id, data_collection_id, feature_name, metric_name
        )
        new_rule_constraint = dq_pb.RuleDefinitionConstraint(
            match_type=dq_rule_pb2.RuleDefinition.MatchType.VIOLATION_COUNT
            if treat_threshold_as_raw_count else
            dq_rule_pb2.RuleDefinition.MatchType.VIOLATION_RATIO,
            operator=SUPPORTED_RULE_THRESHOLD_OPERATORS[operator],
            violation_threshold=violation_threshold
        )
        request = dq_pb.UpdateRuleDefinitionRequest(
            project_id=project_id,
            data_collection_id=data_collection_id,
            rule_id=rule_definition.rule_id,
            updated_constraint=new_rule_constraint
        )
        self.communicator.update_rule_definition(request)

    def generate_rule_definition_from_split(
        self,
        project_id: str,
        data_collection_id: str,
        data_split_id: str,
        overwrite_existing_rule: bool = False
    ) -> None:
        request = dq_pb.GenerateRuleDefinitionFromSplitRequest(
            project_id=project_id,
            data_collection_id=data_collection_id,
            split_id=data_split_id,
            overwrite_existing_rule=overwrite_existing_rule
        )
        response = self.communicator.generate_rule_definition_from_split(
            request
        )
        if response.status == dq_pb.GenerateRuleDefinitionFromSplitResponse.Status.ERROR_RULES_EXIST:
            raise ValueError(
                f"{response.warning}. To overwrite, pass `overwrite_existing_rule=True`."
            )
        elif response.status != dq_pb.GenerateRuleDefinitionFromSplitResponse.Status.SUCCESS:
            raise RuntimeError(response.warning)

    def check_rule_definition_exists(
        self, project_id: str, data_collection_id: str
    ) -> bool:
        request = dq_pb.CheckRuleDefinitionExistsRequest(
            project_id=project_id, data_collection_id=data_collection_id
        )
        response = self.communicator.check_rule_definition_exists(request)
        return response.rules_exist

    def _validate_metric_name(self, metric_name: str) -> None:
        if not metric_name in METRICS_NAME_TO_TYPE:
            raise ValueError(
                f"Metric \"{metric_name}\" is not in list of supported metrics: {list(METRICS_NAME_TO_TYPE.keys())}."
            )
