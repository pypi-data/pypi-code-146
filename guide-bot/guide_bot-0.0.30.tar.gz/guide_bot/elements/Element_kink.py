import numpy as np

from scipy.spatial.transform import Rotation as R

from guide_bot.base_elements import guide_elements
from guide_bot.parameters import instrument_parameters as ipars
from guide_bot.base_elements.base_element_geometry import BaseElementGeometry
from guide_bot.base_elements.base_element_geometry import PositionAndRotation


class Kink(guide_elements.LosBreakerGuideElement):
    """
    Kink GuideElement that inserts an empty space and kink into a guide

    A Kink still has start and end dimensions as it is supposed to fit with the
    surrounding elements, as if it was a guide element. In this way, it can
    for example be used to set a Kink for a chopper, and force the adjacent
    Elements to narrow to the required width / height for the chopper. A kink
    changes the position and direction of a guide element after.
    """

    def __init__(self, name, length=None, start_point=None,
                 start_width=None, start_height=None,
                 end_width=None, end_height=None, angle=None,
                 h_displacement=None, v_displacement=None,
                 displacement=None, kink_dir="horizontal",
                 optimize=False, **kwargs):
        """
        Kink GuideElement that inserts an empty space into a guide

        A Kink still has start and end dimensions as it is supposed to fit with
        the surrounding elements, as if it was a guide element. In this way,
        it can for example be used to set a Kink for a chopper, and force the
        adjacent Elements to narrow to the required width / height for the
        chopper. If end_width / end_height is specified, they will override
        the following modules start_width / start_height settings. A kink
        changes the position and direction of a guide element after, the
        direction is controlled with kink_dir, and a small displacement is
        included unless disabled with for example displacement=0.

        Parameters
        ----------
        name : str
            Name of the element

        length : (float, None, InstrumentParameter)
            Length of guide element, optimized parameter

        start_point : (float, None, InstrumentParameter)
            Distance from source to start of the Kink element

        start_width : (float, None, InstrumentParameter)
            Width of the start of the Kink

        start_height : (float, None, InstrumentParameter)
            Height of the start of the Kink

        end_width : (float, None, InstrumentParameter)
            Width of the end of the Kink

        end_height : (float, None, InstrumentParameter)
            Height of the end of the Kink

        kink_dir : str
            Allowed: 'horizontal', 'vertical', 'left', 'right', 'up', 'down'

        h_displacement : float
            Horizontal displacement of next element [m]

        v_displacement : float
            Vertical displacement of next element [m]

        displacement : float
            Sets both horizontal and vertical displacement simultaneously
        """

        if displacement is not None:
            h_displacement = displacement
            v_displacement = displacement

        # Internalize stuff relevant for this Element

        super().__init__(name, length=length, start_point=start_point,
                         start_width=start_width, start_height=start_height,
                         end_width=end_width, end_height=end_height, **kwargs)

        if kink_dir == "left":
            self.horizontal_kink_par = ipars.FixedInstrumentParameter(self.name + "_horizontal", 1)
            self.kink_sign = 1.0
            min_angle = 0
            max_angle = 3
        elif kink_dir == "right":
            self.horizontal_kink_par = ipars.FixedInstrumentParameter(self.name + "_horizontal", 1)
            self.kink_sign = -1.0
            min_angle = -3
            max_angle = 0
        elif kink_dir == "horizontal":
            self.horizontal_kink_par = ipars.FixedInstrumentParameter(self.name + "_horizontal", 1)
            self.kink_sign = None
            min_angle = -3
            max_angle = 3
        elif kink_dir == "up":
            self.horizontal_kink_par = ipars.FixedInstrumentParameter(self.name + "_horizontal", -1)
            self.kink_sign = 1.0
            min_angle = 0
            max_angle = 3
        elif kink_dir == "down":
            self.horizontal_kink_par = ipars.FixedInstrumentParameter(self.name + "_horizontal", -1)
            self.kink_sign = -1.0
            min_angle = -3
            max_angle = 0
        elif kink_dir == "vertical":
            self.horizontal_kink_par = ipars.FixedInstrumentParameter(self.name + "_horizontal", -1)
            self.kink_sign = None
            min_angle = -3
            max_angle = 3
        else:
            raise RuntimeError("The parameter kink_dir is only allowed these options: "
                               + "left, right, horizontal, up, down, vertical.\n"
                               + "kink_dir was '" + str(kink_dir) + "'.")

        self.kink_angle = guide_elements.handle_input_parameter(name + "_kink_angle", angle,
                                                                default_min=min_angle, default_max=max_angle)

        # Temporary system for switching to a LosInstrumentParameter
        if not optimize and isinstance(self.kink_angle, ipars.RelativeFreeInstrumentParameter):
            # Not specified and not free with the intent of optimizing for performance.
            self.kink_angle = ipars.LosInstrumentParameter(self.kink_angle.name)
            self.dynamic_los_breaker = True
        else:
            # Either fixed or free with the intent of optimizing for performance, not breaking los
            self.dynamic_los_breaker = False

        self.h_displacement = guide_elements.handle_input_parameter(name + "_h_displacement", h_displacement,
                                                                    default_min=-0.03, default_max=0.03)
        self.v_displacement = guide_elements.handle_input_parameter(name + "_v_displacement", v_displacement,
                                                                    default_min=-0.03, default_max=0.03)

    def get_source_focus(self):
        """
        A source needs to focus at the end of a kink
        """

        effective_width = self.end_width.name + " + 2*" + self.h_displacement.name
        effective_height = self.end_height.name + " + 2*" + self.v_displacement.name
        end_distance = self.next_start_point_parameter.name

        return dict(width=effective_width, height=effective_height, dist=end_distance)

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
        if not isinstance(self.kink_angle, ipars.LosInstrumentParameter):
            return

        if self.kink_sign is None:
            self.kink_angle.set_value(value)  # default left
        else:
            self.kink_angle.set_value(self.kink_sign*value)

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
        return abs(self.kink_angle.get_value())

    def add_to_instr(self):
        """
        Adds code describing the Kink element to the current McStas instrument

        This methods uses McStasScript to add components and code to a McStas
        instrument object. The McStas instrument object is an attribute of the
        class called current_instrument. New instrument parameters can also be
        created and added to the optimization by using the current_parameters
        attribute.

        Since the add_to_instr method of all the Elements are called in order
        from the sample to the source, it is important the components are
        added after the Origin component to ensure the correct order.
        """

        self.current_parameters.add_parameter(self.kink_angle)
        self.current_parameters.add_parameter(self.h_displacement)
        self.current_parameters.add_parameter(self.v_displacement)
        self.current_parameters.add_parameter(self.horizontal_kink_par)

        Kink = self.current_instrument.add_component(self.end_component_name, "Arm")
        position = [self.h_displacement.name, self.v_displacement.name, self.get_length_name()]
        Kink.set_AT(position, RELATIVE=self.reference_component_name)

        if self.horizontal_kink_par.get_value() == 1:
            Kink.set_ROTATED([0, self.kink_angle.name, 0], RELATIVE=self.reference_component_name)
        elif self.horizontal_kink_par.get_value() == -1:
            Kink.set_ROTATED([self.kink_angle.name, 0, 0], RELATIVE=self.reference_component_name)
        else:
            raise ValueError("horizontal_kink_par had illegal value.")

    def get_geometry(self):
        return GeometryKink(start_point=self.start_point_parameter, next_start_point=self.next_start_point_parameter,
                            start_width=self.start_width, start_height=self.start_height,
                            end_width=self.end_width, end_height=self.end_height,
                            kink_angle=self.kink_angle, horizontal_kink=self.horizontal_kink_par,
                            h_displacement=self.h_displacement, v_displacement=self.v_displacement)


class GeometryKink(BaseElementGeometry):
    def __init__(self, start_point, next_start_point, start_width, start_height, end_width, end_height,
                 kink_angle, horizontal_kink, h_displacement, v_displacement):

        super().__init__(start_point=start_point, next_start_point=next_start_point,
                         start_width=start_width, start_height=start_height,
                         end_width=end_width, end_height=end_height)

        if self.evaluate(horizontal_kink) == 1:
            direction = "horizontal"
        else:
            direction = "vertical"

        self.set_parameter_attribute("kink_angle", kink_angle, par_type=direction)
        self.set_parameter_attribute("horizontal_kink", horizontal_kink, par_type=direction)
        self.set_parameter_attribute("h_displacement", h_displacement, par_type="horizontal")
        self.set_parameter_attribute("v_displacement", v_displacement, par_type="vertical")

        self.visible = False  # Disable plotting of this element

    def extra_los_points(self, start_pr, distance_unit_less):
        """
        Places extra line of sight check points in a strategic manner to avoid
        a case where a narrow guide and a tall guide have a kink in between them
        and line of sight is not found because the points in the center are both
        blocked. By adding extra points using the translation described by
        displacement variables, line of sight is found again.

        Parameters
        ----------
        start_pr : PositionAndRotation
            point/rotation at start of element

        distance_unit_less : float between 0 and 1
            fraction of the element to transverse before producing points

        """

        pr = self.continue_center_line(start_pr=start_pr, distance_unit_less=distance_unit_less)
        width = self.get_width(distance_unit_less=distance_unit_less)
        height = self.get_height(distance_unit_less=distance_unit_less)

        extra_points = []
        if abs(self.h_displacement) < 0.5 * width and self.h_displacement != 0:
            mx, px = pr.get_points(2.0*self.h_displacement, horizontal=True)
            extra_points.append(px)

        if abs(self.v_displacement) < 0.5 * height and self.v_displacement != 0:
            my, py = pr.get_points(2.0*self.v_displacement, horizontal=False)
            extra_points.append(py)

        return extra_points

    def continue_center_line(self, start_pr, distance_unit_less):

        if distance_unit_less < 1E-6:
            return start_pr

        length = self.next_start_point - self.start_point

        displacement_x = self.h_displacement * distance_unit_less
        displacement_y = self.v_displacement * distance_unit_less
        displacement_z = length * distance_unit_less

        x_vector = np.array([1, 0, 0])
        y_vector = np.array([0, 1, 0])
        z_vector = np.array([0, 0, 1])

        start_direction = start_pr.rotation

        x_vector = start_direction.apply(x_vector)
        y_vector = start_direction.apply(y_vector)
        z_vector = start_direction.apply(z_vector)

        updated_position = start_pr.position + displacement_x * x_vector + displacement_y * y_vector + displacement_z * z_vector

        if self.horizontal_kink == 1:
            updated_rotation = start_pr.rotation * R.from_euler("y", self.kink_angle, degrees=True)
        elif self.horizontal_kink == -1:
            updated_rotation = start_pr.rotation * R.from_euler("x", self.kink_angle, degrees=True)
        else:
            raise RunetimeError("Parameter horizontal_kink must be -1 or 1.")

        return PositionAndRotation(updated_position, updated_rotation)