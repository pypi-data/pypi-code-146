# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import codecs
import errno
import sys
import platform
import logging
import datetime
from songfinder import logger_formatter

__version__ = "0.8.15"
__author__ = "danbei"
__appName__ = "songfinder"

# Define root diretcory
__chemin_root__ = os.getcwd()

# Define data directory
__dataPath__ = os.path.join(os.path.split(__file__)[0], 'data')

def _isPortable():
	# Check if installation is portable
	isPortable = os.path.isfile( os.path.join(__chemin_root__, 'PORTABLE') )
	try:
		with codecs.open( os.path.join(__chemin_root__, 'test.test') ,"w", encoding='utf-8'):
			pass
		os.remove( os.path.join(__chemin_root__, 'test.test') )
	except (OSError, IOError) as error:
		if error.errno == errno.EACCES:
			isPortable = False
		else:
			raise
	return isPortable

__portable__ = _isPortable()

# Define Settings directory
if __portable__:
	__settingsPath__ = os.path.join(__chemin_root__, '.' + __appName__, '')
else:
	__settingsPath__ = os.path.join(os.path.expanduser("~"), '.' + __appName__, '')

def _loggerConfiguration():
	# Set logger configuration
	logFormatter = logger_formatter.MyFormatter()
	consoleHandler = logging.StreamHandler(sys.stdout)
	logDirectory = os.path.join(__settingsPath__, 'logs')
	logFile = os.path.join(logDirectory, \
			'%s.log'%datetime.datetime.now().strftime("%Y-%m-%d-%Hh%Mm%Ss"))
	try:
		os.makedirs(logDirectory)
	except (OSError, IOError) as error:
		if error.errno == errno.EEXIST:
			pass
		else:
			raise
	fileHandler = logging.FileHandler(logFile)
	consoleHandler.setFormatter(logFormatter)
	fileHandler.setFormatter(logFormatter)
	logging.root.addHandler(consoleHandler)
	logging.root.addHandler(fileHandler)

	logging.root.setLevel(logging.DEBUG)
	fileHandler.setLevel(logging.DEBUG)
	return consoleHandler

__consoleHandler__ = _loggerConfiguration()

def _getOs():
	system = platform.system()
	if system == 'Linux':
		platformInfo = platform.platform().split('-')
		if platformInfo[0] == 'Ubuntu':
			outOs = 'ubuntu'
		else:
			outOs = 'linux'
	elif system == 'Windows':
		outOs = 'windows'
	elif system == 'Darwin':
		outOs = 'darwin'
	else:
		outOs = 'notSupported'
		logging.info('Your `%s` isn\'t a supported operatin system`.' \
				% system)
	return outOs

__myOs__ = _getOs()

if sys.maxsize == 9223372036854775807:
	__arch__ = 'x64'
else:
	__arch__ = 'x86'
__dependances__ = 'deps-%s'%__arch__
__unittest__ = False


def _gui(fenetre, fileIn=None):
	# Creat main window and splash icon
	import traceback
	from songfinder import guiHelper
	from songfinder import screen
	from songfinder import splash

	screens = screen.Screens()
	with guiHelper.SmoothWindowCreation(fenetre, screens):
		screens.update(referenceWidget=fenetre)

		with splash.Splash(fenetre, os.path.join(__dataPath__, 'icon.png'), screens):
			# Compile cython file and cmodules
			if not __portable__:
				try:
					import subprocess
					python = sys.executable
					if python:
						command = [python, os.path.join(os.path.split(__file__)[0], 'setup_cython.py'), 'build_ext', '--inplace']
						proc = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
						out, err = proc.communicate()
						try:
							logging.debug(out.decode())
							logging.debug(err.decode())
						except UnicodeDecodeError:
							logging.debug(out)
							logging.debug(err)
				except Exception: # pylint: disable=broad-except
					logging.warning(traceback.format_exc())

			from PIL import ImageTk
			from songfinder import interface

			# Set bar icon
			try:
				if os.name == 'posix':
					img = ImageTk.PhotoImage(file = os.path.join(__dataPath__, 'icon.png') )
					fenetre.tk.call('wm', 'iconphoto', fenetre._w, img) # pylint: disable=protected-access
				else:
					fenetre.iconbitmap( os.path.join(__dataPath__, 'icon.ico'))
			except Exception: # pylint: disable=broad-except
				logging.warning(traceback.format_exc())
			if fileIn :
				fileIn = fileIn[0]
			songFinder = interface.Interface(fenetre, screens=screens, fileIn=fileIn)
			fenetre.title('SongFinder')
			fenetre.protocol("WM_DELETE_WINDOW", songFinder.quit)

	songFinder.__syncPath__() # TODO This is a hack
	fenetre.mainloop()

def _webServer():
	from songfinder import webServer
	print('This feature is currently in development, there is actualy nothing realy interessting happening')
	server = webServer.FlaskServer()
	server.run()

def _song2markdown(fileIn, fileOut):
	from songfinder import fileConverter
	converter = fileConverter.Converter()
	converter.makeSubDirOn()
	converter.markdown(fileIn, fileOut)

def _song2latex(fileIn, fileOut):
	from songfinder import fileConverter
	converter = fileConverter.Converter()
	converter.makeSubDirOn()
	converter.latex(fileIn, fileOut)

def _song2html(fileIn, fileOut):
	from songfinder import fileConverter
	converter = fileConverter.Converter()
	converter.makeSubDirOn()
	converter.html(fileIn, fileOut)

def _scanCDL():
	from songfinder import dataBase
	localData = dataBase.DataBase()
	localData.scanCDL()

def _parseArgs():
	import argparse
	arg_parser = argparse.ArgumentParser()
	arg_parser = argparse.ArgumentParser(description="%s v%s"% (__appName__, __version__),
									formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	arg_parser.add_argument("-f", "--file",
						nargs=1,
						metavar=('inputFile',),
						help="Song file or set file to open")

	arg_parser.add_argument("-m", "--songtomarkdown",
						nargs=2,
						metavar=('song[File/Dir]', 'markdown[File/Dir]'),
						help="Convert song file (xml or chordpro) files to markdown file")

	arg_parser.add_argument("-L", "--songtolatex",
						nargs=2,
						metavar=('song[File/Dir]', 'latex[File/Dir]'),
						help="Convert song file (xml or chordpro) files to latex file")

	arg_parser.add_argument("-t", "--songtohtml",
						nargs=2,
						metavar=('song[File/Dir]', 'html[File/Dir]'),
						help="Convert song file (xml or chordpro) files to html file")

	arg_parser.add_argument("-cdl", "--conducteurdelouange",
						action="store_true",
						default=False,
						help="Scan Conducteur De Louange for songs")

	arg_parser.add_argument("-w", "--webserver",
						action="store_true",
						default=False,
						help="Launch songfinder webserver")

	arg_parser.add_argument("--version",
						action="store_true",
						default=False,
						help="Print songfinder version")

	levelChoices= [logging.getLevelName(x)
		for x in range(1, 101)
		if not logging.getLevelName(x).startswith('Level')]

	arg_parser.add_argument("-l", "--loglevel",
						choices=levelChoices,
						default="INFO",
						help="Increase output verbosity")

	return arg_parser.parse_args()

def songFinderMain():
	logging.info('%s v%s'%(__appName__, __version__))
	platformInfos = [\
				platform.node(),\
				platform.python_implementation(),\
				platform.python_version(),\
				platform.python_compiler(),\
				platform.platform(),\
				platform.processor(),\
				]
	logging.info(', '.join(platformInfos))

	logging.info('Settings are in "%s"'%__settingsPath__)
	logging.info('Datas are in "%s"'%__dataPath__)
	logging.info('Root dir is "%s"'%__chemin_root__)
	if __portable__:
		logging.info('Portable version')
	else:
		logging.info('Installed version')

	args = _parseArgs()
	numeric_level = logging.getLevelName(args.loglevel)
	__consoleHandler__.setLevel(numeric_level)
	if args.webserver:
		_webServer()
	elif args.songtomarkdown:
		_song2markdown(*args.songtomarkdown)
	elif args.songtolatex:
		_song2latex(*args.songtolatex)
	elif args.songtohtml:
		_song2html(*args.songtohtml)
	elif args.conducteurdelouange:
		_scanCDL()
	elif args.version:
		print('%s v.%s by %s'%(__appName__, __version__, __author__))
	else:
		try:
			import tkinter as tk
		except ImportError:
			import Tkinter as tk
		fenetre = tk.Tk()
		dpi_value = fenetre.winfo_fpixels('1i')
		logging.info("Screen DPI: %d"%dpi_value)
		fenetre.tk.call('tk', 'scaling', '-displayof', '.', dpi_value / 72.0)
		try:
			_gui(fenetre, fileIn=args.file)
		except SystemExit:
			raise
		except:
			import traceback
			if not getattr(sys, "frozen", False):
				from songfinder import messages as tkMessageBox
				tkMessageBox.showerror('Erreur', traceback.format_exc(limit=1))
			logging.critical(traceback.format_exc())
			raise

if __name__ == '__main__':
	songFinderMain()
