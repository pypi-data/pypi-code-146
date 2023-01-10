import unittest
from copy import deepcopy

from looqbox.objects.looq_object import LooqObject
from looqbox.objects.visual.shape.looq_line import ObjLine


class TestLine(unittest.TestCase):
    """
    Test Line Component
    """

    def setUp(self):
        self.line_0 = ObjLine()
        self.line_1 = ObjLine(render_condition=False)

    def test_instance(self):
        self.assertIsInstance(self.line_0, LooqObject)

    def test_render_condition(self):
        self.assertFalse(self.line_1.render_condition)

    def test_line_comparison(self):
        self.assertFalse(self.line_0 == self.line_1)
        self.assertTrue(self.line_0 == self.line_0)

    def test_thickness_attribution(self):
        line_test_0 = deepcopy(self.line_0).set_size("3px").set_orientation_horizontal
        line_test_1 = deepcopy(self.line_0).set_orientation_horizontal.set_size("3px")
        self.assertEqual(line_test_0.obj_class, line_test_1.obj_class)
        self.assertEqual(line_test_0.size, line_test_1.size)


if __name__ == '__main__':
    unittest.main()
