import unittest
from looqbox.objects.looq_html import ObjHTML
from looqbox.objects.looq_object import LooqObject
import json


class TestObjectHTML(unittest.TestCase):
    """
    Test looq_html file
    """

    def test_instance(self):
        looq_object_html = ObjHTML("<div> Unit Test Text <div>")

        self.assertIsInstance(looq_object_html, LooqObject)


if __name__ == '__main__':
    unittest.main()
