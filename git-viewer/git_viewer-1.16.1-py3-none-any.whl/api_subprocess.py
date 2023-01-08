#!/usr/bin/env python3

import os
import subprocess
import enum
from collections.abc import Sequence


gitdir: 'str|None' = None
worktree: 'str|None' = None


CalledProcessError = subprocess.CalledProcessError
TimeoutExpired = subprocess.TimeoutExpired

class CommandError(Exception):

	def __init__(self, cmd: 'Sequence[str]', err: 'BaseException|str') -> None:
		exception: 'BaseException|None'
		returncode: 'int|None'
		error: 'str'
		lines: 'Sequence[str]|None' = None
		if isinstance(err, str):
			exception = None
			returncode = None
			error = err
		elif isinstance(err, CalledProcessError):
			exception = err
			returncode = err.returncode
			error = err.stderr.decode('utf-8') if err.stderr else str(err)
		elif isinstance(err, TimeoutExpired):
			exception = err
			returncode = None
			error = str(err)
			lines = err.stdout.decode('utf-8').splitlines() if err.stdout else []
		else:
			exception = err
			returncode = None
			error = str(err)

		super().__init__(err)
		self.cmd = cmd
		self.err = error
		self.returncode = returncode
		self.exception = exception
		self.lines = lines

	def executable_was_found(self) -> bool:
		return not isinstance(self.exception, FileNotFoundError)


class Returncode(enum.Enum):
	PROGRAM_NOT_FOUND = "program-not-found"


class Runner:

	encoding = "utf-8"
	decode_errors = "replace"

	timeout: 'float|None' = None

	RETURNCODE_PROGRAM_NOT_FOUND = Returncode.PROGRAM_NOT_FOUND

	def run(self, cmd: 'Sequence[str]', stdin: 'str|None' = None, check: bool = True) -> 'int|Returncode':
		"""
		Executes cmd without a shell and returns it's return code.
		Does not raise exceptions if check is False.
		Returns RETURNCODE_PROGRAM_NOT_FOUND if check is False and the program is not found.
		Raises CommandError if check is True and the program is not found or fails.

		cmd: list or tuple representing a command with it's arguments
		"""
		cmd = self._amend_command(cmd)

		stdin_bytes = stdin.encode(self.encoding) if stdin is not None else None

		try:
			p = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=check, input=stdin_bytes, timeout=self.get_timeout())
			return p.returncode
		except CalledProcessError as e:
			raise CommandError(cmd, e)
		except TimeoutExpired as e:
			raise CommandError(cmd, e)
		except FileNotFoundError as e:
			if check:
				raise CommandError(cmd, e)
			else:
				return self.RETURNCODE_PROGRAM_NOT_FOUND

	def run_and_get_output(self, cmd: 'Sequence[str]', *, ignore_returncode: bool = False) -> 'str':
		"""
		Executes cmd without a shell and returns stdout as unicode/str.
		Raises CommandError if program is not found or fails.

		cmd: list or tuple representing a command with it's arguments
		"""
		cmd = self._amend_command(cmd)

		try:
			p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=not ignore_returncode, timeout=self.get_timeout())
		except (CalledProcessError, FileNotFoundError, TimeoutExpired) as e:
			raise CommandError(cmd, e)
		out = p.stdout
		return out.decode(self.encoding, errors=self.decode_errors)

	def run_interactive(self, cmd: 'Sequence[str]') -> 'int|Returncode':
		"""
		Executes cmd without rediricting it's streams.
		Exit the main loop before calling this.
		Returns the return code or RETURNCODE_PROGRAM_NOT_FOUND if the program is not installed.
		Does not raise exceptions.

		cmd: list or tuple representing a command with it's arguments
		"""
		cmd = self._amend_command(cmd)

		try:
			p = subprocess.run(cmd, check=False)
			return p.returncode
		except FileNotFoundError:
			return self.RETURNCODE_PROGRAM_NOT_FOUND


	def _amend_command(self, cmd: 'Sequence[str]') -> 'Sequence[str]':
		if isinstance(cmd, str):
			return cmd

		cmd = list(cmd)
		if os.path.split(cmd[0])[1] == "git":
			if worktree:
				cmd.insert(1, '--work-tree')
				cmd.insert(2, worktree)
			if gitdir:
				cmd.insert(1, '--git-dir')
				cmd.insert(2, gitdir)
		return cmd

	def get_timeout(self) -> 'float|None':
		if self.timeout is None or self.timeout < 0:
			return None
		return self.timeout


if __name__ == '__main__':
	r = Runner()
	rc = r.run(["git", "status"])
	if rc == Runner.RETURNCODE_PROGRAM_NOT_FOUND:
		print("git is not installed")
	elif rc != 0:
		print("current working directory is not in a git repository")
	else:
		commit = r.run_and_get_output(["git", "log", "-1", "--pretty=format:%H"])
		print("the last commit was %s" % commit)
