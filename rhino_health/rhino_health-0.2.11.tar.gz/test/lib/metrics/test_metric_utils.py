import pytest

from rhino_health.lib.metrics.metric_utils import nested_metric_groups


class TestNestedMetricGroups:
    def tested_nested_groups_string_tuples(self):
        sample_result = {
            "('F', False)": {"count": 20},
            "('F', True)": {"count": 14},
            "('M', False)": {"count": 17},
            "('M', True)": {"count": 25},
        }
        nested_result = nested_metric_groups(sample_result)
        assert nested_result["F"][False] == sample_result["('F', False)"]
        assert nested_result["F"][True] == sample_result["('F', True)"]
        assert nested_result["M"][False] == sample_result["('M', False)"]
        assert nested_result["M"][True] == sample_result["('M', True)"]

    def tested_nested_groups_actual_tuples(self):
        sample_result = {
            ("F", False): {"count": 20},
            ("F", True): {"count": 14},
            ("M", False): {"count": 17},
            ("M", True): {"count": 25},
        }
        nested_result = nested_metric_groups(sample_result)
        assert nested_result["F"][False] == sample_result[("F", False)]
        assert nested_result["F"][True] == sample_result[("F", True)]
        assert nested_result["M"][False] == sample_result[("M", False)]
        assert nested_result["M"][True] == sample_result[("M", True)]

    def tested_nested_groups_single_group(self):
        sample_result = {
            "F": {"count": 20},
            "M": {"count": 17},
        }
        nested_result = nested_metric_groups(sample_result)
        assert nested_result == sample_result
