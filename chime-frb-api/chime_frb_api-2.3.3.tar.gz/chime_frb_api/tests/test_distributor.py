#!/usr/bin/env python

# Note for tests to run successfully you need
#   frb-master accessible at localhost:8001
#   distributor at localhost:8002

from chime_frb_api.backends.distributor import Distributor

kwargs = {"base_url": "http://localhost:8002", "authentication": False}
distributor = Distributor(debug=True, **kwargs)


def test_create_distributor():
    status = distributor.create_distributor(
        distributor_name="test-distributor", cleanup=True
    )
    assert status == "test-distributor"


def test_create_directory_scanner_distributor():
    status = distributor.create_directory_scanning_distributor(
        distributor_name="dir-scanner",
        directory="./*.py",
        interval=1,
        retries=1,
        cleanup=True,
    )
    assert status == "dir-scanner"


def test_get_status():
    status = distributor.get_status()
    assert "test-distributor" in status


def test_get_unique_status():
    status = distributor.get_status(distributor_name="test-distributor")
    assert status == {
        "name": "test-distributor",
        "queue_size": 0,
        "distributor_stopped": False,
        "perform_cleanup": True,
        "accumulator": {"status": "running", "type": "custom"},
        "work": {},
    }


def test_deposit_work():
    status = distributor.deposit_work(distributor_name="test-distributor", work=1)
    assert status == [True]


def test_get_work():
    work = distributor.get_work(distributor_name="test-distributor")
    assert int(work) == 1


def test_conclude_work():
    status = distributor.conclude_work(
        distributor_name="test-distributor", work_name=1, work_status=True
    )
    assert status == "1 completed"


def test_stop_distributor():
    status = distributor.stop_distributor(distributor_name="test-distributor")
    assert status is True


def test_delete_distributor():
    status = distributor.delete_distributor(distributor_name="test-distributor")
    assert status is True
    status = distributor.delete_distributor(distributor_name="dir-scanner")
    assert status is True
