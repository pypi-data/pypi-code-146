"""Test HTTP operations for the work object."""


from typing import List

import pytest

from chime_frb_api.modules.buckets import Buckets
from chime_frb_api.workflow import Work

buckets = Buckets()
pipeline = "test-work-ops"
pytest.WITHDRAWN = None


def test_deposit_and_withdraw():
    """Test case where withdrawing from a pipeline with work deposited."""
    work = Work(pipeline=pipeline)
    response: List[str] = work.deposit(return_ids=True)
    assert len(response) == 1
    # Withdrawing from the bucket should return the work
    worked = Work.withdraw(pipeline=pipeline)
    assert worked.status == "running"
    assert worked.id == response[0]
    pytest.WITHDRAWN = worked


def test_update_work():
    """Test updating work."""
    work = pytest.WITHDRAWN
    work.status = "success"
    # Update the work
    work.update()
    # Check that the work has been updated
    response = buckets.view(
        query={"pipeline": pipeline}, projection={"id": 1, "status": 1}
    )
    assert response[0]["status"] == "success"
    assert response[0]["id"] == work.id


def test_delete_work():
    """Test deleting work."""
    assert pytest.WITHDRAWN.delete() is True
