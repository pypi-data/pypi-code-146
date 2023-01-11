from unittest import TestCase
from pyPhases.util.EventBus import EventBus
from unittest.mock import MagicMock


class TestpyEventBus(TestCase):

    def test_on(self):
        eventBus = EventBus()
        callback = lambda: 5
        eventBus.on('event1', callback)
        self.assertIn('event1', eventBus.eventMap)
        self.assertIn(callback, eventBus.eventMap['event1'])

    def test_once(self):
        eventBus = EventBus()
        callback = lambda: 5
        eventBus.once('event1', callback)
        eventBus.once('event1', callback)
        self.assertIn('event1', eventBus.eventMap)
        self.assertEqual(len(eventBus.eventMap['event1']), 1)
        self.assertIn(callback, eventBus.eventMap['event1'])

    def test_trigger(self):
        eventBus = EventBus()
        callback = MagicMock()

        eventBus.on('event1', callback)
        eventBus.trigger('event1', 'value1', 'value2')
        callback.assert_called_with('value1', 'value2')
