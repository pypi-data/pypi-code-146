"""Test Results API."""

import bson
import pytest

from chime_frb_api.modules.results import Results
from chime_frb_api.workflow import Work


@pytest.fixture(scope="module")
def results():
    """Results API fixture."""
    return Results(debug=True, authentication=False, base_url="http://0.0.0.0:8005")


@pytest.fixture(scope="module")
def work():
    """Work fixture."""
    work = Work(pipeline="results")
    work.id = str(bson.ObjectId())
    return work


def test_deposit_bad_results(results, work):
    """Test deposit bad results."""
    with pytest.raises(AssertionError):
        results.deposit([work.payload])


def test_deposit_results(results, work):
    """Test deposit results."""
    work.status = "success"
    status = results.deposit([work.payload])
    assert status[work.pipeline] is True

    response = results.view(
        pipeline=work.pipeline,
        query={"status": "success"},
        projection={"id": 1},
    )
    assert len(response) == 1
    assert response[0]["id"] == work.id


def test_update_results(results, work):
    """Test update results."""
    work.status = "failure"
    status = results.update([work.payload])
    assert status[work.pipeline] is True

    response = results.view(
        pipeline=work.pipeline,
        query={"status": "failure"},
        projection={"id": 1, "status": 1},
    )

    assert len(response) == 1
    assert response[0]["id"] == work.id
    assert response[0]["status"] == work.status


def test_count(results, work):
    """Test view count."""
    response = results.count(
        pipeline=work.pipeline,
        query={"status": "success"},
    )
    assert response == 0


def test_status(results, work):
    """Test status."""
    response = results.status()
    assert response == {work.pipeline: 1}


def test_delete_results(results, work):
    """Test delete results."""
    status = results.delete_ids(work.pipeline, [work.id])
    assert status[work.pipeline] is True

    response = results.view(
        pipeline=work.pipeline,
        query={},
        projection={"id": 1},
    )

    assert len(response) == 0
