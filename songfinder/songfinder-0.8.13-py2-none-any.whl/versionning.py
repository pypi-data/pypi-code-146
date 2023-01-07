# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import getpass
import codecs
import shutil
import logging
import traceback
try:
	import tkinter as tk
except ImportError:
	import Tkinter as tk
import os

try: # Windows only imports
	import win32con
	import win32api
except ImportError:
	pass

from songfinder import messages as tkMessageBox
from songfinder import fonctions as fonc
from songfinder import commandLine
from songfinder import inputFrame
import songfinder
from songfinder import guiHelper
from songfinder import classSettings as settings
from songfinder import __version__

#~ client = hglib.open( os.path.join(os.path.expanduser("~"), "Documents", "songFinderData") )
#~ logging.info(client.status())

COMMANDS = {'addAll':{'hg':['addr'], 'git': ['add', '-A']},\
			'pullUpdate':{'hg':['pull', '-u'], 'git': ['pull', '--rebase']},\
			'rebaseAbort':{'hg':['update', '-C'], 'git': ['rebase', '--abort']},\
			'resetHead':{'hg':['update', '-C'], 'git': ['reset', '--hard', 'origin/master']},\
			'configFile':{'hg':['hgrc'], 'git': ['config']},\
			'insecure':{'hg':['--insecure'], 'git': []},\
			'remote':{'hg':['default'], 'git': ['origin']},\
			'merge':{'hg':['merge'], 'git': ['merge']},\
			}

CLEUSB = {'USBEI', 'USBETIENNE'}

MERCURIAL_HGRC="""# example repository config (see 'hg help config' for more info)
[paths]
default = %s

# path aliases to other clones of this repo in URLs or filesystem paths
# (see 'hg help config.paths' for more info)
#
# default:pushurl = ssh://jdoe@example.net/hg/jdoes-fork
# my-fork         = ssh://jdoe@example.net/hg/jdoes-fork
# my-clone        = /home/jdoe/jdoes-clone

[auth]
sfData.prefix = %s
sfData.username = %s
sfData.password = %s

[ui]
# name and email (local to this repository, optional), e.g.
username = %s
"""

GIT_CONFIG="""[core]
	repositoryformatversion = 0
	filemode = false
	bare = false
	logallrefupdates = true
	ignorecase = true
[remote "origin"]
	url = https://%s:%s@%s
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
	remote = origin
	merge = refs/heads/master
[user]
	email = <>
	name = %s
"""

class AddRepo(object): # TODO integrate to repo class
	def __init__(self, paths, exe, screens=None, updateData=None):
		fenetre = tk.Toplevel()
		with guiHelper.SmoothWindowCreation(fenetre, screens=screens):
			fenetre.title("Clonage d'un dépôt")
			self._updateData = updateData
			self.paths = paths
			self.fenetre = fenetre
			self.__exe = exe
			self.__ping = commandLine.Ping('google.fr')
			self.__scm = commandLine.MyCommand(self.__exe)
			self.__scm.checkCommand()

			self.prog = tk.Label(fenetre, text="", justify='left')
			self.ok_button = tk.Button(fenetre, text='Cloner', command=self._cloneRepo)
			self.cancel_button = tk.Button(fenetre, text='Annuler', command=self._closeAddRepo)

			self._pathEntryFrame = inputFrame.entryField(fenetre, \
									packing=tk.LEFT, \
									text='Chemin', \
									width=60)
			self._userEntryFrame = inputFrame.entryField(fenetre, \
									packing=tk.LEFT, \
									text='Utilisateur', \
									width=30)
			self._passwordEntryFrame = inputFrame.entryField(fenetre, \
									packing=tk.LEFT, \
									text='Mot de passe', \
									width=30)

			self._pathEntryFrame.pack(side=tk.TOP, fill=tk.BOTH)
			self._userEntryFrame.pack(side=tk.TOP, fill=tk.BOTH)
			self._passwordEntryFrame.pack(side=tk.TOP, fill=tk.BOTH)

			self.ok_button.pack(side=tk.TOP)
			self.cancel_button.pack(side=tk.TOP)

			fenetre.bind_all("<KeyRelease-Return>", self._cloneRepo)

	def _closeAddRepo(self):
		if self.fenetre:
			self.fenetre.destroy()
			self.fenetre = None

	def _cloneRepo(self, event=0): # pylint: disable=unused-argument
		self.update_fen('Récupération des informations ...')
		repo = self._pathEntryFrame.get() # pylint: disable=no-member
		name = self._userEntryFrame.get() # pylint: disable=no-member
		mdp = self._passwordEntryFrame.get() # pylint: disable=no-member
		if not (repo and name and mdp):
			self.update_fen("    échec\n")
			tkMessageBox.showerror('Erreur', 'Erreur: les informations sont incomplètes')
		else:
			self.prog.pack(side=tk.TOP, fill=tk.BOTH)
			self.update_fen("    ok\nVerification de la connexion ...")
			if self.__ping.run() == 0:
				self.update_fen("    ok\n")
			else:
				self.update_fen("    échec\n")
				#https://epef@bitbucket.org/epef/data

			if repo:
				self.update_fen("Clonage du dépôt (ceci peut prendre quelques minutes) ...")
				shutil.rmtree(self.paths.root)
				os.makedirs(self.paths.root)
				os.chdir(self.paths.root)
				arrobase = repo.find('@')
				user = repo[repo.find('://')+3:arrobase]
				prefix = repo[arrobase+1:]
				fullrepo = repo[:arrobase] + ':' + mdp + repo[arrobase:]
				code, _, err = self.__scm.run( options=['clone'] \
											+ COMMANDS['insecure'][self.__exe] \
											+ [fullrepo, '.'] )
				try:
					self._makeHidden(os.path.join(self.paths.root, '.hg'))
					self._makeHidden(os.path.join(self.paths.root, '.hgignore'))
					self._makeHidden(os.path.join(self.paths.root, 'bitbucket-pipelines.yml'))
				except Exception: # pylint: disable=broad-except
					logging.warning('Failed to make file hidden\n:%s'%traceback.format_exc())
			if code != 0:
				self.update_fen("    échec\n")
				tkMessageBox.showerror('Erreur', 'Erreur: le clonage du dépôt à échoué\n'
												'Erreur %d:\n%s'%(code, err))
				self._closeAddRepo()
				settings.GENSETTINGS.set('Parameters', 'sync', False)
			else:
				if self.__exe == 'hg':
					configContent = MERCURIAL_HGRC%(repo, prefix, user, mdp, name)
				elif self.__exe == 'git':
					configContent = GIT_CONFIG%(user, mdp, prefix, name)
				configFilePath = os.path.join('.%s'%self.__exe, \
								COMMANDS['configFile'][self.__exe][0])
				with codecs.open(configFilePath, "w", encoding='utf-8') as configFile:
					configFile.write(configContent)
				self.update_fen("    ok\n")
				tkMessageBox.showinfo('Confirmation', 'Le dépôt à été cloné.')
				if self._updateData:
					self._updateData()
				self._closeAddRepo()
			os.chdir(songfinder.__chemin_root__)

	def update_fen(self, message):
		self.prog["text"] = fonc.safeUnicode(self.prog["text"].replace('...', '')) \
							+ fonc.safeUnicode(message)
		self.fenetre.update()
		self.fenetre.geometry("%dx%d"%(self.fenetre.winfo_reqwidth(), \
								self.fenetre.winfo_reqheight()))

	def _makeHidden(self, path):
		try:
			win32api.SetFileAttributes(path,win32con.FILE_ATTRIBUTE_HIDDEN)
		except NameError: # For Ubuntu
			pass

class Repo(object):
	def __init__(self, path, exe, papa=None, screens=None):
		self.__myOs = songfinder.__myOs__
		self.__papa = papa
		self.__path = path
		self.__screens = screens

		self.__exe = exe
		self.__scm = commandLine.MyCommand(self.__exe)
		self.__ping = commandLine.Ping('google.fr')
		self.__scm.checkCommand()
		self.__commitName = 'Song Finder v%s'%__version__
		self.__fen_recv = None

		self.__remotes = []
		self.__usbFound = []

	def __gui(self):
		if self.__showGui and not self.__fen_recv:
			self.__fen_recv = tk.Toplevel(self.__papa)
			with guiHelper.SmoothWindowCreation(self.__fen_recv, screens=self.__screens):
				self.__fen_recv.title("Reception/Envoi")
				self.__fen_recv.prog = tk.Label(self.__fen_recv, text="", justify='left')
				self.__fen_recv.prog.grid(sticky='w')

	def __update_fen(self, message):
		if self.__showGui and self.__fen_recv:
			message = fonc.safeUnicode(message)
			newText = fonc.safeUnicode(self.__fen_recv.prog["text"].replace('...', ''))
			exceList = set(self.__usbFound) | {'ok', 'échec', 'aucune'}
			if not set(message.split(' ')) & exceList:
				newText += '\n'
			newText += message
			newText = fonc.strip_perso(newText.replace('\n\n','\n'), '\n')
			self.__fen_recv.prog["text"] = newText
			self.__fen_recv.update()
			self.__fen_recv.geometry("%dx%d"%(self.__fen_recv.winfo_reqwidth(), \
											self.__fen_recv.winfo_reqheight()))
			self.__fen_recv.update()

	def __showError(self, message):
		self.__update_fen('    échec')
		tkMessageBox.showerror('Erreur', message)
		self.__closeAddRepo()
		return 2

	def __showInfo(self, message):
		self.__update_fen('    ok')
		if self.__showGui and self.__fen_recv:
			tkMessageBox.showinfo('Confirmation', message)
		self.__closeAddRepo()
		return 0

	def __closeAddRepo(self):
		os.chdir(songfinder.__chemin_root__)
		if self.__showGui and self.__fen_recv:
			self.__fen_recv.destroy()
			self.__fen_recv = None

	def __checkConnection(self):
		self.__update_fen('Vérification de la connexion ...')
		if self.__ping.run() == 0:
			self.__update_fen('    ok')
			self.__remotes.append(COMMANDS['remote'][self.__exe][0])
		else:
			self.__update_fen('    échec\n')

	def __getUSB(self):
		self.__update_fen('Recherche des clé usb ...')
		for key in CLEUSB:
			path = ''
			if self.__myOs == 'windows':
				getLetterCommand = commandLine.MyCommand('')
				getLetter = ('for /f %D in (\'wmic LogicalDisk get Caption^, '
							'VolumeName ^| find "{}"\') do %D'.format(key))
				driveLetter = getLetterCommand.run(options=getLetter)[1].strip('\r\n')[-2:]
				if driveLetter:
					path = driveLetter
			elif self.__myOs == 'ubuntu':
				path = os.path.join(os.sep, 'media', getpass.getuser(), key)
			if path:
				path = os.path.join(path, 'songfinder')
			if os.path.isdir(path):
				self.__remotes.append(path)
				self.__usbFound.append(key)

		if self.__usbFound:
			self.__update_fen(': ' + ' '.join(self.__usbFound))
		else:
			self.__update_fen('    aucune')

	def __getRemotes(self):
		if not self.__remotes:
			self.__checkConnection()
			#self.__getUSB()
			if self.__remotes == []:
				return self.__showError('La connection a échoué. Verifiez votre connexion à internet.')
		return 0

	def receive(self, send=False, showGui=True):
		self.__showGui = showGui
		self.__gui()
		if self.__getRemotes() == 2:
			return 2
		os.chdir(self.__path)
		self.__update_fen('Réception des modifications ...')
		# ~ code, out, err = self.__scm.run(options=['pull', self.__remotes[0], '&&', 'update'])
		code, out, err = self.__scm.run(options=COMMANDS['pullUpdate'][self.__exe] \
											+ [self.__remotes[0]])

		if out.find('no changes found') != -1 \
				or out.find('aucun changement trouv') != -1 \
				or out.find('Already up to date') != -1 \
				or out.find('Déjà à jour') != -1:
			if send:
				self.__update_fen("    ok")
			else:
				self.__showInfo('Rien à recevoir')
			return 1
		elif self.__exe =='hg' and code == 255:
			return self.__showError('Erreur: Impossible de recupérer les modifications.\nErreur %d:\n%s'\
									%(code, '\n'.join([out,err])))
		elif self.__exe =='hg' and code == 128:
			self.__closeAddRepo()
			return 0
		elif (out.find('other heads') != -1 or \
				out.find(' autre instantan') != -1 or \
				out.find('CONFLICT') != -1) and \
				tkMessageBox.askyesno('Erreur', 'Erreur: Impossible de recupérer les modifications.\n'
									'Erreur %d:\n%s\n'
									'Ceci peut être du au fait que vos modifications sont incompatibles '
									'avec les modifications faites par un autre utilisateur.'
									'Pour résoudre ce conflit vous devez annuler vos modifications '
									'et receptionner les modifications faites par l''autre utilisateurs.'
									'Voulez vous annuler vos modifications (ceci effacera tout vos changements.) ?'\
									%(code, '\n'.join([out,err]))):
			if self.__exe =='hg':
				code, out, err = self.__scm.run(options=COMMANDS['merge'][self.__exe])
				code, out, err = self.__scm.run(options=['resolve', '-t', 'internal:other', '--all'])
				code, out, err = self.__scm.run(options=['commit', '-m', '"%s merge"'%self.__commitName])
			elif self.__exe =='git':
				code, out, err = self.__scm.run(options=COMMANDS['rebaseAbort'][self.__exe])
				code, out, err = self.__scm.run(options=COMMANDS['resetHead'][self.__exe])
			if code != 0:
				return self.__showError('Erreur: la reception forcé à échoué\nErreur %d:\n%s'\
										%(code, '\n'.join([out,err])))
		elif code == 0:
			if send:
				self.__update_fen("    ok")
				return 0
			else:
				return self.__showInfo('Les modifications ont bien été recus.')
		return 0

	def send(self, what='all', showGui=True):
		self.__showGui = showGui
		self.__gui()
		if self.__getRemotes() == 2:
			return 2
		os.chdir(self.__path)
		returns = []
		errs = []
		self.__update_fen('Validation des modifications ...')
		if what == 'all':
			code, out, err = self.__scm.run(options=COMMANDS['addAll'][self.__exe])
			if not code:
				code, out, err = self.__scm.run(options=['commit', '-m', '"%s"'%self.__commitName])
		elif what:
			if self.__exe =='hg':
				code, out, err = self.__scm.run(options=['commit', '-I', what, '-m', '"%s"'%self.__commitName])
			elif self.__exe =='git':
				code, out, err = self.__scm.run(options=['add', what])
				if not code:
					code, out, err = self.__scm.run(options=['commit', '-m', '"%s"'%self.__commitName])

		if out.find('nothing changed') != -1 \
				or out.find('aucun changement') != -1 \
				or out.find('nothing to commit') != -1 \
				or out.find('rien à valider') != -1:
			self.__showInfo('Rien à envoyer')
			return 1
		elif code != 0:
			self.__update_fen("    échec\n")
			return self.__showError('Erreur: la validation a échoué.\nErreur %d:\n%s'\
									%(code, '\n'.join([out,err])))
		else:
			self.__update_fen('Envoi des modifications ...')
			receiveReturn = self.receive(send=True, showGui=showGui)
			if receiveReturn == 2:
				return 2
			for remote in self.__remotes:
				code, out, err = self.__scm.run(options=['push', remote])
				errs.append(err)
				returns.append(str(code))
			if returns == ['0']*len(self.__remotes):
				return self.__showInfo('Les modifications ont été envoyées sur : %s'\
							%', '.join(self.__remotes)) \
						or receiveReturn
			else:
				return self.__showError('Erreur %s:\n%s'%(' '.join(returns), '\n'.join(errs)))
