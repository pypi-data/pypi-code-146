import matplotlib.pyplot as plt

import ipywidgets as widgets
from IPython.display import display
from itertools import cycle

from guide_bot.scan_visualization.base_jb_interface import HiddenPrints
from guide_bot.scan_visualization.base_jb_interface import BaseInterface


class CompareSources(BaseInterface):
    def __init__(self, scan_overview):
        super().__init__(scan_overview)

        self.fig = None
        self.ax = None

        self.show_interface()

        self.dropdown_monitor = None
        self.dropdown_run_name = None

        self.source_enable = {}
        for source in self.get_moderator_list():
            self.source_enable[source] = True

        self.target_scan_labels = None
        self.moderator_scan_labels = None

    def get_monitor_list(self):
        # Overwrite get_monitor_list to only allow 1D monitors
        shape = self.scan_overview.get_shape()
        indicies = tuple(self.list_indicies)
        guide = self.guides_with_at_least_one_run[0]
        moderator = self.get_moderator_list()[0]

        runs = self.scan_overview.data[guide][indicies][moderator].runs

        return runs[self.run_name].get_1D_monitor_list()

    def make_source_checkboxes(self):
        source_checkboxes = []
        for source in self.get_moderator_list():
            widget = widgets.Checkbox(value=True, description=source, disabled=False, indent=True)
            source_checkboxes.append(widget)

        for checkbox in source_checkboxes:
            checkbox.observe(self.update_source_selection, "value")

        return source_checkboxes

    def update_source_selection(self, change):
        if change.new:
            self.enable_source(change["owner"].description)
        else:
            self.disable_source(change["owner"].description)
        self.update_plot()

    def enable_source(self, source):
        self.source_enable[source] = True

    def disable_source(self, source):
        self.source_enable[source] = False

    def enabled_sources(self):
        enabled_sources = []
        for source in self.source_enable:
            if self.source_enable[source]:
                enabled_sources.append(source)
        return enabled_sources

    def get_plot_data(self):

        indices = tuple(self.list_indicies)
        run_name = self.run_name
        monitor = self.monitor

        plot_data = {}

        for guide in self.enabled_guides():
            plot_data[guide] = {}
            for moderator in self.enabled_sources():
                if self.scan_overview.data[guide][indices][moderator] is not None:
                    if run_name in self.scan_overview.data[guide][indices][moderator].runs:
                        try:
                            data = self.scan_overview.data[guide][indices][moderator]
                            plot_data[guide][moderator] = data.runs[run_name].get_data(monitor)
                        except NameError:
                            pass

        return plot_data

    def new_plot(self):

        self.fig, self.ax = plt.subplots()

        self.update_plot()

    def update_plot(self):

        plot_data = self.get_plot_data()

        line_style_cycle = cycle(["solid", "dotted", "dashed", "dashdot"])

        self.ax.cla()
        for guide_label in plot_data:
            line_style = next(line_style_cycle)
            # Reset color cycle to have same color for each source
            line_color_cycle = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])
            for source_label in plot_data[guide_label]:
                line_color = next(line_color_cycle)

                data = plot_data[guide_label][source_label]

                if data is None:
                    continue

                xaxis = data.xaxis
                intensity = data.Intensity

                self.ax.plot(xaxis, intensity,
                             ls=line_style, color=line_color,
                             label=guide_label + " - " + source_label)

                self.ax.set_xlabel(data.metadata.xlabel)
                self.ax.set_ylabel(data.metadata.ylabel)

                self.ax.legend()

        self.ax.grid(True)

    def show_interface(self):
        output = widgets.Output()

        # default line color
        initial_color = '#FF00DD'

        with output:
            # fig, ax = plt.subplots(constrained_layout=True, figsize=(6, 4))
            self.new_plot()

        # move the toolbar to the bottom
        self.fig.canvas.toolbar_position = 'bottom'
        self.ax.grid(True)

        control_widgets = []
        # Place control widgets
        control_widgets += [widgets.Label(value="Data source")]

        self.dropdown_monitor = self.make_dropdown_monitor()
        control_widgets.append(self.dropdown_monitor)

        self.dropdown_run_name = self.make_dropdown_run_name()
        control_widgets.append(self.dropdown_run_name)

        #self.dropdown_moderator = self.make_dropdown_moderator()
        #control_widgets.append(self.dropdown_moderator)

        if len(self.get_scanned_target_parameters()) > 0:
            control_widgets += [widgets.Label(value="Scanned target parameters")]
            control_widgets += self.make_target_scan_sliders()

        if len(self.get_scanned_moderator_parameters()) > 0:
            control_widgets += [widgets.Label(value="Scanned moderator parameters")]
            control_widgets += self.make_moderator_scan_sliders()

        control_widgets += [widgets.Label(value="Guide selection")]

        guide_checkboxes = self.make_guide_checkboxes()
        control_widgets += guide_checkboxes

        control_widgets += [widgets.Label(value="Moderator selection")]

        source_checkboxes = self.make_source_checkboxes()
        control_widgets += source_checkboxes

        controls = widgets.VBox(control_widgets)
        return widgets.HBox([controls, output])
