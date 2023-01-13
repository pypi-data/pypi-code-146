import unittest
from looqbox import ObjLink
from looqbox.objects.looq_object import LooqObject
from looqbox.objects.component_utility.css_option import CssOption as css
from looqbox.objects.visual.looq_text import ObjText


class TestLink(unittest.TestCase):
    """
    Test Link Component
    """

    def setUp(self):
        self.link_0 = ObjLink(ObjText("Test"), ObjText("Test"), question="This is a link",
                              css_options=[css.TextAlign.left])
        self.link_1 = ObjLink(ObjText("Test"), ObjText("Test"), question="This is another link",
                              css_options=[css.TextAlign.left], render_condition=False)

    def test_instance(self):
        self.assertIsInstance(self.link_0, LooqObject)

    def test_properties_access(self):
        self.assertIn(css.TextAlign.left, self.link_0.css_options)

    def test_render_condition(self):
        self.assertFalse(self.link_1.render_condition)

    def test_link_comparison(self):
        self.assertFalse(self.link_0 == self.link_1)
        self.assertTrue(self.link_0 == self.link_0)


if __name__ == '__main__':
    unittest.main()
