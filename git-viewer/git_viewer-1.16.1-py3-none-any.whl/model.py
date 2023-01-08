#!/usr/bin/env python

import os
import stat
import tempfile
import re
import shlex
import shutil
import gettext
import functools
import collections.abc
import typing
_ = gettext.gettext

from .api_subprocess import Runner, CommandError, TimeoutExpired
from .string_formatter import formatter
from .color_decoder import ColorDecoder
from . import utils
from . import settings
from .constants import *

if typing.TYPE_CHECKING:
	from .main import App


UrwidMarkup: 'typing.TypeAlias' = 'str|tuple[str, object]|list[object]'
LogLines: 'typing.TypeAlias' = 'list[tuple[str, str|None, str]]'
LinesOfUrwidMarkup: 'typing.TypeAlias' = 'list[UrwidMarkup]'


ALIGN_CHAR = "^"

#https://matthew-brett.github.io/curious-git/git_object_types.html
OBJECT_TYPE_COMMIT = "commit"
OBJECT_TYPE_TREE = "tree"
OBJECT_TYPE_BLOB = "blob"
OBJECT_TYPE_TAG = "tag"

FLAG_CUSTOM_FORMAT = "--custom-format"
FORMAT_PREFIX = "--pretty=format:"

title_untracked = _('New files, uncommitted and not checked in to index')
title_unstaged = _('Local uncommitted changes, not checked in to index')
title_unstaged_and_untracked = formatter.format(_('{title_unstaged} and {title_untracked:l}'), title_unstaged=title_unstaged, title_untracked=title_untracked)
title_staged   = _('Local changes checked in to index but not committed')
title_stashes_group = _('{number} stashes')
title_todo_log = _('TODO flags')
title_todo_details = _('{number} TODO flags')
title_referencedby = _('This commit is referenced by the following commits:')
title_commit = _("commit {hash_id}{refnames}")
pattern_refnames = _(" ({refnames})")
refnames_sep = _(", ")

error_no_unreachable_commits = _('no unreachable commits')

hint_timeout = _("Either speed up the command (e.g. in case of a grep ignoring untracked files can significantly reduce the amount of files to be searched - depending on the repository and the working directory) or change the timeout in the config file with `set log-view.timeout=<s>` or `set details-view.timeout=<s>` where <s> is the time in seconds or -1 to disable the timeout.")


# ---------- decorators ----------

class CommandFunction:

	def __init__(self,
		method: 'collections.abc.Callable[[LogModel, collections.abc.Sequence[str]], LogLines] | collections.abc.Callable[[DetailsModel, collections.abc.Sequence[str]], LinesOfUrwidMarkup]',
		arguments: str,
		description: str,
		settings: 'collections.abc.Sequence[str]',
	) -> None:
		self.method = method
		self.arguments = arguments
		self.description = description
		self.settings = settings
		functools.update_wrapper(self, method)

	@typing.overload
	def __call__(self, model: 'LogModel', args: 'collections.abc.Sequence[str]') -> 'LogLines':
		pass

	@typing.overload
	def __call__(self, model: 'DetailsModel', args: 'collections.abc.Sequence[str]') -> 'LinesOfUrwidMarkup':
		pass

	def __call__(self, model: 'typing.Any', args: 'collections.abc.Sequence[str]') -> 'typing.Any':
		return self.method(model, args)


def command_function(
	arguments: str,
	description: str,
	settings: 'collections.abc.Sequence[str]',
) -> 'collections.abc.Callable[[collections.abc.Callable[[LogModel, collections.abc.Sequence[str]], LogLines] | collections.abc.Callable[[DetailsModel, collections.abc.Sequence[str]], LinesOfUrwidMarkup]], CommandFunction]':

	def decorator(method: 'collections.abc.Callable[[LogModel, collections.abc.Sequence[str]], LogLines] | collections.abc.Callable[[DetailsModel, collections.abc.Sequence[str]], LinesOfUrwidMarkup]') -> CommandFunction:
		return CommandFunction(method, arguments=arguments, description=description, settings=settings)

	return decorator


# ---------- model classes ----------

class NameSpace:
	pass

class FileInfo:

	# original_fn: the file name as printed by git, with special characters encoded as three digit octal numbers
	# fn: the real file name

	__slots__ = ('fn', 'original_fn', 'object_id_before_left', 'object_id_before_right', 'object_id_after')

	def __init__(self, fn=None):
		self.fn = fn
		self.object_id_before_left = None
		self.object_id_before_right = None
		self.object_id_after = None

class LineInfo:
	__slots__ = ('linenumber_after', 'linenumber_before_right', 'linenumber_before_left',
		'formatted_linenumber_after', 'formatted_linenumber_before_right', 'formatted_linenumber_before_left',
		'is_modified')

	def __init__(self, lnno=None):
		self.linenumber_after = lnno
		self.linenumber_before_right = lnno
		self.linenumber_before_left = lnno

		self.formatted_linenumber_after = None
		self.formatted_linenumber_before_right = None
		self.formatted_linenumber_before_left = None

		self.is_modified = None

	def __repr__(self):
		args = ", ".join("%s" % getattr(self, a) for a in ('linenumber_after', 'linenumber_before_right', 'linenumber_before_left'))
		return "%s(%s)" % (type(self).__name__, args)


class Model(Runner):

	"""
	A command is a list of strings as expected by the subprocess library
	or a list of such commands. If several commands are given they are
	executed one after another and their outputs are concatenated.
	_append_cmd, _remove_cmd and _toggle_cmd operate on the last command only.
	"""

	CARRIAGE_RETURN = '' #r'\r'

	cmd: 'list[str]|list[list[str]]'

	# commands starting with this prefix are not executed as shell commands
	# but looked up in command_functions
	INTERNAL_FUNCTION_PREFIX = "$"

	command_functions: 'collections.abc.Mapping[str, CommandFunction]' = {}

	ignore_returncode = False


	# ------- generate output -------

	def get_lines(self):
		if self.are_several_commands(self.cmd):
			out = list()
			for cmd in self.cmd:
				out.extend(self._get_lines(cmd))
		else:
			cmd = self.cmd
			out = self._get_lines(cmd)

		return out

	def _get_lines(self, cmd):
		i = len(self.INTERNAL_FUNCTION_PREFIX)
		if cmd[0][:i] == self.INTERNAL_FUNCTION_PREFIX:
			fun = cmd[0][i:]
			try:
				fun = self.command_functions[fun]
			except KeyError as e:
				supported_commands =  ", ".join(key for key in sorted(self.command_functions.keys()))
				raise CommandError(cmd, "no such internal command %r, should be one of %s" % (fun, supported_commands))
			args = cmd[1:]
			return fun(self, args)

		return self.run_and_get_output(cmd, ignore_returncode=self.ignore_returncode).replace('\r', self.CARRIAGE_RETURN).splitlines()


	# ------- manipulate commands -------

	@classmethod
	def replace_in_cmd(cls, cmd, wildcard, value):
		if not cls.are_several_commands(cmd):
			cmd = [cmd]

		return [[value if x == wildcard else x for x in subcmd] for subcmd in cmd]

	@classmethod
	def replace_in_cmd_with_several(cls, cmd, wildcard, value):
		if not cls.are_several_commands(cmd):
			cmd = [cmd]

		out = []
		for subcmd in cmd:
			try:
				i = subcmd.index(wildcard)
			except ValueError:
				pass
			else:
				subcmd = subcmd[:i] + value + subcmd[i+1:]
			out.append(subcmd)

		return out

	@classmethod
	def replace_characters_in_cmd(cls, cmd, old, new, count=-1):
		"""
		count = -1: replace all occurences of old with new
		count > -1: replace the first count occurences of old with new
		            in the first argument where old appears of every subcommand
		"""
		if cls.are_several_commands(cmd):
			return [cls.replace_characters_in_subcmd(subcmd, old, new, count) for subcmd in cmd]
		else:
			return cls.replace_characters_in_subcmd(cmd, old, new, count)

	@classmethod
	def replace_characters_in_subcmd(cls, subcmd, old, new, count=-1):
		out = []
		unfinished = True
		for arg in subcmd:
			if unfinished and old in arg:
				arg = arg.replace(old, new, count)
				if count >= 0:
					unfinished = False
			out.append(arg)
		return out


	def replace_custom_format(self, cmd):
		if not self.are_several_commands(cmd):
			cmd = [cmd]

		out = []
		for subcmd in cmd:
			if "-g" in subcmd or "--walk-reflogs" in subcmd:
				subcmd = [FORMAT_PREFIX + self.fmt_reflog if w == FLAG_CUSTOM_FORMAT else w for w in subcmd]
				if subcmd[-1][:1] == '-':
					subcmd.append('HEAD@{0}')
			else:
				subcmd = [FORMAT_PREFIX + self.fmt_log if w == FLAG_CUSTOM_FORMAT else w for w in subcmd]
			out.append(subcmd)
		return out


	@staticmethod
	def are_several_commands(cmd):
		return isinstance(cmd[0], list)

	@classmethod
	def _append_cmd(cls, cmd, options):
		if cls.are_several_commands(cmd):
			cmd[-1].extend(options)
		else:
			cmd.extend(options)

	@classmethod
	def _remove_cmd(cls, cmd, options):
		if cls.are_several_commands(cmd):
			cmd = cmd[-1]
		for opt in options:
			while opt in cmd:
				cmd.remove(opt)

	@classmethod
	def _toggle_cmd(cls, cmd, options):
		if cls.are_several_commands(cmd):
			cmd = cmd[-1]

		count_added = 0
		count_removed = 0
		for opt in options:
			if opt in cmd:
				while opt in cmd:
					cmd.remove(opt)
					count_removed += 1
			else:
				cmd.append(opt)
				count_added += 1

		return count_added, count_removed

	@classmethod
	def _copy_command(cls, cmd):
		if cls.are_several_commands(cmd):
			return [list(c) for c in cmd]
		return list(cmd)


	# ------- branches ------

	_local_branches=None
	def get_local_branches(self):
		cls = type(self)
		if cls._local_branches is None:
			cls._local_branches = self._get_branches()
		return cls._local_branches

	_remote_branches=None
	def get_remote_branches(self):
		cls = type(self)
		if cls._remote_branches is None:
			cls._remote_branches = self._get_branches("--remote")
		return cls._remote_branches

	def _get_branches(self, arg=None):
		cmd = ["git", "branch"]
		if arg:
			cmd.append(arg)

		stdout = self.run_and_get_output(cmd).splitlines()
		return [ln[2:] for ln in stdout]

	@classmethod
	def clear_cache(cls):
		cls._local_branches = None
		cls._remote_branches = None


_cmd_grep_todo = ["git", "grep", "-n", "-I", "-E", '(#|%|"|//)TODO\>|\<TODO[:]', '--', settings.WC_GIT_ROOT]

class LogModel(Model):

	app: 'App'   # is set in App.__init__

	fmt_log    = "%Cred%h%Creset -^%C(yellow)%d%Creset %s %Cgreen(%cd) %C(bold blue)<%an>%Creset"
	fmt_reflog = "%Cred%h %Creset%C(yellow)%gD%Creset^%C(yellow)%d%Creset %gs %Cgreen(%cd) %C(bold blue)<%gn>%Creset"

	cmd_log = [["$stashes"], ["$todo"], ["$status"], ["git", "log", "--color", "--graph", "--date=relative", FLAG_CUSTOM_FORMAT, "--abbrev-commit"]]
	cmd_stash_list = ["git", "stash", "list", "--color", "--pretty=format:%C(cyan)* %Cred%gd%Creset - ^%s %Cgreen(%cr)%Creset", "--abbrev-commit"]
	cmd_unreachable = ["git", "fsck", "--unreachable"]
	cmd_grep_todo_quiet = Model.replace_in_cmd_with_several(_cmd_grep_todo, 'grep', ['grep', '--quiet'])

	timeout = 2

	@classmethod
	def append_cmd_log(cls, options):
		cmd = cls.cmd_log
		if cls.are_several_commands(cmd):
			cmd = cmd[-1]

		if "--no-walk" in options and "--graph" in cmd:
			cmd.remove("--graph")
		elif ("-g" in options or "--walk-reflogs" in options) and "--graph" in cmd:
			cmd.remove("--graph")

		while "--no-graph" in options:
			# remove all occurences of --graph in cmd
			while "--graph" in cmd:
				cmd.remove("--graph")

			# remove all occurences of --graph in options before --no-graph
			i_no_graph = options.index("--no-graph")
			del options[i_no_graph]
			while True:
				try:
					i = options.index("--graph", 0, i_no_graph)
				except ValueError:
					break
				else:
					del options[i]
					i_no_graph -= 1

		cmd.extend(options)

	@classmethod
	def remove_cmd_log(cls, options):
		cls._remove_cmd(cls.cmd_log, options)

	@classmethod
	def toggle_cmd_log(cls, options):
		return cls._toggle_cmd(cls.cmd_log, options)


	def remove_align_character(self):
		align_char = ALIGN_CHAR
		cls = type(self)
		self.fmt_log = cls.fmt_log.replace(align_char, "", 1)
		self.fmt_reflog = cls.fmt_reflog.replace(align_char, "", 1)

		self.cmd_log = self.replace_characters_in_cmd(cls.cmd_log, align_char, "", 1)
		self.cmd_stash_list = self.replace_characters_in_cmd(cls.cmd_stash_list, align_char, "", 1)

		self.ln_pattern = cls.ln_pattern.replace(align_char, "", 1)
		self.ln_pattern_error = cls.ln_pattern_error.replace(align_char, "", 1)
		self.ln_pattern_error_hint = cls.ln_pattern_error_hint.replace(align_char, "", 1)

	def restore_align_character(self):
		cls = type(self)
		self.fmt_log = cls.fmt_log
		self.fmt_reflog = cls.fmt_reflog

		self.cmd_log = cls.cmd_log
		self.cmd_stash_list = cls.cmd_stash_list

		self.ln_pattern = cls.ln_pattern
		self.ln_pattern_error = cls.ln_pattern_error
		self.ln_pattern_error_hint = cls.ln_pattern_error_hint

	WC_LOGENTRY = '{logentry}'
	ln_pattern = '* ^<color=default>' + WC_LOGENTRY
	ln_pattern_error = '^\n<color=%color.echo.error%>{err}</color>\nsee %{setting}%\ncmd = {cmd}\n{hint}'
	ln_pattern_error_hint = '\n{hint}\n\n'

	show_untracked = True
	untracked_files_as_separate_group = False

	show_stashed_changes = True   # NOTE: deprecated, not needed anymore since commit fab472fb25359739418fb9ef1a5ba5d9d2480653
	stashed_changes_reversed_order = False
	stashed_changes_group = None  # True|False|None. None = auto

	show_list_of_todo_flags = None  # True|False|None. None = auto
	show_list_of_todo_flags_on_timeout = False

	re_hex = r'[0-9A-F]'
	reo_hash_id = re.compile(r"(?:\b|(?<=m))(%(re_hex)s{7,40})\b" % dict(re_hex=re_hex), re.IGNORECASE)
	reo_stash_id = re.compile(r"stash@\{\d+\}", re.IGNORECASE)

	def get_lines(self) -> 'LogLines':
		"""return a list of 3-tuples (line, id, type), each representing one line"""
		# committed changes
		self.cmd = self.cmd_log
		self.cmd = self.replace_custom_format(self.cmd)
		try:
			lines = super().get_lines()
		except CommandError as e:
			log = self.format_command_error(e, setting='log-view.cmd.log')
		else:
			log = lines
			log = [(ln, self.extract_hash_id(ln), TYPE_OTHER) if isinstance(ln, str) else ln for ln in log]

		return log

	def format_command_error(self, e: CommandError, setting: str) -> 'LogLines':
		if isinstance(e.exception, TimeoutExpired):
			hint = self.ln_pattern_error_hint.format(hint=hint_timeout)
		else:
			hint = ''
		ln = self.ln_pattern_error.format(err=e.err, cmd=e.cmd, setting=setting, hint=hint)
		ln = utils.colored_str_to_markup(ln, self.app.define_color)
		return [(ln, None, TYPE_ERROR)]

	@command_function(
		arguments = '',
		description = _('Show untracked, unstaged and staged changes if existing'),
		settings = [
			'log-view.show-untracked',
			'log-view.show-untracked-as-separate-group',
			'log-view.line-pattern',
			'title.untracked',
			'title.unstaged',
			'title.untracked-and-unstaged',
			'title.staged',
			settings.COLOR_LOG_UNTRACKED,
			settings.COLOR_LOG_UNSTAGED,
			settings.COLOR_LOG_STAGED,
		],
	)
	def status(self, args: 'collections.abc.Sequence[str]') -> 'LogLines':
		# uncommitted changes
		if args:
			cmd = ['$status'] + list(args)
			raise CommandError(cmd, "status takes no arguments")

		self.cmd = ["git", "status", "--porcelain=v1"]
		status = super().get_lines()

		untracked = False
		unstaged = False
		staged = False

		# X: index
		# Y: work tree
		for ln in status:
			if ln[0] not in ' !?':
				staged = True
			if ln[1] not in ' !?':
				unstaged = True
			if ln[:2] == '??':
				untracked = True

		if not self.show_untracked:
			untracked = False

		log: 'LogLines' = []
		if staged:
			ln = self.format_log_entry(settings.COLOR_LOG_STAGED, title_staged)
			log.insert(0, (ln, ID_STAGED, TYPE_OTHER))

		if unstaged:
			if untracked and not self.untracked_files_as_separate_group:
				title = title_unstaged_and_untracked
				untracked = False
			else:
				title = title_unstaged
			ln = self.format_log_entry(settings.COLOR_LOG_UNSTAGED, title)
			log.insert(0, (ln, ID_UNSTAGED, TYPE_OTHER))

		if untracked:
			ln = self.format_log_entry(settings.COLOR_LOG_UNTRACKED, title_untracked)
			log.insert(0, (ln, ID_UNTRACKED, TYPE_OTHER))

		return log


	@command_function(
		arguments = '',
		description = _('Show stashed changes if existing'),
		settings = [
			'log-view.cmd.stash-list',
			'log-view.show-stashes',
			'log-view.show-stashes-as-group',
			'log-view.show-stashes-in-reverse-order',
			'log-view.line-pattern',
			'title.stashes',
			settings.COLOR_LOG_STASHES,
		],
	)
	def stashes(self, args: 'collections.abc.Sequence[str]') -> 'LogLines':
		if args:
			cmd = ['$stashes'] + list(args)
			raise CommandError(cmd, "stashes takes no arguments")

		log: 'LogLines' = []

		if self.show_stashed_changes:
			self.cmd = self.cmd_stash_list
			try:
				stashed = super().get_lines()
			except CommandError as e:
				log = self.format_command_error(e, setting='log-view.cmd.stash-list') + log
			else:
				if not stashed:
					pass
				elif self.stashed_changes_group or (self.stashed_changes_group is None and len(stashed) > 1):
					ln = formatter.format(title_stashes_group, number=len(stashed))
					ln = self.format_log_entry(settings.COLOR_LOG_STASHES, ln)
					log.insert(0, (ln, ID_STASHES_GROUP, TYPE_STASHED))
				else:
					log = self.format_stashed(stashed) + log

		return log


	@command_function(
		arguments = '',
		description = _('Show TODO flags'),
		settings = [
			'log-view.cmd.todo.grep',
			'log-view.show-todo-flags',
			'log-view.show-todo-flags-on-timeout',
			'log-view.line-pattern',
			'title.todo.log-view',
			settings.COLOR_LOG_TODO,
		],
	)
	def todo(self, args: 'collections.abc.Sequence[str]') -> 'LogLines':
		if args:
			cmd = ['$todo'] + list(args)
			raise CommandError(cmd, "todo takes no arguments")

		out_true: 'LogLines'
		out_true = [(self.format_log_entry(settings.COLOR_LOG_TODO, title_todo_log), ID_TODO, TYPE_TODO)]
		if self.show_list_of_todo_flags:
			return out_true
		elif self.show_list_of_todo_flags is False:
			return []

		root = get_git_root()
		self.cmd = self.replace_in_cmd(self.cmd_grep_todo_quiet, settings.WC_GIT_ROOT, root)
		try:
			lines = super().get_lines()
		except CommandError as e:
			if isinstance(e.exception, TimeoutExpired):
				if e.lines or self.show_list_of_todo_flags_on_timeout:
					# Tests indicate that e.exception.stdout => e.lines is always None. So this is never called.
					return out_true
				else:
					return []
			if e.returncode == 1:
				# no todo flags found
				return []
			return self.format_command_error(e, setting='details-view.cmd.todo.grep')
		else:
			return out_true


	command_functions = dict(
		status = status,
		stashes = stashes,
		todo = todo,
	)

	def format_log_entry(self, color, logentry):
		ln = self.ln_pattern.format(logentry=logentry)
		ln = utils.colored_str_to_markup(ln, self.app.define_color)
		return (color, ln)

	def format_stashed(self, stashed):
		if self.stashed_changes_reversed_order:
			stashed = reversed(stashed)

		log = list()
		for ln in stashed:
			stash_id = self.extract_stash_id(ln)
			log.append((ln, stash_id, TYPE_STASHED))

		return log

	@classmethod
	def extract_hash_id(cls, text):
		m = cls.reo_hash_id.search(text)
		if m:
			return m.group(0)
		else:
			return None

	@classmethod
	def extract_stash_id(cls, text):
		m = cls.reo_stash_id.search(text)
		if m:
			return m.group(0)
		else:
			return None

class StashesModel(LogModel):

	def get_lines(self) -> 'LogLines':
		self.cmd = self.cmd_stash_list
		try:
			stashed = Model.get_lines(self)
		except CommandError as e:
			return self.format_command_error(e, setting='log-view.cmd.stash-list')

		return self.format_stashed(stashed)

class UnreachableModel(LogModel):

	@classmethod
	def append_cmd_unreachable(cls, options):
		cls._append_cmd(cls.cmd_unreachable, options)

	def get_lines(self) -> 'LogLines':
		self.cmd = self.cmd_unreachable
		try:
			lines = Model.get_lines(self)
		except CommandError as e:
			return self.format_command_error(e, setting='log-view.cmd.unreachable')

		lines = [ln.split() for ln in lines]
		lines = [ln[2] for ln in lines if ln[0] == "unreachable" and ln[1] == "commit"]
		if not lines:
			err = error_no_unreachable_commits + "\n"
			ln = self.ln_pattern_error.format(err=err, cmd=self.cmd, setting='log-view.cmd.unreachable', hint='')
			ln = utils.colored_str_to_markup(ln, self.app.define_color)
			return [(ln, None, TYPE_ERROR)]

		original_cmd_log = self.cmd_log
		if self.are_several_commands(self.cmd_log):
			self.cmd_log = self._copy_command(self.cmd_log[-1])
		else:
			self.cmd_log = self._copy_command(self.cmd_log)
		self.append_cmd_log.__func__(self, ["--no-walk"])  # type: ignore [attr-defined]  # I am using this class method as an instance method in order to add '--no-walk' to this instance without changing the template in the class attribute
		self.cmd_log += lines
		log = LogModel.get_lines(self)
		self.cmd_log = original_cmd_log
		return log


class DetailsModel(Model):

	app: 'App'   # is set in App.__init__

	WC_HASH_ID = settings.WC_HASH_ID

	cmd_pattern = [
		#["git", "show", "--color", "--decorate", "--no-patch", WC_HASH_ID],
		["$commitheader", WC_HASH_ID],
		["$referencedby", WC_HASH_ID],
		["git", "show", "--color", "--decorate", "--format=format:", "--patch", WC_HASH_ID],
	]
	cmd_start_header_data = ["git", "show"]
	cmd_pattern_tag = ["git", "show", "--color", "--format=%ncommit %H%n%cd", "--no-patch", WC_HASH_ID, "--"]
	cmd_pattern_blob = ["git", "show", WC_HASH_ID]
	cmd_pattern_tree = ["git", "show", "--color", WC_HASH_ID]
	cmd_unstaged = ["git", "diff", "--color"]
	cmd_staged = cmd_unstaged + ["--cached"]
	cmd_untracked = ["$untracked"]
	cmd_todo = ["$todo"]
	cmd_grep_todo = _cmd_grep_todo
	cmd_pattern_stashed = [
			["git", "log", "-g", "-1", "--pretty=format:%C(yellow)%gD%Creset%ncommit %H%nAuthor: %an <%ae>%nDate:   %ad%w(,4,4)%n%+B%n%n", "--color", WC_HASH_ID],
			["git", "stash", "show", "--patch", "--color", WC_HASH_ID],
	]
	cmd_referencing_commits = [w for w in LogModel.cmd_log[-1] if w != "--graph"] + ["--branches"]

	timeout = 2

	log_format_options = (
		'--no-decorate',
		'--decorate',
		'--decorate-refs',
		'--decorate-refs-exclude',
		'--use-mailmap',

		'--date-order',
		'--author-date-order',
		'--topo-order',
		'--reverse',

		'--pretty',
		'--format',
		'--abbrev-commit',
		'--no-abbrev-commit',
		'--oneline',
		'--encoding',

		'--expand-tabs',
		'--no-expand-tabs',

		'--notes',
		'--no-notes',

		'--show-signature',

		'--relative-date',
		'--date',

		'--left-right',
	)

	_diff_commands = ['cmd_pattern', 'cmd_unstaged', 'cmd_staged', 'cmd_pattern_stashed', 'cmd_start_header_data']


	@classmethod
	def append_cmd_diff(cls, options):
		for cmd in cls._diff_commands:
			cmd = getattr(cls, cmd)
			cls._append_cmd(cmd, options)

	@classmethod
	def remove_cmd_diff(cls, options):
		for cmd in cls._diff_commands:
			cmd = getattr(cls, cmd)
			cls._remove_cmd(cmd, options)

	@classmethod
	def toggle_cmd_diff(cls, options):
		sum_added = 0
		sum_removed = 0
		for cmd in cls._diff_commands:
			cmd = getattr(cls, cmd)
			added, removed = cls._toggle_cmd(cmd, options)
			sum_added += added
			sum_removed += removed

		return sum_added, sum_removed


	@classmethod
	def append_cmd_log(cls, options):
		for opt in options:
			# values are given in the same argument, separated by a =
			key = opt.split('=',1)[0]
			if key in cls.log_format_options:
				cls.cmd_referencing_commits.append(opt)

	@classmethod
	def remove_cmd_log(cls, options):
		cls._remove_cmd(cls.cmd_referencing_commits, options)

	@classmethod
	def toggle_cmd_log(cls, options):
		return cls._toggle_cmd(cls.cmd_referencing_commits, options)


	def remove_align_character(self):
		self.insert_align_character = False
		self.fmt_log = LogModel.fmt_log.replace(ALIGN_CHAR, "", 1)
		self.cmd_referencing_commits = self.replace_characters_in_cmd(type(self).cmd_referencing_commits, ALIGN_CHAR, "", 1)

	def restore_align_character(self):
		self.insert_align_character = True
		self.fmt_log = LogModel.fmt_log
		self.cmd_referencing_commits = type(self).cmd_referencing_commits


	decoration_head_branch_sep = " -> "

	ln_pattern_referencedby = "* {logentry}"
	ln_pattern_untracked_in_unstaged_changes = _("untracked:<color=default> {filename}</color>")
	ln_pattern_untracked_in_separate_group = _("{filename}")

	pattern_user = _("{name} <{email}>")
	pattern_todo = _("<color=magenta>{filename}</color><color=cyan>:</color><color=green>{linenumber}</color><color=cyan>:</color>{todoflag}")

	linenumber_new = "{new}"
	linenumber_old = "{old}"
	linenumber_old_right = "{oldright}"
	linenumber_old_left = "{oldleft}"
	linenumber_sep = " "
	linenumber_off = ""
	linenumber_suffix = " "
	linenumber = linenumber_new
	min_line_number_width = 3

	re_ansi_esscape_sequence = "(\[[0-9;]*m)?"
	reo_start_new_file = re.compile(re_ansi_esscape_sequence + "diff (--git \"?a/(?P<fn1>.*?)\"? \"?b/|--cc \"?(?P<fn2>[^\"]*)\"?|--combined \"?(?P<fn3>[^\"]*))")
	reo_escape = re.compile(r'(\\[0-7][0-7][0-7])+')
	reo_object_id = re.compile(re_ansi_esscape_sequence + "index ((?P<beforeleft>[0-9a-f]+),)?(?P<before>[0-9a-f]+)\.\.(?P<after>[0-9a-f]+)")
	reo_filename = re.compile(re_ansi_esscape_sequence + "(\+\+\+|---) ")
	reo_linenumber = re.compile(re_ansi_esscape_sequence +
		r"(@@@ -(?P<start_before_left>\d+)(,(?P<number_before_left>\d+))? -(?P<start_before_right>\d+)(,(?P<number_before_right>\d+))?"
		r"|@@ -(?P<start_before>\d+)(,(?P<number_before>\d+))?) "
		r"\+(?P<start_after>\d+)(,(?P<number_after>\d+))? @@"
	)
	reo_normal_line_exists_after = re.compile(re_ansi_esscape_sequence + r"[+ ]")
	reo_normal_line_existed_before = re.compile(re_ansi_esscape_sequence + r"[- ]")
	reo_merge_line_exists_after = re.compile(re_ansi_esscape_sequence + r"[+ ][+ ]")
	reo_merge_line_existed_left = re.compile(re_ansi_esscape_sequence  + r"([- ][+ ]|--)")
	reo_merge_line_existed_right = re.compile(re_ansi_esscape_sequence + r"([+ ][- ]|--)")

	reo_hash_id = LogModel.reo_hash_id
	reo_url = re.compile(r'\S+?([.]\S+)+')

	untracked_relative = settings.RELATIVE_CWD
	todo_relative = settings.RELATIVE_NAME_ONLY

	# if linenumbers are activated: insert ALIGN_CHAR in every line which is not represented by a tuple
	insert_align_character = True

	# if insert_align_character is activated: auto_move_align_character for lines in diff (not commit message)
	indent_broken_code = False

	def __init__(self, hash_id, id_type):
		self.hash_id = hash_id
		self.id_type = id_type
		self.is_merge = None
		self.is_diff = True

	def set_cmd(self):
		self.setting_cmd = None
		if self.hash_id == ID_STAGED:
			self.cmd = self.cmd_staged
			self.setting_cmd = 'details-view.cmd.staged'
			self.title = [(settings.COLOR_TITLE, title_staged)]
		elif self.hash_id == ID_UNSTAGED:
			self.cmd = self.cmd_unstaged
			self.setting_cmd = 'details-view.cmd.unstaged'
			self.title = [(settings.COLOR_TITLE, title_unstaged)]
			self.show_untracked_in_unstaged = LogModel.show_untracked and not LogModel.untracked_files_as_separate_group
		elif self.hash_id == ID_UNTRACKED:
			self.cmd = self.cmd_untracked
			self.setting_cmd = 'details-view.cmd.untracked'
			self.title = [(settings.COLOR_TITLE, title_untracked)]
		elif self.hash_id == ID_TODO:
			self.cmd = self.cmd_todo
			self.setting_cmd = 'details-view.cmd.todo'
			self.title = None
		elif self.id_type == TYPE_STASHED:
			self.cmd = self.replace_in_cmd(self.cmd_pattern_stashed, self.WC_HASH_ID, self.hash_id)
			self.setting_cmd = 'details-view.cmd.stash'
			self.title = None
		else:
			try:
				self.object_type = get_object_type(self.hash_id)
			except CommandError as e:
				self.out.extend(self.format_command_error(e, _("get the object type")))
				self.object_type = None
			if self.object_type == OBJECT_TYPE_TAG:
				self.cmd = self.replace_in_cmd(self.cmd_pattern_tag, self.WC_HASH_ID, self.hash_id)
				self.setting_cmd = 'details-view.cmd.tag'
				self.title = None
				self.is_diff = False
			elif self.object_type == OBJECT_TYPE_TREE:
				self.cmd = self.replace_in_cmd(self.cmd_pattern_tree, self.WC_HASH_ID, self.hash_id)
				self.setting_cmd = 'details-view.cmd.tree'
				self.title = None
				self.is_diff = False
			elif self.object_type == OBJECT_TYPE_BLOB:
				self.cmd = self.replace_in_cmd(self.cmd_pattern_blob, self.WC_HASH_ID, self.hash_id)
				self.setting_cmd = 'details-view.cmd.blob'
				self.title = None
				self.is_diff = False
			else: # OBJECT_TYPE_COMMIT
				self.cmd = self.replace_in_cmd(self.cmd_pattern, self.WC_HASH_ID, self.hash_id)
				self.setting_cmd = 'details-view.cmd.commit'
				self.title = None

	def get_lines(self):
		"""
		returns a list of lines where each line is one of the following:
		- "text"
		- [("attr", "text")]  # urwid markup, must not contain tabs!
		- ("text", type)
		- ("text", type, auto_move_align_character)
		- ("text", TYPE_UNTRACKED, file_info)
		- ("text", TYPE_TODO, file_info, line_info)
		- ("text", TYPE_START_OF_FILE, file_info)
		- ("text", TYPE_NUMBERED_LINE, auto_move_align_character, line_info)
		"""
		self.object_type = None
		self.out = []
		self.set_cmd()
		out = self.out

		try:
			out.extend(super().get_lines())
		except CommandError as e:
			out.extend(self.format_command_error(e, setting=self.setting_cmd))
			return out

		if self.hash_id == ID_UNSTAGED and self.show_untracked_in_unstaged:
			cmd = self.cmd
			self.cmd = self.cmd_untracked
			try:
				untracked = super().get_lines()
			except CommandError as e:
				untracked = self.format_command_error(e, setting='details-view.cmd.untracked')
			else:
				pattern = self.ln_pattern_untracked_in_unstaged_changes
				untracked = self.format_untracked(pattern, untracked)
			finally:
				self.cmd = cmd

			if untracked:
				untracked.append("")
				out = untracked + out
				self.title = [(settings.COLOR_TITLE, title_unstaged_and_untracked)]
		elif self.hash_id == ID_UNTRACKED:
			pattern = self.ln_pattern_untracked_in_separate_group
			out = self.format_untracked(pattern, out)

		if self.is_diff:
			self.insert_linenumbers(out)

		if self.title:
			out.insert(0, self.title)
			out.insert(1, "")

		return out

	def format_untracked(self, pattern, filenames):
		path = lambda x: x
		if self.cmd_untracked == ['$untracked']:
			if self.untracked_relative == settings.RELATIVE_CWD:
				path = os.path.abspath

		for i in range(len(filenames)):
			fn = filenames[i]
			if fn.startswith('"') and fn.endswith('"'):
				fn = fn[1:-1]
			fn = self.decode_filename(fn)
			filenames[i] = fn

		return [([(settings.COLOR_DETAILS_UNTRACKED, utils.colored_str_to_markup(formatter.format(pattern, filename=fn), self.app.define_color))], TYPE_UNTRACKED, FileInfo(path(fn))) for fn in filenames]

	def format_command_error(self, e: CommandError, action: 'str|None' = None, setting: 'str|None' = None) -> 'LinesOfUrwidMarkup':
		cmd = "cmd = %r\n" % (e.cmd,)
		err = e.err
		if action:
			err += "\n" + _("while trying to {do_action}").format(do_action=action)
		if setting:
			err += "\n" + _("see %{setting}%").format(setting=setting)

		if isinstance(e.exception, TimeoutExpired):
			hint = hint_timeout
		else:
			hint = ""

		return [cmd, (err, TYPE_ERROR), hint]

	def insert_linenumbers(self, out):
		self.file_info = None
		ns = NameSpace()
		ns.out = out
		ns.look_for_hint = True
		for ns.i in range(len(ns.out)):
			ln = ns.out[ns.i]
			if isinstance(ln, tuple):
				ns.i += 1
			elif isinstance(ln, list):
				ns.i += 1
			elif ns.look_for_hint:
				self.insert_linenumbers__process_metainfo_line(ns)
			else:
				self.insert_linenumbers__process_content_line(ns)

	def insert_linenumbers__process_metainfo_line(self, ns):
		ns.line_info = None
		ln = ns.out[ns.i]
		m = self.reo_linenumber.match(ln)
		if m:
			if m.group('start_before') is not None:
				self.is_merge = False
				self._set_linenumber(ns, 'before_right', m, 'before')
				ns.linenumber_before_left = ns.linenumber_before_right
				ns.last_linenumber_before_left = ns.last_linenumber_before_right
				ns.fmt_linenumber_before_left = ns.fmt_linenumber_before_right

				ns.reo_line_exists_after = self.reo_normal_line_exists_after
				ns.reo_line_existed_left = self.reo_normal_line_existed_before
				ns.reo_line_existed_right = self.reo_normal_line_existed_before
				ns.i_align_character = 1
			else:
				self.is_merge = True
				self._set_linenumber(ns, 'before_right', m, 'before_right')
				self._set_linenumber(ns, 'before_left', m, 'before_left')

				ns.reo_line_exists_after = self.reo_merge_line_exists_after
				ns.reo_line_existed_left = self.reo_merge_line_existed_left
				ns.reo_line_existed_right = self.reo_merge_line_existed_right
				ns.i_align_character = 2

			self._set_linenumber(ns, 'after', m, 'after')

			ns.look_for_hint = False
		else:
			m = self.reo_object_id.match(ln)
			if m:
				self.file_info.object_id_before_left = m.group('beforeleft')
				self.file_info.object_id_before_right = m.group('before')
				self.file_info.object_id_after = m.group('after')
			elif self.reo_filename.match(ln):
				if self.file_info.fn != self.file_info.original_fn:
					ns.out[ns.i] = ns.out[ns.i].replace(self.file_info.original_fn, self.file_info.fn)


		if self.insert_align_character:
			ns.out[ns.i] = ALIGN_CHAR + ns.out[ns.i]
		if self.is_start_new_file(ln):
			if self.file_info.fn != self.file_info.original_fn:
				ns.out[ns.i] = ns.out[ns.i].replace(self.file_info.original_fn, self.file_info.fn)
			ns.out[ns.i] = (ns.out[ns.i], TYPE_START_OF_FILE, self.file_info)

	def _set_linenumber(self, ns, ns_name, match, re_name):
		linenumber = match.group('start_'+re_name)
		linenumber = int(linenumber)
		number_lines = match.group('number_'+re_name)
		if number_lines is None:
			last_linenumber = linenumber
		else:
			last_linenumber = linenumber + int(number_lines) - 1
		fmt = self.create_number_format(last_linenumber)
		setattr(ns, 'linenumber_'+ns_name, linenumber)
		setattr(ns, 'last_linenumber_'+ns_name, last_linenumber)
		setattr(ns, 'fmt_linenumber_'+ns_name, fmt)

	def create_number_format(self, last_linenumber):
		width = len(str(last_linenumber))
		width = max(width, self.min_line_number_width)
		return "%" + str(width) + "s"

	def insert_linenumbers__process_content_line(self, ns):
		ln = ns.out[ns.i]
		ns.line_info = LineInfo()
		ns.line_info.linenumber_after = ns.linenumber_after
		ns.line_info.linenumber_before_right = ns.linenumber_before_right
		ns.line_info.linenumber_before_left = ns.linenumber_before_left
		ns.line_info.is_modified = False
		no_increment = True

		if ns.reo_line_exists_after.match(ln):
			ns.line_info.formatted_linenumber_after = ns.fmt_linenumber_after % ns.linenumber_after
			ns.linenumber_after += 1
			no_increment = False
		else:
			ns.line_info.formatted_linenumber_after = ns.fmt_linenumber_after % ""
			ns.line_info.is_modified = True

		if ns.reo_line_existed_left.match(ln):
			ns.line_info.formatted_linenumber_before_left = ns.fmt_linenumber_before_left % ns.linenumber_before_left
			ns.linenumber_before_left += 1
			no_increment = False
		else:
			ns.line_info.formatted_linenumber_before_left = ns.fmt_linenumber_before_left % ""
			ns.line_info.is_modified = True

		if ns.reo_line_existed_right.match(ln):
			ns.line_info.formatted_linenumber_before_right = ns.fmt_linenumber_before_right % ns.linenumber_before_right
			ns.linenumber_before_right += 1
			no_increment = False
		else:
			ns.line_info.formatted_linenumber_before_right = ns.fmt_linenumber_before_right % ""
			ns.line_info.is_modified = True

		if no_increment:
			# The usual way of counting lines does not work.
			# This happens with --word-diff.
			# So I'm assuming each line is present in all versions.
			# Of course this is not always fullfilled.
			# But it's still better than giving each line the same number.
			ns.line_info.formatted_linenumber_after = ""
			ns.line_info.formatted_linenumber_before_left = ""
			ns.line_info.formatted_linenumber_before_right = ""
			ns.linenumber_after += 1
			ns.linenumber_before_left += 1
			ns.linenumber_before_right += 1
			if self.insert_align_character:
				ln = ALIGN_CHAR + ln
		elif self.insert_align_character:
			ln = self.insert_align_char(ln, ns.i_align_character)

		if ns.linenumber_after > ns.last_linenumber_after and ns.linenumber_before_right > ns.last_linenumber_before_right and ns.linenumber_before_left > ns.last_linenumber_before_left:
			ns.look_for_hint = True

		ln = (ln, TYPE_NUMBERED_LINE, self.indent_broken_code, ns.line_info)
		ns.out[ns.i] = ln

	@staticmethod
	def insert_align_char(ln, pos_align_character):
		n_escape = 0
		for m in ColorDecoder.reo_color_code.finditer(ln):
			i = m.start()
			pos = i - n_escape
			if pos >= pos_align_character:
				break
			n_escape += m.end() - i

		i_align_character = pos_align_character + n_escape
		return ln[:i_align_character] + ALIGN_CHAR + ln[i_align_character:]

	def is_start_new_file(self, ln):
		"""ln: str, possibly starting with one ansi escape sequence"""
		if isinstance(ln, list):
			return False
		m = self.reo_start_new_file.match(ln)
		if m:
			fn = m.group('fn1')
			if fn is None:
				fn = m.group('fn2')
				if fn is None:
					fn = m.group('fn3')

			original_fn = fn
			fn = self.decode_filename(fn)

			self.file_info = FileInfo()
			self.file_info.fn = fn
			self.file_info.original_fn = original_fn

			return True
		else:
			return False

	def decode_filename(self, fn: str) -> str:
		def replace(m: re.Match) -> str:
			original = m.group()
			ls = original.split('\\')
			assert ls[0] == ''
			ls = ls[1:]
			li = [int(n, base=8) for n in ls]
			return bytes(li).decode()

		if self.reo_escape.search(fn):
			try:
				fn = self.reo_escape.sub(replace, fn)
			except UnicodeDecodeError:
				pass

		return fn


	# ------- command functions ------

	todo_strip_indentation = True
	todo_only = False

	@command_function(
		arguments = '',
		description = _('Show a list of the TODO flags in the code'),
		settings = [
			'details-view.cmd.todo.grep',
			'details-view.todo.line-pattern',
			'title.todo.details-view',
		],
	)
	def todo(self, args: 'collections.abc.Sequence[str]') -> 'LinesOfUrwidMarkup':
		if args:
			cmd = ['$todo'] + list(args)
			raise CommandError(cmd, "todo takes no arguments")

		timeout_expired = None
		root = get_git_root()
		self.cmd = self.replace_in_cmd(self.cmd_grep_todo, settings.WC_GIT_ROOT, root)
		try:
			lines = super().get_lines()
		except CommandError as e:
			if isinstance(e.exception, TimeoutExpired) and e.lines:
				lines = e.lines
				timeout_expired = e
			elif e.returncode == 1:
				# no todo flags found
				lines = []
			return self.format_command_error(e, setting='details-view.cmd.todo.grep')

		out = []
		n = 0
		for ln in lines:
			ln = ln.replace('\t', self.app.DetailsView.TAB)
			try:
				filename, linenumber, todoflag = ln.split(':', 2)
				linenumber = int(linenumber)
			except ValueError:
				out.append(ln)
			else:
				filename = self.decode_filename(filename)
				if filename.startswith('"') and filename.endswith('"'):
					filename = filename[1:-1]
				absfilename = os.path.abspath(filename)

				if self.todo_relative == settings.RELATIVE_NAME_ONLY:
					filename = os.path.split(filename)[1]
				elif self.todo_relative == settings.RELATIVE_ROOT:
					filename = absfilename
				elif self.todo_relative == settings.RELATIVE_CWD:
					pass
				elif self.todo_relative == settings.RELATIVE_GIT:
					filename = os.path.relpath(absfilename, root)
				else:
					assert False, 'invalid value for self.todo_relative: %r' % self.todo_relative

				if self.todo_strip_indentation:
					todoflag = todoflag.strip()
				if self.todo_only:
					i = todoflag.index('TODO') + 4
					todoflag = todoflag[i:].lstrip(':').lstrip()

				markup = formatter.format(self.pattern_todo, filename=filename, linenumber=linenumber, todoflag=todoflag)
				markup = utils.colored_str_to_markup(markup, self.app.define_color)
				out.append((markup, TYPE_TODO, FileInfo(absfilename), LineInfo(linenumber)))
				n += 1

		out.insert(0, [(settings.COLOR_TITLE, title_todo_details.format(number=n))])
		out.insert(1, '')

		if timeout_expired:
			out.extend(self.format_command_error(timeout_expired, setting='details-view.cmd.todo.grep'))

		return out


	@command_function(
		arguments = 'CURRENT_COMMIT_HASH',
		description = _('Show a list of commits referencing the current commit'),
		settings = ['details-view.cmd.commit.referenced-by', 'details-view.commit.line-pattern-referenced-by'],
	)
	def referencedby(self, args: 'collections.abc.Sequence[str]') -> 'LinesOfUrwidMarkup':
		assert len(args) == 1
		hash_id = args[0]

		cmd = ["git", "show", "--format=%h", "--no-patch", hash_id]
		short_hash = self.run_and_get_output(cmd).strip()

		bak = self.cmd
		self.cmd = self.cmd_referencing_commits +  ["--grep", r"\<"+short_hash]
		self.cmd = self.replace_custom_format(self.cmd)
		try:
			out = super().get_lines()
		except CommandError as e:
			msg = "command for searching referencing commits failed:\ncmd = {e.cmd}\n{e.err}\nreturn code: {e.returncode}".format(e=e)
			return [(msg, TYPE_ERROR)]
		self.cmd = bak

		out = [(self.ln_pattern_referencedby.format(logentry=ln), TYPE_OTHER) for ln in out]
		if out:
			out.insert(0, title_referencedby)
			out.insert(0, "")

		return out


	@command_function(
		arguments = '',
		description = _('Return untracked files'),
		settings = ['details-view.show-untracked-relative-to'],
	)
	def untracked(self, args: 'collections.abc.Sequence[str]') -> 'LinesOfUrwidMarkup':
		assert len(args) == 0

		self.cmd = ["git", "status", "--porcelain=v1"]
		status = super().get_lines()
		root = get_git_root()

		files = []

		# X: index
		# Y: work tree
		for ln in status:
			if ln[:2] == '??':
				fn = ln[3:]
				if self.untracked_relative == settings.RELATIVE_ROOT or self.untracked_relative == settings.RELATIVE_CWD:
					fn = os.path.join(root, fn)
					if self.untracked_relative == settings.RELATIVE_CWD:
						fn = os.path.relpath(fn)
				files.append(fn)

		return files


	indent_body = _("    ")

	@command_function(
		arguments = 'CURRENT_COMMIT_HASH',
		description = _('Show the meta info of the current commit (hash, branch, tag, author, committer, date, message)'),
		settings = [
			'details-view.cmd.commit.header-data',
			'details-view.commit.user-pattern',
			'title.commit.refnames.head-branch-sep',
			settings.COLOR_TITLE,
			settings.COLOR_DECORATION_HEAD,
			settings.COLOR_DECORATION_HEAD_BRANCH_SEP,
			settings.COLOR_DECORATION_BRANCH_LOCAL,
			settings.COLOR_DECORATION_BRANCH_REMOTE,
			settings.COLOR_DECORATION_TAG,
		],
	)
	def commitheader(self, args: 'collections.abc.Sequence[str]') -> 'LinesOfUrwidMarkup':
		assert len(args) == 1
		hash_id = args[0]

		out: 'LinesOfUrwidMarkup' = []
		values = self.get_commit_header_data(hash_id)
		if values is None:
			return []
		refnames = values.pop('refnames')
		markup_refnames: 'str|list[object]|tuple[str, object]'
		if refnames:
			markup_refnames = utils.replace_to_markup(refnames, ', ', refnames_sep, markup_function=self.markup_deco)
			markup_refnames = utils.replace_to_markup(pattern_refnames, '{refnames}', markup_refnames)
		else:
			markup_refnames = ""

		title = title_commit.format(refnames='{refnames}', **values)
		markup_title = utils.replace_to_markup(title, '{refnames}', markup_refnames)
		markup_title = [(settings.COLOR_TITLE, markup_title)]
		out.append(markup_title)
		self.append_author_committer(out, values)
		out.append("")
		out.append(self.indent_body + values["subject"])
		body = values["body"].rstrip()
		if body:
			out.append("")
			out.append(self.indent_body + body)
		return out

	def get_commit_header_data(self, hash_id):
		key_fmt = ">>> %s:"
		keys = (
			("hash_id", "%H"),
			("refnames", "%D"),
			("subject", "%s"),
			("committer_name", "%cn",),
			("committer_email", "%ce",),
			("committer_date", "%cd",),
			("author_name", "%an",),
			("author_email", "%ae",),
			("author_date", "%ad",),
			("body", "%b"),
			("EOF", "") # ignore trailing newline while ensuring that body is added to values
		)
		fmt = "\n".join((key_fmt % key) + "\n" + wc for key,wc in keys)

		self.cmd = self.cmd_start_header_data + ["--no-patch", "--format="+fmt, hash_id]
		try:
			lines = super().get_lines()
		except CommandError as e:
			self.out.extend(self.format_command_error(e, setting='details-view.cmd.commit.header-data'))
			return None

		values = {}
		current_key = None
		next_key_index = 0
		for ln in lines:
			if next_key_index < len(keys) and ln == key_fmt % keys[next_key_index][0]:
				current_key = keys[next_key_index][0]
				next_key_index += 1
			else:
				if current_key not in values:
					values[current_key] = ln
				else:
					values[current_key] += "\n" + ln

		return values

	def append_author_committer(self, out, values):
		fmt = self.pattern_user
		author = fmt.format(name=values['author_name'], email=values['author_email'])
		committer = fmt.format(name=values['committer_name'], email=values['committer_email'])
		author_date = values['author_date']
		committer_date = values['committer_date']

		align_char = ALIGN_CHAR if self.insert_align_character else ""

		t = []
		if author == committer:
			t.append((_("Author/Committer"), align_char + author))
		else:
			t.append((_("Author"), align_char + author))

		if author_date != committer_date:
			t.append((_("Author Date"), align_char + author_date))

		if committer != author:
			t.append((_("Committer"), align_char + committer))

		if committer_date == author_date:
			t.append((_("Date"), align_char + author_date))
		else:
			t.append((_("Committer Date"), align_char + committer_date))

		containing_tag = get_containing_tag(values['hash_id'], exclusive=False)
		if containing_tag:
			t.append((_("Released in"), containing_tag))

		for ln in utils.format_table(t, fmt=['%s:']):
			ln = utils.colored_str_to_markup(ln, define_color=self.app.define_color)
			# wrap line in a tuple so that ALIGN_CHAR is not added again
			ln = (ln, None)
			out.append(ln)

	def markup_deco(self, decoration):
		HEAD_SEP = " -> "
		i = decoration.find(HEAD_SEP)
		if i >= 0:
			head = decoration[:i]
			sep = self.decoration_head_branch_sep
			i += len(HEAD_SEP)
			branch = decoration[i:]
			return [(settings.COLOR_DECORATION_HEAD, head), (settings.COLOR_DECORATION_HEAD_BRANCH_SEP, sep), (settings.COLOR_DECORATION_BRANCH_LOCAL, branch)]

		if decoration.startswith("tag: "):
			return (settings.COLOR_DECORATION_TAG, decoration)

		if decoration in self.get_local_branches():
			return (settings.COLOR_DECORATION_BRANCH_LOCAL, decoration)

		if decoration in self.get_remote_branches():
			return (settings.COLOR_DECORATION_BRANCH_REMOTE, decoration)

		return decoration


	command_functions = dict(
		referencedby = referencedby,
		untracked = untracked,
		commitheader = commitheader,
		todo = todo,
	)


class DiffModel(DetailsModel):

	cmd = ['git', 'diff', '--color']

	_diff_commands = ['cmd']

	# with --exit-code (implied by --no-index) return code 1 does not mean error but file changed
	ignore_returncode = True

	def __init__(self, args):
		self.hash_id = None
		self.id_type = None
		self.title = None

		self.args = args
		self.is_diff = True

		self.is_merge = None

	def set_cmd(self):
		self.setting_cmd = "details-view.cmd.diff"
		self.cmd = type(self).cmd + self.args



# ---------- modifiers ----------

def append_cmd_log(log_args):
	LogModel.append_cmd_log(log_args)
	DetailsModel.append_cmd_log(log_args)

def remove_cmd_log(log_args):
	LogModel.remove_cmd_log(log_args)
	DetailsModel.remove_cmd_log(log_args)

def toggle_cmd_log(log_args):
	sum_added = 0
	sum_removed = 0
	for cls in (LogModel, DetailsModel):
		added, removed = cls.toggle_cmd_log(log_args)
		sum_added += added
		sum_removed += removed

	return sum_added, sum_removed


def append_cmd_unreachable(unreachable_args):
	UnreachableModel.append_cmd_unreachable(unreachable_args)


def append_cmd_diff(diff_args):
	DetailsModel.append_cmd_diff(diff_args)
	DiffModel.append_cmd_diff(diff_args)

def remove_cmd_diff(diff_args):
	DetailsModel.remove_cmd_diff(diff_args)
	DiffModel.remove_cmd_diff(diff_args)

def toggle_cmd_diff(log_args):
	sum_added = 0
	sum_removed = 0
	for cls in (DetailsModel, DiffModel):
		added, removed = cls.toggle_cmd_diff(log_args)
		sum_added += added
		sum_removed += removed

	return sum_added, sum_removed


# ---------- getters ----------

def get_containing_tag(hash_id: str, exclusive: bool) -> 'str|None':
	'''
	Return the first tag containing hash_id.
	Prereleases are ignored if there is a real release
	because --sort version:refname seems to sort prereleases after the real release.
	'''
	cmd = ["git", "tag", "--list", "--contains", hash_id, "--sort", "version:refname"]
	out = Runner().run_and_get_output(cmd)
	out = out.rstrip()
	lines = out.splitlines()
	if exclusive:
		for tag in lines:
			if is_same_commit(tag, hash_id):
				continue
			return tag
		return None

	if lines:
		return lines[0]
	else:
		return None

def get_last_tag(hash_id, exclusive):
	if exclusive:
		hash_id = "%s^" % hash_id
	cmd = ["git", "describe", "--abbrev=0", hash_id]
	try:
		out = Runner().run_and_get_output(cmd)
	except CommandError:
		return None

	out = out.rstrip()
	return out

def is_same_commit(rev1, rev2):
	return get_commit_hash(rev1) == get_commit_hash(rev2)

def get_commit_hash(revision):
	# show does not work because it shows the annotation for tags
	cmd = ["git", "log", "-1", "--pretty=format:%H", revision, "--"]
	out = Runner().run_and_get_output(cmd)
	out = out.rstrip()
	return out

def get_object_type(hash_id):
	cmd = ["git", "cat-file", "-t", hash_id]
	out = Runner().run_and_get_output(cmd)
	out = out.rstrip()
	return out

def get_git_version():
	cmd = ["git", "--version"]
	try:
		out = Runner().run_and_get_output(cmd)
	except CommandError:
		return None

	out = out.rstrip()
	return out

def get_git_root():
	cmd = ["git", "rev-parse", "--show-toplevel"]
	try:
		out = Runner().run_and_get_output(cmd)
	except CommandError:
		return None

	out = out.rstrip()
	return out

def get_relative_path(path):
	'''
	path: a path relative to the git root directory
	returns: a path relative to the current working directory
	'''
	if os.path.isabs(path):
		return path
	root = get_git_root()
	cwd = os.getcwd()
	cwd = os.path.relpath(cwd, root) + os.sep
	return os.path.relpath(path, cwd)

def get_current_branch() -> 'str|None':
	'''
	returns None in detached HEAD state
	'''
	cmd = ['git', 'symbolic-ref', '--short', 'HEAD']

	try:
		return Runner().run_and_get_output(cmd).rstrip()
	except CommandError:
		return None


# ---------- opener ----------

def initattr(obj, name, value):
	if hasattr(obj, name):
		return
	setattr(obj, name, value)

class Opener:

	EDITOR_AUTO = 'auto'

	default_editor = EDITOR_AUTO

	def __init__(self):
		settings
		self._map = {}
		self.add_editor("vi", linenumber="+{ln}", readonly="-R")
		self.add_editor("vim", linenumber="+{ln}", readonly="-R")
		self.add_editor("nano", linenumber="+{ln}", readonly="-v")

	def add_editor(self, name, command=None, *, linenumber="", readonly=""):
		if not command:
			command = name
		self._map[command] = name
		setattr(self,  "editor_%s_command" % name, command)
		initattr(self, "editor_%s_linenumber" % name, linenumber)
		initattr(self, "editor_%s_readonly" % name, readonly)
		settings.settings["editor.%s.command" % name] = ("app.model.opener.editor_%s_command" % name, str, _("the value of the EDITOR environment variable which activates the corresponding editor settings"))
		settings.settings["editor.%s.linenumber" % name] = ("app.model.opener.editor_%s_linenumber" % name, str, _("a command line argument which is added if a specific line shall be selected, the wildcard {ln} specifies the line number"))
		settings.settings["editor.%s.readonly" % name] = ("app.model.opener.editor_%s_readonly" % name, str, _("a command line argument which is added if a file shall be opened read only"))

	def get_editor(self):
		cmd = os.environ.get('EDITOR', None)
		if cmd:
			name = self._map.get(cmd, None)
			if name is None:
				# in case EDITOR is an absolute path
				name = self._map.get(os.path.split(cmd)[1], None)
			if name is None:
				# in case EDITOR contains flags
				name = self._map.get(shlex.split(cmd)[0], None)
			if name is None:
				# in case EDITOR contains flags and is an absolute path
				name = self._map.get(os.path.split(shlex.split(cmd)[0])[1], None)
		else:
			name = self.get_default_editor_name()
			cmd = self.get_editor_argument(name, "command")
			assert cmd
		return name, cmd

	def get_default_editor_name(self) -> str:
		if self.default_editor != self.EDITOR_AUTO:
			return self.default_editor

		editors = ['vim', 'vi', 'nano']
		for ed in editors:
			if shutil.which(ed):
				return ed

		return 'vi'

	def get_editor_argument(self, editor_name, argument_name):
		return getattr(self, "editor_%s_%s" % (editor_name, argument_name), "")

	def open_old_version_in_editor(self, fn, commit, object_id, which, line_number):
		fn = os.path.split(fn)[1]
		basename,ext = os.path.splitext(fn)
		tmpfn = "{fn}@{which}-{commit}{ext}".format(fn=basename, which=which, commit=commit, ext=ext)
		runner = Runner()
		with tempfile.TemporaryDirectory() as tmpdir:
			tmpfn = os.path.join(tmpdir, tmpfn)
			with open(tmpfn, 'wt') as f:
				cmd = ['git', 'show', object_id]
				content = runner.run_and_get_output(cmd)
				f.write(content)
			os.chmod(tmpfn, stat.S_IREAD)
			self.open_file_in_editor(f.name, line_number, read_only=True)

	def open_file_in_editor(self, fn, line_number, read_only=False, create_dirs=False):
		if not os.path.exists(fn):
			if create_dirs:
				path = os.path.split(os.path.abspath(fn))[0]
				os.makedirs(path, exist_ok=True)
			else:
				raise FileNotFoundError(fn)
		if line_number == 0:
			line_number = 1
		runner = Runner()
		editor_name, editor_cmd = self.get_editor()
		cmd = shlex.split(editor_cmd)
		if line_number is not None:
			arg = self.get_editor_argument(editor_name, "linenumber").format(ln=line_number)
			if arg:
				cmd.append(arg)
		if read_only:
			arg = self.get_editor_argument(editor_name, "readonly")
			if arg:
				cmd.append(arg)
		cmd.append(fn)
		runner.run_interactive(cmd)

	def check_editor(self):
		editor_name, cmd = self.get_editor()
		exe = shlex.split(cmd)[0]
		which = shutil.which(exe)
		if not which:
			if editor_name is None:
				editor_name = _("<unknown editor>")
			return _("cannot open editor {editor_name}, no such executable {exe!r}").format(exe=exe, editor_name=editor_name)
	
		return None


opener = Opener()
open_old_version_in_editor = opener.open_old_version_in_editor
open_file_in_editor = opener.open_file_in_editor
check_editor = opener.check_editor


if __name__ == '__main__':
	log = LogModel()
	for ln in log.get_lines():
		print(ln)
