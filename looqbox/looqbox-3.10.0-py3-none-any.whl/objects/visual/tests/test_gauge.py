import unittest
from looqbox.objects.looq_object import LooqObject
from looqbox.objects.component_utility.css_option import CssOption as css
from looqbox.objects.visual.looq_gauge import ObjGauge


class TestGauge(unittest.TestCase):
    """
    Test Gauge Component
    """

    def setUp(self):
        self.gauge_0 = ObjGauge(20, css_options=[css.Width(200), css.Height(100)])
        self.gauge_1 = ObjGauge(30, maximum=110, css_options=[css.Width(250), css.Height(25)], render_condition=False)

    def test_instance(self):
        self.assertIsInstance(self.gauge_0, LooqObject)

    def test_properties_access(self):
        self.assertIn(css.Width, self.gauge_0.css_options)

    def test_render_condition(self):
        self.assertFalse(self.gauge_1.render_condition)

    def test_gauge_comparison(self):
        self.assertFalse(self.gauge_0 == self.gauge_1)
        self.assertTrue(self.gauge_0 == self.gauge_0)


if __name__ == '__main__':
    unittest.main()
