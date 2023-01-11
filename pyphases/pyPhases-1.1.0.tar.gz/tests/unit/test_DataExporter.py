from unittest import TestCase
from unittest.mock import patch

from pyPhases.exporter.DataExporter import DataExporter


class TestpyDataExporter(TestCase):

    def test_initialOption(self):
        exporter = DataExporter()
        self.assertEqual(exporter.getOption("basePath"), "./data")

    def test_notimplemented(self):
        exporter = DataExporter()
        self.assertRaises(Exception, exporter.stream, None)

    def test_reinit(self):
        exporter = DataExporter({"foo": "bar"})

        exporter2 = exporter.reinit()
        self.assertNotEqual(exporter, exporter2)
        self.assertIsInstance(exporter2, DataExporter)
        self.assertEqual(exporter.options, exporter2.options)

    def test_defaultMethods(self):
        exporter = DataExporter()
        exporter.read("path", {})
        exporter.write("path", "data", {})
        self.assertEqual(exporter.checkType(str), False)
        exporter.finishStream("dataid")

    def test_getPath(self):
        exporter = DataExporter()
        self.assertEqual(exporter.getPath("path"), "data/path")

    def test_exists(self):
        exporter = DataExporter()
        with patch("pathlib.Path.exists") as existsMock:
            existsMock.return_value = True
            self.assertEqual(exporter.exists("path"), True)

    def test_delete(self):
        exporter = DataExporter()
        with patch("pathlib.Path.unlink") as existsMock:
            existsMock.return_value = True
            self.assertEqual(exporter.delete("path"), True)
