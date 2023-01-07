# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

import os
import xml.etree.cElementTree as ET

from songfinder import gestchant
from songfinder import classPaths
from songfinder import fonctions as fonc
from songfinder import exception
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

class Passage(Element):
	def __init__(self, version, livre, chap1, chap2, vers1, vers2):
		Element.__init__(self)
		self.etype = 'verse'
		self.version = version
		self.chemin = os.path.join(classPaths.PATHS.bibles, version \
						+ settings.GENSETTINGS.get('Extentions', 'bible')[0])

		self.livre = livre
		self.chap1 = chap1
		self.chap2 = chap2
		self.vers1 = vers1
		self.vers2 = vers2

		self._title = None
		self._text = None
		self.__bible = None

	def _parse(self):
		if not self.__bible:
			try:
				tree_bible = ET.parse(self.chemin)
			except (OSError, IOError):
				raise exception.DataReadError(self.chemin)
			self.__bible = tree_bible.getroot()

	@property
	def text(self):
		if self._text is None:
			self._parse()
			newslide = settings.GENSETTINGS.get('Syntax', 'newslide')
			text = ''
			if self.chap1==self.chap2:
				for i,passage in enumerate(self.__bible[self.livre][self.chap1][self.vers1:self.vers2+1]):
					text = '%s%s\n%d  %s\n'%(text, newslide[0], self.vers1+i+1, passage.text)
			else:
				text =  '%sChapitre %d\n'%(text, self.chap1+1)
				for i,passage in enumerate(self.__bible[self.livre][self.chap1][self.vers1:]):
					text = '%s%s\n%d %s\n'%(text, newslide[0], self.vers1+i+1, passage.text)
				text =  '%sChapitre %d\n'%(text, self.chap2+1)
				for i,passage in enumerate(self.__bible[self.livre][self.chap2][:self.vers2+1]):
					text = '%s%s\n%d %s\n'%(text, newslide[0], i+1, passage.text)
			self.text = text
			self.title # pylint: disable=pointless-statement
			self.__bible = None
		return self._text

	@text.setter
	def text(self, value):
		self._text = gestchant.nettoyage(value)

	@property
	def title(self):
		if not self._title:
			self._parse()
			title = ''
			if self.livre != -1:
				title += self.__bible[self.livre].attrib['n']\
				+ ' ' + self.__bible[self.livre][self.chap1].attrib['n']

			title += 'v' + self.__bible[self.livre][self.chap1][self.vers1].attrib['n'] + '-'
			if self.chap1!=self.chap2:
				title += self.__bible[self.livre][self.chap2].attrib['n'] + 'v'

			title += self.__bible[self.livre][self.chap1][self.vers2].attrib['n']
			self._title = fonc.enleve_accents(title)
			self.nom = self._title

			self.text # pylint: disable=pointless-statement
			self.__bible = None
		return self._title
