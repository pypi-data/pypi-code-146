import os
import sys
import copy

import numpy as np
import yaml
import mmap
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import ipywidgets as widgets
from IPython.display import display

from mcstasscript.interface import instr, functions, plotter

from guide_bot.logging.log_plotter import LogPlotter


class SingleRun:
    def __init__(self, path, ref_path=None):
        self.path = path
        self.ref_path = ref_path
        if self.ref_path is not None:
            self.has_ref = True
        else:
            self.has_ref = False

        self.name = os.path.split(self.path)[1]

        # Check the folders exist
        if not os.path.isdir(self.path):
            self.data_available = False
            raise NameError("Folder not found.")

        if self.has_ref and not os.path.isdir(self.ref_path):
            self.data_available = False
            raise NameError("Folder not found")

        self.data_available = True

        # load info about the monitors here
        self.main_metadata_list = functions.load_metadata(self.path)

        monitor_sizes = self.load_monitor_sizes(self.path + ".yaml")

        if self.has_ref:
            self.ref_metadata_list = functions.load_metadata(self.ref_path)
            ref_monitor_sizes = self.load_monitor_sizes(self.ref_path + ".yaml")
        else:
            self.ref_metadata_list = None
            ref_monitor_sizes = {}

        self.monitor_info = {}
        for metadata in self.main_metadata_list:
            self.monitor_info[metadata.component_name] = {"data": None, "sum_data": None, "average_data": None,
                                                          "has_ref": False, "ref_data": None}
            self.monitor_info[metadata.component_name]["metadata"] = metadata
            if metadata.component_name in monitor_sizes:
                #self.monitor_info[metadata.component_name]["size"] = monitor_sizes[metadata.component_name]
                size = monitor_sizes[metadata.component_name]
                self.monitor_info[metadata.component_name]["size"] = self.get_monitor_size_value(size, metadata)
            else:
                self.monitor_info[metadata.component_name]["size"] = None

        if self.has_ref:
            for metadata in self.ref_metadata_list:
                if metadata.component_name in self.monitor_info:
                    self.monitor_info[metadata.component_name]["has_ref"] = True
                    self.monitor_info[metadata.component_name]["ref_metadata"] = metadata
                    self.monitor_info[metadata.component_name]["ref_data"] = None
                    self.monitor_info[metadata.component_name]["normalized_data"] = None

                if metadata.component_name in ref_monitor_sizes:
                    size = ref_monitor_sizes[metadata.component_name]
                    #self.monitor_info[metadata.component_name]["ref_size"] = ref_monitor_sizes[metadata.component_name]
                    self.monitor_info[metadata.component_name]["ref_size"] = self.get_monitor_size_value(size, metadata)
                else:
                    self.monitor_info[metadata.component_name]["ref_size"] = None

        run_mccode_path = os.path.join(self.path, "mccode.sim")
        self.run_info = self.read_mccode_meta_data(run_mccode_path)

        if self.has_ref:
            ref_mccode_path = os.path.join(self.ref_path, "mccode.sim")
            self.ref_run_info = self.read_mccode_meta_data(ref_mccode_path)
        else:
            self.ref_run_info = None

        self.monitor_dimensions = {}
        self.monitor_1D_list = []
        self.monitor_2D_list = []
        for monitor in self.monitor_info:
            dimension = self.monitor_info[monitor]["metadata"].dimension
            self.monitor_dimensions[monitor] = dimension
            if type(dimension) == int:
                self.monitor_1D_list.append(monitor)
            elif len(dimension) == 2:
                self.monitor_2D_list.append(monitor)

    def get_monitor_size_value(self, size_data, metadata):
        """
        Gets value from monitor database and metadata,

        The size_data can be floats, in which case they are returned,
        they can also be names that need to looked up in metadata. It
        is also possible it is an expression with names from the
        metadata that then needs to be evaluated first.

        Returns list of horizontal / vertical length in [m]
        """

        return [read_field(size_data[0], metadata),
                read_field(size_data[1], metadata)]

    def load_monitor_sizes(self, path):
        if not os.path.isfile(path):
            return {}

        with open(path, 'r') as ymlfile:
            read_data = yaml.safe_load(ymlfile)

        return read_data

    def get_monitor_list(self):
        if not self.data_available:
            return []

        return list(self.monitor_info.keys())

    def get_1D_monitor_list(self):
        if not self.data_available:
            return []

        return list(self.monitor_1D_list)

    def get_2D_monitor_list(self):
        if not self.data_available:
            return []

        return list(self.monitor_2D_list)

    def get_normalized_monitor_list(self):
        if not self.data_available:
            return []

        normalized_monitors = []
        for mon in self.monitor_info:
            if self.monitor_info[mon]["has_ref"]:
                normalized_monitors.append(mon)

        return normalized_monitors

    def load_data(self, monitor_name, normalize=True):
        if not self.data_available:
            return

        if monitor_name not in self.monitor_info:
            raise KeyError("Didn't find monitor_name: " + str(monitor_name))

        mon_info = self.monitor_info[monitor_name]

        if mon_info["data"] is None:
            metadata = mon_info["metadata"]
            try:
                mon_info["data"] = functions.load_monitor(metadata, self.path)
            except:
                return

        if not normalize:
            return

        if mon_info["has_ref"] and mon_info["ref_data"] is None:
            metadata = mon_info["ref_metadata"]
            try:
                mon_info["ref_data"] = functions.load_monitor(metadata, self.ref_path)
            except:
                return

            data = mon_info["data"]
            ref_data = mon_info["ref_data"]

            if mon_info["size"] is None or mon_info["ref_size"] is None:
                print("No area normalization possible!")
                area_ratio = 1
            else:
                area = mon_info["size"][0]*mon_info["size"][1]
                ref_area = mon_info["ref_size"][0]*mon_info["ref_size"][1]
                area_ratio = ref_area / area

            normalized_data = copy.copy(data)
            normalized_data.Intensity /= ref_data.Intensity
            normalized_data.Intensity *= area_ratio
            normalized_data.Error = np.sqrt(data.Error**2 + ref_data.Error**2)

            normalized_data.set_ylabel("Brilliance transfer [1]")

            # Could change ylabel if 1d data to BT
            self.monitor_info[monitor_name]["normalized_data"] = normalized_data

    def get_data(self, monitor_name, normalize=True):
        if not self.data_available:
            return None

        self.load_data(monitor_name, normalize=normalize)

        if normalize and self.monitor_info[monitor_name]["has_ref"]:
            return self.monitor_info[monitor_name]["normalized_data"]
        else:
            return self.monitor_info[monitor_name]["data"]

    def get_ref_data(self, monitor_name):
        if not self.data_available:
            return None

        self.load_data(monitor_name, normalize=True)

        if self.monitor_info[monitor_name]["has_ref"]:
            return self.monitor_info[monitor_name]["ref_data"]
        else:
            return None

    def get_sum_data(self, monitor_name, normalize=True):
        if not self.data_available:
            return None

        data = self.get_data(monitor_name, normalize=normalize)

        if self.monitor_info[monitor_name]["sum_data"] is None:
            self.monitor_info[monitor_name]["sum_data"] = np.sum(data.Intensity)

        return self.monitor_info[monitor_name]["sum_data"]

    def get_average_data(self, monitor_name, normalize=True):
        if not self.data_available:
            return None

        data = self.get_data(monitor_name, normalize=normalize)

        if self.monitor_info[monitor_name]["average_data"] is None:
            self.monitor_info[monitor_name]["average_data"] = np.sum(data.Intensity)/len(data.Intensity)

        return self.monitor_info[monitor_name]["average_data"]

    def read_mccode_meta_data(self, mccode_path):

        if not os.path.isfile(mccode_path):
            raise RuntimeError("No mccode.sim file!")

        parameters = ["min_wavelength", "max_wavelength"]

        search = {}
        for par in parameters:
            search[par] = "Param: " + par

        values = {}

        with open(mccode_path, "r+b") as f:
            with mmap.mmap(f.fileno(), 0) as mm:
                for par in search:
                    # find the parameter string in the file and seek there
                    search_term = search[par]

                    try:
                        mm.seek(mm.find(search_term.encode("UTF-8")))
                        line = mm.readline().strip().decode("UTF-8")
                        values[par] = float(line.split("=")[1])
                    except:
                        values[par] = None

        return values

    def get_monitor_list(self):
        if not self.data_available:
            return []

        return list(self.monitor_info.keys())

    def __repr__(self):
        string = ""

        string += "Run: " + self.name + " "
        if self.has_ref:
            string += "with ref."
        else:
            string += "without ref."

        return string


class SourceAnalysis:
    def __init__(self, path):
        self.path = path
        self.data_folders = []
        self.runs = {}
        self.find_runs()

        self.log_file = None
        self.guide_log_file = None
        self.find_logs()

    def find_runs(self):
        folders = os.listdir(self.path)

        self.data_folders = []
        for folder in folders:
            folder_path = os.path.join(self.path, folder)
            if os.path.isdir(folder_path):
                mccode_path = os.path.join(folder_path, "mccode.sim")
                if os.path.isfile(mccode_path):
                    self.data_folders.append(folder_path)

        data_loaded = {}
        for folder in self.data_folders:
            data_loaded[folder] = False

        # Find brill cases
        for folder in self.data_folders:
            if folder.endswith("_brill"):
                base_foldername = folder.strip("_brill")
                if base_foldername in self.data_folders:
                    run = SingleRun(base_foldername, ref_path=folder)
                    data_loaded[base_foldername] = True
                    data_loaded[folder] = True
                    self.runs[run.name] = run

        for folder in self.data_folders:
            if not data_loaded[folder]:
                run = SingleRun(folder)
                self.runs[run.name] = run

    def find_logs(self):
        files = os.listdir(self.path)
        for file in files:
            if file.endswith(".guide_log"):
                self.guide_log_file = os.path.join(self.path, file)
            if file.endswith(".log"):
                self.log_file = os.path.join(self.path, file)

    def show_runs(self):
        for run in self.runs:
            print(self.runs[run])

    def get_run_list(self):
        return list(self.runs.keys())

    def get_log_plotter(self):
        self.find_logs()
        return LogPlotter(self.log_file, self.guide_log_file)

    def overview_plot(self):
        self.get_log_plotter().plot_overview()


class ScanOverview:
    def __init__(self, project_path):
        self.project_path = project_path
        overview_path = os.path.join(project_path, "run_overview.yaml")

        with open(overview_path, 'r') as ymlfile:
            self.overview = yaml.safe_load(ymlfile)

        # build up paths for expected data directories
        self.guides = self.overview["guide_names"]

        self.target_scan = self.overview["target"]["target_scan"]
        self.moderator_scan = self.overview["moderator"]["moderator_scan"]

        if "target_units" in self.overview["target"]:
            self.target_scan_units = self.overview["target"]["target_units"]
        else:
            self.target_scan_units = None

        if "moderator_units" in self.overview["moderator"]:
            self.moderator_scan_units = self.overview["moderator"]["moderator_units"]
        else:
            self.moderator_scan_units = None

        # build up a list of scanned parameters (target first)
        self.scan_list_target = list(self.target_scan.keys())
        scan_list_target_lengths = []
        for par_name in self.scan_list_target:
            scan_list_target_lengths.append(len(self.target_scan[par_name]))

        # moderator
        self.scan_list_moderator = list(self.moderator_scan.keys())
        scan_list_moderator_lengths = []
        for par_name in self.scan_list_moderator:
            scan_list_moderator_lengths.append(len(self.moderator_scan[par_name]))

        # Collected scan
        self.total_scan_pars = len(self.scan_list_target) + len(self.scan_list_moderator)

        self.scan_list_cut = len(self.scan_list_target)
        self.scan_list = self.scan_list_target + self.scan_list_moderator
        self.scan_lengths = scan_list_target_lengths + scan_list_moderator_lengths

        # Get list of moderators for which analysis was performed
        self.moderator_list = []
        self.moderator_list.append(self.overview["moderator"]["moderator_name"])
        self.moderator_list += self.overview["analysis_moderators"]

        self.data = {} # Will contain loaded data
        self.log = {} # Will contain path to main log file
        self.log_plotter = {} # Will contain log_plotter objects (when loaded)

        self.succesful_indices = {}

    def get_guide_names(self):
        return self.overview["guide_names"]

    def get_moderators(self):
        return self.moderator_list

    def get_shape(self):
        return self.scan_lengths

    def get_scanned_target_parameters(self):
        return self.scan_list_target

    def get_par_index_target(self, parameter):
        if parameter not in self.scan_list_target:
            raise KeyError("Parameter name not found in target scan list")

        return self.scan_list_target.index(parameter)

    def get_scanned_target_parameter_values(self, par):
        return self.target_scan[par]

    def get_scanned_target_unit(self, par):
        if self.target_scan_units is not None:
            if par in self.target_scan_units:
                return self.target_scan_units[par]

        return None

    def get_global_index_from_target_index(self, index):
        return index

    def get_global_index_from_target_parameter(self, parameter):
        index = self.get_scanned_target_parameters().index(parameter)
        return self.get_global_index_from_target_index(index)

    def get_scanned_moderator_parameters(self):
        return self.scan_list_moderator

    def get_par_index_moderator(self, parameter):
        if parameter not in self.scan_list_moderator:
            raise KeyError("Parameter name not found in moderator scan list")

        return self.scan_list_cut + self.scan_list_moderator.index(parameter)

    def get_scanned_moderator_parameter_values(self, par):
        return self.moderator_scan[par]

    def get_scanned_moderator_unit(self, par):
        if self.moderator_scan_units is not None:
            if par in self.moderator_scan_units:
                return self.moderator_scan_units[par]

        return None

    def get_global_index_from_moderator_index(self, index):
        return index + self.scan_list_cut

    def get_global_index_from_moderator_parameter(self, parameter):
        index = self.get_scanned_moderator_parameters().index(parameter)
        return self.get_global_index_from_moderator_index(index)

    def get_n_scanned_parameters(self):
        return self.total_scan_pars

    def get_scanned_parameters(self):
        return self.scan_list

    def get_type_from_index(self, index):
        if index < self.scan_list_cut:
            return "target"
        else:
            return "moderator"

    def get_scan_values(self, index):
        parameter_name = self.get_scanned_parameters()[index]
        scan_type = self.get_type_from_index(index)
        if scan_type == "target":
            return self.target_scan[parameter_name]
        elif scan_type == "moderator":
            return self.moderator_scan[parameter_name]
        else:
            raise RuntimeError("Failed to get scan_type.")

    def show_scan(self):
        for index, parameter in enumerate(self.get_scanned_parameters()):
            values = self.get_scan_values(index)

            type = self.get_type_from_index(index)
            if type == "moderator":
                unit = self.get_scanned_moderator_unit(parameter)
            elif type == "target":
                unit = self.get_scanned_target_unit(parameter)

            print(type.ljust(12) + parameter.ljust(10) + str(values) + " [" + unit + "]")

    def get_state_string(self, guide_name, indices):
        if type(guide_name) is int:
            guide_names = self.get_guide_names()
            guide_name = guide_names[guide_name]

        if guide_name not in self.get_guide_names():
            raise KeyError("guide_name not found")

        if len(indices) != self.total_scan_pars:
            raise IndexError("Length of index list wrong.")

        for index in range(len(indices)):
            if indices[index] >= self.scan_lengths[index]:
                raise IndexError("Index over length for nr: " + str(index))
            if indices[index] < 0:
                raise IndexError("Index less than 0 for nr: " + str(index))

        target_scan = indices[0:self.scan_list_cut]
        mod_scan = indices[self.scan_list_cut:]

        target_dict = {}
        for index in range(len(target_scan)):
            target_dict[self.scan_list_target[index]] = target_scan[index]

        mod_dict = {}
        for index in range(len(mod_scan)):
            mod_dict[self.scan_list_moderator[index]] = mod_scan[index]

        # todo: update this inefficient search
        for scan_state in self.overview["scan_states"]:

            target_state = scan_state["target_scan"]
            if target_dict != target_state:
                continue

            mod_state = scan_state["moderator_scan"]
            if mod_dict != mod_state:
                continue

            return scan_state["scan_state"]

    def get_base_data_location(self, guide_name, indices):
        if type(guide_name) is int:
            guide_names = self.get_guide_names()
            guide_name = guide_names[guide_name]

        state_string = self.get_state_string(guide_name, indices)

        return os.path.abspath(os.path.join(self.project_path, guide_name, guide_name + state_string))

    def get_optimization_base_data_location(self, guide_name, indices):
        if type(guide_name) is int:
            guide_names = self.get_guide_names()
            guide_name = guide_names[guide_name]

        state_string = self.get_state_string(guide_name, indices)

        return os.path.abspath(os.path.join(self.project_path, guide_name,
                                            guide_name + state_string + "_main_optimization",
                                            guide_name + state_string))

    def get_data_location(self, guide_name, indices, analysis_moderator=None):
        if type(guide_name) is int:
            guide_names = self.get_guide_names()
            guide_name = guide_names[guide_name]

        if analysis_moderator not in self.moderator_list and analysis_moderator is not None:
            raise KeyError("analysis_moderator not found.")

        if analysis_moderator is None:
            analysis_moderator = self.overview["moderator"]["moderator_name"]

        return self.get_base_data_location(guide_name, indices) + "_" + analysis_moderator

    def path_is_data_directory(self, path):
        """
        Method for checking if data directory exists

        Can be expanded further to check all snapshots completed
        """

        return os.path.isdir(path)

    def guide_run_status(self, guide):
        scan = np.ndindex(*self.get_shape())
        widget_list = []
        widget_list_analysis = []
        while (True):
            try:
                state = next(scan)
            except StopIteration:
                break

            # check if main moderator written
            data_path = self.get_data_location(guide, state)
            main_analysis_success = self.path_is_data_directory(data_path)
            data_name = guide + self.get_state_string(guide, state)

            valid_box = widgets.Valid(value=main_analysis_success)
            widget = widgets.HBox([widgets.Label(data_name), valid_box])

            widget_list.append(widget)

            # check if analysis moderators written
            for analysis_mod_name in self.overview["analysis_moderators"]:
                expected_data = self.get_data_location(guide, state, analysis_moderator=analysis_mod_name)
                data_name = guide + self.get_state_string(guide, state) + "_" + analysis_mod_name
                analysis_success = os.path.isdir(expected_data)

                valid_box = widgets.Valid(value=analysis_success)
                widget = widgets.HBox([widgets.Label(data_name), valid_box])

                widget_list_analysis.append(widget)

        display(widgets.VBox(widget_list))
        display(widgets.VBox(widget_list_analysis))

    def run_status(self):

        for guide in self.get_guide_names():
            self.guide_run_status(guide)

    def load_guide_run_information(self, guide):

        self.data[guide] = {}
        self.log[guide] = {}
        self.log_plotter[guide] = {}

        scan = np.ndindex(*self.get_shape())
        while True:
            try:
                state = next(scan)
            except StopIteration:
                break

            self.log[guide][state] = {}
            self.log[guide][state]["main"] = {}
            self.log_plotter[guide][state] = {}
            self.log_plotter[guide][state]["main"] = None

            expected_guide_log_path = self.get_base_data_location(guide, state) + ".guide_log"
            if os.path.isfile(expected_guide_log_path):
                self.log[guide][state]["main"]["guide_log"] = expected_guide_log_path
            else:
                expected_guide_log_path = self.get_optimization_base_data_location(guide, state) + ".guide_log"
                if os.path.isfile(expected_guide_log_path):
                    self.log[guide][state]["main"]["guide_log"] = expected_guide_log_path
                else:
                    self.log[guide][state]["main"]["guide_log"] = None

            expected_log_path = self.get_base_data_location(guide, state) + "_optimization.log"
            if os.path.isfile(expected_log_path):
                self.log[guide][state]["main"]["log"] = expected_log_path
            else:
                expected_log_path = self.get_optimization_base_data_location(guide, state) + "_optimization.log"
                if os.path.isfile(expected_log_path):
                    self.log[guide][state]["main"]["log"] = expected_log_path
                else:
                    self.log[guide][state]["main"]["log"] = None

            self.data[guide][state] = {}

            any_success = False
            for mod in self.moderator_list:
                path = self.get_data_location(guide, state, analysis_moderator=mod)

                if self.path_is_data_directory(path):
                    source_analysis = SourceAnalysis(path)
                    self.data[guide][state][mod] = source_analysis
                    self.log[guide][state][mod] = {}
                    self.log[guide][state][mod]["log"] = source_analysis.log_file
                    self.log[guide][state][mod]["guide_log"] = source_analysis.guide_log_file
                    any_success = True
                else:
                    self.data[guide][state][mod] = None
                    self.log[guide][state][mod] = {}
                    self.log[guide][state][mod]["log"] = None
                    self.log[guide][state][mod]["guide_log"] = None

                self.log_plotter[guide][state][mod] = None

            if any_success:
                if guide not in self.succesful_indices:
                    self.succesful_indices[guide] = []
                self.succesful_indices[guide].append(state)

    def load_run_information(self):
        for guide in self.get_guide_names():
            self.load_guide_run_information(guide)

    def get_log_plotter(self, guide, state, mod):
        if self.log_plotter[guide][state][mod] is not None:
            return self.log_plotter[guide][state][mod]

        log_file = self.log[guide][state][mod]["log"]
        guide_log_file = self.log[guide][state][mod]["guide_log"]
        if log_file is None:
            print("log file not found for this combination.")
            return None

        if guide_log_file is None:
            print("guide log file not found for this combination.")
            return None

        self.log_plotter[guide][state][mod] = LogPlotter(log_file, guide_log_file)
        return self.log_plotter[guide][state][mod]

    def plot_fom_guide_overview_ax(self, ax, guide, mod="main", cs_start=0, cs_end=1, **kwargs):
        log_plotters = []
        scan = np.ndindex(*self.get_shape())
        while True:
            try:
                state = next(scan)
            except StopIteration:
                break

            log_plotter = self.get_log_plotter(guide, state, mod)
            if log_plotter is not None:
                log_plotters.append(log_plotter)

        colors = cm.rainbow(np.linspace(cs_start, cs_end, len(log_plotters)))
        for log_plotter, color in zip(log_plotters, colors):
            log_plotter.plot_1D_fom_ax(ax, color=color, **kwargs)

    """
    def plot_fom_guide_overview(self, guide, mod="main", figsize=(12, 8), **kwargs):
        fig, ax = plt.subplots(figsize=figsize)
        self.plot_fom_guide_overview_ax(ax=ax, guide=guide, mod=mod, **kwargs)

        add_side_legend(ax)
    """

    def plot_fom_overview(self, guide=None, mod="main", figsize=(12,8), **kwargs):
        if guide is None:
            guides_to_plot = self.get_guide_names()
        else:
            guides_to_plot = [guide]

        fig, ax = plt.subplots(figsize=figsize)
        n_guides = len(guides_to_plot)
        cs_start = [x / n_guides for x in range(n_guides)]
        cs_end = [(x + 1) / n_guides for x in range(n_guides)]
        for guide, cs_s, cs_e in zip(guides_to_plot, cs_start, cs_end):
            self.plot_fom_guide_overview_ax(ax=ax, guide=guide, mod=mod, cs_start=cs_s, cs_end=cs_e, **kwargs)

        add_side_legend(ax)


def add_side_legend(ax):
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=7)
    plt.show()


def read_field(field, metadata):

    value = None
    try:
        # If a float or int is given directly, just read that
        value = float(field)
    except ValueError:
        # If a parameter name is given directly, look that up
        if field in metadata.parameters:
            value = metadata.parameters[field]

    # Last attempt to read using python eval in case a simple expression is used
    # This will catch for example "2.0*target_width"
    if value is None:
        try:
            # Try to evaluate field with scope of all instrument parameters
            value = eval(field, metadata.parameters)
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
