#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from functools import wraps
from typing import List
import inspect

from fast_tracker import Layer, Component
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag


def trace(
        op: str = None,
        layer: Layer = Layer.Local,
        component: Component = Component.Unknown,
        tags: List[Tag] = None,
):
    def decorator(func):
        _op = op or func.__name__
        context = get_context()

        span = context.new_local_span(op=_op)
        span.layer = layer
        span.component = component
        [span.tag(tag) for tag in tags or []]

        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                with span:
                    return await func(*args, **kwargs)

            return wrapper

        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                with span:
                    return func(*args, **kwargs)

            return wrapper

    return decorator


def runnable(
        op: str = None,
        layer: Layer = Layer.Local,
        component: Component = Component.Unknown,
        tags: List[Tag] = None,
):
    def decorator(func):
        snapshot = get_context().capture()

        @wraps(func)
        def wrapper(*args, **kwargs):
            _op = op or "Thread/" + func.__name__
            context = get_context()
            with context.new_local_span(op=_op) as span:
                context.continued(snapshot)
                span.layer = layer
                span.component = component
                [span.tag(tag) for tag in tags or []]
                func(*args, **kwargs)

        return wrapper

    return decorator
