"""Test Buckets API."""

import time

import pytest

from chime_frb_api.modules.buckets import Buckets
from chime_frb_api.workflow import Work

pytest.WITHDRAWN = []


@pytest.fixture()
def buckets():
    """Buckets fixture."""
    return Buckets(debug=True, authentication=False, base_url="http://0.0.0.0:8000")


@pytest.fixture()
def work():
    """Work fixture."""
    return Work(pipeline="sample").payload


@pytest.fixture()
def works():
    """Works fixture."""
    works = []
    for i in range(10):
        works.append(
            Work(
                pipeline=f"sample-{i}",
                event=[i, i + 1],
                tags=[f"{i}"],
                site="chime",
                archive=bool(i // 5),
                user="tester",
            ).payload
        )
    return works


def test_status(buckets):
    """Test status."""
    status = buckets.status()
    assert status == {"total": 0, "queued": 0, "running": 0, "success": 0, "failure": 0}


def test_add_work(buckets, work):
    """Test add work."""
    status = buckets.deposit([work])
    assert status is True
    status = buckets.status()
    assert status == {"total": 1, "queued": 1, "running": 0, "success": 0, "failure": 0}


def test_delete_work(buckets):
    """Test delete work."""
    status = buckets.delete_many(pipeline="sample", force=True)
    assert status is True
    status = buckets.status()
    assert status == {"total": 0, "queued": 0, "running": 0, "success": 0, "failure": 0}


def test_deposit_many(buckets, works):
    """Test deposit many."""
    status = buckets.deposit(works)
    assert status is True


def test_work_lifecycle(buckets, works):
    """Test withdraw work."""
    withdrawn = []
    # Withdraw with pipeline
    zero = buckets.withdraw(pipeline="sample-0")
    assert zero["pipeline"] == "sample-0"
    withdrawn.append(zero)
    nothing = buckets.withdraw(pipeline="sample-2", priority=1)
    assert nothing is None
    event = buckets.withdraw(pipeline="sample-9", event=[10])
    assert 10 in event["event"]
    withdrawn.append(event)
    site = buckets.withdraw(pipeline="sample-8", site="chime", user="tester")
    withdrawn.append(site)
    status = buckets.status()
    assert status["running"] == 3
    pytest.WITHDRAWN = withdrawn


def test_update_work(buckets):
    """Test update work."""
    for work in pytest.WITHDRAWN:
        work["status"] = "success"
    status = buckets.update(pytest.WITHDRAWN)
    assert status is True
    assert buckets.status()["success"] == 3


def test_delete_based_on_status(buckets):
    """Test delete based on status."""
    status = buckets.delete_many(pipeline="sample-0", status="success", force=True)
    assert status is True
    assert buckets.status()["total"] == 9


def test_delete_based_on_event(buckets):
    """Test delete based on event."""
    assert buckets.delete_many(pipeline="sample-9", events=[10], force=True) is True
    assert buckets.status()["total"] == 8


def test_pipelines(buckets):
    """Test pipelines."""
    pipelines = buckets.pipelines()
    assert "sample-4" in pipelines
    assert "sample-9" not in pipelines


def test_pipeline_details(buckets):
    """Test pipeline details."""
    assert buckets.status("sample-4") == {
        "total": 1,
        "queued": 1,
        "running": 0,
        "success": 0,
        "failure": 0,
    }


def test_view(buckets):
    """Test view."""
    view = buckets.view(
        query={}, projection={"pipeline": True, "creation": True}, skip=5, limit=1
    )
    assert view[0]["pipeline"] == "sample-3"


def test_delete_work_all(buckets, works):
    """Test delete work all."""
    for i in range(1, 9):
        status = buckets.delete_many(pipeline=f"sample-{i}", force=True)
        assert status is True


def test_stale_work(buckets):
    """Test stale work."""
    stale = Work(pipeline="stale", creation=time.time() - 60 * 24 * 60 * 60).payload
    assert buckets.deposit([stale]) is True
    audit = buckets.audit()
    assert audit["stale"] == 1


def test_removed_audited_work(buckets):
    """Test removed audited work."""
    assert buckets.delete_many(pipeline="stale", force=True) is True
