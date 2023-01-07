# imports - standard imports
import json
import os
import subprocess
import unittest

# imports - third paty imports
import git

# imports - module imports
from pine.utils import exec_cmd
from pine.app import App
from pine.tests.test_base import MELON_BRANCH, TestPineBase
from pine.pine import Pine


# changed from melontheme because it wasn't maintained and incompatible,
# chat app & wiki was breaking too. hopefully melon_docs will be maintained
# for longer since docs.monakerp.com is powered by it ;)
TEST_MELON_APP = "melon_docs"


class TestPineInit(TestPineBase):
	def test_utils(self):
		self.assertEqual(subprocess.call("pine"), 0)

	def test_init(self, pine_name="test-pine", **kwargs):
		self.init_pine(pine_name, **kwargs)
		app = App("file:///tmp/melon")
		self.assertTupleEqual(
			(app.mount_path, app.url, app.repo, app.org),
			("/tmp/melon", "file:///tmp/melon", "melon", "melon"),
		)
		self.assert_folders(pine_name)
		self.assert_virtual_env(pine_name)
		self.assert_config(pine_name)
		test_pine = Pine(pine_name)
		app = App("melon", pine=test_pine)
		self.assertEqual(app.from_apps, True)

	def basic(self):
		try:
			self.test_init()
		except Exception:
			print(self.get_traceback())

	def test_multiple_pines(self):
		for pine_name in ("test-pine-1", "test-pine-2"):
			self.init_pine(pine_name, skip_assets=True)

		self.assert_common_site_config(
			"test-pine-1",
			{
				"webserver_port": 8000,
				"socketio_port": 9000,
				"file_watcher_port": 6787,
				"redis_queue": "redis://localhost:11000",
				"redis_socketio": "redis://localhost:12000",
				"redis_cache": "redis://localhost:13000",
			},
		)

		self.assert_common_site_config(
			"test-pine-2",
			{
				"webserver_port": 8001,
				"socketio_port": 9001,
				"file_watcher_port": 6788,
				"redis_queue": "redis://localhost:11001",
				"redis_socketio": "redis://localhost:12001",
				"redis_cache": "redis://localhost:13001",
			},
		)

	def test_new_site(self):
		pine_name = "test-pine"
		site_name = "test-site.local"
		pine_path = os.path.join(self.pines_path, pine_name)
		site_path = os.path.join(pine_path, "sites", site_name)
		site_config_path = os.path.join(site_path, "site_config.json")

		self.init_pine(pine_name)
		self.new_site(site_name, pine_name)

		self.assertTrue(os.path.exists(site_path))
		self.assertTrue(os.path.exists(os.path.join(site_path, "private", "backups")))
		self.assertTrue(os.path.exists(os.path.join(site_path, "private", "files")))
		self.assertTrue(os.path.exists(os.path.join(site_path, "public", "files")))
		self.assertTrue(os.path.exists(site_config_path))

		with open(site_config_path) as f:
			site_config = json.loads(f.read())

			for key in ("db_name", "db_password"):
				self.assertTrue(key in site_config)
				self.assertTrue(site_config[key])

	def test_get_app(self):
		self.init_pine("test-pine", skip_assets=True)
		pine_path = os.path.join(self.pines_path, "test-pine")
		exec_cmd(f"pine get-app {TEST_MELON_APP} --skip-assets", cwd=pine_path)
		self.assertTrue(os.path.exists(os.path.join(pine_path, "apps", TEST_MELON_APP)))
		app_installed_in_env = TEST_MELON_APP in subprocess.check_output(
			["pine", "pip", "freeze"], cwd=pine_path
		).decode("utf8")
		self.assertTrue(app_installed_in_env)

	@unittest.skipIf(MELON_BRANCH != "develop", "only for develop branch")
	def test_get_app_resolve_deps(self):
		MELON_APP = "healthcare"
		self.init_pine("test-pine", skip_assets=True)
		pine_path = os.path.join(self.pines_path, "test-pine")
		exec_cmd(f"pine get-app {MELON_APP} --resolve-deps --skip-assets", cwd=pine_path)
		self.assertTrue(os.path.exists(os.path.join(pine_path, "apps", MELON_APP)))

		states_path = os.path.join(pine_path, "sites", "apps.json")
		self.assertTrue(os.path.exists(states_path))

		with open(states_path) as f:
			states = json.load(f)

		self.assertTrue(MELON_APP in states)

	def test_install_app(self):
		pine_name = "test-pine"
		site_name = "install-app.test"
		pine_path = os.path.join(self.pines_path, "test-pine")

		self.init_pine(pine_name, skip_assets=True)
		exec_cmd(
			f"pine get-app {TEST_MELON_APP} --branch master --skip-assets", cwd=pine_path
		)

		self.assertTrue(os.path.exists(os.path.join(pine_path, "apps", TEST_MELON_APP)))

		# check if app is installed
		app_installed_in_env = TEST_MELON_APP in subprocess.check_output(
			["pine", "pip", "freeze"], cwd=pine_path
		).decode("utf8")
		self.assertTrue(app_installed_in_env)

		# create and install app on site
		self.new_site(site_name, pine_name)
		installed_app = not exec_cmd(
			f"pine --site {site_name} install-app {TEST_MELON_APP}",
			cwd=pine_path,
			_raise=False,
		)

		if installed_app:
			app_installed_on_site = subprocess.check_output(
				["pine", "--site", site_name, "list-apps"], cwd=pine_path
			).decode("utf8")
			self.assertTrue(TEST_MELON_APP in app_installed_on_site)

	def test_remove_app(self):
		self.init_pine("test-pine", skip_assets=True)
		pine_path = os.path.join(self.pines_path, "test-pine")

		exec_cmd(
			f"pine get-app {TEST_MELON_APP} --branch master --overwrite --skip-assets",
			cwd=pine_path,
		)
		exec_cmd(f"pine remove-app {TEST_MELON_APP}", cwd=pine_path)

		with open(os.path.join(pine_path, "sites", "apps.txt")) as f:
			self.assertFalse(TEST_MELON_APP in f.read())
		self.assertFalse(
			TEST_MELON_APP
			in subprocess.check_output(["pine", "pip", "freeze"], cwd=pine_path).decode("utf8")
		)
		self.assertFalse(os.path.exists(os.path.join(pine_path, "apps", TEST_MELON_APP)))

	def test_switch_to_branch(self):
		self.init_pine("test-pine", skip_assets=True)
		pine_path = os.path.join(self.pines_path, "test-pine")
		app_path = os.path.join(pine_path, "apps", "melon")

		# * chore: change to 14 when avalible
		prevoius_branch = "version-6"
		if MELON_BRANCH != "develop":
			# assuming we follow `version-#`
			prevoius_branch = f"version-{int(MELON_BRANCH.split('-')[1]) - 1}"

		successful_switch = not exec_cmd(
			f"pine switch-to-branch {prevoius_branch} melon --upgrade",
			cwd=pine_path,
			_raise=False,
		)
		if successful_switch:
			app_branch_after_switch = str(git.Repo(path=app_path).active_branch)
			self.assertEqual(prevoius_branch, app_branch_after_switch)

		successful_switch = not exec_cmd(
			f"pine switch-to-branch {MELON_BRANCH} melon --upgrade",
			cwd=pine_path,
			_raise=False,
		)
		if successful_switch:
			app_branch_after_second_switch = str(git.Repo(path=app_path).active_branch)
			self.assertEqual(MELON_BRANCH, app_branch_after_second_switch)


if __name__ == "__main__":
	unittest.main()
