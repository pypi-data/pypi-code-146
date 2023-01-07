# imports - standard imports
import getpass
import json
import os
import shutil
import subprocess
import sys
import traceback
import unittest

# imports - module imports
from pine.utils import paths_in_pine, exec_cmd
from pine.utils.system import init
from pine.pine import Pine

PYTHON_VER = sys.version_info

MELON_BRANCH = "version-6-hotfix"
if PYTHON_VER.major == 3:
	if PYTHON_VER.minor >= 10:
		MELON_BRANCH = "develop"


class TestPineBase(unittest.TestCase):
	def setUp(self):
		self.pines_path = "."
		self.pines = []

	def tearDown(self):
		for pine_name in self.pines:
			pine_path = os.path.join(self.pines_path, pine_name)
			pine = Pine(pine_path)
			mariadb_password = (
				"travis"
				if os.environ.get("CI")
				else getpass.getpass(prompt="Enter MariaDB root Password: ")
			)

			if pine.exists:
				for site in pine.sites:
					subprocess.call(
						[
							"pine",
							"drop-site",
							site,
							"--force",
							"--no-backup",
							"--root-password",
							mariadb_password,
						],
						cwd=pine_path,
					)
				shutil.rmtree(pine_path, ignore_errors=True)

	def assert_folders(self, pine_name):
		for folder in paths_in_pine:
			self.assert_exists(pine_name, folder)
		self.assert_exists(pine_name, "apps", "melon")

	def assert_virtual_env(self, pine_name):
		pine_path = os.path.abspath(pine_name)
		python_path = os.path.abspath(os.path.join(pine_path, "env", "bin", "python"))
		self.assertTrue(python_path.startswith(pine_path))
		for subdir in ("bin", "lib", "share"):
			self.assert_exists(pine_name, "env", subdir)

	def assert_config(self, pine_name):
		for config, search_key in (
			("redis_queue.conf", "redis_queue.rdb"),
			("redis_socketio.conf", "redis_socketio.rdb"),
			("redis_cache.conf", "redis_cache.rdb"),
		):

			self.assert_exists(pine_name, "config", config)

			with open(os.path.join(pine_name, "config", config)) as f:
				self.assertTrue(search_key in f.read())

	def assert_common_site_config(self, pine_name, expected_config):
		common_site_config_path = os.path.join(
			self.pines_path, pine_name, "sites", "common_site_config.json"
		)
		self.assertTrue(os.path.exists(common_site_config_path))

		with open(common_site_config_path) as f:
			config = json.load(f)

		for key, value in list(expected_config.items()):
			self.assertEqual(config.get(key), value)

	def assert_exists(self, *args):
		self.assertTrue(os.path.exists(os.path.join(*args)))

	def new_site(self, site_name, pine_name):
		new_site_cmd = ["pine", "new-site", site_name, "--admin-password", "admin"]

		if os.environ.get("CI"):
			new_site_cmd.extend(["--mariadb-root-password", "travis"])

		subprocess.call(new_site_cmd, cwd=os.path.join(self.pines_path, pine_name))

	def init_pine(self, pine_name, **kwargs):
		self.pines.append(pine_name)
		melon_tmp_path = "/tmp/melon"

		if not os.path.exists(melon_tmp_path):
			exec_cmd(
				f"git clone https://github.com/amonak/melon -b {MELON_BRANCH} --depth 1 --origin upstream {melon_tmp_path}"
			)

		kwargs.update(
			dict(
				python=sys.executable,
				no_procfile=True,
				no_backups=True,
				melon_path=melon_tmp_path,
			)
		)

		if not os.path.exists(os.path.join(self.pines_path, pine_name)):
			init(pine_name, **kwargs)
			exec_cmd(
				"git remote set-url upstream https://github.com/amonak/melon",
				cwd=os.path.join(self.pines_path, pine_name, "apps", "melon"),
			)

	def file_exists(self, path):
		if os.environ.get("CI"):
			return not subprocess.call(["sudo", "test", "-f", path])
		return os.path.isfile(path)

	def get_traceback(self):
		exc_type, exc_value, exc_tb = sys.exc_info()
		trace_list = traceback.format_exception(exc_type, exc_value, exc_tb)
		return "".join(str(t) for t in trace_list)
