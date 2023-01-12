"""Test the transfer daemon."""

import time

import pytest
from click.testing import CliRunner

from chime_frb_api.modules.results import Results
from chime_frb_api.workflow import Work
from chime_frb_api.workflow.daemons import transfer

buckets_kwargs = {
    "debug": True,
    "authentication": False,
    "base_url": "http://0.0.0.0:8000",
}

results_kwargs = {
    "debug": True,
    "authentication": False,
    "base_url": "http://0.0.0.0:8005",
}


@pytest.fixture()
def works():
    """Works fixture."""
    works = []
    for i in range(5):
        works.append(
            Work(
                pipeline=f"sample-{i}",
                event=[i, i + 1],
                tags=[f"{i}"],
                site="chime",
                archive=bool(i % 2),
                user="tester",
            ).payload
        )
    return works


def test_transfer_sucessful_work_to_delete(works):
    """Tests workflow transfer daemon for successful work that has archive=False."""
    runner = CliRunner()
    for work_payload in works:
        work = Work.from_dict(work_payload)
        work.deposit(**buckets_kwargs)

    withdrawn = Work.withdraw(pipeline="sample-0", **buckets_kwargs)
    withdrawn.status = "success"
    withdrawn.archive = False
    withdrawn.update(**buckets_kwargs)

    transfer_results = runner.invoke(
        transfer.transfer_work,
        f"--test-mode={buckets_kwargs['debug']} --buckets-base-url={buckets_kwargs['base_url']} --results-base-url={results_kwargs['base_url']}",  # noqa: E501
        standalone_mode=False,
    )

    assert transfer_results.exit_code == 0
    assert transfer_results.return_value == {"successful_work_deleted": True}


def test_transfer_sucessful_work():
    """Tests workflow transfer daemon for successful work that has archive=True."""
    runner = CliRunner()
    withdrawn = Work.withdraw(pipeline="sample-1", **buckets_kwargs)
    withdrawn.status = "success"
    withdrawn.archive = True
    withdrawn.update(**buckets_kwargs)

    transfer_results = runner.invoke(
        transfer.transfer_work,
        f"--test-mode={buckets_kwargs['debug']} --buckets-base-url={buckets_kwargs['base_url']} --results-base-url={results_kwargs['base_url']}",  # noqa: E501
        standalone_mode=False,
    )
    assert transfer_results.exit_code == 0
    assert transfer_results.return_value == {"successful_work_transferred": True}


def test_transfer_failed_work_to_delete():
    """Tests workflow transfer daemon for failed work that has archive=False."""
    runner = CliRunner()
    withdrawn = Work.withdraw(pipeline="sample-2", **buckets_kwargs)
    withdrawn.status = "failure"
    withdrawn.attempt = withdrawn.retries
    withdrawn.update(**buckets_kwargs)

    transfer_results = runner.invoke(
        transfer.transfer_work,
        f"--test-mode={buckets_kwargs['debug']} --buckets-base-url={buckets_kwargs['base_url']} --results-base-url={results_kwargs['base_url']}",  # noqa: E501
        standalone_mode=False,
    )
    assert transfer_results.exit_code == 0
    assert transfer_results.return_value == {"failed_work_deleted": True}


def test_transfer_failed_work():
    """Tests workflow transfer daemon for failed work that has archive=True."""
    runner = CliRunner()
    withdrawn = Work.withdraw(pipeline="sample-3", **buckets_kwargs)
    withdrawn.status = "failure"
    withdrawn.attempt = withdrawn.retries
    withdrawn.update(**buckets_kwargs)

    transfer_results = runner.invoke(
        transfer.transfer_work,
        f"--test-mode={buckets_kwargs['debug']} --buckets-base-url={buckets_kwargs['base_url']} --results-base-url={results_kwargs['base_url']}",  # noqa: E501
        standalone_mode=False,
    )
    assert transfer_results.exit_code == 0
    assert transfer_results.return_value == {
        "failed_work_transferred": True,
    }


def test_delete_stale_work():
    """Tests workflow transfer daemon for stale work."""
    runner = CliRunner()
    withdrawn = Work.withdraw(pipeline="sample-4", **buckets_kwargs)
    # Set creation time to be older than cutoff time (14 days)
    withdrawn.status = "failure"
    withdrawn.creation = time.time() - (60 * 60 * 24 * 14) - 1
    withdrawn.retries = 1
    withdrawn.attempt = 1
    withdrawn.update(**buckets_kwargs)
    transfer_results = runner.invoke(
        transfer.transfer_work,
        f"--test-mode={buckets_kwargs['debug']} --buckets-base-url={buckets_kwargs['base_url']} --results-base-url={results_kwargs['base_url']}",  # noqa: E501
        standalone_mode=False,
    )
    assert transfer_results.exit_code == 0
    assert transfer_results.return_value == {
        "stale_work_deleted": True,
    }


def test_cleanup_results():
    """Tests workflow transfer daemon cleanup results."""
    results = Results(**results_kwargs)
    for i in [1, 3]:
        pipeline_results = results.view(
            pipeline=f"sample-{i}",
            query={},
            projection={"id": True},
        )
        deletion_status = results.delete_ids(
            pipeline=f"sample-{i}", ids=[pipeline_results[0]["id"]]
        )
        assert deletion_status == {
            f"sample-{i}": True
        }, f"Clean up results failed for pipeline sample-{i}"
