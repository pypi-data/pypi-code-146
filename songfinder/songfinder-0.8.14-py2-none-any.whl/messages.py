# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import traceback
import logging
try:
	from tkinter import messagebox as tkMessageBox
except ImportError:
	import tkMessageBox
try:
	from tkinter import filedialog as tkFileDialog
except ImportError:
	import tkFileDialog
import _tkinter

import songfinder

# python 2/3 compatibility
try:
	input = raw_input # pylint: disable=redefined-builtin
except NameError:
	pass

def showerror(title, message, **kwargs):
	if songfinder.__unittest__ is True:
		logging.warning(message)
	else:
		logging.error('Error %s: %s'%(title, message))
		logging.error('%s'%traceback.format_exc())
		try:
			tkMessageBox.showerror(title, message, **kwargs)
		except _tkinter.TclError:
			pass

def showinfo(title, message, **kwargs):
	if songfinder.__unittest__ is True:
		logging.warning(message)
	else:
		logging.info('Info %s: %s'%(title, message))
		try:
			tkMessageBox.showinfo(title, message, **kwargs)
		except _tkinter.TclError:
			pass

def askyesno(title, message, **kwargs):
	if songfinder.__unittest__ is True:
		logging.warning(message)
		return False
	else:
		try:
			return tkMessageBox.askyesno(title, message)
		except _tkinter.TclError:
			print('Askyesno %s: %s'%(title, message))
			answer = None
			while answer not in ['y', 'Y', 'n', 'N']:
				answer = input(message + ' (y/n)')
				if answer in ['y', 'Y']:
					return True
				elif answer in ['n', 'N']:
					return False

def askdirectory(**kwargs):
	if songfinder.__unittest__ is True:
		logging.warning('askdirectory')
		return None
	else:
		try:
			return tkFileDialog.askdirectory(**kwargs)
		except _tkinter.TclError:
			return None

def askopenfilename(**kwargs):
	if songfinder.__unittest__ is True:
		logging.warning('askopenfilename')
		return None
	else:
		try:
			return tkFileDialog.askopenfilename(**kwargs)
		except _tkinter.TclError:
			return None

def askopenfilenames(**kwargs):
	if songfinder.__unittest__ is True:
		logging.warning('askopenfilenames')
		return None
	else:
		try:
			return tkFileDialog.askopenfilenames(**kwargs)
		except _tkinter.TclError:
			return None

def asksaveasfilename(**kwargs):
	if songfinder.__unittest__ is True:
		logging.warning('asksaveasfilename')
		return None
	else:
		try:
			return tkFileDialog.asksaveasfilename(**kwargs)
		except _tkinter.TclError:
			return None
