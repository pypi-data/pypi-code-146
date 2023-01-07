# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

import os
import errno
import xml.etree.cElementTree as ET
import traceback
import string
import codecs
import logging
import re

from songfinder import gestchant
from songfinder import classPaths
from songfinder import fonctions as fonc
from songfinder import messages as tkMessageBox
from songfinder import pyreplace
from songfinder import classSettings as settings
from songfinder.elements import Element
from songfinder.elements import cdlparser

try:
	basestring # pylint: disable=used-before-assignment
except NameError: # For python 3 Compatibility
	basestring = str # pylint: disable=redefined-builtin

RECEUILS = ['JEM', 'ASA', 'WOC', 'HER', 'HEG', 'FAP', 'MAR', \
			'CCO', 'PBL', 'LDM', 'JFS', 'THB', 'EHO', 'ALG', \
			'BLF', 'ALR', 'HLS', 'IMP', 'PNK', 'DNL', 'ROG', \
			'WOC', 'SOL', 'FRU', 'OST', 'ENC', 'DIV']

class Chant(Element):
	def __init__(self, chant, nom=''):
		self.etype = 'song'
		if fonc.get_ext(chant) == '' and chant.find('http') == -1:
			chant = chant + settings.GENSETTINGS.get('Extentions', 'chant')[0]
		self.chemin = os.path.join(chant)

		Element.__init__( self, chant, self.etype, self.chemin)
		self.nom = fonc.get_file_name(self.chemin)
		self._title = nom
		if self.nom[3:6].isdigit():
			self._ref = self.nom[:3]
			self._customNumber = int(self.nom[3:6])
		self.reset()

	def _getCDL(self):
		parsedSong = cdlparser.CDLParser(self.chemin)
		self.key = parsedSong.key
		self.hymnNumber = parsedSong.hymnNumber
		self.ccli = parsedSong.ccli
		self.text = parsedSong.text
		self.title = parsedSong.title
		self.copyright = parsedSong.copyright
		self.tags = parsedSong.tags
		self.author = parsedSong.authors
		fileName = str(parsedSong) + settings.GENSETTINGS.get('Extentions', 'chant')[0]
		rootPath = classPaths.PATHS.songs
		self.chemin = os.path.join(rootPath, fileName)

	def reset(self):
		self._resetText()
		self._transpose = None
		self._capo = None
		self._key = None
		self._turfNumber = None
		self._hymnNumber = None

	def _resetText(self):
		self._text = None
		self._words = ''
		self._textHash = None
		self.resetDiapos()

	def _save(self):
		# This function is keept for hidden functionality
		# This is probably not the function you actualy want to edit
		# Look at database save method

		# We use a different xml lib here because it does not add carriage return on Windows for writes
		# There might be a way to use xml.etree.cElementTree that don't but have not figured out
		# xml.etree.cElementTree is faster at parsing so keep it for song parsing
		import lxml.etree as ET_write
		ext = settings.GENSETTINGS.get('Extentions', 'chant')[0]
		if fonc.get_ext(self.chemin) != ext:
			path = classPaths.PATHS.songs
			fileName = '%s%d %s'%(self.songBook, self.hymnNumber, self.title)
		else:
			path = fonc.get_path(self.chemin)
			fileName = fonc.get_file_name(self.chemin)
		fileName = fonc.enleve_accents(fileName)
		fileName = re.sub(r'[\/?!,;:*<>"|]+', '', fileName)
		fileName = fileName.strip(' ').replace('  ', ' ')
		self.chemin = os.path.join(path, fileName) + ext
		try:
			tree = ET_write.parse(self.chemin)
			chant_xml = tree.getroot()
		except (OSError, IOError) as error:
			chant_xml = ET_write.Element(self.etype)
		self.safeUpdateXML(chant_xml, 'lyrics', self.text)
		self.safeUpdateXML(chant_xml, 'title', self.title)
		self.safeUpdateXML(chant_xml, 'transpose', self.transpose)
		self.safeUpdateXML(chant_xml, 'capo', self.capo)
		self.safeUpdateXML(chant_xml, 'key', self.key)
		self.safeUpdateXML(chant_xml, 'turf_number', self.turfNumber)
		self.safeUpdateXML(chant_xml, 'hymn_number', self.hymnNumber)
		self.safeUpdateXML(chant_xml, 'author', self.author)
		self.safeUpdateXML(chant_xml, 'copyright', self.copyright)
		self.safeUpdateXML(chant_xml, 'ccli', self.ccli)
		self.safeUpdateXML(chant_xml, 'tags', self.tags)
		fonc.indent(chant_xml)

		tree = ET_write.ElementTree(chant_xml)
		tree.write(self.chemin, encoding="UTF-8", xml_declaration=True)
		self.resetDiapos()

	def _replaceInText(self, toReplace, replaceBy):
		self.text = self.text.replace(toReplace, replaceBy)
		self._save()

	@property
	def nums(self):
		return {'custom':self.customNumber, \
				'turf':self.turfNumber, \
				'hymn':self.hymnNumber, \
				}

	@property
	def turfNumber(self):
		self.text # pylint: disable=pointless-statement
		return self._turfNumber

	@property
	def hymnNumber(self):
		self.text # pylint: disable=pointless-statement
		return self._hymnNumber

	@property
	def customNumber(self):
		self.text # pylint: disable=pointless-statement
		return self._customNumber

	@property
	def transpose(self):
		self.text # pylint: disable=pointless-statement
		return self._transpose

	@property
	def capo(self):
		self.text # pylint: disable=pointless-statement
		return self._capo

	@property
	def key(self):
		self.text # pylint: disable=pointless-statement
		return self._key

	@property
	def author(self):
		self.text # pylint: disable=pointless-statement
		return self._author

	@property
	def copyright(self):
		self.text # pylint: disable=pointless-statement
		return self._copyright

	@property
	def ccli(self):
		self.text # pylint: disable=pointless-statement
		return self._ccli

	@property
	def text(self):
		if self._text is None:
			cdlPath = settings.GENSETTINGS.get('Paths', 'conducteurdelouange')
			if fonc.get_ext(self.chemin) in settings.GENSETTINGS.get('Extentions', 'chordpro'):
				self._getChordPro()
			elif fonc.get_ext(self.chemin) in settings.GENSETTINGS.get('Extentions', 'chant'):
				self._getXML()
			elif self.chemin.find(cdlPath) != -1:
				self._getCDL()
			else:
				logging.warning('Unknown file format for "%s".'%self.chemin)
		return self._text

	def _getXML(self):
		self.reset()
		try:
			tree = ET.parse(self.chemin)
			chant_xml = tree.getroot()
		except (OSError, IOError):
			logging.warning('Not able to read "%s"\n%s'%(self.chemin, traceback.format_exc()))
			self.title = self.nom
			chant_xml = ET.Element(self.etype)
		except ET.ParseError:
			logging.info('Error on %s:\n%s'%(self.chemin, traceback.format_exc()))
			tkMessageBox.showerror('Erreur', 'Le fichier "%s" est illisible.'%self.chemin)
		try:
			tmp = chant_xml.find('lyrics').text
			title = chant_xml.find('title').text
		except (AttributeError, KeyError):
			tmp = ''
			title = ''
		if tmp is None:
			tmp = ''
		try:
			self._transpose = int( chant_xml.find('transpose').text )
		except (AttributeError, KeyError, ValueError, TypeError):
			self._transpose = None
		try:
			self._capo = int( chant_xml.find('capo').text )
		except (AttributeError, KeyError, ValueError, TypeError):
			self._capo = None
		try:
			self._hymnNumber = int( chant_xml.find('hymn_number').text )
		except (AttributeError, KeyError, ValueError, TypeError):
			self._hymnNumber = None
		try:
			self._turfNumber = int( chant_xml.find('turf_number').text )
		except (AttributeError, KeyError, ValueError, TypeError):
			self._turfNumber = None
		try:
			self._key = chant_xml.find('key').text
		except (AttributeError, KeyError):
			self._key = ''
		try:
			self._key = self._key.replace('\n', '')
		except AttributeError:
			pass
		try:
			self._author = chant_xml.find('author').text
		except (AttributeError, KeyError):
			self._author = None
		try:
			self._copyright = chant_xml.find('copyright').text
		except (AttributeError, KeyError):
			self._copyright = None
		try:
			self._ccli = chant_xml.find('ccli').text.replace(' ', '')
		except (AttributeError, KeyError):
			self._ccli = ''
		try:
			tags = chant_xml.find('tags').text
			self.tags = tags
		except (AttributeError, KeyError):
			self._tags = []
		self.title = title
		self.text = tmp

	@transpose.setter
	def transpose(self, value):
		value = value.strip('\n')
		try:
			self._transpose = int(value)
		except (ValueError, TypeError):
			if not value:
				self._transpose = 0
			else:
				self._transpose = None

	@capo.setter
	def capo(self, value):
		value = value.strip('\n')
		try:
			self._capo = int(value)
		except (ValueError, TypeError):
			if not value:
				self._capo = 0
			else:
				self._capo = None

	@turfNumber.setter
	def turfNumber(self, value):
		value = value.strip('\n')
		try:
			self._turfNumber = int(value)
		except (ValueError, TypeError):
			if not value:
				self._turfNumber = 0
			else:
				self._turfNumber = None

	@hymnNumber.setter
	def hymnNumber(self, value):
		try:
			value = value.strip('\n')
		except AttributeError:
			pass
		try:
			self._hymnNumber = int(value)
		except (ValueError, TypeError):
			if not value:
				self._hymnNumber = 0
			else:
				self._hymnNumber = None

	@key.setter
	def key(self, value):
		self._key = value.strip('\n')

	@text.setter
	def text(self, value):
		self._resetText()
		value = fonc.supressB(value, '[', ']') ######
		value = gestchant.nettoyage(fonc.safeUnicode(value))
		value = '%s\n'%value
		self._text = value

	@author.setter
	def author(self, value):
		self._author = value.replace('\n', ' ').replace('  ', ' ').strip(' ')

	@copyright.setter
	def copyright(self, value):
		self._copyright = value.strip('\n')

	@ccli.setter
	def ccli(self, value):
		self._ccli = value.strip('\n').replace(' ', '')

	@property
	def words(self):
		if not self._words:
			text = gestchant.netoyage_paroles(self.text)
			self._words = text.split()
		return self._words

	@property
	def songBook(self):
		return self._ref

	def _getChordPro(self):
		try:
			with codecs.open(self.chemin, encoding='utf-8') as f:
				brut = f.read()
				if not brut:
					logging.warning('File "%s" is empty\n%s'%(self.chemin, traceback.format_exc()))
					return ''
		except (OSError, IOError):
			logging.warning('Not able to read "%s"\n%s'%(self.chemin, traceback.format_exc()))
			return ''

		self.title = fonc.getB(brut, '{t:', '}')[0]
		self.author = fonc.getB(brut, '{st:', '}')[0]
		self.copyright = fonc.getB(brut, '{c:', '}')[0]
		self.key = fonc.getB(brut, '{key:', '}')[0]
		try:
			ccliBrut = fonc.getB(brut, '{c:shir.fr', '}')[0]
		except IndexError:
			ccliBrut = fonc.getB(brut, '{c: jemaf.fr', '}')[0]
		self._getSongBook(ccliBrut)

		brut = pyreplace.cleanupChar(brut.encode('utf-8'))
		brut = pyreplace.cleanupSpace(brut).decode('utf-8')

		# Interprete chorpro syntax
		brut = ' \\ss\n' + brut
		brut = brut.replace('\n\n', '\n\n\\ss\n')
		brut = brut.replace('{soc}', '\n\n\\sc\n')
		brut = brut.replace('{eoc}', '\n\n\\ss\n')
		brut = brut.replace('{c:Pont}', '\n\n\\sb\n')
		brut = fonc.supressB(brut, '{', '}')

		brut = gestchant.nettoyage(brut)
		brut = gestchant.nettoyage(brut)
		brut = brut.replace('\\ss\n\n\\sc', '\\sc')
		brut = brut.replace('\\ss\n\n\\sb', '\\sb')

		# Put double back slash at the last chord of each line
		brut = brut + '\n'
		fin = len(brut)
		while fin != -1:
			line = brut.rfind('\n', 0, fin)
			fin = brut.rfind(']', 0, line)
			if line == fin+1:
				precedant = fin
				while brut[precedant] == ']':
					precedant = brut.rfind('[', 0, precedant)-1
				brut = brut[:precedant+2] + '(' + brut[precedant+2:fin] + ')\\' + brut[fin:]
			else:
				brut = brut[:fin] + '\\' + brut[fin:]
		brut = fonc.strip_perso(brut, '\\\n')

		# Remove space after chord
		for letter in string.ascii_uppercase[:7]:
			brut = brut.replace('\n[%s] '%letter, '\n[%s]'%letter)
		brut = self._convertChordsFormat(brut)
		self.text = brut

	def _getSongBook(self, ccliBrut):
		for receuil in RECEUILS:
			deb = ccliBrut.find(receuil)
			fin = deb + len(receuil)
			for _ in range(10):
				if len(ccliBrut)> fin and not ccliBrut[fin].isdigit():
					break
				fin += 1
			if deb != -1 and fin != -1:
				self._ccli = ccliBrut[deb:fin].replace(' ', '')
				num = ccliBrut[deb + len(receuil):fin]
				try:
					self._hymnNumber = int(num)
					self._ref = receuil
				except ValueError:
					self._hymnNumber = 0
					logging.info('No song number for %s'%self.chemin)
			if self._hymnNumber:
				break

	def _convertChordsFormat(self, text):
		if text != '':
			text = text + '\n'
			listChords = fonc.getB(text, '[', ']')
			where = 0
			last = 0
			for i,chord in enumerate(listChords):
				# Add parenthesis for chord at end of lines
				if chord.find('\\') != -1:
					toAdd = '\\ac ' + ' '.join( listChords[last:i+1] ).replace('\\', '') + '\n'
					where = text.find(chord, where)
					where = text.find('\n', where) + 1
					text = text[:where] + toAdd + text[where:]
					last = i+1
			text = fonc.strip_perso(text, '\n')

			text = fonc.supressB(text, '[', ']')

			for newslide in settings.GENSETTINGS.get('Syntax', 'newslide')[0]:
				text = text.replace('%s\n\n\\ac'%newslide, '%s\n\\ac'%newslide)
			return text
		return ''

	def __ne__(self, other):
		return not self == other

	def __eq__(self, other):
		if not self.words and not other.words:
			if self.title == other.title \
					and self.supInfo == other.supInfo:
				return True
			return False
		myWords = set(self.words)
		otherWords = set(other.words)
		commun = len(myWords & otherWords)
		ratio = 2*commun/(len(myWords) + len(otherWords))
		return ratio > 0.93

	def __hash__(self):
		return hash(self.title + self.supInfo)

	def __gt__(self, other):
		return self.title > other.title

	def __ge__(self, other):
		return self.title >= other.title
