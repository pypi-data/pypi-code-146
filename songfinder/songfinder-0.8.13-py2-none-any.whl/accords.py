# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import warnings

from songfinder import fonctions as fonc
from songfinder import dataAccords
from songfinder import corrector
from songfinder import classSettings as settings

ACCORDSDATA = dataAccords.AccordsData()
CORRALL = corrector.Corrector(ACCORDSDATA.accPossible)

class Accords(object):
	def __init__(self, ligneAcc, data=None, transposeNb=0, capo=0, \
					corrAll=None, exportSettings=None):

		self.data = data
		self._ligneAcc = ligneAcc
		self._transposeNb = transposeNb
		self._capo = capo
		self._accords = None

		if not corrAll:
			self.corrAll = CORRALL
		if not data:
			self.data = ACCORDSDATA
		if not exportSettings:
			self._exportSettings = settings.LATEXSETTINGS
		else:
			self._exportSettings = exportSettings

		self._haveLeftBracket = []
		self._haveRightBracket = []

		self._clean()
		self._getLigne()
		self._compactChord()

	def getChords(self):
		if self._exportSettings.get('Export_Parameters', 'transpose'):
			self._transpose(self._transposeNb)
		if self._exportSettings.get('Export_Parameters', 'capo') and self._capo:
			self._transpose(-self._capo)
		if self._exportSettings.get('Export_Parameters', 'simple_chords'):
			self._simplifyChord()
		if self._exportSettings.get('Export_Parameters', 'keep_first'):
			self._keepFirst()
		if self._exportSettings.get('Export_Parameters', 'keep_last'):
			self._keepLast()
		if self._exportSettings.get('Export_Parameters', 'sol_chords'):
			self._translate('fr')
		self._putBrackets()
		self._noDoublon()
		return self._accords

	def _noDoublon(self):
		newChords = []
		previous = None
		for accord in self._accords:
			if not previous or accord.replace(')','') != previous.replace('(',''):
				newChords.append(accord)
			previous = accord
		self._accords = newChords

	def _clean(self):
		self._ligneAcc = self._ligneAcc
		if not self._ligneAcc:
			warnings.warn('Empty chord')
			self._ligneAcc = ''
			return

		self._ligneAcc = self._ligneAcc.strip(' ')
		self._ligneAcc = fonc.strip_perso(self._ligneAcc, '\n')
		self._ligneAcc = fonc.strip_perso(self._ligneAcc, '\\ac')
		self._ligneAcc = self._ligneAcc.strip(' ')
		self._ligneAcc = self._ligneAcc.replace('M ', '')

		for _ in range(5):
			self._ligneAcc = self._ligneAcc.replace('  ', ' ')

	def _getLigne(self):
		self._accords = self._ligneAcc.split(' ')
		# Checkif has brackets and removes them
		for i,accord in enumerate(self._accords):
			if accord:
				if accord[0] == '(':
					self._haveLeftBracket.append(i)
					accord = accord[1:]
				if accord[-1] == ')':
					self._haveRightBracket.append(i)
					accord = accord[:-1]
			self._accords[i] = accord

		self._translate('ang')

		for i,accord in enumerate(self._accords):
			if accord[:2] in self.data.execpt:
				accord = self.data.execpt[accord[:2]] + accord[2:]

			if self.corrAll:
				accord = '/'.join( [self.corrAll.check(partAcc) \
									for partAcc in accord.split('/')] )
			parts = accord.split('/')
			for j, part in enumerate(parts):
				try:
					parts[j] = self.data.execpt[part]
				except KeyError:
					pass
			self._accords[i] = '/'.join(parts)

	def _putBrackets(self):
		for index in self._haveLeftBracket:
			self._accords[index] = '(%s'%self._accords[index]
		for index in self._haveRightBracket:
			self._accords[index] = '%s)'%self._accords[index]

	def _translate(self, lang='fr'):
		for i, chord in enumerate(self._accords):
			parts = chord.split('/')
			for j, part in enumerate(parts):
				part = fonc.upper_first(part)
				if part[:2] in ['Do', 'DO']:
					index = 0
					reste = part[2:]
				elif part[:2] in ['Fa', 'FA']:
					index = 3
					reste = part[2:]
				elif part[:3] in ['Sol', 'SOl', 'SOL', 'SoL']:
					index = 4
					reste = part[3:]
				else:
					try:
						index = self.data.accordsTonang.index(part[0])
						reste = part[1:]
					except (ValueError, IndexError):
						try:
							# For Ré avec accent, TODO do better
							index = self.data.accordsTon.index( \
										part[0] + part[1].lower().replace('e', 'é') )
							reste = part[2:]
						except (ValueError, IndexError):
							warnings.warn(repr('Accord inconnu "%s"'%part))
							break
				if lang == 'fr':
					part = self.data.accordsTon[index] + reste
				else:
					part = self.data.accordsTonang[index] + reste
				parts[j] = part
			self._accords[i] = '/'.join(parts)

	def _compactChord(self):
		for i, chord in enumerate(self._accords):
			for old, new in self.data.dicoCompact.items():
				chord = chord.replace(old, new)
			self._accords[i] = chord

	def _simplifyChord(self):
		for i, chord in enumerate(self._accords):
			parts = chord.split('/')
			for j, part in enumerate(parts):
				for spe in self.data.modulation:
					part = part.replace(spe, '')
				parts[j] = part
			self._accords[i] = '/'.join(parts)

	def _keepFirst(self):
		for i, chord in enumerate(self._accords):
			self._accords[i] = chord.split('/')[0]

	def _keepLast(self):
		for i, chord in enumerate(self._accords):
			try:
				self._accords[i] = chord.split('/')[1]
			except IndexError:
				self._accords[i] = chord.split('/')[0]

	def _nbAlt(self, accords):
		ind = 0
		for i,diez in enumerate(self.data.ordreDiez):
			if diez + '#' in [accord[:2] for accord in accords]:
				ind = i+1
		for i,bemol in enumerate(reversed(self.data.ordreDiez)):
			if bemol + 'b' in [accord[:2] for accord in accords]:
				ind = (i+1)
		return ind

	def _transposeTest(self, accordsRef, accordsNon, demiTon):
		# Transposition
		newAccords = []
		for chord in accordsRef:
			if len(chord)>1:
				refAlt = chord[-1]
				break

		for accord in self._accords:
			newPart = []
			for part in accord.split('/'):
				if len(part) > 1 and part[1] in ['#', 'b'] and part[1] != refAlt:
					part = accordsRef[accordsNon.index(part[:2])] + part[2:]
				pre = ( part[:1] + ' ' + part[1:] ).replace(' #', '#').replace(' b', 'b')[:2].strip(' ')
				for i,ref in enumerate(accordsRef):
					if pre == ref:
						part = part.replace(ref, accordsRef[(i+demiTon)%len(accordsRef)])
						break
				newPart.append(part)
			newAccords.append('/'.join(newPart))
		return newAccords

	def _transpose(self, demiTon):
		if demiTon:
			accords1 = self._transposeTest(self.data.accordsDie, self.data.accordsBem, demiTon)
			accords2 = self._transposeTest(self.data.accordsBem, self.data.accordsDie, demiTon)
			if self._nbAlt(accords2) >= self._nbAlt(accords1):
				self._accords = accords1
			else:
				self._accords = accords2
