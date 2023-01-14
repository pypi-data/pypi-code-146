import unittest
from looqbox.objects.looq_object import LooqObject
from looqbox.objects.component_utility.css_option import CssOption as css
from looqbox.objects.visual.looq_text import ObjText


class TestText(unittest.TestCase):
    """
    Test Text Component
    """

    def setUp(self):
        self.text_0 = ObjText("Texto 1", css_options=[css.TextAlign.left])
        self.text_1 = ObjText("Texto 2", css_options=[css.TextAlign.left], render_condition=False)
        self.text_2 = ObjText("Texto 3")

    def test_instance(self):
        self.assertIsInstance(self.text_0, LooqObject)

    def test_properties_access(self):
        self.assertIn(css.TextAlign.left, self.text_0.css_options)

    def test_render_condition(self):
        self.assertFalse(self.text_1.render_condition)

    def test_text_comparison(self):
        self.assertFalse(self.text_0 == self.text_1)
        self.assertTrue(self.text_0 == self.text_0)

    def test_helper_method(self):
        self.text_2 = self.text_2.set_text_alignment_right
        self.assertIn(
            css.TextAlign.right.value,
            [p.value for p in self.text_2.css_options if p.property == "textAlign"])


if __name__ == '__main__':
    unittest.main()
