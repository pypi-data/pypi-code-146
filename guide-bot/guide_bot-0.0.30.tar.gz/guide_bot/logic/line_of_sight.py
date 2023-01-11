from guide_bot.base_elements.guide_elements import GuideElement
from guide_bot.base_elements.base_element_geometry import PositionAndRotation
from guide_bot.base_elements.base_element_geometry import line_intersect_plane
from guide_bot.base_elements.base_element_geometry import inside_polygon
from guide_bot.base_elements.base_element_geometry import GuidePoint

import matplotlib.pyplot as plt


class LosError(Exception):
    pass


class ElementPoint:
    def __init__(self, element_name, from_start=None, from_end=None, fraction=None):

        # If user provides a GuideElement object, get its name
        if isinstance(element_name, GuideElement):
            element_name = element_name.get_name()

        self.element_name = element_name
        self.from_start = from_start
        self.from_end = from_end
        self.fraction = fraction

        self.min_length = None

        unused_inputs = sum([self.from_start is None, self.from_end is None, self.fraction is None])
        if unused_inputs == 3:
            # If no info, resort to start of element
            self.from_start = 0
        elif unused_inputs < 2:
            # If 2 or 3 specified by the user,
            raise ValueError("Use only of one from_start, from_end or fraction keywords to specify los point.")

        if self.from_start is not None:
            self.mode = "from_start"
            self.min_length = self.from_start
        elif self.from_end is not None:
            self.mode = "from_end"
            self.min_length = self.from_end
        elif self.fraction is not None:
            self.mode = "fraction"

    def get_fraction(self, element_length):
        if self.mode == "fraction":
            return self.fraction
        elif self.mode == "from_start":
            return self.from_start / element_length
        elif self.mode == "from_end":
            return (element_length - self.from_end) / element_length
        else:
            raise RuntimeError("No mode set for ElementPoint.")

    def get_name(self):
        return self.element_name

    def get_min_length(self):
        return self.min_length

    def __repr__(self):
        string = "ElementPoint: Element: '" + self.get_name() + "' "
        if self.mode == "fraction":
            string += "at " + str(self.fraction*100) + "% of length."
        elif self.mode == "from_start":
            string += "at " + str(self.from_start) + "m after start."
        elif self.mode == "from_end":
            string += "at " + str(self.from_end) + "m before end."

        return string


class LineOfSightSection:
    def __init__(self, start, end):
        if isinstance(start, (ElementPoint, float, int)):
            self.start = start
        else:
            raise ValueError("Need ElementPoint or float to define los start.")

        if isinstance(end, (ElementPoint, float, int)):
            self.end = end
        else:
            raise ValueError("Need ElementPoint or float to define los end.")

        if isinstance(self.start, (float, int)) and isinstance(self.end, (float, int)):
            if self.start > self.end:
                raise ValueError("LOS section start needs to be after end!")

    def get_element_names(self):
        element_names = []
        if isinstance(self.start, ElementPoint):
            element_names.append(self.start.element_name)

        if isinstance(self.end, ElementPoint):
            element_names.append(self.end.element_name)

        return element_names

    def get_start_name(self):
        if isinstance(self.start, ElementPoint):
            return self.start.element_name
        else:
            return None

    def get_end_name(self):
        if isinstance(self.end, ElementPoint):
            return self.end.element_name
        else:
            return None

    def included_elements(self, guide):

        if not (isinstance(self.start, ElementPoint) and isinstance(self.end, ElementPoint)):
            return RuntimeError("Can't determine which elements are in los section.")

        elements_in_section = []
        in_section = False
        for guide_element_name in guide.get_element_names():
            if guide_element_name == self.get_start_name():
                in_section = True

            if in_section:
                elements_in_section.append(guide.get_element(guide_element_name))

            if guide_element_name == self.get_end_name():
                in_section = False

        return elements_in_section

    def included_breakers(self, guide, los_breakers):

        elements_in_section = self.included_elements(guide)

        los_breakers_in_section = []
        for los_breaker in los_breakers:
            if los_breaker.name in [x.name for x in elements_in_section]:
                los_breakers_in_section.append(los_breaker)

        return los_breakers_in_section

    def __repr__(self):
        string = "Line of sight section.\n"
        string += "  Start: " + str(self.start) + "\n"
        string += "  End  : " + str(self.end) + "\n"
        return string


class LosCalculator:
    def __init__(self, guide):
        """
        Sets up a line of sight calculator

        The line of sight calculator gets all necessary information from the
        guide object and can adjust the parameters pertaining to breaking
        line of sight directly through the guide object. Using the solve_los
        method sets these important parameters to the smallest possible
        that breaks line of sight as specified in the los_sections contained
        in the guide object. Some precision is lost as this is an iterative
        approach, but good accuracy is achieved in reasonably short time.

        Parameters
        ----------

        guide : Guide
            Guide through which line of sight should be blocked
        """
        self.guide = guide

        # Prepare los problem

        # Find line of sight sections and corresponding los parameters
        self.specified_los_sections = self.guide.get_los_sections()
        if len(self.specified_los_sections) > 0:
            self.los_calculation_needed = True
        else:
            self.los_calculation_needed = False

        self.los_breakers = self.guide.get_los_breakers()  # Only finds dynamic los breakers

    def find_los_point(self, distance):
        """
        Given a distance from the source and the guide, find element description of that position
        """

        for element in self.guide.guide_elements:
            start_point = element.start_point_parameter.get_value()
            end_point = element.next_start_point_parameter.get_value()
            if start_point <= distance < end_point:
                fraction = (distance - start_point)/(end_point - start_point)
                return ElementPoint(element.name, fraction=fraction)

        guide_start = self.guide.guide_elements[0].start_point_parameter.get_value()
        guide_end = self.guide.guide_elements[-1].next_start_point_parameter.get_value()
        raise ValueError("Given distance '" + str(distance)
                         + "' is outside of current guide range. "
                         + "The guide starts at " + str(guide_start)
                         + " and ends at " + str(guide_end) + ".")

    def solve_los(self):
        """
        Requires all free parameters have a set value from optimizer
        """

        print("In solve_los")
        if not self.los_calculation_needed:
            print("No los calculation needed")
            return

        # Can now find which los breakers can impact which los sections
        # Transform distances from source to points in modules

        los_sections = []
        for specified_los_section in self.specified_los_sections:

            if specified_los_section.get_start_name() is None:
                # find what element and get ElementPoint describing the point
                start = self.find_los_point(distance=specified_los_section.start)
            else:
                # Already given as a ElementPoint
                start = specified_los_section.start

            if specified_los_section.get_end_name() is None:
                # Find what element and get ElementPoint describing the point
                end = self.find_los_point(distance=specified_los_section.end)
            else:
                # Already given as a ElementPoint
                end = specified_los_section.end

            los_sections.append(LineOfSightSection(start, end))

        # Set all los sections to zero
        for los_breaker in self.los_breakers:
            los_breaker.set_los_value(0.0)

        print("Attempting to solving line of sight.")
        for los_section in los_sections:
            self.solve_section(los_section, self.los_breakers)

    def solve_section(self, los_section, all_los_breakers):
        """
        Avoids line of sight in section by tuning the relevant los breakers

        Parameters
        ----------
        los_section : LosSection
            Line of sight section using only ElementPoint

        all_los_breakers : List of LosBreakerGuideElement
            List of the line of sight breakers in the guide
        """

        los_breakers = los_section.included_breakers(self.guide, all_los_breakers)

        # Branch into simple and complex case depending on number of los_breakers
        if len(los_breakers) == 1:
            print("One los breaker:")
            print(los_breakers)

            los_breaker = los_breakers[0]
            current_los_value = los_breaker.get_los_value()

            if current_los_value is None:
                los_breaker.set_los_value(0.0)
                current_los_value = los_breaker.get_los_value()

            if not self.check_los(los_section):
                print("Found los broken without increasing los parameter!")
                return

            # big steps to find angle without line of sight (unit degrees)
            increment_value = 0.5
            limit = 20.0
            value = current_los_value
            while self.check_los(los_section):
                last_value = value
                value += increment_value
                if value >= limit:
                    raise LosError("Can not solve los with los value < 20.0")

                los_breaker.set_los_value(value)

            # Los is broken somewhere between last_value and value
            lower_bound = last_value
            upper_bound = value

            while upper_bound - lower_bound > 0.0001:
                mid_point = 0.5*(upper_bound + lower_bound)
                los_breaker.set_los_value(mid_point)
                if self.check_los(los_section):
                    lower_bound = mid_point
                else:
                    upper_bound = mid_point

            los_breaker.set_los_value(upper_bound)  # Ensure we cut line of sight, highest blocked value
            print("LOS result:", upper_bound)

            return

        else:
            self.guide.print_start_points()
            print(los_section)
            raise LosError("Case with none or multiple los breakers in segment has yet to be implemented.")

    def check_los(self, los_section):
        """
        Returns true if there is line of sight in this section, and false if blocked

        This method construct a list of GuidePoints which contains both los points
        and corners. The los points are used as origins / ends of rays, and the
        corners are used as a goal. The los_section determines where in the guide
        the section starts and stops, and only the part of the guide between those
        two points needs to be considered. All combinations of GuidePoints are used
        as origin / end of rays, except those combinations where the origin is
        further along in the guide than the end (which just saves computational
        time). The cases where origin and end is the same is also ignored. When
        the rays are generated, it is checked whether they go through the goals
        made by all the other GuidePoints, and if a ray does, there is line of
        sight. If no ray does, then line of sight is blocked.

        Parameters
        ----------

        los_section: los_section
            los_section that use only ElementPoints as start/end
        """
        elements = los_section.included_elements(self.guide)

        origin_pr = PositionAndRotation.origin()
        guide_points = []

        if len(elements) == 1:
            guide_points += elements[0].get_los_points(start_pr=origin_pr, los_start=los_section.start,
                                                       los_end=los_section.end)
        else:
            start_element = elements[0]
            guide_points += start_element.get_los_points(start_pr=origin_pr, los_start=los_section.start)

            # Move position/rotation to end of first element
            start_element_geometry = start_element.get_geometry()
            pr = start_element_geometry.continue_center_line(start_pr=origin_pr, distance_unit_less=1.0)

            # Collect guide points for elements between start and end
            for element in elements[1:-1]:
                guide_points += element.get_los_points(start_pr=pr, distance_unit_less=0.0)

                geometry = element.get_geometry()
                pr = geometry.continue_center_line(start_pr=pr, distance_unit_less=1.0)

            end_element = elements[-1]
            guide_points += end_element.get_los_points(start_pr=pr, distance_unit_less=0.0, los_end=los_section.end)

        if len(guide_points) <= 1:
            raise RuntimeError("Problem with guide points")

        #print(guide_points)

        #fig, axs = plt.subplots(figsize=(10, 10), nrows=2, ncols=1)
        #self.guide.plot_guide_ax(from_top_ax=axs[0], from_side_ax=axs[1])

        for start_guide_point in guide_points:
            for end_guide_point in guide_points:
                if start_guide_point is end_guide_point:
                    # No need to run for the same two point, not well defined behavior
                    continue

                if start_guide_point.guide_position > end_guide_point.guide_position:
                    # Symmetric problem, choose to just run if start earlier than end
                    continue

                #if line_of_sight(start_guide_point, end_guide_point, guide_points, ft_ax=axs[0], fs_ax=axs[1]):
                if line_of_sight(start_guide_point, end_guide_point, guide_points):
                    return True

        #plt.show()
        # If all generated lines are blocked, there is not line of sight
        return False


def line_of_sight(start_guide_point, end_guide_point, guide_points, ft_ax=None, fs_ax=None):
    """
    Checks if any line defined by combinations of start/end points go through all goals

    If a line goes through all goals, there is line of sight through the guide.
    """
    for start_p in start_guide_point.los_points:
        for end_p in end_guide_point.los_points:
            # Ray is defined by start_p and end_p which are both 3D points

            los_status = True  # Assume los, then check
            for goal in guide_points:
                # The ray has to pass through all goals to have line of sight
                if goal is start_guide_point or goal is end_guide_point:
                    # Can skip when goal coincides with start or end, they obviously pass
                    continue

                """
                print("plotting", start_p, end_p)
                ft_ax.plot([start_p[2], end_p[2]], [start_p[0], end_p[0]], "grey")
                fs_ax.plot([start_p[2], end_p[2]], [start_p[1], end_p[1]], "grey")
                """

                # Check if this ray intersect the goal
                intersect = line_intersect_plane(start_p, end_p, goal.pr)
                if intersect is None:
                    # line is parallel to plane.
                    los_status = False
                    break

                if not inside_polygon(intersect, goal.corners, epsilon=1E-6):
                    # If not, line of sight is broken
                    los_status = False
                    break  # Go to next ray

            if los_status:
                # If this rays passed through all goals, there is line of sight
                return True

    # If none of the generated rays have line of sight, line of sight is considered blocked
    return False












