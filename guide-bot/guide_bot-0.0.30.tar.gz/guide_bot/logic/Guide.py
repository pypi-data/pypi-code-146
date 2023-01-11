import copy

import matplotlib.pyplot as plt

from guide_bot.parameters import instrument_parameters as ipars
from guide_bot.logic.line_of_sight import LineOfSightSection
from guide_bot.base_elements.guide_elements import LosBreakerGuideElement

class Guide:
    """
    Guide with elements and constraints, can be added to McStas instrument

    The main class for describing a neutron guide, internally keeping a list
    of the added guide modules and user defined constraints. In the main logic
    section of guide_bot, the methods of the Guide object are called to
    prepare for optimization. Since elements define their opening dimensions,
    the end dimensions provided by the user are shifted back to the next
    opening dimensions by the transfer_end_specifications method. The Guide
    can add code to a McStasScript instrument object using the
    add_to_instrument method, this is done from target (backend) to source, and
    the previous start dimensions are transferred to the next module in each step.
    """

    def __init__(self, name=None, instrument_length=None, target_guide_distance=None):
        """
        Provides a Guide object that describes a guide with given constraints

        Initially the guide object is empty, and guide elements should be
        added using the add_guide_element method. The collection of guide
        elements can then be added to a McStasScript instrument and optimized
        together. Constraints on user defined parameters can be added directly
        to this Guide object, these will be in addition to the constraints
        defined through the options of the individual modules. Can have a
        current_owner attribute set which sets that owner to Elements added to
        this guide.

        ----------
        Parameters

        name : str
            Optional name of the guide

        instrument_length : float
            Overwrite the instrument_length for this guide in particular

        target_guide_distance : float
            Overwrite the target_guide_distance for this guide in particular
        """
        self.guide_elements = []

        self.name = name
        self.auto_name = None
        self.generate_name()

        self.overwrite_instrument_length = instrument_length
        self.overwrite_target_guide_distance = target_guide_distance

        self.original_guide_elements = None

        self.constraints = []

        self.current_owner = None
        self.required_components = set()

        self.line_of_sight_sections = []

    def save_original(self):
        """
        Saves the original guide configuration
        """
        self.original_guide_elements = copy.deepcopy(self.guide_elements)

    def restore_original(self):
        """
        Restores to original guide configuration
        """
        self.guide_elements = copy.deepcopy(self.original_guide_elements)

    def generate_name(self):
        """
        Generates a name for this guide using first letter of each element
        """

        if self.auto_name is None:
            self.auto_name = self.name is None

        if self.auto_name:
            self.name = "Guide_"
            for element in self.guide_elements:
                first_letter = type(element).__name__[0]
                self.name += first_letter

    def make_name_unique(self, all_names):
        """
        Ensures the name of the guide is unique

        Parameters
        ----------

        all_names : list
            List of all guide names used to ensure this name is unique
        """
        suggested_name = self.name
        index = 0
        while suggested_name in all_names:
            suggested_name = self.name + "_Alt" + str(index)
            index += 1

        self.name = suggested_name
        return self.name

    def set_current_owner(self, owner):
        """
        Sets the current owner, added Elements will have this owner specified

        Parameters
        ----------

        owner : str
            Specifies the owner of this Element
        """
        self.current_owner = owner

    def add_guide_element(self, guide_element):
        """
        Adds a GuideElement to the Guide object

        This is the main method for adding GuideElements to the guide, this
        is appended to the current list of GuideElements.

        Parameters
        ----------

        guide_element : GuideElement
            New element added to the end of the guide
        """

        # todo: check element name not already in use

        if self.current_owner is not None:
            guide_element.set_owner(self.current_owner)

        self.guide_elements.append(guide_element)
        self.generate_name()

    def __iadd__(self, guide_element):
        """
        Adds a GuideElement to the Guide object with += syntax

        This is the main method for adding GuideElements to the guide, this
        is appended to the current list of GuideElements.

        Parameters
        ----------

        guide_element : GuideElement
            New element added to the end of the guide
        """
        self.add_guide_element(guide_element)

        return self

    def add_guide_element_at_start(self, guide_element):
        """
        Adds a GuideElement to the start of the Guide

        Allows adding a GuideElement to the start of the guide instead of the
        end.

        Parameters
        ----------

        guide_element : GuideElement
            New element added at the start of the guide
        """
        if self.current_owner is not None:
            guide_element.set_owner(self.current_owner)

        # todo: check element name not already in use
        self.guide_elements = [guide_element] + self.guide_elements

    def add_constraint(self, constraint):
        """
        Adds constraint between user defined parameters

        Constraints can be added that uses parameters derived from the
        InstrumentParameter class. These constraints are in addition to those
        defined in the options of the individual guide modules.

        Parameters
        ----------

        constraint : Constraint
            Adds the constraint, will be exported to the optimizer
        """
        self.constraints.append(constraint)

    def export_constraints(self, instrument_parameters):
        """
        Exports the contained constraints to object used by the optimizer

        The modules adds their constraints to instrument_parameters which is
        an instance of InstrumentParameterContainer, and the user defined
        can be exported to this format using this method. In this way the
        optimizer will get both types of constraints in the same system.

        Parameters

        instrument_parameters : InstrumentParameterContainer
            Container to which the Guide constraints are added
        """
        for constraint in self.constraints:
            instrument_parameters.add_constraint(constraint)

    def transfer_end_specifications(self):
        """
        Transfer specified end dimensions to next module as start dimensions

        If end dimensions are specified by the user, they will overwrite the
        start dimensions set at the next module that may or may not have been
        specified by the user.
        """

        for this_guide, next_guide in zip(self.guide_elements[0:-1], self.guide_elements[1:]):
            if this_guide.end_width is not None:
                next_guide.start_width = this_guide.end_width

            if this_guide.end_height is not None:
                next_guide.start_height = this_guide.end_height

    def set_instrument_and_instr_parameters(self, instrument, instrument_parameters):
        """
        Sets McStasScript instrument and instrument parameter container

        All elements are informed of the current instrument object and
        instrument parameter container.

        instrument : McStasScript instr object
            Instrument object to which the guide should be added

        instrument_parameters : InstrumentParameterContainer
            The InstrumentParameterContainer with parameters and constraints
        """

        for element in self.guide_elements:
            element.setup_instrument_and_parameters(instrument, instrument_parameters)

    def connect_to_new_parameters(self, instrument_parameters):
        """
        This methods connects all elements to a new instrument_parameters container

        instrument_parameters : InstrumentParameterContainer
            The InstrumentParameterContainer with parameters and constraints
        """

        for element in self.guide_elements:
            element.connect_to_new_parameters(instrument_parameters)

    def add_to_instrument(self, target_dimensions):
        """
        Adds McStasScript objects describing this guide to a instrument

        Takes a McStasScript instrument objects and adds the guide modules
        contained in this Guide object to the instrument. This is done from
        the target to the source, and the start dimensions from each module
        is carried to the next to ensure the guide is closed. The target and
        moderator is added as well. The wavelength range is contained in the
        target description, but needed by the moderator, this transfer is
        also performed in this method.

        Parameters
        ----------

        target_dimensions : list of length 2
            The width and height parameter for target dimensions in a list
        """

        reference = "ABSOLUTE"
        for element, next_element in zip(self.guide_elements[:-1], self.guide_elements[1:]):
            element.reference_component_name = reference
            reference = element.end_component_name
            element.set_end_dimensions(next_element.start_width, next_element.start_height)
            element.add_to_instr()

        last_element = self.guide_elements[-1]
        last_element.reference_component_name = reference
        last_element.set_end_dimensions(target_dimensions[0], target_dimensions[1])
        last_element.add_to_instr()

    def get_source_focus(self, target):
        """
        Method to provide focusing info dict for this guide

        Focusing info dict contains information used by a source to focus on
        this guide. It may skip some modules if they are not suitable for
        focusing, for example a Gap. Some modules have special focusing
        requirements. The first module that does not return None is used.
        """

        for element in self.guide_elements:
            focus_info = element.get_source_focus()
            if focus_info is not None:
                return focus_info

        # If no module in the guide had focus info, focus on the sample
        focus_info["dist"] = target["target_guide_distance"]
        focus_info["width"] = target["width"]
        focus_info["height"] = target["height"]

        return focus_info

    def write_log_file(self, filename):
        # Start file
        with open(filename, "w") as file:
            file.write("Guide log file from python guide_bot\n")

            for element in self.guide_elements:
                element.write_to_log(file)

    def copy_components(self, destination):
        """
        Copies necessary components to destination
        """
        for element in self.guide_elements:
            required_components = element.copy_components(destination)
            for required_component in required_components:
                self.required_components.add(required_component)

    def get_element(self, name):
        """
        Returns guide element with given name
        """

        for element in self.guide_elements:
            if element.get_name() == name:
                return element

        guide_element_names = [x.get_name() for x in self.guide_elements]
        print(name, guide_element_names)
        raise ValueError("Element named '" + name + "' not found in guide!\n"
                         + "Current elements: " + str(guide_element_names))

    def get_element_names(self):
        return [x.name for x in self.guide_elements]

    def get_element_after(self, name):
        """
        Returns element after given element name
        """
        element = self.get_element(name)
        guide_element_names = [x.get_name() for x in self.guide_elements]

        after_element_index = 1 + guide_element_names.index(element.get_name())
        if after_element_index >= len(guide_element_names):
            return None
        else:
            return self.guide_elements[after_element_index]

    def get_los_breakers(self):
        los_breakers = []
        for element in self.guide_elements:
            if isinstance(element, LosBreakerGuideElement):
                if element.dynamic_los_breaker:
                    los_breakers.append(element)

        return los_breakers

    def get_los_sections(self):
        return self.line_of_sight_sections

    def add_los_section(self, start, end):
        """
        Add line of sight section to guide
        """
        section = LineOfSightSection(start, end)

        start_element = None
        if section.get_start_name() is not None:
            start_element = self.get_element(section.get_start_name())

        end_element = None
        if section.get_end_name() is not None:
            end_element = self.get_element(section.get_end_name())

        # Need to ensure there is a los breaker in the instrument
        los_breakers = self.get_los_breakers()

        if len(los_breakers) == 0:
            raise RuntimeError("There are no line of sight breakers in the guide, can not add los section.")

        # Need to ensure a los_breaker and los_section overlap

        # for distance start
        # Last los_breaker must end after start of los section
        if start_element is None:
            # start is a float
            last_los_breaker = los_breakers[-1]
            print(last_los_breaker.get_name())
            after_last_los_breaker = self.get_element_after(last_los_breaker.get_name())

            last_los_end_parameter = after_last_los_breaker.start_point
            if isinstance(last_los_end_parameter, ipars.RelativeFreeInstrumentParameter):
                last_los_end_min = last_los_end_parameter.get_lower_static_bound()
                last_los_end_max = last_los_end_parameter.get_upper_static_bound()

                if last_los_end_min is None and last_los_end_max is None:
                    last_los_end_parameter.static_lower = start
                elif last_los_end_min is None:
                    if last_los_end_max < start:
                        raise ValueError("Impossible LOS section detected.")
                elif last_los_end_max is None:
                    if last_los_end_min < start:
                        print("Fixed limit")
                        last_los_end_parameter.static_lower = start
                else:
                    # Both limits set
                    if last_los_end_min < start < last_los_end_max:
                        print("Fixed limit")
                        last_los_end_parameter.static_lower = start
        else:
            # start corresponds to an element in the guide, start_element, start is ElementPoint
            # There must be a los_breaker after element

            guide_element_names = [x.get_name() for x in self.guide_elements]
            index_of_start_element = guide_element_names.index(start.get_name())

            elements_after_start = self.guide_elements[index_of_start_element:]
            los_breaker_found = False
            for los_breaker in los_breakers:
                if los_breaker in elements_after_start:
                    los_breaker_found = True

            if not los_breaker_found:
                raise RuntimeError("No los breaker found after element '" + start_element.get_name() + "'.")

            # Ensure the element is long enough for from_end / from_start
            minimum_length = start.get_min_length()
            if minimum_length is not None:
                if isinstance(start_element.length, ipars.FixedInstrumentParameter):
                    if start_element.length.get_value() < minimum_length:
                        raise RuntimeError("ElementPoint defined " + str(minimum_length) + " m "
                                           + "inside of guide section which is only "
                                           + str(start_element.length.get_value()) + "m long!\n"
                                           + "Element name: '" + str(start.get_name()) + "'.")
                elif isinstance(start_element.length, ipars.RelativeFreeInstrumentParameter):
                    current_minimum_length = start_element.length.get_lower_static_bound()
                    if current_minimum_length is None or current_minimum_length < minimum_length:
                        start_element.length.static_lower = minimum_length

        # for distance end
        # First los_breaker must start before end of los section
        if end_element is None:
            # end is a float, distance from source
            first_los_breaker = los_breakers[0]
            first_los_start_parameter = first_los_breaker.start_point

            if isinstance(first_los_start_parameter, ipars.RelativeFreeInstrumentParameter):
                first_los_start_min = first_los_start_parameter.get_lower_static_bound()
                first_los_start_max = first_los_start_parameter.get_upper_static_bound()

                if first_los_start_min is None and first_los_start_max is None:
                    # No limits set, ensure start happens no later than end of los section
                    first_los_start_parameter.static_upper = end
                elif first_los_start_max is None:
                    # A minimum has been set, ensure it is before the end of the los section.
                    if first_los_start_min > end:
                        raise ValueError("Impossible LOS section detected.")
                elif first_los_start_min is None:
                    # A maximum has been set, if smaller than end OK, if larger, limit further
                    if first_los_start_max > end:
                        print("Fixed limit")
                        first_los_start_parameter.static_upper = end
                else:
                    # Both minimum and maximum was set.
                    # If end is within the interval, limit it from tio.
                    if first_los_start_min < end < first_los_start_max:
                        first_los_start_parameter.static_upper = end
                    if end < first_los_start_min:
                        raise ValueError("Impossible LOS section detected.")
        else:
            # end corresponds to an element in the guide, end_element
            # There must be a los_breaker before element
            guide_element_names = [x.get_name() for x in self.guide_elements]
            index_of_end_element = guide_element_names.index(end.get_name())

            elements_before_end = self.guide_elements[:index_of_end_element + 1]
            los_breaker_found = False
            for los_breaker in los_breakers:
                if los_breaker in elements_before_end:
                    los_breaker_found = True

            if not los_breaker_found:
                raise RuntimeError("No los breaker found before element '" + end_element.get_name() + "'.")

            # Ensure the element is long enough for from_end / from_start
            minimum_length = end.get_min_length()
            if minimum_length is not None:
                if isinstance(end_element.length, ipars.FixedInstrumentParameter):
                    if end_element.length.get_value() < minimum_length:
                        raise RuntimeError("ElementPoint defined " + str(minimum_length) + " m "
                                           + "inside of guide section which is only "
                                           + str(end_element.length.get_value()) +  "m long!\n"
                                           + "Element name: '" + str(end.get_name()) + "'.")
                elif isinstance(end_element.length, ipars.RelativeFreeInstrumentParameter):
                    current_minimum_length = end_element.length.get_lower_static_bound()
                    if current_minimum_length is None or current_minimum_length < minimum_length:
                        end_element.length.static_lower = minimum_length

        self.line_of_sight_sections.append(section)

    def plot_guide(self):
        fig, axs = plt.subplots(figsize=(10, 10), nrows=2, ncols=1)
        self.plot_guide_ax(from_top_ax=axs[0], from_side_ax=axs[1])

    def plot_guide_ax(self, from_top_ax, from_side_ax):
        geometries = []
        for element in self.guide_elements:
            geometries.append(element.get_geometry())

        start_pr = None
        for geometry in geometries:
            geometry.load_new_state()
            geometry.plot_on_ax(from_top_ax, start_pr=start_pr, horizontal=True)
            new_pr = geometry.plot_on_ax(from_side_ax, start_pr=start_pr, horizontal=False)
            start_pr = new_pr  # Continue guide from where last element stopped

        #plt.show()


    def print_start_points(self):
        """
        Provide info on start points
        """
        string = "Guide object: "
        if self.name is not None:
            string += self.name
        string += "\n"
        for element in self.guide_elements:
            string += element.get_name() + "\n"
            string += " init sp: " + element.start_point.__repr__() + "\n"
            string += " par sp : " + element.start_point_parameter.__repr__() + "\n"
            string += " next sp: " + element.next_start_point_parameter.__repr__() + 2 * "\n"

        print(string)

    def print_los_sections(self):
        """
        Provide info on line of sight sections
        """
        if len(self.line_of_sight_sections) == 0:
            print("No line of sight sections defined in this guide.")

        for los_section in self.line_of_sight_sections:
            print(los_section)

    def __repr__(self):
        """
        Provides a string describing the Guide object
        """
        string = "Guide object: "
        if self.name is not None:
            string += self.name
        string += "\n"
        for element in self.guide_elements:
            string += element.__repr__() + "\n"
        string += "\n"
        for constraint in self.constraints:
            string += constraint.__repr__() + "\n"
        string += "\n"
        for los_section in self.line_of_sight_sections:
            string += los_section.__repr__() + "\n"

        return string
