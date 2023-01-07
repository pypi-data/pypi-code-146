import pytest

from rhino_health.lib.metrics.aggregate_metrics import calculate_aggregate_metric
from rhino_health.lib.metrics.basic import Count, Mean


class TestWeightedAverage:
    def test_group_by(self):
        sample_result = [
            {
                "m": {"variable_count": 20, "mean": 100},
                "f": {"variable_count": 10, "mean": 100},
                "o": {"variable_count": 20, "mean": 50},
            },
            {"m": {"variable_count": 80, "mean": 0}, "f": {"variable_count": 90, "mean": 0}},
        ]
        metric_configuration = Mean(
            variable="fake_variable",
            group_by={"groupings": ["Gender"]},
        )
        aggregate_results = calculate_aggregate_metric(metric_configuration, sample_result)
        assert aggregate_results["m"]["mean"] == 20
        assert aggregate_results["f"]["mean"] == 10
        assert aggregate_results["o"]["mean"] == 50

    def test_no_group_by(self):
        sample_result = [
            {"variable_count": 20, "mean": 100},
            {"variable_count": 80, "mean": 0},
            {"error": "mean fails data anonymization requirements"},
        ]
        metric_configuration = Mean(
            variable="fake_variable",
        )
        aggregate_results = calculate_aggregate_metric(metric_configuration, sample_result)
        assert aggregate_results["mean"] == 20


class TestCount:
    def test_group_by(self):
        sample_result = [
            {"m": {"count": 70}, "f": {"count": 30}, "o": {"count": 10}},
            {"m": {"count": 10}, "f": {"count": 20}},
        ]
        metric_configuration = Count(
            variable="fake_variable",
            group_by={"groupings": ["Gender"]},
        )
        aggregate_results = calculate_aggregate_metric(metric_configuration, sample_result)
        assert aggregate_results["m"]["count"] == 80
        assert aggregate_results["f"]["count"] == 50
        assert aggregate_results["o"]["count"] == 10

    def test_no_group_by(self):
        sample_result = [
            {
                "count": 20,
            },
            {
                "count": 80,
            },
            {"error": "count fails data anonymization requirements"},
        ]
        metric_configuration = Count(
            variable="fake_variable",
        )
        aggregate_results = calculate_aggregate_metric(metric_configuration, sample_result)
        assert aggregate_results["count"] == 100
