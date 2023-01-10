from looqbox.render.looqbox.base_looqbox_render import BrowserRender
from looqbox.objects.tests import ObjWebFrame
from looqbox.objects.tests import LooqObject
import unittest
import json


class TestObjectWebFrame(unittest.TestCase):
    """
    Test looq_web_frame file
    """
    def setUp(self) -> None:
        self.visitor = BrowserRender()
        self.visitor.remove_nones = False

    def test_instance(self):
        looq_object_web_frame = ObjWebFrame("test", 200)

        self.assertIsInstance(looq_object_web_frame, LooqObject)

    def test_json_creation(self):
        # Testing JSON keys
        looq_object_web_frame = ObjWebFrame("test", 200)

        json_object = list(looq_object_web_frame.to_json_structure(self.visitor).keys())
        self.assertTrue("objectType" in json_object, msg="objectType not found in JSON structure test")
        self.assertTrue("src" in json_object, msg="src not found in JSON structure test")
        self.assertTrue("style" in json_object, msg="style not found in JSON structure test")
        self.assertTrue("enableFullscreen" in json_object, msg="enableFullscreen not found in JSON structure test")
        self.assertTrue("openFullscreen" in json_object, msg="openFullscreen not found in JSON structure test")

        json_style_object = list(looq_object_web_frame.to_json_structure(self.visitor)["style"].keys())
        self.assertTrue("width" in json_style_object, msg="width not found in JSON style structure test")
        self.assertTrue("height" in json_style_object, msg="height not found in JSON style structure test")


if __name__ == '__main__':
    unittest.main()
