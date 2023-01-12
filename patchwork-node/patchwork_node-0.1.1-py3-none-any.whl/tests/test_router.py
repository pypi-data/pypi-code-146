# -*- coding: utf-8 -*-
from dataclasses import dataclass
from unittest.mock import Mock

import betterproto
import pytest
from patchwork.core import Task, AsyncSubscriber
from patchwork.core.proto.google.protobuf import StringValue

from patchwork.node.core import TaskRouter
from patchwork.node.core.exceptions import TaskDrop
from tests.message import Test


@pytest.mark.asyncio
async def test_task_dependency():
    router = TaskRouter()
    worker = Mock()
    router.bind(worker)

    t = Task(task_type='test')

    @router.on('test')
    async def processor(task: Task):
        assert task.uuid == t.uuid

    r = AsyncSubscriber()
    cr = router.handle(t, r)
    await cr


@pytest.mark.asyncio
async def test_pb_payload_dependency():
    router = TaskRouter()
    worker = Mock()
    router.bind(worker)

    @router.on('test')
    async def processor(data: StringValue):
        assert data.value == 'test-string'

    t = Task(task_type='test')
    t.payload = bytes(StringValue('test-string'))
    r = AsyncSubscriber()
    cr = router.handle(t, r)
    await cr


@pytest.mark.asyncio
async def test_better_pb_payload_dependency():
    router = TaskRouter()
    worker = Mock()
    router.bind(worker)

    @dataclass
    class Test(betterproto.Message):
        """Greeting represents a message you can tell a user."""

        message: str = betterproto.string_field(1)

    @router.on('test')
    async def processor(data: Test):
        assert data.message == 'test-betterproto-message'

    t = Task(task_type='test')
    t.payload = bytes(Test(message='test-betterproto-message'))
    r = AsyncSubscriber()
    cr = router.handle(t, r)
    await cr


@pytest.mark.asyncio
async def test_skip_unknown_task():
    router = TaskRouter(skip_unsupported_tasks=True)
    worker = Mock()
    router.bind(worker)

    t = Task(task_type='test')
    t.payload = bytes(Test(message='test-betterproto-message'))
    r = AsyncSubscriber()
    with pytest.raises(TaskDrop):
        cr = router.handle(t, r)
