__version__ = '0.1.5'

from pybpod_gui_plugin_emulator.emulator_gui import EmulatorGUI

from confapp import conf

conf += 'pybpod_gui_plugin_emulator.settings'
conf += 'pybpod_gui_plugin_emulator.resources'
