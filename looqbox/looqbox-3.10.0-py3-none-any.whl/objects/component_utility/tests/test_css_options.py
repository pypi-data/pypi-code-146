import unittest
from looqbox.objects.component_utility.css import Css
from looqbox.objects.component_utility.css_option import CssOption as css


class TestCssOptions(unittest.TestCase):
    """
    Test CssOptions Class
    """

    def setUp(self):
        self.text_align_right = css.TextAlign("right")
        self.text_align_right_by_property = css.TextAlign.right
        self.text_align_default = css.TextAlign

    def test_instance(self):
        self.assertIsInstance(self.text_align_right, Css)

    def test_css_set_value(self):
        self.assertEqual(self.text_align_right.value, self.text_align_right_by_property.value)
        self.assertNotEqual(self.text_align_right.value, self.text_align_default.value)


if __name__ == '__main__':
    unittest.main()
