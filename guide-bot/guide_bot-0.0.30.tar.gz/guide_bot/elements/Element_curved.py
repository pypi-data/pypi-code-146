import numpy as np

from scipy.spatial.transform import Rotation as R

from guide_bot.base_elements import guide_elements
from guide_bot.base_elements.base_element_geometry import BaseElementGeometry
from guide_bot.base_elements.base_element_geometry import PositionAndRotation
from guide_bot.parameters import instrument_parameters as ipars
from guide_bot.base_elements.base_element_geometry import GuidePoint


class Curved(guide_elements.LosBreakerGuideElement):
    """
    Curved GuideElement that inserts a curved section into a guide

    A curved guide section with equal start and end dimensions,
    meaning it has a constant cross section.
    """

    def __init__(self, name, length=None, start_point=None,
                 start_width=None, start_height=None,
                 angle=None, bend="left",
                 **kwargs):
        """
        Curved GuideElement that inserts a curved section into a guide

        A curved guide section with equal start and end dimensions,
        meaning it has a constant cross section.

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
                         **kwargs)

        # This McStas component only supports constant cross section
        # start_width and start_height becomes properties that update end_width and end_height
        self.end_width = self.start_width
        self.end_height = self.start_height

        if bend == "left":
            self.horizontal_bend = True
            self.positive_bend = True

            self.horizontal_bend_par = ipars.FixedInstrumentParameter(self.name + "_horizontal", 1)
            self.positive_bend_par = ipars.FixedInstrumentParameter(self.name + "_bend_dir", 1)
        elif bend == "right":
            self.horizontal_bend = True
            self.positive_bend = False

            self.horizontal_bend_par = ipars.FixedInstrumentParameter(self.name + "_horizontal", 1)
            self.positive_bend_par = ipars.FixedInstrumentParameter(self.name + "_bend_dir", -1)
        elif bend == "down":
            self.horizontal_bend = False
            self.positive_bend = False

            self.horizontal_bend_par = ipars.FixedInstrumentParameter(self.name + "_horizontal", -1)
            self.positive_bend_par = ipars.FixedInstrumentParameter(self.name + "_bend_dir", -1)
        elif bend == "up":
            self.horizontal_bend = False
            self.positive_bend = True

            self.horizontal_bend_par = ipars.FixedInstrumentParameter(self.name + "_horizontal", -1)
            self.positive_bend_par = ipars.FixedInstrumentParameter(self.name + "_bend_dir", 1)
        else:
            raise ValueError("bend must be left, right, up or down (string).")

        # How to handle a los parameter?
        if angle is None:
            # automatic los
            self.dynamic_los_breaker = True
            self.angular_diversion = ipars.LosInstrumentParameter(self.name + "_angular_diversion")
        else:
            if isinstance(angle, ipars.FreeInstrumentParameter):
                raise ValueError("Not supported to have angular_diversion as a free parameter")
            elif isinstance(angle, ipars.InstrumentParameter):
                # Fixed or dependent
                self.dynamic_los_breaker = False
                self.angular_diversion = angle
            elif isinstance(angle, (float, int)):
                self.dynamic_los_breaker = False
                self.angular_diversion = ipars.FixedInstrumentParameter(self.name + "_angular_diversion", angle)
            else:
                raise ValueError("Unknown type of angle")

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

    @property
    def start_width(self):
        """
        Make start_width property so end_width can be updated with it
        """
        return self._start_width

    @start_width.setter
    def start_width(self, value):
        """
        Updates end_width to keep it in line with start_width
        """
        self.end_width = value
        self._start_width = value

    @property
    def start_height(self):
        """
        Make start_height property so end_height can be updated with it
        """
        return self._start_height

    @start_height.setter
    def start_height(self, value):
        """
        Updates end_height to keep it in line with start_height
        """
        self.end_height = value
        self._start_height = value

    def copy_components(self, destination):
        components_to_copy = ["Guide_curved_gravity_safe.comp"]

        self.copy_component(components_to_copy[0], destination)

        return components_to_copy

    def los_input(self, value):
        """
        Input for breaking line of sight, single value input

        The los input is a single value with the property that when it is
        increased, the los breaker becomes more likely to break line of sight.
        At a value of 0.0, it is assumed it wont break line of sight.
        If a value of 10 is reached and line of sight is not broken, an error
        is raised by the line of sight solver.
        This could be the angle in a kink, or the angle a curved guide turns,
        but it is also allowed to have several parameters controlled by the
        los_input. It is also possible to for example invert the sign, so that
        a kink could change directions depending on some other parameter.

        For kink the los input controls the kink angle, starting at 0.0. The
        user input is used to determine the sign.

        Parameters
        ----------

        value : float
            Control value for this line of sight breaker
        """
        #if not isinstance(self.angular_diversion, ipars.LosInstrumentParameter):
        #    return

        # currently in radians, needs to be changed
        radian_value = value * np.pi / 180.0
        self.angular_diversion.set_value(radian_value)  # direction handled elsewhere

    def get_los_status(self):
        """
        Get the los value that would recreate the current los state

        The los_input method uses a positive float value to set a more complex
        los state of the los breaker. Get los value retrieves such a value
        from the los element, meaning the output of this method has to be
        zero or a positive float number. It should roughly correspond to the
        angle deviation the los breaker introduces.

        Returns
        -------

        los_value corresponding to state of element
        """

        radian_value = self.angular_diversion.get_value()
        degree_value = radian_value * 180 / np.pi
        return abs(degree_value)

    def extra_los_points(self, start_pr, distance_unit_less=None, los_start=None, los_end=None):
        """
        Curved guide needs additional los_points and goal at the middle.
        """

        has_start = los_start is not None
        has_end = los_end is not None

        start = self.start_point_parameter.get_value()
        end = self.next_start_point_parameter.get_value()
        length = end - start

        if not has_start and not has_end:
            # Neither los start or end in the segment, set distance unit less to 0.5
            mid_frac = 0.5
        elif has_start and not has_end:
            # Set an extra point midway between start point and end of segment
            start_frac = los_start.get_fraction(length)
            mid_frac = 0.5*(start_frac + 1.0)
        elif not has_start and has_end:
            # Set an extra point midway between start of segment and end point
            end_frac = los_end.get_fraction(length)
            mid_frac = 0.5 * end_frac
        elif has_start and has_end:
            # Set an extra point midway between start point and end point
            start_frac = los_start.get_fraction(length)
            end_frac = los_end.get_fraction(length)
            mid_frac = 0.5*(start_frac + end_frac)
        else:
            raise RuntimeError("Error in curved element extra los_points.")

        return [GuidePoint(self, start_pr=start_pr, distance_unit_less=mid_frac)]

    def extra_repr(self):
        name_length = 25
        string = ""
        string += "angular_diversion:".ljust(name_length) + self.angular_diversion.__repr__() + "\n"
        string += "horizontal_bend_par:".ljust(name_length) + self.horizontal_bend_par.__repr__() + "\n"
        string += "positive_bend_par:".ljust(name_length) + self.positive_bend_par.__repr__() + "\n"
        return string

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

        self.current_parameters.add_parameter(self.angular_diversion)
        self.current_parameters.add_parameter(self.horizontal_bend_par)
        self.current_parameters.add_parameter(self.positive_bend_par)

        # Calculate curvature
        curvature_name = self.name + "_curvature"
        self.current_instrument.add_declare_var("double", curvature_name)

        curvature_calc = curvature_name + " = " + self.get_length_name() + "/" + self.angular_diversion.name + ";"
        self.current_instrument.append_initialize(curvature_calc)

        # Calculating end point of curved guide
        end_x_par_name = self.name + "_end_X"
        end_y_par_name = self.name + "_end_Y"
        end_z_par_name = self.name + "_end_Z"
        self.current_instrument.add_declare_var("double", end_x_par_name)
        self.current_instrument.add_declare_var("double", end_y_par_name)
        self.current_instrument.add_declare_var("double", end_z_par_name)

        if self.horizontal_bend and self.positive_bend:
            guide_z_rot = 0
            end_rot = [0, self.angular_diversion.name + "*RAD2DEG", 0]

            initialize_line1 = end_x_par_name + " = " + curvature_name + "*(1-cos(" + self.angular_diversion.name + "));"
            initialize_line2 = end_y_par_name + " = 0;"
            initialize_line3 = end_z_par_name + " = " + curvature_name + "*sin(" + self.angular_diversion.name + ");"

        elif self.horizontal_bend and not self.positive_bend:
            guide_z_rot = 180
            end_rot = [0, "-" + self.angular_diversion.name + "*RAD2DEG", 0]

            initialize_line1 = end_x_par_name + " = -" + curvature_name + "*(1-cos(" + self.angular_diversion.name + "));"
            initialize_line2 = end_y_par_name + " = 0;"
            initialize_line3 = end_z_par_name + " = " + curvature_name + "*sin(" + self.angular_diversion.name + ");"

        elif not self.horizontal_bend and self.positive_bend:
            guide_z_rot = 90
            end_rot = ["-" + self.angular_diversion.name + "*RAD2DEG", 0, 0]

            initialize_line1 = end_x_par_name + " = 0;"
            initialize_line2 = end_y_par_name + " = " + curvature_name + "*(1-cos(" + self.angular_diversion.name + "));"
            initialize_line3 = end_z_par_name + " = " + curvature_name + "*sin(" + self.angular_diversion.name + ");"

        elif not self.horizontal_bend and not self.positive_bend:
            guide_z_rot = 270
            end_rot = [self.angular_diversion.name + "*RAD2DEG", 0, 0]

            initialize_line1 = end_x_par_name + " = 0;"
            initialize_line2 = end_y_par_name + " = -" + curvature_name + "*(1-cos(" + self.angular_diversion.name + "));"
            initialize_line3 = end_z_par_name + " = " + curvature_name + "*sin(" + self.angular_diversion.name + ");"

        self.current_instrument.append_initialize(initialize_line1)
        self.current_instrument.append_initialize(initialize_line2)
        self.current_instrument.append_initialize(initialize_line3)

        guide = self.current_instrument.add_component(self.name, "Guide_curved_gravity_safe")
        guide.set_AT([0, 0, 0], RELATIVE=self.reference_component_name)
        guide.set_ROTATED([0, 0, guide_z_rot], RELATIVE=self.reference_component_name)

        # turning the guide to vertical direction switches horizontal and vertical.
        if self.horizontal_bend:
            guide.w1 = self.start_width.name
            guide.h1 = self.start_height.name
        else:
            guide.w1 = self.start_height.name
            guide.h1 = self.start_width.name

        guide.l = self.get_length_name()
        guide.curvature = curvature_name

        # Temporary reflectivity model
        guide.R0 = self.R0
        guide.m = self.m
        guide.Qc = self.Qc
        guide.alpha = self.alpha
        guide.W = self.W

        end_arm = self.current_instrument.add_component(self.end_component_name, "Arm")
        end_arm.set_AT([end_x_par_name, end_y_par_name, end_z_par_name], RELATIVE=self.reference_component_name)
        end_arm.set_ROTATED(end_rot, RELATIVE=self.reference_component_name)

    def get_geometry(self):
        return GeometryCurved(start_point=self.start_point_parameter, next_start_point=self.next_start_point_parameter,
                              start_width=self.start_width, start_height=self.start_height,
                              end_width=self.end_width, end_height=self.end_height,
                              angular_diversion=self.angular_diversion,
                              bend_horizontal=self.horizontal_bend_par, positive_bend_par=self.positive_bend_par)


class GeometryCurved(BaseElementGeometry):
    def __init__(self, start_point, next_start_point, start_width, start_height, end_width, end_height,
                 angular_diversion, bend_horizontal, positive_bend_par):

        super().__init__(start_point=start_point, next_start_point=next_start_point,
                         start_width=start_width, start_height=start_height,
                         end_width=end_width, end_height=end_height)

        if self.evaluate(bend_horizontal) == 1:
            direction = "horizontal"
        else:
            direction = "vertical"

        self.set_parameter_attribute("angular_diversion", angular_diversion, par_type=direction)
        self.set_parameter_attribute("bend_horizontal", bend_horizontal, par_type=direction)
        self.set_parameter_attribute("positive_bend_par", positive_bend_par, par_type=direction)

        self.plot_resolution = 60  # Number of points to plot

    def continue_center_line(self, start_pr, distance_unit_less):
        length = self.next_start_point - self.start_point

        if self.angular_diversion == 0.0:
            # Handle no angular_deviation by setting large curvature
            curvature = 1E9
            rotation = 0.0
            displacement_z = length*distance_unit_less
        else:
            curvature = length / self.angular_diversion
            rotation = distance_unit_less * self.angular_diversion
            displacement_z = curvature * np.sin(rotation)

        displacement = self.positive_bend_par * curvature * (1 - np.cos(rotation))
        if self.bend_horizontal == 1:
            displacement_x = displacement
            displacement_y = 0
        elif self.bend_horizontal == -1:
            displacement_x = 0
            displacement_y = displacement
        else:
            raise RuntimeError("Parameter bend_horizontal must be either 1 or -1.")

        x_vector = np.array([1, 0, 0])
        y_vector = np.array([0, 1, 0])
        z_vector = np.array([0, 0, 1])

        start_direction = start_pr.rotation

        x_vector = start_direction.apply(x_vector)
        y_vector = start_direction.apply(y_vector)
        z_vector = start_direction.apply(z_vector)

        updated_position = start_pr.position + displacement_x*x_vector + displacement_y*y_vector + displacement_z*z_vector
        if self.bend_horizontal == 1:
            updated_rotation = start_pr.rotation * R.from_euler("y", self.positive_bend_par * rotation)
        elif self.bend_horizontal == -1:
            updated_rotation = start_pr.rotation * R.from_euler("x", -self.positive_bend_par * rotation)
        else:
            raise RuntimeError("Parameter bend_horizontal must be either 1 or -1.")

        return PositionAndRotation(updated_position, updated_rotation)






