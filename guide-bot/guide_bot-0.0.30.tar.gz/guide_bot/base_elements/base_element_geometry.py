import numpy as np

from scipy.spatial.transform import Rotation as R

from guide_bot.parameters.instrument_parameters import InstrumentParameter


class BaseElementGeometry:
    """
    Stores geometry parameters for generic element, takes either raw values or parameters

    When using parameters, the state of the geometry object can be updated with
    the load_new_state method.
    """
    def __init__(self, start_point, next_start_point, start_width, start_height, end_width, end_height):

        self.instrument_parameters = {}
        self.all_parameter_types = {}

        # Required parameters, sub classes can introduce more
        self.set_parameter_attribute("start_point", start_point, par_type="start_point")
        self.set_parameter_attribute("next_start_point", next_start_point, par_type="start_point")
        self.set_parameter_attribute("start_width", start_width, par_type="horizontal")
        self.set_parameter_attribute("start_height", start_height, par_type="vertical")
        self.set_parameter_attribute("end_width", end_width, par_type="horizontal")
        self.set_parameter_attribute("end_height", end_height, par_type="vertical")

        # Control parameter to enable / disable drawing
        self.visible = True
        # Control line style for plotting
        self.linestyle = "-"
        # Control parameter for number of points in plotting
        self.plot_resolution = 2

    def evaluate(self, input, register_name=None):
        """
        Evaluates an input of either a number or instrument parameter type

        If register_name is specified, the variable is registred in this objects
        dict of variables that need to be reevaluated when a new state is loaded.

        Parameters
        ----------

        input : float, int or InstrumentParameter
            Input that needs to be evaluated to float

        register_name : str or None
            If str given, the variable will be saved with this name in parameter dict
        """

        if isinstance(input, InstrumentParameter):
            if register_name is not None:
                self.instrument_parameters[register_name] = input
            input.calculate()
            return input.get_value()
        elif isinstance(input, (float, int)):
            return input
        else:
            raise ValueError("input type not recoignized")

    def set_parameter_attribute(self, name, variable, par_type=None):
        """
        Set a new parameter, if InstrumentParameter store in variables
        """

        setattr(self, name, self.evaluate(variable, register_name=name))

        if par_type is None:
            par_type = ""

        if par_type not in ["start_point", "horizontal", "vertical", ""]:
            raise ValueError("par_type not recognized.")

        self.all_parameter_types[name] = par_type

    def load_new_state(self):
        """
        Load new state from InstrumentParameters that could be updated
        """
        for par_name in self.instrument_parameters:
            variable = self.instrument_parameters[par_name]
            variable.calculate()
            setattr(self, par_name, variable.get_value())

    def write_to_log(self, file, class_name, element_name):
        """
        Writes all parameters to guide_log
        """

        file.write("\nElement " + class_name + " " + element_name + "\n")
        for parameter_name in self.all_parameter_types:
            if parameter_name not in self.instrument_parameters:
                raise RuntimeError("Logging requires all parameters are instrument parameters.")

            variable_name = self.instrument_parameters[parameter_name].name
            par_type = self.all_parameter_types[parameter_name]

            string = parameter_name.ljust(29) + par_type.ljust(15) + variable_name.ljust(50)
            file.write(" " + string + "\n")

    def continue_center_line(self, start_pr, distance_unit_less):
        """
        Description of center_line, to be overwritten by element

        Default center_line method for simple straight element. Calculates
        the position and orientation of a point along the center of the
        element given a unit less distance from 0 to 1, 0 corresponding to the
        start and 1 to the end. Requires a starting point and orientation
        and returns a point and orientation, as the element could turn.

        Parameters
        ----------

        start_pr : PositionAndRotation
            Start point and orientation for this element in 3D space

        distance_unit_less : float
            Fraction of element length for location of returned point / orientation
        """

        if self.next_start_point is None or self.start_point is None:
            print("None detected in: ", self.__class__.__name__)

        length = self.next_start_point - self.start_point
        this_position = length * distance_unit_less

        z_vector = np.array([0, 0, 1])

        start_direction = start_pr.rotation
        z_vector = start_direction.apply(z_vector)

        updated_position = start_pr.position + this_position * z_vector

        return PositionAndRotation(updated_position, start_pr.rotation)

    def create_start_pr(self):
        # start position and rotation
        return PositionAndRotation(np.array([0, 0, 0]), R.from_euler("z", 0))

    def get_width(self, distance_unit_less):
        assert isinstance(distance_unit_less, (int, float))

        return self.start_width + (self.end_width - self.start_width) * distance_unit_less

    def get_height(self, distance_unit_less):
        assert isinstance(distance_unit_less, (int, float))

        return self.start_height + (self.end_height - self.start_height) * distance_unit_less

    def get_dimension(self, distance_unit_less, horizontal=True):
        if horizontal:
            return self.get_width(distance_unit_less)
        else:
            return self.get_height(distance_unit_less)

    def extra_los_points(self, start_pr, distance_unit_less):
        """
        Allows classes that inherit from this to define additional los points as needed
        """
        return []

    def get_los_points(self, start_pr, distance_unit_less):

        pr = self.continue_center_line(start_pr=start_pr, distance_unit_less=distance_unit_less)
        width = self.get_width(distance_unit_less=distance_unit_less)
        height = self.get_height(distance_unit_less=distance_unit_less)

        center = pr.position
        mx, px = pr.get_points(width, horizontal=True)
        my, py = pr.get_points(height, horizontal=False)

        extra_points = self.extra_los_points(start_pr=start_pr, distance_unit_less=distance_unit_less)

        return [center, px, mx, py, my] + extra_points

    def get_corners(self, start_pr, distance_unit_less):

        pr = self.continue_center_line(start_pr=start_pr, distance_unit_less=distance_unit_less)
        width = self.get_width(distance_unit_less=distance_unit_less)
        height = self.get_height(distance_unit_less=distance_unit_less)

        return pr.get_corners(width=width, height=height)

    def plot_on_ax(self, ax, start_pr, horizontal=True, color="k"):

        if start_pr is None:
            start_pr = self.create_start_pr()

        if not self.visible:
            self.plot_extra(ax=ax, start_pr=start_pr, horizontal=horizontal, color=color)
            return self.continue_center_line(start_pr, 1)

        distances = np.linspace(0, 1, self.plot_resolution)
        plus_array = np.zeros((self.plot_resolution, 3)) # right / top depending on horizontal
        minus_array = np.zeros((self.plot_resolution, 3)) # left / bottom depending on horizontal

        for index, distance in enumerate(distances):
            this_pr = self.continue_center_line(start_pr, distance)
            dim = self.get_dimension(distance, horizontal)
            minus_array[index, :], plus_array[index, :] = this_pr.get_points(dim, horizontal)

        if horizontal:
            ax.plot(plus_array[:, 2], plus_array[:, 0], color=color, linestyle=self.linestyle)
            ax.plot(minus_array[:, 2], minus_array[:, 0], color=color, linestyle=self.linestyle)
        else:
            ax.plot(plus_array[:, 2], plus_array[:, 1], color=color, linestyle=self.linestyle)
            ax.plot(minus_array[:, 2], minus_array[:, 1], color=color, linestyle=self.linestyle)

        self.plot_extra(ax=ax, start_pr=start_pr, horizontal=horizontal, color=color)

        return this_pr  # Returns end pr

    def plot_extra(self, ax, start_pr, horizontal, color):
        """
        Allows Geometry classes to plot something extra in addition to the walls
        """
        pass


def nan_in_array(array):
    return np.isnan(np.sum(array))


class PositionAndRotation:
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation

    @classmethod
    def origin(cls):
        return PositionAndRotation(np.array([0, 0, 0]), R.from_euler("z", 0))

    def width_points(self, width):

        x_vector = np.array([0.5, 0, 0])
        x_vector = self.rotation.apply(x_vector)

        m_position = self.position - width * x_vector
        p_position = self.position + width * x_vector

        return m_position, p_position

    def height_points(self, height):

        y_vector = np.array([0, 0.5, 0])
        y_vector = self.rotation.apply(y_vector)

        m_position = self.position - height * y_vector
        p_position = self.position + height * y_vector

        return m_position, p_position

    def get_corners(self, width, height):

        x_vector = np.array([0.5, 0, 0])
        x_vector = self.rotation.apply(x_vector)
        y_vector = np.array([0, 0.5, 0])
        y_vector = self.rotation.apply(y_vector)

        corner1 = self.position - width * x_vector - height * y_vector
        corner2 = self.position - width * x_vector + height * y_vector
        corner3 = self.position + width * x_vector + height * y_vector
        corner4 = self.position + width * x_vector - height * y_vector

        return [corner1, corner2, corner3, corner4]

    def point_and_normal(self):
        z_vector = np.array([0, 0, 1])
        z_vector = self.rotation.apply(z_vector)
        return self.position, z_vector

    def get_points(self, distance, horizontal):
        """
        Provides 3D points for plotting

        Takes distance between points and whether it is in the
        horizontal direction or vertical (True / False).

        distance: float
            distance between points

        horizontal: bool
            are they spaced horizontally or vertically
        """
        if horizontal:
            return self.width_points(distance)
        else:
            return self.height_points(distance)

    def __repr__(self):
        string = "PositionAndRotation\n"
        string += " Position: " + str(self.position) + "\n"
        string += " Rotation: \n" + str(self.rotation.as_matrix()) + "\n"

        return string


def line_intersect_plane(point0, point1, pr, epsilon=1E-6):
    plane_point, plane_normal = pr.point_and_normal()

    u = point1 - point0
    dot = plane_normal.dot(u)

    if abs(dot) > epsilon:
        w = point0 - plane_point
        fac = - plane_normal.dot(w)/dot
        return point0 + (u * fac)

    return None


def inside_polygon(point, corners, epsilon=1E-6):
    """
    A point is in a polygon if the angle between the test point and each pair of edge points sum to 2 pi
    """

    angle_sum = 0.0
    shifted_corners = corners[1:] + corners[:-1]

    for p0, p1 in zip(corners, shifted_corners):
        vec0 = p0 - point
        vec1 = p1 - point

        m0 = np.linalg.norm(vec0)
        m1 = np.linalg.norm(vec1)
        if m0*m1 <= epsilon:
            return True  # On a node, considered inside
        else:
            costheta = vec0.dot(vec1) / (m0*m1)

        angle_sum += np.arccos(costheta)

    return abs(2*np.pi - angle_sum) < epsilon


class GuidePoint:
    """
    Describes point in the guide with associated los points and corner points

    The los points are used as origins for rays used to test line of sight,
    while the corner points are used to check if a ray passes through the
    guide at that point in the guide. The corners constitute a goal post.
    The class can either be initialized with a distance_unit_less or an
    element_point. The element_point can be a distance from start or end
    of the element.
    """
    def __init__(self, element, start_pr, distance_unit_less=None, element_point=None):
        """
        Describes los points and corners at a certain point along the guide

        Parameters
        ----------

        element : GuideElement
            The element for which a guide point are to be made

        start_pr : PositionAndRotation
            Position/Rotation at the start of the element

        distance_unit_less : float between 0 and 1
            How far along this guide element the position should be

        element_point : ElementPoint
            An element_point object describing where in the element the point should be
        """

        geometry = element.get_geometry()

        start = element.start_point_parameter.get_value()
        end = element.next_start_point_parameter.get_value()
        length = end - start

        if distance_unit_less is None and element_point is None:
            raise RuntimeError("Need to set either unit_less_distance or element_point in GuidePoint")

        if element_point is not None:
            distance_unit_less = element_point.get_fraction(length)

        self.guide_position = start + distance_unit_less * length

        self.pr = geometry.continue_center_line(start_pr=start_pr, distance_unit_less=distance_unit_less)
        self.los_points = geometry.get_los_points(start_pr=start_pr, distance_unit_less=distance_unit_less)
        self.corners = geometry.get_corners(start_pr=start_pr, distance_unit_less=distance_unit_less)

        # Sanity check
        for point in self.los_points:
            if point is None:
                raise ValueError("Invalid los_point returned from ", element.name)

            if np.isnan(np.sum(point)):
                raise ValueError("nan detected in los_point returned from", element.name)

        for point in self.corners:
            if point is None:
                raise ValueError("Invalid corner returned from ", element.name)

            if np.isnan(np.sum(point)):
                raise ValueError("nan detected in corners returned from", element.name)

        self.distance_unit_less = distance_unit_less
        self.name = element.name

    def __repr__(self):
        string = f"GuidePoint {self.name} dul={self.distance_unit_less} at {self.guide_position} m\n"
        string += "los points:\n"
        for los_point in self.los_points:
            string += los_point.__repr__() + "\n"
        string += "corners: \n"
        for corner in self.corners:
            string += corner.__repr__() + "\n"

        return string
