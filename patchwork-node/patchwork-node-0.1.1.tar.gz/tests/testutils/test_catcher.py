# -*- coding: utf-8 -*-
import uuid

from patchwork.core import Task
from patchwork.core.proto.google.protobuf import StringValue, BytesValue

from patchwork.node.testutils.worker import TaskCatcher


def test_catcher_assert_task_type_match():
    tc = TaskCatcher()
    task = Task(task_type='test')

    delta = tc.compare_tasks(task, {
        'task_type': 'test'
    })

    assert not delta


def test_catcher_assert_task_type_not_match():
    tc = TaskCatcher()
    task = Task(task_type='test')

    delta = tc.compare_tasks(task, {
        'task_type': 'another-test'
    })

    assert delta == {'task_type'}


def test_catcher_assert_task_uuid_match():
    tc = TaskCatcher()
    task = Task(task_type='test')

    delta = tc.compare_tasks(task, {
        'uuid': task.uuid,
        'task_type': 'test'
    })

    assert not delta


def test_catcher_assert_task_uuid_not_match():
    tc = TaskCatcher()
    task = Task(task_type='test')

    delta = tc.compare_tasks(task, {
        'uuid': uuid.uuid4(),
        'task_type': 'test'
    })

    assert delta == {'uuid'}


def test_catcher_assert_task_correlation_id_match():
    tc = TaskCatcher()
    task = Task(correlation_id='correlation', task_type='test')

    delta = tc.compare_tasks(task, {
        'correlation_id': 'correlation',
        'task_type': 'test'
    })

    assert not delta


def test_catcher_assert_task_correlation_id_not_match():
    tc = TaskCatcher()
    task = Task(correlation_id='correlation', task_type='test')

    delta = tc.compare_tasks(task, {
        'correlation_id': 'uncorrelated',
        'task_type': 'test'
    })

    assert delta == {'correlation_id'}


def test_catcher_assert_task_payload_bytes_match():
    tc = TaskCatcher()
    task = Task(task_type='test')
    task.payload = b'data'

    delta = tc.compare_tasks(task, {
        'payload': b'data',
        'task_type': 'test'
    })

    assert not delta


def test_catcher_assert_task_payload_bytes_not_match():
    tc = TaskCatcher()
    task = Task(task_type='test')
    task.payload = b'data'

    delta = tc.compare_tasks(task, {
        'payload': b'invalid-data',
        'task_type': 'test'
    })

    assert delta == {'payload'}


def test_catcher_assert_task_payload_string_match():
    tc = TaskCatcher()
    task = Task(task_type='test')
    task.payload = 'data'

    delta = tc.compare_tasks(task, {
        'payload': 'data',
        'task_type': 'test'
    })

    assert not delta


def test_catcher_assert_task_payload_string_not_match():
    tc = TaskCatcher()
    task = Task(task_type='test')
    task.payload = 'data'

    delta = tc.compare_tasks(task, {
        'payload': 'invalid-data',
        'task_type': 'test'
    })

    assert delta == {'payload'}


def test_catcher_assert_task_payload_type_not_match():
    tc = TaskCatcher()
    task = Task(task_type='test')
    task.payload = b'expected-bytes-data'

    delta = tc.compare_tasks(task, {
        'payload': 'invalid-type-its-string',
        'task_type': 'test'
    })

    assert delta == {'payload.@type'}

