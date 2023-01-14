import unittest
from looqbox import ObjRow
from looqbox.objects.looq_object import LooqObject
from looqbox.objects.component_utility.css_option import CssOption as css
from looqbox.objects.visual.looq_text import ObjText


class TestRow(unittest.TestCase):
    """
    Test Row Component
    """

    def setUp(self):
        self.row_0 = ObjRow(ObjText("Test"), ObjText("Test"), css_options=[css.AlignItems.flex_end])
        self.row_1 = ObjRow(
            ObjText("Test"), ObjText("Test"), css_options=[css.AlignItems.flex_end],
            render_condition=False
        )
        self.row_2 = ObjRow(ObjText("Test"), ObjText("Test"))
        self.row_3 = ObjRow(ObjText("Test"), [ObjText("Test"), ObjText("Test")], ObjText("Test"))
        self.row_4 = ObjRow([ObjText("Test"), ObjText("Test")])

    def test_instance(self):
        self.assertIsInstance(self.row_0, LooqObject)

    def test_properties_access(self):
        self.assertIn(css.AlignItems.flex_end, self.row_0.css_options)

    def test_render_condition(self):
        self.assertFalse(self.row_1.render_condition)

    def test_row_comparison(self):
        self.assertFalse(self.row_0 == self.row_1)
        self.assertTrue(self.row_0 == self.row_0)

    def test_helper_method(self):
        self.row_0 = self.row_0.set_cross_alignment_start
        self.assertIn(
            css.AlignContent.flex_start.value,
            [p.value for p in self.row_0.css_options if p.property == "alignContent"]
        )

    def test_spacing_helper_method(self):
        self.row_2 = self.row_2.set_horizontal_child_spacing("5px")
        first_child = self.row_2.children[0]
        self.assertTrue(any(css.Margin.property in p.property for p in first_child.css_options))

    def test_set_all_helper_method(self):
        self.row_2 = self.row_2.set_to_all_child(css.Height("50px"))
        first_child = self.row_2.children[0]
        second_child = self.row_2.children[1]
        self.assertIn(css.Height.property, [p.property for p in first_child.css_options])
        self.assertIn(css.Height.property, [p.property for p in second_child.css_options])

    def test_heterogeneous_unpack(self):
        self.assertEqual(len(self.row_3.children), 4)

    def test_single_list_input(self):
        self.assertEqual(len(self.row_4.children), 2)

    def test_set_size(self):
        self.row_4 = self.row_4.set_size(3).set_mobile_size(10)
        self.assertIn("col-md-3", self.row_4.obj_class)
        self.assertIn("col-xs-10", self.row_4.obj_class)


if __name__ == '__main__':
    unittest.main()
