import asyncio
from functools import wraps
from typing import Awaitable, Callable

from ipywidgets import widgets  # type: ignore[import]

WidgetName = str
WidgetValue = str
WidgetFunc = Callable[[Callable, WidgetValue], Awaitable[None]]

SleepTime = 0.01

# for understanding butter the meaning of these decorators/functions look at:
# https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Asynchronous.html?highlight=unobserve

# The small slipping times  are for being able to trigger the graph with a code
# and not only by the press on the widget. For reasons that are not totally clear
# when python command is send those tiny await slipping times are need in order
# for the graph to respond.

# ToDo - benchmark the sleeping that are needed for the interactive graph:
#  https://classiq.atlassian.net/browse/CAD-2821


def widget_callback(widget_name: WidgetName):
    def decorator(function: WidgetFunc):
        @wraps(function)
        async def wrapper(self: Callable, **kwargs: WidgetValue) -> None:
            widget: widgets = getattr(self, widget_name)
            interactive_loop = _create_interactive_loop_async(
                function=function, self=self, widget=widget
            )
            asyncio.ensure_future(interactive_loop)
            await asyncio.sleep(SleepTime)

        return wrapper

    return decorator


async def _create_interactive_loop_async(
    function: WidgetFunc, self: Callable, widget: widgets
) -> None:
    while True:
        value: WidgetValue = await _wait_for_change(widget=widget)
        await asyncio.sleep(SleepTime)
        await function(self, value)


def _wait_for_change(widget: widgets) -> asyncio.Future:
    future: asyncio.Future = asyncio.Future()

    def _get_value(change) -> None:
        future.set_result(change.new)
        widget.unobserve(_get_value, "value")

    widget.observe(_get_value, "value")
    return future
