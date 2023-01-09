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
"""Tests for the `budosystems.events.message_bus` module."""

import logging
from typing import Any

from budosystems.events.message_bus import MessageBus, Registration, EventType_contra
from budosystems.events import base, MESSAGE_BUS

async def _print_handler(ev: base.Event) -> None:
    print(str(ev))

async def _log_handler(ev: base.Event) -> None:
    logging.info(str(ev))

async def _unregistered_handler(ev: base.Event) -> None:
    logging.error(str(ev))  # pragma: no cover

async def _raising_handler(ev: base.Event) -> None:
    raise EvEx(ev=ev)

class EvEx(Exception):
    event: base.Event

    def __init__(self, ev: base.Event, *args: Any):
        super().__init__(self, *args)
        self.event = ev

class _EventA(base.Event):
    pass

class _EventB(base.Event):
    pass

class _EventC(base.Event):
    pass

class _EventA1(_EventA):
    pass

class _EventD(base.Event):
    """Unregistered event."""


RegSet = set[Registration[EventType_contra]]

class TestMessageBus:
    @staticmethod
    def teardown():
        """Clears the message bus."""
        MESSAGE_BUS.unregister_event_handlers(all_handlers=True)

    def test_is_singleton(self):
        m_bus_1 = MessageBus()
        m_bus_2 = MessageBus()

        assert m_bus_1 == m_bus_2
        assert m_bus_1 is m_bus_2
        assert m_bus_1 is MESSAGE_BUS

    def test_empty_get_event_handlers_no_args(self):
        handlers: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers()

        assert handlers == set()

    def test_empty_get_event_handlers_event_arg(self):
        handlers: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(event_type=_EventD)

        assert handlers == set()

    def test_empty_get_event_handlers_handler_arg(self):
        handlers: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(handler=_print_handler)

        assert handlers == set()

    def test_simple_registration(self):
        MESSAGE_BUS.register_event_handler(base.Event, _print_handler)
        reg_set: set[Registration[base.Event]] = MESSAGE_BUS.get_event_handlers(all_handlers=True)
        assert reg_set == {(base.Event, _print_handler)}


class TestMessageBusPrepopulated:
    """
    Base class for tests that require prepopulated message bus.

    Breaking down the classes by MessageBus method to help keep test names short.
    """
    @staticmethod
    def setup():
        """Populates the message bus."""
        MESSAGE_BUS.register_event_handler(_EventA, _print_handler)
        MESSAGE_BUS.register_event_handler(_EventB, _print_handler)
        MESSAGE_BUS.register_event_handler(_EventC, _print_handler)
        MESSAGE_BUS.register_event_handler(_EventA1, _print_handler)
        MESSAGE_BUS.register_event_handler(_EventA, _log_handler)
        MESSAGE_BUS.register_event_handler(_EventB, _log_handler)
        MESSAGE_BUS.register_event_handler(_EventC, _log_handler)
        MESSAGE_BUS.register_event_handler(_EventA1, _log_handler)

    @staticmethod
    def teardown():
        """Clears the message bus."""
        MESSAGE_BUS.unregister_event_handlers(all_handlers=True)


class TestMessageBus_get_event_handlers(TestMessageBusPrepopulated):
    def test_defaults_only(self):
        regs: set[Registration[base.Event]] = MESSAGE_BUS.get_event_handlers()

        assert len(regs) == 0
        assert regs == set()

    def test_all(self):
        regs: set[Registration[base.Event]] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 8
        assert regs == {
                (_EventA, _print_handler),
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
                (_EventA, _log_handler),
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }

    def test_event(self):
        regs: set[Registration[_EventA]] = MESSAGE_BUS.get_event_handlers(event_type=_EventA)

        assert len(regs) == 2
        assert regs == {(_EventA, _print_handler), (_EventA, _log_handler)}

    def test_handler(self):
        regs: set[Registration[base.Event]] = MESSAGE_BUS.get_event_handlers(handler=_print_handler)

        assert len(regs) == 4
        assert regs == {
                (_EventA, _print_handler),
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
        }

    def test_event_and_handler(self):
        regs: set[Registration[_EventA]] = MESSAGE_BUS.get_event_handlers(
                event_type=_EventA,
                handler=_print_handler)

        assert len(regs) == 1
        assert regs == {(_EventA, _print_handler)}

    def test_event_and_handler_all(self):
        regs: set[Registration[_EventA]] = MESSAGE_BUS.get_event_handlers(
                event_type=_EventA,
                handler=_print_handler,
                all_handlers=True)

        assert len(regs) == 5
        assert regs == {
                (_EventA, _print_handler),
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
                (_EventA, _log_handler),
        }

    def test_unregistered_event(self):
        regs: set[Registration[_EventD]] = MESSAGE_BUS.get_event_handlers(event_type=_EventD)

        assert len(regs) == 0
        assert regs == set()

    def test_unregistered_handler(self):
        regs: set[Registration[base.Event]] = MESSAGE_BUS.get_event_handlers(
                handler=_unregistered_handler)

        assert len(regs) == 0
        assert regs == set()

    def test_unregistered_event_and_unregistered_handler(self):
        regs = MESSAGE_BUS.get_event_handlers(event_type=_EventD,
                                              handler=_unregistered_handler)

        assert len(regs) == 0
        assert regs == set()

    def test_unregistered_event_and_unregistered_handler_all(self):
        regs = MESSAGE_BUS.get_event_handlers(event_type=_EventD,
                                              handler=_unregistered_handler,
                                              all_handlers=True)

        assert len(regs) == 0
        assert regs == set()

    def test_unregistered_event_and_registered_handler(self):
        regs = MESSAGE_BUS.get_event_handlers(event_type=_EventD, handler=_print_handler)

        assert len(regs) == 0
        assert regs == set()

    def test_unregistered_event_and_registered_handler_all(self):
        regs = MESSAGE_BUS.get_event_handlers(event_type=_EventD,
                                              handler=_print_handler,
                                              all_handlers=True)

        assert len(regs) == 4
        assert regs == {
                (_EventA, _print_handler),
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
        }

    def test_registered_event_and_unregistered_handler(self):
        regs = MESSAGE_BUS.get_event_handlers(event_type=_EventA,
                                              handler=_unregistered_handler)

        assert len(regs) == 0
        assert regs == set()

    def test_registered_event_and_unregistered_handler_all(self):
        regs = MESSAGE_BUS.get_event_handlers(event_type=_EventA,
                                              handler=_unregistered_handler,
                                              all_handlers=True)

        assert len(regs) == 2
        assert regs == {
                (_EventA, _print_handler),
                (_EventA, _log_handler),
        }

class TestMessageBus_unregister_event_handlers(TestMessageBusPrepopulated):
    def test_defaults_only(self):
        MESSAGE_BUS.unregister_event_handlers()
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 8
        assert regs == {
                (_EventA, _print_handler),
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
                (_EventA, _log_handler),
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }

    def test_all(self):
        MESSAGE_BUS.unregister_event_handlers(all_handlers=True)
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 0
        assert regs == set()

    def test_event(self):
        MESSAGE_BUS.unregister_event_handlers(event_type=_EventA)
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 6
        assert regs == {
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }

    def test_handler(self):
        MESSAGE_BUS.unregister_event_handlers(handler=_print_handler)
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 4
        assert regs == {
                (_EventA, _log_handler),
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }

    def test_event_and_handler(self):
        MESSAGE_BUS.unregister_event_handlers(event_type=_EventA, handler=_print_handler)
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 7
        assert regs == {
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
                (_EventA, _log_handler),
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }

    def test_event_and_handler_all(self):
        MESSAGE_BUS.unregister_event_handlers(event_type=_EventA, handler=_print_handler, all_handlers=True)
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)
        assert len(regs) == 3
        assert regs == {
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }

    def test_unregistered_event(self):
        MESSAGE_BUS.unregister_event_handlers(event_type=_EventD)
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 8
        assert regs == {
                (_EventA, _print_handler),
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
                (_EventA, _log_handler),
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }

    def test_unregistered_handler(self):
        MESSAGE_BUS.unregister_event_handlers(handler=_unregistered_handler)
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 8
        assert regs == {
                (_EventA, _print_handler),
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
                (_EventA, _log_handler),
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }

    def test_unregistered_event_and_unregistered_handler(self):
        MESSAGE_BUS.unregister_event_handlers(event_type=_EventD,
                                              handler=_unregistered_handler)
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 8
        assert regs == {
                (_EventA, _print_handler),
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
                (_EventA, _log_handler),
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }

    def test_unregistered_event_and_unregistered_handler_all(self):
        MESSAGE_BUS.unregister_event_handlers(event_type=_EventD,
                                              handler=_unregistered_handler,
                                              all_handlers=True)
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 8
        assert regs == {
                (_EventA, _print_handler),
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
                (_EventA, _log_handler),
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }

    def test_unregistered_event_and_registered_handler(self):
        MESSAGE_BUS.unregister_event_handlers(event_type=_EventD, handler=_print_handler)
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 8
        assert regs == {
                (_EventA, _print_handler),
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
                (_EventA, _log_handler),
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }

    def test_unregistered_event_and_registered_handler_all(self):
        MESSAGE_BUS.unregister_event_handlers(event_type=_EventD,
                                              handler=_print_handler,
                                              all_handlers=True)
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 4
        assert regs == {
                (_EventA, _log_handler),
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }

    def test_registered_event_and_unregistered_handler(self):
        MESSAGE_BUS.unregister_event_handlers(event_type=_EventA,
                                              handler=_unregistered_handler)
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 8
        assert regs == {
                (_EventA, _print_handler),
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
                (_EventA, _log_handler),
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }

    def test_registered_event_and_unregistered_handler_all(self):
        MESSAGE_BUS.unregister_event_handlers(event_type=_EventA,
                                              handler=_unregistered_handler,
                                              all_handlers=True)
        regs: RegSet[base.Event] = MESSAGE_BUS.get_event_handlers(all_handlers=True)

        assert len(regs) == 6
        assert regs == {
                (_EventB, _print_handler),
                (_EventC, _print_handler),
                (_EventA1, _print_handler),
                (_EventB, _log_handler),
                (_EventC, _log_handler),
                (_EventA1, _log_handler),
        }


class TestMessageBus_signal(TestMessageBusPrepopulated):
    def test_EventA(self, capsys, caplog):
        with caplog.at_level(logging.INFO):
            MESSAGE_BUS.signal(_EventA())
        captured_sys = capsys.readouterr()
        captured_log = caplog.records

        assert captured_sys.out.strip() == "_EventA()"
        assert len(captured_log) == 1
        assert captured_log[0].message == "_EventA()"

    def test_EventA1(self, capsys, caplog):
        with caplog.at_level(logging.INFO):
            MESSAGE_BUS.signal(_EventA1())
        captured_sys = capsys.readouterr()
        captured_log = caplog.records
        assert captured_sys.out.strip() == "_EventA1()\n_EventA1()"
        assert len(captured_log) == 2
        assert captured_log[0].message == "_EventA1()"
        assert captured_log[1].message == "_EventA1()"

    def test_EventD(self, capsys, caplog):
        with caplog.at_level(logging.INFO):
            MESSAGE_BUS.signal(_EventD())
        captured_sys = capsys.readouterr()
        captured_log = caplog.records

        assert captured_sys.out.strip() == ""
        assert len(captured_log) == 0

    def test_with_exception(self):
        MESSAGE_BUS.register_event_handler(event_type=_EventA, handler=_raising_handler)
        ev = _EventA()
        success, exes = MESSAGE_BUS.signal(ev)
        assert not success
        assert len(exes) == 1
        assert isinstance(exes[0], EvEx)
        assert exes[0].event == ev
