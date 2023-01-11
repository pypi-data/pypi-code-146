import numpy as np
from guide_bot.base_elements import guide_elements
from guide_bot.parameters import instrument_parameters as ipars
from guide_bot.base_elements.base_element_geometry import BaseElementGeometry
from guide_bot.base_elements.base_element_geometry import PositionAndRotation


class Wolter_PH(guide_elements.GuideElement):
    """
    Wolter guide element with Ellipsoid/Hyperbolid pairs.

    """
    def __init__(self, name, length=None, start_point=None,
                 start_width=None, start_height=None,
                 end_width=None, end_height=None,
                 mirror_length=None,
                 mirror_position_fraction=None, hyperboloid_fraction=None, rmax=None,
                 r_fraction=None, focal_offset=None,
                 nshells=1, disk=1, **kwargs):
        """
        Wolter guide element with Ellipsoid/Hyperbolid pairs.

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

        mirror_length : (float, None, InstrumentParameter)
            Total length of wolter mirrors

        mirror_position_fraction : (float, None, InstrumentParameter)
            Total length of wolter mirrors

        hyperboloid_fraction : (float, None, InstrumentParameter)
            Total length of wolter mirrors

        rmax : (float, None, InstrumentParameter)
            Largest diameter of optics

        r_fraction : (float, None, InstrumentParameter)
            Fraction of rmax used, max 1, lower makes a hole in center

        focal_offset_u : (float, None, InstrumentParameter)
            Offset value from focus at guide_bot element start point

        focal_offset_d : (float, None, InstrumentParameter)
            Offset value from focus at guide_bot element end point

        nshells : (float, None, InstrumentParameter)
            Number of mirrors

        disk : (float, None, InstrumentParameter)
            0 for hole through middle, 1 for absorbing disk
        """
        # Internalize stuff relevant for this Element

        self.mirror_length = guide_elements.handle_input_parameter(name + "_mirror_length", mirror_length,
                                                                   default_min=0.10, default_max=1.5)

        if isinstance(self.mirror_length, ipars.FixedInstrumentParameter):
            min_length = 2.0 * self.mirror_length.get_value()
        elif isinstance(self.mirror_length, ipars.RelativeFreeInstrumentParameter):
            min_length = 2.0 * self.mirror_length.get_upper_static_bound()

        if isinstance(length, ipars.RelativeFreeInstrumentParameter):
            # If length is free, check if the minimum allows for the entire mirror
            current_min_length = length.get_lower_static_bound()
            if min_length > current_min_length:
                length.static_lower = min_length
        
        super().__init__(name, length=length, start_point=start_point,
                         start_width=start_width, start_height=start_height,
                         end_width=end_width, end_height=end_height,
                         **kwargs)

        self.nshells = nshells
        self.disk = disk

        self.mirror_position_fraction = guide_elements.handle_input_parameter(name + "_mirror_pos_frac", mirror_position_fraction,
                                                                              default_min=0.05, default_max=0.8)

        self.mirror_length = guide_elements.handle_input_parameter(name + "_mirror_length", mirror_length,
                                                                   default_min=0.05, default_max=1.5)

        self.hyperboloid_fraction = guide_elements.handle_input_parameter(name + "_hyperboloid_frac", hyperboloid_fraction,
                                                                          default_min=0.05, default_max=0.95)
        self.rmax = guide_elements.handle_input_parameter(name + "_rmax", rmax,
                                                          default_min=0.05, default_max=0.3)
        self.r_fraction = guide_elements.handle_input_parameter(name + "_r_mirror_frac", r_fraction,
                                                                default_min=0.05, default_max=0.8)
        self.focal_offset = guide_elements.handle_input_parameter(name + "_focal_offset", focal_offset,
                                                                  default_min=-2.0, default_max=2.0)

        self.center_distance_name = "center_distance_" + self.name
        self.mirror_H_length_name = "mirror_H_length" + self.name
        self.mirror_P_length_name = "mirror_P_length" + self.name

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

    def copy_components(self, destination):
        components_to_copy = ["Conics_PH.comp", "conic.h", "w1_conics.h", "w1_general.h"]

        for component in components_to_copy:
            self.copy_component(component, destination)

        return components_to_copy

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

        self.current_parameters.add_parameter(self.mirror_position_fraction)
        self.current_parameters.add_parameter(self.mirror_length)
        self.current_parameters.add_parameter(self.hyperboloid_fraction)
        self.current_parameters.add_parameter(self.rmax)
        self.current_parameters.add_parameter(self.r_fraction)
        self.current_parameters.add_parameter(self.focal_offset)

        element_length_name = self.get_length_name()

        instr = self.current_instrument


        instr.add_declare_var("double", self.mirror_H_length_name)
        instr.append_initialize(f"{self.mirror_H_length_name} = {self.mirror_length.name} * {self.hyperboloid_fraction.name};")


        instr.add_declare_var("double", self.mirror_P_length_name)
        instr.append_initialize(f"{self.mirror_P_length_name} = {self.mirror_length.name} - {self.mirror_H_length_name};")

        min_center_name = "min_center_" + self.name
        instr.add_declare_var("double", min_center_name)
        max_center_name = "max_center_" + self.name
        instr.add_declare_var("double", max_center_name)


        instr.add_declare_var("double", self.center_distance_name)

        instr.append_initialize(f"{min_center_name} = {self.mirror_P_length_name};")
        instr.append_initialize(f"{max_center_name} = {element_length_name} - {self.mirror_H_length_name};")

        instr.append_initialize(f"{self.center_distance_name} = {min_center_name} + ({max_center_name} - {min_center_name})"
                                f"*{self.mirror_position_fraction.name};")

        wolter = self.current_instrument.add_component(self.name, "Conics_PH")
        wolter.set_AT([0, 0, self.center_distance_name], RELATIVE=self.reference_component_name)
        
        wolter.nshells = self.nshells
        wolter.disk = self.disk

        wolter.rmax = self.rmax.name

        rmin_name = "rmin_" + self.name
        instr.add_declare_var("double", rmin_name)
        instr.append_initialize(f"{rmin_name} = {self.r_fraction.name}*{self.rmax.name};")
        wolter.rmin = rmin_name

        wolter.focal_length = f"{element_length_name} - {self.center_distance_name} + {self.focal_offset.name}"

        wolter.lp = self.mirror_P_length_name
        wolter.lh = self.mirror_H_length_name

        # Temporary reflectivity model
        wolter.m = self.m
        #wolter.R0 = self.R0
        #wolter.Qc = self.Qc
        #wolter.alpha = self.alpha
        #wolter.W = self.W

        end = self.current_instrument.add_component(self.end_component_name, "Arm")
        end.set_AT([0, 0, self.get_length_name()], RELATIVE=self.reference_component_name)

    def get_source_focus(self):
        """
        A source needs to focus at the start of the focusing section
        """

        focus_dist = self.start_point_parameter.name + " + " + self.center_distance_name + " - " + self.mirror_P_length_name
        r_factor = "2.2" # Wolter optics is the required rmax at the center, the opening can be slightly bigger

        return dict(width=r_factor + "*" + self.rmax.name,
                    height=r_factor + "*" + self.rmax.name,
                    dist=focus_dist)

    def get_geometry(self):
        return GeometryWolter_PH(start_point=self.start_point_parameter,
                                 next_start_point=self.next_start_point_parameter,
                                 start_width=self.start_width, start_height=self.start_height,
                                 end_width=self.end_width, end_height=self.end_height,
                                 rmax=self.rmax, mirror_length=self.mirror_length,
                                 hyperboloid_fraction=self.hyperboloid_fraction,
                                 mirror_position_fraction=self.mirror_position_fraction)


class GeometryWolter_PH(BaseElementGeometry):
    def __init__(self, start_point, next_start_point, start_width, start_height, end_width, end_height,
                 rmax, mirror_length, hyperboloid_fraction, mirror_position_fraction):

        super().__init__(start_point=start_point, next_start_point=next_start_point,
                         start_width=start_width, start_height=start_height,
                         end_width=end_width, end_height=end_height)

        self.set_parameter_attribute("rmax", rmax, par_type="horizontal")
        self.set_parameter_attribute("mirror_length", mirror_length, par_type="start_point")
        self.set_parameter_attribute("hyperboloid_fraction", hyperboloid_fraction, par_type="start_point")
        self.set_parameter_attribute("mirror_position_fraction", mirror_position_fraction, par_type="start_point")

        self.plot_resolution = 60  # Number of points to plot
        self.linestyle = "--"

    def get_dimension(self, distance_unit_less, horizontal=True):
        start = self.start_point
        end = self.next_start_point
        length = end - start
        position = distance_unit_less * length

        H_length = self.mirror_length*self.hyperboloid_fraction
        E_length = self.mirror_length - H_length
        min_center = E_length
        max_center = length - H_length
        center = min_center + (max_center - min_center)*self.mirror_position_fraction

        if horizontal:
            start_dim = self.start_width
            end_dim = self.end_width
        else:
            start_dim = self.start_height
            end_dim = self.end_height

        if position < center - E_length:
            frac = position/(center - E_length)
            return 2*(start_dim + frac*(self.rmax-start_dim))

        if position > center + H_length:
            frac = (position - center - H_length)/(length - center - H_length)
            return 2*(self.rmax + frac*(end_dim - self.rmax))

        if center - E_length <= position <= center + H_length:
            return 2*self.rmax

        raise RuntimeError("Failure in get_dimension logic for Wolter.")

    def plot_extra(self, ax, start_pr, horizontal=True, color="black"):

        if start_pr is None:
            start_pr = self.create_start_pr()

        start = self.start_point
        end = self.next_start_point
        length = end - start

        H_length = self.mirror_length * self.hyperboloid_fraction
        P_length = self.mirror_length - H_length
        min_center = P_length
        max_center = length - H_length
        center = min_center + (max_center - min_center) * self.mirror_position_fraction

        # Want to plot from center - H_length to center + H_length
        unitless_start = (center - P_length)/length
        unitless_end = (center + H_length)/length

        plot_resolution = 2
        distances = np.linspace(unitless_start, unitless_end, plot_resolution)

        plus_array = np.zeros((plot_resolution, 3)) # right / top depending on horizontal
        minus_array = np.zeros((plot_resolution, 3)) # left / bottom depending on horizontal

        for index, distance in enumerate(distances):
            this_pr = self.continue_center_line(start_pr, distance)
            dim = self.get_dimension(distance, horizontal)
            minus_array[index, :], plus_array[index, :] = this_pr.get_points(dim, horizontal)

        if horizontal:
            ax.plot(plus_array[:, 2], plus_array[:, 0], color="red", linestyle="-")
            ax.plot(minus_array[:, 2], minus_array[:, 0], color="red", linestyle="-")
        else:
            ax.plot(plus_array[:, 2], plus_array[:, 1], color="red", linestyle="-")
            ax.plot(minus_array[:, 2], minus_array[:, 1], color="red", linestyle="-")




