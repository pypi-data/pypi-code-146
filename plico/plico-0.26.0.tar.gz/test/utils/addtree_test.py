#!/usr/bin/env python
import unittest
import tempfile
import shutil
import os
from plico.utils.addtree import addtree

__version__ = "$Id: addtree_test.py 26 2018-01-26 19:06:25Z lbusoni $"


class Test(unittest.TestCase):


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
        self._createFile(os.path.join(self._fooDir, 'foo2.txt'), "foo2")
        self._booDir= os.path.join(self._srcDir, 'boo')
        os.makedirs(self._booDir)
        self._createFile(os.path.join(self._booDir, 'boo1.txt'), "boo1")


    def _createFile(self, filename, text):
        with open(filename, "w") as out:
            out.write(text)


    def tearDown(self):
        print(self._listSrcDir())
        print(self._listDestDir())
        shutil.rmtree(self._srcDir)
        shutil.rmtree(self._destDir)


    def testHappyPath(self):
        addtree(self._srcDir, self._destDir)
        self._checkAllCopied()


    def _checkAllCopied(self):
        self._checkDestDir('foo')
        self._checkDestDir('boo')
        self._checkDestFile(os.path.join('boo', 'boo1.txt'))
        self._checkDestFile(os.path.join('foo', 'foo1.txt'))
        self._checkDestFile(os.path.join('foo', 'foo2.txt'))
        self._checkDestFile('root1.txt')


    def testCopyOnEmptyDestAndCopyAgain(self):
        addtree(self._srcDir, self._destDir)
        addtree(self._srcDir, self._destDir)
        self._checkAllCopied()


    def testNewlyAddedFilesAreNotRemovedWhenCopying(self):
        addtree(self._srcDir, self._destDir)

        self._createFile(os.path.join(self._destDir, 'root2.txt'), "root2")
        newdir= os.path.join(self._destDir, 'new')
        os.makedirs(newdir)
        self._createFile(os.path.join(newdir, 'new1.txt'), "new1")

        addtree(self._srcDir, self._destDir)
        self._checkAllCopied()
        self._checkNewOnesAreStillThere()


    def testModifiedFilesAreNotOverwrittenWhenCopying(self):
        addtree(self._srcDir, self._destDir)

        fileToModify= os.path.join(self._srcDir, 'root1.txt')
        self._modifyText(fileToModify, "new text for root1")

        addtree(self._srcDir, self._destDir)
        self._checkAllCopied()
        self.assertEqual("new text for root1",
                         self._readFile(fileToModify))


    def _readFile(self, filePath):
        with open(filePath) as file:
            data = file.read()
        return data

    def _modifyText(self, file, newText):
        os.remove(file)
        self._createFile(file, newText)


    def _checkNewOnesAreStillThere(self):
        self._checkDestFile('root2.txt')
        self._checkDestDir('new')
        self._checkDestFile(os.path.join('new', 'new1.txt'))


    def _checkDestDir(self, dirName):
        dirPath= os.path.join(self._destDir, dirName)
        self.assertTrue(os.path.isdir(dirPath),
                        "%s not found" % dirPath)


    def _checkDestFile(self, fileName):
        filePath= os.path.join(self._destDir, fileName)
        self.assertTrue(os.path.isfile(filePath),
                        "%s not found" % filePath)


    def _listSrcDir(self):
        return "src has: %s" % str([x for x in os.walk(self._srcDir)])


    def _listDestDir(self):
        return "dest has: %s" % str([x for x in os.walk(self._destDir)])


if __name__ == "__main__":
    unittest.main()
