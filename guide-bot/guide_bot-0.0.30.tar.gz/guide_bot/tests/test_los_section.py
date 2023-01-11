import unittest

from guide_bot.logic.Guide import Guide
from guide_bot.elements.Element_straight import Straight
from guide_bot.elements.Element_gap import Gap
from guide_bot.elements.Element_kink import Kink
from guide_bot.parameters.instrument_parameters import FixedInstrumentParameter

from guide_bot.logic.line_of_sight import ElementPoint, LineOfSightSection


class Test_los_section(unittest.TestCase):
    def test_ElementPoint_definition(self):
        """
        Should default to 0 m from start
        """
        simple_point = ElementPoint("element_name")

        self.assertEqual(simple_point.from_start, 0)
        self.assertEqual(simple_point.mode, "from_start")
        self.assertEqual(simple_point.get_name(), "element_name")

    def test_ElementPoint_overspecified(self):
        """
        Should throw error if overspecified
        """
        with self.assertRaises(ValueError):
            point = ElementPoint("test", from_start=2, from_end=2)

    def test_ElementPoint_fraction(self):
        """
        Should default to 0 m from start
        """
        simple_point = ElementPoint("element_name", fraction=0.7)

        self.assertEqual(simple_point.fraction, 0.7)
        self.assertEqual(simple_point.mode, "fraction")

    def test_ElementPoint_get_fraction_from_fraction(self):
        """
        Get fraction from ElementPoint defined with fraction
        """
        simple_point = ElementPoint("element_name", fraction=0.7)

        self.assertEqual(simple_point.get_fraction(10.0), 0.7)

    def test_ElementPoint_get_fraction_from_start(self):
        """
        Get fraction from ElementPoint defined with from_start
        """
        simple_point = ElementPoint("element_name", from_start=2.4)

        self.assertEqual(simple_point.get_fraction(10.0), 0.24)

    def test_ElementPoint_get_fraction_from_end(self):
        """
        Get fraction from ElementPoint defined with from_end
        """
        simple_point = ElementPoint("element_name", from_end=3.8)

        self.assertEqual(simple_point.get_fraction(10.0), (10-3.8)/10.0)

    def test_distance_LOS_section(self):
        """
        Only distance los section
        """

        section = LineOfSightSection(1, 45)

        self.assertEqual(len(section.get_element_names()), 0)
        self.assertIsNone(section.get_start_name())
        self.assertIsNone(section.get_end_name())

    def test_mix_LOS_section(self):
        """
        Only distance los section
        """
        point = ElementPoint("ender", from_start=2)
        section = LineOfSightSection(1, point)

        self.assertEqual(section.get_element_names(), ["ender"])
        self.assertIsNone(section.get_start_name())
        self.assertEqual(section.get_end_name(), "ender")
        self.assertEqual(section.end.from_start, 2)
        self.assertEqual(section.end.mode, "from_start")

    def test_point_LOS_section(self):
        """
        Only distance los section
        """
        pointA = ElementPoint("starter", fraction=0.05)
        pointB = ElementPoint("ender", from_start=2)
        section = LineOfSightSection(pointA, pointB)

        self.assertEqual(section.get_element_names(), ["starter", "ender"])
        self.assertEqual(section.get_start_name(), "starter")
        self.assertEqual(section.get_end_name(), "ender")
        self.assertEqual(section.start.fraction, 0.05)
        self.assertEqual(section.start.mode, "fraction")
        self.assertEqual(section.end.from_start, 2)
        self.assertEqual(section.end.mode, "from_start")

    def test_included_elements(self):
        """
        Ensure the included elements method returns only elements within los section
        """

        guide = Guide("test_guide")
        guide += Gap("mod_guide")
        guide += Straight("S1")
        guide += Gap("G")
        guide += Straight("S2")
        guide += Kink("K")
        guide += Straight("S3")
        guide += Gap("mod_guide_sample")

        start_points = [0, 2.0, 5.7, 5.8, 15.0, 15.2, 29.5]
        end_points = [2.0, 5.7, 5.8, 15.0, 15.2, 29.5, 30.0]
        for element, sp, ep in zip(guide.guide_elements, start_points, end_points):
            element.start_point_parameter = FixedInstrumentParameter("sp", sp)
            element.next_start_point_parameter = FixedInstrumentParameter("ep", ep)

        pointA = ElementPoint("S2", fraction=0.05)
        pointB = ElementPoint("S3", from_end=2)
        section = LineOfSightSection(pointA, pointB)
        included_elements = section.included_elements(guide)

        self.assertEqual(len(included_elements), 3)
        self.assertEqual(included_elements[0].name, "S2")
        self.assertEqual(included_elements[1].name, "K")
        self.assertEqual(included_elements[2].name, "S3")


























