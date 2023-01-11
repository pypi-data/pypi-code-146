import unittest
import os
import csv
from pathlib import Path
from pyPhases.util.CSVLogger import CSVLogger

from shutil import rmtree


class TestCSVLogger(unittest.TestCase):
    def setUp(self):
        self.csvPath = "tests/data/test.csv"
        self.logger = CSVLogger(self.csvPath)

    def tearDown(self):
        if Path(self.csvPath).exists():
            Path(self.csvPath).unlink()

    def test_cleanCsv(self):
        # Make sure the file doesn't already exist
        rmtree(self.csvPath, ignore_errors=True)

        self.assertFalse(Path(self.csvPath).exists())

        # Create the file
        with open(self.csvPath, "w+", newline=""):
            pass

        self.assertTrue(Path(self.csvPath).exists())

        # Test the cleanCsv method
        self.logger.cleanCsv()
        self.assertFalse(Path(self.csvPath).exists())

    def test_addCsvRow(self):
        self.logger.cleanCsv()

        row = {"col1": "val1", "col2": "val2"}
        self.logger.addCsvRow(row)

        # Check that the file was created
        self.assertTrue(Path(self.csvPath).exists())

        # Check that the row was added to the file
        with open(self.csvPath, "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [row for row in reader]
            self.assertEqual(len(rows), 1)
            self.assertDictEqual(rows[0], row)

        # Add another row and check that it was added
        row2 = {"col1": "val3", "col2": "val4"}
        self.logger.addCsvRow(row2)
        with open(self.csvPath, "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [row for row in reader]
            self.assertEqual(len(rows), 2)
            self.assertDictEqual(rows[1], row2)

    def test_addCsvRow_createparent(self):
        # remove tests/data/
        rmtree("tests/data", ignore_errors=True)

        # shoud create parent folder
        row = {"col1": "val1", "col2": "val2"}
        self.logger.addCsvRow(row)
        self.assertTrue(Path(self.csvPath).exists())

    def test_getRowsAsDict(self):
        self.logger.cleanCsv()

        row = {"col1": "val1", "col2": "val2"}
        self.logger.addCsvRow(row)

        rows = self.logger.getRowsAsDict()
        self.assertEqual(len(rows), 1)
        self.assertDictEqual(rows[0], row)

        # Add another row and check that it was added
        row2 = {"col1": "val3", "col2": "val4"}
        self.logger.addCsvRow(row2)
        rows = self.logger.getRowsAsDict()
        self.assertEqual(len(rows), 2)
        self.assertDictEqual(rows[1], row2)

    def test_getRowsAsList(self):
        self.logger.cleanCsv()

        row = {"col1": "val1", "col2": "val2"}
        self.logger.addCsvRow(row)

        rows = self.logger.getRowsAsList()
        self.assertEqual(len(rows), 1)
        self.assertListEqual(rows[0], list(row.values()))

        # Add another row and check that it was added
        row2 = {"col1": "val3", "col2": "val4"}
        self.logger.addCsvRow(row2)
        rows = self.logger.getRowsAsList()
        self.assertEqual(len(rows), 2)
        self.assertListEqual(rows[0], list(row.values()))
        self.assertListEqual(rows[1], list(row2.values()))

    def test_getRows_empty(self):
        rows = self.logger.getRowsAsList()
        self.assertEqual(len(rows), 0)
        self.assertEqual(rows, [])
