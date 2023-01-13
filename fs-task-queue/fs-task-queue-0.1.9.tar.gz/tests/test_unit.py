from fs_task_queue import Queue, JobStatus


def add(a: int, b: int):
    return a + b


def divide(a: int, b: int):
    return a / b


def test_integration_simple_pass_add(tmp_path):
    queue = Queue(tmp_path)
    assert queue.stats() == {
        "queued": 0,
        "started": 0,
        "finished": 0,
        "failed": 0,
    }
    job = queue.enqueue(add, 1, 2)
    assert queue.stats() == {
        "queued": 1,
        "started": 0,
        "finished": 0,
        "failed": 0,
    }
    job()
    assert job.result == add(1, 2)
    assert job.get_status() == JobStatus.FINISHED
    assert queue.stats() == {
        "queued": 0,
        "started": 0,
        "finished": 1,
        "failed": 0,
    }


def test_integration_simple_fail_div(tmp_path):
    queue = Queue(tmp_path)
    assert queue.stats() == {
        "queued": 0,
        "started": 0,
        "finished": 0,
        "failed": 0,
    }
    job = queue.enqueue(divide, 1, 0)
    assert queue.stats() == {
        "queued": 1,
        "started": 0,
        "finished": 0,
        "failed": 0,
    }
    job()
    assert job.get_status() == JobStatus.FAILED
    # need to get failed result from task
    assert queue.stats() == {
        "queued": 0,
        "started": 0,
        "finished": 0,
        "failed": 1,
    }


def test_integration_dequeue_simple_pass_add(tmp_path):
    queue = Queue(tmp_path)
    assert queue.stats() == {
        "queued": 0,
        "started": 0,
        "finished": 0,
        "failed": 0,
    }
    queue.enqueue(add, 1, 2)
    assert queue.stats() == {
        "queued": 1,
        "started": 0,
        "finished": 0,
        "failed": 0,
    }
    job = queue.dequeue()
    job()
    assert job.get_status() == JobStatus.FINISHED
    assert job.result == add(1, 2)
    assert queue.stats() == {
        "queued": 0,
        "started": 0,
        "finished": 1,
        "failed": 0,
    }
