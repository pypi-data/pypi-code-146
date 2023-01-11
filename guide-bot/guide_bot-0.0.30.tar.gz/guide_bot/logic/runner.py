import copy
import os
import dill
import shutil

from guide_bot.parameters import instrument_parameters as ipars
from guide_bot.parameters import instrument_parameter_container as ipars_container
from guide_bot.logic import length_system
from guide_bot.optimizer import optimizer
from guide_bot.logic.line_of_sight import LosCalculator

from mcstasscript.interface import instr, plotter, functions


class RunFromFile:
    """
    Manages process of combining a user defined Guide object with the
    provided figure of merit and source, create the instrument object and
    perform the numerical optimization. The length system is used to
    parametrize the length and start points, providing a lower number of
    variables due to the overall constraint of a total instrument length
    and internal constraints. When this method is invoked, the moderator
    and target objects on guide_bot_run are managed, so their values are
    set to the current scan point.
    """

    def __init__(self, filename, settings=None):
        # open package
        infile = open(filename, "rb")
        package = dill.load(infile)
        infile.close()

        # unpack to usual parameter names
        self.scan_name = package["scan_name"]
        self.guide = package["guide"]
        self.settings = package["settings"]
        self.moderator = package["moderator"]
        self.analysis_moderators = package["analysis_moderators"]
        self.target = package["target"]
        self.required_components = package["required_components"]

        if settings is not None:
            # Allows easy update of any settings for cluster runs
            self.settings.update(settings)

        self.instrument = None
        self.optimized_parameters = None

        self.guide.restore_original()

        instr_parameters = ipars_container.InstrumentParameterContainer()
        self.perform_optimization(instr_parameters)

        self.analysis_moderators = [self.moderator] + self.analysis_moderators
        for analysis_moderator in self.analysis_moderators:
            self.perform_analysis(analysis_moderator, instr_parameters)

    def perform_optimization(self, instr_parameters):
        """
        Runs the main optimization of the guide

        Main optimization runs can have many free parameters and will have a
        long run time with potentially thousands of simulation runs.
        The instrument parameters taken are populated by the create_instrument
        method as the guide will provide the relevant parameters. After the
        optimization, the best parameters are stored in the instrument
        parameter object.

        Parameters
        ----------

        instr_parameters : InstrumentParameterContainer
            Empty container for parameters, populated by this method
        """

        optimization_foldername = self.scan_name + "_main_optimization"
        self.create_folder(optimization_foldername)
        base_folder = os.getcwd()
        os.chdir(optimization_foldername)

        instrument = self.create_instrument(self.moderator, instr_parameters, optimization_mode=True)

        print("debug print")
        print(instr_parameters)

        self.guide.write_log_file(self.scan_name + ".guide_log")

        foldername = self.scan_name + "_optimization"
        self.create_folder(foldername)
        self.settings["foldername"] = os.path.join(foldername, "data")
        best_x = optimizer.run_optimizer(instrument=instrument, my_parameters=instr_parameters,
                                         guide=self.guide, settings=self.settings, scan_name=self.scan_name)
        los_calculator = LosCalculator(self.guide)
        instr_parameters.set_values(best_x, los_calculator=los_calculator)

        os.chdir(base_folder)

    def perform_analysis(self, analysis_moderator, instr_parameters):
        """
        Performs analysis of a guide, but can include smaller optimization

        An analysis run takes an optimized guide and a moderator description
        and runs a thorough analysis handled by the Target object. If the
        moderator has free parameters, these will be optimized before analysis
        which could include angling the guide relative to the moderator.
        The data is saved to disk an log files are included.

        Parameters
        ----------

        analysis_moderator : Object derived from BaseSource
            The source used for this analysis

        instr_parameters : InstrumentParameterContainer
            Container with parameters set to described desired guide
        """

        # Generate folder for results
        analysis_name = self.scan_name + "_" + analysis_moderator.get_name()

        self.create_folder(analysis_name)
        base_folder = os.getcwd()
        os.chdir(analysis_name)

        print("given instr_parameters to perform_analysis")
        print(instr_parameters)

        # Start new parameter container
        partial_instr_parameter = ipars_container.InstrumentParameterContainer()

        # Recreate instrument with new parameters
        instrument = self.create_instrument(analysis_moderator, partial_instr_parameter, optimization_mode=True)

        if analysis_moderator is self.moderator:
            # Lock all parameters
            partial_instr_parameter.fix_free_parameters(instr_parameters)
        else:
            # Lock all parameters with a category not called moderator
            partial_instr_parameter.fix_free_parameters(instr_parameters, exclude="moderator")

        self.guide.connect_to_new_parameters(partial_instr_parameter)
        self.guide.write_log_file(analysis_name + ".guide_log")

        # Perform optimization in case new free parameters are added
        foldername = analysis_name + "_optimization"
        self.create_folder(foldername)
        self.settings["foldername"] = os.path.join(foldername, "optimization")

        print("Free parameters before (possible) optimization")
        partial_instr_parameter.print_free()

        best_x_analysis = optimizer.run_optimizer(instrument=instrument, my_parameters=partial_instr_parameter,
                                                  guide=self.guide, settings=self.settings, scan_name=self.scan_name)

        los_calculator = LosCalculator(self.guide)
        partial_instr_parameter.set_values(best_x_analysis, los_calculator=los_calculator)
        print("best_x: ", best_x_analysis)
        print("free parameters after being set: ")
        partial_instr_parameter.print_free()
        #analysis_parameters = partial_instr_parameter.extract_instrument_parameters(best_x_analysis)

        # Recreate instrument in analysis mode and new parameters
        analysis_instr_parameter = ipars_container.InstrumentParameterContainer()
        instrument = self.create_instrument(analysis_moderator, analysis_instr_parameter, optimization_mode=False)

        if analysis_moderator is self.moderator:
            # Lock all parameters
            analysis_instr_parameter.fix_free_parameters(instr_parameters)
        else:
            # Lock all parameters with a category not called moderator
            analysis_instr_parameter.fix_free_parameters(instr_parameters, exclude="moderator")

        self.guide.connect_to_new_parameters(analysis_instr_parameter)
        los_calculator = LosCalculator(self.guide)

        print("best x:", best_x_analysis)
        print("analysis_instr")
        analysis_instr_parameter.print_free()

        #analysis_parameters = partial_instr_parameter.extract_instrument_parameters(best_x_analysis, los_calculator=los_calculator)
        analysis_parameters = analysis_instr_parameter.extract_instrument_parameters(best_x_analysis, los_calculator=los_calculator)

        dummy = ipars_container.InstrumentParameterContainer()

        # Can only run brilliance if div requirements are set
        if "div_horizontal" in self.target.parameters.parameters and "div_vertical" in self.target.parameters.parameters:
            instrument_brill_ref = analysis_moderator.create_brilliance_reference_instrument(self.scan_name, dummy, self.target)
        else:
            instrument_brill_ref = None

        print("Performing analysis with following parameters:")
        print(analysis_parameters)
        print("Running target.perform_analysis")

        self.target.perform_analysis(instrument, instrument_brill_ref, analysis_parameters, self.settings)

        os.chdir(base_folder)

    def create_folder(self, foldername):
        """
        Creates new work folder, including necessary McStas components
        """
        try:
            os.mkdir(foldername)
        except OSError:
            raise RuntimeError("Could not create folder for optimization data! " + foldername)

        current_folder = os.getcwd()
        for file_name in self.required_components:
            origin = os.path.join(current_folder, file_name)
            destination = os.path.join(current_folder, foldername, file_name)

            shutil.copyfile(origin, destination)

    def create_instrument(self, moderator, instr_parameters, optimization_mode=True):
        """
        Makes an instrument object from guide, moderator, target and parameters

        The method constructs the instrument including the source described by
        the moderator object, the guide object and the target object. The
        instrument parameters provided will be populated with the relevant
        parameters from the guide. It can be chosen to have an optimization mode
        on or off with the relevant parameter, in the optimization mode only
        the figure of merit monitor is included in the McStas simulation to save
        on IO during an optimization. When the optimization_mode is disabled,
        a large amount of data is recorded with a range of monitors to describe
        the beam. The monitors for either are controlled by the Target object.


        Parameters
        ----------

        moderator : Object derived from BaseSource
            The source used in this insturment

        instr_parameters : InstrumetParmeterContaienr
            Container parameter which will be populated by this method

        optimization_mode : Bool
            If True instrument only has figure of merit monitors
        """

        self.guide.restore_original()

        instr_parameters.set_current_category("moderator")
        self.guide.set_current_owner("moderator")
        moderator.apply_guide_start(self.guide)
        moderator.add_start(self.guide, instr_parameters)

        instr_parameters.set_current_category("target")
        self.guide.set_current_owner("target")
        self.target.add_end(self.guide, instr_parameters)
        self.guide.transfer_end_specifications()

        self.guide.set_current_owner(None)  # Reset current owner of guide

        instr_parameters.set_current_category("length_system")
        if self.guide.overwrite_instrument_length is None:
            instrument_length = self.target["instrument_length"]
        else:
            instrument_length = self.guide.overwrite_instrument_length
        length_system.length_system(self.guide.guide_elements, instrument_length, instr_parameters)

        # Start the instrument object
        instrument = instr.McStas_instr(self.scan_name)
        instrument.add_component("Origin", "Progress_bar")

        # Inform all guide elements of the instrument and instrument parameters
        instr_parameters.set_current_category("guide")
        self.guide.set_instrument_and_instr_parameters(instrument, instr_parameters)

        # Before adding source, the target needs to set wavelength range
        instr_parameters.set_current_category("target")
        self.target.add_target_info(instr_parameters)

        # Add guide system to the instrument
        instr_parameters.set_current_category("guide")
        self.guide.add_to_instrument(self.target.get_size_parameters())

        # Add source to the instrument
        instr_parameters.set_current_category("moderator")
        focus_info = self.guide.get_source_focus(self.target)
        moderator.add_to_instrument(instrument, instr_parameters, focus_info)

        # Add target to the instrument
        instr_parameters.set_current_category("target")
        if optimization_mode:
            self.target.add_to_instrument(instrument, instr_parameters)
        else:
            self.target.add_analysis_to_instrument(instrument, instr_parameters)
            self.target.add_brilliance_analysis_to_instrument(instrument, instr_parameters)

        instr_parameters.set_current_category(None) # Disable category system
        # Export the instrument parameters to the instrument to become parameters
        instr_parameters.export_to_instrument(instrument)

        """
        print("Info on created instrument")
        instrument.print_components()
        instrument.show_parameters()
        """

        return instrument

    def create_brill_ref_instrument(self, moderator, instr_parameters):
        """
        Creates instrument used for brilliance reference

        Requires sample has divergence limits as well as required spatial
        limits.

        Parameters
        ----------

        moderator : Object derived from BaseSource
            The source used in this insturment

        instr_parameters : InstrumetParmeterContaienr
            Container parameter which will be populated by this method
        """

        # Start the instrument object
        instrument = instr.McStas_instr(self.scan_name + "_brill_ref")
        instrument.add_component("Origin", "Progress_bar")

        # Add source to the instrument
        instr_parameters.set_current_category("moderator")
        focus_info = self.guide.get_source_focus(self.target)
        moderator.add_to_instrument(instrument, instr_parameters, focus_info)

        instr_parameters.set_current_category("brilliance")
        self.target.add_brilliance_analysis_to_instrument(instrument, instr_parameters)

        instr_parameters.export_to_instrument(instrument)

        return instrument
