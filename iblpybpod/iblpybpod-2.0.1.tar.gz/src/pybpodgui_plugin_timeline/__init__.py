# !/usr/bin/python3
# -*- coding: utf-8 -*-

__version__ = "1.0.1"
__author__ = "Carlos Mão de Ferro"
__credits__ = ["Carlos Mão de Ferro", "Ricardo Ribeiro"]
__license__ = "Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>"
__maintainer__ = ["Carlos Mão de Ferro", "Ricardo Ribeiro"]
__email__ = ["cajomferro@gmail.com", "ricardojvr@gmail.com"]
__status__ = "Development"

import loggingbootstrap
from confapp import conf

conf += 'pybpodgui_plugin_timeline.settings'
conf += 'pybpodgui_plugin_timeline.resources'

# setup different loggers but output to single file
loggingbootstrap.create_double_logger("pybpodgui_plugin_timeline", conf.APP_LOG_HANDLER_CONSOLE_LEVEL,
                                      conf.APP_LOG_FILENAME,
                                      conf.APP_LOG_HANDLER_FILE_LEVEL)

from pybpodgui_plugin_timeline.trials_plot_window import TrialsPlotWindow as TrialsPlot
