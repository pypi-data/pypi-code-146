import numpy as np
import yaml

from mcstasscript.interface import functions


class PlotInfo:
    """
    Contains information on options for plotting a McStasScript dataset

    Container for information for McStasScript monitor options including
    methods for applying these monitors to a specific monitor or in a
    larger dataset.
    """
    def __init__(self, mon_name, title=None, xlabel=None, ylabel=None, plot_options=None):
        """
        Sets up a PlotInfo object with initial settings

        The PlotInfo object describes how a McStasScript object should be
        plotted and can be applied to a monitor or dataset. It is required to
        provide a name for the monitor or a McStasScript component instance
        so the monitor can be found in a dataset.

        Parameters
        ----------

        mon_name : str or McStasScript component object
            Name of monitor to be adjusted

        title : str
            Title of the plot

        xlabel : str
            xlabel of the plot

        ylabel : str
            ylabel of the plot

        plot_options : dict
            Dictionary with any McStasScript plot options to be applied
        """
        if isinstance(mon_name, str):
            self.mon_name = mon_name
        else:
            # In case it is a McStasScript component object
            self.mon_name = mon_name.name

        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        if plot_options is None:
            self.plot_options = {}
        else:
            self.plot_options = plot_options

    def set_title(self, title):
        """
        Sets title of the plot

        Parameters
        ----------

        title : str
            String for plot title
        """
        self.title = title

    def set_xlabel(self, xlabel):
        """
        Sets xlabel of the plot

        Parameters
        ----------

        xlabel : str
            String for xlabel
        """
        self.xlabel = xlabel

    def set_ylabel(self, ylabel):
        """
        Sets ylabel of the plot

        Parameters
        ----------

        ylabel : str
            String for ylabel
        """
        self.ylabel = ylabel

    def set_plot_options(self, **kwargs):
        """
        Sets plot_options for the plot

        Parameters
        ----------

        keyword arguments : McStasScript plot_option arguments
            All arguments that can be given to McStasData set_plot_options
        """
        self.plot_options.update(**kwargs)

    def apply_to_single(self, data):
        """
        Applies settings to a data object

        Parameters
        ----------

        data : McStasScript McStasData object
        """
        data.set_title(self.title)
        data.set_xlabel(self.xlabel)
        data.set_ylabel(self.ylabel)
        data.set_plot_options(**self.plot_options)

    def apply_to_data(self, dataset):
        """
        Applies settings to matching object in dataset

        Parameters
        ----------

        dataset : list of McStasScript McStasData objects
            dataset that contains monitor to apply settings to
        """
        mon = functions.name_search(self.mon_name, dataset)
        self.apply_to_single(mon)


class PlotInfoContainer:
    def __init__(self):
        self.infos = []

    def new(self, *args, **kwargs):
        info = PlotInfo(*args, **kwargs)
        self.infos.append(info)
        return info

    def apply_all_data(self, data):
        if data is None:
            return

        for info in self.infos:
            info.apply_to_data(data)


def run_simulation(name, parameters, settings, instrument):
    """
    Performs the McStasScript instrument simulation with given settings

    Parameters
    ----------

    name : str
        Name of the folder to be created with the raw data

    parameters : Dict
        Parameters to be used for the simulation

    settings : Dict
        Settings to be used for the simulation

    instrument : McStasScript instrument object
        Instrument which will be used for the simulation
    """
    write_component_dimensions(name, instrument)

    if "ncount_analysis" in settings:
        ncount = settings["ncount_analysis"]
    else:
        ncount = 10*settings["ncount"]

    if "mpi" not in settings:
        settings["mpi"] = None

    return instrument.run_full_instrument(foldername=name, mpi=settings["mpi"],
                                          increment_folder_name=True,
                                          parameters=parameters,
                                          ncount=ncount)


def run_simulation_brill(name, parameters, settings, instrument):
    """
    Performs the McStasScript instrument simulation with given settings

    Parameters
    ----------

    name : str
        Name of the folder to be created with the raw data

    parameters : Dict
        Parameters to be used for the simulation

    settings : Dict
        Settings to be used for the simulation

    instrument : McStasScript instrument object
        Instrument which will be used for the simulation
    """

    write_component_dimensions(name, instrument)

    if "ncount_analysis" in settings:
        ncount = settings["ncount_analysis"]
    else:
        ncount = 10*settings["ncount"]

    if "mpi" not in settings:
        settings["mpi"] = None

    reduced_parameters = {}
    for parameter in list(instrument.parameters):
        if parameter.name in parameters:
            reduced_parameters[parameter.name] = parameters[parameter.name]

    return instrument.run_full_instrument(foldername=name, mpi=settings["mpi"],
                                          increment_folder_name=True,
                                          parameters=reduced_parameters,
                                          ncount=ncount)


def normalize_brill_ref(data, ref_data, instrument, ref_instrument):
    """
    Performs brilliance transfer normalization for a McStasScript dataset

    When normalizing to brilliance transfer, a intensity data is divided with
    reference data from close to the source. It is required that each data
    set has closed phase-space bounderies in both wavelength, space and
    divergence for this normalization to make sense. The reference data set
    should be evenly illuminated in this space. It is however possible to
    have different phase-space boarders for the data and reference, if this
    is taken into account during the normalization. Here it is assumed the
    divergence and wavelength limits are equal, but the spatial limits can be
    different. The instrument objects for each data set is used to check
    these sizes for use in the normalization.

    Parameters
    ----------

    data : list of McStasData objects
        List of data that will be normalized when twin is found in ref_data

    ref_data : list of McStasData objects
        List of data that will be used for normalization

    instrument : McStasScript instrument object
        Instrument object corresponding to the data

    ref_instrument : McStasScript instrument object
        Instrument object corresponding to the ref_data
    """

    ref_data_names = []
    for data_object in ref_data:
        ref_data_names.append(data_object.name)

    if data is None:
        return None

    normalized_monitors = []
    for data_object in data:
        if data_object.name in ref_data_names:
            ref_data_object = functions.name_search(data_object.name, ref_data)

            monitor = instrument.get_component(data_object.name)
            ref_monitor = ref_instrument.get_component(data_object.name)

            mon_area = get_monitor_area(data_object, monitor)
            ref_mon_area = get_monitor_area(ref_data_object, ref_monitor)

            if mon_area is None or ref_mon_area is None:
                raise RuntimeError("Area could not be read!")

            area_ratio = mon_area/ref_mon_area

            # normalize pixel for pixel (always allowed, but less efficient)
            data_object.Error = np.sqrt((data_object.Error / data_object.Intensity) ** 2 + (ref_data_object.Error / ref_data_object.Intensity) ** 2)
            data_object.Intensity /= ref_data_object.Intensity / area_ratio
            data_object.Error *= data_object.Intensity

            normalized_monitors.append(data_object.name)

            # Could detect situations where it is allowed to sum/average reference
            #  but this depends on whether for example intensity is constant with
            #  wavelength.

    return normalized_monitors


def write_component_dimensions(base_name, instrument):
    component_x_y = {}
    comp_names = [x.name for x in instrument.component_list]
    for comp_name in comp_names:
        comp = instrument.get_component(comp_name)

        if hasattr(comp, "xwidth") and hasattr(comp, "yheight"):
            component_x_y[comp_name] = [comp.xwidth, comp.yheight]

    with open(base_name + ".yaml", 'w') as yaml_file:
        yaml.dump(component_x_y, yaml_file, default_flow_style=False)


def get_monitor_area(data, component):
    """
    Gets the area of a McStas monitor that use standard xwidth / yheight input

    Parameters
    ----------

    data : McStasData object
        data object that contains parameters used for run

    component : McStasScript component object
        component to check
    """

    width = read_field(data, component, "xwidth")
    height = read_field(data, component, "yheight")

    if width is not None and height is not None:
        return width*height # m^2

    return None


def read_field(data, component, field):
    """
    Reads a field of a component using parameters from given dataset

    data : McStasData object
        data object that contains parameters used for run

    component : McStasScript component object
        component to check

    field : str
        name of component field to check
    """

    # If the component doesnt have the field, return
    if not hasattr(component, field):
        return None

    # Read the input given to that field and parameters of run
    component_field = getattr(component, field)
    used_parameters = data.metadata.parameters

    value = None
    try:
        # If a float or int is given directly, just read that
        value = float(component_field)
    except ValueError:
        # If a parameter name is given directly, look that up
        if component_field in used_parameters:
            value = used_parameters[component_field]

    # Last attempt to read using python eval in case a simple expression is used
    # This will catch for example "2.0*target_width"
    if value is None:
        try:
            # Try to evaluate field with scope of all instrument parameters
            value = eval(component_field, used_parameters)
        except:
            value = None

    try:
        value = float(value)
    except ValueError:
        # Do not want to return a string
        value = None
    except TypeError:
        value = None

    return value