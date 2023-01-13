import unittest
from looqbox.objects.looq_simple import ObjSimple
from looqbox.objects.looq_simple import LooqObject
import json


class TestObjSimple(unittest.TestCase):
    """
    Teste looq_simple file
    """
    def test_instance(self):
        looq_object_simple = ObjSimple("Unit Test Text")

        self.assertIsInstance(looq_object_simple, LooqObject)
