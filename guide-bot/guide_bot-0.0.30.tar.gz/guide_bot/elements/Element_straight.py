import numpy as np
from guide_bot.base_elements import guide_elements
from guide_bot.base_elements.base_element_geometry import BaseElementGeometry
from guide_bot.base_elements.base_element_geometry import PositionAndRotation


class Straight(guide_elements.GuideElement):
    """
    Straight GuideElement that inserts a guide with flat mirrors into a guide

    A straight guide section with independent start and end dimensions,
    meaning it can have sloping mirrors, but they are flat. If end_width
    or end_height is specified, they will override the  start_width or
    start_height setting of the next Element in the guide.
    """
    def __init__(self, name, length=None, start_point=None,
                 start_width=None, start_height=None,
                 end_width=None, end_height=None, **kwargs):
        """
        Straight GuideElement that inserts a guide with flat mirrors into a guide

        A straight guide section with independent start and end dimensions,
        meaning it can have sloping mirrors, but they are flat. If end_width
        or end_height is specified, they will override the  start_width or
        start_height setting of the next Element in the guide.

        Parameters
        ----------
        name : str
            Name of the element

        length : (float, None, InstrumentParameter)
            Length of guide element, optimized parameter

        start_point : (float, None, InstrumentParameter)
            Distance from source to start of the gap element

        start_width : (float, None, InstrumentParameter)
            Width of the start of the gap

        start_height : (float, None, InstrumentParameter)
            Height of the start of the gap

        end_width : (float, None, InstrumentParameter)
            Width of the end of the gap

        end_height : (float, None, InstrumentParameter)
            Height of the end of the gap
        """
        # Internalize stuff relevant for this Element
        
        super().__init__(name, length=length, start_point=start_point,
                         start_width=start_width, start_height=start_height,
                         end_width=end_width, end_height=end_height,
                         **kwargs)

        # temporary reflectivity model
        if "R0" in kwargs:
            self.R0 = kwargs["R0"]
        else:
            self.R0 = 0.99

        if "Qc" in kwargs:
            self.Qc = kwargs["Qc"]
        else:
            self.Qc = 0.0217

        if "alpha" in kwargs:
            self.alpha = kwargs["alpha"]
        else:
            self.alpha = 6.07

        if "m" in kwargs:
            self.m = kwargs["m"]
        else:
            self.m = 1.0

        if "W" in kwargs:
            self.W = kwargs["W"]
        else:
            self.W = 0.003

    def add_to_instr(self):
        """
        Adds code describing the straight element to the current McStas instrument

        This methods uses McStasScript to add components and code to a McStas
        instrument object. The McStas instrument object is an attribute of the
        class called current_instrument. New instrument parameters can also be
        created and added to the optimization by using the current_parameters
        attribute.

        Since the add_to_instr method of all the Elements are called in order
        from the sample to the source, it is important the components are
        added after the Origin component to ensure the correct order.
        """

        guide = self.current_instrument.add_component(self.name, "Guide_gravity")
        guide.set_AT([0, 0, 0], RELATIVE=self.reference_component_name)
        
        guide.w1 = self.start_width.name
        guide.h1 = self.start_height.name

        guide.w2 = self.end_width.name
        guide.h2 = self.end_height.name

        guide.l = self.get_length_name() + " - 1E-6"

        # Temporary reflectivity model
        guide.R0 = self.R0
        guide.m = self.m
        guide.Qc = self.Qc
        guide.alpha = self.alpha
        guide.W = self.W

        end = self.current_instrument.add_component(self.end_component_name, "Arm")
        end.set_AT([0, 0, self.get_length_name()], RELATIVE=guide)

    def get_geometry(self):
        return GeometryStraight(start_point=self.start_point_parameter,
                                next_start_point=self.next_start_point_parameter,
                                start_width=self.start_width, start_height=self.start_height,
                                end_width=self.end_width, end_height=self.end_height)


class GeometryStraight(BaseElementGeometry):
    def __init__(self, start_point, next_start_point, start_width, start_height, end_width, end_height):

        super().__init__(start_point=start_point, next_start_point=next_start_point,
                         start_width=start_width, start_height=start_height,
                         end_width=end_width, end_height=end_height)