import unittest

from guide_bot.logic.Guide import Guide
from guide_bot.elements.Element_straight import Straight
from guide_bot.elements.Element_gap import Gap
from guide_bot.elements.Element_kink import Kink
from guide_bot.elements.Element_curved import Curved
from guide_bot.parameters.instrument_parameters import FixedInstrumentParameter
from guide_bot.parameters.instrument_parameters import LosInstrumentParameter

from guide_bot.logic.line_of_sight import ElementPoint, LineOfSightSection, LosCalculator

def setup_guide():
    guide = Guide("test_guide")
    guide += Gap("mod_guide")
    guide += Straight("S1")
    guide += Gap("G")
    guide += Straight("S2")
    guide += Kink("K")
    guide += Straight("S3")
    guide += Gap("guide_sample")

    start_points = [0, 2.0, 5.7, 5.8, 15.0, 15.2, 29.5]
    end_points = [2.0, 5.7, 5.8, 15.0, 15.2, 29.5, 30.0]
    for element, sp, ep in zip(guide.guide_elements, start_points, end_points):
        element.start_point_parameter = FixedInstrumentParameter("sp", sp)
        element.next_start_point_parameter = FixedInstrumentParameter("ep", ep)

        element.start_width = FixedInstrumentParameter("s_w", 0.05)
        element.start_height = FixedInstrumentParameter("s_h", 0.05)
        element.end_width = FixedInstrumentParameter("e_w", 0.05)
        element.end_height = FixedInstrumentParameter("e_h", 0.05)

    return guide


def setup_simple_guide():
    guide = Guide("test_guide")
    guide += Straight("S1")
    guide += Kink("K")
    guide += Straight("S2")

    start_points = [0, 5.0, 5.1]
    end_points = [5.0, 5.1, 10.0]
    for element, sp, ep in zip(guide.guide_elements, start_points, end_points):
        element.start_point_parameter = FixedInstrumentParameter("sp", sp)
        element.next_start_point_parameter = FixedInstrumentParameter("ep", ep)

        element.start_width = FixedInstrumentParameter("s_w", 0.05)
        element.start_height = FixedInstrumentParameter("s_h", 0.05)
        element.end_width = FixedInstrumentParameter("e_w", 0.05)
        element.end_height = FixedInstrumentParameter("e_h", 0.05)

    return guide


def setup_trick_guide():
    """
    Make guide that has los, but it is difficult for the algorithm to detect
    """
    guide = setup_simple_guide()

    S1 = guide.get_element("S1")
    S1.start_width = FixedInstrumentParameter("s_w", 0.456)
    S1.start_height = FixedInstrumentParameter("s_h", 0.583)
    S1.end_width = FixedInstrumentParameter("e_w", 0.001)
    S1.end_height = FixedInstrumentParameter("e_h", 0.08)

    kink = guide.get_element("K")
    kink.kink_angle = FixedInstrumentParameter("ka", 0.0)
    kink.h_displacement = FixedInstrumentParameter("h_displacement", 0.015)
    kink.v_displacement = FixedInstrumentParameter("v_displacement", 0.015)
    kink.start_width = FixedInstrumentParameter("s_w", 0.001)
    kink.start_height = FixedInstrumentParameter("s_h", 0.08)
    kink.end_width = FixedInstrumentParameter("e_w", 0.08)
    kink.end_height = FixedInstrumentParameter("e_h", 0.001)

    S2 = guide.get_element("S2")
    S2.start_width = FixedInstrumentParameter("s_w", 0.08)
    S2.start_height = FixedInstrumentParameter("s_h", 0.001)
    S2.end_width = FixedInstrumentParameter("s_w", 0.583)
    S2.end_height = FixedInstrumentParameter("s_h", 0.319)

    return guide


def setup_one_element_guide():
    guide = Guide("test_guide")
    guide += Gap("mod_guide")
    guide += Curved("C")
    guide += Gap("guide_target")

    start_points = [0, 2.0, 9.5]
    end_points = [2.0, 9.5, 10.0]
    for element, sp, ep in zip(guide.guide_elements, start_points, end_points):
        element.start_point_parameter = FixedInstrumentParameter("sp", sp)
        element.next_start_point_parameter = FixedInstrumentParameter("ep", ep)

        element.start_width = FixedInstrumentParameter("s_w", 0.05)
        element.start_height = FixedInstrumentParameter("s_h", 0.05)
        element.end_width = FixedInstrumentParameter("e_w", 0.05)
        element.end_height = FixedInstrumentParameter("e_h", 0.05)

    return guide


class Test_los_calculator(unittest.TestCase):
    def test_init(self):
        """
        Ensure basic init works
        """

        guide = setup_guide()
        guide.add_los_section(ElementPoint("S2", fraction=0.05), ElementPoint("S3", from_end=2))

        calculator = LosCalculator(guide)
        self.assertEqual(calculator.los_breakers[0].name, "K")

    def test_find_los_point(self):
        """
        Check conversion from distance to ElementPoint
        """
        guide = setup_guide()
        calculator = LosCalculator(guide)

        element_point = calculator.find_los_point(4.0)
        self.assertEqual(element_point.element_name, "S1")
        self.assertEqual(element_point.get_fraction(5.7 - 2.0), (4.0 - 2.0)/(5.7 - 2.0))

        element_point = calculator.find_los_point(29.8)
        self.assertEqual(element_point.element_name, "guide_sample")
        self.assertEqual(element_point.get_fraction(30 - 29.5), (29.8 - 29.5) / (30.0 - 29.5))

    def test_check_los_simple_kink(self):
        """
        Check check_los returns True when there is los, and false when broken
        """
        guide = setup_simple_guide()
        los_section = LineOfSightSection(ElementPoint("S1", from_start=0), ElementPoint("S2", from_end=0))

        kink = guide.get_element("K")
        kink.kink_angle = FixedInstrumentParameter("ka", 0.0)
        kink.h_displacement = FixedInstrumentParameter("h_displacement", 0.0)
        kink.v_displacement = FixedInstrumentParameter("v_displacement", 0.0)

        calculator = LosCalculator(guide)
        self.assertTrue(calculator.check_los(los_section))

        # Still los with some displacement
        kink.h_displacement = FixedInstrumentParameter("h_displacement", 0.02)
        kink.v_displacement = FixedInstrumentParameter("v_displacement", 0.03)
        self.assertTrue(calculator.check_los(los_section))

        # Break los with displacement larger than guide width / height
        kink.v_displacement = FixedInstrumentParameter("v_displacement", 0.06)
        self.assertFalse(calculator.check_los(los_section))

    def test_check_los_trick_guide(self):
        """
        Check check_los returns True when there is los for tricky guide
        """
        guide = setup_trick_guide()
        los_section = LineOfSightSection(ElementPoint("S1", from_start=0), ElementPoint("S2", from_end=0))

        calculator = LosCalculator(guide)
        self.assertTrue(calculator.check_los(los_section))

    def test_solve_section_simple_kink(self):
        """
        Check check_los returns True when there is los, and false when broken
        """
        guide = setup_simple_guide()
        los_section = LineOfSightSection(ElementPoint("S1", from_start=0), ElementPoint("S2", from_end=0))

        kink = guide.get_element("K")
        kink.kink_angle = LosInstrumentParameter("ka")
        kink.los_breaker_parameter = kink.kink_angle # link manual parameter overwrite to los_parameter

        kink.h_displacement = FixedInstrumentParameter("h_displacement", 0.0)
        kink.v_displacement = FixedInstrumentParameter("v_displacement", 0.0)

        calculator = LosCalculator(guide)
        calculator.solve_section(los_section, [guide.get_element("K")])

        self.assertAlmostEqual(kink.kink_angle.get_value(), 1.14641479, 3)  # Calculated los break angle

    def test_single_curved_guide(self):
        """
        Check a single curved guide with gaps around it.
        """
        guide = setup_one_element_guide()
        los_section = LineOfSightSection(ElementPoint("C", from_start=0), ElementPoint("C", from_end=0))

        curved = guide.get_element("C")
        curved.angular_diversion = FixedInstrumentParameter("ad", 0.0)
        curved.horizontal_bend_par = FixedInstrumentParameter("hbp", 1.0)
        curved.positive_bend_par = FixedInstrumentParameter("pbp", 1.0)

        calculator = LosCalculator(guide)
        self.assertTrue(calculator.check_los(los_section))


if __name__ == "__main__":
    unittest.main()
