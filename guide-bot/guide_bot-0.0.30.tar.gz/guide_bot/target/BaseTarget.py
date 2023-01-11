import math

import numpy as np
import yaml

from guide_bot.requirements.requirement_parameters import Parameters
from guide_bot.parameters import instrument_parameters as ipars
from guide_bot.elements import Element_gap

from mcstasscript.interface import instr, plotter, functions

from .Helper import PlotInfoContainer, run_simulation


class BaseTarget:
    """
    Target class that sets figure of merit for the optimized guide

    The Target class describes the figure of merit for the guide, including
    the target size, divergence, wavelength range and distance from source to
    delivery point. Distance between guide and delivery point is also set.
    The parameters describing these aspects can all be scanned to perform
    optimization for each combination the user wish to investigate.

    The figure of merit needs to be measured in the McStas simulation, so part
    of the responsibilities of the class is to add a monitor component to the
    McStas instrument file.

    The Target class is also responsible for adding elements between the guide
    given by the user and the delivery point, which is must often just a gap.
    This could however be something different, and may need optimization, so
    this responsibility has been placed in the Target class.

    It is straight forward to inherit from this BaseTarget object and adjust the
    figure of merit accordingly. Targets that inherit from this should call
    super().__init__(*args, **kwargs) early in order to set up Parameters.

    The Parameters in the Target can be accessed with Target["par_name"],
    and will return the current value in case of a scan, not the entire list
    for the scan.
    """
    def __init__(self, width, height,
                 min_wavelength, max_wavelength,
                 instrument_length, target_guide_distance):
        """
        Description of figure of merit for guide optimization

        All given parameters can be scanned by providing an list of floats
        instead of just a single float. All Parameters can be read using
        Target["par_name"], and will return the current value instead of the
        entire list for the scan.

        Parameters
        ----------

        width : float or list of floats for scan
            Width of target at target position in [m]

        height : float or list of floats for scan
            Height of target at target position in [m]

        min_wavelength : float or list of floats for scan
            Minimum wavelength in figure of merit [Å]

        max_wavelength : float or list of floats for scan
            Maximum wavelength in figure of merit [Å]

        instrument_length : float or list of floats for scan
            Distance from source to target in [m]

        target_guide_distance : float or list of floats for scan
            Distance from guide end to target in [m]

        calculate_guide_end_dimensions: bool or list of bools for scan (default True)
            If true, the guides end dimensions are calculated from target requirements
        """
        self.parameters = Parameters()

        # Required
        self.parameters.add("width", width, unit="m")
        self.parameters.add("height", height, unit="m")
        self.parameters.add("min_wavelength", min_wavelength, unit="AA")
        self.parameters.add("max_wavelength", max_wavelength, unit="AA")
        self.parameters.add("instrument_length", instrument_length, unit="m")
        self.parameters.add("target_guide_distance", target_guide_distance, unit="m")

        # list of PlotInfo objects that will be applied to control plotting with McStasScript
        self.plot_info = PlotInfoContainer()

        # Target dimensions set during setup for each guide and retrieved from parameters object
        self.target_width = None
        self.target_height = None
        self.target_gap = None

    def __getitem__(self, item):
        """
        Ensures Target["par_name"] returns value in parameters

        Parameter
        ---------

        item : str
            Name of the parameter to be retrieved
        """
        return self.parameters[item]

    def lock_parameters(self, par1, par2):
        """
        Lock the scan of two parameters together

        All scanned parameters are assumed independent so a map of all
        combinations is investigated. By locking two parameters together,
        these are considered a single parameter scanned and thus this requires
        they have the same number of scan steps, i.e. length of lists.

        Parameters
        ----------

        par1 : str
            Name of first parameter to lock

        par2 : str
            Name of second parameter to lock
        """
        self.parameters.lock_parameters(par1, par2)

    def add_target_info(self, instrument_parameters):
        """
        Adds wavelength parameters to instrument_parameters

        Parameters
        ----------

        instrument_parameters : InstrumentParameterContainer
            Parameter container where parameters can be added for optimization
        """

        min_wavelength = ipars.FixedInstrumentParameter("min_wavelength", self["min_wavelength"])
        max_wavelength = ipars.FixedInstrumentParameter("max_wavelength", self["max_wavelength"])

        instrument_parameters.add_parameter(min_wavelength)
        instrument_parameters.add_parameter(max_wavelength)

        self.target_width = ipars.FixedInstrumentParameter("target_width", self["width"])
        self.target_height = ipars.FixedInstrumentParameter("target_height", self["width"])

        instrument_parameters.add_parameter(self.target_width)
        instrument_parameters.add_parameter(self.target_height)

    def get_size_parameters(self):
        """
        Returns target size as parameters, only call after add_target_info

        This relies on the target being set up already, otherwise it would
        return information from the previous scan point.
        """

        return [self.target_width, self.target_height]

    def add_to_instrument(self, instrument, instrument_parameters):
        """
        Adds a figure of merit monitor to the McStas instrument file

        Adds a monitor that will measure the figure of merit. The method
        returns the wavelength range.

        Parameters
        ----------

        instrument : McStasScript instrument object
            Instrument object to which the monitor is added

        instrument_parameters : InstrumentParameterContainer
            Parameter container where parameters can be added for optimization
        """

        mon = instrument.add_component("mon", "PSD_monitor")

        mon.nx = 20
        mon.ny = 20
        mon.filename = '"fom.dat"'
        mon.xwidth = "target_width"
        mon.yheight = "target_height"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 0], RELATIVE=self.target_gap.end_component_name)

        return [self["min_wavelength"], self["max_wavelength"]]

    def add_end(self, guide, instrument_parameters):
        """
        Adds GuideElements between user provided guide and the target

        Most often a Gap is added between the provided guide and the target,
        but this method provides the flexibility to do something different.
        If guide has the overwrite_target_guide_distance attribute set to
        something different than None, this methods uses that value instead
        of the one contained in the Target object.

        Parameters
        ----------

        guide : Guide object
            Guide object after apply_guide_start method has been performed

        instrument_parameters : InstrumentParameterContainer
            Parameter container where parameters can be added for optimization
        """

        if guide.overwrite_target_guide_distance is None:
            target_guide_distance = self["target_guide_distance"]
        else:
            target_guide_distance = guide.overwrite_target_guide_distance

        # Use minimalist principle to calculate guide end dimensions
        max_width = self["width"] + 2 * math.tan(3.0 * math.pi / 180.0) * target_guide_distance
        max_height = self["height"] + 2 * math.tan(3.0 * math.pi / 180.0) * target_guide_distance

        width_input = [self["width"], max_width]
        height_input = [self["height"], max_height]

        self.target_gap = Element_gap.Gap(name="guide_target_gap",
                                          length=target_guide_distance,
                                          start_width=width_input, start_height=height_input)

        guide.add_guide_element(self.target_gap)

    def add_analysis_to_instrument(self, instrument, instrument_parameters):
        """
        Adds monitors for target analysis to instrument file

        After successful optimization the target from the guide is analyzed with
        more monitors than during the optimization. These can save more data,
        and the simulations can be performed with a much greater ncount for
        better quality.

        Parameters
        ----------

        instrument : McStasScript instrument object
            Instrument object to which the monitor is added
        """

        divergence_h = 2.5
        divergence_v = 2.5

        mon = instrument.add_component("psd_lin_horizontal", "PSDlin_monitor")
        mon.nx = 300
        mon.filename = '"psd_lin_horizontal.dat"'
        mon.xwidth = "2.0*target_width"
        mon.yheight = "target_height"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 0], RELATIVE=self.target_gap.end_component_name)

        info = self.plot_info.new(mon, title="Horizontal position")
        info.set_xlabel("Horizontal position [cm]")
        info.set_plot_options(x_axis_multiplier=100)

        mon = instrument.add_component("psd_lin_vertical", "PSDlin_monitor")
        mon.nx = 300
        mon.filename = '"psd_lin_vertical.dat"'
        mon.xwidth = "2.0*target_height"
        mon.yheight = "target_width"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 90], RELATIVE="psd_lin_horizontal")

        info = self.plot_info.new("psd_lin_vertical", title="Vertical position")
        info.set_xlabel("Vertical position [cm]")
        info.set_plot_options(x_axis_multiplier=100)

        mon = instrument.add_component("divergence_horizontal", "Hdiv_monitor")
        mon.nh = 200
        mon.filename = '"divergence_horizontal.dat"'
        mon.h_maxdiv = divergence_h
        mon.xwidth = "target_width"
        mon.yheight = "target_height"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 0], RELATIVE="psd_lin_horizontal")

        info = self.plot_info.new(mon, title="Horizontal divergence")
        info.set_xlabel("Horizontal divergence [deg]")

        mon = instrument.add_component("divergence_vertical", "Hdiv_monitor")
        mon.nh = 200
        mon.filename = '"divergence_vertical.dat"'
        mon.h_maxdiv = divergence_v
        mon.xwidth = "target_height"
        mon.yheight = "target_width"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 90], RELATIVE="psd_lin_horizontal")

        info = self.plot_info.new(mon, title="Vertical divergence")
        info.set_xlabel("Vertical divergence [deg]")

        mon = instrument.add_component("psd_analysis_large", "PSD_monitor")
        mon.nx = 300
        mon.ny = 300
        mon.filename = '"psd_large.dat"'
        mon.xwidth = "2.0*target_width"
        mon.yheight = "2.0*target_height"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 0], RELATIVE="psd_lin_horizontal")

        info = self.plot_info.new(mon, title="Large PSD")
        info.set_xlabel("Horizontal position [cm]")
        info.set_ylabel("Vertical position [cm]")

        mon = instrument.add_component("divergence_2D", "Divergence_monitor")
        mon.nh = 200
        mon.nv = 200
        mon.filename = '"divergence_2D.dat"'
        mon.maxdiv_h = divergence_h
        mon.maxdiv_v = divergence_v
        mon.xwidth = "target_width"
        mon.yheight = "target_height"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 0], RELATIVE="psd_lin_horizontal")

        info = self.plot_info.new(mon, title="Divergence 2D")
        info.set_xlabel("Horizontal divergence [deg]")
        info.set_ylabel("Vertical divergence [deg]")

        mon = instrument.add_component("Lambda", "L_monitor")
        mon.Lmin = "min_wavelength"
        mon.Lmax = "max_wavelength"
        mon.nL = 200
        mon.filename = '"wavelength.dat"'
        mon.xwidth = "target_width"
        mon.yheight = "target_height"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 0], RELATIVE="psd_lin_horizontal")

        info = self.plot_info.new(mon, title="Wavelength")
        info.set_xlabel("Wavelength [AA]")

        mon = instrument.add_component("Acceptance_horizontal", "DivPos_monitor")
        mon.nh = 200
        mon.ndiv = 200
        mon.filename = '"Acceptance_horizontal.dat"'
        mon.maxdiv_h = divergence_h
        mon.xwidth = "2.0*target_width"
        mon.yheight = "target_height"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 0], RELATIVE="psd_lin_horizontal")

        info = self.plot_info.new(mon, title="Acceptance horizontal")
        info.set_xlabel("Horizontal position [cm]")
        info.set_ylabel("Horizontal divergence [deg]")
        info.set_plot_options(x_axis_multiplier=100)

        mon = instrument.add_component("Acceptance_vertical", "DivPos_monitor")
        mon.nh = 200
        mon.ndiv = 200
        mon.filename = '"Acceptance_vertical.dat"'
        mon.maxdiv_h = divergence_v
        mon.xwidth = "2.0*target_height"
        mon.yheight = "target_width"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 90], RELATIVE="psd_lin_horizontal")

        info = self.plot_info.new(mon, title="Acceptance vertical")
        info.set_xlabel("Vertical position [cm]")
        info.set_ylabel("Vertical divergence [deg]")
        info.set_plot_options(x_axis_multiplier=100)

        mon = instrument.add_component("psd_analysis", "PSD_monitor")
        mon.nx = 300
        mon.ny = 300
        mon.filename = '"psd.dat"'
        mon.xwidth = "target_width"
        mon.yheight = "target_height"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 0], RELATIVE="psd_lin_horizontal")

        info = self.plot_info.new(mon, title="PSD target size")
        info.set_xlabel("Horizontal position [cm]")
        info.set_ylabel("Vertical position [cm]")

        mon = instrument.add_component("divergence_2D_fom", "Divergence_monitor")
        mon.nh = 200
        mon.nv = 200
        mon.filename = '"divergence_2D_fom.dat"'
        mon.maxdiv_h = divergence_h
        mon.maxdiv_v = divergence_v
        mon.xwidth = "target_width"
        mon.yheight = "target_height"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 0], RELATIVE="psd_lin_horizontal")

        info = self.plot_info.new(mon, title="Divergence 2D target size")
        info.set_xlabel("Horizontal divergence [deg]")
        info.set_ylabel("Vertical divergence [deg]")

    def add_brilliance_analysis_to_instrument(self, instrument, instrument_parameters):
        """
        Adds monitors for target analysis in terms of brilliance transfer to instrument

        After successful optimization the target from the guide is analyzed with
        more monitors than during the optimization. These can save more data,
        and the simulations can be performed with a much greater ncount for
        better quality. The monitors in this part should all have limits for
        divergence and space so that they can be normalized as brilliance
        transfer. The normalization is done by inserting these monitors after
        the same moderator in another instrument, and their signal is used
        to normalize each monitor before plotting.

        Parameters
        ----------

        instrument : McStasScript instrument object
            Instrument object to which the monitor is added

        Returns
        -------
        horizontal and vertical maximum divergence needed : float, float

        """

        return None, None

    def perform_analysis(self, instrument, instrument_brill_ref, parameters,
                         settings):
        """
        Performs analysis of the optimized guide using McStasScript

        After the guide has been optimized, it is characterized by performing
        simulations using the optimal parameters and the additional monitors
        added by the add_analysis_to_instrument method of this class. Here
        a number of wavelength snapshots are defined, and simulations are
        performed with these wavelength ranges. A simulation with a wavelength
        interval larger than the figure of merit is also added. All results
        are plotted and saved to disk in the folder describing the current
        run. This method is intended to be overwritten by the user in order to
        customize how the optimized guides are characterized and the final
        results are presented.

        Parameters
        ---------

        instrument : McStasScript instrument object
            Instrument with current moderator and added analysis monitors

        instrument_brill_ref : McStasScript instrument object
            Instrument with only current moderator and brilliance monitors

        parameters : Dict
            Found optimal parameters for the guide system

        settings : Dict
            Settings for running simulation, optional to use these
        """

        # Snapshot width can be given in settings, float with unit [AA]
        if "snapshot_widths" in settings:
            snapshot_widths = settings["snapshot_widths"]
        else:
            snapshot_widths = 0.01

        snapshot_centers = np.linspace(self["min_wavelength"], self["max_wavelength"], 3)

        snapshot_minimums = snapshot_centers - 0.5 * snapshot_widths
        snapshot_maximums = snapshot_centers + 0.5 * snapshot_widths

        for min_wavelength, max_wavelength, center in zip(snapshot_minimums, snapshot_maximums, snapshot_centers):
            name = "Snapshot_" + str(center) + "_AA"

            parameters["min_wavelength"] = min_wavelength
            parameters["max_wavelength"] = max_wavelength

            sim_data = run_simulation(name, parameters, settings, instrument)

            self.plot_info.apply_all_data(sim_data)
            #self.plot_info.apply_all_data(ref_data) # Doesnt handle case where not all found

            if sim_data is not None:
                plotter.make_sub_plot(sim_data[0:6], filename=name + "_1.png")
                plotter.make_sub_plot(sim_data[6:], filename=name + "_2.png")

        name = "large_wavelength_band"
        parameters["min_wavelength"] = 0.5 * self["min_wavelength"]
        parameters["max_wavelength"] = 2.0 * self["max_wavelength"]

        sim_data = run_simulation(name, parameters, settings, instrument)

        self.plot_info.apply_all_data(sim_data)
        #self.plot_info.apply_all_data(ref_data) # Doesnt handle case where not all found

        if sim_data is not None:
            plotter.make_sub_plot(sim_data[0:6], filename=name + "_1.png")
            plotter.make_sub_plot(sim_data[6:], filename=name + "_2.png")

        name = "fom_wavelength_band"
        parameters["min_wavelength"] = self["min_wavelength"]
        parameters["max_wavelength"] = self["max_wavelength"]

        sim_data = run_simulation(name, parameters, settings, instrument)

        self.plot_info.apply_all_data(sim_data)
        # self.plot_info.apply_all_data(ref_data) # Doesnt handle case where not all found

        if sim_data is not None:
            plotter.make_sub_plot(sim_data[0:6], filename=name + "_1.png")
            plotter.make_sub_plot(sim_data[6:], filename=name + "_2.png")





