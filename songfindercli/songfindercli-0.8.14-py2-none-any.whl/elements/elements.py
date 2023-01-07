# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

import os

from future.utils import python_2_unicode_compatible
from songfinder import gestchant
from songfinder import fonctions as fonc
from songfinder import classDiapo
from songfinder import screen
from songfinder import classSettings as settings

try:
	basestring # pylint: disable=used-before-assignment
except NameError: # For python 3 Compatibility
	basestring = str # pylint: disable=redefined-builtin

RECEUILS = ['JEM', 'ASA', 'WOC', 'HER', 'HEG', 'FAP', 'MAR', \
			'CCO', 'PBL', 'LDM', 'JFS', 'THB', 'EHO', 'ALG', \
			'BLF', 'ALR', 'HLS', 'IMP', 'PNK', 'DNL', 'ROG', \
			'WOC', 'SOL', 'FRU', 'OST', 'ENC', 'DIV']

@python_2_unicode_compatible
class Element(object):
	def __init__(self, nom='', etype='empty', chemin=''):
		self.newline = settings.GENSETTINGS.get('Syntax', 'newline')
		self.nom = fonc.enleve_accents(nom)
		self._title = self.nom
		self._supInfo = ''
		self._ref = ''
		if nom:
			self.nom = fonc.upper_first(self.nom)

		self.etype = etype
		self.chemin = chemin
		self._diapos = []
		self._text = None
		self._author = None
		self._copyright = None
		self._ccli = None
		self._customNumber = None
		self._turfNumber = None
		self._hymnNumber = None
		self._tags = []

	def __str__(self):
		out = '%s -- '%(self.etype)
		num = self._turfNumber or self._hymnNumber or self._customNumber
		if self.ref and num:
			out = '%s%s%04d '%(out, self.ref, \
						self._turfNumber or self._hymnNumber or self._customNumber or 0)
		out = '%s%s'%(out, self.title)
		if self.supInfo:
			out = '%s (%s)'%(out, self.supInfo)
		return out

	def __repr__(self):
		return repr(str(self))

	@property
	def text(self):
		return self._text

	@property
	def title(self):
		if self._title == '':
			self.text # pylint: disable=pointless-statement
		return self._title

	@property
	def supInfo(self):
		if self._supInfo is None:
			self.title # pylint: disable=pointless-statement
		return self._supInfo

	@property
	def ref(self):
		if self._ref == '':
			self.text # pylint: disable=pointless-statement
		if self._turfNumber:
			self._ref = 'TURF'
		return self._ref

	@property
	def transpose(self):
		return None

	@property
	def capo(self):
		return None

	@property
	def key(self):
		return ''

	@property
	def nums(self):
		return dict()

	@property
	def turfNumber(self):
		return None

	@property
	def hymnNumber(self):
		return None

	@property
	def customNumber(self):
		return None

	@property
	def author(self):
		return ''

	@property
	def copyright(self):
		return ''

	@property
	def ccli(self):
		return ''

	@property
	def tags(self):
		return ','.join(self._tags)

	@tags.setter
	def tags(self, tags):
		if isinstance(tags, list):
			self._tags = [gestchant.nettoyage(tag) for tag in tags]
		else:
			tags = tags.replace(' et ', ',').replace(' / ', ',').replace(' - ', ',').replace(';', ',')
			def cleaupTag(tag):
				tag = fonc.upper_first(gestchant.nettoyage(tag))
				tag = tag.replace('st-', 'saint').replace('St-', 'Saint')
				return tag
			self._tags = [cleaupTag(tag) for tag in tags.split(',')]
			self._tags.sort()

	@property
	def diapos(self):
		if self._diapos != []:
			return self._diapos
		# ~ self._diapos = []

		text = '%s\n'%self.text
		text = fonc.supressB(text, '\\ac', '\n')
		text = text.strip('\n')
		ratio = screen.getRatio(settings.GENSETTINGS.get('Parameters', 'ratio'))
		max_car = int(settings.PRESSETTINGS.get('Presentation_Parameters', 'size_line')*ratio)

		listStype = []
		# La première est vide ie au dessus du premier \s
		linePerSlide = settings.PRESSETTINGS.get('Presentation_Parameters', 'line_per_diapo')
		listText, listStype = fonc.splitPerso([text], \
								settings.GENSETTINGS.get('Syntax', 'newslide'), \
								listStype, 0)
		del listText[0]
		listStypePlus = gestchant.getListStypePlus(listStype)
		# Completion des diapo vide
		diapoVide = [i for i, text in enumerate(listText) if text.find('\\...') != -1 \
								or gestchant.nettoyage(text) == '']

		plus = 0
		for index in diapoVide:
			listCandidat = gestchant.getIndexes(listStype[:index], listStype[index])
			if listCandidat != []:
				# Si plus de diapos que disponibles sont demande,
				# cela veut dire qu'il faut dupliquer plusieurs fois les diapos
				if not gestchant.getPlusNum(listStypePlus, index) > len(listCandidat):
					plus = 0
				elif plus == 0:
					plus = gestchant.getPlusNum(listStypePlus, index) - len(listCandidat)
				toTake = -gestchant.getPlusNum(listStypePlus, index)+plus
				indexCopie = listCandidat[toTake]
				if listText[index].find('\\...') != -1:
					listText[index] = listText[index].replace('\\...', listText[indexCopie])
				else:
					listText[index] = listText[indexCopie]

		linePerSlide = settings.PRESSETTINGS.get('Presentation_Parameters', 'line_per_diapo')
		listText, listStype = gestchant.applyMaxNumberLinePerDiapo(listText, listStype, linePerSlide)

		nombre = len(listText)
		for i, text in enumerate(listText):
			diapo = classDiapo.Diapo(self, i+1, listStype[i], \
										max_car, nombre, text)
			self._diapos.append(diapo)
		return self._diapos

	def resetDiapos(self):
		del self._diapos[:]

	@title.setter
	def title(self, newTitle):
		self._supInfo = ''
		if newTitle:
			if newTitle[:3] in ['JEM', 'SUP'] and newTitle[3:6].isdigit():
				newTitle = newTitle[7:]
			newTitle = newTitle.replace('\n', '')
			newTitle = newTitle.strip(' ')

			deb = self.nom.find('(')
			fin = self.nom.find(')')
			if deb != -1 and fin != -1:
				self._supInfo = self.nom[deb+1:fin]

			deb = newTitle.find('(')
			fin = newTitle.find(')')
			if deb != -1 and fin != -1:
				newTitle = newTitle[:deb] + newTitle[fin+1:]

		else:
			newTitle = ''
			self._supInfo = ''
		self._title = fonc.safeUnicode(newTitle)
		self._latexText = ''
		self._beamerText = ''
		self._markdownText = ''

	def exist(self):
		return os.path.isfile(self.chemin) and self.text

	def save(self):
		pass

	def safeUpdateXML(self, xmlRoot, field, value):
		if isinstance(value, (int, float)):
			value = str(value).encode("utf-8").decode("utf-8")
		if value is not None:
			try:
				xmlRoot.find(field).text = fonc.safeUnicode(value)
			except AttributeError:
				import lxml.etree as ET_write
				ET_write.SubElement(xmlRoot, field)
				xmlRoot.find(field).text = fonc.safeUnicode(value)
