# -*- coding: utf-8 -*-
#cython: language_level=2
from __future__ import unicode_literals

import xml.etree.cElementTree as ET
import datetime
import os
import errno
import traceback
import logging

from future.utils import python_2_unicode_compatible
from songfinder import elements
from songfinder import fonctions as fonc
from songfinder import classPaths
from songfinder import classSettings as settings

@python_2_unicode_compatible
class Set(object):
	def __init__(self):
		self._paths = classPaths.PATHS
		self._listElem = []
		self._generateName()
		self._changed = False

	def __eq__(self, other):
		for i, item in enumerate(self._listElem):
			if item != other[i]:
				return False
		return True

	def __len__(self):
		return len(self._listElem)

	def __setitem__(self, key, value):
		self._listElem[key] = value
		self._changed = True

	def __getitem__(self, index):
		return self._listElem[index]

	def __delitem__(self, index):
		del self._listElem[index]
		self._changed = True

	def __contains__(self, element):
		return element in self._listElem

	def __str__(self):
		return self._name

	def _generateName(self):
		nextSunday = datetime.timedelta(days = 6-datetime.datetime.today().weekday())
		self._name = str(datetime.date.today()+ nextSunday)
		while os.path.isfile(self._paths.sets + self._name):
			if len(self._name) == 10:
				self._name = self._name + '_1'
			else:
				self._name = self._name[:11] + str(int(self._name[11:])+1)
		self._fileName = os.path.join(self._paths.sets, self._name) \
						+ settings.GENSETTINGS.get('Extentions', 'liste')[0]

	def _read(self, preferedPath, dataBase):
		tmp = None
		self._listElem = []
		try:
			tree = ET.parse(self._fileName)
			tree.getroot().find('slide_groups')[:] # pylint: disable=expression-not-assigned
		except (OSError, IOError, AttributeError):
			logging.warning('Not able to read "%s"\n%s'%(self._fileName, traceback.format_exc()))
			return 1, traceback.format_exc()
		xmlList = tree.getroot()

		pathToSearch = []
		if preferedPath:
			pathToSearch.append(preferedPath)
		pathToSearch.append(self._paths.songs)
		self._name = xmlList.attrib['name']

		for title in xmlList.find('slide_groups'):
			if title.attrib['type'] == 'song':
				# Different ways of writting the path, test all

				for path in pathToSearch:
					tmp = elements.Chant( os.path.join(path, title.attrib['path'], title.attrib['name']) )
					if not tmp.exist():
						tmp = elements.Chant( os.path.join(path, title.attrib['name']) )
						if not tmp.exist():
							tmp = elements.Chant( os.path.join(path, 'songs', title.attrib['name']) )
					if tmp.exist():
						break

			elif title.attrib['type'] == 'media':
				tmp = elements.Element(title.attrib['name'], title.attrib['type'], title.attrib['path'])
			elif title.attrib['type'] == 'image':
				nom = title.attrib['name']
				try:
					extention = title.attrib['ext']
				except KeyError:
					extention = ''
				tmp = elements.ImageObj(os.path.join(title.attrib['path'], nom + extention))
			elif title.attrib['type'] == 'verse':
				tmp = elements.Passage( title.attrib['version'], int(title.attrib['livre']), \
												int(title.attrib['chap1']), int(title.attrib['chap2']), \
												int(title.attrib['vers1']), int(title.attrib['vers2']) )
			if dataBase:
				try:
					tmp = dataBase[tmp.nom]
					tmp.resetDiapos()
				except KeyError:
					pass
			self._listElem.append(tmp)
		self._changed = False
		return 0, ''

	def append(self, element):
		self._listElem.append(element)
		self._changed = True

	def insert(self, index, element):
		self._listElem.insert(index, element)
		self._changed = True

	def clear(self):
		del self._listElem[:]
		self._changed = True

	def setName(self, inputPath):
		self._name = fonc.get_file_name(inputPath)
		self._fileName = os.path.join(fonc.get_path(inputPath), \
						fonc.enleve_accents(fonc.get_file_name_ext(inputPath)))

	def save(self):
		new_set = ET.Element("set")
		new_set.set("name", self._name)
		slide_groups = ET.SubElement(new_set, "slide_groups")
		slide_group = []
		for i, element in enumerate(self._listElem):
			chemin = fonc.get_path(element.chemin)
			# For compatibility between linux an windows, all path are writtent with slash
			chemin = chemin.replace(os.sep, '/')
			# Write path relative to songs directory
			chemin = chemin.replace('%s'%self._paths.songs.replace(os.sep, '/'), '')

			slide_group.append(ET.SubElement(slide_groups, "slide_group"))
			slide_group[i].set("type", element.etype)
			if element.etype == 'song':
				slide_group[i].set("path", chemin)
				slide_group[i].set("name", element.nom)
			elif element.etype == 'verse':
				slide_group[i].set("name", element.nom)
				slide_group[i].set("path", chemin)
				slide_group[i].set("version", element.version)
				slide_group[i].set("livre", str(element.livre))
				slide_group[i].set("chap1", str(element.chap1))
				slide_group[i].set("chap2", str(element.chap2))
				slide_group[i].set("vers1", str(element.vers1))
				slide_group[i].set("vers2", str(element.vers2))
			elif element.etype == 'image':
				slide_group[i].set("name", element.nom)
				slide_group[i].set("path", chemin)
				slide_group[i].set("ext", element.extention)

		tree = ET.ElementTree(new_set)
		fonc.indent(new_set)
		tree.write(self._fileName, encoding="UTF-8", xml_declaration=True)
		self._changed = False

	def delete(self):
		try:
			os.remove(self._fileName)
		except (OSError, IOError) as error:
			if error.errno == errno.ENOENT:
				logging.warning('File "%s" does not exist.'%self._fileName)
			elif error.errno == errno.EACCES:
				logging.warning('Acces to "%s" is not permited.'%self._fileName)
			else:
				logging.error(traceback.format_exc())
				raise
		self._changed = True

	def load(self, fileName, preferedPath=None, dataBase=None):
		setExtention = settings.GENSETTINGS.get('Extentions', 'liste')[0]
		os.path.join(fonc.get_path(fileName), \
					fonc.enleve_accents(fonc.get_file_name_ext(fileName)))
		if os.path.isfile(fileName):
			self._fileName = fileName
		else:
			self._fileName = os.path.join(self._paths.sets, fileName)
		if fonc.get_ext(self._fileName) != setExtention \
				and os.path.isfile(self._fileName + setExtention):
			self._fileName = self._fileName + setExtention
		return self._read(preferedPath, dataBase)

	@property
	def path(self):
		return self._fileName

	@property
	def changed(self):
		return self._changed
