import os
import shutil
import subprocess
import unittest

from pine.app import App
from pine.pine import Pine
from pine.exceptions import InvalidRemoteException
from pine.utils import is_valid_melon_branch


class TestUtils(unittest.TestCase):
	def test_app_utils(self):
		git_url = "https://github.com/amonak/melon"
		branch = "develop"
		app = App(name=git_url, branch=branch, pine=Pine("."))
		self.assertTrue(
			all(
				[
					app.name == git_url,
					app.branch == branch,
					app.tag == branch,
					app.is_url is True,
					app.on_disk is False,
					app.org == "melon",
					app.url == git_url,
				]
			)
		)

	def test_is_valid_melon_branch(self):
		with self.assertRaises(InvalidRemoteException):
			is_valid_melon_branch(
				"https://github.com/amonak/melon.git", melon_branch="random-branch"
			)
			is_valid_melon_branch(
				"https://github.com/random/random.git", melon_branch="random-branch"
			)

		is_valid_melon_branch(
			"https://github.com/amonak/melon.git", melon_branch="develop"
		)
		is_valid_melon_branch(
			"https://github.com/amonak/melon.git", melon_branch="v6.29.0"
		)

	def test_app_states(self):
		pine_dir = "./sandbox"
		sites_dir = os.path.join(pine_dir, "sites")

		if not os.path.exists(sites_dir):
			os.makedirs(sites_dir)

		fake_pine = Pine(pine_dir)

		self.assertTrue(hasattr(fake_pine.apps, "states"))

		fake_pine.apps.states = {
			"melon": {
				"resolution": {"branch": "develop", "commit_hash": "234rwefd"},
				"version": "7.0.0-dev",
			}
		}
		fake_pine.apps.update_apps_states()

		self.assertEqual(fake_pine.apps.states, {})

		melon_path = os.path.join(pine_dir, "apps", "melon")

		os.makedirs(os.path.join(melon_path, "melon"))

		subprocess.run(["git", "init"], cwd=melon_path, capture_output=True, check=True)

		with open(os.path.join(melon_path, "melon", "__init__.py"), "w+") as f:
			f.write("__version__ = '4.0'")

		subprocess.run(["git", "add", "."], cwd=melon_path, capture_output=True, check=True)
		subprocess.run(
			["git", "config", "user.email", "pine-test_app_states@gha.com"],
			cwd=melon_path,
			capture_output=True,
			check=True,
		)
		subprocess.run(
			["git", "config", "user.name", "App States Test"],
			cwd=melon_path,
			capture_output=True,
			check=True,
		)
		subprocess.run(
			["git", "commit", "-m", "temp"], cwd=melon_path, capture_output=True, check=True
		)

		fake_pine.apps.update_apps_states(app_name="melon")

		self.assertIn("melon", fake_pine.apps.states)
		self.assertIn("version", fake_pine.apps.states["melon"])
		self.assertEqual("4.0", fake_pine.apps.states["melon"]["version"])

		shutil.rmtree(pine_dir)

	def test_ssh_ports(self):
		app = App("git@github.com:22:melon/melon")
		self.assertEqual((app.use_ssh, app.org, app.repo), (True, "melon", "melon"))
