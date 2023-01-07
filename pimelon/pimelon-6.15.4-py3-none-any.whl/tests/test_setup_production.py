# imports - standard imports
import getpass
import os
import pathlib
import re
import subprocess
import time
import unittest

# imports - module imports
from pine.utils import exec_cmd, get_cmd_output, which
from pine.config.production_setup import get_supervisor_confdir
from pine.tests.test_base import TestPineBase


class TestSetupProduction(TestPineBase):
	def test_setup_production(self):
		user = getpass.getuser()

		for pine_name in ("test-pine-1", "test-pine-2"):
			pine_path = os.path.join(os.path.abspath(self.pines_path), pine_name)
			self.init_pine(pine_name)
			exec_cmd(f"sudo pine setup production {user} --yes", cwd=pine_path)
			self.assert_nginx_config(pine_name)
			self.assert_supervisor_config(pine_name)
			self.assert_supervisor_process(pine_name)

		self.assert_nginx_process()
		exec_cmd(f"sudo pine setup sudoers {user}")
		self.assert_sudoers(user)

		for pine_name in self.pines:
			pine_path = os.path.join(os.path.abspath(self.pines_path), pine_name)
			exec_cmd("sudo pine disable-production", cwd=pine_path)

	def production(self):
		try:
			self.test_setup_production()
		except Exception:
			print(self.get_traceback())

	def assert_nginx_config(self, pine_name):
		conf_src = os.path.join(
			os.path.abspath(self.pines_path), pine_name, "config", "nginx.conf"
		)
		conf_dest = f"/etc/nginx/conf.d/{pine_name}.conf"

		self.assertTrue(self.file_exists(conf_src))
		self.assertTrue(self.file_exists(conf_dest))

		# symlink matches
		self.assertEqual(os.path.realpath(conf_dest), conf_src)

		# file content
		with open(conf_src) as f:
			f = f.read()

			for key in (
				f"upstream {pine_name}-melon",
				f"upstream {pine_name}-socketio-server",
			):
				self.assertTrue(key in f)

	def assert_nginx_process(self):
		out = get_cmd_output("sudo nginx -t 2>&1")
		self.assertTrue(
			"nginx: configuration file /etc/nginx/nginx.conf test is successful" in out
		)

	def assert_sudoers(self, user):
		sudoers_file = "/etc/sudoers.d/melon"
		service = which("service")
		nginx = which("nginx")

		self.assertTrue(self.file_exists(sudoers_file))

		if os.environ.get("CI"):
			sudoers = subprocess.check_output(["sudo", "cat", sudoers_file]).decode("utf-8")
		else:
			sudoers = pathlib.Path(sudoers_file).read_text()
		self.assertTrue(f"{user} ALL = (root) NOPASSWD: {service} nginx *" in sudoers)
		self.assertTrue(f"{user} ALL = (root) NOPASSWD: {nginx}" in sudoers)

	def assert_supervisor_config(self, pine_name, use_rq=True):
		conf_src = os.path.join(
			os.path.abspath(self.pines_path), pine_name, "config", "supervisor.conf"
		)

		supervisor_conf_dir = get_supervisor_confdir()
		conf_dest = f"{supervisor_conf_dir}/{pine_name}.conf"

		self.assertTrue(self.file_exists(conf_src))
		self.assertTrue(self.file_exists(conf_dest))

		# symlink matches
		self.assertEqual(os.path.realpath(conf_dest), conf_src)

		# file content
		with open(conf_src) as f:
			f = f.read()

			tests = [
				f"program:{pine_name}-melon-web",
				f"program:{pine_name}-redis-cache",
				f"program:{pine_name}-redis-queue",
				f"program:{pine_name}-redis-socketio",
				f"group:{pine_name}-web",
				f"group:{pine_name}-workers",
				f"group:{pine_name}-redis",
			]

			if not os.environ.get("CI"):
				tests.append(f"program:{pine_name}-node-socketio")

			if use_rq:
				tests.extend(
					[
						f"program:{pine_name}-melon-schedule",
						f"program:{pine_name}-melon-default-worker",
						f"program:{pine_name}-melon-short-worker",
						f"program:{pine_name}-melon-long-worker",
					]
				)

			else:
				tests.extend(
					[
						f"program:{pine_name}-melon-workerbeat",
						f"program:{pine_name}-melon-worker",
						f"program:{pine_name}-melon-longjob-worker",
						f"program:{pine_name}-melon-async-worker",
					]
				)

			for key in tests:
				self.assertTrue(key in f)

	def assert_supervisor_process(self, pine_name, use_rq=True, disable_production=False):
		out = get_cmd_output("supervisorctl status")

		while "STARTING" in out:
			print("Waiting for all processes to start...")
			time.sleep(10)
			out = get_cmd_output("supervisorctl status")

		tests = [
			r"{pine_name}-web:{pine_name}-melon-web[\s]+RUNNING",
			# Have commented for the time being. Needs to be uncommented later on. Pine is failing on travis because of this.
			# It works on one pine and fails on another.giving FATAL or BACKOFF (Exited too quickly (process log may have details))
			# "{pine_name}-web:{pine_name}-node-socketio[\s]+RUNNING",
			r"{pine_name}-redis:{pine_name}-redis-cache[\s]+RUNNING",
			r"{pine_name}-redis:{pine_name}-redis-queue[\s]+RUNNING",
			r"{pine_name}-redis:{pine_name}-redis-socketio[\s]+RUNNING",
		]

		if use_rq:
			tests.extend(
				[
					r"{pine_name}-workers:{pine_name}-melon-schedule[\s]+RUNNING",
					r"{pine_name}-workers:{pine_name}-melon-default-worker-0[\s]+RUNNING",
					r"{pine_name}-workers:{pine_name}-melon-short-worker-0[\s]+RUNNING",
					r"{pine_name}-workers:{pine_name}-melon-long-worker-0[\s]+RUNNING",
				]
			)

		else:
			tests.extend(
				[
					r"{pine_name}-workers:{pine_name}-melon-workerbeat[\s]+RUNNING",
					r"{pine_name}-workers:{pine_name}-melon-worker[\s]+RUNNING",
					r"{pine_name}-workers:{pine_name}-melon-longjob-worker[\s]+RUNNING",
					r"{pine_name}-workers:{pine_name}-melon-async-worker[\s]+RUNNING",
				]
			)

		for key in tests:
			if disable_production:
				self.assertFalse(re.search(key, out))
			else:
				self.assertTrue(re.search(key, out))


if __name__ == "__main__":
	unittest.main()
