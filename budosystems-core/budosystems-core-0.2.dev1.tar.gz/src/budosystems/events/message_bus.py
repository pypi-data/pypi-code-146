#
#  Copyright (c) 2021.  Budo Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

"""Event-driven message bus related classes and functions."""

from __future__ import annotations
from typing import Callable, TypeVar, Awaitable, Optional, Type, Set, Tuple, Any, ClassVar

import asyncio

from .base import Event


EventType_contra = TypeVar("EventType_contra", bound=Event, contravariant=True)
"""Event-type type variable.  Used throughout `MessageBus` methods.
(`bound` = `~budosystems.events.base.Event`)"""

AsyncEventHandler = Callable[[EventType_contra], Awaitable[None]]
"""
Type alias for the signature of event handlers.  In regular Python, it looks like::

    async def handler(event: EventOrSubtype) -> None:
        ...
"""

Registration = Tuple[Type[EventType_contra], AsyncEventHandler[EventType_contra]]
"""Pair of (event_type, event_handler)."""


class MessageBus:
    """The event message bus.

    This is a singleton class.  The canonical reference to the instance is
    `budosystems.events.MESSAGE_BUS`.
    """

    _instance: ClassVar[MessageBus]
    _handlers: Set[Registration[Event]]
    """Set of registered (event_type, handler) pairs."""

    _loop: asyncio.AbstractEventLoop

    def __new__(cls) -> MessageBus:
        if hasattr(cls, '_instance'):
            return cls._instance

        cls._instance = super().__new__(cls)
        cls._instance._handlers = set()
        cls._loop = asyncio.new_event_loop()
        return cls._instance

    def register_event_handler(self,
                               event_type: Type[Event],
                               handler: AsyncEventHandler[Event]
                               ) -> None:
        """
        Registers a callable as a handler for a specific event type.

        :param event_type: A subclass of `Event`.
        :param handler: An async callable which will handle instances of `event_type`.
        """
        self._handlers.add((event_type, handler))

    def get_event_handlers(self, *,
                           event_type: Optional[Type[EventType_contra]] = None,
                           handler: Optional[AsyncEventHandler[EventType_contra]] = None,
                           all_handlers: bool = False
                           ) -> Set[Registration[Event]]:
        """
        Gets a filtered list of registered event handlers.

        If only one of `event_type` or `handler` is specified, includes all handlers associated
        with that parameter.

        If both `event_type` and `handler` are specified:
            - if ``all_handlers`` is ``False`` (default), the returned list includes the associated
              pair only if it was previously registered.
            - if ``all_handlers`` is ``True``, the returned list includes all registrations that
              match either `event_type` or `handler`.

        When `event_type` is specified, the returned list only includes registrations that match
        the type exactly (i.e. no super- or sub-types).

        If neither `event_type` nor `handler` is specified, and `all_handlers` is ``True``,
        the returned list will include all registrations.

        :param event_type: A subclass of `Event`.
        :param handler: An async callable which handled instances of `event_type`.
        :param all_handlers: A flag to determine whether or not to include everything.
        :returns: A set of (event_type, handler) pairs of registered event handlers.
        """
        match_set: Set[Registration[Event]] = set()

        if event_type is None and handler is None:
            if all_handlers:
                # Dump all the registrations
                match_set = set(self._handlers)
            # Else keep it empty
            return match_set  # Bypass all other checks

        for registration in self._handlers:
            (reg_event, reg_handler) = registration
            # pylint: disable=too-many-boolean-expressions
            if (all_handlers and (reg_event == event_type or reg_handler == handler)) \
                    or (reg_event == event_type and reg_handler == handler) \
                    or (event_type is None and reg_handler == handler) \
                    or (handler is None and reg_event == event_type):
                match_set.add(registration)

        return match_set
    # end get_event_handlers

    def unregister_event_handlers(self, *,
                                  event_type: Optional[Type[EventType_contra]] = None,
                                  handler: Optional[AsyncEventHandler[EventType_contra]] = None,
                                  all_handlers: bool = False
                                  ) -> None:
        """Removes event handlers.

        See `get_event_handlers` for the matching process.

        :param event_type: A subclass of `Event`.
        :param handler: An async callable which handled instances of `event_type`.
        :param all_handlers: A flag to determine whether or not to include every thing.
            Only considered if the other two arguments are None (default).
        """
        match_set = self.get_event_handlers(event_type=event_type, handler=handler,
                                            all_handlers=all_handlers)
        for registration in match_set:
            self._handlers.remove(registration)

    def signal(self, event: EventType_contra) -> tuple[bool, list[Any]]:
        """Calls the handlers for the incoming event.  This includes handlers registered for
        supertypes of `event`.

        Processing order of event handlers is not guaranteed.  The only guarantee is that
        all eligible handlers will be processed when `signal` returns.

        :param event: An event being signaled.
        """
        futures = [handler(event)
                   for (event_type, handler) in self._handlers
                   if isinstance(event, event_type)]
        if futures:
            # TODO: Figure out how to avoid passing loop argument.
            tmp_loop = asyncio.get_event_loop()
            asyncio.set_event_loop(self._loop)
            results = self._loop.run_until_complete(
                    asyncio.gather(*futures, return_exceptions=True))
            exes = [ex for ex in results if ex is not None]
            success = exes == []
            asyncio.set_event_loop(tmp_loop)

            return success, exes
        return True, []
