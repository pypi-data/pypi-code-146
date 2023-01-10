from looqbox.render.looqbox.base_looqbox_render import BrowserRender
from looqbox.objects.tests import LooqObject
from looqbox.objects.tests import ObjForm
from collections import OrderedDict
import unittest
import json


class TestObjectForm(unittest.TestCase):
    """
    Test looq_form file
    """

    def setUp(self) -> None:
        self.visitor = BrowserRender()
        self.visitor.remove_nones = False

    def test_instance(self):
        looq_object_form = ObjForm(
            {
                "type": "input", "label": "Loja", "value": "3",
                "name": "loja", "readonly": True
            },
            {
                "type": "input", "label": "Loja2",
                "value": "3", "name": "loja2", "readonly": True
            },
            title="Form"
        )

        self.assertIsInstance(looq_object_form, LooqObject)

    def test_json_creation(self):
        # Testing JSON keys

        looq_object_form = ObjForm(
            {
                "type": "input", "label": "Loja", "value": "3",
                "name": "loja", "readonly": True
            },
            {
                "type": "input", "label": "Loja2",
                "value": "3", "name": "loja2", "readonly": True
            },
            title="Form"
        )

        json_keys = list(looq_object_form.to_json_structure(self.visitor).keys())
        self.assertTrue("objectType" in json_keys, msg="Key objectType not found in JSON structure")
        self.assertTrue("title" in json_keys, msg="Key title not found in JSON structure")
        self.assertTrue("method" in json_keys, msg="Key method not found in JSON structure")
        self.assertTrue("action" in json_keys, msg="Key action not found in JSON structure")
        self.assertTrue("filepath" in json_keys, msg="Key filepath not found in JSON structure")
        self.assertTrue("fields" in json_keys, msg="Key fields not found in JSON structure")


if __name__ == '__main__':
    unittest.main()
