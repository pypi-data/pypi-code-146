from .BaseTarget import BaseTarget
from .Helper import run_simulation, run_simulation_brill, normalize_brill_ref


from guide_bot.requirements.requirement_parameters import Parameters
from guide_bot.elements import Element_gap

from mcstasscript.interface import instr, plotter, functions

# May be needed

import math

import numpy as np
import yaml


from guide_bot.parameters import instrument_parameters as ipars


class Target(BaseTarget):
    def __init__(self, width, height,
                 div_horizontal, div_vertical,
                 min_wavelength, max_wavelength,
                 instrument_length, target_guide_distance,
                 calculate_guide_end_dimensions=True):
        """
        Description of figure of merit for guide optimization

        All given parameters can be scanned by providing an list of floats
        instead of just a single float. All Parameters can be read using
        target["par_name"], and will return the current value instead of the
        entire list for the scan.

        Parameters
        ----------

        width : float or list of floats for scan
            Width of target at target position in [m]

        height : float or list of floats for scan
            Height of target at target position in [m]

        div_horizontal : float or list of floats for scan
            Horizontal target divergence figure of merit in [deg]

        div_vertical : float or list of floats for scan
            Vertical target divergence figure of merit in [deg]

        min_wavelength : float or list of floats for scan
            Minimum wavelength in figure of merit [Å]

        max_wavelength : float or list of floats for scan
            Maximum wavelength in figure of merit [Å]

        instrument_length : float or list of floats for scan
            Distance from source to target in [m]

        target_guide_distance : float or list of floats for sc  an
            Distance from guide end to target in [m]

        calculate_guide_end_dimensions: bool or list of bools for scan (default True)
            If true, the guides end dimensions are calculated from target requirements
        """

        super().__init__(width=width, height=height,
                         min_wavelength=min_wavelength, max_wavelength=max_wavelength,
                         instrument_length=instrument_length,
                         target_guide_distance=target_guide_distance)
        # Required
        self.parameters.add("div_horizontal", div_horizontal, unit="deg")
        self.parameters.add("div_vertical", div_vertical, unit="deg")

        # Optional (has default value)
        self.parameters.add("calculate_guide_end_dimensions", calculate_guide_end_dimensions, unit="bool")

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

        mon = instrument.add_component("mon", "Divergence_monitor")

        mon.nh = 20
        mon.nv = 20
        mon.filename = '"fom.dat"'
        mon.maxdiv_h = self["div_horizontal"]
        mon.maxdiv_v = self["div_vertical"]
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
        width = self["width"] + 2 * math.tan(self["div_horizontal"] * math.pi / 180.0) * target_guide_distance
        height = self["height"] + 2 * math.tan(self["div_vertical"] * math.pi / 180.0) * target_guide_distance

        if self["calculate_guide_end_dimensions"]:
            # If end dimensions should be calculated, use exact values
            width_input = width
            height_input = height
        else:
            # If end dimensions should be optimized, use calculated values to set reasonable limits
            width_input = [0.5 * width, 1.5 * width]
            height_input = [0.5 * height, 1.5 * height]

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

        mcstas_version = instrument.mccode_version

        mon = instrument.add_component("psd_lin_horizontal", "PSDlin_monitor")
        mon.filename = '"psd_lin_horizontal.dat"'
        mon.xwidth = "2.0*target_width"
        mon.yheight = "target_height"
        mon.restore_neutron = 1
        if mcstas_version == 2:
            mon.nx = 300
        else:
            mon.nbins = 300
        mon.set_AT([0, 0, 0], RELATIVE=self.target_gap.end_component_name)

        info = self.plot_info.new(mon, title="Horizontal position")
        info.set_xlabel("Horizontal position [cm]")
        info.set_plot_options(x_axis_multiplier=100)

        mon = instrument.add_component("psd_lin_vertical", "PSDlin_monitor")
        if mcstas_version == 2:
            mon.nx = 300
        else:
            mon.nbins = 300
        mon.filename = '"psd_lin_vertical.dat"'
        mon.xwidth = "2.0*target_height"
        mon.yheight = "target_width"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 90], RELATIVE="psd_lin_horizontal")

        info = self.plot_info.new("psd_lin_vertical", title="Vertical position")
        info.set_xlabel("Vertical position [cm]")
        info.set_plot_options(x_axis_multiplier=100)

        if mcstas_version == 2:
            mon = instrument.add_component("divergence_horizontal", "Hdiv_monitor")
            mon.nh = 200
            mon.h_maxdiv = 2 * self["div_horizontal"]
        else:
            mon = instrument.add_component("divergence_horizontal", "Div1D_monitor")
            mon.ndiv = 200
            mon.maxdiv = 2 * self["div_horizontal"]
            mon.vertical = 0

        mon.filename = '"divergence_horizontal.dat"'
        mon.xwidth = "target_width"
        mon.yheight = "target_height"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 0], RELATIVE="psd_lin_horizontal")

        info = self.plot_info.new(mon, title="Horizontal divergence")
        info.set_xlabel("Horizontal divergence [deg]")


        if mcstas_version == 2:
            mon = instrument.add_component("divergence_vertical", "Hdiv_monitor")
            mon.nh = 200
            mon.h_maxdiv = 2 * self["div_vertical"]
            mon.set_ROTATED([0, 0, 90], RELATIVE="psd_lin_horizontal")
        else:
            mon = instrument.add_component("divergence_vertical", "Div1D_monitor")
            mon.ndiv = 200
            mon.maxdiv = 2 * self["div_vertical"]
            mon.vertical = 1
            mon.set_ROTATED([0, 0, 0], RELATIVE="psd_lin_horizontal")

        mon.filename = '"divergence_vertical.dat"'
        mon.xwidth = "target_height"
        mon.yheight = "target_width"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")

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
        mon.maxdiv_h = 2 * self["div_horizontal"]
        mon.maxdiv_v = 2 * self["div_vertical"]
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
        if mcstas_version == 2:
            mon.nh = 200
            mon.maxdiv_h = 2 * self["div_horizontal"]
        else:
            mon.nb = 200
            mon.maxdiv = 2 * self["div_horizontal"]
            mon.vertical = 0

        mon.ndiv = 200
        mon.filename = '"Acceptance_horizontal.dat"'
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
        if mcstas_version == 2:
            mon.nh = 200
            mon.maxdiv_h = 2 * self["div_vertical"]
            mon.set_ROTATED([0, 0, 90], RELATIVE="psd_lin_horizontal")
        else:
            mon.nb = 200
            mon.maxdiv = 2 * self["div_vertical"]
            mon.vertical = 1
            mon.set_ROTATED([0, 0, 0], RELATIVE="psd_lin_horizontal")
        mon.ndiv = 200
        mon.filename = '"Acceptance_vertical.dat"'
        mon.xwidth = "2.0*target_height"
        mon.yheight = "target_width"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")


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
        mon.maxdiv_h = self["div_horizontal"]
        mon.maxdiv_v = self["div_vertical"]
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

        mcstas_version = instrument.mccode_version

        instrument.add_declare_var("double", "div_h", comment="Horizontal divergence at target position")
        instrument.add_declare_var("double", "div_h_limit", value=self["div_horizontal"])
        instrument.add_declare_var("int", "inside_h_div",
                                   comment="Flag specifying if ray is within horizontal div limits or not")

        instrument.add_declare_var("double", "div_v", comment="Vertical divergence at target position")
        instrument.add_declare_var("double", "div_v_limit", value=self["div_vertical"])
        instrument.add_declare_var("int", "inside_v_div",
                                   comment="Flag specifying if ray is within vertical div limits or not")

        instrument.add_declare_var("int", "inside_div",
                                   comment="Flag specifying if ray is within div limits or not")

        arm = instrument.add_component("fom_check", "Arm", RELATIVE="PREVIOUS")
        arm.append_EXTEND("div_h = RAD2DEG*atan(vx/vz);")
        arm.append_EXTEND("div_v = RAD2DEG*atan(vy/vz);")
        arm.append_EXTEND("if (div_h < div_h_limit && div_h > -div_h_limit) inside_h_div = 1;")
        arm.append_EXTEND("else inside_h_div=0;")
        arm.append_EXTEND("if ( div_v < div_v_limit && div_v > -div_v_limit) inside_v_div = 1;")
        arm.append_EXTEND("else inside_v_div=0;")
        arm.append_EXTEND("if (inside_h_div == 1 && inside_v_div == 1) inside_div = 1;")
        arm.append_EXTEND("else inside_div=0;")

        mon = instrument.add_component("psd_lin_horizontal_brill", "PSDlin_monitor")
        if mcstas_version == 2:
            mon.nx = 300
        else:
            mon.nbins = 300
        mon.filename = '"psd_lin_horizontal_brill.dat"'
        mon.xwidth = "2.0*target_width"
        mon.yheight = "target_height"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_WHEN("inside_div == 1")

        info = self.plot_info.new(mon, title="Linear PSD")
        info.set_xlabel("Horizontal position [cm]")
        info.set_ylabel("Brilliance transfer [1]")
        info.set_plot_options(x_axis_multiplier=100)

        mon = instrument.add_component("psd_lin_vertical_brill", "PSDlin_monitor")
        if mcstas_version == 2:
            mon.nx = 300
        else:
            mon.nbins = 300
        mon.filename = '"psd_lin_vertical_brill.dat"'
        mon.xwidth = "2.0*target_height"
        mon.yheight = "target_width"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 90], RELATIVE="psd_lin_horizontal_brill")
        mon.set_WHEN("inside_div == 1")

        info = self.plot_info.new(mon, title="Linear PSD")
        info.set_xlabel("Vertical position [cm]")
        info.set_ylabel("Brilliance transfer [1]")
        info.set_plot_options(x_axis_multiplier=100)


        if mcstas_version == 2:
            mon = instrument.add_component("divergence_horizontal_brill", "Hdiv_monitor")
            mon.nh = 200
            mon.h_maxdiv = 2 * self["div_horizontal"]
        else:
            mon = instrument.add_component("divergence_horizontal_brill", "Div1D_monitor")
            mon.ndiv = 200
            mon.maxdiv = 2 * self["div_horizontal"]

        mon.filename = '"divergence_horizontal_brill.dat"'
        mon.xwidth = "target_width"
        mon.yheight = "target_height"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 0], RELATIVE="psd_lin_horizontal_brill")
        mon.set_WHEN("inside_v_div == 1")

        info = self.plot_info.new(mon, title="Linear divergence")
        info.set_xlabel("Horizontal divergence [deg]")
        info.set_ylabel("Brilliance transfer [1]")

        if mcstas_version == 2:
            mon = instrument.add_component("divergence_vertical_brill", "Hdiv_monitor")
            mon.nh = 200
            mon.h_maxdiv = 2 * self["div_vertical"]
            mon.set_ROTATED([0, 0, 90], RELATIVE="psd_lin_horizontal_brill")
        else:
            mon = instrument.add_component("divergence_vertical_brill", "Div1D_monitor")
            mon.ndiv = 200
            mon.maxdiv = 2 * self["div_vertical"]
            mon.vertical = 1
            mon.set_ROTATED([0, 0, 0], RELATIVE="psd_lin_horizontal_brill")

        mon.filename = '"divergence_vertical_brill.dat"'
        mon.xwidth = "target_height"
        mon.yheight = "target_width"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_WHEN("inside_h_div == 1")

        info = self.plot_info.new(mon, title="Linear divergence")
        info.set_xlabel("Vertical divergence [deg]")
        info.set_ylabel("Brilliance transfer [1]")

        mon = instrument.add_component("Lambda_brill", "L_monitor")
        mon.Lmin = "min_wavelength"
        mon.Lmax = "max_wavelength"
        mon.nL = 200
        mon.filename = '"wavelength_brill.dat"'
        mon.xwidth = "target_width"
        mon.yheight = "target_height"
        mon.restore_neutron = 1
        mon.set_AT([0, 0, 1E-6], RELATIVE="PREVIOUS")
        mon.set_ROTATED([0, 0, 0], RELATIVE="psd_lin_horizontal_brill")
        mon.set_WHEN("inside_div == 1")

        info = self.plot_info.new(mon, title="Wavelength")
        info.set_xlabel("Wavelength [AA]")
        info.set_ylabel("Brilliance transfer [1]")

        return 2 * self["div_horizontal"], 2 * self["div_vertical"]

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

        for min_wavelength, max_wavelength, center in zip(snapshot_minimums, snapshot_maximums,
                                                          snapshot_centers):
            name = "Snapshot_" + str(center) + "_AA"

            parameters["min_wavelength"] = min_wavelength
            parameters["max_wavelength"] = max_wavelength

            sim_data = run_simulation(name, parameters, settings, instrument)
            ref_data = run_simulation_brill(name + "_brill", parameters, settings,
                                            instrument_brill_ref)  # will have too many parameters and unrecoignized

            normalize_brill_ref(sim_data, ref_data, instrument, instrument_brill_ref)

            self.plot_info.apply_all_data(sim_data)
            # self.plot_info.apply_all_data(ref_data) # Doesnt handle case where not all found

            if sim_data is not None:
                plotter.make_sub_plot(sim_data[0:6], filename=name + "_1.png")
                plotter.make_sub_plot(sim_data[6:11], filename=name + "_2.png")
                plotter.make_sub_plot(sim_data[11:], filename=name + "_3.png")
                plotter.make_sub_plot(ref_data, filename=name + "_ref.png")

        name = "large_wavelength_band"
        parameters["min_wavelength"] = 0.5 * self["min_wavelength"]
        parameters["max_wavelength"] = 2.0 * self["max_wavelength"]

        sim_data = run_simulation(name, parameters, settings, instrument)
        ref_data = run_simulation_brill(name + "_brill", parameters, settings,
                                        instrument_brill_ref)  # will have too many parameters and unrecoignized

        normalize_brill_ref(sim_data, ref_data, instrument, instrument_brill_ref)

        self.plot_info.apply_all_data(sim_data)
        # self.plot_info.apply_all_data(ref_data) # Doesnt handle case where not all found

        if sim_data is not None:
            plotter.make_sub_plot(sim_data[0:6], filename=name + "_1.png")
            plotter.make_sub_plot(sim_data[6:11], filename=name + "_2.png")
            plotter.make_sub_plot(sim_data[11:], filename=name + "_3.png")
            plotter.make_sub_plot(ref_data, filename=name + "_ref.png")

        name = "fom_wavelength_band"
        parameters["min_wavelength"] = self["min_wavelength"]
        parameters["max_wavelength"] = self["max_wavelength"]

        sim_data = run_simulation(name, parameters, settings, instrument)
        ref_data = run_simulation_brill(name + "_brill", parameters, settings,
                                        instrument_brill_ref)  # will have too many parameters and unrecoignized

        normalize_brill_ref(sim_data, ref_data, instrument, instrument_brill_ref)

        self.plot_info.apply_all_data(sim_data)
        # self.plot_info.apply_all_data(ref_data) # Doesnt handle case where not all found

        if sim_data is not None:
            plotter.make_sub_plot(sim_data[0:6], filename=name + "_1.png")
            plotter.make_sub_plot(sim_data[6:11], filename=name + "_2.png")
            plotter.make_sub_plot(sim_data[11:], filename=name + "_3.png")
            plotter.make_sub_plot(ref_data, filename=name + "_ref.png")






