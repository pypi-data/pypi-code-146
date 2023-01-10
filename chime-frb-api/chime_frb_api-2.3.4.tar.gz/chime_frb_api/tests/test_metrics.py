#!/usr/bin/env python
"""Test CHIME/FRB Metrics API."""
from datetime import datetime
from time import sleep

import pytest
import requests

from chime_frb_api.backends import frb_master

master = frb_master.FRBMaster(debug=True, base_url="http://localhost:8001")


def test_configure():
    """Test the configure method."""
    response = master.metrics.configure(
        description="test", category="test", names=["test_a", "test_b"]
    )
    assert response == {"category_registered": True, "collection_created": True}


def test_bad_configure():
    """Test bad configure method."""
    with pytest.raises(TypeError):
        master.metrics.configure(description="bad-test", names=["test_a", "test_b"])


def test_reconfigure():
    """Test the reconfigure method."""
    response = master.metrics.reconfigure(category="test", names=["test_c", "test_d"])
    assert response is True


def test_bad_reconfigure():
    """Test bad reconfigure method."""
    with pytest.raises(TypeError):
        master.metrics.reconfigure(names=["test_a", "test_b"])


def test_overview():
    """Test the overview method."""
    response = master.metrics.overview()
    assert "test_c" in response[0]["names"]
    assert "test_d" in response[0]["names"]


def test_add_new_metric():
    """Test the add method."""
    response = master.metrics.add(
        category="test", metrics={"test_a": 1, "test_b": 2}, patch=False
    )
    assert response is True


def test_bad_add():
    """Test bad add method."""
    with pytest.raises(AttributeError):
        master.metrics.add(metrics={"test_a": 1, "test_b": 2}, patch=False)


def test_patch_add():
    """Test the add method with a patching of values."""
    response = master.metrics.add(
        category="test", metrics={"test_a": 1, "test_b": 2}, patch=True
    )
    assert response == {"acknowledged": True, "matched_count": 2, "modified_count": 2}


def test_timestamp_add():
    """Test the timestamp call to add method."""
    response = master.metrics.add(
        category="test",
        metrics={"test_a": 5, "test_b": 5},
        timestamp=datetime.utcnow().isoformat(),
    )
    assert response is True


def test_get_metrics():
    """Test the get_metrics method."""
    sleep(0.5)
    response = master.metrics.get_metrics(category="test", metric="test_a")
    assert len(response) == 2


def test_bad_get_metrics():
    """Test bad get_metrics method."""
    with pytest.raises(AttributeError):
        master.metrics.get_metrics(metric="test_a")


def test_metric_search():
    """Test the search method."""
    # Sleep 1 second to allow the database to index
    sleep(1)
    response = master.metrics.search(
        category="test",
        metrics=["test_a", "test_b"],
        timestamps=["min", "max"],
        values=[2, 2],
    )
    assert response[0]["metric"] == "test_b"
    assert response[0]["value"] == 2


def test_bad_metric_search():
    """Test the bad search method."""
    with pytest.raises(AttributeError):
        master.metrics.search(metrics=["test_a", "test_b"])
    with pytest.raises(AttributeError):
        master.metrics.search(category="test")


def test_delete_category():
    """Test the delete_category method."""
    response = requests.delete(url="http://localhost:8001/v1/metrics/destroy/test")
    assert response.status_code == 200
