#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = "1.5.1"
__author__ = "Carlos Mao de Ferro, Ricardo Ribeiro, Luís Teixeira"
__credits__ = ["Carlos Mao de Ferro", "Ricardo Ribeiro", 'Luís Teixeira']
__license__ = "Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>"
__maintainer__ = ["Carlos Mao de Ferro", "Ricardo Ribeiro", 'Luís Teixeira']
__email__ = ["cajomferro@gmail.com", "ricardojvr@gmail.com", 'micboucinha@gmail.com']
__status__ = "Development"

import logging

from confapp import conf

logger = logging.getLogger(__name__)

conf += 'pyforms_generic_editor.settings'

# # load the user settings in case the file exists
# try:
# 	import pyforms_generic_editor_user_settings
#
# 	conf += pyforms_generic_editor_user_settings
# except Exception as err:
# 	logger.debug('No user_settings available', exc_info=True)
