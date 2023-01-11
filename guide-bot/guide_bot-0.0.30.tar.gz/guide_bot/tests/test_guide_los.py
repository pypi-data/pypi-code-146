import unittest

from guide_bot.logic.Guide import Guide
from guide_bot.logic.line_of_sight import ElementPoint, LineOfSightSection

from guide_bot.elements.Element_straight import Straight
from guide_bot.elements.Element_gap import Gap
from guide_bot.elements.Element_kink import Kink

from guide_bot.parameters.instrument_parameters import FixedInstrumentParameter


class Test_guide_los(unittest.TestCase):
    def test_simple_section(self):
        guide = Guide("test_guide")
        guide += Straight("S1")
        guide += Kink("K1")
        guide += Straight("S2")
        guide += Kink("K2")
        guide += Straight("S3")

        guide.add_los_section(1.0, 50.0)

        # Should ensure last Kink does not end before 1 m into the guide
        K2_end = guide.get_element_after("K2").start_point
        earliest_allowed_end = K2_end.get_lower_static_bound()
        self.assertEqual(earliest_allowed_end, 1.0)

        # Should ensure first Kink does not start after 50 m into the guide
        K1_start = guide.get_element("K1").start_point
        latest_allowed_start = K1_start.get_upper_static_bound()
        self.assertEqual(latest_allowed_start, 50.0)

    def test_simple_section_limited(self):
        guide = Guide("test_guide")
        guide += Straight("S1")
        guide += Kink("K1", start_point=[None, 45.0])
        guide += Straight("S2")
        guide += Kink("K2")
        guide += Straight("S3", start_point=[3.7, None])

        guide.add_los_section(1.0, 50.0)

        # Ensure user defined limit is not overwritten
        K2_end = guide.get_element_after("K2").start_point
        earliest_allowed_end = K2_end.get_lower_static_bound()
        self.assertEqual(earliest_allowed_end, 3.7)

        # Ensure user defined limit is not overwritten
        K1_start = guide.get_element("K1").start_point
        latest_allowed_start = K1_start.get_upper_static_bound()
        self.assertEqual(latest_allowed_start, 45.0)

    def test_simple_section_fixed(self):
        guide = Guide("test_guide")
        guide += Straight("S1")
        guide += Kink("K1", start_point=7)
        guide += Straight("S2")
        guide += Kink("K2")
        guide += Straight("S3", start_point=48)

        guide.add_los_section(1.0, 50.0)

        # Ensure user defined limit is not overwritten
        K2_end = guide.get_element_after("K2").start_point
        self.assertIsInstance(K2_end, FixedInstrumentParameter)
        self.assertEqual(K2_end.get_value(), 48)

        # Ensure user defined limit is not overwritten
        K1_start = guide.get_element("K1").start_point
        self.assertIsInstance(K1_start, FixedInstrumentParameter)
        self.assertEqual(K1_start.get_value(), 7)

    def test_multiple_sections(self):
        guide = Guide("test_guide")
        guide += Straight("S1")
        guide += Kink("K1")
        guide += Straight("S2")
        guide += Kink("K2")
        guide += Straight("S3")

        guide.add_los_section(1.0, 50.0)
        guide.add_los_section(3.0, 50.5)

        # Ensure limit is overwritten by more restrictive
        K2_end = guide.get_element_after("K2").start_point
        earliest_allowed_end = K2_end.get_lower_static_bound()
        self.assertEqual(earliest_allowed_end, 3.0)

        # Ensure limit is not overwritten by less restrictive
        K1_start = guide.get_element("K1").start_point
        latest_allowed_start = K1_start.get_upper_static_bound()
        self.assertEqual(latest_allowed_start, 50.0)

    def test_point_sections(self):
        guide = Guide("test_guide")
        guide += Straight("S1")
        guide += Kink("K1") # Considered los breaker
        guide += Straight("S2")
        guide += Kink("K2") # Considered los breaker
        guide += Straight("S3")

        # Los sections allows sections with a los breaker in there
        guide.add_los_section(ElementPoint("S1"), ElementPoint("S3", from_end=0))
        guide.add_los_section(ElementPoint("K2"), ElementPoint("S3", from_end=0))
        guide.add_los_section(ElementPoint("S1"), ElementPoint("K1", from_end=0))

        # Ensure impossible section caught, no los breaker in this section
        with self.assertRaises(RuntimeError):
            guide.add_los_section(ElementPoint("S3"), ElementPoint("S3", from_end=0))

        # This is actually not caught yet
        #with self.assertRaises(RuntimeError):
        #    guide.add_los_section(ElementPoint("K2", from_end=0), ElementPoint("S3", from_end=0))

    def test_mix_sections_distance_start(self):
        guide = Guide("test_guide")
        guide += Straight("S1")
        guide += Kink("K1")
        guide += Straight("S2")
        guide += Kink("K2")
        guide += Straight("S3")

        guide.add_los_section(4.0, ElementPoint("S3", from_end=0))

        K2_end = guide.get_element_after("K2").start_point
        earliest_allowed_end = K2_end.get_lower_static_bound()
        self.assertEqual(earliest_allowed_end, 4.0)

    def test_sections_add_min_length(self):
        guide = Guide("test_guide")
        guide += Straight("S1")
        guide += Kink("K1")
        guide += Straight("S2")
        guide += Kink("K2")
        guide += Straight("S3")

        guide.add_los_section(ElementPoint("S1", from_end=5), ElementPoint("K2", from_start=8))

        S1_length = guide.get_element("S1").length
        self.assertEqual(S1_length.get_lower_static_bound(), 5.0)

        K2_length = guide.get_element("K2").length
        self.assertEqual(K2_length.get_lower_static_bound(), 8.0)

    def test_sections_modify_min_length(self):
        guide = Guide("test_guide")
        guide += Straight("S1", length=[3.0, None])
        guide += Kink("K1")
        guide += Straight("S2")
        guide += Kink("K2", length=9)
        guide += Straight("S3")

        S1_length = guide.get_element("S1").length
        self.assertEqual(S1_length.get_lower_static_bound(), 3.0)

        guide.add_los_section(ElementPoint("S1", from_end=5), ElementPoint("K2", from_start=8))

        S1_length = guide.get_element("S1").length
        self.assertEqual(S1_length.get_lower_static_bound(), 5.0)

        K2_length = guide.get_element("K2").length
        self.assertEqual(K2_length.get_value(), 9)