# -*- coding: utf-8 -*-

import os
import importlib
import logging
from distutils.sysconfig import get_config_var

from songfinder import __appName__, __arch__

def load(fullFileName, py2c=False):
	fileName_in = os.path.splitext( os.path.split(fullFileName)[1] )[0]
	fileNames = [fileName_in]
	if py2c:
		fileNames.insert(0, 'c'+fileName_in[2:])
	try:
		targetInfo = os.path.splitext(get_config_var('EXT_SUFFIX'))[0]
	except AttributeError:
		targetInfo = None

	imported = False
	for fileName in fileNames:
		libName = str('%s.lib.%s'%(__appName__, fileName))
		if not targetInfo:
			libName = str('%s_%s'%(libName, __arch__))
		try:
			module = importlib.import_module(libName)
		except (ImportError, NameError):
			pass
		else:
			imported = True
			logging.debug("Using compiled version %s module"%fileName)
			return module

	if not imported:
		raise ImportError

	return None
