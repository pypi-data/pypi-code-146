from guide_bot.base_elements import guide_elements

from guide_bot.base_elements.base_element_geometry import BaseElementGeometry
from guide_bot.base_elements.base_element_geometry import PositionAndRotation

class Slit(guide_elements.GuideElement):
    """
    Gap GuideElement that inserts an empty space into a guide

    A Gap still has start and end dimensions as it is supposed to fit with the
    surrounding elements, as if it was a guide element. In this way, it can
    for example be used to set a gap for a chopper, and force the adjacent
    Elements to narrow to the required width / height for the chopper.
    """

    def __init__(self, name, length=None, start_point=None,
                 start_width=None, start_height=None,
                 end_width=None, end_height=None, **kwargs):
        """
        Slit GuideElement that inserts an empty space into a guide preceeded by a slit

        A Slit still has start and end dimensions as it is supposed to fit with
        the surrounding elements, as if it was a guide element. In this way,
        it can for example be used to set a gap for a chopper, and force the
        adjacent Elements to narrow to the required width / height for the
        chopper. If end_width / end_height is specified, they will override
        the following modules start_width / start_height settings.

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
        
        # Internalize stuff relevant for this
        
        super().__init__(name, length=length, start_point=start_point,
                         start_width=start_width, start_height=start_height,
                         end_width=end_width, end_height=end_height, **kwargs)

    def add_to_instr(self):
        """
        Adds code describing the gap element to the current McStas instrument

        This methods uses McStasScript to add components and code to a McStas
        instrument object. The McStas instrument object is an attribute of the
        class called current_instrument. New instrument parameters can also be
        created and added to the optimization by using the current_parameters
        attribute.

        Since the add_to_instr method of all the Elements are called in order
        from the sample to the source, it is important the components are
        added after the Origin component to ensure the correct order.
        """

        slit = self.current_instrument.add_component(self.name, "Slit")
        slit.set_AT([0, 0, 0], RELATIVE=self.reference_component_name)
        slit.xwidth = self.start_width.name
        slit.yheight = self.start_height.name

        end = self.current_instrument.add_component(self.end_component_name, "Arm")
        end.set_AT([0, 0, self.get_length_name()], RELATIVE=slit)

    def get_geometry(self):
        return GeometrySlit(start_point=self.start_point_parameter,
                            next_start_point=self.next_start_point_parameter,
                            start_width=self.start_width, start_height=self.start_height,
                            end_width=self.end_width, end_height=self.end_height)


class GeometrySlit(BaseElementGeometry):
    def __init__(self, start_point, next_start_point, start_width, start_height, end_width, end_height):

        super().__init__(start_point=start_point, next_start_point=next_start_point,
                         start_width=start_width, start_height=start_height,
                         end_width=end_width, end_height=end_height)

        self.visible = False

    def plot_extra(self, ax, start_pr, horizontal, color):
        """
        Plot the outside of the slit to make it clear, not disabled by visible = False
        """
        inner_dim = self.get_dimension(0.0, horizontal)
        if horizontal:
            outer_dim = self.start_width * 1.5
        else:
            outer_dim = self.start_height * 1.5

        inner_point_plus, inner_point_minus = start_pr.get_points(inner_dim, horizontal)
        outer_point_plus, outer_point_minus = start_pr.get_points(outer_dim, horizontal)

        if horizontal:
            ax.plot([inner_point_plus[2], outer_point_plus[2]],
                    [inner_point_plus[0], outer_point_plus[0]], color=color)
            ax.plot([inner_point_minus[2], outer_point_minus[2]],
                    [inner_point_minus[0], outer_point_minus[0]], color=color)
        else:
            ax.plot([inner_point_plus[2], outer_point_plus[2]],
                    [inner_point_plus[1], outer_point_plus[1]], color=color)
            ax.plot([inner_point_minus[2], outer_point_minus[2]],
                    [inner_point_minus[1], outer_point_minus[1]], color=color)