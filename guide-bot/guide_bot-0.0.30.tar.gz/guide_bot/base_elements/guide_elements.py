import os
import shutil

import numpy as np

from guide_bot.parameters import instrument_parameters as ipars
from guide_bot.base_elements.base_element_geometry import GuidePoint


def handle_input_parameter(name, par, default_min=None, default_max=None):
    """
    Handles input parameters given to elements and returns InstrumentParameter

    Any parameter to be optimized by elements can be given as keyword
    arguments when they are initialized, and these conform to the following
    logic:

    If the parameter keyword is not used, it will be optimized within default
    limits.

    If a list of length two is given, it will be optimized and the values will
    be used as limits (each limit can be None).

    If a value is specified (float/int), the parameter is fixed to that value.

    Alternatively, the user can provide the InstrumentParameter object
    directly, which will then be returned. In case a DependentInstrumentObject
    is given, it will be checked if it can be calculated, and in that case
    it will be converted to a fixed parameter. If they depend on a free
    parameter, they can not be calculated before each optimization step.

    Parameters
    ----------
    name : (str)
        Name of the parameter (will later be extended)

    par : (float, None, InstrumentParameter)
        Parameter information given to the element

    default_min : float
        Default minimum value for this parameter

    default_max : float
        Default maximum value for this parameter

    Returns
    -------

    par : (FreeInstrumentParamter, FixedInstrumentParameter,
           DependentInstrumentParamter)
        The returned InstrumentParameter object
    """
    # If the user is already providing a parameter, use that directly
    if isinstance(par, (ipars.FixedInstrumentParameter, ipars.FreeInstrumentParameter)):
        return par

    if isinstance(par, ipars.DependentInstrumentParameter):
        # Check if any dependents are free
        if par.depends_on_free():
            return par
        else:
            # if no free dependents, convert to a FixedInstrumentParameter
            par.calculate()
            value = par.get_value()
            return ipars.FixedInstrumentParameter(par.name, value)

    if par is not None:
        if isinstance(par, list):
            # List can only be when a range is set for a free parameter
            if len(par) != 2:
                raise ValueError("When setting min, max with list, it must have length 2.")

            min_value = par[0]
            max_value = par[1]

            return ipars.RelativeFreeInstrumentParameter(name, min_value, max_value)

        else:
            # Assume a fixed value is given
            if not isinstance(par, (int, float)):
                raise ValueError("When setting a parameter value, it should be a float or integer.")

            return ipars.FixedInstrumentParameter(name, par)
    
    else:
        # If nothing is specified, use default range (can both be None, None for length / start_point)
        return ipars.RelativeFreeInstrumentParameter(name, default_min, default_max)


class Element:
    """
    Base class for a element that could be part of a guide.

    Each element will have a length and a start point which is a distance
    from the source. These can be optimized or specified.

    Currently, length and start_point can not be DependentInstrumentParameters
    """
    def __init__(self, name, length=None, start_point=None, **kwargs):
        """
        Initialize a guide element with name and optional length / start_point

        Creates attributes for start_point parameter and
        next_start_point_parameter which is used by the length system to set
        the necessary free parameters for satisfying the total length
        constraint.

        May have an owner specified to differentiate between elements added by
        the user, moderator and sample.

        Parameters
        ----------

        name : (str)
            Name of the guide element

        length : (float, None, InstrumentParameter)
            Length of guide element, optimized parameter

        start_point : (float, None, InstrumentParameter)
            Distance from source to start of the guide element
        """

        self.name = name

        if isinstance(length, ipars.InstrumentParameter):
            raise ValueError("length parameter not allowed to be custom parameter.")

        if isinstance(start_point, ipars.InstrumentParameter):
            raise ValueError("start_point parameter not allowed to be custom parameter.")

        self.length = handle_input_parameter(name + "_length", length, default_min=0.1)
        self.start_point = handle_input_parameter(name + "_start_point", start_point)
        
        self.start_point_parameter = None
        self.next_start_point_parameter = None

        self.element_length = None
        self.length_parameter_name = None

        self.reference_component_name = None
        self.end_component_name = name + "_end_point"

        self.owner = None

    def get_name(self):
        return self.name

    def get_length_name(self):
        """
        Provides length name, ensures this variable is available in instrument

        When adding components describing the GuideElement to the instrument
        file, the length will most probably be needed. This method adds code
        to the instrument file that declares a length variable and calculates
        it from the change points that is used as instrument inputs. It then
        returns the name of the variable, which can be used when setting up
        the McStas components. It avoids adding the same parameter more than
        once by checking if it has already been added.
        """

        previous_cb_name = self.start_point_parameter.name
        next_cb_name = self.next_start_point_parameter.name
        length_var_name = self.name + "_length"

        current_variables = [x.name for x in self.current_instrument.declare_list if hasattr(x, "name")]
        if length_var_name not in current_variables:
            self.current_instrument.add_declare_var("double", length_var_name)
            self.current_instrument.append_initialize(
                length_var_name + " = " + next_cb_name + " - " + previous_cb_name + ";")

        self.length_parameter_name = length_var_name

        return length_var_name

    def calculate_length(self):
        self.element_length = self.next_start_point_parameter.get_value() - self.start_point_parameter.get_value()

    def set_owner(self, owner):
        """
        Sets the owner of this Element

        Parameters
        ----------

        owner : str
            Specifies the owner of this Element
        """

        self.owner = owner

    def __repr__(self):
        """
        Provides a basic description of the guide element

        """
        string = "Element: "

        string += self.name + " : \n"
        string += self.length.__repr__() + "\n"
        string += self.start_point.__repr__()

        return string


class GuideElement(Element):
    """
    Element of a guide, including width / height at start. It is assumed it
    will connect to the next element, and thus width / height of end is
    determined by the next guide element. For this reason, a gap in the guide
    is still considered a GuideElement, for example for a chopper.

    """
    def __init__(self, name, length=None, start_point=None, start_width=None, start_height=None,
                 end_width=None, end_height=None, **kwargs):
        """
        Initializing a GuideElement that can be part of a guide

        A GuideElement has length, a start_point, which is the distance from
        source to the start of the guide, and a start width/height. The
        entrance dimensions are typically optimized, and need a default range.

        Initialized GuideElements are provided by the user and is thus an
        important part of the user interface.

        The exit dimensions are determined by the next element, and a parameter
        for this purpose is assigned to these atributes.

        The current_instrument and current_parameters are internalized, allowing
        classes that inherit from GuideElement to easily add new parameters and
        expand the McStas instrument.

        Parameters
        ----------
        name : (str)
            Name of the guide element

        length : (float, int, None, InstrumentParameter)
            Length of guide element, optimized parameter

        start_point : (float, int, None, InstrumentParameter)
            Distance from source to start of the guide element

        start_width : (float, int, None, InstrumentParameter)
            Width of guide entrance

        start_height : (float, int, None, InstrumentParameter)
            Height of guide entrance

        """
        # Maybe it should be up to the GuideElement if they want the user to set start_width/height?
        # Want to be able to make straight modules that just set start_width to end_width
        # These could derive directly from Element instead, but would then have to add a few things
        # A few solutions
        #  A) Have another class between Element and GuideElement that adds all but start_width/height
        #  B) Provide a easy function to set start_width / height (already kind of the case) and have childen do that
        #  C) Move a few things to Element, what element can exists without current_instr / pars?
        #  D) Remove the start_width / height from the parameter pool by overwriting setup_instr_and_pars
        #
        # Still need to ensure all elements have a start_width / height.

        self.start_width = handle_input_parameter(name + "_start_width", start_width,
                                                  default_min=0.005, default_max=0.15)

        self.start_height = handle_input_parameter(name + "_start_height", start_height,
                                                   default_min=0.005, default_max=0.15)

        if end_width is None:
            self.end_width = None
        else:
            self.end_width = handle_input_parameter(name + "_end_width", end_width,
                                                    default_min=0.005, default_max=0.15)

        if end_height is None:
            self.end_height = None
        else:
            self.end_height = handle_input_parameter(name + "_end_height", end_height,
                                                     default_min=0.005, default_max=0.15)

        self.current_instrument = None
        self.current_parameters = None

        super().__init__(name, length=length, start_point=start_point, **kwargs)

    def get_source_focus(self):
        """
        Returns dict describing how to focus on this guide opening

        Should be overwritten in cases where it is not suitable to focus on
        the module which inherits from this baseclass. For example a module
        that want to focus on some point in the middle of the module, or a
        gap which doesn't need focusing at all, in which case this method
        can return None to tell the source to focus on the next part of the
        guide that may have focus data.
        """

        return dict(width=self.start_width.name,
                    height=self.start_height.name,
                    dist=self.start_point_parameter.name)
    
    def setup_instrument_and_parameters(self, instrument, instrument_parameters):
        """
        Set current_instrument and current_parameters attributes using the
        defined instrument and instrument parameters for a certain run among
        many. Adds start_width / height to the current_parameter object,
        which is a container for all parameters of the instrument.
        """
        self.current_instrument = instrument
        self.current_parameters = instrument_parameters
    
        self.current_parameters.add_parameter(self.start_width)
        self.current_parameters.add_parameter(self.start_height)

    def connect_to_new_parameters(self, instrument_parameters):
        """
        Generic method to connect all parameter attributes to new parameter container

        When switching parameter container for the element, the connections from the
        parameter attributes to the container parameters are lost, and they need to be
        reconnected. This method finds all instances of InstrumentParameter attributes
        on the element object and connects them with versions that have an identical
        name in the new instrument_parameters container.
        """

        # Find all instrument parameter objects in current parameters
        attributes_to_instr_par_names = {}
        attributes = vars(self)
        for attr_name, attr in attributes.items():
            if isinstance(attr, ipars.InstrumentParameter):
                attributes_to_instr_par_names[attr_name] = attr.name

        # Switch to new instrument parameters container
        self.current_parameters = instrument_parameters

        # Link the parameters to the ones with same name in new instrument_parameters
        parameter_names = [x.name for x in self.current_parameters.all_parameters]
        for attr_name in attributes_to_instr_par_names:
            instr_par_name = attributes_to_instr_par_names[attr_name]
            if instr_par_name in parameter_names:
                par_index = parameter_names.index(instr_par_name)
                print("reconnecting: ", attr_name, " to ", instr_par_name)
                setattr(self, attr_name, self.current_parameters.all_parameters[par_index])

    def create_new_parameter(self, *args, **kwargs):
        """
        Uncertain about the need for this method

        Add new parameter on the form:
            Fixed parameter: name, value
            Free parameter: name, value, min, max
            Dependent parameter: name, dependent_on, function, constants
        """
    
        if self.current_instrument is None:
            raise ValueError("No instrument object set yet!")

        if self.current_parameters is None:
            raise ValueError("No parameter object set yet!")

        variable_name = args[0]
        
        #self.current_instrument.add_parameter(variable_name)

        if "dependent_on" in kwargs and "func" in kwargs:
            if "constants" in kwargs:
                constants = kwargs["constants"]
            else:
                constants = []
            par = ipars.DependentInstrumentParameter(variable_name, dependent_on=kwargs["dependent_on"],
                                                     func=kwargs["func"], constants=constants)
        elif len(args) == 2:
            par = ipars.FixedInstrumentParameter(variable_name, args[1])
        elif len(args) == 3:
            par = ipars.FreeInstrumentParameter(variable_name, args[1], args[2])

        self.current_parameters.add_parameter(par)
        
        return par

    def set_end_dimensions(self, end_width, end_height):
        """
        Sets the end_width / height attributes, these have a type derived
        from InstrumentParameter.
        """

        self.end_width = end_width
        self.end_height = end_height

    def copy_component(self, name, destination):
        this_file_path = os.path.abspath(__file__)
        this_directory = os.path.split(this_file_path)[0]
        component_path = os.path.join(this_directory, "..", "McStas_components", name)
        destination_path = os.path.join(destination, name)

        shutil.copyfile(component_path, destination_path)

    def copy_components(self, destination):
        return []

    def get_geometry(self):
        """
        Method to be overwritten by each element, returns geometry object
        """
        raise RuntimeError("Base method that must be overwritten.")

    def write_to_log(self, file):
        """
        Uses geometry object to write log file
        """

        geometry = self.get_geometry()
        geometry.write_to_log(file, self.__class__.__name__, self.name)

    def get_los_points(self, start_pr, distance_unit_less=None, los_start=None, los_end=None):
        """
        Provides GuidePoints in this guide section

        Sets a point for distance_unit_less, los_start and los_end. The element
        may add extra points using the extra_los_goals method.

        Parameters
        ----------
        start_pr : PositionAndRotation
            Position/Rotation at the start of the element

        Keyword Parameters
        ------------------

        distance_unit_less : float between 0 and 1
            How far along this guide element the position should be

        los_start : ElementPoint
            An element_point object describing where in the element the los_start is

        los_end : ElementPoint
            An element_point object describing where in the element the los_end is
        """

        guide_points = []

        if distance_unit_less is not None:
            guide_points.append(GuidePoint(self, start_pr, distance_unit_less=distance_unit_less))

        if los_start is not None:
            guide_points.append(GuidePoint(self, start_pr, element_point=los_start))

        if los_end is not None:
            guide_points.append(GuidePoint(self, start_pr, element_point=los_end))

        guide_points += self.extra_los_points(start_pr=start_pr, distance_unit_less=distance_unit_less,
                                              los_start=los_start, los_end=los_end)

        return guide_points

    def extra_los_points(self, start_pr, distance_unit_less=None, los_start=None, los_end=None):
        """
        Method to add extra line of sight goals, to be overwritten
        """
        return []

    def extra_repr(self):
        """
        Called by __repr__ and can be overwritten to write extra information
        """
        return None

    def __repr__(self):
        """
        Provides a basic description of the guide element
        """

        name_length = 12
        string = "GuideElement: "

        string += self.name + " : \n"
        string += "length:".ljust(name_length) + self.length.__repr__() + "\n"
        string += "start:".ljust(name_length) + self.start_point.__repr__() + "\n"
        string += "s width:".ljust(name_length) + self.start_width.__repr__() + "\n"
        string += "s height:".ljust(name_length) + self.start_height.__repr__() + "\n"
        if self.end_width is not None:
            string += "e width:".ljust(name_length) + self.end_width.__repr__() + "\n"
        else:
            string += "no end_width set\n"
        if self.end_height is not None:
            string += "e height:".ljust(name_length) + self.end_height.__repr__() + "\n"
        else:
            string += "no end_height set\n"

        string += "start par:".ljust(name_length) + self.start_point_parameter.__repr__() + "\n"
        string += "n start p:".ljust(name_length) + self.next_start_point_parameter.__repr__()

        extra_string = self.extra_repr()
        if extra_string is not None:
            string += "\n" + extra_string

        return string


class LosBreakerGuideElement(GuideElement):
    def __init__(self, name, length=None, start_point=None, start_width=None, start_height=None,
                 end_width=None, end_height=None, **kwargs):

        super().__init__(name, length=length, start_point=start_point,
                         start_width=start_width, start_height=start_height,
                         end_width=end_width, end_height=end_height,
                         **kwargs)

        self.dynamic_los_breaker = True
        self.last_los_value = None

        """
        How to handle sign ? +/- for left right is common
        
        Could add a sign to LosInstrumentParameter that is applied at get_value
        
        Need to have enable / disable switch.
        Cases:
        kink at moderator can be for performance reasons
        kink can be static
        kink can be meant to block line of sight
        
        If user sets angle, it is static. Disable this as a los_blocker
        If user sets nothing, what to do then? Break los if there is a section, error otherwise?
        If for performance reasons, user could set a optimize this please flag
        """

    def set_los_value(self, value):
        """
        Saves los value and transfers to overwritten los_input method

        Parameters
        ----------
        value : float
            Control value for this line of sight breaker
        """

        self.last_los_value = value
        self.los_input(value)

    def get_los_value(self):
        """
        Get the los value that would recreate the current los state

        The los_input method uses a positive float value to set a more complex
        los state of the los breaker. Get los value retrieves the last los
        value given to an element, meaning the output of this method has to be
        zero or a positive float number. It should roughly correspond to the
        angle deviation the los breaker introduces.

        Returns
        -------
        los_value corresponding to state of element
        """
        return self.last_los_value

    def los_input(self, value):
        """
        Input for breaking line of sight, single value input

        The los input is a single value with the property that when it is
        increased, the los breaker becomes more likely to break line of sight.
        At a value of 0.0, it is assumed it wont break line of sight.
        This could be the angle in a kink, or the angle a curved guide turns,
        but it is also allowed to have several parameters controlled by the
        los_input. It is also possible to for example invert the sign, so that
        a kink could change directions depending on some other parameter.

        Parameters
        ----------

        value : float
            Control value for this line of sight breaker
        """

        raise RuntimeError("los_input must be overwritten by LosBreaker element.")