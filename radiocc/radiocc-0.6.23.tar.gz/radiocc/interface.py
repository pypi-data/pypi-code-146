#!/usr/bin/env python3

"""
Radio occultation user interface
"""

import gi

if gi.require_version("Gtk", "3.0"):
    pass

from typing import Optional  # noqa:F401

from gi.repository import Gtk
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure
from pudb import set_trace as bp  # noqa:F401

import radiocc

SWITCH_STATES = ("Linear", "Quadratic")


class Interface:
    """User interface data structure."""

    def __init__(self) -> None:
        # Embed in GTK3 with Glade.
        self.builder = Gtk.Builder()
        self.builder.add_from_file(
            str(radiocc.ASSETS_PATH / "interface" / "interface.glade")
        )
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window-main")
        self.scrolled_window_matplotlib = self.builder.get_object(
            "scrolled-window-matplotlib"
        )
        self.scrolled_window_navigation = self.builder.get_object("navigation")
        self.label_data = self.builder.get_object("label-data-process")
        self.switch_order = self.builder.get_object("switch-order")
        self.label_switch = self.builder.get_object("label-switch")

        self.__altitude = radiocc.constants.Threshold_Cor
        self.box_altitude = self.builder.get_object("box-altitude")
        self.entry_altitude = self.builder.get_object("entry-altitude")
        self.label_current_altitude = self.builder.get_object("label-current-altitude")
        self.set_altitude(self.__altitude)

        self.box_refractivity = self.builder.get_object("box-refractivity")

        self.__intercept = 0.0
        self.label_current_intercept = self.builder.get_object(
            "label-current-intercept"
        )
        self.entry_intercept = self.builder.get_object("entry-intercept")

        self.__slope = 0.0
        self.label_current_slope = self.builder.get_object("label-current-slope")
        self.entry_slope = self.builder.get_object("entry-slope")

        self.__quadratic = 0.0
        self.label_current_quadratic = self.builder.get_object(
            "label-current-quadratic"
        )
        self.entry_quadratic = self.builder.get_object("entry-quadratic")

        self.button_next = self.builder.get_object("button-next")

        self.WIDTH = self.window.get_property("default-width")
        self.HEIGHT = self.window.get_property("default-height")

        statusIcon = Gtk.StatusIcon()
        statusIcon.set_visible(True)

        # Create figure
        self.figure = Figure(figsize=(1, 1))
        self.figure.subplots_adjust(bottom=0.15)

        # Add a canvas to the scrolled window.
        self.BORDER_WIDTH_ADDITIONAL = 200.0
        self.TOOLBAR_HEIGHT = 46.0
        self.BORDER_WIDTH = self.BORDER_WIDTH_ADDITIONAL + self.TOOLBAR_HEIGHT
        self.CANVAS_WIDTH = self.WIDTH - self.BORDER_WIDTH
        self.CANVAS_HEIGHT = self.CANVAS_WIDTH * 3.0 / 4.0
        self.canvas = FigureCanvas(self.figure)
        self.canvas.set_size_request(self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        self.scrolled_window_matplotlib.add_with_viewport(self.canvas)

        # Add a toolbar.
        self.toolbar = NavigationToolbar(self.canvas, self.window)
        self.scrolled_window_navigation.add(self.toolbar)

        # Init switch label.
        self.label_switch.set_label(SWITCH_STATES[self.switch_order.get_active()])
        # Interface.go_next is True after clicking on Next/Finish button.
        # It is used to go to next graph.
        self.go_next = False

        # Draw.
        self.window.show_all()
        self.box_refractivity.hide()
        self.draw()

    def on_switch_activated(self, switch: Gtk.Switch, gparam: bool) -> None:
        """Called when the switch button linear/quadratic is activated."""
        self.label_switch.set_label(SWITCH_STATES[gparam])

    def format_value_intercept(self, scale: Gtk.Scale, value: float) -> str:
        """Custom format of the displayed label next to the scale intercept."""
        return f"Intercept: {value:f}"

    def on_value_changed_intercept(self, scale: Gtk.Scale) -> None:
        """Called when the scale intercept is updated."""

    def format_value_slope(self, scale: Gtk.Scale, value: float) -> str:
        """Custom format of the displayed label next to the scale slope."""
        return f"Slope: {value:f}"

    def on_value_changed_slope(self, scale: Gtk.Scale) -> None:
        """Called when the scale slope is updated."""

    def format_value_quadratic(self, scale: Gtk.Scale, value: float) -> str:
        """Custom format of the displayed label next to the scale quadratic."""
        return f"Quadratic: {value:f}"

    def on_value_changed_quadratic(self, scale: Gtk.Scale) -> None:
        """Called when the scale quadratic is updated."""

    def on_clicked_next(self, event: MouseEvent) -> None:
        """Called when the button next/finish is clicked."""
        self.canvas.stop_event_loop()
        self.go_next = True

    def on_clicked_compute(self, event: MouseEvent) -> None:
        """Called when the button next/finish is clicked."""
        self.canvas.stop_event_loop()

    def on_entry_altitude_activated(self, entry: Gtk.Entry) -> None:
        """Altitude setter."""
        altitude = self.get_altitude()
        self.set_altitude(altitude)

    def on_entry_intercept_activated(self, entry: Gtk.Entry) -> None:
        """Intercept setter."""
        intercept = self.get_intercept()
        self.set_intercept(intercept)

    def on_entry_slope_activated(self, entry: Gtk.Entry) -> None:
        """Slope setter."""
        slope = self.get_slope()
        self.set_slope(slope)

    def on_entry_quadratic_activated(self, entry: Gtk.Entry) -> None:
        """Quadratic setter."""
        quadratic = self.get_quadratic()
        self.set_quadratic(quadratic)

    def get_altitude(self) -> float:
        """Altitude getter."""
        altitude_str = self.entry_altitude.get_text()
        try:
            altitude = float(altitude_str)
        except ValueError:
            return self.__altitude
        else:
            return altitude

    def get_intercept(self) -> float:
        """Intercept getter."""
        intercept_str = self.entry_intercept.get_text()
        try:
            intercept = float(intercept_str)
        except ValueError:
            return self.__intercept
        else:
            return intercept

    def get_slope(self) -> float:
        """Slope getter."""
        slope_str = self.entry_slope.get_text()
        try:
            slope = float(slope_str)
        except ValueError:
            return self.__slope
        else:
            return slope

    def get_quadratic(self) -> float:
        """Quadratic getter."""
        quadratic_str = self.entry_quadratic.get_text()
        try:
            quadratic = float(quadratic_str)
        except ValueError:
            return self.__quadratic
        else:
            return quadratic

    def set_altitude(self, altitude: float) -> None:
        """Altitude setter."""
        self.__altitude = altitude
        self.label_current_altitude.set_label(f"Current altitude: {altitude:.5e}")

    def set_intercept(self, intercept: float) -> None:
        """Intercept setter."""
        self.__intercept = intercept
        self.label_current_intercept.set_label(f"Current intercept: {intercept:.5e}")

    def set_slope(self, slope: float) -> None:
        """Slope setter."""
        self.__slope = slope
        self.label_current_slope.set_label(f"Current slope: {slope:.5e}")

    def set_quadratic(self, quadratic: float) -> None:
        """Quadratic setter."""
        self.__quadratic = quadratic
        self.label_current_quadratic.set_label(f"Current quadratic: {quadratic:.5e}")

    def on_window_destroy(self, widget: Gtk.Window) -> None:
        """Called when the window is destroyed."""
        Gtk.main_quit()

    def draw(self) -> None:
        """Briefly toggle on/off the interactive to draw the window."""
        self.figure.canvas.draw()
        self.canvas.start_event_loop(timeout=0.01)

    def interactive(self) -> None:
        """Turn the window interactive until it is stopped."""
        self.canvas.start_event_loop()

    def mainloop(self) -> None:
        """GTK mainloop."""
        Gtk.main()
