#!/usr/bin/env python

# Note for tests to run successfully you need
#   frb-master accessible at localhost:8001
#   bucket at localhost:8002

import json

from chime_frb_api.backends import bucket as baltee

kwargs = {"base_url": "http://localhost:4357/buckets", "authentication": False}
bucket = baltee.Bucket(debug=True, **kwargs)


def test_create_bucket():
    status = bucket.create_bucket(bucket_name="test-bucket")
    assert status == "test-bucket"


def test_get_status():
    status = bucket.get_status()
    assert "test-bucket" in status


def test_get_unique_status():
    status = bucket.get_status(bucket_name="test-bucket")
    assert status == {
        "name": "test-bucket",
        "distributors_state": {
            "high": {"name": "high", "status": {}, "stopped": False, "items": []},
            "medium": {"name": "medium", "status": {}, "stopped": False, "items": []},
            "low": {"name": "low", "status": {}, "stopped": False, "items": []},
        },
    }


def test_deposit_work():
    status = bucket.deposit(
        bucket_name="test-bucket", work={"event_no": 9386707}, priority="high"
    )
    assert status == [True]


def test_get_work():
    work = bucket.withdraw(bucket_name="test-bucket", client="test-client", expiry="60")
    assert work == {"event_no": 9386707}


def test_change_priority():
    status = bucket.change_priority(
        bucket_name="test-bucket",
        work_name=json.dumps({"event_no": 9386707}),
        priority="low",
    )
    assert status


def test_conclude_work():
    status = bucket.conclude(
        bucket_name="test-bucket",
        work_name=json.dumps({"event_no": 9386707}),
        redeposit=False,
    )
    assert status


def test_delete_bucket():
    status = bucket.delete_bucket(bucket_name="test-bucket")
    assert status is True
