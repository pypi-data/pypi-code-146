import unittest
from looqbox import ObjTooltip
from looqbox.objects.looq_object import LooqObject
from looqbox.objects.component_utility.css_option import CssOption as css
from looqbox.objects.visual.looq_text import ObjText


class TestTooltip(unittest.TestCase):
    """
    Test Tooltip Component
    """

    def setUp(self):
        self.tooltip_0 = ObjTooltip(ObjText("Test"), ObjText("Test"), text="This is a tooltip",
                                    css_options=[css.TextAlign.left])
        self.tooltip_1 = ObjTooltip(ObjText("Test"), ObjText("Test"), text="This is another tooltip",
                                    css_options=[css.TextAlign.left], render_condition=False)

    def test_instance(self):
        self.assertIsInstance(self.tooltip_0, LooqObject)

    def test_properties_access(self):
        self.assertIn(css.TextAlign.left, self.tooltip_0.css_options)

    def test_render_condition(self):
        self.assertFalse(self.tooltip_1.render_condition)

    def test_tooltip_comparison(self):
        self.assertFalse(self.tooltip_0 == self.tooltip_1)
        self.assertTrue(self.tooltip_0 == self.tooltip_0)


if __name__ == '__main__':
    unittest.main()
