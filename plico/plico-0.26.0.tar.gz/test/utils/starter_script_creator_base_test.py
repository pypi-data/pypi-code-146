#!/usr/bin/env python
import unittest
import os
from plico.utils.starter_script_creator_base import StarterScriptCreatorBase
import shutil

TEST_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        "./tmp/")


class MyStarterScriptCreator(StarterScriptCreatorBase):

    def __init__(self):
        StarterScriptCreatorBase.__init__(self)
        self.destination_path = os.path.join(
            TEST_DIR, 'destination', 'path')
        self.executable = os.path.join('executable', 'module.py')
        self.config_section = 'my_config_section'

    def installExecutables(self):
        self._createAStarterScript(
            self.destination_path,
            self.executable,
            self.config_section
        )


class StarterScriptCreatorBaseTest(unittest.TestCase):

    LOG_DIR = os.path.join(TEST_DIR, "log")
    CONF_FILE = os.path.join("path", "to", "config", "file.conf")
    BIN_DIR = os.path.join(TEST_DIR, "apps", "bin")
    SOURCE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              "../..")

    def setUp(self):
        self.ssc = MyStarterScriptCreator()
        self.ssc.setInstallationBinDir(self.BIN_DIR)
        self.ssc.setPythonPath(self.SOURCE_DIR)
        self.ssc.setConfigFileDestination(self.CONF_FILE)
        self.ssc.installExecutables()

    def tearDown(self):
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)

    def _is_file(self, path):
        import sys
        if sys.version_info.major == 2:
            import os.path
            return os.path.isfile(path)
        elif sys.version_info.major == 3:
            import pathlib
            return pathlib.Path(path).resolve().is_file()
        else:
            raise Exception("unknown python version")

    def test_create_script(self):

        want_file_in = self.ssc.destination_path
        self.assertTrue(self._is_file(want_file_in))


if __name__ == "__main__":
    unittest.main()
