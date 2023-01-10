import unittest
from looqbox.objects.visual.looq_message import ObjMessage
from looqbox.objects.looq_object import LooqObject
import json


class TestObjMessage(unittest.TestCase):
    """
    Test looq_message file
    """

    def test_instance(self):
        looq_object_message = ObjMessage("Unit Test Text")

        self.assertIsInstance(looq_object_message, LooqObject)


if __name__ == '__main__':
    unittest.main()
