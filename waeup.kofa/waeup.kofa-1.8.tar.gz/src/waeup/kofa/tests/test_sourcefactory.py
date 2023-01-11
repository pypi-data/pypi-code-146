## Tests for waeup.kofa.sourcefactory.
import unittest
from waeup.kofa.sourcefactory import SmartBasicContextualSourceFactory

class MyContext(object):
    # a sample context with min and max values
    minimum = 6
    maximum = 8

class MyContextualSource(SmartBasicContextualSourceFactory):
    # a contextual sample source containing all values from context
    def __init__(self, defaults):
        super(MyContextualSource, self).__init__()
        self.defaults = defaults

    def getValues(self, context):
        # This tuple could become quite large. Bad for containment checks.
        return self.defaults + tuple(
            range(context.minimum, context.maximum + 1))

class MySmartContextualSource(MyContextualSource):
    # a smart contextual sample source that can check a value for
    # containment fast, even if there are zillions of values in the
    # source.
    def contains(self, context, value):
        if value in self.defaults:
            return True
        # The context max is excluded. So we know that this method was
        # called.
        if value >= context.minimum and value < context.maximum:
            return True
        return False

class SmartBasicContextualSourceFactoryTests(unittest.TestCase):

    def test_default_get_values(self):
        # smart bcsfs behave like regular ones when asked for values.
        default_values = (4, 5, 6)
        source = MyContextualSource(default_values)(MyContext())
        self.assertEqual(list(source), [4, 5, 6, 6, 7, 8])
        return

    def test_default_contains(self):
        # smart bcsfs can behave like regular ones when checking
        # containment.  The default method is very expensive as it
        # scans each single value of the source.
        default_values = (4, 5, 6)
        source = MyContextualSource(default_values)(MyContext())
        self.assertEqual(6 in source, True)
        self.assertEqual(8 in source, True)
        self.assertEqual(10 in source, False)
        return

    def test_smart_contains(self):
        # smart bcfss support smarter containment checks.
        default_values = (4, 5, 6)
        source = MySmartContextualSource(default_values)(MyContext())
        self.assertEqual(6 in source, True)
        self.assertEqual(8 in source, False) # the special contains()
        self.assertEqual(10 in source, False)
        return
