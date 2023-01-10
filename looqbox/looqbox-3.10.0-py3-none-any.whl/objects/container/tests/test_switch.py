import unittest
from looqbox import ObjSwitch
from looqbox.objects.looq_object import LooqObject
from looqbox.objects.component_utility.css_option import CssOption as css
from looqbox.objects.visual.looq_text import ObjText


class TestSwitch(unittest.TestCase):
    """
    Test Switch Component
    """

    def setUp(self):
        self.switch_0 = ObjSwitch(ObjText("Test"), ObjText("Test"), css_options=[css.TextAlign.left])
        self.switch_1 = ObjSwitch(ObjText("Test"), ObjText("Test"), css_options=[css.TextAlign.left],
                                  render_condition=False)

    def test_instance(self):
        switch_object = ObjSwitch("Test", "Test")
        self.assertIsInstance(switch_object, LooqObject)

    def test_properties_access(self):
        self.assertIn(css.TextAlign.left, self.switch_0.css_options)

    def test_render_condition(self):
        self.assertFalse(self.switch_1.render_condition)

    def test_switch_comparison(self):
        self.assertFalse(self.switch_0 == self.switch_1)
        self.assertTrue(self.switch_0 == self.switch_0)


if __name__ == '__main__':
    unittest.main()
