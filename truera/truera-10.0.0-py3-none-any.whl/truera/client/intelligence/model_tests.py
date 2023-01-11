from collections import namedtuple
import copy
from dataclasses import dataclass
from enum import Enum
import html
import json
import numbers
from string import Template
from typing import Any, Mapping, Optional, Sequence, Tuple, Union
import urllib.parse

from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import ParseDict
from requests.utils import requote_uri
from tabulate import tabulate

from truera.client.intelligence import viz
# pylint: disable=no-name-in-module
from truera.protobuf.public.modeltest.modeltest_pb2 import \
    TestThreshold as _PBTestThreshold
from truera.protobuf.public.modeltest.modeltest_service_pb2 import \
    FairnessTestResult as _PBFairnessTestResult
from truera.protobuf.public.modeltest.modeltest_service_pb2 import \
    PerformanceTestResult as _PBFeatureImportanceTestResult
from truera.protobuf.public.modeltest.modeltest_service_pb2 import \
    PerformanceTestResult as _PBPerformanceTestResult
from truera.protobuf.public.modeltest.modeltest_service_pb2 import \
    StabilityTestResult as _PBStabilityTestResult
from truera.protobuf.public.modeltest.modeltest_service_pb2 import \
    TestResultType as _PBTestResultType
from truera.protobuf.public.modeltest.modeltest_service_pb2 import \
    ThresholdResult as _PBThresholdResult

# pylint: enable=no-name-in-module

THRESHOLD_NOT_SPECIFIED = "Not specified"
RESULT_PENDING = "PENDING"
RESULT_NOT_AVAILABLE = "N/A"

_PERFORMANCE_TEST_COLUMN_NAMES = ["Name", "Split", "Segment", "Metric"]
_STABILITY_TEST_COLUMN_NAMES = [
    "Name", "Comparison Split", "Base Split", "Segment", "Metric"
]
_FAIRNESS_TEST_COLUMN_NAMES = [
    "Name", "Split", "Protected Segment", "Comparison Segment", "Metric"
]
_FEATURE_IMPORTANCE_TEST_COLUMN_NAMES = [
    "Name", "Split", "Segment", "Background Split Name",
    "Min. Importance Value", "Score Type"
]
_TEST_DEFINITIONS_COLUMN_NAMES = [
    "Description", "Warning Condition", "Fail Condition"
]
_TEST_RESULTS_COLUMN_NAMES = ["Score", "Navigate"]

_TEST_NAME_PERFORMANCE = "Performance Tests"
_TEST_NAME_FAIRNESS = "Fairness Tests"
_TEST_NAME_STABILITY = "Stability Tests"
_TEST_NAME_FEATURE_IMPORTANCE = "Feature Importance Tests"

# the id field here is used for ordering.
TestOutcome = namedtuple("Outcome", ["id", "emoji", "color"])


class ThresholdResult(Enum):
    FAILED = TestOutcome(0, "❌", "pink")
    WARNING = TestOutcome(1, "⚠️", "yellow")
    UNDEFINED = TestOutcome(2, "", "")
    PASSED = TestOutcome(3, "✅", "palegreen")


@dataclass
class ModelInfo:
    model_name: str
    model_id: str


class ModelTestDetails:
    STYLE_NOT_SPECIFIED = "notspecified"

    def __init__(self, model_tests: Sequence[Mapping]):
        self.model_tests = model_tests
        self._parsed_test_details = self._parse_model_tests()

    def as_dict(self):
        # Only returns "value" fields from each cells in _parsed_test_details
        test_details = copy.deepcopy(self._parsed_test_details)
        for test_type in test_details:
            test_details[test_type]["Rows"] = [
                [cell.value
                 for cell in row]
                for row in test_details[test_type]["Rows"]
            ]
        return test_details

    def as_json(self):
        return json.dumps(self.as_dict())

    def _repr_html_(self) -> str:
        css = Template(
            """
            .$notspecified {
                color: black;
                background-color: navajowhite
            }
            """
        ).substitute(notspecified=self.STYLE_NOT_SPECIFIED)
        html_str = ""
        for test_type, details in self._parsed_test_details.items():
            html_str += viz.custom_html_table(
                title=test_type,
                column_names=details["Column Names"],
                rows=details["Rows"],
                css=css
            )
        return html_str

    def pretty_print(self) -> None:
        print(self)

    def __str__(self) -> str:
        ret = ""
        test_details = self.as_dict()
        for test_type in test_details:
            ret += f"### {test_type} ###\n"
            ret += tabulate(
                test_details[test_type]["Rows"],
                headers=test_details[test_type]["Column Names"]
            )
            ret += "\n\n"
        return ret

    def _parse_model_tests(self) -> Mapping:
        # parse model_tests into more human readable elements along with appropriate css styling for each cells
        ret = {
            _TEST_NAME_PERFORMANCE:
                {
                    "Column Names":
                        _PERFORMANCE_TEST_COLUMN_NAMES +
                        _TEST_DEFINITIONS_COLUMN_NAMES
                },
            _TEST_NAME_STABILITY:
                {
                    "Column Names":
                        _STABILITY_TEST_COLUMN_NAMES +
                        _TEST_DEFINITIONS_COLUMN_NAMES
                },
            _TEST_NAME_FAIRNESS:
                {
                    "Column Names":
                        _FAIRNESS_TEST_COLUMN_NAMES +
                        _TEST_DEFINITIONS_COLUMN_NAMES
                },
            _TEST_NAME_FEATURE_IMPORTANCE:
                {
                    "Column Names":
                        _FEATURE_IMPORTANCE_TEST_COLUMN_NAMES +
                        _TEST_DEFINITIONS_COLUMN_NAMES
                }
        }
        for model_test_type in ret:
            ret[model_test_type]["Rows"] = []

        for i in self.model_tests:
            if "performance_test" in i:
                ret[_TEST_NAME_PERFORMANCE]["Rows"].append(
                    self._parse_performance_test(i)
                )
            elif "stability_test" in i:
                ret[_TEST_NAME_STABILITY]["Rows"].append(
                    self._parse_stability_test(i)
                )
            elif "fairness_test" in i:
                ret[_TEST_NAME_FAIRNESS]["Rows"].append(
                    self._parse_fairness_test(i)
                )
            elif "feature_importance_test" in i:
                ret[_TEST_NAME_FEATURE_IMPORTANCE]["Rows"].append(
                    self._parse_feature_importance_test(i)
                )
            else:
                raise ValueError(f"Unknown test type! Given: {i} ")
        return ret

    def _parse_performance_test(self,
                                model_test: Mapping) -> Sequence[viz.TableCell]:
        metric_name = model_test["performance_test"][
            "performance_metric_and_threshold"]["accuracy_type"]
        additional_column_entries = [
            model_test["segment_id"].get("segment_desc"), metric_name,
            model_test["description"]
        ]
        return self._parse_generic_test(
            name=model_test["test_name"],
            split_name=model_test["split_name"],
            options_and_threshold=model_test["performance_test"]
            ["performance_metric_and_threshold"],
            score_name=metric_name,
            additional_column_entries=additional_column_entries
        )

    def _parse_stability_test(self,
                              model_test: Mapping) -> Sequence[viz.TableCell]:
        base_split_name = model_test["stability_test"]["base_split_name"
                                                      ] or "MODEL_TRAIN_SPLIT"
        metric_name = model_test["stability_test"][
            "stability_metric_and_threshold"]["distance_type"]
        additional_column_entries = [
            base_split_name, model_test["segment_id"].get("segment_desc"),
            metric_name, model_test["description"]
        ]
        return self._parse_generic_test(
            name=model_test["test_name"],
            split_name=model_test["split_name"],
            options_and_threshold=model_test["stability_test"]
            ["stability_metric_and_threshold"],
            score_name=metric_name,
            additional_column_entries=additional_column_entries
        )

    def _parse_fairness_test(self,
                             model_test: Mapping) -> Sequence[viz.TableCell]:
        metric_name = model_test["fairness_test"][
            "fairness_metric_and_threshold"]["bias_type"]
        additional_column_entries = [
            model_test["fairness_test"]
            ["segment_id_protected"].get("segment_desc"),
            model_test["fairness_test"]
            ["segment_id_comparison"].get("segment_desc"), metric_name,
            model_test["description"]
        ]
        return self._parse_generic_test(
            name=model_test["test_name"],
            split_name=model_test["split_name"],
            options_and_threshold=model_test["fairness_test"]
            ["fairness_metric_and_threshold"],
            score_name=metric_name,
            additional_column_entries=additional_column_entries
        )

    def _parse_feature_importance_test(
        self, model_test: Mapping
    ) -> Sequence[viz.TableCell]:
        score_type = model_test["feature_importance_test"][
            "options_and_threshold"]["score_type"]
        # convert thresholds to int
        for threshold_item in ["threshold_warning", "threshold_fail"]:
            if model_test["feature_importance_test"]["options_and_threshold"][
                threshold_item]["threshold_type"
                               ] != _PBTestThreshold.ThresholdType.Name(
                                   _PBTestThreshold.UNDEFINED
                               ):
                model_test["feature_importance_test"]["options_and_threshold"][
                    threshold_item]["value"]["value"] = int(
                        model_test["feature_importance_test"]
                        ["options_and_threshold"][threshold_item]["value"]
                        ["value"]
                    )
        additional_column_entries = [
            model_test["segment_id"].get("segment_desc"),
            model_test["feature_importance_test"].get("background_split_name"),
            model_test["feature_importance_test"]["options_and_threshold"]
            ["min_importance_value"], score_type, model_test["description"]
        ]
        return self._parse_generic_test(
            name=model_test["test_name"],
            split_name=model_test["split_name"],
            options_and_threshold=model_test["feature_importance_test"]
            ["options_and_threshold"],
            score_name="Num. features with low importance",
            additional_column_entries=additional_column_entries
        )

    def _parse_generic_test(
        self, name: str, split_name: str, options_and_threshold: Mapping,
        score_name: str, additional_column_entries: Sequence[str]
    ) -> Sequence[viz.TableCell]:
        ret = [
            viz.TableCell(value=name),
            viz.TableCell(value=split_name),
            *[viz.TableCell(curr) for curr in additional_column_entries]
        ]
        for threshold_item in ["threshold_warning", "threshold_fail"]:
            stringified_threshold = _stringify_test_threshold(
                metric_name=score_name,
                threshold_details=options_and_threshold.get(
                    threshold_item,
                    MessageToDict(
                        _PBTestThreshold(),
                        including_default_value_fields=True,
                        preserving_proto_field_name=True
                    )
                )
            )
            ret.append(
                viz.TableCell(
                    value=stringified_threshold,
                    html_class=self.STYLE_NOT_SPECIFIED if stringified_threshold
                    == THRESHOLD_NOT_SPECIFIED else None
                )
            )
        return ret


class ModelTestResults:
    SPLIT_PERFORMANCE_PAGE_URL = Template(
        "$connection_string/p/$project_name/m/$model_name/t/performance?splitId=$split_id"
    )
    SPLIT_STABILITY_PAGE_URL = Template(
        "$connection_string/p/$project_name/m/$model_name/t/stability?baseSplitName=$base_split_name&compareSplitName=$compare_split_name&splitId=$split_id"
    )
    SPLIT_SINGLE_SEGMENT_FAIRNESS_PAGE_URL = Template(
        "$connection_string/p/$project_name/m/$model_name"
        "/t/fairness/t/fairness-analysis"
        "?biasSegmentIdJSON={\"segmentationId\":\"$segmentation_id\",\"segmentIndex\":$protected_segment_index}"
        "&splitId=$split_id"
    )
    SPLIT_FAIRNESS_PAGE_URL = Template(
        "$connection_string/p/$project_name/m/$model_name"
        "/t/fairness/t/fairness-analysis"
        "?biasSegmentIdJSON={\"segmentationId\":\"$segmentation_id\",\"segmentIndex\":$protected_segment_index}"
        "&compareSegmentIdJSON={\"segmentationId\":\"$segmentation_id\",\"segmentIndex\":$comparison_segment_index}"
        "&splitId=$split_id"
    )
    SPLIT_FEATURES_PAGE_URL = Template(
        "$connection_string/p/$project_name/m/$model_name"
        "/t/features/t/features-all?splitId=$split_id"
    )
    SEGMENT_URL = Template(
        "segmentLocations=[{\"segmentationId\":\"$segmentation_id\",\"index\":$segment_index}]"
    )

    def __init__(
        self,
        project_name: str,
        model_name: str,
        model_id: str,
        model_test_results: Mapping[str, Sequence[Mapping]],
        model_test_types: Sequence[str],
        connection_string: str,
        comparison_models: Optional[Sequence[Mapping[str, str]]] = None,
        comparison_models_test_results: Optional[Sequence[Mapping[
            str, Sequence[Mapping]]]] = None
    ):
        self.project_name = project_name
        self.model_info = ModelInfo(model_name, model_id)
        self.model_test_results = model_test_results
        self.model_test_types = model_test_types
        self.comparison_models = comparison_models if comparison_models else []
        self.comparison_models_test_results = comparison_models_test_results if comparison_models_test_results else []
        self.connection_string = connection_string
        self._parsed_test_results = self._parse_model_test_results()

    def as_dict(self):
        test_results = copy.deepcopy(self._parsed_test_results)
        for test_type in test_results:
            # Name the enum (first) column and remove the navigation (last) column
            test_results[test_type]["Column Names"][0] = "Outcome"
            test_results[test_type]["Column Names"] = test_results[test_type][
                "Column Names"][:-1]
            score_column_index = test_results[test_type]["Column Names"].index(
                "Score"
            )
            # Convert the first column into human readable outcome (stored as "html_class" in the "Score" column)
            for row in test_results[test_type]["Rows"]:
                row[0].value = row[score_column_index].html_class
            test_results[test_type]["Rows"] = [
                [cell.value
                 for cell in row[:-1]]
                for row in test_results[test_type]["Rows"]
            ]
        return test_results

    def as_json(self):
        return json.dumps(self.as_dict())

    def _repr_html_(self) -> str:
        css = Template(
            """
            .$passed {
                color: black;
                background-color: $color_passed;
            }
            .$warning {
                color: black;
                background-color: $color_warning;
            }
            .$failed {
                color: black;
                background-color: $color_failed;
            }
            """
        ).substitute(
            passed=ThresholdResult.PASSED.name,
            color_passed=ThresholdResult.PASSED.value.color,
            warning=ThresholdResult.WARNING.name,
            color_warning=ThresholdResult.WARNING.value.color,
            failed=ThresholdResult.FAILED.name,
            color_failed=ThresholdResult.FAILED.value.color
        )
        html_str = ""
        for test_type, details in self._parsed_test_results.items():
            html_str += viz.custom_html_table(
                title=
                f"{test_type} Results for Model \"{self.model_info.model_name}\"",
                column_names=details["Column Names"],
                rows=details["Rows"],
                css=css
            )
        return html_str

    def pretty_print(self) -> None:
        print(self)

    def __str__(self) -> str:
        test_results = self.as_dict()
        ret = ""
        for test_type in test_results:
            ret += f"### {test_type} ###\n"
            ret += tabulate(
                test_results[test_type]["Rows"],
                headers=test_results[test_type]["Column Names"]
            )
            ret += "\n\n"
        return ret

    def _parse_model_test_results(self) -> Mapping:
        # parse model_tests into more human readable elements along with appropriate css styling for each cells
        comparison_models_column_names = [
            f"Score diff ({model['name']})" for model in self.comparison_models
        ]
        ret = {}
        if "performance" in self.model_test_types:
            ret[_TEST_NAME_PERFORMANCE] = {
                "Column Names":
                    ["Test ID", ""] + _PERFORMANCE_TEST_COLUMN_NAMES +
                    _TEST_RESULTS_COLUMN_NAMES
            }
        if "stability" in self.model_test_types:
            ret[_TEST_NAME_STABILITY] = {
                "Column Names":
                    ["Test ID", ""] + _STABILITY_TEST_COLUMN_NAMES +
                    _TEST_RESULTS_COLUMN_NAMES
            }
        if "fairness" in self.model_test_types:
            ret[_TEST_NAME_FAIRNESS] = {
                "Column Names":
                    ["Test ID", ""] + _FAIRNESS_TEST_COLUMN_NAMES +
                    _TEST_RESULTS_COLUMN_NAMES
            }
        if "feature_importance" in self.model_test_types:
            ret[_TEST_NAME_FEATURE_IMPORTANCE] = {
                "Column Names":
                    ["Test ID", ""] + _FEATURE_IMPORTANCE_TEST_COLUMN_NAMES +
                    _TEST_RESULTS_COLUMN_NAMES
            }
        self._parse_all_test_results(
            self.model_test_results, self.model_test_types, ret
        )

        comparison_models_test_id_to_result = []
        if self.comparison_models_test_results:
            for test_results in self.comparison_models_test_results:
                parsed_results = {
                    test_type: {
                        "Column Names": ret[test_type]["Column Names"]
                    } for test_type in ret
                }
                test_id_to_result = self._parse_all_test_results(
                    test_results, self.model_test_types, parsed_results
                )
                comparison_models_test_id_to_result.append(test_id_to_result)
        self._add_comparison_models_details_and_drop_test_id(
            parsed_test_results=ret,
            comparison_model_ids=[i["id"] for i in self.comparison_models],
            comparison_models_column_names=comparison_models_column_names,
            comparison_models_test_id_to_result=
            comparison_models_test_id_to_result
        )
        for test_type in ret:
            score_column_index = ret[test_type]["Column Names"].index("Score")
            ret[test_type]["Rows"] = sorted(
                ret[test_type]["Rows"],
                key=lambda i: i[score_column_index].sort_order
            )
        return ret

    def _add_comparison_models_details_and_drop_test_id(
        self, parsed_test_results: Mapping, comparison_model_ids: Sequence[str],
        comparison_models_column_names: Sequence[str],
        comparison_models_test_id_to_result: Sequence[Mapping[str,
                                                              viz.TableCell]]
    ) -> None:
        # Insert comparison columns into `parsed_test_results`
        for test_type in parsed_test_results:
            score_column_index = parsed_test_results[test_type]["Column Names"
                                                               ].index("Score")
            outcome_column_index = parsed_test_results[test_type]["Column Names"
                                                                 ].index("")
            navigate_column_index = parsed_test_results[test_type][
                "Column Names"].index("Navigate")
            # Update the table headers
            parsed_test_results[test_type][
                "Column Names"
            ] = parsed_test_results[test_type]["Column Names"][
                1:-1] + comparison_models_column_names + parsed_test_results[
                    test_type]["Column Names"][-1:]
            # Update content for each rows
            for i in range(len(parsed_test_results[test_type]["Rows"])):
                # Update navigation URL to accommodate multiple models
                parsed_test_results[test_type]["Rows"][
                    i][navigate_column_index
                      ].url += f"&modelIds={self.model_info.model_id}"
                parsed_test_results[test_type]["Rows"][i][
                    navigate_column_index].url += "&" + "&".join(
                        [f"modelIds={i}" for i in comparison_model_ids]
                    )
                unique_identifer_of_result = self._get_unique_identifier_of_test_result(
                    test_type, parsed_test_results[test_type]["Rows"][i]
                )
                base_model_score = parsed_test_results[test_type]["Rows"][i][
                    score_column_index].value
                # base_model_score can be either the score (float) or RESULT_PENDING if waiting for computation
                base_result_available = isinstance(
                    base_model_score, numbers.Number
                )
                comparison_results = []
                for test_id_to_result in comparison_models_test_id_to_result:
                    test_result = test_id_to_result.get(
                        unique_identifer_of_result
                    )
                    if test_result is not None:
                        # test_result[score_column_index].value can be either the score (float) or RESULT_PENDING if waiting for computation
                        comparison_model_score = test_result[score_column_index
                                                            ].value
                        comparison_result_available = isinstance(
                            comparison_model_score, numbers.Number
                        )
                        both_results_available = base_result_available and comparison_result_available
                    else:
                        both_results_available = False
                        comparison_result_available = False
                        comparison_model_score = RESULT_NOT_AVAILABLE
                    diff = viz.TableCell(
                        value=comparison_model_score - base_model_score
                        if both_results_available else comparison_model_score,
                        html_class=test_result[score_column_index].html_class
                        if comparison_result_available else None,
                        is_diff=True,
                        value_suffix=test_result[outcome_column_index].value
                        if comparison_result_available else None
                    )
                    comparison_results.append(diff)
                parsed_test_results[test_type]["Rows"][
                    i] = parsed_test_results[test_type]["Rows"][i][
                        1:-1] + comparison_results + parsed_test_results[
                            test_type]["Rows"][i][-1:]

    def _parse_all_test_results(
        self, test_results: Mapping, test_types: Sequence[str],
        parsed_results: Mapping
    ) -> Mapping[str, viz.TableCell]:
        pending_test_ids = []
        if "pending_test_results" in test_results:
            pending_test_ids = test_results["pending_test_results"][
                "pending_test_ids"]
        # parse `test_results` and store it in `parsed_results`. In addition, return a mapping between test id and test outcome
        if "performance" in test_types:
            parsed_results[_TEST_NAME_PERFORMANCE]["Rows"] = [
                self._parse_performance_test_result(
                    i, pending_test_ids=pending_test_ids
                ) for i in test_results["performance_test_results"]
            ]
        if "stability" in test_types:
            parsed_results[_TEST_NAME_STABILITY]["Rows"] = [
                self._parse_stability_test_result(
                    i, pending_test_ids=pending_test_ids
                ) for i in test_results["stability_test_results"]
            ]
        if "fairness" in test_types:
            parsed_results[_TEST_NAME_FAIRNESS]["Rows"] = [
                self._parse_fairness_test_result(
                    i, pending_test_ids=pending_test_ids
                ) for i in test_results["fairness_test_results"]
            ]
        if "feature_importance" in test_types:
            parsed_results[_TEST_NAME_FEATURE_IMPORTANCE]["Rows"] = [
                self._parse_feature_importance_test_result(
                    i, pending_test_ids=pending_test_ids
                ) for i in test_results["feature_importance_test_results"]
            ]

        test_id_to_result = {}
        for test_type in parsed_results:
            for test_result in parsed_results[test_type]["Rows"]:
                unique_identifer_of_result = self._get_unique_identifier_of_test_result(
                    test_type, test_result
                )
                test_id_to_result[unique_identifer_of_result] = test_result
        return test_id_to_result

    def _get_unique_identifier_of_test_result(
        self, test_type: str, test_result: Sequence
    ) -> Tuple:
        if test_type == _TEST_NAME_PERFORMANCE:
            unique_identifer_of_result = [
                test_result[i].value
                for i in range(2, len(_PERFORMANCE_TEST_COLUMN_NAMES))
            ]
        elif test_type == _TEST_NAME_STABILITY:
            unique_identifer_of_result = [
                test_result[i].value
                for i in range(2, len(_STABILITY_TEST_COLUMN_NAMES))
            ]
        elif test_type == _TEST_NAME_FAIRNESS:
            unique_identifer_of_result = [
                test_result[i].value
                for i in range(2, len(_FAIRNESS_TEST_COLUMN_NAMES))
            ]
        elif test_type == _TEST_NAME_FEATURE_IMPORTANCE:
            unique_identifer_of_result = [
                test_result[i].value
                for i in range(2, len(_FEATURE_IMPORTANCE_TEST_COLUMN_NAMES))
            ]
        else:
            raise ValueError(f"Unexpected test type: {test_type}")
        unique_identifer_of_result.append(test_result[0].value)
        return tuple(unique_identifer_of_result)

    def _parse_performance_test_result(
        self, test_result: Mapping, pending_test_ids: Sequence[str]
    ) -> Sequence[viz.TableCell]:
        model_test = test_result["test_details"]
        metric_name = model_test["performance_test"][
            "performance_metric_and_threshold"]["accuracy_type"]
        test_outcome = self._determine_test_outcome(
            test_result,
            _PBPerformanceTestResult,
            pending_test_ids=pending_test_ids
        )

        url = self.SPLIT_PERFORMANCE_PAGE_URL.substitute(
            connection_string=self.connection_string,
            project_name=self.project_name,
            model_name=self.model_info.model_name,
            split_id=model_test["split_id"]
        )
        url = self._append_segment_to_url(model_test, url)
        additional_column_entries = [
            model_test["segment_id"].get("segment_desc")
        ]
        return self._parse_generic_test_result(
            model_test["id"], test_result, model_test, metric_name,
            test_outcome, url, additional_column_entries
        )

    def _parse_stability_test_result(
        self, test_result: Mapping, pending_test_ids: Sequence[str]
    ) -> Sequence[viz.TableCell]:
        model_test = test_result["test_details"]
        metric_name = model_test["stability_test"][
            "stability_metric_and_threshold"]["distance_type"]
        test_outcome = self._determine_test_outcome(
            test_result,
            _PBStabilityTestResult,
            pending_test_ids=pending_test_ids
        )

        url = self.SPLIT_STABILITY_PAGE_URL.substitute(
            connection_string=self.connection_string,
            project_name=self.project_name,
            model_name=self.model_info.model_name,
            split_id=model_test["split_id"],
            compare_split_name=model_test["split_name"],
            base_split_name=model_test["stability_test"]["base_split_name"],
        )
        url = self._append_segment_to_url(model_test, url)
        base_split_name = model_test["stability_test"]["base_split_name"
                                                      ] or "MODEL_TRAIN_SPLIT"
        additional_column_entries = [
            base_split_name, model_test["segment_id"].get("segment_desc")
        ]
        return self._parse_generic_test_result(
            model_test["id"], test_result, model_test, metric_name,
            test_outcome, url, additional_column_entries
        )

    def _parse_fairness_test_result(
        self, test_result: Mapping, pending_test_ids: Sequence[str]
    ) -> Sequence[viz.TableCell]:
        model_test = test_result["test_details"]
        metric_name = model_test["fairness_test"][
            "fairness_metric_and_threshold"]["bias_type"]
        test_outcome = self._determine_test_outcome(
            test_result,
            _PBFairnessTestResult,
            pending_test_ids=pending_test_ids
        )
        segmentation_id = model_test["fairness_test"]["segment_id_protected"][
            "segmentation_id"]
        protected_segment_index = model_test["fairness_test"][
            "segment_id_protected"].get("segment_index")
        comparison_segment_index = model_test["fairness_test"][
            "segment_id_comparison"].get("segment_index")

        if model_test["fairness_test"]["segment_id_comparison"]["segment_name"]:
            url = self.SPLIT_FAIRNESS_PAGE_URL.substitute(
                connection_string=self.connection_string,
                project_name=self.project_name,
                model_name=self.model_info.model_name,
                segmentation_id=segmentation_id,
                protected_segment_index=protected_segment_index,
                comparison_segment_index=comparison_segment_index,
                split_id=model_test["split_id"]
            )
        else:
            url = self.SPLIT_SINGLE_SEGMENT_FAIRNESS_PAGE_URL.substitute(
                connection_string=self.connection_string,
                project_name=self.project_name,
                model_name=self.model_info.model_name,
                segmentation_id=segmentation_id,
                protected_segment_index=protected_segment_index,
                split_id=model_test["split_id"]
            )
        url = requote_uri(url)
        additional_column_entries = [
            model_test["fairness_test"]
            ["segment_id_protected"].get("segment_desc"),
            model_test["fairness_test"]
            ["segment_id_comparison"].get("segment_desc")
        ]
        return self._parse_generic_test_result(
            model_test["id"], test_result, model_test, metric_name,
            test_outcome, url, additional_column_entries
        )

    def _parse_feature_importance_test_result(
        self, test_result: Mapping, pending_test_ids: Sequence[str]
    ) -> Sequence[viz.TableCell]:
        model_test = test_result["test_details"]
        score_type = model_test["feature_importance_test"][
            "options_and_threshold"]["score_type"]
        test_outcome = self._determine_test_outcome(
            test_result,
            _PBFeatureImportanceTestResult,
            pending_test_ids=pending_test_ids
        )
        url = self.SPLIT_FEATURES_PAGE_URL.substitute(
            connection_string=self.connection_string,
            project_name=self.project_name,
            model_name=self.model_info.model_name,
            split_id=model_test["split_id"]
        )
        url = self._append_segment_to_url(model_test, url)
        additional_column_entries = [
            model_test["segment_id"].get("segment_desc"),
            model_test["feature_importance_test"].get("background_split_name"),
            model_test["feature_importance_test"]["options_and_threshold"]
            ["min_importance_value"],
        ]
        return self._parse_generic_test_result(
            model_test["id"],
            test_result,
            model_test,
            score_type,
            test_outcome,
            url,
            additional_column_entries,
            score_key="num_features_below_importance_threshold"
        )

    def _append_segment_to_url(
        self, model_test: Mapping[str, Any], url: str
    ) -> str:
        if model_test["segment_id"]["segmentation_id"]:
            segment_url = urllib.parse.quote(
                self.SEGMENT_URL.substitute(
                    segmentation_id=model_test["segment_id"]["segmentation_id"],
                    segment_index=model_test["segment_id"].get("segment_index")
                ),
                safe="="
            )
            url = f"{url}&{segment_url}"
        return url

    def _parse_generic_test_result(
        self,
        test_id: str,
        test_result: Mapping[str, Any],
        model_test: Mapping[str, Any],
        metric_name: str,
        test_outcome: ThresholdResult,
        url: str,
        additional_column_entries: Sequence[Any],
        score_key: str = "metric_result"
    ) -> Sequence[viz.TableCell]:
        additional_column_entries = [
            viz.TableCell(curr) for curr in additional_column_entries
        ]
        return [
            viz.TableCell(value=test_id),
            viz.TableCell(value=test_outcome.value.emoji),
            viz.TableCell(value=model_test["test_name"]),
            viz.TableCell(value=model_test["split_name"]),
            *additional_column_entries,
            viz.TableCell(value=metric_name),
            viz.TableCell(
                value=test_result[score_key],
                html_class=test_outcome.name,
                sort_order=test_outcome.value.id
            ),
            viz.TableCell(value="Explore in UI", url=url)
        ]

    def _determine_test_outcome(
        self, test_result: Mapping,
        message_class: Union[_PBFairnessTestResult, _PBPerformanceTestResult,
                             _PBStabilityTestResult],
        pending_test_ids: Sequence[str]
    ) -> ThresholdResult:
        test_outcome = ThresholdResult.UNDEFINED
        if test_result["test_details"]["id"] in pending_test_ids:
            test_result["metric_result"] = RESULT_PENDING
            return test_outcome
        elif test_result["result_type"] != _PBTestResultType.Name(
            _PBTestResultType.VALUE
        ):
            test_result["metric_result"] = RESULT_NOT_AVAILABLE
            return test_outcome
        test_result = ParseDict(
            test_result, message_class(), ignore_unknown_fields=True
        )
        if test_result.warning_result == _PBThresholdResult.THRESHOLD_RESULT_FAIL:
            if test_result.pass_fail_result == _PBThresholdResult.THRESHOLD_RESULT_FAIL:
                test_outcome = ThresholdResult.FAILED
            else:
                test_outcome = ThresholdResult.WARNING
        else:
            if test_result.pass_fail_result == _PBThresholdResult.THRESHOLD_RESULT_FAIL:
                test_outcome = ThresholdResult.FAILED
            elif test_result.pass_fail_result == _PBThresholdResult.THRESHOLD_RESULT_PASS:
                test_outcome = ThresholdResult.PASSED
        return test_outcome


def _stringify_test_threshold(
    metric_name: str,
    threshold_details: Mapping,
) -> str:
    threshold_type = threshold_details["threshold_type"]
    if threshold_type == _PBTestThreshold.ThresholdType.Name(
        _PBTestThreshold.UNDEFINED
    ):
        return THRESHOLD_NOT_SPECIFIED

    elif threshold_type == _PBTestThreshold.ThresholdType.Name(
        _PBTestThreshold.ABSOLUTE_SINGLE_VALUE
    ):
        # pylint: disable=protobuf-undefined-attribute
        if _PBTestThreshold.ThresholdValue.ThresholdCondition.__getattr__(
            threshold_details["value"]["condition"]
        ) == _PBTestThreshold.ThresholdValue.WARN_OR_FAIL_IF_LESS_THAN:
            return f"{metric_name} < {threshold_details['value']['value']}"
        return f"{metric_name} > {threshold_details['value']['value']}"

    elif threshold_type == _PBTestThreshold.ThresholdType.Name(
        _PBTestThreshold.ABSOLUTE_VALUE_RANGE
    ):
        # pylint: disable=protobuf-undefined-attribute
        if _PBTestThreshold.ThresholdValueRange.ThresholdCondition.__getattr__(
            threshold_details["value_range"]["condition"]
        ) == _PBTestThreshold.ThresholdValueRange.WARN_OR_FAIL_IF_WITHIN:
            return f"{threshold_details['value_range']['lower_bound']} < {metric_name} < {threshold_details['value_range']['upper_bound']}"
        return f"{metric_name} < {threshold_details['value_range']['lower_bound']} OR {metric_name} > {threshold_details['value_range']['upper_bound']}"

    elif threshold_type == _PBTestThreshold.ThresholdType.Name(
        _PBTestThreshold.RELATIVE_SINGLE_VALUE
    ):
        reference_name = _resolve_threshold_reference_name(threshold_details)
        sign = "+" if threshold_details["value"]["value"] >= 0 else "-"
        stringified_threshold_value = f"{reference_name} score"
        if abs(threshold_details['value']['value']) != 0:
            stringified_threshold_value += f" {sign} {abs(threshold_details['value']['value'])}"
        # pylint: disable=protobuf-undefined-attribute
        if _PBTestThreshold.ThresholdValue.ThresholdCondition.__getattr__(
            threshold_details["value"]["condition"]
        ) == _PBTestThreshold.ThresholdValue.WARN_OR_FAIL_IF_LESS_THAN:
            return f"{metric_name} < {stringified_threshold_value}"
        return f"{metric_name} > {stringified_threshold_value}"
    # threshold is RELATIVE_VALUE_RANGE
    reference_name = _resolve_threshold_reference_name(threshold_details)
    sign_lb = "+" if threshold_details["value_range"]["lower_bound"
                                                     ] >= 0 else "-"
    sign_ub = "+" if threshold_details["value_range"]["upper_bound"
                                                     ] >= 0 else "-"
    stringified_lower_bound = f"{reference_name} score {sign_lb} {abs(threshold_details['value_range']['lower_bound'])}"
    stringified_upper_bound = f"{reference_name} score {sign_ub} {abs(threshold_details['value_range']['upper_bound'])}"
    # pylint: disable=protobuf-undefined-attribute
    if _PBTestThreshold.ThresholdValueRange.ThresholdCondition.__getattr__(
        threshold_details["value_range"]["condition"]
    ) == _PBTestThreshold.ThresholdValueRange.WARN_OR_FAIL_IF_WITHIN:
        return f"{stringified_lower_bound} < {metric_name} < {stringified_upper_bound}"
    return f"{metric_name} < {stringified_lower_bound} OR {metric_name} > {stringified_upper_bound}"


def _resolve_threshold_reference_name(threshold_details: Mapping):
    reference_split_name = threshold_details.get("reference_split_name")
    reference_model_name = threshold_details.get("reference_model_name")
    if reference_split_name and reference_model_name:
        return f"model \"{reference_model_name}\" on \"{reference_split_name}\""
    elif reference_model_name:
        return f"model \"{reference_model_name}\""
    elif reference_split_name:
        return f"split \"{reference_split_name}\""
    return "MODEL_TRAIN_SPLIT"


class ModelTestLeaderboard:

    def __init__(
        self, test_results: Mapping[str, ModelTestResults],
        models_metadata: Mapping[str, Mapping], data_collection_name: str,
        sort_by: str
    ):
        self.models_metadata = models_metadata
        self.test_summary = self._convert_test_results_to_summary(
            test_results, models_metadata, sort_by
        )
        self.title = f"Test Leaderboard of Models in Data Collection \"{data_collection_name}\""

    def _convert_test_results_to_summary(
        self, test_results: Mapping[str, ModelTestResults],
        models_metadata: Mapping[str, Mapping], sort_by: str
    ) -> Mapping[str, Sequence]:
        ret = {
            "Column Names":
                [
                    "Model Name", "Train Split Name", "Train Parameters",
                    f"{_TEST_NAME_PERFORMANCE} (Failed/Warning/Total)",
                    f"{_TEST_NAME_FAIRNESS} (Failed/Warning/Total)",
                    f"{_TEST_NAME_STABILITY} (Failed/Warning/Total)",
                    f"{_TEST_NAME_FEATURE_IMPORTANCE} (Failed/Warning/Total)"
                ],
            "Rows": []
        }
        for model_name in test_results:
            test_outcomes = self._tally_test_outcomes(test_results[model_name])
            train_split_name = models_metadata[model_name][
                "training_metadata"].get('train_split_name')
            train_parameters = models_metadata[model_name]["training_metadata"
                                                          ].get('parameters')
            if not train_split_name:
                train_split_name = "Unspecified"

            if not train_parameters:
                train_parameters = "Unspecified"
            ret["Rows"].append(
                [
                    model_name, train_split_name, train_parameters,
                    test_outcomes[_TEST_NAME_PERFORMANCE],
                    test_outcomes[_TEST_NAME_FAIRNESS],
                    test_outcomes[_TEST_NAME_STABILITY],
                    test_outcomes[_TEST_NAME_FEATURE_IMPORTANCE]
                ]
            )
        sort_by_to_column_index = {
            "performance": 3,
            "fairness": 4,
            "stability": 5,
            "feature_importance": 6
        }

        def sort_outcome(x):
            if x[sort_by_to_column_index[sort_by]][ThresholdResult.FAILED.name
                                                  ] == RESULT_PENDING:
                return (float('inf'),)
            return x[sort_by_to_column_index[sort_by]][
                ThresholdResult.FAILED.name
            ], x[sort_by_to_column_index[sort_by]][ThresholdResult.WARNING.name]

        ret["Rows"] = sorted(ret["Rows"], key=sort_outcome)
        return ret

    def _tally_test_outcomes(self, model_test_results: ModelTestResults):
        ret = {}
        model_test_results = model_test_results.as_dict()
        for test_type in model_test_results:
            outcome_column_index = model_test_results[test_type][
                "Column Names"].index("Outcome")
            score_column_index = model_test_results[test_type]["Column Names"
                                                              ].index("Score")
            if test_type not in ret:
                ret[test_type] = {i: 0 for i in ThresholdResult.__members__}
                ret[test_type]["TOTAL"] = 0
            for test_result in model_test_results[test_type]["Rows"]:
                if test_result[score_column_index] == RESULT_PENDING:
                    for i in ret[test_type]:
                        ret[test_type][i] = RESULT_PENDING
                    break
                ret[test_type][test_result[outcome_column_index]] += 1
                ret[test_type]["TOTAL"] += 1
        return ret

    def as_dict(self):
        return copy.deepcopy(self.test_summary)

    def as_json(self):
        return json.dumps(self.as_dict())

    def _repr_html_(self) -> str:

        def _stringify_train_parameters(train_parameters: Union[str, Mapping]):
            if isinstance(train_parameters, str):
                return train_parameters
            items = list(train_parameters.items())
            items.sort()
            return "<br>".join([html.escape(f"{i[0]}: {i[1]}") for i in items])

        rows = []
        for i in self.test_summary["Rows"]:
            rows.append(
                [
                    viz.TableCell(value=i[0]),
                    viz.TableCell(value=i[1]),
                    viz.TableCell(value=_stringify_train_parameters(i[2])),
                    viz.TableCell(value=self._stringify_tally(i[3])),
                    viz.TableCell(value=self._stringify_tally(i[4])),
                    viz.TableCell(value=self._stringify_tally(i[5])),
                    viz.TableCell(value=self._stringify_tally(i[6]))
                ]
            )
        html_str = viz.custom_html_table(
            title=self.title,
            column_names=self.test_summary["Column Names"],
            rows=rows
        )
        return html_str

    def pretty_print(self) -> None:
        print(self)

    def __str__(self) -> str:
        rows = []
        for i in self.test_summary["Rows"]:
            rows.append(
                [
                    i[0],
                    i[1],
                    i[2],
                    self._stringify_tally(i[3]),
                    self._stringify_tally(i[4]),
                    self._stringify_tally(i[5]),
                ]
            )
        ret = f"### {self.title} ###"
        ret += tabulate(rows, headers=self.test_summary["Column Names"])
        return ret

    def _stringify_tally(self, test_outcome: Union[str, Mapping]):
        if isinstance(test_outcome, str):
            return test_outcome
        return f"{test_outcome[ThresholdResult.FAILED.name]} {ThresholdResult.FAILED.value.emoji} / {test_outcome[ThresholdResult.WARNING.name]} {ThresholdResult.WARNING.value.emoji} / {test_outcome['TOTAL']}"
