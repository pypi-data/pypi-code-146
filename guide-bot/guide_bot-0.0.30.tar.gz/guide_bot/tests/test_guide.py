import unittest

from guide_bot.logic.Guide import Guide

from guide_bot.elements.Element_straight import Straight
from guide_bot.elements.Element_gap import Gap

from guide_bot.parameters.instrument_parameter_container import InstrumentParameterContainer
from guide_bot.parameters.instrument_parameters import FixedInstrumentParameter

from guide_bot.logic.length_system import length_system

import mcstasscript as ms

def setup_guide():
    guide = Guide("test_guide")
    guide += Straight("S1")
    guide += Gap("G")
    guide += Straight("S2")

    return guide


class Test_guide(unittest.TestCase):
    def test_number_of_elements(self):
        """
        Check guide has 3 elements from setup
        """
        guide = setup_guide()
        self.assertEqual(len(guide.guide_elements), 3)

    def test_add_start(self):
        """
        Check add start adds the element to the start of the list
        """
        guide = setup_guide()
        guide.add_guide_element_at_start(Gap("mod_guide"))
        self.assertEqual(guide.guide_elements[0].name, "mod_guide")

    def test_get_element(self):
        """
        Check get_element works
        """
        guide = setup_guide()
        gap = guide.get_element("G")
        self.assertEqual(gap.name, "G")

    def test_get_element_after(self):
        """
        Ensure get_element_after returns the element after specified element
        """
        guide = setup_guide()
        S2 = guide.get_element_after("G")
        self.assertEqual(S2.name, "S2")

    def test_set_instr_and_parameters(self):
        """
        Check that set_instr_and_parameters sets instr and param, and sets start dimensions
        """
        guide = setup_guide()
        instr_parameters = InstrumentParameterContainer()

        guide.set_instrument_and_instr_parameters("instr_dummy", instr_parameters)

        gap = guide.get_element("G")
        self.assertEqual(gap.current_instrument, "instr_dummy")
        self.assertIs(gap.current_parameters, instr_parameters)

        self.assertIn(gap.start_width, instr_parameters.all_parameters)
        self.assertIn(gap.start_height, instr_parameters.all_parameters)

    def test_set_instr_and_parameters(self):
        """
        Check that set_instr_and_parameters sets instr and param, and sets start dimensions
        """
        guide = setup_guide()
        instrument = ms.McStas_instr("test_isntrument")
        instr_parameters = InstrumentParameterContainer()

        guide.set_instrument_and_instr_parameters(instrument, instr_parameters)
        length_system(guide.guide_elements, 100, instr_parameters)

        # Register sample dimensions
        sample_width = FixedInstrumentParameter("sample_width", 0.423)
        sample_height = FixedInstrumentParameter("sample_height", 0.029)
        instr_parameters.add_parameter(sample_width)
        instr_parameters.add_parameter(sample_height)

        # Pass sample dimension parameters when creating McStas instrument
        guide.add_to_instrument([sample_width, sample_height])

        # Ensure five components included (2 for each straight, 1 for gap)
        self.assertEqual(len(instrument.component_list), 5)

        # Ensure sample size set on last element
        S2 = instrument.get_component("S2")
        self.assertEqual(S2.w2, "sample_width")
        self.assertEqual(S2.h2, "sample_height")

