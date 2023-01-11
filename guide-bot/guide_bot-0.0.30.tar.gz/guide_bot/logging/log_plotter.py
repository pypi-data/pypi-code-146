import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec

from guide_bot.logging.log_plotter_helpers import LogParameter
from guide_bot.logging.log_plotter_helpers import GuideElementLog
from guide_bot.logging.log_plotter_helpers import sort_permutation
from guide_bot.logging.log_plotter_helpers import extract_parameters
from guide_bot.base_elements.base_element_geometry import PositionAndRotation

import guide_bot.elements.Element_gap as Gap
import guide_bot.elements.Element_kink as Kink
import guide_bot.elements.Element_straight as Straight
import guide_bot.elements.Element_elliptic as Elliptic
import guide_bot.elements.Element_curved as Curved
import guide_bot.elements.Element_slit as Slit

from guide_bot.elements.geometry_register import geometry_register

from scipy.spatial.transform import Rotation as R


class LogPlotter:
    def __init__(self, log_filename, guide_log_filename):
        if not os.path.isfile(log_filename):
            raise NameError("Filename not found!" + str(log_filename))

        if not os.path.isfile(guide_log_filename):
            raise NameError("Filename not found!" + str(guide_log_filename))

        self.filename = log_filename
        self.guide_log_filename = guide_log_filename

        self.legend = None
        self.parameters = None
        self.data = None
        self.scan_name = None

        self.read_log_file()

        file_location = os.path.split(self.filename)[0]

        self.guide_element_logs = None
        self.read_guide_log_file()

        self.fom = self.data[:, 0]
        self.fom_sort_indices = sort_permutation(self.fom, reverse=True)

        self.data_fom_sorted = self.data[self.fom_sort_indices, :]
        self.fom_sorted = self.data_fom_sorted[:, 0]

        self.category_dict = {}
        for guide_element in self.guide_element_logs:
            for simple_parameter_name in guide_element.parameter_type:
                par_category = guide_element.parameter_type[simple_parameter_name]
                par_name = guide_element.parameters[simple_parameter_name]
                self.category_dict[par_name] = par_category

        for par in self.parameters:
            if par.name not in self.category_dict:
                self.category_dict[par.name] = "global"

    def read_log_file(self):
        with open(self.filename) as file:
            file.readline()

            second_line = file.readline()
            try:
                n_parameters = int(second_line)
                self.scan_name = None
                skip = n_parameters + 3
            except:
                scan_name = second_line.split(" ")[1]
                self.scan_name = scan_name.strip()
                n_parameters = int(file.readline())
                skip = n_parameters + 4

            parameters = []
            for _ in range(n_parameters):
                par = LogParameter()
                par.read_line(file.readline())
                parameters.append(par)

            self.legend = file.readline().strip().split()

        self.parameters = parameters
        self.data = np.loadtxt(self.filename, skiprows=skip)

        if len(self.data.shape) == 1:
            # 1D array, only one entry. Make it 2D with just one column
            self.data = self.data.reshape(1, self.data.shape[0])

    def read_guide_log_file(self):

        with open(self.guide_log_filename) as file:
            line = file.readline()
            guide_logs = []
            current_log = None
            while line:

                if line.strip() == "":
                    line = file.readline()
                    continue

                if line.startswith("Element"):
                    if current_log is not None:
                        guide_logs.append(current_log)

                    element_type = line.split(" ")[1]
                    element_name = line.split(" ")[2]
                    current_log = GuideElementLog(element_name, element_type)

                elif current_log is not None:
                    par_key = line.split()[0].strip()
                    par_type = line.split()[1].strip()
                    par_name = line.split()[2].strip()

                    current_log.add_parameter(par_key, par_type, par_name)

                line = file.readline()

            if current_log is not None:
                guide_logs.append(current_log)

        self.guide_element_logs = guide_logs

    def plot_best_guide(self):
        fig, axs = plt.subplots(figsize=(10,10), nrows=2, ncols=1)
        self.plot_guide_ax(axs[0], horizontal=True)
        self.plot_guide_ax(axs[1], horizontal=False)

    def plot_guide_ax(self, ax, horizontal=True, data_line=None):

        # If no data is given, plot best configuration
        if data_line is None:
            data_line = self.data_fom_sorted[-1, :]

        # start position and rotation
        start_rot = R.from_euler("z", 0)
        pos_and_rot = PositionAndRotation(np.array([0, 0, 0]), start_rot)

        # plot source
        par_dict = extract_parameters(self.guide_element_logs[0], self.legend, data_line)
        if horizontal:
            if "start_width" in par_dict:
                moderator_width = par_dict["start_width"]
                m_point, p_point = pos_and_rot.width_points(moderator_width)
                ax.plot([m_point[2], p_point[2]], [m_point[0], p_point[0]], color="dimgrey")

        else:
            if "start_height" in par_dict:
                moderator_height = par_dict["start_height"]
                m_point, p_point = pos_and_rot.width_points(moderator_height)
                ax.plot([m_point[1], p_point[1]], [m_point[0], p_point[0]], color="dimgrey")

        # plot guide elements in alternating colors.
        color = "k"
        for guide_element in self.guide_element_logs:

            if color == "k":
                color = "b"
            elif color == "b":
                color = "k"

            # Get dict of generic parameters for this element type that contains the values from this data line
            par_dict = extract_parameters(guide_element, self.legend, data_line)
            Geometry = geometry_register(guide_element.element_type)  # Get appropriate Geometry class for this type
            geometry_object = Geometry(**par_dict)  # Initialize geometry object with the obtained pars / values
            pos_and_rot = geometry_object.plot_on_ax(ax=ax, start_pr=pos_and_rot, horizontal=horizontal, color=color)

        # plot target
        par_dict = extract_parameters(self.guide_element_logs[-1], self.legend, data_line)
        if horizontal:
            if "end_width" in par_dict:
                target_width = par_dict["end_width"]
                m_point, p_point = pos_and_rot.width_points(target_width)
                ax.plot([m_point[2], p_point[2]], [m_point[0], p_point[0]], color="dimgrey")

        else:
            if "end_height" in par_dict:
                target_height = par_dict["end_height"]
                m_point, p_point = pos_and_rot.height_points(target_height)
                ax.plot([m_point[2], p_point[2]], [m_point[1], p_point[1]], color="dimgrey")

        ax.set_xlabel("Distance from source [m]")
        if horizontal:
            ax.set_ylabel("Horizontal [m]")
        else:
            ax.set_ylabel("Vertical [m]")

    def plot_1D_fom_ax(self, ax, highlight_sorted_index=None, **kwargs):
        ax.scatter(range(len(self.fom)), self.fom, marker=".", label=self.scan_name, **kwargs)
        ax.plot(self.fom_sorted, color="orange")
        ax.set_xlabel("Optimizer iteration")
        ax.set_ylabel("FOM")

        if highlight_sorted_index is not None:
            raw_index = self.fom_sort_indices[highlight_sorted_index]
            ax.scatter(raw_index, self.fom[raw_index], s=30,
                       marker="o", label=self.scan_name, color='r', **kwargs)

            ax.scatter(highlight_sorted_index, self.fom_sorted[highlight_sorted_index], s=30,
                       marker="x", label=self.scan_name, color='r', **kwargs)

    def plot_1D_cps_ax(self, ax, sorted=False, **kwargs):
        """
        Plotting change points
        """
        n_guides = len(self.data[:, 0])
        pars_length_system_names = [par.name for par in self.parameters if par.owner == "length_system"]
        pars_length_system_indices = [self.legend.index(par) for par in pars_length_system_names]

        if sorted:
            start_points = self.data_fom_sorted[:, pars_length_system_indices]
        else:
            start_points = self.data[:, pars_length_system_indices]
        start_points_first = start_points[0, :]
        sort_key = sort_permutation(start_points_first)

        ax.plot(range(n_guides), start_points[:, sort_key], **kwargs)
        if sorted:
            ax.set_xlabel("iteration (sorted, fom worst to best)")
        else:
            ax.set_xlabel("Optimizer iteration")
        ax.set_ylabel("start point [m]")

    def plot_1D_given_type_ax(self, ax, type="horizontal", sorted=False, only_free=True, **kwargs):
        """
        Plots parameters of given type
        """
        found_par_names = set()
        for guide_element in self.guide_element_logs:
            for simple_parameter_name in guide_element.parameter_type:
                if guide_element.parameter_type[simple_parameter_name] == type:
                    found_par_names.add(guide_element.parameters[simple_parameter_name])

        if only_free:
            for parameter in self.parameters:
                if parameter.name in found_par_names:
                    free = ("FreeInstrumentParameter", "RelativeFreeInstrumentParameter", "LosInstrumentParameter")
                    if parameter.type not in free:
                        found_par_names.remove(parameter.name)

        plotted_par_indices = [self.legend.index(par) for par in found_par_names if par in self.legend]

        if sorted:
            data = self.data_fom_sorted
        else:
            data = self.data

        n_guides = len(data[:, 0])
        for index in plotted_par_indices:
            ax.scatter(range(n_guides), data[:, index], marker=".", label=self.legend[index], **kwargs)

        ax.legend()
        ax.set_ylabel("Parameter value")
        if sorted:
            ax.set_xlabel("Optimizer iteration (fom sorted, worst to best)")
        else:
            ax.set_xlabel("Optimizer iteration")

    def plot_correlation_ax(self, ax, par1, par2, axis_labels=True, **kwargs):
        par1_index = self.legend.index(par1)
        par2_index = self.legend.index(par2)

        # Todo truncate colormap to avoid completely transparent part
        ax.scatter(self.data[:, par1_index], self.data[:, par2_index],
                   #c=self.data[:, 0], cmap="Greens_r", marker=".", **kwargs)
                   c=self.data[:, 0], cmap="jet", marker=".", **kwargs)

        index_with_fom_zero = np.where(self.data[:, 0] == 0)
        # index_with_fom_zero = np.where(data[:, 0] > 0.1*best_fom)
        ax.scatter(self.data[index_with_fom_zero, par1_index], self.data[index_with_fom_zero, par2_index],
                   marker="x", color="red", **kwargs)

        if axis_labels:
            ax.set_xlabel(par1)
            ax.set_ylabel(par2)

    def plot_correlation(self, par1, par2, **kwargs):

        fig, ax = plt.subplots(figsize=(8, 6))
        self.plot_correlation_ax(ax=ax, par1=par1, par2=par2, **kwargs)

    def plot_all_correlations(self, figsize=(12,6), type=None, owner=None, category=None, **kwargs):

        list_of_free_parameters = []
        for par in self.parameters:
            if par.limits == "" and par.type != "LosInstrumentParameter":
                continue

            if type is not None and par.type != type:
                continue

            if owner is not None and par.owner != owner:
                continue

            if category is not None and self.category_dict[par.name] != category:
                continue

            list_of_free_parameters.append(par.name)

        n_pars = len(list_of_free_parameters)

        if len(list_of_free_parameters) < 2:
            print("Less than 2 parameters within search terms.")
            return

        fig, axs = plt.subplots(figsize=figsize, nrows=n_pars-1, ncols=n_pars-1)

        if n_pars == 2:
            par1 = list_of_free_parameters[0]
            par2 = list_of_free_parameters[1]
            self.plot_correlation_ax(axs, par1=par1, par2=par2, **kwargs)
            return

        for index1, par1 in enumerate(list_of_free_parameters):
            for index2, par2 in enumerate(list_of_free_parameters):
                used_index1 = index1
                used_index2 = index2 - 1
                if used_index1 == n_pars - 1 or used_index2 < 0:
                    continue

                if index1 >= index2:
                    axs[used_index1, used_index2].set_axis_off()
                else:
                    axis_labels = used_index1 == used_index2
                    # switch x and y axis by having par1=par2 and vice versa for nicer plotting
                    self.plot_correlation_ax(axs[used_index1, used_index2], par1=par2, par2=par1,
                                             axis_labels=axis_labels, **kwargs)
                    
                    if not axis_labels:
                        axs[used_index1, used_index2].set_yticklabels([])
                        axs[used_index1, used_index2].set_xticklabels([])

    def print_parameter_types(self):
        type_dict = {}
        for par in self.parameters:
            type_dict[par.type] = None

        print(list(type_dict.keys()))

    def print_parameter_owners(self):
        owner_dict = {}
        for par in self.parameters:
            owner_dict[par.owner] = None

        print(list(owner_dict.keys()))

    def print_parameter_categories(self):
        category_display = {}
        for par in self.parameters:
            category_display[self.category_dict[par.name]] = None

        print(list(category_display))

    def plot_sim_duration_ax(self, ax, fom_correlation=False):
        """
        Plot simulation duration for each simulation iteration
        """

        if "sim_start_t" not in self.legend or "sim_end_t" not in self.legend:
            print("Timing information not in log file")
            ax.text(0.5, 0.5, "No timing data recorded.", va="center", ha="center")
            return

        start_times = self.data[:, self.legend.index("sim_start_t")]
        end_times = self.data[:, self.legend.index("sim_end_t")]

        durations = end_times - start_times

        if fom_correlation:
            ax.scatter(self.fom, durations, marker=".")
            ax.set_xlabel("FOM")
        else:
            ax.scatter(range(len(self.fom)), durations, marker=".")
            ax.set_xlabel("Optimizer iteration")
        ax.set_ylabel("sim time [s]")

    def plot_all(self):

        self.plot_best_guide()

        fig, axs = plt.subplots(figsize=(15, 20), nrows=4, ncols=2)

        self.plot_1D_fom_ax(axs[0, 0])
        self.plot_1D_cps_ax(axs[1, 0])
        self.plot_1D_cps_ax(axs[1, 1], sorted=True)
        self.plot_1D_given_type_ax(axs[2, 0], type="horizontal", sorted=False)
        self.plot_1D_given_type_ax(axs[2, 1], type="horizontal", sorted=False)
        self.plot_1D_given_type_ax(axs[3, 0], type="vertical", sorted=False)
        self.plot_1D_given_type_ax(axs[3, 1], type="vertical", sorted=False)

    def plot_overview(self):
        """
        Plotting full overview
        """

        fig = plt.figure(figsize=(13, 12), tight_layout=True)
        fig.suptitle(self.scan_name, fontsize=16)
        gs = gridspec.GridSpec(3, 3)

        self.plot_1D_fom_ax(fig.add_subplot(gs[0, 0]))
        self.plot_sim_duration_ax(fig.add_subplot(gs[0, 1]), fom_correlation=False)
        self.plot_1D_cps_ax(fig.add_subplot(gs[0, 2]))

        geometry_h_ax = fig.add_subplot(gs[1, 0:2])
        self.plot_guide_ax(geometry_h_ax, horizontal=True)

        geometry_v_ax = fig.add_subplot(gs[2, 0:2])
        self.plot_guide_ax(geometry_v_ax, horizontal=False)

        par_h_ax = fig.add_subplot(gs[1, 2])
        self.plot_1D_given_type_ax(par_h_ax, type="horizontal")

        par_v_ax = fig.add_subplot(gs[2, 2])
        self.plot_1D_given_type_ax(par_v_ax, type="vertical")


