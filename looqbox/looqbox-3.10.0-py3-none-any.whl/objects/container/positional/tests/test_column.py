import unittest
from looqbox import ObjColumn
from looqbox.objects.looq_object import LooqObject
from looqbox.objects.component_utility.css_option import CssOption as css
from looqbox.objects.visual.looq_text import ObjText


class TestColumn(unittest.TestCase):
    """
    Test Column Component
    """

    def setUp(self):
        self.column_0 = ObjColumn(ObjText("Test"), ObjText("Test"), css_options=[css.AlignItems.flex_end])
        self.column_1 = ObjColumn(
            ObjText("Test"), ObjText("Test"), css_options=[css.AlignItems.flex_end],
            render_condition=False
        )
        self.column_2 = ObjColumn(ObjText("Test"), ObjText("Test"))
        self.column_3 = ObjColumn(ObjText("Test"), [ObjText("Test"), ObjText("Test")], ObjText("Test"))

    def test_instance(self):
        column_object = ObjColumn("Test", "Test")
        self.assertIsInstance(column_object, LooqObject)

    def test_properties_access(self):
        self.assertIn(css.AlignItems.flex_end, self.column_0.css_options)

    def test_render_condition(self):
        self.assertFalse(self.column_1.render_condition)

    def test_column_comparison(self):
        self.assertFalse(self.column_0 == self.column_1)
        self.assertTrue(self.column_0 == self.column_0)

    def test_helper_method(self):
        self.column_0 = self.column_0.set_cross_alignment_start
        self.assertIn(
            css.AlignContent.flex_start.value,
            [p.value for p in self.column_0.css_options if p.property == "alignContent"]
        )

    def test_spacing_helper_method(self):
        self.column_2 = self.column_2.set_horizontal_child_spacing("5px")
        first_child = self.column_2.children[0]
        self.assertTrue(any(css.Margin.property in p.property for p in first_child.css_options))

    def test_set_all_helper_method(self):
        self.column_2 = self.column_2.set_to_all_child(css.Height("50px"))
        first_child = self.column_2.children[0]
        second_child = self.column_2.children[1]
        self.assertIn(css.Height.property, [p.property for p in first_child.css_options])
        self.assertIn(css.Height.property, [p.property for p in second_child.css_options])

    def test_heterogeneous_unpack(self):
        self.assertTrue(len(self.column_3.children) == 4)


if __name__ == '__main__':
    unittest.main()
