import unittest
from InCli import InCli
from InCli.SFAPI import file

class Test_File(unittest.TestCase):
    def test_main(self):
        filename = "testFile"
        j1 = "This is a sentence."
        j1n = "This is a sentence.\n"

        filepath = file.write(filename,j1)

        j2 = file.read(filename)
        self.assertTrue(j1==j2)

        j3 = file.read(filepath)
        self.assertTrue(j1==j3)

        file.delete(filename)

        self.assertTrue(file.exists(filename)==False)

        f = file.openFile(filename)
        file.write_line(f,j1)
        file.closeFile(f)

        j4 = file.read(filename)
        self.assertTrue(j1n==j4)

        print()

        
