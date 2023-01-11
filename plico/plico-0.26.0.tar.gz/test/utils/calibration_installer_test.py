#!/usr/bin/env python
import unittest
from plico.utils.calibration_installer import CalibrationInstaller
import tempfile
import os
import shutil

__version__ = "$Id: calibration_installer_test.py 26 2018-01-26 19:06:25Z lbusoni $"


class CalibrationInstallerTest(unittest.TestCase):


    def setUp(self):
        self._srcDir= tempfile.mkdtemp()
        self._destDir= tempfile.mkdtemp()
        print('src dir %s' % self._srcDir)
        print('dest dir %s' % self._destDir)
        self._createSourceFolder()


    def _createSourceFolder(self):
        self._createFile(os.path.join(self._srcDir, 'root1.txt'), "root1")
        self._fooDir= os.path.join(self._srcDir, 'foo')
        os.makedirs(self._fooDir)
        self._createFile(os.path.join(self._fooDir, 'foo1.txt'), "foo1")


    def _createFile(self, filename, text):
        with open(filename, "w") as out:
            out.write(text)


    def tearDown(self):
        shutil.rmtree(self._srcDir)
        shutil.rmtree(self._destDir)



    def testHappyPathWithForcedSrcAndDest(self):
        appDirs= None
        packageName= 'whatever'
        calibInstaller= CalibrationInstaller(
            appDirs,
            packageName,
            src=self._srcDir,
            dest=os.path.join(self._destDir, 'copyhere'))
        self.assertFalse(calibInstaller.doesCalibrationFolderExists())
        calibInstaller.installCalibrationFilesFromPackage()
        self.assertTrue(calibInstaller.doesCalibrationFolderExists())



if __name__ == "__main__":
    unittest.main()
