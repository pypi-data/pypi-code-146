# -*- coding: utf-8 -*-
#cython: language_level=2
from __future__ import unicode_literals
from __future__ import division


try:
	from songfinder import libLoader
	module = libLoader.load(__file__)
	globals().update(
		{n: getattr(module, n) for n in module.__all__} if hasattr(module, '__all__')
		else
		{k: v for (k, v) in module.__dict__.items() if not k.startswith('_')
	})
except (ImportError, NameError):
	# logging.info(traceback.format_exc())

	import os
	import logging
	import traceback
	import errno
	import time
	import re
	try:
		import cython
	except ImportError:
		logging.debug(traceback.format_exc())
		pass

	from songfinder import elements
	from songfinder import classPaths
	from songfinder import fonctions as fonc
	from songfinder import gestchant
	from songfinder import classSettings as settings

	class DataBase(object):
		def __init__(self, songPath=None):
			self._sizeMax = 3
			if songPath:
				self._songPath = songPath
				self._genPath = False
			else:
				self._songPath = classPaths.PATHS.songs
				self._genPath = True
			self._mergedDataBases = []
			self._maxCustomNumber = 0
			self._tagList = []
			self.update()

		def __contains__(self, value):
			return value in self._dicoLyrics

		def __getitem__(self, key):
			return self._dicoLyrics[key]

		def keys(self):
			return self._dicoLyrics.keys()

		def __iter__(self):
			return iter(self._dicoLyrics)

		@property
		def tags(self):
			if not self._tagList :
				tags = set()
				for song in self.keys():
					tags = tags | set(song.tags.split(','))
				self._tagList  = list(tags)
				self._tagList .sort()
			return self._tagList

		def remove(self, song):
			del self._dicoLyrics[song]
			del self._dicoTitles[song]
			del self._dicoTags[song]
			for num in song.nums.values():
				if num:
					self._dicoNums[num].remove(song)

		def add(self, song):
			self._dicoLyrics[song] = self._getStrings('%s %s'%(song.title, song.text))
			self._dicoTitles[song] = self._getStrings(song.title)
			self._dicoTags[song] = self._getStrings(song.tags)
			self.addDictNums(song)
			if song.songBook == 'SUP' \
				and song.customNumber > self._maxCustomNumber:
				self._maxCustomNumber = song.customNumber

		def addDictNums(self, song):
			for num in [num for num in song.nums.values() if num]:
				try:
					self._dicoNums[num].add(song)
				except KeyError:
					self._dicoNums[num] = set([song])

		def getDico(self, whichOne):
			if whichOne == 'lyrics':
				return self._dicoLyrics
			elif whichOne == 'titles':
				return self._dicoTitles
			elif whichOne == 'nums':
				return self._dicoNums
			elif whichOne == 'tags':
				return self._dicoTags
			else:
				logging.warning('Don\'t know which dico to return.'
							'You asked for %s, possible values '
							'are "lyrics", "titles", "num" and "tags".'%whichOne )
				return  dict()

		def update(self, callback=None, args=()):
			tmpsRef = time.time()
			if self._genPath:
				self._songPath = classPaths.PATHS.songs
			self._dicoLyrics = dict()
			self._dicoTitles = dict()
			self._dicoTags = dict()
			self._dicoNums = dict()
			self._findSongs(callback, args)
			logging.info('Updated dataBase in %fs, %d songs'%(time.time()-tmpsRef, len(self)))
			self._merge(update=True)
			self._tagList = []
			self.sanity_check()

		def sanity_check(self):
			for song in self.keys():
				if song!=song:
					logging.error('"%s" is not itself'%song )


		def _findSongs(self, callback, args):
			cdlPath = settings.GENSETTINGS.get('Paths', 'conducteurdelouange')
			if self._songPath.find(cdlPath) != -1:
				self._findSongsCDL(callback, args)
			else:
				self._findSongsLocal(callback, args)

		def _findSongsLocal(self, callback, args):
			extChant = settings.GENSETTINGS.get('Extentions', 'chant') \
						+ settings.GENSETTINGS.get('Extentions', 'chordpro')
			exclude = ['LSG', 'DAR', 'SEM', 'KJV', ]
			counter = 0
			if self._songPath:
				for root, _, files in os.walk(self._songPath):
					for fichier in files:
						path = os.path.join(root, fichier)
						if (path).find(os.sep + '.') == -1 \
								and fonc.get_ext(fichier) in extChant \
								and fichier not in exclude:
							newChant = elements.Chant( os.path.join(root, fichier)) # About 2/3 of the time
							# ~ newChant._replaceInText('raDieux', 'radieux')
							if newChant.exist(): # About 1/3 of the time
								self.add(newChant)
								self.addDictNums(newChant)
							if callback:
								callback(*args)
							counter += 1

		def _findSongsCDL(self, callback, args):
			counter = 0
			if self._songPath:
				for number in range(1,3000):
					url = '%s/%s'%(self._songPath, number)
					newChant = elements.Chant(url)
					self.add(newChant)
					self.addDictNums(newChant)
					if callback:
						callback(*args)
					counter += 1

		def _getStrings(self, paroles):
			try:
				i = cython.declare(cython.int) # pylint: disable=no-member
				size = cython.declare(cython.int) # pylint: disable=no-member
				nb_mots = cython.declare(cython.int) # pylint: disable=no-member
			except NameError:
				pass

			paroles = gestchant.netoyage_paroles(paroles) # Half the time

			list_mots = paroles.split()
			nb_mots = len(list_mots)-1

			outPut = [paroles.replace(' ', ';')] # First word list can be done faster with replace
			for size in range(1, self._sizeMax): # Half the time
				addList = [ ' '.join(list_mots[i:i+size+1]) for i in range(max(nb_mots-size, 0)) ]
				addList.append( ' '.join(list_mots[-size-1:]) )
				outPut.append(';'.join(addList))
			return outPut

		def __len__(self):
			return len(self._dicoLyrics)

		@property
		def maxCustomNumber(self):
			return self._maxCustomNumber

		def merge(self, others, receuilToSave=()):
			self._mergedDataBases += others
			self._merge(receuilToSave=receuilToSave)

		def _merge(self, update=False, receuilToSave=()):
			if self._mergedDataBases:
				tmpsRef = time.time()
				for dataBase in self._mergedDataBases:
					if update:
						dataBase.update()
					tmp = list(self.keys())
					for song in dataBase:
						if not song in tmp:
							self.add(song)
							if song.ref in receuilToSave:
								self.save((song,))
						else:
							tmp.remove(song)
				logging.info('Merged %d dataBase in %fs, %d songs' \
				%(len(self._mergedDataBases)+1, time.time()-tmpsRef, len(self)))

		def removeExtraDatabases(self, update=False):
			del self._mergedDataBases[:]
			if update:
				self.update()

		def save(self, songs=()):
			# We use a different xml lib here because it does not add carriage return on Windows for writes
			# There might be a way to use xml.etree.cElementTree that don't but have not figured out
			# xml.etree.cElementTree is faster at parsing so keep it for song parsing
			import lxml.etree as ET_write
			if not songs:
				songs = self.keys()
			for song in songs:
				ext = settings.GENSETTINGS.get('Extentions', 'chant')[0]
				if fonc.get_ext(song.chemin) != ext:
					path = classPaths.PATHS.songs
					fileName = '%s%d %s'%(song.songBook, song.hymnNumber, song.title)
				else:
					path = fonc.get_path(song.chemin)
					fileName = fonc.get_file_name(song.chemin)
				fileName = fonc.enleve_accents(fileName).strip(' ')
				fileName = re.sub(r'[\/?!,;:*<>"|]+', '', fileName)
				fileName = fileName.strip(' ').replace('  ', ' ')
				song.chemin = os.path.join(path, fileName) + ext
				try:
					tree = ET_write.parse(song.chemin)
					chant_xml = tree.getroot()
				except (OSError, IOError) as error:
					logging.debug(traceback.format_exc())
					chant_xml = ET_write.Element(song.etype)
				song.safeUpdateXML(chant_xml, 'lyrics', song.text)
				song.safeUpdateXML(chant_xml, 'title', song.title)
				song.safeUpdateXML(chant_xml, 'transpose', song.transpose)
				song.safeUpdateXML(chant_xml, 'capo', song.capo)
				song.safeUpdateXML(chant_xml, 'key', song.key)
				song.safeUpdateXML(chant_xml, 'turf_number', song.turfNumber)
				song.safeUpdateXML(chant_xml, 'hymn_number', song.hymnNumber)
				song.safeUpdateXML(chant_xml, 'author', song.author)
				song.safeUpdateXML(chant_xml, 'copyright', song.copyright)
				song.safeUpdateXML(chant_xml, 'ccli', song.ccli)
				song.safeUpdateXML(chant_xml, 'tags', song.tags)
				fonc.indent(chant_xml)

				tree = ET_write.ElementTree(chant_xml)
				tree.write(song.chemin, encoding="UTF-8", xml_declaration=True)
				song.resetDiapos()

				try:
					logging.info('Saved "%s"'%song.chemin)
				except UnicodeEncodeError:
					logging.info('Saved "%s"'%repr(song.chemin))
				self.add(song)

		def scanCDL(self):
			baseURL = settings.GENSETTINGS.get('Paths', 'conducteurdelouange')
			cdlData = DataBase(baseURL)
			for song in self:
				for cdlSong in cdlData:
					if song == cdlSong:
						song.tags = cdlSong.tags
						if not song.author:
							song.author = cdlSong.author
			self.save()
