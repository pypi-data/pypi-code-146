# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

import os

from songfinder import fonctions as fonc
from songfinder import classSettings as settings
from songfinder.elements import Element

try:
	basestring # pylint: disable=used-before-assignment
except NameError: # For python 3 Compatibility
	basestring = str # pylint: disable=redefined-builtin

RECEUILS = ['JEM', 'ASA', 'WOC', 'HER', 'HEG', 'FAP', 'MAR', \
			'CCO', 'PBL', 'LDM', 'JFS', 'THB', 'EHO', 'ALG', \
			'BLF', 'ALR', 'HLS', 'IMP', 'PNK', 'DNL', 'ROG', \
			'WOC', 'SOL', 'FRU', 'OST', 'ENC', 'DIV']

class ImageObj(Element):
	def __init__(self, chemin):
		self.etype = 'image'
		self._extention = fonc.get_ext(chemin)
		if self._extention == '':
			for ext in settings.GENSETTINGS.get('Extentions', 'image'):
				if os.path.isfile(chemin + ext):
					self._extention = ext
					chemin = chemin + ext
					break
		Element.__init__(self, nom=fonc.get_file_name(chemin), etype=self.etype, chemin=chemin)

	@property
	def extention(self):
		return self._extention

	@property
	def text(self):
		return settings.GENSETTINGS.get('Syntax', 'newslide')[0]

	def exist(self):
		return os.path.isfile(self.chemin)
