from unittest import TestCase
from pyPhases.decorator.Decorator import Decorator


class TestDecorator(TestCase):

    def testDefault(self):
        decorator = Decorator()
        self.assertEqual(decorator.filter(None), True)

    def testNoError(self):
        decorator = Decorator()
        decorator.before(None)
        decorator.after(None)
