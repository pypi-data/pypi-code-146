import numpy as np
import copy


class Parameters:
    """
    Class for input parameters that are not optimized, but may be scanned

    The Parameters class holds parameters used as input which are not to be
    optimized since they are requirements. It may however be worthwhile to
    perform optimization for a range of inputs, for example to investigate
    several different target sizes. Creating a new parameter with a value
    creates a fixed parameter, but providing a list instead would scan that
    parameter. If multiple parameters are scanned, every combination is
    scanned, unless they are locked together, this could be done for example
    when wanting to investigate quadratic targets and not all combinations.

    The class needs to be used with the InputConfiguratonIterator class that
    take a Parameters class for the target, and one for the source.

    Parameters can be accessed using object["par_name"], and returns just the
    current value not the entire list of the scan.

    The class can update all keys with a prefix and add this prefix to calls,
    this is made in preparation for allowing joining of two Parameters
    instances that may have conflicting names.
    """
    def __init__(self):
        """
        Creates Parameters object to hold input parameters that can be scanned

        Holds mix of parameters with fixed values and some that are scanned.
        The parameters can be accessed with object["par_name"], and this will
        return the current value in the scan instead of the list of scanned
        values.
        """
        self.parameters = {}
        self.parameter_lengths = {}
        self.scanned_parameters = []
        self.state = None  # internal state deciding what is the current step

        self.lock_map = {}
        self.prefix = ""

        self.parameter_units = {}
        self.parameter_is_filename = {}

    def add(self, name, value, unit=None, is_filename=False):
        """
        Add new parameter, either with fixed value or scanned with list

        Method for adding a new parameter to the Parameters object, that can
        either be a fixed value or a scan when providing a list of values.

        Parameters
        ----------

        name : str
            Name of parameters for access

        value : float or list of floats
            The input for parameter, either float for fixed or list for scan

        Keyword arguments
        -----------------

        unit : str
            Unit for the parameter, used in plotting

        is_filename : bool
            Set to True if this is a path to a file that is needed for simulation
        """
        name = self.prefix + name

        if name in self.parameters:
            raise RuntimeError("Parameter already exist in Parameters instance.")

        self.parameters[name] = value

        if isinstance(value, (int, float, str)) or value is None:
            n_points = 1
        else:
            try:
                n_points = len(value)
                if n_points == 1:
                    self.parameters[name] = value[0]
            except:
                raise RuntimeError("Parameters have to be int, float "
                                   + "str or array with len specified.")

        self.parameter_lengths[name] = n_points

        if n_points > 1:
            self.scanned_parameters.append(name)
        
        self.parameter_units[name] = str(unit)
        self.parameter_is_filename[name] = bool(is_filename)

    def get_n_scanned_parameters(self):
        """
        Returns the number of parameters that are scanned in this object

        Returns
        -------

        int
            Number of scanned parameters
        """
        return len(self.scanned_parameters)

    def get_scan_shape(self):
        """
        Returns the scan shape of the scanned parameters in this object

        Returns
        -------

        list
            List containing number of scan points for each scanned parameter
        """
        scan_shape = []
        for name in self.scanned_parameters:
            scan_shape.append(self.parameter_lengths[name])

        return scan_shape

    def set_state(self, state):
        """
        Sets the state that decides the scan step in all dimensions

        Parameters
        ----------

        state : list
            Index for each scan dimension, in order of scanned_parameters
        """
        self.state = state

    def get_scan_dict(self):
        """
        Gets a dictionary of the scanned parameters

        Returns
        -------
        dictionary with scanned parameter names and their list of values

        """
        scan_dict = {}
        for par in self.scanned_parameters:
            scan_dict[par] = self.parameters[par]

        return scan_dict

    def get_fixed_dict(self):
        """
        Gets a dictionary of the parameters that are not scanned

        Returns
        -------
        dictionary with parameters that are not scanned and their values

        """
        par_dict = {}
        for par in self.parameters:
            if par not in self.scanned_parameters:
                par_dict[par] = self.parameters[par]

        return par_dict

    def get_unit_dict(self, only_scanned=False):
        """
        Gets a dictionary of the units for the scanned parameters

        When only_scanned is set to true, only units of scanned parameters
        are returned

        Keyword arguments
        -----------------

        only_scanned : bool
            True to return dict with only scanned parameters

        Returns
        -------
        dict : str -> str
            Dictionary with units for each parameter name
        """

        if not only_scanned:
            return self.parameter_units

        unit_dict = {}
        for par in self.scanned_parameters:
            unit_dict[par] = self.parameter_units[par]

        return unit_dict

    def get_filename_pars(self):
        """
        Get list of parameter names that correspond til filenames
        """

        filename_par_names = []
        for name, is_file in self.parameter_is_filename.items():
            if is_file:
                filename_par_names.append(name)

        return filename_par_names

    def get_current_scan_state(self):
        """
        Gets a dictionary of current state of parameters

        Returns
        -------
        dictionary with scanned variables and their scan index
        """

        state_dict = {}

        for par in self.scanned_parameters:
            par_index = self.scanned_parameters.index(par)
            scan_index = self.state[par_index]
            state_dict[par] = scan_index

            """
            state_dict[par] = self[par]
            par_index = self.scanned_parameters.index(scan_name)
            """

        return state_dict

    def __getitem__(self, name):
        """
        Providing [] operator that returns current value of requested parameter

        This method allows the user to retrieve the current value of each
        parameter, even those scanned. It uses the current state to select from
        the list of values for each scanned parameter. Locked parameters get
        the state from the parameter they are locked to.

        Parameters
        ----------

        name : str
            Name of the parameter for which the current value is requested
        """
        name = self.prefix + name
        if name not in self.parameters:
            raise KeyError("Parameter named " + name + " not defined.")

        if name in self.lock_map:
            scan_name = self.lock_map[name]
        else:
            scan_name = name

        if scan_name in self.scanned_parameters:
            par_index = self.scanned_parameters.index(scan_name)
            scan_index = self.state[par_index]
            array = self.parameters[name]
            return array[scan_index]
        else:
            return self.parameters[name]

    def __setitem__(self, name, value):
        """
        Allow setting a parameter taking current state into account

        This method allows a user to update a parameter taking the current
        scan state into account.

        Parameters
        ----------

        name : str
            Name of the parameter for which the current value should be updated

        value
            New value for this parameter and current scan state
        """

        name = self.prefix + name
        if name not in self.parameters:
            raise KeyError("Parameter named " + name + " not available")

        if name in self.lock_map:
            scan_name = self.lock_map[name]
        else:
            scan_name = name

        if scan_name in self.scanned_parameters:
            par_index = self.scanned_parameters.index(scan_name)
            scan_index = self.state[par_index]
            array = self.parameters[name]
            array[scan_index] = value
        else:
            self.parameters[name] = value

    def print_current_state(self):
        """
        Prints the current value of all parameters based on the current state
        """

        for key in self.parameters:
            print(key, "=", self[key])

    def lock_parameters(self, par1, par2):
        """
        Lock the scan of two parameters together

        All scanned parameters are assumed independent so a map of all
        combinations is investigated. By locking two parameters together,
        these are considered a single parameter scanned and thus this requires
        they have the same number of scan steps, i.e. length of lists.

        Any prefix in the instance is added to the parameters, keeping the
        prefix from being a concern of the user.

        Parameters
        ----------

        par1 : str
            Name of first parameter to lock

        par2 : str
            Name of second parameter to lock
        """

        par1 = self.prefix + par1
        par2 = self.prefix + par2

        # check both parameters are scanned
        if par1 not in self.scanned_parameters:
            raise RuntimeError("Can not lock parameter that is not scanned.")

        if par2 not in self.scanned_parameters:
            raise RuntimeError("Can not lock parameter that is not scanned.")

        # check they have same length
        if self.parameter_lengths[par1] != self.parameter_lengths[par2]:
            raise RuntimeError("Locked parameters need to have same length.")

        # remove one from scanned parameters
        par2_index = self.scanned_parameters.index(par2)
        self.scanned_parameters.pop(par2_index)
        del self.parameter_lengths[par2]

        # add pairing to the lock map
        self.lock_map[par2] = par1

    def preface_names(self, prefix):
        """
        Adds a prefix to all parameter names in preparation for merging

        If two Parameters instances should be merged, they may have
        conflicting names and as such it can be necessary to add a unique
        prefix for the parameters in each first.

        Parameters
        ----------

        prefix : str
            Name of prefix that will be added to all parameter names
        """
        self.prefix += prefix
        new_parameters = {}
        new_parameter_units = {}
        for key in self.parameters:
            if key in self.scanned_parameters:
                scan_index = self.scanned_parameters.index(key)
                self.scanned_parameters[scan_index] = prefix + key
                n_points = self.parameter_lengths[key]
                del self.parameter_lengths[key]
                self.parameter_lengths[prefix + key] = n_points

            values = self.parameters[key]
            new_parameters[prefix + key] = values
            new_parameter_units[prefix + key] = self.parameter_units[key]

        self.parameters = new_parameters
        self.parameter_units = new_parameter_units

        new_lock_map = {}
        for key in self.lock_map:
            lock_name = self.lock_map[key]
            new_lock_map[self.prefix + key] = prefix + lock_name

        self.lock_map = new_lock_map


class CombinedParameters:
    """
    Experimental class that may take the role of a InputConfigurationIterator
    """


    def __init__(self):
        self.combined_parameters = Parameters()

        self.parameters_link = []

        self.scan_iterator = None
        self.scan_config = None

    def add_set(self, prefix, ingoing):

        self.parameters_link.append(ingoing)
        #parameters_copy = copy.deepcopy(parameters)
        #parameters_copy.preface_names(prefix)
        #self.parameters_copies.append(parameters_copy)

        for key in ingoing.parameters:
            self.combined_parameters.add(key, ingoing.parameters[key])

        for key in ingoing.lock_map:
            self.combined_parameters.lock_parameters(key, ingoing.lock_map[key])

    def reset_configuration(self):
        self.scan_iterator = np.ndindex(*self.combined_parameters.get_scan_shape())
        for par_set in self.parameters_link:
            par_set.state = np.zeros(par_set.get_n_scanned_parameters)

    def next_state(self):
        try:
            self.scan_config = next(self.scan_iterator)
            self.combined_parameters.set_state(self.scan_config)

            # Need to split state and provide it to each parameter_link
            for par_name in self.combined_parameters.scanned_parameters:
                # check to find par_name in each link? (only one will exist)
                for par_set in self.parameters_link:
                    if par_name in par_set.scanned_parameters:
                        global_state_index = self.combined_parameters.scanned_parameters.index(par_name)
                        local_state_index = par_set.scanned_parameters.index(par_name)

                        par_set.state[local_state_index] = self.combined_parameters.state[global_state_index]

            return True

        except StopIteration:
            return False


def join_parameter_sets(target, moderator):
    # preface target with target name
    for key in target.parameters:
        scan_index = target.scanned_parameters.index(key)
        target.scanned_parameters[scan_index] = "target_" + key
        n_points = target.parameter_lengths[key]
        del target.parameter_lengths[key]
        target.parameter_lengths["target_" + key] = n_points
        values = target.parameters[key]
        del target.parameters[key]
        target.parameters["target_" + key] = values



