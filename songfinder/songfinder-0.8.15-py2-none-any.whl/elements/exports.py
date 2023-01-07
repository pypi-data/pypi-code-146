# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import codecs

from songfinder import gestchant
from songfinder import fonctions as fonc
from songfinder import accords
from songfinder import classDiapo
import songfinder
from songfinder import classSettings as settings

try:
	basestring # pylint: disable=used-before-assignment
except NameError: # For python 3 Compatibility
	basestring = str # pylint: disable=redefined-builtin

class ExportBase(object):
	def __init__(self, element, titleLevel, exportSettings=None):
		self.element = element
		self._nbLignes = -1
		self._forcedNewLine = '\\newac'
		self._newLineSuggest = '\\newline'
		self._chordsMarker = '\t\\hspace*{\\fill}'
		self._diapos = []
		self._exportedText = ''
		self._titleLevel = titleLevel

		self._newlineMarker = '\n'
		self._supportedTypes = []
		self._specialChar = []

		if not exportSettings:
			self._exportSettings = settings.LATEXSETTINGS
		else:
			self._exportSettings = exportSettings

	@property
	def text(self):
		return self.element.text

	@property
	def transpose(self):
		return self.element.transpose

	@property
	def capo(self):
		return self.element.capo

	@property
	def diapos(self):
		return self.element.diapos

	@property
	def title(self):
		return self.element.title

	@property
	def etype(self):
		return self.element.etype

	@property
	def nom(self):
		return self.element.nom

	@property
	def key(self):
		return self.element.key

	@property
	def printref(self):
		return self.element.printref

	@property
	def ccli(self):
		return self.element.ccli

	@property
	def hymnNumber(self):
		return self.element.hymnNumber

	@property
	def customNumber(self):
		return self.element.customNumber

	@property
	def turfNumber(self):
		return self.element.turfNumber

	@title.setter
	def title(self, value):
		self.element.title = value

	@etype.setter
	def etype(self, value):
		self.element.etype = value

	@property
	def nbLine(self):
		if self._nbLignes == -1:
			self.exportText # pylint: disable=pointless-statement,no-member
		return self._nbLignes

	def _processChords(self, text):
		deb = 0
		fin = 0
		newtext = ''
		while fin != -1:
			tmp = text.find('\\ac', deb)
			if tmp == -1:
				newtext = newtext + text[deb:]
				fin = -1
			else:
				fin = text.find('\n', tmp)
				if fin != -1:
					extrait = text[tmp:fin]
				else:
					extrait = text[tmp:]

				chordsObj = accords.Accords(extrait, \
											transposeNb=self.transpose, \
											capo=self.capo,\
											exportSettings=self._exportSettings)
				chords = chordsObj.getChords()

				if text[deb:tmp] == '':
					addNewLine = '%s'%self._forcedNewLine
				else:
					addNewLine = ''
				newtext = '%s%s%s\\ac %s%s'%(newtext, text[deb:tmp], addNewLine, \
							'~~'.join(chords), self._forcedNewLine)
				deb = fin+1
		return newtext


	def _processNewLine(self, text):
		if self._exportSettings.get('Export_Parameters', 'saut_lignes'):
			text = text.replace('\n', ' %s'%self._newLineSuggest)
			# Force newline if one line ends a sentence TODO to keep ?
			for ponct in ['.', '!', '?']:
				text = text.replace('%s %s'%(ponct, self._newLineSuggest), '%s\n'%ponct)

		# Saut de ligne apres et pas avant les chaines suivantes
		for execp in ['"', ' "', ' (bis)', ' (ter)', ' (x4)', '.', '?']:
			text = text.replace('\n' + execp, execp + '\n')

		# Proposition de saut de ligne apres et pas avant les chaines suivantes
		for execp in [',', ';', ':']:
			text = text.replace('\n' + execp, execp + self._newLineSuggest)

		# Saut de ligne apres les chaines suivantes
		for execp in ['(bis)', '(ter)', '(x4)', '(bis) ', '(ter) ', '(x4) ', '\\l ']:
			text = text.replace(execp + self._newLineSuggest, execp + '\n')

		text = text.replace('.\n.\n.\n', '...\n')
		text = text.replace('Oh !\n', 'Oh !')
		text = text.replace('oh !\n', 'oh !')
		text = text.replace(self._forcedNewLine, '\n')
		# Force new line after (f) if there are h/f responces)
		text = text.replace('(f) %s'%self._newLineSuggest, '(f) \n')

		supressStarts = [self._newLineSuggest, '\n']
		supressEnds = ['(bis)', '(Bis)', '(ter)', '(x3)', '(x4)']
		for start in supressStarts:
			for end in supressEnds:
				text = text.replace(start+end, '')
		# Must be after for the case where (bis) is just befor chords
		acReplace = [self._newLineSuggest, '\n', '\n ']
		for start in acReplace:
			text = text.replace(start +'\\ac', '\\ac')


		# Do not take away a new line if there is a bis at the end
		for multiple in ['(bis)', '(ter)', '(x4)']:
			fin = len(text)-1
			bis = 0
			while fin != -1 and bis != -1:
				bis = text.rfind(multiple, 0, fin)
				fin = text.rfind(self._newLineSuggest, 0, bis)
				if fin != -1 and bis != -1 and text[fin+8:bis].find('\n') == -1:
					text = text[:fin] + '\n' + text[fin+8:]
		return text

	def _getDiapos(self):
		if self._diapos != []:
			return self._diapos

		text = self.text
		if self._exportSettings.get('Export_Parameters', 'chords'):
			text = self._processChords(text)
		else:
			text = '%s\n'%text
			text = fonc.supressB(text, '\\ac', '\n')
			text = text.strip('\n')
		text = self._processNewLine(text)
		listStype = []
		# La première est vide ie au dessus du premier \s
		listText, listStype = fonc.splitPerso([text], \
								settings.GENSETTINGS.get('Syntax', 'newslide'), \
								listStype, 0)
		del listText[0]

		# Suprime les doublons
		newListText = []
		newListStype = []
		toIgnore = [self._newLineSuggest, settings.GENSETTINGS.get('Syntax', 'newline')]
		for i,text in enumerate(listText):
			match = 0.
			for textRef in newListText:
				match = max(fonc.matchPara(textRef, text, ignore=toIgnore), match)
			stripedText = text.replace(' %s'%self._newLineSuggest, '')
			if match < 10 and text.find('\\...') == -1 and stripedText:
				newListText.append(text)
				newListStype.append(listStype[i])
		listText = newListText
		listStype = newListStype

		listStypePlus = gestchant.getListStypePlus(listStype)

		if self._exportSettings.get('Export_Parameters', 'one_chorus'):
			listStypePlus = fonc.takeOne('\\sc', listStypePlus)
			listStypePlus = fonc.takeOne('\\sb', listStypePlus)

		# Fusion et creation des diapos
		for elem in listStypePlus:
			text = ''
			for i,numDiapo in enumerate(elem[1]):
				text = '%s\n%s\n'%(text, listText[numDiapo])
				if numDiapo == elem[1][-1] or \
						( elem[0] == '\\ss' and len(fonc.supressB(text, '\\ac', '\n')) > 140 ) or \
						( elem[0] == '\\ss' and len(elem[1])%2 == 1 ) or \
						( elem[0] == '\\ss' and i%2 == 1 ):
					if elem[0] == '\\sc':
						if text.find('\\ac') != -1:
							max_car = 85
						else:
							max_car = 95
					else:
						if text.find('\\ac') != -1:
							max_car = 90
						else:
							max_car = 100
					diapo = classDiapo.Diapo( self.element, len(self._diapos)+1, elem[0], max_car, \
									len(listStypePlus), text.strip('\n') )
					self._diapos.append(diapo)
					text = ''
		return self._diapos

	def _clean(self, text):
		for _ in range(5):
			text = text.replace('\n\n\n', '\n\n')
			text = text.replace('{0}{0}'.format(self._newlineMarker), self._newlineMarker)
			text = text.replace('\n%s\n'%self._newlineMarker, '\n\n')
		text = text.strip('\n')
		text = fonc.strip_perso(text, self._newlineMarker)
		self._nbLignes = len(text.splitlines())
		return text

	def escape(self, inputData):
		"""
		Adds a backslash behind latex special characters
		"""
		if isinstance(inputData, basestring):
			output = inputData
			for char in self._specialChar:
				output = output.replace(char, '\\' + char)
		elif isinstance(inputData, list):
			output = []
			for text in inputData:
				for char in self._specialChar:
					text = text.replace(char, '\\' + char)
				output.append(text)
		else:
			raise Exception('Input "%s"must be basestring or list, but is %s.'%(inputData, type(inputData)))
		return output

class ExportLatex(ExportBase):
	def __init__(self, element, titleLevel=1, exportSettings=None):
		ExportBase.__init__(self, element, titleLevel, exportSettings=exportSettings)
		self._newlineMarker = '\\\\'
		self._supportedTypes = ['latex', 'verse']
		self._specialChar = ['#', '_']

	@property
	def exportText(self):
		if self.etype == 'song':
			self.etype = 'latex'
		if self.etype not in self._supportedTypes :
			self.etype = 'song'
			return ''
		# ~ if self._exportedText != '':
			# ~ self.etype = 'song'
			# ~ return self._exportedText
		self._getDiapos()
		text = '\n\n'.join( [diapo.latex for diapo in self._diapos] )
		text = self.escape(text)
		text = text.replace('\\ac', self._chordsMarker)
		text = text.replace('\n', '%s\n'%self._newlineMarker)
		text = text.replace('\n%s'%self._newlineMarker, '\n')
		text = text.replace('\n\\tab %s'%self._newlineMarker, '\n')
		# Accord en debut de chant
		if text[:len(self._chordsMarker)] == self._chordsMarker:
			fin = text.find('%s\n'%self._newlineMarker)
			nextCar = fin+len(self._newlineMarker)
			# Check if there is text after the chords if not do not threat that as starting chords
			if fin != -1 \
					and text[fin:nextCar+2] != '%s\n\n'%self._newlineMarker \
					and text[nextCar+1:nextCar+1+len(self._chordsMarker)] != '%s'%self._chordsMarker:
				text = '(%s)%s\n%s'%(text[len(self._chordsMarker):fin].strip(' '), \
									self._newlineMarker, \
									text[nextCar:])
		text = self._clean(text)

		# Capo
		if self._exportSettings.get('Export_Parameters', 'capo') and self.capo:
			text = '\\emph{Capo %s}%s\n%s'%(str(self.capo), self._newlineMarker, text)

		# Title
		text =  '\\begin{figure}\n\\section{%s}\n%s\n\\end{figure}\n'\
					%(self.escape(self.title), text)

		# Song per page
		if self._exportSettings.get('Export_Parameters', 'one_song_per_page'):
			text = '%s\n\\clearpage'%text

		self._exportedText = text
		self.etype = 'song'
		return text

	@property
	def title(self):
		# Title key
		if self._exportSettings.get('Export_Parameters', 'printkey'):
			chord = accords.Accords(self.key, \
									transposeNb=self.transpose, \
									capo=self.capo,\
									exportSettings=self._exportSettings)
			key = chord.getChords()[0]
			if key != '':
				key = '~--~\\emph{%s}'%key
		else:
			key = ''

		# Reference in title
		if self._exportSettings.get('Export_Parameters', 'printref')\
				and self.ccli:
			refID = ' (%s)'%(self.ccli)
		else:
			refID = ''

		# Title
		return '%s%s%s'%(self.element.title, refID, key)

class ExportMarkdown(ExportBase):
	def __init__(self, element, titleLevel=1, exportSettings=None):
		ExportBase.__init__(self, element, titleLevel, exportSettings=exportSettings)
		self._newlineMarker = '  '
		self._supportedTypes = ['markdown']
		self._specialChar = ['*', '_']

	@property
	def exportText(self):
		if self.etype == 'song':
			self.etype = 'markdown'
		if self.etype not in self._supportedTypes :
			self.etype = 'song'
			return ''
		# ~ if self._exportedText != '':
			# ~ self.etype = 'song'
			# ~ return self._exportedText
		self._getDiapos()
		text = '\n\n'.join( [diapo.markdown for diapo in self._diapos] )
		text = '%s\n'%text
		deb = 0
		fin = 0
		toFindStart = '\\ac'
		toFindEnd = '\n'
		while deb != -1:
			deb = text.find(toFindStart, fin)
			fin = text.find(toFindEnd, deb)
			if deb == -1 or fin == -1:
				break
			text = '%s`%s`\n%s'%(text[:deb], \
								text[deb+len(toFindStart):fin].strip(' '), \
								text[fin+len(toFindEnd):])
			fin -= len(toFindStart) + 2

		text = text.replace('\n', '%s\n'%self._newlineMarker)
		text = text.replace('~~', '  ')
		text = self._clean(text)
		text = '%s\n'%text

		# Capo
		if self._exportSettings.get('Export_Parameters', 'capo') \
														and self.capo:
			text = '*Capo %s*  \n%s'%(str(self.capo), text)

		# Title key
		if self._exportSettings.get('Export_Parameters', 'chords'):
			chord = accords.Accords(self.key, \
									transposeNb=self.transpose, \
									capo=self.capo,\
									exportSettings=self._exportSettings)
			key = chord.getChords()[0]
			if key != '':
				key = ' -- *%s*'%key
		else:
			key = ''

		# Title
		if self._exportSettings.get('Export_Parameters', 'chords'):
			title =  '%s %s%s\n'%('#'*self._titleLevel, self.title, key)
		else:
			title =  '%s %s\n'%('#'*self._titleLevel, self.title)
		if not self._exportSettings.get('Export_Parameters', 'list'):
			text =  '%s%s'%(title, text)
		else :
			text =  '%s'%(title)

		self._exportedText = text
		self.etype = 'song'
		return text

class ExportBeamer(ExportBase):
	def __init__(self, element, titleLevel=1, exportSettings=None):
		ExportBase.__init__(self, element, titleLevel, exportSettings=exportSettings)
		self._newlineMarker = '\\\\'
		self._supportedTypes = ['beamer', 'image', 'verse']
		self._specialChar = ['#', '_']

	@property
	def exportText(self):
		if self.etype == 'song':
			self.etype = 'beamer'
		if self.etype not in self._supportedTypes :
			self.etype = 'song'
			return ''
		# ~ if self._exportedText != '':
			# ~ self.etype = 'song'
			# ~ return self._exportedText
		self._diapos = []
		text = ''
		for diapo in self.diapos:
			toAdd = self.escape(diapo.beamer)
			toAdd = toAdd.replace('\n', '%s\n'%self._newlineMarker)
			toAdd = toAdd.replace('\n%s'%self._newlineMarker, '\n')
			backStr = diapo.backgroundName.replace('\\', '/')
			backStr = '"%s/%s"%s'%(fonc.get_path(backStr), \
								fonc.get_file_name(backStr), \
								fonc.get_ext(backStr))
			text += '\\newframe{%s}\n%s\n\\end{frame}\n\n'%(backStr, toAdd)
		text = self._clean(text)
		text = fonc.noNewLine(text, '\\newframe', self._newlineMarker)
		text = fonc.noNewLine(text, '\\vspace', self._newlineMarker)
		text = '%s\n'%text
		self._exportedText = text
		self.etype = 'song'
		return text

class ExportHtml(ExportBase):
	def __init__(self, element, titleLevel=1, markdowner=None,
						htmlStyle=None, htmlStylePath=None,\
						exportSettings=None):
		ExportBase.__init__(self, element, titleLevel, exportSettings=exportSettings)
		self._element = element
		self._supportedTypes = ['markdown']
		if markdowner:
			self._markdowner = markdowner
		else:
			import markdown # Consumes lots of memory
			self._markdowner = markdown.Markdown()
		self._htmlStyle = htmlStyle

		if not htmlStylePath:
			htmlStylePath = os.path.join(songfinder.__dataPath__, 'htmlTemplates', 'defaultStyle.html')
		if not htmlStyle and os.path.isfile(htmlStylePath):
			with codecs.open(htmlStylePath, 'r', encoding='utf-8') as styleFile:
				self._htmlStyle = styleFile.read()

	def _addTitle(self, text):
		if self.title:
			text = '<title>%s</title>\n'%self.title + text
		return text

	@property
	def exportText(self):
		if self.etype == 'song':
			self.etype = 'markdown'
		if self.etype not in self._supportedTypes :
			self.etype = 'song'
			return ''
		# ~ if self._exportedText != '':
			# ~ self.etype = 'song'
			# ~ return self._exportedText
		markdownText = ExportMarkdown(self._element, titleLevel=self._titleLevel).exportText

		text = self._markdowner.convert(markdownText)
		if self._titleLevel == 1:
			text = self._addTitle(text)
		if self._htmlStyle:
			text = self._htmlStyle.replace('@@body@@', text)
		self._markdowner.reset()
		self._exportedText = text
		self.etype = 'song'
		return text
