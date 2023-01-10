"""Test the audit daemon."""

import time

import pytest
from click.testing import CliRunner

from chime_frb_api.modules.buckets import Buckets
from chime_frb_api.workflow import Work
from chime_frb_api.workflow.daemons import audit

buckets_kwargs = {
    "debug": True,
    "authentication": False,
    "base_url": "http://0.0.0.0:8000",
}


@pytest.fixture()
def works():
    """Works fixture."""
    works = []
    for i in range(3):
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


def test_audit(works):
    """Tests workflow audit daemon."""
    runner = CliRunner()
    for work_payload in works:
        work = Work.from_dict(work_payload)
        work.deposit(**buckets_kwargs)

    audit_results = runner.invoke(
        audit.workflow,
        f"--test-mode={buckets_kwargs['debug']} --base-url={buckets_kwargs['base_url']}",
        standalone_mode=False,
    )
    assert audit_results.exit_code == 0
    assert audit_results.return_value == {"expired": 0, "failed": 0, "stale": 0}


def test_audit_failed():
    """Tests workflow audit daemon for failed work."""
    runner = CliRunner()
    withdrawn = Work.withdraw(pipeline="sample-0", **buckets_kwargs)
    withdrawn.status = "failure"
    withdrawn.update(**buckets_kwargs)
    audit_results = runner.invoke(
        audit.workflow,
        f"--test-mode={buckets_kwargs['debug']} --base-url={buckets_kwargs['base_url']}",
        standalone_mode=False,
    )
    # sample-0 work is failed and requeued.
    assert audit_results.exit_code == 0
    assert audit_results.return_value == {"expired": 0, "failed": 1, "stale": 0}


def test_audit_expired():
    """Tests workflow audit daemon for expired work."""
    runner = CliRunner()
    withdrawn = Work.withdraw(pipeline="sample-1", **buckets_kwargs)
    withdrawn.start = time.time() - 3600.0 * 2
    withdrawn.update(**buckets_kwargs)

    audit_results = runner.invoke(
        audit.workflow,
        f"--test-mode={buckets_kwargs['debug']} --base-url={buckets_kwargs['base_url']}",
        standalone_mode=False,
    )
    # sample-1 work is expired and marked as failure
    assert audit_results.exit_code == 0
    assert audit_results.return_value == {"expired": 1, "failed": 0, "stale": 0}


def test_audit_stale():
    """Tests workflow audit daemon for stale work."""
    runner = CliRunner()
    withdrawn = Work.withdraw(pipeline="sample-2", **buckets_kwargs)
    withdrawn.creation = time.time() - 60 * 86400.0
    withdrawn.update(**buckets_kwargs)
    audit_results = runner.invoke(
        audit.workflow,
        f"--test-mode={buckets_kwargs['debug']} --base-url={buckets_kwargs['base_url']}",
        standalone_mode=False,
    )
    # sample-2 work is stale;
    # the 1 failed work is the expired sample-1 work from previous test
    assert audit_results.exit_code == 0
    assert audit_results.return_value == {"expired": 0, "failed": 1, "stale": 1}


def test_delete_works():
    """Remove the work created for this test."""
    bucket = Buckets(**buckets_kwargs)
    for i in range(3):
        deletion_status = bucket.delete_many(pipeline=f"sample-{i}", force=True)
        assert deletion_status is True
