# !/usr/bin/python3
# -*- coding: utf-8 -*-
import loggingbootstrap

from confapp import conf

__version__ = "1.8.2"
__author__ = "Carlos Mao de Ferro"
__credits__ = ["Carlos Mao de Ferro", "Ricardo Ribeiro", "Sérgio Copeto", 'Luís Teixeira']
__license__ = "MIT"
__maintainer__ = ["Carlos Mao de Ferro", "Ricardo Ribeiro", "Sérgio Copeto", 'Luís Teixeira']
__email__ = ["cajomferro@gmail.com", "ricardojvr@gmail.com", "sergio.copeto@research.fchampalimaud.org", 'micboucinha@gmail.com']
__status__ = "Development"

conf += 'pybpodgui_plugin.settings'
conf += 'pybpodgui_plugin.resources'

# setup different loggers but output to single file
loggingbootstrap.create_double_logger("pybpodgui_plugin", conf.APP_LOG_HANDLER_CONSOLE_LEVEL,
                                      conf.APP_LOG_FILENAME,
                                      conf.APP_LOG_HANDLER_FILE_LEVEL)

loggingbootstrap.create_double_logger("pybranch", conf.APP_LOG_HANDLER_CONSOLE_LEVEL,
                                      conf.APP_LOG_FILENAME,
                                      conf.APP_LOG_HANDLER_FILE_LEVEL)

loggingbootstrap.create_double_logger("pybpodapi", conf.APP_LOG_HANDLER_CONSOLE_LEVEL,
                                      conf.APP_LOG_FILENAME,
                                      conf.APP_LOG_HANDLER_FILE_LEVEL)

if conf.USE_MULTIPROCESSING:
    # https://docs.python.org/3.5/library/multiprocessing.html#multiprocessing.freeze_support
    from multiprocessing import freeze_support  # @UnresolvedImport
    freeze_support()
